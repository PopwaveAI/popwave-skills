# Context Overflow 问题分析报告 — 写作管线上下文溢出与历史失效

> 6-12项目a 以来持续出现 `Context overflow: prompt too large for the model` 的系统级排查、验证与根因分析。
>
> 排查范围：paopao 客户端、OpenClaw session / compaction / history 机制、popwave proxy、skill 管线。
>
> 2026-06-14

---

## 一、问题总览

写作管线项目在推进 15-20 轮后出现两个连锁问题：

**问题 1：Context overflow 硬拦截。** 6-12项目a 15 次 run 中 5 次 overflow（33%），其中 3 次返回空响应。6-14-项目a 更严重——24 次 run 中 19 次 overflow（79%），L26-L46 连续 21 轮全被拦截。直接原因是估算 prompt（89-102K tokens）超过模型预算（79,616 tokens）。

**问题 2：overflow 期间 agent 完全失忆。** 每个被拦截的 session 只有 668 字节——agent 看到的不再是对话历史或已产出的文件摘要，而只有一行 `prompt too large`。所有创作进度、已产出文件清单、管线当前阶段对 agent 完全不可见。

**根因是架构级的不对齐**：OpenClaw 的 session 模型把 toolCall payload（文件写入的完整内容）当作对话历史来存储和回灌，而写作管线的 toolCall 本质上是**产出物落盘**而非**需要回忆的对话**。Compaction 可压缩自然语言对话文本，但完全不触碰 toolCall payload 层。System prompt 本身也从第一轮就被截掉了 15%。

---

## 二、时间线

### 2.1 关键事件

```
2026-06-12 10:13    6-12项目a 创建
2026-06-12 10:21    "我要写本小说 网文"              ✅ 正常 (0 turns history)
2026-06-12 10:23    "你好"                          ✅ 正常
2026-06-12 10:27    "灰骑士之主..."                  ✅ 正常
2026-06-12 10:33    "我倾向于 B..."                  ✅ 正常
2026-06-12 10:35    "我觉得还是不行..."                ✅ 正常
2026-06-12 10:36    "可以 继续吧"                     ✅ 正常
2026-06-12 10:39    "主角叫江轩..."                   ❌ 第一次 OVERFLOW (18分钟后)
                    ─────────────────────────────────────
2026-06-13 13:50    "这个效果还可以..."                ✅ 正常
2026-06-13 16:09    "按skill走 下一步..."             ❌ OVERFLOW
2026-06-13 16:15    "继续任务"                        ❌ OVERFLOW
2026-06-13 16:22    "我想写本小说"  ← 新开话题         ✅ 正常
2026-06-13 16:24    "你叫我老板即可..."                ✅ 正常
2026-06-13 16:30    "确认 样品符合预期"               ❌ OVERFLOW
2026-06-13 16:56    "方向对 继续展开"                  ✅ 正常
2026-06-13 17:03    "力量和设定有问题..."              ❌ OVERFLOW
```

### 2.2 关键发现

- 第一次溢出发生在项目创建后 18 分钟，不是 6 月 14 日。
- 前两次溢出（10:39、16:30）**仍然产出了内容**（precheck 仅警告、未硬拦）；后三次（16:09、16:15、17:03）返回空响应。
- 6月13日下午的「中间3轮正常」是因为用户新开话题重置了对话历史。
- Skill 更新发生在 6月13日 22:23—6月14日 01:18，**晚于所有溢出事件**。Skill 更新不是原因。

---

## 三、问题诊断

### 3.1 System Prompt 结构拆解

每次 run 的 system prompt 总量 **38,470 字符（≈ 9,600 tokens）**，由以下组成部分：

