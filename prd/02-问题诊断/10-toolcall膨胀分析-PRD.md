# toolCall Payload 膨胀分析与根治方案

> 版本：v1.0 | 2026-06-15
> 分类：问题诊断
> 状态：待执行
> 关联：[Context Overflow 问题分析报告.md](../02-问题诊断/02-ContextOverflow报告.md)、[session审计-20260615_113419_c9b495.md](../02-问题诊断/09-session审计-20260615_113419_c9b495.md)
> 数据来源：`state.db` 会话 `20260615_113419_c9b495`，265 条消息全量分析

---

## 〇、一句话范围

**本文档分析 Hermes Agent 中 toolCall payload 持续膨胀的架构根因。**
**范围：** 只诊断「为什么膨胀」，不讨论产出摘要纪律（已在 Context Overflow 报告中覆盖）。
**不做：** 不修框架层代码。本文档作为 Hermes Agent 改进的输入。

---

## 一、问题现象

### 1.1 症状

长文本写作会话中，上下文持续膨胀，最终超过模型窗口（128K token）的数倍，触发 Context Overflow 或隐性质量下降。

### 1.2 定量证据

来自 session `20260615_113419_c9b495`（265 条消息，全量管线 3 小时运行）的 state.db 审计：

| 存储来源 | 大小 | 占比 | 说明 |
|:---------|:----:|:----:|:------|
| System prompt | 19,393 chars | 2% | Hermes 基底指令 |
| Messages.content（全部角色） | 197,587 chars | 25% | 对话正文 |
| **Messages.tool_calls（assistant）** | **563,657 chars** | **72%** | **write_file 的完整文件参数** |
| **Grand total** | **780,637 chars** | **100%** | **≈260K token（2x 128K 窗口）** |

### 1.3 增长曲线（按管线阶段）

```
阶段              累计 chars     占 128K 窗口     增长来源
─────────────────────────────────────────────────────────
System prompt       19,393          15%            基底
creative 完成       72,820          57%           +53K
world 完成         339,855         265%           +267K ← 已超窗口
plot 完成          646,211         505%           +306K ← 5 倍
session 结束       780,637         610%           +134K ← 6 倍
```

从 world 阶段结束（msg_id=600）开始，上下文已超过模型窗口。plot 阶段是单阶段增长最大的区间（+306K chars）。

---

## 二、膨胀机制拆解

### 2.1 数据流：write_file 会留下两份痕迹

```
step 1: Agent 调用 write_file(path, content)
        ↓
        assistant.tool_calls  ← 存储完整 arguments（含文件内容）
        ↓
step 2: Tool 执行，写入磁盘
        ↓
        tool.content  ← 存储精简结果（bytes_written + path）
```

**关键发现：膨胀源是 `assistant.tool_calls`，不是 `tool.content`。**

| 字段 | 存储内容 | 平均大小 | 进入下一轮 context？ |
|:-----|:---------|:-------:|:--------------------:|
| `assistant.tool_calls` | `{name, arguments:{path, content}}` — **完整文件内容** | 13,518 chars | ✅ 是 |
| `tool.content` | `{bytes_written, resolved_path, lint}` — **仅元数据** | 233 chars | ✅ 是 |

### 2.2 逐轮累积：每轮工具调用都回灌全部历史

每轮 prompt 组装时，对话历史中所有 `assistant.tool_calls` 的 `arguments.content` 都被原样注入。即使文件已经写到磁盘，agent 在后续轮次完全不需要在 context 中看到该内容。

**当前 session 中有 38 条 assistant 消息含 write_file 的 tool_calls，总计 563K chars。**

### 2.3 Hermes 的 ContextEngine 为什么没拦截

```python
class ContextCompressor(ContextEngine):
    threshold_percent = 0.75    # 窗口 75% 触发
    protect_first_n = 3
    protect_last_n = 6
    
    def compress(self, messages, ...):
        # 仅压缩 messages[i].content（对话正文）
        # 不碰 messages[i].tool_calls（函数参数）
```

