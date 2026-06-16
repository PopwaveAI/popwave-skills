---
name: pop-shared-skill-create
description: "当用户要求创建/改造/评估/审计 Popwave Skill 时启用。四个模式：A 设计（创建新 skill）、B 改造（存量改造）、C 评估（Review）、D 会话审计（从 state.db 数据驱动分析）。"
---

# pop-shared-skill-create · 设计 · 改造 · 评估 · 会话审计 v4.1

> **定位：创建/改造/评估/会话驱动审计 Popwave Skill 的规范引擎。**
> 四个模式：A 设计（新手）、B 改造（存量）、C 评估（Review）、**D 会话审计（数据驱动）**。
> **核心约束：评估不改代码，改造不改逻辑内容，创建必须走 Q&A 流程。会话审计不直接改 skill，产出改进建议供 B 模式消费。**

---

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **创建即强制双文件** — SKILL.md + skill.json。缺失 → 退回补建 |
| ❌2 | **改造不读全文不动手** — 不读完目标 SKILL.md 全文+红线扫描 → 不动手改 |
| ❌3 | **评估不跑测试不评分** — 维度 8（实测表现）不设计测试 prompt 不跑 → 评分无效 |
| ❌4 | **创建不给 description 写触发式 → 退回** — 必须"当用户说…时启用" |
| ❌5 | **改造后不更新 CHANGELOG+版本号 → 退回** — 版本 +1，CHANGELOG 追加 |
| ❌6 | **评估不打全 8 分维度 → 评分卡残缺** — 缺一个维度就标注 Not Rated |
| ❌7 | **会话审计不查 state.db → 无效** — 只读 SKILL.md 不查执行数据等于无证据审计 |
| ❌8 | **审计只找问题不给数据支撑 → 退回** — 每条发现必须有 state.db 数据行/列/大小的定量证据 |

---

## 速查表

| 我要 | 走什么模式 | 前置条件 | 产出 |
|:-----|:---------|:---------|:-----|
| 创建新 skill | **A 设计模式** | 用户提供了 skill 名称和简要职责 | SKILL.md + skill.json 骨架 |
| 改造/修复存量 skill | **B 改造模式** | 目标 skill 的 SKILL.md 可读 | 改造后的 SKILL.md + 对比报告 |
| 评估/Review skill | **C 评估模式** | 目标 skill 完整文件（含 CHANGELOG） | 8 维评分卡 + 改进建议 |
| **从执行数据审计 skill 问题** | **D 会话审计模式** | 目标 session_id + 可读 state.db | 审计报告（含数据证据 + 改进提案） |

---

## 核心流程

### 步骤 1：设计模式（创建新 skill）
详细指令 → `steps/step-1-design.md`

### 步骤 2：改造模式（改造存量 skill）
详细指令 → `steps/step-2-refactor.md`

### 步骤 3：评估模式（Review 存量 skill）
详细指令 → `steps/step-3-evaluate.md`

### 步骤 4：会话审计模式（数据驱动分析）★NEW
**做什么：** 从 state.db 读取真实会话数据，分析 agent 执行行为与 SKILL.md 要求的偏差，将 agent 违反的红线、工具使用模式、上下文膨胀等量化为证据，产出改进建议供 B 模式消费。
**❌ 门禁：** state.db 不可读或会话未找到 → 终止。无定量数据支撑的发现 → 退回补充证据。

详细指令 → `steps/step-4-session-audit.md`

---

## ❌ WRONG 示例

> ❌ 创建 skill 时只写 SKILL.md 不写 skill.json → 平台无法注册机器元数据
> ✅ 双文件结构强制：SKILL.md + skill.json 同时创建

> ❌ 改造 skill 时不读完整文件，扫一眼前几行就动手 → 遗漏正文中的重要方法论
> ✅ 先 Read 全文，输出红线扫描报告交用户确认后，再执行改造

