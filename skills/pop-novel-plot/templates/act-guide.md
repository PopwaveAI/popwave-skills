# act-XX.yaml 填写指南

> 产出物: `设计/幕/act-XX.yaml`
> 管线: pop-novel-plot v4.1+ · Step 9
> 输入: `act-XX-人物.md` + `act-XX-地图.md` + `act-XX-势力.md` + `info-release-XX.md` + `情节线草案-XX.md` + `里程碑设计.md`

---

## 0. 这个文件是什么

act-XX.yaml = 一卷大纲的**章级编排层**。它把上游 canvas（人物/地图/势力/信息释放）映射成每章的具体设计。

**它不是**：人物设定（→ act-XX-人物.md）、地图设定（→ act-XX-地图.md）、势力设定（→ act-XX-势力.md）。

**它是**：在 canvas 已经画好的舞台上，编排每一章的"这场戏怎么演"。

### ★ 节奏参考（如有拆书成果）

> 消费 deconstructor T4(爽点分布+Act边界) + T5(高潮分布密度/节奏指纹)。
> 如有参考书拆解报告，在开始编排前：
> □ 读 T4：参考书的爽点分布密度、Act 边界、张力曲线 → 作为本卷 payoff_distribution 的参考上限
> □ 读 T5：参考书的高潮分布密度/节奏指纹 → 作为本卷每章 tension 值的参考坐标

---

## 1. 前置条件（填之前确认）

- [ ] act-XX-人物.md 已产出 —读完，记下角色名和出场章
- [ ] act-XX-地图.md 已产出 —读完，记下地点名和位置关系
- [ ] act-XX-势力.md 已产出 —读完，记下各势力的活跃章段
- [ ] info-release-XX.md 已产出 —上面有 P0/P1 信息点的章级分配
- [ ] 情节线草案-XX.md 已产出 —上面有线定义和交叉图式
- [ ] 里程碑设计.md 已产出 —上面有 MK-01~MK-N 的定义

---

## 1.5 ★ 产出文件有向图规范（NEW v4.3）

> 项目的所有产出文件构成一个有向无环图，不是平面目录。
> 每个文件必须声明两样东西：它消费了上游的哪个文件、它被下游的哪个文件消费。
> 任意两个文件定义了同一概念的值时，值必须一致——来源是唯一的。

### 1.5.1 通用头部格式

每个 Canvas 产出文件的第 1-5 行必须为：

```yaml
<!--
@consumed_by: {下游 Skill}.{Phase}.{文件名} — {取什么字段}
@source: {上游文件} → {取什么字段}    ← 本文件中所有数值字段的来源声明
-->
```

**⚠️ `@source` 不是可选的。如果本文件有任何数值字段（等级/攻击力/章号/段位），该字段必须有且仅有一个 `@source` 声明。不声明来源就填的数值 = 游离数据，和项目其他文件冲突的风险不可控。**

### 1.5.2 七个 Canvas 文件的 @source 模板

| 产出文件 | 必须声明的 @source |
|---------|------------------|
| **act-XX-人物.md** | `@source: 起点快照.md → 主角卷初等级/装备/关系` + `@source: L1-04-物种与天赋.md → 非人类角色的种族 traits/faction` |
| **act-XX-地图.md** | `@source: L1-01-世界蓝图.md → 地理总览段` + `@source: 终点快照.md → 卷末主角所在位置（确认本卷不会超出此范围）` |
| **act-XX-势力.md** | `@source: L1-05-势力格局.md → 势力列表/权力分布/关系网` + `@source: 情节线草案.md → 本卷活跃线（确定势力和哪条线挂钩）` |
| **act-XX-装备.md** | `@source: combat_capability.yaml → ranks[本卷段位].min_attack/max_attack` + `@source: monster_rank_map.yaml → 掉落怪物的段位` + `@source: act_rank_schedule.yaml → schedule[本卷].end_rank` |
| **情节线草案-XX.md** | `@source: act_rank_schedule.yaml → schedule[本卷].end_rank（M3 的卷末等级必须和排期一致）` + `@source: story-engine.yaml → core_conflict_type + world_anchor` |
| **info-release-XX.md** | `@source: L1-01~06 → 各 L1 文件的字段名（确保引用的 source_doc 路径可达）` |
| **act-XX.yaml** | `@source: 情节线草案 → 线定义` + `@source: 里程碑设计 → MK 列表` + `@source: act-XX-人物/地图/势力/装备/info-release → 各自的章级分配` |

