# -*- coding: utf-8 -*-
"""一次性迁移：把素材从旧四段目录（满分80-90／七十70）并到新三档目录（八十80／六十60／四十40）。

为什么：口径由"产源定档"改成"成绩定档"后，70 档不再是一格，番茄头部五本按成绩属 80 档。
合格边缘/ 与 不合格/ 两目录**不动**（改了会弄坏历轮 映射表-封存.json 的历史路径），
它们在新方案里是"改写对象池"，不是档位。

跑完必须接着跑 rebuild_manifest.py，并核对每档份数。
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
MAT = Path(r"d:\popwave-skills\新流程探索\网文编辑\素材")

MOVES = [
    ("满分80-90", "A-夜无疆-第1章", "八十80"),
    ("七十70", "A-凡骨-第1章", "八十80"),
    ("七十70", "A-不死帝师-第1章", "八十80"),
    ("七十70", "A-天渊-第1章", "八十80"),
    ("七十70", "A-系统赋我长生-第1章", "八十80"),
    ("七十70", "A-烟雨楼-第1章", "八十80"),
]

for src_gear, rid, dst_gear in MOVES:
    src = MAT / src_gear / ("%s.md" % rid)
    dst = MAT / dst_gear / ("%s.md" % rid)
    if not src.exists():
        print("  跳过（源不存在）%-28s %s" % (rid, src_gear))
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        print("  跳过（目标已存在）%s" % rid)
        continue
    shutil.move(str(src), str(dst))
    print("  迁移 %-28s %s → %s" % (rid, src_gear, dst_gear))

# 清掉搬空的旧目录
for gear in ("满分80-90", "七十70"):
    d = MAT / gear
    if d.exists():
        left = list(d.glob("*.md"))
        if left:
            print("  !! %s 还剩 %d 个文件，不删" % (gear, len(left)))
        else:
            d.rmdir()
            print("  删除空目录 %s" % gear)

print("\n当前素材目录：")
for d in sorted(MAT.iterdir()):
    if d.is_dir():
        print("  %-10s %d 份" % (d.name, len(list(d.glob('*.md')))))
