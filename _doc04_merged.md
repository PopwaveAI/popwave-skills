> **状态：已决策 ✅** ｜ 2026-06-10 经三轮调研后选定 Hermes Agent 作为 Popwave 技术底层。OpenClaw 因记忆架构与 200 万字场景不兼容、安全风险被排除。

# 为什么选择 Hermes Agent 作为 Popwave 技术底层

> 版本：v1.0  
> 日期：2026-06-10  
> 决策者：江轩  
> 产出方：pop 助理  
> 前置调研：Hermes Agent vs OpenClaw 全面对比 · 上下文管理代码级深度对比

---

## 〇、本文档的用途

Popwave 是一个 AI 网文 Agent × IDE 工具。一本网文通常 200 万字，跨 3-6 个月、几十上百个写作 session。每个 session 需要精确获取前面所有章节的角色状态、伏笔进度、世界观规则、数值体系——不能靠"模型自己记住"。

我们需要一个 **Agent 底层运行时**来承载 Popwave 已有的状态协议。

经过三轮深入调研——社区口碑、代码层架构对比、上下文管理源码级分析、以及针对 Popwave 真实项目（深渊主宰·外神降临）的场景匹配——**我们选择 Hermes Agent 作为技术底层**。

本文档记录这个决策的完整推演过程，供团队内部参考和未来回顾。

---

## 一、Popwave 的真实约束：为什么这个选择不是"偏好"而是"唯一解"

### 1.1 核心约束：200 万字 × 跨季度工程

```
一本200万字网文的生命周期：
  开书 → 拆参考书 → DNA提取 → 剧情架构 → 正文写作×N轮 → 审稿QC×N轮 → 修改×N轮 → 发布渲染
  持续：3-6个月 | session数：50-200 | 每session产出：1-3章
```

这个场景对 Agent 基础设施有四个硬性约束：

| 约束 | 含义 | 不可妥协性 |
|-|-|-|
| **海量状态检索** | 写到第 150 章时，需快速检索第 23 章埋的伏笔、第 47/89 章角色的行为记录 | 硬约束 |
| **跨 session 连续性** | 3 个月后的 session 必须感知之前的全部关键状态 | 硬约束 |
| **中文长篇文本检索** | 200 万字中文小说内容，需要高效的全文索引 | 硬约束 |
| **Python 生态兼容** | Popwave 全线 Skill 为 Python，底层运行时必须原生兼容 | 硬约束 |

### 1.2 Popwave 已在手工维护的状态协议

通过对 `6-9测试` 项目的全面审视，Popwave 已经建立了一套极其完整的状态管理协议——跑在文件系统上：

| Popwave 现有组件 | 功能 | 等价 Hermes 能力 |
|-|-|-|
| `novel.db`（SQLite，7 张表） | 章节/角色/事件/关系/伏笔/物品/地点 | `state.db`：SQLite + FTS5 全文检索 |
| `entity-snapshot.yaml`（章末 delta → 全量聚合） | 每章写完后的角色/事件/标记全量快照 | Writer Step 3.3 的自动 delta 聚合 |
| `chapter-state.yaml` | 主角属性/位置/timeline/flags 逐章追踪 | Session state 追踪 |
| `global-summary.md` | 主角/角色/势力/伏笔/L1信息释放 五维状态表 | Context compression summary |
| `constitution.yaml`（cant_do 5 条 + must_do 7 条） | 写作宪法——不可触碰的红线和铁律 | SOUL.md + guardrails |
| `_交叉引用记录.md` | L1 → 角色卡 → 章节 三维映射 + 依赖图 | 跨文件依赖索引 |
| `ch001-design.md`（8 块设计包） | 每章的 8 维设计模板 | Skill 自动生成的前驱形态 |

**Popwave 需要的不是"一个 AI Agent 框架"，而是"一个运行时引擎来消费这些已有的状态协议"。**

---

## 二、为什么 OpenClaw 被排除

### 2.1 致命缺陷 #1：记忆架构与 200 万字场景不可调和

OpenClaw 的记忆系统是**文件式全量注入**——MEMORY.md 的全部内容在每轮对话中拼入 System Prompt：

```
OpenClaw 记忆模型：
  MEMORY.md（Markdown 文件）
    → 全量拼入 System Prompt
    → bootstrapTotalMaxChars = 60000 硬上限
    → 每轮都注入，无论是否需要
    → 文件变化 = System Prompt 变化 = KV Cache 全部失效
```

