# Popwave 全链路 vs Hermes Agent / OpenClaw 精准匹配

> 版本：v1.0  
> 日期：2026-06-10  
> 决策者：江轩  
> 产出方：pop 助理  
> 数据基础：飞书文档「Popwave 管线全链路 + Skill 依赖」+ Hermes / OpenClaw 源码深度拆解

---

## 〇、Popwave 全链路画像

读完飞书文档后，Popwave 的真实架构可以用一句话概括：

> **一个以文件系统为状态协议、以 expert-writer 为调度器的 9-Skill 串行流水线，核心特征是「沉淀过程内容、逐章 delta 聚合、闸门确认驱动」。**

关键结构特征：

| 维度 | Popwave 现状 |
|-|-|
| 调度模式 | expert-writer 元 Skill 路由 → 子 Skill 串行执行 |
| 状态协议 | workspace-index.yaml / entity-snapshot.yaml / chapter-state.yaml / constitution.yaml / project.yaml / global-summary.md / 交叉引用记录.md / novel.db |
| 数据流转 | 每个 Skill 有明确的上游依赖文件 + 下游产出文件（详见飞书文档 §3） |
| 进度追踪 | workspace-index.yaml#progress（last_completed_skill / next_skill / checkpoints） |
| 跨 session 连续性 | entity-snapshot.yaml 章末全量重建 + constitution.yaml 跨项目教训（L001/L002） |
| 闸门机制 | 6 个用户确认闸门（story-engine / 起终点快照 / 场景卡 / 精读闸门 / 里程碑 / 交接验证） |
| 章节上下文 | chXXX-事实骨架.md + chXXX-登场人物卡.md → prose-render 只读这两个文件，不碰上游 Canvas |
| 核心约束 | Design 不碰文风 / Render 不碰剧情 |

---

## 一、逐层匹配：全链路每条能力线 vs 两个框架

### 1.1 调度层：expert-writer vs 框架

| Popwave 能力 | Hermes Agent | OpenClaw | 匹配度 |
|-|-|-|-|
| expert-writer Think→Execute→Reflect 三层 | `delegate_task` role=orchestrator + background_review | Gateway 路由 + agent-runner 四层调用链 | **Hermes 直接对路**——delegate_task 的 role 系统（leaf/orchestrator）是 Popwave Skill 串联的天然载体；OpenClaw 的 Gateway 路由设计为"消息平台→Agent"，不适合"元 Skill→子 Skill"路由 |
| workspace-index.yaml 全局感知 (§0) | MemoryManager.prefetch_all() → FTS5 检索 | MEMORY.md 全量注入 | **Hermes 完胜**——FTS5 检索语义 = workspace-index 的查询模式；OpenClaw 全量注入不可行 |
| Reflect L1 索引回写 (§3.3) | MemoryManager.sync_all() + ContextEngine.afterTurn | 无等价自动回写机制 | **Hermes 原生支持** |
| Reflect L2 consistency check | background_review 机制 | 无等价 | **Hermes 原生支持** |
| pipeline_deps 前置校验 (§3.1.6) | delegate_task 的 subagent auto-deny 栅栏 | 需自定义 Plugin Hook | Hermes 更直接 |
| 管线进度回写协议 (§5.2) | on_session_end + state.db parent_session_id | 需手动配置 | **Hermes 更对路** |

### 1.2 状态层：文档中列出的每个共享文件

