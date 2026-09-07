#!/usr/bin/env python3
"""
novel-review/check_ai_tells.py —— 4 维结构性 AI 检测（统计学）。

借鉴 inkos packages/core/src/agents/ai-tells.ts 算法，独立重写为 Python，加汉字适配。

4 维：
- dim-20: 段落长度变异系数 < 0.15 → warning（段落过于均匀）
- dim-21: 套话密度（"似乎/可能/或许"等）> 3 次/千字 → warning
- dim-22: 同一转折词（"然而/不过/与此同时"等）≥ 3 次 → warning
- dim-23: 连续 ≥ 3 句相同开头模式（列表化结构）→ info

用法：
    python3 check_ai_tells.py --chapter chapters/ch-008.md
    python3 check_ai_tells.py --chapter chapters/ch-008.md --json   # JSON 输出
"""

import argparse
import json
import re
import sys
from pathlib import Path
from statistics import mean, stdev

HEDGE_WORDS = ["似乎", "可能", "或许", "大概", "某种程度上", "一定程度上", "在某种意义上"]
TRANSITION_WORDS = ["然而", "不过", "与此同时", "另一方面", "尽管如此", "话虽如此", "但值得注意的是"]


def strip_frontmatter_and_outline(text: str) -> str:
    """去掉 frontmatter 和章纲段，只保留正文。"""
    # 去 frontmatter
    if text.startswith("---"):
        parts = text.split("\n---\n", 1)
        if len(parts) >= 2:
            text = parts[1]

    # 去掉 ## 本章章纲 / ## hook-账 / 等 metadata 段，保留 --- 后的正文
    # 我们的章节格式：章纲 + hook-账 + --- + 正文
    if "\n---\n" in text:
        text = text.split("\n---\n", 1)[1]

    return text.strip()


def chinese_char_count(text: str) -> int:
    return len(re.findall(r"[一-鿿]", text))


def split_paragraphs(text: str) -> list[str]:
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"([。！？…]+|\.\.\.|\.{3,})", text)
    sentences: list[str] = []
    buffer = ""
    for p in parts:
        if re.match(r"[。！？…]+|\.\.\.|\.{3,}", p):
            buffer += p
            if buffer.strip():
                sentences.append(buffer.strip())
            buffer = ""
        else:
            buffer += p
    if buffer.strip():
        sentences.append(buffer.strip())
    return [s for s in sentences if chinese_char_count(s) > 0]


def check_dim20_paragraph_uniformity(text: str) -> list[dict]:
    """段落长度变异系数 < 0.15 → warning"""
    paragraphs = split_paragraphs(text)
    if len(paragraphs) < 3:
        return []

    lengths = [chinese_char_count(p) for p in paragraphs]
    avg = mean(lengths)
    if avg <= 0:
        return []

    std = stdev(lengths) if len(lengths) >= 2 else 0
    cv = std / avg

    if cv < 0.15:
        return [
            {
                "severity": "warning",
                "dimension": "dim-20.paragraph-uniformity",
                "location": f"全章 {len(paragraphs)} 段",
                "description": f"段落长度变异系数 {cv:.3f}（阈值 < 0.15），段落长度过于均匀，呈 AI 生成特征",
                "suggestion": "增加段落长度差异：短段用于节奏加速或冲击，长段用于沉浸描写",
            }
        ]
    return []


def check_dim21_hedge_density(text: str) -> list[dict]:
    """套话密度 > 3 次/千字 → warning"""
    total = chinese_char_count(text)
    if total == 0:
        return []

    counts: dict[str, int] = {}
    total_hedge = 0
    for w in HEDGE_WORDS:
        c = len(re.findall(w, text))
        if c > 0:
            counts[w] = c
            total_hedge += c

    density = total_hedge / (total / 1000)
    if density > 3:
        detail = "、".join(f'"{w}"×{c}' for w, c in counts.items())
        return [
            {
                "severity": "warning",
                "dimension": "dim-21.hedge-density",
                "location": "全章",
                "description": f"套话密度 {density:.1f} 次/千字（阈值 > 3）。明细：{detail}",
                "suggestion": "用确定性叙述替代模糊表达：去掉「似乎」改为直接描述状态，用具体细节替代「可能」",
            }
        ]
    return []


def check_dim22_formulaic_transitions(text: str) -> list[dict]:
    """同一转折词 ≥ 3 次 → warning"""
    counts: dict[str, int] = {}
    for w in TRANSITION_WORDS:
        c = len(re.findall(w, text))
        if c > 0:
            counts[w] = c

    repeated = {w: c for w, c in counts.items() if c >= 3}
    if not repeated:
        return []

    detail = "、".join(f'"{w}"×{c}' for w, c in repeated.items())
    return [
        {
            "severity": "warning",
            "dimension": "dim-22.formulaic-transitions",
            "location": "全章",
            "description": f"转折词重复 ≥ 3 次：{detail}。同一转折模式高频暴露 AI 生成痕迹",
            "suggestion": "用情节自然转折替代转折词，或换不同过渡手法（动作切入、时间跳跃、视角切换）",
        }
    ]


def check_dim23_list_like_structure(text: str) -> list[dict]:
    """连续 ≥ 3 句相同开头 → info（列表化结构）"""
    sentences = split_sentences(text)
    if len(sentences) < 3:
        return []

    max_consec = 1
    consec = 1
    for i in range(1, len(sentences)):
        prev_prefix = sentences[i - 1][:2]
        curr_prefix = sentences[i][:2]
        if prev_prefix == curr_prefix:
            consec += 1
            max_consec = max(max_consec, consec)
        else:
            consec = 1

    if max_consec >= 3:
        return [
            {
                "severity": "info",
                "dimension": "dim-23.list-like-structure",
                "location": "全章",
                "description": f"检测到 {max_consec} 句连续相同开头模式，呈现列表式 AI 生成结构",
                "suggestion": "变换句式开头：用不同主语、时间词、动作词开头，打破列表感",
            }
        ]
    return []


def run(chapter_path: Path) -> dict:
    text = chapter_path.read_text(encoding="utf-8")
    body = strip_frontmatter_and_outline(text)

    issues: list[dict] = []
    issues.extend(check_dim20_paragraph_uniformity(body))
    issues.extend(check_dim21_hedge_density(body))
    issues.extend(check_dim22_formulaic_transitions(body))
    issues.extend(check_dim23_list_like_structure(body))

    return {
        "checker": "check_ai_tells",
        "chapter": str(chapter_path.name),
        "passed": all(i["severity"] != "critical" for i in issues),
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="check_ai_tells - 4 维 AI 痕迹统计检测")
    parser.add_argument("--chapter", type=Path, required=True)
    parser.add_argument("--json", action="store_true", help="输出 JSON 而非可读格式")
    args = parser.parse_args()

    if not args.chapter.is_file():
        print(f"❌ 章节文件不存在：{args.chapter}", file=sys.stderr)
        return 1

    result = run(args.chapter)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"🔍 check_ai_tells - {args.chapter.name}")
        print(f"   passed: {result['passed']}")
        print(f"   issues: {len(result['issues'])}")
        for issue in result["issues"]:
            sev = issue["severity"].upper()
            print(f"\n   [{sev}] {issue['dimension']} @ {issue['location']}")
            print(f"     {issue['description']}")
            print(f"     建议：{issue['suggestion']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
