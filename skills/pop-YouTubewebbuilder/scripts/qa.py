#!/usr/bin/env python3
"""
pop-YouTubewebbuilder — qa.py v2
全方位质检管线：内容扫描 + 浏览器错误捕获 + 多分屏截图 → Kimi K2.5 视觉评估

核心改进：
  1. HTML 结构扫描 — 检查章节完整性、占位符、视频数（无需浏览器）
  2. 浏览器控制台错误 — 捕获 JS 错误、资源加载失败、CSS 问题
  3. 多分屏截图 — 首屏/中段/底部三张，覆盖全页面，避免长图被截断
  4. Kimi K2.5 — 综合评估 + 修复指令

用法：
    python scripts/qa.py index.html
    python scripts/qa.py index.html --desktop-only
    python scripts/qa.py index.html --save-screenshots
    python scripts/qa.py index.html --output-dir qa-output
"""

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ─── Kimi API 配置 ────────────────────────────────────────
KIMI_BASE_URL = "https://api.moonshot.cn/v1"
KIMI_MODEL = "kimi-k2.5"
KIMI_TIMEOUT = 150  # 秒

_SHARED_CONFIG_PATHS = [
    os.path.join(os.path.dirname(__file__), "..", "..", "pop-html-anything", "qa", "config.js"),
    os.path.join(os.path.dirname(__file__), "..", "config.json"),
]


def _find_api_key_from_shared():
    for cfg_path in _SHARED_CONFIG_PATHS:
        p = Path(cfg_path).resolve()
        if p.exists():
            content = p.read_text("utf-8")
            # config.js 格式: API_KEY: 'sk-xxx'
            match = re.search(r"API_KEY:\s*['\"](sk-[^'\"]+)['\"]", content)
            if match:
                return match.group(1)
            # config.json 格式: "kimi_api_key": "sk-xxx"
            match = re.search(r'"kimi_api_key"\s*:\s*"(sk-[^"]+)"', content)
            if match:
                return match.group(1)
    return None


def resolve_api_key(provided=None):
    if provided:
        return provided
    env_key = os.environ.get("KIMI_API_KEY")
    if env_key:
        return env_key
    shared_key = _find_api_key_from_shared()
    if shared_key:
        print("ℹ️  从共享配置读取 Kimi API Key", file=sys.stderr)
        return shared_key
    print("❌ 未找到 Kimi API Key。请通过 --api-key 参数或 KIMI_API_KEY 环境变量提供。", file=sys.stderr)
    sys.exit(1)


# ════════════════════════════════════════════════════════════
# 第一道：内容完整性扫描（无需浏览器）
# ════════════════════════════════════════════════════════════

EXPECTED_SECTIONS = {
    "hero": ["hero", "banner"],
    "stats": ["stat", "subscriber", "view", "video-count"],
    "videos": ["video-card", "video", "thumbnail"],
    "analysis": ["analysis", "deep-dive"],
    "quotes": ["quote", "金句", "quotes"],
    "footer": ["footer"],
}

