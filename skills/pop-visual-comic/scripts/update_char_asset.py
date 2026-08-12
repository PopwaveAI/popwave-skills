#!/usr/bin/env python3
"""
pop-visual-comic 增量角色定妆图任务清单导出脚本 v2.0.0
========================================================
当角色外观变化时，导出"增量定妆图"生图任务，由主 agent 用 `image_generate` 工具生成。
本脚本不再直调任何 HTTP API、不再内置 API Key。

用法:
  python update_char_asset.py \
    --char-name "索伦" \
    --version 2 \
    --base-prompt "一个18岁的瘦削男性角色..." \
    --change-desc "觉醒后瞳色变金，左手机械化" \
    --output "assets/characters/char-soren-v2.png"

  可选参考图: --ref-image "assets/characters/char-soren-v1.png"

脚本导出单条任务到 stdout（或 --task-output 指定 JSON 文件），
主 agent 读取后调用 image_generate 工具生成。

生成后需手动将新提示词冻结到漫画角色库.md（作为 v2 的冻结提示词）
"""

import argparse
import json
import os
import sys

SIZE = "1125x1500"           # 增量定妆图（总像素 169 万 ≤ 236 万上限）
MAX_PIXELS = 2360000         # 超 236 万像素计费翻倍，所有出图必须 ≤ 上限


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


def ensure_png_format(path):
    """检测文件实际格式，若以 .png 保存但实际是 JPEG 则转码为真 PNG。"""
    if not os.path.exists(path):
        return
    with open(path, "rb") as f:
        header = f.read(8)
    if header[:3] == b'\xff\xd8\xff':
        try:
            from PIL import Image
        except ImportError:
            print(f"  [警告] Pillow未安装，无法转码: {path}", file=sys.stderr)
            return
        img = Image.open(path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        tmp = path + ".tmp"
        img.save(tmp, "PNG", optimize=True)
        os.replace(tmp, path)
        print(f"  [格式修正] JPEG → PNG 转码: {os.path.basename(path)}")


def build_task(char_name, version, base_prompt, change_desc, output_path, ref_image=None):
    """组装增量定妆任务。返回 {task, new_prompt}。"""
    # 组装新提示词：冻结提示词 + 变化描述
    new_prompt = f"参考图中的人物形象，保持面部和发型不变。{change_desc}。{base_prompt}"

    _assert_size_safe(SIZE)

    ref_images = []
    if ref_image and os.path.exists(ref_image):
        ref_images.append(ref_image.replace("\\", "/"))
        print(f"  参考图（上一版本）: {os.path.basename(ref_image)}")
    else:
        print(f"  参考图: 无（纯文生图）")

    task = {
        "id": f"char-{char_name}-v{version}",
        "prompt": new_prompt,
        "size": SIZE,
        "ref_images": ref_images,
        "output_path": output_path.replace("\\", "/"),
    }
    return task, new_prompt


def main():
    parser = argparse.ArgumentParser(description="增量生成角色定妆图任务（角色外观变化时使用）")
    parser.add_argument("--char-name", required=True, help="角色名")
    parser.add_argument("--version", type=int, required=True, help="新版本号")
    parser.add_argument("--base-prompt", required=True, help="上一版本的冻结提示词")
    parser.add_argument("--change-desc", required=True, help="外观变化描述（如：觉醒后瞳色变金）")
    parser.add_argument("--output", required=True, help="输出路径")
    parser.add_argument("--ref-image", default=None, help="上一版本定妆图路径（图生图参考）")
    parser.add_argument("--task-output", default=None, help="任务 JSON 输出路径（可选，默认打印到 stdout）")
    args = parser.parse_args()

    print(f"{'='*60}")
    print(f"增量定妆图任务: {args.char_name} v{args.version}")
    print(f"{'='*60}")

    task, new_prompt = build_task(
        args.char_name,
        args.version,
        args.base_prompt,
        args.change_desc,
        args.output,
        args.ref_image,
    )

    if args.task_output:
        with open(args.task_output, "w", encoding="utf-8") as f:
            json.dump({"tasks": [task]}, f, ensure_ascii=False, indent=2)
        print(f"任务已导出: {args.task_output}")
    else:
        print(json.dumps({"tasks": [task]}, ensure_ascii=False, indent=2))

    print("\n主 agent 请调用 image_generate 工具生成：")
    print(f"  image_generate(prompt=<任务prompt>, size={SIZE}, output={task['output_path']})")
    print("  图生图（有 ref_images 时）：按 image_generate 工具能力传入参考图，保持面部和发型不变。")
    print(f"\n  ⚠️  请将以下新提示词冻结到漫画角色库.md:")
    print(f"  ---")
    print(f"  {new_prompt}")
    print(f"  ---")


if __name__ == "__main__":
    main()