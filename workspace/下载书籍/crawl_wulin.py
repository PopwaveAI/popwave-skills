#!/usr/bin/env python3
"""快速下载武林半侠传 - 电脑版（单页全章）"""
import re, sys, time, os, requests, concurrent.futures
from bs4 import BeautifulSoup

sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
BASE = "https://www.ishubao.org/files/article/html/85/85606"
OUT = r"D:\workspace\参考小说txt\武林半侠传.txt"

# Ads to strip
ADS = [
    r"一秒记住.*", r"百度搜索:.*", r"请记住本书首发域名.*", r"手机用户请浏览.*阅读",
    r".*www\..*\.com", r"本章未完.*", r"推荐.*小说.*", r"上一页.*", r".*下一页.*",
    r"返回目录", r"投推荐票", r"加入书签", r"举报章节出错",
    r"举报.*", r"2016.*阅读", r".*最新网址.*", r".*—.*—.*—.*",
]

def clean_text(text):
    lines = []
    for line in text.split("\n"):
        line = line.strip()
        if not line: continue
        skip = False
        for p in ADS:
            if re.search(p, line): skip = True; break
        if not skip: lines.append(line)
    return "\n".join(lines)

def get_chapter(chapter_id):
    """Get clean text for a single chapter by its numeric ID."""
    url = f"{BASE}/{chapter_id}.html"
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    # Remove scripts/styles
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    # Find the main content div
    content = soup.find("div", class_=re.compile(r"book_content_text|content", re.I))
    if not content:
        # Fallback: find largest text div
        texts = [(len(d.get_text(strip=True)), d) for d in soup.find_all("div")]
        texts.sort(reverse=True)
        if texts and texts[0][0] > 500:
            content = texts[0][1]
        else:
            content = soup.find("body")
    if not content:
        return ""
    text = content.get_text("\n", strip=True)
    return clean_text(text)

def get_chapter_ids():
    """Get all chapter IDs from mobile chapter list."""
    links = []
    seen = set()
    page = 1
    while True:
        url = f"https://wap.ishubao.org/85/85606/" if page == 1 else f"https://wap.ishubao.org/85/85606_{page}/"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.encoding = "utf-8"
            if r.status_code != 200: break
            soup = BeautifulSoup(r.text, "lxml")
            found = 0
            for a in soup.find_all("a", href=True):
                h, t = a["href"], a.get_text(strip=True)
                if "85606" in h and h.endswith(".html") and re.search(r"第.*章|完本感言", t):
                    # Extract numeric ID from href like /85/85606/102616186.html
                    m = re.search(r"/(\d+)\.html$", h)
                    if m and m.group(1) not in seen:
                        seen.add(m.group(1))
                        links.append((m.group(1), t))
                        found += 1
            if found == 0: break
            page += 1
            time.sleep(0.2)
        except: break
    return links

def download_one(args):
    cid, title, idx, total = args
    try:
        text = get_chapter(cid)
        if text and len(text) > 50:
            return (title, text)
        return None
    except Exception as e:
        print(f"  [{idx}/{total}] FAIL {title[:30]}: {e}", file=sys.stderr)
        return None

def main():
    print("Step 1: Getting chapter list...", file=sys.stderr)
    links = get_chapter_ids()
    print(f"Found {len(links)} chapters", file=sys.stderr)
    if not links:
        print("ERROR: No chapters!", file=sys.stderr); return 1

    total = len(links)
    s = time.time()
    args = [(cid, title, i+1, total) for i, (cid, title) in enumerate(links)]

    print(f"Step 2: Downloading {total} chapters (10 workers, PC version)...", file=sys.stderr)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        fs = {ex.submit(download_one, a): a for a in args}
        done = 0
        for f in concurrent.futures.as_completed(fs):
            done += 1
            _, _, idx, _ = fs[f]
            title = fs[f][1]
            if f.result():
                results.append(f.result())
                print(f"  OK [{done}/{total}] {title[:30]}", file=sys.stderr)
            else:
                print(f"  X  [{done}/{total}] {title[:30]}", file=sys.stderr)
            if done % 100 == 0:
                el = time.time() - s
                print(f"  --- {done}/{total} in {el:.0f}s ({done/el:.1f} ch/s)", file=sys.stderr)

    print(f"Downloaded {len(results)}/{total} chapters", file=sys.stderr)

    # Sort by original order
    order = {title: i for i, (_, title) in enumerate(links)}
    results.sort(key=lambda r: order.get(r[0], 9999))

    chapters = [f"# {title}\n\n{text}" for title, text in results]
    full = "\n\n\n".join(chapters)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(full)

    mb = os.path.getsize(OUT) / 1024 / 1024
    el = time.time() - s
    print(f"\noutput={OUT}")
    print(f"bytes={os.path.getsize(OUT)}")
    print(f"chapters={len(results)}/{total}")
    print(f"size_mb={mb:.1f}")
    print(f"time={el:.0f}s ({len(results)/el:.1f} ch/s)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
