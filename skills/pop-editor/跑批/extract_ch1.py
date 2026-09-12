# -*- coding: utf-8 -*-
"""抽三本书的第一章全文，作为 80-90 与 70 两档的整章锚，并追加进 manifest。"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(r"d:\popwave-skills")
SK = REPO / "新流程探索" / "网文编辑"
MAT = SK / "素材"
HAN = re.compile(r"[\u4e00-\u9fff]")
CH = re.compile(r"^#?\s*第(\d+)章[\s\u3000]*(.*)$")

JOBS = [
    ("满分80-90", "A-夜无疆-第1章", REPO / "参考小说txt" / "起点" / "玄幻仙侠" / "夜无疆-辰东.txt", "名家原文·夜无疆 第1章"),
    ("七十70", "A-凡骨-第1章", REPO / "参考小说txt" / "番茄" / "玄幻仙侠" / "凡骨-壹更大师.txt", "小爆款·凡骨 第1章"),
    ("七十70", "A-不死帝师-第1章", REPO / "参考小说txt" / "番茄" / "玄幻仙侠" / "不死帝师-一只榴莲3号.txt", "小爆款·不死帝师 第1章"),
]

new_recs = []
for gear, rid, src, note in JOBS:
    if not src.exists():
        print("!! 缺 %s" % src)
        continue
    (MAT / gear).mkdir(parents=True, exist_ok=True)
    lines = src.read_bytes()[: 4 * 1024 * 1024].decode("utf-8", "ignore").splitlines()
    body, started, ch_title = [], False, ""
    for raw in lines:
        s = raw.strip()
        m = CH.match(s)
        if m:
            n = int(m.group(1))
            if n == 1 and not started:
                started, ch_title = True, m.group(2)
                continue
            if n == 2:
                break
        if started and s and not s.startswith("#"):
            body.append(s)
    text = "\n\n".join(body)
    # 去掉章末作者感言
    for cut in ("正在手打中", "感谢各位书友", "《%s》" % src.stem.split("-")[0]):
        i = text.find(cut)
        if i > 0:
            text = text[:i].rstrip()
    out = MAT / gear / ("%s.md" % rid)
    out.write_text(text, encoding="utf-8")
    n = len(HAN.findall(text))
    new_recs.append({"id": rid, "档位": gear, "赛道": "玄幻-东方幻想", "场景": "整章",
                     "来源": "%s（%s）" % (note, ch_title), "路径": "素材/%s/%s.md" % (gear, rid),
                     "字数": n})
    print("  %-14s %-18s %d 字" % (gear, rid, n))

# 追加进 manifest
path = MAT / "manifest.jsonl"
recs = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
have = {r["id"] for r in recs}
recs.extend(r for r in new_recs if r["id"] not in have)
path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in recs) + "\n", encoding="utf-8")
print("\nmanifest 更新为 %d 条" % len(recs))
