# CHANGELOG — pop-novel-qa

## v0.5.0 (2026-06-04)
- **完整重构 SKILL.md**：
  - 精简 frontmatter 为仅 name+description（3 行），description 采用触发条件格式
  - 新增「❌ 质量红线（开工前→完工后自检）」—— 7 项逐项自检 checkbox，违反标记 REJECT
  - 新增「什么时候用」+「前置条件」表格
  - 三层介入重新编号为 Step 1/2/3（扁平化结构）
  - Spec 合规备注层保留为可选追加
  - 新增「❌ 错误示例」—— 2 个 WRONG 区块（越界给建议、打分排名）
  - 新增「异常与边界条件」表 —— 7 种场景及处理方式
  - 新增「输出说明」—— QC 报告不做存档
  - 版本标记更新为 v0.5.0
- **skill.json 更新**：
  - 从 frontmatter 迁移元数据：category、scenario、mode、recommended、tags、fidelity、novelAgentVersion、orchestration、produces、directory
  - version 升级至 0.5.0
  - description 对齐新格式
  - activation.slashCommands 新增「审一下」「爽点质检」
- **CHANGELOG.md 更新**：新增 v0.5.0 完整记录

## v0.4.2 (2026-06-03)
- **name/directory 字段对齐**：`name: qa-payoff` → `pop-novel-qa`，`directory: skill-qa-payoff` → `pop-novel-qa`

## v0.4.1 (2026-06-03)
- 从 novel-agent-pro/skills/skill-qa-payoff 独立提升
