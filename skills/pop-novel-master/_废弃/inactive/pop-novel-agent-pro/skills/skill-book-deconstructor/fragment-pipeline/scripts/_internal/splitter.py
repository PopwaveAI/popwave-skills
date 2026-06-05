"""Step 2: LLM 语义切割 + 首尾句定位 + 覆盖率校验。

核心修复（v3.3）：
1. search_start 游标：避免短句歧义命中
2. 模糊降级：精确匹配失败时取前/后 N 字模糊匹配
3. 覆盖率校验：切完后校验总覆盖率与夹缝/重叠
4. 滑动窗口：仅在超长章节（>50000 字）触发，带 800 字 overlap

v3.7.1 修复：
- _locate_fragments 采用四级降级（同 combined.py），解决 LLM 省略 \\n\\u3000 导致匹配失败
"""

from __future__ import annotations

import bisect
import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .llm_client import LLMClient

# ── 异步入口（供 build_fragments 异步主循环调用）────────────────────────────

async def split_chapter_async(
    chapter_text: str,
    llm: LLMClient,
) -> list[Fragment]:
    """异步版本的章节切割，内部调用 llm.chat_json_async()。"""
    if len(chapter_text) > SLIDING_WINDOW_THRESHOLD:
        return await _split_with_sliding_window_async(chapter_text, llm)
    return await _split_single_async(chapter_text, llm)


async def _split_single_async(chapter_text: str, llm: LLMClient) -> list[Fragment]:
    prompt = PROMPT_TEMPLATE.format(chapter_text=chapter_text)
    result = await llm.chat_json_async(prompt, max_tokens=4000)
    if not result or "fragments" not in result:
        logger.error("LLM 未返回 fragments 字段（async）")
        return []
    raw_fragments = result["fragments"]
    if not isinstance(raw_fragments, list) or not raw_fragments:
        return []
    fragments = _locate_fragments(chapter_text, raw_fragments)
    if not fragments:
        return []
    ok, msg = _validate_coverage(chapter_text, fragments)
    if not ok:
        logger.error("覆盖率校验失败（async）: %s", msg)
        return []
    return fragments


async def _split_with_sliding_window_async(
    chapter_text: str, llm: LLMClient
) -> list[Fragment]:
    import asyncio as _asyncio
    logger.info("章节字数 %d 超过阈值，启用滑动窗口（async）", len(chapter_text))
    windows: list[tuple[int, int]] = []
    pos = 0
    while pos < len(chapter_text):
        end = min(pos + SLIDING_WINDOW_SIZE, len(chapter_text))
        windows.append((pos, end))
        if end == len(chapter_text):
            break
        pos = end - SLIDING_WINDOW_OVERLAP

    async def _process_window(w_start: int, w_end: int) -> list[Fragment]:
        sub_text = chapter_text[w_start:w_end]
        sub_frags = await _split_single_async(sub_text, llm)
        for f in sub_frags:
            f.start += w_start
            f.end += w_start
        return sub_frags

    results = await _asyncio.gather(*[_process_window(s, e) for s, e in windows])
    all_fragments: list[Fragment] = [f for frags in results for f in frags]

    seen: dict[str, Fragment] = {}
    for f in all_fragments:
        key = f.content[:50]
        if key in seen:
            if (f.end - f.start) > (seen[key].end - seen[key].start):
                seen[key] = f
        else:
            seen[key] = f
    return sorted(seen.values(), key=lambda x: x.start)

logger = logging.getLogger(__name__)

# 触发滑动窗口的章节字数阈值（Kimi-K2 200K context，绝大部分章节单次能处理）
SLIDING_WINDOW_THRESHOLD = 50000
SLIDING_WINDOW_SIZE = 40000
SLIDING_WINDOW_OVERLAP = 800

# 首尾句最少字符数（防止短句歧义命中）
MIN_ANCHOR_LEN = 30
FUZZY_ANCHOR_LEN = 20

