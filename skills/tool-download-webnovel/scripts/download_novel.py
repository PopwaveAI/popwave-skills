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
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

# ── Paywalled official site domains — never search/crawl by default ──
# These sites require login/payment to read full chapters. Crawling them yields
# truncated content (paywall markers), wasting time and producing broken output.
PAYWALL_DOMAINS = [
    "qidian.com",        # 起点中文网
    "jjwxc.net",         # 晋江文学城
    "zongheng.com",      # 纵横中文网
    "17k.com",           # 17K小说网
    "kanshu.com",        # 看书网
    "zhulang.com",       # 逐浪小说网
    "motie.com",         # 磨铁中文网
    "tadu.com",          # 塔读文学
    "hongxiu.com",       # 红袖添香
    "xxsy.net",          # 潇湘书院
    "readnovel.com",     # 小说阅读网
    "qimao.com",         # 七猫小说
    "fanqienovel.com",   # 番茄小说
    "xianging.com",      # 香网
    "faloo.com",         # 飞卢小说网
    "ruochu.com",        # 若初文学网
    "wangyuewen.com",    # 网易云阅读
    "chuangshi.com",     # 创世中文网
    "cloudary.com.cn",   # 盛大文学
]


def is_paywall_site(url: str) -> str | None:
    """Check if URL belongs to a paywalled official site.

    Returns the matched domain if paywalled, None otherwise.
    Strips common subdomain prefixes (www. m. wap. book.) before matching.
    """
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except Exception:
        return None
    host = host.lower()
    for prefix in ("www.", "m.", "wap.", "book.", "read."):
        if host.startswith(prefix):
            host = host[len(prefix):]
    for domain in PAYWALL_DOMAINS:
        if host == domain or host.endswith("." + domain):
            return domain
    return None

# ── Non-chapter navigation labels ──
NAV_LABELS = (
    "开始阅读", "下一页", "上一页", "下页", "上页", "尾页", "首页", "末页",
    "返回书页", "查看全部", "全部章节", "章节目录", "全文阅读", "最新章节",
    "txt下载", "加入书架", "书签", "上一章", "下一章", "back", "next",
    "小说简介", "内容简介", "作品相关", "作品信息", "作者的话", "作者前言",
    "公告", "敬告读者", "本书相关", "书籍简介",
    "直达页面底部", "阅读历史", "永久书架", "回首页", "设为首页",
    "收藏", "登录", "注册", "退出", "记住了",
    "返回", "关灯", "护眼", "字号", "章节报错", "存书签",
    "免登陆", "一秒记住",
)

# ── Content noise patterns — text snippets to strip from chapter content ──
# These are navigation/ad elements that CSS selectors sometimes include.
# Applied after extraction, before saving.
CONTENT_NOISE_PATTERNS = [
    re.compile(r'^首页$\s*', re.M),
    re.compile(r'^返回$\s*', re.M),
    re.compile(r'^关灯$\s*', re.M),
    re.compile(r'^护眼：[关开]$\s*', re.M),
    re.compile(r'^字号：[大小]$\s*', re.M),
    re.compile(r'^章节报错.*$\s*', re.M),
    re.compile(r'^上一章$\s*', re.M),
    re.compile(r'^目录$\s*', re.M),
    re.compile(r'^存书签$\s*', re.M),
    re.compile(r'^下一章$\s*', re.M),
    re.compile(r'^一秒记住.*$\s*', re.M),
    re.compile(r'^biquge\d+\.net.*$\s*', re.M),
    re.compile(r'（本章未完，请点击下一页继续阅读）\s*'),
    re.compile(r'^第.+章.+\(第\d+/\d+页\)\s*$', re.M),  # Page indicator within chapter
]
# ── URL fragments that indicate non-chapter links ──
NAV_URL_PATTERNS = (
    "logout", "login", "/search", "/home", "/sort", "/top", "/rank",
    "javascript:", "bookcase", "history", "/bookcase", "/history",
    "/register", "/sitemap", "/feedback", "/about", "/help",
)

