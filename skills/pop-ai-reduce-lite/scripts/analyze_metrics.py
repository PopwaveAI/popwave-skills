# -*- coding: utf-8 -*-
"""
analyze_metrics.py — 降AI 指标统计脚本（v1.0）
供 pop-ai-reduce / pop-ai-reduce-lite 共用。禁止 agent 运行时自写脚本，统一用本脚本。

用法:
  python analyze_metrics.py <文件路径> [更多文件路径...]

输出:
  每个文件的指标 JSON（stdout），含：
  - chars: 正文字符数（去空白，含标点）
  - paras: 段落数
  - sents: 句子数
  - len_dist: 句长分布 {<=5, 6-14, 15-25, 26-35, 36-49, >=50}
  - max_streak: 15-25字最大连击数
  - streak_sents: 连击句子序号与文本（>=3 时给出，供定位修改）
  - short5: 极短句数(<=5字) / long50: 超长句数(>=50字)
  - max_single_para_run: 连续单句段最大连数
  - dashes: 破折号(——)数 / dash_per_100: 密度/100字
  - ascii_punct: 英文引号+标点总数（" ' , . ! ? : ; -）
  - not_but: "不是...而是..."（含变体"不是X，是Y"）数
  - first20 / last20: 首行前20字 / 末行后20字（供 L2 校验）
"""
import re
import sys
import json
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def strip_title(text):
    """去掉首行标题行（无句号且长度<30视为标题）。"""
    lines = text.split("\n")
    if lines and lines[0].strip() and len(lines[0].strip()) < 30 and "。" not in lines[0]:
        return "\n".join(lines[1:]).strip()
    return text.strip()


def metrics(path):
    raw = read_text(path)
    text = strip_title(raw)
    # 字符统计（去空白）
    chars = len(re.sub(r"\s", "", text))
    # 段落（按空行）
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    # 句子（按 。！？； 切分，省略号……不算切分；先统一 … -> \u2026）
    seg = text.replace("…", "\u2026")
    parts = re.split(r"[。！？；]", seg)
    sents = [p.strip() for p in parts if p.strip()]
    lens = [len(re.sub(r"\s", "", s)) for s in sents]
    # 句长分布
    dist = {"<=5": 0, "6-14": 0, "15-25": 0, "26-35": 0, "36-49": 0, ">=50": 0}
    for l in lens:
        if l <= 5:
            dist["<=5"] += 1
        elif l <= 14:
            dist["6-14"] += 1
        elif l <= 25:
            dist["15-25"] += 1
        elif l <= 35:
            dist["26-35"] += 1
        elif l <= 49:
            dist["36-49"] += 1
        else:
            dist[">=50"] += 1
    # 15-25 连击
    max_streak = 0
    cur = 0
    streak_start = None
    streak_sents = []
    for i, l in enumerate(lens):
        if 15 <= l <= 25:
            if cur == 0:
                streak_start = i
            cur += 1
            if cur > max_streak:
                max_streak = cur
            if cur >= 3:
                if streak_sents and streak_sents[-1]["start"] == streak_start:
                    streak_sents[-1] = {"start": streak_start, "end": i, "n": cur}
                else:
                    streak_sents.append({"start": streak_start, "end": i, "n": cur})
        else:
            cur = 0
            streak_start = None
    # 连续单句段
    para_sent_counts = [len(re.findall(r"[。！？；]", p)) for p in paras]
    max_single_para_run = 0
    cur_single = 0
    for c in para_sent_counts:
        if c == 1:
            cur_single += 1
            max_single_para_run = max(max_single_para_run, cur_single)
        else:
            cur_single = 0
    # 表层字符
    dashes = len(re.findall(r"——", raw))
    ascii_punct = len(re.findall(r'["\',\.!?;:\-]', text))
    not_but = len(re.findall(r"不是[^。！？；]{0,20}而是", text)) + len(
        re.findall(r"不是[^。！？；]{0,15}[，,]是", text)
    )
    lines_nz = [l for l in raw.split("\n") if l.strip()]
    first20 = lines_nz[0][:20] if lines_nz else ""
    last20 = lines_nz[-1][-20:] if lines_nz else ""
    return {
        "file": path,
        "chars": chars,
        "paras": len(paras),
        "sents": len(sents),
        "len_dist": dist,
        "max_streak": max_streak,
        "streak_sents": streak_sents,
        "short5": dist["<=5"],
        "long50": dist[">=50"],
        "max_single_para_run": max_single_para_run,
        "dashes": dashes,
        "dash_per_100": round(dashes * 100 / max(chars, 1), 3),
        "ascii_punct": ascii_punct,
        "not_but": not_but,
        "first20": first20,
        "last20": last20,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python analyze_metrics.py <文件路径> [更多...]", file=sys.stderr)
        sys.exit(1)
    results = [metrics(p) for p in sys.argv[1:]]
    print(json.dumps(results, ensure_ascii=False, indent=2))
