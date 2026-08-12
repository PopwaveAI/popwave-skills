#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pop-comic-content 混音脚本：把分句配音按时间轴混入无声视频，可选加 BGM。
本轮实操验证：配音段用 adelay 定位到对应字幕时间点，amix 混合，volume 控响度。
用法:
  python mix_audio.py \
    --video 成品.mp4 --audio-dir audio \
    --offsets "seg01.mp3=3.0,seg02.mp3=8.9,seg03.mp3=16.2,..." \
    --out 成品-配音.mp4 \
    [--bgm bgm.mp3 --bgm-vol 0.15 --voice-vol 1.1]
"""
import argparse
import os
import subprocess
import sys

import imageio_ffmpeg


def main():
    p = argparse.ArgumentParser(description="把分句配音按时间轴混入无声视频")
    p.add_argument("--video", required=True, help="无声视频")
    p.add_argument("--audio-dir", required=True, help="配音 mp3 目录")
    p.add_argument("--offsets", required=True, help="seg文件=起始秒,逗号分隔，如 seg01.mp3=3.0,seg02.mp3=8.9")
    p.add_argument("--out", required=True, help="输出 mp4")
    p.add_argument("--bgm", default=None, help="可选BGM文件")
    p.add_argument("--bgm-vol", type=float, default=0.15, help="BGM 音量")
    p.add_argument("--voice-vol", type=float, default=1.1, help="口播音量")
    args = p.parse_args()

    segmap = []
    for item in args.offsets.split(","):
        f, _, start = item.partition("=")
        segmap.append((f.strip(), float(start)))
    n_seg = len(segmap)

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)

    inputs = [ffmpeg, "-y", "-i", args.video]
    for f, _ in segmap:
        inputs += ["-i", os.path.join(args.audio_dir, f)]

    delayed = []
    for i in range(n_seg):
        ms = int(round(segmap[i][1] * 1000))
        delayed.append(f"[{i+1}:a]adelay={ms}|{ms}[d{i}]")
    mix_in = "".join(f"[d{i}]" for i in range(n_seg))
    filter_parts = [
        ";".join(delayed) + f";{mix_in}amix=inputs={n_seg}:normalize=0,volume={args.voice_vol}[voice]"
    ]

    if args.bgm:
        inputs += ["-stream_loop", "-1", "-i", args.bgm]
        filter_parts.append(f"[{n_seg+1}:a]volume={args.bgm_vol}[bgm]")
        filter_parts.append("[voice][bgm]amix=inputs=2:duration=first:normalize=0[aout]")
    else:
        filter_parts.append("[voice]anull[aout]")

    cmd = inputs + [
        "-filter_complex", ";".join(filter_parts),
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", args.out,
    ]
    print(" ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr)
        sys.exit(1)
    print(f"[OK] {args.out} {os.path.getsize(args.out)//1024}KB")
    sys.exit(0)


if __name__ == "__main__":
    main()