### 1.5.3 有向图全貌（在脑中而非文件中）

```
                    ┌─────────────────────────┐
                    │  L1-01~06（bookstrap）    │
                    └───┬──┬──┬──┬──┬────────┘
                        │  │  │  │  │
         ┌──────────────┤  │  │  │  └──→ act-XX-装备.md 只读 combat_capability
         │   ┌──────────┤  │  │  └────→ act-XX-势力.md  只读 L1-05
         │   │   ┌──────┤  │  └───────→ act-XX-人物.md  只读 L1-04
         │   │   │      │  └──────────→ act-XX-地图.md  只读 L1-01
         │   │   │      └─────────────→ info-release    只读 L1-01~06
         ▼   ▼   ▼
    ┌──────────────────────────────────────┐
    │   起点快照 → 里程碑设计 → 终点快照      │
    │   情节线草案（从 schedule 取卷末排期）   │
    └────────────────┬─────────────────────┘
                     │
                     ▼
              act-XX.yaml
                     │
                     ▼
              pop-novel-writer
```

**规则**：任何两个文件如果定义了同一概念的值（卷末等级/段位/攻击力范围），该值在 adt-XX.yaml 中做最终收敛。act-XX.yaml 的产出自检（§9）强制校验值一致性。

---

## 2. YAML 整体结构

产出是一个 YAML 文件，顶层结构如下：

```yaml
_meta:          # 元数据 + canvas 引用
act:            # 幕级定义
  core_conflict:
  goal:
  tone_note:
  act_end_state:
  payoff_distribution:
  emotional_arc:
  plotlines:    # 情节线定义（从情节线草案提取关键字段）
  chapters:     # 章级切片（填 20-30 个章节对象）
```

---

## 3. _meta — 元数据与 canvas 引用

```yaml
_meta:
  version: "v4.1"
  target_platform: "番茄小说|起点中文网|..."
  reader_persona: "目标读者画像（一句话）"
  canvas_refs:           # ★ 声明本 yaml 依赖的 canvas 文件
    - "设计/幕/act-XX-人物.md"
    - "设计/幕/act-XX-地图.md"
    - "设计/幕/act-XX-势力.md"
    - "设计/幕/info-release-XX.md"
    - "设计/幕/情节线草案-XX.md"
    - "设计/里程碑设计.md"
```

> `canvas_refs` 是给 writer 的一条声明："我是在这些文件的基础上设计的"——writer 据此知道去哪里取人物/地图/势力的具体内容。

---

## 4. act 幕级定义

### 4.1 core_conflict — 核心冲突

用一句话说清本幕的核心对抗。格式：**A vs B**。

| 字段 | 类型 | 说明 | 示例 |
|:-----|:-----|:-----|:-----|
| `description` | string | 核心对抗，一针见血 | "张北辰 vs 神霄派雷主投影" |
| `stakes` | string | 失败 = 失去什么 | "南疆城全灭，左千户被杀，苏九音被神霄派回收" |
| `escalation_path` | string | 冲突如何从第1章升温到最后一章 | "孤独对抗 → 结盟锦衣卫 → 发现朝廷阴谋 → 正面雷主" |

### 4.2 goal — 幕级目标

| 字段 | 说明 | 示例 |
|:-----|:-----|:-----|
| `goal` | 读者体验目标，格式："读者从「X」到「Y」" | "读者从「师父走了世界好可怕」到「主角有戏，追」" |

### 4.3 tone_note — 情绪基调

1-3 句散文。覆盖：情绪配比、节奏特点、读者感受预期。

> 不要写 "热血50% + 好奇30%…" 这种机械比例，写散文。

### 4.4 act_end_state — 卷末状态

> **与 act-XX-人物.md 的关系**：act-XX-人物.md 是详细的卷初→卷末角色对照，这里的 act_end_state 只提取关键的结构化字段供 writer 快速解析。

