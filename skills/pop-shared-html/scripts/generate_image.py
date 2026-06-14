#!/usr/bin/env python3
"""
pop-shared-html — Seedream 图像生成脚本

从 pop-shared-book-promo 剥离的核心生图能力。
纯生图模式，不包含任何 HTML 模板注入。

用法:
  # 生图
  python3 generate_image.py --prompt "..." --output assets/hero.png

  # 生图 + 同时打印 Data URL（供嵌入 HTML）
  python3 generate_image.py --prompt "..." --output assets/scene1.png --print-data-url

  # 生图 + 保存到 assets 目录
  python3 generate_image.py --prompt "..." --output assets/scene1.png --save-assets .
"""

import argparse, base64, json, os, re, sys, time, urllib.request, urllib.error
from pathlib import Path
from typing import Optional

# ── 常量 ──

# Seedream（火山引擎）内嵌 API Key — 免环境变量即可生图
# 🔑 此 Key 记录在 SKILL.md "凭据" 章节
SEEDREAM_API_KEY = "b597f4e5-2370-4bdf-875f-5ae43e43c52b"
SEEDREAM_MODEL = "doubao-seedream-5-0-260128"
SEEDREAM_API_BASE = "https://ark.cn-beijing.volces.com/api/v3"


# ═══════════════════════════════════════════
# 生图核心
# ═══════════════════════════════════════════

def generate_image(prompt: str, retries: int = 2) -> bytes:
    """调火山引擎 Seedream 图像生成 API，返回图片 bytes

    API Key 优先级：环境变量 ARK_API_KEY > MODEL_IMAGE_API_KEY > 内嵌 key
    如果全部不可用，返回 SVG 占位图
    """
    api_key = (os.getenv("ARK_API_KEY")
               or os.getenv("MODEL_IMAGE_API_KEY")
               or SEEDREAM_API_KEY)
    if not api_key:
        print("  ❌ 未设置 ARK_API_KEY 且无内嵌 Key", file=sys.stderr)
        return _placeholder_image("请设置 ARK_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = json.dumps({
        "model": SEEDREAM_MODEL,
        "prompt": prompt,
        "size": "2048x2048",
        "response_format": "b64_json",
        "watermark": False,
    }).encode()

    timeout = 120
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                f"{SEEDREAM_API_BASE}/images/generations",
                data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read())

            images = data.get("data", [])
            if images:
                b64 = images[0].get("b64_json")
                if b64:
                    return base64.b64decode(b64)
                url = images[0].get("url")
                if url:
                    with urllib.request.urlopen(url, timeout=90) as img_resp:
                        return img_resp.read()
            print(f"  ⚠️  Seedream 响应无图片数据", file=sys.stderr)
            if attempt < retries - 1:
                time.sleep(2)
            continue

        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:300]
            print(f"  ⚠️  Seedream HTTP {e.code}: {detail}", file=sys.stderr)
            if e.code in {401, 403}:
                print("  ❌ API Key 认证失败", file=sys.stderr)
                break
            time.sleep(2)
        except Exception as e:
            print(f"  ⚠️  Seedream 失败 (attempt {attempt+1}): {e}", file=sys.stderr)
            time.sleep(2)

    return _placeholder_image("Seedream 生成失败")


def _placeholder_image(msg: str = "图片生成失败") -> bytes:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="768">
      <rect width="1024" height="768" fill="#1a1a2e"/>
      <text x="512" y="384" text-anchor="middle" fill="#8b949e" font-size="24" font-family="sans-serif">{msg}</text>
      <text x="512" y="420" text-anchor="middle" fill="#484f58" font-size="14" font-family="sans-serif">请检查 API Key 或网络连接</text>
    </svg>'''
    return svg.encode()


def img_to_data_url(img_bytes: bytes) -> str:
    """将图片 bytes 转为 Data URL"""
    if img_bytes[:4] == b'<svg':
        b64 = base64.b64encode(img_bytes).decode()
        return f"data:image/svg+xml;base64,{b64}"
    if img_bytes[:3] == b'\xff\xd8\xff':
        fmt = "jpeg"
    elif img_bytes[:8] == b'\x89PNG\r\n\x1a\n':
        fmt = "png"
    elif img_bytes[:4] == b'RIFF':
        fmt = "webp"
    else:
        fmt = "png"
    b64 = base64.b64encode(img_bytes).decode()
    return f"data:image/{fmt};base64,{b64}"


def safe_filename(value: str, fallback: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|\s]+', "_", value.strip())
    cleaned = cleaned.strip("._")
    return cleaned or fallback


# ═══════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Seedream 图像生成")
    parser.add_argument("--prompt", "-p", required=True, help="生图提示词")
    parser.add_argument("--output", "-o", default="output.png", help="输出文件路径")
    parser.add_argument("--print-data-url", action="store_true", help="同时打印 Data URL")
    parser.add_argument("--save-assets", help="保存到 assets 目录（覆盖 output）")
    args = parser.parse_args()

    prompt = args.prompt
    output_path = Path(args.output)

    # 如果指定了 save-assets，把图片保存到 assets 目录
    if args.save_assets:
        assets_dir = Path(args.save_assets)
        assets_dir.mkdir(parents=True, exist_ok=True)
        output_path = assets_dir / f"{safe_filename(prompt[:30], 'image')}.png"

    print(f"  🎨 正在生成: {prompt[:60]}...")
    img_bytes = generate_image(prompt)

    # 写入文件
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(img_bytes)
    print(f"  ✅ 已保存: {output_path}")

    # 打印 Data URL
    if args.print_data_url:
        data_url = img_to_data_url(img_bytes)
        # 截断打印，完整版由调用方自行获取
        print(f"  📎 Data URL: data:image/png;base64,{data_url[30:70]}...({len(data_url)} chars)")


if __name__ == "__main__":
    main()
