#!/usr/bin/env python3
"""
pop-novel-comic 逐页漫画生成脚本 v4.5.0
- ThreadPoolExecutor 8线程高并发生成（Seedream API限制500图/分钟，8线程安全）
- 支持角色定妆图参考（图生图模式，保证角色一致性）
- 格式保真（JPEG magic bytes检测→PNG转码）
- 自动重试（3次，指数退避 3s/6s/9s）
- 生成元数据JSON

用法:
  1. 修改下方 PAGES 列表（每页的 id + prompt + ref_images + 可选 size）
  2. 修改 OUTPUT_DIR 为输出目录
  3. 修改 CHAR_ASSETS_DIR 为定妆图根目录
  4. 运行: python generate_comic_page.py

环境变量:
  ARK_API_KEY - 火山引擎方舟 API Key

依赖:
  pip install Pillow
"""

import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO

# ============ 配置区（使用前修改） ============

API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
API_KEY = os.environ.get("ARK_API_KEY", "b597f4e5-2370-4bdf-875f-5ae43e43c52b")
MODEL = "doubao-seedream-5-0-pro-260628"
SIZE = "1728x2304"

# 并发线程数（Seedream API限制500图/分钟=8.3图/秒，8线程安全）
CONCURRENCY = 8

# 最大重试次数
MAX_RETRIES = 3

# 输出目录
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
                  "Dark fantasy semi-realistic manga style, watercolor texture, muted tones with warm firelight accents.",
        "ref_images": ["char-苏午-v1.png"],  # 角色定妆图参考（可多张）
        "size": "1728x2304",  # 可选，默认用 SIZE
    },
    # ... 更多页请自行添加
]

# ============ 执行区（无需修改） ============


def image_to_data_uri(path):
    """读取图片文件转为 data URI"""
    with open(path, "rb") as f:
        raw = f.read()
    b64 = base64.b64encode(raw).decode()
    # 检测实际格式
    if raw[:3] == b'\xff\xd8\xff':
        return f"data:image/jpeg;base64,{b64}"
    return f"data:image/png;base64,{b64}"


def ensure_png_bytes(img_bytes):
    """检测字节流的实际格式，若为JPEG则转码为PNG字节流。返回PNG字节流。"""
    if img_bytes[:2] == b'\xff\xd8':  # JPEG magic bytes
        try:
            from PIL import Image
        except ImportError:
            return img_bytes  # 无法转码，返回原始字节
        img = Image.open(BytesIO(img_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        buf = BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()
    return img_bytes


def resolve_ref_image(ref_name):
    """根据定妆图文件名查找完整路径"""
    # 尝试多个路径
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), "assets", "characters", ref_name),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    print(f"  [警告] 定妆图未找到: {ref_name}", file=sys.stderr)
    return None


