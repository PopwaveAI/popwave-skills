# PRD: DeepSeek V4 Flash 思维链增强方案

> 创建日期：2026-06-29
> 状态：待确认
> 作者：pop

## 背景

6-28项目b的 33 个 run 扫描发现三个问题：

1. **28/130 子agent reasoningTokens=0**——没有推理就输出了，质量不可控
2. **reasoning_effort 未配置**——模型用默认 `high`，未启用 `max`，实测数据显示 Flash 从 high→max 正确率从 45% 跳到 80% [3]
3. **思维链内容丢弃**——环境变量 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM` 未开启，推理过程产生但不可见，主 session 做 receipt 检查时无法诊断子agent决策路径

DeepSeek V4 Flash（即 `popwave/writing-standard`）原生支持 `reasoning_effort` 参数（`non-thinking` / `high` / `max`），官方建议复杂 Agent 场景直接上 `max` [3]。但当前 OpenClaw 的 spawn 链路未透传该参数。

## 目标

| 优先级 | 目标 | 预期收益 |
|:-------|:-----|:---------|
| P0 | 子agent思维链内容可见 | 主session可诊断子agent决策质量 |
| P1 | create/revise 子agent启用 `reasoning_effort=max` | 推理正确率 45%→80% [3] |
| P2 | receipt 检查增加 reasoningTokens 监控 | 0-token 子agent自动标记为质量风险 |

## 现状分析

### OpenClaw spawn 链路

```
Paopao主session
  → Popwave Agent tool (input.json: prompt + model配置)
    → openclawAgentWorker.js (解析CLI参数)
      → OpenClaw core (asar内，不可访问)
        → DeepSeek API (model=popwave/writing-standard)
```

### 已确认的事实

| 检查项 | 现状 | 来源 |
|:-------|:-----|:-----|
| worker CLI 参数 | 支持 `--thinking` 和 `--thinking-once` 字符串参数 | `openclawAgentWorker.js` L164-165 |
| 实际 spawn 命令 | 未传 `--thinking` 参数 | Popwave Agent tool event inputSummary |
| `openclaw.json` 配置 | 无 model/reasoning 配置段，仅有 gateway/skills/tools | 配置文件全文 |
| `reasoning_effort` 透传 | worker 无此参数定义 | `effort` 关键词 0 匹配 |
| 思维链流处理 | worker 处理 `thinking.delta`/`thinking.message` 事件，但受 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM` 环境变量控制 | `openclawAgentStream.js` L39-40 |
| 环境变量 | `PAOPAO_OPENCLAW_RAW_THINKING_STREAM` 未设置为 `"1"` | 默认行为 |
| trajectory 记录 | `reasoningTokens` 字段有值（0-18256），但 `reasoning_content` 内容未存储 | trajectory.jsonl 扫描 |

### `--thinking` 参数语义

`--thinking` 是 OpenClaw CLI 的字符串参数，映射到 `options.thinking`。从 worker 代码看，它控制的是思维链流的输出行为（`thinking.delta`/`thinking.message` 事件是否转发给客户端），**不是** `reasoning_effort` 级别控制。

worker 代码中 `reasoning_effort`、`effort`、`budget_tokens` 关键词均为 0 匹配——OpenClaw worker 层面没有 `reasoning_effort` 参数透传能力。

## 方案设计

### Phase 1: 思维链可见性（P0，立即可做）

