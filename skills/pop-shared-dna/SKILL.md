---
name: pop-shared-dna
description: 文风DNA蒸馏引擎。当用户说'提取文风''文风DNA''风格蒸馏''分析作者笔触'时启用。从原文按场景类型提取笔触→产出prose-render可对照的场景参考文件。
---
# pop-shared-dna
> 文风DNA蒸馏引擎 v4.2.0。从原文中按场景类型提取作者笔触，产出不是分析报告而是参考页。

## 做什么
| 输入 | 来源 | 输出 | 下游 |
|------|------|------|------|
| 全书原文 | pop-decon | 写作资产/文风库/{书名}.md（20-30K） | pop-writer-prose, pop-writer-v3-revise |

5级结构定位：文风DNA是横切辅助层，为L1设计包scene字段提供笔触参考。

## 怎么操作（SOP骨架）
> execution.mode: 顺序执行Step 0→4，Step 3门禁不通过退回Step 0扩采。
> 强加载：红线+速查表（每轮必读）；弱加载：steps/references/templates按步骤按需加载。

### Step 0: 取样 → `steps/step-0-sampling.md`
- 全书扫描，采样≥30章≥20,000行；不够退回（短章书走混合策略）

### Step 1: 逐章精读 → `steps/step-1-close-reading.md`
- 采样章全文阅读，标记场景类型+候选原文段

### Step 2: 全书搜索验证 → `steps/step-2-verify.md`
- 全书搜索验证Step 1的判断

### Step 3: 写风格文件 → `steps/step-3-write.md`
- 产出`写作资产/文风库/{书名}.md`（≥6场景卡+≥4通用维度+时间演变段）；门禁不通过退回Step 0

### Step 4: 试写验证 → `steps/step-4-trial.md`
- 2组300字对比稿+差异分析

## 红线
1. **读取协议**：强加载=红线+速查表（每轮必读）；弱加载=steps/references/templates按步骤按需加载。Step 3门禁不通过时退回Step 0。
2. **原文<500字** — 任何维度/场景卡原文<500字 → 退回扩采
3. **场景卡<6个或通用维度<4个** — 覆盖不足 → 退回
4. **无时间演变段** — 不知早期/末期差异的文风认知是残废的 → 退回
5. **降级替换** — 场景卡原文与scene类型不严格对应（如boss战塞设定说明）→ 退回扩采
6. **产出只留摘要未执行** — 写入文件后必须报告摘要，不得在对话中粘贴完整风格文件

## 速查表
| 文件 | 读取时机 | 核心内容 |
|------|----------|----------|
| SKILL.md | 每轮必读 | 红线+SOP骨架+速查表 |
| steps/step-0-sampling.md | Step 0执行时 | 取样策略+门禁（≥30章≥20,000行） |
| steps/step-1-close-reading.md | Step 1执行时 | 逐章精读+场景类型标记 |
| steps/step-2-verify.md | Step 2执行时 | 全书搜索验证方法 |
| steps/step-3-write.md | Step 3执行时 | 风格文件写法+最终门禁 |
| steps/step-4-trial.md | Step 4执行时 | 试写验证+差异分析 |
| references/methodology.md | 需要方法论时 | 文风分析方法论 |
| references/short-chapter-sampling.md | 短章书时 | 混合采样策略（30章精读+全文搜索） |
| templates/style-dna-profile.md | Step 3写文件时 | v4模板（场景卡+通用维度+时间演变） |

## 版本
v4.2.0 | 2026-07-22 | SKILL.md按设计规范重写：frontmatter补触发条件、红线重构为6条(首条读取协议)、速查表改为文件目录引导、版本历史移至CHANGELOG。
