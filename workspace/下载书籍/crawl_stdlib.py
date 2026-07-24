#!/usr/bin/env python3
"""Download all chapters 1-342 using only stdlib."""
import re, sys, os, time, urllib.request, urllib.error

BASE = "https://read.novel.qq.com/read/1057778108/{}"
HDR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://read.novel.qq.com/chapter/1057778108",
}

def fetch(num):
    url = BASE.format(num)
    req = urllib.request.Request(url, headers=HDR)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        # Try UTF-8, fallback to GBK
        try:
            html = data.decode('utf-8')
        except:
            html = data.decode('gbk', errors='replace')
        return html
    except Exception as e:
        return None

def extract_content(html, num):
    # Extract title from <h1>
    m = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    title = m.group(1).strip() if m else f'第{num}章'
    title = re.sub(r'<[^>]+>', '', title)  # strip inner tags
    
    # Extract main content - everything between # title line and "本章想法" or similar markers
    # Look for the chapter text which starts after the metadata block
    content_start = html.find('本章字数：')
    if content_start > 0:
        # Find where the chapter text really starts - after the metadata
        text_start = html.find('</h1>', content_start)
        if text_start < 0:
            text_start = content_start
    else:
        text_start = 0
    
    # Remove HTML tags
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
    text = re.sub(r'<[^>]+>', '\n', text)
    
    # Decode HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&nbsp;', ' ').replace('&quot;', '"')
    
    # Normalize whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = text.strip()
    
    return title, text

lines = []
ok = 0
fail = 0

for i in range(1, 343):
    html = fetch(i)
    if html:
        title, content = extract_content(html, i)
        if content and len(content) > 100:
            lines.append(f'# {title}\n\n{content}')
            ok += 1
        else:
            fail += 1
    else:
        fail += 1
    
    if i % 10 == 0:
        print(f'PROGRESS: {i}/342 ok={ok} fail={fail}', file=sys.stderr)
    
    if i < 342:
        time.sleep(0.3)

output = '\n\n\n'.join(lines)
print(f'RESULT: ok={ok} fail={fail} chars={len(output)}')
sys.exit(0 if ok > 0 else 1)
