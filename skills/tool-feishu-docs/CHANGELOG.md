# CHANGELOG — feishu-docs

> 版本规则：主版本.次版本.修订号
> 每次调优产生一个新版本号

---

## v2.1.0 (2026-06-14)

**根因**: Tier C v5 结构重构
**类型**: 重构
**改动**: 
- 新建 `steps/` 目录，从主工作流中提取 8 个 step 文件：
  `00-quick-ref.md`, `01-token.md`, `02-doc-crud.md`, `03-comments.md`,
  `04-folders.md`, `05-permissions.md`, `06-bitable.md`, `07-markdown-import.md`。
- SKILL.md 从 426 行瘦身至 111 行。红线转为 `| # | 红线 |` 表格。
- 新增 Drop Check 表。
- 核心流程区指向 `steps/` 文件。
- `skill.json`：新增 `pipeline` 字段，版本号升至 2.1.0。
- 逻辑内容无变化。
**效果**: 结构标准化，SKILL.md 加载更轻量。

## v2.0.0 (2026-06-02)

**根因**: —（初始版本记录）
**类型**: —
**改动**: 当前稳定版本。飞书文档集成与操作。
**效果**: —
