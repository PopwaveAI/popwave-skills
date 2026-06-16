# toolCall Payload 膨胀根因分析

> 适用于：走 D 模式会话审计发现上下文膨胀问题时，快速理解"为什么 tool_calls 会占 72%"

---

## 一句话

**write_file 的文件正文（content 字段）完整保存在 `assistant.tool_calls` 中。每轮 prompt 组装时回灌全部历史。压缩器不碰这个字段。**

## 数据对比

| 存储位置 | 内容 | 平均大小 | 占上下文比 |
|:---------|:-----|:--------:|:---------:|
| `assistant.tool_calls` | write_file 的 arguments（path + content） | 13KB/次 | **72%** |
| `tool.content` | 工具返回的元数据（bytes_written + path） | 233B/次 | <1% |
| `assistant.content` | 对话正文 | — | 25% |

## 增长曲线（实际 session 数据）

```
阶段           累计 chars    占 128K 窗口
────────────────────────────────────────
creative 完成    72K           57%    ✅
world 完成      339K          265%    ⚠️ 已超
plot 完成       646K          505%    ❌ 5x
session 结束    780K          610%    🔥 6x
```

## 根因链

```
Hermes 设计假设（coding 场景）：
  tool_call 参数 = 简短函数调用（路径+参数）
  → 不需要压缩
  → 保留在 context 中供后续引用

写作场景实际：
  tool_call 参数 = 完整章节正文（5-30KB）
  → 写到磁盘后不需要再引用
  → 但每轮仍然回灌
```

## 修复方案

| 层面 | 方案 | 状态 |
|:-----|:-----|:----:|
| 框架层 | `context_compressor.py` 新增 `trim_write_file_payloads()` 无条件截断 write_file 的 content 字段 | ✅ 已打到源码 |
| 框架层 | `turn_context.py` 中每轮无条件调用 | ✅ 已打到源码 |
| Skill 层 | 在 `pop-writer-prose`/`plot`/`world` 中加红线：写入后对话只留 ≤200 字摘要 | ⏳ 待执行 |

## 审计检测方法

```python
import sqlite3, json

conn = sqlite3.connect(r"D:\novel-test\state.db")
cur = conn.cursor()

# tool_calls 总大小（主战场）
cur.execute("""
    SELECT SUM(length(tool_calls)) FROM messages
    WHERE session_id = ? AND role='assistant'
          AND tool_calls IS NOT NULL AND tool_calls LIKE '%write_file%';
""", (session_id,))

# content 总大小（对话正文）
cur.execute("""
    SELECT SUM(length(content)) FROM messages WHERE session_id = ?;
""", (session_id,))

# system prompt 大小
cur.execute("""
    SELECT length(system_prompt) FROM sessions WHERE id = ?;
""", (session_id,))
```
