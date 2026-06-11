# Phase 3：项目骨架创建

> 该文件同时作为执行指令和参考指南，无需加载外部 ref 文件。

## 前置条件
Phase 1.5 稳定性检验通过。

## 执行步骤

### 1. 目录结构
按 `references/产出目录结构.md` 创建

### 2. 总控配置
产出 `00-总控/project.yaml`：

```yaml
project:
  name: "书名"
  platform: "fanqie / qidian"
  start_date: "YYYY-MM-DD"
  target_words: 2000000
paths:
  outline: "设计/"
  settings: "00-原始设定/"
  chapters: "正文/"
phase_progress:
  phase_0: true
  # 每完成一个置为 true
reader_profile:
  demographic:
    age_range: "18-28"
    reading_scenario: "commute"
  drop_threshold:
    first_3_chapters:
      - "no_power_up_in_3_chapters"
```

### 3. 章状态（初始快照）

产出 `00-总控/chapter-state.yaml`：

```yaml
current_chapter: 0
next_chapter: 1
protagonist:
  rank: 1
  military_rank: "无品"
  merits: 0
  equipment:
    armor: null
    primary: null
    secondary: null
  enhancements: []
location: "未进入"
party: []
timeline:
  world_time: "第1天"
flags: []
```

> **重要：chapter-state.yaml 是 bookstrap 阶段的初始值快照，仅供首次写作前参考。**
> 写作开始后，状态追踪的唯一 canonical 来源是 **`entity-snapshot.yaml`**（由 Writer Step 3 从所有章末 delta 聚合生成）。
> entity-snapshot.yaml 由 Writer 自动维护；如文件损坏/丢失，重新运行 Writer Step 3.3 聚合即可恢复（源数据在每章正文末尾）。
> 路径注册中心是 project.yaml 的 `paths` 字段 —— 所有 skill 从那里读取目录路径，不硬编码。

### 4. 角色卡
主角满配（背景/动机/成长/关系网/金手指联动）
重要配角中配 → `状态/角色/`
龙套不建文件

**★ 主角成长轨迹（NEW v2.1 — 供 plot A级逐章状态表消费）**

```
在主角卡末尾追加「成长轨迹」段，格式：

## 成长轨迹（供 plot 消费）
| 章段 | 等级/阶位 | 关键属性变化 | 解锁能力 | 关键装备 | 心智变化 |
|:-----|:---------|:----------|:--------|:--------|:--------|
| ch01 | {起点} | — | 面板激活 | 无 | {初始心理} |
| ch02 | {首次变化} | {具体数字} | {首次技能} | {首件装备} | {变化} |
| ... | ... | ... | ... | ... | ... |
| ch22 | {卷末} | {卷末数字} | {卷末技能} | {卷末装备} | {卷末心理} |

规则：
- 22章=22行。不确定的章段允许留{待plot填充}，但章号必须连续
- 等级/阶位从本项目的 combat_capability.yaml#ranks[].name 读取——不同的项目有不同的阶位命名体系
- 属性字段从 combat_capability.yaml 读取——不预设为"力量/敏捷/智力"还是"灵力/神识"
- 如果项目没有 combat_capability.yaml → 角色卡跳过成长轨迹段，由 plot 独立填充
```

> 主角卡的角色名、性格特质、动机等由 L1 设定和 story-engine 决定，不在此模板预设。

**★ 核心欲望（NEW — 供 plot A级角色消费）**

在主角卡和重要配角卡中追加 `core_desire` 字段，拆为两层：

```yaml
core_desire:
  external_goal: "成为天榜第一"          # 外在目标：他要做什么
  internal_need: "证明父亲当年没有看错他"  # 内在需求：他为什么做
```

- external_goal 驱动情节（读者能看到的行动方向）
- internal_need 驱动人物成长（读者能共情的底层动机）
- 两者冲突时 → 人物弧光出现（"他想成为天榜第一，但他的内心需要父亲认可——他做的一切都是向外求"）
- 不面向龙套角色（只填谁吃谁的关系）

### 5. 数据库
`04-数据库/novel.db`

### 6. 追踪面板
`00-总控/project-status.html`