# ── Author index page markers — detect author works page vs book chapter list ──
# When a search returns an author's works index page (作品集) instead of a
# specific book page, the script used to treat book entries as chapter links
# and crawl the wrong book. These markers help detect and reject such pages.
AUTHOR_INDEX_MARKERS = ["作品集", "的文章列表", "全部小说", "全部作品"]

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
    # 80ge.info: primary source for direct TXT download (Jieqi CMS)
    # Anti-leech: direct_download() visits book page first to get session cookies
    # Encoding: UTF-8 (NOT GB2312 — GB2312 returns empty results)
    SourceConfig(
        name="80ge",
        search_url="http://www.80ge.info/modules/article/search.php?searchkey={title}",
        list_selectors=["dd a", "li a", "div#content a"],
        content_selectors=["div#content", "div.content"],
        encoding="utf-8",
        book_url_pattern=r"txtxz/\d+",
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
        name="boquku",
        search_url="",  # search disabled (404); use --source-url with book page URL
        list_selectors=["ul#chapters-list li a", "div#list a", "dd a"],
        content_selectors=["div#content", "div.content", "div#chaptercontent", "div.book_content_text", "div#nr1"],
        encoding=None,
        book_url_pattern=r"/book/\d+",
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
    SourceConfig(
        name="9iecxs",
        search_url="",  # use --source-url with book list page URL
        list_selectors=["dd a", "li a", "div.booklist a", "ul.list a"],
        content_selectors=["div#chaptercontent", "div#content", "div.content", "div.Readarea"],
        encoding=None,
        book_url_pattern=r"/booklist/shu/",
    ),
    SourceConfig(
        name="neiyexs",
        search_url="",  # use --source-url with book page URL
        list_selectors=["ul.detail-list a", "div.chapter-list a", "dd a", "li a"],
        content_selectors=["div#content", "div.content", "div#chaptercontent", "div.book_content_text"],
        encoding=None,
        book_url_pattern=r"/\d+/",
    ),
    SourceConfig(
        name="biquge365",
        search_url="",  # use --source-url with mobile book page URL (m.biquge365.net/shu/{id}/)
        list_selectors=["li a", "dd a"],
        content_selectors=["div.txt", "div#content", "div.content", "div#chaptercontent"],
        encoding=None,
        book_url_pattern=r"/shu/\d+",
    ),
]

