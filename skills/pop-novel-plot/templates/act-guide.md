# act-XX.yaml 字段计算公式参考

> 产出物: `设计/幕/act-XX.yaml`
> 直接填充模版: `templates/act-skeleton.yaml`
> 管线: pop-novel-plot v4.1+ · Step 9
> 输入: `volume-XX.md` + `状态/角色/` + `情节线草案-XX.md` + `里程碑设计.md`

---

## 一、前置条件

- [ ] volume-XX.md 角色池已产出
- [ ] 状态/角色/角色卡存在
- [ ] 情节线草案-XX.md 已产出
- [ ] 里程碑设计.md 已产出
- [ ] combat_capability.yaml 可读
- [ ] act_rank_schedule.yaml 可读
- [ ] collision_curve.yaml 可读

---

## 二、字段计算公式

### 2.1 幕级定义

| 字段 | 公式/来源 |
|:-----|:----------|
| `core_conflict.description` | 格式 `A vs B`。从情节线草案 M1/M2 核心冲突提取 |
| `core_conflict.stakes` | "失败 = 失去什么"。从终点快照反推——如果主角不败，最差结果 |
| `core_conflict.escalation_path` | 冲突从第1章到最后一章如何升级。`volume-XX.md`的地理扩张暗示冲突升级 |
| `goal.goal` | 格式 `"读者从「X」到「Y」"`。X = ch1读者的初始感受，Y = 卷末期待感受 |
| `tone_note` | 1-3句散文。不用比例，写感受。参考 reader_profile 的消费场景 |

### 2.2 卷末状态

所有字段必须先读 `@source` 声明的上游文件，**不凭记忆**。

| 字段 | 计算公式 |
|:-----|:---------|
| `act_end_state.protagonist.level` | = `act_rank_schedule.yaml → schedule[本卷].end_rank`。**不填别的值** |
| `equipment_gained` | = volume-XX.md#装备变化 → 获得 |
| `equipment_lost` | = volume-XX.md#装备变化 → 消耗/遗失 |
| `mental_state` | = volume-XX.md#角色池 → 主角·卷末心理 |
| `key_relationship_changes` | = volume-XX.md#角色池 → 关系字段 |
| `world.crisis_level` | 从"什么"升级到"什么"。来自情节线草案 M1 推进幅度 |
| `world.faction_changes` | = volume-XX.md → 势力动机·各势力卷末动态 |
| `world.revealed_info` | = act-XX.yaml#info_release_plan → 本卷 P0 已释放列表 |

### 2.3 爽点分布

| 级别 | positions 的确定方式 |
|:-----|:---------------------|
| 微爽点 | 不记位置，every chapter |
| 中爽点 | 参考里程碑设计.md 的 MK 中间节点。4-5章间距 |
| 大爽点 | 参考 collision_curve.yaml 的峰值。每幕2个，间距≥5章 |
| 终极爽点 | 幕末最后1章。参考终点快照的终极目标 |

### 2.4 情绪弧线

`checkpoints` 只标关键转折点（4-6个）。从 collision_curve.yaml 的情绪曲线的峰值取。

### 2.5 情节线定义

从 `情节线草案-XX.md` 提取 `id` / `name` / `desc` / `expected_frequency` / `chekhov_guns`。

### 2.6 章级字段

每章必须填：

| 字段 | 约束 |
|:-----|:-----|
| `ch` | 连续不跳号 |
| `title` | — |
| `word_count` | — |
| `emotional_goal` | 第一性。指导 Design 的情绪靶心 |
| `payoff.type` | 与 `payoff_distribution` 的级别对齐。微爽点章 = "微"，高潮章对应级别 |
| `payoff.trigger` | 具体事件名。与后面章节的 payoff 不重复 |
| `reader_emotion_path` | `[起点, 中间, 终点]`。终点必须与下一章的起点衔接 |
| `end_hook.type` | 悬念/信息/情绪 |
| `end_hook.drive` | 读完后"为什么想看下一章"。必须写到具体驱动力 |
| `end_hook.content` | 钩子的正文内容 |
| `characters_active` | 必须可追溯到 volume-XX.md#角色池 |
| `locations` | 必须可追溯到 volume-XX.md#地点池 |

### 2.7 场景规格字段（条件读取）

**战斗章**（当 `title` / `emotional_goal` 暗示战斗时必填）：

| 字段 | 约束 |
|:-----|:------|
| `combat.scale` | 取 `boss战` / `碾压战` / `苦战` / `遭遇战` / `逃亡战` / `围剿战` |
| `combat.purpose` | 剧情目的——不是"打赢"，而是"触发什么/证明什么/获得什么" |
| `combat.result` | 取 `完胜` / `惨胜` / `败退` / `被救` / `敌人撤退` / `中断` |
| `combat.reward` | 收获——等级/装备/情报/名声/关系变化/自我认知 |
| `combat.capability_ref` | 段位来源路径。先读 combat_capability.yaml 确认 min/max 范围 |
| `combat.monster_ref` | monster_rank_map 中的怪物名。BOSS 标注"掉落装备"的 → volume-XX.md#装备路线图中该装备阶位 ≥ boss段位-1 |

**对话/谈判章**：

| 字段 | 约束 |
|:-----|:------|
| `dialogue.relation` | 格式 `A(角色) vs B(角色)` + 权力关系 |
| `dialogue.stakes` | 谈崩了会怎样 |
| `dialogue.result` | 取 `达成合作` / `暂时搁置` / `获得线索但未承诺` / `谈判破裂` / `信息交换完成` |
| `dialogue.reward` | 情报/新盟友/新敌人/知道了对方底牌/知道了自己不知道什么 |

**探索/发现章**：

| 字段 | 约束 |
|:-----|:------|
| `discovery.what` | 具体的东西/地点/真相/线索 |
| `discovery.how` | `追踪线索` / `偶然撞见` / `推理推导` / `他人告知` / `战斗中触发的直觉` |
| `discovery.world_expands` | 世界因此变大了什么——一个句子 |
| `discovery.new_options` | 主角因此获得什么新选项 |

**危机卷入章**：

| 字段 | 约束 |
|:-----|:------|
| `crisis.threat` | 威胁是什么——具体 |
| `crisis.scale` | `个人级` / `局部级` / `全城级` / `世界级` |
| `crisis.cannot_escape_because` | 为什么不能逃——具体到地名/人名 |
| `crisis.cost_of_involvement` | 卷入后失去了什么 |

---

## 三、填完后的快速检查

- [ ] ch 连续不跳号
- [ ] 所有 `characters_active` 在 volume-XX.md#角色池 中存在
- [ ] 所有 `locations` 在 volume-XX.md#地点池 中存在
- [ ] 所有 P0 info_release 分配到具体章节（参考 act#info_release_plan）
- [ ] 连续 2 章无 info_release 的，第 3 章有追加
- [ ] 第 1 章 info_release ≤ 2
- [ ] end_hook 逐章检查：chN 的钩子 → chN+1 的情绪路径[0] 能衔接
- [ ] payoff_distribution 的 `positions` 与 chapters 中的 payoff.type 对齐
- [ ] 战斗章连续 ≤ 2 章 → 配置过渡章
- [ ] 对话/探索章连续 ≤ 3 章 → 插入动作章
- [ ] `act_end_state.protagonist.level` = `act_rank_schedule → schedule[本卷].end_rank`
