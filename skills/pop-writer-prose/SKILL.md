---
name: pop-writer-prose
description: 正文渲染，文风DNA硬阻塞+场景流渲染+情感内省允许
pipeline:
  upstream: [pop-writer-chapter]
  downstream: [pop-writer-qa]
  references: [pop-trope-library]
version: 2.0.0
---

# 正文渲染

正文渲染阶段：文风DNA缺失即硬阻塞终止，按场景流渲染（非逐事件），允许关键决策点的内心活动。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 文风DNA缺失→硬阻塞终止 | 不降级不A/B，空=终止 |
| ❌2 | 场景流渲染 | 非逐事件渲染，按场景流包 |
| ❌3 | 80%展示+20%内省 | 允许关键决策点的内心活动 |

## ⚠️ 步骤加载门禁

进入本skill前，必须确认chapter产物齐全（场景流设计包）且文风DNA已锁定。缺产物=阻塞。

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-render.md | 场景流渲染（DNA硬阻塞+场景流+80/20内省） |
| step-2 | steps/step-2-verify.md | 输出验证（AI观感词+DNA匹配度+字数） |

## 路由

upstream `pop-writer-chapter` → **本skill** → downstream `pop-writer-qa`

## 产出

- 正文（场景流渲染）
- 渲染验证报告（文风DNA匹配度）

## 与v1的差异

文风DNA缺失改为硬阻塞（不降级不A/B），渲染按场景流而非逐事件，允许20%情感内省。

---
v2.0.0 | 2026-06-25 | v2骨架创建 — 