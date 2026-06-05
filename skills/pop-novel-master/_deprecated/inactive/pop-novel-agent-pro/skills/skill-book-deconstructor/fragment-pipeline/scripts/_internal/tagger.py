"""Step 3: LLM 语义标签（v3.6 涌现式）。

核心变化（v3.6）：
- 废弃固定 13 类标签，改为 10 类宽泛 scene_type + LLM 自由 narrative_desc + 自由 tags
- 新增 tag_batch_async()：单次调用处理 4 个片段，减少 ~75% API 调用次数
- TagResult 新增 scene_type / narrative_desc / tags 字段
- 写入 FTS 时将 narrative_desc + tags 合并进索引，支持语义检索
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .llm_client import LLMClient

logger = logging.getLogger(__name__)

VALID_SCENE_TYPES = {
    "战斗", "成长", "获取", "立威", "探索",
    "仪式", "对话", "情感", "建设", "其他",
}

# ── 单片段 Prompt ────────────────────────────────────────────────────────────

_SINGLE_PROMPT = """你是一位网文编辑，擅长判断场景类型和叙事功能。

任务：为以下网文片段打标签。

scene_type（必选 1 个）：
- 战斗：打架/碾压/Boss战/行刑处决/撤退追击
- 成长：修炼/练级/技能习得/突破/面板/顿悟/淬炼
- 获取：战利品/功法秘籍/装备/金钱/势力招募/任务奖励
- 立威：当众示威/被挑衅反击/宣示立场/震慑对手
- 探索：行军/侦察/追踪/发现线索/新地点到达
- 仪式：身体改造/血脉觉醒/职业转化/融合/改写
- 对话：谈判/对质/信息交换/战后交谈/招募说服
- 情感：日常/羁绊建立/情绪内心/休整/牺牲代价
- 建设：种田/势力扩张/资源积累/培养下属/长期规划
- 其他：不属于以上任何类型

输出格式（严格 JSON）：
{{
  "scene_type": "战斗",
  "narrative_desc": "Boss战开场：主角与石质巨人正面对抗，初期劣势被迫后退",
  "tags": ["劣势应战", "强弱悬殊", "以小博大", "主动出击"]
}}

要求：
- narrative_desc：1-2 句话直接描述内容（不是解释分类），入 FTS 索引
- tags：2-5 个从内容提炼的关键词，不限词表
- 严格 JSON，不输出其他内容

片段内容：
{fragment_text}
"""

# ── 批量 Prompt（4 片段 → 1 次调用）────────────────────────────────────────

_BATCH_PROMPT = """你是一位网文编辑。对以下 {count} 个片段逐一打标签。

scene_type 固定选项（每片段必选 1 个）：
战斗 / 成长 / 获取 / 立威 / 探索 / 仪式 / 对话 / 情感 / 建设 / 其他

- 战斗：打架/碾压/Boss战/行刑处决/撤退追击
- 成长：修炼/练级/突破/面板/顿悟
- 获取：战利品/功法/装备/金钱/招募/奖励
- 立威：示威/挑衅反击/宣示立场/震慑
- 探索：行军/侦察/追踪/新地点
- 仪式：身体改造/觉醒/职业转化/融合
- 对话：谈判/对质/信息交换/招募
- 情感：日常/羁绊/情绪/休整/牺牲
- 建设：种田/扩张/积累/培养/规划
- 其他：不属于以上

要求：
- narrative_desc：1-2 句描述实际内容（不解释分类）
- tags：2-5 个关键词，不限词表

输出：严格 JSON 对象（不输出其他内容）：
{{
  "results": [
    {{
      "index": 0,
      "scene_type": "...",
      "narrative_desc": "...",
      "tags": ["...", "..."]
    }}
  ]
}}

片段列表：
{fragments_text}
"""


@dataclass
class TagResult:
    scene_type: str
    narrative_desc: str
    tags: list[str] = field(default_factory=list)

    def fts_text(self, content: str) -> str:
        """返回写入 FTS 的合并文本：原文 + 描述 + 关键词，供 trigram 全文检索。"""
        parts = [content, self.narrative_desc] + self.tags
        return "\n".join(p for p in parts if p)


# ── 同步单片段 ───────────────────────────────────────────────────────────────

def tag_fragment(fragment_text: str, llm: LLMClient) -> TagResult | None:
    prompt = _SINGLE_PROMPT.format(fragment_text=fragment_text)
    result = llm.chat_json(prompt, max_tokens=600)
    return _parse_single(result)


# ── 异步批量（主力） ─────────────────────────────────────────────────────────

async def tag_batch_async(
    fragments: list[str],
    llm: LLMClient,
) -> list[TagResult | None]:
    """
    一次 LLM 调用处理 len(fragments) 个片段（建议 3-5 个）。
    返回与输入等长的列表，失败位置为 None。
    """
    if not fragments:
        return []

    fragments_text = "\n\n".join(
        f"=== 片段 {i} ===\n{text}" for i, text in enumerate(fragments)
    )
    prompt = _BATCH_PROMPT.format(
        count=len(fragments),
        fragments_text=fragments_text,
    )
    result = await llm.chat_json_async(prompt, max_tokens=200 * len(fragments))

    # 支持两种格式：{"results": [...]} 或直接 [...]
    if isinstance(result, dict):
        result = result.get("results") or result.get("fragments")
    if not isinstance(result, list):
        logger.warning("批量打标返回非数组，降级为逐片段异步打标")
        return await _fallback_one_by_one(fragments, llm)

    # 按 index 对齐，容忍 LLM 漏掉部分片段
    out: list[TagResult | None] = [None] * len(fragments)
    for item in result:
        if not isinstance(item, dict):
            continue
        idx = item.get("index")
        if idx is None or not isinstance(idx, int) or idx >= len(fragments):
            continue
        tr = _parse_single(item)
        if tr:
            out[idx] = tr

    # 对失败的降级处理（单独重试）
    failed = [i for i, r in enumerate(out) if r is None]
    if failed:
        logger.warning("批量打标 %d 个片段失败，逐一降级重试", len(failed))
        for i in failed:
            out[i] = await _tag_single_async(fragments[i], llm)

    return out


async def _tag_single_async(fragment_text: str, llm: LLMClient) -> TagResult | None:
    prompt = _SINGLE_PROMPT.format(fragment_text=fragment_text)
    result = await llm.chat_json_async(prompt, max_tokens=600)
    return _parse_single(result)


async def _fallback_one_by_one(
    fragments: list[str], llm: LLMClient
) -> list[TagResult | None]:
    import asyncio
    tasks = [_tag_single_async(f, llm) for f in fragments]
    return list(await asyncio.gather(*tasks))


# ── 解析工具 ─────────────────────────────────────────────────────────────────

def _parse_single(result: dict | None) -> TagResult | None:
    if not isinstance(result, dict):
        return None

    scene_type = str(result.get("scene_type", "")).strip()
    if scene_type not in VALID_SCENE_TYPES:
        logger.warning("LLM 返回未知 scene_type '%s'，映射为'其他'", scene_type)
        scene_type = "其他"

    narrative_desc = str(result.get("narrative_desc", "")).strip()
    raw_tags = result.get("tags", [])
    tags = [str(t).strip() for t in raw_tags if str(t).strip()][:5]

    return TagResult(scene_type=scene_type, narrative_desc=narrative_desc, tags=tags)
