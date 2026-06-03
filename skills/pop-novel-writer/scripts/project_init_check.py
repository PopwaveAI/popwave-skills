#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
project_init_check.py — 项目初始化检查 & 引导

职责：
  检测项目当前准备状态，判断用户处于哪个场景，
  输出清晰的下步操作指引。

使用方式（在任何写作步骤前运行）：
  python scripts/project_init_check.py --project-dir "E:\project\your-novel"

输出：
  - 当前项目阶段判定
  - 缺失资料清单
  - 下步操作建议（含命令示例）
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def _check_exists(path: Path) -> str:
    """返回文件/目录状态图标"""
    if path.exists():
        return "✅"
    return "❌"


def _count_files(directory: Path, pattern: str = None) -> int:
    """统计目录中匹配的文件数"""
    if not directory.exists():
        return 0
    if pattern:
        import fnmatch
        return len([f for f in directory.iterdir() if f.is_file() and fnmatch.fnmatch(f.name, pattern)])
    return len([f for f in directory.iterdir() if f.is_file()])


def _find_latest_chapter(directory: Path) -> int | None:
    """扫描章节目录，找最大章节号"""
    if not directory.exists():
        return None
    max_num = 0
    for f in directory.iterdir():
        if not f.is_file():
            continue
        m = re.search(r'(?:ch|chapter[_\s]?|第)?0*(\d+)', f.stem)
        if m:
            num = int(m.group(1))
            max_num = max(max_num, num)
    return max_num if max_num > 0 else None


