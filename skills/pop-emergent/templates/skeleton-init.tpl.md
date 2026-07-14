# 骨架初始化模板

> 用途：pop-emergent 初始化项目时复制此模板创建空壳文件
> 契约：骨架定义见 `../references/v3.5-pipeline-prd.md` §4.1，owner 见 §4.2，元数据协议见 §5

## 目录树

```text
涌现/
  current-state.md          # 入口层：下一章写作唯一入口包（full-required）
  soul.md                   # 入口层：主卖点+叙事魂+正文气口；可含DNA长期融合策略（full-required）
  seed-种子文档.md          # 库层：长期承诺和故事宪法
  research-写作燃料.md      # 库层：燃料池（唯一名称，禁用"燃料库.md"）
  content-mechanics.md      # 库层：题材机制和参考机制分流
  设定库.md                 # 库层：已确认设定事实
  人物库.md                 # 库层：人物最新状态
  剧情线.md                 # 库层：伏笔、债务、中长线推进
  review-沉淀.md            # 历史层：审稿日志（append-only）
  压缩归档/                 # 历史层：current-state 旧版
    current-state-{YYYYMMDD}-{章位}.md
  正文/                     # 产出层：章节正文
    {书名}-第{N}章-{标题}.txt
写作资产/
  文风库/                   # 章内文风DNA源，由 pop-shared-dna 产出
    {作品}.md
```

## 空壳文件元数据块模板

### current-state.md

```markdown
---
doc_type: current-state
role: 下一章写作唯一入口包
read_policy: full-required
compression: forbid
primary_consumer: write
source_of_truth: true
last_updated: YYYY-MM-DD
---

# Current State

（正文待 review 填充）

## 本章DNA执行包
未启用
```

### soul.md

```markdown
---
doc_type: soul
role: 主卖点 + 叙事魂 + 正文气口
read_policy: full-required
compression: forbid
primary_consumer: write
source_of_truth: true
last_updated: YYYY-MM-DD
---

# Soul

（正文待 seed 填充）

## 文风DNA融合策略
未启用
```

### seed-种子文档.md

```markdown
---
doc_type: seed
role: 长期承诺和故事宪法
read_policy: full-if-targeted
compression: forbid
primary_consumer: review
source_of_truth: true
last_updated: YYYY-MM-DD
---

# Seed 种子文档

（正文待 seed 填充）
```

### research-写作燃料.md

```markdown
---
doc_type: fuel
role: 燃料池
read_policy: full-if-targeted
compression: allow-into-current-state
primary_consumer: review
source_of_truth: true
last_updated: YYYY-MM-DD
---

# Research 写作燃料

（正文待 research 填充）
```

### content-mechanics.md

```markdown
---
doc_type: mechanics
role: 题材机制和参考机制分流
read_policy: full-if-targeted
compression: allow-into-current-state
primary_consumer: review
source_of_truth: true
last_updated: YYYY-MM-DD
---

# Content Mechanics

（正文待 research 填充）
```

### 设定库.md

```markdown
---
doc_type: setting
role: 已确认设定事实
read_policy: index-only
compression: allow-into-current-state
primary_consumer: review
source_of_truth: true
last_updated: YYYY-MM-DD
---

# 设定库

（正文待 review 填充）
```

### 人物库.md

```markdown
---
doc_type: character
role: 人物最新状态
read_policy: index-only
compression: allow-into-current-state
primary_consumer: review
source_of_truth: true
last_updated: YYYY-MM-DD
---

# 人物库

（正文待 review 填充）
```

### 剧情线.md

```markdown
---
doc_type: plotline
role: 伏笔、债务、中长线推进
read_policy: index-only
compression: allow-into-current-state
primary_consumer: review
source_of_truth: true
last_updated: YYYY-MM-DD
---

# 剧情线

（正文待 review 填充）
```

### review-沉淀.md

```markdown
---
doc_type: review-log
role: 审稿日志（append-only）
read_policy: index-only
compression: forbid
primary_consumer: human
source_of_truth: true
last_updated: YYYY-MM-DD
---

# Review 沉淀

（正文待 review 追加）
```

## 注意

- emergent 只建空壳，不填写任何文件正文内容。
- 正文目录 `正文/` 和归档目录 `压缩归档/` 只建空目录，不放占位文件。
- 所有长期文档必须带元数据块（PRD §5）。
