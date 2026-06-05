#!/usr/bin/env python3
"""龙空 lkong.com 自动化舆情采集器 — 完整方案
核心原理：龙空 Fifth Era 是 Next.js SPA，内容在 __NEXT_DATA__ JSON 中
"""
import requests, json, re, time, os, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
INDEX_FILE = os.path.join(os.path.dirname(__file__), "lkong_index.json")
CONCURRENCY = 50

def extract_slate_text(content_raw):
    blocks = json.loads(content_raw) if isinstance(content_raw, str) else (content_raw or [])
    text = ''
    for block in blocks:
        if isinstance(block, dict) and block.get('children'):
            for child in block['children']:
                if isinstance(child, dict) and child.get('text'):
                    text += child['text']
    return text

def fetch_thread(tid):
    """抓单个 thread 的完整数据"""
    try:
        r = requests.get(f"https://www.lkong.com/thread/{tid}", headers=HEADERS, timeout=10)
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text)
        if not m:
            return None
        data = json.loads(m.group(1))
        source = data['props']['pageProps']['source']
        thread_meta = source.get('thread') or {}
        draft = source.get('draft') or {}
        title = thread_meta.get('title') or draft.get('title') or ''
        if not title:
            return None
        
        posts = source.get('posts', [])
        all_text = title + ' '
        for p in posts:
            all_text += extract_slate_text(p.get('content', '[]')) + ' '
        
        return {
            "tid": tid,
            "title": title,
            "text": all_text[:5000],
            "posts_count": len(posts),
            "forum": thread_meta.get('forum', {}).get('name', ''),
        }
    except:
        return None

# ── 索引管理 ──────────────────────────
def build_index(start=2838000, end=3615000, step=1):
    """建立/更新龙空 thread 标题索引"""
    
    total = len(range(start, end, step))
    print(f"扫描范围: {start}-{end} (步长{step}), 共{total}个")
    
    index = {}
    scanned = 0
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
        futs = {ex.submit(fetch_thread, tid): tid for tid in range(start, end, step)}
        for f in as_completed(futs):
            scanned += 1
            t = f.result()
            if t:
                index[str(t['tid'])] = {
                    "title": t['title'],
                    "posts_count": t['posts_count'],
                    "forum": t['forum'],
                    "text_preview": t['text'][:200]
                }
            if scanned % 500 == 0:
                print(f"  进度: {scanned}/{total} ({scanned*100//total}%), 索引: {len(index)}条")
    
    with open(INDEX_FILE, 'w') as f:
        json.dump({"updated": time.strftime("%Y-%m-%d %H:%M"), "total": len(index), "entries": index}, f, ensure_ascii=False, indent=2)
    print(f"✅ 索引保存: {INDEX_FILE} ({len(index)}条)")
    return index

def search_index(keyword):
    """在本地索引中搜索关键词"""
    if not os.path.exists(INDEX_FILE):
        print("⚠️ 索引不存在，先运行 build-index")
        return []
    
    with open(INDEX_FILE) as f:
        data = json.load(f)
    
    entries = data.get('entries', {})
    results = []
    for tid_str, info in entries.items():
        if keyword.lower() in info['title'].lower() or keyword.lower() in info.get('text_preview', '').lower():
            results.append((int(tid_str), info))
    return sorted(results, key=lambda x: -x[1].get('posts_count', 0))

