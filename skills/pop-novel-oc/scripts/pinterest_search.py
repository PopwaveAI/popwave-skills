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

# Web Unlocker API 端点（用 Bright Data 服务器代理下载，不需要本地VPN）
WEB_UNLOCKER_URL = "https://api.brightdata.com/request"
# Web Unlocker zone 名称（在 Bright Data 后台创建，环境变量可覆盖）
DEFAULT_UNLOCKER_ZONE = "web_unlocker1"
UNLOCKER_ZONE = os.environ.get("BRIGHTDATA_UNLOCKER_ZONE") or DEFAULT_UNLOCKER_ZONE


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


# ── 图片下载（三层fallback）─────────────────────────────

def _download_via_proxy(img_url: str, proxies: dict = None, timeout: int = 20) -> bytes | None:
    """Layer 1: 通过本地代理直连下载。成功返回bytes，失败返回None。"""
    try:
        resp = requests.get(img_url, timeout=timeout, proxies=proxies)
        if resp.status_code == 200 and len(resp.content) > 1000:
            return resp.content
    except Exception:
        pass
    return None


def _download_via_unlocker(img_url: str, api_key: str, zone: str, timeout: int = 30) -> bytes | None:
    """Layer 2: 通过 Bright Data Web Unlocker API 下载（不需本地VPN）。

    用 Bright Data 的服务器做代理转发，绕过国内GFW。
    需要在 Bright Data 后台创建名为 zone 的 Web Unlocker zone。
    """
    try:
        resp = requests.post(
            WEB_UNLOCKER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "zone": zone,
                "url": img_url,
                "format": "raw",
            },
            timeout=timeout,
        )
        if resp.status_code == 200 and len(resp.content) > 1000:
            return resp.content
        elif resp.status_code == 400 and "not found" in resp.text.lower():
            print(f"  [Web Unlocker] zone '{zone}' 不存在，请在 Bright Data 后台创建 Web Unlocker zone")
    except Exception:
        pass
    return None


def download_images(pins: list, output_dir: Path, limit: int = 20,
                    proxies: dict = None, api_key: str = None,
                    unlocker_zone: str = None) -> list:
    """下载 pin 图片到本地，在 pin 字典里补充 image_local 字段。

    三层 fallback 策略：
      Layer 1: 本地代理直连（免费，快，需要VPN/Clash）
      Layer 2: Bright Data Web Unlocker API（付费，不需VPN，需创建zone）
      Layer 3: 优雅降级（跳过下载，保留 image_url 在JSON中）

    proxies:       detect_proxy() 检测到的本地代理
    api_key:       Bright Data API Key（用于 Web Unlocker fallback）
    unlocker_zone: Bright Data Web Unlocker zone 名称
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    failed_count = 0
    layer1_hits = 0
    layer2_hits = 0

    use_unlocker = bool(api_key and unlocker_zone)
    if proxies:
        print(f"[下载] Layer 1 (本地代理) 可用")
    if use_unlocker:
        print(f"[下载] Layer 2 (Web Unlocker zone={unlocker_zone}) 可用作为fallback")

    if not proxies and not use_unlocker:
        print("[下载] ⚠ 无本地代理且未配置Web Unlocker，图片将无法下载")
        print("[下载]   → 建议方案：1) 开启VPN/Clash  2) 在Bright Data后台创建Web Unlocker zone")
        print("[下载]   → 当前仅保存图片URL到JSON，不下载图片文件")

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

        content = None
        source = ""

        # Layer 1: 本地代理
        if proxies:
            content = _download_via_proxy(img_url, proxies=proxies)
            if content:
                source = "proxy"

        # Layer 2: Bright Data Web Unlocker
        if not content and use_unlocker:
            content = _download_via_unlocker(img_url, api_key, unlocker_zone)
            if content:
                source = "unlocker"

        # 写入文件
        if content:
            filepath.write_bytes(content)
            pin["image_local"] = str(filepath)
            pin["download_method"] = source
            downloaded += 1
            if source == "proxy":
                layer1_hits += 1
            elif source == "unlocker":
                layer2_hits += 1
            print(f"  [下载 {downloaded}/{limit}] {filename} ({len(content)//1024}KB via {source})")
        else:
            failed_count += 1
            print(f"  [跳过] pin_{pin_id} 所有下载方式失败，URL已保留在JSON中")

    print(f"[下载完成] {downloaded} 张图片 → {output_dir}")
    if downloaded > 0:
        print(f"  Layer 1 (本地代理): {layer1_hits} 张 | Layer 2 (Web Unlocker): {layer2_hits} 张")
    if failed_count > 0:
        print(f"  ⚠ {failed_count} 张图片下载失败（URL已保留，可用浏览器手动打开）")
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

    # 5. 下载图片（三层fallback: 本地代理 → Web Unlocker → 优雅降级）
    if args.download and not args.json_only:
        proxies = detect_proxy()
        pins = download_images(
            pins, output_dir, args.limit,
            proxies=proxies,
            api_key=BRIGHTDATA_API_KEY,
            unlocker_zone=UNLOCKER_ZONE,
        )
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
