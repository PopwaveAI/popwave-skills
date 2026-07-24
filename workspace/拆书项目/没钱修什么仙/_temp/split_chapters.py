#!/usr/bin/env python3
"""Split the TXT file into individual chapter files for Volume 1 (ch1-250)."""

import re
import os
import json

SRC = r"D:\workspace\没钱修什么仙\没钱修什么仙-1-500章.txt"
OUT_DIR = r"D:\workspace\没钱修什么仙\_temp\chapters"
MAX_CH = 250

os.makedirs(OUT_DIR, exist_ok=True)

with open(SRC, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

ch_pattern = re.compile(r'^第(\d+)章\s*(.*)')
chapters = []
current_ch = None
current_lines = []

for i, line in enumerate(lines):
    stripped = line.strip()
    m = ch_pattern.match(stripped)
    if m:
        if current_ch is not None:
            chapters.append({
                'num': current_ch['num'],
                'title': current_ch['title'],
                'content': '\n'.join(current_lines),
                'line_start': current_ch['line_start'],
                'line_end': i
            })
        ch_num = int(m.group(1))
        if ch_num > MAX_CH:
            break
        ch_title = m.group(2).strip()
        current_ch = {'num': ch_num, 'title': ch_title, 'line_start': i}
        current_lines = [line]
    elif current_ch is not None:
        current_lines.append(line)

# Save last chapter
if current_ch is not None and current_ch['num'] <= MAX_CH:
    chapters.append({
        'num': current_ch['num'],
        'title': current_ch['title'],
        'content': '\n'.join(current_lines),
        'line_start': current_ch['line_start'],
        'line_end': len(lines)
    })

print(f"Total chapters in Volume 1 (1-{MAX_CH}): {len(chapters)}")
print(f"Range: ch{chapters[0]['num']:03d} - ch{chapters[-1]['num']:03d}")

# Calculate metadata
total_chars = 0
volumes = [{"name": "第一卷", "start_ch": 1, "end_ch": MAX_CH, "chapters": MAX_CH}]
ch_meta = []

for ch in chapters:
    fname = f"ch{ch['num']:03d}.txt"
    out_path = os.path.join(OUT_DIR, fname)
    chars = len(ch['content'])
    total_chars += chars
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(ch['content'])
    
    ch_meta.append({
        "num": ch['num'],
        "original_num": str(ch['num']),
        "title": ch['title'],
        "chars": chars
    })
    print(f"  Written {fname} ({chars} chars) - {ch['title'][:40]}")

# Also save full text
full_text_path = r"D:\workspace\没钱修什么仙\_temp\full_text.txt"
with open(full_text_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join([ch['content'] for ch in chapters]))

print(f"\nTotal chars: {total_chars}")
print(f"File count: {len(chapters)}")

metadata = {
    "source_book": "没钱修什么仙？",
    "author": "熊狼狗",
    "chapter_count": len(chapters),
    "volume_count": 1,
    "volumes": volumes,
    "chapters": ch_meta,
    "total_chars": total_chars
}

meta_path = r"D:\workspace\没钱修什么仙\_temp\metadata.json"
with open(meta_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print(f"\nMetadata written to {meta_path}")
print("Done!")
