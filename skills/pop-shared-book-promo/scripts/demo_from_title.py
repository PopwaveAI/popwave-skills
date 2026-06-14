#!/usr/bin/env python3
"""
pop-shared-book-promo — 快速演示入口
输入书名，生成女主角 IP 卡 HTML。
不现场调用慢速图像模型，使用预构建资产。
"""
import argparse
import subprocess
import sys
from pathlib import Path

# 相对于 pop-shared-book-promo 根目录的路径
SKILL_ROOT = Path(__file__).resolve().parent.parent

KNOWN_BOOKS = {
    "千屿": str(SKILL_ROOT / "qianyu" / "heroine_card.json")
}


def main() -> None:
    parser = argparse.ArgumentParser(description="投资人演示入口：输入书名，生成女主角 IP 卡")
    parser.add_argument("--title", required=True, help="书名，例如：千屿")
    parser.add_argument("--output-dir", default=Path.cwd(), type=Path)
    args = parser.parse_args()

    if args.title not in KNOWN_BOOKS:
        known = "、".join(KNOWN_BOOKS)
        raise SystemExit(f"暂未内置《{args.title}》资产。当前 demo 可用：{known}")

    output = args.output_dir / f"{args.title}_女主角IP卡.html"
    build_script = SKILL_ROOT / "scripts" / "build_heroine_card.py"

    cmd = [
        sys.executable,
        "-B",
        str(build_script),
        "--input",
        KNOWN_BOOKS[args.title],
        "--output",
        str(output),
    ]
    subprocess.run(cmd, check=True)
    print(f"已生成：{output.resolve()}")


if __name__ == "__main__":
    main()
