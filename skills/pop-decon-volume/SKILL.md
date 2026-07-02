---
name: pop-decon-volume
description: "当用户说'聚类/卷幕/cluster'时启用。从设计包提取L2单元卡+卷纲（含溯源燃料台），产出供下游setting/prd消费。"
---

# pop-decon-volume · 叙事结构提取

> Phase 2 of 拆书管线。从设计包提取L2剧情单元卡+卷纲（含溯源燃料台），不直接产出文件。

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **读取 skill 文件禁止用 Read 工具** — 用 `Get-Content -Encoding UTF8 -Raw`，Read 有行数限制会截断 |
| ❌2 | **Phase 1 未完成就聚类** — 设计包v4/为空或不完整 → 退回 |
| ❌3 | **L2卡无原文证据** — 每个L2单元卡的结构分析必须基于设计包事件链 |
| ❌4 | **卷纲缺溯源燃料台** — 卷纲必须包含剧情/设定/创意/质感四类溯源 |

## 强弱加载保障

- **强保障**：本 SKILL.md 由 host 层每次 run 强制注入
- **弱保障**：`steps/` + `references/` 需 agent 按 SKILL.md 指引主动 readFile

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 查L2单元卡识别流程 | `steps/step-1-plot-units.md` | 识别L2剧情单元时 |
| 查卷纲归纳流程 | `steps/step-2-plotlines.md` | 归纳卷纲+燃料台时 |
| 查跨卷主题线追踪 | `steps/step-3-saga.md` | 追踪跨卷长线时 |
| 查入库流程 | `steps/step-4-intake.md` | L2卡+卷纲入库时 |
| 查管线上下文 | `references/pipeline-context.md` | 理解Phase间消费关系时 |
| 查跨卷边界处理 | `references/跨卷边界处理.md` | 多卷拆解时 |
| 填L2卡模板 | `templates/L2-剧情单元卡.tpl.md` | 产出L2单元卡时 |
| 填卷纲模板 | `templates/卷纲-拆书版.tpl.md` | 产出卷纲时 |

## 速查表（步骤）

| 步骤 | 操作 | 产出 | 门禁 |
|:-----|:-----|:-----|:-----|
| 1 | L2单元卡识别 | `L2-{编号}.md` | 每卡有结构分析+嵌套子线 |
| 2 | 卷纲归纳 | `卷纲.md`（含燃料台） | 4类溯源完整 |
| 3 | 跨卷主题线 | `跨卷主题线.yaml` | 每线有置信度标注 |
| 4 | 入库确认 | pop-trope-library四库 | L2≥3条+卷纲≥1份 |

## 版本

v5.0.0 | 2026-07-01 | 删除套路聚合步骤+按v6.0.0规范重构 → [CHANGELOG.md](CHANGELOG.md)
