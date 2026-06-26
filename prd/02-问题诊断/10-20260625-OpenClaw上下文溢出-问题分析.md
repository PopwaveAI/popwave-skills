# OpenClaw 上下文管理问题 PRD：Truncation 替代 Compaction 导致信息丢失

> **PRD · 2026-06-25 · Platform Engineering**
> **P0 · 核心流程缺陷** | context-management | openclaw | evidence-based
> 基于 project `6-24-项目b` 的 runs 数据与源码逆向分析

---

## 1. 问题背景

2026-06-24，项目 `6-24-项目b`（《魔窟攻略组》）在单会话中连续写作 12 章。复盘发现正文质量从 ch004 开始断崖式下降：设计包字数从 27,786 字跌至 6,102 字，正文字数从 2,811 字递减至 1,420 字。用户连续 20 次发送相同消息"继续下一步 严格按skill执行"，说明 agent 在写作过程中已偏离 skill 规范。

初步排查排除了 skill 版本不一致（7 个 skill 全部匹配最新版本）和项目配置错误（state-log.yaml 正常运作）的可能性。根因指向 OpenClaw 平台的上下文管理机制：在 900K tokens 的上下文窗口中，prompt tokens 只使用了 56.6%，远未溢出，但 `tool-result-truncation` 层从 42.9% 时开始丢弃历史工具结果，而本应触发的 `compaction`（摘要压缩）从未启动。

本文档基于 `runs/` 目录中 41 次运行的 events.jsonl 数据、conversation 日志、以及 OpenClaw 源码逆向分析，建立完整证据链。

> **核心问题**：OpenClaw 的 compaction 是**被动触发**（reactive）——仅当 LLM 返回 context overflow 错误时才启动。但 tool-result-truncation 层提前截断了工具结果，使上下文恰好不溢出，导致 compaction 永远不被触发。结果是：信息被**丢弃**（truncation）而非**压缩**（compaction）。

---

## 2. 证据链

### 2.1 证据一：Prompt Tokens 单调递增，从未溢出

从 `runs/` 目录的 41 次 run 的 `events.jsonl` 中提取 `promptTokens` 和 `contextTokens` 字段。上下文窗口固定为 900,000 tokens，prompt tokens 从 14.6% 单调递增至 56.6%，全程未触及上限。

| Run ID | 时间 | PromptTokens | 上下文占比 | Truncation | Compaction |
|:-------|:-----|:------------|:---------|:----------|:----------|
| 0de71485 | 21:09 | 131,413 | 14.6% | 0 | 0 |
| f66656ad | 21:20 | 169,349 | 18.8% | 0 | 0 |
| 07679c79 | 21:32 | 187,960 | 20.9% | 0 | 0 |
| 8d220b08 | 22:03 | 249,805 | 27.8% | 0 | 0 |
| 43bb9a03 | 22:26 | 281,347 | 31.3% | 0 | 0 |
| 26ad0792 | 23:28 | 333,959 | 37.1% | 0 | 0 |
| 0f5eaf03 | 00:11 | 386,527 | **42.9%** | 0 | 0 |
| 8ca1abd6 | 00:16 | 395,134 | 43.9% | **1** | 0 |
| 44f72971 | 00:22 | 421,584 | 46.8% | **1** | 0 |
| 20cebed8 | 00:29 | 429,764 | 47.8% | **1** | 0 |
| d13d7d71 | 00:36 | 437,451 | 48.6% | **2** | 0 |
| a63cd27a | 00:37 | 452,310 | 50.3% | **1** | 0 |
| f587993e | 00:43 | 458,526 | 50.9% | **1** | 0 |
| f490af61 | 00:45 | 477,370 | 53.0% | **0** | 0 |
| 7a4154a2 | 00:47 | 494,186 | 54.9% | **1** | 0 |
| f3245b7d | 00:51 | 509,677 | **56.6%** | **1** | 0 |
| 9f63ce28 | 00:54 | 81,488 | 9.1% | 0 | 0 |

**数据来源**：`C:\Users\AWMPRO\.paopao\projects\6-24-项目b\runs\*/events.jsonl` 中 `outputSummary.usage` 字段的 `promptTokens` 和 `contextTokens` 值。

**关键拐点**：
- **42.9%**（00:11, run 0f5eaf03）—— truncation 即将首次触发。下一 run（8ca1abd6, 00:16）出现 Truncation=1
- **56.6%**（00:51, run f3245b7d）—— 全程最高点，509K/900K，仍远未溢出
- **9.1%**（00:54, run 9f63ce28）—— 突降回 81K，说明会话被重置或新建

### 2.2 证据二：Compaction 从未触发

