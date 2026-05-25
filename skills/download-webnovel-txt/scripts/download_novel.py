#!/usr/bin/env python3
"""Download authorized web novel chapters and assemble a clean TXT."""

from __future__ import annotations

import argparse
import gzip
import http.client
import html
import json
import posixpath
import random
import re
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
import zlib
from collections.abc import Iterable
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "br",
    "div",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "li",
    "main",
    "p",
    "pre",
    "section",
    "tr",
}

SKIP_TAGS = {"script", "style", "noscript", "svg", "canvas", "iframe", "form"}

GATED_PAGE_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r'type=["\']?password',
        r"下载地址已被隐藏",
        r"输入密码查看",
        r"关注.*公众号",
        r"微信公众号",
        r"回复.*密码",
        r"验证码",
        r"captcha",
        r"cloudflare",
        r"just a moment",
        r"enable javascript",
        r"sorry, you have been blocked",
        r"challenge-platform",
        r"VIP章节",
        r"订阅章节",
        r"晋江币",
        r"购买此章",
        r"由于版权问题不能显示",
        r"请下载.*继续阅读",
        r"蜘蛛未爬行",
        r"APP内更新",
    )
]

DOWNLOAD_EXTENSIONS = (".txt", ".epub", ".zip", ".rar", ".7z")
DOWNLOAD_EXTENSION_PRIORITY = {
    ".txt": 100,
    ".epub": 90,
    ".zip": 80,
    ".rar": 40,
    ".7z": 35,
}

COMMON_SOURCE_BOILERPLATE_PATTERNS = [
    r"知轩藏书下载|zxcs\.zip",
    r"用户上传之内容开始|用户上传之内容结束|内容开始|内容结束",
    r"八零电子书|txt80\.com|免费.*下载服务|版权与本站无任何关系",
    r"您下载的小说来自www\.27txt\.com\s*爱去小说网",
    r"章节内容来源网络，版权归原作者所有，本书仅供书友预览",
]
COMMON_SOURCE_INLINE_PATTERNS = [
    r"(?m)gd\d{6,}:\s*$",
]
DECORATIVE_EDGE_LINE = re.compile(r"^[=\-_*~—]{5,}$")


@dataclass
class Chapter:
    source: str
    title: str
    text: str


@dataclass
class Candidate:
    url: str
    title: str
    source_type: str
    score: int
    reason: str
    downloadable_links: list[str]
    chapter_link_count: int


class LinkExtractor(HTMLParser):
    def __init__(self, pattern: str | None = None) -> None:
        super().__init__(convert_charrefs=True)
        self.pattern = re.compile(pattern) if pattern else None
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attrs_dict = {name.lower(): value or "" for name, value in attrs}
        href = attrs_dict.get("href", "").strip()
        if href and (not self.pattern or self.pattern.search(href)):
            self.links.append(href)


class SearchResultExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.results: list[tuple[str, str]] = []
        self._href: str | None = None
        self._text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attrs_dict = {name.lower(): value or "" for name, value in attrs}
        href = attrs_dict.get("href", "").strip()
        classes = attrs_dict.get("class", "")
        if href and ("result__a" in classes or "/l/?" in href or "bing.com/ck/a" in href):
            self._href = href
            self._text_parts = []

    def handle_data(self, data: str) -> None:
        if self._href:
            self._text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._href:
            text = normalize_spaces(" ".join(self._text_parts))
            if text:
                self.results.append((self._href, text))
            self._href = None
            self._text_parts = []


class TextExtractor(HTMLParser):
    def __init__(self, selector: str | None = None) -> None:
        super().__init__(convert_charrefs=True)
        self.selector = selector
        self.parts: list[str] = []
        self.capture_stack: list[str] = []
        self.skip_depth = 0
        self.title_parts: list[str] = []
        self.in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {name.lower(): value or "" for name, value in attrs}

        if tag in SKIP_TAGS:
            self.skip_depth += 1
            return

        if tag == "title":
            self.in_title = True

        if self.selector:
            if self.capture_stack:
                self.capture_stack.append(tag)
            elif self._matches(tag, attrs_dict, self.selector):
                self.capture_stack = [tag]

        if self.is_capturing and tag in BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self.skip_depth:
            self.skip_depth -= 1
            return

        if tag == "title":
            self.in_title = False

        if self.is_capturing and tag in BLOCK_TAGS:
            self.parts.append("\n")

        if self.selector and self.capture_stack and tag in self.capture_stack:
            last_matching_index = len(self.capture_stack) - 1 - self.capture_stack[::-1].index(tag)
            self.capture_stack = self.capture_stack[:last_matching_index]

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.in_title:
            self.title_parts.append(data)
        if self.is_capturing:
            self.parts.append(data)

    @property
    def is_capturing(self) -> bool:
        return self.selector is None or bool(self.capture_stack)

    @staticmethod
    def _matches(tag: str, attrs: dict[str, str], selector: str) -> bool:
        selector = selector.strip()
        if selector.startswith("#"):
            return attrs.get("id") == selector[1:]
        if selector.startswith("."):
            classes = attrs.get("class", "").split()
            return selector[1:] in classes
        return tag == selector.lower()

    @property
    def document_title(self) -> str:
        return normalize_spaces(" ".join(self.title_parts))

    @property
    def text(self) -> str:
        return clean_text("".join(self.parts))


def clean_text(raw: str) -> str:
    raw = html.unescape(raw)
    raw = raw.replace("\u3000", " ")
    raw = re.sub(r"[ \t\r\f\v]+", " ", raw)
    raw = re.sub(r" *\n *", "\n", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    lines = [line.strip() for line in raw.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines).strip()


def normalize_plain_text(raw: str) -> str:
    raw = html.unescape(raw)
    raw = raw.replace("\ufeff", "")
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    raw = raw.replace("\u3000", " ")
    raw = re.sub(r"[ \t\f\v]+", " ", raw)
    raw = re.sub(r" *\n *", "\n", raw)
    raw = re.sub(r"\n{3,}", "\n\n", raw)
    lines = [line.rstrip() for line in raw.splitlines()]
    return "\n".join(lines).strip()


def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def looks_access_gated(markup: str, text: str = "") -> bool:
    haystack = "\n".join((markup, text))
    matches = sum(1 for pattern in GATED_PAGE_PATTERNS if pattern.search(haystack))
    return matches >= 2


def read_url_list(path: Path) -> list[str]:
    urls: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.append(line)
    return urls


def fetch_source(source: str, cookie: str | None, timeout: float, insecure: bool = False) -> str:
    parsed = urllib.parse.urlparse(source)
    if parsed.scheme in {"http", "https"}:
        request = request_url(source, cookie)
        context = ssl._create_unverified_context() if insecure else None
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                data = response.read()
                charset = response.headers.get_content_charset()
                encoding = response.headers.get("Content-Encoding", "")
        except (http.client.RemoteDisconnected, ConnectionResetError, TimeoutError, urllib.error.URLError):
            data = curl_fetch_bytes(source, cookie, timeout, insecure=insecure)
            charset = None
            encoding = ""
        data = decompress_http_body(data, encoding)
        return decode_markup_bytes(data, charset)

    local_path = Path(source).expanduser()
    return decode_markup_bytes(local_path.read_bytes())


def encode_request_url(source: str) -> str:
    parsed = urllib.parse.urlsplit(source)
    if parsed.scheme not in {"http", "https"}:
        return source
    path = urllib.parse.quote(urllib.parse.unquote(parsed.path), safe="/%")
    query = urllib.parse.quote(urllib.parse.unquote(parsed.query), safe="=&?/:+,%")
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, path, query, parsed.fragment))


def request_url(source: str, cookie: str | None, referer: str | None = None) -> urllib.request.Request:
    request = urllib.request.Request(encode_request_url(source), headers={"User-Agent": USER_AGENT})
    if cookie:
        request.add_header("Cookie", cookie)
    if referer:
        request.add_header("Referer", encode_request_url(referer))
    return request


def fetch_bytes(
    source: str,
    cookie: str | None,
    timeout: float,
    insecure: bool = False,
    referer: str | None = None,
) -> tuple[bytes, str]:
    parsed = urllib.parse.urlparse(source)
    if parsed.scheme in {"http", "https"}:
        context = ssl._create_unverified_context() if insecure else None
        try:
            with urllib.request.urlopen(
                request_url(source, cookie, referer=referer),
                timeout=timeout,
                context=context,
            ) as response:
                data = response.read()
                data = decompress_http_body(data, response.headers.get("Content-Encoding", ""))
                return data, response.headers.get_content_type()
        except (http.client.RemoteDisconnected, ConnectionResetError, TimeoutError, urllib.error.URLError):
            return curl_fetch_bytes(source, cookie, timeout, insecure=insecure, referer=referer), "application/octet-stream"

    local_path = Path(source).expanduser()
    return local_path.read_bytes(), "application/octet-stream"


def decompress_http_body(data: bytes, content_encoding: str | None) -> bytes:
    encoding = (content_encoding or "").lower()
    if "gzip" in encoding:
        return gzip.decompress(data)
    if "deflate" in encoding:
        try:
            return zlib.decompress(data)
        except zlib.error:
            return zlib.decompress(data, -zlib.MAX_WBITS)
    return data


def curl_fetch_bytes(
    source: str,
    cookie: str | None,
    timeout: float,
    insecure: bool = False,
    referer: str | None = None,
) -> bytes:
    command = [
        "curl",
        "-L",
        "--compressed",
        "--silent",
        "--show-error",
        "--max-time",
        str(max(1, int(timeout))),
        "-A",
        USER_AGENT,
    ]
    if insecure:
        command.append("-k")
    if cookie:
        command.extend(["-H", f"Cookie: {cookie}"])
    if referer:
        command.extend(["-e", referer])
    command.append(source)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        raise OSError(result.stderr.decode("utf-8", errors="replace").strip() or f"curl failed: {source}")
    return result.stdout


