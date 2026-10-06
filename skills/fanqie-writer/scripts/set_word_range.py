#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""set_word_range.py — 立项时把「单章字数」写进本书，让门禁脚本自己找得到

━━━ 为什么要有它（2026-09-30 新增）━━━

2026-09-29 技能补了「单章字数按题材分档」的**文档**（`references/fanqie-platform-facts.md` 四·补），
但只改了文档与 SKILL.md 的两处说法——**两个门禁脚本仍硬编码 2200-2800**。
后果：立项按悬疑定 3000 字，写完跑 `check_chapter_wordcount.py` 会被判 FAIL（规则在 ≠ 会执行）。

修法＝**让"分档"落成一份本书级参数文件**，脚本自动读它：

    novels/<书名>/.learnings/立项参数.json
    {
      "题材": "悬疑推理",
      "单章字数": {"min": 2500, "max": 3500},
      "黄金三章": {"mode": "descending", "seq": [2500, 2000, 1500], "tolerance": 0.25}
    }

**本脚本是唯一该写这份文件的地方**——手写容易写歪（数字得跟分档表对得上），
所以数字一律从 `scripts/word-range.json`（机器真源）取，不让人手动敲。

━━━ 用法 ━━━

    # 立项定字数（把 <书名> 换成你的书目录名）
    python scripts/set_word_range.py --book novels/某书 --genre 悬疑推理

    # 黄金三章选「递减结构」（第 1-3 章 = 2500/2000/1500 ±25%）
    python scripts/set_word_range.py --book novels/某书 --genre 悬疑推理 --trend descending

    # 看会写什么但不落盘
    python scripts/set_word_range.py --book novels/某书 --genre 悬疑推理 --dry-run

    # 已存在且要改（覆盖）
    python scripts/set_word_range.py --book novels/某书 --genre 玄幻仙侠 --force
"""

import argparse
import io
import json
import os
import sys

if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
TABLE = os.path.join(HERE, "word-range.json")
CONFIG_REL = os.path.join(".learnings", "立项参数.json")


def load_table(path=TABLE):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def match_genre(table, genre):
    """题材名 → (命中的键, {min,max,note})；匹配不到返回 (None, None)"""
    genres = table.get("genres") or {}
    if genre in genres:
        return genre, genres[genre]
    for k, v in genres.items():
        if k and (genre in k or k in genre):
            return k, v
    return None, None


def main():
    ap = argparse.ArgumentParser(description="把本书的单章字数口径写进 .learnings/立项参数.json")
    ap.add_argument("--book", required=True, help="本书目录（如 novels/第九赛季）")
    ap.add_argument("--genre", required=True, help="题材名（如 悬疑推理 / 玄幻仙侠 / 都市言情）")
    ap.add_argument("--trend", default="stable", choices=["stable", "descending"],
                    help="黄金三章口径：stable＝不额外改区间（默认）／descending＝递减结构")
    ap.add_argument("--table", default=TABLE, help="分档表 json（默认 scripts/word-range.json）")
    ap.add_argument("--force", action="store_true", help="已存在时覆盖")
    ap.add_argument("--dry-run", action="store_true", help="只打印，不落盘")
    args = ap.parse_args()

    if not os.path.isdir(args.book):
        print("[X] 本书目录不存在：%s（先建好项目目录，或把 --book 指向正确路径）" % args.book)
        return 2
    if not os.path.isfile(args.table):
        print("[X] 找不到分档表：%s" % args.table)
        return 2

    table = load_table(args.table)
    key, rng = match_genre(table, args.genre)
    if key is None:
        print("[X] 分档表里没有题材「%s」。" % args.genre)
        print("    可选：%s" % "、".join(sorted((table.get("genres") or {}).keys())))
        print("    新题材请先补 references/fanqie-platform-facts.md 四·补的表，再补 word-range.json，")
        print("    然后跑 python scripts/check_word_range_sync.py 校验两者一致。")
        return 2

    cfg = {
        "_说明": "立项时由 scripts/set_word_range.py 生成。单章字数＝写作期不许改的口径"
                 "（改字数会让卡点位置全乱）；要改须回立项，并说明理由。",
        "_来源": "%s（题材料目：%s）" % (os.path.basename(args.table), key),
        "题材": args.genre,
        "单章字数": {"min": int(rng["min"]), "max": int(rng["max"]), "note": rng.get("note", "")},
    }

    g3 = table.get("golden3") or {}
    if args.trend == "descending":
        d = g3.get("descending") or {}
        cfg["黄金三章"] = {
            "mode": "descending",
            "seq": d.get("seq") or [2500, 2000, 1500],
            "tolerance": d.get("tolerance", 0.25),
            "note": d.get("note", "递减结构，降低新手阅读门槛"),
        }
    else:
        cfg["黄金三章"] = {
            "mode": "stable",
            "note": (g3.get("note") or "") + "；stable ＝ 第 1-3 章沿用本书单章字数区间，不另设区间",
        }

    edges = table.get("algorithm_edges")
    if edges:
        cfg["算法边界（参考，非门禁）"] = {k: v for k, v in edges.items() if k != "note"}

    target = os.path.join(args.book, CONFIG_REL)
    text = json.dumps(cfg, ensure_ascii=False, indent=2) + "\n"

    print("=" * 62)
    print("本书单章字数口径")
    print("=" * 62)
    print("  本书目录 : %s" % args.book)
    print("  题材     : %s（分档表命中键：%s）" % (args.genre, key))
    print("  单章字数 : %d-%d 字" % (cfg["单章字数"]["min"], cfg["单章字数"]["max"]))
    if args.trend == "descending":
        print("  黄金三章 : 递减结构 %s（容差 ±%d%%）"
              % ("→".join(str(x) for x in cfg["黄金三章"]["seq"]),
                 round(cfg["黄金三章"]["tolerance"] * 100)))
    else:
        print("  黄金三章 : 沿用本书区间（stable）")
    print("  落盘位置 : %s" % target)

    if args.dry_run:
        print("\n（--dry-run：未落盘）")
        return 0

    if os.path.isfile(target) and not args.force:
        print("\n[!] 该文件已存在，未覆盖：%s" % target)
        print("    想改口径 → 加 --force 重跑；只想看内容 → 直接读那个文件。")
        return 2

    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8") as fh:
        fh.write(text)
    print("\n[OK] 已写入。写前配额与写后校验会**自动**读它——命令不必再带区间参数。")

    # 立刻回读校验（落盘必校验）
    with io.open(target, encoding="utf-8") as fh:
        back = fh.read()
    ok = ('"题材": "%s"' % args.genre) in back and ('"min": %d' % cfg["单章字数"]["min"]) in back
    print("[%s] 回读校验：%s" % ("OK" if ok else "X", target))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
