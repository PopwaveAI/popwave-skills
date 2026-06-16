# toolCall Payload 根治方案 — Hermes 框架层改动

> 版本：v1.0 | 2026-06-15
> 分类：问题诊断
> 状态：方案设计
> 目标文件：`agent/context_compressor.py`

---

## 〇、一句话方案

**在 ContextCompressor 的 `_prune_old_tool_results` 中增加第二遍扫描：对 protected tail 区域内的 `write_file` 工具调用参数也做截断，因为文件已落盘，不需要全量回灌。**

---

## 一、现状复盘

### 1.1 源代码中已有截断机制

```python
# agent/context_compressor.py — 已存在，功能完整

def _truncate_tool_call_args_json(args: str, head_chars: int = 200) -> str:
    """
    解析 tool_call 的 arguments JSON → 截断所有长字符串字段到 200 字
    → 重新序列化为合法 JSON。
    非字符串字段（path, int, bool）原样保留。
    """
```

### 1.2 问题：只截旧消息，不截新消息

```python
# 当前调用位置：_prune_old_tool_results() 第 989 行

for i in range(prune_boundary):    # ← 只扫 protected tail 之前的消息
    # 截断 tool_call args
    
# 保护尾 (prune_boundary .. end) ← 完全不碰
```

**新写的章节、YAML 文件都在保护尾里，每次回灌。**

### 1.3 用户会话实证

| 阶段 | 膨胀位置 | 是否在保护尾 | 是否被截断 |
|:-----|:---------|:-----------:|:---------:|
| CH1 正文 `write_file("ch001.md", content=9KB)` | 最近 10 条内 | ✅ 是 | ❌ 否 |
| act-01.yaml `write_file("act-01.yaml", content=18KB)` | 最近 10 条内 | ✅ 是 | ❌ 否 |
| 3 轮前的 skill_view 调用 | 保护尾之外 | ❌ 否 | ✅ 是 |

---

## 二、改动方案

### 2.1 改动位置

单个文件：`agent/context_compressor.py` → `_prune_old_tool_results()` 方法

### 2.2 改动内容

在现有逻辑之后，增加一个**保护尾内的精细化截断层**：

```python
# === 新增：Pass 3 — 保护尾内也截断 write_file 的完整文件内容 ===
# 理由：write_file 的 content 字段是完整文件正文，已写入磁盘后不再需要保留在上下文中。
# 保留 path 和 bytes_written 就够了。
for i in range(prune_boundary, len(result)):
    msg = result[i]
    if msg.get("role") != "assistant" or not msg.get("tool_calls"):
        continue
    new_tcs = []
    modified = False
    for tc in msg["tool_calls"]:
        if not isinstance(tc, dict):
            new_tcs.append(tc)
            continue
        fn = tc.get("function", {})
        fn_name = fn.get("name", "")
        args_str = fn.get("arguments", "")
        
        # 只对 write_file 做截断（其他工具的参数需要保留）
        if fn_name == "write_file" and len(args_str) > 500:
            try:
                parsed = json.loads(args_str)
                if "content" in parsed and len(parsed["content"]) > 500:
                    original_len = len(parsed["content"])
                    parsed["content"] = (
                        parsed["content"][:200]
                        + f"\n\n...[Hermes checkpoint: content truncated, "
                        f"original {original_len} chars. Full content on disk at {parsed.get('path', 'unknown')}]"
                    )
                    new_args = json.dumps(parsed, ensure_ascii=False)
                    if new_args != args_str:
                        tc = {**tc, "function": {**fn, "arguments": new_args}}
                        modified = True
            except (json.JSONDecodeError, TypeError):
                pass  # 非 JSON 参数原样保留
        
        new_tcs.append(tc)
    
    if modified:
        result[i] = {**msg, "tool_calls": new_tcs}
```

### 2.3 与现有 `_truncate_tool_call_args_json` 的关系

| 维度 | 现有 Pass 2 | 新增 Pass 3 |
|:-----|:-----------|:-----------|
| 扫描范围 | 保护尾之前（旧消息） | 保护尾内（新消息） |
| 截断对象 | **所有**工具的全部字符串参数 | **仅 `write_file`** 的 `content` 字段 |
| 阈值 | >500 chars | >500 chars |
| 截断后 | `<head_chars>` 字（默认 200） | 200 字 + 文件大小/路径信息 |
| 理由 | 旧消息不需要细节 | 文件已落盘，content 字段无上下文价值 |

### 2.4 安全边界

| 风险 | 是否可控 | 措施 |
|:-----|:--------|:-----|
| 模型不知道文件写了什么？ | ✅ 可控 | 截断后保留路径和大小信息，agent 需要时通过 `read_file` 工具重新读取 |
| 非 `content` 字段误截断？ | ✅ 可控 | `parsed["content"]` 精准定位，其他字段原样保留 |
| 非 `write_file` 的工具参数也丢了？ | ✅ 可控 | 只处理 `fn_name == "write_file"`，其他工具完全不碰 |
| 截断后 JSON 不合法？ | ✅ 可控 | 使用 `json.dumps` 重新序列化，与现有 `_truncate_tool_call_args_json` 相同模式 |
| 影响其他编码场景？ | ✅ 可控 | 编码场景 `write_file` 传的 content 通常小于 500 chars，不会触达截断阈值 |