def generate_page(page, output_path):
    """生成单页漫画，支持多张参考图（image参数传第一张定妆图）。
    使用 b64_json 直接返回图片数据。支持自动重试和格式保真。"""
    prompt_len = len(page["prompt"])
    if prompt_len > 2200:
        print(f"  [警告] {page['id']} 提示词过长: {prompt_len} 字符")

    payload = {
        "model": MODEL,
        "prompt": page["prompt"],
        "size": page.get("size", SIZE),
        "watermark": False,
        "response_format": "b64_json",
    }

    # 解析参考图列表，image参数传第一张定妆图（Seedream API目前只支持单张image参数）
    ref_images = page.get("ref_images", [])
    resolved_refs = []
    for ref_name in ref_images:
        ref_path = resolve_ref_image(ref_name)
        if ref_path:
            resolved_refs.append(ref_path)

    if resolved_refs:
        payload["image"] = image_to_data_uri(resolved_refs[0])

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = json.dumps(payload).encode("utf-8")

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))

            data_list = result.get("data", [])
            if not data_list:
                print(f"  [错误] {page['id']} 尝试{attempt+1}: 未返回图片数据", file=sys.stderr)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(3 * (attempt + 1))
                continue

            item = data_list[0]
            if "error" in item:
                print(f"  [错误] {page['id']} 尝试{attempt+1}: {item['error']}", file=sys.stderr)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(3 * (attempt + 1))
                continue

            b64_data = item.get("b64_json")
            if not b64_data:
                print(f"  [错误] {page['id']} 尝试{attempt+1}: 未返回b64_json", file=sys.stderr)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(3 * (attempt + 1))
                continue

            # 解码base64 + 格式保真
            img_bytes = base64.b64decode(b64_data)
            img_bytes = ensure_png_bytes(img_bytes)

            with open(output_path, "wb") as f:
                f.write(img_bytes)

            file_size = len(img_bytes) / 1024
            ref_info = f" refs={','.join(os.path.basename(r) for r in resolved_refs)}" if resolved_refs else " 文生图"
            print(f"  [OK] {page['id']} ({file_size:.0f}KB{ref_info}, prompt={prompt_len}字符)")
            return {
                "id": page["id"],
                "success": True,
                "path": output_path,
                "refs": [os.path.basename(r) for r in resolved_refs],
                "size": page.get("size", SIZE),
            }

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            print(f"  [错误] {page['id']} 尝试{attempt+1}: HTTP {e.code} - {error_body[:100]}", file=sys.stderr)
            if attempt < MAX_RETRIES - 1:
                time.sleep(3 * (attempt + 1))
        except Exception as e:
            print(f"  [错误] {page['id']} 尝试{attempt+1}: {str(e)[:100]}", file=sys.stderr)
            if attempt < MAX_RETRIES - 1:
                time.sleep(3 * (attempt + 1))

    print(f"  [失败] {page['id']} 所有{MAX_RETRIES}次尝试均失败", file=sys.stderr)
    return {
        "id": page["id"],
        "success": False,
        "path": output_path,
        "refs": [os.path.basename(r) for r in resolved_refs],
        "size": page.get("size", SIZE),
    }


def main():
    print("=" * 60)
    print(f"pop-novel-comic 逐页漫画生成 v4.5.0 (8并发模式)")
    print("=" * 60)

    # 确定输出目录
    out_dir = OUTPUT_DIR
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", out_dir)
    os.makedirs(out_dir, exist_ok=True)

    # 检查定妆图可用性
    print("\n定妆图映射检查:")
    for page in PAGES:
        ref_images = page.get("ref_images", [])
        if ref_images:
            ref_paths = []
            for ref_name in ref_images:
                ref_path = resolve_ref_image(ref_name)
                ref_paths.append(os.path.basename(ref_path) if ref_path else f"{ref_name}(缺失)")
            print(f"  {page['id']}: {', '.join(ref_paths)}")
        else:
            print(f"  {page['id']}: 无（文生图）")

    print(f"\n开始生成 {len(PAGES)} 页（并发数={CONCURRENCY}）...\n")

    start_time = time.time()

    # 高并发逐页生成
    results = []
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = {}
        for page in PAGES:
            output_path = os.path.join(out_dir, f"{page['id']}.png")
            future = executor.submit(generate_page, page, output_path)
            futures[future] = page

        for future in as_completed(futures):
            page = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"  [崩溃] {page['id']}: {e}", file=sys.stderr)
                results.append({"id": page["id"], "success": False, "path": None})

    elapsed = time.time() - start_time

    # 按页号排序结果
    results.sort(key=lambda r: r["id"])

    # 汇总
    print("\n" + "=" * 60)
    print("生成汇总:")
    success_count = 0
    for r in results:
        status = "OK" if r["success"] else "FAIL"
        print(f"  [{status}] {r['id']} -> {r.get('path', 'N/A')}")
        if r["success"]:
            success_count += 1

    print(f"\n成功: {success_count}/{len(PAGES)}")
    print(f"耗时: {elapsed:.1f}秒 (平均 {elapsed/max(len(PAGES),1):.1f}秒/页)")
    print(f"并发效率: 理论串行 ~{elapsed*CONCURRENCY:.0f}秒 -> 实际 {elapsed:.0f}秒")

    # 保存元数据
    meta = {
        "total_pages": len(PAGES),
        "success": success_count,
        "failed": len(PAGES) - success_count,
        "elapsed_seconds": round(elapsed, 1),
        "concurrency": CONCURRENCY,
        "model": MODEL,
        "pages": results,
    }
    meta_path = os.path.join(out_dir, "generation_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"\n元数据已保存: {meta_path}")


if __name__ == "__main__":
    main()
