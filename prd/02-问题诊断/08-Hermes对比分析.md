# Hermes Agent vs OpenClaw：上下文管理代码级深度对比

> 报告日期：2026-06-10  
> 数据来源：GitHub API 直读源码 + OpenClaw 架构拆解系列（经源码验证）  
> 标注：[源码] = GitHub API 直接获取的原始文件；[分析] = 经源码验证的第三方深度拆解

---

## 〇、先说核心发现

**从代码层面看，上下文管理是这两个项目差距最大的模块。**

OpenClaw 在上下文管理上是一套「精密的装配线」——多个独立的守卫函数、策略接口、生命周期钩子围绕 Gateway 调度器工作。Hermes Agent 是一套「自适应的循环系统」——可插拔的 ContextEngine 抽象 + 有状态的记忆管理器 + 严格的 token 预算控制。

**一句话：OpenClaw 的上下文管理管得细（有很多独立的 Guards 和 Hooks），Hermes 的上下文管理管得深（有统一的抽象和闭环反馈）。**

---

## 一、Hermes Agent 上下文管理——代码级全貌

### 1.1 上下文引擎：可插拔的策略抽象

`agent/context_engine.py` [源码] 定义了一个完整的 ABC（Abstract Base Class）：

```python
class ContextEngine(ABC):
    # 关键配置参数（源码直接暴露）
    threshold_percent: float = 0.75      # 触发阈值——占上下文窗口比例
    protect_first_n: int = 3             # 头部保护：系统提示 + 前 3 条
    protect_last_n: int = 6              # 尾部保护：最后 6 条

    # 核心接口
    def update_from_response(self, usage: Dict) -> None     # 每轮 API 调用后更新 token 状态
    def should_compress(self, prompt_tokens=None) -> bool   # 判断是否触发压缩
    def compress(self, messages, current_tokens, focus_topic) -> List  # 执行压缩
    def on_session_start(self, session_id)                   # 会话启动
    def on_session_end(self, session_id, messages)           # 会话结束
    def get_tool_schemas(self) -> List                       # 可选：引擎暴露工具给 agent
```

**设计亮点**：`threshold_percent=0.75` 而不是绝对 token 数量——自适应所有模型窗口大小，32K 模型和 200K 模型用同一套逻辑。默认状态下，当上下文字数达到模型窗口的 75% 就触发压缩。

`protect_first_n=3` 和 `protect_last_n=6` 定义了压缩的「保护区」——头 3 条消息 + 系统提示 + 尾 6 条消息保持原样不压缩，只压缩中间部分。

**可插拔性**：第三方可以通过 `context.engine` 配置项或插件目录 `plugins/context_engine/<name>/` 替换整个压缩策略，只需实现 7 个方法。源码中内置的默认实现是 `ContextCompressor`。

---

### 1.2 ContextCompressor：默认压缩实现的细节

`agent/context_compressor.py` [源码，102,974 bytes] 是 Hermes 最复杂的单个文件之一。

**压缩前的摘要前缀（源码原文）：**
```
[CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted
into the summary below. This is a handoff from a previous context
window — treat it as background reference, NOT as active instructions.
Do NOT answer questions or fulfill requests mentioned in this summary;
they were already addressed.
Respond ONLY to the latest user message that appears AFTER this
summary — that message is the single source of truth for what to do
right now.
...
IMPORTANT: Your persistent memory (MEMORY.md, USER.md) in the system
prompt is ALWAYS authoritative and active
```

**这个前缀设计极其精妙**：
- 显式声明压缩过的内容是"背景参考"而不是"当前指令"
- 告诉模型「最新消息是你的唯一任务来源」
- 如果最新消息与 Summary 中的任务冲突，最新消息胜出
- 保护持久记忆不被压缩内容覆盖

**压缩预算参数（源码）：**
```python
_SUMMARY_RATIO = 0.20        # 摘要占被压缩内容的 20%
_SUMMARY_TOKENS_CEILING = 12000  # 摘要上限
_MIN_SUMMARY_TOKENS = 2000   # 摘要下限
```