> ❌ 评估 skill 时不打维度 8 实测 → 评分卡缺 25% 权重，结论不可信
> ✅ 每个维度必须打分，维度 8 子 agent 不可用时退化为干跑验证（标注 dry_run）

> ❌ 会话审计只看 assistant.content 不看 assistant.tool_calls → 漏掉 72% 的膨胀源
> ✅ assistant.content（对话正文）和 assistant.tool_calls（工具调用参数）分别分析。tool_calls 才是写操作的主战场

> ❌ 会话审计只读几条消息就下结论 → 样本偏差导致误判
> ✅ 全量读取目标 session 的所有消息，按阶段分组分析，每条结论标注数据来源 msg_id

---

## 边界条件

| 场景 | 触发条件 | 处理 |
|:-----|:---------|:-----|
| 目标 SKILL.md 不存在（改造/评估） | 读取目标时文件未找到 | 提示用户确认路径。不捏造，不自动切到其他文件 |
| 子 agent 不可用（评估维度 8） | — | 降级为干跑验证，标注 dry_run |
| 用户中途改模式（评估→改造） | 评估中用户要求直接改 | 暂停评估，输出已完成部分，用户确认后再切 |
| 多 skill 同时要求改造 | 用户列出多个 | 逐个出扫描报告，用户逐个确认后执行 |
| skill.json 缺失（创建） | 新建时 skill.json 不存在 | 必须补建。不能只有 SKILL.md |
| CHANGELOG 缺失（改造） | 改造目标无 CHANGELOG.md | 创建空的 CHANGELOG.md，在改造末尾追加 |
| state.db 不可读（审计） | DB 文件不存在或无权限 | 提示用户确认 HERMES_HOME 路径和 DB 文件位置 |
| 会话审计报告与已知 PRD 冲突 | 审计发现与已有 PRD 文档不一致 | 交叉引用已有 PRD，标注"与已有 PRD 同步"或"已有修复未落地" |

---

## 落盘检查点

| 确认项 | 状态 |
|:-------|:----:|
| `{skill-id}/SKILL.md` 已写入 | [ ] |
| `{skill-id}/skill.json` 已写入（含 pipeline 字段） | [ ] |
| `{skill-id}/CHANGELOG.md` 已写入 | [ ] |
| `{skill-id}/steps/` 目录存在（含至少 1 个 step 文件） | [ ] |
| `{skill-id}/templates/` 存在（产文件型 skill） | [ ] |
| `{skill-id}/references/` 存在（需方法论支撑的 skill） | [ ] |
| `{skill-id}/examples/` 存在（如有范例数据） | [ ] |
| 会话审计报告已归档到 `prd/02-问题诊断/` | [ ] |

---

## 与 expert-writer 的关系

| 维度 | expert-writer | pop-shared-skill-create |
|:-----|:-------------|:-----------------|
| 定位 | 写作管线的元 skill（调度） | Skill 全生命周期的规范工具 + 数据驱动审计 |
| 触发 | 创作/拆书/修改正文 | 创建/改造/评估/审计 skill 本身 |
| 重叠 | 无——expert-writer 不涉及 skill 创建和审计 |

## 参考资料索引

| 文件 | 用途 | 什么时候读 |
|:-----|:------|:----------|
| `references/step-4-session-audit.md` | 会话审计模式执行步骤 | 走 D 模式时 |
| `references/session-data-guide.md` | state.db 数据架构说明 | 首次连接 DB 时 |
| `references/prd-specification.md` | PRD 文档写作规范 | 创建/改造后写报告时 |
| `references/toolcall-bloat-analysis.md` | toolCall payload 膨胀根因分析 | 审计发现膨胀问题时 |

## 版本

v4.2.0 | 2026-06-15 | 新增 `references/prd-specification.md` PRD 写作规范参考 + `references/toolcall-bloat-analysis.md` 膨胀分析参考 + 参考资料索引表 → [CHANGELOG.md](CHANGELOG.md)
