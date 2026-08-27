# -*- coding: utf-8 -*-
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = r"d:\popwave-skills\library\知名小说wiki\超维度玩家\_temp\batches\src"

def split_by_index(src, groups):
    # groups: list of (out_name, block_count) in order
    raw = io.open(base + "\\" + src, encoding="utf-8").read().splitlines()
    blocks = []
    cur = None
    for ln in raw:
        m = re.match(r"^#\s*(第[0-9一二三四五六七八九十百千]+章.*)", ln)
        if m:
            cur = [m.group(1).strip(), []]
            blocks.append(cur)
        elif cur is not None:
            cur[1].append(ln)
    i = 0
    for out_name, cnt in groups:
        picked = blocks[i:i+cnt]
        i += cnt
        with io.open(base + "\\" + out_name, "w", encoding="utf-8") as f:
            f.write("\n\n".join("# " + t + "\n" + "\n".join(b) for t, b in picked))
        print("wrote", out_name, "blocks=", len(picked), "first=", picked[0][0], "last=", picked[-1][0])

split_by_index("V5_B3_ch065-096.txt", [
    ("V5_B3a_ch065-080.txt", 16),
    ("V5_B3b_ch081-096.txt", 16),
])
split_by_index("V5_B4_ch097-128.txt", [
    ("V5_B4a_ch097-112.txt", 16),
    ("V5_B4b_ch113-129.txt", 17),
])
print("done")