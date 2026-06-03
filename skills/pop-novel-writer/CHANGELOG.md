# CHANGELOG — pop-novel-writer

## v9.3.1 (2026-06-03)
- **P0-1: 补齐 glue/ 模块**：创建 `glue/project_config.py`，解决 `post_write.py`/`pre_flight.py`/`validate.py`/`main.py`/`check_db.py` 的 `from glue.project_config import ...` 断链
- **P0-2: 修复 main.py 三条错误路径**：glue import（3-level→1-level）、knowledge-base 路径（`skills/`→`pop-novel-writer/`）、template-pools 路径（从项目根上三层→自身目录）
- **P0-3: 清除旧路径硬编码**：`project_init_check.py`（9处）、`update_project_status.py`（15处 skill 名+路径）、`update_global_summary.py`（docstring）中的 `novel-agent-pro/skills/skill-emergent-writer` 引用全部替换
- **name/directory 字段对齐**：`name: emergent-writer`→`pop-novel-writer`，`directory: skill-emergent-writer`→`pop-novel-writer`
- **内部旧 skill 名修复**：`skill-plot-architecture`→`pop-novel-plot`、`qa-payoff`→`pop-novel-qa`、`spec-bridge`→`pop-novel-master`
- **重复版本条目删除**：尾部重复的 `9.0.0` 条目已清理
- **书数据污染清理**：`project_init_check.py` 中 `诡异游戏` 路径替换为通用路径
- **存在意义框架**：SKILL.md 补全（来自上一轮 review）

## v9.3.0 (2026-06-03)
- 从 novel-agent-pro/skills/skill-emergent-writer 独立提升
- 修复路径引用指向新 skill 名
