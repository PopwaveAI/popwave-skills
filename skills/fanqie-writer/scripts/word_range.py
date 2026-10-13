#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""word_range.py — 单章字数区间的**唯一解析入口**（共用模块，不带平台词汇）

━━━ 为什么需要它（2026-09-30 新增）━━━

字数区间此前**硬编码在两个脚本里**（各写 DEFAULT=2200/2800），而「按题材分档」只写在文档里。
文档改了、脚本没改，就会**「规则在 ≠ 会执行」**：立项按某题材定 3000 字，写完跑门禁被判 FAIL。
本模块把"区间从哪来"收成一处，两个脚本共用；上层技能可另设校验器兜漂移。

━━━ 解析优先级（高 → 低）━━━

    ① 命令行显式 `--min/--max`            —— 一次性的临时口径
    ② 本书立项参数 `.learnings/立项参数.json` —— 立项拍板的口径
       **查找起点（v1.29.30 补第三档）**：`book_dir` ＞ `chapter_path` ＞ **当前目录**，
       从起点逐级向上找。
    ③ `--range-config <json>` ＋ `--genre <题材>` —— machine 分档表（平台专属数据放在各技能自己的 json 里）
    ④ 内置默认 2200-2800                  —— **通用保守值；降级到这一层会在输出里显式标出**

**⚠️ 降级必须可见**：返回的 `label` 会被两个脚本打印出来。缺书档、题材没匹配上，
执行者一眼能看到「用的是哪一档」，不许静默用默认值糊过去。

**⚠️ 为什么②要认「当前目录」（v1.29.30 修）**：`plan_word_quota.py` 的**写前**用法
（`--total/--scenes`，不给任何路径）此前 `start=None` → **直接跳过②**，落到④内置默认。
实测：`.learnings/立项参数.json` 就在那个目录里，脚本照样报「未找到」，
**并且退出码 0**——静默降级。之所以一路没被发现，是因为几个样本的本书区间
**恰好等于内置默认 2200-2800**，表里的数字全对。
**降级发生在"区间来源"这一维上时，检查面覆盖不到它**（缺维病）。
故：起点链补上「当前目录」，并且上层脚本读到④时要**中止**而不是照算。

━━━ 黄金三章 ━━━

