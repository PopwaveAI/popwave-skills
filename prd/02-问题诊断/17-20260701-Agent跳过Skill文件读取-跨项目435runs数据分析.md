# Agent 跳过 Skill 文件读取：跨项目 435 runs 数据分析

> **编号**: 17-20260701  
> **日期**: 2026-07-01  
> **类型**: 问题诊断  
> **数据源**: 14 个项目、435 个 runs、201 个有 token 数据  
> **前置文档**: [17-Pop调度层硬加载多Skill集群-PRD](../01-管线架构/17-Pop调度层硬加载多Skill集群-PRD.md)
> **测试平台**: Popwave（基于 OpenClaw 开源项目）

## 一、问题现象

用户在 6-30-项目d 中指令 agent "把飓风营救纳入幕1去整合剧情"，连续 5 轮 agent 未能理解——产出偏离指令、把确认门当产出、最终可用幕纲是用户自己写的。

## 二、根因定位：Skill 加载的强保障与弱保障

### 2.1 Skill 加载的两层机制

Popwave (OpenClaw) 的 skill 加载分两层，保障强度完全不同：

| 层级 | 机制 | 保障强度 | 覆盖范围 |
|:-----|:-----|:---------|:---------|
| **强保障（程序硬注入）** | 元 skill（如 expert-writer）的 SKILL.md 由 host 层每次 run 强制注入 prompt | 100% 保证加载 | 仅元 skill 的 SKILL.md 本身 |
| **弱保障（prompt 唤起）** | 元 skill 的 step 文件、references 文件，以及所有下游 skill（plot/create/seed 等）的 SKILL.md、step 文件、模板文件 | 依赖 agent 按 SKILL.md 中的指引主动 readFile | 所有非元 skill SKILL.md 的文件 |

**元 skill 的 SKILL.md 是程序保证每次都能加载的。** 但元 skill 的 step 和 reference 文件，以及所有下游 skill 的全部文件，都是通过已加载的 SKILL.md 中的 prompt 指引（如"读取 step-1-volume-anchor.md"）唤起 agent 去 readFile——这天然是弱保障，受对话轮次、上下文压力、注意力分配影响。

### 2.2 Agent 从未读取 plot skill 文件

从 events.jsonl 确认：15 轮对话历史注入，cacheRead 212K tokens 中 skill 文件内容占比 < 1%。expert-writer 的 SKILL.md 虽然每次被强制注入（强保障），但其中指向 plot SKILL.md 和 step 文件的读取指引（弱保障）从未被 agent 执行。Agent 在纯对话记忆模式下运行，plot v14.1 的外部燃料台机制完全没被读到。

### 2.3 Skill 机制存在但 Agent 感知不到

用户说"飓风营救做主干、深渊主宰做发动机"，这正是外部燃料台的骨架源/发动机源角色定义。但 agent 没读到这个机制，把两个参考平权并列，实际执行时拿深渊主宰结构当骨架，Taken 只做点缀。

### 2.4 对话历史替代了 Skill 原文

卷纲幕001映射"绝境建置·割喉者诞生"在对话历史中，agent 把它当硬约束。即使口头说"用 Taken 做主干"，agent 仍在尝试把 Taken 塞进深渊主宰结构里——因为它对"怎么整合外部参考"的理解全部来自对话上下文中的自我推理，而非 skill 原文。

## 三、跨项目数据分析

### 3.1 数据规模

| 维度 | 数值 |
|:-----|:-----|
| 扫描项目数 | 14 |
| 总 runs 数 | 435 |
| 有 token 数据的 runs | 201 |
| 检测到 agent 主动读取 skill 文件的 runs | 16 (3.7%) |

### 3.2 按对话轮次分段

| 注入轮次 | runs 数 | skill 读取率 | 平均 cacheRead (K tokens) | 平均输出 tokens |
|:---------|:--------|:------------|:------------------------|:---------------|
| 0-3 轮 | 63 | **11.1%** | 178K | 1803 |
| 3-6 轮 | 31 | **0.0%** | 516K | 2355 |
| 6-10 轮 | 59 | **1.7%** | 153K | 921 |
| 10-15 轮 | 130 | **3.1%** | 362K | 1624 |
| 15-20 轮 | 91 | **2.2%** | 659K | 2295 |
| 20+ 轮 | 61 | **3.3%** | 776K | 2766 |

### 3.3 按 cacheRead 分段

| 缓存大小 (K tokens) | runs 数 | skill 读取率 | 平均轮次 |
|:---------------------|:--------|:------------|:---------|
| 0-50K | 7 | 14.3% | 6.0 |
| 50-100K | 12 | **0.0%** | 7.2 |
| 100-200K | 21 | **0.0%** | 8.3 |
| 200-300K | 12 | 16.7% | 9.7 |
| 300-500K | 41 | **2.4%** | 13.0 |
| 500K+ | 107 | **2.8%** | 14.1 |

