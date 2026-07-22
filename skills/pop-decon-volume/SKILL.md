---
name: pop-decon-volume
description: "当用户说'聚类/卷幕/cluster'时启用。从白描卡产出叙事白描→L2单元卡+卷纲（含溯源燃料台+叙事技法分析），产出供下游setting/prd消费。"
---

# pop-decon-volume · 叙事结构提取

> Phase 2 of 拆书管线。从白描卡产出叙事白描→L2剧情单元卡+卷纲（含溯源燃料台+叙事技法分析）。v7.1.0

## 做什么

| 输入 | 输出 | 下游 |
|:-----|:-----|:-----|
| 白描卡（Phase 1 产出） | 叙事白描 + L2单元卡 + 卷纲 | pop-decon-setting, pop-decon-prd |

## 怎么操作

> execution.mode: 串行 | 强保障：本 SKILL.md 由 host 层每次 run 强制注入 | 弱保障：steps/ + references/ 需 agent 主动 readFile

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 0 | 叙事白描 | 叙事白描.md | 因果链完整+卷末钩子 | `steps/step-0-叙事白描.md` |
| 1 | L2单元卡识别 | `L2-{编号}.md` | 每卡有结构分析+嵌套子线 | `steps/step-1-plot-units.md` |
| 2 | 卷纲归纳 | `卷纲.md`（含燃料台） | 4类溯源完整 | `steps/step-2-plotlines.md` |
| 3 | 跨卷主题线 | `跨卷主题线.yaml` | 每线有置信度标注 | `steps/step-3-saga.md` |
| 4 | 入库确认 | 项目本地文件夹 | L2≥3条+卷纲≥1份 | `steps/step-4-intake.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. Phase 1 未完成就聚类 — 设计包v4/为空或不完整 → 退回
3. L2卡无原文证据 — 每个L2单元卡的结构分析必须基于设计包事件链
4. 卷纲缺溯源燃料台 — 卷纲必须包含剧情/设定/创意/质感四类溯源

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-0-叙事白描.md` | 将白描卡串联为叙事白描时 | 叙事白描流程 |
| `steps/step-1-plot-units.md` | 识别L2剧情单元时 | L2单元卡识别流程 |
| `steps/step-2-plotlines.md` | 归纳卷纲+燃料台时 | 卷纲归纳流程 |
| `steps/step-3-saga.md` | 追踪跨卷长线时 | 跨卷主题线追踪 |
| `steps/step-4-intake.md` | L2卡+卷纲入库时 | 入库流程 |
| `references/pipeline-context.md` | 理解Phase间消费关系时 | 管线上下文 |
| `references/跨卷边界处理.md` | 多卷拆解时 | 跨卷边界处理 |
| `templates/L2-剧情单元卡.tpl.md` | 产出L2单元卡时 | L2卡模板 |
| `templates/卷纲-拆书版.tpl.md` | 产出卷纲时 | 卷纲模板 |

## 版本

v7.1.0 | 2026-07-22 | 按规范重写 SKILL.md：补全做什么/怎么操作/强弱加载声明，合并双速查表为文件目录引导，版本只留最新 → [CHANGELOG.md](CHANGELOG.md)
