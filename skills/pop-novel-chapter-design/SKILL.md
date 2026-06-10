---
name: pop-novel-chapter-design
description: 导演卡/章纲设计。接收大纲的完整 Canvas（人物/地图/势力/信息释放），产出结构化的事实骨架和登场人物卡。不碰文风、修辞、文本质感。用户说"设计这章/章纲/导演卡"时启用。由 expert-writer 通过子 agent 调度。
---

# 章纲设计 / 导演卡 v1.3

接收上游 Plot 的完整 Canvas，为每一章产出回合级的事件骨架和登场人物卡。下游由 pop-novel-prose-render 消费。

**核心约束：不碰文风。** 不知道文风DNA的存在。不写叙事者声音、不写句子节奏、不写修辞风格。

---

## ❌ 质量红线（开工前→完工后自检）

- [ ] **Canvas 就绪** — act-XX.yaml + 人物 + 地图 + 势力 + info-release + 里程碑 全部存在
- [ ] **entity-snapshot 已读取** — 角色当前状态的唯一 canon
- [ ] **所有出场角色可追溯** — 每个角色在 act-XX-人物.md 中存在
- [ ] **所有发生地点可追溯** — 每个地点在 act-XX-地图.md 中存在
- [ ] **info_release 全部落地** — 本章 P0 信息释放项全部在事件链中有对应节点
- [ ] **事件链覆盖本章剧情** — 无遗漏无冗余
- [ ] **情绪节拍与 act-XX.yaml 的 emotional_goal 对齐**
- [ ] **constitution 红线未触发**
- [ ] ★ **事件数 ≥ 章字数 ÷ 200** — 硬性下限，"靶心不够，Render 没材料"

## 执行流程

```
Step 1  读入 Canvas + 状态       → 建立本章设计基线
Step 2  事件链设计               → 分解本章为 3-5 个事件
Step 3  角色调度                 → 确定每个事件的出场角色和状态
Step 4  空间编排                 → 确定每个事件的发生地点
Step 5  信息释放落地             → 将 info_release 分配进事件
Step 6  情绪节拍设计             → 标注每个事件的读者情绪
Step 7  产出与状态更新            → 事实骨架.md + 登场人物卡.md + entity-snapshot 更新
```

---

## 步骤详情（按需加载）

| 步骤 | 详细指令 | 所用模板 |
|:-----|:---------|:---------|
| Step 1 — 读入上下文 | `steps/step-1-read-canvas.md` | — |
| Step 2 — 事件链设计 | `steps/step-2-event-chain.md` | `templates/fact-skeleton.md` |
| Step 3 — 角色调度 | `steps/step-3-character-scheduling.md` | `templates/character-card.md` |
| Step 4 — 空间编排 | `steps/step-4-location-orchestration.md` | — |
| Step 5 — 信息释放落地 | `steps/step-5-info-release.md` | — |
| Step 6 — 情绪节拍 | `steps/step-6-emotional-beats.md` | — |
| Step 7 — 产出与状态 | `steps/step-7-output-state.md` | — |

---

## 最终产出

| 产物 | 路径 | 消费者 |
|:-----|:-----|:-------|
| **chXXX-事实骨架.md** | `03-写作资产/` | pop-novel-prose-render |
| **chXXX-登场人物卡.md** | `03-写作资产/` | pop-novel-prose-render |
| entity-snapshot.yaml（更新） | `00-总控/` | 下一章 Design |

---

## ❌ 错误示例

### WRONG 1：把事件写成正文
→ "他推开木门，屋里弥漫着焚香的气味……"——这是正文，不是事件链。  
→ ✅ 正确：`事件1: 抵达晨曦布道站。地点=布道站正厅。角色=江轩、保罗修女。情绪目标=从焦虑到安心。`

### WRONG 2：角色不在人物清单中
→ 事件链中出现了一个 act-XX-人物.md 没有定义的角色。  
→ ✅ 正确：所有出场角色必须先确认在人物清单中存在。

### WRONG 3：不读 entity-snapshot 凭记忆写状态
→ Design 说「主角当前等级=1级盗贼」，但 entity-snapshot 里是 2级。  
→ ✅ 正确：角色 before 状态从 entity-snapshot 取，不出凭记忆。

---

## 目录结构

```
pop-novel-chapter-design/
├── SKILL.md              ← 路由层（本文件）
├── skill.json
├── CHANGELOG.md
├── steps/                ← 各步骤详细指令
│   ├── step-1-read-canvas.md
│   ├── step-2-event-chain.md
│   ├── step-3-character-scheduling.md
│   ├── step-4-location-orchestration.md
│   ├── step-5-info-release.md
│   ├── step-6-emotional-beats.md
│   └── step-7-output-state.md
└── templates/            ← 产出物模板
    ├── fact-skeleton.md
    └── character-card.md
```

---

## 版本 v1.3.0 | 2026-06-10
