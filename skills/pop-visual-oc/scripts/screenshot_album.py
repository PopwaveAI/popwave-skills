#!/usr/bin/env python3
"""
pop-visual-oc 画册页长图截图脚本 v1.0
- Playwright 整页高清截图（deviceScaleFactor=2），专为 OC 画册页设计
- 画册页是单页连续排版（.frame 整体），用 full_page 高清截图即可，底部质量不退化
- 输出 PNG（无损长图）

用法:
  python screenshot_album.py <HTML文件路径> [输出图片路径]

示例:
  python screenshot_album.py "规则卡-借香他化-画册页.html" "规则卡-借香他化-画册页-长图.png"
  python screenshot_album.py "素材/视觉资产/规则卡-借香他化-画册页.html" "素材/视觉资产/规则-长图.png"

依赖:
  pip install playwright Pillow
  playwright install chromium

环境变量:
  SCREENSHOT_WIDTH - 截图视口宽度（默认680，对应 .wrap max-width）
  SCREENSHOT_SCALE - 缩放到设备像素的倍率（默认2，高清）
"""

import os
import sys
import time


def parse_args():
    if len(sys.argv) < 2:
        print("用法: python screenshot_album.py <HTML路径> [输出路径]")
        print("示例:")
        print('  python screenshot_album.py "规则卡-借香他化-画册页.html" "规则卡-长图.png"')
        sys.exit(1)

    source = sys.argv[1]

    # 默认输出路径
    if len(sys.argv) >= 3:
        output = sys.argv[2]
    else:
        base = os.path.splitext(source)[0]
        output = f"{base}-长图.png"

    return source, output


def screenshot_album(source, output_path):
    """画册页整页高清长图截图。"""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[错误] 未安装 playwright，请执行: pip install playwright && playwright install chromium")
        sys.exit(1)

    width = int(os.environ.get("SCREENSHOT_WIDTH", "680"))
    scale = int(os.environ.get("SCREENSHOT_SCALE", "2"))

    # 判断是URL还是文件路径
    if source.startswith("http://") or source.startswith("https://"):
        url = source
    else:
        html_path = os.path.abspath(source)
        url = f"file:///{html_path.replace(os.sep, '/')}"

    print(f"截图源: {url}")
    print(f"输出: {output_path}")
    print(f"视口宽度: {width}px × 设备倍率 {scale}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={"width": width, "height": 1200},
            device_scale_factor=scale,
        )

        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # 移除lazy loading
        page.evaluate("""
            document.querySelectorAll('img[loading="lazy"]').forEach(img => {
                img.removeAttribute('loading');
            });
        """)

        # 等待所有图片完全加载
        page.wait_for_function("""
            () => {
                const imgs = document.querySelectorAll('img');
                return Array.from(imgs).every(img => img.complete && img.naturalWidth > 0);
            }
        """, timeout=30000)
        print("所有图片加载完成")

        # 字体/样式稳定
        page.wait_for_timeout(1200)

        # 整页高清截图
        page.screenshot(path=output_path, full_page=True)

        w = page.evaluate("() => document.body.scrollWidth")
        h = page.evaluate("() => document.body.scrollHeight")

        browser.close()

        try:
            from PIL import Image
            img = Image.open(output_path)
            size = f"{img.width}x{img.height}px"
        except Exception:
            size = "未知"
        fsize = os.path.getsize(output_path) / 1024
        print(f"页面逻辑尺寸: {w}x{h}px")
        print(f"长图已保存: {output_path} ({size}, {fsize:.0f}KB)")


def main():
    source, output = parse_args()
    screenshot_album(source, output)


if __name__ == "__main__":
    main()