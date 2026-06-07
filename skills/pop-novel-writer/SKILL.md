---
name: pop-novel-writer
description: 正文写作引擎，3步驱动。Design(LLM)→Render(LLM)→State Update(零LLM)。Director与Skeleton合并为单一设计包，减少重复文件输出。
---

# 正文写作引擎（v12.0）

3步管线（2次 LLM + 1次零 LLM）：Design 设计包（设计说明+信息释放策略+事件链+设定包）→ Render 渲染（设计包+文风源）→ State Update 状态更新。

产出物供给 pop-novel-qa 管线。

---

## ❌ 质量红线

| # | 标准 | 确认 |
|:-:|:-----|:----:|
| ❌1 | **act-XX.yaml 已存在并通过节奏自检** — 无幕纲不进正文 | [ ] |
| ❌2 | **写前必读已执行** — 读 global-summary + 当前幕纲 + L1 设定 | [ ] |
| ❌3 | **Design必须输出事件链+设定包** — 不可省略事件链直接进渲染 | [ ] |
| ❌4 | **Render必须覆盖事件链全部节点** — 每个事件必须在正文中出现 | [ ] |
| ❌5 | **写后自评必须执行** — 信息释放覆盖、字数差、文风原则遵守 | [ ] |
| ❌6 | **QC 红线触发 → 退回重写** — "想跳过"≥2 或 "会弃书" 不通过 | [ ] |
| ❌7 | **State after 必须更新** — global-summary 维护 | [ ] |
| ❌8 | **里程碑已纳入上下文** — 如 design/里程碑设计.md 存在，Design 必须读取并输出里程碑对齐块 | [ ] |

---

## 写前必读清单

```
□ global-summary.md → 确定本章衔接点
□ 当前幕纲（act-XX.yaml）→ emotional_goal + info_release + 钩子
□ project.yaml#reader_profile → 写给谁看
□ design/里程碑设计.md → 确认本章对应哪个 MK（如有）
□ design/终点快照.md → 确认当前进度与终点距离（如有）
```

---

## 管线（3步驱动）

```
Step 1 — Design（LLM）
  读 act-XX.yaml + reader_profile + L1设定 + global-summary + 上一章结尾
  一次性产出：设计包（设计说明 + 信息释放策略 + 事件链 + 设定包 + 上下文快照）
  输出文件：03-写作资产/chXXX-design.md（Render完成后可删除）
  详细指令 → steps/step-1-design.md

Step 2 — Render（LLM）
  输入：设计包 + 文风源（10章语料包或文风DNA）+ 宪法红线 + global-summary
  输出：正文（02-正文/chXXX.md）+ 状态更新块
  写后自评四问 + 写作后自查
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

v12.0 | 2026-06-07 | Step 1 Director + Step 3 Skeleton 合并为 Step 1 Design
