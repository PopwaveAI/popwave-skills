#!/usr/bin/env python3
"""
Bilibili 视频字幕获取器 — Phase A (B站数据源)
==============================================

功能：
  给定 B 站视频 URL/BV号，获取字幕 JSON + 元信息，输出结构化上下文包。
  支持直连和 CDP 两条路径：
    - 直连 API（快速路径，适用于有 CC 字幕的视频）
    - CDP fallback（通过已登录 Chrome 获取需要登录的 AI 字幕）

用法：
  单集获取：  py bili_subtitle.py "https://www.bilibili.com/video/BVxxxxxx"
  批量获取：  py bili_subtitle.py --batch urls.txt
  仅JSON：    py bili_subtitle.py "BVxxxxxx" --json-only

输出：
  - 原文/ 目录下生成字幕上下文包（.json），供 AI 清洗为文章
  - 清洗由大模型完成（脚本不承担清洗逻辑）

API 调用链：
  view API  →  x/web-interface/view?bvid=    →  aid, cid, title, owner
  player API → x/player/v2?aid=&cid=          →  subtitle URLs (直连)
  player API → CDP fetch with login           →  subtitle URLs (CDP)
  subtitle URL → JSON subtitle body (auth_key 直接可访问)
"""
import json
import os
import sys
import time
import re
import urllib.request
import urllib.parse
from typing import Optional, List, Dict

# ── CDP 常量 ─────────────────────────────────────────────────────
CDP_BASE = "http://localhost:3456"


