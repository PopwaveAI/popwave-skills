# Step 1: 读每章 JSON

> **方向**：消费 Phase 1 产出的逐章 JSON，提取事件链基底。
> **核心约束**：仅读取，不修改 JSON 内容。JSON 缺失的章节跳过并记录。

---

## I/O 注解

| 维度 | 内容 |
|:-----|:-----|
| **读什么** | `_temp/chapter-data/ch001.json` ... `chNNN.json` |
| **做什么** | 提取 event_summaries、role_appearances、key_dialogues |
| **产出** | 每章的事件链基底（原文事件摘要列表） |
| **门禁** | JSON 缺失 → 跳过该章并记录日志 |

---

## 操作步骤

### 1. 验证 Phase 1 产出

```
□ _temp/chapter-data/ 目录存在且非空
□ 获取文件列表：ch001.json → chNNN.json
□ 记录缺失的章号（如有）
```

### 2. 逐章读取 JSON

对每章执行：

```python
# 伪代码逻辑
json_data = read_json("_temp/chapter-data/chXXX.json")

extracted_baseline = {
    "chapter_number": json_data.chapter_number,
    "chapter_title": json_data.chapter_title,
    "total_char_count": json_data.total_char_count,
    "event_summaries": json_data.event_summaries,          # 核心数据：事件摘要列表
    "role_appearances": json_data.role_appearances,         # 角色出场信息
    "key_dialogues": json_data.key_dialogues,               # 关键对话
    "chapter_type": json_data.chapter_type,                 # 章节类型
    "cliffhanger": json_data.cliffhanger                    # 章末悬念
}
```

### 3. 检查数据质量

| 检查项 | 通过条件 | 失败处理 |
|:-------|:---------|:---------|
| event_summaries 数量 | ≥ 3 条 | 标注「本章内容简略」，按实际数量继续 |
| role_appearances 非空 | 至少 1 个角色 | 标注「本章无角色出场」|
| 数据一致性 | role_appearances 覆盖所有 event_summaries 出现的角色 | 记录缺失的角色名 |

### 4. 产出：事件链基底

每章产出事件链基底，格式示例：

```json
{
  "ch001": {
    "chapter_number": 1,
    "title": "觉醒",
    "baseline_events": [
      {"id": "e001", "summary": "主角在野外遇袭", "roles": ["主角"], "location": "野外"},
      {"id": "e002", "summary": "主角反击妖兽", "roles": ["主角"], "location": "野外"},
      {"id": "e003", "summary": "神秘人出手相救", "roles": ["主角", "神秘人"], "location": "野外"}
    ],
    "data_quality": {
      "has_minimum_events": true,
      "role_coverage_complete": true,
      "notes": []
    }
  }
}
```

### 5. 门禁检查（通过/跳过）

```
□ _temp/chapter-data/ 目录存在且非空
□ 已处理 N 章 JSON，跳过 M 章（缺失）
□ 每章至少 1 个事件摘要
→ 全部通过（或跳过已标注章节）→ 进入 Step 2
→ 全部缺失 → 退回 Phase 1（pop-decon-clean）
```

---

## 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **目录不存在仍继续** — `_temp/chapter-data/` 不存在却假装 Phase 1 已完成 |
| ❌2 | **跳过不记录** — JSON 缺失的章跳过后不记录日志，导致最终设计包缺章不可追溯 |

---

## 产出

每章内存中的事件链基底（作为 Step 2 的输入）

## 下一步

Step 1 完成 → 进入 Step 2：填充事件链
