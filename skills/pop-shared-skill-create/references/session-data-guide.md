# Hermes state.db 数据模型参考

> 版本：v1.0 | 2026-06-15
> 用途：会话审计模式（Mode D）的数据源参考

---

## 一、数据库位置

```
$HERMES_HOME/state.db
```

当前环境：`D:\novel-test\state.db`

## 二、核心表结构

### sessions 表 — 会话元数据

```sql
CREATE TABLE sessions (
    id              TEXT PRIMARY KEY,     -- "20260615_114113_b09106" 格式
    source          TEXT,                 -- "tui", "gateway", "telegram" 等
    user_id         TEXT,
    model           TEXT,                 -- "deepseek-v4-flash"
    model_config    TEXT,                 -- JSON 字符串
    system_prompt   TEXT,                 -- 完整的 system prompt（含 skill 注入）
    parent_session_id TEXT,
    started_at      REAL,                -- Unix timestamp
    ended_at        REAL,
    end_reason      TEXT,
    message_count   INTEGER,
    tool_call_count INTEGER,
    input_tokens    INTEGER,
    output_tokens   INTEGER,
    cache_read_tokens     INTEGER,
    cache_write_tokens    INTEGER,
    reasoning_tokens      INTEGER,
    cwd             TEXT,
    billing_provider TEXT,
    billing_base_url TEXT,
    billing_mode    TEXT,
    estimated_cost_usd    REAL,
    actual_cost_usd       REAL,
    cost_status     TEXT,
    cost_source     TEXT,
    pricing_version TEXT,
    title           TEXT,
    api_call_count  INTEGER,
    handoff_state         TEXT,
    handoff_platform      TEXT,
    handoff_error   TEXT,
    rewind_count    INTEGER,
    archived        INTEGER DEFAULT 0
);
```

**审计关键字段：**

| 字段 | 用途 |
|:-----|:------|
| `system_prompt` | 查看注入的完整 skill 内容 |
| `message_count` | 会话长度，>150 需关注 |
| `tool_call_count` | 工具调用密集度 |
| `input_tokens` + `output_tokens` | token 消耗总量 |
| `title` | 会话标题，用于快速定位 |

### messages 表 — 消息详情

```sql
CREATE TABLE messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      TEXT,                 -- FK → sessions.id
    role            TEXT,                 -- "user", "assistant", "tool"
    content         TEXT,                 -- 消息正文（助理回复）或工具结果
    tool_call_id    TEXT,                 -- 工具调用的 ID
    tool_calls      TEXT,                 -- JSON: assistant 消息中的工具调用规范
    tool_name       TEXT,                 -- 工具消息中的工具名
    timestamp       REAL,
    token_count     INTEGER,              -- 该消息的 token 数（可能缺失）
    finish_reason   TEXT,
    reasoning       TEXT,                 -- 推理内容
    reasoning_content TEXT,
    reasoning_details TEXT,
    codex_reasoning_items TEXT,
    codex_message_items TEXT,
    platform_message_id  TEXT,
    observed        INTEGER DEFAULT 0,
    active          INTEGER DEFAULT 1
);
```

**审计关键字段：**

| 字段 | role | 存储内容 | 大小典型值 | 审计价值 |
|:-----|:-----|:---------|:---------:|:---------|
| `content` | user | 用户消息 | 50-500 chars | 用户需求 / 纠错 |
| `content` | assistant | 助理回复 | 200-2000 chars | 摘要纪律检查 |
| `content` | tool | 工具返回结果 | 200-500 chars | write_file 元数据 |
| **`tool_calls`** | **assistant** | **工具调用参数（含文件内容）** | **5K-32K chars** | **膨胀主战场** |
| `tool_name` | tool | 工具名 | ~10 chars | 筛选 write_file 调用 |

## 三、膨胀审计公式

### 3.1 tool_calls 总大小

```sql
SELECT SUM(length(tool_calls)) FROM messages
WHERE session_id = ? AND role='assistant' AND tool_calls IS NOT NULL;
```

### 3.2 content 总大小

```sql
SELECT SUM(length(content)) FROM messages
WHERE session_id = ?;
```

### 3.3 System prompt 大小

```sql
SELECT length(system_prompt) FROM sessions WHERE id = ?;
```

### 3.4 健康判定

```
总量          = system_prompt + content_total + tool_calls_total
估 token      = 总量 / 3（中英文混合场景）
窗口占比      = 估 token / model_context_length * 100

健康：窗口占比 < 75%   → 压缩器不触发
警告：窗口占比 > 75%   → 压缩器启动，但 tool_calls 不压缩
危险：窗口占比 > 150%  → 即使压缩后仍超限，随时可能 overflow
```

### 3.5 write_file 调用识别

```sql
SELECT id, length(tool_calls) as bloat, substr(tool_calls, 1, 200) as preview
FROM messages
WHERE session_id = ? AND role='assistant'
      AND tool_calls LIKE '%write_file%'
ORDER BY id ASC;
```

## 四、审计注意事项

| 注意点 | 说明 |
|:-------|:------|
| `token_count` 字段可能全为 NULL | 不是所有模型都会返回 token 用量；用字符数/3 粗估 |
| `tool_calls` 是 JSON 字符串 | 解析后结构为 `[{id, function:{name, arguments}}]`，arguments 字段是 JSON 编码的 {path, content} |
| `content` 可能为空 | 纯工具调用时 assistant 的 content 可能为 null 或空字符串 |
| `system_prompt` 存在但可能不完整 | Hermes 的 limitChars=32768 可能在写入时截断 |
