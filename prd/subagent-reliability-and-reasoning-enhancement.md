# PRD: 子Agent 可靠性与推理增强

> 创建日期：2026-06-29
> 状态：待确认
> 作者：pop
> 数据来源：6-26项目c（22个run）+ 6-28项目b（33个run，130个子agent session）

## TL;DR

子agent 存在两类独立问题：**框架层静默失败**（5个根因，导致子agent产出丢失或错误）和**推理能力未释放**（思维链内容丢弃+reasoning_effort 未配置，导致质量不稳定）。本 PRD 合并三条调查线索，给出统一的修复优先级和实施方案。

## 问题全景

### 框架层：子Agent 静默失败

6-26项目c 的 22 个 run 扫描确认 5 个独立根因，其中 3 个框架层、2 个 skill 层：

| # | 根因 | 层级 | 现象 |
|:--|:-----|:-----|:-----|
| RC-1 | Gateway WebSocket 断裂 | 框架 | `1006 abnormal closure` 导致子agent session 成为 orphaned，completion event 永久丢失 |
| RC-2 | sessions_spawn 虚假 accepted | 框架 | 返回 `status: accepted` 但子agent session 文件从未持久化 |
| RC-3 | 无 completion 超时熔断 | 框架 | yield 后无限挂起，无 error、无降级 |
| RC-4 | context 组装漏传种子 | Skill | ch002 的 spawn task 未包含种子六要素，子agent凭记忆脑补出「海因里希」 |
| RC-5 | 无角色名交叉校验 | Skill | 三层校验只覆盖行为维度，不核对命名一致性 |

**关键异常信号**：14/22 个 run 使用 exec 轮询文件系统（最高 58 次），直接违反 spawn 返回的明确指令 `do NOT call sessions_list, sessions_history, exec sleep, or any polling tool`。push-based completion event 机制普遍性失效，agent 被迫降级为轮询模式。

### 推理层：思维链潜力未释放

6-28项目b 的 33 个 run + 130 个子agent session 扫描确认 3 个问题：

| # | 问题 | 现状 | 影响 |
|:--|:-----|:-----|:-----|
| R-1 | reasoning_effort 未配置 | 全部用默认 `high`，未启用 `max` | V4-Flash 从 high→max 正确率 45%→80%（实测 20 任务） |
| R-2 | 28/130 子agent reasoningTokens=0 | 22% 的 session 产生零推理 token | 质量不可控，无法区分"不需要推理"和"推理被抑制" |
| R-3 | 思维链内容丢弃 | `PAOPAO_OPENCLAW_RAW_THINKING_STREAM` 未开启 | 主session 做 receipt 检查时看不到子agent推理过程，无法诊断偏离原因 |

**实测数据**：V4-Flash `high` 模式 20 任务正确率 9/20（45%），`max` 模式 16/20（80%），输出 token 增加 4 倍，延迟增加约 400ms。官方建议 max 模式上下文窗口至少 384K。

## 目标

| 优先级 | 目标 | 衡量标准 |
|:-------|:-----|:---------|
| P0 | 消除子agent静默失败 | 10章测试中0个无 response.md 的 run |
| P0 | 思维链内容可见 | 主session能查看子agent思维链临时文件 |
| P1 | create/revise 启用 reasoning_effort=max | reasoningTokens 平均值从 ~420 提升到 ≥1500 |
| P1 | context 全文注入（种子+L2卡+文风DNA） | spawn task payload 包含完整种子六要素 |
| P2 | receipt 检查增加 reasoning 监控 | 0-token 子agent自动标记为质量风险 |
| P2 | 命名一致性校验 | qa 质检报告包含命名核对项 |

## 框架层修复方案

### RC-1+RC-3: Gateway 断裂 + 无超时熔断

**根因**：OpenClaw 子agent调度依赖本地 `ws://127.0.0.1:18789` WebSocket gateway 进行 push-based completion event 传递。gateway 断裂时（1006），正在运行的子agent成为 orphaned，completion event 无法推送回主 session，主agent在 `sessions_yield` 后永久阻塞，无 timeout、无 error、无降级。

**证据**：多个 run 的 stderr 中出现 `[subagent-interrupted-resume] failed to resume orphaned session` + `gateway closed (1006 abnormal closure)`。同一 orphaned session UUID 在多个 run 中反复出现，说明 OpenClaw 重启后尝试 resume 但 gateway 始终不可用。

