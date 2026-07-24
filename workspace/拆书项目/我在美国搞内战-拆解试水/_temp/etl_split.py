#!/usr/bin/env python3
"""ETL: Split first 74 chapters from the source TXT into individual files."""
import re, os, json

SRC = r'D:\workspace\下载书籍\我在美国搞内战.txt'
OUT = r'D:\workspace\拆书项目\我在美国搞内战-拆解试水'
LIMIT = 74

with open(SRC, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all # 第X章 header lines
ch_pattern = re.compile(r'^# 第(\d+)章\s+(.*)')

chapters = []
for i, line in enumerate(lines):
    m = ch_pattern.match(line)
    if m:
        ch_num = int(m.group(1))
        ch_title = m.group(2).strip()
        chapters.append((ch_num, ch_title, i))

print(f'Total # 第X章 headers: {len(chapters)}')
print(f'First: ch{chapters[0][0]} - {chapters[0][1]}')
print(f'Last: ch{chapters[-1][0]} - {chapters[-1][1]}')

# Filter for first 74
target_chapters = [c for c in chapters if c[0] <= LIMIT]
print(f'\nProcessing first {len(target_chapters)} chapters...')

metadata = {
    'source_file': '我在美国搞内战.txt',
    'source_path': SRC,
    'total_chapters': len(target_chapters),
    'chapters': []
}

for idx, (ch_num, ch_title, start_line) in enumerate(target_chapters):
    # Determine end: next chapter's start, or end of file
    if idx + 1 < len(target_chapters):
        end_line = target_chapters[idx + 1][2]
    else:
        end_line = len(lines)
    
    # Chapter content (include header line and everything between)
    ch_content = ''.join(lines[start_line:end_line]).strip()
    
    # Write chapter file
    fname = f'_temp/chapters/ch{ch_num:03d}.txt'
    fpath = os.path.join(OUT, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(ch_content)
    
    metadata['chapters'].append({
        'num': ch_num,
        'title': ch_title,
        'file': fname,
        'lines': end_line - start_line,
        'chars': len(ch_content)
    })

# Write metadata
meta_path = os.path.join(OUT, '_temp', 'metadata.json')
with open(meta_path, 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

# Verify
ch_files = sorted(os.listdir(os.path.join(OUT, '_temp', 'chapters')))
print(f'\nFiles written: {len(ch_files)}')
print(f'First: {ch_files[0]}')
print(f'Last: {ch_files[-1]}')
total_chars = sum(c['chars'] for c in metadata['chapters'])
print(f'Total chars: {total_chars:,}')
print(f'Avg chars/chapter: {total_chars // len(target_chapters):,}')
print('\nDone!')
