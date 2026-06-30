# OpenClaw Gateway 并发 Spawn 崩溃：6-30 项目b 复盘

> **问题诊断 · 2026-06-30 · Platform Engineering**
> **P0 · 核心流程缺陷** | gateway | websocket | spawn-failure | evidence-based
> 基于 project `6-30-项目b` 的 runs 数据分析

---

## 1. 问题现象

6-30-项目b 在 plot 环节连续 5 个 run（16:12-16:25）报子 agent 失败。错误信息：

```
OpenClaw sessions_spawn 返回 accepted，但宿主在 materialization 窗口内没有看到子 Agent session 或 registry 记录落盘。
子会话：agent:main:subagent:dcae27f8-8a0c-475f-9e23-2ac64e6619f4
Run：c3ab3af1-9021-4f63-b16f-3613625c2b01
等待：10 秒
```

第二个子 agent 同样失败：
```
子会话：agent:main:subagent:ec3608eb-ca87-443e-a3c5-c435d79e4e00
Run：ef3bb486-82b8-490d-9a8f-95832ff7142b
```

## 2. 根因分析

### 2.1 触发条件：同一 run 内连续并发 spawn

从 run `31e0958d` 的 events.jsonl 可以看到完整调用链：

| 时间 | 事件 | 结果 |
|:-----|:-----|:-----|
| 08:22:34 | spawn 第一个子 agent `a6873c87`（完成剩余文件） | accepted → materialized 成功 |
| 08:23:28 | 发现第一个子 agent 未产出文件，同时 spawn 两个并行子 agent | |
| 08:23:28 | spawn `dcae27f8`（方案B/C/PK） | accepted → **未落盘** |
| 08:23:28 | spawn `ec3608eb`（审计压缩+幕纲） | accepted → **未落盘** |
| 08:23:49 | 10 秒窗口到期，2 个子 agent 均未 materialized | 触发 fallback |

**关键触发条件**：agent 在发现第一个子 agent 没产出文件后，在**同一秒内**同时 spawn 了两个并行子 agent。gateway 在处理并发 spawn 时崩溃。

### 2.2 根因：Orphaned Session 积压导致 Gateway 崩溃

从 events.jsonl line 12 的 stderr 可以看到：

```
[subagent-interrupted-resume] failed to resume orphaned session 
agent:main:subagent:dc369cd9-e437-40ad-b0e1-266c3de4d96b: 
gateway closed (1006 abnormal closure (no close frame)): no close reason
Gateway target: ws://127.0.0.1:18789
```

stderr 中记录了**4 个 orphaned session**（`dc369cd9`、`a18423de`、`4257036b`、`b5980b0e`）都因为 gateway 异常关闭而无法 resume。

**崩溃机制**：

```
1. 之前的 run 产生了孤儿 session（子 agent 完成但 session 未清理）
2. 新 run 启动时，gateway 尝试恢复这些孤儿 session
3. 恢复时 websocket 连接异常断开（1006 abnormal closure）
4. gateway 崩溃 → 新 spawn 的子 agent 无法落盘
5. 主 agent 等待 10 秒 → materialization 窗口超时 → spawn-unmaterialized
6. 触发 fallback，但子 agent 的实际工作丢失
```

### 2.3 与历史问题的关系

本次失败模式与 [子Agent 可靠性与推理增强 PRD](../subagent-reliability-and-reasoning-enhancement.md) 中记录的 RC-1 和 RC-2 完全一致：

| 历史根因 | 本次表现 |
|:---------|:---------|
| RC-1: Gateway WebSocket 断裂（1006 abnormal closure） | 完全一致，4 个 orphaned session 均 1006 |
| RC-2: sessions_spawn 虚假 accepted | 完全一致，2 个子 agent 返回 accepted 但未落盘 |

**新增发现**：历史文档未记录的触发条件——**并发 spawn 是崩溃的放大器**。单个 spawn 可以正常 materialize（如本 run 第一个子 agent `a6873c87` 成功），但并发 spawn 两个以上时，gateway 在处理第二个连接时崩溃。

## 3. 影响范围

