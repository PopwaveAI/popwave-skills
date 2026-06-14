#!/usr/bin/env python3
"""
知识获取器 — Phase A（微信数据源）
=====================================
通过 CDP Proxy 操控已登录的 Chrome 下载微信公众号文章。

用法：
  单篇下载：  py downloader.py "https://mp.weixin.qq.com/s/xxxxx"
  专辑下载：  py downloader.py "专辑链接" --album
  批量下载：  py downloader.py --batch urls.txt
"""
import json
import re
import os
import sys
import time
import glob
import base64
import urllib.request
import urllib.parse
from typing import List, Dict, Optional


class WechatArticleDownloader:
    """微信公众号文章下载器"""

    def __init__(self, output_dir: str = "./articles", kimi_key: Optional[str] = None):
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, "images")
        self.kimi_key = kimi_key or os.getenv("KIMI_API_KEY")
        self.cdp_base = "http://localhost:3456"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)

    # ── CDP 底层 HTTP 调用 ──────────────────────────────────────────

    def _cdp_get(self, path: str, timeout: int = 30) -> str:
        url = f"{self.cdp_base}{path}"
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.read().decode("utf-8").strip()

    def _cdp_post(self, path: str, body: str, timeout: int = 30) -> str:
        url = f"{self.cdp_base}{path}"
        data = body.encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "text/plain")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8").strip()

    def _cdp_new_tab(self, url: str) -> str:
        raw = self._cdp_get(f"/new?url={url}", timeout=30)
        return self._unwrap_cdp_response(raw)

    def _cdp_eval(self, target_id: str, js_code: str) -> str:
        raw = self._cdp_post(f"/eval?target={target_id}", js_code, timeout=30)
        raw = self._unwrap_cdp_response(raw)
        try:
            inner = json.loads(raw)
            if isinstance(inner, str):
                return inner
            if isinstance(inner, (dict, list)):
                return json.dumps(inner, ensure_ascii=False)
            return str(inner)
        except (json.JSONDecodeError, TypeError):
            return raw

    @staticmethod
    def _unwrap_cdp_response(raw: str) -> str:
        if raw.startswith("{"):
            try:
                obj = json.loads(raw)
                if "value" in obj:
                    return obj["value"]
                if "targetId" in obj:
                    return obj["targetId"]
                if "success" in obj:
                    return str(obj["success"])
                return raw
            except json.JSONDecodeError:
                return raw
        lines = raw.split("\n")
        if len(lines) >= 2 and "value" in lines[0] and "---" in lines[1]:
            return "\n".join(lines[2:]).strip()
        return raw

    def _cdp_scroll(self, target_id: str):
        self._cdp_eval(target_id, "window.scrollTo(0, document.body.scrollHeight);")

    def _cdp_close(self, target_id: str):
        try:
            self._cdp_get(f"/close?target={target_id}", timeout=10)
        except Exception:
            pass

    # ── 页面数据提取 ────────────────────────────────────────────────

    def _get_article_info(self, target_id: str) -> dict:
        js = """(function(){
var e=document.querySelector('#activity_name');
var t=e?e.textContent.trim():'';
if(!t){var h=document.querySelector('h1');t=h?h.textContent.trim():document.title;}
var a=document.querySelector('#js_name');var ac=a?a.textContent.trim():'';
var d=document.querySelector('#publish_time');var dt=d?d.textContent.trim():'';
var c=document.querySelector('#js_content');var ct=c?c.textContent.trim():'';
return JSON.stringify({title:t,account:ac,date:dt,content:ct.substring(0,99999)});
})()"""
        raw = self._cdp_eval(target_id, js)
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1:
            return json.loads(raw[start:end+1])
        return {}

    def _get_page_images(self, target_id: str) -> List[Dict]:
        js = """(function(){
var imgs=document.querySelectorAll('img[data-src]');
var out=[];for(var i=0;i<imgs.length;i++){
var img=imgs[i];
out.push({index:i,src:img.getAttribute('src'),data_src:img.getAttribute('data-src'),alt:img.getAttribute('alt')||'',width:img.naturalWidth,height:img.naturalHeight});
}return JSON.stringify(out);})()"""
        raw = self._cdp_eval(target_id, js)
        start = raw.find("[")
        end = raw.rfind("]")
        if start != -1 and end != -1:
            return json.loads(raw[start:end+1])
        return []

    def _get_album_links(self, target_id: str) -> List[Dict]:
        js = """(function(){
var out=[];var as=document.querySelectorAll('a[href*="mp.weixin.qq.com/s"]');
for(var i=0;i<as.length;i++){var a=as[i];out.push({title:a.textContent.trim(),url:a.href});}
return JSON.stringify(out);})()"""
        raw = self._cdp_eval(target_id, js)
        start = raw.find("[")
        end = raw.rfind("]")
        if start != -1 and end != -1:
            return json.loads(raw[start:end+1])
        return []

    # ── 图片下载 & OCR ──────────────────────────────────────────────

    def _download_image(self, url: str, save_path: str) -> bool:
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://mp.weixin.qq.com/",
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                with open(save_path, "wb") as f:
                    f.write(resp.read())
            return True
        except Exception as e:
            print(f"    下载失败: {e}")
        return False

    def _ocr_image(self, image_path: str) -> str:
        if not self.kimi_key:
            return "[未配置Kimi API Key]"
        try:
            with open(image_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            ext = os.path.splitext(image_path)[1].lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            req = urllib.request.Request(
                "https://api.moonshot.cn/v1/chat/completions",
                data=json.dumps({
                    "model": "kimi-k2.5",
                    "messages": [
                        {"role": "system", "content": "你是专业 OCR 工具。请完整提取图片中所有文字内容，按原文换行和分段输出。保留原文中的标题、列表、重点标记。如果包含代码、对话、诗歌等特殊格式，请保持原样。只输出文字本身，不要添加任何解释、评论或额外格式。"},
                        {"role": "user", "content": [
                            {"type": "text", "text": "把这张图片里的所有文字完整提取出来，保持原文的换行和分段结构。"},
                            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                        ]}
                    ],
                    "temperature": 1.0,
                    "max_tokens": 4096,
                }).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.kimi_key}",
                    "Content-Type": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode())
                if "choices" in result and result["choices"]:
                    return result["choices"][0]["message"]["content"]
                return f"[OCR错误: {result.get('error', '未知错误')}]"
        except Exception as e:
            return f"[OCR异常: {e}]"

    # ── 辅助 ────────────────────────────────────────────────────────

    @staticmethod
    def _clean_title(title: str) -> str:
        return re.sub(r'[\\/*?:"<>|]', "", title)[:50]

    @staticmethod
    def _build_markdown(title: str, account: str, date: str, url: str,
                        content: str, images: List[Dict], ocr_results: List[Dict]) -> str:
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        formatted_body = "\n\n".join(paragraphs)
        md = f"""---
title: "{title}"
account: "{account}"
date: "{date}"
source_url: "{url}"
images_count: {len(images)}
---

# {title}

> **来源：** {account} · {date}

---

## 正文

{formatted_body}

"""
        if images:
            md += "\n---\n\n## 📷 文章截图\n\n"
            for i, img in enumerate(images, 1):
                md += f"![截图 {i}](images/{img['filename']})\n\n"
        if ocr_results:
            md += "\n---\n\n## 📝 截图文字内容（OCR 提取）\n\n"
            for i, ocr in enumerate(ocr_results, 1):
                md += f"### 截图 {i}\n\n> 图片：`{ocr['filename']}`\n\n"
                md += f"```\n{ocr['text']}\n```\n\n"
        return md

    # ── 核心下载流程 ────────────────────────────────────────────────

    def download_article(self, url: str, do_ocr: bool = True) -> str:
        banner = "=" * 56
        print(f"\n{banner}")
        print(f"  下载文章")
        print(f"{banner}")
        print(f"  URL: {url}")
        target_id = self._cdp_new_tab(url)
        try:
            print(f"  ⏳ 打开页面...")
            time.sleep(3)
            print(f"  ⏳ 滚动触发懒加载...")
            self._cdp_scroll(target_id)
            time.sleep(2)
            print(f"  ⏳ 提取文章信息...")
            info = self._get_article_info(target_id)
            title = info.get("title", "未知标题")
            account = info.get("account", "未知公众号")
            date = info.get("date", "")
            content = info.get("content", "")
            print(f"  ✅ 标题: {title}")
            print(f"  ✅ 公众号: {account}")
            print(f"  ⏳ 提取图片...")
            images = self._get_page_images(target_id)
            real_images = [img for img in images if img.get("width", 0) > 100 and img.get("height", 0) > 100]
            print(f"  ✅ 截图: {len(real_images)} 张")
            self._cdp_close(target_id)
            clean = self._clean_title(title)
            downloaded = []
            if real_images:
                print(f"  ⏳ 下载图片...")
            for i, img in enumerate(real_images):
                src = img.get("data_src", "")
                if not src:
                    continue
                ext = ".jpg" if (".jpg" in src or ".jpeg" in src) else ".png"
                fname = f"{clean}_{i+1:02d}{ext}"
                fpath = os.path.join(self.images_dir, fname)
                if self._download_image(src, fpath):
                    downloaded.append({"filename": fname, "path": fpath, "url": src, "index": i + 1})
                    print(f"    ✅ {fname}")
                else:
                    print(f"    ❌ {fname}")
            ocr = []
            if do_ocr and self.kimi_key and downloaded:
                print(f"  ⏳ OCR 识别截图文字...")
                for i, img in enumerate(downloaded):
                    print(f"    [{i+1}/{len(downloaded)}] {img['filename']}")
                    text = self._ocr_image(img["path"])
                    ocr.append({"filename": img["filename"], "text": text})
                    print(f"    ✅ OCR 完成 ({len(text)} 字)")
            md = self._build_markdown(title, account, date, url, content, downloaded, ocr)
            md_path = os.path.join(self.output_dir, f"{clean}.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md)
            print(f"\n  📄 已保存: {md_path}")
            print(f"{banner}\n")
            return md_path
        except Exception:
            self._cdp_close(target_id)
            raise

    def download_album(self, album_url: str, do_ocr: bool = True) -> List[str]:
        banner = "=" * 56
        print(f"\n{banner}")
        print(f"  下载专辑")
        print(f"{banner}")
        print(f"  URL: {album_url}")
        target_id = self._cdp_new_tab(album_url)
        try:
            print(f"  ⏳ 提取专辑文章列表...")
            time.sleep(3)
            articles = self._get_album_links(target_id)
            seen = set()
            unique = []
            for a in articles:
                if a["url"] not in seen:
                    seen.add(a["url"])
                    unique.append(a)
            print(f"  ✅ 共 {len(unique)} 篇文章")
            self._cdp_close(target_id)
            saved = []
            for i, a in enumerate(unique, 1):
                print(f"\n{'─' * 48}")
                print(f"  [{i}/{len(unique)}] {a['title'][:60]}")
                try:
                    saved.append(self.download_article(a["url"], do_ocr=do_ocr))
                    if i < len(unique):
                        print(f"  ⏳ 等待 2 秒避免触发风控...")
                        time.sleep(2)
                except Exception as e:
                    print(f"  ❌ 下载失败: {e}")
            print(f"\n{banner}")
            print(f"  专辑下载完成! 共 {len(saved)} 篇")
            print(f"{banner}\n")
            return saved
        except Exception:
            self._cdp_close(target_id)
            raise


def _load_batch_urls(url_path: str) -> list:
    with open(url_path, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    seen = set()
    unique = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique


def _organize_output(output_dir: str):
    yuanwen_dir = os.path.join(output_dir, "原文")
    chaijie_dir = os.path.join(output_dir, "拆解文")
    os.makedirs(yuanwen_dir, exist_ok=True)
    os.makedirs(chaijie_dir, exist_ok=True)
    images_src = os.path.join(output_dir, "images")
    if os.path.isdir(images_src):
        images_dst = os.path.join(yuanwen_dir, "images")
        if os.path.exists(images_dst):
            import shutil
            shutil.rmtree(images_dst)
        os.rename(images_src, images_dst)
    for f in glob.glob(os.path.join(output_dir, "*_拆解报告.md")):
        dest = os.path.join(chaijie_dir, os.path.basename(f))
        if not os.path.isfile(dest):
            os.rename(f, dest)
    for f in glob.glob(os.path.join(output_dir, "*.md")):
        name = os.path.basename(f)
        if name.endswith("_拆解报告.md"):
            continue
        dest = os.path.join(yuanwen_dir, name)
        if not os.path.isfile(dest):
            os.rename(f, dest)
    print(f"\n{'=' * 56}")
    print(f"  目录整理完成")
    print(f"  📄 原文 → {yuanwen_dir}")
    print(f"  🧠 拆解文 → {chaijie_dir}")
    print(f"{'=' * 56}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="知识获取器 — Phase A（微信数据源）")
    parser.add_argument("url", nargs="?", help="文章或专辑URL")
    parser.add_argument("--output", "-o", default="./articles", help="输出目录")
    parser.add_argument("--kimi-key", help="Kimi API Key")
    parser.add_argument("--no-ocr", action="store_true", help="跳过OCR识别")
    parser.add_argument("--album", action="store_true", help="下载整个专辑")
    parser.add_argument("--no-report", action="store_true", help="仅下载原文，不生成拆解报告")
    parser.add_argument("--batch", metavar="URLS_FILE", help="批量下载：从文本文件读取 URL（自动去重）")
    parser.add_argument("--organize", action="store_true", help="整理目录为 原文/ 和 拆解文/")

    args = parser.parse_args()

    if args.organize:
        _organize_output(args.output)
        sys.exit(0)

    if args.batch:
        urls = _load_batch_urls(args.batch)
        print(f"\n批量下载: {len(urls)} 个（已去重）")
        downloader = WechatArticleDownloader(output_dir=args.output, kimi_key=args.kimi_key)
        saved = []
        for i, url in enumerate(urls, 1):
            print(f"\n  [{i}/{len(urls)}]")
            try:
                saved.append(downloader.download_article(url, do_ocr=not args.no_ocr))
                if i < len(urls):
                    time.sleep(2)
            except Exception as e:
                print(f"  ❌ 失败: {e}")
        print(f"\n✅ Phase A 完成: {len(saved)}/{len(urls)} 篇成功")
        if not args.no_report and saved:
            print(f"⏳ 进入 Phase B...")
            for path in saved:
                print(f"  📄 {path}  🧠 {os.path.splitext(path)[0]}_拆解报告.md")
        sys.exit(0)

    # ── 单篇下载 ──
    if not args.url:
        parser.print_help()
        sys.exit(1)

    downloader = WechatArticleDownloader(output_dir=args.output, kimi_key=args.kimi_key)
    if args.album:
        saved_files = downloader.download_album(args.url, do_ocr=not args.no_ocr)
    else:
        saved_files = [downloader.download_article(args.url, do_ocr=not args.no_ocr)]

    if not args.no_report:
        print(f"\n✅ Phase A 下载完成 → 进入 Phase B 拆解阶段...")
        for path in saved_files:
            print(f"  📄 原文: {path}")
            print(f"  🧠 报告: {os.path.splitext(path)[0]}_拆解报告.md")
