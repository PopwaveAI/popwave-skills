#!/usr/bin/env python3
"""贴吧AI全量爬虫 — aiotieba已打补丁(HTTP)"""
import sys, asyncio, json, os
sys.stdout.reconfigure(encoding='utf-8')
import aiotieba

OUTPUT = "/sessions/6a059e60ba447f17446893e8/workspace/.workbuddy/tieba_raw"
os.makedirs(OUTPUT, exist_ok=True)

FORUMS = ["小说", "网文", "写小说", "变身嫁人小说", "番茄小说", "原创小说", "起点"]

AI_KWS = [
    'ai', '人工智能', 'deepseek', 'chatgpt', 'gpt', 'claude', '豆包', 'kimi',
    '蛙蛙', '星月', '笔灵', '智能体', '工作流', 'prompt', '提示词', '大模型',
    'ai味', 'ai辅助', 'ai写作', 'ai生成', 'ai文', '鉴ai', '去ai', 'ai检测',
    'ai判定', 'ai审核', 'ai泛滥', 'ai污染', 'ai封', 'coze', '元宝', '文心',
    '通义', 'ai工具', 'ai写', 'ai润', 'ai润色', 'ai修改', 'ai内容', 'ai小说',
    'ai稿', 'ai码', 'ai识别', 'ai审查', 'ai痕迹', 'ai特征', 'ai违规',
    'ai举报', 'ai封号', 'ai自证', 'ai溯源', 'ai标注', '中译中', 'AI', 'Ai',
]

def has_ai(text):
    return any(kw in text.lower() for kw in AI_KWS)

async def scan_forum(client, fname, pages=5):
    threads = {}
    for pn in range(1, pages + 1):
        try:
            th = await client.get_threads(fname, pn=pn, rn=50)
            if not th: break
        except: break
        for t in th:
            tid = str(t.tid)
            title = t.title or ''
            text = t.text or ''
            if has_ai(f"{title} {text}") and tid not in threads:
                threads[tid] = {"tid": t.tid, "title": title, "text": text[:2000], "reply_num": t.reply_num, "forum": fname}
        print(f"  {fname} p{pn}: +{len([k for k in threads if k not in threads])}AI", flush=True)
        await asyncio.sleep(0.3)
    return threads

async def get_replies(client, tid, max_pages=5):
    all_posts = []
    for pn in range(1, max_pages + 1):
        try:
            posts = await client.get_posts(tid, pn=pn, rn=30)
            if not posts: break
        except Exception as e:
            print(f"    get_posts p{pn} err: {e}", flush=True)
            break
        for p in posts:
            text = p.text or ''
            if text.strip():
                all_posts.append({"author_id": p.author_id, "text": text[:3000]})
        if len(posts) < 30: break
        await asyncio.sleep(0.3)
    return all_posts

async def main():
    client = aiotieba.Client()
    async with client:
        # Phase 1: Scan
        print("📋 Phase 1: 扫描各吧", flush=True)
        all_ai = {}
        for fname in FORUMS:
            ft = await scan_forum(client, fname)
            for tid, t in ft.items():
                if tid not in all_ai: all_ai[tid] = t
        print(f"📊 共{len(all_ai)}个AI帖子\n", flush=True)
        
        # Phase 2: Get replies  
        print("📄 Phase 2: 获取回复", flush=True)
        sorted_tids = sorted(all_ai.items(), key=lambda x: -x[1]['reply_num'])
        
        for i, (tid, t) in enumerate(sorted_tids):
            if t['reply_num'] < 1 or i >= 80:  # skip 0-reply and limit
                continue
            print(f"  [{i+1}/{min(len(sorted_tids), 80)}] {t['title'][:45]} ({t['reply_num']}回)", flush=True)
            replies = await get_replies(client, t['tid'])
            all_ai[tid]['replies'] = replies
            print(f"    -> {len(replies)}条", flush=True)
        
        # Save
        final = sorted(all_ai.values(), key=lambda x: -(x.get('reply_num', 0)))
        out = os.path.join(OUTPUT, "tieba_ai_full.json")
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(final, f, ensure_ascii=False, indent=2)
        
        total_replys = sum(len(t.get('replies', [])) for t in final)
        print(f"\n🎉 完成! {len(final)}话题 {total_replys}回复", flush=True)

asyncio.run(main())