| 组件 | 大小 | 占比 | 来源 |
|------|------|:---:|------|
| expert-writer SKILL.md (v3.1.0) | 4,922 chars | 12.8% | `D:\popwave-skills\skills\expert-writer\` |
| Skill registry 条目描述（42 个 skill） | 14,013 chars | 36.4% | OpenClaw skill plugin 层 |
| Tool schema（27 个 tool） | 28,491 chars | 74.1% | OpenClaw tool 框架 |
| 项目 workspace 引导文件（7 个） | 13,844 chars | 36.0% | OpenClaw bootstrap 机制 |
| OpenClaw 框架底文 | 2,600 chars | 6.8% | 客户端注入 |
| **去重后合计** | **38,470 chars** | — | — |

> 注：SKILL.md 已经过 v3.0 精简（从 29.9KB 压缩至 5KB），references/*.md 确认按需加载、未注入 system prompt。当前瓶颈不在 expert-writer 自身。

### 3.2 Workspace 引导文件详情

7 个文件由 OpenClaw 的 bootstrap 机制在每次 session 启动时自动注入。模板源位于 `D:\popwave\resources\openclaw\openclaw\docs\reference\templates\`：

| 文件 | 大小 | 内容 | 与写作相关 |
|------|------|------|:---:|
| AGENTS.md | 7,877 chars | 通用 Agent 指南：内存管理、群聊礼仪、Discord/WhatsApp 格式 | 无 |
| SOUL.md | 1,797 chars | Agent 人格：要有观点、记住你是客人 | 无 |
| BOOTSTRAP.md | 1,510 chars | 首次启动引导：起名字、选 emoji（用后应删除） | 无 |
| TOOLS.md | 910 chars | 摄像头名称、SSH 别名、TTS 音色配置 | 无 |
| IDENTITY.md | 693 chars | Agent 身份卡：名字/物种/emoji | 无 |
| USER.md | 534 chars | 用户画像：姓名/称呼/时区 | 低 |
| HEARTBEAT.md | 225 chars | 心跳任务清单 | 无 |
| **合计** | **13,844 chars** | | |

**结论**：13,844 字符与写作管线完全无关，属于 OpenClaw 通用 workspace 初始化模板被不分场景地注入。

### 3.3 会话历史膨胀分析

对 `paopao-conv-075f388e-*.jsonl`（90 条消息，533KB）逐条分析：

```
注入的 10 轮历史中的助理产出（按大小排序）：