在全部 41 个 run 中，Compaction 列的值**全部为 0**。对 openclaw 运行日志（`C:\Users\AWMPRO\AppData\Local\Temp\openclaw\openclaw-2026-06-24.log`，61MB）搜索 `compact` 关键词，返回 **0 条实际 compaction 执行记录**。所有 "compact" 关键词匹配均来自字段名（如 `compactionTokensAfter`、`compactParams`），而非 compaction 事件。

源码分析确认了原因。OpenClaw 的 compaction 触发逻辑位于 `D:\popwave\resources\openclaw\openclaw\dist\embedded-agent-BgvyyCVT.js`，触发条件为：

- **Layer 2 (Overflow Recovery)**：LLM 返回 context overflow 错误时触发。本项目 prompt tokens 最高 56.6%，LLM 从未 overflow
- **Layer 3 (Timeout Compaction)**：LLM 超时**且** `tokenUsedRatio > 0.65` 时触发。truncation 将 token 使用率压在 65% 以下
- **Layer 4 (Background Compaction)**：需配置 `turnMaintenanceMode: "background"`。项目 `openclaw.json` 中未配置

> **根因确认**：三层 compaction 触发条件均未满足：**不溢出 → Layer 2 不触发**；**truncation 压制了 token 使用率 → Layer 3 不触发**；**未配置 background 模式 → Layer 4 不触发**。Compaction 永远不会被启动。

### 2.3 证据三：Truncation 递增与质量下降时间吻合

将 truncation 首次出现时间与正文字数、设计包字数下降时间交叉对比：

| 时间段 | 对应章节 | Truncation | 正文字数 | 设计包字数 |
|:------|:--------|:----------|:--------|:---------|
| 21:09-23:28 | ch1-ch3 | 0 次 | 2811→1909→2055 | 20K-28K |
| 00:11-00:16 | ch3→ch4 过渡 | **首次出现** | ch4: 2029 | **ch4: 6102 ← 断崖** |
| 00:22-00:51 | ch5-ch12 | 持续 1-2 次/run | 1652→1486→1420 | 3K-5K |

**数据来源**：正文字数由 `Get-Content ch*.md` 统计去空白字符数；设计包字数同法统计；Truncation 数据来自 events.jsonl。

truncation 在 00:16（ch4 写作期间）首次触发，设计包字数在同一时间点从 27,786 字断崖式下降到 6,102 字。这不是巧合——truncation 丢弃了 chapter skill 的设计包模板和早期章节的参考内容，导致 agent 从 ch4 开始丢失了写作规范。

### 2.4 证据四：Conversation 日志中的截断模式

主对话文件 `61986530-c3bb-4e18-9941-636847fa987e.jsonl`（2.8MB，78 行）中发现 **25 处 truncation 匹配**，模式为：

```
[tool-result-truncation] Truncated N tool result(s) for prompt history (maxChars=64000 aggregateBudget)
```

截断数量随对话推进**逐步升级**：

| 对话阶段 | 被截断的工具结果数 |
|:--------|:----------------|
| 早期（ch1-ch3） | 3 → 6 |
| 中期（ch4-ch8） | 11 → 14 |
| 后期（ch9-ch12） | 15 → 16 → **17** |

到 ch9-ch12 时，agent 已经看不到 17 个历史工具结果——包括 chapter skill 的设计包模板、prose skill 的渲染规范、早期章节的文风锚定等。第一次截断甚至发生在 `项目总控.md` 模板本身。

### 2.5 证据五：辅助错误加剧上下文负担

openclaw 日志还显示该 session 存在大量非 overflow 错误，这些错误的重试进一步消耗上下文预算：

| Run | 时间 | 错误类型 | 影响 |
|:----|:-----|:--------|:-----|
| 5c0a8449 | 23:06 | 401 AI 访问令牌无效或已过期 | Run 完全失败（OutKB=0） |
| b58a91bb | 23:10 | 401 AI 访问令牌无效或已过期 | Run 完全失败（OutKB=0） |
| 8d220b08 | 22:03 | 3 个 orphaned subagent session 恢复失败 | recovered=0 failed=3 skipped=56 |

这些错误均不触发 context overflow recovery，因此 compaction 不会被启动。但重试机制会增加上下文中的错误-重试对话轮次，间接加速 truncation 的触发。

---

## 3. 根因分析

### 3.1 OpenClaw 四层上下文管理架构

