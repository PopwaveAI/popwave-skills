# 长会话超时问题诊断与修复 PRD

> 版本：2026-08-10 v3 · 类型：缺陷诊断 + 修复需求 · 输出格式：Markdown
> 关联数据：`bug排查/runs/` 下 25 个 8.10 run（其中 8 个超时失败）

---

## 1. 问题定调

**40 章就触发压缩超时，属于产品缺陷，不是用户使用方式问题。**

用户在同一会话内连续写作（写章节、降 AI 味），属于正常且高频的使用路径。业界主流工具（Codex、Trae）均支持数百轮的长会话。本产品在正文累积约 40 章（每章 4500+ 字）时，上下文压缩（compaction）即超时并导致整个 run 失败，压缩容量与超时设计严重不匹配长会话预期。

**压缩必须是强制任务，不是异步任务。** 触发压缩即打断/冻结用户任务，压缩成功后再续传——这是 Trae 的做法，也是本 PRD 的整改方向。压缩失败导致整个 run 报错，本身就说明产品把"上下文治理的强制步骤"当成了"可失败的附属步骤"。

**一个关键事实**：8 个超时 run 中 `skills` 字段全部为空，没有任何 run 加载了 skill。但 `skills` 为空不代表 agent 没在执行 skill 职责——它只是没被注入 skill，凭训练知识临场发挥。超时的首因在 **harness 层**（应用运行时），skill 层是次级放大器，不是触发源。

---

## 2. 数据基础

| 项目 | 值 |
|:---|:---|
| 会话 | `5a816f28-4d29-4354-b3d8-17a5d47bc70a`（`两两成宝` 项目） |
| 8.10 run 总数 | 25 个 |
| 超时失败 run | 8 个 |
| run ID | `92c6b1b9` `92a0926c` `de5d17ce` `190773af` `818a9236` `bfd885e2` `52246208` `ec2300a4` |
| 触发的任务 | 继续写 21-40 章、降 AI 味 |
| 压缩超时 | 7 次 |
| LLM 请求超时 | 1 次（70 秒，`FailoverError`） |
| 历史注入 | `injectedHistoryTurns: 6`（每轮仅注入 6 轮） |
| skill 加载 | 全部为空 |

---

## 3. Harness 层问题（主因）

### 3.1 压缩触发机制（精确）：临界点触发，非固定比例；worker 单独超时且 no-retry

**触发不是按固定百分比，而是按"token 是否溢出预留区"。** 源码 `attempt.tool-run-context-CT5r1Qgk.js` 的 `shouldPreemptivelyCompactBeforePrompt`：

```
promptBudgetBeforeReserve = contextTokenBudget − effectiveReserveTokens
当 estimatedPromptTokens > promptBudgetBeforeReserve → 触发压缩
```

- `contextTokenBudget` = 会话 `contextTokens`（`runCliTurnCompactionLifecycle` 从 `sessionEntry.contextTokens` 读取）
- `effectiveReserveTokens` 取 `reserveTokens` 与 floor 的较大者，floor 默认 **20,000 token**（`agent-settings` 第6行 `DEFAULT_AGENT_COMPACTION_RESERVE_TOKENS_FLOOR = 2e4`）
- 逻辑：**context 涨到预算 − 2 万预留 token 就触发**，不是提前分卷归档，也不留额外余量——这正是"到临界点才处理"、40 章才爆的原因

**压缩规划 worker 有独立超时，且是本次 7/8 失败的直接原因。** 触发后压缩委托给 worker 线程（`tool-result-middleware-BUb-oCHG.js`）：

- 压缩规划 worker 默认超时 `COMPACTION_PLANNING_WORKER_TIMEOUT_MS = 60 秒`（第375行）
- 外层整体安全超时 `EMBEDDED_COMPACTION_TIMEOUT_MS = 180 秒`（第260行）
- worker 仅在消息数 ≥64 条时启用（`shouldUsePlanningWorker`，`messageCount >= COMPACTION_PLANNING_WORKER_MIN_MESSAGES`）
- 实测 `durationMs = 116086 / 117002`（约 116-117 秒）——落在 60~180 秒之间，是传入的 timeoutMs 生效，**worker 被 `worker.terminate()` 终止**，报 `compaction planning worker timed out`

**完整证据链（diag 行）：**