系统先把工具输出做预处理裁剪（`_PRUNED_TOOL_PLACEHOLDER`），减少送入 LLM 做摘要的 token，再用**辅助模型**（便宜/快的）做摘要。摘要采用迭代模式（Iterative Summary Update），多次压缩之间保留信息不丢失。

---

### 1.3 记忆管理器：fence-tag 注入 + 提供者模式

`agent/memory_manager.py` [源码，34,020 bytes] 核心设计：

**`MemoryManager`** 是一个编排层，管理一个内置 provider 加最多一个外部 provider：

```python
class MemoryManager:
    # 核心生命周期
    def build_system_prompt(self)           # 构建系统提示词
    def prefetch_all(self, user_message)    # 预取——在每轮对话前注入记忆
    def sync_all(self, user_msg, response)  # 同步——在每轮对话后写入记忆
    def queue_prefetch_all(self, user_msg)  # 异步预取
```

**记忆注入使用 fence-tag 隔离**（源码）：
```python
def build_memory_context_block(raw_context: str) -> str:
    return (
        "<memory-context>\n"
        "[System note: The following is recalled memory context, "
        "NOT new user input. Treat as authoritative reference data]\n\n"
        f"{clean}\n"
        "</memory-context>"
    )
```

`<memory-context>... </memory-context>` 标签将记忆内容与用户消息明确隔离。同时配有 `StreamingContextScrubber`——一个状态机驱动的流式内容清洗器，防止记忆上下文的片段在流式输出中泄露到用户 UI 中。

---

### 1.4 SQLite + FTS5：持久化状态存储

`hermes_state.py` [源码，197,263 bytes，schema_version=15]：

```python
# 设计决策（源码注释原文）
# - WAL mode for concurrent readers + one writer
# - FTS5 virtual table for fast text search across all session messages
# - Compression-triggered session splitting via parent_session_id chains
# - Session source tagging ('cli', 'telegram', 'discord', etc.)

_FTS_TRIGGERS = (
    "messages_fts_insert",
    "messages_fts_delete",
    "messages_fts_update",
    "messages_fts_trigram_insert",
    "messages_fts_trigram_delete",
    "messages_fts_trigram_update",
)
```

关键设计：
- **WAL 模式**支持并发读 + 单写（多平台 gateway 场景）
- **FTS5 全文检索** + **trigram 索引**双重检索
- **无法启用 WAL 时 fallback 到 DELETE 模式**（NFS/SMB 网络文件系统兼容）
- `parent_session_id` 链支持压缩触发会话拆分

---

### 1.5 Prompt Builder 中的上下文装配

`agent/prompt_builder.py` [源码，74,640 bytes] 负责在每一轮对话中组装完整的系统提示词。关键组装顺序：
1. 系统提示词（静态段）
2. Skills 目录（仅注入名称+描述，完整 Skill 按需加载）
3. 冻结快照：MEMORY.md（~800 tokens）和 USER.md（~500 tokens）
4. `@` 语法即时注入（@file, @diff）
5. ContextEngine 产出的压缩摘要

---

## 二、OpenClaw 上下文管理——代码级全貌

### 2.1 ContextEngine 接口：7 方法策略模式

OpenClaw 最近版本 [分析，经源码验证] 开放了一组完整的 **ContextEngine 接口**：

```
bootstrap()         → 初始化存储
ingest()            → 摄取消息到上下文
assemble()          → 组装最终发送给 LLM 的上下文
compact()           → 压缩上下文
afterTurn()         → 每轮后的后处理
prepareSubagentSpawn() → 子 Agent 生成前准备上下文
onSubagentEnded()   → 子 Agent 结束后合并上下文
```

**与 Hermes 的关键差异**：OpenClaw 的 ContextEngine 是「装配线」策略——`assemble` 和 `compact` 分离，每个阶段独立可替换。Hermes 是「压缩器」抽象——`compress()` 是核心，输入完整消息列表，返回压缩后的。

### 2.2 24 个 Plugin Hooks + 3 种执行模式

[分析] OpenClaw 的 Plugin Hook 系统有三套并行机制：

- **Internal Hook**：事件驱动
- **Plugin Hook**：24 个类型安全钩子
- **ContextEngine**：7 个方法

