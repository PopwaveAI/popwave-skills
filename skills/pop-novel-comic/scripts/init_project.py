#!/usr/bin/env python3
"""
pop-novel-comic 项目初始化脚本
创建漫画项目目录结构 + 初始化记忆文件

用法:
  python init_project.py --project "{小说项目路径}" --book-name "{书名}"

 creates:
  {项目}/漫画/
  ├── assets/characters/
  ├── 漫画角色库.md
  ├── 漫画快照.md
  ├── 漫画状态.md
  └── 视觉沉淀.md
"""

import argparse
import os
import sys
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def init_project(project_path, book_name, style_anchor):
    """初始化漫画项目目录和记忆文件"""
    comic_dir = os.path.join(project_path, "漫画")
    assets_dir = os.path.join(comic_dir, "assets", "characters")

    # 创建目录
    os.makedirs(assets_dir, exist_ok=True)
    print(f"已创建目录: {comic_dir}")
    print(f"已创建目录: {assets_dir}")

    today = date.today().isoformat()

    # 漫画角色库.md（空模板）
    char_lib_path = os.path.join(comic_dir, "漫画角色库.md")
    with open(char_lib_path, "w", encoding="utf-8") as f:
        f.write(f"""# 漫画角色库

> 角色视觉资产唯一真相源。每个角色含四层结构：规格表（人读）→ 冻结提示词（API读，真相源）→ 定妆图资产（版本管理）→ 决策日志（append-only）。

## 风格锚定串（全系列冻结）

{style_anchor}

---

<!-- Phase 0 初始化时，为每个角色添加四层结构条目 -->
""")
    print(f"已创建: {char_lib_path}")

    # 漫画快照.md
    snapshot_path = os.path.join(comic_dir, "漫画快照.md")
    with open(snapshot_path, "w", encoding="utf-8") as f:
        f.write(f"""# 漫画快照

> 全书累计视图。每次 Phase 2 审核后更新（replace 模式）。跨章一致性的中期记忆。

## 基本信息

- 书名: {book_name}
- 漫画项目路径: {comic_dir}
- 创建日期: {today}

## 风格锚定串（全系列冻结）

{style_anchor}

> 风格锚定串在 Phase 0 确定后冻结，全系列所有章节共用。禁止每章重新推导。

## 角色清单

| 角色 | 最新定妆图版本 | 路径 | 出场章节 |
|:-----|:---------------|:-----|:---------|
<!-- Phase 0 初始化时填入 -->

## 已生成章节

| 章号 | 章节名 | 生成日期 | 帧数 | 图片大小 | 定妆图版本快照 |
|:-----|:-------|:---------|:-----|:---------|:---------------|
<!-- Phase 2 审核后追加 -->

## 已知视觉问题池

- （暂无）

## 角色出场记录

| 角色 | 出场章节列表 | 最近状态变化 |
|:-----|:-----------|:-------------|
<!-- Phase 2 审核后更新 -->
""")
    print(f"已创建: {snapshot_path}")

    # 漫画状态.md
    state_path = os.path.join(comic_dir, "漫画状态.md")
    with open(state_path, "w", encoding="utf-8") as f:
        f.write(f"""# 漫画状态

> 章位入口包。每次 Phase 1 开始时读取，Phase 2 结束时更新（replace 模式）。短期工作记忆。

## 当前章位

- 下一章: 第1章
- 上一章完成: 无

## 角色状态

| 角色 | 当前定妆图版本 | 当前状态 | 备注 |
|:-----|:---------------|:---------|:-----|
<!-- Phase 0 初始化时填入 -->

## 上一章问题

（首次初始化，无历史问题）

## 注意事项

- Phase 0 刚完成，第1章为首次生成
- 注意检查所有角色定妆图是否就绪

## 待处理增量定妆图

（暂无）

## 风格锚定串

{style_anchor}
""")
    print(f"已创建: {state_path}")

    # 视觉沉淀.md（空文件）
    sediment_path = os.path.join(comic_dir, "视觉沉淀.md")
    with open(sediment_path, "w", encoding="utf-8") as f:
        f.write("""# 视觉沉淀

> 每章审核结果追加至此（append-only，永不删改历史）。

""")
    print(f"已创建: {sediment_path}")

    print(f"\n{'='*60}")
    print(f"漫画项目初始化完成: {comic_dir}")
    print(f"{'='*60}")
    print(f"\n下一步: 在 Phase 0 中为每个角色生成定妆图，")
    print(f"然后将规格表+冻结提示词填入 漫画角色库.md")


def main():
    parser = argparse.ArgumentParser(description="初始化漫画项目目录结构和记忆文件")
    parser.add_argument("--project", required=True, help="小说项目根目录路径")
    parser.add_argument("--book-name", required=True, help="书名")
    parser.add_argument(
        "--style",
        default="暗黑奇幻半写实日式漫画风格，水彩质感笔触，灰暗色调，暖色火光点缀，情绪氛围浓郁",
        help="风格锚定串（全系列冻结）",
    )
    args = parser.parse_args()

    if not os.path.exists(args.project):
        print(f"错误：项目路径不存在: {args.project}", file=sys.stderr)
        sys.exit(1)

    init_project(args.project, args.book_name, args.style)


if __name__ == "__main__":
    main()
