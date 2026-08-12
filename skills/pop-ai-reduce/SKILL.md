---
name: pop-ai-reduce
description: "当用户说'降AI/去AI味/降朱雀/润色网文'时启用。18技法+比例框架+节奏规划，优先子Agent→超时降级主Agent快速模式。"
---

# pop-ai-reduce · 网文降 AI 检测率

> v4.1.0 | 18 技法按比例框架分配 + 深度区集中走神 + 三级降级梯子
>
> ⚠️ **路由规则**：用户说"降AI/去AI味/降朱雀/润色"→ 默认走本 Skill。如果用户明确说"快速降AI味"或"表层降噪"→ 路由到 `pop-ai-reduce-lite`。

## 执行模式（三级降级梯子）

**优先子Agent，1次调用，不重试。**

| 级别 | 触发条件 | 执行方式 | 质量目标 |
|:---|:---|:-----|:---|
| **L1 子Agent** | 默认 | 子Agent读skill文件→Step 2a节奏规划→5步流水线→双文件输出 | 朱雀≤0.50 |
| **L2 回收** | 子Agent超时 | 检查结果是否已到达→已到则直接用 | 子Agent产出标准 |
| **L3 快速模式** | 回收失败 | 主Agent亲自执行：简化版流程，详见 `references/fallback-strategy.md` | 降幅≥20% 或 连击≤3 |

## 质量红线

| # | 红线 |
|:-:|:-----|
| 1 | **一次任务仅一章** — 严禁单次任务改写多章 |
| 2 | **读 reference 用 Get-Content -Encoding UTF8 -Raw** — Read 工具会截断 |
| 3 | **每次改写前必须先做 Step 2a 节奏比例规划** — 全文均匀走神 = 新规律 |
| 4 | **B3 联想发散只在深度区使用** — 非深度区绝对不走神 |
| 5 | **每处操作 ≥ 2 层技法** — 单技法朱雀无视 |
| 6 | **子Agent超时禁止重试** — 进回收→快速模式 |
| 7 | **快速模式禁止微调迭代** — 一次写完即交付 |

## 快速模式止损规则

| 条件 | 判定 |
|:---|:-----|
| 朱雀预估降幅 ≥ 20% 且 15-25字连击 ≤ 3 | ✅ 直接交付 |
| 降幅 < 20% 或 连击 > 5 | ⚠️ 报告中标注风险，仍交付 |
| 高频词各降 ≥ 50% | ✅ 达标 |

## 强弱加载保障

- **强保障**：本 SKILL.md 红线 + 执行模式每次 run 强制注入
- **弱保障**：`references/`、`steps/`、`templates/` 文件需 agent 主动读取

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 组装子Agent上下文 | `references/subagent-execution.md` | 主Agent收到降AI请求时 |
| 子Agent超时处理 | `references/fallback-strategy.md` | 子Agent返回超时信号时 |
| 主Agent快速模式 | `references/fallback-strategy.md` | 回收失败，主Agent亲自执行时 |
| 改写文本（含节奏规划） | `steps/pipeline-execute.md` | 子Agent/主Agent开始改写时 |
| 技法定义与比例约束 | `references/techniques.md` | Step 2a 规划前必须加载 |
| 输出格式与位置 | `templates/rewrite-output.md` | 生成输出文件时 |

## 版本

v4.1.0 | 2026-08-12 | 18技法+比例框架+节奏规划+深度区集中走神 → [CHANGELOG.md](CHANGELOG.md)
