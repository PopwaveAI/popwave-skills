#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pinterest 关键词搜索 → 参考图采集工具

基于 Bright Data Pinterest Scraper API。
异步触发搜索 → 轮询结果 → 下载图片 → 标准化输出 JSON。

用法:
    python pinterest_search.py "暗黑修仙封面" --limit 5 --download
    python pinterest_search.py "home office decor" --download --output-dir ./refs

环境变量:
  BRIGHTDATA_API_KEY - Bright Data API Key（已内置默认值，可通过环境变量覆盖）
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

import requests

# ── 配置 ──────────────────────────────────────────────
# 内置 API Key（环境变量优先）
DEFAULT_BRIGHTDATA_API_KEY = "dc0021db-1769-4887-b973-649afe2c1074"
BRIGHTDATA_API_KEY = os.environ.get("BRIGHTDATA_API_KEY") or DEFAULT_BRIGHTDATA_API_KEY

# dataset_id：Pinterest - Posts - Collects posts by specific keywords
DATASET_ID = "gd_lk0sjs4d21kdr7cnlv"

# API 端点
TRIGGER_URL = "https://api.brightdata.com/datasets/v3/trigger"
SNAPSHOT_URL = "https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}"

# 轮询间隔（秒）
POLL_INTERVAL = 10
# 最大等待时间（秒），超时则放弃
MAX_WAIT = 300

# 常见本地代理端口（Clash/v2ray/SS等），按优先级排列
FALLBACK_PROXY_PORTS = [7890, 7897, 1080, 10809, 10808, 8080]


# ── 代理自动检测 ────────────────────────────────────────

def detect_proxy() -> dict | None:
    """自动检测可用代理，返回 requests 格式的 proxies dict。

    检测顺序：
    1. 环境变量 HTTP_PROXY/HTTPS_PROXY
    2. Windows 注册表系统代理（trust_env 机制）
    3. 常见本地代理端口探测（Clash 7890 / v2ray 10809 等）
    返回 None 表示无代理（直连）。
    """
    # 1. 环境变量
    env_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") \
        or os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy") \
        or os.environ.get("ALL_PROXY") or os.environ.get("all_proxy")
    if env_proxy:
        print(f"[代理] 使用环境变量代理: {env_proxy}")
        return {"http": env_proxy, "https": env_proxy}

    # 2. Windows 注册表系统代理
    try:
        system_proxies = urllib.request.getproxies()
        if system_proxies:
            # getproxies() 返回 {'http': '...', 'https': '...'} 或 {'http': '...'}
            http_proxy = system_proxies.get("https") or system_proxies.get("http")
            if http_proxy:
                print(f"[代理] 使用系统代理: {http_proxy}")
                return {"http": http_proxy, "https": http_proxy}
    except Exception:
        pass

    # 3. 探测常见本地代理端口
    import socket
    for port in FALLBACK_PROXY_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex(("127.0.0.1", port))
            sock.close()
            if result == 0:
                proxy_url = f"http://127.0.0.1:{port}"
                print(f"[代理] 探测到本地代理: {proxy_url}")
                return {"http": proxy_url, "https": proxy_url}
        except Exception:
            continue

    print("[代理] 未检测到代理，使用直连")
    return None


# ── 核心流程 ────────────────────────────────────────────

