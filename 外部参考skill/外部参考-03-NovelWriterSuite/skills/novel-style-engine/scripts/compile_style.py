#!/usr/bin/env python3
"""
novel-style-engine 写法编译器。

读取 style/features.md + style/anti-ai.md + story.md，
按 task 类型编译成 5 个 prompt block 到 style/compiled/。

用法：
    python3 compile_style.py --vault /path/to/vault --task chapter
    python3 compile_style.py --vault . --task polish

task 选项：
    chapter   章节正文生成（默认）
    continue  续写
    polish    润色
    rewrite   改写
    fix-ai    AI 味修正

借鉴 AI-NWA prompt-compiler v1 设计，独立重写。
"""

import argparse
import re
import sys
from pathlib import Path

# task 配置矩阵：决定每个 layer 的强度
TASK_CONFIG: dict[str, dict] = {
    "chapter": {
        "style_strength": "high",
        "anti_ai_strength": "high",
        "self_check": True,
        "extra_constraint": "字数按 word-target 控制",
    },
    "continue": {
        "style_strength": "high",
        "anti_ai_strength": "high",
        "self_check": True,
        "extra_constraint": "必须延续前文气质，禁止突然升华主题或改变叙述节奏",
    },
    "polish": {
        "style_strength": "medium",
        "anti_ai_strength": "medium",
        "self_check": True,
        "extra_constraint": "不增加新剧情信息，不改变人物关系，不改变事件结果",
    },
    "rewrite": {
        "style_strength": "high",
        "anti_ai_strength": "high",
        "self_check": True,
        "extra_constraint": "保留事实顺序不变，只替换表达方式 / 情绪传达方式 / 节奏",
    },
    "fix-ai": {
        "style_strength": "none",
        "anti_ai_strength": "high",
        "self_check": False,
        "extra_constraint": "只修改违规表达，保留剧情事实不变",
    },
}

# 强度档措辞映射
TIER_WORDING = {
    "high": {
        "verb_must": "必须",
        "verb_forbid": "禁止 / 不得",
        "verb_avoid": "禁止",
        "intensity_desc": "硬约束 - 写完自检发现违规请立即改正",
    },
    "medium": {
        "verb_must": "优先",
        "verb_forbid": "注意避免",
        "verb_avoid": "警惕",
        "intensity_desc": "软约束 - 倾向遵守，特殊情况可以让步",
    },
    "low": {
        "verb_must": "尽量",
        "verb_forbid": "倾向避免",
        "verb_avoid": "留意",
        "intensity_desc": "提示 - 仅作风格倾向参考",
    },
    "none": {
        "verb_must": "",
        "verb_forbid": "",
        "verb_avoid": "",
        "intensity_desc": "",
    },
}


def weight_to_tier(weight: float) -> str:
    """按权重选档。"""
    if weight >= 0.85:
        return "high"
    if weight >= 0.65:
        return "medium"
    if weight >= 0.30:
        return "low"
    return "none"


def task_aware_tier(feature_tier: str, task_strength: str) -> str:
    """task 强度对 feature tier 的降档。

    比如 task=polish 时整体降一档：原本 high → medium。
    """
    if task_strength == "none":
        return "none"
    order = ["none", "low", "medium", "high"]
    f_idx = order.index(feature_tier)
    t_idx = order.index(task_strength)
    return order[min(f_idx, t_idx)]


def parse_features(path: Path) -> dict:
    """简易解析 style/features.md 中的 ### category 块和 - enabled/weight/rule 列表。

    不引入 YAML 库——只解析我们自己的结构。
    """
    if not path.is_file():
        return {"categories": {}}

    text = path.read_text(encoding="utf-8")

    # 跳过 frontmatter
    if text.startswith("---"):
        parts = text.split("\n---\n", 1)
        text = parts[1] if len(parts) > 1 else text

    categories: dict[str, list[dict]] = {}
    current_cat: str | None = None
    current_item: dict | None = None

    for line in text.split("\n"):
        stripped = line.strip()

        cat_match = re.match(r"^###\s+([\w-]+)\s*$", stripped)
        if cat_match:
            if current_item and current_cat:
                categories.setdefault(current_cat, []).append(current_item)
                current_item = None
            current_cat = cat_match.group(1)
            categories.setdefault(current_cat, [])
            continue

        if stripped.startswith("- enabled:"):
            if current_item and current_cat:
                categories.setdefault(current_cat, []).append(current_item)
            current_item = {"enabled": "true" in stripped.lower()}
            continue

        if current_item is not None and ":" in stripped and not stripped.startswith("-"):
            key, _, value = stripped.partition(":")
            current_item[key.strip()] = value.strip().strip('"').strip("'")

    if current_item and current_cat:
        categories.setdefault(current_cat, []).append(current_item)

    return {"categories": categories}


