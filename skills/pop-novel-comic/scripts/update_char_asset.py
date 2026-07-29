#!/usr/bin/env python3
"""
pop-novel-comic 增量角色定妆图生成脚本
当角色外观变化时，基于冻结提示词+变化描述生成新版本定妆图

用法:
  python update_char_asset.py \
    --char-name "索伦" \
    --version 2 \
    --base-prompt "一个18岁的瘦削男性角色..." \
    --change-desc "觉醒后瞳色变金，左手机械化" \
    --output "assets/characters/char-soren-v2.png"

生成后需手动将新提示词冻结到漫画角色库.md（作为 v2 的冻结提示词）
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
API_KEY = os.environ.get("ARK_API_KEY", "b597f4e5-2370-4bdf-875f-5ae43e43c52b")
MODEL = "doubao-seedream-5-0-lite-260128"
SIZE = "1728x2304"


def image_to_data_uri(path):
    """读取图片文件转为 data URI"""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    f = open(path, "rb")
    header = f.read(8)
    f.close()
    if header[:3] == b'\xff\xd8\xff':
        return f"data:image/jpeg;base64,{b64}"
    return f"data:image/png;base64,{b64}"


def ensure_png_format(path):
    """检测文件实际格式，若以 .png 保存但实际是 JPEG 则转码为真 PNG。"""
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


def generate_incremental_asset(char_name, version, base_prompt, change_desc, output_path, ref_image=None):
    """基于冻结提示词+变化描述生成新版本定妆图"""

    # 组装新提示词：冻结提示词 + 变化描述
    new_prompt = f"参考图中的人物形象，保持面部和发型不变。{change_desc}。{base_prompt}"

    payload = {
        "model": MODEL,
        "prompt": new_prompt,
        "size": SIZE,
        "watermark": False,
        "response_format": "url",
    }

    # 传入上一版本定妆图作为参考
    if ref_image and os.path.exists(ref_image):
        payload["image"] = image_to_data_uri(ref_image)
        print(f"  参考图（上一版本）: {os.path.basename(ref_image)}")
    else:
        print(f"  参考图: 无（纯文生图）")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")

    print(f"  正在生成 {char_name} v{version} 定妆图...")
    print(f"  变化描述: {change_desc}")
    print(f"  新提示词: {new_prompt[:80]}...")

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"  HTTP 错误 {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"  错误: {e}", file=sys.stderr)
        sys.exit(1)

    data_list = result.get("data", [])
    if not data_list:
        print(f"  错误：未返回图片数据", file=sys.stderr)
        sys.exit(1)

    item = data_list[0]
    if "error" in item:
        print(f"  生成失败: {item['error']}", file=sys.stderr)
        sys.exit(1)

    url = item.get("url")
    if not url:
        print(f"  错误：未返回URL", file=sys.stderr)
        sys.exit(1)

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 下载图片
    req2 = urllib.request.Request(url)
    with urllib.request.urlopen(req2, timeout=300) as resp:
        with open(output_path, "wb") as f:
            f.write(resp.read())

    ensure_png_format(output_path)
    print(f"\n  已保存: {output_path}")
    print(f"  ⚠️  请将以下新提示词冻结到漫画角色库.md:")
    print(f"  ---")
    print(f"  {new_prompt}")
    print(f"  ---")
    return new_prompt


def main():
    parser = argparse.ArgumentParser(description="增量生成角色定妆图（角色外观变化时使用）")
    parser.add_argument("--char-name", required=True, help="角色名")
    parser.add_argument("--version", type=int, required=True, help="新版本号")
    parser.add_argument("--base-prompt", required=True, help="上一版本的冻结提示词")
    parser.add_argument("--change-desc", required=True, help="外观变化描述（如：觉醒后瞳色变金）")
    parser.add_argument("--output", required=True, help="输出路径")
    parser.add_argument("--ref-image", default=None, help="上一版本定妆图路径（图生图参考）")
    args = parser.parse_args()

    print(f"{'='*60}")
    print(f"增量定妆图生成: {args.char_name} v{args.version}")
    print(f"{'='*60}")

    new_prompt = generate_incremental_asset(
        args.char_name,
        args.version,
        args.base_prompt,
        args.change_desc,
        args.output,
        args.ref_image,
    )


if __name__ == "__main__":
    main()