| 路径 | 字段 | 说明 | @source |
|:-----|:-----|:-----|:--------|
| `protagonist.level` | string | 等级/境界变化 | **act_rank_schedule.yaml → schedule[本卷].end_rank**。不填别的数字——此值必须和排期一致。 |
| `protagonist.equipment_gained` | string[] | 获得的关键装备 | act-XX-装备.md → 装备变化清单·获得 |
| `protagonist.equipment_lost` | string[] | 消耗/遗失的装备 | act-XX-装备.md → 装备变化清单·消耗/遗失 |
| `protagonist.mental_state` | string | 心智状态变化 | act-XX-人物.md → 主角·卷末心理状态 |
| `protagonist.key_relationship_changes` | string[] | 关系变化（如 "左千户从怀疑→信任"） | act-XX-人物.md → 角色的关系字段 |
| `world.crisis_level` | string | 世界危机从什么升级到什么 | 情节线草案 → M1 本卷推进幅度 |
| `world.faction_changes` | string[] | 势力格局变化 | act-XX-势力.md → 各势力卷末动态 |
| `world.revealed_info` | string[] | 新揭示的世界观关键信息 | info-release-XX.md → P0 信息点·本卷已释放 |

### 4.5 equipment_flow — 装备/资源变化表

> 只列"在哪个章节节点有装备变化"，详细描述见 act-XX-装备.md。

每个条目：

| 字段 | 类型 | 说明 | 可取值 |
|:-----|:-----|:-----|:-------|
| `item` | string | 物品名 | |
| `chapter` | int | 发生在哪章 | |
| `action` | string | 动作 | `获得` / `消耗` / `升级` / `遗失` |
| `significance` | string | 一句话：对后续剧情的影响 | |

示例：
```yaml
equipment_flow:
  - item: "北极驱邪院令牌"
    chapter: 1
    action: "获得"
    significance: "师父坐化前传给主角——全书核心装备"
  - item: "令牌"
    chapter: 20
    action: "升级"
    significance: "第4道裂痕→主角不再依赖令牌本身"
```

### 4.6 payoff_distribution — 爽点分布

| 级别 | 铺垫-释放比 | frequency | positions | design |
|:----|:----------|:----------|:----------|:-------|
| 微爽点 | 2:1 | 每章1-2个 | — | 每章通过什么给获得感 |
| 中爽点 | 4:1 | 每4-5章1个 | [3,7,11,...] | 每个中爽点事件名 |
| 大爽点 | 8-10:1 | 每幕2个 | [10,20] | 大爽点事件名 |
| 终极爽点 | 20:1 | 幕末1个 | [20] | 终极爽点事件名 |

> positions 数组里的数字 = 章节号。必须与 chapters 数组的 ch 字段一致。

### 4.7 emotional_arc — 情绪弧线检视点

> 只标 **关键转折点**（通常 4-6 个），不是每章都标。每章的情绪设计在 chapters[] 里。

每个检视点：

| 字段 | 说明 |
|:-----|:-----|
| `chapter` | 转折发生在哪章 |
| `emotion` | 情绪描述（如 "震撼+好奇"） |
| `intensity` | 1-10 |
| `hook` | 该点的钩子 |

overview 是一句话概览："起点情绪 → 中间情绪 → 终点情绪"。

---

## 5. plotlines — 情节线定义

> 直接从 `情节线草案-XX.md` 提取关键字段。M1/M2/M3 必选，S 线可选 1-3 条。

每条线：

| 字段 | 说明 |
|:-----|:-----|
| `id` | M1 / M2 / M3 / S1 / S2 / S3 |
| `name` | 线名 |
| `desc` | 一句话：这条线是什么 |
| `expected_frequency` | 每N章（描述性文本） |
| `chekhov_guns` | 这条线上的契诃夫枪列表 |

契诃夫枪子字段：
- `name` — 枪名
- `setup_ch` — 设伏章
- `payoff_ch` — 回收章
- `desc` — 这把枪是什么、为什么重要

---

## 6. chapters — 章级切片

> 这是 act-XX.yaml 最核心的部分。每章一个对象，按章节顺序排列。

