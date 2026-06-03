"""切割 + 打标合并：单次 LLM 调用同时完成边界定位和语义标注（v3.7）。

优化效果：
- 旧：每章 1 次切割调用 + N/4 次打标调用（4-5 次/章）
- 新：每章 1 次合并调用（节省 ~75-80% API 调用次数）

v3.7.1 修复：
- 锚点四级降级匹配：精确 → 模糊前N字 → 归一化（去 \\n\\u3000） → 归一化+模糊
  解决 LLM 将段落分隔符 \\n\\u3000\\u3000 省略后锚点无法匹配的问题
"""

from __future__ import annotations

import bisect
import logging
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .tagger import VALID_SCENE_TYPES, TagResult

if TYPE_CHECKING:
    from .llm_client import LLMClient

logger = logging.getLogger(__name__)

# 滑动窗口参数（复用 splitter 的阈值）
SLIDING_WINDOW_THRESHOLD = 50000
SLIDING_WINDOW_SIZE = 40000
SLIDING_WINDOW_OVERLAP = 800

# 锚点最短长度
MIN_ANCHOR_LEN = 30
FUZZY_ANCHOR_LEN = 20

# ── 合并 Prompt ───────────────────────────────────────────────────────────────

COMBINED_PROMPT_TEMPLATE = """你是一位网文编辑。一次完成两个任务：①按叙事功能切割章节 ②为每个片段打标签。

切割原则：
1. 每个片段是一个完整叙事单元（一场战斗、一段对话、一次探索、一段独白）
2. 片段长度 500-1500 字（战斗场景可放宽到 2000 字）
3. 切割点在叙事功能切换处：战斗↔对话、时间跳跃、地点切换
4. 禁止在句子中间切断

⚠️ 锚点严格要求（最常见错误，务必遵守）：
- first_line：片段第一句话的原文，必须 ≥ 40 字符
- last_line：片段最后一句话的原文，必须 ≥ 40 字符
- 如不足 40 字，必须连同紧邻的下一句一起作为锚点，直到凑足 40 字
- 从章节原文直接复制，一字不改

scene_type（每片段必选 1 个）：
- 战斗：打架/碾压/Boss战/行刑/撤退追击
- 成长：修炼/练级/突破/面板/顿悟/淬炼
- 获取：战利品/功法/装备/金钱/招募/奖励
- 立威：示威/挑衅反击/宣示立场/震慑
- 探索：行军/侦察/追踪/发现线索/新地点
- 仪式：身体改造/血脉觉醒/职业转化/融合
- 对话：谈判/对质/信息交换/招募说服
- 情感：日常/羁绊/情绪/休整/牺牲
- 建设：种田/势力扩张/积累/培养下属
- 其他：不属于以上

输出格式（严格 JSON 对象，不输出其他内容）：
{{
  "fragments": [
    {{
      "first_line": "至少40字的首句原文，从章节直接复制不改动",
      "last_line": "至少40字的尾句原文，从章节直接复制不改动",
      "scene_type": "战斗",
      "narrative_desc": "1-2句描述这段的具体内容（不是解释分类）",
      "tags": ["关键词1", "关键词2", "关键词3"]
    }}
  ]
}}

章节内容：
{chapter_text}
"""


# ── 数据类 ────────────────────────────────────────────────────────────────────

@dataclass
class CombinedFragment:
    start: int
    end: int
    content: str
    scene_type: str
    narrative_desc: str
    tags: list[str] = field(default_factory=list)

    def to_tag_result(self) -> TagResult:
        return TagResult(
            scene_type=self.scene_type,
            narrative_desc=self.narrative_desc,
            tags=self.tags,
        )


# ── 公共入口 ──────────────────────────────────────────────────────────────────

async def split_and_tag_async(
    chapter_text: str,
    llm: LLMClient,
) -> list[CombinedFragment]:
    """合并切割+打标，单次 LLM 调用完成。超长章节自动滑动窗口。"""
    if len(chapter_text) > SLIDING_WINDOW_THRESHOLD:
        return await _split_with_sliding_window_async(chapter_text, llm)
    return await _split_and_tag_single_async(chapter_text, llm)


# ── 内部实现 ──────────────────────────────────────────────────────────────────

