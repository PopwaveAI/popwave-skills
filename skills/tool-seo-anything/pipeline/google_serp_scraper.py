#!/usr/bin/env python3
"""
Google SERP Scraper - 使用 Playwright 抓取 Google 搜索结果
自动排除广告、视频、AI Overview，提取博客/文章类型结果 + People Also Ask 问题
"""

import asyncio
import json
import os
import re
import sys
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'data')


def clean_description(raw: str) -> str:
    """清洗 Google SERP 描述中的重复和噪音"""
    if not raw:
        return ''
    parts = re.split(r'\s{2,}', raw)
    seen = set()
    cleaned = []
    for p in parts:
        p = p.strip()
        if p and p not in seen and len(p) > 5:
            seen.add(p)
            cleaned.append(p)
    result = ' '.join(cleaned)
    return result[:300].strip()


def extract_domain(url: str) -> str:
    """提取域名"""
    m = re.search(r'https?://(?:www\.)?([^/]+)', url)
    return m.group(1) if m else url


async def scrape_google_serp(keyword: str, num_results: int = 20):
    """
    抓取 Google SERP 结果，含 People Also Ask 问题
    """
    results = []
    seen_urls = set()
    paa_questions = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--incognito',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-gpu',
            ]
        )

        context = await browser.new_context(
            locale='en-US',
            timezone_id='America/Phoenix',
            viewport={'width': 1280, 'height': 900},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        )

        page = await context.new_page()

        search_url = f'https://www.google.com/search?q={keyword.replace(" ", "+")}&hl=en&gl=us&num=30'

        print(f"正在搜索: {keyword}")
        print(f"URL: {search_url}")

        try:
            await page.goto(search_url, wait_until='domcontentloaded', timeout=60000)
            await asyncio.sleep(3)

            # ====== 提取 PAA (People Also Ask) ======
            try:
                paa_selectors = [
                    'div[data-q]',
                    'g-accordion-expander',
                    'div.related-question-pair',
                    '[jsname="yEVEwb"]',
                ]
                for sel in paa_selectors:
                    elems = await page.query_selector_all(sel)
                    for e in elems:
                        txt = await e.text_content()
                        if txt and len(txt) > 10:
                            txt = txt.strip()
                            if '?' in txt:
                                q = txt.split('?')[0].strip() + '?'
                            else:
                                q = txt[:150].strip()
                            if q not in paa_questions:
                                paa_questions.add(q)
            except Exception:
                pass

            # ====== 提取搜索结果 ======
            while len(results) < num_results:
                containers = await page.query_selector_all(
                    'div[data-sokoban-container], div.g, div.MjjYud, div[data-ved]'
                )

                for container in containers:
                    if len(results) >= num_results:
                        break

                    link_elem = await container.query_selector('h3 a[href^="https"], a[href^="https"]')
                    if not link_elem:
                        continue

                    url = await link_elem.get_attribute('href')
                    if not url or url in seen_urls:
                        continue

                    if any(x in url.lower() for x in [
                        'youtube.com', 'youtu.be',
                        'google.com/search', 'support.google',
                        'maps.google', 'play.google',
                        'reddit.com',
                    ]):
                        continue

                    title_elem = await container.query_selector('h3')
                    if not title_elem:
                        continue

                    title = await title_elem.text_content()
                    if not title or len(title) < 10:
                        continue

                    desc_selectors = [
                        'div[data-snc]', '.VwiC3b', '.s3v94d',
                        '.IsZvec', '.lEBKkf',
                        'div[style*="-webkit-line-clamp"]',
                        'div[data-content-feature="1"] span',
                    ]
                    description = ''
                    for ds in desc_selectors:
                        de = await container.query_selector(ds)
                        if de:
                            raw = await de.text_content()
                            description = clean_description(raw)
                            if description:
                                break

                    seen_urls.add(url)
                    results.append({
                        'rank': len(results) + 1,
                        'title': title.strip(),
                        'url': url,
                        'domain': extract_domain(url),
                        'description': description,
                    })

                if len(results) >= num_results:
                    break

                next_button = await page.query_selector('a#pnnext, a:has-text("Next")')
                if next_button and len(results) < num_results:
                    print(f"已提取 {len(results)} 条，翻页中...")
                    await next_button.click()
                    await asyncio.sleep(2)
                else:
                    break

        except Exception as e:
            print(f"Error: {e}")

        finally:
            await browser.close()

    return results, list(paa_questions)


def save_results(results, paa_questions, keyword):
    """保存结果到 JSON"""
    safe_name = re.sub(r'[^\w\s-]', '', keyword).strip().replace(' ', '_').lower()
    filepath = os.path.join(OUTPUT_DIR, f'{safe_name}_serp_results.json')

    output = {
        'keyword': keyword,
        'total_results': len(results),
        'serp': results,
        'paa_questions': paa_questions,
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存到: {filepath}")
    return filepath


def print_summary(results, paa_questions):
    """打印摘要"""
    print("\n" + "=" * 80)
    print(f"SERP 结果: {len(results)} 条")
    print(f"PAA 问题: {len(paa_questions)} 条")
    print("=" * 80)

    for r in results:
        print(f"\n【#{r['rank']}】{r['title']}")
        print(f"    域名: {r['domain']}")
        print(f"    URL: {r['url']}")
        if r['description']:
            desc_preview = r['description'][:150]
            print(f"    摘要: {desc_preview}...")

    if paa_questions:
        print("\n--- People Also Ask ---")
        for q in paa_questions[:10]:
            print(f"  Q: {q}")


async def main():
    keyword = "ai marketing"
    num_results = 20

    if len(sys.argv) > 1:
        keyword = ' '.join(sys.argv[1:]).strip()
        if keyword.split()[-1].isdigit():
            parts = keyword.split()
            num_results = int(parts[-1])
            keyword = ' '.join(parts[:-1])

    print(f"\n🔍 Google SERP Scraper")
    print(f"关键词: {keyword}")
    print(f"目标结果数: {num_results}")
    print("-" * 80)

    results, paa_questions = await scrape_google_serp(keyword, num_results)

    if results:
        print_summary(results, paa_questions)
        save_results(results, paa_questions, keyword)
    else:
        print("\n❌ 未找到任何结果")


if __name__ == '__main__':
    asyncio.run(main())