### 3.4 按 promptTokens 分段

| prompt 大小 (K tokens) | runs 数 | skill 读取率 | 平均轮次 |
|:-----------------------|:--------|:------------|:---------|
| 0-50K | 76 | 3.9% | 11.1 |
| 50-100K | 21 | 4.8% | 7.0 |
| 100-150K | 14 | **0.0%** | 9.9 |
| 150-200K | 28 | **0.0%** | 10.8 |
| 200-300K | 24 | **0.0%** | 14.7 |
| 300K+ | 37 | 8.1% | 18.4 |

## 四、核心结论

### 4.1 临界点

| 指标 | 临界点 | 现象 |
|:-----|:-------|:-----|
| 对话轮次 | **3 轮之后** | skill 读取率从 11% 骤降至 0-3% |
| cacheRead | **100K tokens 之后** | 读取率归零（直到 200K 才偶尔有） |
| promptTokens | **100K tokens 之后** | 持续为 0%，直到 300K+ 才偶发恢复 |

### 4.2 本质机制

Agent 在第 1 轮被注入 expert-writer SKILL.md（host 层强制注入），然后在第 2-3 轮可能主动读取了一次下游 skill 的 SKILL.md。但从第 3 轮开始，agent **完全切换到对话记忆模式**：

1. cacheRead 积累到 100K tokens 时，agent 已有"足够多的上下文记忆"
2. 模型基于上下文记忆判断"不需要再读 skill 文件"
3. 后续所有行为都基于对话历史中对 skill 的**摘要理解和错误推断**
4. 对话历史中的摘要信息比 skill 原文优先级更高（因为更近、更熟悉）
5. 即使 skill 被更新（如 plot v14.1 新增外部燃料台），agent 也不会感知到变化

### 4.3 雪崩效应

```
轮次1-2: agent 读 SKILL.md → 理解基本流程
轮次3+: agent 停止读 SKILL.md → 靠记忆推断
轮次5+: 记忆中的摘要已偏离 skill 原文 → 但 agent 不自知
轮次10+: 用户给出新指令（如"用Taken做主干"）→ agent 用旧记忆理解新指令
轮次15+: agent 产出的内容完全基于错误推断 → 用户不满 → agent 反思但只改症状不改根因
```

### 4.4 16 个有 skill 读取的样本特征

- **绝大多数在 turns=0-2**：首次进入 skill 时 agent 会读
- 读取最多的是 `pop-writer-v3-plot/SKILL.md` 和 `pop-writer-v3-create/SKILL.md`
- 只有 2 个在 turns=16+ 时读取了 create 的 SKILL.md + step-1
- 6-30-项目d 的 turns=0 run 读了 7 个 skill 文件（seed/plot/create），但后续 15 轮全部不读

### 4.5 高轮次无读取的重灾区

| 项目 | 轮次 | cacheRead | promptTokens | 输出 tokens | skill 读取 |
|:-----|:-----|:----------|:-------------|:-----------|:-----------|
| 6-26项目d | 20 | 5269K | 411K | 6465 | 0 |
| 6-26项目d | 20 | 1125K | 429K | 10165 | 0 |
| 6-27项目a | 20 | 2072K | 0K | 3729 | 0 |
| 6-27项目a | 20 | 2251K | 455K | 1770 | 0 |
| 6-30-项目d | 20 | 792K | 389K | - | 0 |

## 五、多平台对比与方案借鉴

"Lost in the Middle"和"Context Rot"是所有 LLM agent 的共性问题。Claude Code、OpenAI Codex、Cursor 均已遇到并采取了不同解决方案。

### 5.1 问题普遍性

| 平台 | 问题表现 | 证据 |
|:-----|:---------|:-----|
| **Claude Code** | 长对话后"忘记"CLAUDE.md规则，工具权限被稀释 | Anthropic 承认 context rot，200K 窗口设定 167K 阈值触发自动压缩 |
| **OpenAI Codex** | 长程对话 cost quadratic 增长，context window 溢出 | OpenAI 发布《Unrolling the Codex Agent Loop》专文讲解 |
| **Cursor** | .cursorrules 在长对话后不被遵守，AI "降智" | 社区普遍反馈，Cursor 将 rules 定义为"长期隐式 system prompt"但承认长对话会稀释 |
| **Popwave (OpenClaw)** | 3 轮后 skill 读取率降至 0-3% | 本文 435 runs 数据分析 |

### 5.2 各平台解决方案

**Claude Code：静态/动态分层 + Prompt 末尾注入**