def unwrap_search_url(url: str) -> str:
    url = html.unescape(url)
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    for key in ("uddg", "u", "url"):
        value = query.get(key)
        if value:
            return value[0]
    return url


def absolute_links(markup: str, base_url: str, pattern: str | None = None) -> list[str]:
    parser = LinkExtractor(pattern=pattern)
    parser.feed(markup)
    seen: set[str] = set()
    links: list[str] = []
    for href in parser.links:
        absolute = urllib.parse.urljoin(base_url, href)
        if absolute not in seen:
            seen.add(absolute)
            links.append(absolute)
    return links


def jjwxc_chapter_links_from_markup(markup: str, base_url: str) -> list[str]:
    links: list[str] = []
    seen: set[str] = set()
    pattern = re.compile(
        r'''(?:href|rel)=["']([^"']*/onebook(?:_vip)?\.php\?[^"']*novelid=\d+[^"']*chapterid=\d+[^"']*)["']''',
        re.IGNORECASE,
    )
    for match in pattern.finditer(markup):
        link = html.unescape(match.group(1))
        absolute = urllib.parse.urljoin(base_url, link)
        if absolute not in seen:
            seen.add(absolute)
            links.append(absolute)
    return links


def url_extension(url: str) -> str:
    return Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).suffix.lower()


def downloadable_file_links(markup: str, base_url: str, extensions: tuple[str, ...]) -> list[str]:
    pattern = r"\.(" + "|".join(re.escape(ext.lstrip(".")) for ext in extensions) + r")(\?|$)"
    return absolute_links(markup, base_url, pattern)


def filter_dynamic_download_links(links: Iterable[str]) -> list[str]:
    filtered: list[str] = []
    for link in links:
        lower = link.lower()
        if re.search(r"(app|client|android|ios|iphone|mobile|jj-app-download)", lower):
            continue
        filtered.append(link)
    return filtered


def choose_download_link(links: list[str]) -> str | None:
    if not links:
        return None

    def score(link: str) -> tuple[int, int, int, str]:
        parsed = urllib.parse.urlparse(link)
        extension = url_extension(link)
        dynamic_download = 1 if parsed.query and re.search(r"(down|download)", parsed.path, re.IGNORECASE) else 0
        html_penalty = -1 if extension in {".html", ".htm"} else 0
        return (
            DOWNLOAD_EXTENSION_PRIORITY.get(extension, 0),
            dynamic_download,
            html_penalty,
            link,
        )

    return max(
        links,
        key=score,
    )


def sniff_download_extension(data: bytes, content_type: str) -> str:
    content_type = content_type.lower()
    if data.startswith(b"PK\x03\x04"):
        return ".zip"
    if data.startswith(b"Rar!\x1a\x07"):
        return ".rar"
    if data.startswith(b"7z\xbc\xaf\x27\x1c"):
        return ".7z"
    if "epub" in content_type:
        return ".epub"
    if "zip" in content_type:
        return ".zip"
    if "rar" in content_type:
        return ".rar"
    if "7z" in content_type:
        return ".7z"
    if content_type.startswith("text/"):
        return ".txt"
    return ""


def classify_url(url: str, args: argparse.Namespace) -> Candidate:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    title = Path(parsed.path).stem or parsed.netloc
    source_type = "unknown"
    score = 0
    reason_parts: list[str] = []
    downloadable_links: list[str] = []
    chapter_link_count = 0

    if path.endswith(".txt"):
        return Candidate(url, title, "direct-txt", 95, "URL ends with .txt", [], 0)
    if path.endswith(".epub"):
        return Candidate(url, title, "direct-epub", 90, "URL ends with .epub", [], 0)
    if path.endswith(".zip"):
        return Candidate(url, title, "direct-zip", 88, "URL ends with .zip", [], 0)
    if path.endswith((".rar", ".7z")):
        return Candidate(url, title, "unsupported-archive", 55, "Archive type needs external extractor", [], 0)

    try:
        markup = fetch_source(
            url,
            cookie=parse_cookie(args.cookie, args.cookie_file),
            timeout=args.timeout,
            insecure=args.insecure,
        )
    except (OSError, UnicodeError, urllib.error.URLError) as exc:
        return Candidate(url, title, "fetch-failed", 0, str(exc), [], 0)

    text, document_title = extract_with_selector(markup, None)
    title = document_title or extract_title(markup, None, url, 1)
    if looks_access_gated(markup, text):
        return Candidate(url, title, "access-gated", 0, "login/password/captcha placeholder detected", [], 0)

    downloadable_links = downloadable_file_links(markup, url, DOWNLOAD_EXTENSIONS)
    dynamic_download_links = (
        filter_dynamic_download_links(absolute_links(markup, url, args.download_link_regex))
        if getattr(args, "download_link_regex", None)
        else []
    )
    chapter_links = absolute_links(
        markup,
        url,
        r"(chapter|read|view|book|html|\d{3,})",
    )
    same_host_chapters = [
        link
        for link in chapter_links
        if urllib.parse.urlparse(link).netloc == parsed.netloc
    ]
    chapter_link_count = len(same_host_chapters)

    if downloadable_links or dynamic_download_links:
        extensions = {Path(urllib.parse.urlparse(link).path).suffix.lower() for link in downloadable_links}
        if ".txt" in extensions:
            source_type = "download-page-txt"
            score = 86
        elif ".epub" in extensions:
            source_type = "download-page-epub"
            score = 82
        elif ".zip" in extensions:
            source_type = "download-page-zip"
            score = 80
        elif extensions & {".rar", ".7z"}:
            source_type = "download-page-unsupported-archive"
            score = 48
        elif dynamic_download_links:
            source_type = "download-page-dynamic"
            score = 84
        reason_parts.append(f"{len(downloadable_links)} downloadable link(s), {len(dynamic_download_links)} dynamic download link(s)")

    if chapter_link_count >= args.min_chapter_links:
        if score < 75:
            source_type = "toc"
            score = 75
        reason_parts.append(f"{chapter_link_count} likely chapter links")

    if source_type == "unknown":
        if re.search(r"目录|章节|正文|最新章节|全文阅读|txt下载|全集下载", text):
            source_type = "possible-novel-page"
            score = 35
            reason_parts.append("novel keywords found")
        else:
            reason_parts.append("no clear download or TOC signal")

    return Candidate(url, title, source_type, score, "; ".join(reason_parts), downloadable_links[:20], chapter_link_count)


def search_web(title: str, args: argparse.Namespace) -> list[tuple[str, str]]:
    query_variants = [
        f"{title} txt 下载 全本 精校",
        f"{title} txt 全本",
        f"{title} 全文阅读",
        f"{title} 小说",
    ]
    results: list[tuple[str, str]] = []
    seen: set[str] = set()

    for query in query_variants:
        search_urls = [
            "https://duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query}),
            "https://www.bing.com/search?" + urllib.parse.urlencode({"q": query}),
        ]

        for search_url in search_urls:
            last_error: Exception | None = None
            for attempt in range(1, args.retries + 2):
                try:
                    markup = fetch_source(search_url, cookie=None, timeout=args.timeout, insecure=args.insecure)
                    parser = SearchResultExtractor()
                    parser.feed(markup)
                    before_count = len(results)
                    for href, label in parser.results:
                        url = unwrap_search_url(href)
                        parsed = urllib.parse.urlparse(url)
                        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
                            continue
                        if "duckduckgo.com" in parsed.netloc or "bing.com" in parsed.netloc:
                            continue
                        if url not in seen:
                            seen.add(url)
                            results.append((url, label))
                        if len(results) >= args.discover_max:
                            return results
                    if len(results) > before_count:
                        break
                    break
                except (OSError, UnicodeError, urllib.error.URLError) as exc:
                    last_error = exc
                    if attempt <= args.retries:
                        print(f"[RETRY] search attempt {attempt}/{args.retries}: {exc}", file=sys.stderr)
                        time.sleep(args.retry_delay)
                    else:
                        print(f"[SEARCH FAIL] {search_url}: {last_error}", file=sys.stderr)
    return results


