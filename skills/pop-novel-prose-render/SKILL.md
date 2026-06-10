---
name: pop-novel-prose-render
description: 正文渲染/上色表达。消费 Design 的骨架产物（事实骨架+登场人物卡），注入文风DNA、锚定章和写作技法，渲染为可读的正文。不判断剧情逻辑、不验证设定一致性。用户说"写正文/渲染这章"时启用。由 expert-writer 通过子 agent 调度。
pipeline:
  upstream: [pop-novel-chapter-design, pop-dna]
  downstream: [pop-novel-qa]
---

# 正文渲染 / 上色表达 v1.0

消费 pop-novel-chapter-design 的骨架产物，注入风格材料，产出可读的正文。

**核心约束：不碰剧情。** 不读上游 Canvas、不验证设定、不判断角色出场是否合理。Design 说了这章发生什么 → 我只管写好。

---

## ❌ 质量红线（开工前→完工后自检）

- [ ] **事实骨架存在** — chXXX-事实骨架.md 完整可读
- [ ] **登场人物卡存在** — chXXX-登场人物卡.md 完整可读
- [ ] **文风DNA 已读取** — styles/ 下有对应档案
- [ ] **锚定章已匹配** — 本章场景类型对应的锚定章已找到（如有）
- [ ] **Phase 1 风格契约已产出** — 提取为可执行的写作规则
- [ ] **Phase 2 所有事件已渲染** — 每个骨架事件在正文中有对应段落
- [ ] **Phase 3 风格验证通过** — 无风格偏差 ≥ 2 处
- [ ] **constitution 红线未触发**
- [ ] **叙事者不解释** — 没有"他意识到/他感到/他仿佛"等 AI 观感词

---

## 三阶段渲染流程

```
Phase 1 — 风格锚定
  读文风DNA → 提取本章场景类型的风格规则 → 读锚定章特征提炼
  → 产出：风格契约（叙事哲学/句式/描写/对话的具体执行规则）

Phase 2 — 正文渲染
  事实骨架 × 登场人物卡 × 风格契约 → 逐事件渲染正文
  → 每个事件：理解意图 → 选切入点 → 用风格契约选句子 → 写段落

Phase 3 — 风格验证
  对照风格契约自检 → 标记偏差 → 最小修补
  → 宪法红线检查 → 叙事者不解释检查
```

---

## 步骤详情（按需加载）

| 步骤 | 详细指令 | 所用模板 |
|:-----|:---------|:---------|
| Step 1 — 读入输入 | `steps/step-1-read-input.md` | — |
| Step 2 — 风格锚定 | `steps/step-2-style-anchor.md` | `templates/style-contract.md` |
| Step 3 — 逐事件渲染 | `steps/step-3-event-render.md` | — |
| Step 4 — 风格验证 | `steps/step-4-style-verify.md` | — |
| Step 5 — 最终输出 | `steps/step-5-output.md` | — |

---

## 最终产出

| 产物 | 路径 |
|:-----|:-----|
| **chXXX.md** | `03-正文/` — 完成正文 + 章末状态更新块 |

---

## ❌ 错误示例

### WRONG 1：叙事者跳出来解释
→ 「他的匕首很锋利——这把武器是他三天前从科尔手里缴获的，那场战斗之后他一直在熟悉它的重心。」  
→ ✅ 正确：「他的匕首在煤油灯下反着冷光。握柄的缠绳已经被手心磨出了贴合掌纹的凹痕。」

### WRONG 2：因为文风规则而跳过骨架事件
→ 骨架有 `事件4: 主角向保罗修女提问`，但 Render 觉得「对话太长不符合简洁风格」就直接删了。  
→ ✅ 正确：骨架说了有对话就必须写对话。语言可以简洁，事件不可跳过。

### WRONG 3：读上游 Canvas
→ Render 读了 act-01.yaml 或 L1 设定。  
→ ✅ 正确：Render 不知道这些文件的存在。只读骨架 + 人物卡 + 风格材料。

---

## 目录结构

```
pop-novel-prose-render/
├── SKILL.md              ← 路由层（本文件）
├── skill.json
├── CHANGELOG.md
├── steps/                ← 各阶段详细指令
│   ├── step-1-read-input.md
│   ├── step-2-style-anchor.md
│   ├── step-3-event-render.md
│   ├── step-4-style-verify.md
│   └── step-5-output.md
└── templates/            ← 产出物模板
    └── style-contract.md
```

---

## 版本 v1.0.0 | 2026-06-09
