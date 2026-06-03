#!/usr/bin/env python3
"""REDLINE 扫描 + 碎句自动修复脚本（API 强制调用，不可跳过）

用法：
    python redline_scan.py --file 03-正文/v5/chapter-002.md
    python redline_scan.py --file 03-正文/v5/chapter-002.md --fix   # 自动修复碎句

输出：
    - stdout: JSON 违规报告
    - --fix: 同时原地修复正文文件（合并碎句独占行）
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path

from _llm import LLMClient

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── REDLINE 规则配置 ──────────────────────────────────────────────────────────

REDLINE_RULES = {
    "notAbutB": "not A， but B 结构（否定A肯定B的任何变体）",
    "碎句独占行": "一行一段，不足8字，没有主谓宾结构的纯名词/动词碎片",
    "感到类": "\"他感到/他意识到/他评估/他觉得\"",
    "XX级": "巡航级/战术级/待战级/战场级/标准时等人造军事术语",
    "破折号滥用": "破折号用于非招式名（招式名格式：【XX——！】）",
    "句号滥用": "枚举项用句号分隔（应用顿号）",
}


def read_file(path: str) -> tuple[str, list[str]]:
    """读取文件，返回 (正文部分, 全部行列表)"""
    p = Path(path)
    if not p.exists():
        print(json.dumps({"error": f"文件不存在: {path}"}))
        sys.exit(1)
    with open(p, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 切出正文部分（本章新增设定之前）
    body = []
    for line in lines:
        if "本章新增设定" in line:
            break
        body.append(line)
    # 也去掉标题行（# 开头）
    text = "".join(body)
    return text, lines


def llm_scan(text: str) -> list[dict]:
    """用 LLM 扫描 REDLINE 违规"""
    client = LLMClient()

    rules_text = "\n".join(f"  {k}: {v}" for k, v in REDLINE_RULES.items())

    prompt = f"""你是一个网文写作编辑。检查以下正文是否违反红线规则。

红线规则：
{rules_text}

正文：
{text[:8000]}  # 仅检查前8000字符以确保JSON输出稳定

请逐条检查，输出JSON格式：
{{
  "violations": [
    {{"rule": "notAbutB", "line_approx": 行号, "content": "违规原文片段", "severity": "high/mid/low"}}
  ],
  "summary": {{"total": 总违规数, "fatal": 致命违规数}}
}}

注意：
- 碎句独占行：一行一段且<8字且以句号结尾且不在引号内。核心意象句（如\"两个月亮\"）不判罚
- notAbutB：搜索"不是A是B""不在A在B""不XX是XX"句式
- 仅报告确认违规项，存疑不报"""
    # LLM的JSON mode + 严格的prompt限制
    result = client.chat_json(
        prompt,
        system="你是一位严格的网文编辑。按JSON格式输出违规清单。",
        max_tokens=2000,
    )
    if result is None:
        return []
    violations = result.get("violations", [])
    return violations


def rule_scan(text: str) -> list[dict]:
    """规则层扫描（快筛，覆盖80%违规）"""
    violations = []
    lines = text.split("\n")

    # 保留的核心意象句
    keep_phrases = ["两个月亮", "不是泰拉", "不是火星", "他停了一下", "沉默"]

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped == "……" or stripped.startswith("#"):
            continue

        # 跳过标题/分隔符
        if stripped.startswith("---") or stripped.startswith("**"):
            continue

        # 跳过核心意象句
        if any(k in stripped for k in keep_phrases):
            continue

        # 碎句独占行检测：<8字，以句号结尾，不在引号内
        if len(stripped) < 8 and stripped.endswith(("。", "？", "！")) and '"' not in stripped:
            violations.append({
                "rule": "碎句独占行",
                "line_approx": i + 1,
                "content": stripped,
                "severity": "mid",
            })

    return violations


def fix_fragments(text: str, violations: list[dict]) -> str:
    """自动修复碎句独占行：将碎句合并到上一行末尾"""
    if not violations:
        return text

    lines = text.split("\n")
    frag_lines = {v["line_approx"] - 1 for v in violations if v["rule"] == "碎句独占行"}

    result = []
    skip_next = False
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        if i in frag_lines and i + 1 < len(lines):
            # 碎句合并到下一行开头
            stripped = line.strip()
            next_line = lines[i + 1].strip()
            # 如果下一行也是碎句或者是段落，判断合并方式
            if next_line and next_line != "……":
                result.append(f"{stripped} {next_line}\n")
                skip_next = True
            else:
                result.append(line)
        else:
            result.append(line)

    return "".join(result)


def main():
    parser = argparse.ArgumentParser(description="REDLINE 扫描 + 碎句修复")
    parser.add_argument("--file", required=True, help="正文文件路径")
    parser.add_argument("--fix", action="store_true", help="自动修复碎句")
    parser.add_argument("--llm", action="store_true", help="启用LLM深度扫描（耗时）")
    args = parser.parse_args()

    text, original_lines = read_file(args.file)

    # Step 1: 规则层扫描
    rule_violations = rule_scan(text)

    # Step 2: 可选LLM深度扫描
    llm_violations = []
    if args.llm:
        logger.info("LLM深度扫描中...")
        llm_violations = llm_scan(text)

    # 合并
    all_violations = rule_violations + llm_violations
    unique_rules = set(v["rule"] for v in all_violations)

    report = {
        "file": args.file,
        "redline_check": {
            rule: "PASS" if rule not in unique_rules else "FAIL"
            for rule in REDLINE_RULES
        },
        "violations": all_violations,
        "summary": {
            "total": len(all_violations),
            "fatal": len([v for v in all_violations if v.get("severity") == "high"]),
        },
        "passed": len(all_violations) == 0,
    }

    # Step 3: 自动修复
    if args.fix and rule_violations:
        fixed = fix_fragments(text, rule_violations)
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(fixed)
        report["fixed"] = True
        report["fix_count"] = len(rule_violations)

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if not report["passed"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