async def _split_and_tag_single_async(
    chapter_text: str, llm: LLMClient
) -> list[CombinedFragment]:
    prompt = COMBINED_PROMPT_TEMPLATE.format(chapter_text=chapter_text)
    result = await llm.chat_json_async(prompt, max_tokens=8000)

    if not result or not isinstance(result, dict) or "fragments" not in result:
        logger.error("合并 LLM 未返回 fragments 字段: %s", str(result)[:200])
        return []

    raw_fragments = result["fragments"]
    if not isinstance(raw_fragments, list) or not raw_fragments:
        logger.error("合并 LLM fragments 为空或类型错误")
        return []

    fragments = _locate_combined_fragments(chapter_text, raw_fragments)
    if not fragments:
        return []

    ok, msg = _validate_coverage(chapter_text, fragments)
    if not ok:
        logger.error("覆盖率校验失败: %s", msg)
    return fragments


async def _split_with_sliding_window_async(
    chapter_text: str, llm: LLMClient
) -> list[CombinedFragment]:
    import asyncio as _asyncio

    logger.info("章节字数 %d 超阈值，启用滑动窗口", len(chapter_text))
    windows: list[tuple[int, int]] = []
    pos = 0
    while pos < len(chapter_text):
        end = min(pos + SLIDING_WINDOW_SIZE, len(chapter_text))
        windows.append((pos, end))
        if end == len(chapter_text):
            break
        pos = end - SLIDING_WINDOW_OVERLAP

    async def _process_window(w_start: int, w_end: int) -> list[CombinedFragment]:
        sub_frags = await _split_and_tag_single_async(chapter_text[w_start:w_end], llm)
        for f in sub_frags:
            f.start += w_start
            f.end += w_start
        return sub_frags

    results = await _asyncio.gather(*[_process_window(s, e) for s, e in windows])
    all_frags: list[CombinedFragment] = [f for frags in results for f in frags]

    # 去重：overlap 区域内相同内容保留更长版本
    seen: dict[str, CombinedFragment] = {}
    for f in all_frags:
        key = f.content[:50]
        if key not in seen or (f.end - f.start) > (seen[key].end - seen[key].start):
            seen[key] = f
    return sorted(seen.values(), key=lambda x: x.start)


def _norm_mapping(text: str) -> tuple[str, list[int]]:
    """去除段落分隔符（\\n 和 \\u3000 全角空格），返回 (归一化文本, 位置映射)。

    pos_map[norm_idx] = orig_idx，用于将归一化位置还原为原文位置。
    """
    norm_chars: list[str] = []
    pos_map: list[int] = []
    for i, ch in enumerate(text):
        if ch == "\n" or ch == "\u3000":
            continue
        norm_chars.append(ch)
        pos_map.append(i)
    return "".join(norm_chars), pos_map


def _norm_str(s: str) -> str:
    """同样方式归一化锚点字符串（去 \\n 和 \\u3000）。"""
    return s.replace("\n", "").replace("\u3000", "")


def _find_start(
    anchor: str,
    text: str,
    from_pos: int,
    norm_text: str,
    pos_map: list[int],
) -> int:
    """四级降级查找 anchor 在 text 中的起始位置。"""
    # 1. 精确匹配
    pos = text.find(anchor, from_pos)
    if pos != -1:
        return pos

    # 2. 模糊：精确前 N 字
    fuzzy = anchor[:FUZZY_ANCHOR_LEN]
    pos = text.find(fuzzy, from_pos)
    if pos != -1:
        logger.debug("首句模糊(前%d字)匹配", FUZZY_ANCHOR_LEN)
        return pos

    # 3. 归一化匹配
    norm_anchor = _norm_str(anchor)
    norm_from = bisect.bisect_left(pos_map, from_pos)
    norm_pos = norm_text.find(norm_anchor, norm_from)
    if norm_pos != -1:
        logger.debug("首句归一化匹配成功")
        return pos_map[norm_pos]

    # 4. 归一化 + 模糊前 N 字
    norm_fuzzy = norm_anchor[:FUZZY_ANCHOR_LEN]
    if norm_fuzzy:
        norm_pos = norm_text.find(norm_fuzzy, norm_from)
        if norm_pos != -1:
            logger.debug("首句归一化+模糊匹配成功")
            return pos_map[norm_pos]

    return -1