def main():
    parser = argparse.ArgumentParser(description="项目初始化检查 & 引导")
    parser.add_argument("--project-dir", "-p", required=True, help="项目根目录")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细文件清单")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    if not project_dir.exists():
        print(f"\n❌ 项目目录不存在: {project_dir}")
        print("   请确认路径正确，或先运行 skill-project-bootstrap 创建项目骨架。")
        sys.exit(1)

    print("=" * 60)
    print(f"  novel-agent v2.0 — 项目初始化检查")
    print(f"  项目: {project_dir.name}")
    print(f"  路径: {project_dir}")
    print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # ── Step 1: 检查项目骨架 ─────────────────────
    print("\n┌─ 一、项目骨架 ──────────────────────────┐")
    has_bootstrap = project_dir.joinpath("project.yaml").exists()
    has_l1 = project_dir.joinpath("00-原始设定", "L1-元设定层").exists()
    has_chapter_outlines = project_dir.joinpath("02-章纲").exists()
    has_chapter_dir = project_dir.joinpath("02-章纲").exists()

    print(f"  {_check_exists(project_dir / 'project.yaml')}  project.yaml（项目定义文件）")
    print(f"  {_check_exists(project_dir / '00-原始设定')}  00-原始设定/（L0-L3设定层）")
    print(f"  {_check_exists(project_dir / '02-章纲')}  02-章纲/（章纲目录）")
    print(f"  {_check_exists(project_dir / '03-正文')}  03-正文/（正文目录）")

    has_any_chapter = False
    chapter_dir_candidates = []
    for dirname in ["03-正文", "正文当前", "正文", "chapters"]:
        d = project_dir / dirname
        if d.exists():
            chapter_dir_candidates.append(d)
            file_count = _count_files(d, "*.md") + _count_files(d, "*.txt")
            if file_count > 0:
                has_any_chapter = True

    # ── Step 2: 检查全局摘要 & 角色状态 ──────────
    print("\n┌─ 二、写作基础设施 ──────────────────────┐")
    has_global_summary = project_dir.joinpath("02-章纲", "global-summary.md")
    has_state_anchor = project_dir.joinpath("02-章纲", "character-state-anchor.md")
    has_pipeline_state = project_dir.joinpath("_pipeline_state.json")

    print(f"  {_check_exists(has_global_summary)}  02-章纲/global-summary.md（全局摘要）")
    print(f"  {_check_exists(has_state_anchor)}  02-章纲/character-state-anchor.md（角色状态锚）")
    print(f"  {_check_exists(has_pipeline_state)}  _pipeline_state.json（管线进度）")

    # 检测已有章节（扫描常见目录）
    latest_chapter = None
    for d in chapter_dir_candidates:
        lc = _find_latest_chapter(d)
        if lc and (latest_chapter is None or lc > latest_chapter):
            latest_chapter = lc
            latest_chapter_dir = d

    if latest_chapter:
        print(f"  📖 已有章节: CH01 ~ CH{latest_chapter:02d}（位于 {latest_chapter_dir.name}/）")
    else:
        print(f"  📖 已有章节: 未检测到（新书将从 CH01 开始）")

    # ── Step 2.5: 检查 project-status.html ────────
    has_status_html = project_dir.joinpath("project-status.html").exists()
    print(f"  {_check_exists(has_status_html)}  project-status.html（项目总控台）" if not has_status_html 
          else f"  {_check_exists(has_status_html)}  project-status.html（项目总控台，可刷新）")

    # ── Step 3: 场景判定 ─────────────────────────
    print("\n┌─ 三、场景判定 ──────────────────────────┐")

    if not has_bootstrap:
        scenario = "new_project"
        print(f"\n  🆕 场景A：从零开新书")
        print(f"  ─────────────────────────────────────")
        print(f"  项目尚未初始化。需要先创建项目骨架和元设定。")
        print(f"")
        print(f"  下步操作:")
        print(f"    1. 运行 skill-project-bootstrap 创建项目")
        print(f"    2. 完成后刷新项目总控台：")
        print(f"       python <novel-agent-pro>/skills/skill-emergent-writer/scripts/update_project_status.py --project-dir \"{project_dir}\"")
        print(f"    3. 运行 skill-plot-architecture 设计剧情架构")
        print(f"    4. 运行 skill-chapter-outline 生成章纲")
        print(f"    5. 运行 skill-emergent-writer 开始写作")
        print(f"")
        print(f"  命令示例:")
        print(f"    # 请在你的 Agent 会话中调用对应的 skill 命令")

    elif not has_any_chapter:
        scenario = "new_but_no_chapters"
        print(f"\n  📋 场景B：项目已创建，尚未写正文")
        print(f"  ─────────────────────────────────────")
        print(f"  骨架已就绪，直接进入写作循环即可。")
        print(f"  写完第一章通过 QC 后，运行 update_global_summary.py 初始化摘要。")
        print(f"")
        print(f"  下步操作:")
        print(f"    1. 刷新项目总控台（了解全貌）：")
        print(f"       python <novel-agent-pro>/skills/skill-emergent-writer/scripts/update_project_status.py --project-dir \"{project_dir}\"")
        print(f"    2. 编写第一章正文")
        print(f"    3. 通过 QC 质检")
        print(f"    4. 运行更新摘要（单章模式）:")
        print(f"       python scripts/update_global_summary.py ^")
        print(f"           --project-dir \"{project_dir}\" ^")
        print(f"           --chapter 1 ^")
        print(f"           --chapter-file \"03-正文/ch001.md\"")
        print(f"    5. 再次刷新总控台：")
        print(f"       python <novel-agent-pro>/skills/skill-emergent-writer/scripts/update_project_status.py --project-dir \"{project_dir}\"")

    elif latest_chapter and not has_global_summary.exists():
        scenario = "mid_project_no_summary"
        print(f"\n  🔄 场景C：已有 {latest_chapter} 章正文，全局摘要未初始化")
        print(f"  ─────────────────────────────────────")
        print(f"  检测到已有章节但无全局摘要。需要批量初始化后再继续写作。")
        print(f"")
        print(f"  下步操作:")
        print(f"    运行批量初始化:")
        print(f"       python scripts/update_global_summary.py ^")
        print(f"           --project-dir \"{project_dir}\" ^")
        print(f"           --batch-init ^")
        print(f"           --chapters-dir \"{latest_chapter_dir.name}\" ^")
        print(f"           --max-chapter {latest_chapter}")
        print(f"")
        print(f"    刷新总控台：")
        print(f"       python <novel-agent-pro>/skills/skill-emergent-writer/scripts/update_project_status.py --project-dir \"{project_dir}\"")
        print(f"")
        print(f"    完成后即可进入正常写作循环。")

    elif latest_chapter and has_global_summary.exists():
        scenario = "normal"
        print(f"\n  ✅ 场景D：正常写作循环中")
        print(f"  ─────────────────────────────────────")
        print(f"  所有基础设施就绪。当前进展到 CH{latest_chapter:02d}。")
        print(f"  如需继续，直接进入导演层 → 碎片写作 → QC 循环。")
        print(f"  写完新章后运行单章更新。")

    else:
        scenario = "unknown"
        print(f"\n  ❓ 场景无法判定")
        print(f"  项目结构不标准，请手动检查。")

    # ── Step 4: 缺失清单汇总 ─────────────────────
    print("\n┌─ 四、缺失资料清单 ─────────────────────┐")
    missing = []
    if not has_bootstrap:
        missing.append("project.yaml（项目定义文件）")
    if not has_l1:
        missing.append("00-原始设定/L1-元设定层/（核心元设定）")
    if not has_global_summary.exists() and has_any_chapter:
        missing.append("02-章纲/global-summary.md（全局摘要 — 可批量初始化）")
    if not has_state_anchor.exists() and has_any_chapter:
        missing.append("02-章纲/character-state-anchor.md（角色状态锚 — 可批量初始化）")
    if not has_chapter_outlines and not has_any_chapter:
        missing.append("02-章纲/（章纲 — 需先设计剧情架构）")
    if not chapter_dir_candidates and not has_bootstrap:
        missing.append("03-正文/（正文目录 — 需先创建项目骨架）")

    if missing:
        for item in missing:
            print(f"  ⬜ {item}")
    else:
        print(f"  ✅ 无缺失资料，项目已就绪。")

    # ── 结尾 ─────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  场景: {scenario}")
    print(f"  建议: ", end="")
    if scenario == "new_project":
        print("运行 skill-project-bootstrap 开始。")
    elif scenario == "new_but_no_chapters":
        print("刷新总控台 → 直接进入写作循环。")
    elif scenario == "mid_project_no_summary":
        print("先运行 --batch-init 初始化摘要，再进入写作循环。")
    elif scenario == "normal":
        print("继续写作循环。记得每章 QC 通过后刷新总控台。")
    elif scenario == "unknown":
        print("请手动检查项目结构。")
    print()
    print(f"  💡 随时刷新 project-status.html 仪表盘：")
    print(f"     python <novel-agent-pro>/skills/skill-emergent-writer/scripts/update_project_status.py --project-dir \"{project_dir}\"")
    print("=" * 60)


if __name__ == "__main__":
    main()
