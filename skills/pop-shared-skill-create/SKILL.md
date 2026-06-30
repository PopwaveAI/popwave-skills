---
name: pop-shared-skill-create
description: "当用户说'创建skill/新建skill/加个skill/改造skill/修复skill/重写skill/skill规范'时启用。Popwave Skill 设计规范——格式/内容定位/路由/精简原则/强弱加载保障。"
---

# pop-shared-skill-create

> Popwave Skill 设计规范。不是工具，是规范——告诉 agent "skill 该写成什么样"。

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **读取 skill 文件禁止用 Read 工具** — 用 `skill_view` 或 `Get-Content -Encoding UTF8 -Raw`，Read 有行数限制会截断 |
| ❌2 | **创建必须双文件** — SKILL.md + skill.json 缺一不可 |
| ❌3 | **红线≤7条** — 只有违反后会断裂下游的才叫红线，格式细节降级为检查清单 |
| ❌4 | **版本三处一致** — SKILL.md 正文 + skill.json + CHANGELOG.md 版本号必须一致 |

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 查 skill 设计规范全文 | `steps/step-1-design.md` | 创建/改造 skill 时必读 |

## 强弱加载保障

- **强保障**：本 SKILL.md 由 host 层每次 run 强制注入，100% 到达 agent 上下文
- **弱保障**：`steps/step-1-design.md` 需 agent 按 SKILL.md 指引主动 readFile，天然弱保障
- **设计原则**：设计 SKILL.md 时假设 step 文件可能没被读到，关键约束必须在 SKILL.md 红线中自包含

## 版本

v6.0.0 | 2026-07-01 | 从四模式工具重构为纯规范文档 → [CHANGELOG.md](CHANGELOG.md)