def discover_title(args: argparse.Namespace) -> int:
    results = search_web(args.discover_title, args)
    candidates: list[Candidate] = []
    for url, label in results:
        candidate = classify_url(url, args)
        if not candidate.title:
            candidate.title = label
        candidates.append(candidate)
        print(f"[{candidate.source_type}] score={candidate.score} {candidate.url}", file=sys.stderr)
        if args.delay:
            time.sleep(args.delay)

    candidates.sort(key=lambda item: item.score, reverse=True)
    payload = {
        "title": args.discover_title,
        "count": len(candidates),
        "candidates": [candidate.__dict__ for candidate in candidates],
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote {len(candidates)} candidates to {args.output}", file=sys.stderr)
    else:
        print(text)
    return 0 if candidates else 1


def probe_url(args: argparse.Namespace) -> int:
    candidate = classify_url(args.probe_url, args)
    text = json.dumps(candidate.__dict__, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote probe result to {args.output}", file=sys.stderr)
    else:
        print(text)
    return 0 if candidate.score > 0 else 1


def safe_download_path(url: str, args: argparse.Namespace) -> Path:
    if args.download_output:
        return args.download_output
    extension = url_extension(url)
    if args.output:
        return args.output.with_suffix(extension or ".bin")
    name = Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).name
    if not name:
        name = "download.bin"
    return Path(name)


def download_file_candidate(args: argparse.Namespace) -> tuple[str, Path, str]:
    cookie = parse_cookie(args.cookie, args.cookie_file)
    referer = args.referer
    source_url = args.download_file_url

    if args.download_file_from:
        referer = referer or args.download_file_from
        markup = fetch_source(
            args.download_file_from,
            cookie=cookie,
            timeout=args.timeout,
            insecure=args.insecure,
        )
        text, _ = extract_with_selector(markup, None)
        if not args.allow_gated_text and looks_access_gated(markup, text):
            raise SystemExit("Download page looks access-gated.")
        extensions = tuple(
            ext.strip() if ext.strip().startswith(".") else f".{ext.strip()}"
            for ext in args.download_extensions.split(",")
            if ext.strip()
        )
        source_url = choose_download_link(downloadable_file_links(markup, args.download_file_from, extensions))
        if not source_url and args.download_link_regex:
            source_url = choose_download_link(
                absolute_links(markup, args.download_file_from, args.download_link_regex)
            )
        if not source_url:
            raise SystemExit("No downloadable file link found on page.")

    if not source_url:
        raise SystemExit("Provide --download-file-url or --download-file-from.")

    follow_hops = 0
    last_error: Exception | None = None
    while True:
        output_path = safe_download_path(source_url, args)
        followed_html = False
        for attempt in range(1, args.retries + 2):
            try:
                data, content_type = fetch_bytes(
                    source_url,
                    cookie=cookie,
                    timeout=args.timeout,
                    insecure=args.insecure,
                    referer=referer,
                )
                if content_type.lower().startswith("text/html") and follow_hops < args.download_follow_html:
                    markup = decode_markup_bytes(data)
                    next_links = downloadable_file_links(markup, source_url, DOWNLOAD_EXTENSIONS)
                    if args.download_link_regex:
                        next_links.extend(absolute_links(markup, source_url, args.download_link_regex))
                    next_url = choose_download_link(next_links)
                    if next_url and next_url != source_url:
                        print(f"[FOLLOW] HTML landing page -> {next_url}", file=sys.stderr)
                        referer = source_url
                        source_url = next_url
                        follow_hops += 1
                        followed_html = True
                        break

                detected_extension = url_extension(source_url) or sniff_download_extension(data, content_type)
                if detected_extension and not output_path.suffix:
                    output_path = output_path.with_suffix(detected_extension)
                if detected_extension and output_path.suffix == ".bin":
                    output_path = output_path.with_suffix(detected_extension)
                output_path.write_bytes(data)
                print(
                    f"Wrote download to {output_path} ({len(data)} bytes, {content_type})",
                    file=sys.stderr,
                )
                return source_url, output_path, detected_extension
            except (OSError, urllib.error.URLError) as exc:
                last_error = exc
                if attempt <= args.retries:
                    print(f"[RETRY] download attempt {attempt}/{args.retries}: {exc}", file=sys.stderr)
                    time.sleep(args.retry_delay)
                else:
                    raise SystemExit(f"Download failed: {last_error}")
        if not followed_html:
            break

    raise SystemExit(f"Download failed: {last_error}")


def download_file(args: argparse.Namespace) -> int:
    source_url, output_path, detected_extension = download_file_candidate(args)
    extension = detected_extension or url_extension(source_url) or output_path.suffix.lower()

    if args.no_auto_convert_download or not args.output:
        print(f"Selected file URL: {source_url}", file=sys.stderr)
        return 0

    if extension == ".txt":
        args.normalize_txt = output_path
        return normalize_existing_txt(args)
    if extension == ".epub":
        args.extract_epub = output_path
        return extract_epub(args)
    if extension == ".zip":
        args.extract_zip = output_path
        return extract_zip(args)
    if extension in {".rar", ".7z"}:
        args.extract_archive = output_path
        return extract_archive(args)

    print(
        f"Saved {extension or 'unknown'} file but automatic conversion is not supported.",
        file=sys.stderr,
    )
    return 1


def extract_with_selector(markup: str, selector: str | None) -> tuple[str, str]:
    parser = TextExtractor(selector=selector)
    parser.feed(markup)
    return parser.text, parser.document_title


def html_fragment_to_text(fragment: str) -> str:
    fragment = re.sub(r"(?i)<br\s*/?>", "\n", fragment)
    fragment = re.sub(r"(?i)</p\s*>", "\n", fragment)
    fragment = re.sub(r"(?i)</div\s*>", "\n", fragment)
    fragment = re.sub(r"(?is)<(script|style|noscript|svg|canvas|iframe|form)\b.*?</\1>", " ", fragment)
    fragment = re.sub(r"(?is)<[^>]+>", " ", fragment)
    return clean_text(fragment)


def extract_jjwxc_official(markup: str) -> tuple[str, str]:
    body_match = re.search(
        r'<div\s+class=["\']novelbody["\'][^>]*>',
        markup,
        flags=re.IGNORECASE,
    )
    if not body_match:
        raise ValueError("JJWXC official body not found")

    body_start = body_match.end()
    tail = markup[body_start:]
    title = ""
    title_match = re.search(r"<h2[^>]*>(.*?)</h2>", tail, flags=re.IGNORECASE | re.DOTALL)
    if title_match:
        title = clean_text(re.sub(r"<[^>]+>", " ", title_match.group(1)))

    if title_match:
        after_title_offset = body_start + title_match.end()
        clear_match = re.search(
            r'<div\b[^>]*style=["\'][^"\']*clear\s*:\s*both[^"\']*["\'][^>]*>\s*</div>',
            markup[after_title_offset:],
            flags=re.IGNORECASE | re.DOTALL,
        )
        start = after_title_offset + (clear_match.end() if clear_match else 0)
    else:
        start = body_start

    end_markers = [
        r'<div\s+id=["\']favoriteshow_3["\']',
        r'<div\s+align=["\']right["\']',
        r'<div\s+id=["\']note_danmu_wrapper["\']',
        r'<div\s+class=["\']note_chapter_title["\']',
    ]
    end_candidates: list[int] = []
    for marker in end_markers:
        match = re.search(marker, markup[start:], flags=re.IGNORECASE)
        if match:
            end_candidates.append(start + match.start())
    if not end_candidates:
        next_body = re.search(
            r'<div\s+class=["\']novelbody["\'][^>]*>',
            markup[start:],
            flags=re.IGNORECASE,
        )
        if next_body:
            end_candidates.append(start + next_body.start())
    end = min(end_candidates) if end_candidates else len(markup)

    text = html_fragment_to_text(markup[start:end])
    if not text:
        raise ValueError("JJWXC official text not found")
    return text, title


def extract_content(markup: str, args: argparse.Namespace) -> tuple[str, str]:
    if args.content_mode == "jjwxc":
        return extract_jjwxc_official(markup)
    return extract_with_selector(markup, args.content_selector)


def extract_title(
    markup: str,
    title_selector: str | None,
    fallback: str,
    index: int,
    title_regex: str | None = None,
    text_hint: str | None = None,
) -> str:
    heading_candidates: list[str] = []
    for pattern in (
        r"<h1[^>]*>(.*?)</h1>",
        r"<h2[^>]*>(.*?)</h2>",
        r"<title[^>]*>(.*?)</title>",
    ):
        for match in re.finditer(pattern, markup, flags=re.IGNORECASE | re.DOTALL):
            title = clean_text(re.sub(r"<[^>]+>", " ", match.group(1)))
            if title:
                heading_candidates.append(title)

    if title_regex:
        pattern = re.compile(title_regex)
        for candidate in heading_candidates + [
            clean_text(re.sub(r"<[^>]+>", "\n", markup)),
            text_hint or "",
        ]:
            if not candidate:
                continue
            match = pattern.search(candidate)
            if match:
                return normalize_spaces(match.group(1) if match.groups() else match.group(0))

    if title_selector:
        selected, _ = extract_with_selector(markup, title_selector)
        first_line = selected.splitlines()[0] if selected else ""
        if first_line:
            return first_line

    if heading_candidates:
        return heading_candidates[0]

    name = Path(urllib.parse.urlparse(fallback).path).stem
    return normalize_spaces(name) or f"Chapter {index}"


def filter_lines(
    text: str,
    start_after: str | None,
    start_after_last: str | None,
    end_before: str | None,
    drop_line: list[str] | None,
    remove_regex: list[str] | None,
    dedupe_adjacent_lines: bool = False,
    drop_common_boilerplate: bool = True,
    keep_private_use: bool = False,
) -> str:
    if remove_regex:
        for pattern in remove_regex:
            text = re.sub(pattern, "", text)
    if drop_common_boilerplate:
        for pattern in COMMON_SOURCE_INLINE_PATTERNS:
            text = re.sub(pattern, "", text)
    if not keep_private_use:
        text = re.sub(r"[\uE000-\uF8FF]", "", text)

    lines = text.splitlines()

    if start_after:
        pattern = re.compile(start_after)
        for offset, line in enumerate(lines):
            if pattern.search(line):
                lines = lines[offset + 1 :]
                break

    if start_after_last:
        pattern = re.compile(start_after_last)
        last_offset: int | None = None
        for offset, line in enumerate(lines):
            if pattern.search(line):
                last_offset = offset
        if last_offset is not None:
            lines = lines[last_offset + 1 :]

    if end_before:
        pattern = re.compile(end_before)
        for offset, line in enumerate(lines):
            if pattern.search(line):
                lines = lines[:offset]
                break

    drop_patterns = list(drop_line or [])
    if drop_common_boilerplate:
        drop_patterns.extend(COMMON_SOURCE_BOILERPLATE_PATTERNS)

    if drop_patterns:
        patterns = [re.compile(pattern) for pattern in drop_patterns]
        lines = [
            line
            for line in lines
            if not any(pattern.search(line) for pattern in patterns)
        ]

    if drop_common_boilerplate:
        while lines and (not lines[0].strip() or DECORATIVE_EDGE_LINE.match(lines[0].strip())):
            lines.pop(0)
        while lines and (not lines[-1].strip() or DECORATIVE_EDGE_LINE.match(lines[-1].strip())):
            lines.pop()

    if dedupe_adjacent_lines:
        deduped: list[str] = []
        previous = ""
        for line in lines:
            current = normalize_spaces(line)
            if current and current != previous:
                deduped.append(line)
            previous = current
        lines = deduped

    return "\n".join(lines).strip()


def parse_cookie(cookie: str | None, cookie_file: Path | None) -> str | None:
    if cookie:
        return cookie.strip()
    if not cookie_file:
        return None

    text = cookie_file.read_text(encoding="utf-8", errors="replace")
    pairs: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "\t" in line:
            fields = line.split("\t")
            if len(fields) >= 7:
                pairs.append(f"{fields[5]}={fields[6]}")
        elif "=" in line:
            pairs.append(line)
    return "; ".join(pairs) if pairs else None


def extract_links(args: argparse.Namespace) -> int:
    if not args.extract_links_from:
        raise SystemExit("--extract-links-from is required in link extraction mode.")

    cookie = parse_cookie(args.cookie, args.cookie_file)
    seen: set[str] = set()
    links: list[str] = []
    for source in args.extract_links_from:
        base_url = args.base_url or source
        markup = fetch_source(
            source,
            cookie=cookie,
            timeout=args.timeout,
            insecure=args.insecure,
        )
        parser = LinkExtractor(pattern=args.link_regex)
        parser.feed(markup)
        for href in parser.links:
            absolute = urllib.parse.urljoin(base_url, href)
            if absolute not in seen:
                seen.add(absolute)
                links.append(absolute)

    if args.link_sort_numeric:
        regex = re.compile(args.link_sort_numeric)

        def sort_key(url: str) -> tuple[int, str]:
            match = regex.search(url)
            return (int(match.group(1)) if match else 0, url)

        links.sort(key=sort_key)

    if args.output:
        args.output.write_text("\n".join(links) + ("\n" if links else ""), encoding="utf-8")
        print(f"Wrote {len(links)} links to {args.output}", file=sys.stderr)
    else:
        for link in links:
            print(link)
    return 0 if links else 1


def numeric_tail(value: str) -> int:
    matches = re.findall(r"(\d+)", value)
    return int(matches[-1]) if matches else 0


def auto_chapter_links_from_toc(source: str, args: argparse.Namespace) -> list[str]:
    markup = fetch_source(
        source,
        cookie=parse_cookie(args.cookie, args.cookie_file),
        timeout=args.timeout,
        insecure=args.insecure,
    )
    base_url = args.base_url or source
    base = urllib.parse.urlparse(base_url)
    source_query = dict(urllib.parse.parse_qsl(base.query))
    source_novelid = source_query.get("novelid", "")
    links = absolute_links(markup, base_url) + jjwxc_chapter_links_from_markup(markup, base_url)
    groups: dict[str, list[str]] = {}
    sort_keys: dict[str, int] = {}
    seen: set[str] = set()
    for order, link in enumerate(links):
        parsed = urllib.parse.urlparse(link)
        if link in seen:
            continue
        seen.add(link)

        query = dict(urllib.parse.parse_qsl(parsed.query))
        is_jjwxc_chapter = (
            parsed.path.lower().endswith(("/onebook.php", "/onebook_vip.php"))
            and "novelid" in query
            and "chapterid" in query
            and (not source_novelid or query.get("novelid") == source_novelid)
        )
        if "chapterid" in query and (parsed.netloc == base.netloc or is_jjwxc_chapter):
            novel_key = query.get("novelid", "")
            group_key = (
                f"jjwxc?novelid={novel_key}&chapterid=*"
                if is_jjwxc_chapter
                else f"{parsed.path}?novelid={novel_key}&chapterid=*"
            )
            groups.setdefault(group_key, []).append(link)
            sort_keys[link] = int(query.get("chapterid") or 0)
            continue

        path_lower = parsed.path.lower()
        is_chapter_slug_path = (
            parsed.netloc == base.netloc
            and re.search(r"/chapters?/[^/]+/?$", path_lower)
        )
        if is_chapter_slug_path:
            group_key = re.sub(r"/chapters?/[^/]+/?$", "/chapters/*", parsed.path)
            groups.setdefault(group_key, []).append(link)
            sort_keys[link] = order
            continue

        if not re.search(r"\d", parsed.path) or not path_lower.endswith((".html", ".htm", "/")):
            continue
        group_key = posixpath.dirname(parsed.path.rstrip("/"))
        groups.setdefault(group_key, []).append(link)
        sort_keys[link] = numeric_tail(parsed.path)

    if not groups:
        return []

    _, best = max(groups.items(), key=lambda item: len(item[1]))
    best.sort(key=lambda link: (sort_keys.get(link, numeric_tail(urllib.parse.urlparse(link).path)), link))
    return best


def extract_chapter_links_auto(args: argparse.Namespace) -> int:
    best = auto_chapter_links_from_toc(args.extract_chapter_links_auto_from, args)
    if not best:
        raise SystemExit("No likely chapter-link groups found.")

    if len(best) < args.min_chapter_links:
        print(
            f"Warning: best group has only {len(best)} links; inspect before full download.",
            file=sys.stderr,
        )

    if args.output:
        args.output.write_text("\n".join(best) + ("\n" if best else ""), encoding="utf-8")
        print(f"Wrote {len(best)} auto-detected chapter links to {args.output}", file=sys.stderr)
    else:
        for link in best:
            print(link)
    return 0 if best else 1


def generate_url_template(args: argparse.Namespace) -> int:
    if args.range_start is None or args.range_end is None:
        raise SystemExit("--range-start and --range-end are required with --generate-url-template.")
    if args.range_end < args.range_start:
        raise SystemExit("--range-end must be greater than or equal to --range-start.")

    urls: list[str] = []
    for number in range(args.range_start, args.range_end + 1):
        if "{n}" in args.generate_url_template:
            url = args.generate_url_template.replace("{n}", str(number))
        else:
            url = args.generate_url_template.format(number)
        urls.append(url)

    if args.output:
        args.output.write_text("\n".join(urls) + "\n", encoding="utf-8")
        print(f"Wrote {len(urls)} generated URLs to {args.output}", file=sys.stderr)
    else:
        for url in urls:
            print(url)
    return 0


def linked_pages(markup: str, source: str, pattern: str, sort_numeric: str | None) -> list[str]:
    parser = LinkExtractor(pattern=pattern)
    parser.feed(markup)

    seen = {source}
    pages = [source]
    for href in parser.links:
        absolute = urllib.parse.urljoin(source, href)
        if absolute not in seen:
            seen.add(absolute)
            pages.append(absolute)

    if sort_numeric:
        regex = re.compile(sort_numeric)

        def sort_key(url: str) -> tuple[int, str]:
            match = regex.search(url)
            return (int(match.group(1)) if match else 1, url)

        pages.sort(key=sort_key)

    return pages


def download_chapters(args: argparse.Namespace) -> tuple[list[Chapter], list[tuple[str, str]]]:
    sources = list(args.url or [])
    if args.urls_file:
        sources.extend(read_url_list(args.urls_file))
    if not sources:
        raise SystemExit("Provide at least one --url or --urls-file.")

    cookie = parse_cookie(args.cookie, args.cookie_file)
    chapters: list[Chapter] = []
    failures: list[tuple[str, str]] = []
    consecutive_failures = 0

    for index, source in enumerate(sources, start=1):
        chapter: Chapter | None = None
        success = False
        last_error: Exception | None = None
        for attempt in range(1, args.retries + 2):
            try:
                markup = fetch_source(source, cookie=cookie, timeout=args.timeout, insecure=args.insecure)
                page_sources = (
                    linked_pages(markup, source, args.page_link_regex, args.page_link_sort_numeric)
                    if args.page_link_regex
                    else [source]
                )
                page_texts: list[str] = []
                for page_source in page_sources:
                    page_markup = markup if page_source == source else fetch_source(
                        page_source,
                        cookie=cookie,
                        timeout=args.timeout,
                        insecure=args.insecure,
                    )
                    page_text, page_title = extract_content(page_markup, args)
                    if not args.allow_gated_text and looks_access_gated(page_markup, page_text):
                        raise ValueError("access-gated placeholder detected")
                    page_texts.append(page_text)
                text = filter_lines(
                    "\n".join(page_texts),
                    args.start_after,
                    args.start_after_last,
                    args.end_before,
                    args.drop_line,
                    args.remove_regex,
                    args.dedupe_adjacent_lines,
                    not args.keep_source_boilerplate,
                    args.keep_private_use,
                )
                title = extract_title(
                    markup,
                    args.title_selector,
                    source,
                    index,
                    title_regex=args.title_regex,
                    text_hint=text,
                )
                if page_title and args.content_mode == "jjwxc":
                    title = page_title
                if not text:
                    raise ValueError("no extractable text")
                chapter = Chapter(source=source, title=title, text=text)
                chapters.append(chapter)
                success = True
                consecutive_failures = 0
                print(f"[OK] {index}/{len(sources)} {title}", file=sys.stderr)
                break
            except (OSError, UnicodeError, urllib.error.URLError, ValueError) as exc:
                last_error = exc
                if attempt <= args.retries:
                    print(
                        f"[RETRY] {index}/{len(sources)} attempt {attempt}/{args.retries}: {source}: {exc}",
                        file=sys.stderr,
                    )
                    time.sleep(args.retry_delay)
                else:
                    failures.append((source, str(exc)))
                    consecutive_failures += 1
                    print(f"[FAIL] {index}/{len(sources)} {source}: {exc}", file=sys.stderr)

        if args.flush_each and chapter:
            write_txt(args.output, args.title, chapters)

        if (
            not success
            and args.stop_after_consecutive_failures
            and consecutive_failures >= args.stop_after_consecutive_failures
        ):
            print(
                f"Stopping after {consecutive_failures} consecutive failures.",
                file=sys.stderr,
            )
            break

        if args.delay and index < len(sources):
            time.sleep(args.delay + (random.uniform(0, args.delay_jitter) if args.delay_jitter else 0))

    if failures and args.failure_output:
        args.failure_output.write_text(
            "\n".join(source for source, _ in failures) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {len(failures)} failed source URL(s) to {args.failure_output}", file=sys.stderr)

    return chapters, failures


def write_txt(path: Path, novel_title: str | None, chapters: list[Chapter]) -> None:
    chunks: list[str] = []
    if novel_title:
        chunks.append(novel_title.strip())
    for chapter in chapters:
        text = chapter.text
        lines = text.splitlines()
        if lines and normalize_spaces(lines[0]) == normalize_spaces(chapter.title):
            text = "\n".join(lines[1:]).strip()
        chunks.append(f"{chapter.title}\n\n{text}")
    path.write_text("\n\n\n".join(chunks).strip() + "\n", encoding="utf-8")


def clean_existing_txt(args: argparse.Namespace) -> int:
    if not args.output:
        raise SystemExit("--output is required with --clean-txt.")

    raw = decode_plain_bytes(args.clean_txt.read_bytes(), args.input_encoding)
    blocks = [block.strip() for block in re.split(r"\n{3,}", raw) if block.strip()]
    if not blocks:
        raise SystemExit("No text blocks found.")

    novel_title = args.title or blocks[0].splitlines()[0].strip()
    cleaned: list[Chapter] = []
    title_pattern = re.compile(args.title_regex) if args.title_regex else None

    for index, block in enumerate(blocks[1:], start=1):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        title = lines[0]
        body_lines = lines[1:]

        if title_pattern and (title in {"阅读页", "正文", "目录"} or not title_pattern.search(title)):
            for offset, line in enumerate(body_lines):
                match = title_pattern.search(line)
                if match:
                    title = normalize_spaces(match.group(1) if match.groups() else match.group(0))
                    body_lines = body_lines[offset + 1 :]
                    break

        text = "\n".join(body_lines)
        text = filter_lines(
            text,
            args.start_after,
            args.start_after_last,
            args.end_before,
            args.drop_line,
            args.remove_regex,
            args.dedupe_adjacent_lines,
            not args.keep_source_boilerplate,
            args.keep_private_use,
        )
        if text:
            cleaned.append(Chapter(source=f"block-{index}", title=title, text=text))

    write_txt(args.output, novel_title, cleaned)
    print(f"Wrote {len(cleaned)} cleaned chapters to {args.output}", file=sys.stderr)
    return 0 if cleaned else 1


def normalize_existing_txt(args: argparse.Namespace) -> int:
    if not args.output:
        raise SystemExit("--output is required with --normalize-txt.")

    raw = decode_plain_bytes(args.normalize_txt.read_bytes(), args.input_encoding)
    text = normalize_plain_text(raw)
    text = filter_lines(
        text,
        args.start_after,
        args.start_after_last,
        args.end_before,
        args.drop_line,
        args.remove_regex,
        args.dedupe_adjacent_lines,
        not args.keep_source_boilerplate,
        args.keep_private_use,
    )
    if args.title:
        lines = [line for line in text.splitlines() if line.strip()]
        if not lines or normalize_spaces(lines[0]) != normalize_spaces(args.title):
            text = f"{args.title.strip()}\n\n{text}".strip()
    args.output.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"Wrote normalized TXT to {args.output}", file=sys.stderr)
    return 0 if text else 1


def decoded_text_score(text: str) -> int:
    replacement = text.count("\ufffd")
    private_use = len(re.findall(r"[\uE000-\uF8FF]", text))
    mojibake_markers = sum(text.count(marker) for marker in ("锟", "斤拷", "Ã", "Â", "Ð", "Ñ"))
    controls = len(re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text))
    return replacement * 1000 + private_use * 50 + mojibake_markers * 20 + controls * 10


