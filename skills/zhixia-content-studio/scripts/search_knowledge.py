#!/usr/bin/env python3
"""Search curated Markdown knowledge files in this skill."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="检索知夏主题知识")
    parser.add_argument("query", nargs="+", help="一个或多个关键词")
    parser.add_argument("--context", type=int, default=1, help="命中行前后文行数")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1] / "references" / "knowledge"
    terms = [term.casefold() for term in args.query]
    found = False

    for path in sorted(root.rglob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        hits = [
            i for i, line in enumerate(lines)
            if all(term in line.casefold() for term in terms)
        ]
        for i in hits:
            found = True
            start = max(0, i - args.context)
            end = min(len(lines), i + args.context + 1)
            print(f"\n{path.relative_to(root)}:{i + 1}")
            for j in range(start, end):
                mark = ">" if j == i else " "
                print(f"{mark} {j + 1:4}: {lines[j]}")

    if not found:
        print("未找到匹配内容。可减少关键词或换同义词。")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