L55: 29,042 chars   世界蓝图 #01（完整 6 篇 L1 设定）
L73: 29,072 chars   世界蓝图 #01 Phase 1.2 深度展开（全文重发）
L79: 12,184 chars   势力格局 #05（全文）
L82:  7,231 chars   交叉引用记录（全文）
L86:  4,618 chars   世界稳定性检验报告（全文）
L62:  3,729 chars   世界蓝图 #01（压缩版，仍包含大量原文）
L66:  3,411 chars   世界蓝图 #01（又注入一次）
L84:  1,155 chars   交叉引用（再次注入）
L88:  1,759 chars   稳定性报告（再次注入）
```

**问题本质**：同一批 L1 设定（世界蓝图、势力格局、交叉引用、稳定性报告）在历史中被注入 **3-5 遍**。每轮助理回复都把完整产出塞回上下文，导致相同内容反复占位。

### 3.4 COMPACTION 压缩机制失效

session 中存在 4 个 compaction 事件，但全部内容为空摘要：

```
L33: 5,267 chars  摘要="No prior history. None. ..."
L42: 5,267 chars  摘要="No prior history. None. ..."
L64: 10,057 chars 摘要="No prior history. None. ..." + Turn Context
L90: 16,788 chars 摘要="No prior history. None. ..." + Turn Context
```

4 个 compaction 总计 **37,379 字符**，没有压缩任何历史内容，反而自身占用了 10% 的 prompt 预算。

### 3.5 模型上下文元数据

OpenClaw 的 context-overflow-precheck 日志：

```
provider: popwave/writing-standard
contextTokens: 96000
reserveTokens: 16384
promptBudgetBeforeReserve: 79616
estimatedPromptTokens: 89913
overflowTokens: 10297
route: compact_only
messages: 37
```

- `contextTokens=96000` 由 popwave proxy 返回（模型元数据）。
- 扣除 16,384 预留后，实际 prompt 预算 79,616 tokens。
- 估算 prompt 89,913 tokens → 超出 10,297 tokens（+12.9%）。

### 3.6 Precheck 激活时间窗口

遍历全部 70 个 trajectory 文件，仅 3 个包含 context-overflow-precheck 日志：

| Session | Provider | Model | 创建时间 | precheck |
|---------|----------|-------|---------|:---:|
| `3b4153e4`（未命名项目） | deepseek | deepseek-v4-flash | 6/10 14:33 | 无 |
| `6f041a19`（未命名项目） | deepseek | deepseek-v4-flash | 6/11 06:37 | 无 |
| `41e60aff`（未命名项目） | popwave | writing-standard | 6/12 10:10 | 无 |
| `01560ab8` run（未命名，14 turns） | popwave | writing-standard | 6/12 10:09 | 无 |
| ────────────── | **边界线** | ────────────── | | |
| `cd7ff0f6` | popwave | writing-standard | 6/12 10:22 | ✅ 首次触发 |
| `075f388e`（6-12项目a） | popwave | writing-standard | 6/12 10:23 | ✅ 触发 |
| `6f041a19`（后续 run） | deepseek | deepseek-v4-flash | 6/12 后续 | ✅ 触发 |

时间边界线精确落在 **6月12日 10:10—10:22** 之间。

### 3.7 未命名项目同样存在回灌，但没有 precheck 拦截

旧项目的 session `3b4153e4` 工具使用情况：

| 工具 | 调用次数 | 最大单次 payload |
|------|:---:|------|
| exec | 29 | 5,056 字符 |
| write | **17** | **20,119 字符** |

旧项目同样在设定阶段大量写入文件——工具模式和 payload 体量与新项目完全一致。Assistant 产出的回灌**不是新项目独有的问题**，历史上一共存在。

但旧项目的 run 中没有任何一个包含 `context-overflow-precheck` 或 `contextTokens` 字样。翻遍 53 个 run 的 events 为零命中。

### 3.8 对比：未命名项目为何正常

| 指标 | 未命名项目 | 6-12项目a |
|------|----------|----------|
| 模型 | popwave/writing-standard（同） | popwave/writing-standard（同） |
| 历史深度 | 14 turns | 10 turns |
| 项目文件 | 含 6MB 小说全文 | 含 6 篇 L1 设定 |
| 历史内容 | 正常对话（回复多 ≤ 8KB） | 每轮回复 30KB+ 长文设定稿 |
| Assistant write 调用 | 17 次，最大 20KB | 5 次，每次 4-5KB |
| context-overflow-precheck | **从未触发** | 每次 session 都触发 |
| 时间 | 6/10—6/12 10:09 | 6/12 10:22 之后 |
| 结果 | 正常 | 3/15 次硬拦截 |

新项目的回灌问题（assistant 产出反复注入）旧项目也有，但当时没有被 precheck 拦截。根本差异不在行为模式，在**拦截机制是否激活**。

---

## 四、触发机制

### 4.1 直接原因

单次 prompt 估算 **89,913 tokens**，超过模型预算 **79,616 tokens**（96K 窗口 − 16K 预留）。

### 4.2 precheck 激活前的状态

| 因子 | 消耗 | 可控性 |
|------|------|:---:|
| **System prompt 底文** | ~9,600 tokens | 可优化 |
| └ Workspace 引导文件（与写作无关） | ~3,500 tokens | 可直接删除 |
| └ Skill registry + Tool schema（框架层） | ~5,500 tokens | 需框架改动 |
| **对话历史** | ~77,000 tokens | 可优化 |
| └ Assistant 产出反复回灌 | ~50,000 tokens（重复 3-5 遍） | Skill 输出策略可改 |
| └ COMPACTION 压缩失效 | ~4,000 tokens（空摘要） | 需框架修复 |
| **context-overflow-precheck** | — | 拦截行为 |

### 4.3 触发开关：popwave proxy 新增 contextTokens 字段

##### 触发链路

```
变更前（6/12 10:09 之前）：
  popwave proxy → 不返回 contextTokens 字段
  → OpenClaw 不启动 precheck
  → prompt 即使估算超 96K，也直接发送
  → 模型实际 128K 窗口硬兜 → 用户无感知

