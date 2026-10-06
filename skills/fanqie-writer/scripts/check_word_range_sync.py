#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_word_range_sync.py — 「单章字数」两条真源的一致性校验器

━━━ 它判什么 ━━━

同一份口径现在有两个落点，缺校验器就会各走各的：

  ① 人读版：`references/fanqie-platform-facts.md` 的「四·补、单章字数」（表格）
  ② 机器版：`scripts/word-range.json`（脚本读它）

本脚本逐项比对两边的**每一个数**：题材分档表、官方上下限、默认区间、算法三条边界、
黄金三章两种口径。**任意一处对不上就报 FAIL 并以退出码 1 结束。**

⚠️ 判据方向要说清：本脚本判的是「**两边是否一致**」，不是「json 是否等于某个基准」——
**两边一起改、改成同样值 = OK**；只有一边动过才报 FAIL。

━━━ 污染测试（自带）━━━

    python scripts/check_word_range_sync.py --selftest

拿"改歪了的 json"喂进来必须被拦下（5 组用例），同时拿原版必须 0 FAIL——
**证明校验器有区分度**，而不是"跑起来没报错"。

━━━ 用法 ━━━

    python scripts/check_word_range_sync.py            # 比对 + 报结果
    python scripts/check_word_range_sync.py --quiet     # 只出结论行
