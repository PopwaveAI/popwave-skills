#!/usr/bin/env python3
"""pop-video-comic TTS 配音脚本 v0.1.1
按已确认的口播脚本逐句调用 edge-tts（异步库直调，比子进程更稳）生成人声，
输出分句 mp3 + 时长清单。
用法：
  python tts_generate.py --script "<项目>/视频/口播脚本.md" --out "<项目>/视频/audio" --voice zh-CN-YunxiNeural
"""
import argparse
import asyncio
import json
import os
import re
import sys
import time

import av
import edge_tts


def parse_script(script_path):
    """从口播脚本.md 提取口播句。每句形如:
    N. [pageX] (情绪) 文案
    或
    1. [page-封面] (钩子) 文案
    """
    with open(script_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    sentences = []
    pat = re.compile(r"^\s*(\d+)[.、]\s*\[([^\]]+)\]\s*\(([^)]*)\)\s*(.+)$")
    for ln in lines:
        m = pat.match(ln)
        if m:
            sentences.append({
                "seq": int(m.group(1)),
                "page": m.group(2).strip(),
                "emotion": m.group(3).strip(),
                "text": m.group(4).strip(),
            })
    if not sentences:
        print("[错误] 未从脚本解析到任何口播句。格式应为: 1. [page1] (情绪) 文案", file=sys.stderr)
        sys.exit(1)
    return sentences


def get_audio_duration(mp3_path):
    """用 PyAV 读取音频时长（秒）。PyAV 自带完整 ffmpeg 库，可解码 mp3。"""
    try:
        with av.open(mp3_path) as c:
            if c.duration:
                return c.duration / av.time_base
            return 0.0
    except Exception:
        return 0.0


async def synth_one(text, voice, out_path, retries=3):
    """异步合成单句，失败重试。"""
    for attempt in range(1, retries + 1):
        tts = edge_tts.Communicate(text, voice)
        try:
            await tts.save(out_path)
        except Exception as e:
            print(f"  [重试 {attempt}/{retries}] {type(e).__name__}: {e}", file=sys.stderr)
            await asyncio.sleep(1.5)
            continue
        if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
            return True
        print(f"  [重试 {attempt}/{retries}] 文件为空", file=sys.stderr)
        await asyncio.sleep(1.5)
    return False


def generate(sentences, out_dir, voice, retries=3):
    os.makedirs(out_dir, exist_ok=True)
    manifest = []
    for s in sentences:
        seg = f"seg{s['seq']:02d}.mp3"
        out_path = os.path.join(out_dir, seg)
        print(f"[{seg}] {s['page']} ({s['emotion']}) {s['text']}")
        ok = asyncio.run(synth_one(s["text"], voice, out_path, retries))
        if not ok:
            print(f"  [错误] 生成失败（重试{retries}次）: {s['text']}", file=sys.stderr)
            sys.exit(1)
        dur = get_audio_duration(out_path)
        manifest.append({
            "seq": s["seq"],
            "page": s["page"],
            "emotion": s["emotion"],
            "text": s["text"],
            "file": seg,
            "duration_sec": dur,
        })
        print(f"  duration: {dur}s")

    manifest_path = os.path.join(out_dir, "时长清单.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    total = sum(m["duration_sec"] for m in manifest)
    print(f"\n完成: {len(manifest)} 句, 总时长约 {total:.1f}s")
    print(f"清单: {manifest_path}")
    return manifest


def main():
    p = argparse.ArgumentParser(description="pop-video-comic TTS 配音")
    p.add_argument("--script", required=True, help="口播脚本.md 路径")
    p.add_argument("--out", required=True, help="输出音频目录")
    p.add_argument("--voice", default="zh-CN-YunxiNeural", help="edge-tts 音色")
    p.add_argument("--retries", type=int, default=3, help="每句失败重试次数")
    args = p.parse_args()

    sentences = parse_script(args.script)
    generate(sentences, args.out, args.voice, args.retries)


if __name__ == "__main__":
    main()