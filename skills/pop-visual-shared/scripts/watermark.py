#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pop-visual-shared 品牌水印脚本（图片一级，像素级注入）v1.0.0
=================================================================
用途：给所有生图产出（OC/封面/定妆/漫画页/素材）在**图片落地后**叠加半透明小字水印
`popwave.cn`。走工程化后处理，不进入生图提示词（避免污染 Seedream 文生图质量）。

为什么图片一级水印不用提示词：
  在提示词里要求"右下角写 popwave.cn"会挤压画面主体、干扰 Seedream 文生图，
  且文字渲染不稳定。改为图后处理，用 Pillow 精确控制位置/透明度/字号，稳定可控。

用法（CLI）:
  python watermark.py <图片路径> [更多图片路径...] [--text 文字] [--pos 位置] [--alpha 透明度] [--dry-run]
位置参数:
  图片路径（可多个，空格分隔）
选项:
  --text    水印文字，默认 "popwave.cn"
  --pos     右下/左下/右上/左上，默认 右下
  --alpha   透明度 0-255，默认 80（约 31% 不透明，可见但低调）
  --dry-run 只校验是否已含水印，不写入

幂等：通过**元数据标记**（PNG tEXt chunk / JPEG comment）判定已含水印，重复运行不叠加。
  比像素颜色检测可靠：颜色检测在低透明度+JPEG 有损压缩下会误判。

依赖：Pillow (pip install pillow)。
"""
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
except ImportError:
    print("[错误] 需要 Pillow。请先 `pip install pillow`。", file=sys.stderr)
    sys.exit(1)

DEFAULT_TEXT = "popwave.cn"
# 品牌色（暗红/砖红），与 popwave 视觉识别一致
BRAND_RGB = (176, 58, 66)
# 元数据标记键（幂等检测依据）
META_KEY = "popwave_watermark"
META_VAL = "1"
# 默认透明度（0-255，值越小越淡）；80 ≈ 31% 不透明，可见但低调
DEFAULT_ALPHA = 80
# 水印相对图片宽度的字号比例（很小，不抢焦点）
FONT_RATIO = 0.025
# 距边缘的边距比例
MARGIN_RATIO = 0.02


def _load_font(size):
    """尝试加载中文字体，找不到则回退默认。"""
    candidates = [
        "C:/Windows/Fonts/msyh.ttc",   # 微软雅黑
        "C:/Windows/Fonts/msyhbd.ttc",
        "C:/Windows/Fonts/simhei.ttf", # 黑体
        "C:/Windows/Fonts/simsun.ttc", # 宋体
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _has_watermark(path):
    """幂等检测：读取图片元数据标记。"""
    try:
        img = Image.open(path)
        if img.format == "PNG":
            return dict(img.text).get(META_KEY) == META_VAL
        elif img.format in ("JPEG",):
            return img.info.get("comment") == META_VAL.encode("utf-8")
        else:
            return False
    except Exception:
        return False


def _write_meta(img, path):
    """写入水印元数据标记（保存前设置）。"""
    img.info[META_KEY] = META_VAL


def add_watermark(path, text=DEFAULT_TEXT, pos="右下", alpha=DEFAULT_ALPHA, dry_run=False):
    """给单张图片叠加半透明水印。返回 (已处理, 是否已含水印)。"""
    if not os.path.exists(path):
        print(f"  [跳过] 文件不存在: {path}", file=sys.stderr)
        return False, False

    if _has_watermark(path):
        print(f"  [幂等] 已含水印，跳过: {os.path.basename(path)}")
        return False, True

    if dry_run:
        print(f"  [dry-run] 未含水印，将添加: {os.path.basename(path)}")
        return False, False

    img = Image.open(path).convert("RGBA")
    w, h = img.size
    font_size = max(10, int(w * FONT_RATIO))
    font = _load_font(font_size)

    # 用临时图层测量文字尺寸
    probe = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(probe)
    bbox = pdraw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    margin = int(w * MARGIN_RATIO)
    if pos == "右下":
        x = w - tw - margin
        y = h - th - margin
    elif pos == "左下":
        x = margin
        y = h - th - margin
    elif pos == "右上":
        x = w - tw - margin
        y = margin
    else:  # 左上
        x = margin
        y = margin

    # 创建水印层：品牌色文字 + 低透明度
    wm = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(wm)
    draw.text((x, y), text, font=font, fill=(BRAND_RGB[0], BRAND_RGB[1], BRAND_RGB[2], alpha))

    # 叠加
    out = Image.alpha_composite(img, wm)
    ext = os.path.splitext(path)[1].lower()
    tmp = path + ".tmp"

    if ext in (".jpg", ".jpeg"):
        out = out.convert("RGB")
        out.info[META_KEY] = META_VAL
        out.save(tmp, "JPEG", quality=95, comment=META_VAL.encode("utf-8"))
    else:
        meta = PngImagePlugin.PngInfo()
        meta.add_text(META_KEY, META_VAL)
        out.save(tmp, "PNG", optimize=True, pnginfo=meta)
    os.replace(tmp, path)
    print(f"  [OK] 已加水印: {os.path.basename(path)} ({pos}, alpha={alpha})")
    return True, False


def main():
    argv = sys.argv[1:]
    opts = {"--text": DEFAULT_TEXT, "--pos": "右下", "--alpha": DEFAULT_ALPHA, "--dry-run": False}
    paths = []
    j = 0
    while j < len(argv):
        a = argv[j]
        if a in ("--text", "--pos", "--alpha"):
            opts[a] = argv[j + 1]
            j += 2
        elif a == "--dry-run":
            opts["--dry-run"] = True
            j += 1
        else:
            paths.append(a)
            j += 1

    if not paths:
        print(__doc__)
        sys.exit(2)

    ok = True
    for path in paths:
        processed, already = add_watermark(
            path,
            text=opts["--text"],
            pos=opts["--pos"],
            alpha=int(opts["--alpha"]),
            dry_run=opts["--dry-run"],
        )
        if not processed and not already:
            ok = False
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()