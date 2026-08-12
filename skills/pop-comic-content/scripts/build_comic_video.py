#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pop-comic-content v0.11 出片脚本：整页顺序播放 + 封面信息页 + xfade 淡入淡出。
输入：封面图(可选) + 分享/成品整页图 + 对齐.json(整段配音每句 start/end) + 整段配音 mp3。
输出：无音轨中间 mp4 + 混入整段配音的 final mp4。不烧录字幕（成品图已内嵌文字）。

切页点对齐口播段边界：每页口播窗口 = 该页首句 start → 末句 end，
xfade 过渡中心 = 上一页末句 end（即下一页口播开始）。

用法：
  python build_comic_video.py \
    --base <项目根目录> --chap <第N章目录> --share <分享目录> \
    --align <对齐.json> --voice <整段配音.mp3> --chapter 1 --v v10 \
    [--cover <封面图.png>] [--cover-seq 0] [--trans 0.4]
"""
import argparse, json, os, subprocess, sys
import imageio_ffmpeg
from PIL import Image

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def build_cover(long_img, out_png, w=1080, h=1920):
    """从章节长图顶部标题区裁出竖版封面。"""
    im = Image.open(long_img)
    W, H = im.size
    crop_h = int(W / (w / h))
    top = im.crop((0, 0, W, min(crop_h, H)))
    top.resize((w, h), Image.LANCZOS).save(out_png)
    return out_png


def main():
    p = argparse.ArgumentParser(description="pop-comic-content 整页顺序播放出片")
    p.add_argument("--base", required=True, help="项目根目录")
    p.add_argument("--share", required=True, help="分享成品图目录")
    p.add_argument("--align", required=True, help="对齐.json（每句 start/end）")
    p.add_argument("--voice", required=True, help="整段配音 mp3")
    p.add_argument("--outdir", required=True, help="输出视频目录")
    p.add_argument("--chapter", type=int, default=1, help="章节号")
    p.add_argument("--v", default="v10", help="版本号")
    p.add_argument("--cover", default=None, help="封面图路径（长图或已裁封面）")
    p.add_argument("--cover-seq", type=int, default=0, help="封面对应的口播段 seq（0-based）")
    p.add_argument("--page-seq", default=None, help="JSON 字符串，页文件名->seq列表，如 '{\"page01.png\":[1,2],\"page02.png\":[3]}'；缺省则一页一段")
    p.add_argument("--trans", type=float, default=0.4, help="xfade 交叉时长")
    p.add_argument("--fg-h", type=int, default=1515, help="分享页前景缩放高度（820x1150->1515）")
    args = p.parse_args()

    with open(args.align, encoding="utf-8") as f:
        align = json.load(f)
    seq_time = {a["seq"]: (a["start"], a["end"]) for a in align}

    # 平滑消除句间 gap/重叠
    order = sorted(seq_time.keys())
    smooth = {}
    for i, s in enumerate(order):
        st, en = seq_time[s]
        if i > 0:
            st = max(st, seq_time[order[i - 1]][1])
        if en <= st + 0.3:
            en = st + 0.3
        smooth[s] = (round(st, 3), round(en, 3))

    # 素材：封面 + 分享页（依序）
    share = args.share
    imgs = []
    if args.cover:
        imgs.append(("cover", args.cover))
    # 分享页 page01..N.png
    for f in sorted(os.listdir(share)):
        if f.lower().startswith("page0") and f.lower().endswith((".png", ".jpg", ".jpeg")):
            imgs.append((f, os.path.join(share, f)))
    if not imgs:
        print("[错误] 未在分享目录找到 page0*.png", file=sys.stderr)
        sys.exit(1)

    # 页 -> seq 映射（默认一页一段；可用 --page-seq 精确指定）
    page_seq = {}
    if args.page_seq:
        page_seq = json.loads(args.page_seq)
    else:
        seq_used = [args.cover_seq] if args.cover else []
        cursor = args.cover_seq + 1 if args.cover else 0
        for name, _ in imgs:
            if name == "cover":
                page_seq["cover"] = [args.cover_seq]
            else:
                page_seq[name] = [cursor]
                cursor += 1

    # 每页口播窗口 & 输入时长
    TRANS = args.trans
    page_bounds = {}
    for img, seqs in page_seq.items():
        st = min(smooth[s][0] for s in seqs)
        en = max(smooth[s][1] for s in seqs)
        page_bounds[img] = (st, en)
    pages = list(page_bounds.keys())
    page_in_dur = {p: (page_bounds[p][1] - page_bounds[p][0]) + TRANS for p in pages}

    print("[i] 每页口播窗口:")
    for img in pages:
        st, en = page_bounds[img]
        print(f"  {img}: {st:7.3f} - {en:7.3f} ({en-st:.2f}s)")

    # 封面若不存在的口播段（如仅展示）则跳过
    cmd = [FFMPEG, "-y"]
    for img, imp in imgs:
        cmd += ["-loop", "1", "-t", f"{page_in_dur[img]:.3f}", "-i", imp]

    FG_H = args.fg_h
    fc_parts = []
    imgs_order = [nm for (nm, _) in imgs]
    for i, img in enumerate(imgs_order):
        fc_parts.append(
            f"[{i}:v]split[s{i}a][s{i}b];"
            f"[s{i}b]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"gblur=sigma=40,eq=brightness=0.35:contrast=0.9[b{i}];"
            f"[s{i}a]scale=1080:{FG_H}[f{i}];"
            f"[b{i}][f{i}]overlay=0:{(1920-FG_H)//2}[v{i}]"
        )
    prev = "v0"
    for i in range(1, len(imgs_order)):
        offset = page_bounds[imgs_order[i - 1]][1] - TRANS / 2
        outl = f"vx{i}"
        fc_parts.append(
            f"[{prev}][v{i}]xfade=transition=fade:duration={TRANS}:offset={offset:.3f}[{outl}]"
        )
        prev = outl

    fc = ";".join(fc_parts)
    os.makedirs(args.outdir, exist_ok=True)
    out = os.path.join(args.outdir, f"第{args.chapter}章-{args.v}.mp4")
    cmd += ["-filter_complex", fc, "-map", f"[{prev}]", "-r", "30",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast",
            "-movflags", "+faststart", out]
    print("[i] 运行 ffmpeg 拼接...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:], file=sys.stderr)
        sys.exit(1)
    print(f"[OK] {out} {os.path.getsize(out)//1024}KB")

    out_final = os.path.join(args.outdir, f"第{args.chapter}章-配音-{args.v}-final.mp4")
    cmd2 = [FFMPEG, "-y", "-i", out, "-i", args.voice,
            "-map", "0:v", "-map", "1:a",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", out_final]
    r2 = subprocess.run(cmd2, capture_output=True, text=True)
    if r2.returncode != 0:
        print(r2.stderr[-3000:], file=sys.stderr)
        sys.exit(1)
    print(f"[OK] {out_final} {os.path.getsize(out_final)//1024}KB")


if __name__ == "__main__":
    main()