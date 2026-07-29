#!/usr/bin/env python3
"""
pop-novel-comic 批量分镜生成脚本
读取角色定妆图作为参考，逐格生成多帧分镜画面

用法:
  1. 修改下方 FRAMES 列表（每帧的 id + prompt）
  2. 修改 CHAR_IMG 为角色定妆图路径
  3. 修改 OUTPUT_DIR 为输出目录
  4. 运行: python generate_storyboard.py

环境变量:
  ARK_API_KEY - 火山引擎方舟 API Key
"""

import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error

# ============ 配置区（使用前修改） ============

API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
API_KEY = os.environ.get("ARK_API_KEY", "b597f4e5-2370-4bdf-875f-5ae43e43c52b")
MODEL = "doubao-seedream-5-0-lite-260128"
SIZE = "1728x2304"

# 角色定妆图路径
CHAR_IMG = r"output/char-vivian.png"

# 输出目录
OUTPUT_DIR = r"output"

# 风格锚定串（全章统一，追加在每格提示词末尾）
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

# ============ 执行区（无需修改） ============


def image_to_data_uri(path):
    """读取图片文件转为 data URI"""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b64}"


def ensure_png_format(path):
    """检测文件实际格式，若以 .png 保存但实际是 JPEG 则转码为真 PNG。

    Seedream API 返回的 URL 资源实际为 JPEG，直接保存为 .png 会导致
    扩展名与内容不符。浏览器做 MIME sniffing 能兼容，但严格 webview
    会判定为图片损坏。此函数自动检测并转码。
    """
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


def generate_frame(frame, ref_image_uri, output_path):
    """生成单帧分镜"""
    payload = {
        "model": MODEL,
        "prompt": frame["prompt"],
        "size": SIZE,
        "watermark": False,
        "response_format": "url",
        "image": ref_image_uri,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")

    print(f"  正在生成 {frame['id']}...")
    print(f"  提示词: {frame['prompt'][:60]}...")

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"  HTTP 错误 {e.code}: {error_body}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  错误: {e}", file=sys.stderr)
        return False

    data_list = result.get("data", [])
    if not data_list:
        print(f"  错误：未返回图片数据", file=sys.stderr)
        return False

    item = data_list[0]
    if "error" in item:
        print(f"  生成失败: {item['error']}", file=sys.stderr)
        return False

    url = item.get("url")
    if not url:
        print(f"  错误：未返回URL", file=sys.stderr)
        return False

    # 下载图片
    req2 = urllib.request.Request(url)
    with urllib.request.urlopen(req2, timeout=300) as resp:
        with open(output_path, "wb") as f:
            f.write(resp.read())

    ensure_png_format(output_path)
    print(f"  已保存: {output_path}")
    return True


def main():
    print("=" * 60)
    print("pop-novel-comic 批量分镜生成")
    print("=" * 60)

    # 读取角色参考图
    char_path = CHAR_IMG
    if not os.path.isabs(char_path):
        char_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", char_path)

    print(f"\n读取角色参考图: {char_path}")
    if not os.path.exists(char_path):
        print(f"  错误：角色定妆图不存在: {char_path}", file=sys.stderr)
        sys.exit(1)

    ref_uri = image_to_data_uri(char_path)
    print(f"  data URI 长度: {len(ref_uri)} 字符")

    # 确定输出目录
    out_dir = OUTPUT_DIR
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", out_dir)
    os.makedirs(out_dir, exist_ok=True)

    # 逐帧生成
    results = []
    for i, frame in enumerate(FRAMES):
        print(f"\n[{i+1}/{len(FRAMES)}] {frame['id']}")
        output_path = os.path.join(out_dir, f"{frame['id']}.png")

        success = generate_frame(frame, ref_uri, output_path)
        results.append({"id": frame["id"], "success": success, "path": output_path})

        if success and i < len(FRAMES) - 1:
            print("  等待 2 秒...")
            time.sleep(2)

    # 汇总
    print("\n" + "=" * 60)
    print("生成汇总:")
    success_count = 0
    for r in results:
        status = "✅" if r["success"] else "❌"
        print(f"  {status} {r['id']} → {r['path']}")
        if r["success"]:
            success_count += 1
    print(f"\n成功: {success_count}/{len(FRAMES)}")


if __name__ == "__main__":
    main()
