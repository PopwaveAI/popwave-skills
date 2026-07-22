---
name: pop-decon-design-pack
description: "当用户说'拆书/提取设计包/ETL拆分/白描卡'时启用。双模式：precision(v4设计包3层+1区) / fast(瘦身白描卡4段式，DS API并发)。产出供下游volume/setting消费。"
---

# pop-decon-design-pack · 章节设计包

> Phase 1 of 拆书管线。双模式逐章提取设计包，不跨章聚合。v6.1.0

## 做什么

| 输入 | 输出 | 下游 |
|:-----|:-----|:-----|
| 源文件（TXT/EPUB） | precision: 设计包v4 / fast: 瘦身白描卡 | pop-decon-volume, pop-decon-prd |

### 双模式

| 模式 | execution.mode | 格式 | 单章字数 | 压缩比 | 适用场景 |
|:-----|:-------------|:-----|:---------|:------:|:---------|
| 精度模式 | `precision`（默认） | v4 设计包（3层+1区） | 1-2K | 80-100% | 精品拆书/拆书为写/prose-render |
| 快速模式 | `fast` | 瘦身白描卡（4段式） | 150-400 | ~11% | 大规模拆书/快速验证/全书骨架 |

**模式选择**：章数 > 100 且不需要 prose-render 直接消费 → fast；否则 precision。

## 怎么操作

> execution.mode: precision/fast | 强保障：本 SKILL.md 由 host 层每次 run 强制注入 | 弱保障：steps/ + references/ 需 agent 主动 readFile

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 0 | 源文件获取 | `{书名}.txt` | 无源文件→退回 | `steps/step-0-source-acquire.md` |
| 1 | ETL+拆分 | `_temp/chapters/chXXX.txt` | 章数不匹配→退回 | `steps/step-1-etl-split.md` |
| 2 | 逐章提取（双模式） | precision: `设计包v4/chXXX.md` / fast: `白描卡/chXXX.md` | 结构完整 | `steps/step-2-batch-process.md` |
| 3 | 验证（双模式） | 验证报告 | 全覆盖 | `steps/step-3-verify.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. 源文件+ETL前置缺失 — 未获取源文件/未ETL/未按章拆分 → 退回
3. 凭空发明内容 — beat链/事件白描中出现原文不存在的内容 → 退回
4. 精度模式锚点缺失 — 每beat必须有scene+POV+关键对白/数据(🔒)+感官锚点
5. 结构不完整 — precision: 3层+1区全部小节; fast: 事件白描+关键数据+爽点钩子三段必须存在

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-0-source-acquire.md` | Step 0 源文件获取时 | 源文件获取流程 |
| `steps/step-1-etl-split.md` | Step 1 按章拆分时 | ETL+拆分流程 |
| `steps/step-2-batch-process.md` | Step 2 提取设计包时 | 逐章提取流程（双模式） |
| `steps/step-3-verify.md` | Step 3 验证产出时 | 验证流程（双模式） |
| `references/设计包v3-格式规范.md` | 精度模式理解设计包格式时 | v4格式规范（precision） |
| `references/slim-card-format-spec.md` | 快速模式理解白描卡格式时 | 瘦身白描卡格式规范（fast） |
| `references/v3-format-quick-reference.md` | 嵌入delegate_task context时 | v4格式快照 |
| `references/precision-anchor-format.md` | 理解scene/POV/🔒/感官锚点时 | 精度锚点格式 |
| `references/chinese-novel-etl.md` | 中文TXT拆分时 | 中文网文ETL |
| `references/batch-scaling.md` | ≥50章并行提取时 | 批量提取策略 |
| `references/token-budget-delegate.md` | delegate_task上下文预算时 | token预算指南 |
| `references/post-hoc-format-normalization.md` | 首行格式漂移修复时 | 格式归一化 |
| `references/cn-novel-format-injection-failure.md` | 多批次格式不一致时 | 格式注入失败案例 |
| `templates/fact-skeleton.md` | precision模式产出时 | v4设计包模板 |
| `templates/slim-card-template.md` | fast模式产出时 | 瘦身白描卡模板 |
| `scripts/normalize-headlines-from-source.py` | 首行格式修复时 | 标题归一化脚本 |
| `scripts/slim_card_batch.py` | fast模式批量处理时 | DS API并发脚本 |

## 版本

v6.1.0 | 2026-07-22 | 按规范重写 SKILL.md：补全做什么/怎么操作/强弱加载声明，合并双速查表为文件目录引导，版本只留最新 → [CHANGELOG.md](CHANGELOG.md)