```
[compaction-diag] trigger=cli_budget provider=popwave/writing-standard
  attempt=1 maxAttempts=1 outcome=failed reason=guard_blocked durationMs=117002
```

- `trigger=cli_budget`：命中上面 token 预算公式才触发
- `attempt=1 maxAttempts=1`：**只尝试 1 次，无任何重试**
- `reason=guard_blocked`：safeguard 为保历史而**取消**压缩
- `durationMs=117002`：worker 超时后整个压缩被取消，run 失败
- 影响：7/8 次失败，全部是压缩规划 worker 超时，不是主请求超时

**真正的触发机制**：conversation transcript 并不是"干净的历史"，而是**被前几轮失败 run 的错误转储层层撑爆**。`input.json` 里 `injectedHistoryTurns: 6` 只注入 6 轮历史，但每一轮失败 run 的完整 fallback 诊断块（含 `raw_params` 全文、堆栈、错误摘要）都被当作"User/Assistant 历史"塞进了下一轮。于是：

1. 第 1 轮 fail（LLM 超时）→ 错误转储进历史
2. 第 2 轮 fail（edit 失配 + 压缩超时）→ 错误转储再进历史
3. 第 3 轮 fail（降AI）→ 历史已含前两轮巨型错误 → 立即命中 `cli_budget` → 触发压缩
4. 压缩 worker 必须一次性消化这堆被撑爆的 transcript → 超时
5. 压缩失败 → 整个 run 失败 → 错误转储又进历史 → 下一轮更大

**这是一个自我放大的负反馈环**：失败产生错误转储 → 错误转储撑大 context → context 撑爆触发压缩 → 压缩也失败 → 又产生错误转储。压缩失败不是孤立事件，是"失败循环"的其中一环。

### 3.2 压缩设计错误：尝试 1 次即放弃，且把压缩当"可失败步骤"

压缩失败后直接取消（safeguard 为保历史而取消），没有重试、没有"压缩一部分再继续"的兜底。对比 Trae：**压缩是强制的，触发即打断用户任务、冻结、压缩成功、再续传**。本产品把压缩当"可失败的附属步骤"，与正确设计相反。

用户的判断是对的：**压缩不是"异步化"的取舍，而是必须强制完成的前置死任务**。触发压缩就该打断/冻结用户任务，压缩成功才放行，压缩失败必须重试/分块直到成功，绝不因一次超时取消整个 run。

### 3.3 单次 LLM 请求 70 秒超时门槛过低

写 36-40 章时出现 `LLM request timed out`，单次请求 70 秒处理不动（`FailoverError`，`durationMs=70243`）。长会话下注入的历史 + 待生成正文使单次请求体量远超模型处理能力，70 秒阈值没有随请求体量放大。

### 3.4 压缩 worker 与主请求同源同限，落入同一陷阱

压缩 worker 与主会话共用同一模型与超时策略。当会话已巨大（40 章 + 失败转储），worker 要读取并概括全部历史，请求体量与主请求一样大，同样在 70 秒/117 秒尺度超时。**压缩本应"以更小体量治理更大上下文"，却把整个 transcript 一次性扔给 worker 单次消化**——与主请求犯了同一个"单次全量"错误。

### 3.5 修复方向（harness 层）

| # | 方案 | 说明 |
|:-:|:---|:---|
| H1 | 压缩强制化 + 断点续传 | 触发压缩即**打断/冻结**用户任务，压缩成功后自动续传；压缩期间不继续主 run。**压缩是强制任务，不是异步任务**（对齐 Trae） |
| H2 | 压缩必须成功，绝不放弃 | worker 失败要重试 / 分块压缩 / 流式摘要，`maxAttempts` 从 1 提升，绝不因一次超时取消整个 run |
| H3 | 压缩预算与超时扩容 | worker 的读取方式从"单次全量消化"改为"分块逐段摘要后合成"，超时阈值随体量动态放大 |
| H4 | 失败转储不污染历史 | **失败 run 的错误诊断块不得作为"历史"注入下一轮**，或仅注入一行摘要——从源头斩断失败负反馈环，这是比压缩扩容更前置的修复 |
| H5 | 增量历史注入 | 每轮按需注入关键历史（大纲/设定/最近章节），历史对话按相关性摘要注入 |
| H6 | 分卷归档 | 按卷/里程碑自动归档旧上下文，新上下文从归档摘要续写，避免触发压缩 |
| H7 | Edit 前强制重读最新内容 | **Edit 失配 22 次（6 run）的独立修复**：edit 前强制重读文件最新内容，杜绝用旧文本做 `old_str` 匹配 |

