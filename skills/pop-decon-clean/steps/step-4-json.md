# Step 4: 逐章结构化 JSON

> **方向**：将清洗后的逐章正文提取为结构化 JSON。
> **核心约束**：仅提取原文显式存在的内容。不归纳、不推导、不编造。

---

## I/O 注解

| 维度 | 内容 |
|:-----|:-----|
| **读什么** | 清洗后的 `_temp/chapters/chXXX.txt` |
| **做什么** | LLM 提取每章的事件摘要、角色出场、关键对话 → JSON |
| **产出** | `_temp/chapter-data/ch001.json` ... `chNNN.json` |
| **门禁** | JSON 中 event_summaries 为空 → 退回 |

---

## 操作步骤

### 1. 逐章读取清洗后的正文

依次读取 `_temp/chapters/ch001.txt` → `chNNN.txt`。

### 2. LLM 结构化提取指令

```
你是一个网文章节结构化提取助手。从以下章节正文中提取结构化数据。

输出格式为 JSON，字段定义如下：

{
  "chapter_number": 1,                    // 章号（数字）
  "chapter_title": "觉醒",                // 章节标题
  "total_char_count": 2500,               // 正文字数
  "event_summaries": [                     // 事件摘要列表（必须 ≥ 3 条）
    {
      "event_id": "e001",
      "summary": "主角在野外遭遇妖兽袭击，被迫使用隐藏能力",  // 一句话概述
      "characters_involved": ["主角名", "配角名"],          // 参与角色
      "location": "野外森林",                               // 事件发生地点
      "has_dialogue": true                                 // 是否包含对话
    }
    // ... 更多事件
  ],
  "role_appearances": {                    // 角色出场映射
    "角色A": {
      "first_appearance_line": 12,          // 首次出场的段落行号
      "status_in_chapter": "战斗后受伤",    // 本章状态
      "has_dialogue": true,                 // 是否有对话
      "dialogue_count": 3                   // 对话次数
    }
  },
  "key_dialogues": [                       // 关键对话（可选）
    {
      "speaker": "角色A",
      "content": "我不会放弃的！",
      "context": "面对强敌时"
    }
  ],
  "chapter_type": "战斗",                   // 章节类型：战斗/对话/探索/过渡/混合
  "cliffhanger": "主角被逼入绝境，隐藏能力即将暴露"  // 章末悬念（如有）
}

=== 正文开始 ===
{在此粘贴 chXXX.txt 的全文}
=== 正文结束 ===

约束：
1. event_summaries 必须 ≥ 3 条，每条来自原文真实内容
2. role_appearances 只列出本章实际出现的角色
3. key_dialogues 只提取对剧情有推动作用的对话
4. 如果没有悬念，cliffhanger 设为 null
5. 不要编造任何原文不存在的内容
```

### 3. 验证 JSON

每章 JSON 验证：

- `event_summaries` 非空且 ≥ 3 条
- 所有 `characters_involved` 中的角色在 `role_appearances` 中存在
- `total_char_count` 与原文实际字数一致
- JSON 格式合法（可被 `ConvertFrom-Json` 解析）

### 4. 门禁检查（通过/退回）

```
□ _temp/chapter-data/chXXX.json 已写入
□ event_summaries 非空（≥ 3 条）
□ JSON 格式合法
□ 所有参与角色在 role_appearances 中有映射
→ 全部通过 → 当前章完成，继续下一章
→ 未通过 → 退回重新提取
```

---

## 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **无数据** — `chapter-data/chXXX.json` 中 event_summaries 为空仍写入 |
| ❌2 | **编造事件** — 事件摘要内容在原文中不存在 |
| ❌3 | **角色遗漏** — 原文出场的角色在 role_appearances 中不存在 |
| ❌4 | **JSON 格式错误** — 输出为非合法 JSON（无法被标准 JSON 解析）|

---

## 产出

```
_temp/chapter-data/
├── ch001.json
├── ch002.json
├── ...
└── chNNN.json
```

## 下一步

所有 JSON 写入完成 → Phase 1 清洗完毕 → 进入 `pop-decon-design-pack`（Phase 2）
