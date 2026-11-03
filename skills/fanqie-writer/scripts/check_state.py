#!/usr/bin/env python3
"""项目状态检查：必备文件、状态.md 的下一步、正文与章日志配套、快照存在。

用法：
  python check_state.py --project <项目目录>

任何 FAIL 时以退出码 1 结束。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def read(path: Path) -> str | None:
    return path.read_text(encoding="utf-8").strip() if path.is_file() else None


def chapter_files(folder: Path) -> dict[str, Path]:
    if not folder.is_dir():
        return {}
    return {path.stem: path for path in sorted(folder.glob("ch*.md"))}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    checks: list[tuple[str, str, str]] = []

    def add(name: str, status: str, detail: str) -> None:
        checks.append((name, status, detail))

    required = {
        "用户约束.md": project / "用户约束.md",
        "立项/00-卖点卡.md": project / "立项" / "00-卖点卡.md",
        "立项/01-立项卡.md": project / "立项" / "01-立项卡.md",
        "状态.md": project / "状态.md",
    }
    for label, path in required.items():
        if path.is_file() and read(path):
            add(label, "PASS", "存在")
        else:
            add(label, "FAIL", "不存在或为空")

    status_text = read(project / "状态.md") or ""
    if status_text:
        for field in ("已完成", "下一步", "更新时间"):
            add(f"状态字段 {field}", "PASS" if f"{field}" in status_text else "FAIL", "已写" if field in status_text else "缺失")
        next_match = re.search(r"下一步[：:]\s*(.*)", status_text)
        if next_match:
            next_line = next_match.group(1)
            task = re.search(r"T[1-7]", next_line)
            if not task:
                add("下一步任务号", "FAIL", f"未找到 T1-T7：{next_line}")
            else:
                add("下一步任务号", "PASS", task.group(0))
                chapter = re.search(r"ch(\d{3})", next_line)
                if task.group(0) in {"T5", "T6"} and not chapter:
                    add("下一步章号", "FAIL", f"{task.group(0)} 必须带 chNNN：{next_line}")
                elif chapter:
                    outline = project / "章纲" / f"{chapter.group(0)}.md"
                    if task.group(0) in {"T5", "T6"} and not outline.is_file():
                        add("下一步章纲", "FAIL", f"{outline.name} 不存在，先做 T4")
                    else:
                        add("下一步章纲", "PASS", f"{chapter.group(0)} 对应文件存在")
        else:
            add("下一步任务号", "FAIL", "状态.md 没有「下一步」行")

    bodies = chapter_files(project / "正文")
    logs = chapter_files(project / "剧情日志")
    missing_logs = sorted(set(bodies) - set(logs))
    extra_logs = sorted(set(logs) - set(bodies))
    if missing_logs:
        add("章日志配套", "FAIL", f"缺日志：{', '.join(missing_logs)}")
    else:
        add("章日志配套", "PASS", f"{len(bodies)} 章正文都有日志")
    if extra_logs:
        add("多余章日志", "WARN", f"无对应正文：{', '.join(extra_logs)}")

    if bodies:
        snapshot = read(project / "剧情快照.md")
        if snapshot and len(snapshot) > 100:
            add("剧情快照", "PASS", f"{len(snapshot)} 字符")
        else:
            add("剧情快照", "FAIL", "正文已有章节，剧情快照缺失或过短")
    else:
        add("剧情快照", "PASS", "尚无正文，允许缺失")

    failed = [item for item in checks if item[1] == "FAIL"]
    print(project)
    for name, status, detail in checks:
        print(f"[{status}] {name}：{detail}")
    print("结论：" + ("FAIL" if failed else "PASS"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
