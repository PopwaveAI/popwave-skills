#!/usr/bin/env python3
"""
Crawl a Chinese web novel chapter-by-chapter from a book page.

Strategy:
  1. Load the chapter list page.
  2. Find all chapter links (various CSS selectors for common CN novel sites).
  3. Optionally try to find a "全本TXT下载" (full-book download) link first.
  4. Visit each chapter page, extract the visible text content.
  5. Assemble into a single UTF-8 TXT file with chapter headings.

Usage:
  python crawl_novel.py --list-url <URL> --title "书名"
  python crawl_novel.py --list-url <URL> --title "书名" --workers 16
  python crawl_novel.py --list-url <URL> --title "书名" --limit 50
  python crawl_novel.py --list-url <URL> --title "书名" --chapter-selector "#content" --delay 1.5
  python crawl_novel.py --list-url <URL> --title "书名" --resume  # 断点续爬
"""

from __future__ import annotations

import argparse
import os
import random
import re
import sys
import threading
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ── Default CSS selectors tried in order for chapter links on the list page ──
CHAPTER_LINK_SELECTORS = [
    "ul.chapter-list a",
    "div.list-chapters a",
    "div#list-chapter-all a",
    "div#list a",
    "div.chapterlist a",
    "div.book-list a",
    "dd a",
    "li a",
    "a[href*='chapter']",
    "a[href*='read']",
    "a[href$='.html']",
]

# ── Content extraction selectors (tried in order) ──
CONTENT_SELECTORS = [
    "div#content",
    "div.content",
    "div#chaptercontent",
    "div.book_content_text",
    "div#nr1",
    "div#booktxt",
    "div.txtnav",
    "article",
    "div.read-content",
    "div.showtxt",
    "div.novel-content",
    "div#TextContent",
]

# ── Anti-crawl User-Agent rotation pool ──
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

# ── Anti-spider content markers (skip pages that look like anti-crawl) ──
ANTI_SPIDER_MARKERS = [
    "验证码",
    "请输入验证码",
    "captcha",
    "人机验证",
    "安全验证",
    "请开启JavaScript",
    "您的请求过于频繁",
]

# ── Non-chapter navigation labels to skip when collecting chapter links ──
NAV_LABELS = (
    "开始阅读", "下一页", "上一页", "下页", "上页", "尾页", "首页", "末页",
    "返回书页", "查看全部", "全部章节", "章节目录", "全文阅读", "最新章节",
    "txt下载", "加入书架", "书签", "上一章", "下一章", "back", "next",
    "小说简介", "内容简介", "作品相关", "作品信息", "作者的话", "作者前言",
    "公告", "敬告读者", "本书相关", "书籍简介",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Crawl a Chinese web novel chapter-by-chapter into a UTF-8 TXT file."
    )
    parser.add_argument("--list-url", required=True, help="URL of the chapter list page.")
    parser.add_argument("--title", required=True, help="Book title for output filename.")
    parser.add_argument(
        "--output-dir",
        default=r"D:\popwave-skills\downloads",
        help="Output directory for the assembled TXT.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max chapters to crawl (0 = all). Use for testing with a few chapters.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Min delay in seconds between chapter requests (default 1.0).",
    )
    parser.add_argument(
        "--chapter-selector",
        default=None,
        help="Override CSS selector for chapter links on list page.",
    )
    parser.add_argument(
        "--content-selector",
        default=None,
        help="Override CSS selector for chapter text content.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Override base URL for resolving relative chapter links.",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        default=False,
        help="Reverse chapter order (some sites list latest first).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=10,
        help="Concurrent download threads (default 10). Set 1 for serial mode.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        default=False,
        help="Resume: skip chapters already present in the output file and append new ones.",
    )
    return parser.parse_args()


def safe_filename(title: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", title).strip(" ._")
    return name or "crawled-novel"


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        # Only advertise encodings urllib3 can decode. Declaring `br` without
        # the optional `brotli` package installed makes the server return
        # Brotli-compressed bytes that requests cannot decompress, turning
        # resp.text into silent garbage (mojibake) — BeautifulSoup then finds
        # zero chapter links and the crawl fails with "无法从页面提取章节链接".
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    })
    return session