通过逆向分析 `D:\popwave\resources\openclaw\openclaw\dist\` 下的源码，OpenClaw 有四层上下文管理：

```
┌─────────────────────────────────────────────────────────────────┐
│ Layer 1: Tool Result Truncation（预截断 · 每轮触发）              │
│ · 每轮 LLM 调用前自动触发                                         │
│ · 单工具结果上限: 64,000 chars                                    │
│ · 总量上限: 256,000 chars                                         │
│ · 策略: head+tail 截断（保留头尾，中间用 [... omitted] 替换）      │
│ · 不可逆：截断后原始内容从 session 中永久丢失                       │
└──────────────────────────┬──────────────────────────────────────┘
                           │ 截断后不溢出
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 2: Context Overflow Recovery（被动 · 溢出时触发）            │
│ · 触发条件: LLM 返回 context overflow 错误                        │
│ · 恢复流程: 先尝试 truncation → 再触发 auto-compaction             │
│ · 最多重试 MAX_OVERFLOW_COMPACTION_ATTEMPTS = 3 次                 │
│ · 本项目状态: 从未触发（prompt tokens 最高 56.6%，未溢出）          │
└──────────────────────────┬──────────────────────────────────────┘
                           │ overflow 不发生
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 3: Timeout Compaction（被动 · 超时+高占用时触发）            │
│ · 触发条件: LLM 超时 且 tokenUsedRatio > 0.65                     │
│ · 本项目状态: 从未触发（truncation 压制了 token 使用率 < 65%）      │
└──────────────────────────┬──────────────────────────────────────┘
                           │ token 使用率 < 65%
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│ Layer 4: Background Compaction（后台 · 延迟触发）                  │
│ · 触发条件: ownsCompaction=true 且 turnMaintenanceMode=background │
│ · 本项目状态: 从未触发（openclaw.json 中未配置）                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │ 未配置
                           ▼
                    ╔═══════════════════╗
                    ║ Compaction 从未触发 ║
                    ╚═══════════════════╝
```

### 3.2 为什么 Compaction 从未被触发

核心矛盾在于 Layer 1（truncation）和 Layer 2（compaction）之间的**触发条件互斥**：

```
对话增长 → 工具结果累积 → 总量接近 256KB 预算
    ↓
Layer 1 触发 truncation（截断最旧/最大的工具结果）
    ↓
上下文被压回 256KB 以内 → LLM 调用不会 overflow
    ↓
Layer 2 的 overflow 触发条件永远不满足
    ↓
Compaction（摘要压缩）永远不启动
    ↓