200 万字 ≈ 3,000,000+ 字符。OpenClaw 的 `bootstrapTotalMaxChars=60000` 只能容纳约 2% 的内容。而且全量注入意味着每次 API 调用都在浪费 token 发送不需要的 98%。

**这是硬边界，不是偏好选择。**

### 2.2 致命缺陷 #2：安全风险达到国家级警告级别

| 来源 | 动作 |
|-|-|
| **中国国家互联网应急中心（CNCERT）** | 联合发布《OpenClaw 安全使用实践指南》 |
| **国家网络安全通报中心** | 发布安全风险预警 |
| **工信部 NVDB** | 多次发布风险提示 |
| **微软** | 建议不要在企业工作站运行 |
| **Meta** | 带头封杀内部使用 |

累计漏洞 111+，高危 38 个。ClawHub 技能市场约 25% 恶意率。全球 135,000+ 实例暴露公网。

Popwave 将来可能承载用户的创作数据——原创内容、角色设定、章节草稿。这些数据的泄露对创作者是灾难性的。**安全底座不硬的框架，不能作为创作工具的底层。**

### 2.3 次要缺陷 #3：TypeScript 生态与 Python 写作管线不兼容

Popwave 全线 Skill 为 Python：pop-novel-writer、pop-novel-plot、pop-dna、pop-novel-deconstructor、pop-novel-bookstrap、pop-novel-qa。在 TypeScript 框架中桥接 Python 写作管线属于"给自己制造无谓的摩擦"。

### 2.4 次要缺陷 #4：运维成本随时间递增

OpenClaw 用户真实反馈（Hacker News）：

- "每次大版本升级都会破坏已有配置"
- "15% broken at every moment"
- 更新频率 2-3 次/周，每次都可能破坏工作流

跨季度工程需要的是稳定的基础设施，不是在每个写作 session 前先修框架配置。

---

## 三、为什么 Hermes Agent 是正确答案

### 3.1 架构匹配：检索式记忆 = 200 万字小说唯一可行的检索方案

```
Hermes Agent 记忆模型：
  SQLite state.db（WAL 模式，并发安全）
    → FTS5 全文索引 + trigram 索引
    → 工具调用：session_search("张三 伏笔") → 10ms 返回相关片段
    → 只注入相关片段到上下文（O(1) 而非 O(n)）
    → 无容量硬上限（FTS5 索引可无限扩展）
    → Session 结束后索引保留，跨 session 检索
```

对 Popwave 而言，这意味着：

- 写到第 150 章时，Agent 可以通过 `session_search` 检索任何前 149 章的内容
- 检索结果按相关度排序，只注入最相关的片段进上下文
- 不需要把整本小说拼进 Prompt
- 每轮对话的 System Prompt 保持稳定 \~ KV Cache 持续命中 \~ 成本可控

### 3.2 协议对接：MemoryProvider ABC = 自然接入 Popwave 已有数据层

Hermes 的 `MemoryManager` 设计为"内置 provider + 最多一个外部 provider"的可插拔模式。Popwave 只需要实现一个 `PopwaveMemoryProvider`：

```python
class PopwaveMemoryProvider(MemoryProvider):
    """对接 Popwave 的 novel.db + YAML 状态文件到 Hermes 记忆系统"""

    def prefetch(self, user_message: str) -> str:
        # 从 novel.db 的 FTS5 索引检索相关伏笔/角色/事件
        # 从 entity-snapshot.yaml 加载当前角色状态
        # 从 global-summary.md 注入压缩摘要
        ...

    def sync(self, user_msg: str, assistant_response: str) -> None:
        # 写完一章后自动更新 entity-snapshot.yaml
        # 更新 global-summary.md
        # 更新 chapter-state.yaml
        ...
```

**Popwave 已有的数据层不用改，加一个适配器即可接入 Hermes 运行时。**

### 3.3 自进化技能：跨季度工程的核心增值能力

Popwave 的工作流中有大量重复模式。每个模式在 3-6 个月的工程中会重复几十上百次。Hermes 的学习循环可以在积累足够经验后自动蒸馏 Skill：

```
每次 QC 审稿的流程（重复 100+ 次）：
  读章节 → 感受型三层介入 → 发现问题 → 标记 → 建议方向

  15 次后 → Hermes 识别出「江轩的审稿模式」
  30 次后 → 自动蒸馏为 pop-novel-qa.skill.yaml
  后续 QC → 自动带上有经验的检查项
```