变更后（6/12 10:22 之后）：
  popwave proxy → 返回 contextTokens: 96000
  → OpenClaw 启动 context-overflow-precheck
  → 测得 89,913 tokens > 79,616 预算
  → 硬拦截 → 用户看到 overflow
```

证据：

- 70 个 trajectory 文件中，仅 3 个包含 precheck 日志——全部创建于 6/12 10:22 之后。
- 旧项目 session `3b4153e4` 有 17 次 write 调用 + 最大 20KB payload——与新项目完全相同的工具模式，但因运行在 6/10-6/11，proxy 未返回 contextTokens，precheck 从未启动。
- 绑定 deepseek provider 的 session `6f041a19` 在 6/12 后续也被激活了 precheck（deepseek 被统一为 popwave proxy 路由后同样受到影响）。

##### 放大因子（导致实际超出的叠加原因）

即使没有 precheck 拦截，写作管线的 prompt 也确实在逼近甚至超过 96K。以下是导致 prompt 膨胀的三个放大因子：

1. **助理长文产出被完整回灌进历史**——书设阶段的助理回复（29KB 设定稿）每次都被原样注入下一轮上下文，同一批 L1 设定重复出现 3-5 次，累计浪费约 50,000 tokens。OpenClaw session 将 toolCall 的完整 payload（包括写入文件的全部内容）视为对话历史的一部分。

2. **COMPACTION 压缩机制空转**——4 个 compaction 事件占 37KB 但摘要全部为空（`No prior history. None.`），历史内容未被压缩，空占预算。

3. **Workspace 引导文件与写作场景无关**——13,844 字符的 Agent 通用人格/工具/心跳指南对 novel-buddy 完全无用，被不分场景地注入。

---

## 五、根因：架构级的不对齐

### 5.1 两个互不理解的系统叠在一起

问题的本质不是"压缩没做好"，而是 OpenClaw 和写作管线对 toolCall 的理解完全不同：

```
OpenClaw 的模型：
  session = 对话历史
  toolCall = 对话的一部分（"agent 做了这个操作"）
  → 完整存储，完整回灌
  → 压缩 = 压缩对话文本

写作管线的现实：
  session = 创作进程
  toolCall write = 产出物落盘（"产出物写到磁盘"）
  → 文件内容不应该回灌进 prompt
  → agent 需要时通过 Read 重新加载——这才是正确的上下文路径
```

OpenClaw 不知道它在跑写作管线。它只知道有个 agent 在频繁调用 `write` 工具，把大量文本写入磁盘——这在它的模型里是正常的（coding agent 也会写文件）。但它不知道这 30KB 的写入内容是**创作产出**，不是**需要记忆的上下文**。

一个典型写作 session 的 token 分布：

```
system prompt           9,600 tokens  ████████
workspace bootstrap     3,500 tokens  ███
user messages           1,200 tokens  █
assistant text            800 tokens  █
─────────────────────────────────────
以上合计 ~15,000 tokens ← compaction 的作用域

toolCall payload       75,000 tokens  ██████████████████████████████████████████████████████████████
                     ← compaction 完全不碰这部分
```

**Compaction 压缩的是那 800 字的 assistant text，放过的是 75K token 的 toolCall payload。**

### 5.2 三层截断的叠加效应

溢出不只是一次性拦截——它在不同层面同时造成上下文丢失。

#### 第一层：`limitChars` — system prompt 被硬截掉了 15%

```
originalChars=38470  →  limitChars=32768
```

每次 session 启动，system prompt 最后 5,702 字符被丢弃。虽然被丢弃的主要是 skill registry 尾段（lark-* 等），但这说明 capacity 从一开始就不够。

#### 第二层：Compaction — 只记意图，不记产出

对 6-14-项目a 的 54 个 compaction 事件全量审计：

| compaction 数量 | 摘要模板 |
|:---:|------|
| 54 个全部 | `## Goal 用户要写一本跨界融合小说：博德之门3骨灰玩家穿越到DND世界…` |

**54 个 compaction，全部只记用户最初的需求声明。** 它完全不记录：