### 6.1 每章必须包含的字段

#### 基础

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `ch` | int | 章节号 |
| `title` | string | 章标题 |
| `word_count` | int | 预期字数 |

#### 情绪设计

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `emotional_goal` | string | 本章想让读者感受到什么（第一性） |
| `payoff.type` | string | `微` / `中` / `大` / `终极` |
| `payoff.trigger` | string | 爽点触发方式 |
| `payoff.reader_feeling` | string | 读者获得什么 |
| `reader_emotion_path` | string[] | 三元素：`[起点, 中间, 终点]` |

#### ★ 战斗规格（v4.2 — 当本章涉及战斗时必填）

> plot 层只管"这是什么性质的战斗"——规格/目的/结果/收获。具体怎么打归章纲层。

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `combat.scale` | string | `boss战` / `碾压战` / `苦战` / `遭遇战` / `逃亡战` / `围剿战` |
| `combat.purpose` | string | 剧情目的——"触发血脉第一次有意识借用" / "证明实力站稳码头" |
| `combat.result` | string | `完胜` / `惨胜` / `败退` / `被救` / `敌人撤退` / `中断` |
| `combat.reward` | string | 收获——等级/装备/情报/名声/关系变化/自我认知 |
| `combat.capability_ref` | string | 段位战力来源 → `{项目}/数值体系/combat_capability.yaml` 中的 rank name。如 `"武僧·低阶(1-3级)"`。填写前必须先读 combat_capability.yaml 确认该段位的 min/max 攻击范围，然后根据敌我段位差设计战斗难度。 |
| `combat.monster_ref` | string | 怪物等级来源 → `{项目}/数值体系/monster_rank_map.yaml` 中的 monster name。如 `"教团打手·10级平民/3级战士"`。如为 BOSS 级且标注"掉落装备"，act-XX-装备.md 中该装备的阶位 ≥ monster 段位 - 1。 |

#### ★ 对话/谈判规格（v4.2 — 当本章核心是重要对话或谈判时必填）

> plot 层只管"这场对话是什么性质"——权力关系/筹码/结果。具体怎么谈归章纲层。

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `dialogue.relation` | string | 双方权力关系——"江轩(被注视者) vs 阴影假面(试探者)" / "平等对峙" / "单方压制" |
| `dialogue.stakes` | string | 赌注——"谈崩了=教团信息断线，江轩继续盲打" |
| `dialogue.result` | string | 对话结果——`达成合作` / `暂时搁置` / `获得线索但未承诺` / `谈判破裂` / `信息交换完成` |
| `dialogue.reward` | string | 收获——情报/新盟友/新敌人/了解了对方底牌/知道了自己不知道什么 |

#### ★ 发现/探索规格（v4.2 — 当本章核心是主角发现某物/某地/某真相时必填）

> plot 层只管"发现了什么、怎么发现的、世界因此变大了多少"。具体怎么发现归章纲层。

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `discovery.what` | string | 发现了什么——具体的东西/地点/真相/线索 |
| `discovery.how` | string | 发现方式——`追踪线索` / `偶然撞见` / `推理推导` / `他人告知` / `战斗中触发的直觉` |
| `discovery.world_expands` | string | 发现后世界变大了什么——"知道了教团在码头底下有据点" / "原来不止自己一个人有这种血脉" |
| `discovery.new_options` | string | 主角获得了什么新选项——"可以去找阴影假面摊牌" / "必须做选择:逃还是查" |

#### ★ 危机卷入规格（v4.2 — 当本章核心是外部威胁降临、主角被动卷入时必填）

> plot 层只管"什么威胁、多大规模、为什么不能跑"。具体怎么卷入归章纲层。

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `crisis.threat` | string | 威胁是什么——"教团在码头区公开抓人" / "一夜之间失踪十几个人" |
| `crisis.scale` | string | 规模——`个人级(只针对主角)` / `局部级(码头区)` / `全城级(琥珀城)` / `世界级(圣者浩劫)` |
| `crisis.cannot_escape_because` | string | 为什么不能逃——"身后是小石藏身的仓库" / "跑了教团会追到天涯海角" |
| `crisis.cost_of_involvement` | string | 卷入后主角失去了什么——"失去了'安分过日子'的选项" / "被打上教团的追杀名单" |

