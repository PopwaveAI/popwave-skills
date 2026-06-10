---
name: pop-novel-plot
description: 剧情架构设计。卷级定义（定位/快照/时间地理人物剧情线）+ 幕级章纲编排（情绪弧线/payoff/每章切片）。v5.0 重构：卷/幕分离，下游只读 2 个文件。
pipeline:
  upstream: [pop-novel-bookstrap, pop-novel-deconstructor]
  downstream: [pop-novel-chapter-design]
---

# 剧情架构 v5.0

> 重构核心：下游（pop-novel-chapter-design）只需要读 2 个文件：
> `设计/卷/volume-XX.md` + `设计/幕/act-XX.yaml`
>
> 其他所有中间产物不再产出，或仅供 plot skill 内部使用。

---

## 0. 设计理念

### 0.1 卷 vs 幕

| 级别 | 范围 | 定位 | 产出物 | 下游消费 |
|:-----|:----:|:-----|:-------|:---------|
| **卷** | 80-150章 | 一个大剧情的完整呈现 | `volume-XX.md`（1个文件） | ✅ chapter-design 读此获取人物/地图/剧情线 |
| **幕** | 20-35章 | 卷内的情绪阶段 | `act-XX.yaml`（每幕1个YAML） | ✅ chapter-design 读此获取当前幕的章级切片 |

**一卷 = N 幕**（N = 3-6）。卷定义"有什么"，幕定义"怎么演"。

### 0.2 产出物精简

```
旧：11个文件/幕（用户说"到底看哪个"）
新：
    设计/卷/volume-XX.md        ← 单文件：卷定位/快照/时间地理人物剧情线/版本里程碑/势力/装备
    设计/幕/act-XX.yaml          ← 章级切片：每章的情绪/payoff/钩子/场景规格
```

---

## ❌ 质量红线

- [ ] **PRD + L1 设定已存在** — bootstrap 没过不进 plot
- [ ] **卷设计已产出** — volume-XX.md 完整
- [ ] **每章有 emotional_goal + payoff + end_hook** — act-XX.yaml 章级切片齐备
- [ ] **爽点等级与铺垫-释放比匹配** — 微 2:1 / 中 4:1 / 大 8-10:1 / 终极 20:1
- [ ] **幕内无连续 3 章同一情绪叠加组合**
- [ ] **主角等级 = act_rank_schedule.end_rank** — 跨文件值一致性
- [ ] **连续 2 章无信息释放 → 第 3 章必追加**

---

## 执行流程

```
第一阶段：卷设计（1次/卷，Step 1-3）
  Step 1    卷级定义             → 确定卷定位/章节范围/幕划分/快照
  Step 2    卷 Canvas 设计       → 时间地理人物剧情线 + 版本里程碑 + 势力装备路线图
  [用户确认闸门]     → 确认卷定义后再进幕纲
  ↓ 产出: 设计/卷/volume-XX.md

第二阶段：幕纲编排（N次/卷，每幕 Step 4-6）
  Step 4    信息释放规划         → 当前幕的 P0/P1 信息点章级分配
  Step 5    幕纲设计（核心）     → 幕级情绪弧线 + 每章 emotional_goal/payoff/钩子/场景规格
  Step 6    自检                → 节奏 + 值一致性 + 平台校准
  ↓ 产出: 设计/幕/act-XX.yaml + info-release-XX.md

  → 跳到 Step 4 设计下一幕
  → 所有幕完成后 → 通知下游 chapter-design
```

---

## 步骤详情

| 步骤 | 产出文件 | 模板 | 说明 |
|:-----|:---------|:-----|:------|
| Step 1 — 卷级定义 | —（口述确认） | — | 卷号/章节范围/幕划分/快照/核心命题 |
| Step 2 — 卷 Canvas 设计 | `设计/卷/volume-XX.md` | `templates/volume-design.md` | 时间地理人物剧情线 + 版本里程碑 + 势力装备 |
| Step 3 — 用户确认 | —（闸门） | — | 展示 volume-XX.md → 用户点头才进章纲 |
| Step 4 — 信息释放规划 | `设计/幕/info-release-XX.md` | `templates/info-release.md` | P0/P1 信息点章级分配 |
| Step 5 — 幕纲设计 | `设计/幕/act-XX.yaml` | `templates/act-skeleton.yaml` | 每章 emotional_goal/payoff/钩子/场景规格 |
| Step 6 — 自检 | — | `templates/rhythm-check.md` | 节奏 + 值一致性 + 平台校准（不检出文件） |

---

## 最终产出目录

```
设计/
├── 卷/
│   └── volume-XX.md          ← 下游消费：卷级 Canvas（人物/地图/剧情线/版本/里程碑）
└── 幕/
    ├── act-XX.yaml            ← 下游消费：章级切片（每章情绪/payoff/钩子/场景规格）
    └── info-release-XX.md     ← 下游消费：当前幕的设定信息释放规划
```

---

## 附录：旧版 Canvas 文件的处置

| 旧文件 | 去向 |
|:-------|:-----|
| 节点B-XX.md | ❌ 删除（内部思考，不需要产出） |
| 情节线草案-XX.md | ✅ 合并入 volume-XX.md §四 |
| act-XX-人物.md | ✅ 合并入 volume-XX.md §三 |
| act-XX-地图.md | ✅ 合并入 volume-XX.md §三 |
| act-XX-势力.md | ✅ 合并入 volume-XX.md §六 |
| act-XX-装备.md | ✅ 合并入 volume-XX.md §七 |
| 里程碑设计.md | ✅ 合并入 volume-XX.md §五 |
| 节奏自检报告.md | ❌ 删除（不产出，只花 5 分钟自检） |
| 情节线纲汇总表.md | ❌ 删除 |
| 场景卡试读 | 🔄 可选（仅在用户要求时产出） |

---

## 目录结构

```
pop-novel-plot/
├── SKILL.md              ← 路由层（本文件）
├── skill.json
├── CHANGELOG.md
└── templates/            ← 产出物模板
    ├── volume-design.md  ← 卷设计模板（新建）
    ├── act-skeleton.yaml ← 幕纲 YAML 骨架
    ├── act-guide.md      ← 字段计算公式参考
    ├── info-release.md   ← 信息释放规划
    ├── rhythm-check.md   ← 自检清单
    └── deprecated/       ← 被合并的历史模板（保留不动，但不再更新）
```

> 以下旧模板已合并入 volume-design.md 或 act-skeleton.yaml，不再单独维护：
> `checkpoint-b.md` / `character-list.md` / `map-design.md` / `faction-dynamics.md` / `equipment-flow.md` / `milestone-design.md` / `plotline-draft.md`

---

## 版本 v5.0.0 | 2026-06-10
