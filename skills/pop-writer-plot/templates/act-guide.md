# act-guide.md — 幕字段计算公式参考

> 管线: pop-writer-plot v6.1 · Step 2
> 消费: pop-writer-chapter 做字段追溯时参考
> 输入: volume-XX.md（卷级战略）+ act-skeleton.md 骨架 + 状态/角色/核心角色卡
> 产出: 设计/幕/vol-XX/act-YY.md（Markdown）

---

## 前置检查清单

- [ ] volume-XX.md 已产出（角色池/地点池/剧情线/势力动机）
- [ ] 状态/角色/核心角色卡存在（取 core_desire）
- [ ] act-skeleton.md 骨架已读取

---

## 一、字段来源速查表

### 1.1 幕级定义

| 字段 | 公式/来源 |
|:-----|:----------|
| `core_conflict.description` | 格式 `A vs B`。从 volume-XX.md#剧情线 提取本幕核心冲突 |
| `core_conflict.stakes` | "失败 = 失去什么"。从卷终点反推——如果主角不败，最差结果 |
| `core_conflict.escalation_path` | 冲突从第1章到最后一章如何升级。volume-XX.md 的地理扩张暗示冲突升级 |
| `goal` | 格式 `"读者从「X」到「Y」"`。X = ch1读者的初始感受，Y = 幕末期待感受 |
| `tone_note` | 1-3句散文。不用比例，写感受 |

### 1.2 信息释放计划（参考 act-skeleton.md 模板）

| 字段 | 来源 |
|:-----|:-----|
| `p0_must_release` | 从 volume-XX.md 各节扫描本章段需要的设定信息，标记 P0（不释放就看不懂剧情） |
| `p1_recommended` | 拓展读者体验的信息点 |
| `density_check` | 第1章新概念上限 ≤ 2；连续2章无信息释放 → 第3章必须追加 |

### 1.3 爽点分布

> 设计方法论 → `references/payoff-design-guide.md`。承接指南 → `pop-writer-chapter/references/payoff-guide.md`
> 此表仅列出 plot 层面需要关注的密度约束和大/特大位置规划。

| 级别 | 密度约束 | plot 负责什么 |
|:-----|:--------|:-------------|
| 小爽点 | 每章 ≥ 5 个 | **不负责** — 归 chapter-design 事件链设计 |
| 中爽点 | 每章 ≥ 1 个 | **位置规划 — Canvas 确保每章 ≥1 条线=中，跟踪各线铺垫→释放节奏** |
| 大爽点 | 间隔 ≤ 5 章 | **位置规划** — Canvas 逐线标记 payoff_level=大 + 蓄力设计 |
| 特大爽点 | 每卷 ≥ 1 个 | **位置规划** — Canvas 多线大汇聚章识别（≥2 线=大） |

### 1.4 情绪弧线

`checkpoints` 只标关键转折点（4-6个）。从 Canvas 矩阵的情绪走势反推。

---

## 二、章级字段

每章必须填：

| 字段 | 约束 |
|:-----|:-----|
| `ch` | 连续不跳号 |
| `title` | — |
| `word_count` | — |
| `emotional_goal` | 第一性。指导章节的情绪靶心 |
| `payoff.type` | 与 `payoff_distribution` 的级别对齐。微爽点章 = "微"，高潮章对应级别 |
| `payoff.trigger` | 具体事件名。与后面章节的 payoff 不重复 |
| `reader_emotion_path` | `[起点, 中间, 终点]`。终点必须与下一章的起点衔接 |
| `end_hook.type` | 悬念/信息/情绪 |
| `end_hook.drive` | 读完后"为什么想看下一章"。必须写到具体驱动力 |
| `end_hook.content` | 钩子的具体内容 |
| `characters_active` | 必须可追溯到 volume-XX.md#角色池 |
| `locations` | 必须可追溯到 volume-XX.md#地点池 |
| `plotlines_active` | 推进了哪些线（line id 对应 volume-XX.md#剧情线） |
| `chekhov_set` | 本章新设的契诃夫枪 |
| `chekhov_fire` | 本章回收的契诃夫枪 |
| `info_release` | 本章释放的信息点（item_id/title/source_doc/release_method/density/priority/chapter_context） |

---

## 三、场景规格字段（条件读取）

### 3.1 战斗章（当章节涉及战斗时必填）

| 字段 | 约束 |
|:-----|:------|
| `combat.scale` | 取 `boss战` / `碾压战` / `苦战` / `遭遇战` / `逃亡战` / `围剿战` |
| `combat.purpose` | 剧情目的——触发什么/证明什么/获得什么，而非简单地"打赢" |
| `combat.result` | 取 `完胜` / `惨胜` / `败退` / `被救` / `敌人撤退` / `中断` |
| `combat.reward` | 收获——等级/装备/情报/名声/关系变化/自我认知 |

### 3.2 对话/谈判章

| 字段 | 约束 |
|:-----|:------|
| `dialogue.relation` | 格式 `A(角色) vs B(角色)` + 权力关系 |
| `dialogue.stakes` | 谈崩了会怎样 |
| `dialogue.result` | 取 `达成合作` / `暂时搁置` / `获得线索但未承诺` / `谈判破裂` / `信息交换完成` |
| `dialogue.reward` | 情报/新盟友/新敌人/知道了对方底牌/知道了自己不知道什么 |

### 3.3 探索/发现章

| 字段 | 约束 |
|:-----|:------|
| `discovery.what` | 具体的东西/地点/真相/线索 |
| `discovery.how` | `追踪线索` / `偶然撞见` / `推理推导` / `他人告知` / `战斗中触发的直觉` |
| `discovery.world_expands` | 世界因此变大了什么——一个句子 |
| `discovery.new_options` | 主角因此获得什么新选项 |

### 3.4 危机卷入章

| 字段 | 约束 |
|:-----|:------|
| `crisis.threat` | 威胁是什么——具体 |
| `crisis.scale` | `个人级` / `局部级` / `全城级` / `世界级` |
| `crisis.cannot_escape_because` | 为什么不能逃——具体到地名/人名 |
| `crisis.cost_of_involvement` | 卷入后失去了什么 |

---

## 四、填完后的快速检查

- [ ] ch 连续不跳号
- [ ] 所有 `characters_active` 在 volume-XX.md#角色池 中存在
- [ ] 所有 `locations` 在 volume-XX.md#地点池 中存在
- [ ] 所有 P0 info_release 分配到具体章节
- [ ] 连续 2 章无 info_release 的，第 3 章有追加
- [ ] 第 1 章 info_release ≤ 2
- [ ] end_hook 逐章检查：chN 的钩子 → chN+1 的情绪路径[0] 能衔接
- [ ] payoff_distribution 的 `positions` 与 chapters 中的 payoff.type 对齐
- [ ] 战斗章连续 ≤ 2 章 → 配置过渡章
- [ ] 对话/探索章连续 ≤ 3 章 → 插入动作章