#### 钩子

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `end_hook.type` | string | `悬念` / `信息` / `情绪` |
| `end_hook.drive` | string | 驱动力 |
| `end_hook.content` | string | 钩子内容 |

#### 情节线推进

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `plotlines_active` | string[] | 本章推进了哪些线（填 plotlines.id） |
| `chekhov_set` | string[] | 本章设伏的枪（格式：`{线id}.{枪名}`） |
| `chekhov_fire` | string[] | 本章回收的枪（格式同上） |

#### 里程碑

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `milestone_active` | string | 本章推进的 MK 编号，可为空 |
| `milestone_progress` | string | `start` / `mid` / `complete`，可为空 |

#### 信息释放

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `info_release[].item_id` | string | 设定项 ID |
| `info_release[].title` | string | 设定项标题 |
| `info_release[].source_doc` | string | L1 设定文件路径（writer 凭此读取原文） |
| `info_release[].release_method` | string | `实战展示` / `角色对话` / `叙事者说明` / `探索发现` |
| `info_release[].density` | string | `集中爆发` / `均匀撒放` / `埋伏笔` |
| `info_release[].priority` | string | `P0` / `P1` |
| `info_release[].chapter_context` | string | 在本章的哪个场景释放 |

#### ★ Canvas 消费字段（NEW v4.1）

> 这些字段声明本章消费了哪些 canvas 产物。writer 凭此去对应文件取详细内容。

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `characters_active` | string[] | 本章登场的角色名（必须存在于 act-XX-人物.md） |
| `locations` | string[] | 本章发生的地点（必须存在于 act-XX-地图.md） |

---

### 6.2 章节填写示例

```yaml
chapters:
  - ch: 1
    title: "师父坐化了"
    word_count: 2500

    emotional_goal: "让读者感到孤独和压迫——全书最安静也最沉重的一章"
    payoff:
      type: "微"
      trigger: "师父坐化前递给主角令牌"
      reader_feeling: "主角被迫接过责任——读者感到 '不走不行了'"
    reader_emotion_path: ["悲伤", "无力", "被推着往前走"]

    end_hook:
      type: "悬念"
      drive: "令牌传来刺痛——它认出你了，不是你在用它，是它在用你"
      content: "主角低头看手心，一道裂痕正在蔓延"

    plotlines_active: ["M1", "M2"]
    chekhov_set: ["M1.师父最后一句话"]
    chekhov_fire: []

    milestone_active: "MK-01"
    milestone_progress: "start"

    info_release:
      - item_id: "世界观.百诡昼行"
        title: "百诡昼行现象"
        source_doc: "00-原始设定/L1-元设定层/02-世界观表层规则.md"
        release_method: "环境展示"
        density: "埋伏笔"
        priority: "P0"
        chapter_context: "主角走出道观，看到第一处诡异降临的场景——井口冒黑烟"

    characters_active: ["张北辰", "师父"]       # ← 从 act-XX-人物.md
    locations: ["荒村道观"]                     # ← 从 act-XX-地图.md

    # ★ 非战斗章 → 无 combat 字段

  - ch: 2
    title: "井口之手"
    word_count: 2200

    emotional_goal: "第一次正面冲突——让读者攥紧拳头"
    payoff:
      type: "中"
      trigger: "井口伸出的手抓住主角脚踝→挣脱反击"
      reader_feeling: "肾上腺素拉满——这个主角能打！"

    combat:                                      # ★ 战斗章必填
      scale: "遭遇战"
      purpose: "展示主角在绝境中的第一反应——证明他不是被动等死的人"
      result: "惨胜"
      reward: "手臂受伤但活下来了。初步认知到危机不是幻觉——世界观可信度+1"

    reader_emotion_path: ["警觉", "恐惧", "燃烧"]
    end_hook:
      type: "悬念"
      drive: "井里还有东西在动——不止一只手"
      content: "主角低头看井口深处，黑暗中有两点微光亮了一下。那不是水面的反光。"

    plotlines_active: ["M1", "M2"]
    chekhov_set: ["M1.井中之物"]
    chekhov_fire: []

    milestone_active: "MK-01"
    milestone_progress: "mid"

    info_release:
      - item_id: "世界观.百诡昼行"
        title: "诡异生物初次接触"
        source_doc: "00-原始设定/L1-元设定层/02-世界观表层规则.md"
        release_method: "实战展示"
        density: "集中爆发"
        priority: "P0"
        chapter_context: "井口战斗——主角第一次和诡异生物近距离接触"

    characters_active: ["张北辰"]
    locations: ["荒村井口"]
```

