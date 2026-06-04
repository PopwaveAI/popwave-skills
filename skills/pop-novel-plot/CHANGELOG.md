# CHANGELOG — pop-novel-plot

## v2.8.0 (2026-06-03)
- **场景卡改为交互闸门**：不再是产出步骤，改为幕纲设计完成后写1段中爽点试读输出给老板确认
- **SKILL.md 重写"交互闸门·场景卡试读"section**：流程/写哪一段/格式/用途全部更新
- **frontmatter 同步**：produces 从"爽点版场景卡（归档）"改为"场景卡试读（不归档）"，tags 新增"交互闸门"
- **管线图更新**：步骤名由"爽点版场景卡"改为"交互闸门·场景卡试读"

## v2.7.1 (2026-06-03)
- **name/directory 字段对齐**：`name: plot-architecture`→`pop-novel-plot`，`directory: skill-plot-architecture`→`pop-novel-plot`
- **路径引用修复**：`glue/check_db.py`→`scripts/check_db.py`、`glue/validate.py`→`scripts/validate.py`、`skills/_shared/`→`skills/pop-novel-master/_shared/`
- **书数据污染清理**：`沈渊降临渊界，激活铭牌`→`主角穿越异界，激活金手指`
- **旧 skill 名修复**：`emergent-writer`→`pop-novel-writer`、`skill-plot-architecture`→`pop-novel-plot`

## v2.7.0 (2026-06-03)
- 从 novel-agent-pro/skills/skill-plot-architecture 独立提升
- 修复路径引用（glue/ → scripts/，_shared/ → pop-novel-master/_shared/）