同样适用于：人物卡一致性检查、伏笔追踪、世界观规则验证、金手指节奏检查、面板更新频率检查——这些都是 constitution.yaml 中已定义的规则，可以被自动化为 Skill。

**第 1 个月和第 6 个月，Agent 的能力不一样。这是 OpenClaw 的静态技能体系无法提供的。**

### 3.4 多 Agent 编排：足够用且对路

从 `delegate_task` 工具源码分析，Hermes 的多 Agent 支持完全覆盖 Popwave 的管线需求：

| Popwave 需求 | Hermes 能力 |
|-|-|
| 串行管线（开书→拆书→DNA→剧情→写作→QC） | 单子 Agent 委派，父 Agent 只收摘要 |
| 并行拆 3 本参考书 | `delegate_task` batch 模式，ThreadPoolExecutor 并发 |
| 写作 + QC 同时跑 | 默认 3 并发子 Agent，可配更高 |
| 不同阶段用不同模型 | 子 Agent 独立配置 toolset + provider |
| 运行时监控 | 活跃注册表 + 心跳 + 中断（`interrupt_subagent`） |
| 防止无限嵌套 | `max_spawn_depth` 控制 + `DELEGATE_BLOCKED_TOOLS` 安全栅栏 |

**OpenClaw 的 24 个 Plugin Hook + 子 Agent 生命周期钩子粒度更细，但对 Popwave 是 over-engineering——我们的管线是串行流水线，不需要那么细的上下文传递控制。**

### 3.5 安全底座：零 CVE + 容器硬化 + 注入扫描

| Hermes 安全能力 | 对 Popwave 的意义 |
|-|-|
| Docker 默认只读根文件系统 | 用户的创作数据不会因为 Agent 工具调用被意外修改 |
| `CONTEXT_THREAT_PATTERNS` 注入扫描 | 外部上下文文件（参考书分析、素材蒸馏）注入前安全检查 |
| `Tirith` 凭证剥离 | API Key 不会泄露到生成内容中 |
| `StreamingContextScrubber` 流式清洗 | 记忆上下文不会泄露到用户可见的写作输出中 |
| 零已知 CVE | 安全记录干净，适合承载用户创作数据 |

### 3.6 Python 原生兼容：零语言摩擦

Popwave 全线 Skill 为 Python。Hermes Agent 核心为 Python。Popwave 的 Skill 可以直接作为 Hermes 的 Skill 加载，或通过 MCP 调用。不需要任何桥接层。

---

## 四、需要正视的风险

### 4.1 FTS5 中文分词质量 —— 上线前必做 PoC

SQLite FTS5 默认使用空格分词，对中文的支持不如 jieba 等专业分词器。Hermes 源码中有 trigram 索引作为补充（`messages_fts_trigram_*` 触发器），但 200 万字中文小说场景下的检索召回率和精度需要在真实数据上验证。

**PoC 验证项：**

- 在 10 万/50 万/200 万字小说正文上建立 FTS5 + trigram 索引
- 测试以下典型检索场景的召回率与精度：

  - 角色名检索（"江轩"、"巴拉斯"）
  - 伏笔检索（"恐惧神子印记"、"外神渗透"）
  - 事件检索（"科尔帮覆灭"、"沙漠神庙"）
  - 模糊检索（"那个瘦高男人"、"主角第一次杀人的时候"）
- 测量 200 万字索引的建立时间和存储开销
- 如果需要，评估接入 jieba 分词 + FTS5 tokenizer 的可行性

### 4.2 项目尚年轻（3 个月）

Hermes Agent 2026 年 2 月发布。虽然 Nous Research 是有信誉的团队（融资过亿美元，YaRN/Nomos/Psyche 模型家族），但 Agent 框架本身暴露时间短。版本迭代剧烈（v0.16.0 单版 874 commits），API 可能存在 breaking change。

**缓解措施：** 锁定版本号，不追 latest；接入前在 staging 环境完成全面集成测试。

### 4.3 社区负面声音

- 抄袭争议（EvoMap Evolver 同构指控）——声誉风险，暂未实质影响项目
- 游击营销争议（Reddit 用户指控 astroturfing）——不影响技术决策
- 自我评估不可靠（AI 自评永远满分）——不影响我们，Popwave 的 QC 由作家/编辑评判

