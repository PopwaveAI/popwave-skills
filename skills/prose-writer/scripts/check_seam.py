#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_seam.py — 接缝检查：续文与前文**接得顺不顺**

━━━ 为什么需要它（2026-10-09 新增）━━━

「接续模式」的质量判据是**接缝测试五问**（见 `references/continuation-guide.md` 第六节）。
其中两问是**可机械化的**，不做成脚本就会退化成"凭感觉看一眼"：

    缝1 · 语气跳不跳    → 两侧跑同一把尺子（复用 `chapter_stats.analyze`），比**三项**画像
                          （均段长／均句长／短句率）。**对白占比只报数不判**——它随场景性质变，
                          且 benchmark 已证其 0–94% 不可分（见 RATIO_METRICS 注释）。
    缝5 · 有没有复述感  → 续文首段与前文的重叠度（字符 2-gram containment）

其余三问（视角人称时态 / 称呼用语 / 未完成项接住没有）**语义判定，脚本不碰**——
本脚本只做确定性部分，**不许把"脚本全绿"当成"接缝没问题"**。

━━━ 用法 ━━━

    python check_seam.py 前文.md 续文.md          # 全跑
    python check_seam.py 前文.md 续文.md --quiet  # 只输出告警行

退出码：0 ＝ 无告警；1 ＝ 有跳档或复述嫌疑。
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from chapter_stats import analyze as cs_analyze, extract_body as cs_extract
except Exception:  # pragma: no cover
    cs_analyze = cs_extract = None

# ── 判定阈值 ────────────────────────────────────────────────
JUMP_RATIO = 2.0      # 画像任一"倍数项"达到 2 倍即判跳档（沿用 benchmark-writing 的"跳档一倍"口径）
REPEAT_RATIO = 0.45   # 续文首段与前文某段 2-gram 重叠达 45% 即判复述嫌疑
OVERALL_REPEAT = 0.60 # 续文全文与前文全文的重叠（防大段搬运）

# 参与"倍数判定"的三项（碎句链/短对白链只报数，不判定——沿用风格层纪律）
#
# ⚠️ **对白行占比为何不在判定项里（2026-10-09 实测降级）**
#   首版把它当第四项倍数判据，实测立刻误伤：以基准样本 ch001 做截断续写，
#   半截稿（湖边等待，有对话）对白占比 25%，续文（屋内独处，无人可对话）0% —— 判"跳档"。
#   但**原文后半（标准答案）本身也只有 7.1%**：场景性质变了（相遇→独处），对白自然消失。
#   且 `references/benchmark-writing.md` 早有结论：**对白占比在 8 本正例里 0–94%、跨度 94 倍、"不可分"**。
#   → 拿它判跳档，就是判据违反了自己文件里的既有结论。**降级为只报数**（门禁校准：误伤即拆级）。
RATIO_METRICS = [
    ("均段长", "avg_para", "字/段"),
    ("均句长", "avg_sent", "字/句"),
    ("短句率", "short_ratio", "%"),
]
# 只报数、不判定的参考项
REPORT_ONLY = [
    ("对白行占比", "dlg_line_ratio", "%"),
    ("最长碎句链", "short_run", "句"),
    ("最长短对白链", "short_dlg_run", "行"),
]


def cn_only(text):
    return re.sub(r"[^\u4e00-\u9fff]", "", text or "")


def load_body(path):
    """取正文段（去标题行与空行），返回 list[str]——复用 chapter_stats 的正文切分口径"""
    if cs_extract is not None:
        try:
            body, _src = cs_extract(Path(path))
            # ⚠️ 必须再过一遍标题过滤：extract_body 在 'txt-whole' / 'md-title' 分支
            #    会把章节标题行一起返回，不过滤就会把标题当成"续文首段"，
            #    复述检测（缝5）永远命中不到真正的首段。污染测试 2026-10-09 抓到。
            rows = [l.strip() for l in body.split("\n")
                    if l.strip() and not l.strip().startswith("#")]
            if rows:
                return rows
        except Exception:
            pass
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            out.append(s)
    return out


def profile(path):
    """跑同一把尺子取画像；均段长由 total/paras 推出"""
    if cs_analyze is None:
        return None
    try:
        r = cs_analyze(Path(path))
    except Exception:
        return None
    if not isinstance(r, dict):
        return None
    out = dict(r)
    if out.get("paras") and out.get("total"):
        out["avg_para"] = out["total"] / out["paras"]
    return out


def pct(v):
    try:
        return float(v) * 100.0
    except (TypeError, ValueError):
        return 0.0


def check_profile(p_path, c_path):
    """① 语气跳不跳：两侧画像逐项比 → (rows, warns, err)"""
    a, b = profile(p_path), profile(c_path)
    if not a or not b:
        return [], [], "（画像不可用：chapter_stats 未就绪）"
    rows, warns = [], []
    for label, key, unit in RATIO_METRICS:
        va, vb = a.get(key), b.get(key)
        if va is None or vb is None:
            continue
        if unit == "%":
            sa, sb = "%.1f%%" % pct(va), "%.1f%%" % pct(vb)
            na, nb = pct(va), pct(vb)
        else:
            sa, sb = "%.1f" % va, "%.1f" % vb
            na, nb = float(va), float(vb)
        lo, hi = min(na, nb), max(na, nb)
        ratio = (hi / lo) if lo > 0 else (float("inf") if hi > 0 else 1.0)
        if lo == 0 and hi == 0:
            verdict = "OK"
        elif ratio >= JUMP_RATIO:
            verdict = "跳档?"
            warns.append("缝1 %s：前文 %s vs 续文 %s（差 %.1f 倍）——续文去贴前文，不是改前文"
                         % (label, sa, sb, ratio))
        else:
            verdict = "OK"
        rows.append((label, sa, sb, ("%.1f×" % ratio) if ratio != float("inf") else "∞", verdict))
    # 参考项（对白占比 / 碎句链 / 短对白链）：**只报数、不判定**
    for label, key, unit in REPORT_ONLY:
        va, vb = a.get(key), b.get(key)
        if va is None or vb is None:
            continue
        if unit == "%":
            sa, sb = "%.1f%%" % pct(va), "%.1f%%" % pct(vb)
        else:
            sa, sb = str(va), str(vb)
        rows.append((label + "（只报数）", sa, sb, "-", "INFO"))
    return rows, warns, None