- "L1 六件套已写入哪些文件，每个文件的核心设定是什么"
- "卷1设计了 3 幕 13 章，Canvas 矩阵已填充"
- "ch001 设计包 18 事件已产出"

模型在后续轮次对"我们当前处在哪个阶段、哪些文件已产出、每个文件的大致内容"毫无认知——这些信息全在 toolCall payload 里，而 compaction 不碰。

#### 第三层：Overflow 后直接拒绝，agent 完全失忆

```
L26 开始: context.compiled size=668   ← 只有 precheck error block
L27-L199: 全部 size=668               ← 15+ 次 session 全被拦截
```

溢出不等于"截掉尾部内容后发送"——等于**完全不发送**。每个被拦截的 session agent 看到的是：

```
Context overflow: prompt too large for the model.
Try /reset (or /new) to start a fresh session.
```

所有之前的对话历史、创作进度、已产出文件的元信息，**全部不可见**。这就是为什么 6-14-项目a L26-L46 连续 21 轮全是 127 字的 overflow 报错——agent 已经被剥夺了全部记忆。

### 5.3 toolCall payload 的链式累积

Session 中 toolCall payload 的逐级累积：

```
Phase           每轮 toolCall payload  →   累积
─────────────────────────────────────────────
creative        ~5KB × 3 轮           →  15KB
world           ~16KB × 3 轮          →  63KB
plot            ~12KB × 4 轮          →  111KB
chapter-design  ~8KB × 5 轮           →  151KB
deconstructor   ~29KB × N 轮          →  ＞325KB  ← 此时溢出
```

6-14-项目a trajectory 中的 tokensBefore 指标证实了这一点——从初始的 58K 上涨到 97K，每过一个子 skill 就增加 ~10-15K tokens。

### 5.4 总结

| 层面 | 问题 | agent 感知 |
|------|------|-----------|
| System prompt | limitChars=32768，截掉 15% | 丢失 ~6K chars 的 skill/tool 描述 |
| Compaction | 只压缩自然语言对话，不碰 toolCall payload | 记住了"用户要写跨界小说"，不知道"L1 六件套 / 3卷13章" |
| toolCall payload | write 工具的完整文件内容被视为对话历史 | 每轮 5-30KB 历史累积，75K tokens 的产出废物 |
| Overflow | 不是截断，是完全拒绝 | agent 看到 668 字节 + "prompt too large"，以前所有创作进度归零 |

**正确的修法不是让 compaction 更聪明，而是让 toolCall write 的 payload 从历史中移除**——文件内容不应被回灌进 prompt，因为它们是磁盘上的产出物，agent 需要时通过文件读取获取。这要求区分两种 toolCall 的历史注入策略：

| 类型 | 示例 | 历史注入策略 |
|------|------|------------|
| **读操作** | `Read file X`, `Get-Content Y` | 存完整结果 |
| **写操作** | `write file X with content` | 存元数据（path + size），不存 content |

---

## 六、优化方案

### 6.1 最高优先级：修复触发根因

#### D. popwave proxy 模型上下文窗口配置

**这是本次问题的直接开关。** 将 `writing-standard` 的 context window 配置为实际值（128K），或移除 `contextTokens` 元数据返回，即可关闭 precheck 硬拦截。

具体而言，6月12日 10:10—10:22 之间的 proxy 变更新增了 `contextTokens: 96000` 的返回。如果 `writing-standard`（即 deepseek-v4-flash）的实际上下文窗口为 128K，则 proxy 返回的值是错误的保守值。修正为 128000 即可。

> **节省**：无需客户端改动，一次配置变更消除所有拦截。此前 prompt 超 96K 从未被拦截，模型实际 128K 能兜住。
>
> **依赖**：后端确认模型实际 context window 并调整 proxy 配置。
>
> **执行周期**：即时。

### 6.2 高优先级：削减 prompt 体量（治本）

即使 precheck 关闭，写作管线 prompt 也确实在爬升。以下方案削减消耗，让管线在更小的窗口下也能安全运行。

#### A. 清理 Workspace 引导文件