| 维度 | 影响 |
|:-----|:-----|
| **受影响 run** | 6-30-项目b 最后 5 个 run（16:12-16:25），前 43 个正常 |
| **丢失产出** | 方案B/方案C全章、竞技场PK、审计压缩说明、最终幕纲、产物索引——6 个文件 |
| **agent 行为** | agent 检测到子 agent 失败后触发 fallback，但 fallback 只能收集空结果，无法恢复子 agent 的实际工作 |
| **用户感知** | 连续 5 轮对话都报子 agent 错误，用户体验中断 |

## 4. 证据链

### 4.1 时间线

| 时间 | run | 事件 |
|:-----|:----|:-----|
| 15:47-16:09 | 19564d3c 等 7 个 run | 正常执行，无 spawn 错误 |
| 16:12 | 30db4992 | 最后一个正常 run |
| 16:17 | 52daed1d | 开始报 spawn-unmaterialized |
| 16:17 | 3166ec1a | 同上 |
| 16:24 | 820be7be | 同上 |
| 16:25 | 2b71c51b | 同上 |
| 16:25 | 31e0958d | 同上，有完整 events.jsonl |

### 4.2 证据：run 31e0958d 的完整 spawn 链

从 events.jsonl 提取的 spawn 事件序列：

1. `08:22:34` spawn `a6873c87` → `08:22:41` materialized 成功（7 秒）
2. `08:23:28` spawn `dcae27f8` + `ec3608eb`（同一秒并发）
3. `08:23:49` 两个均未 materialized（21 秒后超时）

第一个子 agent 单独 spawn 时成功，两个并发 spawn 时失败——证明问题是并发触发，不是 gateway 全局不可用。

### 4.3 证据：stderr 中的 orphaned session

run 31e0958d 的 stderr 记录了 4 个 orphaned session 恢复失败：

| orphaned session | 错误 |
|:-----------------|:-----|
| `dc369cd9` | gateway closed (1006 abnormal closure) |
| `a18423de` | gateway closed (1006 abnormal closure) |
| `4257036b` | gateway closed (1006 abnormal closure) |
| `b5980b0e` | gateway closed (1006 abnormal closure) |

这 4 个孤儿 session 是之前 run 积累的，在新 run 启动时触发 gateway 恢复尝试，恢复失败导致 gateway 不稳定。

## 5. 修复建议

### 5.1 即时修复（用户侧）

- **重启 paopao**：清理 gateway 状态和 orphaned sessions
- **避免并发 spawn**：skill 中增加约束——一次只 spawn 一个子 agent，等它完成后再 spawn 下一个

### 5.2 Skill 层修复

在 expert-writer 的 step-2-execute 中增加子 agent 调度纪律：

```
## 子 Agent 调度纪律

1. 一次只 spawn 一个子 agent
2. spawn 后 yield 等待 completion event
3. 如果子 agent 未产出文件，不要立即重新 spawn——先检查：
   a. 子 agent 是否真的在运行（process list）
   b. 目标目录是否有写入权限
4. 如果需要重新 spawn，等上一个完全退出后再启动
5. 禁止同一秒内并发 spawn 多个子 agent
```

### 5.3 框架层修复（OpenClaw 侧）

| 修复项 | 优先级 | 说明 |
|:-------|:------:|:-----|
| Gateway orphaned session 自动清理 | P0 | run 启动时自动清理超过 N 分钟的孤儿 session，不尝试恢复 |
| 并发 spawn 限流 | P1 | gateway 限制同一 run 内的并发子 agent 数量（建议 ≤ 2） |
| Materialization 超时加长 | P2 | 10 秒太短，复杂任务（如 plot 产出 6 个文件）需要更长时间才能落盘 |
| Gateway 崩溃自动重启 | P2 | gateway 1006 崩溃时自动重启，不依赖用户手动重启 paopao |

## 6. 复现条件

| 条件 | 必要性 |
|:-----|:------:|
| 累计 40+ 个 run（孤儿 session 积累到阈值） | 必要 |
| 同一 run 内并发 spawn 2+ 个子 agent | 触发放大 |
| gateway `ws://127.0.0.1:18789` 状态不稳定 | 必要 |

## 7. 相关文档

- [子Agent 可靠性与推理增强 PRD](../subagent-reliability-and-reasoning-enhancement.md) — RC-1/RC-2 的原始记录
- [OpenClaw 上下文溢出问题分析](10-20260625-OpenClaw上下文溢出-问题分析.md) — 上下文管理机制问题
- [subagent-failure-prd](../subagent-failure-prd/) — 之前的子 agent 失败 PRD（HTML 格式）