"""

import argparse
import copy
import io
import json
import os
import re
import sys

if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
TABLE = os.path.join(HERE, "word-range.json")
FACTS = os.path.join(SKILL, "references", "fanqie-platform-facts.md")

SECTION_RE = re.compile(r"^##\s*四·补、单章字数(.*?)(?=^##\s|\Z)", re.S | re.M)


# ─────────────────────────── 解析 md 侧 ───────────────────────────
def md_section(md_text):
    m = SECTION_RE.search(md_text)
    return m.group(0) if m else ""


def md_genre_rows(sec):
    """取「题材分档」表里的 (名字, min, max)；通用区间单独返回"""
    rows, common = [], None
    grab = False
    for line in sec.splitlines():
        if "题材分档" in line:
            grab = True
            continue
        if grab and line.strip().startswith("**") and "题材分档" not in line:
            grab = False  # 下一个加粗小标题＝表结束了
        if not grab or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        name = re.sub(r"[*`]", "", cells[0]).strip()
        if name in ("题材", "") or set(name) <= set("-: "):
            continue
        m = re.search(r"(\d+)\s*-\s*(\d+)", re.sub(r"[*`]", "", cells[1]))
        if not m:
            continue
        pair = (int(m.group(1)), int(m.group(2)))
        if "通用" in name:
            common = pair
        else:
            for token in re.split(r"[/、,，]", name):
                token = token.strip()
                if token:
                    rows.append((token, pair))
    return rows, common


def md_scalars(sec):
    """取散落在正文里的单值口径"""
    def one(pat, label):
        m = re.search(pat, sec)
        return int(m.group(1)) if m else None

    out = {
        "官方下限": one(r"最少\s*\*{0,2}(\d+)\s*字", "min"),
        "官方上限": one(r"最多\s*\*{0,2}(\d+)\s*字", "max"),
        "算法边界·稀疏下限": one(r"单章\s*\*{0,2}<\s*(\d+)\s*字", "sparse"),
        "算法边界·广告上限": one(r"单章\s*\*{0,2}>\s*(\d+)\s*字", "ads"),
        "算法边界·连三章下限": one(r"连续\s*3\s*章总字数\s*\*{0,2}<\s*(\d+)\s*字", "three"),
        "黄金三章·建议下限": one(r"建议\s*(\d+)\s*字以上", "g3"),
    }
    m = re.search(r"默认的\s*(\d+)\s*-\s*(\d+)\s*是通用保守值", sec)
    out["默认区间"] = (int(m.group(1)), int(m.group(2))) if m else None
    m = re.search(r"首秀期保持\s*\*{0,2}(\d+)\s*-\s*(\d+)", sec)
    out["黄金三章·稳定区间"] = (int(m.group(1)), int(m.group(2))) if m else None
    # 注意：这一节里还有一处 "2000→4000→1500"（讲「忌忽长忽短」的反例），
    # 故必须锚在「递减结构」上，否则会抓错串（首跑实测踩到）。
    m = re.search(r"递减结构」?\s*(\d+)\s*→\s*(\d+)\s*→\s*(\d+)", sec)
    out["黄金三章·递减序列"] = tuple(int(x) for x in m.groups()) if m else None
    return out


# ─────────────────────────── 比对 ───────────────────────────
def compare(cfg, md_text):
    """返回 rows: (项目, 状态 OK/FAIL/MISS, 详情)"""
    sec = md_section(md_text)
    rows = []
    if not sec:
        return [("整节", "FAIL", "在 facts 里找不到「## 四·补、单章字数」这一节")]

    sc = md_scalars(sec)
    genres = cfg.get("genres") or {}

    def pair(name, md_pair, key, sub=""):
        v = cfg
        for k in key.split("."):
            v = (v or {}).get(k) if isinstance(v, dict) else None
        if md_pair is None:
            rows.append((name, "MISS", "md 侧没解析到该数值（可能改了措辞）"))
            return
        if not isinstance(v, dict) or "min" not in v:
            rows.append((name, "FAIL", "json 侧缺 %s（md＝%s）" % (key, md_pair)))
            return
        jv = (int(v["min"]), int(v["max"]))
        rows.append((name, "OK" if jv == md_pair else "FAIL",
                     "md=%d-%d ／ json=%d-%d" % (md_pair[0], md_pair[1], jv[0], jv[1])))

    # ① 官方上下限
    for name, key in (("官方下限", "official.min"), ("官方上限", "official.max")):
        md_v = sc.get(name)
        v = cfg.get("official") or {}
        jv = v.get("min") if name.endswith("下限") else v.get("max")
        if md_v is None:
            rows.append((name, "MISS", "md 侧没解析到"))
        else:
            rows.append((name, "OK" if md_v == jv else "FAIL",
                         "md=%s ／ json=%s" % (md_v, jv)))

    # ② 默认区间
    pair("默认区间", sc.get("默认区间"), "default")

    # ③ 题材分档表
    g_rows, common = md_genre_rows(sec)
    for name, md_pair in g_rows:
        hit = name if name in genres else None
        if hit is None:
            for k in genres:
                if k and (name in k or k in name):
                    hit = k
                    break
        if hit is None:
            rows.append(("题材·%s" % name, "FAIL", "json 里没有这个题材（md=%d-%d）" % md_pair))
            continue
        jv = (int(genres[hit]["min"]), int(genres[hit]["max"]))
        rows.append(("题材·%s" % name, "OK" if jv == md_pair else "FAIL",
                     "md=%d-%d ／ json=%d-%d" % (md_pair[0], md_pair[1], jv[0], jv[1])))

    # ④ 读者偏好区间（md 的「通用区间」行）
    pair("读者偏好区间", common, "reader_preferred")

    # ⑤ 算法三条边界
    edges = cfg.get("algorithm_edges") or {}
    for name, jkey in (("算法边界·稀疏下限", "sparse_below"),
                       ("算法边界·广告上限", "ad_break_above"),
                       ("算法边界·连三章下限", "three_chapter_sparse_below")):
        md_v, jv = sc.get(name), edges.get(jkey)
        if md_v is None:
            rows.append((name, "MISS", "md 侧没解析到"))
        else:
            rows.append((name, "OK" if md_v == jv else "FAIL",
                         "md=%s ／ json=%s" % (md_v, jv)))

    # ⑥ 黄金三章
    g3 = cfg.get("golden3") or {}
    md_v = sc.get("黄金三章·建议下限")
    rows.append(("黄金三章·建议下限", "OK" if md_v == g3.get("suggest_min") else "FAIL",
                 "md=%s ／ json=%s" % (md_v, g3.get("suggest_min"))))
    pair("黄金三章·稳定区间", sc.get("黄金三章·稳定区间"), "golden3.stable")
    md_seq = sc.get("黄金三章·递减序列")
    j_seq = tuple((g3.get("descending") or {}).get("seq") or [])
    rows.append(("黄金三章·递减序列", "OK" if md_seq == j_seq else "FAIL",
                 "md=%s ／ json=%s" % ("→".join(map(str, md_seq or [])) or "未解析",
                                        "→".join(map(str, j_seq)) or "缺")))
    return rows


# ─────────────────────────── 主流程 ───────────────────────────
def load():
    with io.open(TABLE, encoding="utf-8") as fh:
        cfg = json.load(fh)
    with io.open(FACTS, encoding="utf-8") as fh:
        md = fh.read()
    return cfg, md


def report(rows, quiet=False):
    bad = [r for r in rows if r[1] != "OK"]
    if not quiet:
        print("=" * 66)
        print("单章字数 · 两条真源一致性校验")
        print("  human : %s" % os.path.relpath(FACTS, SKILL))
        print("  machine: %s" % os.path.relpath(TABLE, SKILL))
        print("=" * 66)
        for name, status, detail in rows:
            mark = "[OK]  " if status == "OK" else "[X]   "
            print("%s%-22s %s" % (mark, name, detail))
        print("-" * 66)
    if bad:
        print("[X] %d 处不一致：" % len(bad))
        for name, status, detail in bad:
            print("    - %s：%s" % (name, detail))
        print("\n修法：以 facts 的表格为准同步 word-range.json（或反之），两边改成同一个数后重跑。")
        return 1
    print("[OK] 全部一致（共 %d 项）。" % len(rows))
    return 0


def selftest(cfg, md):
    """污染测试：改歪的 json 必须被拦下；原版必须 0 FAIL"""
    cases = []

    def mut(fn, label):
        c = copy.deepcopy(cfg)
        fn(c)
        cases.append((label, c))

    mut(lambda c: c["genres"]["悬疑推理"].__setitem__("max", 3600), "题材·悬疑推理 max 3500→3600")
    mut(lambda c: c["default"].__setitem__("min", 2100), "默认区间 min 2200→2100")
    mut(lambda c: c["algorithm_edges"].__setitem__("sparse_below", 1600), "算法稀疏下限 1500→1600")
    mut(lambda c: c["golden3"]["descending"].__setitem__("seq", [2500, 2100, 1500]),
        "黄金三章递减序列 2000→2100")
    mut(lambda c: c["genres"].pop("都市言情"), "删掉题材·都市言情")
    mut(lambda c: c["official"].__setitem__("max", 5000), "官方上限 50000→5000")

    print("=" * 66)
    print("污染测试（校验器自身有没有区分度）")
    print("=" * 66)

    ok_all = True
    base = [r for r in compare(cfg, md) if r[1] != "OK"]
    if base:
        ok_all = False
        print("[X]   基准（原版 json）本该 0 FAIL，却报了 %d 处：" % len(base))
        for n, s, d in base:
            print("      - %s：%s" % (n, d))
    else:
        print("[OK]  基准：原版 json 无 FAIL（不会误伤）")

    for label, c in cases:
        bad = [r for r in compare(c, md) if r[1] != "OK"]
        if bad:
            print("[OK]  拦下：%s（报 %d 处）" % (label, len(bad)))
        else:
            ok_all = False
            print("[X]   漏过：%s（本该报 FAIL）" % label)

    print("-" * 66)
    print("[%s] 污染测试%s" % ("OK" if ok_all else "X",
                              "通过：改歪必被拦下、原版不被误伤" if ok_all else "未通过"))
    return 0 if ok_all else 1


def main():
    ap = argparse.ArgumentParser(description="单章字数两条真源一致性校验器")
    ap.add_argument("--quiet", action="store_true", help="只出结论行")
    ap.add_argument("--selftest", action="store_true", help="污染测试自证（改歪的 json 必须被拦下）")
    args = ap.parse_args()

    if not os.path.isfile(TABLE):
        print("[X] 找不到 %s" % TABLE)
        return 2
    if not os.path.isfile(FACTS):
        print("[X] 找不到 %s" % FACTS)
        return 2

    cfg, md = load()
    if args.selftest:
        return selftest(cfg, md)
    return report(compare(cfg, md), quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
