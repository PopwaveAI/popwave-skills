# -*- coding: utf-8 -*-
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r"d:\popwave-skills\library\知名小说wiki\超维度玩家\_temp\batches\src"
for name in ["V5_B3_ch065-096","V5_B4_ch097-128","V5_B5_ch129-136"]:
    p = base + "\\" + name + ".txt"
    print("##### "+name+" #####")
    lines = io.open(p, encoding="utf-8").read().splitlines()
    for ln in lines:
        m = re.match(r"^#\s*(第[0-9一二三四五六七八九十百千]+章.*)", ln)
        if m:
            print(m.group(1))