#!/bin/bash
# Download all chapters using curl
OUTPUT="D:/workspace/下载书籍/我在美国搞内战.txt"
TMPDIR="/tmp/novel_temp"
mkdir -p "$TMPDIR"

UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REFERER="https://read.novel.qq.com/chapter/1057778108"

OK=0
FAIL=0

for i in $(seq 1 342); do
    URL="https://read.novel.qq.com/read/1057778108/${i}"
    TMPFILE="${TMPDIR}/ch_$(printf '%04d' $i).txt"
    
    # Fetch with curl
    HTTP_CODE=$(curl -s -o "$TMPFILE" -w "%{http_code}" \
        -A "$UA" \
        -e "$REFERER" \
        --max-time 10 \
        "$URL" 2>/dev/null)
    
    if [ "$HTTP_CODE" != "200" ]; then
        echo "FAIL ch$i HTTP=$HTTP_CODE" >> /dev/stderr
        FAIL=$((FAIL+1))
        continue
    fi
    
    # Extract text: remove HTML tags, keep content between h1 and "本章想法"
    python3 -c "
import re, sys
html = open('${TMPFILE//\\//}', 'rb').read()
try:
    text = html.decode('utf-8')
except:
    text = html.decode('gbk', errors='replace')
# Remove script/style
text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
# Extract title
m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
title = m.group(1).strip() if m else '第${i}章'
title = re.sub(r'<[^>]+>', '', title)
# Strip HTML
text = re.sub(r'<[^>]+>', '\n', text)
text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
text = text.replace('&nbsp;', ' ')
text = re.sub(r'\n{3,}', '\n\n', text)
text = re.sub(r'[ \t]{2,}', ' ', text)
text = text.strip()
if len(text) > 100:
    print(f'# {title}')
    print()
    print(text)
    print()
    print()
" 2>/dev/null >> "$OUTPUT"
    
    if [ $? -eq 0 ] && [ -s "$OUTPUT" ]; then
        OK=$((OK+1))
    else
        FAIL=$((FAIL+1))
    fi
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "PROGRESS: $i/342 ok=$OK fail=$FAIL" >> /dev/stderr
    fi
    
    sleep 0.5
done

echo "DONE: ok=$OK fail=$FAIL" >> /dev/stderr
du -h "$OUTPUT" >> /dev/stderr
