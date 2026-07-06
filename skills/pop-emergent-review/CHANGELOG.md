# CHANGELOG

## v3.5.0 - 2026-07-06

### 重构：四层架构对齐
- SKILL.md 重写为 ≤60 行入口文件，删除自有 execution.mode 三档表，改引 PRD §4.5。
- skill.json 补全 version/displayName/entry/activation/permissions 字段。
- 新增 steps/step-1-audit.md：审稿 6 步 SOP + 归因规则表 + 门禁。
- 新增 steps/step-2-commit.md：沉淀分流执行，归档/覆盖/沉淀职责分离。
- 新增 templates/current-state.tpl.md：current-state 空模板（元数据块 + 章节结构）。

### 核心修复（问题 9：历史层职责分离）
- current-state 更新前先归档旧版到 `涌现/压缩归档/current-state-{YYYYMMDD}-{章位}.md`，再覆盖 current-state.md。
- review-沉淀.md 改为 append-only：每次审稿在末尾追加一段，不删改历史。
- 两者不重叠：沉淀记"判断和规则"，归档存"旧版入口包全文"（见 PRD §4.4）。

### 核心修复（问题 8：燃料文件引用统一）
- 燃料文件唯一名 `research-写作燃料.md`，删除"或 燃料库.md"别名（见 PRD §4.3）。

### 契约对齐
- 骨架/owner/命名/execution.mode/回复格式引用 PRD §4（../pop-emergent/references/v3.5-pipeline-prd.md）。
- 版本三处一致：SKILL.md + skill.json + CHANGELOG.md = 3.5.0。

## v1.1.0
- 旧版单文件 SKILL.md，含自有 execution.mode 三档表、current-state 模板内联、库文件更新建议表，燃料文件出现 `燃料库.md` 别名，无四层架构，无步骤文件，无归档/沉淀职责分离。
