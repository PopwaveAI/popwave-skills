#!/usr/bin/env python3
"""
pop-book-promo — Preflight 前置检查

在每次正式生成前运行，验证运行环境是否就绪。
返回 0 = 全部通过，非 0 = 有阻塞项。

用法:
  python3 preflight.py [--input <data.json>] [--backend seedream|openrouter]
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PASS = "✅"
WARN = "⚠️"
FAIL = "❌"

checks = []


def check(ok: bool, label: str, detail: str = ""):
    icon = PASS if ok else FAIL
    checks.append((ok, label, detail))
    print(f"  {icon}  {label}")
    if detail:
        print(f"       {detail}")


def main():
    parser = argparse.ArgumentParser(description="pop-book-promo preflight")
    parser.add_argument("--input", "-i", type=Path, help="可选：额外校验输入 JSON 文件")
    parser.add_argument("--backend", choices=["seedream", "openrouter"],
                        default="seedream", help="生图后端（默认 seedream）")
    args = parser.parse_args()

    print("\n═══════════════════════════════════════════")
    print("  pop-book-promo · 前置检查")
    print("═══════════════════════════════════════════\n")

    # ── 1. Python 版本 ──
    py_ok = sys.version_info >= (3, 8)
    check(py_ok, f"Python ≥ 3.8", f"当前: {sys.version}")

    # ── 2. Python 依赖 — generate.py 只用标准库无需安装 ——
    try:
        import json, base64, urllib.request, html, re
        check(True, "Python 标准库就绪（json/base64/urllib/html/re）")
    except ImportError as e:
        check(False, "Python 标准库就绪", f"缺失: {e}")

    # ── 3. API Key 检查 ──
    if args.backend == "seedream":
        # Seedream: 内嵌 key 总是可用，环境变量覆盖
        check(True, "Seedream API Key", "已内嵌（可被 ARK_API_KEY 环境变量覆盖）")
    else:
        # OpenRouter: 需要环境变量或 --api-key
        api_key = os.getenv("OPEN_ROUTER_API_KEY")
        if api_key:
            masked = api_key[:8] + "..." + api_key[-4:]
            check(True, "OPEN_ROUTER_API_KEY 已设置", masked)
        else:
            check(False, "OPEN_ROUTER_API_KEY 已设置",
                  "请设置环境变量: export OPEN_ROUTER_API_KEY='sk-or-v1-...'")

    # ── 4. 模板文件完整 ──
    expected_templates = ["comic.html", "scroll.html", "scenes.html", "quote.html", "gallery.html"]
    templates_dir = HERE / "templates"
    missing_tpls = [t for t in expected_templates if not (templates_dir / t).exists()]
    check(len(missing_tpls) == 0, "模板文件完整",
          f"缺失: {', '.join(missing_tpls)}" if missing_tpls else f"已找到 {len(expected_templates)} 个模板")

    # ── 5. 生成脚本存在 ──
    gen_script = HERE / "scripts" / "generate.py"
    check(gen_script.exists(), "generate.py 存在",
          str(gen_script) if gen_script.exists() else "文件未找到")

    # ── 6. 可选：输入 JSON 校验 ──
    if args.input:
        input_path = args.input
        if not input_path.exists():
            check(False, f"输入文件存在: {input_path.name}", "文件未找到")
        else:
            try:
                data = json.loads(input_path.read_text(encoding="utf-8"))
                check(True, f"输入 JSON 格式合法: {input_path.name}")

                # 根据 mode 检查必填字段
                if "scenes" in data:
                    check(len(data["scenes"]) > 0, "scenes 数组非空")
                if "quotes" in data:
                    check(len(data["quotes"]) > 0, "quotes 数组非空")
                if "characters" in data:
                    check(len(data["characters"]) > 0, "characters 数组非空")
                if data.get("novel") or data.get("title"):
                    title = data.get("novel") or data.get("title", "")
                    check(True, f"小说名: {title}")
                else:
                    check(False, "小说名缺失",
                          "JSON 中需要 'novel' 或 'title' 字段")
            except json.JSONDecodeError as e:
                check(False, f"输入 JSON 格式合法: {input_path.name}", str(e))

    # ── 汇总 ──
    print()
    passed = sum(1 for ok, _, _ in checks if ok)
    failed = sum(1 for ok, _, _ in checks if not ok)
    total = len(checks)
    print(f"  结果: {passed}/{total} 通过", end="")
    if failed > 0:
        print(f", {failed} 项失败 ❌")
    else:
        print(" ✅")

    print()
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