def _find_end(
    anchor: str,
    text: str,
    from_pos: int,
    norm_text: str,
    pos_map: list[int],
) -> int:
    """四级降级查找 anchor 在 text 中的结束位置（包含 anchor 末尾）。"""
    # 1. 精确匹配
    pos = text.find(anchor, from_pos)
    if pos != -1:
        return pos + len(anchor)

    # 2. 模糊：后 N 字
    fuzzy_last = anchor[-FUZZY_ANCHOR_LEN:]
    pos = text.find(fuzzy_last, from_pos)
    if pos != -1:
        logger.debug("尾句模糊(后%d字)匹配", FUZZY_ANCHOR_LEN)
        return pos + len(fuzzy_last)

    # 3. 归一化匹配
    norm_anchor = _norm_str(anchor)
    norm_from = bisect.bisect_left(pos_map, from_pos)
    norm_pos = norm_text.find(norm_anchor, norm_from)
    if norm_pos != -1:
        logger.debug("尾句归一化匹配成功")
        end_norm = norm_pos + len(norm_anchor)
        orig_end = pos_map[end_norm - 1] + 1 if end_norm - 1 < len(pos_map) else len(text)
        return orig_end

    # 4. 归一化 + 模糊后 N 字
    norm_fuzzy = norm_anchor[-FUZZY_ANCHOR_LEN:]
    if norm_fuzzy:
        norm_pos = norm_text.find(norm_fuzzy, norm_from)
        if norm_pos != -1:
            logger.debug("尾句归一化+模糊匹配成功")
            end_norm = norm_pos + len(norm_fuzzy)
            orig_end = pos_map[end_norm - 1] + 1 if end_norm - 1 < len(pos_map) else len(text)
            return orig_end

    return -1


def _locate_combined_fragments(
    chapter_text: str, raw_fragments: list[dict]
) -> list[CombinedFragment]:
    """用 first_line/last_line 定位边界，同时提取标签元数据。

    四级降级匹配：精确 → 模糊 → 归一化 → 归一化+模糊
    解决 LLM 省略段落分隔符 \\n\\u3000 导致精确匹配失败的问题。
    """
    # 预计算归一化文本和位置映射（仅计算一次）
    norm_text, pos_map = _norm_mapping(chapter_text)

    fragments: list[CombinedFragment] = []
    search_start = 0

    for i, item in enumerate(raw_fragments):
        first = item.get("first_line", "").strip()
        last = item.get("last_line", "").strip()

        scene_type = str(item.get("scene_type", "其他")).strip()
        if scene_type not in VALID_SCENE_TYPES:
            logger.warning("片段 %d scene_type '%s' 非法，映射为'其他'", i, scene_type)
            scene_type = "其他"

        narrative_desc = str(item.get("narrative_desc", "")).strip()
        raw_tags = item.get("tags", [])
        tags = [str(t).strip() for t in raw_tags if str(t).strip()][:5]

        if not first or not last:
            logger.warning("片段 %d 缺少 first_line/last_line，跳过", i)
            continue

        if len(first) < MIN_ANCHOR_LEN:
            logger.warning("片段 %d first_line 过短（%d字）", i, len(first))
        if len(last) < MIN_ANCHOR_LEN:
            logger.warning("片段 %d last_line 过短（%d字）", i, len(last))

        start = _find_start(first, chapter_text, search_start, norm_text, pos_map)
        if start == -1:
            logger.error("片段 %d 首句四级匹配均失败: %.40s", i, first)
            continue

        last_from = start + max(len(first), 10)
        end = _find_end(last, chapter_text, last_from, norm_text, pos_map)
        if end == -1:
            logger.error("片段 %d 尾句四级匹配均失败: %.40s", i, last[-40:])
            continue

        fragments.append(CombinedFragment(
            start=start,
            end=end,
            content=chapter_text[start:end],
            scene_type=scene_type,
            narrative_desc=narrative_desc,
            tags=tags,
        ))
        search_start = end

    return fragments


def _validate_coverage(
    chapter_text: str, fragments: list[CombinedFragment]
) -> tuple[bool, str]:
    if not fragments:
        return False, "无片段"

    total_covered = sum(len(f.content) for f in fragments)
    coverage = total_covered / len(chapter_text)
    if coverage < 0.75:
        logger.warning("覆盖率偏低: %.2f（可能漏掉部分内容）", coverage)
    if coverage > 1.15:
        return False, f"覆盖率超 1: {coverage:.2f}（存在重叠）"

    for i in range(len(fragments) - 1):
        gap = fragments[i + 1].start - fragments[i].end
        if 0 < gap <= 50:
            # 小夹缝并入前片段
            fragments[i].end = fragments[i + 1].start
            fragments[i].content = chapter_text[fragments[i].start: fragments[i].end]
        elif gap > 50:
            logger.warning("片段 %d 与 %d 间隔 %d 字", i, i + 1, gap)
        elif gap < -20:
            return False, f"片段 {i} 与 {i + 1} 重叠 {-gap} 字"

    return True, "ok"