**修复方向**：
- `sessions_yield` 增加超时参数（如 120s），超时后返回 timeout error
- Gateway 增加 heartbeat 检测和自动重连
- Completion 丢失时主动通知主agent降级

**所属层**：OpenClaw 框架（需平台开发）

### RC-2: 虚假 accepted

**根因**：`sessions_spawn` 存在先返回后持久化的竞态问题。API 返回 `accepted` + `childSessionKey` + `runId`，但子agent session 文件从未写入磁盘。对 1e41b6f2 run 中 spawn 的 5 个子agent的 10 个 UUID 在 OpenClaw 状态目录中全部搜索不到。

**修复方向**：spawn 在 session 文件持久化成功后才返回 accepted，或区分 `accepted`（排队中）和 `persisted`（已落盘可追踪）两种状态。

**所属层**：OpenClaw 框架（需平台开发）

### RC-4: context 漏传种子

**根因**：步骤文件写明了要传种子六要素，但主agent在长会话中凭记忆拼凑 context 时遗漏。ch002 的 spawn task 中没有种子六要素、没有主角全名、没有行为准则详细映射、没有压力矩阵、没有冲突轴、没有活跃线索——只有 chapter_plan 和简化的行为准则。子agent凭记忆脑补出「索伦·海因里希」，而种子文档只规定主角名=索伦，ch001 正文写的是汤姆·索伦森。

**修复方向**（已在 v9.5.0~v9.8.0 实施）：
- v9.5.0：L2卡替代种子文档，context manifest 白盒注入
- v9.7.0：全文注入铁律（红线❌8），禁止主agent摘要后注入
- v9.8.0：网文铁律8条内联，强化创作质量约束

**所属层**：expert-writer skill（已修复，需验证）

### RC-5: 无命名校验

**根因**：create/revise/qa 三层校验全部聚焦于行为/道德/战斗风格是否偏离种子设定，不涉及命名核对。当 context isolation 下子agent根本不读种子文件时（RC-4），缺少独立的命名校验作为安全网。

**修复方向**：revise 子agent增加命名一致性检查项，核对正文中的角色名与 L2卡/设定文件是否一致。

**所属层**：expert-writer skill

## 推理层修复方案

### R-1: reasoning_effort=max 透传

**当前状态**：DeepSeek V4 Flash 原生支持 `reasoning_effort` 参数（`high` / `max`），官方建议复杂 Agent 场景直接上 `max`。`openclawAgentWorker.js` 第260行附近已有提取逻辑（`if(t?.reasoning_effort)`），但 `sessions_spawn` 的 task payload 中未包含此字段。

**API 参数定义**（DeepSeek 官方文档）：

| 参数 | 可选值 | 默认值 | 说明 |
|:-----|:-------|:-------|:-----|
| `thinking.type` | `enabled` / `disabled` | `enabled` | 控制思考模式开关 |
| `reasoning_effort` | `high` / `max` | `high` | 控制推理深度。复杂 agent 请求自动设为 max。兼容映射：low/medium→high，xhigh→max |

**改动点**：
- `step-2-3-dispatch-create-revise.md`：create/revise 子agent spawn 时，task payload 新增 `reasoning_effort: "max"`
- `SKILL.md`：5步循环门禁表 Step3 行，硬门禁列新增"reasoning_effort=max 已设置"

**配置策略**：

| 子agent 类型 | reasoning_effort | 理由 |
|:-------------|:-----------------|:-----|
| create（涌现写作） | max | 创作需要深度推理：情节逻辑、人物动机、爽感设计、设定一致性 |
| revise（完全重写） | max | 修订需要深度推理：文风匹配、导演意图验证、事实一致性检查 |
| pop-research（调研） | high（默认） | 调研以信息检索为主，推理深度需求中等 |
| 其他工具调用 | 不设置 | 文件读取等简单操作不需要推理 |

**交互逻辑**：

```
expert-writer step-2-3 dispatch
  → task payload 中新增 reasoning_effort 字段（值由 skill 层决定）
  → Popwave Agent tool 调用传入 task
  → OpenClaw sessions_spawn 接收
  → openclawAgentWorker.js 提取 reasoning_effort
  → DeepSeek API 请求体包含该参数
  → 模型按指定深度推理
```

