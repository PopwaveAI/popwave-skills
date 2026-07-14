# CHANGELOG

## v4.0.0 - 2026-07-14

### 番茄覆盖替换
- SKILL.md 替换为番茄小说创作 skill 群的 seed 内容：故事基底构建器（种子阶段+世界展开阶段双链路）。
- 新增 frontmatter（name: pop-emergent-seed）。
- SOP 部分新增 execution.mode 三档说明（formal/draft/trial）。
- templates/ 新增世界圣经-模板.md、主角引擎-模板.md、角色储备池-模板.md（番茄 seed 原始模板）。
- 保留 steps/ 目录（step-1-collide.md, step-2-lock.md）。
- skill.json 版本升至 4.0.0，description 更新为番茄 seed 描述。

## v3.5.0 - 2026-07-06

### 重构：四层架构对齐
- SKILL.md 重写为 ≤60 行入口文件，删除自有 execution.mode 三档表，改引 PRD §4.5。
- skill.json 补全 version/displayName/entry/activation/permissions 字段。
- 新增 steps/step-1-collide.md：碰撞 idea + 候选 PK + 推荐方案 + 门禁。
- 新增 steps/step-2-lock.md：锁定种子 + 落盘 seed-种子文档.md + 落盘 soul.md 首版。
- 新增 templates/seed-doc.tpl.md：seed 文档空模板（含元数据块 + 章节结构）。
- 新增 templates/soul.tpl.md：soul 空模板（含元数据块 + 9 项必填字段）。

### 核心修复（问题 1）
- soul.md 由"草案"升级为"首版正式落盘"：step-2 中 seed 正式写入 涌现/soul.md，带元数据（doc_type: soul, read_policy: full-required, primary_consumer: write）+ 9 项必填字段。owner=seed 见 PRD §4.2。

### 契约对齐
- 骨架/owner/命名/execution.mode/回复格式引用 PRD §4（../pop-emergent/references/v3.5-pipeline-prd.md）。
- 版本三处一致：SKILL.md + skill.json + CHANGELOG.md = 3.5.0。

## v1.1.0
- 旧版单文件 SKILL.md，含自有 execution.mode 三档表，soul 仅作"草案"段落，无四层架构。
