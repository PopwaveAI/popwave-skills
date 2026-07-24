import urllib.request, re, sys

def fetch(url, timeout=10):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        data = resp.read()
        try:
            return data.decode('utf-8', errors='replace')
        except:
            return data.decode('gbk', errors='replace')
    except Exception as e:
        print(f'  Error: {e}')
        return None

# Try a known site that serves chapter content without JS
# Check if kshuz.com or 99csw have the book
sites = [
    f'https://www.99csw.com/book/10477/10477798.htm',
    f'http://www.99lib.net/book/10477/10477798.htm',
]

for url in sites:
    html = fetch(url)
    if html:
        m = re.search(r'<title>(.*?)</title>', html, re.I)
        title = m.group(1) if m else 'no title'
        print(f'{url}: got {len(html)}b, title={title[:50]}')
        if '美国' in html or '拼高' in html:
            print('  FOUND BOOK!')
            # Check for chapter list
            links = re.findall(r'href=[\"\']([^\"\']+)[\"\'][^>]*>([^<]*第[^<]*章[^<]*)<', html)
            if links:
                print(f'  Found {len(links)} chapter links')
                for u, t in links[:5]:
                    print(f'    {u[:60]} -> {t[:30]}')
    else:
        print(f'{url}: no response')

# Try Qingkan/书旗 etc
print('\n--- Trying other sites ---')
more = [
    'https://www.qingkan.net/book/1047777980/',
    'https://www.69shu.com/book/1047777980/',
]
for url in more:
    html = fetch(url)
    if html and len(html) > 200:
        m = re.search(r'<title>(.*?)</title>', html, re.I)
        title = m.group(1) if m else 'no title'
        print(f'{url}: got {len(html)}b, title={title[:50]}')
        if '美国' in html or '拼高' in html:
            print('  FOUND BOOK!')

# Check exiaoshuo.com (e小说网)
print('\n--- Check exiaoshuo for chapter list ---')
for bid in ['1047777980', '178296', '153582']:
    for base in ['https://www.exiaoshuo.com', 'https://m.exiaoshuo.com']:
        url = f'{base}/book/{bid}/'
        html = fetch(url)
        if html and len(html) > 500:
            m = re.search(r'<title>(.*?)</title>', html, re.I)
            title = m.group(1) if m else 'no title'
            print(f'{url}: got {len(html)}b, title={title[:50]}')
            if '美国' in html or '拼高' in html:
                print('  FOUND BOOK!')

print('\nDone.')