def rotate_ua(session: requests.Session) -> None:
    session.headers["User-Agent"] = random.choice(USER_AGENTS)


# ── Thread-local session pool — each worker thread gets its own connection pool ──
_thread_local = threading.local()


def get_thread_session() -> requests.Session:
    """Return a thread-local requests.Session (one per worker thread)."""
    if not hasattr(_thread_local, "session"):
        _thread_local.session = make_session()
    return _thread_local.session


def fetch_page(session: requests.Session, url: str, timeout: int = 30) -> str | None:
    """Fetch a page, return None on failure."""
    rotate_ua(session)
    try:
        resp = session.get(url, timeout=timeout)
        resp.raise_for_status()
        # Prefer chardet-detected encoding for CJK pages — the server-declared
        # charset is sometimes wrong (e.g. declares utf-8 while serving GBK).
        detected = resp.apparent_encoding
        if detected and detected.lower() != "ascii":
            resp.encoding = detected
        text = resp.text
        # Detect silent decompression/decoding failure. A page full of U+FFFD
        # replacement characters means the response body was not decoded
        # correctly (classic symptom: advertised `br` but no brotli decoder).
        # Surfacing this explicitly beats returning mojibake that downstream
        # reports as a misleading "无法从页面提取章节链接".
        replacement_count = text.count("\ufffd")
        if replacement_count > 50:
            ce = resp.headers.get("Content-Encoding", "none")
            print(
                f"WARN: 响应内容疑似乱码（{replacement_count} 个替换字符，"
                f"Content-Encoding={ce}），可能声明了不支持的压缩编码。URL: {url}",
                file=sys.stderr,
            )
            return None
        # Check for anti-spider pages
        for marker in ANTI_SPIDER_MARKERS:
            if marker in text[:2000]:
                print(f"WARN: 可能触发反爬（'{marker}'），URL: {url}", file=sys.stderr)
                return None
        return text
    except requests.RequestException as exc:
        print(f"WARN: 请求失败 {url}: {exc}", file=sys.stderr)
        return None


def extract_chapter_links(
    html: str, base_url: str, selector_override: str | None = None
) -> list[dict]:
    """Parse the chapter list page and return [(title, url), ...]."""
    soup = BeautifulSoup(html, "lxml")
    selectors = [selector_override] if selector_override else CHAPTER_LINK_SELECTORS
    seen = set()
    links: list[dict] = []

    for selector in selectors:
        if not selector:
            continue
        elements = soup.select(selector)
        if elements:
            for el in elements:
                href = el.get("href", "").strip()
                text = el.get_text(strip=True)
                if not href or not text:
                    continue
                # Skip non-chapter links
                if len(text) < 2 or len(text) > 60:
                    continue
                # Skip navigation labels (下一页/尾页/开始阅读/…)
                if any(nav in text.lower() for nav in NAV_LABELS):
                    continue
                # Resolve relative URLs
                full_url = urllib.parse.urljoin(base_url, href)
                if full_url not in seen:
                    seen.add(full_url)
                    links.append({"title": text.strip(), "url": full_url})
            if links:
                print(f"INFO: 使用选择器 '{selector}' 找到了 {len(links)} 个章节链接", file=sys.stderr)
                break

    return links


def _clean_chapter_text(text: str) -> str:
    """Normalize whitespace and strip stray-punctuation lead lines.

    Some chapter pages leave a lone punctuation mark (e.g. '、') as the first
    line after nav buttons like 展开/收起 are stripped — remove such a leading
    line so the chapter opens cleanly with real prose.
    """
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    lines = text.split("\n")
    # Drop a leading line that contains no letter/digit/CJK char (pure
    # punctuation/whitespace artifact), at most once.
    if lines and not re.search(r"[\u4e00-\u9fffa-zA-Z0-9]", lines[0]):
        lines.pop(0)
    return "\n".join(lines).strip()


def _strip_page_suffix(path: str) -> str:
    """Strip trailing _N / /N / _N.html suffix for intra-chapter prefix matching."""
    path = re.sub(r"_\d+\.html?$", "", path)
    path = re.sub(r"\.html?$", "", path)
    path = re.sub(r"/\d+/?$", "", path)
    return path


