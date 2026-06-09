---
name: pop-novel-plot
description: 剧情架构设计，以情绪驱动设计幕级爽点分布、情绪弧线和情节线规划（罗琳式支线追踪+契诃夫枪链）。v4.3 新增产出文件有向图规范（@source/@consumed_by）+ 跨文件值一致性校验。
---

# 剧情架构 v4.3

小说的本质是让读者经历情绪变化。幕纲的第一性 = 爽点分布与情绪弧线。

产出物供给 pop-novel-writer（正文写作）管线。

---

## ❌ 质量红线（开工前→完工后自检）

- [ ] **PRD + L1 设定已存在** — 先过 bootstrap，不过开书不进幕纲
- [ ] **节点B导演判断已输出** — 写幕纲前先思考"这个幕的第一性是什么"
- [ ] **每章有 emotional_goal + payoff + end_hook** — 章级切片齐备
- [ ] **爽点等级与铺垫-释放比匹配** — 微 2:1 / 中 4:1 / 大 8-10:1 / 终极 20:1
- [ ] **幕内无连续 3 章同一情绪叠加组合**
- [ ] **节奏自检 7+3+3 项全部通过**
- [ ] **场景卡交互闸门已通过**
- [ ] **平台节奏校准已完成**
- [ ] ★ **act-XX.yaml 已输出**（含 core_conflict / act_end_state / equipment_flow / plotlines / info_release）
- [ ] ★ **act-XX-人物.md 已输出**（本卷登场人物清单）— NEW v4.1
- [ ] ★ **act-XX-地图.md 已输出**（本卷地图设计）— NEW v4.1

---

## 执行顺序（一卷一大纲）

> **设计依赖原则**：先画 canvas（谁上场、在哪演、势力怎么动），再编排 act-XX.yaml（每章怎么演）。

```
Step 1    前置条件 + 节点B              → 节点B-XX.md
Step 2    锚点确认（起点→终点）         → 确认摘要
Step 3    里程碑设计                    → 里程碑设计.md [用户确认闸门]
Step 4    情节线草案                    → 情节线草案-XX.md [用户确认闸门]
          ─── Canvas 绘制阶段 ───
Step 5    本卷人物设计                  → act-XX-人物.md  — NEW v4.1（谁上场）
Step 6    本卷地图设计                  → act-XX-地图.md  — NEW v4.1（在哪演）
Step 7    本卷世界设计（势力/装备）     → act-XX-势力.md + act-XX-装备.md（势力怎么动）
          ─── Canvas 就绪，开始编排 ───
Step 8    L1信息释放规划               → info-release-XX.md（放什么信息）
Step 9    幕纲设计（act-XX.yaml）       → act-XX.yaml（综合以上，章级切片）
Step 10   场景卡试读                    → 场景卡 [用户确认闸门]
Step 11   节奏自检 + 平台校准           → 节奏自检报告.md
Step 12   最终输出校验                  → 全部文件到位
```

> 单幕闸门原则：一次只设计一卷。用户确认后继续下一卷。

---

## 步骤详情（按需加载）

| 步骤 | 详细指令 | 所用模板 |
|:-----|:---------|:---------|
| Step 1 — 前置条件+节点B | `steps/step-1-prerequisite.md` | `templates/checkpoint-b.md` |
| Step 2 — 锚点确认 | `steps/step-2-anchors.md` | — |
| Step 3 — 里程碑设计 | `steps/step-3-milestones.md` | `templates/milestone-design.md` |
| Step 4 — 情节线草案 | `steps/step-4-plotlines.md` | `templates/plotline-draft.md` |
| Step 5 — 本卷人物设计 | `steps/step-5-characters.md` | `templates/character-list.md` |
| Step 6 — 本卷地图设计 | `steps/step-6-map.md` | `templates/map-design.md` |
| Step 7 — 本卷世界设计 | `steps/step-7-world.md` | `templates/faction-dynamics.md` `templates/equipment-flow.md` |
| Step 8 — info_release规划 | `steps/step-8-info-release.md` | `templates/info-release.md` |
| Step 9 — 幕纲设计 | `steps/step-9-act-yaml.md` | `templates/act-guide.md` |
| Step 10 — 场景卡试读 | `steps/step-10-scene-card.md` | — |
| Step 11 — 节奏自检+校准 | `steps/step-11-check.md` | `templates/rhythm-check.md` |
| Step 12 — 输出清单 | `steps/step-12-output.md` | — |

---

## 最终产出目录

```
设计/
├── 起点快照.md                    （bookstrap Phase 6 产出）
├── 终点快照.md                    （bookstrap Phase 7 产出）
├── 里程碑设计.md                  （Step 3 产出）
└── 幕/
    ├── act-XX.yaml                ← P0 强制：幕纲核心产物
    ├── act-XX-人物.md             ← P0 强制：本卷登场人物清单
    ├── act-XX-地图.md             ← P0 强制：本卷地图设计
    ├── 节点B-XX.md                ← 幕设计前思考
    ├── 情节线草案-XX.md           ← 情节线草案
    ├── info-release-XX.md         ← 信息释放规划
    ├── act-XX-势力.md             ← 势力动态（P1建议）
    ├── act-XX-装备.md             ← 装备变化（P1建议）
    ├── 节奏自检报告.md            ← 自检结果
    └── 情节线纲汇总表.md          ← 可选产出
```

---

## ❌ 错误示例

### WRONG 1：跳过节点B直接填模板
→ Agent 直接产出 act-XX.yaml 而没有节点B思考 → 退回补思考说明

### WRONG 2：幕纲完成直接跳正文
→ 跳过了场景卡闸门 + 节奏自检 + 平台校准 → 退回

### WRONG 3：无人物清单直接进章纲
→ act-XX-人物.md 缺失 → 章纲阶段无法知道本卷还有谁会出场 → 退回补人物清单

### WRONG 4：无地图设计导致正文场景矛盾
→ act-XX-地图.md 缺失 → 正文地理位置描述先后矛盾 → 退回补地图

### WRONG 5：跳过大纲直接写正文
→ 用户一开口就要求写正文，但无 act-XX.yaml → 驳回，先过大纲设计

---

## 目录结构

```
pop-novel-plot/
├── SKILL.md              ← 路由层（本文件）
├── skill.json
├── CHANGELOG.md
├── steps/                ← 各步骤详细指令
│   ├── step-1-prerequisite.md
│   ├── step-2-anchors.md
│   ├── step-3-milestones.md
│   ├── step-4-plotlines.md
│   ├── step-5-characters.md
│   ├── step-6-map.md
│   ├── step-7-world.md
│   ├── step-8-info-release.md
│   ├── step-9-act-yaml.md
│   ├── step-10-scene-card.md
│   ├── step-11-check.md
│   └── step-12-output.md
└── templates/            ← 产出物模板
    ├── act-guide.md
    ├── character-list.md
    ├── map-design.md
    ├── faction-dynamics.md
    ├── equipment-flow.md
    ├── milestone-design.md
    ├── info-release.md
    ├── plotline-draft.md
    ├── checkpoint-b.md
    └── rhythm-check.md
```

---

## 版本 v4.3.0 | 2026-06-09
