---
name: pop-shared-skill-create
description: "当用户说'创建skill/新建skill/加个skill/改造skill/修复skill/重写skill/skill规范'时启用。Popwave Skill 设计规范——SOP骨架/资源分层/scripts代码目录/精简原则/强弱加载保障。"
---

# pop-shared-skill-create

> Popwave Skill 设计规范。不是工具，是规范——告诉 agent "skill 该写成什么样、该按什么顺序落盘"。

## 这个 Skill 做什么

用于创建、改造、修复 Popwave Skill。输出不是泛泛建议，而是可落盘的 Skill 文件结构：`SKILL.md`、`skill.json`、`CHANGELOG.md`，以及按需存在的 `steps/`、`references/`、`templates/`、`scripts/`。

## 怎么运作

1. **确认职责**：先确认 skill 名称、触发场景、核心产物、下游消费者；若用户已给 PRD 或现有 skill，直接以它为源材料。
2. **抽象骨架**：做"换皮测试"，抽掉具体项目名后仍可复用的流程才写进 skill；一次性案例或纯资料查询不强行 skill 化。
3. **规划结构**：`SKILL.md` 写完整 SOP 骨架和红线；复杂步骤进 `steps/`；方法论进 `references/`；可复制产物进 `templates/`；可执行代码进 `scripts/`。
4. **落盘实现**：新建或更新 `SKILL.md` + `skill.json` + `CHANGELOG.md`，按需创建一级资源目录；改造旧 skill 时只改结构、格式、门禁和规范，不擅自改业务方法论。
5. **一致性校验**：检查 description 触发条件、版本三处一致、速查表覆盖全文件、弱保障文件都有读取时机，涉及代码时验证 `scripts/` 的代表性脚本可运行。

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **读取 skill 文件禁止用 Read 工具** — 用 `skill_view` 或 `Get-Content -Encoding UTF8 -Raw`，Read 有行数限制会截断 |
| ❌2 | **创建必须双文件** — SKILL.md + skill.json 缺一不可 |
| ❌3 | **SKILL.md 必须自带 SOP 骨架** — 不能只放路由表；即使 steps/references 没读到，agent 也要知道完整流程 |
| ❌4 | **版本三处一致** — SKILL.md 正文 + skill.json + CHANGELOG.md 版本号必须一致 |
| ❌5 | **代码必须进一级 `scripts/`** — 可执行脚本、工具代码、批处理逻辑不放在 references/templates 根下 |
| ❌6 | **红线≤7条** — 只有违反后会断裂下游的才叫红线，格式细节降级为检查清单 |

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 查 skill 设计规范全文 | `steps/step-1-design.md` | 创建/改造 skill 时必读 |

## 强弱加载保障

- **强保障**：本 SKILL.md 由 host 层每次 run 强制注入，100% 到达 agent 上下文
- **弱保障**：`steps/step-1-design.md` 需 agent 按 SKILL.md 指引主动 readFile，天然弱保障
- **设计原则**：设计 SKILL.md 时假设 step 文件可能没被读到，核心 SOP 骨架和断裂级红线必须在 SKILL.md 自包含

## 版本

v6.1.0 | 2026-07-09 | 对齐知识工程 PRD：SKILL.md 承载 SOP 骨架，补充一级代码目录 scripts/ → [CHANGELOG.md](CHANGELOG.md)
