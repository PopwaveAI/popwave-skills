#!/usr/bin/env python3
"""
novel-suite vault 结构校验器 —— 检查 vault 是否符合 DESIGN.md 第 3 节的标准结构。

用法：
    python3 validate_structure.py --vault /path/to/vault

退出码：
    0 - 结构合规
    1 - 有 critical 错误（必填项缺失）
    2 - 仅有 warning（可选项缺失）

输出格式：
    每行一条 issue：[severity] path: message
"""

import argparse
import re
import sys
from pathlib import Path

# 必需目录（缺失即 critical）
REQUIRED_DIRS = [
    "characters",
    "worldbuilding",
    "worldbuilding/locations",
    "worldbuilding/systems",
    "plot",
    "plot/arcs",
    "chapters",
    "style",
    "style/samples",
]

# 推荐目录（缺失只是 warning）
OPTIONAL_DIRS = [
    "style/compiled",
    "deliverables",
    ".memory",
    ".memory/checkpoints",
]

# 必需文件
REQUIRED_FILES = [
    "story.md",
    "status.md",
    "characters/_index.md",
    "worldbuilding/_index.md",
    "plot/_index.md",
    "plot/timeline.md",
    "plot/foreshadowing.md",
    "chapters/_index.md",
    "style/_index.md",
]

# story.md frontmatter 必填字段
STORY_REQUIRED_FIELDS = ["title", "length-target", "genre", "pov", "tense", "status"]


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """提取 markdown 文件顶部的 YAML frontmatter（简单解析，不引入 PyYAML）。

    只支持 key: value 单行格式，足够当前 schema。
    """
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return None
    body = match.group(1)
    fields: dict[str, str] = {}
    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def check(vault: Path) -> tuple[list[str], list[str]]:
    """返回 (critical_issues, warnings)。"""
    critical: list[str] = []
    warnings: list[str] = []

    if not vault.exists() or not vault.is_dir():
        critical.append(f"vault 路径不存在或不是目录：{vault}")
        return critical, warnings

    for d in REQUIRED_DIRS:
        if not (vault / d).is_dir():
            critical.append(f"缺少必需目录：{d}/")

    for d in OPTIONAL_DIRS:
        if not (vault / d).is_dir():
            warnings.append(f"缺少推荐目录：{d}/（按需自动创建）")

    for f in REQUIRED_FILES:
        if not (vault / f).is_file():
            critical.append(f"缺少必需文件：{f}")

    # story.md frontmatter 完整性
    story = vault / "story.md"
    if story.is_file():
        text = story.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            critical.append("story.md 缺少 YAML frontmatter")
        else:
            for field in STORY_REQUIRED_FIELDS:
                if field not in fm or not fm[field]:
                    critical.append(f"story.md frontmatter 缺少字段：{field}")

    return critical, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="novel-suite vault 结构校验")
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--quiet", action="store_true", help="只输出退出码")
    args = parser.parse_args()

    vault: Path = args.vault.resolve()
    critical, warnings = check(vault)

    if not args.quiet:
        for issue in critical:
            print(f"[critical] {issue}")
        for issue in warnings:
            print(f"[warning] {issue}")
        if not critical and not warnings:
            print(f"✅ vault 结构合规：{vault}")
        else:
            print(f"\nvault: {vault}")
            print(f"critical: {len(critical)}, warning: {len(warnings)}")

    if critical:
        return 1
    if warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
