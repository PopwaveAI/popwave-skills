"""通用逐帧渲染脚本：把 JS 驱动的 HTML 动效时间线渲染成 PNG 帧序列。
用法:
  python render_frames.py --html <index.html> --out <frames或preview目录> \
      [--fps 30] [--w 1920] [--h 1080] [--mode preview|full] \
      [--start 0] [--end 33] [--times 0.5,2.0,7.0]
约定: HTML 必须暴露 window.render(t)（t 为秒），渲染由 agent 的 JS 时间线驱动。
mode=preview 按 --times 抓关键帧做构图校验；mode=full 按 [start,end]@fps 逐帧渲染。
"""
import os, sys, argparse
from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=float, default=30.0)
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--mode", default="preview", choices=["preview", "full"])
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=33.0)
    ap.add_argument("--times", default="")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.w, "height": args.h},
                                device_scale_factor=1)
        page.goto("file:///" + os.path.abspath(args.html).replace("\\", "/"))
        page.wait_for_timeout(300)

        if args.mode == "preview":
            times = [float(x) for x in args.times.split(",") if x.strip()] or [5.0]
            for t in times:
                page.evaluate(f"render({t})")
                page.wait_for_timeout(60)
                page.screenshot(path=os.path.join(args.out, f"t_{t:04.1f}.png"))
            print("preview done", len(times))
        else:
            n = int(round((args.end - args.start) * args.fps))
            for i in range(n):
                t = args.start + i / args.fps
                page.evaluate(f"render({t})")
                page.screenshot(path=os.path.join(args.out, f"f_{i:05d}.png"))
                if i % 150 == 0:
                    print("frame", i, "/", n, flush=True)
            print("render done", n)
        browser.close()


if __name__ == "__main__":
    main()