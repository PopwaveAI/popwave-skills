#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""word_range.py — 单章字数区间的**唯一解析入口**（共用模块，不带平台词汇）

━━━ 为什么需要它（2026-09-30 新增）━━━

字数区间此前**硬编码在两个脚本里**（各写 DEFAULT=2200/2800），而「按题材分档」只写在文档里。
文档改了、脚本没改，就会**「规则在 ≠ 会执行」**：立项按某题材定 3000 字，写完跑门禁被判 FAIL。
本模块把"区间从哪来"收成一处，两个脚本共用；上层技能可另设校验器兜漂移。

━━━ 解析优先级（高 → 低）━━━

    ① 命令行显式 `--min/--max`            —— 一次性的临时口径
    ② 本书立项参数 `.learnings/立项参数.json` —— 立项拍板的口径（从章节文件/目录向上自动找到）
    ③ `--range-config <json>` ＋ `--genre <题材>` —— machine 分档表（平台专属数据放在各技能自己的 json 里）
    ④ 内置默认 2200-2800                  —— **通用保守值；降级到这一层会在输出里显式标出**

**⚠️ 降级必须可见**：返回的 `label` 会被两个脚本打印出来。缺书档、题材没匹配上，
执行者一眼能看到「用的是哪一档」，不许静默用默认值糊过去。

━━━ 黄金三章 ━━━

本书参数里 `黄金三章.mode == "descending"`（递减结构）时，**第 1-3 章改用递减序列**
（默认 2500 / 2000 / 1500，容差 ±25%）——否则递减结构的第 2、3 章会被字数门禁**误判 FAIL**。
「stable」（稳定区间）不需要特殊处理，用本书/分档区间即可。
"""

import json
import os
import re

DEFAULT_MIN = 2200
DEFAULT_MAX = 2800

BOOK_CONFIG_REL = os.path.join(".learnings", "立项参数.json")
CHAPTER_RE = re.compile(r"第\s*(\d+)\s*章")

# 本书参数文件里可接受的「字数区间」键名（写法不同都认）
_RANGE_KEYS = ("单章字数", "字数区间", "word_range")


def parse_chapter_index(name):
    """从文件名里取章号（第01章/第12章-标题 → 1/12）；取不到返回 None"""
    m = CHAPTER_RE.search(os.path.basename(name or ""))
    return int(m.group(1)) if m else None


def find_book_config(start):
    """从 start（文件或目录）逐级向上找 `.learnings/立项参数.json`；找不到返回 None"""
    if not start:
        return None
    p = os.path.abspath(start)
    if os.path.isfile(p):
        p = os.path.dirname(p)
    while True:
        cand = os.path.join(p, BOOK_CONFIG_REL)
        if os.path.isfile(cand):
            return cand
        parent = os.path.dirname(p)
        if parent == p:
            return None
        p = parent


def _load_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def _book_range(cfg, chapter_index=None):
    """读本书立项参数 → {min,max,label,note}；不合规返回 None"""
    if not isinstance(cfg, dict):
        return None

    # 黄金三章·递减结构：第 1-3 章用递减序列，别让门禁误伤
    g3 = cfg.get("黄金三章") or cfg.get("黄金三章口径") or {}
    if isinstance(g3, dict):
        mode = str(g3.get("mode", "")).strip().lower()
        if mode in ("descending", "递减", "递减结构") and chapter_index and 1 <= chapter_index <= 3:
            seq = g3.get("seq") or [2500, 2000, 1500]
            tol = float(g3.get("tolerance", 0.25))
            target = int(seq[chapter_index - 1])
            lo = int(round(target * (1 - tol)))
            hi = int(round(target * (1 + tol)))
            return {
                "min": lo,
                "max": hi,
                "label": "本书参数·黄金三章递减结构（第 %d 章目标 %d 字，容差 ±%d%%）"
                         % (chapter_index, target, round(tol * 100)),
                "note": "递减结构同书择一，不混用（facts 第四节·补）",
            }

    wr = None
    for k in _RANGE_KEYS:
        if isinstance(cfg.get(k), dict):
            wr = cfg[k]
            break
    if wr is None:
        return None
    try:
        lo, hi = int(wr.get("min")), int(wr.get("max"))
    except (TypeError, ValueError):
        return None
    if lo <= 0 or hi <= 0 or lo > hi:
        return None
    genre = cfg.get("题材") or cfg.get("题材包") or ""
    return {
        "min": lo,
        "max": hi,
        "label": "本书立项参数（%s）" % (genre or "未记题材"),
        "note": "来自 .learnings/立项参数.json；写作期不改",
    }


def _config_range(table, genre):
    """从分档表（各技能自带的字数分档 json）取区间；题材没匹配上就退到表内 default"""
    if not isinstance(table, dict):
        return None
    genres = table.get("genres") or {}
    key = None
    if genre:
        if genre in genres:
            key = genre
        else:
            for k in genres:
                if k and (genre in k or k in genre):
                    key = k
                    break
    if key is None:
        d = table.get("default")
        if not isinstance(d, dict):
            return None
        try:
            lo, hi = int(d["min"]), int(d["max"])
        except (KeyError, TypeError, ValueError):
            return None
        return {
            "min": lo,
            "max": hi,
            "label": "分档表默认档（题材「%s」未匹配）" % (genre or "未给"),
            "note": d.get("note", ""),
        }
    v = genres[key]
    return {
        "min": int(v["min"]),
        "max": int(v["max"]),
        "label": "分档表·%s" % key,
        "note": v.get("note", ""),
    }


def resolve(min_words=None, max_words=None, range_config=None, genre=None,
            book_dir=None, chapter_path=None):
    """解析字数区间，返回 dict：min / max / label / note

    参数任一可为 None；chapter_path 既用于向上找本书参数，也用于取章号（黄金三章判断）。
    """
    # ① 命令行显式
    if min_words and max_words:
        return {"min": int(min_words), "max": int(max_words),
                "label": "命令行显式指定", "note": ""}

    # ② 本书立项参数
    start = book_dir or chapter_path
    if start:
        cfg_path = find_book_config(start)
        if cfg_path:
            cfg = _load_json(cfg_path)
            idx = parse_chapter_index(chapter_path) if chapter_path else None
            r = _book_range(cfg, idx)
            if r:
                return r

    # ③ 分档表（machine）
    if range_config:
        table = _load_json(range_config)
        if table is None:
            return {"min": DEFAULT_MIN, "max": DEFAULT_MAX,
                    "label": "⚠️ 分档表读取失败（%s）→ 回落默认" % range_config, "note": ""}
        r = _config_range(table, genre)
        if r:
            return r

    # ④ 内置默认
    return {"min": DEFAULT_MIN, "max": DEFAULT_MAX,
            "label": "⚠️ 内置默认（未找到 .learnings/立项参数.json）", "note": "通用保守值"}


def describe(r):
    """一行文字：区间 ＋ 来源（给用户/执行者看，降级时必须可见）"""
    s = "%d-%d 字  ← 来源：%s" % (r["min"], r["max"], r["label"])
    if r.get("note"):
        s += "（%s）" % r["note"]
    return s