---

## 五、实施路线：Hermes 作为 Popwave 状态协议的运行时

### 5.1 核心思路

**不是「用 Hermes 替代 Popwave 的 Skill 管线」，而是「让 Hermes 成为 Popwave 状态协议的运行时引擎」。**

```
Popwave 状态层（已有，不变）：
  novel.db ←→ entity-snapshot.yaml ←→ chapter-state.yaml ←→ global-summary.md

                    ↕ PopwaveMemoryProvider 适配器 ↕

Hermes 运行时层（新增）：
  MemoryManager → FTS5 检索 → ContextEngine 压缩 → Prompt Builder 装配
```

### 5.2 分步实施

```
Phase 1：PoC 验证
  - FTS5 中文分词验证
  - novel.db schema 与 state.db 对齐评估
  - 最小可用的 PopwaveMemoryProvider 原型
  - 目标：在一次 Hermes session 中成功检索到小说历史内容

Phase 2：核心接入
  - 实现 PopwaveMemoryProvider（对接 novel.db + entity-snapshot.yaml）
  - 实现 PopwaveContextEngine（基于 constitution.yaml 的规则注入）
  - 实现 Chapter Delta → Entity Snapshot 自动聚合
  - 目标：写完一章后自动更新全部状态文件

Phase 3：Skill 自动化
  - 将 pop-novel-qa / pop-novel-plot 等管线接入 Hermes 的 delegate_task
  - 识别高频重复模式，配置自进化循环
  - 接入 background_review 进行章节间一致性检查

Phase 4：生产化
  - 锁定 Hermes 版本
  - 完整测试套件（包含 200 万字规模的检索性能测试）
  - 部署文档
```

---

## 六、决策记录

| 决策项 | 结论 | 决策基础 |
|-|-|-|
| Agent 底层运行时 | **Hermes Agent** | 4 个硬约束全部满足，3 个次要优势（安全/生态/自进化）加分 |
| 排除 OpenClaw | 硬性排除 | 记忆架构不可行 + 安全风险不可接受 + 生态不兼容 |
| 接入方式 | MemoryProvider 适配器 | 不修改 Popwave 已有数据层，只加适配器 |
| 关键 PoC | FTS5 中文分词验证 | 上线前必须通过 |

### 选择 Hermes 不是因为它"更好"——是因为 Popwave 场景（200 万字 × 跨季度 × 检索式记忆 × Python 生态）与 OpenClaw 的架构边界（文件全量注入 × 60000 字硬上限 × TypeScript）之间存在**硬冲突**。

### 这个场景只有一个合理的选择。

---

## 七、参考来源

1. `NousResearch/hermes-agent/agent/context_engine.py` —— GitHub API 直读，2026-06-10
2. `NousResearch/hermes-agent/agent/context_compressor.py` —— GitHub API 直读，2026-06-10
3. `NousResearch/hermes-agent/agent/memory_manager.py` —— GitHub API 直读，2026-06-10
4. `NousResearch/hermes-agent/hermes_state.py` —— GitHub API 直读，2026-06-10
5. `NousResearch/hermes-agent/agent/prompt_builder.py` —— GitHub API 直读，2026-06-10
6. `NousResearch/hermes-agent/tools/delegate_tool.py` —— GitHub API 直读，2026-06-10
7. `NousResearch/hermes-agent/tools/mixture_of_agents_tool.py` —— GitHub API 直读，2026-06-10
8. `openclaw/openclaw/VISION.md` —— GitHub API 直读，2026-06-10
9. OpenClaw Agent Loop 架构拆解 —— DataLab 系列（源码级验证）
10. OpenClaw vs OpenCode 钩子系统对比 —— 经源码验证的第三方分析
11. Hacker News "Ask HN: Who is using OpenClaw?" (2026)
12. Reddit r/LocalLLaMA / r/openclaw / r/hermesagent 社区讨论
13. Security Scorecard / 微软 / 思科 Talos 安全报告
14. 中国国家互联网应急中心（CNCERT）《OpenClaw 安全使用实践指南》
15. Popwave 项目实例：`6-9测试/深渊主宰·外神降临` 完整项目文件结构

---

# 附录A：全链路逐层匹配报告

以下内容来自「Popwave 全链路 vs Hermes Agent / OpenClaw 精准匹配」：

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