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
  outline: "02-大纲/"
  settings: "00-原始设定/"
  chapters: "03-正文/"
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

### 3. 宪法文件
产出 `constitution.yaml`：

```yaml
tone: "热血 / 黑暗 / 轻松 / 悬疑 / 治愈"

cant_do:
  - rule: "规则描述"
    example: "正文第X章的例子"
    reason: "为什么这条规则存在（人格定位 / 世界规则 / 读者预期）"

must_do:
  - rule: "规则描述"
    example: "规则对应的正文示例"
    reason: "为什么这是强制约束（平台节奏 / 核心情绪 / 读者承诺）"
```

**示例**（以遮天为参考）：

```yaml
tone: "宏大·苍凉"

cant_do:
  - rule: "主角不杀普通人"
    example: "ch5 叶凡放过挑衅的同门"
    reason: "荒古圣体传人的定位——不屑于对弱者动手"
  - rule: "越级战斗不能没有代价"
    example: "ch12 越级杀妖兽后卧床三天"
    reason: "力量体系中的跨级约束必须遵守"

must_do:
  - rule: "每20章至少一次境界突破或实力跃迁"
    example: "ch1-20 轮海突破"
    reason: "平台节奏要求，读者期待成长可见"
  - rule: "战斗必须有决策（不只是数值对抗）"
    example: "ch18 用地形伏击代替正面硬拼"
    reason: "L1 力量体系设定——战斗是策略不是对砍"
```

### 4. 章状态（初始快照）

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

### 5. 角色卡
主角满配（背景/动机/成长/关系网/金手指联动）
重要配角中配 → `02-大纲/L3-角色层/`
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

### 6. 数据库
`04-数据库/novel.db`

### 7. 追踪面板
`00-总控/project-status.html`