def search_and_extract(keyword_or_tids, max_results=10):
    """全自动：接受关键词或 thread ID 列表 → 提取内容
    
    用法1: search_and_extract("诡秘之主") → WebSearch 发现 → 提取
    用法2: search_and_extract(["3025466", "3042256"]) → 直接提取
    """
    seen, threads = set(), []
    
    # 如果传入的是 thread ID 列表
    if isinstance(keyword_or_tids, list):
        for tid in keyword_or_tids:
            if str(tid) in seen: continue
            seen.add(str(tid))
            t = fetch_thread(int(tid))
            if t:
                threads.append(t)
                if len(threads) >= max_results: break
            time.sleep(0.3)
        return threads
    
    # 否则：关键词搜索
    keyword = keyword_or_tids
    
    # 路径A：AnySearch site:lkong.com
    try:
        import subprocess
        r = subprocess.run(["python",
            "/sessions/6a059e60ba447f17446893e8/workspace/cnovel-research/tools/anysearch/scripts/anysearch_cli.py",
            "search", f"site:lkong.com/thread {keyword}", "--max_results", str(max_results * 3)],
            capture_output=True, text=True, timeout=30)
        for tid in re.findall(r'lkong\.com/thread/(\d+)', r.stdout):
            if tid in seen: continue
            seen.add(tid)
            t = fetch_thread(int(tid))
            if t and keyword.lower() in (t.get('text','') + t.get('title','')).lower():
                threads.append(t)
                if len(threads) >= max_results: break
            time.sleep(0.3)
    except:
        pass
    
    # 路径B：Google dork（服务器直连，作为降级）
    if not threads:
        try:
            import urllib.request, urllib.parse
            query = urllib.parse.quote(f'site:lkong.com/thread {keyword}')
            req = urllib.request.Request(
                f'https://www.google.com/search?q={query}&num={max_results*3}',
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
            resp = urllib.request.urlopen(req, timeout=15).read().decode('utf-8', errors='ignore')
            for tid in re.findall(r'lkong\.com/thread/(\d+)', resp):
                if tid in seen: continue
                seen.add(tid)
                t = fetch_thread(int(tid))
                if t and keyword.lower() in (t.get('text','') + t.get('title','')).lower():
                    threads.append(t)
                    if len(threads) >= max_results: break
                time.sleep(0.3)
        except:
            pass
    
    return threads

def setup():
    """一次性环境检查：Playwright + 浏览器 + 龙空登录态"""
    print("🔍 检查环境...")
    
    # 1. Playwright
    try:
        from playwright.sync_api import sync_playwright
        print("  ✅ playwright 已安装")
    except ImportError:
        print("  ❌ playwright 未安装。请运行:")
        print("     pip install playwright --break-system-packages")
        print("     python -m playwright install chromium")
        return False
    
    # 2. 读龙空 Cookie
    print("  🧪 尝试读浏览器中 lkong.com 的登录态...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            cookies = context.cookies()
            browser.close()
            
            lkong_cookies = [c for c in cookies if 'lkong' in c.get('domain', '')]
            if lkong_cookies:
                print(f"  ✅ 检测到 {len(lkong_cookies)} 个龙空 Cookie，搜索功能可用")
                return True
            else:
                print("  ⚠️ 未检测到龙空 Cookie。")
                print("     可能是因为你还没在浏览器里登录过 lkong.com。")
                print("     搜索功能会自动降级到搜索引擎查找。")
                print("     降级模式下老书通常能搜到一些讨论，新书可能搜不到。")
                print("     如果你愿意，可以用浏览器打开 lkong.com 登录后再跑一次 setup。")
                return True  # 不是致命错误
    except Exception as e:
        print(f"  ⚠️ 无法启动浏览器 ({e})")
        print("     搜索功能会自动降级到搜索引擎查找。")
        return True  # 降级不是失败


# ── CLI ──────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("网文舆情 - 龙空采集器")
        print("")
        print("首次使用:")
        print("  python lkong_scraper.py setup             # 检查环境（一次性）")
        print("")
        print("日常使用:")
        print("  python lkong_scraper.py search <关键词>   # 搜索+提取")
        print("  python lkong_scraper.py extract <tid>      # 提取指定帖子")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "setup":
        setup()
    
    elif cmd == "search":
        keyword = sys.argv[2] if len(sys.argv) > 2 else input("搜索词: ")
        threads = search_and_extract(keyword)
        for t in threads:
            print(f"\n📌 [{t['tid']}] {t['title'][:80]}")
            print(f"   回复: {t['posts_count']}条 | 版块: {t['forum']}")
            print(f"   内容: {t['text'][:200]}")
        if not threads:
            print("未找到。可能的原因：")
            print("  1) 龙空确实没人讨论这本书")
            print("  2) 需要登录态搜（python lkong_scraper.py setup 确认）")
            print("  3) 书名太新，搜索引擎还没索引")
    elif cmd == "extract":
        tid = int(sys.argv[2])
        t = fetch_thread(tid)
        if t:
            print(f"标题: {t['title']}")
            print(f"回复: {t['posts_count']}条")
            print(f"正文: {t['text'][:500]}")