def parse_anti_ai(path: Path) -> dict:
    """解析 style/anti-ai.md 的 forbidden / risk / encourage 三段。"""
    if not path.is_file():
        return {"forbidden": [], "risk": [], "encourage": []}

    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("\n---\n", 1)
        text = parts[1] if len(parts) > 1 else text

    sections: dict[str, list[dict]] = {"forbidden": [], "risk": [], "encourage": []}
    current_section: str | None = None
    current_rule: dict | None = None

    for line in text.split("\n"):
        stripped = line.strip()

        m = re.match(r"^##\s+(forbidden|risk|encourage)", stripped, re.IGNORECASE)
        if m:
            if current_rule and current_section:
                sections[current_section].append(current_rule)
                current_rule = None
            current_section = m.group(1).lower()
            continue

        if stripped.startswith("- "):
            if current_rule and current_section:
                sections[current_section].append(current_rule)
            current_rule = {}
            # 一行内可能有 key: value
            inner = stripped[2:]
            if ":" in inner:
                k, _, v = inner.partition(":")
                current_rule[k.strip()] = v.strip().strip('"').strip("'")
            continue

        if current_rule is not None and ":" in stripped:
            k, _, v = stripped.partition(":")
            current_rule[k.strip()] = v.strip().strip('"').strip("'")

    if current_rule and current_section:
        sections[current_section].append(current_rule)

    return sections


def render_style_rules(features: dict, task_strength: str) -> str:
    """编译 Layer 2 写法主规则层。"""
    if task_strength == "none":
        return "<!-- 此任务不注入写法规则 -->\n"

    categories = features.get("categories", {})
    out_lines = ["# 写法规则（Layer 2）", ""]

    cat_order = ["narrative", "character-voice", "language", "rhythm"]
    cat_labels = {
        "narrative": "叙事方式",
        "character-voice": "人物表达",
        "language": "语言风格",
        "rhythm": "节奏控制",
    }

    for cat in cat_order:
        items = categories.get(cat, [])
        active = [it for it in items if it.get("enabled", False)]
        if not active:
            continue

        out_lines.append(f"## {cat_labels.get(cat, cat)}")
        out_lines.append("")

        for it in active:
            try:
                w = float(it.get("weight", "0.5"))
            except ValueError:
                w = 0.5
            tier = task_aware_tier(weight_to_tier(w), task_strength)
            if tier == "none":
                continue
            verb = TIER_WORDING[tier]["verb_must"]
            rule = it.get("rule", "(no rule text)")
            line = f"- {verb}：{rule}" if verb else f"- {rule}"
            if "example-good" in it:
                line += f"\n  - 正例：{it['example-good']}"
            if "example-bad" in it:
                line += f"\n  - 反例：{it['example-bad']}"
            out_lines.append(line)
        out_lines.append("")

    return "\n".join(out_lines)


def render_anti_ai(rules: dict, task_strength: str) -> str:
    """编译 Layer 4 反 AI 约束层。"""
    if task_strength == "none":
        return "<!-- 此任务不注入反 AI 约束 -->\n"

    tier = task_strength
    verb_forbid = TIER_WORDING[tier]["verb_forbid"]
    verb_avoid = TIER_WORDING[tier]["verb_avoid"]

    out = ["# 反 AI 约束（Layer 4）", "", f"_强度档位：{tier} - {TIER_WORDING[tier]['intensity_desc']}_", ""]

    if rules.get("forbidden"):
        out.append("## A. 禁止项")
        out.append("")
        for r in rules["forbidden"]:
            pattern = r.get("pattern", "?")
            desc = r.get("description", "")
            line = f"- {verb_forbid} 出现：`{pattern}`"
            if desc:
                line += f"（{desc}）"
            out.append(line)
        out.append("")

    if rules.get("risk"):
        out.append("## B. 风险监控（频次限制）")
        out.append("")
        for r in rules["risk"]:
            pattern = r.get("pattern", "?")
            limit = r.get("max-per-3000") or r.get("max-density-per-1000")
            desc = r.get("description", "")
            line = f"- {verb_avoid} 过度使用：`{pattern}`"
            if limit:
                line += f"（上限 {limit}）"
            if desc:
                line += f" - {desc}"
            out.append(line)
        out.append("")

    if rules.get("encourage"):
        out.append("## C. 鼓励出现")
        out.append("")
        for r in rules["encourage"]:
            desc = r.get("description", "")
            out.append(f"- 优先加入：{desc}")
        out.append("")

    return "\n".join(out)


