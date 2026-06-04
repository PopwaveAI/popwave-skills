# CHANGELOG — pop-novel-plot

## v2.9.0 — 2026-06-04

### 完整改革（SKILL.md 全量重写）

- **frontmatter 精简**：仅保留 name + description（共 3 行），触发条件式描述对齐 skill.json
- **质量红线改为 [ ] checkbox 列表**：从 markdown 表格转为 10 条可勾选清单，附"开工前画 [ ] / 完工后改 [x]" 使用说明
- **新增"什么时候用"第 5 行**：检查现有幕纲节奏问题
- **流程保持 5 步扁平结构**：前置检查→设计幕纲→场景卡闸门→自检+校准→输出
- **新增 WRONG 4 错误示例**：用户一开口直接写多幕
- **新增「异常与边界条件」表**：12 类异常场景（act 文件缺失 / L1 未就绪 / 节点B 跳过 / 场景卡退回 / 自检失败 / 平台校准失败 / Boss 战缺阶段 / 中途换平台 / 场景卡存档冲突 / 多幕命名冲突 / 老板设计缺阶段指示 / 中途换项目），每项含触发条件 + 处理方式
- **版本行格式化为三级标题**：`## 版本 v2.9.0 | 2026-06-04 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)`
- **输出路径不变**：`设计/幕/act-XX.yaml` + `设计/幕/节奏自检报告.md`

### skill.json 同步

- version: 2.8.0 → 2.9.0
- description 对齐 frontmatter 触发条件式

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
