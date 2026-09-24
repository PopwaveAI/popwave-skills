#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""plan_word_quota.py — 单章字数配额表（**写前**用，不是写后补）

把「这一章 2200-2800 字」翻译成三把可以照着写的尺：
    每场目标字数 ／ 每场目标段数 ／ 每场建议拍数（谁对谁做了什么的一个来回）

━━━ 为什么需要它（2026-09-24 实测）━━━

沙雕样本三次重写，第一稿分别是 **1486 / 1822 / 1475 字**（目标 2200），
每次都要 3-5 轮扩写才达标。根因不是"描写不够"，是**拍数不够**。

实测恒等式 `字数 = 段数 × 均段字数`：

    叙述驱动（古言样本）  2436 字 ÷  91 段 = 26.8 字/段
    对白驱动（沙雕样本）  2217 字 ÷ 108 段 = 20.5 字/段

→ 2200 字需要的段数是 **82-107 段**，而第一稿只写到约 **70 段**。
   实务上"扩写"补的从来不是形容词，是**别人的反应与对白来回**。

所以配额必须落在「段数／拍数」上，不能落在「字数」上——字数不是一个可写的单位。

━━━ 用法 ━━━

    # 基础：6 场、目标 2250 字的逐场配额
    python plan_word_quota.py --total 2250 --scenes 6

    # 指定各场权重（重头场多给、收尾场少给；按场序给，逗号分隔）
    python plan_word_quota.py --total 2250 --scenes 6 --weights 1,1.3,1.3,1,0.9,0.6

    # 换均段长（叙述驱动取 26-27；对白驱动取 20-21；不给则用中值 23）
    python plan_word_quota.py --total 2250 --scenes 6 --avg-para 27

    # 写完核对：数出实际字数/段数，与目标对账
    python plan_word_quota.py --total 2250 --scenes 6 --check 第01章.md

输出是 Markdown，可直接贴进 `.learnings/施工细账_卷N.md` 的写前准备。
"""

import argparse
import os
import re
import sys

# 均段长实测参考（2026-09-24 两个样本，均为通过门禁的章节）
PARA_LEN_NARRATIVE = 26.8   # 叙述驱动（古言样本 2436 字 / 91 段）
PARA_LEN_DIALOGUE = 20.5    # 对白驱动（沙雕样本 2217 字 / 108 段）
PARA_LEN_DEFAULT = 23.0     # 中值

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
                    help="均段长（叙述驱动 26-27 / 对白驱动 20-21 / 不给用中值 23）")
    ap.add_argument("--floor", type=int, default=2200, help="字数下限（默认 2200）")
    ap.add_argument("--ceil", type=int, default=2800, help="字数上限（默认 2800）")
    ap.add_argument("--check", type=str, default=None, help="已写章节文件，写完对账用")
    ap.add_argument("--actual", type=str, default=None,
                    help="各场实际字数，逗号分隔（如 206,63,1171,453,137,180）→ 逐场差额表")
    args = ap.parse_args()

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
        print(f"| 段数 | **{st['paras']}** | ≥ {hi}（下限 {args.floor} 字） | "
              f"{'✅ OK' if para_ok else '❌ 偏少'} |")
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
