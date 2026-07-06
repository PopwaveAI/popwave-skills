#!/usr/bin/env python3
"""Unified webnovel downloader: search → test → crawl → verify → deliver.

One command does everything:
  python download_novel.py "书名"
  python download_novel.py "书名" --workers 16
  python download_novel.py "书名" --source-url "URL"          # skip search
  python download_novel.py "书名" --source-url "URL" --direct  # direct TXT/ZIP

Replaces the old 3-step agent workflow (step-1-search → step-2-download →
step-3-verify) with a single script call.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import threading
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# ── Anti-crawl User-Agent rotation pool ──
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

# ── Anti-spider markers ──
ANTI_SPIDER_MARKERS = ["验证码", "请输入验证码", "captcha", "人机验证", "安全验证", "请开启JavaScript", "您的请求过于频繁"]

# ── Paywall markers (chapter content truncated) ──
PAYWALL_MARKERS = ["本章未完", "上QQ阅读APP", "登录订阅本章", "后续精彩内容", "本章想法", "打开APP阅读"]

# ── Non-chapter navigation labels ──
NAV_LABELS = (
    "开始阅读", "下一页", "上一页", "下页", "上页", "尾页", "首页", "末页",
    "返回书页", "查看全部", "全部章节", "章节目录", "全文阅读", "最新章节",
    "txt下载", "加入书架", "书签", "上一章", "下一章", "back", "next",
    "小说简介", "内容简介", "作品相关", "作品信息", "作者的话", "作者前言",
    "公告", "敬告读者", "本书相关", "书籍简介",
)

# ── Known source configurations (replaces sources.md + step-1-search.md) ──
# Each source: auto-search → find book → test chapter → crawl.
# Priority order: most reliable first.

@dataclass
class SourceConfig:
    name: str
    search_url: str          # URL template with {title} placeholder
    list_selectors: list[str] = field(default_factory=list)
    content_selectors: list[str] = field(default_factory=list)
    encoding: str | None = None  # None = auto-detect
    needs_pc: bool = False       # convert m.→www.
    book_url_pattern: str = ""   # regex to identify book page links in search results


SOURCES: list[SourceConfig] = [
    SourceConfig(
        name="boquku",
        search_url="",  # search disabled (404); use --source-url with book page URL
        list_selectors=["ul#chapters-list li a", "div#list a", "dd a"],
        content_selectors=["div#content", "div.content", "div#chaptercontent", "div.book_content_text", "div#nr1"],
        encoding=None,
        book_url_pattern=r"/book/\d+",
    ),
    SourceConfig(
        name="miaobige",
        search_url="https://www.miaobige.com/search.html?keyword={title}",
        list_selectors=["ul.chapter-list a", "div.list-chapters a", "dd a", "li a"],
        content_selectors=["div#content", "div.content", "div#chaptercontent", "div.book_content_text"],
        encoding=None,
        book_url_pattern=r"/shu/\d+",
    ),
    SourceConfig(
        name="ishubao",
        search_url="",  # site often times out; use --source-url if found via search
        list_selectors=["div.book-list a", "div#list a", "dd a"],
        content_selectors=["div.book_content_text", "div#content", "div#nr1"],
        encoding=None,
        needs_pc=True,
        book_url_pattern=r"/book/\d+",
    ),
]

# ── Fallback content selectors (tried in order when site-specific ones fail) ──
FALLBACK_CONTENT_SELECTORS = [
    "div#content", "div.content", "div#chaptercontent", "div.book_content_text",
    "div#nr1", "div#booktxt", "div.txtnav", "article", "div.read-content",
    "div.showtxt", "div.novel-content", "div#TextContent",
]

FALLBACK_LIST_SELECTORS = [
    "ul.chapter-list a", "div.list-chapters a", "div#list-chapter-all a",
    "div#list a", "div.chapterlist a", "div.book-list a", "dd a", "li a",
    "a[href*='chapter']", "a[href*='read']", "a[href$='.html']",
]


# ═══════════════════════════════════════════════════════════════════════════
# HTTP Session Management
# ═══════════════════════════════════════════════════════════════════════════

def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    })
    return session


_thread_local = threading.local()


def get_thread_session() -> requests.Session:
    if not hasattr(_thread_local, "session"):
        _thread_local.session = make_session()
    return _thread_local.session


def rotate_ua(session: requests.Session) -> None:
    session.headers["User-Agent"] = random.choice(USER_AGENTS)


def fetch_page(session: requests.Session, url: str, timeout: int = 30) -> str | None:
    """Fetch a page with encoding detection and anti-spider checks."""
    rotate_ua(session)
    try:
        resp = session.get(url, timeout=timeout)
        resp.raise_for_status()
        detected = resp.apparent_encoding
        if detected and detected.lower() != "ascii":
            resp.encoding = detected
        text = resp.text
        replacement_count = text.count("\ufffd")
        if replacement_count > 50:
            print(f"WARN: 响应疑似乱码（{replacement_count} 个替换字符），URL: {url}", file=sys.stderr)
            return None
        for marker in ANTI_SPIDER_MARKERS:
            if marker in text[:2000]:
                print(f"WARN: 可能触发反爬（'{marker}'），URL: {url}", file=sys.stderr)
                return None
        return text
    except requests.RequestException as exc:
        print(f"WARN: 请求失败 {url}: {exc}", file=sys.stderr)
        return None


def safe_filename(title: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", title).strip(" ._")
    return name or "novel"


# ═══════════════════════════════════════════════════════════════════════════
# Phase 1: Source Discovery (replaces step-1-search.md)
# ═══════════════════════════════════════════════════════════════════════════

def parse_search_results(html: str, base_url: str, title: str, book_pattern: str) -> str | None:
    """Find a book page URL from search results page."""
    soup = BeautifulSoup(html, "lxml")
    title_lower = title.lower()
    pattern_re = re.compile(book_pattern) if book_pattern else None

    # Strategy 1: find links whose text contains the title
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a.get("href", "").strip()
        if not href or href.startswith(("javascript:", "#")):
            continue
        if title_lower in text.lower() and len(text) < 60:
            full_url = urllib.parse.urljoin(base_url, href)
            if not pattern_re or pattern_re.search(full_url):
                return full_url

    # Strategy 2: find any link matching the book URL pattern
    if pattern_re:
        for a in soup.find_all("a", href=True):
            href = a.get("href", "").strip()
            if not href or href.startswith(("javascript:", "#")):
                continue
            full_url = urllib.parse.urljoin(base_url, href)
            if pattern_re.search(full_url):
                return full_url

    return None


def try_source(session: requests.Session, source: SourceConfig, title: str, timeout: int) -> tuple[str, SourceConfig] | None:
    """Try one source: search → find book URL. Returns (book_url, source) or None."""
    if not source.search_url:
        print(f"INFO: [{source.name}] 搜索不可用，跳过（用 --source-url 手动传入）", file=sys.stderr)
        return None
    search_url = source.search_url.replace("{title}", urllib.parse.quote(title))
    print(f"INFO: [{source.name}] 搜索: {search_url}", file=sys.stderr)
    html = fetch_page(session, search_url, timeout)
    if not html:
        return None

    book_url = parse_search_results(html, search_url, title, source.book_url_pattern)
    if not book_url:
        print(f"INFO: [{source.name}] 搜索结果中未找到《{title}》", file=sys.stderr)
        return None

    # Convert to PC version if needed
    if source.needs_pc:
        book_url = re.sub(r"https?://(m\.|wap\.)", "https://www.", book_url)

    print(f"INFO: [{source.name}] 找到: {book_url}", file=sys.stderr)
    return (book_url, source)


def discover_source(session: requests.Session, title: str, timeout: int) -> tuple[str, SourceConfig] | None:
    """Try all known sources in priority order."""
    for source in SOURCES:
        result = try_source(session, source, title, timeout)
        if result:
            return result
    return None


def _match_source_by_url(url: str) -> SourceConfig | None:
    """Match a user-provided URL against known sources by domain."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    for source in SOURCES:
        # Try to extract domain from source.search_url
        src_host = urllib.parse.urlparse(source.search_url).hostname or "" if source.search_url else ""
        # Fallback: derive domain from source.name (e.g. "boquku" → "boquku.com")
        if not src_host:
            name_domains = {
                "boquku": "boquku.com",
                "miaobige": "miaobige.com",
                "ishubao": "ishubao.org",
            }
            src_host = name_domains.get(source.name, "")
        if src_host and src_host.replace("www.", "") in host.replace("www.", ""):
            return source
    return None


