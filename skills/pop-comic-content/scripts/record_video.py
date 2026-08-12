"""pop-comic-content 方案B：浏览器自播 + 录屏出片（替代逐帧截图）。
原理：给已有 render(t) 的 HTML 注入"自播时钟"，requestAnimationFrame 按真实时间驱动
render(t) 从 0 播到 duration 秒，Playwright record_video 边播边录成 WebM，再转 MP4。
对比逐帧截图方案：不落千张 PNG，57s 视频实测全程 ~86s 出片（逐帧方案光渲染就 7-10 分钟）。

用法:
  python record_video.py --html <index.html> --out <成品.mp4> \
      --duration <总时长秒> [--w 1080] [--h 1920] [--fps 30] [--crf 18] [--preset veryfast]

前置: 同 render_frames.py（Playwright + Chromium + imageio-ffmpeg）。
"""
import os, sys, time, subprocess, argparse
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

# 注入到 </body> 前的自播时钟脚本（不改原 render(t) 逻辑）
SELFPLAY_JS = """
<script>
window._startSelfPlay = function(durationSec){
  var start = performance.now();
  function tick(){
    var t = (performance.now() - start) / 1000;
    window.render(t);
    if (t < durationSec) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
};
</script>
"""


def inject_selfplay(html_path, out_html):
    with open(html_path, encoding="utf-8") as f:
        html = f.read()
    if "</body>" in html:
        html = html.replace("</body>", SELFPLAY_JS + "</body>")
    else:
        html += SELFPLAY_JS
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    return out_html


def webm_to_mp4(webm, mp4, fps, crf, preset):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg, "-y",
           "-i", webm,
           "-c:v", "libx264",
           "-pix_fmt", "yuv420p",
           "-crf", str(crf),
           "-preset", preset,
           "-r", str(fps),
           "-movflags", "+faststart",
           mp4]
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--duration", type=float, required=True, help="动画总时长(秒)")
    ap.add_argument("--w", type=int, default=1080)
    ap.add_argument("--h", type=int, default=1920)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="veryfast", help="x264 转码预设(veryfast更快/fast/medium质量更好)")
    ap.add_argument("--keep-webm", action="store_true", help="保留中间 webm")
    args = ap.parse_args()

    workdir = os.path.dirname(os.path.abspath(args.out)) or "."
    os.makedirs(workdir, exist_ok=True)
    # 自播 HTML 必须写到 HTML 原同目录：HTML 里的相对资源（如 panels/P1-1.png）
    # 是相对 index.html 所在目录解析的，写错目录会导致图片全部 404 破图。
    html_dir = os.path.dirname(os.path.abspath(args.html)) or "."
    tmp_html = os.path.join(html_dir, "_selfplay.html")
    inject_selfplay(args.html, tmp_html)

    video_dir = os.path.join(workdir, "_rec")
    os.makedirs(video_dir, exist_ok=True)

    t0 = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": args.w, "height": args.h},
            device_scale_factor=1,
            record_video_dir=video_dir,
            record_video_size={"width": args.w, "height": args.h},
        )
        page = ctx.new_page()
        page.goto("file:///" + os.path.abspath(tmp_html).replace("\\", "/"))
        page.wait_for_timeout(400)  # 等图片加载
        page.evaluate(f"window._startSelfPlay({args.duration})")
        page.wait_for_timeout(int((args.duration + 0.8) * 1000))
        page.wait_for_timeout(300)
        video = page.video
        webm = video.path() if video else None
        ctx.close()
        browser.close()

    if not webm or not os.path.exists(webm):
        print("[错误] 未生成录屏 webm", file=sys.stderr)
        sys.exit(1)

    rec_sec = time.time() - t0
    print(f"[OK] 录屏完成 {rec_sec:.1f}s -> {webm}")

    res = webm_to_mp4(webm, args.out, args.fps, args.crf, args.preset)
    if res.returncode != 0:
        print("STDERR tail:", res.stderr[-600:], file=sys.stderr)
        sys.exit(1)
    total_sec = time.time() - t0
    print(f"[OK] 转码完成 {total_sec:.1f}s -> {args.out}")

    if not args.keep_webm and os.path.exists(webm):
        try:
            os.remove(webm)
        except OSError:
            pass
    if os.path.exists(tmp_html):
        try:
            os.remove(tmp_html)
        except OSError:
            pass


if __name__ == "__main__":
    main()