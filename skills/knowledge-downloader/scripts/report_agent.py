#!/usr/bin/env python3
"""
知识获取器 — Phase B：拆解报告生成器

通用工具，处理微信和 B 站的数据源。
通过读取原文 .md 文件 + 模板 + Prompt，输出供 AI 执行拆解的结构化上下文。

用法：
  单篇生成：  py report_agent.py "原文/文章.md" -o "拆解文/"
  批量生成：  py report_agent.py --batch "原文/" -o "拆解文/"
  批量去重：  py report_agent.py --batch "原文/" -o "拆解文/" --skip-existing
  目录整理：  py report_agent.py --organize -o "输出目录"
"""
import json
import os
import sys
import re
import glob

# ── 路径 ──────────────────────────────────────────────────────────
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(SKILL_DIR, "templates")
PROMPT_FILE = os.path.join(TEMPLATES_DIR, "report-prompt.md")
REPORT_TEMPLATE_FILE = os.path.join(TEMPLATES_DIR, "report-template.md")


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_frontmatter(path: str) -> dict:
    content = read_file(path)
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {"title": os.path.splitext(os.path.basename(path))[0], "account": "未知"}
    fm = {}
    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def build_report_context(article_path: str, report_path: str) -> str:
    fm = read_frontmatter(article_path)
    article_content = read_file(article_path)
    prompt_text = read_file(PROMPT_FILE)
    template_text = read_file(REPORT_TEMPLATE_FILE)

    context = f"""📄 原文文件: {article_path}
🧠 预期报告: {report_path}

---

## 原文信息

- **标题:** {fm.get('title', '未知')}
- **公众号:** {fm.get('account', '未知')}
- **日期:** {fm.get('date', '')}
- **源链接:** {fm.get('source_url', '')}

---

## 原文全文

```markdown
{article_content}
```

---

## 拆解模板（report-template.md）

```markdown
{template_text}
```

---

## 撰写 Prompt（report-prompt.md）

```markdown
{prompt_text}
```

---

请严格按照上述模板和 prompt 撰写拆解报告，保存到 `{report_path}`。
"""
    return context


def generate_report(article_path: str, output_dir: str) -> str:
    base = os.path.splitext(os.path.basename(article_path))[0]
    if base.endswith("_拆解报告"):
        return ""
    report_name = f"{base}_拆解报告.md"
    report_path = os.path.join(output_dir, report_name)
    context = build_report_context(article_path, report_path)
    return context


def batch_generate(articles_dir: str, output_dir: str, skip_existing: bool = False):
    md_files = sorted(glob.glob(os.path.join(articles_dir, "*.md")))
    md_files = [f for f in md_files if not os.path.basename(f).endswith("_拆解报告.md")]

    print("=" * 56)
    print(f"  Phase B 批处理模式")
    print(f"  原文目录: {articles_dir}")
    print(f"  输出目录: {output_dir}")
    print(f"  待处理: {len(md_files)} 篇")
    if skip_existing:
        print(f"  跳过已有: 是")
    print("=" * 56)

    pending = []
    for i, f in enumerate(md_files, 1):
        base = os.path.splitext(os.path.basename(f))[0]
        report_path = os.path.join(output_dir, f"{base}_拆解报告.md")
        exists = os.path.isfile(report_path)
        status = "✅ 已有" if exists else "⏳ 待处理"
        print(f"  [{i}/{len(md_files)}] {status}: {base[:50]}")
        if skip_existing and exists:
            continue
        pending.append(f)

    print(f"\n⏳ 待生成报告: {len(pending)} 篇\n")
    for i, f in enumerate(pending, 1):
        base = os.path.splitext(os.path.basename(f))[0]
        report_path = os.path.join(output_dir, f"{base}_拆解报告.md")
        print(f"{'─' * 48}")
        print(f"  [{i}/{len(pending)}] {base[:60]}")
        print(f"📄 原文: {f}")
        print(f"🔍 请完成拆解并保存到: {report_path}")
    return pending


def organize_output(output_dir: str):
    yuanwen_dir = os.path.join(output_dir, "原文")
    chaijie_dir = os.path.join(output_dir, "拆解文")
    os.makedirs(yuanwen_dir, exist_ok=True)
    os.makedirs(chaijie_dir, exist_ok=True)

    images_src = os.path.join(output_dir, "images")
    if os.path.isdir(images_src):
        images_dst = os.path.join(yuanwen_dir, "images")
        if os.path.exists(images_dst):
            import shutil
            shutil.rmtree(images_dst)
        os.rename(images_src, images_dst)

    for f in glob.glob(os.path.join(output_dir, "*_拆解报告.md")):
        dest = os.path.join(chaijie_dir, os.path.basename(f))
        if not os.path.isfile(dest):
            os.rename(f, dest)

    for f in glob.glob(os.path.join(output_dir, "*.md")):
        name = os.path.basename(f)
        if name.endswith("_拆解报告.md"):
            continue
        dest = os.path.join(yuanwen_dir, name)
        if not os.path.isfile(dest):
            os.rename(f, dest)

    print(f"\n{'=' * 56}")
    print(f"  目录整理完成")
    print(f"  📄 原文 → {yuanwen_dir}")
    print(f"  🧠 拆解文 → {chaijie_dir}")
    print(f"{'=' * 56}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="知识获取器 — Phase B：拆解报告生成"
    )
    parser.add_argument("path", nargs="?", help="单篇原文 .md 路径，或 --batch 时的目录路径")
    parser.add_argument("--output", "-o", default="./articles", help="拆解报告输出目录")
    parser.add_argument("--batch", action="store_true",
                        help="批量模式：处理 path 目录下所有非拆解报告的 .md 文件")
    parser.add_argument("--skip-existing", action="store_true",
                        help="跳过已有拆解报告的篇目（仅 --batch 模式有效）")
    parser.add_argument("--organize", action="store_true",
                        help="整理输出目录为 原文/ 和 拆解文/ 结构")

    args = parser.parse_args()

    if args.organize:
        organize_output(args.output)
        sys.exit(0)

    if args.batch:
        if not args.path:
            print("❌ --batch 模式需要指定原文目录路径")
            sys.exit(1)
        batch_generate(args.path, args.output, args.skip_existing)
        sys.exit(0)

    if not args.path:
        parser.print_help()
        sys.exit(1)

    if not os.path.isfile(args.path):
        print(f"❌ 文件不存在: {args.path}")
        sys.exit(1)

    if os.path.basename(args.path).endswith("_拆解报告.md"):
        print(f"⏭️ 跳过拆解报告文件: {args.path}")
        sys.exit(0)

    context = generate_report(args.path, args.output)
    print(context)
