#!/usr/bin/env python3
"""
novel-review/check_hook_ledger.py —— 伏笔账核对（hook ledger validator）。

借鉴 inkos packages/core/src/utils/hook-ledger-validator.ts 算法，独立重写为 Python。

核心检查：
1. 章节的 ## hook-账 段中，advance / resolve 列表的每一条，必须在正文中有关键词回声
2. 揭 1 埋 1 硬底线：本章 resolve 多少个 hook，必须至少 open 同样多个新 hook
3. defer 必须给出原因

用法：
    python3 check_hook_ledger.py --chapter chapters/ch-008.md --vault {vault}
"""

import argparse
import json
import re
import sys
from pathlib import Path

ASCII_STOPWORDS = {
    "and", "the", "for", "with", "from", "that", "into", "then",
    "open", "close", "advance", "resolve", "defer", "new",
}

PLACEHOLDER_TOKENS = re.compile(r"^(无|空|none|nil|null|暂无|n/a|na|tbd|todo|待定)$", re.IGNORECASE)


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("\n---\n", 1)
        if len(parts) >= 2:
            return parts[1]
    return text


def find_hook_ledger_section(text: str) -> str | None:
    """提取 ## hook-账 或 ## hook 账（实际）段的内容。

    我们优先匹配"实际"（write 完成后的真实操作），其次匹配"预定"。
    """
    patterns = [
        r"##\s+hook[-\s]*账[（(]实际[)）]\s*\n(.*?)(?=\n##\s|\Z)",
        r"##\s+hook[-\s]*账\s*\n(.*?)(?=\n##\s|\Z)",
    ]
    for pat in patterns:
        m = re.search(pat, text, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def parse_ledger(section: str) -> dict:
    """解析 ledger 内容。返回 {open, advance, resolve, defer, new_open_count}"""
    result: dict = {"open": [], "advance": [], "resolve": [], "defer": [], "new_open_count": 0}
    current: str | None = None

    for raw in section.split("\n"):
        line = raw.strip()
        if not line:
            continue

        # 三级标题：### open / ### advance / ### resolve / ### defer
        m = re.match(r"^###\s*(open|advance|resolve|defer)\s*$", line, re.IGNORECASE)
        if m:
            current = m.group(1).lower()
            continue

        # 行内子段：- open: / - advance: 等
        m_inline = re.match(r"^-?\s*(open|advance|resolve|defer)\s*[:：]\s*$", line, re.IGNORECASE)
        if m_inline:
            current = m_inline.group(1).lower()
            continue

        if not current:
            continue
        if not line.startswith("-"):
            continue

        cleaned = re.sub(r"^-+\s*", "", line)

        # `[new]` 占位符：新伏笔无 ID，但计入 new_open_count
        if current == "open" and re.match(r"^\[new\]", cleaned, re.IGNORECASE):
            result["new_open_count"] += 1
            # 提取后面的描述作为 keywords
            description = re.sub(r"^\[new\]\s*", "", cleaned, flags=re.IGNORECASE)
            keywords = extract_keywords(description)
            result[current].append({"id": "[new]", "description": description, "keywords": keywords})
            continue

        # 占位符 - 无 / - none 等
        first_word = cleaned.split()[0] if cleaned else ""
        if PLACEHOLDER_TOKENS.match(first_word):
            continue

        # 标准格式：H001 "描述" → ... 或 H001 描述
        id_match = re.match(r"^([A-Za-z一-鿿][\w\-一-鿿]{0,19})", cleaned)
        if not id_match:
            continue

        hook_id = id_match.group(1)
        if PLACEHOLDER_TOKENS.match(hook_id):
            continue

        descriptor = cleaned[len(hook_id):].strip()
        keywords = extract_keywords(descriptor)
        result[current].append({"id": hook_id, "description": descriptor, "keywords": keywords})

    return result


def extract_keywords(descriptor: str) -> list[str]:
    """从 descriptor 中抽 CJK 2-gram + 整词 ASCII，作为正文中要找的关键词。

    优先：如果 descriptor 里有引号包裹的 hook 名（如 "胖虎借条"），用引号内容
    其次：箭头 → 前的部分（→ 后通常是状态变化，可能误匹配）
    """
    if not descriptor:
        return []

    # 引号内
    quote_match = re.search(r'["“「『]([^"”」』\n]+)', descriptor)
    if quote_match:
        source = quote_match.group(1)
    else:
        # → 之前
        source = re.split(r"→|->", descriptor, 1)[0]

    # CJK 2-gram
    cjk_runs = re.findall(r"[一-鿿]{2,}", source)
    cjk_tokens: list[str] = []
    for run in cjk_runs:
        cjk_tokens.append(run)
        if len(run) >= 3:
            for i in range(len(run) - 1):
                cjk_tokens.append(run[i : i + 2])
        if len(run) >= 4:
            cjk_tokens.append(run[:3])
            cjk_tokens.append(run[-3:])

    # ASCII 整词
    ascii_words = [w.lower() for w in re.findall(r"[A-Za-z]{3,}", source) if w.lower() not in ASCII_STOPWORDS]

    # 去重保序
    seen = set()
    unique: list[str] = []
    for tok in cjk_tokens + ascii_words:
        if tok not in seen:
            seen.add(tok)
            unique.append(tok)
    return unique


def get_chapter_body(text: str) -> str:
    """提取章节正文（去掉 frontmatter / 章纲 / hook-账）。"""
    body = strip_frontmatter(text)

    # 去掉所有 ## section 段，留下纯正文
    # 我们的格式：章纲、hook-账（预定）在前，--- 后是正文，正文后可能有 hook-账（实际）

    # 简化策略：如果有 --- 分隔，取 --- 后第一段作为正文
    if "\n---\n" in body:
        body = body.split("\n---\n", 1)[1]
        # 去掉末尾的 ## hook-账（实际）段
        body = re.sub(r"##\s+hook[-\s]*账[（(]实际[)）].*$", "", body, flags=re.DOTALL | re.IGNORECASE)

    return body.strip()


def check_keyword_echo(body: str, entries: list[dict], severity: str = "critical") -> list[dict]:
    """检查 entries 中每条 hook 是否在 body 中有关键词回声。"""
    issues: list[dict] = []
    body_lower = body.lower()
    for entry in entries:
        hook_id = entry["id"]
        keywords = entry["keywords"]

        if not keywords:
            # bare-id 或无 descriptor：尝试匹配 ID 本身
            if re.match(r"^[A-Za-z0-9_-]+$", hook_id):
                if not re.search(rf"\b{re.escape(hook_id)}\b", body):
                    issues.append(
                        {
                            "severity": severity,
                            "dimension": "hook-ledger.no-evidence",
                            "location": "正文",
                            "description": f"hook {hook_id} 在 ledger 中声明但正文无任何相关引用",
                            "suggestion": f"在正文中加入对 {hook_id} 的具体推进，或把它移到 defer 并给原因",
                        }
                    )
            continue

        # 任一 keyword 在 body 中出现即通过
        found = False
        for kw in keywords:
            if re.match(r"^[a-z]", kw):
                if kw in body_lower:
                    found = True
                    break
            else:
                if kw in body:
                    found = True
                    break

        if not found:
            issues.append(
                {
                    "severity": severity,
                    "dimension": "hook-ledger.no-evidence",
                    "location": "正文",
                    "description": f'hook {hook_id} 在 ledger 中声明 {entry["description"][:30]}... 但正文中找不到关键词（{", ".join(keywords[:3])}）',
                    "suggestion": f"在正文中具体推进 {hook_id}（动作 / 对话 / 环境变化），或移到 defer 并给原因",
                }
            )

    return issues


def check_open_close_balance(ledger: dict) -> list[dict]:
    """揭 1 埋 1 硬底线：resolve N 个，必须 open ≥ N 个"""
    resolved = len(ledger["resolve"])
    opened = len(ledger["open"]) + ledger["new_open_count"]

    if resolved > 0 and opened < resolved:
        return [
            {
                "severity": "critical",
                "dimension": "hook-ledger.open-close-imbalance",
                "location": "ledger",
                "description": f"本章 resolve 了 {resolved} 个 hook，但 open 只有 {opened} 个新 hook。只揭不埋会让故事失去前进拉力（番茄文章 10 - 揭 1 埋 1）",
                "suggestion": f"在 ledger 的 open 段下至少再埋 {resolved - opened} 个新 hook（与已揭 hook 相关或铺垫新支线）",
            }
        ]
    return []


def run(chapter_path: Path, vault: Path) -> dict:
    text = chapter_path.read_text(encoding="utf-8")

    section = find_hook_ledger_section(text)
    if not section:
        return {
            "checker": "check_hook_ledger",
            "chapter": chapter_path.name,
            "passed": True,
            "issues": [
                {
                    "severity": "warning",
                    "dimension": "hook-ledger.missing",
                    "location": "章节文件",
                    "description": "章节中找不到 ## hook-账 段",
                    "suggestion": "在章节末尾加 ## hook-账（实际）段，记录本章的 open / advance / resolve / defer",
                }
            ],
        }

    ledger = parse_ledger(section)
    body = get_chapter_body(text)

    issues: list[dict] = []
    # advance 和 resolve 必须有关键词回声
    issues.extend(check_keyword_echo(body, ledger["advance"], severity="critical"))
    issues.extend(check_keyword_echo(body, ledger["resolve"], severity="critical"))
    # 揭 1 埋 1
    issues.extend(check_open_close_balance(ledger))

    return {
        "checker": "check_hook_ledger",
        "chapter": chapter_path.name,
        "passed": all(i["severity"] != "critical" for i in issues),
        "issues": issues,
        "ledger_summary": {
            "open": len(ledger["open"]),
            "new_open": ledger["new_open_count"],
            "advance": len(ledger["advance"]),
            "resolve": len(ledger["resolve"]),
            "defer": len(ledger["defer"]),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="check_hook_ledger - 伏笔账核对")
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
        print(f"🔍 check_hook_ledger - {args.chapter.name}")
        print(f"   passed: {result['passed']}")
        s = result.get("ledger_summary", {})
        print(f"   ledger: open={s.get('open', 0)} new_open={s.get('new_open', 0)} "
              f"advance={s.get('advance', 0)} resolve={s.get('resolve', 0)} defer={s.get('defer', 0)}")
        print(f"   issues: {len(result['issues'])}")
        for issue in result["issues"]:
            sev = issue["severity"].upper()
            print(f"\n   [{sev}] {issue['dimension']}")
            print(f"     {issue['description']}")
            print(f"     建议：{issue['suggestion']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
