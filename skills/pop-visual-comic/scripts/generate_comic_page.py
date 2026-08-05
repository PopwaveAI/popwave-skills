#!/usr/bin/env python3
"""
pop-visual-comic 逐页漫画任务清单导出脚本 v5.0.0
================================================
生图改为由主 agent 调用 `image_generate` 工具完成，本脚本不再直调任何 HTTP API、不再内置 API Key。

职责：
  1. 从下方 PAGES 列表读取每页的 id + prompt + ref_images + size
  2. 做文字控制占位符（NEG<DIALOGUE>/NEG<TEXT>）替换 + 尺寸安全校验
  3. 解析角色定妆图参考路径（REF_IMAGES 字段）
  4. 导出 `generation_tasks.json`（每页一条任务：id/prompt/size/ref_images/output_path）
  5. 打印"请用 image_generate 工具逐张生成"的指引

主 agent 用法：
  1. 修改下方 PAGES 列表（每页的 id + prompt + ref_images + 可选 size）
  2. 修改 OUTPUT_DIR / CHAR_ASSETS_DIR
  3. 运行: python generate_comic_page.py
  4. 读取生成的第{N}章/output/generation_tasks.json
  5. 对每条任务调用 image_generate 工具（prompt/text=任务prompt, size=任务size, output=任务output_path，参考图按工具能力传入）
  6. 生成后用 ensure_png_format 校验（本脚本已内置校验函数）

依赖:
  pip install Pillow
"""

import base64
import json
import os
import sys

# ============ 配置区（使用前修改） ============

SIZE = "1125x1500"           # 竖版漫画页（总像素 169 万 ≤ 236 万上限）
MAX_PIXELS = 2360000         # 超 236 万像素计费翻倍，所有出图必须 ≤ 上限

# 输出目录（章节级）
OUTPUT_DIR = r"第1章/output"

# 定妆图根目录（项目级，跨章复用）
CHAR_ASSETS_DIR = r"assets/characters"

# 页面列表（每页是一张包含多格的完整漫画图）
PAGES = [
    {
        "id": "page1",
        "prompt": "A vertical manga comic page with 4 panels arranged in a 2x2 grid. "
                  "Panel 1: A thin girl crouches before a broken stove, stirring porridge. "
                  "Panel 2: Close-up of her face, firelight illuminating her tired eyes. "
                  "Panel 3: She walks through a muddy street carrying a basket. "
                  "Panel 4: A tall merchant grabs her wrist at a market stall. "
                  "Dark fantasy semi-realistic manga style, watercolor texture, muted tones with warm firelight accents. "
                  "NEG<TEXT>",  # 见下方 text_control 常量，生成时替换为锁定负面词
        "ref_images": ["char-苏午-v1.png"],  # 角色定妆图参考（可多张）
        "size": "1125x1500",  # 可选，默认用 SIZE（总像素须 ≤236万）
    },
    # ... 更多页请自行添加
]

# ===== 文字控制负面词（2026-08-03 实测锁定，见 references/content-layer.md §六）=====
# 对话场景（角色开口/对峙）：NEG_DIALOGUE —— 禁气泡，防伪对话乱字
TEXT_CONTROL_DIALOGUE = (
    "No speech bubbles, no dialogue balloons, no thought bubbles, no caption boxes, no dialogue text, "
    "no quotes, no sound effect text. The characters speak purely through their expressions and posture, "
    "NO text bubbles anywhere. No text, no letters, no numbers, no words, no typography, no labels, "
    "no captions, no inscriptions, no writing, no calligraphy, no handwriting, no glyphs, no symbols, "
    "no runes, no icons, no logos, no dial numerals, no roman numerals. Pure visual imagery only, "
    "no readable characters anywhere."
)
# 非对话场景：NEG_STRONG
TEXT_CONTROL_STRONG = (
    "No text, no letters, no numbers, no words, no typography, no labels, no captions, no inscriptions, "
    "no writing, no calligraphy, no handwriting, no glyphs, no symbols, no runes, no icons, no logos, "
    "no dial numerals, no roman numerals. Pure visual imagery only, no readable characters anywhere."
)

# ============ 通用工具 ============


