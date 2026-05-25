#!/usr/bin/env python3
"""
Trae 网文下载器 —— LLM 调用版
LLM 负责搜源+选源+生成URL，这个脚本只负责下载+质检。

用法:
  # 从 URL 列表下载
  python3 dl.py --urls urls.txt --output 书名.txt --title "书名"
  
  # 从目录页自动提取+下载
  python3 dl.py --toc "https://xxx/book/123/" --output 书名.txt --title "书名"
  
  # 质量报告
  python3 dl.py --check 书名.txt --expected 1132
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# 自动定位 download_novel.py
HERE = Path(__file__).resolve().parent
NOVEL_PY = HERE / "scripts" / "download_novel.py"


def run(*args, check: bool = True):
    """运行命令并打印输出"""
    cmd = [str(a) for a in args]
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    out = result.stdout.strip()
    err = result.stderr.strip()
    if out:
        for line in out.splitlines()[-30:]:
            print(f"  {line}")
    if err:
        for line in err.splitlines()[-5:]:
            print(f"  [stderr] {line}")
    if check and result.returncode != 0:
        print(f"  ⚠️  exit_code={result.returncode}")
    return result


def cmd_download(urls_file: Path, output: Path, title: str, expected: int = 0):
    """从URL列表批量下载"""
    args = [
        "python3", NOVEL_PY,
        "--urls-file", urls_file,
        "--output", output,
        "--title", title,
        "--delay", "0.6", "--delay-jitter", "0.3",
        "--retries", "3", "--timeout", "30",
        "--flush-each",
        "--failure-output", output.with_suffix(".failed.txt"),
        "--stop-after-consecutive-failures", "30",
        "--dedupe-adjacent-lines",
    ]
    if expected:
        args += ["--expected-sections", str(expected)]
    run(*args)


def cmd_toc(toc_url: str, output: Path, title: str, expected: int = 0):
    """从目录页自动提取链接 + 下载"""
    urls_file = output.with_suffix(".urls.txt")
    
    # Step 1: 提取章节链接
    print(f"\n📋 从目录页提取链接...")
    r1 = run(
        "python3", NOVEL_PY,
        "--extract-chapter-links-auto-from", toc_url,
        "--output", urls_file,
        check=False,
    )
    
    if r1.returncode != 0 or not urls_file.exists():
        print(f"❌ 目录提取失败")
        return False
    
    n = len(urls_file.read_text().splitlines())
    print(f"✅ 提取到 {n} 个章节链接")
    
    # Step 2: 下载
    cmd_download(urls_file, output, title, expected)
    return True


def cmd_check(txt_path: Path, expected: int = 0, required_term: str = ""):
    """质量验证"""
    args = [
        "python3", NOVEL_PY,
        "--quality-report", txt_path,
        "--output", txt_path.with_suffix(".quality.json"),
        "--require-chapter-number-sequence",
    ]
    if expected:
        args += ["--expected-sections", str(expected),
                 "--expected-numeric-sections", str(expected)]
    if required_term:
        args += ["--required-term", required_term]
    
    r = run(*args, check=False)
    
    qfile = txt_path.with_suffix(".quality.json")
    if qfile.exists():
        with open(qfile) as f:
            q = json.load(f)
        print(f"\n📊 质量报告:")
        print(f"   文件大小: {q['bytes']:,} bytes ({q['bytes']/1024/1024:.1f} MB)")
        print(f"   完成状态: {q['completion_status']}")
        print(f"   接受状态: {q['acceptance_status']}")
        print(f"   章节标题: {q['chapter_heading_count']}")
        print(f"   唯一块:   {q['unique_block_section_count']} / {q['block_section_count']}")
        print(f"   数字章节: {q['numeric_chapter_heading_count']}")
        print(f"   缺号:     {q['missing_numeric_chapter_numbers_count']}")
        print(f"   重号:     {q['duplicate_numeric_chapter_numbers']}")
        sc = q['suspicious_counts']
        suspicious = {k: v for k, v in sc.items() if v > 0}
        print(f"   噪声:     {suspicious if suspicious else '✅ 全部清零'}")
        if q['acceptance_issues']:
            print(f"   问题:     {q['acceptance_issues']}")
        return q['acceptance_status'] == 'pass'
    return False


def main():
    parser = argparse.ArgumentParser(description="Trae 网文下载器")
    parser.add_argument("--urls", type=Path, help="章节URL列表文件")
    parser.add_argument("--toc", help="目录页URL（自动提取链接）")
    parser.add_argument("--output", type=Path, default=Path("novel.txt"), help="输出TXT路径")
    parser.add_argument("--title", default="novel", help="书名")
    parser.add_argument("--expected", type=int, default=0, help="期望章节数")
    parser.add_argument("--check", type=Path, help="只做质量验证")
    parser.add_argument("--required-term", default="", help="源漂移关键词")
    args = parser.parse_args()

    if args.check:
        ok = cmd_check(args.check, args.expected, args.required_term)
        sys.exit(0 if ok else 1)

    if args.toc:
        ok = cmd_toc(args.toc, args.output, args.title, args.expected)
        if not ok:
            sys.exit(1)
    elif args.urls:
        cmd_download(args.urls, args.output, args.title, args.expected)
    else:
        print("❌ 需要 --urls 或 --toc")
        sys.exit(1)

    # 自动质检
    if args.output.exists():
        print(f"\n{'='*50}")
        cmd_check(args.output, args.expected, args.required_term)


if __name__ == "__main__":
    main()