**边界与异常**：
- 如果 Paopao tool 调用不支持透传自定义字段：降级方案为在 task prompt 开头注入 `/reasoning_effort max` 文本前缀
- 如果 OpenClaw 版本不支持 `reasoning_effort`：需升级 OpenClaw 到支持 V4 Flash 参数的版本

### R-3: 思维链内容可见性

**当前状态**：`openclawAgentStream.js` 第39-40行检查环境变量 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM`，第424行将思维链内容写入 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM_PATH` 指定的临时目录。当前环境变量未开启，思维链内容产生后即丢弃，只保留 token 计数。

**改动点**：
- 设置环境变量 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM=1`
- 设置临时文件目录 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM_PATH`（如 `C:\Users\AWMPRO\AppData\Local\Temp\paopao-thinking-streams\`）
- 子agent session 结束后，思维链内容以 JSONL 格式写入临时文件

**限制**：思维链内容不注入回上下文。DeepSeek API 明确要求多轮对话中 `reasoning_content` 不能作为输入消息传回，否则返回 400 错误。思维链内容仅供主 session 在 receipt 检查失败时按需读取诊断。

### R-2+诊断: 失败诊断能力

**当前状态**：Step4 receipt 检查失败时，主 session 只能看到子agent的最终产出（receipt YAML），无法看到推理过程。如果子agent偏离导演意图，主 session 无法判断"子agent为什么会这么写"。

**改动点**：
- `step-2-4-receipt-check.md`：receipt 检查失败时，新增诊断步骤——读取对应子agent session 的思维链临时文件
- 诊断信息不写入活记忆或项目总控，仅供主 session 判断"重试还是降级"

**诊断流程**：

```
Step4 receipt 检查失败
  → 读取子agent session ID（从 spawn 结果获取）
  → 定位思维链临时文件（按 session ID 查找）
  → 读取思维链内容
  → 判断失败原因（理解偏差/信息缺失/推理不足）
  → 决策：重试（补充 context manifest）/ 降级主会话执行
```

## 次要问题

| 问题 | 说明 | 优先级 |
|:-----|:-----|:-------|
| 401 认证过期 | 重新登录可解决，与调度链路无关 | — |
| workspace 文件路径混乱 | 主agent在错误路径查找子agent产出文件，被迫用 `Get-ChildItem -Recurse` 搜索 | P2 |
| taskName 命名不统一 | 统一为 `ch{NNN}-{create\|revise\|qa}[-v{N}]` | P3 |
| exec 轮询普遍化 | 14/22 个 run 使用 exec 轮询（最高 58 次），修复 RC-1/2/3 后 push-based 恢复可靠则自动消除 | P2（依赖 P0） |

## 根因关系图

```
用户发起写作请求
  → expert-writer 主会话
    → Step 0/1: 规划+信息获取
      → Step 2: sessions_spawn create子agent
        │
        ├─ RC-2: spawn 返回 accepted？
        │   ├─ session未持久化 → RC-1: gateway断裂 → RC-3: 无限挂起 = 静默失败
        │   └─ session已持久化 → 子agent正常执行
        │       └─ completion event到达？
        │           ├─ 是 → 主agent收到结果继续
        │           └─ 否（gateway断裂）→ RC-3: 无限挂起 → agent自行降级: exec轮询
        │
        ├─ RC-4: context含种子？
        │   ├─ 是 → 子agent正确引用种子
        │   └─ 否 → 子agent凭记忆脑补 → RC-5: 无命名校验 → bug流入正文
        │
        └─ R-1: reasoning_effort？
            ├─ max → 深度推理（正确率80%）
            └─ high（默认）→ 浅推理（正确率45%）
                └─ R-2: reasoningTokens=0 → 无推理 → 质量不可控
