#!/usr/bin/env python3
"""
pop-visual-shared 生图任务清单导出脚本（视觉 skill 群共享）v2.0.0
=================================================================
生图改为由主 agent 调用 `image_generate` 工具完成，本脚本不再直调 Seedream HTTP API、
不再内置任何 API Key。

职责（image 子命令）：
  读取 --prompt/--size/--output/--image(参考图) 等参数，校验尺寸安全，
  导出单条生图任务（stdout 或 --task-output 文件），供主 agent 用 image_generate 工具生成。

用法（image / 图片生成）:
  导出任务（默认打印到 stdout）:
    python generate.py image --prompt "提示词" --size 1125x1500 --output "封面.png"
  导出到文件（供主 agent 读取）:
    python generate.py image --prompt "提示词" --size 1125x1500 --output "封面.png" --task-output "tasks.json"
  参考图（图生图）:
    python generate.py image --prompt "提示词" --size 1125x1500 --image "素材/参考.png" --output "封面.png"

视频生成（Seedance）说明：
  视频无对应的 image_generate 工具，仍走外部 API。本脚本不再内置 key，
  需显式设置环境变量 ARK_API_KEY 方可使用（不设置则拒绝执行）。
"""

import argparse
import json
import os
import sys

# 输出图像像素上限（Seedream 5.0 Pro 计费临界）
MAX_PIXELS = 2360000


def assert_size_safe(size):
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
            f"（Seedream 5.0 Pro 超 236 万像素报价翻倍），已中止。"
            f"请改用安全尺寸，如 1125x1500 / 1500x1500 / 1500x1125。",
            file=sys.stderr,
        )
        sys.exit(1)