# ═══════════════════════════════════════════════════════════════════════════
# Phase 2: Chapter Link Extraction + Content Selector Detection
# ═══════════════════════════════════════════════════════════════════════════

def extract_chapter_links(html: str, base_url: str, selectors: list[str]) -> list[dict]:
    """Parse chapter list page, return [{title, url}, ...]."""
    soup = BeautifulSoup(html, "lxml")
    seen = set()
    links: list[dict] = []

    all_selectors = selectors + FALLBACK_LIST_SELECTORS
    for selector in all_selectors:
        elements = soup.select(selector)
        if not elements:
            continue
        for el in elements:
            href = el.get("href", "").strip()
            text = el.get_text(strip=True)
            if not href or not text or len(text) < 2 or len(text) > 60:
                continue
            if any(nav in text.lower() for nav in NAV_LABELS):
                continue
            # Skip non-chapter URLs (homepage, login, logout, search, category)
            if any(skip in href.lower() for skip in ("logout", "login", "/search", "/home", "/sort", "/top", "javascript:")):
                continue
            full_url = urllib.parse.urljoin(base_url, href)
            if full_url not in seen:
                seen.add(full_url)
                links.append({"title": text.strip(), "url": full_url})
        if links:
            print(f"INFO: 选择器 '{selector}' 找到 {len(links)} 个章节链接", file=sys.stderr)
            break

    return links