| Popwave 共享文件（飞书 §4.1） | 被消费场景 | Hermes 等价 | OpenClaw 等价 | 判决 |
|-|-|-|-|-|
| **story-engine.yaml** | plot / chapter-design | SOUL.md 或 MemoryProvider 注入 | AGENTS.md（bootstrapMaxChars=12000） | 平手——都是文件注入 |
| **constitution.yaml** | plot / chapter-design / render / qa | guardrails + SOUL.md | 无原生 guardrails，需 plugin | **Hermes 胜**——can_do/must_do 规则天然匹配 |
| **project.yaml** | 多个 Skill | state.db 配置表 | 配置文件（.json/.yaml） | 平手 |
| **L1-01\~06 六件套** | plot Steps 1-7 / chapter-design | 按需 FTS5 检索注入 | 全量 Markdown 文件注入 | **Hermes 胜**——L1 文件总 size 可能非常大，FTS5 按需优于全量 |
| **act-XX.yaml** | chapter-design 核心输入 | 当前幕的压缩摘要注入 | 文件注入 | Hermes 胜（可以按当前幕过滤检索） |
| **entity-snapshot.yaml** | chapter-design 下一章 | **state.db 的 session delta → aggregate 机制** | MEMORY.md | **Hermes 碾压**——entity-snapshot 的"章末全量重建"模式与 Hermes 的 delta 聚合完全一致；OpenClaw 没有等价结构 |
| **起点快照.md / 终点快照.md** | plot Step 2 / chapter-design | 冻结快照注入 System Prompt | 文件注入 | 平手 |
| **chXXX-事实骨架.md + 人物卡** | prose-render 唯二输入 | @ 语法即时注入（@file:骨架:10-50） | 全量拼接 | **Hermes 胜**——@ 语法精准取片段的模式优于全量拼接 |
| **styles/{书名}.md** | prose-render Phase 1 | Skill 目录懒加载 + 按需完整加载 | 文件注入 | Hermes 胜——双通道加载节省 token |

### 1.3 管线阶段：逐阶段匹配

| Popwave 阶段 | 核心操作 | Hermes 能力 | OpenClaw 能力 |
|-|-|-|-|
| **bookstrap (FWD)** | 20 个 Phase 串行，大量设定文件产出 | subagent_dispatch 逐个 Phase → 父 Agent 聚合 | 需自定义编排，无原生"Phase 管道" |
| **bookstrap (REV)** | Phase r1\~r6 逐章读取已有正文 | FTS5 检索 + delegate_task 并行拆 N 章 | MEMORY.md 全量注入（不可行） |
| **plot** | 12 个 Step，每步消费多个上游文件 | delegate_task + 按需检索上游文件 | 文件全量注入（上游文件多且大） |
| **chapter-design** | Step 1\~3，有硬性约束（不碰文风） | subagent toolset 隔离 + DELEGATE_BLOCKED_TOOLS | Agent 路由 + tool 权限白名单 |
| **prose-render** | Phase 1\~3 + Step 5，有硬性约束（不碰剧情） | subagent toolset 隔离 + 独立 context | Agent 路由 |
| **qa** | 三层感受型报告（不存档） | delegate_task 摘要返回 | 子 Agent 返回 |
| **deconstructor** | 7 个 Phase 串行并行可选 | delegate_task + batch 并行 | 自定义编排 |
| **pop-dna** | ≥20 章采样 + 全书搜索 | FTS5 全文搜索 | 文件读取 |
| **闸门机制** | 6 个用户确认闸门 | 原生 approval 回调 | Gateway 级 DM 配对审批 |

### 1.4 跨 session / 跨项目能力

| Popwave 能力 | Hermes Agent | OpenClaw | 判决 |
|-|-|-|-|
| **跨 session 连续性**（3 个月后写第 150 章） | state.db FTS5 索引跨 session 保留 | MEMORY.md 全量注入（根本装不下 149 章上下文） | **Hermes 碾压** |
| **跨项目教训**（constitution L001/L002） | **自进化 Skill 蒸馏**——从经验中提取可复用模式 | 无自进化能力，靠用户手动写 | **Hermes 独有优势** |
| **pre_read_status 精读闸门** | ContextEngine 压缩摘要 + FTS5 检索倒数 20 章关键事实 | 文件读取 20 个章文件全量注入（不可行） | **Hermes 碾压** |
| **entity-snapshot 一致性校验**（Reflect L2） | background_review + guardrails | 需自定义 Plugin | Hermes 原生支持 |

---

## 二、两个框架在 Popwave 管线中的「不可行点」

### OpenClaw 的不可行点