**H7 证据链（独立于压缩超时的第二个高频问题）：**

```
触发：Edit 工具报 "Could not find the exact text" / "edits["
分布：22 次失配，命中 6 个 run（818a9236 / 4b00ec05 / 52a9adb2 / 92a0926c / 7510bb70 / 92c6b1b9）
根因：章节文件被反复重写，agent 仍用旧文本做 old_str 定位替换 → 匹配失败 → Repeatedly fail → 错误转储又撑大 context
```

Edit 失配不是超时，但会二次放大：失配 → 重试 → 失败转储进历史 → context 增大 → 更快撞上压缩预算。它与压缩超时是**同一条负反馈环上的两个源头**。

---

## 4. Skill 层问题（次级放大器）

### 4.1 关键发现：`skills` 为空不代表没执行 skill 任务

8 个 run 的 `skills` 字段均为空，但两个"降AI味"run（`52246208`、`ec2300a4`）证明：**agent 在没有加载任何 skill 文档的情况下，自主进入了 `pop-ai-reduce` 的职责范围**。用户说"降AI味"，agent 就自行扫描模板词、逐章 read/write/edit，用的是自己训练知识里的网文模板词，执行的是**自创的伪降AI流程**，而非 skill v3.2.0 规范（无段落分层 L3/L2、无子 Agent 干净上下文、无双文件输出）。

这暴露一个比"没加载"更严重的问题：**系统未把 skill 注入，agent 凭训练知识临场发挥，质量失控且无规范约束**。`skills` 空 ≠ 没在干 skill 的活。

### 4.2 修正：pop-ai-reduce 设计上已是按章拆，放大器是"注入缺口"而非技能设计

**先纠正上一版 PRD 的误判。** `pop-ai-reduce`（v3.2.0）的 SKILL.md 与 `subagent-execution.md` 白纸黑字写明：

- SKILL.md 第 12 行："**每次任务仅处理一章正文。**"
- SKILL.md 第 17 行："超量必拆：主 Agent 先按章拆分，逐章发起独立子 Agent 任务，禁止一章塞多章"
- SKILL.md 红线 #8："**一次任务仅一章** — 严禁单次任务改写多章"
- `subagent-execution.md` 第 28 行："**一次任务仅组装一章原文。**"

也就是说，**技能设计层面已经实现了按章拆、单章独立上下文、干净子 Agent**——上一版 PRD 的 S1-S3"按章切分"是重复劳动。真实的放大器不是技能设计，而是：

1. **技能没被注入**（`skills=[]`）→ agent 凭训练知识临场发挥 → 才出现"整本全量透传"的伪流程
2. 伪流程 + 压缩 worker 单次全量消化 → 双重放大

所以修复重心从"改 skill 分片"（S1-S3，已完成）转向"**强制注入 skill + 输出规范校验**"（S4-S5）。

### 4.3 修复方向（skill 层）

| # | 方案 | 说明 |
|:-:|:---|:---|
| S4 | 强注入 skill | 命中 skill 意图时，host 必须把 SKILL.md 注入 prompt，杜绝 agent 凭训练知识临场发挥——**这是本节最高优先级** |
| S5 | 规范强制校验 | 输出前校验是否满足分层/叠层/双文件/单章等硬约束，不满足则不入库 |
| S1-S3 | （已在 v3.2.0 实现） | 按章拆、单章上下文、参考文件按需加载——保留为验收标准，不再作为待开发项 |

### 4.4 子 Agent 是否放大了超时问题

**是，但分两层看，且真正的放大点是 worker 而非 skill 子 Agent。**

第一层（直接放大）：**压缩规划 worker 本身就是一级子任务**（`[agent/embedded] [compaction-diag]` 表明它作为 embedded 子 run 运行）。压缩机制把"生成摘要"委托给这个 worker，而 worker 必须**单次读取并消化整个被失败转储撑爆的 transcript**——且 worker 有独立超时（默认 60s / 外层 180s，实测 116-117s 被 terminate，见 3.1）。子 Agent 本该提供"干净小上下文"，这里却成了"把全量塞进单个子任务"——子任务没有减小摘要负担，反而继承了主请求的"单次全量"陷阱，还叠加了自己的超时门槛。

