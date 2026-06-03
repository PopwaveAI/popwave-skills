"""Step 1: 清洗 + 章级分割。"""

from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

# 章节标题正则：兼容阿拉伯数字与中文数字
CHAPTER_RE = re.compile(
    r"第\s*([\d零一二三四五六七八九十百千万]+)\s*章\s*([^\n]*)"
)

# 广告/版权常见模式（按需扩展）
AD_PATTERNS = [
    re.compile(r"^.{0,20}(?:本书首发|本章未完|更多精彩|全本小说|笔趣阁|起点中文网).{0,80}$", re.MULTILINE),
    re.compile(r"^.{0,5}(?:www\.|http[s]?://)[^\s]+.{0,30}$", re.MULTILINE),
    re.compile(r"^.{0,5}\(本章完\).{0,10}$", re.MULTILINE),
]

# 中文数字 → 阿拉伯
_CN_NUM = {
    "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
}


def _cn_to_int(s: str) -> int | None:
    """中文数字转 int（支持 千百十）。"""
    if s.isdigit():
        return int(s)
    if not s:
        return None

    total = 0
    current = 0
    for ch in s:
        if ch in _CN_NUM:
            current = _CN_NUM[ch]
        elif ch == "十":
            total += (current or 1) * 10
            current = 0
        elif ch == "百":
            total += (current or 1) * 100
            current = 0
        elif ch == "千":
            total += (current or 1) * 1000
            current = 0
        elif ch == "万":
            total = (total + current) * 10000
            current = 0
        else:
            return None
    return total + current


def load_text(txt_path: Path, encoding: str = "gbk") -> str:
    """读 txt → utf-8 字符串。"""
    raw = txt_path.read_bytes()
    try:
        text = raw.decode(encoding)
    except UnicodeDecodeError:
        # 兜底：errors='replace'，记录字节位置
        text = raw.decode(encoding, errors="replace")
        logger.warning("解码 %s 出现非法字符，已替换为 ?", txt_path)
    return text


def clean_text(text: str) -> str:
    """去广告、统一空白。"""
    # 标准化换行
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # 删除广告
    for pat in AD_PATTERNS:
        text = pat.sub("", text)
    # 多余空行（≥3 个连续空行 → 2 个）
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def split_chapters(text: str) -> list[tuple[int, str, str]]:
    """
    按"第X章"切分章节。
    返回：[(seq_idx, chapter_title, chapter_text), ...]

    chapter_text 不包含标题行。
    seq_idx 为全书顺序索引（1-based），避免多弧线重置章号导致重复。
    chapter_title 保留原标题文字（原章号信息已在日志中记录）。
    """
    matches = list(CHAPTER_RE.finditer(text))
    if not matches:
        logger.error("未匹配到任何章节标题")
        return []

    chapters: list[tuple[int, str, str]] = []
    seq_idx = 0
    for i, m in enumerate(matches):
        ch_num_raw = m.group(1)
        ch_title = m.group(2).strip()
        ch_num = _cn_to_int(ch_num_raw)

        body_start = m.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[body_start:body_end].strip()

        if len(body) < 100:
            display_num = ch_num if ch_num is not None else ch_num_raw
            logger.warning("第 %s 章内容过短（%d 字），跳过", display_num, len(body))
            continue

        seq_idx += 1
        chapters.append((seq_idx, ch_title, body))

    logger.info("共解析出 %d 章", len(chapters))
    return chapters


def load_and_split(txt_path: Path, encoding: str = "gbk") -> list[tuple[int, str, str]]:
    """便捷函数：读文件 → 清洗 → 切章节。"""
    text = load_text(txt_path, encoding)
    text = clean_text(text)
    return split_chapters(text)
