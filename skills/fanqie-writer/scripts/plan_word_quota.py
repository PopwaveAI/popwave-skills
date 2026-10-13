#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""plan_word_quota.py — 单章字数配额表（**写前**用，不是写后补）

把「这一章 N 字」翻译成三把可以照着写的尺：
    每场目标字数 ／ 每场目标段数 ／ 每场建议拍数（谁对谁做了什么的一个来回）

**N 从哪来**：区间由 `scripts/word_range.py` 解析——命令行 `--min/--max`
＞ 本书 `.learnings/立项参数.json`（立项时定）＞ `--range-config` 分档表 ＞ 默认 2200-2800。
**本书参数怎么找到**（v1.29.30 修）：查找起点＝ `--book` ＞ `--check` 的章节文件 ＞ **当前目录**，
从起点逐级向上找 `.learnings/立项参数.json`。
> ⚠️ **一个路径都不给、又不在本书目录下运行时，读不到本书区间**——v1.29.29 及以前会
> **静默回落 2200-2800**（几个样本的本书区间恰好等于默认值，所以一直没被发现）。
> 现在**读到默认档就直接中止、退出码 3、不输出配额表**：表是要贴进 `施工细账_卷N.md` 的实物，
> **用错区间算出来的表比没有表更坏**。

━━━ 为什么需要它（2026-09-24 实测）━━━

沙雕样本三次重写，第一稿分别是 **1486 / 1822 / 1475 字**（目标 2200），
每次都要 3-5 轮扩写才达标。根因不是"描写不够"，是**拍数不够**。

实测恒等式 `字数 = 段数 × 均段字数`：

    叙述驱动（古言样本）        2436 字 ÷  91 段 = 26.8 字/段
    对白驱动·长段（沙雕样本）   2217 字 ÷ 108 段 = 20.5 字/段
    短句市井体（市井题材样本）  2480 字 ÷ 166 段 = **14.9 字/段**

→ 2200 字需要的段数：前两档 **82-107 段**；**短句市井体要到 145-165 段**。
   而第一稿通常只写到约 **70 段**。实务上「扩写」补的从来不是形容词，
   是**别人的反应与对白来回**。

⚠️ **第三条只有 1 本实测**（v1.29.31 记）——按「单一正例不得当标尺」，
   它**暂时只报数、不设参考带**；写的时候 `--avg-para 15` 即可，不必等它定档。
   对照数字：同一章按 `20.5` 推得 124 段，成稿实测 166 段（**多 34%**）——
   **字数是准的，段数与拍数会系统性低估**。写「一句话一段」的市井体时，
   别照默认的 23 或对白档的 20.5 给均段长。

所以配额必须落在「段数／拍数」上，不能落在「字数」上——字数不是一个可写的单位。

━━━ 用法 ━━━

    # 基础：6 场、目标 2250 字的逐场配额
    #   **在本书目录下运行**（查找起点会认当前目录，区间自动读本书立项参数）
    python plan_word_quota.py --total 2250 --scenes 6

    # 不在本书目录下运行 → 用 --book 指到本书（**写前推荐写法**，别省这个参数）
    python plan_word_quota.py --book novels/<书名> --total 2250 --scenes 6

    # 指定各场权重（重头场多给、收尾场少给；按场序给，逗号分隔）
    python plan_word_quota.py --book novels/<书名> --total 2250 --scenes 6 --weights 1,1.3,1.3,1,0.9,0.6

    # 换均段长（叙述驱动取 26-27；对白驱动取 20-21；不给则用中值 23）
    python plan_word_quota.py --book novels/<书名> --total 2250 --scenes 6 --avg-para 27

    # 写完核对：数出实际字数/段数，与目标对账（区间自动从本书立项参数取）
    python plan_word_quota.py --book novels/<书名> --total 3000 --scenes 6 --check 第01章.md

    # 不想写本书参数时，也可以直接指定题材/区间
    python plan_word_quota.py --total 3000 --scenes 6 --genre <题材名> --range-config <分档表 json>

**读不到本书区间时它不输出表**：打印 `[X] 区间来源未确定` 并以退出码 3 结束。
解法的正确顺序＝① 补 `--book <本书目录>` ② `cd <本书目录>` 后再跑 ③ 显式 `--floor/--ceil`
（**别用 ③ 糊过本书口径**）；三者都不成立＝立项漏了落盘那一步。

