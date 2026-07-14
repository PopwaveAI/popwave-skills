# CHANGELOG

## v1.0.0 - 2026-07-14

### 初始迁移：从番茄 plot-design 迁移
- 从番茄小说创作 skill 群的 plot-design 迁移至 pop-emergent-plot。
- SKILL.md 新增 frontmatter（name: pop-emergent-plot）。
- SOP 部分新增 execution.mode 三档说明（formal/draft/trial）。
- 施工卡交接部分由"交接给 prose-render"改为"交接给 review（由 review 压缩进 current-state.md 的'下一章硬推进'字段）"。
- 保留番茄 plot-design 全部内容不变：6道门禁/剧情白描/反拆维度/施工卡/赛道文档等。
- 目录结构完整迁移：steps/（4个文件）+ templates/（1个文件）+ references/（7个赛道文件 + 设计原则库5个文件）。
- 新增 skill.json，声明 pipeline 上下游关系（upstream: qidian-seed, downstream: pop-emergent-review）。