def find_chapter_next_page(html: str, base_url: str, chapter_url: str) -> str | None:
    """Find an intra-chapter 'next page' link, NOT a 'next chapter' link.

    Many novel sites split one chapter across multiple pages. Without this
    function the crawler only grabs page 1 and silently drops the rest.
    """
    soup = BeautifulSoup(html, "lxml")
    next_labels = ("下一页", "下页", "下一頁", "next", "nextpage")
    current_path = urllib.parse.urlparse(chapter_url).path.rstrip("/")
    current_prefix = _strip_page_suffix(current_path)

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a.get("href", "").strip()
        if not href or href.startswith(("javascript:", "#")):
            continue
        if "章" in text:
            continue
        text_lower = text.lower()
        if not any(label in text_lower for label in next_labels):
            continue
        full_url = urllib.parse.urljoin(base_url, href)
        if full_url == chapter_url:
            continue
        next_path = urllib.parse.urlparse(full_url).path.rstrip("/")
        next_prefix = _strip_page_suffix(next_path)
        if next_prefix and next_prefix == current_prefix:
            return full_url
        if next_path.startswith(current_path) or current_path.startswith(next_prefix):
            return full_url
    return None


def fetch_chapter_content(
    session: requests.Session, url: str, selector_override: str | None,
    timeout: int, max_pages: int = 50,
) -> str:
    """Fetch a chapter, following intra-chapter pagination, return full text."""
    parts: list[str] = []
    current_url = url
    seen: set[str] = {url}
    pages = 0

    while current_url and pages < max_pages:
        html = fetch_page(session, current_url, timeout)
        if not html:
            break
        text = extract_chapter_content(html, selector_override)
        if text:
            parts.append(text)
        pages += 1

        next_url = find_chapter_next_page(html, current_url, current_url)
        if not next_url or next_url in seen:
            break
        seen.add(next_url)
        current_url = next_url
        time.sleep(0.3)

    if pages > 1:
        print(f"INFO: 章节分页，共抓取 {pages} 页", file=sys.stderr)
    return "\n\n".join(parts) if parts else ""


def extract_chapter_content(html: str, selector_override: str | None = None) -> str:
    """Extract the visible text content from a chapter page."""
    soup = BeautifulSoup(html, "lxml")
    selectors = [selector_override] if selector_override else CONTENT_SELECTORS

    for selector in selectors:
        if not selector:
            continue
        elements = soup.select(selector)
        if elements:
            # Take the largest content element (by text length)
            best = max(elements, key=lambda e: len(e.get_text(strip=True)))
            text = best.get_text("\n", strip=True)
            if len(text) > 100:  # Must have meaningful text
                return _clean_chapter_text(text)

    # Fallback: just get all visible text from body
    body = soup.find("body")
    if body:
        text = body.get_text("\n", strip=True)
        if len(text) > 200:
            print("WARN: 未找到已知内容选择器，使用 body 全文提取", file=sys.stderr)
            return _clean_chapter_text(text)

    return ""


def _is_direct_file_url(href: str) -> bool:
    """Heuristic: does this URL point at a downloadable file, not a page?"""
    path = href.lower().split("?")[0].split("#")[0]
    return path.endswith((".txt", ".zip", ".epub", ".rar", ".azw3"))


