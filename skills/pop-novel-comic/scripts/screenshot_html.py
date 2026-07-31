#!/usr/bin/env python3
"""
HTML 截长图脚本
将自包含漫画 HTML 截取为长图 PNG/JPEG，方便分享。

用法:
  python screenshot_html.py <html文件路径> [--output 输出路径] [--width 940] [--format png|jpeg] [--quality 95]

依赖：系统已安装 Microsoft Edge 或 Google Chrome（Windows 自带 Edge）+ Pillow。
原理：浏览器 headless 模式渲染 HTML → 截取全页 → Pillow 自动裁剪底部多余背景。
"""

import argparse
import os
import subprocess
import sys
import tempfile

# 浏览器候选路径（Edge 优先，Windows 自带）
BROWSER_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

# HTML 模板 body 背景色 #1a1a1a
BODY_BG = (26, 26, 26)
# HTML 模板 comic-page 背景色 #f5f0e8
PAGE_BG = (245, 240, 232)
# 颜色容差：像素与背景色的差值超过此值则视为"有内容"
COLOR_THRESHOLD = 15
# comic-page 背景色匹配容差
PAGE_BG_THRESHOLD = 12
# 裁剪时每行采样间隔（px），越大越快但精度越低
SAMPLE_INTERVAL = 8


def find_browser():
    """查找可用的浏览器，返回可执行文件路径"""
    # 先检查环境变量覆盖
    env_browser = os.environ.get("COMIC_BROWSER")
    if env_browser and os.path.exists(env_browser):
        return env_browser
    for path in BROWSER_PATHS:
        if os.path.exists(path):
            return path
    return None


