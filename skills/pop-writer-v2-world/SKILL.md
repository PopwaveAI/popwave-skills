---
name: pop-writer-v2-world
description: v2管线·世界构筑+金手指引擎，金手指数值化以行动引擎为核心，社会结构从生态图谱推导
pipeline:
  upstream: [pop-writer-v2-creative]
  downstream: [pop-writer-v2-character]
  references: [pop-trope-library]
version: 1.0.0
---

# v2-世界构筑

世界构筑阶段：从creative继承金手指行动引擎并数值化，从生态图谱推导社会结构，产出无矛盾的世界宪法。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 金手指必须行动驱动 | 从creative继承，校验行动机制 |
| ❌2 | 社会结构从生态图谱推导 | 不凭空设计，溯源至生态图谱 |
| ❌3 | 世界宪法无自相矛盾 | 交叉校验所有宪法条款 |

## ⚠️ 步骤加载门禁

进入本skill前，必须确认creative产物齐全（PRD+生态图谱+金手指卡）。缺产物=阻塞。

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-constitution.md | 世界宪法 |
| step-2 | steps/step-2-power-system.md | 力量体系 |
| step-3 | steps/step-3-golden-finger-numeric.md | 金手指数值化 |
| step-4 | steps/step-4-social-structure.md | 社会结构 |
| step-5 | steps/step-5-verify.md | 世界观自洽校验 |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 3 金手指数值化 | `references/金手指数值化指南.md` | 5维度数值化规范+行动驱动校验 |
| Step 4 社会结构 | `references/社会结构推导SOP.md` | 从生态图谱推导社会金字塔流程 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 1 产出世界宪法 | `templates/世界宪法-模板.md` | 三类法则+溯源标注 |
| Step 3 产出数值表 | `templates/金手指数值表-模板.md` | 5维度数值+戏剧性服务点 |
| Step 4 产出金字塔 | `templates/社会结构金字塔-模板.md` | 金字塔表+溯源+流动规则 |

## 路由

upstream `pop-writer-v2-creative` → **本skill** → downstream `pop-writer-v2-character`

## 产出

- 世界蓝图（L1-01至L1-06）
- 金手指数值化引擎
- 社会结构金字塔（从生态图谱推导）
- 世界宪法（无矛盾版）

## 与v1的差异

金手指数值化以行动引擎为核心，社会结构从生态图谱推导而非凭空设计。

---
v1.0.0 | 2026-06-25 | v2骨架创建 — AB测试用
