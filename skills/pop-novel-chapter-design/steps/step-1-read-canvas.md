# Step 1：读入 Canvas + 状态

> 管线: pop-novel-chapter-design v1.5
> 模板: `templates/fact-skeleton.md`
> 参考资料: `references/character-scheduling.md` / `references/location-orchestration.md` / `references/emotional-beats.md`

---

## 目的

读取上游 Plot 产出的全部 Canvas 文件 + 当前项目状态，建立本章设计基线。

所有字段读完后再开始 Step 2 的事件链设计。

---

## 前置条件

- [ ] `设计/卷/volume-XX.md` 存在（卷级 Canvas：人物池/地点池/剧情线/版本里程碑）
- [ ] `设计/幕/act-XX.yaml` 存在（当前幕的章级切片）
- [ ] `状态/角色/{主角}-角色卡.md` 存在（取 core_desire）
- [ ] 00-总控/entity-snapshot.yaml 存在

---

## 执行

### 1. 读幕纲（act-XX.yaml）

定位当前章的章节号（ch = N），从 `chapters[]` 数组中提取 N 对应的 chapter block。

> **v6.2 起每章一个自包含 block。** Canvas 数据（各线推进+payoff_level）已内嵌在 `chapters[N].canvas` 中，不再有独立的 `canvas.entries` 段。一次性读完即可。

#### 必读字段

| 字段 | 取什么 | 将用于 |
|:-----|:-------|:-------|
| `title` | 本章标题 | 填入事实骨架 |
| `word_count` | 预期字数 | `事件数 ≥ word_count ÷ 200` |
| `canvas.payoff_summary` | ≥中 的线数 | 0=本章无供给侧，需自行制造中爽点 |
| `canvas.D` | 本章应向读者披露的设定/世界观/等级信息 | Step 2 事件链中至少有一个事件承载它 |
| `canvas.D_load` | 0=无新设定 | 1=适量 | ≥2=过载 | 过载时在事件链中展开而不是塞进一个事件里 |
| `canvas.{M1..S2}` | 每条线的本章摘要 | 哪些线在动、做了什么 |
| `canvas.{M1..S2}_payoff` | 每条线的 payoff_level | 中/大/特大→ plot 指定了释放窗口 |
| `canvas.note` | 节奏笔记 | "双线并行""蓄力章" |
| `emotional_goal` | 情感方向 | Step 2 事件情绪目标的上边界 |
| `payoff_note` | 中/大/特大的蓄力上下文 | "M1线ch3-6蓄力，本章释放" → 设计事件时知道压力多大 |
| `end_hook.type` + `drive` | 钩子方向 | Step 2 章末事件凭据 |
| `chekhov_set` / `chekhov_fire` | 本章埋/收的枪 | Step 2 标注 |

#### ★ 角色池 & 地点池（从 volume-XX.md 拿）
v6.2 起 chapters[].characters_active / locations 已从 act-skeleton 移除。
直接从 `设计/卷/volume-XX.md §三` 拿到本卷角色/地点。

#### ★ 本节活跃线（从 Canvas entries 行直接读）
v6.2 起 chapters[].plotlines_active 已从 act-skeleton 移除。
直接从 Canvas entries 当前章行：哪些线有内容（非空）→ 就是本章活跃线。

#### ★ 场景规格字段（v4.2 新增——按场景类型条件读取）

根据本章的场景类型，决定读哪些额外字段。设计事件链时需要参考这些字段来规划：

**如果本章涉及战斗**（`title` 或 `emotional_goal` 暗示是战斗章）：

| 字段 | 取什么 | 将用于 |
|:-----|:-------|:-------|
| `combat.scale` | boss战/碾压战/苦战/遭遇战/逃亡战/围剿战 | 决定战斗事件链的类——密集型还是分散型 |
| `combat.purpose` | 剧情目的 | Step 2 中确保事件链围绕该目的展开 |
| `combat.result` | 完胜/惨胜/败退/被救/敌人撤退/中断 | 章末钩子的前置条件 |
| `combat.reward` | 收获——等级/装备/情报/名声/关系变化 | Step 2 中确保有事件指向该收获 |
| `combat.capability_ref` | 段位来源的 combat_capability.yaml 路径 | 如果事件链中涉及具体段位数字，参考比值 |
| `combat.monster_ref` | monster_rank_map 中的怪物名 | 如果敌人是特定怪物，参考其段位和掉落 |

