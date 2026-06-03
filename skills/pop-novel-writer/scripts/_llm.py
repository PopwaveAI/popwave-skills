"""LLM API 封装（轻量版，复用拆书技能配置）"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)


def load_config() -> dict:
    return {
        "api_key": os.environ["DEEPSEEK_API_KEY"],
        "base_url": os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        "model": os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash"),
    }


class LLMClient:
    def __init__(self):
        config = load_config()
        self.client = OpenAI(
            api_key=config["api_key"],
            base_url=config["base_url"],
        )
        self.model = config["model"]

    def chat_json(
        self,
        prompt: str,
        system: str = "你是一位专业的网文编辑，严格按 JSON 格式输出。",
        max_tokens: int = 4000,
        temperature: float = 0.3,
        max_retries: int = 3,
    ) -> dict[str, Any] | list[Any] | None:
        last_err = None
        for attempt in range(max_retries):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format={"type": "json_object"},
                )
                text = resp.choices[0].message.content or ""
                return json.loads(text)
            except Exception as e:
                last_err = e
                wait = 2**attempt
                logger.warning("LLM 调用失败 (attempt %d): %s", attempt + 1, e)
                time.sleep(wait)
        logger.error("LLM 调用最终失败: %s", last_err)
        return None
