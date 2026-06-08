---
name: pop-novel-writer
description: 正文写作引擎，3步驱动。Design(LLM/八块设计包)→Render(LLM/三阶段：风格锚定→正文渲染→风格验证)→State Update(零LLM)。v14.0 新增本章空间+登场人物+设定嵌入表+字数预算。
---

# 正文写作引擎（v14.0）

3步管线（2次 LLM + 1次零 LLM）：

```
Step 1 — Design（LLM · 产出八块 chXXX-design.md）
  块A 设计说明 / 块B 本章空间 / 块C 登场人物 / 块D 事件链(含子节拍+反应节点)
  块E 设定嵌入表 / 块F 渲染指引 / 块G 字数预算 / 块H 上下文快照

Step 2 — Render（LLM / 三阶段）
  Phase 1：风格锚定 — 读文风DNA → 提取5-8条可度量风格契约
  Phase 2：正文渲染 — 事件链强制覆盖 × 风格契约同步执行
  Phase 3：风格验证 — P0禁句扫描 + 契约对照 + 情绪弧线检查

Step 3 — State Update（零 LLM）
```

核心原则：**结构正确（Design）≠ 质感正确（Render）。Design 负责空间约束、人设底线、事件节拍和设定嵌入点——Render 负责把这些变成读者读到的句子。****

产出物供给 pop-novel-qa 管线。

---

## ❌ 质量红线

| # | 标准 | 确认 |
|:-:|:-----|:----:|
| ❌1 | **act-XX.yaml 已存在并通过节奏自检** — 无幕纲不进正文 | [ ] |
| ❌2 | **写前必读已执行** — 读 global-summary + 当前幕纲 + L1 设定 | [ ] |
| ❌3 | **Design必须输出事件链+爽点链+渲染指引** — 三块缺一不可 | [ ] |
| ❌4 | **Render 必须覆盖事件链全部节点** — 每个事件必须在正文中出现 | [ ] |
| ❌5 | **风格锚定必须执行（Phase 1）** — 无风格契约不进 Phase 2 | [ ] |
| ❌6 | **风格验证 P0 项 0 违规（Phase 3）** — P0 > 0 立即修补 | [ ] |
| ❌7 | **QC 红线触发 → 退回重写** — "想跳过"≥2 或 "会弃书" 不通过 | [ ] |
| ❌8 | **State after 必须更新** — global-summary + style_report 维护 | [ ] |
| ❌9 | **里程碑已纳入上下文** — 如 design/里程碑设计.md 存在，Design 必须读取并输出里程碑对齐块 | [ ] |

---

## 写前必读清单

```
□ global-summary.md → 确定本章衔接点
□ 当前幕纲（act-XX.yaml）→ emotional_goal + info_release + 钩子
□ project.yaml#reader_profile → 写给谁看
□ design/里程碑设计.md → 确认本章对应哪个 MK（如有）
□ design/终点快照.md → 确认当前进度与终点距离（如有）
□ 续写/长篇小说：精读倒数20章全文 → 输出事实提取报告（闸门由 expert-writer 强制）
```

---

## 管线（3步驱动）

```
Step 1 — Design（LLM · 产出八块 chXXX-design.md）
  读 act-XX.yaml + canvas 人物/地图 + constitution + story-engine + L1设定 + global-summary + 上一章
  产出八块：设计说明 + 本章空间 + 登场人物 + 事件链 + 设定嵌入表 + 渲染指引 + 字数预算 + 上下文快照
  输出文件：03-写作资产/chXXX-design.md
  详细指令 → steps/step-1-design.md

Step 2 — Render（LLM / 三阶段）
  Phase 1：风格锚定 — 读文风DNA → 提取5-8条可度量风格契约
  Phase 2：正文渲染 — 事件链强制覆盖 × 风格契约同步执行
  Phase 3：风格验证 — P0禁句扫描 + 契约对照 + 情绪弧线检查
  输出：正文（02-正文/chXXX.md）+ 状态更新块（含 style_report）
  详细指令 → steps/step-2-render.md

Step 3 — State Update（零 LLM）
  从状态更新块解析 → 追加到 global-summary.md
  详细指令 → steps/step-3-state-update.md
```

---

## ❌ 错误示例

### WRONG 1：不读文件靠"我记得"

```
Agent：我记得主角的力量体系是XXX…
❌ 没有读取 L1 设定和数值体系就直接写正文
✅ 先读 global-summary + L1 设定 + 数值体系，确认后再写
```

### WRONG 2：Design 不输出事件链

```
设计说明：本章写主角和 Boss 战斗，目标2300字
❌ 没有事件链——"这章具体发生哪几件事？顺序是什么？"
✅ 附上完整事件链："①对峙→②战术分析→③第一次交锋失败→④利用环境扭转局面→⑤终结一击→⑥战后"
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
└── step-3-state-update.md

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

v14.0 | 2026-06-08 | Design 升级为八块（+本章空间+登场人物+设定嵌入表+字数预算）。输入增加 canvas 人物/地图/constitution/story-engine
