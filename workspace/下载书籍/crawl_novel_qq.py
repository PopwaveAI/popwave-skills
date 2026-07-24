#!/usr/bin/env python3
"""Crawl all chapters from read.novel.qq.com and assemble into one TXT."""
import re
import sys
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://read.novel.qq.com/read/1057778108/{}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://read.novel.qq.com/chapter/1057778108",
}

# First, get the chapter list to find all valid chapter numbers
def get_chapter_numbers():
    """Get chapter numbers from the chapter list page."""
    resp = requests.get(
        "https://read.novel.qq.com/chapter/1057778108",
        headers=HEADERS,
        timeout=30
    )
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'lxml')
    links = soup.select('a[href*="/read/1057778108/"]')
    numbers = set()
    titles = {}
    for a in links:
        m = re.search(r'/(\d+)$', a.get('href', ''))
        if m:
            num = int(m.group(1))
            numbers.add(num)
            text = a.get_text(strip=True)
            # Clean title (remove APP免费 etc.)
            text = re.sub(r'\s*APP免费\s*', '', text).strip()
            if num not in titles:
                titles[num] = text
    return sorted(numbers), titles

def extract_content(html, chapter_num):
    """Extract the chapter title and body from a chapter page."""
    soup = BeautifulSoup(html, 'lxml')
    
    # Try to get title
    title_el = soup.select_one('h1, .chapter-title, .title')
    if title_el:
        title = title_el.get_text(strip=True)
    else:
        title = f"第{chapter_num}章"
    
    # Try various content selectors
    content = ""
    for selector in [
        'div.content', 'div.read-content', 'div#chaptercontent',
        'article', 'div.txtnav', 'div.novel-content',
        'div.content-body', '.content', 'div.book-content'
    ]:
        el = soup.select_one(selector)
        if el:
            content = el.get_text('\n', strip=True)
            break
    
    if not content:
        # Fallback: get text from body, remove script/style/nav
        body = soup.find('body')
        if body:
            for tag in body(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                tag.decompose()
            content = body.get_text('\n', strip=True)
    
    return title, content

def main():
    print("Step 1: Getting chapter list...", file=sys.stderr)
    numbers, titles = get_chapter_numbers()
    print(f"Found {len(numbers)} chapters (1-{max(numbers)})", file=sys.stderr)
    
    # Also try sequential 1-342 for safety
    all_nums = numbers
    
    output_lines = []
    success = 0
    failed = 0
    
    print(f"Step 2: Crawling {len(all_nums)} chapters...", file=sys.stderr)
    
    for i, num in enumerate(all_nums, 1):
        url = BASE_URL.format(num)
        chapter_title = titles.get(num, f"第{num}章")
        
        print(f"  [{i}/{len(all_nums)}] Chapter {num}: {chapter_title}", file=sys.stderr)
        
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.encoding = 'utf-8'
            
            if resp.status_code != 200:
                print(f"    SKIP: HTTP {resp.status_code}", file=sys.stderr)
                failed += 1
                continue
            
            title, content = extract_content(resp.text, num)
            
            if content and len(content) > 50:
                # Clean the content
                content = re.sub(r'\n{3,}', '\n\n', content)
                output_lines.append(f"# {title}\n\n{content}")
                success += 1
            else:
                print(f"    SKIP: content too short ({len(content) if content else 0} chars)", file=sys.stderr)
                failed += 1
        
        except Exception as e:
            print(f"    ERROR: {e}", file=sys.stderr)
            failed += 1
        
        # Rate limiting
        if i < len(all_nums):
            time.sleep(0.8)
    
    if not output_lines:
        print("ERROR: No chapters crawled successfully!", file=sys.stderr)
        sys.exit(1)
    
    full_text = "\n\n".join(output_lines)
    output_path = r"D:\workspace\下载书籍\我在美国搞内战.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    preview = re.sub(r'\s+', ' ', full_text[:120]).strip()
    
    print(f"\noutput={output_path}")
    print(f"encoding=utf-8")
    print(f"bytes={os.path.getsize(output_path)}")
    print(f"chapters_crawled={success}")
    print(f"chapters_failed={failed}")
    print(f"preview={preview}")
    print(f"size_mb={size_mb:.1f}")
    return 0

if __name__ == '__main__':
    import os
    raise SystemExit(main())