def grams(text, n=2):
    t = cn_only(text)
    return set(t[i:i + n] for i in range(max(0, len(t) - n + 1)))


def containment(small, big):
    """small 被 big 覆盖的比例"""
    if not small:
        return 0.0
    return len(small & big) / float(len(small))


def check_repeat(p_path, c_path):
    """⑤ 有没有复述感：续文首段/全文 与前文的重叠"""
    prev = load_body(p_path)
    cur = load_body(c_path)
    if not prev or not cur:
        return [], []
    p_all = grams("".join(prev))
    warns, rows = [], []

    # 续文首段（前 2 段）逐个比
    for idx, para in enumerate(cur[:2], 1):
        g = grams(para)
        best, best_i = 0.0, -1
        for j, pp in enumerate(prev, 1):
            c = containment(g, grams(pp))
            if c > best:
                best, best_i = c, j
        rows.append(("续文第 %d 段 vs 前文" % idx,
                     "最高重叠 %.0f%%（前文第 %d 段）" % (best * 100, best_i),
                     "复述?" if best >= REPEAT_RATIO else "OK"))
        if best >= REPEAT_RATIO:
            warns.append("缝5 续文第 %d 段与前文第 %d 段重叠 %.0f%%——疑似复述，做删减测试后删或改写"
                         % (idx, best_i, best * 100))

    # 续文全文 vs 前文全文
    c_all = grams("".join(cur))
    ov = containment(c_all, p_all)
    rows.append(("续文全文 vs 前文全文", "重叠 %.0f%%" % (ov * 100),
                 "复述?" if ov >= OVERALL_REPEAT else "OK"))
    if ov >= OVERALL_REPEAT:
        warns.append("缝5 续文全文与前文重叠 %.0f%%——大段复述，回第三步查禁令①" % (ov * 100))
    return rows, warns


def check_naming(p_path, c_path):
    """③ 专名提示（**只提示，不判定**）：续文里出现、前文从未出现的短引语（可能是新称呼/新叫法）"""
    prev_txt, cur_txt = "", ""
    try:
        prev_txt = "\n".join(load_body(p_path))
        cur_txt = "\n".join(load_body(c_path))
    except Exception:
        return []
    quotes = re.findall(r"[“「]([^”」]{1,6})[”」]", cur_txt)
    prev_set = set(re.findall(r"[“「]([^”」]{1,6})[”」]", prev_txt))
    # 称呼候选：1-3 个汉字，且**整段引语不带句读**（带句读的多半是台词，不是称呼）
    fresh = [q for q in quotes
             if q not in prev_set
             and 1 <= len(cn_only(q)) <= 3
             and not re.search(r"[。？！，、…：；．]", q)]
    seen, uniq = set(), []
    for q in fresh:
        if q not in seen:
            seen.add(q)
            uniq.append(q)
    return uniq[:12]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv
    if len(args) < 2:
        print(__doc__)
        return 2
    p_path, c_path = args[0], args[1]
    for p in (p_path, c_path):
        if not os.path.exists(p):
            print("[X] 文件不存在：%s" % p)
            return 2

    warns = []
    if not quiet:
        print("=" * 62)
        print("接缝检查 · %s  →  %s" % (os.path.basename(p_path), os.path.basename(c_path)))
        print("=" * 62)
        print("本脚本只判**确定性**部分（缝1 语气／缝5 复述）。")
        print("缝2 视角人称时态／缝3 称呼用语／缝4 未完成项——语义判定，由模型逐条举证。")
        print()

    rows, w1, err = check_profile(p_path, c_path)
    warns += w1
    if not quiet:
        print("── ① 语气锚：两侧画像对照（缝1）" + ("  " + err if err else ""))
        print("   %-22s %10s %10s %8s  %s" % ("指标", "前文", "续文", "倍数", "判定"))
        for label, a, b, r, v in rows:
            print("   %-22s %10s %10s %8s  %s" % (label, a, b, r, v))
        print()

    r2, w2 = check_repeat(p_path, c_path)
    warns += w2
    if not quiet and r2:
        print("── ⑤ 复述检测（缝5）")
        for label, val, v in r2:
            print("   %-24s %-34s %s" % (label, val, v))
        print()

    names = check_naming(p_path, c_path)
    if not quiet and names:
        print("── ③ 称呼提示（**只提示，不判定**）：续文里出现、前文没有的短引语")
        print("   这些可能只是新台词，也可能是**换了叫法**。请搜前文确认同一人怎么叫。")
        print("   " + "／".join(names))
        print()

    if warns:
        print("⚠️ 告警 %d 条：" % len(warns))
        for w in warns:
            print("   - " + w)
        print()
        print("提醒：本脚本只覆盖缝1／缝5。**脚本全绿 ≠ 接缝没问题**——缝2/3/4 必须逐条举证。")
        return 1
    print("[OK] 缝1（语气画像）与缝5（复述检测）未发现告警。")
    print("     仍需逐条过 缝2 视角人称时态／缝3 称呼用语／缝4 未完成项。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