def check_for_full_download(session: requests.Session, list_html: str, base_url: str) -> str | None:
    """Check if the list page has a *real* full-book direct download link.

    Only returns links that point at an actual file (.txt/.zip/...). A link
    labelled "txt下载" but ending in .html is an intermediate download portal
    (often JS-gated) that download_text.py cannot consume — those are skipped
    so the caller falls back to chapter-by-chapter crawling instead of dying
    on a HTML download page.
    """
    soup = BeautifulSoup(list_html, "lxml")
    download_keywords = ["txt下载", "全本下载", "全集下载", "下载txt", "全文下载", "本地下載"]

    page_candidates: list[tuple[str, str]] = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "").strip()
        text = a_tag.get_text(strip=True)
        if not href or href.startswith(("javascript:", "#")):
            continue
        full_url = urllib.parse.urljoin(base_url, href)
        # Real direct file link — trust it immediately.
        if _is_direct_file_url(href):
            print(f"INFO: 发现直链下载: {full_url} (『{text}』)", file=sys.stderr)
            return full_url
        # "txt下载" label on a page URL — record but do NOT return; these are
        # usually JS-gated download portals, not real file URLs.
        for kw in download_keywords:
            if kw in text.lower() or kw in href.lower():
                page_candidates.append((text, full_url))
                break

    if page_candidates:
        text, url = page_candidates[0]
        print(
            f"WARN: 发现『{text}』-> {url}，但链接是页面而非直链"
            f"（多为 JS 下载入口），跳过，改用逐章爬取",
            file=sys.stderr,
        )
    return None


def find_next_page(html: str, base_url: str) -> str | None:
    """Find a 'next page' link on a paginated chapter list."""
    soup = BeautifulSoup(html, "lxml")
    next_labels = ("下一页", "下页", "下一頁", "next")
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True).lower()
        href = a.get("href", "").strip()
        if not href or href.startswith(("javascript:", "#")):
            continue
        if text in next_labels:
            return urllib.parse.urljoin(base_url, href)
    return None


def collect_chapter_links(
    session: requests.Session,
    first_html: str,
    list_url: str,
    base_url: str,
    selector: str | None,
    limit: int,
    timeout: int,
    max_pages: int = 30,
) -> tuple[list[dict], int]:
    """Collect chapter links, following pagination across list pages.

    Returns (links, pages_fetched). Reuses first_html for page 1 to avoid a
    duplicate request, then follows "下一页" links until exhausted.
    """
    all_links: list[dict] = []
    seen: set[str] = set()
    pages = 0
    current_html: str | None = first_html
    current_url = list_url
    while current_html and pages < max_pages:
        pages += 1
        page_links = extract_chapter_links(current_html, current_url, selector)
        added = 0
        for link in page_links:
            if link["url"] not in seen:
                seen.add(link["url"])
                all_links.append(link)
                added += 1
        if limit > 0 and len(all_links) >= limit:
            return all_links[:limit], pages
        # No new links on a non-first page → pagination exhausted / dead end.
        if added == 0 and pages > 1:
            break
        next_url = find_next_page(current_html, current_url)
        if not next_url or next_url == current_url:
            break
        current_url = next_url
        time.sleep(0.5)  # be gentle between list pages
        current_html = fetch_page(session, current_url, timeout)
    return all_links, pages


