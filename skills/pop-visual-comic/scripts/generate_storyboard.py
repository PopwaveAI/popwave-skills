#!/usr/bin/env python3
"""
pop-visual-comic 分镜任务清单导出脚本 v4.0.0
================================================
生图改为由主 agent 调用 `image_generate` 工具完成，本脚本不再直调任何 HTTP API、不再内置 API Key。

职责：
  1. 从下方 FRAMES 列表读取每帧的 id + prompt + 可选 size
  2. 校验尺寸安全
  3. 解析每帧的角色定妆图参考路径（FRAME_REFS）
  4. 导出 `generation_tasks.json`（每帧一条任务：id/prompt/size/ref_images/output_path）
  5. 打印"请用 image_generate 工具逐张生成"的指引

主 agent 用法：
  1. 修改下方 FRAMES 列表（每帧的 id + prompt）
  2. 修改 FRAME_REFS 映射每帧的角色定妆图路径（None=无角色帧）
  3. 修改 OUTPUT_DIR 为输出目录
  4. 运行: python generate_storyboard.py
  5. 读取 generation_tasks.json，对每条任务调用 image_generate 工具生成

依赖:
  pip install Pillow
"""

import json
import os
import sys

# ============ 配置区（使用前修改） ============

SIZE = "1125x1500"           # 分镜帧（总像素 169 万 ≤ 236 万上限）
MAX_PIXELS = 2360000         # 超 236 万像素计费翻倍，所有出图必须 ≤ 上限

# 输出目录（章节级）
OUTPUT_DIR = r"第1章/output"

# 定妆图根目录（项目级，跨章复用）
CHAR_ASSETS_DIR = r"assets/characters"

# 风格锚定串（全系列冻结，从漫画快照.md复制）
STYLE = "暗黑奇幻半写实日式漫画风格，水彩质感笔触，灰暗色调，暖色火光点缀，情绪氛围浓郁"

# 分镜帧列表
FRAMES = [
    {
        "id": "frame1",
        "prompt": f"参考图中的人物形象。一个瘦弱女孩侧面蹲在破旧灶台前，用木棍搅动陶碗里的稀粥，灶膛火光映亮她的脸。破烂的屋顶漏雨，屋内弥漫浓烟和蒸汽。阴暗破败的贫民区小屋，墙角堆着湿柴。{STYLE}，压抑氛围。"
    },
    {
        "id": "frame2",
        "prompt": f"参考图中的人物形象。瘦弱女孩在阴暗街道被一个高大摊主攥住手腕，女孩表情惊恐，周围围观人群嘲笑。泥泞的地面，破旧摊位。{STYLE}，压抑屈辱氛围。"
    },
    # ... 更多帧请自行添加
]

# 按帧映射角色定妆图（None=无角色帧，直接文生图）
FRAME_REFS = {
    "frame1": "char-vivian-v1.png",
    "frame2": "char-vivian-v1.png",
    # "frame3": "char-soren-v1.png",
    # "frame4": None,  # 无角色帧
}

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


def resolve_ref_image(frame_id):
    """根据帧ID查找对应的角色定妆图路径"""
    ref_name = FRAME_REFS.get(frame_id)
    if not ref_name:
        return None
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), "assets", "characters", ref_name),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path.replace("\\", "/")
    print(f"  [警告] 定妆图未找到: {ref_name}，该帧将使用文生图", file=sys.stderr)
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
    """把 FRAMES 列表导出为 generation_tasks.json，供主 agent 用 image_generate 工具逐张生成。"""
    out_dir = OUTPUT_DIR
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", out_dir)
    os.makedirs(out_dir, exist_ok=True)

    tasks = []
    print("\n定妆图映射检查:")
    for frame in FRAMES:
        prompt = frame["prompt"]
        if len(prompt) > 2200:
            print(f"  [警告] {frame['id']} 提示词过长: {len(prompt)} 字符")

        size = frame.get("size", SIZE)
        _assert_size_safe(size)

        ref_path = resolve_ref_image(frame["id"])
        refs = [ref_path] if ref_path else []

        output_path = os.path.join(out_dir, f"{frame['id']}.png").replace("\\", "/")
        tasks.append({
            "id": frame["id"],
            "prompt": prompt,
            "size": size,
            "ref_images": refs,
            "output_path": output_path,
        })

        status = os.path.basename(ref_path) if ref_path else "无（文生图）"
        print(f"  {frame['id']}: {status}  size={size}")

    meta = {
        "total_frames": len(FRAMES),
        "generator": "generate_storyboard.py v4.0.0",
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
    print("  生成完成后用 ensure_png_format 校验格式，必要时手动转码。")
    return meta_path


if __name__ == "__main__":
    export_tasks()