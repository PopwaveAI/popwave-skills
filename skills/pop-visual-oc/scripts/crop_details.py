#!/usr/bin/env python3
"""
pop-visual-oc 3A设定集 细节特写裁图脚本 v1.0
- 从主视觉（已有存量图）按相对坐标裁剪出细节特写局部图，复用存量视觉，不新增 AI 生图
- 引线不在 PIL 画（避免定位不准），由 HTML SVG 叠加（更可控）
- config 用 JSON 定义：裁剪框（相对主视觉的 x/y/w/h，0-1）+ 标签 + 输出尺寸

用法:
  python crop_details.py <源图> <输出目录> --config <xxx.json>

示例 config.json:
{
  "details": [
    {"x": 0.62, "y": 0.10, "w": 0.34, "h": 0.26, "out": "detail-face", "label": "青丝落尽·眉眼藏锋", "scale": 1.0},
    {"x": 0.10, "y": 0.55, "w": 0.30, "h": 0.30, "out": "detail-bird", "label": "白鸟栖肩", "scale": 1.0}
  ]
}

说明:
- x/y/w/h 均为主视觉宽高的相对比例（0-1），从左上角计算
- scale: 输出放大倍率（默认1.0）。裁出后按此倍率放大，保证细节图清晰
- 输出: <输出目录>/<out>.jpg，JPEG 高质量（quality=92）
- 若提供 --sheet，会将所有细节按网格拼成一张 sheet 图（供 HTML 一次性引用）

依赖:
  pip install pillow
"""

import json
import os
import sys


def parse_args():
    args = sys.argv[1:]
    source = None
    out_dir = None
    config = None
    sheet = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--config" and i + 1 < len(args):
            config = args[i + 1]
            i += 2
        elif a == "--sheet":
            sheet = True
            i += 1
        elif source is None:
            source = a
            i += 1
        elif out_dir is None:
            out_dir = a
            i += 1
        else:
            i += 1
    if not source or not out_dir or not config:
        print("用法: python crop_details.py <源图> <输出目录> --config <xxx.json> [--sheet]")
        sys.exit(1)
    return source, out_dir, config, sheet


def main():
    source, out_dir, config_path, sheet = parse_args()

    try:
        from PIL import Image
    except ImportError:
        print("[错误] 未安装 pillow，请执行: pip install pillow")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    img = Image.open(source)
    W, H = img.size
    os.makedirs(out_dir, exist_ok=True)

    print(f"源图: {source} ({W}x{H})")
    print(f"输出目录: {out_dir}")
    print(f"细节数: {len(cfg['details'])}\n")

    results = []
    for i, d in enumerate(cfg["details"]):
        x = int(d["x"] * W)
        y = int(d["y"] * H)
        w = int(d["w"] * W)
        h = int(d["h"] * H)
        # 边界裁剪
        x = max(0, x)
        y = max(0, y)
        w = min(w, W - x)
        h = min(h, H - y)
        box = (x, y, x + w, y + h)
        crop = img.crop(box)
        scale = d.get("scale", 1.0)
        if scale != 1.0:
            crop = crop.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
        out_name = d["out"] + ".jpg"
        out_path = os.path.join(out_dir, out_name)
        crop.save(out_path, "JPEG", quality=92)
        label = d.get("label", "")
        results.append({"file": out_name, "label": label, "box": box, "size": f"{crop.width}x{crop.height}"})
        print(f"  [{i+1}] {out_name}  box={box}  size={crop.width}x{crop.height}  label={label}")

    if sheet:
        sheet_path = os.path.join(out_dir, "_details_sheet.jpg")
        cols = cfg.get("sheet_cols", len(results))
        tsize = 320
        rows = (len(results) + cols - 1) // cols
        sheet_img = Image.new("RGB", (cols * tsize, rows * tsize), (10, 12, 18))
        for i, r in enumerate(results):
            c = Image.open(os.path.join(out_dir, r["file"]))
            c.thumbnail((tsize - 8, tsize - 8), Image.LANCZOS)
            px = (i % cols) * tsize + (tsize - c.width) // 2
            py = (i // cols) * tsize + (tsize - c.height) // 2
            sheet_img.paste(c, (px, py))
        sheet_img.save(sheet_path, "JPEG", quality=92)
        print(f"\n详情sheet: {sheet_path} ({sheet_img.width}x{sheet_img.height})")

    print("\n完成。请将上述 file/label 填入 album-3a-*.tpl.html 的 detail 区，引线由 SVG 叠加。")


if __name__ == "__main__":
    main()