def find_next_page(html: str, base_url: str) -> str | None:
    soup = BeautifulSoup(html, "lxml")
    for label in ("下一页", "下页", "下一頁", "next"):
        for a in soup.find_all("a", href=True):
            if a.get_text(strip=True).lower() == label:
                href = a.get("href", "").strip()
                if href and not href.startswith(("javascript:", "#")):
                    return urllib.parse.urljoin(base_url, href)
    return None


def collect_chapter_links(
    session: requests.Session, first_html: str, list_url: str, base_url: str,
    selectors: list[str], limit: int, timeout: int, max_pages: int = 30,
) -> list[dict]:
    """Collect chapter links, following pagination."""
    all_links: list[dict] = []
    seen: set[str] = set()
    current_html = first_html
    current_url = list_url
    pages = 0

    while current_html and pages < max_pages:
        pages += 1
        page_links = extract_chapter_links(current_html, current_url, selectors)
        for link in page_links:
            if link["url"] not in seen:
                seen.add(link["url"])
                all_links.append(link)
        if limit > 0 and len(all_links) >= limit:
            return all_links[:limit]
        if pages > 1 and not page_links:
            break
        next_url = find_next_page(current_html, current_url)
        if not next_url or next_url == current_url:
            break
        current_url = next_url
        time.sleep(0.3)
        current_html = fetch_page(session, current_url, timeout)

    return all_links


def detect_content_selector(session: requests.Session, links: list[dict], timeout: int) -> str | None:
    """Fetch a real chapter page, try selectors, return the best one."""
    if not links:
        return None
    # Skip non-chapter links (navigation, homepage) — real chapter URLs
    # typically contain a numeric ID or end with .html
    test_link = None
    for link in links:
        url = link["url"]
        if re.search(r"/\d{4,}|\.html", url) and "logout" not in url and "login" not in url:
            test_link = link
            break
    if not test_link:
        test_link = links[0]

    html = fetch_page(session, test_link["url"], timeout)
    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")
    best_selector = None
    best_len = 0

    for selector in FALLBACK_CONTENT_SELECTORS:
        elements = soup.select(selector)
        if elements:
            text_len = len(max(elements, key=lambda e: len(e.get_text(strip=True))).get_text(strip=True))
            if text_len > best_len:
                best_len = text_len
                best_selector = selector

    if best_selector and best_len > 100:
        print(f"INFO: 内容选择器确定: '{best_selector}' (测试章 {best_len} 字)", file=sys.stderr)
        return best_selector

    print("WARN: 无法确定内容选择器，将使用 body 全文提取", file=sys.stderr)
    return None


# ═══════════════════════════════════════════════════════════════════════════
# Phase 3: Concurrent Crawling (replaces step-2-download.md path B)
# ═══════════════════════════════════════════════════════════════════════════

def _clean_chapter_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    lines = text.split("\n")
    if lines and not re.search(r"[\u4e00-\u9fffa-zA-Z0-9]", lines[0]):
        lines.pop(0)
    return "\n".join(lines).strip()


