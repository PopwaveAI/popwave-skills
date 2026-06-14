# 输入规范

### 方式 A：结构化 Markdown / YAML（推荐）

```markdown
---
type: dashboard|list|detail|card-deck|knowledge|timeline|network|gallery|reader
title: "页面标题"
description: "页面描述/副标题"
source: "来源 skill 名称"
---
```

### 方式 B：纯结构化 YAML（pop-shared-reader 新格式）

```yaml
volume_stats:
  total_chapters: 59
  total_characters: 42
  core_characters: 8
chapters:
  ch1:
    title: "初入战警"
    entities: ["陈昂", "暴风女"]
    tone: "强势登场"
characters:
  - name: "陈昂"
    role: "主角"
    image_prompt: "..."
scenes:
  - title: "帝国大厦宣告"
    image_prompt: "..."
entity_cooccurrence:
  - pair: "陈昂 ↔ 左冷禅"
    chapters: 8
```

> 收到 `.yaml` 文件时自动按此格式解析。`volume_stats` → 指标卡片，`chapters` → 时间线/阅读器，`entity_cooccurrence` → 关系图谱。

### 方式 C：直接数据结构

直接传入 JSON/YAML 数据结构（通过对话上下文）。