本书参数里 `黄金三章.mode == "descending"`（递减结构）时，**第 1-3 章改用递减序列**
（默认 2500 / 2000 / 1500，容差 ±25%）——否则递减结构的第 2、3 章会被字数门禁**误判 FAIL**。
「stable」（稳定区间）不需要特殊处理，用本书/分档区间即可。
"""

import json
import os
import re
import sys

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
            book_dir=None, chapter_path=None, cwd=None):
    """解析字数区间，返回 dict：min / max / label / note

    参数任一可为 None；chapter_path 既用于向上找本书参数，也用于取章号（黄金三章判断）。
    cwd 是**查找起点的最后一档**（不给则取 os.getcwd()）；显式传参是为了让污染测试
    能在不 chdir 的前提下验「写前那一步到底读不读得到本书口径」。
    """
    # ① 命令行显式
    if min_words and max_words:
        return {"min": int(min_words), "max": int(max_words),
                "label": "命令行显式指定", "note": ""}

    # ② 本书立项参数（查找起点：book_dir ＞ chapter_path ＞ 当前目录）
    start = book_dir or chapter_path or cwd or os.getcwd()
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
            "label": "⚠️ 内置默认（区间来源未确定：命令行没给 --min/--max，也没找到本书 .learnings/立项参数.json）",
            "note": "通用保守值；写前请加 --book <本书目录>，或 cd 到本书目录下运行"}


# ─────────────────────────── 污染测试（自带）───────────────────────────
def _selftest():
    """**改前必 FAIL、改后必 PASS**：锁住「写前那一步真的读得到本书口径」

    区分度在哪：用例③ 用的是 `plan_word_quota.py` 写前的真实调用形态
    （一个路径都不给），而本书参数区间**故意设成 2500-3500**（≠ 内置默认 2200-2800）
    —— 静默回落时数字会露馅，不会像几个存量样本那样"恰好等于默认值"。
    """
    import tempfile

    rows = []

    def check(label, ok, detail=""):
        rows.append((label, bool(ok), detail))

    with tempfile.TemporaryDirectory() as td:
        book = os.path.join(td, "某本书")
        os.makedirs(os.path.join(book, ".learnings"))
        cfg = os.path.join(book, ".learnings", "立项参数.json")
        with open(cfg, "w", encoding="utf-8") as fh:
            json.dump({"题材": "悬疑推理", "单章字数": {"min": 2500, "max": 3500}},
                      fh, ensure_ascii=False)
        ch = os.path.join(book, "第01章.md")
        with open(ch, "w", encoding="utf-8") as fh:
            fh.write("# 第01章\n")

        r = resolve(book_dir=book)
        check("① --book 指向本书 → 读到本书区间",
              (r["min"], r["max"]) == (2500, 3500),
              "%s-%s ← %s" % (r["min"], r["max"], r["label"]))

        r = resolve(chapter_path=ch)
        check("② 给章节文件 → 读到本书区间",
              (r["min"], r["max"]) == (2500, 3500),
              "%s-%s ← %s" % (r["min"], r["max"], r["label"]))

        r = resolve(cwd=book)
        check("③ **只给当前目录**（写前那一步的真实形态）→ 读到本书区间",
              (r["min"], r["max"]) == (2500, 3500),
              "%s-%s ← %s   ← 本格是 v1.29.30 修的缺陷：改前这里回落 2200-2800"
              % (r["min"], r["max"], r["label"]))

        empty = os.path.join(td, "空目录")
        os.makedirs(empty)
        r = resolve(cwd=empty)
        check("④ 不在任何书内 → 回落默认**且带 ⚠️ 标记**（不许假装读到了）",
              (r["min"], r["max"]) == (DEFAULT_MIN, DEFAULT_MAX)
              and r["label"].startswith("⚠️"),
              "%s-%s ← %s" % (r["min"], r["max"], r["label"]))

        with open(cfg, "w", encoding="utf-8") as fh:
            json.dump({"题材": "悬疑推理", "单章字数": {"min": 2500, "max": 3500},
                       "黄金三章": {"mode": "descending", "seq": [2500, 2000, 1500]}},
                      fh, ensure_ascii=False)
        r = resolve(cwd=book, chapter_path=os.path.join(book, "第02章.md"))
        check("⑤ 回跑存量项：黄金三章递减第 2 章仍按递减序列放行（2000±25%）",
              (r["min"], r["max"]) == (1500, 2500),
              "%s-%s ← %s" % (r["min"], r["max"], r["label"]))

        r = resolve(min_words=3000, max_words=4000, cwd=book)
        check("⑥ 回跑存量项：命令行显式仍最高优先（3000-4000 不被本书 2500-3500 盖掉）",
              (r["min"], r["max"]) == (3000, 4000),
              "%s-%s ← %s" % (r["min"], r["max"], r["label"]))

    print("=" * 66)
    print("word_range · 污染测试（区间解析入口有没有区分度）")
    print("=" * 66)
    bad = 0
    for label, ok, detail in rows:
        print("%s %s" % ("[OK]" if ok else "[X] ", label))
        if detail:
            print("      %s" % detail)
        bad += 0 if ok else 1
    print("-" * 66)
    print("[%s] 污染测试%s" % ("OK" if not bad else "X",
                              "通过：写前也读得到本书口径，真没有时才降级" if not bad
                              else "未通过（%d 处）" % bad))
    return 0 if not bad else 1


def main():
    import argparse
    ap = argparse.ArgumentParser(description="字数区间解析入口（共用模块）")
    ap.add_argument("--selftest", action="store_true", help="污染测试自证")
    ap.add_argument("--book", help="本书目录")
    ap.add_argument("--check", help="章节文件（既用于找本书参数，也用于取章号）")
    ap.add_argument("--genre", help="题材名，配合 --range-config")
    ap.add_argument("--range-config", help="分档表 json")
    ap.add_argument("--min", type=int, help="显式下限")
    ap.add_argument("--max", type=int, help="显式上限")
    args = ap.parse_args()

    if args.selftest:
        return _selftest()

    r = resolve(min_words=args.min, max_words=args.max,
                range_config=args.range_config, genre=args.genre,
                book_dir=args.book, chapter_path=args.check)
    print(describe(r))
    # 降级到「来源未确定」＝ 调用方读不到本书口径，按失败结束（退出码 3）
    return 3 if str(r["label"]).startswith("⚠️") else 0


if __name__ == "__main__":
    sys.exit(main())


def describe(r):
    """一行文字：区间 ＋ 来源（给用户/执行者看，降级时必须可见）"""
    s = "%d-%d 字  ← 来源：%s" % (r["min"], r["max"], r["label"])
    if r.get("note"):
        s += "（%s）" % r["note"]
    return s