def _assert_size_safe(size):
    """校验尺寸总像素 ≤ MAX_PIXELS。超限/无法解析则报错中止。"""
    if not size:
        return
    s = str(size).strip().lower()
    if "x" in s:
        try:
            w, h = s.split("x")
            pixels = int(w) * int(h)
        except Exception:
            print(f"  [错误] 无法解析尺寸: {size}", file=sys.stderr)
            sys.exit(1)
    else:
        rating = {"1k": 1024, "2k": 2048, "4k": 4096}.get(s)
        if rating is None:
            print(f"  [错误] 未知尺寸档位: {size}", file=sys.stderr)
            sys.exit(1)
        pixels = rating * rating
    if pixels > MAX_PIXELS:
        print(
            f"  [错误] 尺寸 {size} = {pixels} 像素，超过上限 {MAX_PIXELS} 像素"
            f"（超 236 万像素计费翻倍），已中止。",
            file=sys.stderr,
        )
        sys.exit(1)


def resolve_ref_image(ref_name):
    """根据定妆图文件名查找完整路径"""
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), "assets", "characters", ref_name),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path.replace("\\", "/")
    print(f"  [警告] 定妆图未找到: {ref_name}", file=sys.stderr)
    return None


def ensure_png_format(path):
    """检测文件实际格式，若以 .png 保存但实际是 JPEG 则转码为真 PNG。"""
    if not os.path.exists(path):
        return
    with open(path, "rb") as f:
        header = f.read(8)
    if header[:3] == b'\xff\xd8\xff':  # JPEG magic bytes
        try:
            from PIL import Image
        except ImportError:
            print(f"  [警告] 文件为JPEG内容但Pillow未安装，无法转码: {path}", file=sys.stderr)
            return
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        tmp = path + ".tmp"
        img.save(tmp, "PNG", optimize=True)
        os.replace(tmp, path)
        print(f"  [格式修正] JPEG → PNG 转码: {os.path.basename(path)}")


def export_tasks():
    """把 PAGES 列表导出为 generation_tasks.json，供主 agent 用 image_generate 工具逐张生成。"""
    out_dir = OUTPUT_DIR
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", out_dir)
    os.makedirs(out_dir, exist_ok=True)

    tasks = []
    print("\n定妆图映射检查:")
    for page in PAGES:
        # 文字控制占位符替换
        prompt = page["prompt"]
        prompt = prompt.replace("NEG<DIALOGUE>", TEXT_CONTROL_DIALOGUE)
        prompt = prompt.replace("NEG<TEXT>", TEXT_CONTROL_STRONG)
        if len(prompt) > 2200:
            print(f"  [警告] {page['id']} 提示词过长: {len(prompt)} 字符")

        size = page.get("size", SIZE)
        _assert_size_safe(size)

        # 解析参考图路径
        ref_images = page.get("ref_images", [])
        resolved_refs = []
        for ref_name in ref_images:
            ref_path = resolve_ref_image(ref_name)
            if ref_path:
                resolved_refs.append(ref_path)

        output_path = os.path.join(out_dir, f"{page['id']}.png").replace("\\", "/")
        tasks.append({
            "id": page["id"],
            "prompt": prompt,
            "size": size,
            "ref_images": resolved_refs,
            "output_path": output_path,
        })
        if resolved_refs:
            print(f"  {page['id']}: refs={', '.join(os.path.basename(r) for r in resolved_refs)}  size={size}")
        else:
            print(f"  {page['id']}: 文生图  size={size}")

    # 导出任务清单
    meta = {
        "total_pages": len(PAGES),
        "generator": "generate_comic_page.py v5.0.0",
        "note": "用 image_generate 工具逐条生成，输出到每条任务的 output_path",
        "tasks": tasks,
    }
    meta_path = os.path.join(out_dir, "generation_tasks.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"已导出 {len(tasks)} 条生图任务 → {meta_path.replace(os.sep, '/')}")
    print("=" * 60)
    print("\n主 agent 请按以下方式用 image_generate 工具逐张生成：")
    print("  对 generation_tasks.json 中每条任务：")
    print("    image_generate(prompt=<任务prompt>, size=<任务size>, output=<任务output_path>)")
    print("  图生图（有 ref_images 时）：按 image_generate 工具能力传入参考图，保证角色一致性。")
    print("  生成完成后本脚本的 ensure_png_format 可校验格式，必要时手动转码。")
    return meta_path


if __name__ == "__main__":
    export_tasks()