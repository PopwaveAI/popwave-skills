---
name: 09-pop-novel-chapter-design
description: 当用户说"设计第X章/章纲/骨架/导演卡"时启用。消费 plot 的 Canvas 矩阵，产出事实骨架+登场人物卡合并设计包。
pipeline:
  upstream: [08-pop-novel-plot]
  downstream: [10-pop-novel-prose-render]
---

# 章纲设计 / 导演卡 v1.5.0

接收上游 Plot 的完整 Canvas，为每一章产出回合级的事件骨架和登场人物卡。下游由 10-pop-novel-prose-render 消费。

**核心约束：不碰文风。** 不知道文风DNA的存在。不写叙事者声音、不写句子节奏、不写修辞风格。

---

## 速查表

| 我要 | 操作 | 前置条件 |
|------|------|---------|
| 设计第X章 | 读 Canvas → 事件链设计 → 输出设计包 | plot 必须产出 act-XX.yaml |
| 战斗章 | 事件数≥字数÷200 + 中爽点≥1 + ◆小爽点≥5 | 同上 |
| 对话章 | 场景类型识别=对话 → 应用对话设计规则 | 同上 |

---

## ❌ 质量红线（开工前→完工后自检）

- [ ] **Canvas 就绪** — `设计/卷/volume-XX.md` + `设计/幕/act-XX.yaml`（info_release_plan 内嵌）全部存在
- [ ] **entity-snapshot 已读取** — 角色当前状态的唯一 canon
- [ ] **所有出场角色可追溯** — 每个角色在 volume-XX.md §三（角色池）中存在
- [ ] **所有发生地点可追溯** — 每个地点在 volume-XX.md §三（地点池）中存在
- [ ] **info_release 全部落地** — 本章 P0 信息释放项全部在事件链中有对应节点
- [ ] **事件链覆盖本章剧情** — 无遗漏无冗余
- [ ] **情绪节拍与 act-XX.yaml 的 emotional_goal 对齐**
- [ ] **Canvas 字段约束未突破**
- [ ] ★ **事件数 ≥ 章字数 ÷ 200** — 硬性下限，"靶心不够，Render 没材料"
- [ ] ★ **产出只留摘要** — 写入设计包后对话中只说"已写入 {路径}。摘要：{核心}。需展开任一段告诉我。"

## 执行流程

```
Step 1  读入 Canvas + 状态       → 建立本章设计基线（角色池/地点池/信息清单/幕纲字段/场景规格）
Step 2  事件链设计（★ 核心）     → 逐个回合设计事件，每个事件同步确定地点/角色/内容/情绪/信息释放/字数
                                  同步检查：角色在 Canvas + 地点在 Canvas + 事件数 ≥ 下限
                                  跨章弧线识别：如需跨章 → 标注 arc_span + 本章位置
Step 3  产出与状态更新            → 设计包.md（含事实骨架+登场人物卡）+ entity-snapshot 更新
```

> 步骤 2 是唯一的核心步骤。角色调度、空间编排、信息释放、情绪节拍不是独立步骤——它们是 Step 2 中设计每个事件时**同步**完成的工作。参考资料见 `references/`。

---

## 步骤详情（按需加载）

| 步骤 | 详细指令 | 所用模板/参考 |
|:-----|:---------|:--------------|
| Step 1 — 读入上下文 | `steps/step-1-read-canvas.md` | — |
| Step 2 — 事件链设计（核心） | `steps/step-2-event-chain.md` | `templates/fact-skeleton.md` + `references/` 五个文件 |
| Step 3 — 产出与状态 | `steps/step-3-output.md` | `templates/fact-skeleton.md`（已合并） |

---

## 最终产出

| 产物 | 路径 | 消费者 |
|:-----|:-----|:-------|
| **chXXX-设计包.md** | `写作资产/设计包/` | 10-pop-novel-prose-render |
| entity-snapshot.yaml（更新） | `00-总控/` | 下一章 Design |

---

## ❌ 错误示例

### WRONG 1：独立步骤执行角色/空间/信息/情绪
→ 先把事件链全部设计完，再回头逐个补角色、分配地点、塞信息、标情绪。  
→ ✅ 正确：每设计一个事件同步确定在哪/谁/发生什么/情绪/字数。角色/空间/信息/情绪是事件设计的组成部分，不是事后补填。

### WRONG 2：把事件写成正文
→ "他推开木门，屋里弥漫着焚香的气味……"——这是 Render 的微节拍，不是 Design 的事件。  
→ ✅ 正确：`事件: 抵达驿站。地点=驿站正厅。角色=主角、配角A。情绪目标=从焦虑到安心。`