def extract_chapter_content(html: str, selector: str | None) -> str:
    soup = BeautifulSoup(html, "lxml")
    if selector:
        elements = soup.select(selector)
        if elements:
            best = max(elements, key=lambda e: len(e.get_text(strip=True)))
            text = best.get_text("\n", strip=True)
            if len(text) > 100:
                return _clean_chapter_text(text)
    # Fallback: try all selectors
    for sel in FALLBACK_CONTENT_SELECTORS:
        elements = soup.select(sel)
        if elements:
            text = max(elements, key=lambda e: len(e.get_text(strip=True))).get_text("\n", strip=True)
            if len(text) > 100:
                return _clean_chapter_text(text)
    # Last resort: body text
    body = soup.find("body")
    if body:
        text = body.get_text("\n", strip=True)
        if len(text) > 200:
            return _clean_chapter_text(text)
    return ""


def crawl_chapters(
    session: requests.Session, links: list[dict], content_selector: str | None,
    workers: int, timeout: int, resume_titles: set[str] | None = None,
) -> tuple[dict[int, str | None], int, int, int]:
    """Crawl all chapters concurrently. Returns (results, crawled, failed, skipped)."""
    resume_titles = resume_titles or set()
    todo = [(i, link) for i, link in enumerate(links, 1) if link["title"].strip() not in resume_titles]
    skipped = len(links) - len(todo)
    if skipped:
        print(f"INFO: 断点续爬 — 跳过已下载 {skipped} 章，剩余 {len(todo)} 章", file=sys.stderr)

    results: dict[int, str | None] = {}
    failed = 0
    crawled = 0

    def _fetch_one(idx_link):
        i, link = idx_link
        sess = get_thread_session()
        html = fetch_page(sess, link["url"], timeout)
        if not html:
            return (i, None)
        content = extract_chapter_content(html, content_selector)
        return (i, content)

    if workers > 1 and len(todo) > 1:
        print(f"INFO: 并发爬取 — {workers} 线程，{len(todo)} 章", file=sys.stderr)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(_fetch_one, item): item[0] for item in todo}
            done_count = 0
            for fut in as_completed(futures):
                i, content = fut.result()
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
            html = fetch_page(session, link["url"], timeout)
            if not html:
                failed += 1
                results[i] = None
                continue
            content = extract_chapter_content(html, content_selector)
            if content:
                results[i] = content
                crawled += 1
            else:
                failed += 1
                results[i] = None
            time.sleep(0.5)

    return results, crawled, failed, skipped


# ═══════════════════════════════════════════════════════════════════════════
# Phase 4: Verification (replaces step-3-verify.md + inline paywall script)
# ═══════════════════════════════════════════════════════════════════════════

def detect_paywall(file_path: Path) -> list[str]:
    """Check for paywall-truncated chapters. Returns list of problem chapters."""
    text = file_path.read_text(encoding="utf-8")
    parts = re.split(r"^# (.*?)\n", text, flags=re.M)
    problems = []
    for i in range(1, len(parts), 2):
        title = parts[i]
        content = parts[i + 1]
        clean = content
        for marker in PAYWALL_MARKERS:
            clean = re.sub(re.escape(marker) + r".*", "", clean, flags=re.S)
        clean = clean.strip()
        if len(clean) < 500:
            problems.append(f"{title} (仅 {len(clean)} 字)")
    return problems


def verify_output(file_path: Path, min_bytes: int = 102400) -> dict:
    """Run all verification checks. Returns structured result."""
    result = {
        "file_exists": file_path.exists(),
        "size_bytes": 0,
        "size_mb": 0,
        "encoding": "utf-8",
        "paywall_chapters": [],
        "warnings": [],
    }
    if not file_path.exists():
        result["warnings"].append("文件不存在")
        return result

    size = file_path.stat().st_size
    result["size_bytes"] = size
    result["size_mb"] = round(size / 1024 / 1024, 2)

    if size < min_bytes:
        result["warnings"].append(f"文件偏小 ({size} bytes < {min_bytes})")

    # Paywall detection
    problems = detect_paywall(file_path)
    result["paywall_chapters"] = problems
    if problems:
        result["warnings"].append(f"付费墙检测: {len(problems)} 章内容过短")

    return result


