#!/usr/bin/env python3
"""Scrape novel from chapter sites."""
import re, sys, time

# Use only standard library - no bs4 dependency
try:
    import urllib.request, urllib.parse
    HAS_REQUESTS = False
except:
    print("No urllib available")
    sys.exit(1)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = resp.read()
        html = data.decode('utf-8', errors='replace')
        if len(html) < 100 and 'charset=gb' in str(resp.headers).lower():
            html = data.decode('gbk', errors='replace')
        return html
    except Exception as e:
        return None

def content_text(html):
    """Extract text content from HTML without bs4."""
    # Remove scripts and styles
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.I)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.I)
    # Remove comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    # Replace block tags with newline
    html = re.sub(r'</?(?:div|p|br|h[1-6]|li|tr|td|th|section|article|blockquote)[^>]*>', '\n', html, flags=re.I)
    # Remove remaining tags
    text = re.sub(r'<[^>]+>', '', html)
    # Decode entities
    text = text.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    # Clean lines
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if line:
            lines.append(line)
    return '\n'.join(lines)

def find_links(html, pattern=None):
    """Find all href links matching pattern."""
    links = re.findall(r'href=[\'"]([^\'"]+)[\'"]([^>]*)>([^<]*)<', html)
    return [(u, t.strip(), a) for u, a, t in links]

# Strategy 1: Try minorjanai.net with possible book IDs
print("=== Strategy 1: Search book on minorjanai ===")
# The book was listed with chapter 318. Try to find the book page via the recent update list
html = fetch('https://www.minorjanai.net/')
if html:
    # Search for 美国 in the HTML
    for line in html.split('\n'):
        if '美国' in line or '捕梦' in line or '拼高达' in line:
            print(f"  MATCH: {line.strip()[:200]}")

# Strategy 2: Try the dysdx.com 新笔趣阁
print("\n=== Strategy 2: Try dysdx.com (新笔趣阁) ===")
html = fetch('https://www.dysdx.com/search.html?searchkey=%E6%88%91%E5%9C%A8%E7%BE%8E%E5%9B%BD%E6%90%9E%E5%86%85%E6%88%98')
if html:
    txt = content_text(html)
    # Look for any mention of the book
    lines = [l for l in txt.split('\n') if '美国' in l]
    for l in lines[:10]:
        print(f"  {l[:200]}")
else:
    print("  No response from dysdx search")

# Search for old name too
html = fetch('https://www.dysdx.com/search.html?searchkey=%E6%88%91%E5%9C%A8%E7%BE%8E%E5%9B%BD%E6%8B%BC%E9%AB%98%E8%BE%BE')
if html:
    txt = content_text(html)
    lines = [l for l in txt.split('\n') if '美国' in l]
    for l in lines[:10]:
        print(f"  {l[:200]}")

# Strategy 3: Try the 龙头小说 ltxs.la
print("\n=== Strategy 3: Try ltxs.la (龙头小说) ===")
# The author page for 捕梦者
html = fetch('http://m.ltxs.la/search.html?searchkey=%E6%8D%95%E6%A2%A6%E8%80%85')
if html:
    links = find_links(html)
    for url, text, attr in links:
        if '美国' in text or '拼高' in text:
            print(f"  LINK: {url} -> {text}")
else:
    print("  No response from ltxs.la")

# Try searching for the book by old name
html = fetch('http://m.ltxs.la/search.html?searchkey=%E6%88%91%E5%9C%A8%E7%BE%8E%E5%9B%BD%E6%8B%BC%E9%AB%98%E8%BE%BE')
if html:
    txt = content_text(html)
    lines = [l for l in txt.split('\n') if '美国' in l]
    for l in lines[:10]:
        print(f"  {l[:200]}")
else:
    print("  No response from ltxs.la search")

print("\nDone.")