第二层（间接放大）：当 skill 也要求子 Agent（如 pop-ai-reduce），且 agent 因未注入技能而全量临场发挥时，会把整章/整本文本透传给子 Agent，进一步增加 context 与单请求体量。但在本次 8 个失败 run 里，压缩失败发生在 run 启动时（agent 尚未动手降AI），**直接压垮 run 的是压缩 worker 超时，不是 skill 子 Agent**。

子 Agent 本身不是坏设计（干净上下文、防污染有效）。问题是两处原生放大：压缩 worker"单次全量消化"、以及失败转储污染历史。子 Agent 的任务粒度在整个 skill 生态里已按章/按卷受控。

### 4.5 同类放大风险 skill 排查（修正版）

对 `skills/` 下所有带子 Agent 或全量加载模式的 skill 做全量扫描，结论：**没有 skill 在设计上把整本喂给单次子任务**。

| skill | 子 Agent 模式 | 体量控制 | 风险 |
|:---|:---|:---|:---|
| `pop-ai-reduce` | 逐章独立子 Agent，每任务仅一章 | SKILL.md 红线 #8 强制单章 | **低**（设计已防放大；未注入时才失控） |
| `pop-decon` 家族 | `delegation-orchestration.md` 明确"分块扫描→并行产出→集中合成，避免一次性全量塞入一个子 agent（Token 爆炸）" | 按卷/按幕分批 | 低（设计已规避） |
| `pop-decon-design-pack` | quality=每章 1 子 agent；performance=每 30 章 1 子 agent 合并产出白描卡 | 单 agent 体量受控（30 章为批次上限） | 中低（批次有界，非整本） |
| `pop-decon-prd` / `pop-decon-setting` | 并行 2-4 子 agent 消费设计包 | 消费已提取的设计包，非整本原文 | 低 |
| `pop-fanqie-pipeline` / `pop-qidian-pipeline` | Phase 4 write 走子 Agent | 逐章渲染（write 单章） | 低 |
| `pop-research` | 子 Agent 读本文件 + 参考书 txt | 单本参考书，无整书堆叠 | 低 |
| `pop-recommend` | 三阶段扫描，100 章只精读 30-40 章 | 有采样控制 | 低 |

结论：**skill 层在设计上均已做按章/按卷/采样切分，没有"整本全量喂单任务"的高危项**。真正的放大风险不在 skill 设计，而在：

1. **技能注入缺口**（S4）——不注入则 agent 临场发挥，破坏既有切分约束
2. **harness 层压缩 worker 单次全量消化 + 失败转储污染历史**（H4）——这才是本次 7/8 失败的直接原因

---

## 5. 功能需求明细

### 5.1 压缩强制化 + 断点续传（H1）

| 字段 | 内容 |
|:---|:---|
| 触发 | 上下文达到压缩阈值时（见 3.1 精确机制） |
| 处理 | 立即**打断/冻结**当前用户任务，进入压缩阶段；压缩成功后自动续传主 run |
| 性质 | **强制任务**——压缩期间不继续主 run，不是后台异步 |
| 失败 | 压缩必须成功：worker 失败则重试或分块压缩，直到成功，绝不因一次超时取消整个 run |
| 结果 | 参考 Trae 的断点续传行为：压缩完成，用户任务无缝继续 |

### 5.2 失败转储不污染历史（H4，新增，P0）

| 字段 | 内容 |
|:---|:---|
| 触发 | 每轮 run 组装上下文时 |
| 处理 | 失败 run 的错误诊断块（fallback 块、raw_params 全文、堆栈）**不得作为"历史"注入下一轮**；如需保留，只注入一行摘要 |
| 结果 | 从源头斩断"失败→转储→context 撑爆→压缩失败→再失败"的负反馈环 |

### 5.3 压缩容量与请求超时扩容（H3）

| 字段 | 内容 |
|:---|:---|
| 目标 | 长会话（数百轮、数十万字正文）压缩不超时 |
| worker 读取 | 从"单次全量消化 transcript"改为"分块逐段摘要后合成" |
| 请求超时 | 随单次请求体量动态放大，而非固定 70 秒 |
| 验收 | 40 章长会话连续写作不再触发压缩超时 |

