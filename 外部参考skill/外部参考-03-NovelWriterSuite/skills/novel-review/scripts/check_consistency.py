#!/usr/bin/env python3
"""
novel-review/check_consistency.py —— 跨实体一致性检查。

检查项：
1. 章节 frontmatter 中的 appeared / locations-used / systems-invoked 引用的实体是否在 vault 中存在
2. continuity-facts.md 中标注的"永久事实"是否在本章被违反（简单关键词匹配）
3. 章节 frontmatter 中的 pov / location 必须存在

主观一致性检查（OOC / 战力崩坏 / 时间线）留给 LLM 评估，不在本脚本中。

用法：
    python3 check_consistency.py --chapter chapters/ch-008.md --vault {vault}
"""

import argparse
import json
import re
import sys
from pathlib import Path


def strip_frontmatter(text: str) -> tuple[str, dict]:
    """返回 (正文, frontmatter dict)"""
    fm: dict = {}
    if not text.startswith("---"):
        return text, fm
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return text, fm

    fm_text = m.group(1)
    body = text[m.end():]

    # 简易 YAML 解析（key: value 行，list 解析为字符串数组）
    current_key: str | None = None
    for line in fm_text.split("\n"):
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith(" ") or line.startswith("\t"):
            # 列表项 - item
            m_list = re.match(r"^\s*-\s+(.+)$", line)
            if m_list and current_key:
                val = m_list.group(1).strip().strip('"').strip("'")
                fm.setdefault(current_key, [])
                if isinstance(fm[current_key], list):
                    fm[current_key].append(val)
            continue

        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if not value:
                # 后面是列表
                fm[key] = []
                current_key = key
            else:
                fm[key] = value
                current_key = key

    return body, fm


def list_existing_entities(vault: Path) -> dict:
    """扫描 vault 下的实体文件，返回 {characters: set, locations: set, systems: set}"""
    chars = {p.stem for p in (vault / "characters").glob("*.md") if p.name != "_index.md"}
    locs = {p.stem for p in (vault / "worldbuilding" / "locations").glob("*.md")}
    systems = {p.stem for p in (vault / "worldbuilding" / "systems").glob("*.md")}
    return {"characters": chars, "locations": locs, "systems": systems}


def parse_continuity_facts(vault: Path) -> list[str]:
    """从 .memory/continuity-facts.md 提取"永久事实"作为禁违反清单。

    格式预期：每条事实写在列表项里，特别是 ## sera-voss 身体特征 等段。
    v0.1 简化：把整个文件按行扫描，挑 - 开头的当作事实。
    """
    facts_path = vault / ".memory" / "continuity-facts.md"
    if not facts_path.is_file():
        return []

    facts: list[str] = []
    text = facts_path.read_text(encoding="utf-8")
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("- "):
            facts.append(s[2:].strip())
    return facts


def check_pov_exists(fm: dict, entities: dict) -> list[dict]:
    pov = fm.get("pov", "").strip()
    if not pov:
        return [
            {
                "severity": "warning",
                "dimension": "consistency.frontmatter",
                "location": "frontmatter",
                "description": "章节 frontmatter 缺少 pov 字段",
                "suggestion": "在 frontmatter 添加 pov: {character-kebab}",
            }
        ]
    if pov not in entities["characters"]:
        return [
            {
                "severity": "critical",
                "dimension": "consistency.pov-missing",
                "location": "frontmatter.pov",
                "description": f"pov 角色 {pov} 在 characters/ 中不存在",
                "suggestion": f"用 novel-characters 创建 {pov}.md，或修正 pov 字段",
            }
        ]
    return []


def check_location_exists(fm: dict, entities: dict) -> list[dict]:
    loc = fm.get("location", "").strip()
    if not loc:
        return []
    if loc not in entities["locations"]:
        return [
            {
                "severity": "warning",
                "dimension": "consistency.location-missing",
                "location": "frontmatter.location",
                "description": f"location {loc} 在 worldbuilding/locations/ 中不存在",
                "suggestion": f"用 novel-worldbuilding 创建 {loc}.md，或修正 location 字段",
            }
        ]
    return []


def check_appeared_exist(fm: dict, entities: dict) -> list[dict]:
    appeared = fm.get("appeared", []) or []
    if isinstance(appeared, str):
        appeared = [appeared]
    issues: list[dict] = []
    for char in appeared:
        if char not in entities["characters"]:
            issues.append(
                {
                    "severity": "warning",
                    "dimension": "consistency.appeared-missing",
                    "location": "frontmatter.appeared",
                    "description": f"出场角色 {char} 在 characters/ 中不存在（cameo 角色可忽略）",
                    "suggestion": f"如果是重要角色，用 novel-characters 创建；如果是 cameo，可忽略",
                }
            )
    return issues


def check_systems_known(fm: dict, entities: dict) -> list[dict]:
    systems = fm.get("systems-invoked", []) or []
    if isinstance(systems, str):
        systems = [systems]
    issues: list[dict] = []
    for sys_name in systems:
        if sys_name not in entities["systems"]:
            issues.append(
                {
                    "severity": "warning",
                    "dimension": "consistency.system-missing",
                    "location": "frontmatter.systems-invoked",
                    "description": f"涉及体系 {sys_name} 在 worldbuilding/systems/ 中不存在",
                    "suggestion": f"用 novel-worldbuilding 创建 {sys_name}.md，或修正 systems-invoked 字段",
                }
            )
    return issues


def check_continuity_facts(body: str, facts: list[str]) -> list[dict]:
    """检查永久事实是否被简单关键词违反。

    v0.1 实现非常简单：fact 描述如 "sera 左手有伤"，
    在 body 中搜"sera 的左手" + "光滑 / 无痕 / 完好"等冲突词，命中即报。
    这是个粗糙的启发式，主要靠 LLM 层处理。
    """
    # v0.1 暂留为占位符，返回空列表。
    # 真正的违反检测交给 LLM 评估。
    return []


def run(chapter_path: Path, vault: Path) -> dict:
    text = chapter_path.read_text(encoding="utf-8")
    body, fm = strip_frontmatter(text)
    entities = list_existing_entities(vault)
    facts = parse_continuity_facts(vault)

    issues: list[dict] = []
    issues.extend(check_pov_exists(fm, entities))
    issues.extend(check_location_exists(fm, entities))
    issues.extend(check_appeared_exist(fm, entities))
    issues.extend(check_systems_known(fm, entities))
    issues.extend(check_continuity_facts(body, facts))

    return {
        "checker": "check_consistency",
        "chapter": chapter_path.name,
        "passed": all(i["severity"] != "critical" for i in issues),
        "issues": issues,
        "entity_counts": {
            "characters": len(entities["characters"]),
            "locations": len(entities["locations"]),
            "systems": len(entities["systems"]),
            "continuity_facts": len(facts),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="check_consistency - 跨实体一致性")
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
        print(f"🔍 check_consistency - {args.chapter.name}")
        print(f"   passed: {result['passed']}")
        c = result["entity_counts"]
        print(f"   vault: {c['characters']} chars / {c['locations']} locations / "
              f"{c['systems']} systems / {c['continuity_facts']} facts")
        print(f"   issues: {len(result['issues'])}")
        for issue in result["issues"]:
            sev = issue["severity"].upper()
            print(f"\n   [{sev}] {issue['dimension']} @ {issue['location']}")
            print(f"     {issue['description']}")
            print(f"     建议：{issue['suggestion']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
