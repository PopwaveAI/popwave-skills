#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pop-video-brand 火山语音 TTS 配音脚本 v0.1.0
用火山语音「豆包语音合成」按口播文案生成人声 MP3。
默认音色：知性灿灿 2.0（zh_female_cancan_uranus_bigtts），温暖专业女声，品宣首选。

前置：火山语音控制台开通「豆包语音合成大模型」，申请 X-Api-Key（新版控制台单头鉴权）。
接口：POST https://openspeech.bytedance.com/api/v3/tts/create   model=seed-audio-1.0

用法：
  python tts_generate.py \
    --api-key <X-Api-Key> \
    --text "要合成的文案" \
    --out "out.mp3" \
    [--speaker zh_female_cancan_uranus_bigtts] \
    [--speech-rate 0] [--loudness-rate 0] [--pitch-rate 0]
"""
import argparse
import base64
import json
import os
import sys
import urllib.request

URL = "https://openspeech.bytedance.com/api/v3/tts/create"
DEFAULT_SPEAKER = "zh_female_cancan_uranus_bigtts"  # 知性灿灿 2.0（默认）


def synth(api_key, text, out_path, speaker=None,
          speech_rate=0, loudness_rate=0, pitch_rate=0, retries=3):
    """逐句合成，失败重试。返回是否成功。"""
    payload = {
        "model": "seed-audio-1.0",
        "text_prompt": text,
        "audio_config": {
            "format": "mp3",
            "sample_rate": 48000,
            "pitch_rate": pitch_rate,
            "speech_rate": speech_rate,
            "loudness_rate": loudness_rate,
        },
        "watermark": {},
    }
    if speaker:
        # seed-audio-1.0 的音色必须放在 references[0].speaker，顶层 speaker 字段不生效
        payload["references"] = [{"speaker": speaker}]
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    for attempt in range(1, retries + 1):
        req = urllib.request.Request(URL, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        req.add_header("X-Api-Key", api_key)
        req.add_header("X-Api-Request-Id", f"popwave-tts-{os.path.basename(out_path)}-{attempt}")
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                body = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"  [重试 {attempt}/{retries}] HTTP {e.code}: {e.read().decode(errors='ignore')[:300]}", file=sys.stderr)
            _sleep(1.5)
            continue
        except Exception as e:
            print(f"  [重试 {attempt}/{retries}] {type(e).__name__}: {e}", file=sys.stderr)
            _sleep(1.5)
            continue

        audio_b64 = body.get("audio")
        if not audio_b64:
            print(f"  [重试 {attempt}/{retries}] code={body.get('code')} msg={body.get('message')}", file=sys.stderr)
            _sleep(1.5)
            continue
        raw = base64.b64decode(audio_b64)
        with open(out_path, "wb") as f:
            f.write(raw)
        print(f"[OK] {out_path} {len(raw)//1024}KB dur={body.get('duration')}s")
        return True
    return False


def _sleep(s):
    import time
    time.sleep(s)


def main():
    p = argparse.ArgumentParser(description="pop-video-brand 火山语音 TTS 配音")
    p.add_argument("--api-key", required=True, help="火山语音 X-Api-Key")
    p.add_argument("--text", required=True, help="要合成的文案")
    p.add_argument("--out", required=True, help="输出 MP3 路径")
    p.add_argument("--speaker", default=DEFAULT_SPEAKER, help="音色,默认知性灿灿2.0")
    p.add_argument("--speech-rate", type=int, default=0, help="语速 [-50,100],0不调")
    p.add_argument("--loudness-rate", type=int, default=0, help="音量 [-50,100],0不调")
    p.add_argument("--pitch-rate", type=int, default=0, help="音调 [-12,12],0不调")
    p.add_argument("--retries", type=int, default=3, help="失败重试")
    args = p.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    ok = synth(args.api_key, args.text, args.out, args.speaker,
               args.speech_rate, args.loudness_rate, args.pitch_rate, args.retries)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()