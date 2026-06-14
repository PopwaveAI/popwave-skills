---
name: pop-writer-plot
description: "当用户说'设计剧情/规划大纲/情绪弧线/画幕纲'时启用。消费 pop-writer-creative 的 story-engine，产出卷级战略+幕级战术（Canvas矩阵/情绪弧线/payoff链）。"
pipeline:
  upstream: [pop-writer-creative, pop-decon]
  downstream: [pop-writer-chapter]
---

# pop-writer-plot · 剧情架构设计 v6.3.1

> **卷 = 战略** — 目标、背景（时间/地理/角色/势力动机）、剧情线列表、开局→结束快照。
> **幕 = 战术** — Canvas 矩阵（章节×剧情线交叉表）、情绪弧线、爽点分布、每章切片。
>
> 下游（pop-writer-chapter）只需读 2 个文件：`设计/卷/volume-XX.md` + `设计/幕/act-XX.yaml`

---

## 速查表

| 步骤 | 操作 | 读什么 | 产出 | 门禁 |
|:-----|:-----|:-------|:-----|:-----|
| 全书架构 | 卷拆分 → 地理全图 → 角色出场 → 主线全览 → 卷间钩子 | bookstrap 产出 | `设计/全书架构.md` | bookstrap 完成 |
| 卷设计 | 核心命题 → 剧情线分配 → 读者感受定调 | 全书架构.md | `设计/卷/volume-XX.md` | 全书架构确认 |
| 幕纲编排 | 逐章填充 → Canvas矩阵 → 节奏自检 | volume-XX.md | `设计/幕/act-XX.yaml` | 卷设计确认 |

---

## 0. 设计理念

卷（80-150章）= 战略，幕（20-35章）= 战术。一卷 = 3-6 幕。

```
卷 → 设计/卷/volume-XX.md: 目标/背景(时间+地理+角色池+势力动机)/剧情线(主线1-3+支线)/状态(开局→结束)
幕 → 设计/幕/act-XX.yaml: Canvas矩阵(章节×剧情线)/幕级定义(核心冲突+爽点+情绪弧线)/章级切片(情绪+payoff+钩子+场景)
```

爽点四级定义 + 方法论 → `references/payoff-design-guide.md`

---

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| 1 | **PRD + L1 设定已存在** — bootstrap 没过不进 plot |
| 2 | **卷设计已产出** — volume-XX.md 包含目标/背景/剧情线/快照 |
| 3 | **每卷至少 主线1/主线2/主线3 三条主线** — 世界危机 + 主角成长 + 主角行动 为必选，剧情线须经用户确认 |
| 4 | **Canvas 矩阵已填充** — act-XX.yaml#canvas.entries 无持续空白行 |
| 5 | **每条剧情线无连续超限留白** — act-XX.yaml#rhythm_check 自检通过 |
| 6 | **每章有 emotional_goal + payoff + end_hook** — act-XX.yaml 章级切片齐备 |
| 7 | **爽点密度达标** — 小≥5/章 + 中≥1/章 / 大间隔≤5章 + 特大≥1/卷 |
| 8 | **幕内无连续 3 章同一情绪叠加组合** |
| 9 | **连续 2 章无信息释放 → 第 3 章必追加** |
| 10 | **首卷黄金窗口（vol-01/act-01）** — ch01 核心卖点亮相 + 钩子 / ch02 第一次战斗或重大矛盾 / 连续铺垫 ≤ 1章。任一违规 → P0 退回 |

---

## 执行流程

| 阶段 | 步骤 | 产出 | 闸门 |
|:-----|:-----|:-----|:-----|
| **Phase 0** 全书架构 | Step 0 全书架构定义 | `设计/全书架构.md` | 用户确认全书架构 |
| **第一阶段** 卷设计 | Step 1 卷级定义 → Step 2 Canvas 设计（背景+剧情线） | `设计/卷/volume-XX.md` | 剧情线确认闸门（主线1/2/3）+ 用户确认卷定义 |
| **第二阶段** 幕纲编排 | Step 3 信息释放规划 → Step 4 Canvas 填充+幕级定义+章级切片 → Step 5 自检 | `设计/幕/vol-XX/act-YY.yaml` | 留白检查+节奏+值一致性+番茄标准 |

所有幕完成后 → 通知下游 chapter-design。

---

## ❌ 错误示例

| ❌ 错误 | 问题 | ✅ 正确 |
|:--------|:-----|:--------|
| 幕内连续放空（主线连续 4 章无进展） | 读者遗忘这条线 | 每条线每幕至少出现 1 次，连续空白 ≤ 3 章 |
| Canvas 矩阵留白（剧情线行全空） | 该线在本幕断掉 | 所有剧情线行至少有 1 个交点 |
| 主线只设 2 条 | 剧情感单薄 | 必须产出 主线1（世界危机）+ 主线2（主角成长）+ 主线3（主角行动） |

---

## 异常与边界条件

| 场景 | 触发条件 | 处理方式 |
|:-----|:---------|:---------|
| 用户跳步（未做全书架构直接要卷设计） | Phase 0 产出不存在 | 拒绝，提示先完成 Phase 0 |
| 用户跳步（未做卷设计直接要幕纲） | volume-XX.md 不存在 | 拒绝，提示先完成卷定义 |
| 幕内总章数超出卷章数预算 | act 覆盖章数 > volume 分配范围 | 提示预算超限，建议拆分幕或调整卷 |
| 剧情线确认闸门未通过 | 用户未确认三条主线 | 阻塞，等待确认 |
| 首卷黄金窗口违规 | ch01 无核心卖点/ch02 无战斗/连续铺垫>1章 | P0 退回，重新设计前两章 |
| Canvas 维度不匹配 | 剧情线数量 ≠ canvas.entries 行数 | 自检报错，修复对齐 |
| 跨卷角色出场节奏断裂 | 角色在角色池但本卷无出场计划 | 警告，提示补充或移除 |

---

## 本阶段边界

**做：** 全书架构 → 卷设计 → 幕纲编排 + 首卷黄金窗口检查
**不做：** ❌ 不设计章级细节（chapter-design） ❌ 不写正文（prose-render）

**越界检测：** "第X章怎么写/这章几个事件" → "这属于 chapter-design，先确认卷和幕结构。"

---

## 落盘检查点

| 检查项 | 路径 | 状态要求 |
|:-------|:-----|:---------|
| 全书架构 | `设计/全书架构.md` | 已写入，含卷拆分/地理全图/角色出场/主线全览/卷间钩子 |
| 卷设计 | `设计/卷/volume-XX.md` | 已写入，含目标/背景/剧情线/快照 |
| 幕骨架 | `设计/幕/vol-XX/act-YY.yaml` | 已写入，Canvas 矩阵 + rhythm_check 自检通过 |
| 剧情线状态 | volume-XX.md §剧情线 | 主线1/2/3 + 支线均已用户确认 |
| 跨文件一致性 | volume-XX.end_rank vs act-XX.act_rank_schedule.end_rank | 值一致 |

**落盘后动作：** 若当前卷所有幕已完成 → 通知 downstream `pop-writer-chapter` 可开工。

---

## 目录结构

```
pop-writer-plot/
├── SKILL.md / skill.json / CHANGELOG.md
├── steps/          ← step-0-architecture, step-1-volume, step-2-act
├── templates/      ← volume-design.md, act-skeleton.yaml, act-guide.md, rhythm-check.md
└── references/     ← payoff-design-guide.md
```

---

## 版本 v6.3.1 | 2026-06-14 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)
