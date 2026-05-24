#!/usr/bin/env python3
"""B站AI写作相关视频 + 评论全量采集"""
import requests, json, os, time, sys
sys.stdout.reconfigure(encoding='utf-8')

OUTPUT = "/sessions/6a059e60ba447f17446893e8/workspace/.workbuddy/bilibili_raw"
os.makedirs(OUTPUT, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.bilibili.com/",
}

QUERIES = [
    "AI写小说", "AI写作", "AI辅助写作", "AI润色",
    "DeepSeek写作", "AI小说", "番茄AI", "起点AI",
    "AI生成小说", "AI网文",
]

def search_videos(query, max_pages=3):
    """Search B站 for videos matching query"""
    all_videos = {}
    for page in range(1, max_pages + 1):
        try:
            r = requests.get("https://api.bilibili.com/x/web-interface/search/type",
                params={"search_type": "video", "keyword": query, "page": page},
                headers=HEADERS, timeout=15)
            data = r.json()
            results = data.get("data", {}).get("result", [])
            if not results:
                break
            for v in results:
                aid = str(v["aid"])
                if aid not in all_videos:
                    all_videos[aid] = {
                        "aid": v["aid"],
                        "bvid": v.get("bvid", ""),
                        "title": v.get("title", "").replace('<em class="keyword">','').replace('</em>',''),
                        "play": v.get("play", 0),
                        "video_review": v.get("video_review", 0),  # 弹幕
                        "comment": v.get("comment", 0),
                        "author": v.get("author", ""),
                        "description": (v.get("description", "") or "")[:500],
                        "query": query,
                    }
        except Exception as e:
            print(f"    p{page}: ❌ {e}", flush=True)
            break
        time.sleep(0.5)
    return all_videos

def get_comments(oid, max_pages=5):
    """Get comments for a video"""
    all_replies = []
    for page in range(max_pages):
        try:
            r = requests.get("https://api.bilibili.com/x/v2/reply/main",
                params={"oid": oid, "type": 1, "mode": 3, "next": page},
                headers=HEADERS, timeout=15)
            data = r.json()
            if data.get("code") != 0:
                break
            replies = data.get("data", {}).get("replies", [])
            if not replies:
                break
            for rp in replies:
                member = rp.get("member", {})
                content = rp.get("content", {})
                all_replies.append({
                    "author": member.get("uname", ""),
                    "content": content.get("message", ""),
                    "like": rp.get("like", 0),
                    "ctime": rp.get("ctime", 0),
                    "rcount": rp.get("rcount", 0),  # 子回复数
                })
            if len(replies) < 20:  # last page
                break
        except Exception as e:
            print(f"      ❌ {e}", flush=True)
            break
        time.sleep(0.3)
    return all_replies

all_videos = {}
for q in QUERIES:
    print(f"🔍 [{q}]", flush=True)
    vids = search_videos(q)
    for aid, v in vids.items():
        if aid not in all_videos:
            all_videos[aid] = v
    print(f"  +{len(vids)} (总{len(all_videos)})", flush=True)
    time.sleep(1)

print(f"\n📊 共 {len(all_videos)} 个视频", flush=True)

# Sort by engagement (comment count) and get comments for top videos
sorted_vids = sorted(all_videos.values(), key=lambda x: -x.get('comment', 0))
top_n = min(50, len(sorted_vids))

print(f"\n📄 获取前{top_n}个热门视频的评论...", flush=True)
for i, v in enumerate(sorted_vids[:top_n]):
    oid = v['aid']
    cc = v['comment']
    if cc == 0:
        continue
    print(f"  [{i+1}/{top_n}] [{cc}评] {v['title'][:50]}", flush=True)
    comments = get_comments(oid)
    all_videos[str(v['aid'])]['comments'] = comments
    print(f"    -> {len(comments)} 条评论", flush=True)
    time.sleep(0.5)

# Save
output_file = os.path.join(OUTPUT, "bilibili_ai_videos.json")
final = sorted(all_videos.values(), key=lambda x: -x.get('comment', 0))
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

total_comments = sum(len(v.get('comments', [])) for v in final)
total_plays = sum(v.get('play', 0) for v in final)
print(f"\n🎉 完成! {len(final)} 视频, {total_comments} 条评论, {total_plays/10000:.1f}万播放")
print(f"💾 保存到: {output_file}", flush=True)
