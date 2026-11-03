#!/usr/bin/env python3
"""按任务组装本轮任务包，只读配方列出的文件。

用法：
  python build_context.py --project <项目目录> --task T5 --chapter 12
  python build_context.py --project <项目目录> --task T1 --user-input "想写 80 年代重生"

输出：默认写 <项目目录>/任务包.md，并打印每块字数与总字数。
缺必填文件时以退出码 2 结束，不做静默降级。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BUDGETS = {"T1": 8000, "T2": 6000, "T3": 5000, "T4": 5000, "T5": 6000, "T6": 9000, "T7": 5000}
TASKS = set(BUDGETS)

FAIL_MISSING = 2


def read_text(path: Path) -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8").strip()


def block(title: str, text: str) -> str:
    return f"## {title}\n\n{text.strip()}\n"


def chapter_no(raw: str | None) -> int | None:
    if raw is None:
        return None
    match = re.search(r"\d+", raw)
    return int(match.group()) if match else None


def chapter_name(n: int) -> str:
    return f"ch{n:03d}"


def find_snapshot(project: Path) -> tuple[str | None, str]:
    text = read_text(project / "剧情快照.md")
    if text is None:
        return None, "剧情快照.md 不存在"
    return text, ""


def genre_file(skill_root: Path, setup_text: str | None) -> Path | None:
    genre = skill_root / "references" / "genre-男频年代都市重生.md"
    if not genre.is_file():
        return None
    if setup_text and any(word in setup_text for word in ("年代", "都市", "重生")):
        return genre
    return None


def sell_point_summary(text: str, limit: int = 200) -> str:
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- 一句话卖点") or stripped.startswith("- 三个爽点"):
            lines.append(stripped)
        elif lines and stripped.startswith("- 第"):
            lines.append(stripped)
    summary = "\n".join(lines).strip()
    if not summary:
        summary = text.strip()
    return summary[:limit]


def prose_summary(skill_root: Path, limit: int = 1500) -> str:
    rules = read_text(skill_root / "references" / "prose-rules.md")
    if not rules:
        return ""
    match = re.search(r"<!-- prose-summary:start -->(.*?)<!-- prose-summary:end -->", rules, re.S)
    body = match.group(1) if match else rules
    body = body.replace("## 摘要（写正文时随任务包传入）", "").strip()
    return body[:limit]


def character_section(setup_text: str) -> str:
    match = re.search(r"## 人物卡.*?(?=\n## |\Z)", setup_text, re.S)
    return match.group(0).strip() if match else ""


def appearing_names(outline_text: str) -> list[str]:
    match = re.search(r"- (?:出场人物与本章状态|出场人物)[：:](.*)", outline_text)
    if not match:
        return []
    raw = match.group(1)
    names = re.split(r"[、，,；;/]", raw)
    result = []
    for item in names:
        name = item.strip().split("（")[0].split("(")[0].strip()
        if name:
            result.append(name)
    return result


def scene_characters(setup_text: str, outline_text: str) -> str:
    section = character_section(setup_text)
    if not section:
        return ""
    names = appearing_names(outline_text)
    if not names:
        return section
    lines = [line for line in section.splitlines() if any(name in line for name in names)]
    return "\n".join(lines) if lines else section


def previous_tail(project: Path, chapter: int) -> tuple[str | None, str]:
    path = project / "正文" / f"{chapter_name(chapter - 1)}.md"
    text = read_text(path)
    if text is None:
        return None, f"{path.name} 不存在（首章可忽略）"
    return f"（上一章末 {min(1000, len(text))} 字）\n{text[-1000:]}", ""


def volume_table(project: Path, chapter: int | None) -> tuple[str | None, str]:
    files = sorted((project / "卷纲").glob("*爽点表*.md")) if (project / "卷纲").is_dir() else []
    if not files:
        return None, "卷纲/*爽点表*.md 不存在"
    if chapter:
        for path in files:
            text = read_text(path) or ""
            for start, end in re.findall(r"ch(\d{3})-ch(\d{3})", text):
                if int(start) <= chapter <= int(end):
                    return text, ""
            for start, end in re.findall(r"第(\d+)-(\d+)章", text):
                if int(start) <= chapter <= int(end):
                    return text, ""
    return read_text(files[-1]) or "", f"按章节未匹配到卷爽点表，回退到 {files[-1].name}"


def batch_logs(project: Path) -> tuple[str | None, str]:
    logs = sorted((project / "剧情日志").glob("ch*.md")) if (project / "剧情日志").is_dir() else []
    if not logs:
        return None, "剧情日志/ 下没有章日志"
    selected = logs[-5:]
    text = "\n\n".join(f"### {path.name}\n{read_text(path) or ''}" for path in selected)
    return text, f"本批日志 {len(selected)} 份：{', '.join(path.name for path in selected)}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--task", required=True, choices=sorted(TASKS))
    parser.add_argument("--chapter", default=None)
    parser.add_argument("--user-input", default="")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    skill_root = Path(__file__).resolve().parent.parent
    chapter = chapter_no(args.chapter)
    task = args.task
    budget = BUDGETS[task]

    if task in {"T4", "T5", "T6"} and chapter is None:
        print("该任务需要 --chapter，例如 --chapter 12", file=sys.stderr)
        return FAIL_MISSING

    constraints = read_text(project / "用户约束.md")
    sell_point = read_text(project / "立项" / "00-卖点卡.md")
    setup = read_text(project / "立项" / "01-立项卡.md")
    snapshot, snapshot_note = find_snapshot(project)

    blocks: list[tuple[str, str, bool]] = []
    missing: list[str] = []
    warnings: list[str] = []

    if task in {"T2", "T3", "T4", "T5", "T6", "T7"}:
        if not sell_point:
            missing.append("立项/00-卖点卡.md（先做 T1）")
    if task in {"T3", "T4", "T5", "T6", "T7"}:
        if not setup:
            missing.append("立项/01-立项卡.md（先做 T2）")

    if task == "T1":
        if args.user_input:
            blocks.append(("用户本轮要求", args.user_input, False))
        if setup:
            blocks.append(("已有立项（重做卖点时参考）", setup, True))
        if sell_point:
            blocks.append(("已有卖点卡（重做时参考）", sell_point, True))
        if constraints:
            blocks.append(("用户约束", constraints, True))
        genre = genre_file(skill_root, setup)
        if genre:
            blocks.append((f"题材包（{genre.name}）", read_text(genre) or "", True))
    elif task == "T2":
        blocks.append(("卖点卡", sell_point or "", False))
        if args.user_input:
            blocks.append(("用户本轮要求", args.user_input, False))
        if setup:
            blocks.append(("已有立项（重做时参考）", setup, True))
        if constraints:
            blocks.append(("用户约束", constraints, True))
        genre = genre_file(skill_root, setup)
        if genre:
            blocks.append((f"题材包（{genre.name}）", read_text(genre) or "", True))
    elif task == "T3":
        blocks.append(("卖点卡", sell_point or "", False))
        blocks.append(("立项卡", setup or "", False))
        if constraints:
            blocks.append(("用户约束", constraints, True))
        genre = genre_file(skill_root, setup)
        if genre:
            blocks.append((f"题材包（{genre.name}）", read_text(genre) or "", True))
    elif task == "T4":
        blocks.append(("卖点摘要", sell_point_summary(sell_point or ""), False))
        blocks.append(("立项卡", setup or "", False))
        table, note = volume_table(project, chapter)
        if table:
            blocks.append(("本卷爽点表", table, False))
        else:
            warnings.append(note)
        if snapshot:
            blocks.append(("剧情快照", snapshot, False))
        else:
            warnings.append(snapshot_note)
        blocks.append(("人物卡", character_section(setup or ""), False))
        if constraints:
            blocks.append(("用户约束", constraints, True))
        summary = prose_summary(skill_root)
        if summary:
            blocks.append(("文笔规则摘要", summary, True))
    elif task == "T5":
        outline = read_text(project / "章纲" / f"{chapter_name(chapter)}.md")
        if not outline:
            missing.append(f"章纲/{chapter_name(chapter)}.md（先做 T4）")
        else:
            blocks.append(("本章章纲", outline, False))
        if snapshot:
            blocks.append(("剧情快照", snapshot, False))
        else:
            warnings.append(snapshot_note)
        tail, note = previous_tail(project, chapter)
        if tail:
            blocks.append(("上一章末尾", tail, False))
        else:
            warnings.append(note)
        blocks.append(("出场人物卡", scene_characters(setup or "", outline or ""), False))
        blocks.append(("卖点摘要", sell_point_summary(sell_point or ""), False))
        if constraints:
            blocks.append(("用户约束", constraints, True))
        summary = prose_summary(skill_root)
        if summary:
            blocks.append(("文笔规则摘要", summary, True))
    elif task == "T6":
        body = read_text(project / "正文" / f"{chapter_name(chapter)}.md")
        outline = read_text(project / "章纲" / f"{chapter_name(chapter)}.md")
        if not body:
            missing.append(f"正文/{chapter_name(chapter)}.md")
        else:
            blocks.append(("本章正文", body, False))
        if not outline:
            missing.append(f"章纲/{chapter_name(chapter)}.md")
        else:
            blocks.append(("本章章纲", outline, False))
        if snapshot:
            blocks.append(("剧情快照", snapshot, False))
        else:
            warnings.append(snapshot_note)
        blocks.append(("卖点卡", sell_point or "", False))
        if constraints:
            blocks.append(("用户约束", constraints, True))
    else:  # T7
        logs, note = batch_logs(project)
        if logs:
            blocks.append(("本批五章日志", logs, False))
        else:
            warnings.append(note)
        blocks.append(("卖点卡", sell_point or "", False))
        table, note = volume_table(project, chapter)
        if table:
            blocks.append(("本卷爽点表", table, False))
        else:
            warnings.append(note)
        if constraints:
            blocks.append(("用户约束", constraints, True))

    if missing:
        print("缺必填文件，未生成任务包：", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
        return FAIL_MISSING

    empty = [title for title, text_value, _ in blocks if not text_value.strip()]
    if empty:
        warnings.append(f"以下区块为空，已跳过：{', '.join(empty)}")
    blocks = [item for item in blocks if item[1].strip()]

    # 超预算时先丢可选块，再报错，不改写原文。
    def total(items: list[tuple[str, str, bool]]) -> int:
        return sum(len(text) for _, text, _ in items)

    kept = [item for item in blocks if not item[2]]
    for item in blocks:
        if item[2] and total(kept + [item]) <= budget:
            kept.append(item)
    dropped = [title for title, _, optional in blocks if optional and all(title != kept_title for kept_title, _, _ in kept)]
    over = total(kept)
    if over > budget:
        print(f"总字数 {over} 超过 {task} 预算 {budget}，没有自动截断。各块字数：", file=sys.stderr)
        for title, text, _ in blocks:
            print(f"- {title}: {len(text)}", file=sys.stderr)
        return FAIL_MISSING
    if dropped:
        warnings.append(f"超预算已丢弃可选块：{', '.join(dropped)}")

    header = f"# 本轮任务包 · {task}" + (f" · {chapter_name(chapter)}" if chapter else "")
    parts = [header]
    for title, text_value, _ in kept:
        parts.append(block(title, text_value))
    output = "\n".join(parts).strip() + "\n"

    out_path = Path(args.out).expanduser() if args.out else project / "任务包.md"
    out_path.write_text(output, encoding="utf-8")

    print(f"任务：{task}" + (f" {chapter_name(chapter)}" if chapter else ""))
    for title, text_value, _ in kept:
        print(f"  {title}: {len(text_value)} 字符")
    print(f"总计：{len(output)} / {budget} 字符")
    if warnings:
        print("提示：")
        for item in warnings:
            print(f"  - {item}")
    print(f"已写入：{out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
