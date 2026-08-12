#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pop-visual-comic 按页导出分享图脚本 v1.1
- Playwright 逐页截图 index.html 中每个 .page + .info-page 容器（保留文字叠加层）
- Pillow 在每张底部追加品牌水印条（popwave.cn 让创意一键落地）
- 同时生成整条 HTML 长图（逐元素截图拼接，非 full_page），与分页一起放入 分享/
- 输出到 <章节目录>/分享/page{NN}.png + <章节目录>/分享/长图-{章节名}.png

背景：2026-08-07 老板校准——交付 HTML 后只产整条长图，但用户分享是"一张一张图去分享"。
故新增按页切图：每页独立一张分享图（带文字叠加），且每页底部压品牌水印。
2026-08-07 老板再加：分享图与整条 HTML 长图都要放进 分享/ 文件夹，统一管理。

用法:
  python export_pages.py <HTML文件路径> [输出目录] [视口宽度]

示例:
  python export_pages.py "第1章/index.html"
  # 默认输出到 第1章/分享/page01.png ... 视口默认 820

依赖:
  pip install playwright Pillow
  playwright install chromium
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

SLOGAN = 'popwave.cn 让创意一键落地'
WATERMARK_BAR_HEIGHT = 56          # 底部水印条高度
WATERMARK_BG = (18, 18, 24, 255)   # 深色背景
WATERMARK_BORDER = (154, 43, 38)   # 暗红分隔线
WATERMARK_TEXT = (138, 130, 116)   # 灰度文字


def parse_args():
    if len(sys.argv) < 2:
        print('用法: python export_pages.py <HTML路径> [输出目录] [视口宽度]')
        sys.exit(1)
    html = sys.argv[1]
    html_dir = os.path.dirname(os.path.abspath(html)) or '.'
    out_dir = os.path.join(html_dir, '分享') if len(sys.argv) < 3 else sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) >= 4 else 820
    return html, out_dir, width


def _find_font(sizes):
    """Windows 常见中文字体路径，优先微软雅黑。"""
    candidates = [
        r'C:\Windows\Fonts\msyh.ttc',
        r'C:\Windows\Fonts\msyhbd.ttc',
        r'C:\Windows\Fonts\simhei.ttf',
        r'C:\Windows\Fonts\simsun.ttc',
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, sizes[0]), ImageFont.truetype(path, sizes[1])
            except Exception:
                continue
    return None, None


