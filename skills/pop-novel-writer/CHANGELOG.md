# CHANGELOG — pop-novel-writer

## v9.3.1 (2026-06-03)
- **name/directory 字段对齐**：`name: emergent-writer`→`pop-novel-writer`，`directory: skill-emergent-writer`→`pop-novel-writer`
- **内部旧 skill 名修复**：`skill-plot-architecture`→`pop-novel-plot`、`qa-payoff`→`pop-novel-qa`、`spec-bridge`→`pop-novel-master`
- **重复版本条目删除**：尾部重复的 `9.0.0` 条目已清理
- **书数据污染清理**：`project_init_check.py` 中 `诡异游戏` 路径替换为通用路径
- **存在意义框架**：SKILL.md 补全（来自上一轮 review）

## v9.3.0 (2026-06-03)
- 从 novel-agent-pro/skills/skill-emergent-writer 独立提升
- 修复路径引用指向新 skill 名
