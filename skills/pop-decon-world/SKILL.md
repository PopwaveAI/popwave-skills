---
name: pop-decon-world
description: "当拆书时用户说'世界观/设定/地理/势力/历史/物种/物品'时启用。消费章节白描+力量体系(可选)→产出世界观拆解：地理+历史+物种+势力+物品。"
---
# pop-decon-world · 世界观拆解

> 拆书独立维度 skill。从章节白描拆解世界观：地理蓝图 + 历史驱动力 + 物种天赋 + 势力格局 + 资源物品。v1.0.0

## 做什么

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 章节白描（必）+ 力量体系（可选） | pop-decon-design-pack / pop-decon-power | `设计/世界观/` 系列 | pop-decon-prd、创作参考 |

## 怎么操作

> execution.mode: 骨架优先，血肉可并行 | 强保障：本 SKILL.md 每次 run 强制注入 | 弱保障：steps/ 需 agent 主动读取

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 1 | 地理蓝图 | `地理蓝图` | 骨架锚点：力量层级空间投影 | `steps/step-1-geography.md` |
| 2 | 历史与驱动力 | `历史与驱动力` | 骨架锚点：力量体系历史演化 | `steps/step-2-history.md` |
| 3 | 势力格局 | `势力格局` | 骨架锚点：势力力量层级定位 | `steps/step-3-factions.md` |
| 4 | 物种与天赋 | `物种与天赋` | 有chXX证据 | `steps/step-4-species.md` |
| 5 | 资源与物品 | `资源与物品` | 有chXX证据 | `steps/step-5-items.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **无白描就拆** — 必须先有章节白描，世界观不得直接读原文
3. **凭空发明设定** — 无chXX证据且未标注「数据极少」的名称/体系=编造
4. **前N章产出全书级文件** — 文件名不得含"全书"，必须有scope声明
5. **正文内联chXX** — 正文中不得出现内联章节号，证据归表格列或段落末尾证据行

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-geography.md` | Step 1 | 地理蓝图 + 骨架锚点 |
| `steps/step-2-history.md` | Step 2 | 历史驱动力 + 骨架锚点 |
| `steps/step-3-factions.md` | Step 3 | 势力格局 + 骨架锚点 |
| `steps/step-4-species.md` | Step 4 | 物种与天赋 |
| `steps/step-5-items.md` | Step 5 | 资源与物品 |
| `references/pipeline-context.md` | 需要管线上下文时 | 维度skill在拆书体系的位置 |

## 版本

v1.0.0 | 2026-08-06 | 新建：世界观独立拆解维度 skill，从 pop-decon-setting 拆分 → [CHANGELOG.md](CHANGELOG.md)