def decode_plain_bytes(data: bytes, preferred_encoding: str | None = None) -> str:
    candidates: list[str] = []
    if preferred_encoding:
        candidates.append(preferred_encoding)
    candidates.extend(["utf-8", "gb18030", "gbk", "big5"])

    seen: set[str] = set()
    decoded_candidates: list[tuple[int, int, str]] = []
    for encoding in candidates:
        if encoding in seen:
            continue
        seen.add(encoding)
        try:
            text = data.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
        preference_penalty = 0 if encoding == preferred_encoding else 1
        decoded_candidates.append((decoded_text_score(text), preference_penalty, text))

    if decoded_candidates:
        decoded_candidates.sort(key=lambda item: (item[0], item[1]))
        return decoded_candidates[0][2]
    return data.decode(preferred_encoding or "utf-8", errors="replace")


def decode_markup_bytes(data: bytes, preferred_encoding: str | None = None) -> str:
    head = data[:1000].decode("ascii", errors="ignore")
    match = re.search(r'charset=["\']?([A-Za-z0-9._-]+)', head, flags=re.IGNORECASE)
    candidates = []
    if preferred_encoding:
        candidates.append(preferred_encoding)
    if match:
        candidates.append(match.group(1))
    candidates.extend(["utf-8", "gb18030"])
    for encoding in candidates:
        try:
            return data.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
    return data.decode("utf-8", errors="replace")