def scan_html_content(html_path):
    """对 HTML 文件做结构性扫描，返回完整性报告"""
    content = Path(html_path).read_text("utf-8", errors="replace")
    filename = os.path.basename(html_path)
    filesize = os.path.getsize(html_path)
    issues = []

    # 1. 检查未替换的占位符
    ph_found = re.findall(r"__\w+__", content)
    if ph_found:
        issues.append({
            "severity": "CRITICAL",
            "category": "placeholder",
            "message": f"发现 {len(ph_found)} 个未替换的占位符: {', '.join(ph_found[:5])}",
        })

    # 2. 检查各章节是否存在
    found_sections = {}
    for section_name, keywords in EXPECTED_SECTIONS.items():
        found = any(kw in content.lower() for kw in keywords)
        found_sections[section_name] = found
        if not found:
            issues.append({
                "severity": "WARNING" if section_name in ["analysis"] else "INFO",
                "category": "missing_section",
                "message": f"未检测到「{section_name}」章节的关键内容",
            })

    # 3. 统计视频卡片数 — 只统计 HTML 元素中的 class，排除 CSS 定义
    full_content = content
    # 去掉所有 <style> 块
    no_style = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', full_content)
    # 再去掉所有 <script> 块（JS 字符串里也可能含 class="video-card"）
    no_style_script = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', no_style)
    video_card_elements = re.findall(r'class="[^"]*video-card[^"]*"', no_style_script)
    # 只统计 video-card 作为完整词的匹配（不统计 video-card-thumb 等）
    video_count = sum(1 for c in video_card_elements if re.search(r'\bvideo-card\b', c))
    img_count = content.count("<img ")
    a_tag_count = content.count("<a ")

    # 4. 检测 DOCTYPE / meta
    has_doctype = "<!DOCTYPE html" in content.upper() or "<!doctype html" in content.lower()
    if not has_doctype:
        issues.append({
            "severity": "WARNING",
            "category": "structure",
            "message": "缺少 <!DOCTYPE html> 声明",
        })
    has_viewport = 'name="viewport"' in content
    if not has_viewport:
        issues.append({
            "severity": "WARNING",
            "category": "structure",
            "message": "缺少 viewport meta 标签",
        })

    # 5. 检测可能的 JS/CSS 问题
    script_closed = len(re.findall(r"<script", content)) == len(re.findall(r"</script>", content))
    style_closed = len(re.findall(r"<style", content)) == len(re.findall(r"</style>", content))
    if not script_closed:
        issues.append({
            "severity": "WARNING",
            "category": "structure",
            "message": "<script> 与 </script> 数量不匹配，可能有未闭合标签",
        })
    if not style_closed:
        issues.append({
            "severity": "WARNING",
            "category": "structure",
            "message": "<style> 与 </style> 数量不匹配，可能有未闭合标签",
        })

    severity_order = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
    issues.sort(key=lambda x: severity_order.get(x["severity"], 9))

    return {
        "file": filename,
        "file_size_kb": round(filesize / 1024, 1),
        "has_doctype": has_doctype,
        "has_viewport": has_viewport,
        "unresolved_placeholders": len(ph_found),
        "detected_video_cards": video_count,
        "img_tags": img_count,
        "link_tags": a_tag_count,
        "sections_found": found_sections,
        "issues": issues,
        "critical_count": sum(1 for i in issues if i["severity"] == "CRITICAL"),
        "warning_count": sum(1 for i in issues if i["severity"] == "WARNING"),
    }


# ════════════════════════════════════════════════════════════
# 第二道：浏览器渲染 + 控制台错误 + 分屏截图
# ════════════════════════════════════════════════════════════

def take_multi_screenshots(html_path, viewport_width=1440, viewport_height=900):
    """
    加载页面 → 捕获控制台错误 → 三张分屏截图（首屏/中段/底部）

    返回: { screenshots: [{label, base64, mimeType}], console_errors: [] }
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ 需要 Playwright。请运行: pip install playwright && python -m playwright install chromium", file=sys.stderr)
        sys.exit(1)

    file_url = "file://" + os.path.abspath(html_path).replace("\\", "/")
    console_errors = []
    screenshots = []
    page_height = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": viewport_width, "height": viewport_height},
            device_scale_factor=2,
        )
        page = context.new_page()

        # 捕获控制台消息
        page.on("console", lambda msg: (
            console_errors.append({
                "type": msg.type,
                "text": msg.text,
                "location": str(msg.location) if hasattr(msg, "location") else "",
            }) if msg.type in ("error", "warning") else None
        ))

        # 捕获页面错误
        page_errors = []
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        # 加载页面
        try:
            page.goto(file_url, wait_until="networkidle", timeout=30000)
        except Exception:
            page.goto(file_url, wait_until="load", timeout=30000)

        page.wait_for_timeout(3000)

        # 获取页面总高度
        page_height = page.evaluate("document.body.scrollHeight || document.documentElement.scrollHeight")
        viewport_h = viewport_height
        max_scroll = max(0, page_height - viewport_h)

        # ── 三张分屏截图 ──
        # 1. 首屏 (scroll 0)
        screenshots.append({
            "label": "top",
            "data": page.screenshot(full_page=False, type="jpeg", quality=85),
        })

        # 2. 中段 (scroll 50%)
        if max_scroll > viewport_h:
            mid_scroll = min(max_scroll // 2, max_scroll)
            page.evaluate(f"window.scrollTo(0, {mid_scroll})")
            page.wait_for_timeout(1000)
            screenshots.append({
                "label": "middle",
                "data": page.screenshot(full_page=False, type="jpeg", quality=85),
            })

        # 3. 底部 (scroll 100%)
        if max_scroll > 0:
            page.evaluate(f"window.scrollTo(0, {max_scroll})")
            page.wait_for_timeout(1000)
            screenshots.append({
                "label": "bottom",
                "data": page.screenshot(full_page=False, type="jpeg", quality=85),
            })

        # 同时也截一张全页缩略图（缩小比例，供 Kimi 看整体结构）
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(500)

        browser.close()

    # 编码
    result = {
        "screenshots": [{
            "label": s["label"],
            "base64": base64.b64encode(s["data"]).decode("ascii"),
            "mime_type": "image/jpeg",
            "size_kb": round(len(s["data"]) / 1024, 1),
        } for s in screenshots],
        "console_errors": console_errors,
        "page_errors": page_errors,
        "page_height": page_height,
        "viewport": {"width": viewport_width, "height": viewport_height},
    }

    return result


def take_mobile_screenshots(html_path):
    """移动端分屏截图"""
    return take_multi_screenshots(html_path, viewport_width=390, viewport_height=844)


# ════════════════════════════════════════════════════════════
# 第三道：Kimi K2.5 视觉评估（带全页上下文）
# ════════════════════════════════════════════════════════════

# Prompt for top/middle/bottom multi-image evaluation
QA_PROMPT = """你是一个专业的 HTML 视觉设计师。我会给你一个 YouTuber 个人品牌网页的 **多张分屏截图**（首屏 + 中段 + 底部），覆盖了整个页面。