---

## 三、节省估算

基于 session `20260615_113419_c9b495` 的实测数据：

| 指标 | 改前 | 改后（预期） | 节省 |
|:-----|:----|:-----------|:----:|
| 每条 write_file 的 tool_calls 大小 | 13,518 chars（平均） | ~500 chars（200 字摘要 + 头尾标记） | **-96%** |
| 全 session tool_calls 总大小 | 563,657 chars | ~40,000 chars | **-93%** |
| 全 session 上下文总大小 | 780,637 chars | ~257,000 chars | **-67%** |
| 占 128K 窗口比例 | 610% | **~200%** | ↓ 但仍未进入安全区 |
| 占 256K 窗口比例 | 305% | **~100%** | ✅ 安全 |

> 注意：即使加上截断，266 条消息的对话正文（System prompt + 全部角色的 content）仍有 ~200K chars。根治还需要结合 `/reset` 分段策略。但 tool_calls 截断可以砍掉 72% 的膨胀。

---

## 四、验证方法

### 4.1 单元测试

在 `tests/agent/test_context_compressor.py` 中新增用例：

```python
def test_write_file_content_truncated_in_tail():
    """Protected tail 内的 write_file tool_call content 应该被截断。"""
    messages = [
        {"role": "system", "content": "You are Hermes"},
        {"role": "assistant", "content": "Writing file",
         "tool_calls": [{
             "id": "call_xxx",
             "function": {
                 "name": "write_file",
                 "arguments": json.dumps({
                     "path": "/tmp/ch001.md",
                     "content": "A" * 10000  # 10KB chapter text
                 })
             }
         }]},
        {"role": "tool", "content": '{"bytes_written": 10000}'},
    ]
    engine = ContextCompressor()
    result, count = engine._prune_old_tool_results(messages, protect_tail_count=10)
    
    # 验证：tool_call arguments 中的 content 已被截断
    tc = result[1]["tool_calls"][0]
    args = json.loads(tc["function"]["arguments"])
    assert len(args["content"]) < 1000  # 截断到 200 字左右
    assert "original 10000 chars" in args["content"]  # 保留原始大小信息
    assert args["path"] == "/tmp/ch001.md"  # 非 content 字段原样保留
```

### 4.2 集成验证

```
1. 启动 Hermes
2. 通过 @file: 或 skill 触发一次大文件写入（> 500 chars 的 content）
3. 检查下一轮 prompt 中该 tool_call 的 arguments.content 是否被截断
4. 检查 agent 是否能通过 read_file 工具重新读取完整内容
```

---

## 五、后续优化方向

### 5.1 扩展到其他写工具（未来）

如果 `patch` 工具也存在大 content 参数，可以用同样模式截断。当前只有 `write_file` 问题最严重。

### 5.2 配合 Skill 层红线（双管齐下）

即使框架层截断了 tool_calls，assistant.content 中仍可能贴完整文件内容。需要：

```
框架层：tool_calls 截断 ← 本文案
Skill 层：assistant.content 摘要化红线 ← 已有，需强化
```

两条线加起来，才能把 72% 的膨胀砍到 5% 以内。

---

## 六、补丁文件

```diff
--- a/agent/context_compressor.py
+++ b/agent/context_compressor.py
@@ -1005,6 +1005,46 @@ class ContextCompressor:
 
         return result, pruned
 
+        # === Pass 3: Truncate write_file content even in protected tail ===
+        # write_file's "content" field carries the full file text.
+        # Once written to disk, the agent does not need it in context.
+        # Keep path + size metadata; truncate content to 200 chars.
+        for i in range(prune_boundary, len(result)):
+            msg = result[i]
+            if msg.get("role") != "assistant" or not msg.get("tool_calls"):
+                continue
+            new_tcs = []
+            modified = False
+            for tc in msg["tool_calls"]:
+                if not isinstance(tc, dict):
+                    new_tcs.append(tc)
+                    continue
+                fn = tc.get("function", {})
+                fn_name = fn.get("name", "")
+                args_str = fn.get("arguments", "")
+
+                if fn_name == "write_file" and len(args_str) > 500:
+                    try:
+                        parsed = json.loads(args_str)
+                        if "content" in parsed and len(parsed["content"]) > 500:
+                            original_len = len(parsed["content"])
+                            parsed["content"] = (
+                                parsed["content"][:200]
+                                + f"\n\n...[Hermes checkpoint: content truncated, "
+                                f"original {original_len} chars. "
+                                f"Full content on disk at {parsed.get('path', 'unknown')}]"
+                            )
+                            new_args = json.dumps(parsed, ensure_ascii=False)
+                            if new_args != args_str:
+                                tc = {**tc, "function": {**fn, "arguments": new_args}}
+                                modified = True
+                    except (json.JSONDecodeError, TypeError):
+                        pass
+
+                new_tcs.append(tc)
+
+            if modified:
+                result[i] = {**msg, "tool_calls": new_tcs}
+
     # ------------------------------------------------------------------
     # Summarization
     # ------------------------------------------------------------------
```