def epub_rootfile(archive: zipfile.ZipFile) -> str:
    container = ElementTree.fromstring(archive.read("META-INF/container.xml"))
    for element in container.iter():
        if element.tag.endswith("rootfile") and element.attrib.get("full-path"):
            return element.attrib["full-path"]
    raise ValueError("EPUB container does not define a rootfile")


def looks_epub_navigation_text(text: str) -> bool:
    lines = [normalize_spaces(line) for line in text.splitlines() if normalize_spaces(line)]
    if not lines:
        return True

    first = lines[0].lower()
    if first in {"bookcover", "cover", "封面", "总目录", "目录", "contents", "table of contents"}:
        return True
    if any("返回总目录" in line or "返回目录" in line for line in lines):
        return True

    heading_regex = re.compile(
        r"^(楔子|序章|尾声|番外|第[一二三四五六七八九十百千万零〇0-9]+[章节回卷集部])"
    )
    heading_count = sum(1 for line in lines if heading_regex.search(line))
    prose_count = sum(1 for line in lines if len(line) >= 50 and not heading_regex.search(line))
    return len(lines) <= 80 and heading_count >= 3 and prose_count == 0


def extract_epub(args: argparse.Namespace) -> int:
    if not args.output:
        raise SystemExit("--output is required with --extract-epub.")

    chapters: list[str] = []
    with zipfile.ZipFile(args.extract_epub) as archive:
        rootfile = epub_rootfile(archive)
        opf_dir = posixpath.dirname(rootfile)
        opf = ElementTree.fromstring(archive.read(rootfile))
        manifest: dict[str, str] = {}

        for element in opf.iter():
            if element.tag.endswith("item"):
                item_id = element.attrib.get("id")
                href = element.attrib.get("href")
                media_type = element.attrib.get("media-type", "")
                if item_id and href and (
                    "html" in media_type or href.lower().endswith((".html", ".xhtml", ".htm"))
                ):
                    manifest[item_id] = posixpath.normpath(posixpath.join(opf_dir, href))

        for element in opf.iter():
            if not element.tag.endswith("itemref"):
                continue
            item_path = manifest.get(element.attrib.get("idref", ""))
            if not item_path:
                continue
            markup = decode_markup_bytes(archive.read(item_path))
            text, _ = extract_with_selector(markup, args.content_selector)
            text = filter_lines(
                text,
                args.start_after,
                args.start_after_last,
                args.end_before,
                args.drop_line,
                args.remove_regex,
                args.dedupe_adjacent_lines,
                not args.keep_source_boilerplate,
                args.keep_private_use,
            )
            if not args.keep_epub_navigation and looks_epub_navigation_text(text):
                continue
            if text and len(text) >= args.min_section_chars:
                chapters.append(text)

    output = "\n\n\n".join(([args.title.strip()] if args.title else []) + chapters).strip()
    args.output.write_text(output + "\n", encoding="utf-8")
    print(f"Wrote {len(chapters)} EPUB text sections to {args.output}", file=sys.stderr)
    return 0 if chapters else 1


def zip_text_members(archive: zipfile.ZipFile, member_regex: str | None) -> list[zipfile.ZipInfo]:
    pattern = re.compile(member_regex) if member_regex else None
    members = [
        info
        for info in archive.infolist()
        if not info.is_dir()
        and info.filename.lower().endswith(".txt")
        and (not pattern or pattern.search(info.filename))
    ]
    if pattern:
        return members
    return sorted(members, key=lambda info: info.file_size, reverse=True)[:1]


def extract_zip(args: argparse.Namespace) -> int:
    if not args.output:
        raise SystemExit("--output is required with --extract-zip.")

    sections: list[str] = []
    with zipfile.ZipFile(args.extract_zip) as archive:
        members = zip_text_members(archive, args.zip_member_regex)
        if not members:
            raise SystemExit("No matching .txt members found in ZIP.")

        for member in members:
            raw = archive.read(member)
            text = normalize_plain_text(decode_plain_bytes(raw, args.input_encoding))
            text = filter_lines(
                text,
                args.start_after,
                args.start_after_last,
                args.end_before,
                args.drop_line,
                args.remove_regex,
                args.dedupe_adjacent_lines,
                not args.keep_source_boilerplate,
                args.keep_private_use,
            )
            if text and len(text) >= args.min_section_chars:
                sections.append(text)

    output = "\n\n\n".join(([args.title.strip()] if args.title else []) + sections).strip()
    args.output.write_text(output + "\n", encoding="utf-8")
    print(f"Wrote {len(sections)} ZIP text member(s) to {args.output}", file=sys.stderr)
    return 0 if sections else 1


def archive_member_pattern(args: argparse.Namespace) -> str | None:
    return args.archive_member_regex or args.zip_member_regex


