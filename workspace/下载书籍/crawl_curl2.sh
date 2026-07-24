#!/bin/bash
# Download all chapters using curl + Python (Windows paths)
OUTPUT="D:/workspace/下载书籍/我在美国搞内战.txt"
TMPDIR="D:/workspace/下载书籍/tmp_chapters"
mkdir -p "$TMPDIR"
> "$OUTPUT"  # clear file

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REFERER="https://read.novel.qq.com/chapter/1057778108"

OK=0
FAIL=0

for i in $(seq 1 342); do
    URL="https://read.novel.qq.com/read/1057778108/${i}"
    
    # Fetch with curl
    HTML=$(curl -s -A "$UA" -e "$REFERER" --max-time 10 "$URL" 2>/dev/null)
    
    if [ -z "$HTML" ]; then
        echo "FAIL ch$i EMPTY" >&2
        FAIL=$((FAIL+1))
        continue
    fi
    
    # Extract text using python
    TEXT=$(echo "$HTML" | python3 -c "
import re, sys
html = sys.stdin.read()
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
title = re.sub(r'<[^>]+>', '', m.group(1).strip()) if m else '第${i}章'
text = re.sub(r'<[^>]+>', '\n', text)
text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
text = text.replace('&nbsp;', ' ')
text = re.sub(r'\n{3,}', '\n\n', text)
text = re.sub(r'[ \t]{2,}', ' ', text).strip()
print(title)
print('---CONTENT---')
print(text)
" 2>/dev/null)
    
    TITLE=$(echo "$TEXT" | head -1)
    CONTENT=$(echo "$TEXT" | sed -n '/---CONTENT---/,$ p' | tail -n +2)
    CLEN=$(echo "$CONTENT" | wc -c)
    
    if [ "$CLEN" -gt 100 ]; then
        printf '# %s\n\n%s\n\n\n' "$TITLE" "$CONTENT" >> "$OUTPUT"
        OK=$((OK+1))
    else
        echo "FAIL ch$i SHORT($CLEN)" >&2
        FAIL=$((FAIL+1))
    fi
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "PROGRESS: $i/342 ok=$OK fail=$FAIL" >&2
    fi
    
    sleep 0.4
done

echo "DONE: ok=$OK fail=$FAIL" >&2
du -h "$OUTPUT" >&2