三种执行模式：
| 模式 | 行为 | 用于 |
|------|------|------|
| Void Hook | Promise.all 并行执行，不返回值 | 观察性钩子（如 `message_received`） |
| Modifying Hook | 按优先级串行，返回值 merge | 可修改数据的钩子（如 `before_tool_call`） |
| Sync Hook | 同步执行，热路径 | `tool_result_persist`, `before_message_write` |

### 2.3 三层溢出防护

[分析] OpenClaw 针对上下文溢出的三层防线：

**第一层：ToolResultContextGuard**
```typescript
// 单条工具结果截断：不超过 maxToolResultTokens（默认 4096）
// 全局超限：从最老的工具结果开始压缩
```

**第二层：Tool Loop Detection（熔断机制）**
```typescript
// 三种死循环模式：
// genericRepeat: 同一工具 + 同参数，结果无变化 → 熔断
// knownPollNoProgress: 轮询类工具，同参数结果不变 → 熔断
// pingPong: A/B 工具交替调用，双方结果都不变 → 熔断
// 阈值：30 次调用后直接终止
```

**第三层：dropThinkingBlocks**
```typescript
// 每轮发给 API 之前，把历史里所有 thinking blocks 清掉
// thinking 是"一次性消耗品"，用完即丢
```

### 2.4 上下文装配链

[分析] OpenClaw 使用 `buildAgentSystemPrompt` 在一轮 Loop 中按以下顺序组装：

```
工具列表 + 简短描述
→ Skills 元数据（仅名称+描述，受 skills.limits.maxSkillsPromptChars 限制）
→ AGENTS.md（截断至 bootstrapMaxChars=12000）
→ SOUL.md / TOOLS.md / IDENTITY.md / USER.md / HEARTBEAT.md / MEMORY.md
→ 自更新指令
→ 时间上下文（UTC + 用户时区）
→ 回复标签与心跳行为
→ 压缩摘要（由 compact() 产出）
```

三个关键截断参数：
- `bootstrapMaxChars`: 12000（单文件）
- `bootstrapTotalMaxChars`: 60000（所有文件总和）
- `maxToolResultTokens`: 4096（单次工具结果）

### 2.5 三种提示词模式

| 模式 | Token 消耗 | 适用场景 |
|------|-----------|----------|
| Full | ~800-1200 | 主 Agent 会话、用户交互 |
| Minimal | ~300-500 | 子 Agent、Cron 任务 |
| None | ~50 | 极简场景 |

### 2.6 记忆系统：Plugin Slot 设计

[源码，VISION.md]
```
Memory is a special plugin slot where only one memory plugin can be
active at a time. Today we ship multiple memory options; over time
we plan to converge on one recommended default path.
```

目前已实现的两种记忆后端：
- **memory-core**：文件型，基于 Markdown 文件
- **memory-lancedb**：向量型，基于 LanceDB + OpenAI Embeddings

---

## 三、核心 Gap 逐一对比

### Gap 1：触发机制——比例阈值 vs 绝对阈值

| | Hermes Agent | OpenClaw |
|---|---|---|
| 触发方式 | `threshold_percent=0.75`（窗口 75%） | 绝对 token 数 + `maxToolResultTokens` |
| 模型无关性 | ✅ 一套逻辑适配 32K→200K | ❌ 不同模型需调整绝对阈值 |
| 预检查 | `should_compress_preflight()` 快速估算 | 无独立预检查 |

**赢家：Hermes**。比例阈值是更优雅的设计，不绑定具体模型窗口大小。

### Gap 2：抽象层次——策略模式 vs 函数模块

| | Hermes Agent | OpenClaw |
|---|---|---|
| 上下文管理抽象 | `ContextEngine` ABC，7 个方法 | ContextEngine（7 方法）+ Plugin Hooks（24 个）+ Internal Hooks |
| 可替换性 | 通过 `context.engine` 配置或插件目录整体替换 | 每个钩子可独立替换，由优先级控制先后 |
| 复杂度 | 低——一个抽象搞定 | 高——三套并行系统（Internal Hook / Plugin Hook / ContextEngine） |
| 学习成本 | 低——实现 7 个方法即可 | 高——需理解三套系统的交互顺序 |

