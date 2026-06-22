#!/usr/bin/env python3
"""Download or import an authorized webnovel text file and normalize it to UTF-8."""

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


HTML_PATTERNS = (
    re.compile(rb"<!doctype\s+html", re.I),
    re.compile(rb"<html[\s>]", re.I),
    re.compile(rb"<title>.*</title>", re.I | re.S),
)

BAD_TEXT_MARKERS = (
    "404",
    "403",
    "not found",
    "access denied",
    "百度网盘",
    "请输入提取码",
    "防盗链",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download/copy an authorized txt or zip source and save a UTF-8 txt file."
    )
    parser.add_argument("source", help="Authorized http(s) URL or local file path.")
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
        help="Minimum output size. Use a lower value for samples or short works.",
    )
    return parser.parse_args()


def safe_filename(title: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", title).strip(" ._")
    return name or "downloaded-webnovel"


def fetch_source(source: str, tmp_dir: Path) -> Path:
    parsed = urllib.parse.urlparse(source)
    if parsed.scheme in {"http", "https"}:
        suffix = Path(urllib.parse.unquote(parsed.path)).suffix or ".download"
        target = tmp_dir / f"source{suffix}"
        request = urllib.request.Request(
            source,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; popwave-skill/1.0)",
                "Accept": "text/plain,application/zip,*/*",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                with target.open("wb") as output:
                    shutil.copyfileobj(response, output)
        except urllib.error.URLError as exc:
            raise RuntimeError(f"下载失败：{exc}") from exc
        return target

    path = Path(source).expanduser()
    if not path.exists():
        raise RuntimeError(f"本地文件不存在：{path}")
    target = tmp_dir / path.name
    shutil.copy2(path, target)
    return target


def extract_text_file(path: Path, tmp_dir: Path) -> Path:
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
    issues: list[str] = []
    if any(pattern.search(raw[:4096]) for pattern in HTML_PATTERNS):
        issues.append("下载结果像 HTML 页面，不像正文 TXT")
    normalized = html.unescape(text[:5000]).lower()
    for marker in BAD_TEXT_MARKERS:
        if marker.lower() in normalized:
            issues.append(f"疑似错误页或网盘页：包含“{marker}”")
            break
    if len(text.encode("utf-8")) < min_bytes:
        issues.append(f"文件小于阈值 {min_bytes} bytes，可能不完整")
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text[:20000]))
    if cjk_count < 100 and len(text) > 1000:
        issues.append("前段中文字符过少，可能不是中文正文或编码异常")
    return issues


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_name:
        tmp_dir = Path(temp_name)
        source_path = fetch_source(args.source, tmp_dir)
        text_path = extract_text_file(source_path, tmp_dir)
        raw = text_path.read_bytes()
        text, encoding = decode_bytes(raw)
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        issues = validate_text(raw, text, args.min_bytes)
        if issues:
            for issue in issues:
                print(f"ERROR: {issue}", file=sys.stderr)
            return 2

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