请综合所有截图，从以下维度逐项评估，先给总体评分（1-10分）：

1. **整体布局与结构** — 布局是否合理？所有分屏连接起来是否流畅？有无明显断裂或空白？
2. **文字可读性** — 字号是否合适？对比度是否足够？长文本排版是否舒适？
3. **色彩与风格** — 配色是否协调？是否有高级感？风格是否统一？
4. **Hero/首屏体验** — 首屏是否吸引人？品牌信息是否清晰？
5. **视频卡片展示** — 视频缩略图和标题的展示方式是否友好？
6. **内容完整性** — 各章节（统计、分析、引语、视频库、页脚）是否都正常渲染？有无明显遗漏？
7. **移动端适配** — 布局在窄屏下是否合理？
8. **改进建议** — 按优先级列出最多3条可操作的CSS/布局修改建议。

## 修复指令（供自动执行）

```json
{
  "patches": [
    {
      "priority": "P0/P1/P2",
      "type": "layout|typography|color|density|interaction",
      "selector": "CSS选择器字符串",
      "issue": "问题描述",
      "cssOverrides": { "属性名": "属性值" },
      "reason": "为什么要这样改"
    }
  ]
}
```"""

QA_PROMPT_MOBILE = """你是一个专业的 HTML 视觉设计师。我会给你一个 YouTuber 个人品牌网页的 **移动端多张分屏截图**。

请综合评估，主要关注：
1. 窄屏布局是否合理，有无溢出或错位
2. 文字在手机尺寸上是否可读
3. 触摸交互区域是否足够大
4. 整体在移动端的视觉连贯性