设置环境变量 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM=1`，让思维链内容写入临时文件：

```
%TEMP%\paopao-openclaw-streams\{runId}-{pid}.jsonl
```

**前置确认**：
- 这个环境变量在哪里设置？需要确认 Paopao 启动方式（系统环境变量 / Paopao 配置文件 / 启动脚本）
- 设置后是否影响性能？思维链写入临时文件是追加模式，不影响主流程
- 临时文件是否自动清理？需确认清理策略

**限制**：思维链内容写入临时文件供人类查看，但**不会注入回上下文**——主session做 receipt 检查时仍然看不到子agent的推理过程。要实现推理过程注入，需要 OpenClaw 平台层面支持。

### Phase 2: reasoning_effort=max 透传（P1，需平台支持）

当前 OpenClaw worker 不支持 `reasoning_effort` 参数。实现这个需要三层之一：

| 方案 | 改动层 | 可行性 | 说明 |
|:-----|:-------|:-------|:-----|
| A: Paopao 配置面板增加 reasoning_effort 选项 | Paopao 应用层 | 需 Paopao 开发 | 在 Popwave Agent tool 的 model 配置中增加下拉选项 |
| B: OpenClaw CLI 增加 --reasoning-effort 参数 | OpenClaw 平台层 | 需 OpenClaw 开发 | worker 新增 stringFlag，透传到 API 请求体 `extra_body` |
| C: openclaw.json 增加 model 配置段 | 配置层 | 需 OpenClaw 支持 | 在 profile 配置中声明 `model.reasoning_effort: max` |

**推荐方案 B**：改动最小且最灵活。worker 已有 `--thinking` 参数的先例，新增 `--reasoning-effort` 参数模式一致。OpenClaw core 在发起 DeepSeek API 调用时，将 `reasoning_effort` 写入请求体即可。

API 调用示例（DeepSeek 官方文档 [1]）：

```python
response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=messages,
    extra_body={"reasoning_effort": "max"},  # 新增
)
```

### Phase 3: receipt 检查增加 reasoning 监控（P2，skill 层面）

在 expert-writer 的 Step4 receipt 检查中增加 reasoningTokens 监控。但当前问题是：**Paopao 不会把子agent的 trajectory 数据返回给主session**——主session只能看到子agent的最终输出（response.md），看不到 reasoningTokens。

要实现这个，需要 Phase 2 的平台改动同时增加一个返回字段，让子agent的 `usage.reasoningTokens` 出现在 Popwave Agent tool 的 result 中。

**skill 层面能立即做的**：在 create/revise 的 manifest 中增加一条要求——子agent在 receipt 中自报 reasoningTokens 数量。但这依赖子agent诚实报告，不可靠。

## 实施计划

| 阶段 | 事项 | 依赖 | 预估工时 |
|:-----|:-----|:-----|:---------|
| Phase 1 | 确认 Paopao 环境变量设置方式，开启 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM=1` | 无 | 0.5h |
| Phase 1 | 运行一轮 create/revise，检查临时文件中思维链内容是否完整 | 环境变量已设 | 1h |
| Phase 2 | 向 Paopao/OpenClaw 提交 `reasoning_effort` 透传需求 | 平台开发排期 | — |
| Phase 2 | 确认 `--thinking` 参数是否已能控制 reasoning depth（需查 OpenClaw core 源码） | OpenClaw 源码访问 | 2h |
| Phase 3 | receipt 检查增加 reasoningTokens 字段（依赖平台返回该数据） | Phase 2 完成 | 1h |

## 风险

| 风险 | 影响 | 缓解 |
|:-----|:-----|:-----|
| `reasoning_effort=max` 导致输出 token 膨胀 4 倍 [3] | 成本增加、延迟增加 ~400ms | 仅对 create/revise 启用，文件读取等简单工具调用保持默认 |
| max 模式建议上下文 ≥384K [3] | 当前上下文可能不足导致截断 | 需检查当前 input token 用量，确认是否超限 |
| `--thinking` 参数语义未确认 | 可能是流控制而非深度控制 | Phase 2 前需查 OpenClaw core 源码确认 |
| 思维链内容包含敏感信息 | 临时文件泄露风险 | 确认临时文件目录权限和清理策略 |

## 验收标准

1. `PAOPAO_OPENCLAW_RAW_THINKING_STREAM=1` 设置后，`%TEMP%\paopao-openclaw-streams\` 下能看到子agent的思维链 JSONL 文件
2. create/revise 子agent的 `reasoning_effort` 设为 `max` 后，trajectory 中 `reasoningTokens` 平均值显著提升（从 ~420 提升到 ≥1500）
3. 0-token 子agent数量从 28/130 降低到 ≤5/130（保留的是真正的简单工具调用）
