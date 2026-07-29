#!/usr/bin/env python3
"""
HTML 图片内联化脚本
将 HTML 中所有本地图片引用替换为压缩 base64 data URI，使 HTML 完全自包含。

用法:
  python inline_html.py <html文件路径> [--width 800] [--quality 65]

popwave webview 安全策略禁止加载外部资源（相对路径、绝对路径、file:// 均不行）。
此脚本将图片压缩并内联为 data URI，确保 HTML 在 popwave 中正常显示。
原图片文件保留在 output/ 目录，不受影响。
"""

import argparse
import base64
import io
import os
import re
import sys


def inline_images(html_path, max_width=800, quality=65):
    """将 HTML 中的本地图片引用替换为压缩 base64 data URI"""
    try:
        from PIL import Image
    except ImportError:
        print("错误：Pillow 未安装，请运行 pip install Pillow", file=sys.stderr)
        sys.exit(1)

    base_dir = os.path.dirname(os.path.abspath(html_path))

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 匹配 src="相对路径" 的本地图片引用
    pattern = re.compile(
        r'src="((?:output/|\./|\.\\)[^"]*\.(?:png|jpg|jpeg|gif|webp))"',
        re.IGNORECASE,
    )

    total_img_bytes = 0
    replaced = 0

    def replace_src(match):
        nonlocal total_img_bytes, replaced
        src = match.group(1)
        img_path = os.path.join(base_dir, src.replace("/", os.sep))
        if not os.path.exists(img_path):
            print(f"  [MISS] {src} — 文件不存在，跳过")
            return match.group(0)

        img = Image.open(img_path)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # 缩放到指定宽度
        if img.width > max_width:
            ratio = max_width / img.width
            img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

        # 转 JPEG base64
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=quality)
        b64 = base64.b64encode(buf.getvalue()).decode()
        total_img_bytes += len(buf.getvalue())
        replaced += 1
        print(f"  [OK]   {src} → {len(buf.getvalue()) // 1024}KB")
        return f'src="data:image/jpeg;base64,{b64}"'

    html = pattern.sub(replace_src, html)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    total_kb = os.path.getsize(html_path) // 1024
    print(f"\n完成: 内联 {replaced} 张图片")
    print(f"HTML 总大小: {total_kb}KB ({total_kb / 1024:.1f}MB)")
    print(f"已覆盖: {html_path}")


def main():
    parser = argparse.ArgumentParser(description="HTML 图片内联化 — 将本地图片转为 base64 data URI")
    parser.add_argument("html_path", help="HTML 文件路径")
    parser.add_argument("--width", type=int, default=800, help="图片最大宽度像素（默认800）")
    parser.add_argument("--quality", type=int, default=65, help="JPEG 质量 1-100（默认65）")
    args = parser.parse_args()

    if not os.path.exists(args.html_path):
        print(f"错误：文件不存在: {args.html_path}", file=sys.stderr)
        sys.exit(1)

    print(f"内联化: {args.html_path}")
    print(f"参数: 最大宽度={args.width}px, JPEG质量={args.quality}")
    print()
    inline_images(args.html_path, args.width, args.quality)


if __name__ == "__main__":
    main()
