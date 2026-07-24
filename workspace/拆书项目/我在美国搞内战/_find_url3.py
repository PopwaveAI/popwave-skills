import urllib.request, re, sys

def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    })
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = resp.read()
        ct = resp.headers.get('Content-Type', '')
        try:
            return data.decode('utf-8', errors='replace')
        except:
            return data.decode('gbk', errors='replace')
    except Exception as e:
        return None

# Try popular笔趣阁 sites with known URL patterns for the book
# Book ID on起点: 1047777980
# Some站点 use the same ID

sites_to_try = [
    # Common笔趣阁 variants
    ('https://www.biquge.com.cn/book/{id}/', '{id} -> biquge.com.cn'),
    ('https://www.biquge.tv/book/{id}/', '{id} -> biquge.tv'),
    ('https://www.biquge.info/book/{id}/', '{id} -> biquge.info'),
    ('https://www.ibiquge.net/book/{id}/', '{id} -> ibiquge.net'),
    ('https://www.biquge.com/book/{id}/', '{id} -> biquge.com'),
    ('https://www.bqgka.com/book/{id}/', '{id} -> bqgka.com'),
]

# Try with the old name too: 我在美国拼高达
# Some sites might have it under this name

# Check the起点 book ID pattern - many笔趣阁 sites use the same numeric ID
bid = '1047777980'
print(f'Checking 起点 book ID {bid} on sites...')
for url_tpl, name in sites_to_try:
    url = url_tpl.replace('{id}', bid)
    try:
        html = fetch(url)
        if html and '我在美国' in html:
            print(f'  FOUND: {url}')
            # Get the page title
            m = re.search(r'<title>(.*?)</title>', html, re.I)
            title = m.group(1) if m else 'no title'
            print(f'  Title: {title}')
            # Save the URL for crawling
            with open('D:\\workspace\\拆书项目\\我在美国搞内战\\_book_url.txt', 'w') as f:
                f.write(url)
            print(f'  Saved to _book_url.txt')
        elif html:
            title_m = re.search(r'<title>(.*?)</title>', html, re.I)
            title = title_m.group(1) if title_m else 'no title'
            print(f'  Checked {url} - not found (title: {title[:50]})')
        else:
            print(f'  Checked {url} - no response')
    except Exception as e:
        print(f'  Error {url}: {e}')

# Also try searching the new name
print('\n--- Also trying new name search approach ---')
# Check if biquke.com has it by searching
search_urls = [
    f'https://www.biquge.com.cn/search.html?keyword={urllib.parse.quote("我在美国搞内战")}',
    f'https://www.bqgka.com/search.html?keyword={urllib.parse.quote("我在美国搞内战")}',
]

for url in search_urls:
    try:
        html = fetch(url)
        if html and ('我在美国' in html or '拼高达' in html):
            print(f'  Found at: {url}')
            # Extract links
            for m in re.finditer(r'<a[^>]*href=[\"\']([^\"\']+)[\"\'][^>]*>(.*?)</a>', html, re.I):
                txt = m.group(2)
                url2 = m.group(1)
                if '美国' in txt or '拼高' in txt:
                    full = url2 if url2.startswith('http') else f'https://www.biquge.com.cn{url2}'
                    print(f'  -> {full} : {txt[:50]}')
    except Exception as e:
        print(f'  Error {url}: {e}')

print('\nDone.')