def render_global_context(story_md_path: Path) -> str:
    """编译 Layer 1 世界与任务基础层（story.md 摘要）。"""
    if not story_md_path.is_file():
        return "<!-- story.md 未找到 -->\n"

    text = story_md_path.read_text(encoding="utf-8")

    out = ["# 全书基础上下文（Layer 1）", ""]

    # frontmatter 提要
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if fm_match:
        out.append("## 基础信息")
        out.append("")
        out.append("```yaml")
        out.append(fm_match.group(1))
        out.append("```")
        out.append("")
        text = text[fm_match.end():]

    # 拷贝特定 section
    for section_name in ["一句话简介", "核心矛盾", "30 章承诺", "题材定位", "文风方向"]:
        pat = re.compile(rf"^##\s+{re.escape(section_name)}\s*$(.*?)(?=^##\s|\Z)", re.DOTALL | re.MULTILINE)
        m = pat.search(text)
        if m:
            content = m.group(1).strip()
            if content and not content.startswith("<!--"):
                out.append(f"## {section_name}")
                out.append("")
                out.append(content)
                out.append("")

    return "\n".join(out)


def render_output_format(task: str, extra: str) -> str:
    """编译 Layer 5 输出格式层。"""
    base_lines = {
        "chapter": [
            "请输出本章正文。",
            "- 直接输出正文，不要标题不要解释",
            "- 段落用空行分隔",
            "- 章节末尾用 `## hook-账` 段记录本章实际的 advance / resolve / open / defer",
        ],
        "continue": [
            "请输出续写部分。",
            "- 直接续写，不要重复前文",
            "- 保持前文的人称、时态、节奏",
        ],
        "polish": [
            "请输出润色后的文本。",
            "- 不增剧情、不改人物关系",
            "- 保持事件结果不变",
        ],
        "rewrite": [
            "请输出改写后的文本。",
            "- 保留事实顺序不变",
            "- 替换表达方式 / 情绪传达 / 节奏",
        ],
        "fix-ai": [
            "请输出修正后的文本。",
            "- 仅修改违规表达",
            "- 保留剧情事实",
        ],
    }
    lines = ["# 输出格式（Layer 5）", ""]
    lines.extend(base_lines.get(task, base_lines["chapter"]))
    if extra:
        lines.append(f"- {extra}")
    return "\n".join(lines) + "\n"


def render_self_check(enabled: bool, anti_ai_rules: dict) -> str:
    """编译 Layer 6 自检指令层。"""
    if not enabled:
        return "<!-- 此任务不要求自检 -->\n"

    items = ["写完后请自检："]
    for r in anti_ai_rules.get("forbidden", []):
        pattern = r.get("pattern", "?")
        items.append(f"- 是否出现了 `{pattern}` → 改写")
    items.append("- 段落长度是否过于均匀（变异系数 < 0.15）→ 调整")
    items.append("- 章节结尾是否有具体钩子 → 没有则补一个")
    items.append("")
    items.append("若有违规，先修正再输出最终正文。")

    return "# 自检（Layer 6）\n\n" + "\n".join(items) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="novel-style-engine 编译器")
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--task", default="chapter", choices=list(TASK_CONFIG.keys()))
    args = parser.parse_args()

    vault: Path = args.vault.resolve()
    config = TASK_CONFIG[args.task]

    features = parse_features(vault / "style" / "features.md")
    anti_ai = parse_anti_ai(vault / "style" / "anti-ai.md")

    compiled_dir = vault / "style" / "compiled"
    compiled_dir.mkdir(parents=True, exist_ok=True)

    # 5 个 prompt block
    (compiled_dir / "global-context.md").write_text(
        render_global_context(vault / "story.md"), encoding="utf-8"
    )
    (compiled_dir / "style-rules.md").write_text(
        render_style_rules(features, config["style_strength"]), encoding="utf-8"
    )
    (compiled_dir / "anti-ai.md").write_text(
        render_anti_ai(anti_ai, config["anti_ai_strength"]), encoding="utf-8"
    )
    (compiled_dir / "output-format.md").write_text(
        render_output_format(args.task, config["extra_constraint"]), encoding="utf-8"
    )
    (compiled_dir / "self-check.md").write_text(
        render_self_check(config["self_check"], anti_ai), encoding="utf-8"
    )

    # 计数报告
    feature_count = sum(
        1
        for cat_items in features.get("categories", {}).values()
        for it in cat_items
        if it.get("enabled", False)
    )
    print(f"✅ 写法已编译（task={args.task}）")
    print(f"   启用特征：{feature_count} 条")
    print(f"   反 AI 规则：{len(anti_ai.get('forbidden', []))} forbidden + "
          f"{len(anti_ai.get('risk', []))} risk + {len(anti_ai.get('encourage', []))} encourage")
    print(f"   输出：{compiled_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