输出是 Markdown，可直接贴进 `.learnings/施工细账_卷N.md` 的写前准备。
"""

import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from word_range import resolve as resolve_range  # noqa: E402

# 均段长实测参考（均为**通过门禁**的章节；三档口径见文件头恒等式）
PARA_LEN_NARRATIVE = 26.8   # 叙述驱动（古言样本 2436 字 / 91 段）
PARA_LEN_DIALOGUE = 20.5    # 对白驱动·长段（沙雕样本 2217 字 / 108 段）
PARA_LEN_TERSE = 14.9       # 短句市井体（市井题材样本 2480 字 / 166 段）
                            # ⚠️ 仅 1 本实测（v1.29.31），**只报数、不设带**——
                            #    「单一正例不得当标尺」；写市井体请显式 --avg-para 15
PARA_LEN_DEFAULT = 23.0     # 中值（**仅在前三档都不适用且没给 --avg-para 时用**）

# 一拍（谁向谁施压 → 回应 → 局面变化）的估算字数：约 3 段
BEAT_CHARS = 65


def count_chapter(path):
    """统计章节的正文汉字数、段数、对白段占比、均段字数。只算正文，不含标题行。"""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    han = len(re.findall(r"[\u4e00-\u9fff]", text))
    paras = [p for p in text.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    n = len(paras) or 1
    dialogue = sum(1 for p in paras if p.strip().startswith("“"))
    return {
        "path": path,
        "han": han,
        "paras": len(paras),
        "avg_para": han / n,
        "dialogue_ratio": dialogue / n * 100,
    }


def build_quota(total, scenes, weights, avg_para):
    if weights is None:
        weights = [1.0] * scenes
    if len(weights) != scenes:
        raise ValueError(f"--weights 给了 {len(weights)} 个，但 --scenes 是 {scenes}，必须一一对应")
    if any(w <= 0 for w in weights):
        raise ValueError("--weights 每一项必须 > 0")

    s = sum(weights)
    rows = []
    for i, w in enumerate(weights, 1):
        chars = total * w / s
        paras = chars / avg_para
        beats = chars / BEAT_CHARS
        rows.append({
            "scene": i,
            "weight": w,
            "chars": int(round(chars)),
            "paras": int(round(paras)),
            "beats": max(1, int(round(beats))),
        })
    return rows


def main():
    ap = argparse.ArgumentParser(
        description="单章字数配额表（写前用）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--total", type=int, default=2250, help="本章目标字数（默认 2250）")
    ap.add_argument("--scenes", type=int, required=True, help="本章场数")
    ap.add_argument("--weights", type=str, default=None,
                    help="各场权重，逗号分隔（如 1,1.3,1.3,1,0.9,0.6）；不给则均分")
    ap.add_argument("--avg-para", type=float, default=None,
                    help="均段长。实测三档：叙述驱动 26-27 ／ 对白驱动·长段 20-21 ／ "
                         "**短句市井体 15**（一句话一段的写法用这个，别用默认 23）；"
                         "不给则用中值 23")
    ap.add_argument("--floor", type=int, default=None,
                    help="字数下限（不给则自动解析：本书立项参数 ＞ 分档表 ＞ 默认 2200）"
                         "—— 只用于一次性试算，**别用它绕开本书口径**")
    ap.add_argument("--ceil", type=int, default=None,
                    help="字数上限（不给则自动解析：本书立项参数 ＞ 分档表 ＞ 默认 2800）"
                         "—— 只用于一次性试算，**别用它绕开本书口径**")
    ap.add_argument("--genre", type=str, default=None,
                    help="题材名，配合 --range-config 用")
    ap.add_argument("--range-config", type=str, default=None,
                    help="分档表 json（各技能自带的字数分档 json）")
    ap.add_argument("--book", type=str, default=None,
                    help="本书目录，用于找 .learnings/立项参数.json"
                         "（写前推荐给上；不给则从 --check 的文件向上找，再退到当前目录向上找）")
    ap.add_argument("--check", type=str, default=None, help="已写章节文件，写完对账用")
    ap.add_argument("--actual", type=str, default=None,
                    help="各场实际字数，逗号分隔（如 206,63,1171,453,137,180）→ 逐场差额表")
    args = ap.parse_args()

    rng = resolve_range(min_words=args.floor, max_words=args.ceil,
                        range_config=args.range_config, genre=args.genre,
                        book_dir=args.book, chapter_path=args.check)
    args.floor, args.ceil = rng["min"], rng["max"]

    # ── v1.29.30：区间没落到本书口径就**不输出配额表** ──────────────────
    # 缺陷原状：本脚本的「写前」用法（--total/--scenes，一个路径都不给）此前读不到
    # 本书参数，静默回落 2200-2800，**退出码还是 0**；样本区间恰好等于默认值，
    # 所以这个静默降级一路没被发现。配额表是要贴进 `施工细账_卷N.md` 的实物——
    # **用错区间算出来的表比没有表更坏**（后面逐场对账全部按错基准判）。
    # 故：读到 ⚠️ 档即中止，并把「怎么修」打在屏幕上。
    if str(rng.get("label", "")).startswith("⚠️"):
        print("[X] **区间来源未确定**：命令行没给 `--min/--max`，也没找到本书 "
              "`.learnings/立项参数.json`。")
        print("    查找起点顺序：`--book` ＞ `--check` 的章节文件 ＞ **当前目录**（各自逐级向上找）。")
        print("    配额表会被贴进 `施工细账_卷N.md` 并作为逐场对账的基准，"
              "**用错区间算出来的表比没有表更坏**——故本脚本在此中止，不输出表。")
        print("    三选一：")
        print("      1) 加 `--book <本书目录>`              ← **写前常态**，本书口径已落盘时用这个")
        print("      2) `cd <本书目录>` 后重跑               ← 查找起点会认当前目录")
        print("      3) 显式给区间 `--floor <下限> --ceil <上限>`（**别用它糊过本书口径**）")
        print("    三者都不成立？→ 回立项跑 `scripts/set_word_range.py` 把本书区间落盘。")
        return 3

    avg_para = args.avg_para or PARA_LEN_DEFAULT
    weights = None
    if args.weights:
        weights = [float(x) for x in args.weights.split(",") if x.strip()]

    try:
        rows = build_quota(args.total, args.scenes, weights, avg_para)
    except ValueError as e:
        print(f"[X] {e}")
        return 2

    # ── 写前配额表 ──────────────────────────────────────────────
    print(f"## 本章字数配额（写前排定 · 目标 {args.total} 字 · {args.scenes} 场 · 均段长 {avg_para:.1f}）")
    print()
    print(f"> **区间来源**：{rng['label']}——下限 {rng['min']} ／ 上限 {rng['max']}"
          + (f"（{rng['note']}）" if rng.get('note') else ""))
    if not (args.floor <= args.total <= args.ceil):
        print(f"> ⚠️ 目标 {args.total} 字**落在区间 {args.floor}-{args.ceil} 之外**——"
              f"先回立项确认本书单章字数区间。")
    print()
    print("| 场 | 权重 | **目标字** | **目标段数** | **建议拍数** | 写完实测字 | 差额 |")
    print("|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['scene']} | {r['weight']:.2f} | **{r['chars']}** | **{r['paras']}** | {r['beats']} | | |")
    tot_p = sum(r["paras"] for r in rows)
    tot_b = sum(r["beats"] for r in rows)
    print(f"| **合计** | — | **{sum(r['chars'] for r in rows)}** | **{tot_p}** | **{tot_b}** | | |")
    print()

    lo = int(round(args.floor / PARA_LEN_DIALOGUE))
    hi = int(round(args.floor / PARA_LEN_NARRATIVE))
    print(f"> **写法（照这个写，不要照字数写）**：全章约 **{tot_p} 段**、**{tot_b} 拍**。")
    print(f"> 段数参考带：字数下限 {args.floor} 落在 **{hi}-{lo} 段**之间"
          f"（叙述驱动 {hi} 段 / 对白驱动 {lo} 段，实测均段长 "
          f"{PARA_LEN_NARRATIVE} vs {PARA_LEN_DIALOGUE}）。")
    print(f"> **上面那张表的「目标段数」用的是「均段长 {avg_para:.1f}」**"
          f"（命令行 `--avg-para` ＞ 中值 {PARA_LEN_DEFAULT}）；"
          f"**与本行参考带是两把尺**——参考带给的是**不同写法下的段数范围**"
          f"（叙述体少、对白体多），表中段数才是照写的目标。"
          f"**短句市井体（一句话一段）请显式传 `--avg-para 15`**"
          f"（实测 {PARA_LEN_TERSE}；不给会被按中值算、段数少掉约三分之一）。")
    print(f"> **一拍 ≈ {BEAT_CHARS} 字**（谁向谁施压 → 回应 → 局面变化）。"
          f"**拍数是可写的单位，字数不是。**")
    print("> ⚠️ **写前算，写后只做验收**。写完若某场差额 > 20%：**回细纲补「人的反应」，不回正文加形容词**"
          "（实测：历次扩写补的全是别人的反应与来回，没有一次是补描写）。")
    print()

    # ── 写完对账 ────────────────────────────────────────────────
    if args.check:
        if not os.path.exists(args.check):
            print(f"[X] 找不到文件：{args.check}")
            return 2
        st = count_chapter(args.check)
        print(f"### 对账：{os.path.basename(args.check)}")
        print()
        print(f"| 项 | 实测 | 目标 | 判定 |")
        print(f"|---|---|---|---|")
        ok_len = args.floor <= st["han"] <= args.ceil
        print(f"| 正文汉字数 | **{st['han']}** | {args.floor}-{args.ceil} | "
              f"{'✅ OK' if ok_len else ('❌ 不足' if st['han'] < args.floor else '❌ 超出')} |")
        para_ok = st["paras"] >= hi
        print(f"| 段数 | **{st['paras']}** | ≥ {hi}（下限 {args.floor} 字 ÷ 叙述档 "
              f"{PARA_LEN_NARRATIVE}） | {'✅ OK' if para_ok else '❌ 偏少'} |")
        print(f"| 均段长 | {st['avg_para']:.1f} | — | 参考（只画像，不判定） |")
        print(f"| 对白段占比 | {st['dialogue_ratio']:.0f}% | — | 参考（只画像，不判定） |")
        gap = st["paras"] - hi
        print()
        if st["han"] < args.floor:
            print(f"> ❌ **字数不足**：还差 **{args.floor - st['han']} 字**。")
            if gap < 0:
                print(f"> **缺的是 {abs(gap)} 段**——按一拍约 3 段算，等于 **"
                      f"{max(1, abs(gap) // 3)} 拍**。")
                print("> **补法：回细纲 / 写前准备，补「场上另外几个人各自的反应」与对白来回，"
                      "不回正文加形容词。**")
            else:
                print(f"> 段数已够，说明**均段长低于参考带**（当前 {st['avg_para']:.1f}）——"
                      f"可给已有段落补感官细节或动作延宕。")
                print(f"> ⚠️ **但先看这一条**：本档实测「短句市井体」均段长就是 "
                      f"{PARA_LEN_TERSE}（一句话一段）——若本书就是这个写法，"
                      f"**上面这句不适用**，问题不在均段长，而在**拍数不够**（回细纲补来回）。")
        elif st["han"] > args.ceil:
            print(f"> ❌ **超出上限** {st['han'] - args.ceil} 字：**删无功能元素，不删事件**。")
        else:
            print(f"> ✅ 字数达标。**下一步不是加字，是过位置验收与四问自检。**")
        print()

    # ── 逐场对账（甲8）────────────────────────────────────────
    if args.actual:
        try:
            actual = [int(x) for x in args.actual.split(",") if x.strip()]
        except ValueError:
            print("[X] --actual 必须是逗号分隔的整数")
            return 2
        if len(actual) != args.scenes:
            print(f"[X] --actual 给了 {len(actual)} 个，但 --scenes 是 {args.scenes}")
            return 2

        print(f"### 逐场对账（甲8）")
        print()
        print("| 场 | 计划字 | 实际字 | 差额 | 判定 |")
        print("|---|---|---|---|---|")
        over, under = [], []
        for r, a in zip(rows, actual):
            plan = r["chars"]
            diff = (a - plan) / plan * 100
            if diff < -30:
                v = "❌ **空场**（低于 70%）"; under.append(r["scene"])
            elif diff > 50:
                v = "❌ **独大**（高于 150%）"; over.append(r["scene"])
            elif diff < -20:
                v = "⚠️ 偏少"
            elif diff > 20:
                v = "⚠️ 偏多"
            else:
                v = "✅ 在 ±20% 内"
            print(f"| {r['scene']} | {plan} | {a} | {diff:+.0f}% | {v} |")
        print(f"| **合计** | **{sum(r['chars'] for r in rows)}** | **{sum(actual)}** | "
              f"**{(sum(actual) - sum(r['chars'] for r in rows)) / sum(r['chars'] for r in rows) * 100:+.0f}%** | |")
        print()
        if over:
            top = max(zip(rows, actual), key=lambda t: t[1])
            print(f"> ❌ **场 {over} 独大**（最大一场占全章 **{top[1] / sum(actual) * 100:.0f}%**，"
                  f"计划只占 {top[0]['chars'] / sum(r['chars'] for r in rows) * 100:.0f}%）——")
            print(f"> **把这一场切出去**：它里面至少能拆成 **2 场戏**（换地点或换对手即算一场）。")
            print(f"> **读者侧症状**：前半章读得很饱，后半章像赶场。")
        if under:
            print(f"> ❌ **场 {under} 是空场**——这些场**只写了一两句就跳过去了**，`跳`（动作级缺环）的温床。")
            print(f"> **补法**：给这些场补「场上另外几个人各自的反应」与对白来回，**不是补形容词**。")
        if not over and not under:
            print(f"> ✅ 逐场分布均衡。**这一项（甲8）过了。**")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
