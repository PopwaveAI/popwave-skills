# -*- coding: utf-8 -*-
"""把三轮改写的结果从 JSON 里抽成可直接读的正文文件。

- 修正官 → 按"引文→改法"逐条替换原稿，产出 一级·逐句修 后的整章
- 段落改写官 → 取"重写"字段，产出 二级·段落改写 的那一段
- 重构官 → 取"重写正文"字段，产出 三级·大重构 后的整章

替换是机械的：引文在原文里找不到就跳过并记一笔，最后打印命中数，不静默。
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
SK = Path(r"d:\popwave-skills\新流程探索\网文编辑")
OUT = SK / "scripts" / "输出" / "第改写轮"
DST = SK / "scripts" / "改写"
DST.mkdir(parents=True, exist_ok=True)

manifest = {}
for line in (SK / "素材" / "manifest.jsonl").read_text(encoding="utf-8").splitlines():
    if line.strip():
        r = json.loads(line)
        manifest[r["id"]] = r

for p in sorted(OUT.glob("*.json")):
    tag = p.stem
    rec = json.loads(p.read_text(encoding="utf-8"))
    d = rec.get("json") or {}
    if tag.endswith("__修正官"):
        rid = tag[:-len("__修正官")]
        src = (SK / manifest[rid]["路径"]).read_text(encoding="utf-8")
        text, ok, miss = src, 0, []
        for x in d.get("逐句问题") or []:
            quote, fix = (x.get("引文") or "").strip(), (x.get("改法") or "").strip()
            if not quote or not fix:
                continue
            if quote in text:
                text = text.replace(quote, fix, 1)
                ok += 1
            else:
                miss.append("%s行%s %s" % (rid, x.get("行"), quote[:18]))
        (DST / ("%s__一级逐句修.md" % rid)).write_text(text, encoding="utf-8")
        print("  %-20s 一级逐句修：替换 %d 条，未命中 %d 条" % (rid, ok, len(miss)))
        for m in miss:
            print("      未命中 %s" % m)
    elif tag.endswith("__段落改写"):
        rid = tag[:-len("__段落改写")]
        body = d.get("重写") or ""
        (DST / ("%s__二级段落改写.md" % rid)).write_text(body.strip() + "\n", encoding="utf-8")
        print("  %-20s 二级段落改写：%d 字  ｜ 原段问题：%s" % (rid, len(body), str(d.get("原文问题"))[:46]))
    elif tag.endswith("__重构"):
        rid = tag[:-len("__重构")]
        body = d.get("重写正文") or ""
        (DST / ("%s__三级重构.md" % rid)).write_text(body.strip() + "\n", encoding="utf-8")
        print("  %-20s 三级重构：%d 字  ｜ 重排：%s" % (rid, len(body), str(d.get("重排说明"))[:46]))

print("\n改写稿落盘 → %s" % DST)