class BilibiliSubtitleFetcher:
    """B站视频字幕获取器"""

    BASE_VIEW = "https://api.bilibili.com/x/web-interface/view"
    BASE_PLAYER = "https://api.bilibili.com/x/player/v2"

    def __init__(self, output_dir: str = "./articles"):
        self.output_dir = output_dir
        self.yuanwen_dir = os.path.join(output_dir, "原文")
        os.makedirs(self.yuanwen_dir, exist_ok=True)

    # ── 工具 ──────────────────────────────────────────────────────

    @staticmethod
    def _extract_bvid(url_or_bvid: str) -> Optional[str]:
        m = re.match(r'^BV[A-Za-z0-9]{10,}$', url_or_bvid.strip())
        if m:
            return m.group(0)
        m = re.search(r'BV[A-Za-z0-9]{10,}', url_or_bvid)
        if m:
            return m.group(0)
        m = re.search(r'b23\.tv/\w+', url_or_bvid)
        if m:
            return None
        return None

    @staticmethod
    def _clean_title(title: str) -> str:
        return re.sub(r'[\\/*?:"<>|]', "", title)[:80]

    # ── HTTP 工具 ─────────────────────────────────────────────────

    def _api_get(self, url: str, timeout: int = 15) -> dict:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com/",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # ── CDP 工具 ──────────────────────────────────────────────────

    @staticmethod
    def _cdp_get(path: str, timeout: int = 30) -> str:
        url = f"{CDP_BASE}{path}"
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.read().decode("utf-8").strip()

    @staticmethod
    def _cdp_post(path: str, body: str, timeout: int = 30) -> str:
        url = f"{CDP_BASE}{path}"
        data = body.encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "text/plain")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8").strip()

    @staticmethod
    def _cdp_unwrap(raw: str) -> str:
        if raw.startswith("{"):
            try:
                obj = json.loads(raw)
                if "value" in obj: return obj["value"]
                if "targetId" in obj: return obj["targetId"]
                return str(obj.get("success", raw))
            except: pass
        return raw.strip()

    def _cdp_eval(self, target_id: str, js: str) -> str:
        raw = self._cdp_post(f"/eval?target={target_id}", js, timeout=30)
        return self._cdp_unwrap(raw)

    # ── API 调用 ──────────────────────────────────────────────────

    def get_video_info(self, bvid: str) -> dict:
        url = f"{self.BASE_VIEW}?bvid={bvid}"
        data = self._api_get(url)
        if data.get("code") != 0:
            raise Exception(f"B站API错误: {data.get('message', '未知错误')}")
        vinfo = data["data"]
        return {
            "bvid": bvid,
            "aid": vinfo.get("aid"),
            "cid": vinfo["cid"] if isinstance(vinfo.get("cid"), int) else (vinfo.get("pages") or [{}])[0].get("cid"),
            "title": vinfo.get("title", ""),
            "owner": vinfo.get("owner", {}).get("name", ""),
            "publish_date": vinfo.get("pubdate", 0),
            "views": vinfo.get("stat", {}).get("view", 0),
            "tags": [t.get("tag_name", "") for t in (vinfo.get("tagname", []) if isinstance(vinfo.get("tagname"), list) else [])],
            "description": vinfo.get("desc", ""),
            "pic": vinfo.get("pic", ""),
        }

    def get_subtitle_direct(self, aid: int, cid: int) -> dict:
        """直连 API 获取字幕信息，返回 {"subtitles": [...], "need_login": bool}"""
        url = f"{self.BASE_PLAYER}?aid={aid}&cid={cid}"
        data = self._api_get(url)
        if data.get("code") != 0:
            raise Exception(f"player API错误: {data.get('message', '未知错误')}")
        sub_info = data.get("data", {}).get("subtitle", {})
        need_login = data.get("data", {}).get("need_login_subtitle", False)
        return {
            "subtitles": sub_info.get("subtitles", []),
            "need_login": need_login,
        }

    def get_subtitle_via_cdp(self, aid: int, cid: int, bvid: str) -> Optional[str]:
        """通过 CDP + 已登录 Chrome 获取字幕 URL"""
        # 开新 tab 到视频页
        target = self._cdp_unwrap(
            self._cdp_get(f"/new?url=https://www.bilibili.com/video/{bvid}")
        )
        time.sleep(3)

        js = f"""
(async function() {{
try {{
    let resp = await fetch('{self.BASE_PLAYER}?aid={aid}&cid={cid}', {{
        credentials:'include',
        headers:{{'Referer':'https://www.bilibili.com/video/{bvid}'}}
    }});
    let d = await resp.json();
    let subs = d.data?.subtitle?.subtitles || [];
    if(subs.length === 0) return 'NO_SUBS';
    // 优先选中文
    for(let s of subs) {{
        if(s.lan_doc && s.lan_doc.indexOf('中文') > -1) {{
            return s.subtitle_url;
        }}
    }}
    return subs[0].subtitle_url;
}} catch(e) {{ return 'ERROR: ' + e.message; }}
}})()
"""
        result = self._cdp_eval(target, js)
        # 关 tab
        try: self._cdp_get(f"/close?target={target}", timeout=5)
        except: pass
        return result if result not in ("NO_SUBS", "") else None

    def fetch_subtitle_body(self, subtitle_url: str) -> List[Dict]:
        if not subtitle_url.startswith("http"):
            subtitle_url = f"https:{subtitle_url}"
        data = self._api_get(subtitle_url)
        return data.get("body", [])

    # ── 核心流程 ──────────────────────────────────────────────────

    def build_context_package(self, url_or_bvid: str) -> dict:
        """构建可供 AI 清洗的结构化上下文包"""
        bvid = self._extract_bvid(url_or_bvid)
        if not bvid:
            raise ValueError(f"无法提取BV号: {url_or_bvid}")

        # Step 1: 视频元信息
        vinfo = self.get_video_info(bvid)
        aid = vinfo["aid"]
        cid = vinfo["cid"]

        # Step 2: 尝试直连获取字幕
        direct = self.get_subtitle_direct(aid, cid)
        subtitle_url = None
        subtitle_lan = ""

        if direct["subtitles"]:
            # 直连成功（通常是有 CC 字幕的视频）
            for s in direct["subtitles"]:
                if "中文" in s.get("lan_doc", ""):
                    subtitle_url = s.get("subtitle_url", "")
                    subtitle_lan = s.get("lan_doc", "")
                    break
            if not subtitle_url and direct["subtitles"]:
                subtitle_url = direct["subtitles"][0].get("subtitle_url", "")
                subtitle_lan = direct["subtitles"][0].get("lan_doc", "")

        # Step 3: 直连没拿到, 且 need_login → CDP fallback
        if not subtitle_url and direct["need_login"]:
            print(f"  ⏳ 直连无字幕, 通过 CDP 获取...")
            cdp_url = self.get_subtitle_via_cdp(aid, cid, bvid)
            if cdp_url:
                subtitle_url = cdp_url
                subtitle_lan = "中文 (AI)"

        # Step 4: 获取字幕正文
        subtitle_body = []
        if subtitle_url:
            subtitle_body = self.fetch_subtitle_body(subtitle_url)

        # Step 5: 组装上下文包
        context = {
            "bvid": bvid,
            "aid": aid,
            "cid": cid,
            "title": vinfo["title"],
            "author": vinfo["owner"],
            "platform": "bilibili",
            "publish_date": vinfo["publish_date"],
            "views": vinfo["views"],
            "tags": vinfo["tags"],
            "description": vinfo["description"],
            "pic": vinfo["pic"],
            "subtitle_language": subtitle_lan,
            "subtitle_count": len(subtitle_body),
            "subtitle_body": subtitle_body,
            "source_url": f"https://www.bilibili.com/video/{bvid}",
        }
        return context

    def save_context(self, context: dict) -> str:
        clean = self._clean_title(context["title"])
        path = os.path.join(self.yuanwen_dir, f"{clean}_字幕原始数据.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(context, f, ensure_ascii=False, indent=2)
        return path

    def download(self, url_or_bvid: str) -> str:
        banner = "=" * 56
        print(f"\n{banner}")
        print(f"  B站字幕获取")
        print(f"{banner}")
        print(f"  URL: {url_or_bvid}")

        bvid = self._extract_bvid(url_or_bvid)
        if not bvid:
            print(f"  ❌ 无法提取BV号")
            return ""

        try:
            context = self.build_context_package(url_or_bvid)
            clean = self._clean_title(context["title"])
            saved_path = self.save_context(context)

            print(f"  ✅ 标题: {context['title'][:60]}")
            print(f"  ✅ UP主: {context['author']}")
            print(f"  ✅ 字幕: {context['subtitle_count']} 条 ({context['subtitle_language']})")
            print(f"  📄 已保存: {saved_path}")
            print(f"{banner}")

            print(f"\n{'=' * 56}")
            print(f"  ⏳ 等待 AI 清洗字幕 → 文章")
            print(f"  {'=' * 56}")
            print(f"\n📄 字幕原始数据: {saved_path}")
            print(f"🧠 即将生成: {self.yuanwen_dir}/{clean}.md")
            print(f"\n任务：读取字幕 JSON，清洗为连贯可读的文章，保存到原文目录。\n")

            return saved_path
        except Exception as e:
            print(f"  ❌ 获取失败: {e}")
            return ""


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Bilibili 视频字幕获取器 — Phase A (B站数据源)"
    )
    parser.add_argument("url", nargs="?", help="B站视频 URL 或 BV 号")
    parser.add_argument("--output", "-o", default="./articles", help="输出目录")
    parser.add_argument("--batch", metavar="URLS_FILE", help="批量模式：从文本文件读取 URL")
    parser.add_argument("--json-only", action="store_true", help="仅输出上下文 JSON 到 stdout")
    parser.add_argument("--no-cdp", action="store_true", help="禁用 CDP fallback，仅直连")

    args = parser.parse_args()

    if not args.url and not args.batch:
        parser.print_help()
        sys.exit(0)

    fetcher = BilibiliSubtitleFetcher(output_dir=args.output)

    # 批量模式
    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
        seen = set()
        unique = []
        for u in urls:
            if u not in seen:
                seen.add(u)
                unique.append(u)
        print(f"\n批量获取: {len(unique)} 个视频（已去重）")
        for i, url in enumerate(unique, 1):
            print(f"\n{'─' * 48}")
            print(f"  [{i}/{len(unique)}]")
            fetcher.download(url)
            if i < len(unique):
                time.sleep(1)
        sys.exit(0)

    # 单篇
    if args.json_only:
        context = fetcher.build_context_package(args.url)
        print(json.dumps(context, ensure_ascii=False, indent=2))
        sys.exit(0)

    fetcher.download(args.url)


if __name__ == "__main__":
    main()