def ensure_format_integrity(output_path):
    """检测文件实际格式，若与扩展名不符则用 Pillow 转码保真。"""
    if not os.path.exists(output_path):
        return
    ext = os.path.splitext(output_path)[1].lower()
    try:
        with open(output_path, "rb") as f:
            header = f.read(8)
    except Exception:
        return
    is_jpeg = header[:3] == b'\xff\xd8\xff'
    is_png = header[:8] == b'\x89PNG\r\n\x1a\n'
    if ext == ".png" and is_jpeg:
        try:
            from PIL import Image
        except ImportError:
            print(f"  [警告] 文件为JPEG内容但Pillow未安装，无法转码: {output_path}", file=sys.stderr)
            return
        img = Image.open(output_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        tmp = output_path + ".tmp"
        img.save(tmp, "PNG", optimize=True)
        os.replace(tmp, output_path)
        print(f"  [格式修正] JPEG → PNG 转码: {os.path.basename(output_path)}")
    elif ext in (".jpg", ".jpeg") and is_png:
        try:
            from PIL import Image
        except ImportError:
            return
        img = Image.open(output_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        tmp = output_path + ".tmp"
        img.save(tmp, "JPEG", quality=95)
        os.replace(tmp, output_path)
        print(f"  [格式修正] PNG → JPEG 转码: {os.path.basename(output_path)}")


def export_image_task(args):
    """导出单条生图任务。不发起任何 API 调用。"""
    if args.size:
        assert_size_safe(args.size)

    ref_images = []
    if args.image:
        # 支持多图（--image 可多次传入）
        if isinstance(args.image, list):
            ref_images = [os.path.abspath(p).replace("\\", "/") for p in args.image]
        else:
            ref_images = [os.path.abspath(args.image).replace("\\", "/")]

    task = {
        "id": args.task_id or os.path.splitext(os.path.basename(args.output))[0],
        "prompt": args.prompt,
        "size": args.size or "1125x1500",
        "ref_images": ref_images,
        "output_path": os.path.abspath(args.output).replace("\\", "/"),
    }

    print("=" * 60)
    print("生图任务（请用 image_generate 工具生成）")
    print("=" * 60)
    if args.task_output:
        os.makedirs(os.path.dirname(os.path.abspath(args.task_output)) or ".", exist_ok=True)
        with open(args.task_output, "w", encoding="utf-8") as f:
            json.dump({"tasks": [task]}, f, ensure_ascii=False, indent=2)
        print(f"任务已导出: {os.path.abspath(args.task_output)}")
    else:
        print(json.dumps({"tasks": [task]}, ensure_ascii=False, indent=2))

    print("\n主 agent 请调用 image_generate 工具生成：")
    print(f"  image_generate(prompt=<任务prompt>, size={task['size']}, output={task['output_path']})")
    if ref_images:
        print("  图生图：按 image_generate 工具能力传入参考图路径，保证风格/角色一致。")
    print("  生成后用 ensure_format_integrity 校验格式（扩展名与实际字节一致）。")


def generate_video(args):
    """视频生成（Seedance）。无对应 image_generate 工具，仍需外部 API。
    本脚本不再内置 key，必须显式设置环境变量 ARK_API_KEY，否则拒绝执行。"""
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print(
            "[错误] 视频生成需要外部 API Key。本脚本已移除内置 key，请显式设置环境变量 ARK_API_KEY。",
            file=sys.stderr,
        )
        sys.exit(1)

    import time
    import urllib.request
    import urllib.error

    SEEDANCE_TASK_API = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
    SEEDANCE_QUERY_API = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"

    content = [{"type": "text", "text": args.prompt}]
    if args.image:
        content.append({
            "type": "image_url",
            "image_url": {"url": args.image},
            "role": "first_frame",
        })

    payload = {
        "model": args.model,
        "content": content,
        "ratio": args.ratio,
        "duration": args.duration,
        "resolution": args.resolution,
        "camera_fixed": args.camera_fixed,
        "watermark": args.watermark,
    }

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    def make_request(url, data=None, method="POST"):
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else ""
            print(f"HTTP 错误 {e.code}: {error_body}", file=sys.stderr)
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"网络错误: {e.reason}", file=sys.stderr)
            sys.exit(1)

    print(f"正在创建视频生成任务... (模型: {args.model})")
    result = make_request(SEEDANCE_TASK_API, json.dumps(payload).encode("utf-8"))
    if "error" in result:
        print(f"API 错误: {result['error'].get('message', '未知错误')}", file=sys.stderr)
        sys.exit(1)
    task_id = result.get("id")
    if not task_id:
        print("错误：API 未返回任务 ID", file=sys.stderr)
        sys.exit(1)

    print(f"任务已创建，ID: {task_id}，正在等待生成完成...")
    max_wait = args.max_wait
    poll_interval = 10
    elapsed = 0
    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval
        query_result = make_request(SEEDANCE_QUERY_API.format(task_id=task_id), None, method="GET")
        status = query_result.get("status", "unknown")
        print(f"  [{elapsed}s] 状态: {status}")
        if status == "succeeded":
            content_list = query_result.get("content", [])
            if not content_list:
                print("错误：任务成功但未返回视频", file=sys.stderr)
                sys.exit(1)
            video_url = content_list[0].get("video_url", {}).get("url")
            if not video_url:
                print("错误：未找到视频 URL", file=sys.stderr)
                sys.exit(1)
            out_dir = os.path.dirname(args.output)
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
            with urllib.request.urlopen(video_url, timeout=300) as resp:
                with open(args.output, "wb") as f:
                    f.write(resp.read())
            print(f"视频生成完成: {args.output}")
            return
        elif status == "failed":
            print(f"任务失败: {query_result.get('error', {}).get('message', '未知错误')}", file=sys.stderr)
            sys.exit(1)
        elif status == "expired":
            print("任务超时", file=sys.stderr)
            sys.exit(1)
    print(f"等待超时（{max_wait}秒），请稍后手动查询任务状态: {task_id}", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="pop-visual-shared 生图任务清单导出脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="生成模式")

    # 图片生成子命令（任务导出，不调 API）
    img_parser = subparsers.add_parser("image", help="Seedream 生图任务导出")
    img_parser.add_argument("--prompt", required=True, help="提示词（中文≤300字）")
    img_parser.add_argument("--model", default="doubao-seedream-5-0-pro-260628", help="模型 ID（提示用，image_generate 工具自行决定模型）")
    img_parser.add_argument("--size", default=None, help="图片尺寸（如 1125x1500，总像素须 ≤236万）")
    img_parser.add_argument("--output", required=True, help="输出文件路径")
    img_parser.add_argument("--image", action="append", default=None, help="参考图路径（可多次传入，图生图）")
    img_parser.add_argument("--task-id", default=None, help="任务 ID（默认取输出文件名）")
    img_parser.add_argument("--task-output", default=None, help="任务 JSON 输出路径（可选，默认打印到 stdout）")
    img_parser.set_defaults(func=export_image_task)

    # 视频生成子命令（无对应 image_generate 工具，需外部 key）
    vid_parser = subparsers.add_parser("video", help="Seedance 视频生成（需显式设置 ARK_API_KEY）")
    vid_parser.add_argument("--prompt", required=True, help="提示词（中文≤500字）")
    vid_parser.add_argument("--model", default="doubao-seedance-1-0-pro-250428", help="模型 ID")
    vid_parser.add_argument("--ratio", default="16:9", help="视频比例")
    vid_parser.add_argument("--duration", type=int, default=5, help="视频时长（秒）")
    vid_parser.add_argument("--resolution", default="1080p", help="分辨率")
    vid_parser.add_argument("--camera-fixed", action="store_true", default=False, help="固定镜头")
    vid_parser.add_argument("--watermark", action="store_true", default=False, help="添加水印")
    vid_parser.add_argument("--output", required=True, help="输出文件路径")
    vid_parser.add_argument("--image", default=None, help="首帧图片路径")
    vid_parser.add_argument("--max-wait", type=int, default=600, help="最大等待时间（秒）")
    vid_parser.set_defaults(func=generate_video)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()