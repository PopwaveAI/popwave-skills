#!/usr/bin/env python3
"""
pop-visual-comic 漫画长图截图脚本 v1.0
- Playwright 逐元素截图 + Pillow 拼接，避免全页截图的底部质量退化
- 支持自动检测页面元素（.frame, .scene-break, .comic-page > *）
- 输出 PNG（无损）和 JPEG（分享用）

用法:
  python screenshot_comic.py <HTML文件路径或URL> [输出图片路径]

示例:
  python screenshot_comic.py "第1章/index.html" "第1章/漫画-第一章.png"
  python screenshot_comic.py "http://localhost:8000/index.html" "长图.jpg"

依赖:
  pip install playwright Pillow
  playwright install chromium

环境变量:
  SCREENSHOT_WIDTH - 截图视口宽度（默认820）
  SCREENSHOT_FORMAT - 输出格式 png/jpeg（默认png）
"""

import os
import sys
import time
from PIL import Image

def parse_args():
    if len(sys.argv) < 2:
        print("用法: python screenshot_comic.py <HTML路径或URL> [输出路径]")
        print("示例:")
        print('  python screenshot_comic.py "第1章/index.html" "第1章/长图.png"')
        print('  python screenshot_comic.py "http://localhost:8000/index.html" "长图.jpg"')
        sys.exit(1)

    source = sys.argv[1]

    # 默认输出路径
    if len(sys.argv) >= 3:
        output = sys.argv[2]
    else:
        base = os.path.splitext(source)[0]
        output = f"{base}_长图.png"

    # 确定格式
    ext = os.path.splitext(output)[1].lower()
    fmt = "jpeg" if ext in (".jpg", ".jpeg") else os.environ.get("SCREENSHOT_FORMAT", "png")

    return source, output, fmt


def screenshot_element_wise(source, output_path, fmt="png"):
    """逐元素截图 + 拼接，确保底部质量不退化。"""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[错误] 未安装 playwright，请执行: pip install playwright && playwright install chromium")
        sys.exit(1)

    width = int(os.environ.get("SCREENSHOT_WIDTH", "820"))
    temp_dir = os.path.join(os.environ.get("TEMP", "/tmp"), "comic_shots")
    os.makedirs(temp_dir, exist_ok=True)

    # 判断是URL还是文件路径
    if source.startswith("http://") or source.startswith("https://"):
        url = source
    else:
        # 转为绝对路径并启动本地HTTP服务器
        html_path = os.path.abspath(source)
        html_dir = os.path.dirname(html_path)
        url = f"file:///{html_path.replace(os.sep, '/')}"

    print(f"截图源: {url}")
    print(f"输出: {output_path} ({fmt})")
    print(f"视口宽度: {width}px")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": 1200})

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

        page.wait_for_timeout(1500)

        # 获取所有需要截图的元素
        all_elements = page.evaluate("""
            () => {
                const selectors = ['.frame', '.scene-break', '.comic-page > div:not(.frame)'];
                const elements = [];
                const seen = new Set();

                for (const sel of selectors) {
                    document.querySelectorAll(sel).forEach(el => {
                        if (!seen.has(el) && el.offsetHeight > 0) {
                            seen.add(el);
                            elements.push({
                                tag: el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''),
                                height: el.offsetHeight,
                                marker: 'shot_' + elements.length
                            });
                            el.setAttribute('data-screenshot-marker', 'shot_' + (elements.length - 1));
                        }
                    });
                }

                // 如果没找到任何元素，回退到 body 直接截图
                if (elements.length === 0) {
                    return [{tag: 'body', height: document.body.scrollHeight, marker: 'body'}];
                }

                return elements;
            }
        """)

        if not all_elements:
            # 回退：整页截图
            print("未检测到分帧元素，使用整页截图...")
            page.screenshot(path=output_path, full_page=True)
            browser.close()
            print(f"长图已保存: {output_path}")
            return

        print(f"检测到 {len(all_elements)} 个元素，逐个截图...")

        # 逐个元素截图
        frame_images = []
        for i, el_info in enumerate(all_elements):
            marker = el_info["marker"]
            tag = el_info["tag"]
            height = el_info["height"]

            try:
                if marker == "body":
                    page.screenshot(path=output_path, full_page=True)
                    browser.close()
                    print(f"长图已保存: {output_path}")
                    return

                element = page.locator(f'[data-screenshot-marker="{marker}"]')
                element.scroll_into_view_if_needed()
                page.wait_for_timeout(150)

                temp_path = os.path.join(temp_dir, f"el_{i:03d}.png")
                element.screenshot(path=temp_path)

                if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                    img = Image.open(temp_path)
                    frame_images.append(temp_path)
                    print(f"  [{i+1:02d}/{len(all_elements)}] {tag[:40]:40s} {img.width}x{img.height}px OK")
                else:
                    print(f"  [{i+1:02d}/{len(all_elements)}] {tag[:40]:40s} FAILED")
            except Exception as e:
                print(f"  [{i+1:02d}/{len(all_elements)}] {tag[:40]:40s} ERROR: {str(e)[:60]}")

        browser.close()

        if not frame_images:
            print("[错误] 所有元素截图失败", file=sys.stderr)
            sys.exit(1)

        # 拼接所有段
        print(f"\n拼接 {len(frame_images)} 张截图...")

        images = []
        max_width = 0
        for path in frame_images:
            img = Image.open(path)
            images.append(img)
            if img.width > max_width:
                max_width = img.width

        total_height = sum(img.height for img in images)
        print(f"画布尺寸: {max_width}x{total_height}px")

        # 创建画布
        result = Image.new('RGB', (max_width, total_height), (10, 10, 18))

        y_offset = 0
        for img in images:
            x_offset = (max_width - img.width) // 2
            result.paste(img, (x_offset, y_offset))
            y_offset += img.height

        # 保存
        save_kwargs = {}
        if fmt == "jpeg":
            save_kwargs = {"quality": 92, "optimize": True}
            # 确保RGB模式
            if result.mode != "RGB":
                result = result.convert("RGB")
            output_path = os.path.splitext(output_path)[0] + ".jpg"
        else:
            save_kwargs = {"optimize": True}
            output_path = os.path.splitext(output_path)[0] + ".png"

        result.save(output_path, format=fmt.upper(), **save_kwargs)

        file_size = os.path.getsize(output_path) / 1024
        print(f"\n长图已保存: {output_path}")
        print(f"尺寸: {max_width}x{total_height}px")
        print(f"文件大小: {file_size:.0f}KB")

        # 清理临时文件
        for path in frame_images:
            try:
                os.remove(path)
            except:
                pass
        try:
            os.rmdir(temp_dir)
        except:
            pass
        print("临时文件已清理")


def main():
    source, output, fmt = parse_args()
    screenshot_element_wise(source, output, fmt)


if __name__ == "__main__":
    main()
