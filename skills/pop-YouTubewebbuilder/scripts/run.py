#!/usr/bin/env python3
"""
pop-YouTubewebbuilder — run.py (v4.1)
一键数据管线：抓取 YouTube 频道数据 → 结构化分析 → 输出供 agent 创作的素材。

v4 变更：
  - 移除所有 emoji（兼容 Windows GBK 终端）
  - 自动以频道 handle 命名输出文件（避免 data.json 被覆盖）
  - 用法示例全面兼容 Windows PowerShell

用法：
    python scripts/run.py --channel-url "https://www.youtube.com/@handle"
    python scripts/run.py --channel-url "https://www.youtube.com/@handle" --analysis-only
    python scripts/run.py --channel-id "UC_xxxxx"
    # Windows PowerShell 用户用 ; 分隔，如：
    # cd 项目目录; python scripts/run.py --channel-url "..."
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)


def resolve_api_key(provided=None):
    if provided:
        return provided
    cfg_path = os.path.join(ROOT_DIR, "config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            key = cfg.get("youtube_api_key", "")
            if key and len(key) > 10:
                return key
        except Exception:
            pass
    return None


def extract_handle(channel_url):
    """从频道 URL 中提取 @handle，做文件名安全处理"""
    if not channel_url:
        return None
    m = re.search(r'@([\w\-\.]+)', channel_url)
    if m:
        handle = m.group(1)
        # 文件名安全处理：只保留字母数字下划线
        safe = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fff]', '_', handle)
        return safe
    return None


def derive_filename(args):
    """如果用户没有指定 --data/--analysis，根据频道标识自动命名"""
    prefix = None
    if args.channel_url:
        safe = extract_handle(args.channel_url)
        if safe:
            prefix = f"data_{safe}"
    elif args.channel_id:
        cid = args.channel_id.replace("UC_", "").replace("UC", "")[:12]
        prefix = f"data_{cid}"

    if prefix:
        if args.data == "data.json":
            args.data = f"{prefix}.json"
        if args.analysis == "analysis_ready.json":
            args.analysis = f"{prefix}_analysis.json"
    return args


DEFAULT_DATA = "data.json"
DEFAULT_ANALYSIS = "analysis_ready.json"


def print_guide(data_file, analysis_file):
    print(f"""
{'=' * 60}
  [OK] 数据管线完成！可用素材已准备就绪：
{'=' * 60}

  以下文件可供 agent 创作时读取：

    [FILE] {data_file}              <- YouTube 原始频道 + 视频数据
    [FILE] {analysis_file}    <- 结构化分析 + 创作提示

  接下来三步走（详见 SKILL.md）：

    第 1 步 -> 产出网站设计 PRD
      读取 {data_file} + {analysis_file}
      参照 SKILL.md 中的「设计原则」+「PRD 模板」
      输出 {频道名}_设计PRD.md

    第 2 步 -> 给用户确认 PRD
      用户过目 PRD 中的色彩/字体/布局决策
      确认后方可进入 HTML 创作

    第 3 步 -> 创作 HTML
      基于已确认的 PRD
      输出自包含单文件 HTML（所有 CSS/JS 内联）

  铁律：PRD 未经确认，不得进入 HTML 创作。
""")


def main():
    parser = argparse.ArgumentParser(description="pop-YouTubewebbuilder - 数据管线")
    parser.add_argument("--api-key", help="YouTube Data API v3 Key（默认从 config.json 读取）")
    parser.add_argument("--channel-url", help="YouTube 频道链接")
    parser.add_argument("--channel-id", help="YouTube 频道 ID")
    parser.add_argument("--data", default=DEFAULT_DATA, help=f"输出数据 JSON 路径（默认自动按频道名命名）")
    parser.add_argument("--analysis", default=DEFAULT_ANALYSIS, help=f"输出分析 JSON 路径（默认自动按频道名命名）")
    parser.add_argument("--max-videos", type=int, default=12, help="最多视频数（默认12）")
    parser.add_argument("--analysis-only", action="store_true", help="跳过抓取，仅对已有数据做分析")
    args = parser.parse_args()

    # 自动命名输出文件（如果用户没指定）
    args = derive_filename(args)

    if not args.analysis_only:
        # -- Step 1: 校验输入 --
        if not args.channel_url and not args.channel_id:
            print("[ERR] 请指定 --channel-url 或 --channel-id")
            sys.exit(1)

        # -- Step 2: 抓取数据 --
        api_key = resolve_api_key(args.api_key)
        if not api_key:
            print("[ERR] 未找到 API Key。请在 config.json 中配置 youtube_api_key，或用 --api-key 传入。")
            sys.exit(1)

        fetch_args = [sys.executable, os.path.join(SCRIPT_DIR, "fetch_youtube.py")]
        if args.channel_url:
            fetch_args += ["--channel-url", args.channel_url]
        elif args.channel_id:
            fetch_args += ["--channel-id", args.channel_id]
        fetch_args += ["--api-key", api_key, "--out", args.data, "--max-videos", str(args.max_videos)]

        print(f"[YT] 抓取 YouTube 数据...")
        start = time.time()
        result = subprocess.run(fetch_args)
        if result.returncode != 0:
            print("[ERR] 数据抓取失败")
            sys.exit(1)
        print(f"  [OK] 数据已保存: {args.data}  ({time.time()-start:.1f}s)")

    else:
        if not os.path.exists(args.data):
            print(f"[ERR] 数据文件不存在: {args.data}")
            print("   请先不带 --analysis-only 运行以抓取数据")
            sys.exit(1)
        print(f"[FILE] 使用已有数据: {args.data}")

    # -- Step 3: 数据分析 --
    print(f"[ANLZ] 运行数据分析...")
    analyze_args = [
        sys.executable, os.path.join(SCRIPT_DIR, "analyze.py"),
        "--data", args.data,
        "--out", args.analysis,
    ]
    result = subprocess.run(analyze_args)
    if result.returncode != 0:
        print("[WARN] 数据分析失败（不影响抓取的数据文件）")
    else:
        print(f"  [OK] 分析完成: {args.analysis}")

    # -- Step 4: 输出创作引导 --
    print_guide(args.data, args.analysis)


if __name__ == "__main__":
    main()