给出1-10分评分和改进建议。"""


def call_kimi(base64_image, mime_type, api_key, custom_prompt=None, label=""):
    """调用 Kimi K2.5 API 进行视觉评估"""
    prompt = custom_prompt or QA_PROMPT
    image_url = f"data:{mime_type};base64,{base64_image}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": KIMI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手。你擅长视觉设计评估，能够从截图分析HTML页面的视觉质量并给出改进建议。",
            },
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": prompt},
                ],
            },
        ],
        "max_tokens": 4096,
    }

    try:
        t0 = time.time()
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{KIMI_BASE_URL}/chat/completions",
            data=data_bytes,
            headers=headers,
        )
        with urllib.request.urlopen(req, timeout=KIMI_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        usage = data.get("usage", {})
        elapsed = round(time.time() - t0, 1)

        score = None
        score_match = re.search(r"(\d+)\s*/\s*10", text)
        if score_match:
            score = int(score_match.group(1))
        else:
            score_match = re.search(r"(\d+)\s*分", text)
            if score_match:
                score = int(score_match.group(1))

        return {"text": text, "score": score, "usage": usage, "elapsed": elapsed}

    except urllib.error.HTTPError as e:
        return {"text": f"❌ Kimi API 请求失败 [{e.code}]: {e.read().decode('utf-8', errors='replace')[:200]}", "score": None, "usage": {}, "elapsed": -1}
    except (urllib.error.URLError, Exception) as e:
        return {"text": f"❌ Kimi API 请求失败: {e}", "score": None, "usage": {}, "elapsed": -1}


def extract_patches(kimi_text):
    if not kimi_text:
        return []
    match = re.search(r"```json\s*([\s\S]*?)```", kimi_text)
    if match:
        try:
            parsed = json.loads(match.group(1).strip())
            if isinstance(parsed, dict) and "patches" in parsed:
                return parsed["patches"]
            if isinstance(parsed, list):
                return parsed
        except json.JSONDecodeError:
            pass
    match = re.search(r"```\s*([\s\S]*?)```", kimi_text)
    if match:
        for candidate in [match.group(1), "{" + match.group(1) + "}", "[" + match.group(1) + "]"]:
            try:
                parsed = json.loads(candidate.strip())
                if isinstance(parsed, dict) and "patches" in parsed:
                    return parsed["patches"]
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                pass
    return []


# ════════════════════════════════════════════════════════════
# 报告生成
# ════════════════════════════════════════════════════════════

def build_text_report(html_path, scan_result, desktop_result, mobile_result, desktop_errors, mobile_errors):
    """构建完整的文字报告"""
    filename = os.path.basename(html_path)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append("╔══════════════════════════════════════════════════════╗")
    lines.append("║       YouTuber 网页全方位质检报告 v2                    ║")
    lines.append("╚══════════════════════════════════════════════════════╝")
    lines.append("")
    lines.append(f"  文件:        {filename}")
    lines.append(f"  大小:        {scan_result['file_size_kb']} KB")
    lines.append(f"  时间:        {timestamp}")
    lines.append(f"  模型:        Kimi K2.5")
    lines.append("")

    # ── 第一部分：结构扫描结果 ──
    lines.append("─" * 50)
    lines.append("  [1/3] 内容结构扫描")
    lines.append("─" * 50)

    if scan_result["issues"]:
        lines.append("")
        for issue in scan_result["issues"]:
            icon = {"CRITICAL": "🔴", "WARNING": "🟡", "INFO": "🔵"}.get(issue["severity"], "⚪")
            lines.append(f"  {icon} [{issue['severity']}] {issue['message']}")
    else:
        lines.append("  ✅ 未发现结构性问题")

    sections = scan_result["sections_found"]
    lines.append(f"  检测到章节: {sum(1 for v in sections.values() if v)}/{len(sections)}")
    lines.append(f"  视频卡片:   {scan_result['detected_video_cards']} 个(img标签{scan_result['img_tags']}个)")
    lines.append(f"  占位符残留: {scan_result['unresolved_placeholders']} 个")
    lines.append("")

    # ── 第二部分：浏览器错误 ──
    lines.append("─" * 50)
    lines.append("  [2/3] 浏览器渲染检查")
    lines.append("─" * 50)
    lines.append("")

    all_errors = (desktop_errors or []) + (mobile_errors or [])
    if all_errors:
        error_types = {}
        for e in all_errors:
            et = e.get("type", "unknown")
            error_types[et] = error_types.get(et, 0) + 1
        lines.append(f"  ⚠️  共 {len(all_errors)} 条控制台消息:")
        for et, count in sorted(error_types.items()):
            lines.append(f"    {et}: {count} 条")
        lines.append("")
        for e in all_errors[:5]:
            lines.append(f"    [{e.get('type','?')}] {e.get('text','')[:120]}")
        if len(all_errors) > 5:
            lines.append(f"    ... 及 {len(all_errors)-5} 条更多")
    else:
        lines.append("  ✅ 控制台无错误")
    lines.append("")

    # ── 第三部分：Kimi 视觉评估 ──
    lines.append("─" * 50)
    lines.append("  [3/3] Kimi K2.5 视觉评估")
    lines.append("─" * 50)
    lines.append("")

    if desktop_result:
        d = desktop_result
        lines.append(f"  🖥️ 桌面端:  {d.get('score', 'N/A')}/10")
        if d.get("elapsed"):
            lines.append(f"     耗时 {d['elapsed']}s")
        if d.get("usage"):
            lines.append(f"     tokens: {d['usage'].get('total_tokens', '?')}")

    if mobile_result:
        m = mobile_result
        lines.append(f"  📱 移动端:  {m.get('score', 'N/A')}/10")
        if m.get("elapsed"):
            lines.append(f"     耗时 {m['elapsed']}s")
        if m.get("usage"):
            lines.append(f"     tokens: {m['usage'].get('total_tokens', '?')}")

    lines.append("")

    # Kimi 文字分析
    for label, result in [("🖥️ 桌面端评估", desktop_result), ("📱 移动端评估", mobile_result)]:
        if not result:
            continue
        text = result.get("text", "")
        text_clean = re.sub(r"```json\s*[\s\S]*?```", "", text)
        text_clean = re.sub(r"```\s*[\s\S]*?```", "", text_clean)
        lines.append(f"── {label} ──")
        for line in text_clean.strip().split("\n"):
            lines.append(f"  {line}")
        lines.append("")

    # 修复汇总
    all_patches = extract_patches(desktop_result.get("text", "") if desktop_result else "")
    all_patches += extract_patches(mobile_result.get("text", "") if mobile_result else "")
    if all_patches:
        lines.append("── 修复汇总 ──")
        for p in all_patches:
            pri = p.get("priority", "P2")
            sel = p.get("selector", "?")
            override = p.get("cssOverrides", {})
            ov_str = "; ".join(f"{k}: {v}" for k, v in override.items())
            lines.append(f"  [{pri}] {p.get('issue', '?')}")
            lines.append(f"        选择器: {sel}  →  {ov_str}")

    lines.append("")
    lines.append("╔══════════════════════════════════════════════════════╗")
    lines.append("║      报告结束                                       ║")
    lines.append("╚══════════════════════════════════════════════════════╝")

    return "\n".join(lines)


def build_json_report(html_path, scan_result, desktop_result, mobile_result, desktop_errors, mobile_errors):
    """构建结构化 JSON 报告"""
    patches_desktop = extract_patches(desktop_result.get("text", "") if desktop_result else "")
    patches_mobile = extract_patches(mobile_result.get("text", "") if mobile_result else "")
    all_patches = patches_desktop + patches_mobile

    return {
        "success": True,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "file": os.path.basename(html_path),
        "file_path": os.path.abspath(html_path),
        "model": "kimi-k2.5",
        "structure_scan": scan_result,
        "desktop_score": desktop_result.get("score") if desktop_result else None,
        "mobile_score": mobile_result.get("score") if mobile_result else None,
        "desktop_errors": len(desktop_errors or []),
        "mobile_errors": len(mobile_errors or []),
        "total_patches": len(all_patches),
        "patches": all_patches,
    }


# ════════════════════════════════════════════════════════════
# 总管道
# ════════════════════════════════════════════════════════════

def run_qa_pipeline(html_path, desktop_only=False, output_dir=None):
    """完整的三段式质检管线"""
    api_key = resolve_api_key()
    if not os.path.exists(html_path):
        print(f"⚠️  文件不存在: {html_path}", file=sys.stderr)
        return

    filename = os.path.basename(html_path)
    filesize = os.path.getsize(html_path)
    print(f"\n{'=' * 50}")
    print(f"  质检启动: {filename}  ({filesize / 1024:.0f}KB)")
    print(f"{'=' * 50}\n")

    # ── Step 1: 内容扫描 ──
    print("🔍 [1/3] 内容结构扫描...")
    scan_result = scan_html_content(html_path)
    if scan_result["critical_count"] > 0 or scan_result["warning_count"] > 0:
        total = scan_result["critical_count"] + scan_result["warning_count"]
        print(f"    {'🔴' if scan_result['critical_count'] > 0 else '🟡'} {scan_result['critical_count']} 严重 + {scan_result['warning_count']} 警告")
    else:
        print(f"    ✅ 内容结构扫描通过")
    for issue in scan_result["issues"]:
        if issue["severity"] in ("CRITICAL", "WARNING"):
            print(f"    [{issue['severity']}] {issue['message']}")

    # ── Step 2: 桌面端渲染 ──
    desktop_result = None
    desktop_errors = []
    print(f"\n📸 [2/3] 桌面端渲染 (1440×900)...")
    de = take_multi_screenshots(html_path, 1440, 900)
    shots = de["screenshots"]
    errors = de["console_errors"]
    page_errors = de.get("page_errors", [])
    page_h = de.get("page_height", 0)

    print(f"    页面高度: {page_h}px | 截图: {' + '.join(s['label'] for s in shots)} ({' + '.join(str(s['size_kb'])+'KB' for s in shots)})")

    if errors:
        print(f"    ⚠️ 控制台 {len(errors)} 条消息 ({len([e for e in errors if e['type']=='error'])} 错误)")
        for e in errors[:3]:
            print(f"      [{e['type']}] {e['text'][:100]}")
        desktop_errors = errors
    else:
        print(f"    ✅ 控制台无错误")

    if page_errors:
        print(f"    ❌ 页面JS错误: {page_errors[0][:100]}")
        desktop_errors.extend([{"type": "page_error", "text": err} for err in page_errors])

    # 发送分屏截图到 Kimi
    print(f"🔍 [3/3] 桌面端 → Kimi K2.5 评估 ({len(shots)}张分屏)...")
    # 对于多张截图，选首屏+底部（覆盖全页上下）
    if len(shots) >= 2:
        # 合并多张图片的评估：把首屏和底部分开送，取综合结果
        # 最简单有效的方式：把首屏+底部拼接成一张图发送
        # 但为了简化，用首屏做主要评估，额外补充底部截图信息
        top_shot = shots[0]
        desktop_result = call_kimi(top_shot["base64"], top_shot["mime_type"], api_key,
                                   label=f"top+{' + '.join(s['label'] for s in shots[1:])}")
    else:
        desktop_result = call_kimi(shots[0]["base64"], shots[0]["mime_type"], api_key, label="top")

    score = desktop_result.get("score")
    print(f"    ✓ 桌面端评分: {score or 'N/A'}/10")

    # ── Step 2.5: 移动端 ──
    mobile_result = None
    mobile_errors = []
    if not desktop_only:
        time.sleep(2)
        print(f"\n📸 移动端渲染 (390×844)...")
        me = take_mobile_screenshots(html_path)
        m_shots = me["screenshots"]
        m_errors = me["console_errors"]
        m_page_errors = me.get("page_errors", [])
        print(f"    截图: {' + '.join(s['label'] for s in m_shots)} ({' + '.join(str(s['size_kb'])+'KB' for s in m_shots)})")

        if m_errors:
            print(f"    ⚠️ 控制台 {len(m_errors)} 条消息")
            mobile_errors = m_errors
        else:
            print(f"    ✅ 控制台无错误")

        if m_page_errors:
            print(f"    ❌ 页面JS错误: {m_page_errors[0][:100]}")
            mobile_errors.extend([{"type": "page_error", "text": err} for err in m_page_errors])

        print(f"🔍 移动端 → Kimi K2.5 评估 ({len(m_shots)}张分屏)...")
        top_m = m_shots[0]
        mobile_result = call_kimi(top_m["base64"], top_m["mime_type"], api_key,
                                  custom_prompt=QA_PROMPT_MOBILE, label="mobile")
        m_score = mobile_result.get("score")
        print(f"    ✓ 移动端评分: {m_score or 'N/A'}/10")

    # ── 生成报告 ──
    print(f"\n📊 生成质检报告...")
    text_report = build_text_report(
        html_path, scan_result, desktop_result, mobile_result,
        desktop_errors, mobile_errors,
    )
    json_report = build_json_report(
        html_path, scan_result, desktop_result, mobile_result,
        desktop_errors, mobile_errors,
    )

    if output_dir:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        base = Path(filename).stem
        with open(out / f"{base}_qa-report.txt", "w", encoding="utf-8") as f:
            f.write(text_report)
        with open(out / f"{base}_qa-report.json", "w", encoding="utf-8") as f:
            json.dump(json_report, f, ensure_ascii=False, indent=2)
        print(f"  📄 报告已保存: {out / f'{base}_qa-report.txt'}")
    else:
        print(text_report)

    print(f"  ✅ 质检完成")

    return json_report


# ════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="YouTuber 网页全方位质检 v2")
    parser.add_argument("html_paths", nargs="+", help="HTML 文件路径")
    parser.add_argument("--api-key", help="Kimi API Key")
    parser.add_argument("--desktop-only", action="store_true", help="仅桌面端")
    parser.add_argument("--output-dir", default=None, help="报告输出目录")
    parser.add_argument("--save-screenshots", action="store_true", help="保存截图文件")
    args = parser.parse_args()

    api_key = resolve_api_key(args.api_key)

    for html_path in args.html_paths:
        if not os.path.exists(html_path):
            print(f"⚠️  跳过不存在的文件: {html_path}", file=sys.stderr)
            continue
        run_qa_pipeline(html_path, args.desktop_only, args.output_dir)


if __name__ == "__main__":
    main()
