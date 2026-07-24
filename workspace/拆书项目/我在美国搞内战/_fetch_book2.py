#!/usr/bin/env python3
"""Try harder to fetch the novel."""
import urllib.request
import urllib.parse
import re
import sys

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        html = resp.read()
        ct = resp.headers.get('Content-Type', '')
        if 'charset=' in ct:
            enc = ct.split('charset=')[-1].split(';')[0].strip()
        else:
            enc = 'utf-8'
        return html.decode(enc, errors='replace')
    except Exception as e:
        return f"ERROR: {e}"

def strip_html(html):
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.I)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL|re.I)
    text = re.sub(r'<[^>]+>', '\n', text)
    text = re.sub(r'&nbsp;', ' ', text).replace('&lt;', '<').replace('&gt;', '>')
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# 1. Try gd958.com (58小说网) - see if they have the book
print("=== Checking gd958.com main page ===")
html = fetch('http://www.gd958.com/')
if 'ERROR' not in html:
    for match in re.finditer(r'href=[\'"]([^\'"]+)[\'"][^>]*>[^<]*(\S[^<]{2,50})<', html):
        text = match.group(2)
        if '美国' in text and '内战' in text or '拼高达' in text:
            print(f"  Found: {match.group(1)} -> {text}")

# 2. Try m.35wx.la (三五第一小说网) 
print("\n=== Checking 35wx.la ===")
html = fetch('https://m.35wx.la/book/153582/')
if 'ERROR' not in html:
    txt = strip_html(html)
    grep = [l.strip() for l in txt.split('\n') if '美国' in l or '捕梦' in l or '拼高达' in l]
    for l in grep[:10]:
        print(f"  {l}")
    # Find links to the book
    for m in re.finditer(r'href=[\'"]([^\'"]+)[\'"][^>]*>[^<]*美国[^<]*<', html):
        print(f"  Link: {m.group(1)}")

# 3. Try searching for the old URL pattern on minorjanai
# From earlier search: the latest chapter was "第三百一十八章 册封子民(求月票)"
# The book was listed as [科幻灵异]我在美国搞内战【正版无广】
print("\n=== Trying to find book on minorjanai via spider routes ===")
html = fetch('https://www.minorjanai.net/')
if 'ERROR' not in html:
    txt = strip_html(html)
    for line in txt.split('\n'):
        if '美国' in line and ('内战' in line or '拼高' in line):
            print(f"  Found on homepage: {line.strip()}")

# 4. Try a known笔趣阁 site - let's look for more specific URLs
print("\n=== Trying to fetch from the reader.qq.com (QQ阅读) ===")
# QQ阅读 might have the book in a simpler format
html = fetch('https://ubook.reader.qq.com/kol-rec/sq6a56a889206ee33c')
if 'ERROR' not in html:
    print(f"  QQ阅读 page: {len(html)} bytes")
    txt = strip_html(html)
    grep = [l.strip() for l in txt.split('\n') if len(l.strip()) > 20]
    for l in grep[:20]:
        print(f"  {l}")

# 5. Try ltxs.la (龙头小说) - they had the book listed under 捕梦者
print("\n=== Checking ltxs.la for 捕梦者 author page ===")
html = fetch('http://m.ltxs.la/ls134/134839/index_2.html')
if 'ERROR' not in html:
    txt = strip_html(html)
    grep = [l.strip() for l in txt.split('\n') if '美国' in l or '拼高达' in l]
    for l in grep[:10]:
        print(f"  {l}")

print("\nDone.")