| # | 场景 | 为什么不可行 | 严重性 |
|-|-|-|-|
| 1 | bookstrap REV 逐章读取已有 149 章内容 | MEMORY.md 全量注入上限 60000 字符，149 章远超此限 | 🔴 致命 |
| 2 | entity-snapshot 章末自动重建 | 无等价机制——需手动维护文件 | 🔴 致命 |
| 3 | 跨 session 检索："第 47 章张三做了什么？" | 无 FTS5，只能全量注入 MEMORY.md → 装不下 → 查不到 | 🔴 致命 |
| 4 | 跨项目经验自动蒸馏 | 无自进化，L001/L002 只能人工手动跨项目抄 | 🟠 严重 |
| 5 | 多 Phase/Step 串行管线调度 | 需在 TypeScript 中手写编排逻辑 | 🟡 中等 |
| 6 | Python Skill 管线 | TypeScript 桥接 = 无谓摩擦 | 🟡 中等 |

### Hermes Agent 的不可行点

| # | 场景 | 说明 | 严重性 |
|-|-|-|-|
| 1 | FTS5 中文分词 | SQLite FTS5 原生不支持中文分词，需验证 trigram 补丁质量 | 🟡 PoC 必做 |
| 2 | — | 除 FTS5 中文分词外，全链路无其他不可行点 | — |

---

## 三、关键结论

### 3.1 匹配度量化

| 管线层 | Hermes Agent | OpenClaw |
|-|-|-|
| 调度层（expert-writer 路由 + 进度回写） | ✅ 高度匹配（delegate_task + background_review） | ⚠️ 部分匹配（Gateway 路由设计方向不同） |
| 状态层（9 类共享文件 + novel.db） | ✅ 高度匹配（FTS5 + MemoryProvider 适配器） | ❌ 不可行（60000 字符硬上限 vs 200 万字数据） |
| 管线执行（bookstrap/plot/design/render/qa） | ✅ 全部可承载 | ⚠️ 部分承载（长文本场景不可行） |
| 跨 session（entity-snapshot 连续性） | ✅ 原生支持 | ❌ 不可行 |
| 跨项目（L001/L002 教训蒸馏） | ✅ 独有能力 | ❌ 不支持 |
| 生态兼容（Python Skill 管线） | ✅ 原生 Python | ❌ TypeScript 摩擦 |

### 3.2 根本原因

Popwave 的全链路文档揭示了一个本质事实：

> **Popwave 不是一个"多消息渠道的 AI 助手"，而是一个"以文件为状态协议、以多 Skill 串行执行为核心的写作工程管线"。**

OpenClaw 的整个架构是为"多消息平台 + 多 Agent 协作 + 即插即用"设计的——这是它的优势也是它的边界。当场景变为"200 万字长文本 + 串行管线 + 文件状态协议"时，OpenClaw 的核心设计（文件全量注入 × 60000 字符硬上限 × Gateway 路由）和 Popwave 的核心需求之间存在硬冲突。

Hermes Agent 的架构（FTS5 检索 × 无容量硬上限 × delegate_task 委派 × MemoryProvider 适配器）则与 Popwave 的管线设计呈**结构同构**——不是"能适配"，而是"你在文件系统上手工维护的这套状态协议，正好是 Hermes 运行时的设计模式"。

### 3.3 一句话

**看完 Popwave 全链路文档后，选 Hermes 的理由从 4 个硬约束变成了 6 个匹配层 + 0 个不可行点（除 FTS5 中文分词）；选 OpenClaw 的代价从 1 个致命约束变成了 4 个不可行点。差距不是缩小了，是拉大了。**

---

## 四、参考来源

- Popwave 业务全链路飞书文档：`Jkezdi72uoWoYBxE60Tctp7cnbd`
- `NousResearch/hermes-agent` 源码直读（context_engine / context_compressor / memory_manager / hermes_state / prompt_builder / delegate_tool / mixture_of_agents_tool）
- `openclaw/openclaw/VISION.md` 源码直读
- Hermes Agent vs OpenClaw 全面对比
- 上下文管理代码级深度对比
- 为什么选择 Hermes Agent 作为 Popwave 技术底层