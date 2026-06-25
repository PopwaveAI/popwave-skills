---
name: pop-writer-plot
description: 剧情架构，危机交叉设计+事件密度基准+情绪闭环检查
pipeline:
  upstream: [pop-writer-character]
  downstream: [pop-writer-chapter]
  references: [pop-trope-library]
version: 2.0.0
---

# 剧情架构

剧情架构阶段：危机交叉设计确保多样性，事件密度基准保证节奏，情绪闭环检查保证体验完整。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 每章≥8个事件 | 密度基准，逐章计数 |
| ❌2 | 每幕危机事件来自≥3个系统 | 危机多样性，来源分类 |
| ❌3 | 每3章≥1个完整情绪闭环 | 情绪弧线校验 |
| ❌4 | 角色卡缺失→硬阻塞 | plot需要角色弧线作为输入 |

## ⚠️ 步骤加载门禁

进入本skill前，必须确认character产物齐全（角色卡+弧线+关系网）。缺产物=阻塞。

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-volume-strategy.md | 卷战略+危机系统分配 |
| step-2 | steps/step-2-crisis-design.md | 危机交叉设计（≥3系统/幕） |
| step-3 | steps/step-3-plotline.md | 剧情线文档（L3/L2+金手指任务驱动） |
| step-4 | steps/step-4-act-plan.md | 分幕+章锚点（事件密度+情绪闭环标注） |
| step-5 | steps/step-5-density-audit.md | 事件密度+情绪闭环检查 |

## 路由

upstream `pop-writer-character` → **本skill** → downstream `pop-writer-chapter`

## 产出

- 卷大纲（含危机交叉设计）
- 章节锚点（事件密度+情绪闭环标注）
- 剧情线文档

## 与v1的差异

引入危机交叉设计、事件密度基准（≥8/章）和情绪闭环检查（每3章≥1闭环）。

---
v2.0.0 | 2026-06-25 | v2骨架创建 — 