#!/usr/bin/env python3
"""pop-video-comic 渲染合成脚本 v0.2.0
用 PyAV（自带完整 ffmpeg 库）完成：HTML 排版 + Playwright 截图 + 图片→视频 + 音频混流。
不再依赖外部 ffmpeg exe（TRAE 内置 ffmpeg 为精简版，无音频解码）。
用法：
  python render_video.py --manifest "<项目>/视频/audio/时长清单.json" \
    --assets "<项目>/漫画/第1章/output" --out "<项目>/视频/绯红.mp4" \
    --size 1080x1920
"""
import argparse
import json
import os
import subprocess
import sys
from fractions import Fraction

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

try:
    from playwright.sync_api import sync_playwright
    HAS_PW = True
except ImportError:
    HAS_PW = False

WIDTH, HEIGHT = 1080, 1920
FPS = 30
FONT_CANDIDATES = ["Noto Sans CJK SC", "WenQuanYi Micro Hei", "Microsoft YaHei", "SimHei"]


def load_manifest(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def find_image(assets_dir, page):
    for cand in (f"{page}.png", f"{page}.jpg", f"{page}.jpeg"):
        p = os.path.join(assets_dir, cand)
        if os.path.exists(p):
            return p
    return None


def load_font(size):
    for name in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def render_frame(img_path, text, duration_sec, width, height):
    """渲染单帧图：图片 cover 填充 + 底部字幕 + 字幕分段显示。"""
    img = Image.open(img_path).convert("RGB")
    # object-fit: cover 缩放居中
    iw, ih = img.size
    scale = max(width / iw, height / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    x = (nw - width) // 2
    y = (nh - height) // 2
    img = img.crop((x, y, x + width, y + height))

    # 字幕
    draw = ImageDraw.Draw(img)
    font = load_font(int(height * 0.045))
    # 简单居中换行
    lines = []
    max_chars = max(1, (width - 60) // (int(height * 0.045)))
    cur = ""
    for ch in text:
        if len(cur) >= max_chars:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    lines.append(cur)
    # 底部渐变遮罩
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(int(height * 0.25)):
        alpha = int(180 * (i / (height * 0.25)))
        od.line([(0, height - int(height * 0.25) + i),
                 (width, height - int(height * 0.25) + i)], fill=(0, 0, 0, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

    # 画字幕文字
    draw = ImageDraw.Draw(img)
    total_h = len(lines) * (int(height * 0.045) + 8)
    y_start = height - int(height * 0.25) + (int(height * 0.25) - total_h) // 2
    for i, line in enumerate(lines):
        tw = draw.textlength(line, font=font)
        tx = (width - tw) // 2
        ty = y_start + i * (int(height * 0.045) + 8)
        draw.text((tx, ty), line, font=font, fill=(255, 255, 255),
                  stroke_width=2, stroke_fill=(0, 0, 0))
    return img


def ken_burns(img, t, duration, width, height):
    """Ken Burns 推拉：从 scale 1.0 缓动到 1.12，轻微上移。"""
    progress = min(max(t / duration, 0.0), 1.0)
    scale = 1.0 + 0.12 * progress
    iw, ih = width, height
    nw, nh = int(iw * scale), int(ih * scale)
    # 居中缩放 + 轻微上移
    x = (nw - iw) // 2
    y = (nh - ih) // 2 - int((nh - ih) * 0.15 * progress)
    return img.resize((nw, nh), Image.LANCZOS).crop((x, y, x + iw, y + ih))


def assemble_av(frames, manifest, out_path, width, height, fps=FPS):
    """用 PyAV 把帧序列 + 音频合成 MP4。"""
    out_mp4 = out_path
    os.makedirs(os.path.dirname(os.path.abspath(out_mp4)) or ".", exist_ok=True)

    # 收集每句音频片段路径（相对 out 目录 / 或 manifest 同级 audio/）
    audio_dir = os.path.join(os.path.dirname(os.path.abspath(out_mp4)), "audio")
    audio_segments = []
    for m in manifest:
        p = os.path.join(audio_dir, m.get("file", ""))
        audio_segments.append(p if os.path.exists(p) else None)

    with av.open(out_mp4, "w") as container:
        vstream = container.add_stream("h264", rate=fps)
        vstream.width = width
        vstream.height = height
        vstream.pix_fmt = "yuv420p"
        vstream.options = {"preset": "veryfast", "crf": "23"}

        # 视频流
        for img in frames:
            arr = np.asarray(img)
            frame = av.VideoFrame.from_ndarray(arr, format="rgb24")
            for packet in vstream.encode(frame):
                container.mux(packet)
        for packet in vstream.encode(None):
            container.mux(packet)

        # 音频流：先解码所有片段到 PCM，拼接成连续数组，再统一写入
        astream = container.add_stream("aac", 24000)
        astream.layout = "mono"
        pending = []  # 待写音频帧（已重采样 24k mono fltp）
        for i, m in enumerate(manifest):
            ap = audio_segments[i]
            if not ap:
                print(f"[警告] 音频缺失 {m.get('file')}，跳过", file=sys.stderr)
                continue
            try:
                with av.open(ap) as ac:
                    ast = ac.streams.audio[0]
                    resampler = av.AudioResampler(format="fltp", layout="mono", rate=24000)
                    for frame in ac.decode(ast):
                        for rframe in resampler.resample(frame):
                            pending.append(rframe)
            except Exception as e:
                print(f"[警告] 音频解码失败 {m.get('file')}: {e}", file=sys.stderr)
            # 片段间加 0.3s 静音（用零数组）
            silence = av.AudioFrame.from_ndarray(
                np.zeros((1, 7200), dtype="float32"), format="fltp", layout="mono")
            silence.sample_rate = 24000
            pending.append(silence)

        # 统一写入，时间戳连续
        sample_pos = 0
        for rframe in pending:
            rframe.pts = sample_pos
            for packet in astream.encode(rframe):
                container.mux(packet)
            sample_pos += rframe.samples
        for packet in astream.encode(None):
            container.mux(packet)

    print(f"视频已生成: {out_mp4}")


def main():
    p = argparse.ArgumentParser(description="pop-video-comic 渲染合成 v0.2.0")
    p.add_argument("--manifest", required=True, help="时长清单.json 路径")
    p.add_argument("--assets", required=True, help="漫画页图片目录")
    p.add_argument("--out", required=True, help="输出 mp4 路径")
    p.add_argument("--size", default="1080x1920", help="画布尺寸 WxH")
    args = p.parse_args()
    w, h = map(int, args.size.lower().split("x"))

    manifest = load_manifest(args.manifest)

    # 生成每帧时长（口播时长 + 尾音余量）
    frames = []
    for m in manifest:
        dur = m.get("duration_sec") or 3.0
        hold = round(dur + 0.5, 2)
        img_path = find_image(args.assets, m["page"])
        if not img_path:
            print(f"[警告] 未找到图片 {m['page']}，跳过", file=sys.stderr)
            continue
        base = render_frame(img_path, m["text"], dur, w, h)
        n_frames = max(1, int(hold * FPS))
        for i in range(n_frames):
            frames.append(ken_burns(base, i / FPS, hold, w, h))
        print(f"[{m['seq']}] {m['page']} hold={hold}s 帧数={n_frames}")

    if not frames:
        print("[错误] 无帧可合成", file=sys.stderr)
        sys.exit(1)

    total_sec = len(frames) / FPS
    print(f"总帧数={len(frames)} 总时长约={total_sec:.1f}s")

    assemble_av(frames, manifest, args.out, w, h)


if __name__ == "__main__":
    main()