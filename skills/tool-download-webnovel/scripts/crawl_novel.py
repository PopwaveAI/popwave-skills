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
  python crawl_novel.py --list-url <URL> --title "书名" --limit 50
  python crawl_novel.py --list-url <URL> --title "书名" --chapter-selector "#content" --delay 1.5
"""

from __future__ import annotations

import argparse
import os
import random
import re
import sys
import time
import urllib.parse
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
    "div#booktxt",
    "div.txtnav",
    "article",
    "div.read-content",
    "div.showtxt",
    "div.novel-content",
    "div#TextContent",
    "div#chaptercontent",
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
    return parser.parse_args()


def safe_filename(title: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", title).strip(" ._")
    return name or "crawled-novel"


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
    })
    return session


def rotate_ua(session: requests.Session) -> None:
    session.headers["User-Agent"] = random.choice(USER_AGENTS)


def fetch_page(session: requests.Session, url: str, timeout: int = 30) -> str | None:
    """Fetch a page, return None on failure."""
    rotate_ua(session)
    try:
        resp = session.get(url, timeout=timeout)
        resp.raise_for_status()
        # Detect encoding from Content-Type or HTML meta
        if resp.encoding and resp.encoding.lower() != "utf-8":
            resp.encoding = resp.apparent_encoding or resp.encoding
        text = resp.text
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
                # Resolve relative URLs
                full_url = urllib.parse.urljoin(base_url, href)
                if full_url not in seen:
                    seen.add(full_url)
                    links.append({"title": text.strip(), "url": full_url})
            if links:
                print(f"INFO: 使用选择器 '{selector}' 找到了 {len(links)} 个章节链接", file=sys.stderr)
                break

    return links


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
                # Clean up excessive whitespace
                text = re.sub(r"\n{3,}", "\n\n", text)
                text = re.sub(r"[ \t]{2,}", " ", text)
                return text.strip()

    # Fallback: just get all visible text from body
    body = soup.find("body")
    if body:
        text = body.get_text("\n", strip=True)
        text = re.sub(r"\n{3,}", "\n\n", text)
        if len(text) > 200:
            print("WARN: 未找到已知内容选择器，使用 body 全文提取", file=sys.stderr)
            return text.strip()

    return ""


def check_for_full_download(session: requests.Session, list_html: str, base_url: str) -> str | None:
    """Check if the list page has a '全本TXT下载' or similar direct download link."""
    soup = BeautifulSoup(list_html, "lxml")
    download_keywords = ["txt下载", "全本下载", "全集下载", "下载txt", "全文下载", "本地下載"]
    
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "")
        text = a_tag.get_text(strip=True)
        for kw in download_keywords:
            if kw in text.lower() or kw in href.lower():
                full_url = urllib.parse.urljoin(base_url, href)
                print(f"INFO: 发现全本下载链接: {full_url} (『{text}』)", file=sys.stderr)
                return full_url

    # Check for direct download links (.txt or .zip end)
    for a_tag in soup.find_all("a", href=True):
        href = a_tag.get("href", "").lower()
        if href.endswith(".txt") or href.endswith(".zip"):
            full_url = urllib.parse.urljoin(base_url, a_tag.get("href", ""))
            print(f"INFO: 发现直链下载: {full_url}", file=sys.stderr)
            return full_url

    return None


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

    # ── Step 3: Extract chapter links ──
    links = extract_chapter_links(list_html, base_url, args.chapter_selector)
    if not links:
        print("ERROR: 无法从页面提取章节链接", file=sys.stderr)
        return 1

    if args.reverse:
        links.reverse()

    if args.limit > 0:
        links = links[:args.limit]

    print(f"INFO: 共发现 {len(links)} 个章节，开始爬取…", file=sys.stderr)

    # ── Step 4: Crawl each chapter ──
    chapters_text: list[str] = []
    crawled = 0
    failed = 0

    for i, link in enumerate(links, 1):
        print(f"INFO: [{i}/{len(links)}] {link['title']}", file=sys.stderr)
        html = fetch_page(session, link["url"], args.timeout)
        if not html:
            failed += 1
            continue

        content = extract_chapter_content(html, args.content_selector)
        if content:
            chapters_text.append(f"# {link['title']}\n\n{content}")
        else:
            print(f"WARN: 未能提取章节内容: {link['title']}", file=sys.stderr)
            failed += 1

        crawled += 1

        # Rate limiting
        if i < len(links):
            delay = args.delay + random.uniform(0, args.delay * 0.5)
            time.sleep(delay)

    # ── Step 5: Assemble and save ──
    if not chapters_text:
        print("ERROR: 未能成功爬取任何章节", file=sys.stderr)
        return 1

    full_text = "\n\n".join(chapters_text)
    output_path = output_dir / f"{safe_filename(args.title)}.txt"
    output_path.write_text(full_text, encoding="utf-8", newline="\n")

    file_size = output_path.stat().st_size
    preview = re.sub(r"\s+", " ", full_text[:120]).strip()

    print(f"output={output_path}")
    print(f"encoding=utf-8")
    print(f"bytes={file_size}")
    print(f"chapters_crawled={crawled}")
    print(f"chapters_failed={failed}")
    print(f"preview={preview}")

    if failed > 0 and failed > crawled * 0.3:
        print(f"WARN: 失败率较高 ({failed}/{failed + crawled})，部分内容可能缺失", file=sys.stderr)
    return 0


def main() -> int:
    args = parse_args()
    return crawl_novel(args)


if __name__ == "__main__":
    raise SystemExit(main())
