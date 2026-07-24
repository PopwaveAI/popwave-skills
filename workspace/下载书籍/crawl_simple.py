#!/usr/bin/env python3
"""Download all chapters 1-342 from read.novel.qq.com and assemble TXT."""
import re, sys, os, time
import requests
from bs4 import BeautifulSoup

BASE = "https://read.novel.qq.com/read/1057778108/{}"
HDR = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://read.novel.qq.com/chapter/1057778108",
}

def get_content(num):
    url = BASE.format(num)
    try:
        r = requests.get(url, headers=HDR, timeout=10)
        if r.status_code != 200:
            return None, None
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        # title
        h1 = soup.select_one('h1')
        title = h1.get_text(strip=True) if h1 else f"第{num}章"
        # content - try selectors
        content = ""
        for sel in ['div.content', 'div.read-content', 'div#chaptercontent',
                     'article', 'div.txtnav', 'div.novel-content', '.content',
                     'div.content-body']:
            el = soup.select_one(sel)
            if el:
                content = el.get_text('\n', strip=True)
                break
        if not content or len(content) < 50:
            return None, None
        content = re.sub(r'\n{3,}', '\n\n', content)
        return title, content
    except Exception as e:
        return None, None

lines = []
ok = 0
fail = 0

for i in range(1, 343):
    title, content = get_content(i)
    if content:
        lines.append(f"# {title}\n\n{content}")
        ok += 1
        sys.stderr.write(f"OK  [{i}/342] {title}\n")
    else:
        fail += 1
        sys.stderr.write(f"FAIL[{i}/342]\n")
    sys.stderr.flush()
    if i < 342:
        time.sleep(0.5)

if not lines:
    print("ERROR: no chapters", file=sys.stderr)
    sys.exit(1)

out = r"D:\workspace\下载书籍\我在美国搞内战.txt"
full = "\n\n".join(lines)
with open(out, 'w', encoding='utf-8') as f:
    f.write(full)

sz = os.path.getsize(out)
preview = re.sub(r'\s+', ' ', full[:120]).strip()
print(f"output={out}")
print(f"bytes={sz}")
print(f"success={ok}")
print(f"failed={fail}")
print(f"preview={preview}")