### WRONG 3：三个战斗回合合并为一个事件
→ "他在据点里解决了二楼的三个人"——三个回合合并，Design 事件太粗。  
→ ✅ 正确：拆为三个——「推门进房间→目标正背对翻抽屉」「目标转身拔剑→已经来不及了」「正面格杀→补刀确认死亡」。

### WRONG 4：不读 act-XX.yaml 的场景规格字段
→ 本章是战斗章但 Step 1 没读 combat.purpose / combat.result。  
→ ✅ 正确：根据场景类型按需读 combat / dialogue / discovery / crisis 字段。

### WRONG 5：不读 entity-snapshot 凭记忆写状态
→ Design 说「主角当前等级=1级盗贼」，但 entity-snapshot 里是 2级。  
→ ✅ 正确：角色 before 状态从 entity-snapshot 取，不许凭记忆。

---

## 异常与边界条件

| 场景 | 触发条件 | 处理方式 |
|:-----|:---------|:---------|
| Canvas 上游未产出 | act-XX.yaml 不存在 | 拒绝，提示先完成 plot 幕纲编排 |
| entity-snapshot 未读取 | Step 1 未加载 entity-snapshot.yaml | 阻断，角色 before 状态无 canon 来源 |
| 事件数不达标 | 设计后事件数 < 章字数 ÷ 200 | 退回，追加事件直到满足下限 |
| 角色不在角色池 | 事件引用的角色未在 volume-XX.md §角色池出现 | 拒绝，提示从角色池选取或先在 volume 中注册 |
| 地点不在地点池 | 事件引用的地点未在 volume-XX.md §地点池出现 | 拒绝，提示从地点池选取或先在 volume 中注册 |
| info_release P0 未全部落地 | 本章 P0 信息释放项存在无对应事件节点 | 退回，为每个 P0 项匹配至少一个事件节点 |
| 跨章弧线标注缺失 | 事件横跨多章但未标注 arc_span | 退回，补全 arc_span + 本章位置标注 |
| 章字数估算与设计不匹配 | 各事件估算字数之和与 act-XX.yaml 的 word_count 偏差 > 20% | 警告，调整事件粒度或更新 word_count |

---

## 本阶段边界

### 本步做什么
- 读 Canvas → 事件链设计 → 事实骨架+登场人物卡
- ◆小爽点≥5/章 + ★中爽点≥1/章
- 钩子字段：10种类型 + L1-L5强度 + driver + relates_to

### 本步不做什么
- ❌ 不渲染正文（那是 prose-render 的活——我们只有事件级描述，没有段落级文案）
- ❌ 不验证剧情逻辑（那是 QA 的活）

**越界检测**：如果对话出现"这段怎么写/用什么词/节奏怎么切"→ 说"这属于 prose-render 的范围，到那一步处理。现在先把骨架的因果链和爽点密度确认好。"

---

## 落盘检查点

执行完毕后确认以下文件落盘：

| 检查项 | 路径 | 状态要求 |
|:-------|:-----|:---------|
| 设计包 | `写作资产/设计包/chXXX-设计包.md` | 已写入，包含事实骨架 + 登场人物卡 |
| entity-snapshot 更新 | `00-总控/entity-snapshot.yaml` | 已更新，角色 after 状态写入 |
| 事件-角色可追溯 | chXXX-设计包.md §登场人物卡 | 所有出场角色在 volume-XX.md §角色池中存在 |
| 事件-地点可追溯 | chXXX-设计包.md §事实骨架 | 所有事件地点在 volume-XX.md §地点池中存在 |
| 爽点密度 | chXXX-设计包.md §事实骨架 | ◆小爽点≥5 + ★中爽点≥1 |

**落盘后动作**：通知 downstream `10-pop-novel-prose-render` 可开工。

---

## 目录结构

```
09-pop-novel-chapter-design/
├── SKILL.md              ← 路由层（本文件）
├── skill.json
├── CHANGELOG.md
├── steps/                ← 执行步骤
│   ├── step-1-read-canvas.md
│   ├── step-2-event-chain.md   ← ★ 核心
│   └── step-3-output.md
├── templates/            ← 产出物模板
│   ├── fact-skeleton.md
│   └── character-card.md
├── references/           ← Step 2 消费的参考文档（非独立步骤）
    ├── character-scheduling.md
    ├── location-orchestration.md
    ├── emotional-beats.md
    └── info-release.md
```

---

## 引用关系

```
Step 2 事件链设计（核心）
  消费：
    └── templates/fact-skeleton.md              ← 产出格式模板
    └── references/character-scheduling.md ← 角色 before/after/关系/台词风格检查
    └── references/location-orchestration.md ← 地点可追溯性/移动逻辑检查
    └── references/emotional-beats.md      ← 情绪库/弧线检查
    └── references/info-release.md         ← 信息释放检查
```

---

## 版本 v1.5.0 | 2026-06-13
