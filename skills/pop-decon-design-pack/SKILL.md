---
name: pop-decon-design-pack
description: "当用户说'拆书/提取设计包/ETL拆分'时启用。逐章提取设计包(beat链+爽点+角色+设定区)，产出供下游volume/setting消费。"
---

# pop-decon-design-pack · 章节设计包

> Phase 1 of 拆书管线。逐章提取3层+1区设计包，不跨章聚合。

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **读取 skill 文件禁止用 Read 工具** — 用 `Get-Content -Encoding UTF8 -Raw`，Read 有行数限制会截断 |
| ❌2 | **源文件+ETL前置缺失** — 未获取源文件/未ETL/未按章拆分/中文TXT硬跑extract.py → 退回 |
| ❌3 | **凭空发明beat** — beat链中出现原文不存在的beat → 退回 |
| ❌4 | **精度锚点缺失** — 每beat必须有scene+POV+关键对白/数据(🔒)+感官锚点 |
| ❌5 | **结构不完整** — 必须包含3层+1区全部小节，beat链必须用表格格式 |

## 强弱加载保障

- **强保障**：本 SKILL.md 由 host 层每次 run 强制注入
- **弱保障**：`steps/` + `references/` 需 agent 按 SKILL.md 指引主动 readFile

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 查源文件获取流程 | `steps/step-0-source-acquire.md` | Step 0 源文件获取时 |
| 查ETL+拆分流程 | `steps/step-1-etl-split.md` | Step 1 按章拆分时 |
| 查逐章提取流程 | `steps/step-2-batch-process.md` | Step 2 提取设计包时 |
| 查验证流程 | `steps/step-3-verify.md` | Step 3 验证产出时 |
| 查v4格式规范 | `references/设计包v3-格式规范.md` | 理解设计包格式时 |
| 查v4格式快照 | `references/v3-format-quick-reference.md` | 嵌入delegate_task context时 |
| 查精度锚点格式 | `references/precision-anchor-format.md` | 理解scene/POV/🔒/感官锚点时 |
| 查中文网文ETL | `references/chinese-novel-etl.md` | 中文TXT拆分时 |
| 查批量提取策略 | `references/batch-scaling.md` | ≥50章并行提取时 |
| 查token预算指南 | `references/token-budget-delegate.md` | delegate_task上下文预算时 |
| 查格式归一化 | `references/post-hoc-format-normalization.md` | 首行格式漂移修复时 |
| 查格式注入失败案例 | `references/cn-novel-format-injection-failure.md` | 多批次格式不一致时 |
| 填设计包模板 | `templates/fact-skeleton.md` | 产出设计包时 |
| 跑标题归一化脚本 | `scripts/normalize-headlines-from-source.py` | 首行格式修复时 |

## 速查表（步骤）

| 步骤 | 操作 | 产出 | 门禁 |
|:-----|:-----|:-----|:-----|
| 0 | 源文件获取 | `{书名}.txt` | 无源文件→退回 |
| 1 | ETL+拆分 | `_temp/chapters/chXXX.txt` | 章数不匹配→退回 |
| 2 | 逐章v4提取 | `设计包v4/chXXX-设计包.md` | 3层+1区完整 |
| 3 | 验证 | 验证报告 | 全覆盖 |

## 版本

v5.0.0 | 2026-07-01 | 删除本章套路字段+按v6.0.0规范重构 → [CHANGELOG.md](CHANGELOG.md)
