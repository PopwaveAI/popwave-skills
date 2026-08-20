#!/usr/bin/env python3
"""
漫画拼图脚本 — 纯 Pillow 实现
零留白 / 严丝合缝 / 无 HTML 依赖 / 直接输出长图

替代旧版 HTML 组装 + inline_html.py + screenshot_html.py 三步流程。
直接将分镜帧拼合成漫画长图，叠加旁白文字，输出最终图片。

用法:
  python assemble_comic.py <config.json>
  python assemble_comic.py <config.json> --output output.jpg

config.json 格式:
{
  "title": "诡秘之主",
  "subtitle": "第一章 · 绯红",
  "frames_dir": "path/to/frames",
  "output": "path/to/output.jpg",
  "output_format": "jpeg",        // jpeg(默认) 或 png
  "jpeg_quality": 92,
  "footer": "popwave",
  "frames": [
    {"file": "frame1.png", "layout": "full",   "position": "center 15%", "caption": "旁白文字"},
    {"file": "frame2.png", "layout": "full",   "position": "center"},
    {"separator": "line"},
    {"file": "frame3.png", "layout": "scene",  "position": "center",     "caption": "名场面旁白", "style": "feature"},
    {"file": "frame4.png", "layout": "half",   "position": "center 25%", "caption": "旁白"},
    {"file": "frame5.png", "layout": "half",   "position": "center",     "caption": "旁白"},
    {"separator": "line"},
    {"file": "frame6.png", "layout": "full",   "position": "center 35%", "caption": "旁白"},
    {"file": "frame7.png", "layout": "impact", "position": "center 30%", "caption": "冲击旁白", "style": "impact"},
    {"separator": "line"},
    {"file": "frame8.png", "layout": "hook",   "position": "center 55%", "caption": "钩子文字", "style": "hook"}
  ]
}

layout 类型:
  full   — 全宽格 (16:9)
  scene  — 名场面格 (2:3，更大)
  impact — 冲击格 (2:1)
  hook   — 章末钩子格 (16:9，暗角+居中文字)
  half   — 半宽格 (1:1，自动配对并排)

style 类型 (可选，默认按 layout 自动推断):
  normal  — 普通黑边
  feature — 粗黑边+红色发光
  impact  — 粗白边+橙色发光
  hook    — 无边框+暗角

position (可选，默认 "center"):
  "center"       — 居中
  "center 30%"   — 垂直30%位置
  "top"          — 顶部
  "bottom"       — 底部
"""

import argparse
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

try:
    LANCZOS = Image.Resampling.LANCZOS
except AttributeError:
    LANCZOS = Image.LANCZOS

# === 页面参数 ===
PAGE_WIDTH = 900
PAGE_PADDING = 24
PAGE_BG = (245, 240, 232)      # #f5f0e8
GUTTER = 4                      # 格间间距
CONTENT_W = PAGE_WIDTH - PAGE_PADDING * 2  # 852
HALF_W = (CONTENT_W - GUTTER) // 2         # 424

# 分隔线
SEP_HEIGHT = 2
SEP_PADDING_V = 8
SEP_COLOR = (51, 51, 51)

# 边框
BORDER_COLOR = (26, 26, 26)
BORDER_WHITE = (255, 255, 255)
GLOW_FEATURE = (200, 30, 30)
GLOW_IMPACT = (255, 90, 20)

# 标题
TITLE_SIZE = 26
SUBTITLE_SIZE = 13
TITLE_COLOR = (42, 26, 10)
SUBTITLE_COLOR = (138, 122, 106)

# 旁白
CAPTION_SIZE = 15
CAPTION_PAD_H = 10
CAPTION_PAD_V = 6
CAPTION_BG_ALPHA = 190
CAPTION_TEXT_COLOR = (255, 255, 255)

# 钩子文字
HOOK_SIZE = 22
HOOK_COLOR = (255, 255, 255)

# 页脚
FOOTER_SIZE = 11
FOOTER_COLOR = (170, 170, 170)

# 字体路径
_FONT_PATHS = [
    "C:\\Windows\\Fonts\\msyh.ttc",
    "C:\\Windows\\Fonts\\simhei.ttf",
    "C:\\Windows\\Fonts\\Deng.ttf",
    "C:\\Windows\\Fonts\\simsun.ttc",
]
_font_cache = {}


def get_font(size):
    """加载中文字体（带缓存）"""
    if size in _font_cache:
        return _font_cache[size]
    for path in _FONT_PATHS:
        try:
            if os.path.exists(path):
                font = ImageFont.truetype(path, size)
                _font_cache[size] = font
                return font
        except Exception:
            continue
    font = ImageFont.load_default()
    _font_cache[size] = font
    return font


