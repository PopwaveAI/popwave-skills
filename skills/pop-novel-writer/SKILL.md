---
name: pop-novel-writer
description: 正文写作引擎，5步驱动。Director(LLM)→上下文搜集(零LLM)→骨架Agent(LLM)→渲染(LLM)→状态更新(零LLM)。当用户说"写第N章"/"下一章"/"正文"/"续写章节"时启用。含黄金三章模式。
---

# 正文写作引擎

5步管线（3次 LLM + 2次零 LLM）：Director 设计说明+信息释放策略 → 上下文搜集世界快照 → 骨架 Agent 产出事实骨架+QC → 渲染（骨架+DNA）输出正文+状态更新块 → 状态更新维护 global-summary + entity-state。

产出物供给 pop-novel-qa 管线。

---

## ❌ 质量红线

| # | 标准 | 确认 |
|:-:|:-----|:----:|
| ❌1 | **act-XX.yaml 已存在并通过节奏自检** — 无幕纲不进正文 | [ ] |
| ❌2 | **写前必读已执行** — 读 global-summary + 当前幕纲 + L1 设定 + 数值体系 + 读者画像 | [ ] |
| ❌3 | **Director 必须输出信息释放策略** — 哪些设定、什么方式放 | [ ] |
| ❌4 | **骨架层QC已通过** — 事件链完整、设定包完整、密度标记完整、实体≥8、字数≥1800 | [ ] |
| ❌5 | **写后自评必须执行** — 信息释放按骨架执行、读者停下来时刻、字数差、DNA原则遵守 | [ ] |
| ❌6 | **QC 红线触发 → 退回重写** — "想跳过"≥2 或 "会弃书" 不通过 | [ ] |
| ❌7 | **黄金三章特有** — 中爽点起步、前300字首屏、三章情绪弧线完整 | [ ] |
| ❌8 | **State after 必须更新** — global-summary + entity-state 维护 | [ ] |

---

## 写前必读清单

```
□ global-summary.md + entity-state.yaml → 确定本章衔接点
□ 当前幕纲（act-XX.yaml）→ emotional_goal + info_release + 钩子
□ project.yaml#reader_profile → 写给谁看
□ L1 元设定层 + 数值体系 → 能力边界和设定约束
□ 地理+时间轴 → 场景地理和时间点
```

---

## 管线（5步驱动）

### 正常管线（CH4+）

```
Step 1 — Director（LLM）
  读 act-XX.yaml(info_release) + 读者画像 + L1 设定
  出设计说明 + 信息释放策略
  详细指令 → steps/step-1-director.md

Step 2 — 上下文搜集（零 LLM）
  按信息释放策略读 L1 设定 + entity-state + global-summary + 上一章结尾
  出世界快照
  详细指令 → steps/step-2-context.md

Step 3 — 骨架 Agent（LLM）
  读设计说明 + 世界快照
  按 templates/事实骨架模板.md 产事件链+设定包+密度标记
  骨架层 QC（实体≥8、字数≥1800、无叙事决策）
  详细指令 → steps/step-3-skeleton.md

Step 4 — 渲染（LLM）
  输入：骨架 + 世界快照 + 设计说明 + 文风DNA + 红线 + 全局摘要 + 上一章结尾
  Layer 1（骨架）→ 写什么 / Layer 3（文风DNA）→ 怎么写
  输出：正文 + 状态更新块
  写后自评四问 + 写作后自查
  详细指令 → steps/step-4-render.md

Step 5 — 状态更新（零 LLM）
  从状态更新块解析 → 追加到 global-summary.md
  → 更新 entity-state.yaml
  详细指令 → steps/step-5-state-update.md
```

### 黄金三章模式（CH1–CH3）

前三章与正常管线的差异：

| 维度 | 正常 | 黄金三章 |
|:---|:---|:---|
| 爽点等级 | 微爽点打底 | **中爽点起步，三章内≥1大爽点** |
| 字数 | 1800-2500 | **2200-2500（最低2000）** |
| 场景卡 | 可选 | **强制** |
| 写前 | Director | 节点C·黄金 5项检查 |
| 自检 | 4项 | +3项专项 |

详细指令 → `steps/step-golden-triple.md`

---

## ❌ 错误示例

### WRONG 1：不读文件靠"我记得"

```
Agent：我记得主角的力量体系是XXX…
❌ 没有读取 L1 设定和数值体系就直接写正文
✅ 先读 global-summary + L1 设定 + 数值体系，确认后再写
```

