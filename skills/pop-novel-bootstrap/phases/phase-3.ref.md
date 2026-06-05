> ⚠️ 参考文件。执行 Phase 3 前加载。

# Phase 3 参考：项目骨架模板

## project.yaml schema

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
  # ... 每完成一个置为 true
reader_profile:
  demographic:
    age_range: "18-28"
    reading_scenario: "commute"
  drop_threshold:
    first_3_chapters:
      - "no_power_up_in_3_chapters"
```

## chapter-state.yaml schema

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

## constitution.yaml 模板

```yaml
## 核心情绪基调
tone: "热血 / 黑暗 / 轻松 / 悬疑 / 治愈"

## 禁止清单（主角绝对不能做或世界不可能发生的事）
cant_do:
  - rule: "规则描述"
    example: "正文第X章的例子"  # 给出1个具体例子
    reason: "为什么这条规则存在（人格定位 / 世界规则 / 读者预期）"

## 强制约束（正文写作时必须遵守的铁律）
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

## 角色卡

主角满配 | 配角中配 | 龙套不建文件
