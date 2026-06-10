# Step 1：读入 Canvas + 状态

> 管线: pop-novel-chapter-design v1.4
> 模板: `templates/fact-skeleton.md` + `templates/character-card.md`
> 参考资料: `references/character-scheduling.md` / `references/location-orchestration.md` / `references/info-release.md` / `references/emotional-beats.md`

---

## 目的

读取上游 Plot 产出的全部 Canvas 文件 + 当前项目状态，建立本章设计基线。

所有字段读完后再开始 Step 2 的事件链设计。

---

## 前置条件

- [ ] act-XX.yaml 存在
- [ ] act-XX-人物.md 存在
- [ ] act-XX-地图.md 存在
- [ ] info-release-XX.md 存在
- [ ] 里程碑设计.md 存在
- [ ] entity-snapshot.yaml 存在
- [ ] constitution.yaml 存在

---

## 执行

### 1. 读幕纲（act-XX.yaml）

定位当前章的章节号（ch = N），从 `chapters[]` 数组中提取 N 对应的章级切片。

#### 必读的章级字段

| 字段 | 取什么 | 将用于 |
|:-----|:-------|:-------|
| `title` | 本章标题 | 填入事实骨架的标题 |
| `word_count` | 预期字数 | 事件密度基线的公式输入：`事件数 ≥ word_count ÷ 200` |
| `emotional_goal` | 本章想让读者感受到什么 | Step 2 的事件情绪目标的上边界 |
| `reader_emotion_path` | 三元素 `[起点, 中间, 终点]` | Step 2 的情绪节拍起点和终点 |
| `payoff.type` | 微 / 中 / 大 / 终极 | 确保事件链中有对应等级的爽点事件 |
| `payoff.trigger` | 爽点触发方式 | Step 2 设计该事件时参考 |
| `end_hook.type` + `drive` + `content` | 章末钩子 | Step 2 的章末事件 = 钩子事件的凭据 |
| `plotlines_active` | 本章推进哪些线 | Step 2 每个事件可标注正在推进哪条线 |
| `chekhov_set` | 本章设伏的枪 | Step 2 标注 chekhov_set 字段 |
| `chekhov_fire` | 本章回收的枪 | Step 2 标注 chekhov_fire 字段 |
| `characters_active` | 本章可出场的角色名 | **角色池**——所有事件的角色必须在其中 |
| `locations` | 本章可用的地点名 | **地点池**——所有事件的地点必须在其中 |
| `milestone_active` | 本章进度对应的 MK | Step 2 标注该章的里程碑状态 |
| `milestone_progress` | start / mid / complete | Step 2 标注 |
| `info_release` | 本章应释放的设定信息 | **信息释放清单**——每个 info_release 项有一个目标事件 |

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

### 2. 读 Canvas 文件

**人物** — `act-XX-人物.md`：
- 从 `characters_active` 中取角色名列表
- 对每个角色，读 `act-XX-人物.md` 中的对应条目：卷初状态、卷末状态、叙事功能、与主角关系基线

**地图** — `act-XX-地图.md`：
- 从 `locations` 中取地点名列表
- 对每个地点，读 `act-XX-地图.md` 中的对应条目：视觉印象、叙事功能、位置关系、空间情绪

**势力** — `act-XX-势力.md`（如有）：
- 如果本章 plotlines_active 包含 M1（世界危机），读势力在当前章段的活动

### 3. 读后感盘和里程碑

**info-release-XX.md**：
- 定位分配的章节段中的 P0/P1 信息点
- 确认每个信息点的 source_doc 路径和 release_method
- 这是 Step 2 中「信息释放」字段的来源

**里程碑设计.md**：
- 如果本章 `milestone_active` 不为空，读对应的 MK 定义

### 4. 读项目状态

| 文件 | 取什么 | 用途 |
|:-----|:-------|:-----|
| `entity-snapshot.yaml` | 所有角色的当前状态 | 角色 before 状态——这是唯一 canon，不许凭记忆 |
| `03-正文/ch{上一章}.md` 末尾的状态更新块 | 上一章的 entity_updates + event_log | 衔接点：上章未闭合的节点、语感起点 |
| 上一章的 design 文件 | ch{上一章}-事实骨架.md | 检查上章末尾是否有关闭的钩子或未解决的事件 |

### 5. 读宪法

| 文件 | 取什么 |
|:-----|:-------|
| `constitution.yaml` | 红线清单——主角战力上限/世界观禁止项/写作红牌 |

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