def _add_watermark_bar(img):
    """在图片底部追加品牌水印条。"""
    w, h = img.size
    bar = Image.new('RGBA', (w, WATERMARK_BAR_HEIGHT), WATERMARK_BG)
    draw = ImageDraw.Draw(bar)

    # 暗红分隔线（顶部）
    draw.rectangle([0, 0, w, 3], fill=WATERMARK_BORDER)

    # 品牌文案
    font_small, font_big = _find_font((20, 28))
    if font_big is None:
        draw.text((w // 2 - 80, 14), SLOGAN, fill=WATERMARK_TEXT)
    else:
        # 居中绘制
        bbox = draw.textbbox((0, 0), SLOGAN, font=font_big)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(((w - tw) / 2, (WATERMARK_BAR_HEIGHT - th) / 2 - 4),
                  SLOGAN, font=font_big, fill=WATERMARK_TEXT)

    # 拼接
    result = Image.new('RGBA', (w, h + WATERMARK_BAR_HEIGHT), WATERMARK_BG)
    result.alpha_composite(img.convert('RGBA'), (0, 0))
    result.alpha_composite(bar, (0, h))
    return result.convert('RGB')


def _extract_title(html_path):
    """从 HTML 标题标签提取章节名（用于长图命名）。"""
    import re
    title = '漫画'
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        m = re.search(r'<title>(.*?)</title>', content, re.S)
        if m:
            t = m.group(1).strip()
            if t:
                title = t
    except Exception:
        pass
    return title


def _export_long_image(page, html_path, out_dir, width):
    """逐元素截图拼接整条 HTML 长图（title-banner + .page/.info-page + footer-banner），输出到 分享/。

    逐元素截图 + Pillow 拼接，避免浏览器 full_page 全页截图在长页面底部质量退化。
    """
    import io as _io

    # 收集要拼进长图的顶层元素（按文档顺序）
    sel = page.evaluate("""
        () => {
            const els = [];
            document.querySelectorAll('.title-banner, .page, .info-page, .footer-banner').forEach(el => {
                if (el.offsetHeight > 0) els.push(el);
            });
            return els.length;
        }
    """)
    if sel == 0:
        print('  [长图] 未找到可拼接元素，跳过', file=sys.stderr)
        return None

    pieces = page.query_selector_all('.title-banner, .page, .info-page, .footer-banner')
    images = []
    for el in pieces:
        el.scroll_into_view_if_needed()
        page.wait_for_timeout(80)
        shot = el.screenshot()
        images.append(Image.open(_io.BytesIO(shot)).convert('RGB'))

    max_w = max(img.width for img in images)
    total_h = sum(img.height for img in images)

    canvas = Image.new('RGB', (max_w, total_h), (13, 13, 18))
    y = 0
    for img in images:
        x = (max_w - img.width) // 2
        canvas.paste(img, (x, y))
        y += img.height

    # 长图底部追加品牌水印条（与逐页一致）
    canvas = _add_watermark_bar(canvas)

    title = _extract_title(html_path)
    out_path = os.path.join(out_dir, f'长图-{title}.png')
    canvas.save(out_path, 'PNG', optimize=True)
    print(f'\n[长图] HTML 整条长图已保存: {os.path.basename(out_path)} {canvas.width}x{canvas.height}px')
    return out_path


def export_pages(html, out_dir, width=820):
    os.makedirs(out_dir, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('[错误] 未安装 playwright，请执行: pip install playwright && playwright install chromium')
        sys.exit(1)

    url = f'file:///{os.path.abspath(html).replace(os.sep, "/")}'

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': width, 'height': 1200})

        page.goto(url, wait_until='domcontentloaded', timeout=30000)

        # 移除 lazy loading + 等待所有图片加载
        page.evaluate("""
            document.querySelectorAll('img[loading="lazy"]').forEach(img => img.removeAttribute('loading'));
        """)
        page.wait_for_function("""
            () => {
                const imgs = document.querySelectorAll('img');
                return imgs.length === 0 || Array.from(imgs).every(img => img.complete && img.naturalWidth > 0);
            }
        """, timeout=30000)
        page.wait_for_timeout(1200)

        # 定位所有页面容器（漫画页 .page + 信息页 .info-page，含文字叠加层）
        page_els = page.query_selector_all('.page, .info-page')
        if not page_els:
            print('[错误] 未在 HTML 中找到 .page / .info-page 容器', file=sys.stderr)
            sys.exit(1)

        print(f'检测到 {len(page_els)} 个页面容器（含信息页），逐页导出...')
        saved = []
        for i, el in enumerate(page_els, 1):
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(120)
            shot = el.screenshot()
            img = Image.open(__import__('io').BytesIO(shot))
            img = _add_watermark_bar(img)
            out_path = os.path.join(out_dir, f'page{i:02d}.png')
            img.save(out_path, 'PNG', optimize=True)
            saved.append(out_path)
            print(f'  [{i:02d}/{len(page_els):02d}] {os.path.basename(out_path)} {img.width}x{img.height}px OK')

        # 生成 HTML 整条长图，与分页一起放入 分享/ 目录
        long_path = _export_long_image(page, html, out_dir, width)

        browser.close()

    print(f'\n按页导出完成: {len(saved)} 页 -> {os.path.abspath(out_dir)}')
    if long_path:
        print(f'长图导出完成: {os.path.basename(long_path)} -> {os.path.abspath(out_dir)}')
    result = list(saved)
    if long_path:
        result.append(long_path)
    return result


def main():
    html, out_dir, width = parse_args()
    export_pages(html, out_dir, width)


if __name__ == '__main__':
    main()