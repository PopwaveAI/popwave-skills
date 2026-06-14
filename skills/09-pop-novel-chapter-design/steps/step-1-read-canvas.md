# Step 1：读入 Canvas + 状态

> 管线: 09-pop-novel-chapter-design v1.5
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
| `canvas.设定线` | 本章应向读者交付的设定信息（`信息项名: 内容`） | Step 2 事件链中至少有一个事件承载它 |
| `canvas.设线负载` | 0=无新设定 | 1=适量 | ≥2=过载 | 过载时在事件链中展开而不是塞进一个事件里 |
| `canvas.{主线1..支线2}` | 每条线的本章摘要 | 哪些线在动、做了什么 |
| `canvas.{主线1..支线2}_payoff` | 每条线的 payoff_level | 中/大/特大→ plot 指定了释放窗口 |
| `canvas.note` | 节奏笔记 | "双线并行""蓄力章" |
| `登场角色` | 角色名列表 | 本章可用角色池。从 `状态/角色/{角色名}-角色卡.md` 取 core_desire 等不变信息，从 `entity-snapshot.yaml` 取当前状态 |
| `emotional_goal` | 情感方向 | Step 2 事件情绪目标的上边界 |
| `payoff_note` | 中/大/特大的蓄力上下文 | "主线1ch3-6蓄力，本章释放" → 设计事件时知道压力多大 |
| `end_hook.type` + `drive` | 钩子方向 | Step 2 章末事件凭据 |
| `chekhov_set` / `chekhov_fire` | 本章埋/收的枪 | Step 2 标注 |

#### ★ 角色池 & 地点池（从 act-XX.yaml + volume-XX.md 拿）

**角色**：从 `chapters[N].登场角色` 拿角色名列表
- 对每个角色，读 `状态/角色/{角色名}-角色卡.md` 取 core_desire、人格基线、能力上限（不变/慢变信息）
- 当前微状态（等级/位置/情绪）从 `entity-snapshot.yaml` 取

**地点**：v6.2 起 chapters[].locations 已从 act-skeleton 移除
- 直接从 `设计/卷/volume-XX.md §三` 拿到本卷地点池
- 在本章 Canvas 线摘要中找地点名暗示

#### ★ 本节活跃线（从 Canvas entries 行直接读）
v6.2 起 chapters[].plotlines_active 已从 act-skeleton 移除。
直接从 Canvas entries 当前章行：哪些线有内容（非空）→ 就是本章活跃线。

#### ★ 场景类型推断（从 Canvas 线摘要）

v6.3 起 act-skeleton 不再预设 combat/dialogue/discovery 等场景规格字段。这些由 design 根据 Canvas 线摘要自行判断场景类型并设计事件链。

场景类型推断参考（从 Canvas 线摘要的关键词识别）：

| 线摘要暗示 | 推断场景类型 |
|:-----------|:-------------|
| `"遭遇"` `"攻击"` `"战斗"` `"追杀"` | 战斗章 |
| `"商量"` `"谈判"` `"质问"` `"坦白"` | 对话章 |
| `"发现"` `"探索"` `"进入"` `"揭示"` | 发现章 |
| `"危机"` `"压"` `"紧迫"` `"绝境"` | 危机章 |

> **核心原则**：plot 不给规格——只给上下文。design 从上下文推断场景类型，自己设计事件链。

### 2. 读卷 Canvas（`设计/卷/volume-XX.md`）

卷 Canvas 是下游消费的唯一入口。所有角色/地点/剧情线/势力/装备信息都在此文件。

**人物池** — `volume-XX.md §三`：
- 从 `chapters[N].登场角色` 拿角色名（已在 §1 读取）
- 对每个角色，读 volume-XX.md §三 的对应条目：卷初状态、叙事功能、与主角关系基线（卷级不变信息）
- 当前微状态从 entity-snapshot.yaml 取

**地点池** — `volume-XX.md §三`：
- 从本卷的地点池直接取（卷级定义）
- 结合 Canvas 线摘要的地名暗示确定本章具体地点

**势力** — `volume-XX.md §三`（如有）：
- 如果本章 Canvas 线摘要涉及 主线1 推进 → 读势力条目
- 当前势力状态从 entity-snapshot.yaml 取

**剧情线** — `volume-XX.md §四`：
- 读取 主线1/主线2/主线3/支线1/支线2 的定义和契诃夫枪，用于 Step 2 标注 chekhov_set/fire

### 3. 读后感盘和版本

> v6.3 起独立 info_release_plan 段已删除。设定交付通过 Canvas 设定线前缀统一管理。

### 4. 读项目状态

| 文件 | 取什么 | 用途 |
|:-----|:-------|:-----|
| `00-总控/entity-snapshot.yaml` | 所有角色的当前状态 | 角色 before 状态——这是唯一 canon，不许凭记忆 |
| `正文/ch{上一章}.md` 末尾的状态更新块 | 上一章的 entity_updates + event_log | 衔接点：上章未闭合的节点、语感起点 |
| 上一章的 design 文件 | 写作资产/设计包/ch{上一章}-设计包.md | 检查上章末尾是否有关闭的钩子或未解决的事件 |

### 5. 读 Canvas 约束

| 文件 | 取什么 |
|:-----|:-------|
| `act-XX.yaml` chapters[N] block | Canvas 约束已全部内嵌在 chapter block 中：payoff_level / 登场角色 / chekhov_set / 设定线 |

---

## 产出

以下信息建立为**本章设计基线**（内存，不落盘）：

```
本章在幕中的位置
  - 幕号、章节号、标题
  - 本章在 Canvas 中的 payoff 位置（蓄力/释放/高潮）

本章的槽和约束
  - emotional_goal: act-XX.yaml 指定的情绪目标
  - 场景类型：从 Canvas 线摘要推断（如"遭遇"=战斗、"发现"=探索、"商量"=对话）
  - 设定线交付：设线负载+前缀信息项名（这章必须让读者搞懂什么）
  - 钩子方向：end_hook.type + drive
  - 字数上限：word_count

本章的可用资源
  - 角色池：登场角色[] + 每个角色的角色卡（core_desire）+ entity-snapshot（当前状态）
  - 地点池：从 volume-XX.md §三 拿 + Canvas 线摘要的地名暗示
  - 契诃夫枪：chekhov_set（设伏）/ chekhov_fire（回收）

衔接
  - 上章末尾状态（entity_updates + event_log）
  - 上章未闭合的节点
```
