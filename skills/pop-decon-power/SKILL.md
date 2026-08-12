---
name: pop-decon-power
description: "当拆书时用户说'力量/境界/战斗/升级/体系'时启用。消费章节白描→产出力量体系拆解：力量定义+升级路线+战斗体系。"
---
# pop-decon-power · 力量体系拆解

> 拆书独立维度 skill。从章节白描拆解力量体系：力量定义 + 境界金字塔 + 主角升级路线 + 战斗体系。v1.0.0

## 做什么

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 章节白描（必） | pop-decon-design-pack | `设计/力量体系.md` | pop-decon-character、pop-decon-world、pop-decon-prd |

## 怎么操作

> execution.mode: 串行 | 强保障：本 SKILL.md 每次 run 强制注入 | 弱保障：steps/ 需 agent 主动读取

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 1 | 力量体系归纳 | `力量体系` | 境界链有chXX证据 | `steps/step-1-power-system.md` |
| 2 | 主角升级路线 | `升级路线` | 覆盖起点→当前最高点 | `steps/step-2-level-roadmap.md` |
| 3 | 战斗体系 | `战斗体系` | 战斗类型标注五轴 | `steps/step-3-combat-system.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **无白描就拆** — 必须先有章节白描，力量拆解不得直接读原文
3. **凭空设计境界链** — 无chXX证据且未标注「数据极少」的境界分级=编造
4. **境界链无因果来源** — 每级境界必须有出处（升级事件/原文描述），不得自行发明
5. **战斗分析不标注战斗类型** — 战斗必须按五轴标注（作用距离/作用方式/增益方向/参与形态/节奏形态）

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-power-system.md` | Step 1 | 力量体系归纳 + 境界金字塔 |
| `steps/step-2-level-roadmap.md` | Step 2 | 主角升级路线 |
| `steps/step-3-combat-system.md` | Step 3 | 战斗体系 + 五轴标注 |
| `references/pipeline-context.md` | 需要管线上下文时 | 维度skill在拆书体系的位置 |

## 版本

v1.0.0 | 2026-08-06 | 新建：力量体系独立拆解维度 skill，从 pop-decon-setting 拆分 → [CHANGELOG.md](CHANGELOG.md)