```

## 修复优先级矩阵

| 优先级 | 根因 | 修复方向 | 所属层 | 预估难度 |
|:-------|:-----|:---------|:-------|:---------|
| P0 | RC-1+RC-3: gateway断裂+无熔断 | yield 增加超时机制；gateway 增加 heartbeat 和自动重连 | OpenClaw 框架 | 高 |
| P0 | RC-2: 虚假accepted | spawn 在 session 文件持久化成功后才返回 accepted | OpenClaw 框架 | 中 |
| P0 | R-3: 思维链内容丢弃 | 设置 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM=1` | 环境变量配置 | 低 |
| P1 | R-1: reasoning_effort 未配置 | task payload 新增 `reasoning_effort: "max"` | expert-writer skill | 低 |
| P1 | RC-4: context漏传种子 | 全文注入铁律（v9.7.0已实施） | expert-writer skill | 已完成 |
| P1 | RC-5: 无命名校验 | revise 增加"命名一致性检查"项 | expert-writer skill | 低 |
| P2 | R-2: 0-token 子agent | receipt 检查增加 reasoningTokens 监控（依赖 R-1 平台改动） | expert-writer skill | 低 |
| P2 | exec 轮询普遍化 | 修复 RC-1/2/3 后自动消除 | OpenClaw 框架 | 依赖 P0 |
| P2 | workspace 路径混乱 | spawn 时在 task payload 中明确指定 outputPath | expert-writer skill | 低 |
| P3 | taskName 命名不统一 | 统一命名规范 | expert-writer skill | 极低 |

## 实施计划

| 阶段 | 事项 | 依赖 | 预估工时 |
|:-----|:-----|:-----|:---------|
| Phase 1 | 设置 `PAOPAO_OPENCLAW_RAW_THINKING_STREAM=1`，开启思维链可见性 | 无 | 0.5h |
| Phase 1 | 运行一轮 create/revise，检查临时文件中思维链内容是否完整 | 环境变量已设 | 1h |
| Phase 2 | step-2-3 新增 `reasoning_effort: "max"` 配置 | 无 | 0.5h |
| Phase 2 | revise 新增命名一致性检查项 | 无 | 0.5h |
| Phase 2 | 10章测试验证：导演意图执行率 ≥70%，事件密度 ≥60%，0个无 response.md 的 run | Phase 1+2 完成 | 2h |
| Phase 3 | 向 Paopao/OpenClaw 提交框架层修复需求（RC-1/2/3） | 平台开发排期 | — |
| Phase 3 | receipt 检查增加 reasoningTokens 监控（依赖平台返回该数据） | 平台改动完成 | 1h |

## 风险

| 风险 | 影响 | 缓解 |
|:-----|:-----|:-----|
| `reasoning_effort=max` 导致输出 token 膨胀 4 倍 | 成本增加、延迟增加 ~400ms | 仅对 create/revise 启用，文件读取等保持默认 |
| max 模式建议上下文 ≥384K | 当前上下文可能不足导致截断 | 需检查当前 input token 用量 |
| 思维链内容包含敏感信息 | 临时文件泄露风险 | 确认临时文件目录权限和清理策略（如 7 天） |
| 框架层修复依赖平台排期 | RC-1/2/3 无法在 skill 层面解决 | skill 层先做已能做的（全文注入+reasoning_effort+命名校验），框架层问题同步提需求 |

## 验收标准

| 验收项 | 验收标准 | 验证方法 |
|:-------|:---------|:---------|
| RC-1/3 修复 | gateway 断裂后 yield 在 120s 内返回 timeout error | 模拟 gateway 关闭，验证 yield 不无限挂起 |
| RC-2 修复 | spawn 返回 accepted 后 session 文件必须存在于磁盘 | spawn 后立即检查 sessions 目录 |
| RC-4 修复 | spawn task payload 包含完整种子/L2卡全文 | 检查 events.jsonl 中 spawn input |
| RC-5 修复 | revise 质检报告包含"命名一致性检查"项 | 检查 revise receipt |
| R-1 修复 | create/revise 子agent reasoning_effort=max | 检查 task payload 含 `reasoning_effort: "max"` |
| R-2 修复 | 0-token 子agent 从 28/130 降到 ≤5/130 | trajectory 统计 |
| R-3 修复 | `%TEMP%\paopao-thinking-streams\` 下有思维链 JSONL 文件 | 文件系统检查 |
| 整体质量 | 10章测试中导演意图执行率 ≥70%，事件密度 ≥60% | 10章批量测试 |
| 静默失败消除 | 10章测试中 0 个无 response.md 的 run | 统计 response.md 存在率 |