# === 布局高度 ===
def calc_height(layout):
    """根据布局类型计算格子高度（像素）"""
    if layout == "full":   return round(CONTENT_W * 9 / 16)   # 479
    if layout == "scene":  return round(CONTENT_W * 2 / 3)    # 568
    if layout == "impact": return round(CONTENT_W * 1 / 2)    # 426
    if layout == "hook":   return round(CONTENT_W * 9 / 16)   # 479
    if layout == "half":   return HALF_W                      # 424
    return round(CONTENT_W * 9 / 16)


def resolve_style(frame):
    """从 frame 字典解析 style（默认按 layout 推断）"""
    style = frame.get("style")
    if style:
        return style
    layout = frame.get("layout", "full")
    if layout == "hook":    return "hook"
    if layout == "impact":  return "impact"
    if layout == "scene":   return "feature"
    return "normal"


# === 图片裁剪填充 ===
def cover_crop(img, target_w, target_h, position="center"):
    """
    将图片裁剪填充到目标尺寸（类似 CSS object-fit:cover）。
    确保零留白——图片完全填充目标区域，不变形。
    """
    if img.mode != "RGB":
        img = img.convert("RGB")
    src_w, src_h = img.size
    if src_w == 0 or src_h == 0:
        return Image.new("RGB", (target_w, target_h), (0, 0, 0))

    src_ratio = src_w / src_h
    dst_ratio = target_w / target_h

    if src_ratio > dst_ratio:
        new_w = int(src_h * dst_ratio)
        x0 = _parse_x(position, src_w, new_w)
        img = img.crop((x0, 0, x0 + new_w, src_h))
    else:
        new_h = int(src_w / dst_ratio)
        y0 = _parse_y(position, src_h, new_h)
        img = img.crop((0, y0, src_w, y0 + new_h))

    return img.resize((target_w, target_h), LANCZOS)


def _parse_y(position, src_h, crop_h):
    """解析 y 方向位置: 'center 30%' → 像素偏移"""
    if not position or position == "center":
        return (src_h - crop_h) // 2
    parts = position.split()
    if len(parts) >= 2:
        v, h = parts[0], parts[1]
        if v == "top":    return 0
        if v == "bottom": return max(0, src_h - crop_h)
        if v == "center":
            if h.endswith("%"):
                return int((src_h - crop_h) * float(h[:-1]) / 100)
            return (src_h - crop_h) // 2
    if position == "top":    return 0
    if position == "bottom": return max(0, src_h - crop_h)
    return (src_h - crop_h) // 2


def _parse_x(position, src_w, crop_w):
    """解析 x 方向位置"""
    if not position or "center" in position:
        return (src_w - crop_w) // 2
    if "left" in position:  return 0
    if "right" in position: return max(0, src_w - crop_w)
    return (src_w - crop_w) // 2


# === 文字换行 ===
def wrap_text(text, font, max_width, draw):
    """中文逐字换行"""
    lines = []
    current = ""
    for char in text:
        test = current + char
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] > max_width and current:
            lines.append(current)
            current = char
        else:
            current = test
    if current:
        lines.append(current)
    return lines


# === 边框 ===
def draw_border(canvas, x, y, w, h, style):
    """在格子内侧绘制边框"""
    if style == "hook":
        return
    draw = ImageDraw.Draw(canvas)
    if style == "feature":
        draw.rectangle([x, y, x + w - 1, y + h - 1], outline=BORDER_COLOR, width=3)
        _draw_glow(canvas, x, y, w, h, GLOW_FEATURE)
    elif style == "impact":
        draw.rectangle([x, y, x + w - 1, y + h - 1], outline=BORDER_WHITE, width=3)
        _draw_glow(canvas, x, y, w, h, GLOW_IMPACT)
    else:
        draw.rectangle([x, y, x + w - 1, y + h - 1], outline=BORDER_COLOR, width=2)


