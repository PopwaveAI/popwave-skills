---
name: pop-novel-writer
description: 正文写作引擎，3步驱动。Design(LLM/八块设计包)→Render(LLM/三阶段：风格锚定→正文渲染→风格验证)→State Update(零LLM)。v15.0 状态协议重构：章末delta单源 + entity-snapshot.yaml全量快照聚合。
---

# 正文写作引擎（v15.0）

3步管线（2次 LLM + 1次零 LLM）：

```
Step 1 — Design（LLM · 产出八块 chXXX-design.md）
  块A 设计说明 / 块B 本章空间 / 块C 登场人物 / 块D 事件链(含子节拍+反应节点)
  块E 设定嵌入表 / 块F 渲染指引 / 块G 字数预算 / 块H 上下文快照
  ★ 输出文件: 03-写作资产/chXXX-design.md（必须写入磁盘——不可只口头汇报）
  ★ 每章必须新建独立 design 文件，不得复用上一章 design
  ★ 前置必读: entity-snapshot + act-XX.yaml + canvas(人物/地图) + constitution + story-engine + L1
  ★ 硬性产出: 块A(设计说明) + 块B(本章空间) + 块C(登场人物) + 块D(事件链) + 块E(设定嵌入表)。五块缺一 → 退回。

Step 2 — Render（LLM / 三阶段）
  Phase 1：风格锚定 — 读原文片段 → 语感对齐 → 产生风格调音叉
  Phase 2：正文渲染 — 事件链强制覆盖 × 风格调音叉同步执行
  Phase 3：风格验证 — P0禁句扫描 + 调音叉对照 + 情绪弧线检查
  ★ 输出文件: 03-正文/chXXX.md
  ★ 章末必须附带 # === 状态更新 === 块（entity_updates + world_updates + event_log + style_report）

Step 3 — State Update（零 LLM）
  章末delta确认 → entity-snapshot.yaml全量快照聚合 → global-summary轻量追加
  ★ 输出文件: 00-总控/entity-snapshot.yaml（覆盖写入·从所有章 delta 聚合）
  ★ 同时更新: 03-写作资产/global-summary.md（叙事摘要·轻量追加）
```

**状态协议（v15.0 新增）：每章正文末尾的 `# === 状态更新 ===` 块是唯一写入源（delta）。entity-snapshot.yaml 是从所有章 delta 聚合的编译产物，损坏/丢失可重跑聚合恢复。路径从 project.yaml#paths 派生，不硬编码。**

核心原则：**结构正确（Design）≠ 质感正确（Render）。Design 负责空间约束、人设底线、事件节拍和设定嵌入点——Render 负责把这些变成读者读到的句子。Phase 1 不提取规则——读原文片段，用自己的语感对齐句子的质感。**

产出物供给 pop-novel-qa 管线。

---

## ❌ 质量红线

| # | 标准 | 确认 |
|:-:|:-----|:----:|
| ❌1 | **act-XX.yaml 已存在并通过节奏自检** — 无幕纲不进正文 | [ ] |
| ❌2 | **写前必读已执行** — 读 entity-snapshot + 当前幕纲 + L1 设定 | [ ] |
| ❌3 | **Design必须输出事件链+爽点链+渲染指引** — 三块缺一不可 | [ ] |
| ❌4 | **Render 必须覆盖事件链全部节点** — 每个事件必须在正文中出现 | [ ] |
| ❌5 | **风格锚定必须执行（Phase 1）** — 无调音叉不进 Phase 2 | [ ] |
| ❌6 | **风格验证 P0 项 0 违规（Phase 3）** — P0 > 0 立即修补 | [ ] |
| ❌7 | **QC 红线触发 → 退回重写** — "想跳过"≥2 或 "会弃书" 不通过 | [ ] |
| ❌8 | **State after 必须更新** — entity-snapshot.yaml 聚合 + global-summary 追加 | [ ] |
| ❌9 | **里程碑已纳入上下文** — 如 design/里程碑设计.md 存在，Design 必须读取并输出里程碑对齐块 | [ ] |
| ❌10 | **Design 文件已写入磁盘** — 03-写作资产/chXXX-design.md 存在且非空。每章独立文件，不复用上一章 | [ ] |
| ❌11 | **Entity-snapshot 已更新** — 00-总控/entity-snapshot.yaml 被覆盖写入 | [ ] |

