# PRD-02: 子Agent调度物化失败

> **严重级别：** P0 / 严重
> **来源文档：** 08, 10, 15, 16, 18
> **最后更新：** 2026-07-01

---

## 问题概述

OpenClaw 的子Agent调度系统（sessions_spawn / sessions_yield / Gateway WebSocket）存在多层级故障链——从 Gateway WebSocket 断裂到 spawn 虚假 accepted 到结果捕获失败到 fallback 覆盖不全，形成"spawn 表面成功 → 子 session 未物化 → 结果无法读取 → fallback 部分补救 → 产出永久丢失"的完整失败链。这是导致拆书/写作管线大面积中断的直接原因。

---

## 根因分析

### 1. Gateway WebSocket 断裂（1006 abnormal closure）

之前的 run 产生孤儿 session（子 agent 完成但 session 未清理），新 run 启动时 gateway 尝试恢复，恢复时 WebSocket 连接异常断开，gateway 崩溃 → 新 spawn 的子 agent 无法落盘。框架缺乏 orphaned session 自动清理机制。

### 2. sessions_spawn 虚假 accepted

API 返回 accepted + childSessionKey + runId，但子 agent session 文件从未写入磁盘。存在先返回后持久化的竞态问题。

### 3. 子Agent结果捕获失败

子Agent执行完成并落盘文件后，其结束文本/完成信号未能被 orchestrator 读取。100% 复现率。

### 4. 并发 spawn 放大崩溃

单个 spawn 可正常 materialize，但同一秒内并发 spawn 两个以上时 gateway 崩溃。但后续发现不限于并发——长会话积累后也会自发崩溃。

### 5. Fallback 覆盖不全

paopao-background-task 隐藏支线会话在检测到 spawn-unmaterialized 后启动补救，但覆盖率不全——同一类型失败部分触发部分跳过。

---

## 证据链

### 文档15（15-1）

- ch001 调用 sessions_spawn 返回 accepted + childSessionKey，5 分钟后报"未能读取到子Agent最终文本：error"
- 日志 `[37]ev31-35`：spawn accepted → `[37]ev35` 收集结果 error
- 日志 `[39]ev2`：agent 自述"创作子skill没跑成功。我直接写"
- project_memory 记录 OpenClaw v2026.6.8 已知缺陷

### 文档16（16-1 ~ 16-5）

- run 31e0958d 的 stderr 记录 4 个 orphaned session（dc369cd9 / a18423de / 4257036b / b5980b0e）均报 gateway closed（1006 abnormal closure）
- 08:22:34 单独 spawn a6873c87 → 7 秒 materialized 成功
- 08:23:28 同一秒并发 spawn dcae27f8 + ec3608eb → 21 秒后均未 materialized
- 15:47-16:09 正常 → 16:17 起连续 5 个 run 报 spawn-unmaterialized
- 复现条件：累计 40+ 个 run

### 文档08（08-1）

- batch-1 到 batch-21，100% 返回"未能读取到子Agent最终文本"
- 实际 61 个设计包 + 135 个套路文件全部在磁盘上
- 用户手动 push 5 次

### 文档10（10-2）

- run 8d220b08 出现 3 个 orphaned subagent session 恢复失败，recovered=0, failed=3, skipped=56

### 文档18（18-1, 18-2, 18-3）

- 100 章拆书在 47 章断流
- batch 1-5 正常 → batch 6 部分失败 → batch 7-8 失败但 fallback 补救 → batch 9-11 失败且 fallback 未触发（缺口）→ batch 12-13 失败但 fallback 补救 → batch 14+ 完全未跑（ch048-ch100 全缺）
- fallback 覆盖率约 40%
- run e05dfa4d 连 response 都没产出

---

## 影响表现

- 53 章设计包永久缺失（ch048-ch100）；6 个文件丢失（方案B/方案C 全章等）
- Phase 1 未完成 → Phase 2/3/4 全部阻塞 → 全管线死亡
- v3.2/v3.3 核心架构改进（context 隔离 / create / revise / qa 三层独立检查）从根基崩塌
- agent 获得"走捷径"心理许可，永久放弃 spawn 改为直写
- spawn 失稳破坏力随管线长度非线性增长：5 个 spawn 时 fallback 能兜住，34 个 spawn 时覆盖率降至 ~40%

---

## 历史演进时间线

| 时间 | 文档编号 | 发现 |
|:-----|:---------|:-----|
| 6-23 | 08-1 | 结果捕获 100% 失败，61 设计包在磁盘但 orchestrator 读不到 |
| 6-25 | 10-2 | orphaned session 恢复失败（recovered=0, failed=3） |
| 6-27 | 15-1 | spawn 虚假 accepted + completion 未送达，agent 改直写 |
| 6-30 | 16-1~16-5 | gateway 断裂 + 并发放大 + 超时 + 无重启，复现条件明确 |
| 7-1 | 18-1~18-3 | 大规模复发 + fallback 不全（~40%）+ 长会话自发崩溃 |

---

## 相关文档

- [08-20260623-武林半侠传拆书中断-问题分析](../08-20260623-武林半侠传拆书中断-问题分析.md)
- [10-20260625-OpenClaw上下文溢出-问题分析](../10-20260625-OpenClaw上下文溢出-问题分析.md)
- [15-20260627-v3.3项目d前三章复盘-核心根因分析](../15-20260627-v3.3项目d前三章复盘-核心根因分析.md)
- [16-20260630-OpenClaw并发Spawn崩溃-问题分析](../16-20260630-OpenClaw并发Spawn崩溃-问题分析.md)
- [18-20260701-海贼法典拆书中断-问题分析](../18-20260701-海贼法典拆书中断-问题分析.md)