**赢家：取决于需求**。Hermes 的单一抽象更优雅，OpenClaw 的多层机制更灵活但更复杂。OpenClaw 的 24 个 Plugin Hook 覆盖面比 Hermes 大得多（子 Agent 生命周期、消息到达、模型选择等）。

### Gap 3：记忆注入——Fence-tag 隔离 vs 全量拼接

| | Hermes Agent | OpenClaw |
|---|---|---|
| 注入方式 | `<memory-context>` fence-tag 包裹 | MEMORY.md 全量拼入 System Prompt |
| 隔离性 | ✅ 明确分隔，流式输出有 Scrubber 清理 | ❌ 与 System Prompt 混合，无标记隔离 |
| 大小控制 | ~800 tokens 快照 + FTS5 按需检索 | `bootstrapMaxChars=12000` 截断 |
| 安全性 | 注入内容有 `CONTEXT_THREAT_PATTERNS` 扫描 | 依赖 Gateway 层过滤 |

**赢家：Hermes**。Fence-tag 隔离 + 流式 Scrubber + 注入前安全扫描，三层防护。OpenClaw 的全量拼接在工程上更简单但隔离性差。

### Gap 4：压缩质量——迭代摘要 vs 单次摘要

| | Hermes Agent | OpenClaw |
|---|---|---|
| 摘要策略 | 迭代更新（Iterative Summary Update）多次压缩之间保留信息 | 单次摘要 + 硬截断 |
| 摘要前缀 | 详细的 handoff 指令（告知模型如何理解压缩内容） | 简化标记 |
| 辅助模型 | ✅ 用便宜模型做摘要，省钱 | 未指定 |
| 工具输出预处理 | ✅ 先裁剪工具输出再送摘要 | Soft Trim（截断中间保留头尾） |

**赢家：Hermes**。迭代摘要 + 详细 handoff prefix + 辅助模型调用，在压缩保真度上有明显优势。

### Gap 5：检索 vs 全量——FTS5 按需 vs Markdown 全注入

这是最深层的设计哲学差异。

| | Hermes Agent | OpenClaw |
|---|---|---|
| 长期记忆存储 | SQLite + FTS5 + trigram 索引 | Markdown 文件（MEMORY.md） |
| 注入方式 | **按需检索**——FTS5 关键词搜索 → 只注入相关片段 | **全量注入**——整个 MEMORY.md 拼入 System Prompt |
| 容量限制 | 无硬限制（FTS5 索引可无限扩展） | `bootstrapTotalMaxChars=60000` 全局上限 |
| 检索延迟 | ~10ms @ 10k+ 记忆 | N/A（全量拼接） |
| 跨会话 | ✅ WAL 模式，多平台 gateway | ❌ 文件级，无并发保护 |
| KV Cache 友好度 | 高——冻结快照 + 按需检索 = System Prompt 稳定 | 低——MEMORY.md 变化 = System Prompt 变 = Cache 全失效 |

**赢家：Hermes。这是代码层面差距最大的维度。** OpenClaw 的「文件全量拼接」是最简单的实现方式但最不 scalable，而 Hermes 的「FTS5 搜索引擎式记忆」是真正的工程创新。Peter Steinberger 自己在 VISION.md 中也承认了记忆系统的不足：计划「converge on one recommended default path」。

### Gap 6：用户建模——辩证推理 vs 静态文件

| | Hermes Agent | OpenClaw |
|---|---|---|
| 机制 | Honcho 辩证式建模 | USER.md 静态文件 |
| 推理能力 | ✅ 观察选择 → 推断特质 → 检验假设 | ❌ 纯记录 |
| 生成方式 | 动态更新，随使用深化 | Agent 手动写入 |

**赢家：Hermes**。但 Honcho 是可选模块，不是始终激活。

### Gap 7：Token 效率——参数化控制