删除或清空 `C:\Users\AWMPRO\.openclaw-novel-buddy\workspace\` 下与写作无关的 6 个文件（AGENTS.md / SOUL.md / BOOTSTRAP.md / TOOLS.md / IDENTITY.md / HEARTBEAT.md），仅保留 USER.md。

> **节省**：~3,300 tokens（13,844 → 534 chars）。
>
> **风险**：零。这些文件是 OpenClaw 初始化模板，novel-buddy 场景下不依赖任何一条规则。

#### B. 助理产出避免全量回灌

在 expert-writer 和子 skill 中增加一条纪律：**关键产出物写入文件后，对话中仅保留摘要（≤ 500 字），不将完整产出文本留在 assistant 消息中**。

> **节省**：~40,000 tokens（设定阶段每轮从 30KB 降至 1KB 摘要）。
>
> **影响**：需要 skill 文档层面配合，agent 需在产出完成后做「写入文件 → 对话摘要」的动作。

### 6.3 中优先级（需框架配合）

#### C. 修复 COMPACTION 压缩

COMPACTION 事件应真正压缩历史内容，而非输出 `No prior history. None.` 的空摘要。当前 37KB 的压缩开销完全浪费。

> **节省**：~4,000 tokens + 历史压缩带来的可持续轮次。
>
> **依赖**：OpenClaw 框架层 compaction 逻辑修复。

#### E. Skill registry + Tool schema 按场景裁剪

当前 42 个 skill 和 27 个 tool 全量注入，其中 lark-*、weather、cron、browser 等与写作无关。按 agent profile（novel-buddy）过滤，仅暴露写作相关条目。

> **节省**：~2,000 tokens（skill registry）+ ~3,000 tokens（tool schema）。
>
> **依赖**：OpenClaw / paopao 框架层支持 profile-based filtering。

### 6.4 汇总

| 方案 | 层面 | 可节省 | 难度 | 执行周期 |
|------|------|--------|:---:|---------|
| D. Proxy context window | 后端 | 消除拦截 | 低 | 即时 |
| A. 清理 Workspace 文件 | 客户端 | ~3,300 tokens | 极低 | 立即 |
| B. 产出摘要化 | skill | ~40,000 tokens | 中 | 1-2 天 |
| C. COMPACTION 修复 | 框架 | ~4,000 tokens | 中 | 需评估 |
| E. Registry/Schema 裁剪 | 框架 | ~5,000 tokens | 高 | 需规划 |
| **合计** | | **~52,000 tokens** | | |

优化后 system prompt + 历史总 token 预估从 90K 降至 **38K**，在 96K（甚至 64K）窗口下有充分安全边际。

---

## 七、证据索引

| 证据项 | 路径 | 内容 |
|--------|------|------|
| 会话日志 | `C:\Users\AWMPRO\.paopao\projects\6-12项目a\conversations\075f388e-*.jsonl` | 12 轮对话，759KB |
| OpenClaw session | `C:\Users\AWMPRO\.openclaw-novel-buddy\agents\main\sessions\paopao-conv-075f388e-*.jsonl` | 90 条消息，533KB |
| Run 历史 | `C:\Users\AWMPRO\.paopao\projects\6-12项目a\runs\` | 15 次 run，5 次 overflow 标记 |
| 溢出 run input | `runs\69a61e15-*\input.json` | injectedHistoryTurns=10, skillNames=expert-writer |
| Trajectory | `paopao-conv-075f388e-*.trajectory.jsonl` | context.compiled + context-overflow-precheck 日志 |
| Skill 文件 | `D:\popwave-skills\skills\expert-writer\SKILL.md` | v3.1.0，4,922 chars |
| 对比项目 | `C:\Users\AWMPRO\.paopao\projects\未命名项目\` | 53 runs，无 overflow 记录 |
| Workspace 模板源 | `D:\popwave\resources\openclaw\openclaw\docs\reference\templates\` | 7 个模板文件 |
| Provider 配置 | openclaw.json | gateway token + skill entries |
| 全量 trajectory 审计 | `*.trajectory.jsonl`（70 个文件） | 仅 3 个含 precheck 日志，全部创建于 6/12 10:22 后 |
| 旧 session 工具追踪 | `paopao-conv-3b4153e4-*.jsonl` | 17 次 write，最大 20KB——同模式无 precheck |
| Precheck 时间边界 | 6/12 10:09（无）→ 10:22（触发） | popwave proxy 新增 contextTokens 的时间窗口 |
| 6-14-项目a paopao conv | `6-14-项目a\conversations\dddb03c5-*.jsonl` | 46 轮，12940KB |
| 6-14-项目a OpenClaw session | `paopao-conv-dddb03c5-*.jsonl` | 1467 行，~70MB |
| 6-14-项目a trajectory | `paopao-conv-dddb03c5-*.trajectory.jsonl` | 2787KB，model=writing-standard，projectContextChars=13844 |
| 6-14-项目b paopao conv | `6-14-项目b\conversations\1db39603-*.jsonl` | 6 轮 |
| 6-14-项目b trajectory | `paopao-conv-1db39603-*.trajectory.jsonl` | 1623KB，projectContextChars=13844，无 precheck |

---

## 八、方案执行与验证（2026-06-14）

### 8.1 已执行方案

#### B. 产出摘要化 — 18 个 skill 文件全覆盖

在 expert-writer 红线 + 17 个子 skill 的质量红线/产出纪律中，新增统一规则：

> 写入文件后对话中只留摘要（≤ 200 字），不粘贴完整产出。正确格式："已写入 {路径}。摘要：{核心}。需展开告诉我。"

| Skill | 规则位置 | 状态 |
|-------|---------|:---:|
| expert-writer | 红线 ❌7 | ✅ |
| pop-novel-creative | 质量红线 ❌9 | ✅ |
| pop-novel-world | 产出纪律（新章节） | ✅ |
| pop-novel-continue | 产出纪律（新章节） | ✅ |
| pop-novel-deconstructor | 质量红线 ❌10 | ✅ |
| pop-novel-plot | 质量红线 checklist | ✅ |
| pop-novel-chapter-design | 质量红线 checklist | ✅ |
| pop-novel-prose-render | 质量红线表格行 | ✅ |
| pop-novel-qa | 产出纪律（新章节） | ✅ |
| pop-dna | 质量红线 checklist | ✅ |
| pop-novel-character-schema | 质量红线 ❌5 | ✅ |
| pop-novel-html-renderer | 质量红线 ❌5 | ✅ |
| pop-novel-game | 质量红线 ❌6 | ✅ |
| pop-shared-reader | 质量红线 ❌7 | ✅ |
| pop-shared-html | 质量红线 checklist | ✅ |
| tool-cnovel-research | 产出纪律（新章节） | ✅ |
| tool-opinion-tracker | 产出纪律（新章节） | ✅ |
| download-webnovel-txt | 质量红线（新章节） | ✅ |

#### A. 清理 Workspace 引导文件 — 已执行但无效

磁盘文件已清为 0 字节，但 trajectory 显示 `projectContextChars=13844` 在所有后续项目中未变化。根因：OpenClaw 从内部模板目录（`D:\popwave\resources\openclaw\openclaw\docs\reference\templates\`）注入，不经过磁盘 workspace 文件。磁盘文件是 **输出** 而非输入。

**结论**：方案 A 在当前 OpenClaw 实现下无效。需要框架层配置或 agent profile 开关。

### 8.2 6-14-项目a 验证结果

项目创建于改动后 2 分钟（UTC 2026-06-13 18:23），完成完整写作管线 creative→world→plot→chapter-design。

#### Paopao 对话层 — 产出纪律完全生效

| 轮次 | 阶段 | 体量 | 格式 |
|:--:|------|------|------|
| L4 | creative 方向碰撞 | 1,636 字 | 方向草图 |
| L6 | creative 进度一览 | 421 字 | 表格 |
| L8 | world L1 成果看板 | 693 字 | 表格 |
| L10 | world 完整进度 | 726 字 | 表格 |
| L12 | plot 全书架构摘要 | 374 字 | 摘要 |
| L14 | plot 卷设计摘要 | 645 字 | 摘要 |
| L18 | plot 幕纲 Canvas | 777 字 | 摘要 |
| L20 | plot 三幕落盘 | 869 字 | 摘要 |
| L22 | chapter-design 设计包 | 516 字 | 摘要 |
| L24 | chapter-design 全章骨架 | 702 字 | 摘要 |

全程无一轮超过 2KB。对比 6-12 项目 world 阶段 29KB 完整设定贴入，改善 ~97%。**产出纪律验证通过。**

#### 但 L26 开始仍 OVERFLOW — 连续 21 轮拦截

```
L26-L46: Context overflow: prompt too large for the model. × 21
```

| overflow run | estimatedPromptTokens | overflowTokens | 超幅 |
|:---|------|------|:---:|
| 2866d802 | 79,998 | 382 | +0.5% |
| 1c7c7e05 | 89,952 | 10,336 | +13.0% |
| cb462fb2 | 102,525 | 22,909 | +28.8% |
| 49bc6429 | 96,634 | 17,018 | +21.4% |

溢出发生在 plot→chapter-design 阶段，且溢出量持续上升。

### 8.3 未被解决的真正瓶颈：toolCall payload 回灌

产出纪律管的是 **assistant text 输出**，管不了 **write 工具调用的 payload**。

每次 `write` 工具调用，文件内容必须作为参数传给工具。OpenClaw session 将完整的 toolCall（含 `input.content`）存入会话历史。下一轮 run 时，整个 toolCall payload 原样注入 prompt。

Session 每轮累积：

```
Phase           每轮 toolCall payload
────────────────────────────────────
creative        ~5KB × 3 轮     →  15KB
world           ~16KB × 3 轮    →  63KB
plot            ~12KB × 4 轮    →  111KB
chapter-design  ~8KB × 5 轮     →  151KB
deconstructor   ~29KB × N 轮    →  ＞325KB  ← 此时溢出
```

这是逐级累加的链式膨胀，与 assistant text 输出是否摘要化无关。

### 8.4 方案有效性矩阵

| 方案 | 状态 | 实际效果 |
|------|:---:|------|
| A. 清理 Workspace 文件 | ❌ 无效 | OpenClaw 从内部模板注入，不读磁盘文件 |
| B. 产出摘要化 | ✅ 生效 | assistant text 从 29KB → 700 字（-97%）|
| C. COMPACTION 修复 | ⚠️ 外部改善 | 6-14 项目有实际摘要（非空），但与 skill 改动无关 |
| D. Proxy context window 128K | ⏸️ 未执行 | 即使执行，只会延缓不会根治 |
| E. Registry/Schema 裁剪 | ⏸️ 未执行 | 框架层改动 |

### 8.5 下一步：必须的框架层改动

**方案 F：OpenClaw session history 中 toolCall payload 截断**

当前 toolCall 在历史注入时的行为：完整存储 write 工具的 input（含文件内容），导致每轮 5-30KB 累积。

改造后行为：`write` 类型的 toolCall 在注入历史时，不存 `input.content`，仅存元数据：

```json
{
  "name": "write",
  "input": {
    "file_path": "00-原始设定/L1-元设定层/01-世界蓝图.md",
    "content_size": 5234,
    "summary": "含地理/位面/时间/法则四个字段"
  }
}
```

改造位置：OpenClaw session history builder 层。每轮 5-30KB → ~100 字节。

> **节省**：~150,000 tokens（完整管线全程累积）。
>
> **依赖**：OpenClaw 框架层改动。
>
> **副作用**：模型在后续轮次看不到完整文件内容，需要 agent 通过 `Read` 工具重新加载。这是可接受的——assistant text 摘要已经指引了文件路径。

**方案 G：管线分段 /reset**

在 framework 改动到位前，将完整管线拆分为 2-3 个 session：

```
session 1: creative + world      → /reset
session 2: plot + chapter-design → /reset
session 3: prose-render + qa
```

每次 /reset 清空前序 toolCall 历史，让每个 session 的 prompt 保持在安全区间。