**压缩器只对 `content` 做迭代摘要，对 `tool_calls` 不做任何处理。** 这是由 Coding 场景假设决定的——Coding 场景下 `tool_calls.arguments` 的内容是简短的函数名和参数（`{"name":"write_file","arguments":"{\"path\":\"...\"}"}`），不需要压缩。

---

## 三、根因分析：Coding 优先假设

### 3.1 四条隐式假设

| # | 假设 | Coding 场景成立？ | 写作场景成立？ | 偏差 |
|:-:|:-----|:----------------:|:-------------:|:-----|
| 1 | **单次 write 内容短**（2-10KB） | ✅ 函数/类级别 | ❌ 章节级别（5-30KB） | 5-10x |
| 2 | **write 次数有限**（20-50 次） | ✅ PR/feature 级别 | ❌ 30 章 × 多次写入（100+） | 3-5x |
| 3 | **payload 有复用价值** | ✅ 后续需要读回来改 | ❌ 写到磁盘后不再需要 | 定性差异 |
| 4 | **对话摘要压缩够用** | ✅ 代码变更摘要很短 | ❌ 章节摘要无法替代全文参考 | 定性差异 |

### 3.2 偏差的量化对比

以 `pop-writer-prose` 一轮典型写作为例：

```
Coding 场景：
  工具调用链: write_file(50行) → run_test → read_result → write_file(20行) → ...
  Payload 总大小: ~200KB 跨全部会话
  窗口占用: 50-60%（128K 窗口）
  结论: ✅ 安全

写作场景：
  工具调用链: write_file(3000字) → write_file(3000字) → ... ×30章
  Payload 总大小: ~1.5MB 跨全部会话
  窗口占用: 610%（128K 窗口）
  结论: ❌ 6倍溢出
```

### 3.3 这不是 bug，是 feature gap

Hermes Agent 的设计对 coding 场景是合理的——toolCall arguments 保留在 context 中，agent 可以引用自己刚才写的内容做后续修改。但在写作场景中，这个设计变成了负收益：**保留 563K 的已落盘文件内容在 context 中，既占用窗口，又不提供增量信息。**

---

## 四、影响面

### 4.1 当前会话（已发生）

session `20260615_113419_c9b495` 中，workd 阶段结束后已超出模型窗口。后续 plot / prose 阶段在隐性降级下运行：
- Chat 回复质量下降（agent 无法有效管理 6x 窗口的信息）
- 每轮 token 消耗极高（156K in / 130K out = 286K tokens 一轮）
- 继续写 CH4+ 必然 Overflow

### 4.2 管线全量运行（预测）

按目前每章平均 27KB tool_calls 膨胀计算：

| 写作进度 | tool_calls 累计 | 窗口倍数 | 状态 |
|:---------|:--------------:|:--------:|:----:|
| CH1-3（当前） | 563K chars | 2x | 已超 |
| CH10 | ~1.4M chars | 5x | 隐性降级 |
| CH30（全书） | ~3.8M chars | **14x** | 不可用 |

---

## 五、根治方案

### 5.1 方案对比

| 方案 | 层面 | 效果 | 难度 | 执行周期 |
|:-----|:----|:----|:---:|:--------|
| **A. Skill 层强化摘要纪律** | Skill SKILL.md | 治标（不碰 tool_calls） | 低 | 1-2 天 |
| **B. 框架层截断 tool_calls** | Hermes ContextEngine | 治本（砍掉 72% 膨胀） | 中 | 需 Hermes 开发 |
| **C. 双管齐下** | 两者 | 完全消除 | 中 | A 先做，B 后做 |

### 5.2 方案 A 详情（Skill 层加固）

在以下 SKILL.md 中新增红线：

