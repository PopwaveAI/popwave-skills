---
name: pop-decon-beat
description: "当拆书时用户说'爽点/名场面/读者体验/节奏/爽点分布'时启用。消费章节白描+剧情线(可选)→产出爽点体验拆解：名场面库+读者体验曲线+爽点分布。"
---
# pop-decon-beat · 爽点体验拆解

> 拆书独立维度 skill。从章节白描拆解爽点体验：名场面库 + 读者体验曲线 + 爽点分布。v1.1.0

## 做什么

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 章节白描（必）+ 剧情线（可选） | pop-decon-design-pack / pop-decon-plot | `设计/名场面库.md`、`设计/读者体验曲线-卷N.md` | pop-decon-prd、创作参考 |

## 怎么操作

> execution.mode: 串行 | 强保障：本 SKILL.md 每次 run 强制注入 | 弱保障：steps/ 需 agent 主动读取

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 1 | 名场面深度拆解 | `名场面库.md` | 叙事式拆解有原文锚点 | `steps/step-1-iconic-scenes.md` |
| 2 | 读者体验曲线 | `读者体验曲线-卷N.md` | 爽点分布覆盖全部章节 | `steps/step-2-reader-experience.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **无白描就拆** — 必须先有章节白描，爽点拆解不得直接读原文
3. **前置铺垫必须标注具体chXX** — 不得只写"前面有铺垫"，必须列出章号
4. **爽感必须点出公式** — 弱→强/被欺→反击/未知→揭示/压力→突破，不得只写"很爽"
5. **名场面叙事式拆解不拆表格** — 产出是自然叙事文，不是维度表

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-iconic-scenes.md` | Step 1 | 名场面深度拆解 |
| `steps/step-2-reader-experience.md` | Step 2 | 读者体验曲线 + 爽点分布 |
| `references/pipeline-context.md` | 需要管线上下文时 | 维度skill在拆书体系的位置 |

## 版本

v1.1.0 | 2026-08-13 | skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步 → [CHANGELOG.md](CHANGELOG.md)