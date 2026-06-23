#!/usr/bin/env python3
"""Download or import a webnovel text from a source and normalize it to UTF-8.

Supports:
  - Direct TXT/ZIP URL download
  - Local file import
  - Webpage text extraction (--extract-from-page)

No longer blocks HTML pages, 网盘 pages, or small files — the user
controls quality via --min-bytes and --force.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


# Still check for clear error pages, but much more relaxed
ERROR_MARKERS = (
    re.compile(rb"<title>404\s+Not\s+Found</title>", re.I),
    re.compile(rb"<title>403\s+Forbidden</title>", re.I),
    re.compile(rb"<title>503\s+Service\s+Unavailable</title>", re.I),
)

MAX_FILE_BYTES = 50 * 1024 * 1024  # 50 MB


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download/copy a webnovel source and save a UTF-8 txt file."
    )
    parser.add_argument("source", help="URL or local file path.")
    parser.add_argument("--title", required=True, help="Book title used for output filename.")
    parser.add_argument(
        "--output-dir",
        default=r"D:\popwave-skills\downloads",
        help="Directory for normalized txt output.",
    )
    parser.add_argument(
        "--min-bytes",
        type=int,
        default=100 * 1024,
        help="Minimum output size (default 100KB). Ignored with --force.",
    )
    parser.add_argument(
        "--extract-from-page",
        action="store_true",
        default=False,
        help="If set, extract visible text from the web page instead of downloading a raw file.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Skip validation warnings and save anyway.",
    )
    return parser.parse_args()


def safe_filename(title: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", title).strip(" ._")
    return name or "downloaded-webnovel"


def download_url(source: str, tmp_dir: Path, timeout: int = 60) -> Path:
    """Download a URL to a temp file."""
    parsed = urllib.parse.urlparse(source)
    suffix = Path(urllib.parse.unquote(parsed.path)).suffix or ".download"
    target = tmp_dir / f"source{suffix}"

    request = urllib.request.Request(
        source,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > MAX_FILE_BYTES:
                raise RuntimeError(f"文件过大 ({int(content_length)//1024//1024} MB > 50 MB)")
            with target.open("wb") as output:
                shutil.copyfileobj(response, output)
            actual_size = target.stat().st_size
            if actual_size > MAX_FILE_BYTES:
                target.unlink()
                raise RuntimeError(f"文件过大 ({actual_size//1024//1024} MB > 50 MB)")
            return target
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}：{exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"下载失败：{exc.reason}") from exc


def fetch_source(source: str, tmp_dir: Path, extract_from_page: bool) -> Path:
    """Get the raw source file into tmp_dir."""
    parsed = urllib.parse.urlparse(source)

    if parsed.scheme in {"http", "https"}:
        if extract_from_page:
            # Use requests + bs4 to extract visible text
            return _extract_page_text(source, tmp_dir)
        return download_url(source, tmp_dir)

    path = Path(source).expanduser()
    if not path.exists():
        raise RuntimeError(f"本地文件不存在：{path}")
    target = tmp_dir / path.name
    shutil.copy2(path, target)
    return target


def _extract_page_text(url: str, tmp_dir: Path) -> Path:
    """Use requests+BeautifulSoup to extract visible text from a web page."""
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        raise RuntimeError("需要安装 requests 和 beautifulsoup4 来使用 --extract-from-page")

    resp = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
        timeout=30,
    )
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"

    soup = BeautifulSoup(resp.text, "lxml")
    # Remove script/style tags
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    text = soup.get_text("\n", strip=True)
    text = re.sub(r"\n{3,}", "\n\n", text)

    output = tmp_dir / "extracted.txt"
    output.write_text(text, encoding="utf-8")
    return output


def extract_text_file(path: Path, tmp_dir: Path) -> Path:
    """If ZIP, extract largest .txt/.md. Otherwise return as-is."""
    if path.suffix.lower() != ".zip":
        return path

    with zipfile.ZipFile(path) as archive:
        candidates = [
            info
            for info in archive.infolist()
            if not info.is_dir() and Path(info.filename).suffix.lower() in {".txt", ".md"}
        ]
        if not candidates:
            raise RuntimeError("ZIP 中未找到 .txt/.md 文件")
        candidates.sort(key=lambda info: info.file_size, reverse=True)
        selected = candidates[0]
        output = tmp_dir / Path(selected.filename).name
        with archive.open(selected) as source, output.open("wb") as target:
            shutil.copyfileobj(source, target)
        return output


def decode_bytes(data: bytes) -> tuple[str, str]:
    """Try encodings in order, pick the one with most CJK chars."""
    encodings = ("utf-8-sig", "utf-8", "gb18030", "gbk", "big5")
    best_text = ""
    best_encoding = ""
    best_score = -1

    for encoding in encodings:
        try:
            text = data.decode(encoding)
        except UnicodeDecodeError:
            continue
        replacement_count = text.count("\ufffd")
        cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text))
        score = cjk_count - replacement_count * 20
        if score > best_score:
            best_text = text
            best_encoding = encoding
            best_score = score

    if not best_text:
        raise RuntimeError("无法识别文本编码")
    return best_text, best_encoding


def validate_text(raw: bytes, text: str, min_bytes: int) -> list[str]:
    """Return warnings but no longer hard-block most content."""
    issues: list[str] = []

    # Only hard-block clear HTTP error pages
    for pattern in ERROR_MARKERS:
        if pattern.search(raw[:4096]):
            issues.append("HTTP 错误页（404/403/503），不是正文内容")
            return issues  # Short-circuit — this is definitely wrong

    if len(text.encode("utf-8")) < min_bytes:
        issues.append(f"文件小于阈值 {min_bytes} bytes，可能不完整")

    if len(text) > 1000:
        cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text[:20000]))
        if cjk_count < 50:
            issues.append("中文字符过少，可能不是中文正文或编码异常")

    return issues


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_name:
        tmp_dir = Path(temp_name)
        source_path = fetch_source(args.source, tmp_dir, args.extract_from_page)
        text_path = extract_text_file(source_path, tmp_dir)
        raw = text_path.read_bytes()
        text, encoding = decode_bytes(raw)
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        issues = validate_text(raw, text, args.min_bytes)
        if issues:
            # Hard-block only on HTTP error pages
            if "HTTP 错误页" in issues[0]:
                for issue in issues:
                    print(f"ERROR: {issue}", file=sys.stderr)
                return 2
            # Otherwise just warn
            for issue in issues:
                print(f"WARN: {issue}", file=sys.stderr)
            if not args.force:
                return 2  # Still fail without --force

        output_path = output_dir / f"{safe_filename(args.title)}.txt"
        output_path.write_text(text, encoding="utf-8", newline="\n")

    preview = re.sub(r"\s+", " ", text[:120]).strip()
    print(f"output={output_path}")
    print(f"encoding={encoding}")
    print(f"bytes={output_path.stat().st_size}")
    print(f"preview={preview}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