---

## 7. 章节号连续性检查

chapters 数组的 ch 字段必须连续（1, 2, 3... 不跳号），且起止章与 chapter_range 一致。

---

## 8. 常见错误

| 错误 | 原因 | 正确做法 |
|:-----|:-----|:---------|
| plotlines_active 里出现不存在的线 id | 没有与 plotlines 定义对齐 | 先完成 plotlines 定义，再填每章 |
| characters_active 里的角色不在 act-XX-人物.md | 角色没在 canvas 中定义 | 先确保 act-XX-人物.md 包含该角色 |
| locations 里的地点不在 act-XX-地图.md | 地点没在 canvas 中定义 | 先确保 act-XX-地图.md 包含该地点 |
| info_release[].source_doc 路径错误 | 没有与 L1 目录对齐 | 严格按照 `00-原始设定/L1-元设定层/XX.md` 格式 |
| 同一个 info 项在 3 章内重复释放 | 信息释放过密 | 每个设定知识 ≥ 3 章间隔 |
| chapters 的 milestones 与里程碑设计.md 不同步 | 两边独立维护 | 填完 chapters 后对照里程碑设计.md |
| end_hook 和下一章 emotional_goal 不衔接 | 钩子指向的情绪跟下一章开篇情绪断裂 | 检查相邻两章：chN 的 end_hook.drive → chN+1 的 reader_emotion_path[0] |

---

## 9. 产出自检

### 文件级
- [ ] 七个 Canvas 产出文件的头部均含 `@consumed_by` 和 `@source` 声明
- [ ] `_meta.canvas_refs` 列出所有上游 canvas 文件
- [ ] 所有 `characters_active` 的角色在 act-XX-人物.md 中存在
- [ ] 所有 `locations` 的地点在 act-XX-地图.md 中存在

### 值一致性（NEW v4.3 — 跨文件校验）
> 任何两个文件定义了同一概念的值时，act-XX.yaml 做最终收敛。以下检查全部基于 @source 声明路径反向验证。

- [ ] **段位对齐**：`act_end_state.protagonist.level` = `act_rank_schedule.yaml → schedule[本卷].end_rank`（从 @source 路径逐读验证，不靠记忆）
- [ ] **装备数值在段位范围内**：act-XX-装备.md 中每件核心装备的攻击力在 `combat_capability.yaml → ranks[对应段位].min_attack ~ max_attack` 区间内
- [ ] **BOSS 掉落装备段位 ≥ BOSS 段位 - 1**：蛇魔(3阶) → 蛇魔剑 ≥ 2阶。在 monster_rank_map 中标记"掉落装备"的怪物，act-XX-装备 中该装备的阶位不低于对应规则
- [ ] **情节线草案 M3 卷末等级 = act_rank_schedule 的 end_rank**（不从情节线草案直接取，从 act_rank_schedule 反向读）
- [ ] **act_end_state.world.faction_changes 与 act-XX-势力.md 的卷末动态一致**（势力在卷末的存活/消亡/崛起状态不矛盾）

### 章级
- [ ] 所有 chapters 的 `ch` 连续不跳号
- [ ] 所有 `plotlines_active` 的值在 `plotlines` 定义中存在
- [ ] 所有 P0 info_release 都已分配到具体章节
- [ ] 连续 2 章无 info_release 的，第 3 章有追加
- [ ] 第 1 章 info_release 数量 ≤ 2
- [ ] 契诃夫枪的 payoff_ch 不早于 setup_ch，且不超出本卷范围
- [ ] end_hook 逐章检查：chN 的钩子 → chN+1 的情绪路径起点能衔接