---

## 写前必读清单

```
□ entity-snapshot.yaml → 当前全量角色状态/时间线/伏笔（状态追踪唯一canon）
□ 上一章正文末尾 # === 状态更新 === 块 → 上章未闭合节点 + 衔接点
□ 当前幕纲（act-XX.yaml）→ emotional_goal + info_release + 钩子
□ project.yaml#reader_profile → 写给谁看
□ project.yaml#paths → 章文件目录路径
□ design/里程碑设计.md → 确认本章对应哪个 MK（如有）
□ design/终点快照.md → 确认当前进度与终点距离（如有）
□ 续写/长篇小说：精读倒数20章全文 → 输出事实提取报告（闸门由 expert-writer 强制）
```

---

## 管线（3步驱动）

```
Step 1 — Design（LLM · 产出八块 chXXX-design.md）
  读 act-XX.yaml + canvas 人物/地图 + constitution + story-engine + L1设定 + entity-snapshot + 上一章delta
  产出八块：设计说明 + 本章空间 + 登场人物 + 事件链 + 设定嵌入表 + 渲染指引 + 字数预算 + 上下文快照
  输出文件：03-写作资产/chXXX-design.md
  详细指令 → steps/step-1-design.md

Step 2 — Render（LLM / 三阶段）
  Phase 1：风格锚定 — 读原文片段 → 语感对齐 → 产生风格调音叉
  Phase 2：正文渲染 — 事件链强制覆盖 × 风格调音叉同步执行
  Phase 3：风格验证 — P0禁句扫描 + 调音叉对照 + 情绪弧线检查
  输出：正文（{paths.chapters}/chXXX.md）+ 章末状态更新块（含 style_report）
  详细指令 → steps/step-2-render.md

Step 3 — State Update（零 LLM）
  确认章末delta → 聚合全部章的delta为entity-snapshot.yaml（覆盖写入）→ 追加global-summary
  详细指令 → steps/step-5-state-update.md
```

---

## ❌ 错误示例

### WRONG 1：不读文件靠"我记得"

```
Agent：我记得主角的力量体系是XXX…
❌ 没有读取 L1 设定和数值体系就直接写正文
✅ 先读 entity-snapshot + L1 设定 + 数值体系，确认后再写
```

### WRONG 2：Design 不输出事件链

```
设计说明：本章写主角和 Boss 战斗，目标2300字
❌ 没有事件链——"这章具体发生哪几件事？顺序是什么？"
✅ 附上完整事件链："①对峙→②战术分析→③第一次交锋失败→④利用环境扭转局面→⑤终结一击→⑥战后"
```

### WRONG 3：硬编码文件路径

```
Agent：写入 entity-state.yaml 到 design/ 目录
❌ 路径可能不存在或与项目目录结构不匹配
✅ 先从 project.yaml#paths 读取路径，派生子路径
```

---

## 目录结构

```
SKILL.md              ← 轻量菜单（本文）
skill.json
CHANGELOG.md

steps/                ← 各步骤详细指令
├── step-1-design.md
├── step-2-render.md
└── step-5-state-update.md

templates/            ← 模板文件
└── entity-state-schema.md

styles/               ← 文风DNA档案
├── abyss.md
├── zhetian.md
├── longfu.md
└── tunshixingkong.md
```

---

## 版本

v15.0 | 2026-06-09 | **状态协议重构**：章末delta单源 + entity-snapshot全量快照聚合。project.yaml#paths 路径派生替代硬编码。global-summary降级为叙事摘要。step-5-state-update 完全重写。保留 v14 原文片段调音叉格式。
