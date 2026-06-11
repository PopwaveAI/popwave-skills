---
name: pop-novel-plot
description: 剧情架构设计。卷级战略（目标/背景/剧情线/快照）+ 幕级战术（Canvas矩阵/情绪弧线/payoff/每章切片）。v6.0 重构：卷幕分层更清晰，新增 Canvas 矩阵做节奏检查。
pipeline:
  upstream: [pop-novel-bookstrap, pop-novel-deconstructor]
  downstream: [pop-novel-chapter-design]
---

# 剧情架构 v6.1

> **卷 = 战略** — 目标、背景（时间/地理/角色/势力动机）、剧情线列表、开局→结束快照。
> **幕 = 战术** — Canvas 矩阵（章节×剧情线交叉表）、情绪弧线、爽点分布、每章切片。
> **全书架构（Phase 0）** — N 卷蓝图：卷拆分/地理全图/角色出场节奏/主线全览。
>
> 下游（pop-novel-chapter-design）只需要读 2 个文件：
> `设计/卷/volume-XX.md` + `设计/幕/act-XX.yaml`

---

## 0. 设计理念

### 0.1 卷 vs 幕

| 级别 | 范围 | 定位 | 产出物 | 下游消费 |
|:-----|:----:|:-----|:-------|:---------|
| **卷** | 80-150章 | 一个大剧情的完整呈现（战略） | `volume-XX.md`（1个文件） | ✅ chapter-design 读此获取地图/角色/剧情线/势力动机 |
| **幕** | 20-35章 | 卷内的战术执行阶段 | `act-XX.yaml`（每幕1个YAML） | ✅ chapter-design 读此获取 Canvas 矩阵 + 章级切片 |

**一卷 = N 幕**（N = 3-6）。卷定义"有什么"，幕定义"怎么演"。

### 0.2 分层产出

```
卷（战略）→ 设计/卷/volume-XX.md
    目标：核心命题 + 读者感受
    背景：时间/地理/角色池/势力动机
    剧情线：M1-Mn · S1-Sn 的本卷定义
    状态：开局快照 → 结束快照

幕（战术）→ 设计/幕/act-XX.yaml
    Canvas 矩阵：章节×剧情线交叉表（★ v6.0 新增）
    幕级定义：核心冲突/爽点分布/情绪弧线
    章级切片：每章情绪/payoff/钩子/场景规格
    节奏检查：每条线最大连续空白章数自检

> 爽点四档定义 + 设计方法 + 责任归属 → `templates/payoff-guide.md`
```

---

## ❌ 质量红线

- [ ] **PRD + L1 设定已存在** — bootstrap 没过不进 plot
- [ ] **卷设计已产出** — volume-XX.md 包含目标/背景/剧情线/快照
- [ ] **每卷至少 M1/M2/M3 三条主线** — 世界危机 + 主角成长 + 外部推进 为必选，S 线可选追加。剧情线须经用户确认
- [ ] **Canvas 矩阵已填充** — act-XX.yaml#canvas.entries 无持续空白行
- [ ] **每条剧情线无连续超限留白** — act-XX.yaml#canvas.rhythm_check 自检通过
- [ ] **每章有 emotional_goal + payoff + end_hook** — act-XX.yaml 章级切片齐备
- [ ] **爽点等级与铺垫-释放比匹配** — 微 2:1 / 中 4:1 / 大 8-10:1 / 终极 20:1
- [ ] **幕内无连续 3 章同一情绪叠加组合**
- [ ] **主角等级 = act_rank_schedule.end_rank** — 跨文件值一致性
- [ ] **连续 2 章无信息释放 → 第 3 章必追加**
- [ ] **首卷黄金窗口（vol-01/act-01）** — ch01 核心卖点亮相 + 钩子 / ch02 第一次战斗或重大矛盾 / 连续铺垫 ≤ 1章。番茄标准，任一违规 → P0 退回

---

## 执行流程

```
Phase 0：全书架构（1次）
  Step 0    全书架构定义         → 全书架构.md（卷拆分/地理全图/角色出场节奏/主线全览）
  [用户确认闸门]      → 确认全书架构后再进单卷设计
  ↓ 产出: 设计/全书架构.md

第一阶段：卷设计（1次/卷）
  Step 1    卷级定义             → 从全书架构拆取第N卷 → 目标/幕划分/快照
  Step 2    卷 Canvas 设计       → 背景（时间/地理/角色/势力动机）+ 剧情线列表
  [剧情线确认闸门]   → M1/M2/M3 三条主线 + 可选 S 线须经用户确认后才锁定
  [用户确认闸门]     → 确认卷定义（含剧情线）后再进幕纲
  ↓ 产出: 设计/卷/volume-XX.md

第二阶段：幕纲编排（N次/卷，每幕）
  Step 3    信息释放规划         → 当前幕的 P0/P1 信息点章级分配
  Step 4    幕纲设计（核心）     → Canvas 矩阵填充 + 幕级定义 + 每章切片
  Step 5    自检                → 剧情线留白检查 + 节奏 + 值一致性 + 番茄标准校准
  ↓ 产出: 设计/幕/act-XX.yaml（info-release已内嵌于act#info_release_plan）

  → 跳到 Step 3 设计下一幕
  → 所有幕完成后 → 通知下游 chapter-design
```

---

## 步骤详情

| 步骤 | 产出文件 | 模板/参考 | 说明 |
|:-----|:---------|:----------|:------|
| Step 0 — 全书架构 | `设计/全书架构.md` | `steps/step-0-architecture.md` | 卷拆分/地理全图/角色出场节奏/主线全览（开书后执行一次，卷间可修订） |
| Step 1 — 卷定义 | `设计/卷/volume-XX.md` | `steps/step-1-volume.md` + `templates/volume-design.md` | 从全书架构拆取本卷战略：目标/背景/剧情线/快照 + 用户确认闸门 |
| Step 2 — 幕纲编排 | `设计/幕/vol-XX/act-YY.yaml`（info-release已内嵌于act#info_release_plan） | `steps/step-2-act.md` + `templates/act-skeleton.yaml` | Canvas 矩阵 → 章级切片 → info_release_plan → 自检（循环N次） |

---

## 最终产出目录

```
设计/
├── 全书架构.md              ← Phase 0 产出：幕按卷分组结构
├── 卷/
│   └── volume-XX.md          ← 下游消费：卷级战略（目标/背景/剧情线/快照）
└── 幕/
    └── vol-XX/act-YY.yaml    ← 下游消费：Canvas 矩阵 + 章级切片 + info_release_plan + 节奏检查
```

---

## 目录结构

```
pop-novel-plot/
├── SKILL.md              ← 路由层（本文件）
├── skill.json
├── CHANGELOG.md
├── steps/                ← 执行步骤（3个步骤）
│   ├── step-0-architecture.md ← 全书架构设计
│   ├── step-1-volume.md  ← 卷定义
│   └── step-2-act.md     ← 幕纲编排（Canvas 矩阵 + act-XX.yaml + info_release_plan + 自检）
└── templates/            ← 产出物模板
    ├── volume-design.md  ← 卷设计模板（含 全书隶属 段）
    ├── act-skeleton.yaml ← 幕纲 YAML 骨架（含 Canvas 矩阵 + info_release_plan）
    ├── act-guide.md      ← 字段计算公式参考
    └── rhythm-check.md   ← 自检清单
```

---

## 版本 v6.1.0 | 2026-06-11 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)