System Prompt 分 10 层组装，第 6 层 `SYSTEM_PROMPT_DYNAMIC_BOUNDARY` 是分水岭：

| 层 | 内容 | 特性 |
|:---|:-----|:-----|
| 1-5 静态 | 角色定义、输出风格、系统规则、任务准则、操作安全 | 可缓存、跨会话不变 |
| 6-10 动态 | 环境上下文、Git 状态、**CLAUDE.md**、运行时配置 | 每次重新注入 |

关键设计：CLAUDE.md 放在步骤 9（Prompt 末尾），利用 Recency Effect 获得最强注意力。静态部分可缓存降成本，动态部分每轮重新注入保证不被遗忘。

**OpenAI Codex：自动 Compaction + Harness/Model 职责分离**

- 自动压缩：`auto_compact_limit` 超阈值时触发 `/responses/compact`，用户无感知
- 核心哲学：**让模型只做推理，基础设施做其他所有事**——模型不需要"记住"之前发生了什么，那是 harness 的职责；模型不需要"决定"何时压缩，那也是 harness 的职责
- Prompt 缓存让 cost 从 quadratic 降为 linear

**Cursor：每轮注入 + 路径匹配**

- `.cursorrules` 和 project rules 作为"长期隐式 system prompt"
- 按路径匹配注入不同 rules（`cursor/rules/` 目录）
- 每次新对话都重新注入 rules

### 5.3 平台能力对比

| 维度 | Claude Code | Codex | Cursor | Popwave (OpenClaw) |
|:-----|:-----------|:-----|:-------|:-------------------|
| 静态/动态分层 | 10 层，分界线隔离 | system>developer>user 优先级 | rules + memory | **有分层**：bootstrap files + 工具结果独立预算 |
| 规则注入位置 | Prompt 末尾（Recency 最强） | developer 指令层 | .cursorrules | Bootstrap files 会话启动时加载（单文件 12K 字符上限，总计 60K） |
| 自动压缩 | 167K 阈值 LLM 摘要 | auto_compact_limit | 手动 /compact | **有**：历史超上下文 50% 触发剪枝 + LLM 多轮摘要 |
| 工具结果限制 | 25K tokens / 50K 字符 | — | — | 16K 字符或上下文 30%（取较小值） |
| 子 Agent 隔离 | 空白对话 + fork 模式 | — | — | 全新隔离会话，无父转录 |
| Harness 管理 | ✅ harness 管 context | ✅ harness 管 context | ✅ | ✅ harness 管 context |

### 5.4 OpenClaw 已有的 Context 管理机制

