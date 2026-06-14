# OpenClaw-401问题报告

> 来源：飞书文档 | [原文链接](https://n0mqbh938qa.feishu.cn/wiki/VnSow6IhiiJpLqkF7uMcGH0jndb)
> 同步时间：2026-06-14 | doc_id: VhhYdLKumo1zFwxJziqcbESwnic | rev: 5

# OpenClaw 首次 Auth 401 问题报告

> **📌 修复状态：待迁移解决 ⏳** ｜ 本文档记录 OpenClaw 运行时的 Auth bug。  
> 2026-06-10 已选定 Hermes Agent 替代 OpenClaw 作为 Popwave 技术底层。  
> 迁移完成后此问题自动消除。目前 OpenClaw 仍在使用中，临时方案为「遇到 401 时重试一次」。  
> 迁移计划见「为什么选择 Hermes Agent 作为 Popwave 技术底层」§五-实施路线图。

> 日期：2026-06-09  
> 项目：6-9测试（深渊主宰同人文）  
> 问题：每个对话的第一次 Agent 调用总是失败（OpenClaw 401）

---

## §1 现象

用户在 paopao 中启动新对话，发送第一条 `/pop-novel-bookstrap` 指令后，Agent 返回错误：

```
OpenClaw 调用失败
退出码：1
stderr: HTTP 401: Authentication Fails
         Your api key: ****e619 is invalid
```

**但**重新发送同一条指令后，第二次调用正常返回，Agent 成功开始工作。

---

## §2 证据链

### 2.1 第一次调用 — 失败

| 字段 | 值 |
|-|-|
| Run ID | `2cb1d8ae-d1c5-41a6-8582-7391e39e243e` |
| Profile | `novel-buddy` |
| Model | `deepseek/deepseek-v4-flash` |
| 错误 | `HTTP 401: Authentication Fails, Your api key: ****e619 is invalid` |
| auth 状态 | `reason=auth, window=cooldown, reused=false` |

### 2.2 第二次调用 — 成功

| 字段 | 值 |
|-|-|
| Run ID | `cd9d5043-0901-4f17-9aa1-20c4a1889b32` |
| Profile | `novel-buddy`（同一个） |
| Model | `deepseek/deepseek-v4-flash`（同一个） |
| 错误 | 无，正常返回 |
| 结果 | Agent 正常响应，开始追问 story-engine |

### 2.3 关键差异

| 维度 | 第一次 | 第二次 |
|-|-|-|
| API Key | `****e619` | `****e619`（同一个） |
| Provider 冷却状态 | `cooldown` | 已恢复 |
| Auth Profile | `reused=false`（首次加载） | `reused=true`（复用已验证的） |

**结论**：同一个 key、同一个模型、同一个 profile。key 没有真的失效——第二次请求用它成功了。故障发生在第一次请求时，auth profile 尚未完成初始化。

---

## §3 根因

**OpenClaw embedded runtime 的 auth profile 初始化是异步的。**

```
时序：
T0: 用户点击发送
T1: OpenClaw 收到 agent 请求 → 创建 run
T2: 开始读取 auth profile C:\Users\AWMPRO\.openclaw-novel-buddy\agents\main\agent\auth-profiles.json
T3: Agent 请求到达 LLM provider → 发送 api key
但此时 T2 尚未完成 → api key 未被正确注入 → Provider 返回 401
T4: Auth profile 加载完成
T5: Provider 进入 cooldown 状态

第二次调用：
T6: Auth profile 已缓存（reused=true）→ 正常注入 → 200 OK
```

**这不是 key 无效，是 key 还没准备好。**

---

## §4 影响范围

- 每个对话的第一次 Agent 调用 100% 复现
- 后续调用不受影响（auth profile 被缓存后正常）
- 不影响 key 本身的可用性
- 对话中段（如 Phase 1.2 补全任务）也可能触发，因为长对话中间 auth profile 可能过期重载

---

## §5 修复方案

### 方案 A（Runtime 侧·推荐）

OpenClaw 在 agent 启动前增加 auth profile 预热步骤：

```javascript
// 在 agent 启动前同步加载并验证 auth profile
await authProfileManager.load(profileId);
await authProfileManager.validate(profileId);  // 发一次 cheap 请求确认 key 有效
// 然后再接收用户消息
```

**改动位置**：OpenClaw `agent-command` 模块，agent 启动逻辑中，在接收第一条 message 之前插入预热。不涉及 skill 侧。

### 方案 B（Runtime 侧·备选）

当前 auth profile 加载失败时，OpenClaw 已有 fallback 重试逻辑，但只重试一次。**将 auth 401 的重试次数从 1 改为 3，间隔 500ms。**

```yaml
# openclaw.json 中增加
auth:
  retry_on_401: true
  max_retries: 3
  retry_interval_ms: 500
```

### 方案 C（用户侧·临时规避）

用户在首启配置中重新保存一次 API Key，强制 OpenClaw 重建 auth profile 缓存。这不修复根因，但可能在部分环境下降低复现率。

---

## §6 处理建议

**推荐方案 A**（预热验证），优先级 P1。方案 B（增加重试）作为降级兜底，P2。

此问题从 skill 侧无可修复——auth 初始化在 OpenClaw runtime 层，不在 agent prompt 或 pipeline 层面。