import urllib.request, re

def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cookie': 'novel_visited=1'
    })
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read()
    try:
        return html.decode('utf-8', errors='replace')
    except:
        return html.decode('gbk', errors='replace')

# Try zhichangshuwu.com
sites = [
    ('zhichangshuwu.com', '职场书屋'),
]

# Check if the book exists on 58小说网 (gd958)
print("=== 58小说网 (gd958) ===")
try:
    html = fetch('http://www.gd958.com/search.html?searchkey=我在美国搞内战')
    txt = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.I)
    txt = re.sub(r'<style[^>]*>.*?</style>', '', txt, flags=re.DOTALL|re.I)
    txt = re.sub(r'<[^>]+>', '\n', txt)
    txt = re.sub(r'\n+', '\n', txt)
    for line in txt.split('\n'):
        if '美国' in line and ('内战' in line or '拼高' in line or '捕梦' in line):
            print(f"  {line.strip()[:150]}")
    if not any('美国' in l for l in txt.split('\n')):
        print(f"  No relevant content found. First 500 chars: {txt[:500]}")
except Exception as e:
    print(f"  Error: {e}")

# Try nbaxiaoshuo (NBA小说网)
print("\n=== NBA小说网 (nbaxiaoshuo) ===")
try:
    html = fetch('http://www.nbaxiaoshuo.com/search.html?searchkey=我在美国搞内战')
    txt = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.I)
    txt = re.sub(r'<[^>]+>', '\n', txt)
    for line in txt.split('\n'):
        if '美国' in line:
            print(f"  {line.strip()[:150]}")
except Exception as e:
    print(f"  Error: {e}")

# Try a generic approach - search the old name on dysdx
print("\n=== 新笔趣阁 (dysdx) ===")
try:
    # Direct search
    html = fetch('https://www.dysdx.com/search.html?searchkey=我在美国拼高达')
    txt = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.I)
    txt = re.sub(r'<[^>]+>', '\n', txt)
    txt = re.sub(r'\n+', '\n', txt)
    found = False
    for line in txt.split('\n'):
        if '美国' in line and ('拼高' in line or '捕梦' in line or '内战' in line):
            print(f"  {line.strip()[:200]}")
            found = True
    if not found:
        print(f"  Page text (first 800): {txt[:800]}")
except Exception as e:
    print(f"  Error: {e}")

# Try the 龙头小说 more carefully
print("\n=== 龙头小说 (ltxs.la) ===")
try:
    html = fetch('http://m.ltxs.la/search.html?searchkey=我在美国拼高达')
    txt = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.I)
    txt = re.sub(r'<[^>]+>', '\n', txt)
    for line in txt.split('\n'):
        if '美国' in line or '拼高' in line:
            print(f"  {line.strip()[:200]}")
    if not any('美国' in l for l in txt.split('\n')):
        print(f"  First 500: {txt[:500]}")
except Exception as e:
    print(f"  Error: {e}")