根据 OpenClaw 源码（`D:\popwave\resources\app.asar.unpacked\`）和技术分析，OpenClaw 继承自 Pi (pi-mono) 的上下文管理架构，具备完整的 harness 层 context 管理：

**1. 文件读取截断（继承 Pi）**
- 硬性限制：单文件 2,000 行或 50KB（先到为准）
- 超限时头部截断，附继续提示 `[Showing lines 1-2000 of 50000. Use offset=2001 to continue.]`

**2. Bootstrap files 限制（OpenClaw 独有）**
- 单文件不超过 12,000 字符，总计不超过 60,000 字符
- 超限时 75% 头部 + 25% 尾部，保留首尾舍弃中间

**3. 工具结果独立预算**
- 单工具结果上限：16,000 字符或上下文窗口 30%（取较小值）
- 超限时保留开头，若尾部含"重要"内容（错误/JSON 闭合/摘要关键词）则切换头+尾模式

**4. 会话剪枝（Session Pruning）**
- 历史超过上下文窗口 50% 时触发
- 将历史分为等量 Token 块，丢弃最旧块
- 丢弃内容经 LLM 多轮摘要后作为合成消息前置
- 通过 `repairToolUseResultPairing` 修复孤儿工具结果

**5. 预压缩刷新**
- 历史消失前静默执行一次 Agent 轮次，将状态持久化到内存文件

**6. 工具结果非破坏性剪枝**
- 5 分钟缓存 TTL，软修剪后硬清除，保护持久对话同时释放上下文

### 5.5 真正的问题：机制存在但 Skill 注入不在管理范围内

OpenClaw 有完整的 context 管理机制，但 **skill 文件的注入不在这些机制覆盖范围内**：

| OpenClaw 已管理 | OpenClaw 未管理（skill 问题所在） |
|:----------------|:----------------------------------|
| 文件读取大小（2K 行/50KB 截断） | SKILL.md 是否被 agent 重新读取 |
| 工具结果预算（16K 字符） | Skill 版本变化后是否重新注入 |
| 历史剪枝（50% 阈值 + LLM 摘要） | 压缩后是否重新注入当前 skill 的 SKILL.md |
| Bootstrap files 总量（60K 字符） | Skill step 文件的按需注入 |
| 预压缩状态刷新 | 压缩后 step 进度是否保留 |

**核心差距不是"没有 harness"，而是"harness 管的是通用 context，不管 skill 生命周期"。** OpenClaw 的 compaction 会在历史超 50% 时触发摘要，但摘要后不会重新注入 skill 文件——agent 拿到的是对话历史的摘要，不是 skill 原文。同样，bootstrap files 限制只管会话启动时的加载，不管后续轮次中 skill 是否需要重新读取。

## 六、解决方案：把弱保障提升为强保障

### 6.1 核心思路

问题本质：强保障只覆盖元 skill SKILL.md，下游 skill 的所有文件都是弱保障。

解决方向：**把下游 skill SKILL.md + 当前 step 文件从弱保障提升为强保障。**

| 文件 | 当前保障 | 目标保障 |
|:-----|:---------|:---------|
| 元 skill SKILL.md（expert-writer） | 强（host 硬注入） | 强（不变） |
| 下游 skill SKILL.md（plot/create/seed） | 弱（agent 主动读） | **强（host 硬注入）** |
| 当前 step 文件 | 弱（agent 主动读） | **强（host 硬注入）** |
| references / 模板 | 弱（agent 主动读） | 弱（保持，非关键） |

### 6.2 平台层方案（需要 OpenClaw 支持）

**扩展 host 层的强注入范围**，从"仅元 skill SKILL.md"扩展到三层：

1. **元 skill SKILL.md**：每次 run 强制注入（已有）
2. **下游 skill SKILL.md**：host 层读取元 skill SKILL.md 中的路由表，把当前激活的下游 skill SKILL.md 也强制注入
3. **当前 step 文件**：host 层跟踪 step 进度，把当前 step 文件强制注入

compaction 后重注入这三层文件，类似 Claude Code 压缩后恢复最近 5 个文件的做法。

### 6.3 Skill 层退路方案（平台层不改时可用）

如果 OpenClaw 不支持扩展强注入，在 skill 层面做降级处理：

**把下游 skill SKILL.md 的核心红线内嵌到 expert-writer SKILL.md 的路由表中。**

当前 expert-writer SKILL.md 路由表写的是：
```
| Step 1 卷纲 | steps/step-1-volume-anchor.md | templates/卷纲-模板.md | 卷纲/卷N-卷纲.md |
```

改为内嵌核心指令：
```
| Step 1 卷纲 | [内嵌] plot SKILL.md 红线：禁止卷纲写beat/禁止跳过选种子/禁止未通过质量门标记formal。执行入口：1a定位→1b燃料台→1c幕序列→1d种子池→1e高潮点→1f确认门。 | templates/卷纲-模板.md | 卷纲/卷N-卷纲.md |
```

这样即使 agent 不读 plot SKILL.md，也能从 expert-writer SKILL.md（强保障）中拿到 plot 的核心红线和执行入口。代价是 expert-writer SKILL.md 体积增加，但每条路由只多 2-3 行，总体可控。

### 6.4 方案选择

| 方案 | 改动方 | 效果 | 代价 |
|:-----|:-------|:-----|:-----|
| 6.2 平台层 | OpenClaw 代码 | 根治：所有下游 skill 文件强保障 | 需要平台开发 |
| 6.3 Skill 层退路 | 我们自己 | 缓解：核心红线强保障，但 step 细节仍弱保障 | expert-writer SKILL.md 膨胀 |
| 6.2 + 6.3 组合 | 双方 | 根治 + 过渡 | 短期用 6.3，长期等 6.2 |

**推荐**：先用 6.3 作为短期方案落地（我们可控），同时推动 6.3 向 6.2 演进。

## 七、与历史诊断的关联

| 日期 | 诊断 | 结论 |
|:-----|:-----|:-----|
| 2026-06-08 | [01-Paopao上下文与Skill加载](01-20260608-Paopao上下文与Skill加载-问题分析.md) | 首次发现 skill 加载不稳定 |
| 2026-06-26 | [14-v3管线28章质量诊断](14-20260626-v3管线28章质量诊断与v3.1优化-问题分析.md) | 发现 agent 跳过 SKILL.md 和 step 文件 |
| 2026-07-01 | 本文 | 跨项目量化确认：3 轮后 skill 读取率降至 0-3%；多平台对比确认需 harness 层解决 |

---

*本分析基于 14 个项目 435 个 runs 的 events.jsonl 和 input.json 数据。token 数据从 events.jsonl 中通过正则提取 cacheRead/promptTokens 字段获得。skill 读取检测通过搜索 events.jsonl 中的 readFile 工具调用和 SKILL.md/step-N 路径引用实现。*
