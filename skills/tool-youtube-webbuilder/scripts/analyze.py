#!/usr/bin/env python3
"""
tool-youtube-webbuilder - analyze.py
格式化抓取的频道数据，输出 agent 可分析的结构化 JSON。

不调用任何 API，只做数据处理。
输出: analysis_ready.json（给 agent 分析用）
"""

import json
import os
import re
import sys
from collections import Counter

def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_language_hint(texts):
    """根据视频标题判断语言倾向"""
    if not texts:
        return "unknown"
    cjk = 0
    latin = 0
    for t in texts:
        for ch in t[:50]:
            if '\u4e00' <= ch <= '\u9fff' or '\u3040' <= ch <= '\u30ff' or '\uac00' <= ch <= '\ud7af':
                cjk += 1
            elif ch.isalpha():
                latin += 1
    total = cjk + latin
    if total == 0:
        return "unknown"
    ratio = cjk / total
    if ratio > 0.4:
        return "chinese"  # 含中文、日文、韩文
    if latin > cjk * 2:
        return "english"
    return "bilingual"

def extract_tags(texts):
    """从标题和描述中提取关键词"""
    all_text = " ".join(texts).lower()
    # 简单关键词匹配
    niche_keywords = {
        "music": ["music", "song", "audio", "official", "video", "remix", "cover", "feat", "lyric"],
        "gaming": ["game", "gameplay", "playthrough", "walkthrough", "stream", "gaming"],
        "education": ["tutorial", "guide", "how to", "learn", "course", "lesson", "tips"],
        "tech": ["review", "unboxing", "tech", "setup", "gear", "camera"],
        "vlog": ["vlog", "day in", "my life", "daily", "routine"],
        "manifestation": ["显化", "吸引力", "显化", "财富", "心灵", "成长", "灵性", "冥想"],
        "entertainment": ["comedy", "funny", "prank", "challenge", "reaction"],
        "fitness": ["workout", "fitness", "gym", "exercise", "health"],
        "beauty": ["makeup", "skincare", "beauty", "fashion", "hair"],
        "cooking": ["recipe", "cook", "cooking", "food", "baking"],
        "travel": ["travel", "vlog", "adventure", "trip", "explore"],
    }
    
    tags = []
    for niche, keywords in niche_keywords.items():
        if any(kw in all_text for kw in keywords):
            tags.append(niche)
    
    return list(set(tags))

def analyze(data):
    """核心分析函数"""
    channel = data.get("channel", {})
    snippet = channel.get("snippet", channel)
    stats = channel.get("statistics", {})
    videos = data.get("videos", [])
    
    # 收集所有标题
    titles = [v.get("snippet", v).get("title", "") for v in videos]
    descriptions = [v.get("snippet", v).get("description", "")[:200] for v in videos]
    
    # 语言分析
    lang = extract_language_hint(titles)
    
    # 内容标签
    tags = extract_tags(titles + descriptions)
    
    # 频道描述摘要
    raw_desc = snippet.get("description", "")
    
    return {
        "channel_analysis": {
            "name": snippet.get("title", ""),
            "language": lang,
            "language_note": {
                "chinese": "主要面向中文受众，导航和标签使用中文",
                "english": "主要面向英文受众，导航和标签使用英文",
                "bilingual": "中英混用，需要统一语言",
                "unknown": "无法判断语言"
            }.get(lang, ""),
            "tags": tags,
            "tag_descriptions": {
                "music": "音乐/歌曲频道",
                "manifestation": "显化/心灵成长/吸引力法则",
                "education": "教育/教程",
                "gaming": "游戏",
                "tech": "科技",
                "vlog": "生活Vlog",
                "entertainment": "娱乐",
                "fitness": "健身",
                "beauty": "美妆",
                "cooking": "美食",
                "travel": "旅行",
            },
            "subscriber_count": stats.get("rawSubscriberCount", stats.get("subscriberCount", 0)),
            "video_count": stats.get("rawVideoCount", stats.get("videoCount", 0)),
            "view_count": stats.get("rawViewCount", stats.get("viewCount", 0)),
            "channel_description": raw_desc[:500] if raw_desc else "",
        },
        "video_analysis": {
            "total_videos": len(videos),
            "titles": titles[:12],
            "descriptions": descriptions[:6],
            "first_title": titles[0] if titles else "",
        },
        "analysis_prompt": """请根据以上频道数据分析，输出以下 JSON 格式的分析结论（只输出 JSON，不要其他文字）：

{
  "language": "chinese|english|bilingual",
  "nav_labels": ["首页", "作品", ...],
  "stat_labels": ["订阅者", "视频", "播放量"],
  "hero_tagline": "频道的一句话定位标语（非标题，是品牌定位）",
  "hero_description": "适合展示在首屏的简短品牌描述",
  "cta_text": "按钮文字（如'看作品 →'或'View Work'）",
  "footer_copyright_template": "版权声明格式",
  "style_notes": "对页面风格的建议（配色/字体/氛围），不超过50字",
  "key_themes": ["主题词1", "主题词2", "主题词3"],
  "audience": "目标受众描述（不超过20字）"
}
"""
    }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="tool-youtube-webbuilder - 频道数据分析准备")
    parser.add_argument("--data", required=True, help="data.json 路径")
    parser.add_argument("--out", default="analysis_ready.json", help="输出路径")
    args = parser.parse_args()
    
    raw = load_data(args.data)
    result = analyze(raw)
    
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"analysis ready: {args.out}")
    print(f"  Language: {result['channel_analysis']['language']}")
    print(f"  Tags: {', '.join(result['channel_analysis']['tags'])}")
    print(f"  Subscribers: {result['channel_analysis']['subscriber_count']}")
    print(f"  Analysis prompt ready for agent")

if __name__ == "__main__":
    main()
