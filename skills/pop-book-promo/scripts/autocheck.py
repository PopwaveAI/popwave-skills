#!/usr/bin/env python3
"""
pop-book-promo — Autocheck 自检脚本

验证技能完整性：
  1. 所有 Python 依赖可导入
  2. 模板文件完整
  3. 示例 JSON 均为合法格式
  4. 生成引擎可被 import（dry-run 导入检查）

用法:
  python3 -B scripts/autocheck.py
"""

import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # pop-book-promo 根目录
PASS = "✅"
FAIL = "❌"
WARN = "⚠️"

errors = []


def test(label: str, ok: bool, detail: str = ""):
    icon = PASS if ok else FAIL
    print(f"  {icon}  {label}")
    if not ok:
        errors.append((label, detail))
        if detail:
            print(f"       {detail}")
    elif detail:
        print(f"       {detail}")


def main():
    print("\n═══════════════════════════════════════════")
    print("  pop-book-promo · 自检")
    print("═══════════════════════════════════════════\n")

    # 1. Python 版本
    py_ok = sys.version_info >= (3, 8)
    test("Python ≥ 3.8", py_ok, f"当前: {sys.version}")

    # 2. Python imports — generate.py 仅用标准库，无需 pip install
    for mod in ["json", "base64", "argparse", "html", "re", "urllib.request"]:
        try:
            importlib.import_module(mod)
            test(f"模块可导入: {mod}", True)
        except ImportError:
            test(f"模块可导入: {mod}", False, "请 pip install")

    # 3. generate.py 可导入（语法检查）
    gen_path = HERE / "scripts" / "generate.py"
    if gen_path.exists():
        try:
            compile(gen_path.read_text(encoding="utf-8"), str(gen_path), "exec")
            test("generate.py 语法正确", True)
        except SyntaxError as e:
            test("generate.py 语法正确", False, str(e))
    else:
        test("generate.py 存在", False, "文件未找到")

    # 4. 模板完整性
    expected_templates = ["comic.html", "scroll.html", "scenes.html", "quote.html", "gallery.html"]
    tpl_dir = HERE / "templates"
    found = [t for t in expected_templates if (tpl_dir / t).exists()]
    missing = [t for t in expected_templates if t not in found]
    test(f"模板文件: {len(found)}/5", len(missing) == 0,
         f"缺失: {', '.join(missing) if missing else '全部完整'}")

    # 5. 示例 JSON 完整性
    json_files = ["scenes.json", "profile.json", "quotes.json", "characters.json"]
    ex_dir = HERE / "examples"
    valid_count = 0
    for jf in json_files:
        jp = ex_dir / jf
        if jp.exists():
            try:
                data = json.loads(jp.read_text(encoding="utf-8"))
                valid_count += 1
                # 检查基本字段
                has_novel = bool(data.get("novel") or data.get("title"))
                test(f"示例 {jf}: JSON 合法{' · 含novel字段' if has_novel else ''}", True)
            except json.JSONDecodeError as e:
                test(f"示例 {jf}: JSON 格式错误", False, str(e))
        else:
            test(f"示例 {jf}: 文件缺失", False)
    test(f"示例 JSON: {valid_count}/{len(json_files)} 合法", valid_count == len(json_files))

    # 6. preflight.py 存在且语法正确
    pf_path = HERE / "preflight.py"
    if pf_path.exists():
        try:
            compile(pf_path.read_text(encoding="utf-8"), str(pf_path), "exec")
            test("preflight.py 语法正确", True)
        except SyntaxError as e:
            test("preflight.py 语法正确", False, str(e))
    else:
        test("preflight.py 存在", False)

    # 7. 总摘要
    print(f"\n  自检完成: {len(errors)} 个问题")
    if errors:
        for label, detail in errors:
            print(f"    {FAIL} {label}")
            if detail:
                print(f"       {detail}")
        print("\n  请修复以上问题后再运行。")
        return 1
    else:
        print("  全部通过 ✅")
        return 0


if __name__ == "__main__":
    sys.exit(main())
