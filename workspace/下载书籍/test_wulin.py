#!/usr/bin/env python3
"""Test fetching a chapter from ishubao.org"""
import re
import sys
import requests
from bs4 import BeautifulSoup

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = 'https://wap.ishubao.org/85/85606/102616186.html'
resp = requests.get(url, headers=headers, timeout=15)
resp.encoding = 'utf-8'

soup = BeautifulSoup(resp.text, 'lxml')

# Save page for inspection
with open('D:\\workspace\\下载书籍\\_test_chapter.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)
print(f'Saved {len(resp.text)} bytes')

# Remove scripts/style
for tag in soup(['script', 'style']):
    tag.decompose()

# Get body text
body = soup.find('body')
if body:
    text = body.get_text('\n', strip=True)
    print(f'Body text: {len(text)} chars')
    print(text[:600])
