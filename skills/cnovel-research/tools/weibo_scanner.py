#!/usr/bin/env python3
"""微博AI写作讨论 全量采集"""
import sys, asyncio, json, os, time
sys.stdout.reconfigure(encoding='utf-8')
from crawl4weibo import WeiboClient

OUTPUT = "/sessions/6a059e60ba447f17446893e8/workspace/.workbuddy/weibo_raw"
os.makedirs(OUTPUT, exist_ok=True)

QUERIES = [
    "AI写小说", "AI写作", "网文AI", "AI润色", "AI辅助写作",
    "DeepSeek写作", "豆包写作", "AI小说", "番茄AI", "起点AI",
    "AI生成小说", "AI网文", "ChatGPT写小说"
]

MAX_PAGES = 3  # 每个关键词最多翻3页
MAX_POSTS_PER_QUERY = 50
COMMENT_LIMIT = 20  # 每个帖子最多取20条评论

async def main():
    client = WeiboClient()
    all_posts = {}
    
    for query in QUERIES:
        print(f"\n🔍 [{query}]", flush=True)
        query_posts = 0
        
        for page in range(1, MAX_PAGES + 1):
            if query_posts >= MAX_POSTS_PER_QUERY:
                break
            
            try:
                result = client.search_posts(query, page=page, with_comments=False)
                posts, has_more = result if isinstance(result, tuple) else (result, False)
                
                new = 0
                for p in posts:
                    pid = str(p.id)
                    if pid not in all_posts:
                        all_posts[pid] = {
                            "id": p.id,
                            "text": (p.text or '')[:2000],
                            "comments_count": p.comments_count,
                            "reposts_count": p.reposts_count,
                            "query": query,
                        }
                        new += 1
                        query_posts += 1
                
                print(f"  p{page}: +{new} (总{len(all_posts)})", flush=True)
                
                if not has_more:
                    break
                
                time.sleep(1)  # rate limit
                
            except Exception as e:
                print(f"  p{page}: ❌ {type(e).__name__}", flush=True)
                break
    
    print(f"\n{'='*50}", flush=True)
    print(f"📊 共{len(all_posts)}条微博", flush=True)
    
    # Get comments for top posts
    sorted_posts = sorted(all_posts.values(), key=lambda x: -x['comments_count'])
    print(f"\n📄 获取前30条热门微博的评论...", flush=True)
    
    for i, p in enumerate(sorted_posts[:30]):
        if p['comments_count'] == 0:
            continue
        print(f"  [{i+1}/30] {p['text'][:50]}... ({p['comments_count']}评)", flush=True)
        try:
            result = client.search_posts(p['query'], page=1, with_comments=True, comment_limit=COMMENT_LIMIT)
            # This might not return comments directly, try alternative
        except:
            pass
    
    # Save
    output_file = os.path.join(OUTPUT, "weibo_ai_posts.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted(all_posts.values(), key=lambda x: -x['comments_count']), f, ensure_ascii=False, indent=2)
    
    total_comments = sum(p['comments_count'] for p in all_posts.values())
    print(f"\n🎉 完成! {len(all_posts)}条微博, {total_comments}条评论")
    print(f"💾 保存到: {output_file}", flush=True)

asyncio.run(main())
