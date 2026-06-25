---
name: pop-writer-creative
description: 立项+生态调研，生态图谱替代域DNA，文风DNA立项锁定，金手指行动引擎
pipeline:
  upstream: [pop-decon]
  downstream: [pop-writer-world, pop-writer-character, pop-writer-plot]
  references: [pop-trope-library]
version: 2.0.0
---

# 创意研究

立项阶段：从拆书输入推导创意决策，产出生态图谱、金手指行动引擎、文风DNA锁定。PRD写创意决策不写施工图。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 文风DNA未锁定→硬阻塞 | 扫描写作资产/文风库/，空=终止 |
| ❌2 | 金手指必须含≥1个行动驱动机制 | 任务/技能/经验/血量/战宠 |
| ❌3 | 生态图谱≥3个角色群 | 替代域DNA摘要 |
| ❌4 | PRD写创意决策不写施工图 | 决策导向，非执行细节 |

## ⚠️ 步骤加载门禁

进入本skill前，必须确认上游产物齐全。缺产物=阻塞，不降级执行。

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-ecology.md | 生态图谱调研 |
| step-2 | steps/step-2-golden-finger.md | 金手指行动引擎设计 |
| step-3 | steps/step-3-dna-lock.md | 文风DNA锁定 |
| step-4 | steps/step-4-prd.md | 立项PRD产出 |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 1 生态调研 | `references/生态调研SOP.md` | 角色群调研标准流程 |
| Step 2 金手指设计 | `references/金手指设计指南.md` | 5维度行动引擎设计规范+数值风格声明 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 1 产出生态图谱 | `templates/生态图谱-模板.md` | 角色群清单+5字段+交叉点 |
| Step 2 产出行动引擎 | `templates/金手指行动引擎-模板.md` | 5维度表+剧情驱动+数值风格 |
| Step 3 产出锁定声明 | `templates/文风DNA锁定声明-模板.md` | 5维度拆解+硬锁定 |
| Step 4 产出PRD | `templates/立项PRD-模板.md` | 创意决策版PRD |

## 路由

upstream `pop-decon` → **本skill** → downstream `pop-writer-world` / `pop-writer-character` / `pop-writer-plot`

## 产出

- PRD（创意决策版）
- 生态图谱（≥3角色群）
- 金手指行动引擎卡
- 文风DNA锁定声明

## 与v1的差异

生态图谱替代域DNA摘要，文风DNA在立项阶段硬锁定，金手指必须行动驱动。

---
v2.0.0 | 2026-06-25 | v2骨架创建 — 