# ── Fallback content selectors (tried in order when site-specific ones fail) ──
FALLBACK_CONTENT_SELECTORS = [
    "div#content", "div.content", "div#chaptercontent", "div.book_content_text",
    "div#nr1", "div#booktxt", "div.txtnav", "article", "div.read-content",
    "div.showtxt", "div.novel-content", "div#TextContent", "div.txt",
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
    session.verify = False  # Ignore SSL errors (many mirror sites have bad certs)
    session.trust_env = False  # Ignore system proxy (127.0.0.1:7890 causes timeouts)
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


def fetch_page(session: requests.Session, url: str, timeout: int = 30, retries: int = 2) -> str | None:
    """Fetch a page with encoding detection, anti-spider checks, and retry."""
    for attempt in range(retries + 1):
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
            if attempt < retries:
                wait = 2 ** attempt  # 1s, 2s, 4s
                print(f"WARN: 请求失败 (attempt {attempt+1}/{retries+1}) {url}: {exc}, {wait}s后重试", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"WARN: 请求失败 {url}: {exc}", file=sys.stderr)
                return None
    return None


def safe_filename(title: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", title).strip(" ._")
    return name or "novel"


# ═══════════════════════════════════════════════════════════════════════════
# Phase 1: Source Discovery (replaces step-1-search.md)
# ═══════════════════════════════════════════════════════════════════════════

def is_author_index_page(html: str) -> bool:
    """Detect if a page is an author's works index page rather than a book chapter list.

    Author index pages list multiple books by one author, each with "TXT下载"
    links. If we treat these as chapter links, we crawl the wrong book.

    Detection signals:
    - Page contains "作品集" / "的文章列表" / "全部小说" / "全部作品"
    - Multiple "TXT下载" links (real chapter lists never have these)
    """
    # Check for author index markers in the first 3000 chars
    head = html[:3000]
    for marker in AUTHOR_INDEX_MARKERS:
        if marker in head:
            return True
    # Check for multiple "TXT下载" links (strong signal of author page)
    txt_download_count = html.count("TXT下载") + html.count("txt下载")
    if txt_download_count >= 2:
        return True
    return False


def verify_author_on_page(html: str, author: str) -> bool:
    """Check if the author name appears in the page content.

    Used to verify that a search result actually matches the requested author.
    Checks the first 5000 chars of the page for the author name.
    """
    if not author:
        return True  # No author specified, skip verification
    author_clean = author.strip()
    # Check in page content (case-insensitive for Latin, exact for CJK)
    head = html[:5000]
    return author_clean in head


def parse_search_results(html: str, base_url: str, title: str, book_pattern: str) -> list[str]:
    """Find book page URLs from search results page. Skips paywalled sites.

    Returns a list of candidate URLs (best match first), not just the first match.
    This allows author verification to try the next candidate if the first fails.
    """
    soup = BeautifulSoup(html, "lxml")
    title_clean = re.sub(r"[?？：:！!]", "", title).strip().lower()
    candidates: list[tuple[int, str, str]] = []  # (score, url, text)

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a.get("href", "").strip()
        if not href or href.startswith(("javascript:", "#")):
            continue
        if len(text) > 80:
            continue
        text_clean = re.sub(r"[?？：:！!]", "", text).strip().lower()
        full_url = urllib.parse.urljoin(base_url, href)
        if is_paywall_site(full_url):
            continue
        pattern_re = re.compile(book_pattern) if book_pattern else None
        if pattern_re and not pattern_re.search(full_url):
            continue
        # Full substring match: title in result text, or result text in title
        if title_clean and (title_clean in text_clean or text_clean in title_clean):
            score = len(text_clean)  # Prefer longer (more specific) matches
            candidates.append((score, full_url, text))

    # Sort by score descending (most specific match first)
    candidates.sort(key=lambda x: -x[0])

    # Deduplicate URLs while preserving order
    seen = set()
    result = []
    for _, url, text in candidates:
        if url not in seen:
            seen.add(url)
            result.append(url)

    if result:
        print(f"INFO: 搜索匹配到 {len(result)} 个候选结果", file=sys.stderr)

    # Fallback: find any link matching the book URL pattern (loose fallback)
    if not result and book_pattern:
        pattern_re = re.compile(book_pattern)
        for a in soup.find_all("a", href=True):
            href = a.get("href", "").strip()
            if not href or href.startswith(("javascript:", "#")):
                continue
            full_url = urllib.parse.urljoin(base_url, href)
            if is_paywall_site(full_url):
                continue
            if pattern_re.search(full_url):
                result.append(full_url)

    return result


def try_source(
    session: requests.Session, source: SourceConfig, title: str, timeout: int,
    author: str | None = None,
) -> tuple[str, SourceConfig] | None:
    """Try one source: search → find book URL → verify author (if provided).

    Returns (book_url, source) or None.
    When author is provided, fetches each candidate page and verifies the
    author name appears on it. Skips candidates that don't match.
    """
    if not source.search_url:
        print(f"INFO: [{source.name}] 搜索不可用，跳过（用 --source-url 手动传入）", file=sys.stderr)
        return None
    search_url = source.search_url.replace("{title}", urllib.parse.quote(title))
    print(f"INFO: [{source.name}] 搜索: {search_url}", file=sys.stderr)
    html = fetch_page(session, search_url, timeout)
    if not html:
        return None

    candidate_urls = parse_search_results(html, search_url, title, source.book_url_pattern)
    if not candidate_urls:
        print(f"INFO: [{source.name}] 搜索结果中未找到《{title}》", file=sys.stderr)
        return None

    # If author is provided, verify each candidate
    for i, book_url in enumerate(candidate_urls):
        # Convert to PC version if needed
        if source.needs_pc:
            book_url = re.sub(r"https?://(m\.|wap\.)", "https://www.", book_url)

        if author:
            print(f"INFO: [{source.name}] 验证候选 {i+1}/{len(candidate_urls)}: {book_url}", file=sys.stderr)
            page_html = fetch_page(session, book_url, timeout)
            if not page_html:
                continue
            if is_author_index_page(page_html):
                print(f"WARN: [{source.name}] 候选 {i+1} 是作者作品集页面，跳过", file=sys.stderr)
                continue
            if not verify_author_on_page(page_html, author):
                print(f"WARN: [{source.name}] 候选 {i+1} 页面未找到作者 '{author}'，跳过", file=sys.stderr)
                continue
            print(f"INFO: [{source.name}] 作者验证通过: {book_url}", file=sys.stderr)
            return (book_url, source)
        else:
            # No author to verify, but still check for author index page
            page_html = fetch_page(session, book_url, timeout)
            if page_html and is_author_index_page(page_html):
                print(f"WARN: [{source.name}] 候选 {i+1} 是作者作品集页面，跳过", file=sys.stderr)
                continue
            print(f"INFO: [{source.name}] 找到: {book_url}", file=sys.stderr)
            return (book_url, source)

    print(f"INFO: [{source.name}] 所有候选结果均未通过验证", file=sys.stderr)
    return None


def discover_source(
    session: requests.Session, title: str, timeout: int,
    author: str | None = None,
) -> tuple[str, SourceConfig] | None:
    """Try all known sources in priority order. Passes author for verification."""
    for source in SOURCES:
        result = try_source(session, source, title, timeout, author)
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
                "80ge": "80ge.info",
                "boquku": "boquku.com",
                "miaobige": "miaobige.com",
                "ishubao": "ishubao.org",
                "9iecxs": "9iecxs.com",
                "9iec": "9iec.cc",
                "neiyexs": "neiyexs.com",
                "biquge365": "biquge365.net",
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
            # Skip non-chapter URLs (homepage, login, logout, search, category, etc.)
            if any(skip in href.lower() for skip in NAV_URL_PATTERNS):
                continue
            # Skip links that are just the site root (likely navigation)
            parsed_href = urllib.parse.urlparse(href)
            if parsed_href.path in ("", "/", "/index.html", "/index.php", "/default.html"):
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
    selectors: list[str], limit: int, timeout: int, max_pages: int = 200,
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
    """Fetch real chapter pages, try selectors, return the best one."""
    if not links:
        return None
    # Filter to likely-real chapter links (numeric ID or .html in URL)
    test_links = []
    for link in links:
        url = link["url"]
        if re.search(r"/\d{4,}|\.html|/\d+/", url) and not any(skip in url.lower() for skip in NAV_URL_PATTERNS):
            test_links.append(link)
    if not test_links:
        test_links = links[:3]
    # Try up to 3 chapter pages to find a working selector
    for test_link in test_links[:3]:
        html = fetch_page(session, test_link["url"], timeout)
        if not html:
            continue
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
    # Strip content noise (navigation/ad elements from CSS selector leakage)
    for pattern in CONTENT_NOISE_PATTERNS:
        text = pattern.sub('', text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    lines = text.split("\n")
    if lines and not re.search(r"[\u4e00-\u9fffa-zA-Z0-9]", lines[0]):
        lines.pop(0)
    return "\n".join(lines).strip()


def _strip_page_suffix(path: str) -> str:
    """Strip trailing _N / /N / _N.html suffix for intra-chapter prefix matching.

    /book/123_2.html → /book/123
    /book/123.html   → /book/123
    /read/123/2      → /read/123
    /read/123        → /read/123
    """
    path = re.sub(r"_\d+\.html?$", "", path)
    path = re.sub(r"\.html?$", "", path)
    path = re.sub(r"/\d+/?$", "", path)
    return path


def find_chapter_next_page(html: str, base_url: str, chapter_url: str) -> str | None:
    """Find an intra-chapter 'next page' link, NOT a 'next chapter' link.

    Many novel sites split one chapter across multiple pages (e.g.
    /book/123.html → /book/123_2.html → /book/123_3.html). Without this
    function the crawler only grabs page 1 and silently drops the rest.

    Distinguishes pagination from chapter navigation by checking that the
    next URL shares a path prefix with the current chapter URL after
    stripping trailing page-number suffixes.
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
        # Exclude "下一章" (next chapter) — only match pure page-flip labels
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
        # Accept if prefixes match (same chapter, different page)
        if next_prefix and next_prefix == current_prefix:
            return full_url
        # Also accept if next path extends current (e.g. /read/123 → /read/123/2)
        if next_path.startswith(current_path) or current_path.startswith(next_prefix):
            return full_url
    return None


def fetch_chapter_content(
    session: requests.Session, url: str, content_selector: str | None,
    timeout: int, max_pages: int = 50,
) -> str:
    """Fetch a chapter, following intra-chapter pagination, return full text.

    Many novel sites split one chapter across multiple pages. This function
    detects 'next page' links *within* the chapter (not 'next chapter') and
    concatenates all pages.
    """
    parts: list[str] = []
    current_url = url
    seen: set[str] = {url}
    pages = 0

    while current_url and pages < max_pages:
        html = fetch_page(session, current_url, timeout)
        if not html:
            break
        text = extract_chapter_content(html, content_selector)
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
        content = fetch_chapter_content(sess, link["url"], content_selector, timeout)
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
            content = fetch_chapter_content(session, link["url"], content_selector, timeout)
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


def validate_content_match(file_path: Path, expected_title: str, expected_author: str | None) -> list[str]:
    """Check if downloaded content matches the expected title and author.

    Reads the first 2000 chars of the file and checks for title/author presence.
    Returns a list of warning messages (empty if all good).
    """
    warnings = []
    try:
        text = file_path.read_text(encoding="utf-8")[:2000]
    except Exception:
        return warnings

    if expected_title:
        title_clean = re.sub(r"[?？：:！!]", "", expected_title).strip()
        if title_clean and title_clean not in text:
            warnings.append(f"内容校验: 文件中未找到书名 '{expected_title}'，可能下错了书")

    if expected_author:
        if expected_author not in text:
            warnings.append(f"内容校验: 文件中未找到作者 '{expected_author}'，可能下错了书")

    return warnings


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
    parsed = urllib.parse.urlparse(url)

    # For 80ge.info: visit book page first to get anti-leech cookies
    if "80ge.info" in (parsed.hostname or ""):
        # Extract book_id from URL path: /{book_id}/{title}.txt
        path_parts = parsed.path.strip("/").split("/")
        book_id = path_parts[0] if path_parts else ""
        if book_id:
            book_page_url = f"http://www.80ge.info/txtxz/{book_id}.html"
            session.headers["Referer"] = "http://www.80ge.info/"
            try:
                page_resp = session.get(book_page_url, timeout=15)
                # Try to extract the actual download URL from the page
                for enc in ("utf-8", "gbk", "gb2312"):
                    try:
                        page_resp.encoding = enc
                        page_html = page_resp.text
                        if "\ufffd" not in page_html[:500]:
                            break
                    except:
                        continue
                import re as _re
                direct_match = _re.search(r'(?:https?://)?txt\.80ge\.info/\d+/[^"\'<>\s]+\.txt', page_html)
                if direct_match:
                    new_url = direct_match.group(0)
                    if not new_url.startswith("http"):
                        new_url = "http://" + new_url
                    url = new_url
            except Exception:
                pass  # Continue with original URL even if page visit fails
        session.headers["Referer"] = f"http://www.80ge.info/"
    else:
        session.headers["Referer"] = f"{parsed.scheme}://{parsed.hostname}/"

    # Retry logic for direct download
    max_retries = 3
    for attempt in range(max_retries):
        try:
            resp = session.get(url, timeout=timeout, stream=True)
            resp.raise_for_status()
            raw = resp.content
            break
        except requests.RequestException as exc:
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 3
                print(f"WARN: 直链下载重试 ({attempt+1}/{max_retries}) {wait}s后: {exc}", file=sys.stderr)
                time.sleep(wait)
            else:
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
    parser.add_argument("--author", default=None, help="Author name (for output filename + search verification).")
    parser.add_argument("--output-dir", default=r"D:\popwave-skills\downloads", help="Output directory.")
    parser.add_argument("--output-subdir", default=None, help="Subdirectory under output-dir (e.g. 番茄top20).")
    parser.add_argument("--workers", type=int, default=10, help="Concurrent threads (default 10).")
    parser.add_argument("--source-url", default=None, help="Skip search, use this URL directly.")
    parser.add_argument("--direct", action="store_true", help="Source URL is a direct TXT/ZIP link.")
    parser.add_argument("--chapter-selector", default=None, help="Override chapter list CSS selector.")
    parser.add_argument("--content-selector", default=None, help="Override content CSS selector.")
    parser.add_argument("--limit", type=int, default=0, help="Max chapters (0 = all). For testing.")
    parser.add_argument("--resume", action="store_true", help="Resume: skip already-downloaded chapters.")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds.")
    parser.add_argument("--delay", type=float, default=0, help="Delay between requests (serial mode only).")
    parser.add_argument("--include-paywall", action="store_true", help="Allow crawling paywalled official sites (excluded by default).")
    parser.add_argument("--reverse", action="store_true", help="Reverse chapter order (some sites list latest first).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    session = make_session()
    output_dir = Path(args.output_dir)
    if args.output_subdir:
        output_dir = output_dir / args.output_subdir
    output_dir.mkdir(parents=True, exist_ok=True)
    # Filename: title-author.txt or title.txt
    if args.author:
        filename = f"{safe_filename(args.title)}-{safe_filename(args.author)}.txt"
    else:
        filename = f"{safe_filename(args.title)}.txt"
    output_path = output_dir / filename

    start_time = time.time()

    # ── Paywall site guard: reject paywalled official sites by default ──
    if args.source_url and not args.include_paywall:
        paywall_domain = is_paywall_site(args.source_url)
        if paywall_domain:
            msg = f"URL 属于付费墙正版网站 ({paywall_domain})，默认排除"
            print(f"ERROR: {msg}", file=sys.stderr)
            print(json.dumps({
                "status": "error",
                "reason": msg,
                "matched_domain": paywall_domain,
                "suggestion": "请搜索免费来源（笔趣阁/80txt等），或加 --include-paywall 强制",
            }, ensure_ascii=False))
            return 1

    # ── Mode 1: Direct download ──
    if args.source_url and args.direct:
        print(f"INFO: 直链下载模式: {args.source_url}", file=sys.stderr)
        if not direct_download(session, args.source_url, output_path, args.timeout):
            print(json.dumps({"status": "error", "reason": "直链下载失败"}, ensure_ascii=False))
            return 1
        verify = verify_output(output_path)
        preview = re.sub(r"\s+", " ", output_path.read_text(encoding="utf-8")[:120]).strip()
        # Content validation for direct downloads too
        content_warnings = validate_content_match(output_path, args.title, args.author)
        verify["warnings"].extend(content_warnings)
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
        discovered = discover_source(session, args.title, args.timeout, args.author)
        if not discovered:
            print(f"ERROR: 所有已知源均未找到《{args.title}》", file=sys.stderr)
            suggestion = "请用 popwave-search 搜索其他来源，然后用 --source-url 传入"
            if args.author:
                suggestion += f"。已提供作者 '{args.author}' 但所有源的搜索结果均未通过作者验证"
            print(json.dumps({
                "status": "error",
                "reason": "所有已知源均未找到此书" + (f"（作者验证未通过: {args.author}）" if args.author else ""),
                "suggestion": suggestion,
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

    # ── Author index page detection ──
    if is_author_index_page(list_html):
        msg = f"页面是作者作品集页面，非书籍章节列表: {list_url}"
        print(f"ERROR: {msg}", file=sys.stderr)
        print(json.dumps({
            "status": "error",
            "reason": msg,
            "suggestion": "请搜索具体的书籍章节页 URL，而非作者作品集页面",
        }, ensure_ascii=False))
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
    if args.reverse:
        links.reverse()
        print(f"INFO: 章节顺序已反转（最新章在后）", file=sys.stderr)
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

    # ── Content validation: check if downloaded content matches expected title/author ──
    content_warnings = validate_content_match(output_path, args.title, args.author)
    verify["warnings"].extend(content_warnings)

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