信息被丢弃（truncation）而非压缩（compaction）
```

### 3.3 Truncation vs Compaction：信息保留对比

| 维度 | Tool Result Truncation（实际发生） | Compaction（应该发生但没发生） |
|:-----|:-------------------------------|:---------------------------|
| 机制 | 截断工具结果，替换为 `[... truncated]` | 将旧对话摘要为 compact summary |
| 信息保留 | **丢失**——原始内容不可恢复 | **保留**——关键信息被压缩进摘要 |
| 可逆性 | **不可逆**——session 文件被重写 | **可逆**——原始 session 有 checkpoint |
| 触发条件 | 每轮 LLM 调用前自动触发 | 仅 LLM overflow/timeout 时触发 |
| 对 agent 的影响 | 看到 Swiss cheese 上下文 | 看到压缩但完整的摘要 |

### 3.4 配置层面的发现

从 `C:\Users\AWMPRO\.openclaw-novel-buddy\openclaw.json` 配置文件看：

- `agents.defaults.contextTokens`：未配置（无上限 cap）
- `agents.defaults.compaction.model`：未配置（无专用压缩模型）
- `agents.defaults.compaction`：完全未配置

这意味着 OpenClaw 使用的是默认的被动 compaction 策略，没有配置任何主动 compaction 机制。

---

## 4. 影响评估

### 4.1 对写作管线的实际影响

truncation 丢弃的信息按重要性排序：

| 被丢弃的信息 | 丢弃时间 | 对产出的影响 |
|:-----------|:--------|:-----------|
| chapter skill 设计包模板 | ch4 前后 | 设计包从 20K 字退化为 4-6K 字 |
| prose skill 渲染规范 | ch4-ch6 | 正文从场景渲染退化为事件流水账 |
| 早期章节文风锚定 | ch6-ch8 | PRD 定义的"牢A式黑色幽默"完全消失 |
| 角色卡和关系动态 | ch8-ch10 | 角色行为一致性下降 |
| state-log 早期基线 | ch10-ch12 | 伏笔追踪和跨章弧线断裂 |

### 4.2 影响范围

该问题**不仅影响本项目**。任何在 OpenClaw 上进行长会话操作（超过 ~10 轮工具调用）的 agent 都会遇到相同问题。写作管线因为单章需要 5-8 个工具调用（Read skill → Read 设计包 → Write 正文 → Write state-log 等），是重灾区。但代码开发、研究分析等需要长会话的场景同样受影响。

---

## 5. 解决方案

### 5.1 平台层（OpenClaw 配置）

**方案 A：配置主动 compaction（推荐）**

在 `openclaw.json` 中配置基于阈值的自动 compaction，使 compaction 在 token 使用率达到阈值时主动触发，而非等待 overflow：

- 设置 `agents.defaults.compaction.triggerRatio` 为 `0.5`（token 使用率 >50% 时触发）
- 设置 `agents.defaults.compaction.model` 指定专用压缩模型
- 设置 `turnMaintenanceMode: "background"` 启用后台 compaction

这样 compaction 会在 truncation 之前介入，将旧对话摘要为 compact summary，保留关键信息。

**方案 B：调整 truncation 策略**

- 将 `aggregateBudgetChars` 从 256KB 调高到 512KB 或更高，推迟 truncation 触发时间
- 将 truncation 策略从 head+tail 改为摘要式截断（对被截断内容生成一句话摘要）
- 增加 truncation 前的告警机制，让 agent 知道上下文即将被截断

**方案 C：增加 truncation 与 compaction 的协调**

修改 Layer 1 的逻辑：当 truncation 被触发时，同时触发一次 compaction，而非仅截断。这样即使不 overflow，也能在 truncation 时将旧对话压缩为摘要，而非直接丢弃。

### 5.2 Skill 层（写作管线）

**方案 D：每章独立会话（最有效）**

从根本上避免单会话上下文累积。每章（或每 2-3 章）启动新会话，通过项目总控文件传递进度和状态。这是当前最有效的修复——不依赖平台改动，立即生效。

**方案 E：精简工具结果**

- skill 文档进一步精简（SKILL.md ≤60 行已在执行）
- 按需加载：只加载当前章节需要的 skill step 文件
- 减少设计包模板的冗余字段

### 5.3 优先级排序

| 方案 | 层级 | 实施难度 | 效果 | 优先级 |
|:-----|:-----|:--------|:-----|:------|
| D. 每章独立会话 | Skill | 低 | 根治 | **P0 · 立即执行** |
| A. 配置主动 compaction | 平台 | 中 | 根治 | **P0 · 需平台支持** |
| C. truncation+compaction 协调 | 平台 | 高 | 根治 | P1 · 需源码修改 |
| B. 调整 truncation 策略 | 平台 | 低 | 缓解 | P1 · 配置调整 |
| E. 精简工具结果 | Skill | 低 | 缓解 | P2 · 持续优化 |

---

## 6. 验收标准

- **AC-1**：单会话连续写作 12 章后，prompt tokens 占比超过 50% 时，events.jsonl 中出现 compaction 执行记录（非 truncation）
- **AC-2**：compaction 后的 session 中，旧对话被替换为 compact summary，而非 `[... truncated]` 标记
- **AC-3**：12 章的设计包字数标准差 < 5,000 字（当前 ch1-ch3 标准差 ~4,200 字，ch4-ch12 标准差 ~800 字，整体标准差 ~8,500 字）
- **AC-4**：12 章的正文字数全部 ≥ 2,000 字（当前 ch6 后全部不达标）
- **AC-5**：ch12 的设计包仍包含完整字段（事件链 + 角色关系动态 + 信息释放清单 + 跨章弧线 + 质量自检），与 ch1 设计包字段覆盖率 ≥ 80%

---

## 附录：完整证据链索引

| 证据 | 数据源 | 路径 | 关键发现 |
|:-----|:------|:-----|:--------|
| 证据一 | runs/events.jsonl | `C:\Users\AWMPRO\.paopao\projects\6-24-项目b\runs\*/events.jsonl` | promptTokens 14.6%→56.6%，从未溢出 900K |
| 证据二 | openclaw 日志 | `C:\Users\AWMPRO\AppData\Local\Temp\openclaw\openclaw-2026-06-24.log` | 0 条 compaction 执行记录 |
| 证据三 | 正文+设计包字数 | `...\paopao-workspace\projects\6-24-项目b\正文\ch*.md` + `章节设计包\ch*设计包.md` | truncation 首次触发 = 设计包断崖时间 |
| 证据四 | conversation 日志 | `C:\Users\AWMPRO\.paopao\projects\6-24-项目b\conversations\61986530*.jsonl` | 25 处截断，3→17 递增 |
| 证据五 | openclaw 日志错误 | 同证据二 | 401 错误 + orphaned subagent 恢复失败 |
| 源码分析 | openclaw dist | `D:\popwave\resources\openclaw\openclaw\dist\embedded-agent-BgvyyCVT.js` | compaction 三层触发条件均为被动 |
| 配置分析 | openclaw.json | `C:\Users\AWMPRO\.openclaw-novel-buddy\openclaw.json` | compaction 完全未配置 |

---

> 文档类型：PRD · 问题报告 + 解决方案
> 创建日期：2026-06-25
> 数据来源：runs/ 目录 41 次 run 的 events.jsonl · conversation 日志 · openclaw 运行日志 · openclaw dist 源码逆向分析
> 关联项目：6-24-项目b（《魔窟攻略组》）