**pop-writer-prose**（当前最严重）：
```
❌{N} | **文件内容不得留在工具调用参数中** — 写入正文/chXXX.md 后，
      对话中仅保留 ≤200 字摘要。工具调用不携带完整文件内容。
```

**pop-writer-plot**（次严重，plot 阶段贡献了 +306K chars）：
```
❌{N} | **Canvas 矩阵写入后仅保留摘要** — act-XX.yaml 写入后，
      assistant 消息中不粘贴完整 YAML 内容。
```

**pop-writer-world**（world 阶段贡献了 +267K chars）：
```
❌{N} | **L1 设定写入后仅保留摘要** — 大块设定文件写入后，
      对话中只保留文件路径 + 一句话摘要。
```

### 5.3 方案 B 详情（框架层改动）

Hermes Agent `prompt_builder.py` / `context_engine.py` 中增加逻辑：

```python
def _prune_tool_call_payload(tool_calls: list) -> list:
    """
    对 write_file 类型的 toolCall，在注入历史上下文时
    截断 arguments.content 字段，仅保留元数据。
    """
    pruned = []
    for tc in tool_calls:
        if tc.get('function', {}).get('name') == 'write_file':
            args = json.loads(tc['function']['arguments'])
            if 'content' in args:
                content_size = len(args['content'])
                # 只保留前 200 字作为摘要
                args['content'] = args['content'][:200] + f"\n...[truncated, original {content_size} chars]"
                tc['function']['arguments'] = json.dumps(args)
        pruned.append(tc)
    return pruned
```

**改动位置：** `agent/context_engine.py` → `compress()` 方法，在生成压缩摘要前做 tool_calls 裁剪。

**节省效果：** 按当前 session 数据，563K chars → ~10K chars（-98%），从 72% 占比降至 ~2%。

### 5.4 推荐方案 C

| 优先级 | 方案 | 执行 | 预期节省 |
|:-----:|:-----|:-----|:--------:|
| P0 | 方案 A：Skill 层红线加固 | 本周 | assistant.content 再减 50% |
| P1 | 方案 B：框架层 tool_calls 截断 | 需排期 | tool_calls 减 98%（主战场） |
| P2 | 评估 ContextEngine 压缩范围 | 后续 | 防止其他大参数工具膨胀 |

---

## 六、验收标准

```python
# 验收条件
# 1. 新会话写入 30 个文件后，上下文不超过 80% 窗口
# 2. assistant.tool_calls 字段中 write_file 的 content 被截断
# 3. 原有功能不受影响（agent 仍然能正确引用已写的文件路径和大小）
```

---

## 附录 A：审计脚本

从 `state.db` 提取膨胀数据的 Python 脚本：

```python
import sqlite3

conn = sqlite3.connect(r"D:\novel-test\state.db")
cur = conn.cursor()

# tool_calls bloat
cur.execute("""
    SELECT SUM(length(tool_calls)) FROM messages 
    WHERE session_id = ? AND role='assistant' AND tool_calls IS NOT NULL
    AND tool_calls LIKE '%write_file%';
""", (session_id,))

# content size
cur.execute("""
    SELECT SUM(length(content)) FROM messages 
    WHERE session_id = ?;
""", (session_id,))

# system prompt size
cur.execute("""
    SELECT length(system_prompt) FROM sessions WHERE id = ?;
""", (session_id,))
```

---

## 附录 B：受影响 Skill 清单

| Skill | 阶段 tool_calls 膨胀 | 根因 |
|:------|:-------------------:|:------|
| `pop-writer-prose` | 82K chars / 3 章 | 整章正文作为 write_file content |
| `pop-writer-plot` | 306K chars | act-XX.yaml 多次重写 + 大块 Canvas 写入 |
| `pop-writer-world` | 267K chars | L1 六件套 + 数值体系批量写入 |
| `pop-writer-creative` | 53K chars | 素材蒸馏 + 故事引擎 + 样品试读 |
