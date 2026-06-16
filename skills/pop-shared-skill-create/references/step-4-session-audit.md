# Step 4：会话审计模式 — 数据驱动分析

> **定位：** 从 Hermes state.db 读取真实会话执行数据，分析 agent 行为与 SKILL.md 要求的偏差，产出带定量证据的改进提案。
> **前置条件：** `state.db` 可读，目标 `session_id` 已知。
> **产出：** 审计报告，归档到 `prd/02-问题诊断/{编号}-{描述}.md`。

---

## 4.1 连接数据源

```python
import sqlite3

db_path = r"D:\novel-test\state.db"  # 或 $HERMES_HOME/state.db
conn = sqlite3.connect(db_path)
cur = conn.cursor()
session_id = "20260615_113419_c9b495"
```

## 4.2 会话元数据

```python
cur.execute("""
    SELECT id, title, source, model, message_count, tool_call_count,
           input_tokens, output_tokens, cwd
    FROM sessions WHERE id = ?;
""", (session_id,))
```

关键字段：

| 字段 | 含义 | 审计价值 |
|:-----|:------|:---------|
| `message_count` | 消息总数 | 会话长度，>150 需关注上下文膨胀 |
| `tool_call_count` | 工具调用次数 | 写操作占比，>50 需关注 write payload |
| `input_tokens` | 输入 token 量 | 上下文大小基线，与模型窗口对比 |

## 4.3 膨胀源定位（核心步骤）

### 4.3.1 助理消息大小分布

```python
cur.execute("""
    SELECT id, length(content) as clen FROM messages
    WHERE session_id = ? AND role='assistant' ORDER BY id ASC;
""", (session_id,))
```

**红线检查：** SKILL.md 要求写入文件后助理消息 ≤200 字。超过 500 字的助理消息就是违规。

### 4.3.2 tool_calls 膨胀（主战场）

```python
cur.execute("""
    SELECT id, length(tool_calls) as tclen, substr(tool_calls, 1, 200)
    FROM messages
    WHERE session_id = ? AND role='assistant'
          AND tool_calls IS NOT NULL AND tool_calls LIKE '%write_file%'
    ORDER BY id ASC;
""", (session_id,))
```

**关键洞察：** `assistant.tool_calls` 存储 write_file 的完整 arguments（含文件正文）。这是上下文膨胀的主战场（占 72%）。tool result（`tool.content`）只存元数据（~233 chars），不是问题。

**对比公式：**

```
tool_calls 总大小 = SUM(length(tool_calls)) for assistant messages
content 总大小 = SUM(length(content)) for all roles
膨胀比 = tool_calls 总大小 / content 总大小
健康值：膨胀比 < 1.0（tool_calls 小于对话正文）
警告值：膨胀比 > 3.0（tool_calls 是正文的 3 倍以上）
```

### 4.3.3 各阶段膨胀分解

按 msg_id 范围分组，计算每阶段的新增 tool_calls：

```python
phase_ranges = [
    ("creative", 0, 200),
    ("world", 200, 1050),
    ("world-revise", 1050, 1240),
    ("plot", 1240, 1350),
    ("chapter-design", 1350, 1384),
    ("prose", 1384, 1460),
    ("prose-v2", 1460, 9999),
]
for name, start, end in phase_ranges:
    cur.execute("""
        SELECT SUM(length(tool_calls)) FROM messages
        WHERE session_id = ? AND id BETWEEN ? AND ?
              AND role='assistant' AND tool_calls IS NOT NULL;
    """, (session_id, start, end))
```

**哪个阶段膨胀最严重，就是哪个 skill 需要优化。**

### 4.3.4 上下文总量估算

```python
# System prompt
cur.execute("SELECT length(system_prompt) FROM sessions WHERE id = ?;", (session_id,))

# All content (all roles)
cur.execute("SELECT SUM(length(content)) FROM messages WHERE session_id = ?;", (session_id,))

# All tool_calls (assistant only)
cur.execute("""
    SELECT SUM(length(tool_calls)) FROM messages
    WHERE session_id = ? AND role='assistant' AND tool_calls IS NOT NULL;
""", (session_id,))

total = sp_len + content_total + tc_total
estimated_tokens = total // 3  # 中文场景 approx
pct_of_128k = total / 128000 * 100
```

## 4.4 行为违规分析

### 4.4.1 用户纠错检测

扫描 user 消息，识别用户纠正 agent 行为的节点：

```python
correction_keywords = ['跳过', '跳过了', '太浅', '不够', '不行',
                       '有问题', '不对', '太厚', '太后', '不足']
```

每个纠正节点 = 一个 skill 缺陷信号。

### 4.4.2 写操作审计

检查是否有文件被多次写入（重写浪费），按文件名分组识别重复写入。**多次重写同一文件 = 设计包/模板有缺陷，导致 agent 写错。**

```python
# 识别同一文件的多次写入
cur.execute("""
    SELECT id, length(tool_calls) as tclen FROM messages
    WHERE session_id = ? AND role='assistant'
          AND tool_calls LIKE '%write_file%'
    ORDER BY id ASC;
""", (session_id,))
```

### 4.4.3 阶段跳跃检测

检查 agent 是否跳过了管线步骤（如 chapter-design 的 design 包）。

## 4.5 产出审计报告

### 报告模板

```markdown
# Session 审计报告：{session_id}

> 分析时间：{date} | 会话标题：{title}
> 模型：{model} | 消息数：{count} | 工具调用：{tool_count}

## 一、总体数据

| 指标 | 值 | 健康阈值 | 判定 |

## 二、问题 1：{标题}

**现象：**
**证据（含 msg_id 和数据）：**
**根因：**
**修复建议（含对应 SKILL.md 改动）：**

## 三、针对 SKILL.md 的优化建议

| 优先级 | Skill | 改动 | 对应问题 |
|:-----:|:------|:-----|:--------|
| P0 | pop-writer-{name} | 红线新增... | 问题 1 |
```

### 归档路径

审计报告归档到 `prd/02-问题诊断/{序号}-{描述}.md`，序号接续已有文件。

## 4.6 审计范围限制

| 不做什么 | 理由 |
|:---------|:------|
| 不直接改 SKILL.md | 审计产出的改进建议先交用户确认，然后走 B 模式改造 |
| 不分析 skill 逻辑正确性 | 只分析执行行为偏差，不判断 skill 设计本身是否合理 |
| 不覆盖 Hermes 框架层问题 | 框架层膨胀记录在报告中，不走 skill 改造路由 |