# ═══════════════════════════════════════════════════════════════════════════
# Phase 5: Assembly & Delivery
# ═══════════════════════════════════════════════════════════════════════════

def assemble_and_save(
    links: list[dict], results: dict[int, str | None],
    output_path: Path, resume: bool, existing_count: int,
) -> str:
    """Assemble chapters in order and save to file."""
    new_chapters = []
    for i, link in enumerate(links, 1):
        content = results.get(i)
        if content:
            new_chapters.append(f"# {link['title']}\n\n{content}")

    if not new_chapters:
        return ""

    write_mode = "a" if (resume and existing_count > 0) else "w"
    with open(output_path, write_mode, encoding="utf-8", newline="\n") as f:
        if write_mode == "a":
            f.write("\n\n")
        f.write("\n\n".join(new_chapters))

    preview_src = new_chapters[0]
    return re.sub(r"\s+", " ", preview_src[:120]).strip()


# ═══════════════════════════════════════════════════════════════════════════
# Direct Download (replaces download_text.py for --direct mode)
# ═══════════════════════════════════════════════════════════════════════════

def direct_download(session: requests.Session, url: str, output_path: Path, timeout: int = 60) -> bool:
    """Download a direct TXT/ZIP URL and save as UTF-8."""
    rotate_ua(session)
    try:
        resp = session.get(url, timeout=timeout, stream=True)
        resp.raise_for_status()
        raw = resp.content
    except requests.RequestException as exc:
        print(f"ERROR: 直链下载失败: {exc}", file=sys.stderr)
        return False

    # Handle ZIP
    if url.lower().split("?")[0].endswith(".zip"):
        import io
        import zipfile
        try:
            archive = zipfile.ZipFile(io.BytesIO(raw))
            candidates = [i for i in archive.infolist() if not i.is_dir() and Path(i.filename).suffix.lower() in {".txt", ".md"}]
            if not candidates:
                print("ERROR: ZIP 中未找到 TXT", file=sys.stderr)
                return False
            candidates.sort(key=lambda i: i.file_size, reverse=True)
            raw = archive.read(candidates[0])
        except Exception as exc:
            print(f"ERROR: ZIP 解压失败: {exc}", file=sys.stderr)
            return False

    # Decode
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "gbk", "big5"):
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        print("ERROR: 无法识别文本编码", file=sys.stderr)
        return False

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    output_path.write_text(text, encoding="utf-8", newline="\n")
    return True


