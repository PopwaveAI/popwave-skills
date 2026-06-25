---
name: pop-writer-character
description: 角色设计，增加生态位置/生态关系/生态冲突点字段
pipeline:
  upstream: [pop-writer-world]
  downstream: [pop-writer-plot]
  references: [pop-trope-library]
version: 2.0.0
---

# 角色设计

角色设计阶段：在v1角色卡基础上增加生态位字段，确保角色嵌入生态图谱，主角决策转折点≥3个。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 角色卡含生态位字段 | 生态位置/生态关系/生态冲突点 |
| ❌2 | 主角决策转折点≥3个 | 弧线节点校验 |
| ❌3 | 角色关系网完整 | 每个角色≥2个关系 |

## ⚠️ 步骤加载门禁

进入本skill前，必须确认world产物齐全（世界蓝图+社会结构）。缺产物=阻塞。

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-select-level.md | 角色级别选择+生态位定位 |
| step-2 | steps/step-2-write-card.md | 角色卡撰写（v1字段+生态位三字段） |
| step-3 | steps/step-3-verify.md | 角色卡校验（生态位+决策转折点+关系网） |

## 路由

upstream `pop-writer-world` → **本skill** → downstream `pop-writer-plot`

## 产出

- 角色卡（含生态位字段）
- 主角弧线（≥3决策转折点）
- 角色关系网（每角色≥2关系）

## 与v1的差异

角色卡增加生态位置/生态关系/生态冲突点字段，将角色锚定到生态图谱中。

---
v2.0.0 | 2026-06-25 | v2骨架创建 — 