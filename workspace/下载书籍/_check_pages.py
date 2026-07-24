import re, requests
from bs4 import BeautifulSoup

BASE = 'https://wap.ishubao.org'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

url = BASE + '/85/85606/'
resp = requests.get(url, headers=HEADERS, timeout=15)
resp.encoding = 'utf-8'
soup = BeautifulSoup(resp.text, 'lxml')

# Find any links that might be page numbers
for a in soup.find_all('a', href=True):
    href = a['href']
    text = a.get_text(strip=True)
    # Show all links on the page
    if '85606' in href or text.isdigit() or '页' in text:
        print(f'{href}: {text}')
