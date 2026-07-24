"""Extract sampled chapters from 武林半侠传"""
import re
import os

SRC = r"D:\workspace\参考小说txt\武林半侠传.txt"
OUT = r"D:\workspace\写书项目\文风dna有效性测试\_temp\sampled_chapters"

with open(SRC, "r", encoding="utf-8") as f:
    text = f.read()

# Find all chapters
chapters = []
for m in re.finditer(r"^# (.+)$", text, re.M):
    title = m.group(1).strip()
    start = m.end()
    next_m = re.search(r"^# ", text[m.end():], re.M)
    end = m.end() + next_m.start() if next_m else len(text)
    content = text[start:end]
    ch_num = 0
    num_m = re.search(r"(\d+)", title)
    if num_m:
        ch_num = int(num_m.group(1))
    chapters.append((ch_num, title, len(content), content))

story_chs = [c for c in chapters if c[0] > 0]
total = len(story_chs)

# Sample 60 chapters evenly
step = max(1, total // 60)
sample = [story_chs[i] for i in range(0, total, step)]
sample.sort(key=lambda x: x[0])

os.makedirs(OUT, exist_ok=True)

total_chars = 0
total_lines = 0
for ch_num, title, cc, content in sample:
    safe_title = re.sub(r'[\\/:*?"<>|]', "", title[:40])
    fname = f"CH{ch_num:03d}-{safe_title}.txt"
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(content)
    total_chars += cc
    total_lines += content.count("\n")

print(f"Sampled {len(sample)} chapters, {total_lines} lines, {total_chars} chars")
print(f"Output: {OUT}")
for ch_num, title, cc, _ in sample:
    print(f"  CH{ch_num:03d} ({cc} chars): {title}")