### WRONG 2：Director 不输出信息释放策略

```
设计说明：本章写主角和 Boss 战斗，目标2300字
❌ 没有信息释放策略——"这章放哪几个设定？什么方式放？"
✅ 附上信息释放策略："释放金手指绑定（叙事者说明）+ 力量体系升级（实战展示）；新概念≤2"
```

### WRONG 3：黄金三章当普通章写

```
CH1：主角在家起床→吃饭→出门遇熟人
❌ 微爽点打底，前300字没抓住人
✅ CH1 第一段就上冲突/悬念/信息炸弹，中爽点起步
```

---

## 异常与边界条件

| 场景 | 触发条件 | 兜底行为 |
|:-----|:---------|:---------|
| act-XX.yaml 不存在 | Director 前检测缺失 | 基于 spec.md 生成最低可行 act，记录警告 |
| L1 设定缺失 | Step 2 检测到设定文件不存在 | 跳过设定项，仅用通用常识，记录缺失清单 |
| entity-state.yaml 不存在 | Step 2 读取不到 | 跳过，标注"首次启动无历史状态" |
| 骨架实体计数 < 8 | Step 3 骨架产出后 | 检索上章+spec高频名词补至8项，标记 [auto-filled] |
| 文风锚定包不存在 | Step 4 读取不到 | 降级 styles/default.md 兜底 |
| 写后自评发现重大缺陷 | Step 4 自评分数低 | 不修复，中断输出，弹出QC拒稿报告 |
| 用户中途要求改平台/风格 | 流程运行时 | 冻结当前草稿，回退至 Director 重做 |
| 上章 global-summary 损坏 | Step 2 读取失败 | 重新扫描最近3章提取关键事件，重新生成 |

> **核心原则：绝不静默编造内容。** 所有兜底输出必须标注来源，不得掩盖异常路径。

---

## 文风锚定包系统（v3.0）

文风控制通过文风锚定包注入。由 deconstructor 拆书时产出，含 Layer 1（锚定章实例）和 Layer 3（5条叙事哲学DNA）。

```
deconstructor Step 3-b → 01-写作资产/文风锚定包.md
  ↓ 读取优先级：
  ① 01-写作资产/文风锚定包.md（项目级）
  ② styles/{writing_style}.md（内部预置）
  ③ styles/default.md（通用兜底）
  ↓
Step 4 渲染器仅读取 DNA 节（5条原则）→ 不含锚定章片段
```

### 内部预置风格

| ID | 定位 | 适用 | 不适用 |
|:---|:-----|:-----|:-------|
| **abyss** | 西幻·黑暗写实 | DND/实体出版 | 快节奏对话驱动网文 |
| **tomato** | 极致快节奏爽文 | 番茄/零门槛 | 氛围沉浸类 |
| **zhetian** | 文学化叙事·意象 | 仙侠/出版/重情感 | 数据化升级流 |
| **tunshi** | 硬核升级流·参数 | 升级流/无限流 | 情感驱动类 |
| **shengwang** | 狂暴升级·设定密集型 | 玄幻/高信息密度 | 慢热铺垫类 |
| **yazhou** | 同人二次元·吐槽 | 穿越/日漫同人 | 西幻/写实 |
| **zerg** | 异兽种田·系统面板 | 游戏系统/基地建设 | 对话驱动类 |
| **guichui** | 悬疑盗墓·知识科普 | 悬疑/探秘/民俗 | 现代爽文 |
| **nvpin** | 女频古言·细腻慢热 | 古言/宅斗/慢燃 | 快节奏升级流 |
| **default** | 通用兜底 | 所有题材 | — |

---

## 目录结构

```
SKILL.md              ← 轻量菜单（本文）
skill.json
CHANGELOG.md

steps/                ← 各步骤详细指令（按需加载）
├── step-1-director.md
├── step-2-context.md
├── step-3-skeleton.md
├── step-4-render.md
├── step-5-state-update.md
└── step-golden-triple.md

templates/            ← 模板文件（填空式）
├── 事实骨架模板.md
├── entity-state-schema.md
└── everything-bundle-schema.md

prompt-templates/     ← Agent prompt 文本
├── Director-prompt.md
├── Pass2-renderer.md
├── global-summary-schema.md
├── experience-log-schema.md
└── QC-checklist.md

styles/               ← 文风DNA参考
├── 文风锚定包模板.md
├── abyss.md ... zhetian.md
└── default.md
```

---

## 版本

v11.0.0 | 2026-06-05 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)
