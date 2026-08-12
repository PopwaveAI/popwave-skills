"""通用帧序列编码脚本：用 imageio-ffmpeg 自带的完整版 ffmpeg 把 PNG 帧合成 MP4。
用法:
  python encode.py --frames <frames目录> --out <out.mp4> [--fps 30] [--crf 18]
说明: 用完整版 ffmpeg（含 libx264），可处理标准 PNG 输入；系统精简版 ffmpeg 无此能力。
"""
import os, subprocess, argparse
import imageio_ffmpeg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, default=18)
    args = ap.parse_args()

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg, "-y",
           "-framerate", str(args.fps),
           "-i", os.path.join(args.frames, "f_%05d.png"),
           "-c:v", "libx264",
           "-pix_fmt", "yuv420p",
           "-crf", str(args.crf),
           "-preset", "medium",
           "-movflags", "+faststart",
           "-r", str(args.fps),
           args.out]
    print("encode with:", ffmpeg)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("STDERR tail:", res.stderr[-800:])
    print("exit", res.returncode)


if __name__ == "__main__":
    main()