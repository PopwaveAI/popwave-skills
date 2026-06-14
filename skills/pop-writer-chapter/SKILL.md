---
name: pop-writer-chapter
description: "当用户说'设计第X章/章纲/骨架/导演卡'时启用。消费 plot 的 Canvas 矩阵，产出事实骨架+登场人物卡合并设计包。"
pipeline:
  upstream: [pop-writer-plot]
  downstream: [pop-writer-prose]
---

# 章纲设计 / 导演卡 v1.5.0

> **定位：消费 plot 的 Canvas，产出事实骨架 + 角色状态更新。**
> **核心约束：不碰文风。不写叙事者声音、不写句子节奏、不写修辞风格。**

---

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **Canvas 未就绪** — `设计/卷/volume-XX.md` + `设计/幕/act-XX.yaml` 任一缺失 → 终止，提示先完成 plot |
| ❌2 | **entity-snapshot 未读取** — Step 1 未加载 `00-总控/entity-snapshot.yaml` → 阻断，角色 before 状态无 canon 来源 |
| ❌3 | **出场角色不可追溯** — 事件引用角色不在 `volume-XX.md §三` 角色池中 → 拒绝，补充或注册进 volume |
| ❌4 | **事件密度不达标** — 事件链事件数 < 章字数 ÷ 200 → 退回扩充事件直到达标 |
| ❌5 | **info_release P0 未全部落地** — 本章 P0 信息释放项无对应事件节点 → 退回匹配 |
| ❌6 | **产出只留摘要** — 写入 design 包后对话中不粘贴完整文件。格式：「已写入 {路径}。摘要：{核心}。需展开告诉我。」 |

---

## 速查表

| 步骤 | 操作 | 读什么 | 产出 | 门禁 |
|:-----|:-----|:-------|:-----|:-----|
| 1 | 读入上下文 | `steps/step-1-read-canvas.md` | context 中的完整基线 | ❌ Canvas 缺退回 |
| 2 | 事件链设计 | `steps/step-2-event-chain.md` | 完整事件链（≥章字数÷200 条） | ❌ 密度不够退回 |
| 3 | 产出落盘 | `steps/step-3-output.md` | 设计包.md + entity-snapshot 更新 | ❌ 缺落盘退回 |

---

## 核心流程

### 步骤 1：读入上下文
详细指令 → `steps/step-1-read-canvas.md`

### 步骤 2：事件链设计（★ 核心）
详细指令 → `steps/step-2-event-chain.md`

### 步骤 3：产出与状态更新
详细指令 → `steps/step-3-output.md`

> 步骤 2 是唯一的核心步骤。角色调度、空间编排、信息释放、情绪节拍不是独立步骤——它们是 Step 2 中设计每个事件时**同步**完成的工作。参考资料见 `references/`。

---

## ❌ WRONG 示例

> ❌ 先把事件链全部设计完，再回头逐个补角色、分配地点、塞信息、标情绪
> ✅ 每设计一个事件同步确定在哪/谁/发生什么/情绪/字数。角色/空间/信息/情绪是事件设计时的组成部分

> ❌ "他推开木门，屋里弥漫着焚香的气味……"——这是 Render 的微节拍
> ✅ `事件：抵达驿站。地点=驿站正厅。角色=主角、配角A。情绪目标=从焦虑到安心。`

> ❌ 本章是战斗章但 Step 1 没读 combat.purpose/combat.result 场景规格字段
> ✅ 根据场景类型按需读 combat / dialogue / discovery / crisis 字段

---

## 边界条件

| 场景 | 触发条件 | 处理 |
|:-----|:---------|:-----|
| Canvas 上游未产出 | act-XX.yaml 不存在 | 拒绝，提示先完成 plot 幕纲编排 |
| 角色不在角色池 | 事件引用的角色未在 volume-XX.md §3 出现 | 拒绝，从角色池选取或先在 volume 中注册 |
| 地点不在地点池 | 事件引用的地点未在 volume-XX.md §3 出现 | 拒绝，从地点池选取或先在 volume 中注册 |
| 跨章弧线标注缺失 | 事件横跨多章但未标注 arc_span | 退回，补全 arc_span + 本章位置 |
| 章字数偏差过大 | 各事件估算字数之和与 act-XX.yaml 的 word_count 偏差 > 20% | 警告，调整事件粒度或更新 word_count |
| 越界到 prose-render | 对话出现"这段怎么写/用什么词/节奏怎么切" | 提示：这是 prose-render 的范围，到那一步处理 |

---

## 本阶段边界

| 做什么 | 不做什么 |
|:-------|:---------|
| 读 Canvas → 事件链设计 → 事实骨架+登场人物卡 | ❌ 不渲染正文（那是 prose-render 的活） |
| ◆小爽点≥5/章 + ★中爽点≥1/章 | ❌ 不验证剧情逻辑（那是 QA 的活） |
| 钩子字段：10种类型 + L1-L5强度 | |

---

## 落盘检查点

| 确认项 | 状态 |
|:-------|:----:|
| `写作资产/设计包/chXXX-设计包.md` 已写入 | [ ] |
| `00-总控/entity-snapshot.yaml` 已更新（角色 after 状态） | [ ] |
| 所有出场角色在 volume-XX.md §角色池中存在 | [ ] |
| 所有事件地点在 volume-XX.md §地点池中存在 | [ ] |
| ◆小爽点≥5 + ★中爽点≥1 | [ ] |

---

## 引用关系

```
Step 2 事件链设计（核心）
  消费：
    └── templates/fact-skeleton.md              ← 产出格式模板
    └── references/character-scheduling.md      ← 角色 before/after/关系/台词风格
    └── references/location-orchestration.md    ← 地点可追溯性/移动逻辑
    └── references/emotional-beats.md           ← 情绪库/弧线检查
    └── references/info-release.md              ← 信息释放检查
```

## 版本

v1.5.0 | 2026-06-13 → [CHANGELOG.md](CHANGELOG.md)
