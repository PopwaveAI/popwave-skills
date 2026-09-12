# -*- coding: utf-8 -*-
"""收卷：只做三件事。①汇总可核栏 ②定位分歧 ③出判决书骨架。

禁止：改评委结论、调和分歧、加总结感想。
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SK = Path(r"d:\popwave-skills\新流程探索\网文编辑")


def load(out_dir):
    data = defaultdict(dict)
    for p in sorted(out_dir.glob("*.json")):
        if p.stem == "排序官":
            continue
        code, _, role = p.stem.partition("__")
        d = json.loads(p.read_text(encoding="utf-8"))
        data[code][role] = d
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--round", default="1")
    args = ap.parse_args()
    out_dir = SK / "scripts" / "输出" / ("第%s轮" % args.round)
    rec_dir = SK / "迭代记录" / ("第%s轮" % args.round)
    rec_dir.mkdir(parents=True, exist_ok=True)
    data = load(out_dir)

    # ① 可核栏：按红线编号归并
    hits, no_red = Counter(), []
    for code, roles in data.items():
        ed = (roles.get("编辑") or {}).get("json") or {}
        for it in ed.get("逐句问题", []):
            red = (it.get("红线") or "").strip()
            if red:
                hits[red] += 1
            else:
                no_red.append((code, it.get("行"), it.get("引文"), it.get("问题")))
    lines = ["# 可核栏 · 第%s轮\n" % args.round,
             "> 这一栏不用作者看。每条都带行号与原文，可直接回原文核。\n",
             "## 命中红线统计\n"]
    if hits:
        for red, n in hits.most_common():
            lines.append("- %s：%d 次" % (red, n))
    else:
        lines.append("- 本轮没有命中红线的条目")
    lines.append("\n## 未挂红线的逐句问题（%d 条，需人工过一眼）\n" % len(no_red))
    for code, ln, quote, kind in no_red:
        lines.append("- %s 行%s「%s」：%s" % (code, ln, quote, kind))
    (rec_dir / "可核栏.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ② 争议栏：三方差 vs 单方
    disp = ["# 争议栏 · 第%s轮\n" % args.round,
            "> 三方都说坏的不必交作者；**只有一方说坏的，才是作者要看的地方**。\n"]
    for code, roles in sorted(data.items()):
        rd = (roles.get("读者") or {}).get("json") or {}
        ed = (roles.get("编辑") or {}).get("json") or {}
        op = (roles.get("对手") or {}).get("json") or {}
        disp.append("\n## %s\n" % code)
        disp.append("- 读者：%s（%s）" % (rd.get("还想不想看下一章", "未答"), rd.get("理由", "")))
        disp.append("- 读者出戏处：%s" % (rd.get("读到哪里出戏") or "无"))
        disp.append("- 编辑最严重三处：%s" % (ed.get("最严重的三处") or "无"))
        disp.append("- 对手最经不起追问：%s" % (op.get("最经不起追问的一处") or "无"))
        only_one = (bool(rd.get("读到哪里出戏")) + bool(ed.get("最严重的三处")) + bool(op.get("最经不起追问的一处"))) == 1
        disp.append("- 判读：%s" % ("**单方指出，交作者判**" if only_one else "多方指向，按可核栏处理"))
    (rec_dir / "争议栏.md").write_text("\n".join(disp) + "\n", encoding="utf-8")

    # ③ 判决书骨架
    rank = out_dir / "排序官.json"
    rk = json.loads(rank.read_text(encoding="utf-8")).get("json") if rank.exists() else None
    jd = ["# 判决书 · 第%s轮\n" % args.round, "## 一、排序（三维各自独立）\n"]
    if rk:
        for k in ("文笔质感", "内容剧情", "情绪节奏"):
            jd.append("- %s：%s" % (k, " > ".join(rk.get(k) or [])))
        jd.append("\n- 两维相反的稿：%s" % rk.get("两维相反的稿"))
        jd.append("- 最稳 / 最差：%s / %s" % (rk.get("最稳的一稿"), rk.get("最差的一稿")))
    else:
        jd.append("- 未跑排序官")
    jd.append("\n## 二、可核栏")
    jd.append("见同目录 `可核栏.md`。作者只需看统计：命中几条、集中在哪几条红线。")
    jd.append("\n## 三、要作者判的（一稿最多三条）")
    jd.append("见同目录 `争议栏.md`，已筛出只由一方指出的条目。")
    jd.append("\n## 四、抽检记录")
    jd.append("每批抽 1 稿读完整正文核对行号；抽 3 条可核栏结论回原文核。**未抽检即视为本轮结论不可用。**")
    (rec_dir / ("判决书-第%s轮.md" % args.round)).write_text("\n".join(jd) + "\n", encoding="utf-8")

    print("可核栏：命中红线 %d 类，未挂红线 %d 条" % (len(hits), len(no_red)))
    print("争议栏与判决书已写入 %s" % rec_dir)


if __name__ == "__main__":
    main()