**如果本章涉及重要对话或谈判**：

| 字段 | 取什么 |
|:-----|:-------|
| `dialogue.relation` | 权力关系 |
| `dialogue.stakes` | 谈崩了会怎样 |
| `dialogue.result` | 对话结果 |
| `dialogue.reward` | 收获 |

**如果本章涉及探索/发现**：

| 字段 | 取什么 |
|:-----|:-------|
| `discovery.what` | 发现了什么 |
| `discovery.how` | 发现方式 |
| `discovery.world_expands` | 世界变大了什么 |
| `discovery.new_options` | 主角的新选项 |

**如果本章是危机卷入**：

| 字段 | 取什么 |
|:-----|:-------|
| `crisis.threat` | 威胁是什么 |
| `crisis.scale` | 规模 |
| `crisis.cannot_escape_because` | 为什么不能逃 |
| `crisis.cost_of_involvement` | 卷入代价 |

### 2. 读卷 Canvas（`设计/卷/volume-XX.md`）

卷 Canvas 是下游消费的唯一入口。所有角色/地点/剧情线/势力/装备信息都在此文件。

**人物池** — `volume-XX.md §三`：
- 从 act-XX.yaml 的 `characters_active` 中取角色名列表
- 对每个角色，读 volume-XX.md §三 的对应条目：卷初状态、叙事功能、与主角关系基线
- 当前状态从 entity-snapshot.yaml 取（不是从卷设计取）

**地点池** — `volume-XX.md §三`：
- 从 act-XX.yaml 的 `locations` 中取地点名列表
- 对每个地点，读 volume-XX.md §三 的对应条目：视觉印象、叙事功能、位置关系、空间情绪

**势力** — `volume-XX.md §六`（如有）：
- 如果本章 plotlines_active 包含 M1，读势力当前章段的活动

**剧情线** — `volume-XX.md §四`：
- 读取 M1/M2/M3/S1/S2 的定义和契诃夫枪，用于 Step 2 标注 chekhov_set/fire

**版本里程碑** — `volume-XX.md §五`（如有）：
- 如果本章 `milestone_active` 不为空，读对应的 MK 定义

**装备路线图** — `volume-XX.md §七`（如有）：
- 如果本章涉及装备变化，读装备路线图的段位约束

### 3. 读幕纲（act-XX.yaml）

幕纲提供本章的章级切片数据，包括 emotional_goal / payoff / end_hook / combat 规格等。详见上方 §1。

### 4. 读后感盘和版本

**act-XX.yaml#info_release_plan**：
- 定位当前幕分配的 P0/P1 信息点
- 确认每个信息点的 source_doc 路径和 release_method
- 这是 Step 2 中「信息释放」字段的来源

### 5. 读项目状态

| 文件 | 取什么 | 用途 |
|:-----|:-------|:-----|
| `00-总控/entity-snapshot.yaml` | 所有角色的当前状态 | 角色 before 状态——这是唯一 canon，不许凭记忆 |
| `正文/ch{上一章}.md` 末尾的状态更新块 | 上一章的 entity_updates + event_log | 衔接点：上章未闭合的节点、语感起点 |
| 上一章的 design 文件 | 写作资产/设计包/ch{上一章}-设计包.md | 检查上章末尾是否有关闭的钩子或未解决的事件 |

### 6. 读 Canvas 约束

| 文件 | 取什么 |
|:-----|:-------|
| `act-XX.yaml` 各字段（combat.scale / payoff / chekhov_set） | 已隐含所有约束 |

---

## 产出

以下信息建立为**本章设计基线**（内存，不落盘）：

```
本章在幕中的位置
  - 幕号、章节号、标题
  - 本章在情绪弧线上的位置（从 emotional_goal 推断：蓄力/拉人/释放/高潮）

本章的槽和约束
  - actor_goal: act-XX.yaml 指定的情绪目标
  - 场景类型：combat / dialogue / discovery / crisis / transition / mix（+ 对应的场景规格字段）
  - 爽点等级：payoff.type
  - 钩子规格：end_hook.type + content（章末必须对齐）
  - 字数上限：word_count

本章的可用资源
  - 角色池：characters_active + 每个角色的 after 来自 entity-snapshot
  - 地点池：locations + 每个地点的视觉印象和位置关系
  - 信息释放清单：info_release[]（含 source_doc / release_method）

衔接
  - 上章末尾状态（entity_updates + event_log）
  - 上章未闭合的节点
```
