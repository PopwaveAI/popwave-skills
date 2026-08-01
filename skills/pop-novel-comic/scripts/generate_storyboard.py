#!/usr/bin/env python3
"""
pop-novel-comic 批量分镜生成脚本 v3.0
- ThreadPoolExecutor 高并发生成（默认8线程，Seedream API限制500图/分钟）
- 自动重试（3次，指数退避）
- 格式保真（JPEG magic bytes检测→PNG转码）
- 按帧映射角色定妆图（多角色参考图）
- 生成元数据JSON

用法:
  1. 修改下方 FRAMES 列表（每帧的 id + prompt + 可选 size）
  2. 修改 FRAME_REFS 映射每帧的角色定妆图路径（None=无角色帧）
  3. 修改 OUTPUT_DIR 为输出目录
  4. 运行: python generate_storyboard.py

环境变量:
  ARK_API_KEY - 火山引擎方舟 API Key

依赖:
  pip install requests Pillow
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

# ============ 执行区（无需修改） ============


def image_to_data_uri(path):
    """读取图片文件转为 data URI"""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    # 检测实际格式
    f.seek(0)
    header = f.read(8)
    if header[:3] == b'\xff\xd8\xff':
        return f"data:image/jpeg;base64,{b64}"
    return f"data:image/png;base64,{b64}"


def ensure_png_format(path):
    """检测文件实际格式，若以 .png 保存但实际是 JPEG 则转码为真 PNG。"""
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


def resolve_ref_image(frame_id):
    """根据帧ID查找对应的角色定妆图路径"""
    ref_name = FRAME_REFS.get(frame_id)
    if not ref_name:
        return None
    # 尝试多个路径
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), CHAR_ASSETS_DIR, ref_name),
        os.path.join(os.getcwd(), "assets", "characters", ref_name),
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    print(f"  [警告] 定妆图未找到: {ref_name}，该帧将使用文生图", file=sys.stderr)
    return None


def generate_frame(frame, output_path):
    """生成单帧分镜，自动选择参考图。使用 b64_json 直接返回图片数据。
    支持自动重试和格式保真。"""
    prompt_len = len(frame["prompt"])
    if prompt_len > 2200:
        print(f"  [警告] {frame['id']} 提示词过长: {prompt_len} 字符")

    payload = {
        "model": MODEL,
        "prompt": frame["prompt"],
        "size": frame.get("size", SIZE),
        "watermark": False,
        "response_format": "b64_json",
    }

    # 按帧映射角色参考图
    ref_path = resolve_ref_image(frame["id"])
    if ref_path:
        payload["image"] = image_to_data_uri(ref_path)

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
                print(f"  [错误] {frame['id']} 尝试{attempt+1}: 未返回图片数据", file=sys.stderr)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(3 * (attempt + 1))
                continue

            item = data_list[0]
            if "error" in item:
                print(f"  [错误] {frame['id']} 尝试{attempt+1}: {item['error']}", file=sys.stderr)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(3 * (attempt + 1))
                continue

            b64_data = item.get("b64_json")
            if not b64_data:
                print(f"  [错误] {frame['id']} 尝试{attempt+1}: 未返回b64_json", file=sys.stderr)
                if attempt < MAX_RETRIES - 1:
                    time.sleep(3 * (attempt + 1))
                continue

            # 解码base64 + 格式保真
            img_bytes = base64.b64decode(b64_data)
            img_bytes = ensure_png_bytes(img_bytes)

            with open(output_path, "wb") as f:
                f.write(img_bytes)

            file_size = len(img_bytes) / 1024
            ref_info = f" ref={os.path.basename(ref_path)}" if ref_path else " 文生图"
            print(f"  [OK] {frame['id']} ({file_size:.0f}KB{ref_info}, prompt={prompt_len}字符)")
            return {"id": frame["id"], "success": True, "path": output_path}

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            print(f"  [错误] {frame['id']} 尝试{attempt+1}: HTTP {e.code} - {error_body[:100]}", file=sys.stderr)
            if attempt < MAX_RETRIES - 1:
                time.sleep(3 * (attempt + 1))
        except Exception as e:
            print(f"  [错误] {frame['id']} 尝试{attempt+1}: {str(e)[:100]}", file=sys.stderr)
            if attempt < MAX_RETRIES - 1:
                time.sleep(3 * (attempt + 1))

    print(f"  [失败] {frame['id']} 所有{MAX_RETRIES}次尝试均失败", file=sys.stderr)
    return {"id": frame["id"], "success": False, "path": output_path}


def main():
    print("=" * 60)
    print(f"pop-novel-comic 批量分镜生成 v3.0 (并发={CONCURRENCY})")
    print("=" * 60)

    # 确定输出目录
    out_dir = OUTPUT_DIR
    if not os.path.isabs(out_dir):
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", out_dir)
    os.makedirs(out_dir, exist_ok=True)

    # 检查定妆图可用性
    print("\n定妆图映射检查:")
    for frame in FRAMES:
        ref_path = resolve_ref_image(frame["id"])
        status = os.path.basename(ref_path) if ref_path else "无（文生图）"
        print(f"  {frame['id']}: {status}")

    print(f"\n开始生成 {len(FRAMES)} 帧（并发数={CONCURRENCY}）...\n")

    start_time = time.time()

    # 高并发生成
    results = []
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        futures = {}
        for i, frame in enumerate(FRAMES):
            output_path = os.path.join(out_dir, f"{frame['id']}.png")
            future = executor.submit(generate_frame, frame, output_path)
            futures[future] = frame

        for future in as_completed(futures):
            frame = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"  [崩溃] {frame['id']}: {e}", file=sys.stderr)
                results.append({"id": frame["id"], "success": False, "path": None})

    elapsed = time.time() - start_time

    # 按帧号排序结果
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

    print(f"\n成功: {success_count}/{len(FRAMES)}")
    print(f"耗时: {elapsed:.1f}秒 (平均 {elapsed/max(len(FRAMES),1):.1f}秒/帧)")
    print(f"并发效率: 理论串行 ~{elapsed*CONCURRENCY:.0f}秒 -> 实际 {elapsed:.0f}秒")

    # 保存元数据
    meta = {
        "total_frames": len(FRAMES),
        "success": success_count,
        "failed": len(FRAMES) - success_count,
        "elapsed_seconds": round(elapsed, 1),
        "concurrency": CONCURRENCY,
        "model": MODEL,
        "frames": results,
    }
    meta_path = os.path.join(out_dir, "generation_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print(f"\n元数据已保存: {meta_path}")


if __name__ == "__main__":
    main()
