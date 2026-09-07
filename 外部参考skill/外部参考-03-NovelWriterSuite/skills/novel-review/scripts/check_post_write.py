#!/usr/bin/env python3
"""
novel-review/check_post_write.py —— 硬规则违规检测。

借鉴 inkos packages/core/src/agents/post-write-validator.ts，独立重写为 Python。
规则源是 style/anti-ai.md（项目级，可定制）；如果没有则用 references/default-anti-ai.md。

用法：
    python3 check_post_write.py --chapter chapters/ch-008.md --vault {vault}
    python3 check_post_write.py --chapter chapters/ch-008.md --vault {vault} --json
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 默认规则（如果 vault 里没有 style/anti-ai.md）
DEFAULT_FORBIDDEN = [
    {"pattern": r"不是[^，。！？\n]{0,30}[，,]?\s*而是", "desc": "AI 句式：不是…而是…"},
    {"pattern": r"并非[^，。！？\n]{0,30}[，,]?\s*而是", "desc": "AI 句式变体：并非…而是…"},
    {"pattern": r"——", "desc": "中文网文禁用：破折号"},
    {"pattern": r"读者(可能|会|应该|也许)", "desc": "元叙事 - 跳出叙述跟读者对话"},
    {"pattern": r"接下来(就是|将会|即将)", "desc": "编剧旁白模式"},
    {"pattern": r"我们(可以|不妨|来看)", "desc": "讲解员口吻"},
    {"pattern": r"值得注意的是", "desc": "学术报告腔"},
    {"pattern": r"(核心|关键)在于", "desc": "学术报告腔"},
    {"pattern": r"从某种意义上说", "desc": "AI 模糊表达"},
    {"pattern": r"显然|毋庸置疑|不言而喻|众所周知|不难看出", "desc": "上帝判断 / 说教词"},
    {"pattern": r"(核心动机|信息边界|信息落差|核心风险|锚定效应|沉没成本|认知共鸣|利益最大化|行为约束|性格过滤|情绪外化)", "desc": "学术分析词漏到正文"},
    {"pattern": r"(全场|众人|所有人|在场的人)([，,]?)?(都|全|齐齐|纷纷)?(震惊|惊呆|倒吸凉气|目瞪口呆|哗然|惊呼)", "desc": "全场震惊式集体反应"},
    {"pattern": r"(全场|一片)([，,]?)?(寂静|哗然|沸腾|震动)", "desc": "全场反应模板"},
]

DEFAULT_RISK = [
    {"pattern": r"(突然|忽然|猛然|猛地)", "max_per_3000": 1, "desc": "突兀转折词"},
    {"pattern": r"(似乎|可能|或许|大概)", "max_density_per_1000": 3, "desc": "套话密度"},
    {"pattern": r"(然而|不过|与此同时|另一方面|尽管如此)", "max_per_3000": 3, "desc": "公式化转折词"},
    {"pattern": r"(此外|另外|因此|所以)", "max_per_3000": 5, "desc": "AI 偏爱副词"},
    {"pattern": r"(最终|最后|结局是|结果是)", "max_per_3000": 2, "desc": "过度总结词"},
    {"pattern": r"(仿佛|宛如|犹如|好像)", "max_per_3000": 3, "desc": "比喻过密"},
    {"pattern": r"(竟然|居然|没想到|原来)", "max_per_3000": 2, "desc": "震惊词"},
    {"pattern": r"(不禁|不由)", "max_per_3000": 1, "desc": "陈词滥调"},
]


def strip_frontmatter_and_outline(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("\n---\n", 1)
        if len(parts) >= 2:
            text = parts[1]
    if "\n---\n" in text:
        text = text.split("\n---\n", 1)[1]
    return text.strip()


def chinese_char_count(text: str) -> int:
    return len(re.findall(r"[一-鿿]", text))


def load_custom_rules(vault: Path) -> tuple[list[dict], list[dict]]:
    """从 vault/style/anti-ai.md 加载用户自定义规则。失败则返回 ([], [])"""
    anti_ai_path = vault / "style" / "anti-ai.md"
    if not anti_ai_path.is_file():
        return [], []

    text = anti_ai_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("\n---\n", 1)
        if len(parts) >= 2:
            text = parts[1]

    forbidden: list[dict] = []
    risk: list[dict] = []
    section: str | None = None
    current: dict | None = None

    for line in text.split("\n"):
        s = line.strip()
        m = re.match(r"^##\s+(forbidden|risk)", s, re.IGNORECASE)
        if m:
            if current and section:
                (forbidden if section == "forbidden" else risk).append(current)
                current = None
            section = m.group(1).lower()
            continue

        if s.startswith("- "):
            if current and section:
                (forbidden if section == "forbidden" else risk).append(current)
            current = {}
            inner = s[2:]
            if ":" in inner:
                k, _, v = inner.partition(":")
                current[k.strip()] = v.strip().strip('"').strip("'")
            continue

        if current is not None and ":" in s:
            k, _, v = s.partition(":")
            current[k.strip()] = v.strip().strip('"').strip("'")

    if current and section:
        (forbidden if section == "forbidden" else risk).append(current)

    return forbidden, risk


def find_location(text: str, match: re.Match) -> str:
    """计算 match 在 text 中的行号 + 列号近似位置。"""
    pos = match.start()
    line = text[:pos].count("\n") + 1
    col = pos - text.rfind("\n", 0, pos)
    return f"L {line}:{col}"


def check_forbidden(text: str, rules: list[dict]) -> list[dict]:
    issues: list[dict] = []
    for r in rules:
        pattern = r.get("pattern") if isinstance(r, dict) else None
        if not pattern:
            continue
        desc = r.get("description") or r.get("desc", "?")
        for match in re.finditer(pattern, text):
            issues.append(
                {
                    "severity": "critical",
                    "dimension": "post-write.forbidden",
                    "location": find_location(text, match),
                    "description": f'出现禁用模式 "{match.group()}"（{desc}）',
                    "suggestion": "改用动作 / 场景 / 直接陈述代替",
                }
            )
    return issues


def check_risk(text: str, rules: list[dict]) -> list[dict]:
    issues: list[dict] = []
    total_chinese = chinese_char_count(text)

    for r in rules:
        pattern = r.get("pattern") if isinstance(r, dict) else None
        if not pattern:
            continue
        desc = r.get("description") or r.get("desc", "?")

        max_per_3000 = r.get("max_per_3000") or r.get("max-per-3000")
        max_density = r.get("max_density_per_1000") or r.get("max-density-per-1000")

        try:
            max_per_3000 = int(max_per_3000) if max_per_3000 else None
        except (ValueError, TypeError):
            max_per_3000 = None
        try:
            max_density = float(max_density) if max_density else None
        except (ValueError, TypeError):
            max_density = None

        matches = list(re.finditer(pattern, text))
        count = len(matches)
        if count == 0:
            continue

        # 上限 per 3000 字
        if max_per_3000 is not None:
            actual_limit = max(1, total_chinese // 3000) * max_per_3000
            if count > actual_limit:
                issues.append(
                    {
                        "severity": "warning",
                        "dimension": "post-write.risk-frequency",
                        "location": "全章",
                        "description": f'"{pattern}" 出现 {count} 次（上限 {actual_limit} 次/{total_chinese} 字，{desc}）',
                        "suggestion": "用具体动作或感官描写替代",
                    }
                )

        # 上限 density per 1000
        if max_density is not None and total_chinese > 0:
            density = count / (total_chinese / 1000)
            if density > max_density:
                issues.append(
                    {
                        "severity": "warning",
                        "dimension": "post-write.risk-density",
                        "location": "全章",
                        "description": f'"{pattern}" 密度 {density:.1f} 次/千字（上限 {max_density}，{desc}）',
                        "suggestion": "降低密度，用确定性叙述替代",
                    }
                )

    return issues


def run(chapter_path: Path, vault: Path) -> dict:
    text = chapter_path.read_text(encoding="utf-8")
    body = strip_frontmatter_and_outline(text)

    custom_forbidden, custom_risk = load_custom_rules(vault)
    forbidden_rules = custom_forbidden if custom_forbidden else DEFAULT_FORBIDDEN
    risk_rules = custom_risk if custom_risk else DEFAULT_RISK

    issues = check_forbidden(body, forbidden_rules) + check_risk(body, risk_rules)

    return {
        "checker": "check_post_write",
        "chapter": chapter_path.name,
        "passed": all(i["severity"] != "critical" for i in issues),
        "issues": issues,
        "rules_source": "custom (style/anti-ai.md)" if custom_forbidden else "default",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="check_post_write - 硬规则违规检测")
    parser.add_argument("--chapter", type=Path, required=True)
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.chapter.is_file():
        print(f"❌ 章节文件不存在：{args.chapter}", file=sys.stderr)
        return 1

    result = run(args.chapter, args.vault.resolve())

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"🔍 check_post_write - {args.chapter.name}（规则源：{result['rules_source']}）")
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
