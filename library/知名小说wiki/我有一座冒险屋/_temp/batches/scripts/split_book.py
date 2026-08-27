# -*- coding: utf-8 -*-
import re, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r"D:\popwave-skills\参考小说txt\起点\悬疑灵异\我有一座冒险屋-我会修空调.txt"
BASE = r"d:\popwave-skills\library\知名小说wiki\我有一座冒险屋"
CHDIR = os.path.join(BASE, "_temp", "chapters")
SRCDIR = os.path.join(BASE, "_temp", "batches", "src")

txt = open(SRC, encoding="utf-8").read()
lines = txt.splitlines()

# 分章：每行片段匹配 "# 第N章 标题"
chap_pattern = re.compile(r"^#\s*(第[0-9一二三四五六七八九十百千]+章\s*\S.*?)$")
chapters = []  # (章标题行原文, 正文行列表)
cur = None
for ln in lines:
    m = chap_pattern.match(ln)
    if m:
        if cur is not None:
            chapters.append(cur)
        cur = [m.group(1).strip(), []]
    elif cur is not None:
        cur[1].append(ln)
if cur is not None:
    chapters.append(cur)

print("total chapters:", len(chapters))

# 写逐章文件
os.makedirs(CHDIR, exist_ok=True)
titles = []
for i, (title, body) in enumerate(chapters, start=1):
    num = f"ch{i:04d}"
    title_clean = re.sub(r"^第[0-9一二三四五六七八九十百千]+章\s*", "", title)
    titles.append(f"{num}\t{title_clean}")
    with io.open(os.path.join(CHDIR, num + ".txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(body).strip())
with io.open(os.path.join(CHDIR, "_chapter_titles.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(titles))

print("wrote", len(titles), "chapter files")

# 生成批次 src（30章/批）
BATCH = 30
os.makedirs(SRCDIR, exist_ok=True)
n = len(chapters)
nb = (n + BATCH - 1) // BATCH
for b in range(nb):
    s = b * BATCH
    e = min(s + BATCH, n)
    c1 = chapters[s][0]
    c2 = chapters[e-1][0]
    def chnum(tt):
        mm = re.search(r"第([0-9]+)章", tt)
        return int(mm.group(1)) if mm else 0
    fn = f"V1_B{b+1}_ch{chnum(c1):03d}-{chnum(c2):03d}.txt"
    with io.open(os.path.join(SRCDIR, fn), "w", encoding="utf-8") as f:
        for (title, body) in chapters[s:e]:
            f.write("# " + title + "\n" + "\n".join(body) + "\n\n")
    print("batch", b+1, fn, "chapters", chnum(c1), "-", chnum(c2), "chunks", e-s)