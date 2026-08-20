#!/usr/bin/env python3
"""Batch download novels from a book list JSON file.

Usage:
    python batch_download.py book_list.json --output-base "D:\workspace\参考小说txt" --script-dir "D:\workspace\skill_modifications"

Book list JSON format:
    [
        {
            "title": "书名",
            "author": "作者",
            "platform": "番茄|起点|晋江",
            "source_url": "https://...",      // optional
            "content_selector": "div#content", // optional
            "workers": 10,                     // optional, default 10
            "status": "pending|success|failed" // auto-updated
        }
    ]
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


def load_book_list(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_book_list(books: list[dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)


def load_results(path: str) -> dict:
    if Path(path).exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_results(results: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def download_one(book: dict, script_dir: str, output_base: str) -> dict:
    """Download one book and return the result."""
    title = book["title"]
    author = book.get("author", "")
    platform = book.get("platform", "")
    source_url = book.get("source_url", "")
    content_selector = book.get("content_selector", "")
    workers = book.get("workers", 10)
    download_mode = book.get("download_mode", "")

    script_path = str(Path(script_dir) / "download_novel.py")
    output_dir = str(Path(output_base))

    cmd = [
        sys.executable, script_path, title,
        "--output-dir", output_dir,
        "--workers", str(workers),
    ]

    if author:
        cmd.extend(["--author", author])
    if platform:
        subdir = f"{platform}top20"
        cmd.extend(["--output-subdir", subdir])
    if source_url:
        cmd.extend(["--source-url", source_url])
    if content_selector:
        cmd.extend(["--content-selector", content_selector])
    if download_mode == "direct":
        cmd.append("--direct")

    print(f"\n{'='*60}")
    print(f"下载《{title}》 — {platform} — {author}")
    print(f"URL: {source_url or 'auto-search'}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=3600,  # 60 min max per book
            encoding="utf-8",
            errors="replace",
        )
        # Parse JSON from stdout (supports both single-line and multi-line JSON)
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        json_result = None

        # Strategy 1: Try to find a complete JSON block in stdout
        # Look for the first { and the last } and try to parse everything between
        first_brace = stdout.find("{")
        last_brace = stdout.rfind("}")
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            json_str = stdout[first_brace:last_brace + 1]
            try:
                json_result = json.loads(json_str)
            except json.JSONDecodeError:
                pass

        # Strategy 2: Try line-by-line (for compact single-line JSON)
        if not json_result:
            for line in stdout.split("\n"):
                line = line.strip()
                if line.startswith("{") and line.endswith("}"):
                    try:
                        json_result = json.loads(line)
                    except json.JSONDecodeError:
                        continue

        if json_result:
            json_result["title"] = title
            json_result["author"] = author
            json_result["platform"] = platform
            return json_result
        else:
            return {
                "status": "error",
                "title": title,
                "author": author,
                "platform": platform,
                "reason": "No JSON output from script",
                "stdout_tail": stdout[-500:] if stdout else "",
                "stderr_tail": stderr[-500:] if stderr else "",
            }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "title": title,
            "author": author,
            "platform": platform,
            "reason": "Timeout (60 min)",
        }
    except Exception as e:
        return {
            "status": "error",
            "title": title,
            "author": author,
            "platform": platform,
            "reason": f"{type(e).__name__}: {str(e)[:200]}",
        }


def main():
    parser = argparse.ArgumentParser(description="Batch download novels from a book list.")
    parser.add_argument("book_list", help="Path to book list JSON file.")
    parser.add_argument("--output-base", default=r"D:\workspace\参考小说txt", help="Base output directory.")
    parser.add_argument("--script-dir", default=r"D:\workspace\skill_modifications", help="Directory containing download_novel.py.")
    parser.add_argument("--results-file", default=None, help="Path to batch results JSON (default: <output-base>/batch_results.json).")
    parser.add_argument("--resume", action="store_true", help="Skip books already marked as success.")
    parser.add_argument("--retry-failed", action="store_true", help="Only retry books that previously failed.")
    parser.add_argument("--platform-filter", default=None, help="Only download books from this platform (番茄/起点/晋江).")
    parser.add_argument("--start-index", type=int, default=0, help="Start from this index in the book list.")
    parser.add_argument("--end-index", type=int, default=0, help="End at this index (0 = until end).")
    args = parser.parse_args()

    books = load_book_list(args.book_list)
    results_path = args.results_file or str(Path(args.output_base) / "batch_results.json")
    results = load_results(results_path)

    # Filter books
    to_download = []
    for i, book in enumerate(books):
        if args.platform_filter and book.get("platform", "") != args.platform_filter:
            continue
        if args.start_index and i < args.start_index:
            continue
        if args.end_index and i >= args.end_index:
            continue

        key = f"{book['title']}_{book.get('author','')}"
        prev = results.get(key, {})

        if args.resume and prev.get("status") == "success":
            print(f"跳过（已成功）: {book['title']}")
            continue
        if args.retry_failed and prev.get("status") != "error" and prev.get("status") != "partial":
            if prev.get("status") == "success":
                print(f"跳过（已成功）: {book['title']}")
            continue

        to_download.append((i, book))

    print(f"\n准备下载: {len(to_download)} 本")
    print(f"输出目录: {args.output_base}")
    print(f"结果文件: {results_path}")

    success_count = 0
    fail_count = 0
    partial_count = 0

    for idx, (i, book) in enumerate(to_download):
        print(f"\n[{idx+1}/{len(to_download)}] ", end="")

        result = download_one(book, args.script_dir, args.output_base)

        key = f"{book['title']}_{book.get('author','')}"
        results[key] = result
        save_results(results, results_path)  # Save after each book

        status = result.get("status", "error")
        if status == "success":
            success_count += 1
            chapters = result.get("chapters_crawled", 0)
            size_mb = result.get("size_mb", 0)
            print(f"  ✓ 成功: {chapters} 章, {size_mb:.2f} MB")
        elif status == "partial":
            partial_count += 1
            chapters = result.get("chapters_crawled", 0)
            failed = result.get("chapters_failed", 0)
            print(f"  △ 部分成功: {chapters} 章成功, {failed} 章失败")
        else:
            fail_count += 1
            reason = result.get("reason", result.get("warnings", ["unknown"]))[:100]
            print(f"  ✗ 失败: {reason}")

        # Update book status
        books[i]["status"] = status
        if "output" in result:
            books[i]["output_path"] = result["output"]
        if "source" in result:
            books[i]["source"] = result["source"]
        save_book_list(books, args.book_list)

        # Small delay between books
        time.sleep(3)

    # Print summary
    total = len(to_download)
    print(f"\n{'='*60}")
    print(f"批量下载完成")
    print(f"{'='*60}")
    print(f"总数: {total}")
    print(f"成功: {success_count}")
    print(f"部分: {partial_count}")
    print(f"失败: {fail_count}")
    print(f"成功率: {(success_count + partial_count) / total * 100:.1f}%" if total > 0 else "")

    # Save final summary
    summary = {
        "total": total,
        "success": success_count,
        "partial": partial_count,
        "failed": fail_count,
        "success_rate": f"{(success_count + partial_count) / total * 100:.1f}%" if total > 0 else "0%",
    }
    results["_summary"] = summary
    save_results(results, results_path)


if __name__ == "__main__":
    main()