def crawl_novel(args: argparse.Namespace) -> int:
    """Main crawl logic. Returns 0 on success, 1+ on failure."""
    session = make_session()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Step 1: Fetch chapter list page ──
    print(f"INFO: 正在获取章节列表页: {args.list_url}", file=sys.stderr)
    list_html = fetch_page(session, args.list_url, args.timeout)
    if not list_html:
        print("ERROR: 无法获取章节列表页", file=sys.stderr)
        return 1

    base_url = args.base_url or args.list_url

    # ── Step 2: Check for "全本TXT下载" (full download) link ──
    download_url = check_for_full_download(session, list_html, base_url)
    if download_url:
        print(f"FULL_DOWNLOAD={download_url}")
        return 0  # Signal to caller: use download_text.py instead

    # ── Step 3: Extract chapter links (with pagination) ──
    links, pages = collect_chapter_links(
        session, list_html, args.list_url, base_url,
        args.chapter_selector, args.limit, args.timeout,
    )
    if not links:
        print("ERROR: 无法从页面提取章节链接", file=sys.stderr)
        return 1

    if pages > 1:
        print(f"INFO: 列表分页，共抓取 {pages} 页", file=sys.stderr)

    if args.reverse:
        links.reverse()

    # limit already applied inside collect_chapter_links, but keep for safety
    if args.limit > 0:
        links = links[:args.limit]

    print(f"INFO: 共发现 {len(links)} 个章节，开始爬取…", file=sys.stderr)

    # ── Step 4: Crawl each chapter (concurrent or serial) ──
    output_path = output_dir / f"{safe_filename(args.title)}.txt"

    # Resume: detect already-downloaded chapters by title
    done_titles: set[str] = set()
    existing_count = 0
    if args.resume and output_path.exists():
        try:
            old = output_path.read_text(encoding="utf-8")
            for m in re.finditer(r"^# (.+)$", old, flags=re.M):
                done_titles.add(m.group(1).strip())
            existing_count = len(done_titles)
            if done_titles:
                print(f"INFO: 断点续爬 — 已有 {existing_count} 章，将跳过", file=sys.stderr)
        except Exception:
            pass

    # Filter out already-downloaded chapters
    todo = [(i, link) for i, link in enumerate(links, 1) if link["title"].strip() not in done_titles]
    skipped = len(links) - len(todo)
    if skipped:
        print(f"INFO: 跳过已下载 {skipped} 章，剩余 {len(todo)} 章", file=sys.stderr)

    results: dict[int, str | None] = {}  # 1-based index -> content (None = failed)
    failed = 0
    crawled = 0

    def _fetch_one(idx_link):
        """Worker: fetch & extract one chapter. Returns (index, content_or_None, title)."""
        i, link = idx_link
        sess = get_thread_session()
        content = fetch_chapter_content(sess, link["url"], args.content_selector, args.timeout)
        return (i, content, link["title"])

    if args.workers > 1 and len(todo) > 1:
        print(f"INFO: 并发爬取 — {args.workers} 线程，{len(todo)} 章", file=sys.stderr)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(_fetch_one, item): item[0] for item in todo}
            done_count = 0
            for fut in as_completed(futures):
                i, content, title = fut.result()
                results[i] = content
                done_count += 1
                if content:
                    crawled += 1
                else:
                    failed += 1
                if done_count % 50 == 0 or done_count == len(todo):
                    print(f"INFO: 进度 {done_count}/{len(todo)} (成功 {crawled}, 失败 {failed})", file=sys.stderr)
    else:
        print(f"INFO: 串行爬取 — {len(todo)} 章", file=sys.stderr)
        for i, link in todo:
            print(f"INFO: [{i}/{len(links)}] {link['title']}", file=sys.stderr)
            content = fetch_chapter_content(session, link["url"], args.content_selector, args.timeout)
            if content:
                results[i] = content
                crawled += 1
            else:
                print(f"WARN: 未能提取章节内容: {link['title']}", file=sys.stderr)
                failed += 1
                results[i] = None
            if i < len(links):
                delay = args.delay + random.uniform(0, args.delay * 0.5)
                time.sleep(delay)

    # ── Step 5: Assemble and save (in original chapter order) ──
    if crawled == 0:
        print("ERROR: 未能成功爬取任何章节", file=sys.stderr)
        return 1

    new_chapters: list[str] = []
    for i, link in enumerate(links, 1):
        content = results.get(i)
        if content:
            new_chapters.append(f"# {link['title']}\n\n{content}")

    # Resume mode: append; otherwise overwrite
    write_mode = "a" if (args.resume and existing_count > 0) else "w"
    with open(output_path, write_mode, encoding="utf-8", newline="\n") as f:
        if write_mode == "a":
            f.write("\n\n")
        f.write("\n\n".join(new_chapters))

    file_size = output_path.stat().st_size
    preview_src = new_chapters[0] if new_chapters else ""
    preview = re.sub(r"\s+", " ", preview_src[:120]).strip()

    print(f"output={output_path}")
    print(f"encoding=utf-8")
    print(f"bytes={file_size}")
    print(f"chapters_crawled={crawled}")
    print(f"chapters_failed={failed}")
    print(f"chapters_skipped={skipped}")
    print(f"workers={args.workers}")
    print(f"preview={preview}")

    if failed > 0 and failed > crawled * 0.3:
        print(f"WARN: 失败率较高 ({failed}/{failed + crawled})，部分内容可能缺失", file=sys.stderr)
    return 0


def main() -> int:
    args = parse_args()
    return crawl_novel(args)


if __name__ == "__main__":
    raise SystemExit(main())
