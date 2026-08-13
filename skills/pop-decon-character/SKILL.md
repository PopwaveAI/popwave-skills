---
name: pop-decon-character
description: "当拆书时用户说'人物/角色/人设/弧线/成长'时启用。消费章节白描+剧情线(可选)→产出人物角色拆解：角色卡+弧线+动机+成长。"
---
# pop-decon-character · 人物角色拆解

> 拆书独立维度 skill。从章节白描拆解人物角色：角色卡 + 弧线 + 动机 + 成长。v1.1.0

## 做什么

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 章节白描（必）+ 剧情线（可选） | pop-decon-design-pack / pop-decon-plot | `设计/角色/主要角色人物卡.md`、`设计/角色/角色弧线.md` | pop-decon-prd、创作参考 |

## 怎么操作

> execution.mode: 串行 | 强保障：本 SKILL.md 每次 run 强制注入 | 弱保障：steps/ 需 agent 主动读取

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 1 | 角色人物卡 | `主要角色人物卡` | 每卡有原文chXX证据 | `steps/step-1-character-cards.md` |
| 2 | 角色弧线 | `角色弧线` | 每弧线有状态/心态/触发事件 | `steps/step-2-character-arc.md` |
| 3 | 角色对白风格库 | `角色对白风格库` | 逐字摘录原文对白 | `steps/step-3-dialogue-style.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **无白描就拆** — 必须先有章节白描，角色拆解不得直接读原文
3. **凭空发明角色设定** — 无chXX证据且未标注「数据极少」的角色信息=编造
4. **弧线无状态变化** — 角色弧线必须覆盖起点→终点，标注心态/状态/触发事件
5. **对白风格凭空描述** — 对白风格必须逐字摘录原文，不得概括"他说话很酷"

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-character-cards.md` | Step 1 | 角色人物卡（含敌人卡） |
| `steps/step-2-character-arc.md` | Step 2 | 角色弧线（状态/心态/触发事件） |
| `steps/step-3-dialogue-style.md` | Step 3 | 角色对白风格库 |
| `references/pipeline-context.md` | 需要管线上下文时 | 维度skill在拆书体系的位置 |

## 版本

v1.1.0 | 2026-08-13 | skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步 → [CHANGELOG.md](CHANGELOG.md)