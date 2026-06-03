"""LLM API 封装：同步/异步双模式，重试 + JSON 严格解析 + 指数退避。"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

load_dotenv()

logger = logging.getLogger(__name__)

VALID_SCENE_TYPES = {
    "战斗", "成长", "获取", "立威", "探索",
    "仪式", "对话", "情感", "建设", "其他",
}


@dataclass
class LLMConfig:
    api_key: str
    base_url: str
    model: str
    temperature: float = 0.3
    max_retries: int = 3
    retry_backoff: float = 2.0  # 指数退避基数（秒）


def _load_config() -> LLMConfig:
    api_key = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("KIMI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "未配置 API key。请复制 .env.example 为 .env 并填入 DEEPSEEK_API_KEY"
        )
    return LLMConfig(
        api_key=api_key,
        base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        model=os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash"),
    )


class LLMClient:
    """对外提供 chat_json()（同步）和 chat_json_async()（异步）。"""

    def __init__(self, config: LLMConfig | None = None):
        self.config = config or _load_config()
        self._sync_client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
        )
        self._async_client: AsyncOpenAI | None = None

    def _get_async_client(self) -> AsyncOpenAI:
        if self._async_client is None:
            self._async_client = AsyncOpenAI(
                api_key=self.config.api_key,
                base_url=self.config.base_url,
            )
        return self._async_client

    # ── 同步版本 ──────────────────────────────────────────────────────────────

    def chat_json(
        self,
        prompt: str,
        *,
        system: str = "你是一位专业的网文编辑，严格按 JSON 格式输出。",
        max_tokens: int = 4000,
        force_json_object: bool = True,
    ) -> dict[str, Any] | list[Any] | None:
        last_err: Exception | None = None
        for attempt in range(self.config.max_retries):
            try:
                kwargs: dict[str, Any] = {}
                if force_json_object:
                    kwargs["response_format"] = {"type": "json_object"}
                resp = self._sync_client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=self.config.temperature,
                    max_tokens=max_tokens,
                    **kwargs,
                )
                text = resp.choices[0].message.content or ""
                parsed = _extract_json(text)
                if parsed is not None:
                    return parsed
                logger.warning(
                    "LLM 返回非 JSON（attempt %d/%d）: %.200s",
                    attempt + 1, self.config.max_retries, text,
                )
            except Exception as e:  # noqa: BLE001
                last_err = e
                wait = self.config.retry_backoff ** attempt
                logger.warning(
                    "LLM 调用失败（attempt %d/%d），%.1fs 后重试: %s",
                    attempt + 1, self.config.max_retries, wait, e,
                )
                time.sleep(wait)
        logger.error("LLM 调用最终失败: %s", last_err)
        return None

    # ── 异步版本 ──────────────────────────────────────────────────────────────

    async def chat_json_async(
        self,
        prompt: str,
        *,
        system: str = "你是一位专业的网文编辑，严格按 JSON 格式输出。",
        max_tokens: int = 4000,
        force_json_object: bool = True,
    ) -> dict[str, Any] | list[Any] | None:
        client = self._get_async_client()
        last_err: Exception | None = None
        for attempt in range(self.config.max_retries):
            try:
                kwargs: dict[str, Any] = {}
                if force_json_object:
                    kwargs["response_format"] = {"type": "json_object"}
                resp = await client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=self.config.temperature,
                    max_tokens=max_tokens,
                    **kwargs,
                )
                text = resp.choices[0].message.content or ""
                parsed = _extract_json(text)
                if parsed is not None:
                    return parsed
                logger.warning(
                    "LLM 返回非 JSON（attempt %d/%d）: %.200s",
                    attempt + 1, self.config.max_retries, text,
                )
            except Exception as e:  # noqa: BLE001
                last_err = e
                wait = self.config.retry_backoff ** attempt
                logger.warning(
                    "LLM 异步调用失败（attempt %d/%d），%.1fs 后重试: %s",
                    attempt + 1, self.config.max_retries, wait, e,
                )
                await asyncio.sleep(wait)
        logger.error("LLM 异步调用最终失败: %s", last_err)
        return None


# ── JSON 提取工具 ────────────────────────────────────────────────────────────

_JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*([{\[].*?[}\]])\s*```", re.DOTALL)


def _extract_json(text: str) -> dict[str, Any] | list[Any] | None:
    """从 LLM 输出中提取 JSON 对象或数组。"""
    text = text.strip()

    # 1. markdown 代码块
    m = _JSON_BLOCK_RE.search(text)
    candidate = m.group(1) if m else None

    # 2. 直接是裸 JSON
    if candidate is None:
        if (text.startswith("{") and text.endswith("}")) or (
            text.startswith("[") and text.endswith("]")
        ):
            candidate = text

    # 3. 在文本中找首个完整 {...} 或 [...]
    if candidate is None:
        for open_ch, close_ch in [("{", "}"), ("[", "]")]:
            depth = 0
            start = -1
            for i, ch in enumerate(text):
                if ch == open_ch:
                    if depth == 0:
                        start = i
                    depth += 1
                elif ch == close_ch:
                    depth -= 1
                    if depth == 0 and start != -1:
                        candidate = text[start : i + 1]
                        break
            if candidate:
                break

    if candidate is None:
        return None

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None