# ═══════════════════════════════════════════════════════════════════════════
# Main Orchestration
# ═══════════════════════════════════════════════════════════════════════════

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Unified webnovel downloader: search → test → crawl → verify → deliver."
    )
    parser.add_argument("title", help="Book title to search and download.")
    parser.add_argument("--output-dir", default=r"D:\popwave-skills\downloads", help="Output directory.")
    parser.add_argument("--workers", type=int, default=10, help="Concurrent threads (default 10).")
    parser.add_argument("--source-url", default=None, help="Skip search, use this URL directly.")
    parser.add_argument("--direct", action="store_true", help="Source URL is a direct TXT/ZIP link.")
    parser.add_argument("--chapter-selector", default=None, help="Override chapter list CSS selector.")
    parser.add_argument("--content-selector", default=None, help="Override content CSS selector.")
    parser.add_argument("--limit", type=int, default=0, help="Max chapters (0 = all). For testing.")
    parser.add_argument("--resume", action="store_true", help="Resume: skip already-downloaded chapters.")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds.")
    parser.add_argument("--delay", type=float, default=0, help="Delay between requests (serial mode only).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session = make_session()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{safe_filename(args.title)}.txt"

    start_time = time.time()

    # ── Mode 1: Direct download ──
    if args.source_url and args.direct:
        print(f"INFO: 直链下载模式: {args.source_url}", file=sys.stderr)
        if not direct_download(session, args.source_url, output_path, args.timeout):
            print(json.dumps({"status": "error", "reason": "直链下载失败"}, ensure_ascii=False))
            return 1
        verify = verify_output(output_path)
        preview = re.sub(r"\s+", " ", output_path.read_text(encoding="utf-8")[:120]).strip()
        _print_result(output_path, preview, 0, 0, 0, args.workers, args.source_url, "direct", verify, start_time)
        return 0

    # ── Mode 2: Source URL provided (skip search) ──
    if args.source_url:
        # Try to match URL against known sources for better selectors
        source = _match_source_by_url(args.source_url)
        if not source:
            source = SourceConfig(
                name="user-provided",
                search_url="",
                list_selectors=[args.chapter_selector] if args.chapter_selector else [],
                content_selectors=[args.content_selector] if args.content_selector else [],
            )
        else:
            print(f"INFO: URL 匹配已知源: {source.name}", file=sys.stderr)
            if args.chapter_selector:
                source.list_selectors = [args.chapter_selector]
            if args.content_selector:
                source.content_selectors = [args.content_selector]
        list_url = args.source_url
        source_name = source.name
        print(f"INFO: 使用指定源: {list_url}", file=sys.stderr)
    else:
        # ── Mode 3: Auto-discover source ──
        print(f"INFO: 自动搜索《{args.title}》…", file=sys.stderr)
        discovered = discover_source(session, args.title, args.timeout)
        if not discovered:
            print(f"ERROR: 所有已知源均未找到《{args.title}》", file=sys.stderr)
            print(json.dumps({
                "status": "error",
                "reason": "所有已知源均未找到此书",
                "suggestion": "请用 popwave-search 搜索其他来源，然后用 --source-url 传入",
            }, ensure_ascii=False))
            return 1
        list_url, source = discovered
        source_name = source.name

    # ── Fetch chapter list page ──
    print(f"INFO: 获取章节列表: {list_url}", file=sys.stderr)
    list_html = fetch_page(session, list_url, args.timeout)
    if not list_html:
        print(json.dumps({"status": "error", "reason": f"无法获取章节列表页: {list_url}"}, ensure_ascii=False))
        return 1

    # ── Extract chapter links ──
    selectors = source.list_selectors if source.list_selectors else []
    if args.chapter_selector:
        selectors = [args.chapter_selector]
    links = collect_chapter_links(session, list_html, list_url, list_url, selectors, args.limit, args.timeout)
    if not links:
        print("ERROR: 无法从页面提取章节链接", file=sys.stderr)
        print(json.dumps({"status": "error", "reason": "无法提取章节链接，可能是JS动态加载"}, ensure_ascii=False))
        return 1

    if args.limit > 0:
        links = links[:args.limit]
    print(f"INFO: 共 {len(links)} 章", file=sys.stderr)

    # ── Auto-detect content selector ──
    content_sel = args.content_selector
    if not content_sel:
        content_sel = detect_content_selector(session, links, args.timeout)

    # ── Resume: detect existing chapters ──
    done_titles: set[str] = set()
    existing_count = 0
    if args.resume and output_path.exists():
        try:
            old = output_path.read_text(encoding="utf-8")
            for m in re.finditer(r"^# (.+)$", old, flags=re.M):
                done_titles.add(m.group(1).strip())
            existing_count = len(done_titles)
        except Exception:
            pass

    # ── Crawl ──
    results, crawled, failed, skipped = crawl_chapters(
        session, links, content_sel, args.workers, args.timeout, done_titles
    )

    if crawled == 0:
        print("ERROR: 未能成功爬取任何章节", file=sys.stderr)
        print(json.dumps({"status": "error", "reason": "所有章节爬取失败"}, ensure_ascii=False))
        return 1

    # ── Assemble & save ──
    preview = assemble_and_save(links, results, output_path, args.resume, existing_count)

    # ── Verify ──
    verify = verify_output(output_path)

    # ── Print structured result ──
    _print_result(output_path, preview, crawled, failed, skipped, args.workers, list_url, source_name, verify, start_time)
    return 0


def _print_result(
    output_path: Path, preview: str, crawled: int, failed: int, skipped: int,
    workers: int, source_url: str, source_name: str, verify: dict, start_time: float,
) -> None:
    elapsed = time.time() - start_time
    result = {
        "status": "success",
        "output": str(output_path),
        "size_bytes": verify["size_bytes"],
        "size_mb": verify["size_mb"],
        "encoding": "utf-8",
        "chapters_crawled": crawled,
        "chapters_failed": failed,
        "chapters_skipped": skipped,
        "workers": workers,
        "source": source_name,
        "source_url": source_url,
        "elapsed_seconds": round(elapsed, 1),
        "paywall_warnings": len(verify["paywall_chapters"]),
        "warnings": verify["warnings"],
        "preview": preview,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    raise SystemExit(main())
