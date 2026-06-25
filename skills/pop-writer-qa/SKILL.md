---
name: pop-writer-qa
description: 质检，密度/多样性/温度量化检查
pipeline:
  upstream: [pop-writer-prose]
  downstream: []
  references: [pop-trope-library]
version: 2.0.0
---

# 质检

质检阶段：对正文进行密度量化、多样性量化、温度量化三项检查，产出质检报告。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 密度量化 | 每章≥8事件，每3章≥1情绪闭环 |
| ❌2 | 多样性量化 | 每幕危机≥3系统，无连续3章同源 |
| ❌3 | 温度量化 | 文风DNA匹配度≥80% |

## ⚠️ 步骤加载门禁

进入本skill前，必须确认prose产物齐全（正文+渲染验证报告）。缺产物=阻塞。

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-quantitative.md | 量化检查（密度/多样性/温度） |
| step-2 | steps/step-2-qualitative.md | 定性检查+修复建议 |

## 路由

upstream `pop-writer-prose` → **本skill** → downstream（管线终点）

## 产出

- 质检报告（密度/多样性/温度三项量化）
- 不合格项修复建议

## 与v1的差异

质检从定性升级为量化：密度（≥8事件/章）、多样性（≥3系统/幕）、温度（DNA匹配度≥80%）。

---
v2.0.0 | 2026-06-25 | v2骨架创建 — 