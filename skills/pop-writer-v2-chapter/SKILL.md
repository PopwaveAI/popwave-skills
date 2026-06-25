---
name: pop-writer-v2-chapter
description: v2管线·场景设计，场景流设计包（导演指令式，≤8K字）
pipeline:
  upstream: [pop-writer-v2-plot]
  downstream: [pop-writer-v2-prose]
  references: [pop-trope-library]
version: 1.0.0
---

# v2-章节设计

章节设计阶段：以导演指令式产出场景流设计包，3-5场景/章，DQTC决策溯源独立附录。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 设计包≤8K字 | 导演指令式，非逐事件填表 |
| ❌2 | 场景流设计 | 3-5场景/章，非逐事件 |
| ❌3 | DQTC决策溯源附录独立 | 不膨胀主设计包 |

## ⚠️ 步骤加载门禁

进入本skill前，必须确认plot产物齐全（卷大纲+章节锚点）。缺产物=阻塞。

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-read-canvas.md | 读取章锚点+角色卡+state-log |
| step-2 | steps/step-2-scene-design.md | 场景流设计（导演指令式，3-5场景/章） |
| step-3 | steps/step-3-polish.md | 润色（爽点+情绪弧线+章末钩子） |
| step-4 | steps/step-4-output.md | 落盘+state-log更新+DQTC附录 |

## 路由

upstream `pop-writer-v2-plot` → **本skill** → downstream `pop-writer-v2-prose`

## 产出

- 场景流设计包（≤8K字，导演指令式）
- DQTC决策溯源附录（独立文件）

## 与v1的差异

用场景流设计包替代逐事件填表，导演指令式控制篇幅≤8K字，DQTC附录独立。

---
v1.0.0 | 2026-06-25 | v2骨架创建 — AB测试用
