#!/usr/bin/env python3
"""
pop-YouTubewebbuilder — fetch_youtube.py
通过 YouTube Data API v3 抓取频道信息和最新视频，保存为 JSON。

用法：
    python scripts/fetch_youtube.py --api-key "KEY" --channel-url "https://www.youtube.com/@handle"
    python scripts/fetch_youtube.py --api-key "KEY" --channel-id "UC_xxxxx"
    python scripts/fetch_youtube.py --api-key "KEY" --channel-name "频道名称"
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from urllib.request import urlopen, Request, build_opener, ProxyHandler, install_opener
from urllib.parse import urlencode, quote
from urllib.error import HTTPError

YT_API_BASE = "https://www.googleapis.com/youtube/v3"

# ── 代理自动检测 ──────────────────────────────────────
def setup_proxy():
    """
    自动检测 HTTP_PROXY / HTTPS_PROXY 环境变量，安装到 urllib。
    在 Clash / V2Ray / 系统代理 环境下生效。
    """
    proxy_vars = [
        os.environ.get("HTTPS_PROXY"),
        os.environ.get("https_proxy"),
        os.environ.get("HTTP_PROXY"),
        os.environ.get("http_proxy"),
    ]
    proxy_url = next((p for p in proxy_vars if p), None)
    if proxy_url:
        print(f"[PROXY] 检测到代理: {proxy_url}", file=sys.stderr)
        handler = ProxyHandler({
            "http": proxy_url,
            "https": proxy_url,
        })
        opener = build_opener(handler)
        install_opener(opener)
        return True
    return False


# ── 自动读取 API Key ────────────────────────────────────
def resolve_api_key(provided=None):
    """按优先级获取 API Key: 参数 > config.json"""
    if provided:
        return provided
    # 尝试从 config.json 读取
    cfg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            key = cfg.get("youtube_api_key", "")
            if key and len(key) > 10:
                print("[INFO] 从 config.json 读取 YouTube API Key", file=sys.stderr)
                return key
        except Exception:
            pass
    print("[ERR] 未找到 API Key。请通过 --api-key 参数提供，或在 config.json 中配置 youtube_api_key。",
          file=sys.stderr)
    sys.exit(1)


def api_request(url):
    """发送 HTTP GET 请求并返回 JSON 响应"""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        print(f"  [YT] 请求: {url[:80]}...", file=sys.stderr)
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"[ERR] API 请求失败 [{e.code}]: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # 如果直接请求失败且未检测到代理，提示用户配置代理
        err_msg = str(e)
        if "timed out" in err_msg.lower() or "connection refused" in err_msg.lower() or "connect" in err_msg.lower():
            print(f"[NET] 网络连接失败: {err_msg}", file=sys.stderr)
            print("[TIP] 如果在中国大陆，你可能需要配置 HTTP_PROXY 代理", file=sys.stderr)
            print("   例如: set HTTP_PROXY=http://127.0.0.1:7890", file=sys.stderr)
            print("   或者: $env:HTTP_PROXY='http://127.0.0.1:7890'", file=sys.stderr)
        sys.exit(1)


def format_number(n):
    """友好格式化数字：1000 → 1,000 / 10000 → 1万 / 100000000 → 1亿"""
    try:
        n = int(n)
    except (ValueError, TypeError):
        return str(n)
    if n >= 100000000:
        return f"{n / 100000000:.1f}亿"
    elif n >= 10000:
        return f"{n / 10000:.1f}万"
    else:
        return f"{n:,}"


def parse_duration(iso_duration):
    """将 ISO 8601 时长 (PT10M30S) 转为可读格式"""
    import re
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso_duration)
    if not match:
        return iso_duration
    h, m, s = [int(g) if g else 0 for g in match.groups()]
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    else:
        return f"{m}:{s:02d}"


def time_ago(iso_str):
    """返回相对时间文字（如 '3天前', '1个月前'）"""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta = now - dt
        days = delta.days
        if days < 1:
            hours = delta.seconds // 3600
            return f"{hours}小时前" if hours else "刚刚"
        elif days < 30:
            return f"{days}天前"
        elif days < 365:
            return f"{days // 30}个月前"
        else:
            return f"{days // 365}年前"
    except Exception:
        return iso_str


def get_channel_by_handle(api_key, handle):
    """通过频道 handle (例如 @channelname) 查找频道"""
    handle = handle.strip().lstrip("@")
    url = f"{YT_API_BASE}/search?part=snippet&type=channel&q={quote(handle)}&key={api_key}&maxResults=1"
    data = api_request(url)
    items = data.get("items", [])
    if not items:
        print(f"[ERR] 未找到频道: @{handle}", file=sys.stderr)
        sys.exit(1)
    channel_id = items[0]["snippet"]["channelId"]
    print(f"[OK] 通过 handle 找到频道: {items[0]['snippet']['title']} ({channel_id})")
    return channel_id


def get_channel_by_name(api_key, name):
    """通过频道名称搜索频道"""
    url = f"{YT_API_BASE}/search?part=snippet&type=channel&q={quote(name)}&key={api_key}&maxResults=1"
    data = api_request(url)
    items = data.get("items", [])
    if not items:
        print(f"[ERR] 未找到频道: {name}", file=sys.stderr)
        sys.exit(1)
    channel_id = items[0]["snippet"]["channelId"]
    print(f"[OK] 搜索到频道: {items[0]['snippet']['title']} ({channel_id})")
    return channel_id


def get_channel_info(api_key, channel_id):
    """获取频道详细信息（统计 + 品牌信息）"""
    url = (f"{YT_API_BASE}/channels?part=snippet,statistics,brandingSettings"
           f"&id={channel_id}&key={api_key}")
    data = api_request(url)
    items = data.get("items", [])
    if not items:
        print(f"[ERR] 未找到频道 ID: {channel_id}", file=sys.stderr)
        sys.exit(1)
    return items[0]


def get_latest_videos(api_key, channel_id, max_results=12):
    """获取频道最新视频列表"""
    # 先获取上传播放列表 ID
    channel_url = (f"{YT_API_BASE}/channels?part=contentDetails"
                   f"&id={channel_id}&key={api_key}")
    channel_data = api_request(channel_url)
    items = channel_data.get("items", [])
    if not items:
        return []
    uploads_id = items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # 获取播放列表中的视频
    playlist_url = (f"{YT_API_BASE}/playlistItems?part=snippet,contentDetails"
                    f"&playlistId={uploads_id}&key={api_key}&maxResults={max_results}")
    playlist_data = api_request(playlist_url)
    video_items = playlist_data.get("items", [])

    if not video_items:
        return []

    # 获取每个视频的统计信息
    video_ids = [item["contentDetails"]["videoId"] for item in video_items]
    video_stats_url = (f"{YT_API_BASE}/videos?part=statistics,contentDetails,snippet"
                       f"&id={','.join(video_ids)}&key={api_key}")
    stats_data = api_request(video_stats_url)
    stats_map = {}
    for item in stats_data.get("items", []):
        stats_map[item["id"]] = item

    # 组装最终数据
    videos = []
    for item in video_items:
        vid = item["contentDetails"]["videoId"]
        snippet = item["snippet"]
        stats_item = stats_map.get(vid, {})
        statistics = stats_item.get("statistics", {})
        content_details = stats_item.get("contentDetails", {})
        videos.append({
            "id": vid,
            "title": snippet.get("title", ""),
            "description": snippet.get("description", "")[:200],
            "publishedAt": snippet.get("publishedAt", ""),
            "thumbnails": snippet.get("thumbnails", {}),
            "duration": parse_duration(content_details.get("duration", "PT0S")),
            "statistics": {
                "viewCount": format_number(statistics.get("viewCount", 0)),
                "likeCount": format_number(statistics.get("likeCount", 0)),
                "commentCount": format_number(statistics.get("commentCount", 0)),
            },
            "timeAgo": time_ago(snippet.get("publishedAt", "")),
            "url": f"https://www.youtube.com/watch?v={vid}",
        })
    return videos


def resolve_channel_url(url):
    """从 YouTube 频道 URL 中提取 handle 或 channel ID"""
    url = url.strip()
    # https://www.youtube.com/@handle
    if "/@" in url:
        handle = url.split("/@")[-1].split("/")[0].split("?")[0]
        return "handle", handle
    # https://www.youtube.com/channel/UC_xxx
    if "/channel/" in url:
        cid = url.split("/channel/")[-1].split("/")[0].split("?")[0]
        return "id", cid
    # https://www.youtube.com/c/customname
    if "/c/" in url:
        cname = url.split("/c/")[-1].split("/")[0].split("?")[0]
        return "custom", cname
    # @handle 直接输入
    if url.startswith("@"):
        return "handle", url[1:]
    return None, None


def find_social_links(description):
    """从频道描述中提取社交媒体链接"""
    import re
    links = []
    patterns = [
        (r'(https?://(?:www\.)?twitter\.com/\S+)', 'Twitter / X'),
        (r'(https?://(?:www\.)?instagram\.com/\S+)', 'Instagram'),
        (r'(https?://(?:www\.)?facebook\.com/\S+)', 'Facebook'),
        (r'(https?://(?:www\.)?github\.com/\S+)', 'GitHub'),
        (r'(https?://(?:www\.)?tiktok\.com/\S+)', 'TikTok'),
        (r'(https?://(?:www\.)?twitch\.tv/\S+)', 'Twitch'),
        (r'(https?://discord\.(?:gg|com)/\S+)', 'Discord'),
        (r'(https?://(?:www\.)?patreon\.com/\S+)', 'Patreon'),
        (r'(https?://(?:www\.)?bilibili\.com/\S+)', 'Bilibili'),
        (r'(https?://(?:www\.)?weibo\.com/\S+)', '微博'),
        (r'(https?://(?:www\.)?xiaohongshu\.com/\S+)', '小红书'),
        (r'(https?://(?:www\.)?zhihu\.com/\S+)', '知乎'),
    ]
    seen = set()
    for pattern, platform in patterns:
        for match in re.finditer(pattern, description, re.IGNORECASE):
            url = match.group(1).rstrip("/.,;:")
            if url not in seen:
                seen.add(url)
                links.append({"platform": platform, "url": url})
    return links


def main():
    parser = argparse.ArgumentParser(description="YouTube 频道信息抓取工具")
    parser.add_argument("--api-key", help="YouTube Data API v3 Key（默认从 config.json 读取）")
    parser.add_argument("--channel-url", help="YouTube 频道链接 (https://www.youtube.com/@handle)")
    parser.add_argument("--channel-id", help="YouTube 频道 ID (UC_xxxxx)")
    parser.add_argument("--channel-name", help="频道名称（自动搜索）")
    parser.add_argument("--out", default="data.json", help="输出 JSON 文件路径")
    parser.add_argument("--max-videos", type=int, default=12, help="最多获取视频数 (默认12)")
    args = parser.parse_args()

    api_key = resolve_api_key(args.api_key)
    setup_proxy()  # 自动检测代理环境变量
    start_time = time.time()

    # 确定频道 ID
    channel_id = None
    if args.channel_id:
        channel_id = args.channel_id
        print(f"[YT] 使用频道 ID: {channel_id}")
    elif args.channel_url:
        mode, value = resolve_channel_url(args.channel_url)
        if mode == "handle":
            channel_id = get_channel_by_handle(api_key, value)
        elif mode == "id":
            channel_id = value
            print(f"[YT] 使用频道 ID: {channel_id}")
        elif mode == "custom":
            channel_id = get_channel_by_name(api_key, value)
    elif args.channel_name:
        channel_id = get_channel_by_name(api_key, args.channel_name)
    else:
        print("[ERR] 请提供 --channel-url、--channel-id 或 --channel-name 之一", file=sys.stderr)
        sys.exit(1)

    # 获取频道信息
    print("[YT] 正在获取频道信息...")
    raw = get_channel_info(api_key, channel_id)
    snippet = raw.get("snippet", {})
    statistics = raw.get("statistics", {})
    branding = raw.get("brandingSettings", {})

    # 提取 banner URL
    banner_url = None
    if "brandingSettings" in raw:
        img = raw["brandingSettings"].get("image", {})
        banner_url = img.get("bannerExternalUrl")

    # 提取社交链接
    desc = snippet.get("description", "")
    social_links = find_social_links(desc)

    channel_data = {
        "id": channel_id,
        "title": snippet.get("title", "未知频道"),
        "description": desc,
        "customUrl": snippet.get("customUrl", ""),
        "publishedAt": snippet.get("publishedAt", ""),
        "country": snippet.get("country", ""),
        "thumbnails": snippet.get("thumbnails", {}),
        "bannerUrl": banner_url,
        "statistics": {
            "viewCount": format_number(statistics.get("viewCount", 0)),
            "subscriberCount": format_number(statistics.get("subscriberCount", 0)),
            "videoCount": format_number(statistics.get("videoCount", 0)),
            "rawViewCount": int(statistics.get("viewCount", 0)),
            "rawSubscriberCount": int(statistics.get("subscriberCount", 0)),
            "rawVideoCount": int(statistics.get("videoCount", 0)),
        },
        "socialLinks": social_links,
    }

    # 获取最新视频
    print(f"[YT] 正在获取最新 {args.max_videos} 个视频...")
    videos = get_latest_videos(api_key, channel_id, args.max_videos)

    # 构建最终数据
    result = {
        "channel": channel_data,
        "videos": videos,
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
        "totalVideos": len(videos),
    }

    # 写入文件
    out_path = args.out
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - start_time
    print(f"\n[OK] 完成！耗时 {elapsed:.1f}秒")
    print(f"   频道: {channel_data['title']}")
    print(f"   订阅: {channel_data['statistics']['subscriberCount']}")
    print(f"   视频: {len(videos)} 个")
    print(f"   输出: {os.path.abspath(out_path)}")


if __name__ == "__main__":
    main()