| | Hermes Agent | OpenClaw |
|---|---|---|
| 压缩预算 | `_SUMMARY_RATIO=0.20`, `_SUMMARY_TOKENS_CEILING=12000` | `maxToolResultTokens=4096`, `bootstrapMaxChars=12000` |
| Skills 加载 | 双通道：目录懒加载（~2000 tokens）+ 按需完整加载 | 仅名称+描述注入，受 `maxSkillsPromptChars` 限制 |
| @ 语法预加载 | ✅ 一次注入替代多轮工具调用 | ❌ 无 |
| Prompt 缓存意识 | ✅ 冻结快照保证 System Prompt 稳定 | 有缓存归一化但被 MEMORY.md 变动破坏 |

**赢家：Hermes**。双通道 Skill 加载 + @ 语法预加载是漂亮的工程优化。

### Gap 8：循环保护——异常驱动 vs 精确定义

| | Hermes Agent | OpenClaw |
|---|---|---|
| 循环检测 | 14 类结构化异常自愈（含 `context_overflow`） | 3 种死循环模式 + 30 次熔断 |
| 精细度 | 异常分类绑定独立恢复策略 | 熔断逻辑更直观 |
| Thinking 处理 | 丢弃历史 thinking（标准做法） | `dropThinkingBlocks`（标准做法） |

**平手**。各有优势——Hermes 的异常分类更系统，OpenClaw 的熔断更直观。

---

## 四、源码层面的根本分歧总结

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  OpenClaw 的上下文管理是「装配线思维」                            │
│  —— 多个独立的 Guards + 多个 Hooks + 多个截断参数                │
│  —— 每个问题写一个函数解决，每层一个守卫                         │
│  —— 功能全但组合逻辑分散在多个模块中                             │
│  —— 记忆是文件，全量拼入，简单直接                               │
│                                                                  │
│  Hermes Agent 的上下文管理是「自适应思维」                        │
│  —— 一个 ContextEngine ABC + 一个 MemoryManager + 一个 Compressor │
│  —— 比例阈值自适应所有模型，FTS5 引擎式检索                      │
│  —— 冻结快照保 Cache，迭代摘要保信息，fence-tag 隔离保安全       │
│  —— 记忆是数据库，按需检索，工程化程度更高                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 五、如果你要二选一——上下文管理维度的决策

### 选 Hermes Agent 的场景：
- 你期待 Agent 长期运行，跨会话积累知识
- 你的上下文窗口大小不确定/会变化（换模型容易）
- 你需要安全边界清晰（fence-tag + 注入扫描）
- 你愿意接受 Python 技术栈
- **代码层的硬理由**：FTS5 检索 > 全量文件拼接；比例阈值 > 绝对阈值；迭代摘要 > 单次压缩

### 选 OpenClaw 的场景：
- 你需要细粒度控制上下文装配的每一个步骤
- 你需要在子 Agent 生成/结束时定制上下文传递
- 你需要 TypeScript 技术栈
- 你更在乎「每个环节都可独立替换」的灵活性
- **代码层的硬理由**：24 个 Plugin Hook 覆盖面无人能及；ContextEngine 7 方法 + Hooks 提供了最细粒度的上下文生命周期控制

### 代码层最难追上的 Gap：
1. **Hermes 的 FTS5 检索式记忆**——OpenClaw 要从「文件全量拼接」改为「数据库按需检索」，需要改记忆架构底层
2. **OpenClaw 的子 Agent 上下文生命周期钩子**——Hermes 的 ContextEngine 没有 `prepareSubagentSpawn`/`onSubagentEnded` 等价物

---

## 六、参考来源

1. `NousResearch/hermes-agent/agent/context_engine.py` —— GitHub API 直读，2026-06-10
2. `NousResearch/hermes-agent/agent/context_compressor.py` —— GitHub API 直读，2026-06-10
3. `NousResearch/hermes-agent/agent/memory_manager.py` —— GitHub API 直读，2026-06-10
4. `NousResearch/hermes-agent/hermes_state.py` —— GitHub API 直读，2026-06-10
5. `NousResearch/hermes-agent/agent/prompt_builder.py` —— GitHub API 直读，2026-06-10
6. `openclaw/openclaw/VISION.md` —— GitHub API 直读，2026-06-10
7. OpenClaw Agent Loop 架构拆解 —— DataLab 系列（源码级验证）
8. OpenClaw vs OpenCode 钩子系统对比 —— 头条技术分析（源码级验证）
