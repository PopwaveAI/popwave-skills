# -*- coding: utf-8 -*-
"""
汇总 输出/manifest.jsonl，出对比表。

    python analyze.py                  # 全部
    python analyze.py --model deepseek-flash
    python analyze.py --detail          # 逐稿列表
"""

import argparse
import json
import statistics as st
from pathlib import Path

BASE = Path(__file__).resolve().parent
MANIFEST = BASE / "输出" / "manifest.jsonl"


def load():
    recs = []
    if not MANIFEST.exists():
        raise SystemExit("还没有 manifest.jsonl，先跑 run_test.py")
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        if r.get("status") == "ok":
            recs.append(r)
    return recs


def avg(xs):
    return round(st.mean(xs), 1) if xs else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model")
    ap.add_argument("--detail", action="store_true")
    a = ap.parse_args()

    recs = load()
    if a.model:
        recs = [r for r in recs if r["model"] == a.model]
    if not recs:
        raise SystemExit("没有匹配的记录")

    models = sorted({r["model"] for r in recs})
    print("=" * 78)
    print("总览")
    print("=" * 78)
    print("%-18s %5s %8s %8s %8s %8s %7s %7s" %
          ("模型", "稿数", "平均汉字", "最短", "最长", "平均秒", "半角引", "markdown"))
    for m in models:
        sub = [r for r in recs if r["model"] == m]
        han = [r["form"]["han"] for r in sub]
        sec = [r["seconds"] for r in sub]
        hq = sum(r["form"]["half_width_quote"] for r in sub)
        md = sum(r["form"]["md_bold"] + r["form"]["md_heading"] + r["form"]["md_hr"] + r["form"]["md_list"] for r in sub)
        print("%-18s %5d %8.1f %8d %8d %8.1f %7d %7d" %
              (m, len(sub), avg(han), min(han), max(han), avg(sec), hq, md))

    for m in models:
        sub = [r for r in recs if r["model"] == m]
        print()
        print("=" * 78)
        print("分赛道 · " + m)
        print("=" * 78)
        print("%-14s %5s %8s %8s %8s %8s %7s" %
              ("赛道", "稿数", "平均汉字", "最短", "最长", "平均秒", "助手话尾"))
        genres = []
        for r in sub:
            if r["genre"] not in genres:
                genres.append(r["genre"])
        for g in genres:
            gs = [r for r in sub if r["genre"] == g]
            han = [r["form"]["han"] for r in gs]
            sec = [r["seconds"] for r in gs]
            chatter = sum(1 for r in gs if r.get("tail_chatter"))
            print("%-14s %5d %8.1f %8d %8d %8.1f %7d" %
                  (g, len(gs), avg(han), min(han), max(han), avg(sec), chatter))

    # 思考量
    print()
    print("=" * 78)
    print("思考量")
    print("=" * 78)
    for m in models:
        sub = [r for r in recs if r["model"] == m]
        rt = [r.get("usage", {}).get("completion_tokens_details", {}).get("reasoning_tokens", 0) for r in sub]
        ct = [r.get("usage", {}).get("completion_tokens", 0) for r in sub]
        print("%-18s 思考tokens均值=%s  总completion均值=%s  思考占比=%s" %
              (m, avg(rt), avg(ct), ("%.0f%%" % (100.0 * avg(rt) / avg(ct))) if avg(ct) else "-"))

    if a.detail:
        print()
        print("=" * 78)
        print("逐稿")
        print("=" * 78)
        for r in sorted(recs, key=lambda x: (x["model"], x["genre"], x["run"])):
            f = r["form"]
            print("%-18s %-12s r%02d %6ss 汉字%5d 段%3d 破折号%2d %s" %
                  (r["model"], r["genre"], r["run"], r["seconds"], f["han"], f["paragraphs"],
                   f["em_dash"], "助手话尾" if r.get("tail_chatter") else ""))


if __name__ == "__main__":
    main()
