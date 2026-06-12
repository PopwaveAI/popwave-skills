#!/usr/bin/env python3
"""章纲 → 标签 → 检索 → 注入闸门。

用法：
    # 直接传入叙事功能字符串，输出到 stdout
    python scripts/search_fragments.py --narrative "势均力敌战 + 营救" --top 3

    # 从章纲 md 自动提取叙事功能字段，注入到闸门文件
    python scripts/search_fragments.py \\
        --chapter-outline 02-章纲/ch005-章纲.md \\
        --inject-to 03-闸门/_prompt_ch005.md

    # 仅输出 JSON（不写闸门）
    python scripts/search_fragments.py --narrative "对话 + 招募" --json
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _internal.db import get_conn  # noqa: E402
from _internal.injector import format_injection  # noqa: E402
from _internal.retriever import log_usage, retrieve  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("search_fragments")

# 章纲 md 中"叙事功能"字段的提取
NARRATIVE_FIELD_RE = re.compile(
    r"^\s*[-*]?\s*[*_]*叙事功能[*_]*\s*[:：]\s*(.+)$",
    re.MULTILINE,
)


def extract_narrative_from_outline(md_path: Path) -> str:
    """从章纲 md 提取'叙事功能: xxx'字段。"""
    text = md_path.read_text(encoding="utf-8")
    m = NARRATIVE_FIELD_RE.search(text)
    if not m:
        raise ValueError(f"未在 {md_path} 中找到'叙事功能'字段")
    return m.group(1).strip()


def inject_to_gate_file(gate_path: Path, injection_md: str) -> None:
    """
    将检索结果注入到闸门文件。

    规则：
    - 若文件存在且有 '## 🔴声音锁' 区块 → 替换整个区块
    - 否则追加到文件末尾
    """
    gate_path.parent.mkdir(parents=True, exist_ok=True)

    if not gate_path.exists():
        gate_path.write_text(injection_md, encoding="utf-8")
        logger.info("✓ 已新建闸门文件: %s", gate_path)
        return

    existing = gate_path.read_text(encoding="utf-8")
    # 查找已有声音锁区块
    pattern = re.compile(
        r"## 🔴声音锁.*?(?=\n## |\Z)",
        re.DOTALL,
    )
    if pattern.search(existing):
        new_text = pattern.sub(injection_md.strip(), existing)
    else:
        new_text = existing.rstrip() + "\n\n" + injection_md
    gate_path.write_text(new_text, encoding="utf-8")
    logger.info("✓ 已更新闸门文件: %s", gate_path)


def main() -> None:
    ap = argparse.ArgumentParser(description="章纲 → 锚定片段检索 → 注入闸门")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--narrative", help="直接传入叙事功能字符串")
    src.add_argument("--chapter-outline", help="章纲 md 文件路径（自动提取叙事功能）")

    ap.add_argument("--top", type=int, default=3, help="返回片段数（默认 3）")
    ap.add_argument("--project", default="default", help="项目名（用于 usage_log 去重）")
    ap.add_argument(
        "--chapter",
        default="unknown",
        help="当前写作章节标识（用于 usage_log）",
    )
    ap.add_argument(
        "--inject-to",
        help="闸门文件路径。指定则写入该文件，否则输出到 stdout",
    )
    ap.add_argument("--json", action="store_true", help="以 JSON 输出候选片段")
    args = ap.parse_args()

    # 1. 获取叙事功能字符串
    if args.narrative:
        narrative = args.narrative
        chapter_hint = args.chapter
    else:
        outline_path = Path(args.chapter_outline)
        narrative = extract_narrative_from_outline(outline_path)
        chapter_hint = outline_path.stem
        logger.info("从 %s 提取到叙事功能: %s", outline_path.name, narrative)

    # 2. 执行检索
    with get_conn() as conn:
        candidates = retrieve(
            conn,
            narrative,
            project=args.project,
            top_n=args.top,
        )

        if not candidates:
            logger.warning("无匹配片段")
        else:
            logger.info(
                "检索到 %d 条候选（层级：%s，书源：%s）",
                len(candidates),
                {c.match_level for c in candidates},
                {c.source_book for c in candidates},
            )
            # 记录使用
            log_usage(conn, args.project, chapter_hint, candidates)

    # 3. 输出
    if args.json:
        print(json.dumps(
            [asdict(c) for c in candidates],
            ensure_ascii=False,
            indent=2,
        ))
        return

    injection_md = format_injection(candidates, narrative)
    if args.inject_to:
        inject_to_gate_file(Path(args.inject_to), injection_md)
    else:
        print(injection_md)


if __name__ == "__main__":
    main()