def trigger_search(api_key: str, keyword: str, max_results: int = 20) -> str:
    """触发 Pinterest 关键词搜索，返回 snapshot_id。

    max_results: 限制 API 返回的结果数（从源头省额度，而非拉回来再截断）。
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    params = {
        "dataset_id": DATASET_ID,
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
        "limit_per_input": str(max_results),
    }
    data = [{"keyword": keyword}]

    resp = requests.post(TRIGGER_URL, headers=headers, params=params, json=data, timeout=30)

    if resp.status_code != 200:
        print(f"[触发失败] HTTP {resp.status_code}: {resp.text[:500]}")
        sys.exit(1)

    result = resp.json()
    snapshot_id = result.get("snapshot_id")
    if not snapshot_id:
        print(f"[触发失败] 响应无 snapshot_id: {result}")
        sys.exit(1)

    print(f"[已触发] snapshot_id = {snapshot_id}，结果上限 {max_results} 条")
    return snapshot_id


def poll_snapshot(api_key: str, snapshot_id: str) -> list:
    """轮询快照，返回结果列表。"""
    headers = {"Authorization": f"Bearer {api_key}"}
    url = SNAPSHOT_URL.format(snapshot_id=snapshot_id) + "?format=json"

    elapsed = 0
    while elapsed < MAX_WAIT:
        resp = requests.get(url, headers=headers, timeout=30)

        if resp.status_code == 200:
            data = resp.json()
            count = len(data) if isinstance(data, list) else 0
            print(f"[完成] 获取到 {count} 条结果（耗时 ~{elapsed}s）")
            return data
        elif resp.status_code == 202:
            print(f"[等待中] {elapsed}s... 结果未就绪，{POLL_INTERVAL}s 后重试")
        else:
            print(f"[轮询异常] HTTP {resp.status_code}: {resp.text[:300]}")
            sys.exit(1)

        time.sleep(POLL_INTERVAL)
        elapsed += POLL_INTERVAL

    print(f"[超时] 等待 {MAX_WAIT}s 后仍未完成，请稍后用 snapshot_id 手动查询")
    sys.exit(1)


# ── 数据标准化 ──────────────────────────────────────────

def normalize_pins(raw_results: list, keyword: str) -> list:
    """将 Bright Data 原始字段映射为统一 schema。"""
    pins = []
    for item in raw_results:
        # 跳过错误项 / 无图无效项
        if item.get("warning_code") == "dead_page":
            continue
        if not item.get("image_video_url"):
            continue

        pin = {
            "title": item.get("title", ""),
            "description": item.get("content", ""),
            "url": item.get("url", ""),
            "pin_id": item.get("post_id", ""),
            "image_url": item.get("image_video_url", ""),
            "user_name": item.get("user_name", ""),
            "user_url": item.get("user_url", ""),
            "followers": item.get("followers", 0),
            "hashtags": item.get("hashtags", []),
            "categories": item.get("categories", []),
            "date_posted": item.get("date_posted", ""),
            "post_type": item.get("post_type", ""),
            "comments_num": item.get("comments_num", 0),
            "search_keyword": keyword,
        }
        pins.append(pin)

    return pins


# ── 图片下载 ────────────────────────────────────────────

def download_images(pins: list, output_dir: Path, limit: int = 20, proxies: dict = None) -> list:
    """下载 pin 图片到本地，在 pin 字典里补充 image_local 字段。

    proxies: 代理配置（由 detect_proxy() 检测）。Pinterest CDN (i.pinimg.com)
    在国内被墙，必须走代理下载。传 None 则尝试直连（国内大概率失败）。
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    if proxies:
        print(f"[下载] 使用代理下载 Pinterest 图片")

    for pin in pins[:limit]:
        img_url = pin.get("image_url", "")
        if not img_url:
            continue

        pin_id = pin.get("pin_id", f"pin_{downloaded}")
        ext = ".jpg"
        if ".png" in img_url:
            ext = ".png"
        filename = f"pin_{pin_id}{ext}"
        filepath = output_dir / filename

        try:
            resp = requests.get(img_url, timeout=20, proxies=proxies)
            if resp.status_code == 200 and len(resp.content) > 1000:
                filepath.write_bytes(resp.content)
                pin["image_local"] = str(filepath)
                downloaded += 1
                print(f"  [下载 {downloaded}/{limit}] {filename} ({len(resp.content)//1024}KB)")
            else:
                print(f"  [跳过] pin_{pin_id} HTTP {resp.status_code} 或内容过小")
        except Exception as e:
            err_short = str(e)[:200]
            print(f"  [失败] pin_{pin_id}: {err_short}")

    print(f"[下载完成] {downloaded} 张图片 → {output_dir}")
    return pins


# ── 主入口 ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Pinterest 关键词搜索 → 参考图采集（基于 Bright Data API）"
    )
    parser.add_argument("keyword", help="搜索关键词，如 '暗黑修仙封面'")
    parser.add_argument("--limit", type=int, default=5, help="下载图片数量上限（默认 5）")
    parser.add_argument("--max-results", type=int, default=5, help="API 返回结果上限，控制额度消耗（默认 5）")
    parser.add_argument("--download", action="store_true", help="是否下载图片到本地")
    parser.add_argument(
        "--output-dir", default="./pinterest_refs",
        help="图片输出目录（默认 ./pinterest_refs）"
    )
    parser.add_argument(
        "--json-only", action="store_true",
        help="只输出标准化 JSON，不触发下载"
    )
    args = parser.parse_args()

    keyword = args.keyword
    print(f"\n{'='*60}")
    print(f"Pinterest 搜索：{keyword}")
    print(f"{'='*60}\n")

    # 1. 触发搜索（从源头限制结果数，省额度）
    snapshot_id = trigger_search(BRIGHTDATA_API_KEY, keyword, args.max_results)

    # 2. 轮询结果
    raw_results = poll_snapshot(BRIGHTDATA_API_KEY, snapshot_id)

    # 3. 标准化
    pins = normalize_pins(raw_results, keyword)
    print(f"[标准化] {len(pins)} 条有效结果")

    # 4. 输出 JSON
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"pinterest_{keyword.replace(' ', '_')}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(pins, f, ensure_ascii=False, indent=2)
    print(f"[JSON] 已保存 → {json_path}")

    # 5. 下载图片
    if args.download and not args.json_only:
        proxies = detect_proxy()
        pins = download_images(pins, output_dir, args.limit, proxies=proxies)
        # 更新 JSON（补充 image_local 字段）
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(pins, f, ensure_ascii=False, indent=2)

    # 6. 摘要
    print(f"\n{'='*60}")
    print(f"搜索完成：{keyword}")
    print(f"  有效结果：{len(pins)} 条")
    print(f"  JSON：{json_path}")
    if args.download:
        print(f"  图片目录：{output_dir}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