def external_archive_txt_members(path: Path, member_regex: str | None) -> list[tuple[str, bytes]]:
    bsdtar = shutil.which("bsdtar")
    if not bsdtar:
        raise SystemExit("RAR/7z extraction requires bsdtar, unar, or 7z; none were found.")

    listing = subprocess.run(
        [bsdtar, "-tf", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    pattern = re.compile(member_regex) if member_regex else None
    member_names = [
        line.strip()
        for line in listing.stdout.splitlines()
        if line.strip()
        and line.strip().lower().endswith(".txt")
        and (not pattern or pattern.search(line.strip()))
    ]
    if not member_names:
        return []

    extracted: list[tuple[str, bytes]] = []
    for member_name in member_names:
        result = subprocess.run(
            [bsdtar, "-xOf", str(path), member_name],
            check=True,
            capture_output=True,
        )
        extracted.append((member_name, result.stdout))
    if pattern:
        return extracted
    return sorted(extracted, key=lambda item: len(item[1]), reverse=True)[:1]


def extract_archive(args: argparse.Namespace) -> int:
    if not args.output:
        raise SystemExit("--output is required with --extract-archive.")

    sections: list[str] = []
    for member_name, raw in external_archive_txt_members(
        args.extract_archive,
        archive_member_pattern(args),
    ):
        text = normalize_plain_text(decode_plain_bytes(raw, args.input_encoding))
        text = filter_lines(
            text,
            args.start_after,
            args.start_after_last,
            args.end_before,
            args.drop_line,
            args.remove_regex,
            args.dedupe_adjacent_lines,
            not args.keep_source_boilerplate,
            args.keep_private_use,
        )
        if text and len(text) >= args.min_section_chars:
            sections.append(text)
            print(f"[OK] extracted archive member {member_name}", file=sys.stderr)

    if not sections:
        raise SystemExit("No matching TXT members found in archive.")

    output = "\n\n\n".join(([args.title.strip()] if args.title else []) + sections).strip()
    args.output.write_text(output + "\n", encoding="utf-8")
    print(f"Wrote {len(sections)} archive text member(s) to {args.output}", file=sys.stderr)
    return 0


def parse_txt_chapters(path: Path, title_regex: str | None = None) -> tuple[str | None, list[Chapter]]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    blocks = [block.strip() for block in re.split(r"\n{3,}", raw) if block.strip()]
    if not blocks:
        return None, []

    title_pattern = re.compile(title_regex or r"^第[0-9]+[章节回].*")
    novel_title = blocks[0].splitlines()[0].strip()
    chapters: list[Chapter] = []

    for block in blocks[1:]:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        title = lines[0]
        body_lines = lines[1:]
        if not title_pattern.search(title):
            continue
        text = "\n".join(body_lines).strip()
        if text:
            chapters.append(Chapter(source=str(path), title=title, text=text))
    return novel_title, chapters


def merge_txt(args: argparse.Namespace) -> int:
    if not args.output:
        raise SystemExit("--output is required with --merge-txt.")

    by_number: dict[int, Chapter] = {}
    novel_title = args.title
    title_number = re.compile(args.chapter_number_regex)

    for path in args.merge_txt:
        detected_title, chapters = parse_txt_chapters(path, args.title_regex)
        if not novel_title and detected_title:
            novel_title = detected_title
        for chapter in chapters:
            match = title_number.search(chapter.title)
            if match:
                by_number[int(match.group(1))] = chapter

    merged = [by_number[number] for number in sorted(by_number)]
    write_txt(args.output, novel_title, merged)
    print(f"Wrote {len(merged)} merged chapters to {args.output}", file=sys.stderr)
    return 0 if merged else 1


def sample_lines(lines: list[str], start: int, count: int = 8) -> list[str]:
    return [line for line in lines[start : start + count] if line.strip()]


def detect_numeric_chapter_headings(lines: list[str], max_number: int | None = None) -> list[tuple[int, int, str]]:
    results: list[tuple[int, int, str]] = []
    seen_lines: set[int] = set()
    patterns = [
        re.compile(r"^\s*0*(\d{1,5})\s*[、,，.]\s*第"),
        re.compile(r"^\s*0*(\d{1,5})\D{0,8}第"),
        re.compile(r"^\s*第\s*0*(\d{1,5})\s*[章节回](?:\s|$|[：:、.])"),
        re.compile(r"^\s*第\s*0*(\d{1,5})\s+\S.{0,40}$"),
    ]
    for line_index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if len(stripped) > 100:
            continue
        for pattern in patterns:
            match = pattern.search(stripped)
            if not match:
                continue
            number = int(match.group(1))
            inner_match = re.search(r"第\s*0*(\d{1,5})\s*[章节回]", stripped)
            if max_number and number > max_number and inner_match:
                inner_number = int(inner_match.group(1))
                if 1 <= inner_number <= max_number:
                    number = inner_number
            if line_index not in seen_lines:
                results.append((line_index, number, stripped))
                seen_lines.add(line_index)
            break
    return results


def quality_report(args: argparse.Namespace) -> int:
    raw = args.quality_report.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()
    nonempty = [line for line in lines if line.strip()]
    blocks = [block.strip() for block in re.split(r"\n{3,}", raw) if block.strip()]
    section_blocks = blocks[1:] if blocks else []
    block_section_count = len(section_blocks)
    block_titles = [
        next((line.strip() for line in block.splitlines() if line.strip()), "")
        for block in section_blocks
    ]
    block_fingerprints = [
        normalize_spaces(block)[:600]
        for block in section_blocks
    ]
    unique_block_section_count = len(set(block_fingerprints))
    duplicate_block_title_count = block_section_count - len(set(block_titles))
    duplicate_block_fingerprint_count = block_section_count - unique_block_section_count
    required_patterns = [re.compile(pattern) for pattern in (args.required_term or [])]
    blocks_missing_required_terms: list[int] = []
    if required_patterns:
        for index, block in enumerate(section_blocks, start=1):
            if not any(pattern.search(block) for pattern in required_patterns):
                blocks_missing_required_terms.append(index)
    chapter_regex = re.compile(
        args.title_regex
        or r"^((\d+|[一二三四五六七八九十百千万零〇]+)[.、]\s*)?第\s*[一二三四五六七八九十百千万零〇0-9]+\s*[章节回](\s|$|[：:、.])|^[一二三四五六七八九十百千万零〇]{1,4}[、.]\s*\S.{0,24}$"
    )
    special_heading_regex = re.compile(r"^((\d+|[一二三四五六七八九十百千万零〇]+)[.、]\s*)?(序章|序幕|楔子|引子|尾声|末章|终章|完结章|后记|番外)")
    volume_regex = re.compile(r"^第[一二三四五六七八九十百千万零〇0-9]+[卷集部]\s*")
    suspicious_patterns = {
        "replacement_char": r"�",
        "private_use": r"[\uE000-\uF8FF]",
        "download_noise": r"下载|最新网址|电子书|txt小说|书城",
        "navigation_noise": r"上一章|下一章|返回目录|加入书签",
        "social_gate_noise": r"公众号|验证码|输入密码|关注.{0,8}微信|微信.{0,8}(回复|公众号|关注)",
        "url_noise": r"https?://|www\.",
        "upload_marker_noise": r"用户上传|内容开始|内容结束",
        "html_markup_noise": r"<!DOCTYPE|<html\b|<body\b|<script\b|</div>",
    }

    suspicious: dict[str, int] = {}
    examples: dict[str, list[tuple[int, str]]] = {}
    for name, pattern in suspicious_patterns.items():
        regex = re.compile(pattern, re.IGNORECASE)
        hits: list[tuple[int, str]] = []
        for index, line in enumerate(lines, start=1):
            if regex.search(line):
                hits.append((index, line.strip()))
        suspicious[name] = len(hits)
        examples[name] = hits[:5]

    chapter_lines = [(index, line.strip()) for index, line in enumerate(lines, start=1) if chapter_regex.search(line.strip())]
    special_heading_lines = [
        (index, line.strip())
        for index, line in enumerate(lines, start=1)
        if special_heading_regex.search(line.strip()) and len(line.strip()) <= 60
    ]
    volume_lines = [(index, line.strip()) for index, line in enumerate(lines, start=1) if volume_regex.search(line.strip())]
    expected_numeric_count = args.expected_numeric_sections or args.expected_sections
    numeric_source_lines = block_titles if block_section_count > 1 else lines
    numeric_chapter_headings = detect_numeric_chapter_headings(numeric_source_lines, expected_numeric_count)
    numeric_values = [number for _, number, _ in numeric_chapter_headings]
    duplicate_numeric_values = sorted({number for number in numeric_values if numeric_values.count(number) > 1})
    missing_numeric_values: list[int] = []
    if expected_numeric_count and numeric_values:
        present = set(number for number in numeric_values if 1 <= number <= expected_numeric_count)
        missing_numeric_values = [
            number
            for number in range(1, expected_numeric_count + 1)
            if number not in present
        ]
    midpoint = max(0, len(lines) // 2 - 4)
    detected_section_count = max(
        len(chapter_lines) + len(special_heading_lines),
        unique_block_section_count,
    )
    completion_status = (
        "unknown"
        if not args.expected_sections
        else "complete"
        if detected_section_count >= args.expected_sections
        else "partial"
    )
    acceptance_issues: list[str] = []
    if not args.expected_sections and detected_section_count == 0 and len(raw.strip()) < 20000:
        acceptance_issues.append("no sections detected in short TXT")
    if completion_status == "partial":
        acceptance_issues.append("detected sections below expected count")
    if duplicate_block_fingerprint_count:
        acceptance_issues.append("duplicate section fingerprints detected")
    if blocks_missing_required_terms:
        acceptance_issues.append("sections missing required target terms")
    if suspicious.get("html_markup_noise", 0):
        acceptance_issues.append("html markup detected in TXT")
    if args.require_chapter_number_sequence and missing_numeric_values:
        acceptance_issues.append("missing numeric chapter numbers detected")
    if args.require_chapter_number_sequence and duplicate_numeric_values:
        acceptance_issues.append("duplicate numeric chapter numbers detected")
    partial_only = acceptance_issues == ["detected sections below expected count"]
    if args.allow_partial_quality and partial_only:
        acceptance_status = "partial"
    else:
        acceptance_status = "fail" if acceptance_issues else "pass"
    payload = {
        "path": str(args.quality_report),
        "bytes": args.quality_report.stat().st_size,
        "chars": len(raw),
        "lines": len(lines),
        "nonempty_lines": len(nonempty),
        "block_section_count": block_section_count,
        "unique_block_section_count": unique_block_section_count,
        "duplicate_block_title_count": duplicate_block_title_count,
        "duplicate_block_fingerprint_count": duplicate_block_fingerprint_count,
        "required_term_count": len(required_patterns),
        "blocks_missing_required_terms_count": len(blocks_missing_required_terms),
        "blocks_missing_required_terms_sample": blocks_missing_required_terms[:20],
        "chapter_heading_count": len(chapter_lines),
        "special_heading_count": len(special_heading_lines),
        "total_section_heading_count": len(chapter_lines) + len(special_heading_lines),
        "numeric_chapter_heading_count": len(numeric_chapter_headings),
        "first_numeric_chapter_headings": numeric_chapter_headings[:5],
        "last_numeric_chapter_headings": numeric_chapter_headings[-5:],
        "missing_numeric_chapter_numbers_count": len(missing_numeric_values),
        "missing_numeric_chapter_numbers_sample": missing_numeric_values[:50],
        "duplicate_numeric_chapter_numbers": duplicate_numeric_values[:50],
        "detected_section_count": detected_section_count,
        "expected_section_count": args.expected_sections,
        "completion_status": completion_status,
        "acceptance_status": acceptance_status,
        "acceptance_issues": acceptance_issues,
        "partial_reason": args.partial_reason if acceptance_status == "partial" else None,
        "volume_heading_count": len(volume_lines),
        "first_chapter_headings": chapter_lines[:5],
        "last_chapter_headings": chapter_lines[-5:],
        "special_headings": special_heading_lines[:20],
        "suspicious_counts": suspicious,
        "suspicious_examples": examples,
        "first_sample": sample_lines(lines, 0),
        "middle_sample": sample_lines(lines, midpoint),
        "last_sample": sample_lines(lines, max(0, len(lines) - 8)),
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"Wrote quality report to {args.output}", file=sys.stderr)
    else:
        print(text)
    return 0


def default_auto_title_regex() -> str:
    return r"(序章[^\n]*|第\s*[一二三四五六七八九十百千万零〇0-9]+\s*[章节回][^\n]*|尾声[^\n]*|末章[^\n]*|终章[^\n]*|完结章[^\n]*|后记[^\n]*|番外[^\n]*)"


def auto_base_path(args: argparse.Namespace, source: str) -> Path:
    if args.output:
        return args.output
    stem = args.title or Path(urllib.parse.urlparse(source).path).stem or "novel"
    stem = re.sub(r"[^\w\u4e00-\u9fff.-]+", "-", stem).strip("-") or "novel"
    return Path(f"{stem}.txt")


def infer_book_title_from_candidate(page_title: str, fallback: str) -> str:
    title = html.unescape(page_title or "").strip()
    quoted = re.search(r"《([^》]{1,80})》", title)
    if quoted:
        return normalize_spaces(quoted.group(1))

    first_part = re.split(r"[|_\-]|[:：]\s+| - ", title, maxsplit=1)[0]
    first_part = re.sub(r"TXT下载.*$|txt下载.*$|全文阅读.*$|最新章节.*$|全集.*$", "", first_part)
    first_part = re.sub(r"[（(][^）)]{1,20}[）)]", "", first_part)
    first_part = first_part.strip(" \t\r\n《》【】[]")
    if 1 <= len(first_part) <= 40 and re.search(r"[\u4e00-\u9fff]", first_part):
        return normalize_spaces(first_part)
    return fallback


def write_auto_quality(args: argparse.Namespace, output_path: Path, expected_sections: int | None) -> dict[str, object] | None:
    if args.no_auto_quality:
        return None
    old_quality = args.quality_report
    old_expected = args.expected_sections
    old_output = args.output
    args.quality_report = output_path
    args.expected_sections = expected_sections
    args.output = args.quality_output or output_path.with_suffix(".quality.json")
    try:
        quality_report(args)
        if args.output and args.output.exists():
            return json.loads(args.output.read_text(encoding="utf-8"))
        return None
    finally:
        args.quality_report = old_quality
        args.expected_sections = old_expected
        args.output = old_output


def require_auto_quality_pass(args: argparse.Namespace, payload: dict[str, object] | None) -> None:
    if not getattr(args, "_auto_title_mode", False) or not payload:
        return
    if payload.get("acceptance_status") == "fail":
        issues = ", ".join(str(issue) for issue in payload.get("acceptance_issues", []))
        raise SystemExit(f"auto quality failed: {issues or 'unknown quality issue'}")


def auto_from_url(args: argparse.Namespace, source: str | None = None) -> int:
    source = source or args.auto_from_url
    if not source:
        raise SystemExit("--auto-from-url requires a URL.")

    output_path = auto_base_path(args, source)
    candidate = classify_url(source, args)
    print(f"[AUTO] {candidate.source_type} score={candidate.score} {source}", file=sys.stderr)
    if candidate.source_type in {"access-gated", "fetch-failed", "unknown"}:
        raise SystemExit(f"Source is not directly usable: {candidate.source_type} {candidate.reason}")

    if candidate.source_type.startswith("direct-") or candidate.source_type.startswith("download-page-"):
        old_download_from = args.download_file_from
        old_download_url = args.download_file_url
        old_download_output = args.download_output
        old_output = args.output
        try:
            if candidate.source_type.startswith("direct-"):
                args.download_file_url = source
                args.download_file_from = None
            else:
                args.download_file_from = source
                args.download_file_url = None
            args.output = output_path
            args.download_output = args.download_output or output_path.with_suffix(".raw.bin")
            status = download_file(args)
            if status == 0 and output_path.exists():
                quality_payload = write_auto_quality(args, output_path, args.expected_sections)
                require_auto_quality_pass(args, quality_payload)
            return status
        finally:
            args.download_file_from = old_download_from
            args.download_file_url = old_download_url
            args.download_output = old_download_output
            args.output = old_output

    if candidate.source_type in {"toc", "possible-novel-page"}:
        links = auto_chapter_links_from_toc(source, args)
        if len(links) < args.min_chapter_links:
            raise SystemExit(f"Only found {len(links)} likely chapter links.")
        urls_path = args.urls_output or output_path.with_suffix(".urls.txt")
        urls_path.write_text("\n".join(links) + "\n", encoding="utf-8")
        print(f"[AUTO] wrote {len(links)} chapter URLs to {urls_path}", file=sys.stderr)

        old_url = args.url
        old_urls_file = args.urls_file
        old_output = args.output
        old_title_regex = args.title_regex
        old_content_selector = args.content_selector
        old_page_link_regex = args.page_link_regex
        old_page_link_sort_numeric = args.page_link_sort_numeric
        old_failure_output = args.failure_output
        try:
            args.url = None
            args.urls_file = urls_path
            args.output = output_path
            args.title_regex = args.title_regex or default_auto_title_regex()
            args.content_selector = args.content_selector or args.auto_content_selector
            args.page_link_regex = args.page_link_regex or args.auto_page_link_regex
            args.page_link_sort_numeric = args.page_link_sort_numeric or args.auto_page_link_sort_numeric
            args.failure_output = args.failure_output or output_path.with_suffix(".failed-urls.txt")
            if not args.stop_after_consecutive_failures:
                args.stop_after_consecutive_failures = 20
            chapters, failures = download_chapters(args)
            if not chapters:
                return 2
            write_txt(output_path, args.title, chapters)
            quality_payload = write_auto_quality(args, output_path, len(links))
            require_auto_quality_pass(args, quality_payload)
            return 1 if failures else 0
        finally:
            args.url = old_url
            args.urls_file = old_urls_file
            args.output = old_output
            args.title_regex = old_title_regex
            args.content_selector = old_content_selector
            args.page_link_regex = old_page_link_regex
            args.page_link_sort_numeric = old_page_link_sort_numeric
            args.failure_output = old_failure_output

    raise SystemExit(f"Unsupported auto source type: {candidate.source_type}")


def auto_title(args: argparse.Namespace) -> int:
    candidates = [candidate for candidate in (classify_url(url, args) for url, _ in search_web(args.auto_title, args)) if candidate.score > 0]
    if not candidates:
        raise SystemExit("No usable candidates found.")
    candidates.sort(key=lambda item: item.score, reverse=True)
    if args.candidates_output:
        payload = {
            "title": args.auto_title,
            "count": len(candidates),
            "candidates": [candidate.__dict__ for candidate in candidates],
        }
        args.candidates_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    last_error: Exception | None = None
    old_title = args.title
    old_auto_title_mode = getattr(args, "_auto_title_mode", False)
    if not args.title:
        args.title = args.auto_title
    args._auto_title_mode = True
    try:
        for candidate in candidates[: args.auto_try_candidates]:
            try:
                print(f"[AUTO] trying candidate {candidate.url}", file=sys.stderr)
                args.title = infer_book_title_from_candidate(candidate.title, args.auto_title)
                status = auto_from_url(args, candidate.url)
                if status == 0:
                    return status
                raise SystemExit(f"auto candidate returned status {status}")
            except (SystemExit, OSError, ValueError) as exc:
                last_error = exc
                print(f"[AUTO] candidate failed: {exc}", file=sys.stderr)
                if args.delay:
                    time.sleep(args.delay)
        raise SystemExit(f"No candidate completed. Last error: {last_error}")
    finally:
        args.title = old_title
        args._auto_title_mode = old_auto_title_mode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Download authorized web novel chapter pages and assemble TXT."
    )
    parser.add_argument("--url", action="append", help="Chapter URL or local HTML file path.")
    parser.add_argument("--urls-file", type=Path, help="UTF-8 file with one URL/path per line.")
    parser.add_argument("--output", type=Path, help="Output .txt path or extracted link list path.")
    parser.add_argument("--title", help="Novel title to place at the top of the TXT.")
    parser.add_argument("--content-selector", help="Simple selector: #id, .class, or tag name.")
    parser.add_argument(
        "--content-mode",
        choices=("selector", "jjwxc"),
        default="selector",
        help="Extraction strategy. Use jjwxc for authorized/public JJWXC official chapter pages.",
    )
    parser.add_argument("--title-selector", help="Simple selector for chapter title.")
    parser.add_argument("--title-regex", help="Regex for chapter title; first capture group is used when present.")
    parser.add_argument("--start-after", help="Regex line; keep text after the first matching line.")
    parser.add_argument("--start-after-last", help="Regex line; keep text after the last matching line.")
    parser.add_argument("--end-before", help="Regex line; keep text before the first matching line.")
    parser.add_argument("--drop-line", action="append", help="Regex line to remove. Can be repeated.")
    parser.add_argument("--remove-regex", action="append", help="Regex text fragment to delete. Can be repeated.")
    parser.add_argument("--dedupe-adjacent-lines", action="store_true", help="Remove immediately repeated identical lines after filtering.")
    parser.add_argument("--keep-source-boilerplate", action="store_true", help="Do not apply the built-in removal list for common download-site wrappers.")
    parser.add_argument("--keep-private-use", action="store_true", help="Preserve Unicode private-use characters instead of removing likely encoding artifacts.")
    parser.add_argument("--cookie", help="Authorized Cookie header value.")
    parser.add_argument("--cookie-file", type=Path, help="Cookie string or Netscape cookie file.")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests in seconds.")
    parser.add_argument("--delay-jitter", type=float, default=0.0, help="Add a random 0..N seconds to each inter-request delay.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds.")
    parser.add_argument("--retries", type=int, default=0, help="Retry count per source.")
    parser.add_argument("--retry-delay", type=float, default=2.0, help="Delay between retries in seconds.")
    parser.add_argument("--flush-each", action="store_true", help="Write output after every successful chapter.")
    parser.add_argument("--failure-output", type=Path, help="Write failed chapter URLs for a later補跑.")
    parser.add_argument("--stop-after-consecutive-failures", type=int, default=0, help="Stop a run after N consecutive failed chapter sources; 0 disables this guard.")
    parser.add_argument("--insecure", action="store_true", help="Disable TLS certificate verification.")
    parser.add_argument("--discover-title", help="Search for a novel title and write classified source candidates as JSON.")
    parser.add_argument("--discover-max", type=int, default=10, help="Maximum search results to probe with --discover-title.")
    parser.add_argument("--probe-url", help="Fetch one URL and classify it as a source candidate.")
    parser.add_argument("--auto-from-url", help="Automatically convert one candidate URL to TXT by probing its source type.")
    parser.add_argument("--auto-title", help="Search a title, try ranked candidates, and produce a TXT plus quality report.")
    parser.add_argument("--auto-try-candidates", type=int, default=3, help="Maximum ranked candidates to try with --auto-title.")
    parser.add_argument("--auto-content-selector", default="#cont-body", help="Default content selector for auto TOC downloads.")
    parser.add_argument("--auto-page-link-regex", default=r"_[0-9]+\.html", help="Default in-chapter pagination regex for auto TOC downloads.")
    parser.add_argument("--auto-page-link-sort-numeric", default=r"_([0-9]+)\.html", help="Default in-chapter pagination sort regex for auto TOC downloads.")
    parser.add_argument("--urls-output", type=Path, help="Where auto modes should write detected chapter URLs.")
    parser.add_argument("--quality-output", type=Path, help="Where auto modes should write the generated quality report.")
    parser.add_argument("--candidates-output", type=Path, help="Where --auto-title should write ranked candidates.")
    parser.add_argument("--no-auto-quality", action="store_true", help="Do not write a quality report in auto modes.")
    parser.add_argument("--min-chapter-links", type=int, default=10, help="Minimum likely chapter links needed to classify a page as a TOC.")
    parser.add_argument("--download-file-from", help="Download the best TXT/EPUB/ZIP/RAR/7z link found on an HTML download page.")
    parser.add_argument("--download-file-url", help="Download a direct TXT/EPUB/ZIP/RAR/7z URL.")
    parser.add_argument("--download-output", type=Path, help="Path for the raw downloaded file. Defaults to output path with the source extension.")
    parser.add_argument("--download-extensions", default="txt,epub,zip,rar,7z", help="Comma-separated file extensions to consider with --download-file-from.")
    parser.add_argument("--download-link-regex", default=r"(down|download|read_down|DownSoft|DownSys)", help="Fallback href regex for dynamic download endpoints without file extensions.")
    parser.add_argument("--download-follow-html", type=int, default=2, help="Follow up to N HTML landing pages when looking for the final downloadable file.")
    parser.add_argument("--referer", help="Referer header for direct file downloads.")
    parser.add_argument("--no-auto-convert-download", action="store_true", help="Only save the raw file; do not convert TXT/EPUB/ZIP to --output.")
    parser.add_argument("--extract-links-from", action="append", help="TOC URL or local HTML file to extract chapter links from. Can be repeated.")
    parser.add_argument("--extract-chapter-links-auto-from", help="Infer the largest same-site numeric chapter-link group from a TOC page.")
    parser.add_argument("--base-url", help="Base URL to resolve links when extracting from a local HTML file.")
    parser.add_argument("--generate-url-template", help="Generate a URL list from a template containing {n}, for continuous numbered chapter paths.")
    parser.add_argument("--range-start", type=int, help="First number for --generate-url-template.")
    parser.add_argument("--range-end", type=int, help="Last number for --generate-url-template.")
    parser.add_argument("--link-regex", help="Only keep hrefs matching this regex.")
    parser.add_argument("--link-sort-numeric", help="Sort links by the first capture group of this regex.")
    parser.add_argument("--page-link-regex", help="Within each chapter, also fetch linked subpages whose href matches this regex.")
    parser.add_argument("--page-link-sort-numeric", help="Sort chapter subpages by the first capture group of this regex.")
    parser.add_argument("--clean-txt", type=Path, help="Clean an already generated TXT file.")
    parser.add_argument("--normalize-txt", type=Path, help="Decode and normalize an existing plain TXT file without re-chapterizing it.")
    parser.add_argument("--extract-epub", type=Path, help="Extract EPUB spine XHTML/HTML content to a UTF-8 TXT file.")
    parser.add_argument("--keep-epub-navigation", action="store_true", help="Keep EPUB cover/table-of-contents/navigation pages during extraction.")
    parser.add_argument("--extract-zip", type=Path, help="Extract TXT member(s) from a ZIP archive to a UTF-8 TXT file.")
    parser.add_argument("--extract-archive", type=Path, help="Extract TXT member(s) from RAR/7z or other bsdtar-supported archives to UTF-8 TXT.")
    parser.add_argument("--zip-member-regex", help="With --extract-zip, only extract TXT members whose ZIP path matches this regex.")
    parser.add_argument("--archive-member-regex", help="With --extract-archive, only extract TXT members whose archive path matches this regex.")
    parser.add_argument("--min-section-chars", type=int, default=0, help="With --extract-epub or --extract-zip, skip extracted sections shorter than this many characters.")
    parser.add_argument("--input-encoding", default="utf-8", help="Encoding for --clean-txt, --normalize-txt, or --extract-zip input.")
    parser.add_argument("--merge-txt", action="append", type=Path, help="Merge TXT files by chapter number. Can be repeated; later files override earlier chapters.")
    parser.add_argument("--chapter-number-regex", default=r"第([0-9]+)", help="Regex used to extract numeric chapter order.")
    parser.add_argument("--quality-report", type=Path, help="Write a JSON quality report for a generated UTF-8 TXT file.")
    parser.add_argument("--expected-sections", type=int, help="Expected chapter/section count for --quality-report completion status.")
    parser.add_argument("--expected-numeric-sections", type=int, help="Expected numeric chapter sequence length when it differs from --expected-sections.")
    parser.add_argument("--require-chapter-number-sequence", action="store_true", help="Fail quality acceptance if expected numeric chapter numbers are missing or duplicated.")
    parser.add_argument("--required-term", action="append", help="Regex that should appear in each section for target-drift checks. Can be repeated.")
    parser.add_argument("--allow-partial-quality", action="store_true", help="Mark a clean but incomplete TXT as partial instead of fail. Use only after full-source attempts are documented.")
    parser.add_argument("--partial-reason", help="Reason recorded when --allow-partial-quality marks a clean incomplete TXT as partial.")
    parser.add_argument("--save-html", type=Path, help="Save fetched HTML for selector inspection.")
    parser.add_argument("--allow-gated-text", action="store_true", help="Do not reject pages that look like login/password/captcha placeholders.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.save_html:
        if not args.url or len(args.url) != 1:
            raise SystemExit("--save-html requires exactly one --url.")
        cookie = parse_cookie(args.cookie, args.cookie_file)
        markup = fetch_source(args.url[0], cookie=cookie, timeout=args.timeout, insecure=args.insecure)
        args.save_html.write_text(markup, encoding="utf-8")
        print(f"Wrote HTML to {args.save_html}", file=sys.stderr)
        return 0
    if args.discover_title:
        return discover_title(args)
    if args.probe_url:
        return probe_url(args)
    if args.auto_title:
        return auto_title(args)
    if args.auto_from_url:
        return auto_from_url(args)
    if args.download_file_from or args.download_file_url:
        return download_file(args)
    if args.extract_links_from:
        return extract_links(args)
    if args.extract_chapter_links_auto_from:
        return extract_chapter_links_auto(args)
    if args.generate_url_template:
        return generate_url_template(args)
    if args.quality_report:
        return quality_report(args)
    if args.normalize_txt:
        return normalize_existing_txt(args)
    if args.extract_epub:
        return extract_epub(args)
    if args.extract_zip:
        return extract_zip(args)
    if args.extract_archive:
        return extract_archive(args)
    if args.clean_txt:
        return clean_existing_txt(args)
    if args.merge_txt:
        return merge_txt(args)
    if not args.output:
        raise SystemExit("--output is required when downloading chapters.")
    chapters, failures = download_chapters(args)
    if not chapters:
        print("No chapters downloaded.", file=sys.stderr)
        return 2

    write_txt(args.output, args.title, chapters)
    print(f"Wrote {len(chapters)} chapters to {args.output}", file=sys.stderr)
    if failures:
        print(f"Skipped {len(failures)} failed sources.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
