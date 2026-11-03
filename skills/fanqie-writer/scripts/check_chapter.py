#!/usr/bin/env python3
"""单章正文检查：字数、开头、AI 高频词密度、引号、段落与钩子。

用法：
  python check_chapter.py --chapter 正文/ch012.md
  python check_chapter.py --chapter 正文/ch012.md --min 2000 --max 2500 --json

任何 FAIL 时以退出码 1 结束；只有 WARN 时退出码 0。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

AI_WORDS = [
    "心中一凛", "心头一震", "瞳孔骤缩", "倒吸一口凉气", "嘴角勾起", "眼底闪过",
    "气氛凝重", "空气凝固", "时间仿佛静止", "莫名", "说不出的",
    "然而", "与此同时", "值得一提的是", "不得不说", "显而易见", "毋庸置疑",
    "总而言之", "由此可见", "仿佛在诉说", "深深地", "缓缓地", "默默地", "微微地", "轻轻地",
    "宛如天神", "气势轰然", "深邃如渊", "嘴角的弧度",
]
OPENING_BANNED = ["天气", "早晨", "清晨", "起床", "镜子", "闹钟", "揉了揉眼睛", "上回", "上一章"]
STRAIGHT_QUOTES = ['"', "'"]


def chinese_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def paragraphs(text: str) -> list[str]:
    return [item.strip() for item in re.split(r"\n\s*\n", text) if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter", required=True)
    parser.add_argument("--min", type=int, default=2000)
    parser.add_argument("--max", type=int, default=2500)
    parser.add_argument("--max-ai", type=float, default=3.0, help="每千字允许的 AI 套话命中数")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.chapter).expanduser()
    if not path.is_file():
        print(f"文件不存在：{path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    body = re.sub(r"^#.*$", "", text, count=1, flags=re.M)
    chars = chinese_count(body)
    paras = paragraphs(body)

    checks: list[dict] = []

    def add(name: str, status: str, detail: str) -> None:
        checks.append({"check": name, "status": status, "detail": detail})

    # 1 字数
    if chars < args.min:
        add("字数", "FAIL", f"{chars} 字，低于下限 {args.min}")
    elif chars > args.max:
        add("字数", "FAIL", f"{chars} 字，超过上限 {args.max}")
    else:
        add("字数", "PASS", f"{chars} 字")

    # 2 开头
    opening = "\n".join(paras[:3])
    hits = [word for word in OPENING_BANNED if word in opening]
    if hits:
        add("开头进入变化", "FAIL", f"前三段出现禁用元素：{'、'.join(hits)}")
    else:
        add("开头进入变化", "PASS", "前三段未见天气/起床/照镜子/回顾")

    # 3 AI 套话密度
    words = [word for word in AI_WORDS if word in body]
    count = sum(body.count(word) for word in AI_WORDS)
    density = count / max(chars, 1) * 1000
    if density > args.max_ai:
        add("AI 套话密度", "FAIL", f"{count} 处 / {chars} 字 = {density:.1f}/千字，上限 {args.max_ai}")
    else:
        add("AI 套话密度", "PASS", f"{count} 处，{density:.1f}/千字" + (f"；命中：{'、'.join(words[:6])}" if words else ""))

    # 4 引号格式
    straight = sum(body.count(mark) for mark in STRAIGHT_QUOTES)
    if straight:
        add("引号格式", "FAIL", f"出现 {straight} 个英文直引号，改用中文弯引号")
    else:
        add("引号格式", "PASS", "未出现英文直引号")

    # 5 段落长度（软）
    longest = max((len(item) for item in paras), default=0)
    if longest > 500:
        add("段落长度", "WARN", f"最长一段 {longest} 字，建议拆到 300 字以内")
    else:
        add("段落长度", "PASS", f"最长一段 {longest} 字")

    # 6 章末钩子（软，启发式）
    tail = body.strip()[-200:]
    hook_marks = ["？", "?", "……", "却", "突然", "没想到", "必须", "只剩", "明天"]
    if any(mark in tail for mark in hook_marks):
        add("章末钩子", "PASS", "末尾 200 字含问题/转折/新目标信号")
    else:
        add("章末钩子", "WARN", "末尾 200 字未检出钩子信号，人工复核")

    # 7 平均句长（软）
    sentences = [item for item in re.split(r"[。！？!?]", body) if item.strip()]
    avg = sum(len(item) for item in sentences) / max(len(sentences), 1)
    if avg > 45:
        add("平均句长", "WARN", f"{avg:.0f} 字/句，偏长，拆短句")
    else:
        add("平均句长", "PASS", f"{avg:.0f} 字/句")

    # 8 对话占比（软）
    dialogue = sum(1 for line in body.splitlines() if line.strip().startswith(("「", "“")))
    ratio = dialogue / max(len(paras), 1)
    if ratio < 0.05:
        add("对话占比", "WARN", f"{ratio:.0%} 段落以对话开头，可能对话过少")
    else:
        add("对话占比", "PASS", f"{ratio:.0%} 段落以对话开头")

    failed = [item for item in checks if item["status"] == "FAIL"]
    if args.json:
        print(json.dumps({"file": str(path), "chars": chars, "checks": checks, "result": "FAIL" if failed else "PASS"}, ensure_ascii=False, indent=2))
    else:
        print(f"{path}  {chars} 字")
        for item in checks:
            print(f"[{item['status']}] {item['check']}：{item['detail']}")
        print("结论：" + ("FAIL" if failed else "PASS"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