def take_screenshot(html_path, output_path, width=940, max_height=12000, fmt="png", quality=95):
    """使用浏览器 headless 模式截取全页长图，然后裁剪底部空白"""

    browser = find_browser()
    if not browser:
        print("错误：未找到 Microsoft Edge 或 Google Chrome", file=sys.stderr)
        print("请确保已安装其中一种浏览器，或设置 COMIC_BROWSER 环境变量", file=sys.stderr)
        sys.exit(1)

    # 生成 file:/// URL
    abs_path = os.path.abspath(html_path)
    url = "file:///" + abs_path.replace("\\", "/")

    # 临时文件保存原始截图
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        raw_path = tmp.name

    try:
        cmd = [
            browser,
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--screenshot={raw_path}",
            f"--window-size={width},{max_height}",
            url,
        ]

        browser_name = os.path.basename(browser)
        print(f"浏览器: {browser_name}")
        print(f"窗口尺寸: {width}x{max_height}")
        print("正在渲染并截图...")

        result = subprocess.run(cmd, capture_output=True, timeout=60)

        if not os.path.exists(raw_path) or os.path.getsize(raw_path) == 0:
            print("错误：浏览器未生成截图文件", file=sys.stderr)
            if result.stderr:
                stderr_text = result.stderr.decode("utf-8", errors="replace")[:500]
                print(f"  stderr: {stderr_text}", file=sys.stderr)
            sys.exit(1)

        # Pillow 裁剪
        try:
            from PIL import Image
        except ImportError:
            print("错误：Pillow 未安装，请运行 pip install Pillow", file=sys.stderr)
            sys.exit(1)

        img = Image.open(raw_path)
        print(f"原始截图: {img.width}x{img.height}")

        # 确保是 RGB 模式
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")

        pixels = img.load()
        img_w, img_h = img.size

        # === 自动裁剪：定位 comic-page div 的底边界 ===
        # 策略：comic-page div 有 #f5f0e8 背景色，左右有 24px padding。
        # 扫描 padding 列的 #f5f0e8 像素，精确定位内容区域底边界。
        # 这比"找非 body 背景色"更可靠——hook panel 的暗角不会被误判。

        # 计算 comic-page 左 padding 的 x 坐标
        # body padding=20px，comic-page 居中，max-width=900px，padding=24px
        if img_w <= 940:
            padding_x = 32  # 20(body) + 12(half of 24px comic-page padding)
        else:
            comic_start = 20 + (img_w - 40 - 900) // 2
            padding_x = comic_start + 12

        # 主策略：扫描 padding 列找 #f5f0e8（comic-page 背景色）
        last_content_row = 0
        for y in range(img_h - 1, -1, -1):
            p = pixels[padding_x, y]
            r, g, b = p[0], p[1], p[2]
            if abs(r - PAGE_BG[0]) < PAGE_BG_THRESHOLD and \
               abs(g - PAGE_BG[1]) < PAGE_BG_THRESHOLD and \
               abs(b - PAGE_BG[2]) < PAGE_BG_THRESHOLD:
                last_content_row = y
                break

        # 备选策略：如果主策略没找到（非标准模板），回退到全宽扫描非 body 背景
        if last_content_row == 0:
            print("  [INFO] 主策略未匹配，回退到全宽扫描")
            for y in range(img_h - 1, -1, -1):
                found = False
                for x in range(0, img_w, SAMPLE_INTERVAL):
                    p = pixels[x, y]
                    r, g, b = p[0], p[1], p[2]
                    if abs(r - BODY_BG[0]) > COLOR_THRESHOLD or \
                       abs(g - BODY_BG[1]) > COLOR_THRESHOLD or \
                       abs(b - BODY_BG[2]) > COLOR_THRESHOLD:
                        found = True
                        break
                if found:
                    last_content_row = y
                    break

        # 安全检查
        if last_content_row < 100:
            print("⚠️  警告：裁剪位置异常低，可能裁剪失败，保留完整截图")
            last_content_row = img_h - 1

        # 检查是否可能被截断
        if last_content_row >= img_h - 30:
            print(f"⚠️  警告：内容可能超出最大高度 {max_height}px，请增大 --max-height 参数")

        # 底部留 20px 边距（保持 body padding 视觉一致）
        crop_bottom = min(last_content_row + 20, img_h)
        cropped = img.crop((0, 0, img_w, crop_bottom))
        print(f"裁剪后: {cropped.width}x{cropped.height}")

        # 保存
        if fmt == "jpeg":
            if cropped.mode == "RGBA":
                cropped = cropped.convert("RGB")
            # 确保输出路径是 .jpg
            base = os.path.splitext(output_path)[0]
            output_path = base + ".jpg"
            cropped.save(output_path, "JPEG", quality=quality)
        else:
            cropped.save(output_path, "PNG")

        size_kb = os.path.getsize(output_path) // 1024
        size_mb = size_kb / 1024
        if size_mb >= 1:
            print(f"\n✅ 完成: {output_path} ({size_mb:.1f}MB)")
        else:
            print(f"\n✅ 完成: {output_path} ({size_kb}KB)")

    finally:
        if os.path.exists(raw_path):
            os.unlink(raw_path)


def main():
    parser = argparse.ArgumentParser(
        description="HTML 截长图 — 将漫画 HTML 截取为可分享的长图"
    )
    parser.add_argument("html_path", help="HTML 文件路径")
    parser.add_argument(
        "--output", "-o",
        help="输出图片路径（默认同目录同名 .png）",
    )
    parser.add_argument(
        "--width", type=int, default=940,
        help="截图宽度像素（默认940，匹配漫画模板）",
    )
    parser.add_argument(
        "--max-height", type=int, default=12000,
        help="截图最大高度像素（默认12000，内容多时增大）",
    )
    parser.add_argument(
        "--format", choices=["png", "jpeg"], default="png",
        help="输出格式：png（无损）或 jpeg（小体积，默认png）",
    )
    parser.add_argument(
        "--quality", type=int, default=95,
        help="JPEG 质量 1-100（默认95，仅 --format=jpeg 时生效）",
    )
    args = parser.parse_args()

    if not os.path.exists(args.html_path):
        print(f"错误：文件不存在: {args.html_path}", file=sys.stderr)
        sys.exit(1)

    output = args.output
    if not output:
        base = os.path.splitext(args.html_path)[0]
        ext = ".jpg" if args.format == "jpeg" else ".png"
        output = base + ext

    print(f"输入: {args.html_path}")
    print(f"输出: {output}")
    print()

    take_screenshot(
        args.html_path, output,
        width=args.width,
        max_height=args.max_height,
        fmt=args.format,
        quality=args.quality,
    )


if __name__ == "__main__":
    main()