PROMPT_TEMPLATE = """你是一位网文编辑，擅长按叙事功能切割小说章节。

任务：将以下章节按叙事功能切成若干片段。

切割原则：
1. 每个片段必须是一个完整的叙事单元（一场战斗、一段对话、一次探索、一段内心独白）
2. 片段长度 500-1500 字（战斗场景可放宽到 2000 字）
3. 切割点必须在叙事功能切换处：
   - 战斗 → 对话 / 对话 → 环境描写 / 环境 → 战斗
   - 时间跳跃（"三天后"）/ 地点切换（"与此同时，另一边"）
4. 禁止在句子中间切断
5. 如果一个叙事单元超过 2000 字，按"回合"或"阶段"拆分

⚠️ 锚点严格要求（最常见错误，务必遵守）：
- first_line：该片段第一句话原文，**必须 ≥ 40 字符**
- last_line：该片段最后一句话原文，**必须 ≥ 40 字符**
- 如果句子不足 40 字，必须连同紧邻的下一句一起作为锚点，直到凑足 40 字
- 从章节原文直接复制，一字不改

输出格式示例：
{{
  "fragments": [
    {{
      "first_line": "他踏入战场的瞬间，脚下的地面在他的力量下颤抖了，空气中弥漫着浓郁的血腥味。",
      "last_line": "敌人的尸体已铺满四周，鲜血渗入泥土，但更多的还在涌来，黑压压的一片望不到头。",
      "reason": "Boss战：主角 vs 巨型怪物，从接敌到劣势"
    }}
  ]
}}

章节内容：
{chapter_text}
"""


@dataclass
class Fragment:
    start: int
    end: int
    content: str
    reason: str = ""
    estimated_type: str = ""


def split_chapter(
    chapter_text: str,
    llm: LLMClient,
) -> list[Fragment]:
    """
    切割单章。返回 Fragment 列表。
    超长章节自动走滑动窗口。
    定位失败/校验失败返回空列表（调用方决定是否降级）。
    """
    if len(chapter_text) > SLIDING_WINDOW_THRESHOLD:
        return _split_with_sliding_window(chapter_text, llm)
    return _split_single(chapter_text, llm)


def _split_single(chapter_text: str, llm: LLMClient) -> list[Fragment]:
    """单次 LLM 调用切割。"""
    prompt = PROMPT_TEMPLATE.format(chapter_text=chapter_text)
    result = llm.chat_json(prompt, max_tokens=4000)
    if not result or "fragments" not in result:
        logger.error("LLM 未返回 fragments 字段")
        return []

    raw_fragments = result["fragments"]
    if not isinstance(raw_fragments, list) or not raw_fragments:
        logger.error("LLM fragments 为空或类型错误")
        return []

    fragments = _locate_fragments(chapter_text, raw_fragments)
    if not fragments:
        return []

    ok, msg = _validate_coverage(chapter_text, fragments)
    if not ok:
        logger.error("覆盖率校验失败: %s", msg)
        return []

    return fragments


def _norm_mapping(text: str) -> tuple[str, list[int]]:
    norm_chars: list[str] = []
    pos_map: list[int] = []
    for i, ch in enumerate(text):
        if ch == "\n" or ch == "\u3000":
            continue
        norm_chars.append(ch)
        pos_map.append(i)
    return "".join(norm_chars), pos_map


def _norm_str(s: str) -> str:
    return s.replace("\n", "").replace("\u3000", "")


