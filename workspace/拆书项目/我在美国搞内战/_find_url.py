import urllib.request, re

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=10)
    try:
        return resp.read().decode('utf-8', errors='replace')
    except:
        return resp.read().decode('gbk', errors='replace')

# Check zhongbeitianfeng homepage
html = fetch('https://www.zhongbeitianfeng.com/')
for m in re.finditer(r"<a[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", html, re.I):
    text = m.group(2)
    if '我在美国' in text:
        print(f"FOUND: href={m.group(1)}, text={text}")
    elif '美国搞内战' in text or '美国拼高' in text:
        print(f"FOUND: href={m.group(1)}, text={text}")

# Check if the site has a search
print("\n--- Trying zhongbeitianfeng search ---")
for keyword in ['我在美国搞内战', '我在美国拼高达', '捕梦者']:
    encoded = urllib.parse.quote(keyword)
    html2 = fetch(f'https://www.zhongbeitianfeng.com/search.html?searchkey={encoded}')
    for m in re.finditer(r"<a[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", html2, re.I):
        text = m.group(2)
        if len(text) < 60:
            print(f"  [{keyword}] {m.group(1)} -> {text[:50]}")

# Try txtbmp.com search
print("\n--- Trying txtbmp.com search ---")
for keyword in ['我在美国搞内战', '我在美国拼高达']:
    encoded = urllib.parse.quote(keyword)
    try:
        html3 = fetch(f'https://www.txtbmp.com/search.html?searchkey={encoded}')
        for m in re.finditer(r"<a[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", html3, re.I):
            text = m.group(2)
            if len(text) < 60:
                print(f"  [{keyword}] {m.group(1)} -> {text[:50]}")
    except:
        print(f"  [{keyword}] Failed")

# Try minorjanai autor search
print("\n--- Trying minorjanai search ---")
html4 = fetch('https://www.minorjanai.net/search.html?searchkey=%E6%88%91%E5%9C%A8%E7%BE%8E%E5%9B%BD%E6%90%9E%E5%86%85%E6%88%98')
for m in re.finditer(r"<a[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", html4, re.I):
    text = m.group(2)
    if len(text) < 60:
        print(f"  {m.group(1)} -> {text[:50]}")
