# CHANGELOG

## v2.0.0 - 2026-07-14

### 版本升级：番茄 review 覆盖
- 番茄小说创作 skill 群覆盖替换 pop-emergent 系列。
- SKILL.md 采用番茄 review 全文（逐beat对比/gap分类/质量判断5维度/笔触审核8维度/状态快照/红线/速查表），保留全部原始内容不变。
- 新增 frontmatter（name: pop-emergent-review）。
- 新增 execution.mode 三档（formal/draft/trial）。
- 新增 current-state 更新章节（吸收自 pop-emergent 架构资产：更新规则/历史层规则/沉淀分流）。
- 保留 steps/step-2-commit.md（current-state 更新逻辑）和 templates/current-state.tpl.md（current-state 模板）。

## v3.7.0 - 2026-07-09

### 调整：章内文风DNA审计
- 审稿 SOP 从三层审计改为章内笔触和单章套路审计。
- current-state 的 `本章DNA执行包` 改为章型、笔触目标、章内套路、可见反馈、禁止误用。
- 下一章执行包禁止迁移全书架构、角色口癖、开篇专用机制和特殊高光章。

## v3.6.0 - 2026-07-08

### 新增：文风DNA三层审计
- 审稿 SOP 从 6 步升级为 7 步，新增文风DNA三层执行检查。
- 新增层1笔触、层2叙事组织、层3商业反馈、角色/口癖污染检查。
- current-state 模板新增 `本章DNA执行包`，供下一轮 write 消费。
- step-2 新增下一章DNA执行包写入规则，避免 DNA 停留在审稿建议里。

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