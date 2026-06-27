---
name: pop-writer-v3-qa
description: 涌现写作质检子skill。context隔离，五问反思引用正文证据+种子生长判断+爽点终验+主角行为一致性终验。
pipeline:
  upstream: [pop-writer-v3-revise]
  downstream: [pop-writer-v3-emerge]
version: 1.0.0
---

# 质检子skill

> 由 pop-writer-v3-emerge Step 4 调度，context隔离。

v3.2管线涌现写作的质检子skill。做4项任务：五问反思（每问须引用正文证据）、种子生长判断、爽点终验、主角行为一致性终验。context隔离消除自我审视偏差——质检子skill拿到的是修订稿（不知道创作过程），只看正文质量，判断更客观。

## 红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| 1 | 质检不通过=回退重写本章 | 五问任一不达标 或 行为一致性终验❌ 或 爽点终验任一❌，回退create/revise子skill |
| 2 | context隔离——传入精简context，不传会话历史 | emerge调度时只传该步骤所需最小context |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-qa.md | 五问反思+种子生长判断+爽点终验+主角行为一致性终验 |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 爽点终验 | `references/网文爽感机制.md` | 10条法则终验标准 |
| step-1 种子生长判断 | `references/活种子生长触发规则.md` | 生长场景+判断原则+版本管理 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 质检产出 | `templates/质检报告-模板.md` | 五问反思+种子生长判断+爽点终验+行为一致性终验+回退目标 |

## 输入/输出契约

- **输入：** 修订稿+活记忆+种子/（冲突轴+压力矩阵+主角引擎）+网文法则+质检模板
- **输出：** 质检报告+通过/不通过+回退目标

## 路由

upstream `pop-writer-v3-revise`（修订子skill，产出修订稿） → **本skill** → downstream `pop-writer-v3-emerge`（调度器，Step 5机械执行记忆更新）

**调度架构：** 本skill由emerge调度器Step 4调用，context隔离——只接收精简context（修订稿+活记忆+种子+网文法则+质检模板），不接收会话历史、创作决策记录、修订记录、文风DNA。质检完成后返回质检报告+通过/不通过+回退目标给emerge调度器。

---

v1.0.0 | 2026-06-26 | 从pop-writer-v3-emerge v1.2.0拆分出质检子skill；新增主角行为一致性终验维度；context隔离红线（红线❌2）；自包含网文爽感机制.md和活种子生长触发规则.md副本