def _draw_glow(canvas, x, y, w, h, color):
    """在格子外侧绘制半透明发光（简化版）"""
    glow_w, glow_h = w + 8, h + 8
    glow = Image.new("RGBA", (glow_w, glow_h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(4):
        alpha = int(60 * (1 - i / 4))
        gd.rectangle([4 - i, 4 - i, glow_w - 5 + i, glow_h - 5 + i],
                     outline=(*color, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=3))
    canvas.paste(glow, (x - 4, y - 4), glow)


# === 暗角 ===
def draw_vignette(canvas, x, y, w, h):
    """绘制径向暗角效果（高效版：小图渐变+放大）"""
    small = 60
    vignette = Image.new("L", (small, small), 0)
    px = vignette.load()
    cx = cy = small / 2
    max_dist = (cx ** 2 + cy ** 2) ** 0.5
    for py in range(small):
        for pxi in range(small):
            dist = ((pxi - cx) ** 2 + (py - cy) ** 2) ** 0.5
            px[pxi, py] = min(int(200 * (dist / max_dist) ** 1.5), 200)
    vignette = vignette.resize((w, h), LANCZOS)
    black = Image.new("RGB", (w, h), (0, 0, 0))
    canvas.paste(black, (x, y), vignette)


# === 旁白 ===
def draw_caption(canvas, x, y, w, h, text, style):
    """在格子上绘制旁白文字"""
    if not text:
        return
    draw = ImageDraw.Draw(canvas)

    if style == "hook":
        draw_vignette(canvas, x, y, w, h)
        font = get_font(HOOK_SIZE)
        lines = wrap_text(text, font, w - 60, draw)
        line_h = HOOK_SIZE + 4
        total_h = len(lines) * line_h
        ty = y + h - total_h - int(h * 0.15)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            tw = bbox[2] - bbox[0]
            tx = x + (w - tw) // 2
            for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                draw.text((tx + dx, ty + dy), line, font=font, fill=(0, 0, 0))
            draw.text((tx, ty), line, font=font, fill=HOOK_COLOR)
            ty += line_h
    else:
        font = get_font(CAPTION_SIZE)
        lines = wrap_text(text, font, w - CAPTION_PAD_H * 2, draw)
        line_h = CAPTION_SIZE + 3
        bar_h = len(lines) * line_h + CAPTION_PAD_V * 2
        bar_y = y + h - bar_h
        bar = Image.new("RGBA", (w, bar_h), (0, 0, 0, CAPTION_BG_ALPHA))
        canvas.paste(bar, (x, bar_y), bar)
        ty = bar_y + CAPTION_PAD_V
        for line in lines:
            draw.text((x + CAPTION_PAD_H, ty), line, font=font, fill=CAPTION_TEXT_COLOR)
            ty += line_h


# === 分隔线 ===
def draw_separator(canvas, y):
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([PAGE_PADDING, y, PAGE_PADDING + CONTENT_W - 1, y + SEP_HEIGHT - 1],
                   fill=SEP_COLOR)


# === 标题 ===
def draw_title(canvas, y, title, subtitle):
    """绘制标题+副标题，返回占用高度"""
    draw = ImageDraw.Draw(canvas)
    h = 0
    if title:
        font = get_font(TITLE_SIZE)
        bbox = draw.textbbox((0, 0), title, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((PAGE_WIDTH - tw) // 2, y), title, font=font, fill=TITLE_COLOR)
        h = TITLE_SIZE + 6
    if subtitle:
        font = get_font(SUBTITLE_SIZE)
        bbox = draw.textbbox((0, 0), subtitle, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((PAGE_WIDTH - tw) // 2, y + h), subtitle, font=font, fill=SUBTITLE_COLOR)
        h += SUBTITLE_SIZE + 4
    h += 16
    return h


# === 页脚 ===
def draw_footer(canvas, y, text="popwave"):
    font = get_font(FOOTER_SIZE)
    draw = ImageDraw.Draw(canvas)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((PAGE_WIDTH - tw) // 2, y), text, font=font, fill=FOOTER_COLOR)
    return FOOTER_SIZE + 4


# === 行解析 ===
def parse_rows(frames):
    """
    将 frames 列表解析为行。
    返回 [("separator", None), ("full", frame), ("half_pair", (left, right)), ...]
    """
    rows = []
    i = 0
    while i < len(frames):
        item = frames[i]
        if item.get("separator"):
            rows.append(("separator", None))
            i += 1
        elif item.get("layout") == "half" and \
                i + 1 < len(frames) and \
                frames[i + 1].get("layout") == "half":
            rows.append(("half_pair", (item, frames[i + 1])))
            i += 2
        else:
            if item.get("layout") == "half":
                print(f"  [WARN] half 格未配对，当全宽处理: {item.get('file', '?')}")
            rows.append(("full", item))
            i += 1
    return rows


# === 总高度 ===
def calc_total_height(rows, title, subtitle, footer):
    total = PAGE_PADDING
    if title or subtitle:
        total += draw_title_height(title, subtitle)
    for i, (rtype, _) in enumerate(rows):
        if rtype == "separator":
            total += SEP_PADDING_V * 2 + SEP_HEIGHT
        elif rtype == "half_pair":
            total += calc_height("half")
        else:
            total += calc_height(rows[i][1].get("layout", "full"))
        if i < len(rows) - 1:
            total += GUTTER
    if footer:
        total += GUTTER + FOOTER_SIZE + 4
    total += PAGE_PADDING
    return total


def draw_title_height(title, subtitle):
    h = 0
    if title:   h += TITLE_SIZE + 6
    if subtitle: h += SUBTITLE_SIZE + 4
    h += 16
    return h


# === 单格绘制 ===
def draw_panel(canvas, x, y, w, h, frame, frames_dir):
    """绘制单个格子：图片裁剪+边框+旁白"""
    fname = frame.get("file", "")
    path = os.path.join(frames_dir, fname)
    if not os.path.exists(path):
        print(f"  [MISS] {fname} — 用黑底填充")
        img = Image.new("RGB", (w, h), (0, 0, 0))
    else:
        img = Image.open(path)
        img = cover_crop(img, w, h, frame.get("position", "center"))
    canvas.paste(img, (x, y))

    style = resolve_style(frame)
    draw_border(canvas, x, y, w, h, style)
    draw_caption(canvas, x, y, w, h, frame.get("caption"), style)


# === 主拼图 ===
def assemble(config):
    """主拼图函数"""
    title = config.get("title", "")
    subtitle = config.get("subtitle", "")
    frames_dir = config.get("frames_dir", ".")
    output = config.get("output", "comic_output.jpg")
    fmt = config.get("output_format", "jpeg")
    quality = config.get("jpeg_quality", 92)
    footer = config.get("footer", "popwave")
    frames = config.get("frames", [])

    if not frames:
        print("错误：frames 列表为空", file=sys.stderr)
        return False

    print(f"拼图配置:")
    print(f"  页面宽度: {PAGE_WIDTH}px | 内容宽度: {CONTENT_W}px | 半宽: {HALF_W}px")
    print(f"  帧数: {len(frames)} | 帧目录: {frames_dir}")
    print(f"  输出: {output} ({fmt})")
    print()

    rows = parse_rows(frames)
    total_h = calc_total_height(rows, title, subtitle, footer)
    print(f"  行数: {len(rows)} | 画布总高度: {total_h}px")

    canvas = Image.new("RGB", (PAGE_WIDTH, total_h), PAGE_BG)

    # 标题
    cursor_y = PAGE_PADDING
    if title or subtitle:
        cursor_y += draw_title(canvas, cursor_y, title, subtitle)

    # 帧
    for i, (rtype, rdata) in enumerate(rows):
        if rtype == "separator":
            cursor_y += SEP_PADDING_V
            draw_separator(canvas, cursor_y)
            cursor_y += SEP_HEIGHT + SEP_PADDING_V
        elif rtype == "half_pair":
            h = calc_height("half")
            left, right = rdata
            draw_panel(canvas, PAGE_PADDING, cursor_y, HALF_W, h, left, frames_dir)
            draw_panel(canvas, PAGE_PADDING + HALF_W + GUTTER, cursor_y,
                       HALF_W, h, right, frames_dir)
            cursor_y += h
        else:
            layout = rdata.get("layout", "full")
            h = calc_height(layout)
            draw_panel(canvas, PAGE_PADDING, cursor_y, CONTENT_W, h, rdata, frames_dir)
            cursor_y += h
        if i < len(rows) - 1:
            cursor_y += GUTTER

    # 页脚
    if footer:
        cursor_y += GUTTER
        cursor_y += draw_footer(canvas, cursor_y, footer)

    # 保存
    if fmt == "jpeg":
        canvas.save(output, "JPEG", quality=quality, optimize=True)
    else:
        canvas.save(output, "PNG")

    size_kb = os.path.getsize(output) // 1024
    size_str = f"{size_kb / 1024:.1f}MB" if size_kb >= 1024 else f"{size_kb}KB"
    print(f"\n✅ 完成: {output} ({size_str}, {PAGE_WIDTH}x{total_h})")
    return True


def main():
    parser = argparse.ArgumentParser(description="漫画拼图 — 纯 Pillow，零留白/严丝合缝")
    parser.add_argument("config", help="JSON 配置文件路径")
    parser.add_argument("--output", "-o", help="覆盖配置中的输出路径")
    args = parser.parse_args()

    if not os.path.exists(args.config):
        print(f"错误：配置文件不存在: {args.config}", file=sys.stderr)
        sys.exit(1)

    with open(args.config, "r", encoding="utf-8") as f:
        config = json.load(f)
    if args.output:
        config["output"] = args.output

    sys.exit(0 if assemble(config) else 1)


if __name__ == "__main__":
    main()