### 5.4 增量历史注入（H5）

| 字段 | 内容 |
|:---|:---|
| 触发 | 每轮 run 组装上下文时 |
| 处理 | 优先注入大纲、世界观设定、最近 N 章正文；历史对话按相关性摘要注入 |
| 结果 | context 增长从超线性降为近线性，压缩触发频率下降 |

### 5.5 分卷归档（H6）

| 字段 | 内容 |
|:---|:---|
| 触发 | 达到卷/里程碑边界（如每 10 章） |
| 处理 | 将已成卷章节归档为摘要，后续上下文从摘要续写，不再携带全量 |
| 结果 | 长会话可控，不与压缩容量冲突 |

### 5.6 skill 强注入 + 规范校验（S4-S5）

| 字段 | 内容 |
|:---|:---|
| 触发 | 命中 skill 意图（如"降AI味"命中 `pop-ai-reduce`）时 |
| 处理 | host 必须把 SKILL.md 注入 prompt，杜绝 agent 凭训练知识临场发挥；输出前校验单章/分层/双文件等硬约束 |
| 结果 | 既有 skill 的按章切分设计真正被遵守，不再因未注入而临场全量 |

### 5.7 Edit 失配修复（H7，新增，P1）

| 字段 | 内容 |
|:---|:---|
| 触发 | `Edit` 工具失配时报 `Could not find the exact text` / `edits[`（22 次 / 6 run） |
| 处理 | **edit 前强制重读文件最新内容**；对整章/大段改写改用追加或整段覆写，替代定位替换 |
| 结果 | 消除 22 次失配，切断"失配→重试→失败转储→context 撑爆"的二次放大 |

---

## 6. 分级与优先级

| 优先级 | 项 | 依据 |
|:---|:---|:---|
| P0 | H4 失败转储不污染历史 | **斩断失败负反馈环**，从源头防 context 被失败撑爆，最前置 |
| P0 | H1 压缩强制化 + H2 压缩必须成功 | 直接消除 7/8 次"全 run 失败" |
| P0 | H3 压缩分块 + 超时扩容 | 根治 40 章压缩超时，对标长会话预期 |
| P1 | S4 skill 强注入 | 消除 agent 未注入技能时的临场全量放大 |
| P1 | H7 Edit 失配修复 | 消除 22 次高频工具报错，切断第二个放大源 |
| P2 | H5 增量历史注入 / H6 分卷归档 | 降低压缩触发频率，长期支撑超长会话 |
| P2 | S5 输出规范校验 | 保障注入后 skill 约束真正被执行 |

---

## 7. 本次复盘修正记录

| 上一版结论 | 本次修正 | 证据 |
|:---|:---|:---|
| pop-ai-reduce 整本全量透传子 agent，最高风险 | 设计上已是按章拆，放大器是**注入缺口**而非设计 | SKILL.md 红线 #8 + subagent-execution.md 第 28 行 |
| S1-S3 需开发（按章切分） | 已在 v3.2.0 实现，转为验收标准 | SKILL.md 第 12/17 行 |
| 压缩"异步化"是方向 | **压缩是强制、打断、冻结、续传的死任务**，非异步 | `guard_blocked` + 用户/ Trae 行为对齐 |
| 压缩失败是孤立事件 | 是**失败转储污染历史**的负反馈环一环 | `input.json` 失败转储注入历史 + `trigger=cli_budget` |
| skill 层存在"整本喂单任务"高危项 | 全量扫描无一整本高危项，decon 已显式规避 Token 爆炸 | `delegation-orchestration.md` |
| 压缩按固定比例触发 | **临界点触发**：context 涨到预算 − 2 万预留 token 即触发，非固定百分比 | `attempt.tool-run-context-CT5r1Qgk.js` 公式 + `agent-settings` floor=2e4 |
| 压缩 worker 超时来源不明 | **worker 独立超时**：默认 60s / 外层 180s，实测 116-117s 命中传入 timeoutMs 被 terminate | `tool-result-middleware` 第375/260行 + `durationMs=117002` |
| 高频报错仅限压缩超时 | **Edit 失配 22 次（6 run）是独立高频问题**，与压缩超时同属一条负反馈环的两个源 | 6 个 run 的 `Could not find the exact text` |