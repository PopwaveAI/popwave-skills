"""闸门注入：结构参考 + 声音参考 双区块格式化。"""

from __future__ import annotations

from .retriever import Candidate

MAX_TOTAL_WORDS = 8000  # 单次注入总字数上限


def truncate_by_quality(
    candidates: list[Candidate], max_words: int = MAX_TOTAL_WORDS
) -> list[Candidate]:
    """按 quality_score 降序保留，直到总字数 <= max_words。"""
    sorted_cs = sorted(candidates, key=lambda x: -x.quality_score)
    kept: list[Candidate] = []
    total = 0
    for c in sorted_cs:
        if total + c.word_count > max_words and kept:
            break
        kept.append(c)
        total += c.word_count
    # 按原始顺序（match_score + quality_score）返回
    kept_ids = {c.id for c in kept}
    return [c for c in candidates if c.id in kept_ids]


def format_injection(
    candidates: list[Candidate],
    narrative: str,
) -> str:
    """
    格式化为闸门 markdown 区块。

    输出结构：
        ## 🔴声音锁（标签匹配·片段级）
        > 本次匹配：...
        ### 结构参考（这场戏怎么推进）
        #### ...
        ### 声音参考（句子怎么写）
        #### ...
    """
    if not candidates:
        return _format_no_match(narrative)

    candidates = truncate_by_quality(candidates)

    # 第一条作为结构参考，其余作为声音参考
    structure_ref = candidates[0]
    voice_refs = candidates[1:]

    total_words = sum(c.word_count for c in candidates)
    books = {c.source_book for c in candidates}

    lines = [
        "## 🔴声音锁（标签匹配·片段级）",
        "",
        f"> 本次匹配：叙事功能「{narrative}」· "
        f"候选 {len(candidates)} 条 · "
        f"总字数 {total_words} · "
        f"来源 {len(books)} 本书",
        "",
        "### 结构参考（这场戏怎么推进）",
        "",
        _format_fragment_block(structure_ref),
    ]

    if voice_refs:
        lines.extend([
            "",
            "### 声音参考（句子怎么写）",
            "",
        ])
        for c in voice_refs:
            lines.append(_format_fragment_block(c))
            lines.append("")

    # 无匹配的书提示
    from_books_set = {c.source_book for c in candidates}
    # 注意：这里无法知道全部应有的书，由调用方传入；这里只记录已匹配的
    return "\n".join(lines)


def _format_fragment_block(c: Candidate) -> str:
    """单个片段的 markdown 块。"""
    match_label = {
        "Level1": "【标签精准匹配】",
        "Level2": "【近似标签匹配】",
        "Level3": "【FTS降级】",
    }.get(c.match_level, "")

    tags_display = c.matched_tags if c.matched_tags else "（FTS 无标签）"
    header = (
        f"#### {tags_display} —— {c.source_book} "
        f"ch{c.chapter_number}-{c.fragment_number}"
        f"（{c.word_count}字·score={c.quality_score}）{match_label}"
    )
    note = f"\n> ⚠️ {c.note}" if c.note else ""

    return (
        f"{header}\n"
        f"```\n{c.content}\n```"
        f"{note}"
    )


def _format_no_match(narrative: str) -> str:
    return (
        "## 🔴声音锁（标签匹配·片段级）\n"
        "\n"
        f"> ⚠️ 本次叙事功能「{narrative}」无自动匹配片段，请人工选择。\n"
    )
