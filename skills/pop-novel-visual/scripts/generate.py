#!/usr/bin/env python3
"""
pop-novel-visual API 调用脚本
支持 Seedream（图片生成）和 Seedance（视频生成）

用法:
  图片生成:
    python generate.py image --prompt "提示词" --model doubao-seedream-4-5-251128 --size 1728x2304 --output "封面.png"

  视频生成:
    python generate.py video --prompt "提示词" --model doubao-seedance-1-0-pro-250428 --ratio 3:4 --duration 5 --output "封面.mp4"

环境变量:
  ARK_API_KEY - 火山引擎方舟 API Key（已内置默认值，可通过环境变量覆盖）
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import base64

# API 端点
SEEDREAM_API = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
SEEDANCE_TASK_API = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
SEEDANCE_QUERY_API = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}"

# 内置 API Key（环境变量优先）
DEFAULT_ARK_API_KEY = "b597f4e5-2370-4bdf-875f-5ae43e43c52b"


def get_api_key():
    """获取 API Key，环境变量优先，回退到内置默认值"""
    api_key = os.environ.get("ARK_API_KEY") or DEFAULT_ARK_API_KEY
    return api_key


def make_request(url, payload, api_key, method="POST"):
    """发送 HTTP 请求"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = json.dumps(payload).encode("utf-8")
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


def download_file(url, output_path):
    """下载文件到本地"""
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=300) as response:
            with open(output_path, "wb") as f:
                f.write(response.read())
        print(f"文件已保存: {output_path}")
    except Exception as e:
        print(f"下载失败: {e}", file=sys.stderr)
        sys.exit(1)


def save_base64_image(b64_data, output_path):
    """将 Base64 编码的图片保存到本地"""
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    try:
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(b64_data))
        print(f"图片已保存: {output_path}")
    except Exception as e:
        print(f"保存失败: {e}", file=sys.stderr)
        sys.exit(1)


def generate_image(args):
    """调用 Seedream API 生成图片"""
    api_key = get_api_key()

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "watermark": args.watermark,
        "response_format": args.response_format,
    }

    if args.size:
        payload["size"] = args.size

    if args.image:
        payload["image"] = args.image

    if args.seed is not None:
        payload["seed"] = args.seed

    print(f"正在生成图片...")
    print(f"  模型: {args.model}")
    print(f"  尺寸: {args.size or '默认'}")
    print(f"  提示词: {args.prompt[:80]}...")

    result = make_request(SEEDREAM_API, payload, api_key)

    if "error" in result:
        print(f"API 错误: {result['error'].get('message', '未知错误')}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", [])
    if not data:
        print("错误：API 未返回图片数据", file=sys.stderr)
        sys.exit(1)

    for i, item in enumerate(data):
        if "error" in item:
            print(f"  图片 {i+1} 生成失败: {item['error'].get('message', '未知错误')}", file=sys.stderr)
            continue

        if args.response_format == "b64_json":
            output_path = args.output
            if len(data) > 1:
                base, ext = os.path.splitext(args.output)
                output_path = f"{base}_{i+1}{ext}"
            save_base64_image(item["b64_json"], output_path)
        else:
            url = item.get("url")
            if not url:
                print(f"  图片 {i+1} 未返回 URL", file=sys.stderr)
                continue
            output_path = args.output
            if len(data) > 1:
                base, ext = os.path.splitext(args.output)
                output_path = f"{base}_{i+1}{ext}"
            download_file(url, output_path)

        size_info = item.get("size", "未知")
        print(f"  尺寸: {size_info}")

    usage = result.get("usage", {})
    print(f"生成完成。图片数量: {usage.get('generated_images', '未知')}, Token: {usage.get('total_tokens', '未知')}")


def generate_video(args):
    """调用 Seedance API 生成视频"""
    api_key = get_api_key()

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

    print(f"正在创建视频生成任务...")
    print(f"  模型: {args.model}")
    print(f"  比例: {args.ratio}")
    print(f"  时长: {args.duration}秒")
    print(f"  分辨率: {args.resolution}")
    print(f"  提示词: {args.prompt[:80]}...")

    result = make_request(SEEDANCE_TASK_API, payload, api_key)

    if "error" in result:
        print(f"API 错误: {result['error'].get('message', '未知错误')}", file=sys.stderr)
        sys.exit(1)

    task_id = result.get("id")
    if not task_id:
        print("错误：API 未返回任务 ID", file=sys.stderr)
        print(f"返回内容: {json.dumps(result, ensure_ascii=False, indent=2)}", file=sys.stderr)
        sys.exit(1)

    print(f"任务已创建，ID: {task_id}")
    print(f"正在等待生成完成...")

    # 轮询任务状态
    max_wait = args.max_wait
    poll_interval = 10
    elapsed = 0

    while elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval

        query_url = SEEDANCE_QUERY_API.format(task_id=task_id)
        query_result = make_request(query_url, None, api_key, method="GET")

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
                print(f"返回内容: {json.dumps(query_result, ensure_ascii=False, indent=2)}", file=sys.stderr)
                sys.exit(1)

            download_file(video_url, args.output)
            print(f"视频生成完成！")
            return

        elif status == "failed":
            error_info = query_result.get("error", {})
            print(f"任务失败: {error_info.get('message', '未知错误')}", file=sys.stderr)
            sys.exit(1)

        elif status == "expired":
            print("任务超时", file=sys.stderr)
            sys.exit(1)

    print(f"等待超时（{max_wait}秒），请稍后手动查询任务状态: {task_id}", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="pop-novel-visual API 调用脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="生成模式")

    # 图片生成子命令
    img_parser = subparsers.add_parser("image", help="Seedream 图片生成")
    img_parser.add_argument("--prompt", required=True, help="提示词（中文≤300字）")
    img_parser.add_argument("--model", default="doubao-seedream-5-0-pro-260628", help="模型 ID（默认 5.0 Pro）")
    img_parser.add_argument("--size", default=None, help="图片尺寸（如 1728x2304 或 2K）")
    img_parser.add_argument("--output", required=True, help="输出文件路径")
    img_parser.add_argument("--watermark", action="store_true", default=False, help="添加水印")
    img_parser.add_argument("--response-format", choices=["url", "b64_json"], default="url", help="返回格式")
    img_parser.add_argument("--image", default=None, help="参考图 URL 或 Base64")
    img_parser.add_argument("--seed", type=int, default=None, help="随机种子")
    img_parser.set_defaults(func=generate_image)

    # 视频生成子命令
    vid_parser = subparsers.add_parser("video", help="Seedance 视频生成")
    vid_parser.add_argument("--prompt", required=True, help="提示词（中文≤500字）")
    vid_parser.add_argument("--model", default="doubao-seedance-1-0-pro-250428", help="模型 ID")
    vid_parser.add_argument("--ratio", default="16:9", help="视频比例")
    vid_parser.add_argument("--duration", type=int, default=5, help="视频时长（秒）")
    vid_parser.add_argument("--resolution", default="1080p", help="分辨率")
    vid_parser.add_argument("--camera-fixed", action="store_true", default=False, help="固定镜头")
    vid_parser.add_argument("--watermark", action="store_true", default=False, help="添加水印")
    vid_parser.add_argument("--output", required=True, help="输出文件路径")
    vid_parser.add_argument("--image", default=None, help="首帧图片 URL 或 Base64")
    vid_parser.add_argument("--max-wait", type=int, default=600, help="最大等待时间（秒）")
    vid_parser.set_defaults(func=generate_video)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
