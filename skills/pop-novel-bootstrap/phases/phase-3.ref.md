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
[一句话]

## 禁止清单
- ❌ 规则1...

## 强制约束
- ✅ 约束1...
```

## 角色卡

主角满配 | 配角中配 | 龙套不建文件
