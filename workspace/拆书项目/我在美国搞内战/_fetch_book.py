#!/usr/bin/env python3
"""Try to fetch the novel text from various盗版 sites."""
import urllib.request
import urllib.parse
import re
import json
import sys

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    })
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        html = resp.read()
        # Try to detect encoding
        content_type = resp.headers.get('Content-Type', '')
        if 'charset=' in content_type:
            enc = content_type.split('charset=')[-1].split(';')[0].strip()
        else:
            enc = 'utf-8'
        return html.decode(enc, errors='replace')
    except Exception as e:
        return f"ERROR: {e}"

def extract_text_from_html(html):
    """Simple HTML to text extraction."""
    # Remove script and style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '\n', html)
    # Decode HTML entities
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&amp;', '&').replace('&quot;', '"')
    # Clean excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# 1. Try txtbmp.com (文本小说网)
print("=== Trying txtbmp.com ===")
html = fetch('https://www.txtbmp.com/search.html?searchkey=%E6%88%91%E5%9C%A8%E7%BE%8E%E5%9B%BD%E6%90%9E%E5%86%85%E6%88%98')
if 'ERROR' not in html:
    # Look for links to the book
    matches = re.findall(r'href=[\'"]([^\'"]+)[\'"][^>]*>[^<]*我在美国[^<]*<', html)
    for m in matches:
        full_url = m if m.startswith('http') else 'https://www.txtbmp.com' + m
        print(f"Found: {full_url}")
else:
    print(f"Error: {html}")

# 2. Try searching txtbmp for the old name
print("\n=== Trying txtbmp.com (拼高达) ===")
html = fetch('https://www.txtbmp.com/search.html?searchkey=%E6%88%91%E5%9C%A8%E7%BE%8E%E5%9B%BD%E6%8B%BC%E9%AB%98%E8%BE%BE')
if 'ERROR' not in html:
    matches = re.findall(r'href=[\'"]([^\'"]+)[\'"][^>]*>[^<]*我在美国[^<]*<', html)
    for m in matches:
        full_url = m if m.startswith('http') else 'https://www.txtbmp.com' + m
        print(f"Found: {full_url}")
else:
    print(f"Error: {html}")

# 3. Try zhongbeitianfeng.com directly - check homepage for the book link
print("\n=== Trying zhongbeitianfeng.com main page ===")
html = fetch('https://www.zhongbeitianfeng.com/')
if 'ERROR' not in html:
    # The book was on the homepage under 玄幻修真 section
    matches = re.findall(r'href=[\'"]([^\'"]+)[\'"][^>]*>[^<]*我在美国搞内战[^<]*<', html)
    if not matches:
        matches = re.findall(r'href=[\'"]([^\'"]+)[\'"][^>]*>[^<]*我在美国[^<]*<', html)
    for m in matches:
        full_url = m if m.startswith('http') else 'https://www.zhongbeitianfeng.com' + m
        print(f"Found: {full_url}")
else:
    print(f"Error: {html}")

# 4. Try the direct path on zhongbeitianfeng for this book
print("\n=== Trying specific patterns on zhongbeitianfeng ===")
# Try to find book id from homepage
html = fetch('https://www.zhongbeitianfeng.com/')
if 'ERROR' not in html:
    # Look for book page links
    book_links = re.findall(r'/yewujieshao/\d+\.html', html)
    for bl in set(book_links):
        print(f"  book page candidate: https://www.zhongbeitianfeng.com{bl}")
else:
    print(f"Error: {html}")

# 5. Try the 58小说网 (gd958.com) 
print("\n=== Trying 58小说网 (gd958.com) ===")
html = fetch('http://www.gd958.com/')
if 'ERROR' not in html:
    print(f"Page size: {len(html)} bytes - sample: {html[:200]}")
else:
    print(f"Error: {html}")

print("\nDone.")
