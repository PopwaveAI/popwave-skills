---
name: pop-shared-skill-create
description: "当用户要求创建/改造/评估/审计 Popwave Skill 时启用。四个模式：A 设计、B 改造、C 评估、D 会话审计。"
---

# pop-shared-skill-create

> Popwave Skill 全生命周期规范引擎。四模式：A 设计 → B 改造 → C 评估 → D 会话审计。

## ❌ 质量红线（路由层）

| # | 红线 |
|:-:|:-----|
| ❌1 | **读取 skill 文件禁止用 Read 工具** — 用 `skill_view` 或 `Get-Content -Encoding UTF8 -Raw`，Read 有行数限制会截断 |
| ❌2 | **创建必须双文件** — SKILL.md + skill.json 缺一不可 |
| ❌3 | **改造不读全文不动手** — 先读完整 SKILL.md + skill.json + CHANGELOG，输出扫描报告 |
| ❌4 | **评估不改代码，改造不改逻辑，审计不直接改 skill** |

## 速查表（全文件目录引导）

| 我要 | 读什么文件 | 什么时候读 | 产出 |
|:-----|:----------|:----------|:-----|
| 创建新 skill | `steps/step-1-design.md` | 用户说"创建/新建/加个 skill" | SKILL.md + skill.json 骨架 |
| 改造存量 skill | `steps/step-2-refactor.md` | 用户说"改造/修复/重写 skill" | 改造后文件 + 审计报告 |
| 跨 skill 边界审计 | `references/cross-skill-audit.md` | 改造完一个 skill 后，检查相邻 skill 边界 | 8 条边界检查通过 |
| 评估 skill | `steps/step-3-evaluate.md` | 用户说"评估/打分/review" | 8 维评分卡 + 改进建议 |
| 审计 skill 执行数据 | `steps/step-4-session-audit.md` | 用户说"审计/数据驱动分析" | 审计报告 |
| 查 state.db 表结构 | `references/session-data-guide.md` | D 模式首次连接 DB 时 | — |
| 查 PRD 写作规范 | `references/prd-specification.md` | 写审计报告时 | — |
| 查 toolCall 膨胀根因 | `references/toolcall-bloat-analysis.md` | 审计发现膨胀问题时 | — |

## 核心流程

1. **路由** — 从速查表匹配模式，加载对应 step 文件
2. **改造前置** — Mode B 先输出扫描报告（结构/越界/膨胀/缺口），通过后进 step-2-refactor
3. **改造后置** — 改造完成后执行 `references/cross-skill-audit.md`（8 条边界检查），确认相邻 skill 未破坏
4. **验收** — 按 step 文件的落盘检查点逐项验证

## 读取协议（所有文件读取强制执行）

```
工具选择：skill_view（首选）或 Get-Content -Encoding UTF8 -Raw
❌ 禁止用 Read 工具读取 skill 文件（有行数限制，会截断）

截断检测：
1. 读取后对比 content.length vs (Get-Item '{path}').Length
2. content.length < file_size × 0.9 → ⚠️ 截断警告
3. 回退 Get-Content -Encoding UTF8 -Raw 重读
4. 连续 2 次不过 → 终止，告知用户
```

## 版本

v5.5.0 | 2026-06-23 | 新增 ❌D19/D20：瘦身不重复 + 注意力预算原则 → [CHANGELOG.md](CHANGELOG.md)
