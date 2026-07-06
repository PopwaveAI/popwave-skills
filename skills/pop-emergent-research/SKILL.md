---
name: pop-emergent-research
description: "当用户说'找燃料/补燃料/题材机制/涌现式research'时启用。找能入场面的燃料和题材机制，产出 research-写作燃料.md 和 content-mechanics.md，不写正文不排章纲。"
---

# pop-emergent-research

> 找能入场面的燃料和题材机制，不写正文不排章纲。

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | 读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具（有行数限制会截断） |
| ❌2 | 创建必须双文件 SKILL.md + skill.json |
| ❌3 | 版本三处一致（SKILL.md + skill.json + CHANGELOG） |
| ❌4 | 不写正文、不排章纲 |
| ❌5 | 燃料必须落到事件形状 + 主角操作点 + 可外显爽点 |
| ❌6 | content-mechanics.md 必须落盘带元数据（owner=research，见 PRD §4.2） |
| ❌7 | 不把内容机制伪装成文风特征交给 soul/write |

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 找燃料 + 题材机制分流 | `steps/step-1-find.md` | 进入本 skill 第一步 |
| 落盘燃料 + 机制文档 | `steps/step-2-output.md` | step-1 门禁通过后 |
| 填燃料文档 | `templates/fuel-doc.tpl.md` | step-2 落盘前 |
| 填机制文档 | `templates/mechanics-doc.tpl.md` | step-2 落盘前 |
| 查契约层（骨架/owner/命名/mode/回复格式） | `../pop-emergent/references/v3.5-pipeline-prd.md` | 对齐 PRD §4 时 |

## execution.mode

引用 PRD §4.5，不在此重复定义三档表。本 skill 的 formal 必读输入：已读 seed/临时 seed；燃料不少于 3 条；主燃料有事件形状/主角操作点/可外显爽点。三档切换条件见 PRD §4.5。

## 回复格式

采用 PRD §4.7 统一回复格式（本次采用 skill / execution.mode / 专属产出摘要 / 下一步）。

## 强弱加载保障

- 强保障：本 SKILL.md 由 host 层每次 run 强制注入，100% 到达
- 弱保障：steps/templates 需 agent 按速查表主动 readFile，天然弱保障
- 关键约束已在红线中自包含，不依赖"agent 会去读 step 文件"

## 版本

v3.5.0 | 2026-07-06 | 四层架构对齐 + content-mechanics 正式落盘 → [CHANGELOG.md](CHANGELOG.md)