def _locate_fragments(chapter_text: str, raw_fragments: list[dict]) -> list[Fragment]:
    """用 first_line / last_line 定位片段。四级降级：精确→模糊→归一化→归一化+模糊。"""
    norm_text, pos_map = _norm_mapping(chapter_text)
    fragments: list[Fragment] = []
    search_start = 0

    for i, frag in enumerate(raw_fragments):
        first = frag.get("first_line", "").strip()
        last = frag.get("last_line", "").strip()

        if not first or not last:
            logger.warning("片段 %d 缺少 first_line/last_line，跳过", i)
            continue

        if len(first) < MIN_ANCHOR_LEN or len(last) < MIN_ANCHOR_LEN:
            logger.warning("片段 %d 锚点过短（first=%d, last=%d）", i, len(first), len(last))

        # ── 首句定位（四级降级）──
        start = chapter_text.find(first, search_start)
        if start == -1:
            start = chapter_text.find(first[:FUZZY_ANCHOR_LEN], search_start)
        if start == -1:
            norm_from = bisect.bisect_left(pos_map, search_start)
            norm_first = _norm_str(first)
            np = norm_text.find(norm_first, norm_from)
            if np != -1:
                start = pos_map[np]
        if start == -1:
            norm_from = bisect.bisect_left(pos_map, search_start)
            np = norm_text.find(_norm_str(first)[:FUZZY_ANCHOR_LEN], norm_from)
            if np != -1:
                start = pos_map[np]
        if start == -1:
            logger.error("片段 %d 首句四级匹配均失败: %.40s", i, first)
            continue

        # ── 尾句定位（四级降级）──
        last_from = start + max(len(first), 10)
        end = -1
        ep = chapter_text.find(last, last_from)
        if ep != -1:
            end = ep + len(last)
        if end == -1:
            ep = chapter_text.find(last[-FUZZY_ANCHOR_LEN:], last_from)
            if ep != -1:
                end = ep + len(last[-FUZZY_ANCHOR_LEN:])
        if end == -1:
            norm_from = bisect.bisect_left(pos_map, last_from)
            norm_last = _norm_str(last)
            np = norm_text.find(norm_last, norm_from)
            if np != -1:
                en = np + len(norm_last)
                end = pos_map[en - 1] + 1 if en - 1 < len(pos_map) else len(chapter_text)
        if end == -1:
            norm_from = bisect.bisect_left(pos_map, last_from)
            np = norm_text.find(_norm_str(last)[-FUZZY_ANCHOR_LEN:], norm_from)
            if np != -1:
                en = np + len(_norm_str(last)[-FUZZY_ANCHOR_LEN:])
                end = pos_map[en - 1] + 1 if en - 1 < len(pos_map) else len(chapter_text)
        if end == -1:
            logger.error("片段 %d 尾句四级匹配均失败: %.40s", i, last[-40:])
            continue

        fragments.append(Fragment(
            start=start,
            end=end,
            content=chapter_text[start:end],
            reason=frag.get("reason", ""),
            estimated_type=frag.get("estimated_type", ""),
        ))
        search_start = end

    return fragments


def _validate_coverage(
    chapter_text: str, fragments: list[Fragment]
) -> tuple[bool, str]:
    """
    校验覆盖率与夹缝/重叠。
    会就地修改 fragments（小夹缝并入前一片段）。
    """
    if not fragments:
        return False, "无片段"

    # 1. 总覆盖率（容忍 ±15%）
    total_covered = sum(len(f.content) for f in fragments)
    coverage = total_covered / len(chapter_text)
    if coverage < 0.80:
        logger.warning("覆盖率过低: %.2f（可能漏掉大段内容）", coverage)
    if coverage > 1.15:
        return False, f"覆盖率超 1: {coverage:.2f}（存在重叠）"

    # 2. 相邻夹缝/重叠检查
    for i in range(len(fragments) - 1):
        gap = fragments[i + 1].start - fragments[i].end
        if 0 < gap <= 50:
            # 小夹缝并入前一片段
            new_end = fragments[i + 1].start
            fragments[i].end = new_end
            fragments[i].content = chapter_text[fragments[i].start: new_end]
        elif gap > 50:
            logger.warning(
                "片段 %d 与 %d 间隔 %d 字，可能漏掉过渡内容",
                i, i + 1, gap,
            )
        elif gap < -20:
            return False, f"片段 {i} 与 {i + 1} 重叠 {-gap} 字"

    return True, "ok"


def _split_with_sliding_window(
    chapter_text: str, llm: LLMClient
) -> list[Fragment]:
    """超长章节滑动窗口切割（带 overlap，合并去重）。"""
    logger.info("章节字数 %d 超过阈值 %d，启用滑动窗口", len(chapter_text), SLIDING_WINDOW_THRESHOLD)
    windows: list[tuple[int, int]] = []
    pos = 0
    while pos < len(chapter_text):
        end = min(pos + SLIDING_WINDOW_SIZE, len(chapter_text))
        windows.append((pos, end))
        if end == len(chapter_text):
            break
        pos = end - SLIDING_WINDOW_OVERLAP

    all_fragments: list[Fragment] = []
    for w_start, w_end in windows:
        sub_text = chapter_text[w_start:w_end]
        sub_frags = _split_single(sub_text, llm)
        # 偏移修正
        for f in sub_frags:
            f.start += w_start
            f.end += w_start
        all_fragments.extend(sub_frags)

    # 合并：去除 overlap 区域内的重复片段（首句完全相同视为重复，保留更长的）
    seen: dict[str, Fragment] = {}
    for f in all_fragments:
        key = f.content[:50]
        if key in seen:
            if (f.end - f.start) > (seen[key].end - seen[key].start):
                seen[key] = f
        else:
            seen[key] = f

    merged = sorted(seen.values(), key=lambda x: x.start)
    return merged
