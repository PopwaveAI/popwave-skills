# Superpowers × novel-agent-pro 融合分析

> 日期：2026-05-20
> 背景：安装了 obra/superpowers v5.1.0（全栈 AI 编程方法论），对 novel-agent-pro v2.1（网文写作引擎）做交叉分析，评估哪些模式可以移植/借鉴

---

## 0. 两种 Skill 体系的底层差异

| 维度 | Superpowers | novel-agent-pro |
|------|-------------|-----------------|
| **领域** | 软件开发 | 网文创作 |
| **核心约束对象** | AI 代理的行为流程 | AI 代理的创作内容 |
| **铁律性质** | **过程铁律**（必须先做 A 才能做 B） | **内容铁律**（世界观不可违反的规则） |
| **Skill 触发** | 系统级强制（1% rule + `Skill` 工具） | 无系统级触发，依赖 LLM 自主识别 |
| **错误检测** | Red Flags（AI 的理性化自查表） | 无等价机制 |
| **版本体系** | 单一版本号（无子模块版本） | 双版本矩阵（主版本 + 子 Skill 版本） |
| **项目一致性** | 有 CLAUDE.md / AGENTS.md 全局引导 | 有 skill-mapping.yaml + VERSION.md |
| **子代理使用** | 核心模式（每任务新子代理 + 两轮审查） | 少量使用（market-test） |
| **胶水层** | 无——依赖 skill 工具自身 | 有 glue/ 层（路径解析、schema 校验） |
| **平台适配** | 8 个平台（Claude/Codex/Cursor/Gemini 等） | 单一平台（WorkBuddy/Claude Code） |

---

## 1. 高价值融合项（建议优先引入）

### 1.1 「过程铁律」机制（Hard Gate + Iron Law 模式）

Superpowers 用了两种强力约束：

**HARD-GATE**（硬闸门）：
```html
<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project,
or take any implementation action until you have presented a design and the
user has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>
```

**Iron Law**（铁则）：
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
NO SKILL WITHOUT A FAILING TEST FIRST
```

#### 现状：novel-agent-pro 目前只有「内容铁律」（世界观设定不可违反），没有「过程铁律」（写作工序不可跳过）。

#### 融合建议：

在核心串联点加入过程铁律，示例：

```markdown
<HARD-GATE>
不要在没有经过剧情架构设计的情况下直接开始写章节正文。
如果用户要求"直接写一章"，先检查是否存在已批准的幕纲（act-XX.yaml）。
如无幕纲 → 调 skill-plot-architecture 先设计当前幕的爽点分布。
如有幕纲 → 确认是"本章设计"的素材已就位（幕纲切片 + 全局摘要 + 角色状态）。
</HARD-GATE>
```

**建议新增 4 条写作过程铁律：**

| 铁律 | 来源 | 写作版 |
|------|------|--------|
| NO CHAPTER WITHOUT ACT OUTLINE | TDD 的 NO CODE WITHOUT TEST | 没有幕纲切片不准写章节正文 |
| NO ACT WITHOUT PAYOFF MAP | 同上 | 没有爽点分布不准设计幕 |
| NO COMPLETION WITHOUT FRESH CHECK | verification-before-completion | 说"写好了"之前必须跑 5 项自检 + 更新 global_summary |
| NO FIX WITHOUT ROOT CAUSE | systematic-debugging | 审稿发现问题必须先定位根因再改 |

---

### 1.2 Red Flags 表（AI 理性化自查）

Superpowers 在 `using-superpowers` 里有一张 Red Flags 表，列出 AI 可能有的"理性化借口"：

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I remember this skill" | Skills evolve. Read current version. |

#### 融合建议：
在 `novel-agent-pro` 的入口层（skill-mapping.yaml 或顶层 README）加一张网文版 Red Flags 表：

```markdown
| 想法 | 真相 |
|------|------|
| "这章很简单，直接写就行" | 没有幕纲切片直接写 = 盲写。先去调剧情架构。 |
| "我先收集下素材" | skill 告诉你怎么收集。先检查当前在哪个阶段。 |
| "之前写过类似的，照搬就行" | 每章的情绪曲线和爽点不一样。调 emergent-writer 重新组装上下文。 |
| "这章不用自检" | 每章都自检。不跑自检就声称完成了 = 谎报。 |
```

---

### 1.3 系统级 Skill 触发机制

Superpowers 的 `using-superpowers` 是整个系统的开关：

```
1. 用户发消息 → 代理收到
2. 检查是否有 skill 适用（1% rule）
3. 有 → 调 Skill 工具
4. 检查该 skill 是否有 checklist → 创建 TodoWrite
5. 严格按照 skill 执行
```

#### 现状：novel-agent-pro 没有等价机制。AI 收到"写一章"指令时，依赖自身判断该做什么。

#### 融合建议：
在 novel-agent-pro 顶层新增一个 `using-novel-agent.md`（或融入已有 `skill-mapping.yaml`），定义阶段转换规则：

```
用户说"开新书"         → 检查：已有项目骨架？无 → 调 skill-project-bootstrap
用户说"写一章"         → 检查：已有幕纲切片？无 → 调 skill-plot-architecture
用户说"写 ch005"      → 检查：current_act 数据就绪？→ 调 skill-emergent-writer
完成一章               → 自动：更新 global_summary + 更新角色状态
用户说"审稿"          → 检查：已有正文？→ 调 skill-market-test
```

这个机制可以让 AI 严格按流水线走，不会跳步或走错方向。

---

### 1.4 子代理 + 两轮审查模式（subagent-driven-development）

Superpowers 的 SDD 流程：

```
① 派发实现子代理（指定任务 + 上下文）
② 实现子代理完成任务、测试、提交、自审
③ 派发规格审查子代理（subagent → 检查是否匹配 spec）
   └─ 不符合 → 退回实现子代理修复
④ 派发代码质量审查子代理（subagent → 检查代码质量）
   └─ 不符合 → 退回实现子代理修复
⑤ 任务完成
```

#### 现状：novel-agent-pro 的 market-test 用了子代理，但 pipeline 核心流程（emergent-writer）是同一个会话内串行完成的。

#### 融合建议：
应用到高成本节点：

1. **拆书场景**：主代理负责决策（选模式A/B/C + 定方向）→ 子代理负责执行（真实跑拆分管线）→ 主代理审结果
2. **市场验证**：已有 market-test 的子代理模式，但可以加强"两轮审查"概念——先审"是否符合品类常识"，再审"赛道对标是否到位"
3. **批量写作**：主代理准备上下文 → 子代理1写 ch021 → 子代理2写 ch022（并行）→ 主代理统一汇总自检

---

## 2. 中度价值（可融入现有逻辑）

### 2.1 Bite-Sized Task 分解粒度

Superpowers 的 plan 粒度是 2-5 分钟/步：
```
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code" — step
```

#### 写作版建议：
emergent-writer 目前是"一条 prompt 一次生成一整章"。可以考虑拆得更细：

```
① 组装上下文（读幕纲切片 + global_summary + character_state）
② 写初稿（LLM 生成 1500-2000 字）
③ 跑 5 项自检
④ 如有问题：定位根因 + 局部修复
⑤ 更新 global_summary（脚本执行）
⑥ 更新 character_state（脚本执行）
⑦ 埋下一章钩子
```

每步都很小、可验证、可独立回退。如果初稿自检不过，不需要重写整章，定位到具体问题修就行。

### 2.2 Verification-Before-Completion（声称完成前必须验证）

Superpowers 的铁律：「NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE」
也就是说，在当前对话里没有跑过验证命令，就不能说"搞定了"。

#### 写作版建议：
emergent-writer 现在有 5 项轻量自检（已集成），但缺一个检查清单式的完工声明：

```
✅ 5 项自检全部通过
✅ global_summary 已更新
✅ character_state 已更新
✅ 下一章钩子已写入幕纲
```

AI 在说"这章写好了"之前，必须先跑这 4 项检查并报告结果。

### 2.3 Finishing-a-Development-Branch（完成里程碑后的结构化收尾）

Superpowers 处理"做完了一个功能分支"：
```
① 跑全量测试验证
② 检测环境（当前分支、是否有未提交）
③ 展示选项：merge / PR / 保留 / 丢弃
④ 执行选择
⑤ 清理 worktree
```

#### 写作版建议：
对应"写完一卷"或"写完一个幕"后的收尾流程：

```
① 跑 market-test 三层检视（品类常识 + 赛道对标 + 自设承诺）
② 更新全局摘要（反映全幕进展）
③ 检查伏笔回收待办列表
④ 展示选项：继续写下一幕 / 回头修前面 / 发书前验证
```

---

## 3. 低价值/不适用的项目

| Superpowers Skill | 不适用的原因 |
|-------------------|-------------|
| **test-driven-development** | 写作不写测试。RED-GREEN-REFACTOR 循环不适用于小说创作。 |
| **using-git-worktrees** | 网文不需要多分支并行开发。git 只用于历史版本管理。 |
| **systematic-debugging** | 写作的"缺陷"（读者体验问题）不是能重现的 bug。审稿发现的问题需要用读者洞察去判断，不是 root-cause-tracing。 |
| **writing-skills** | novel-agent-pro 已有自己的 skill 编写方法论，且 skill 不是通过 TDD 验证行为（而是通过实际写作效果验证）。 |

---

## 4. 推荐实施路线

### Phase 1：文本级融合（改动最小，立即可做）

| 任务 | 文件 | 工作量 |
|------|------|--------|
| 在 3 个核心 SKILL.md 头部加 `<HARD-GATE>` 硬闸门 | `skill-plot-architecture` `skill-emergent-writer` `skill-market-test` | ~30分钟 |
| 在 `skill-emergent-writer` 尾部加自检后完工声明模板 | `skill-emergent-writer/SKILL.md` | ~15分钟 |
| 在 `skill-mapping.yaml` 加 Red Flags 表 | `skills/skill-mapping.yaml` | ~20分钟 |

### Phase 2：流程级融合（需要设计+测试）

| 任务 | 工作量 |
|------|--------|
| 设计 `using-novel-agent.md`（写作版 trigger 映射） | ~1天 |
| emergent-writer 拆成可验证的 bite-sized 步骤（5-7步） | ~0.5天 |
| 完工 4 项检查自动化脚本（检查 global_summary + character_state 是否最新） | ~1天 |

### Phase 3：架构级融合（长期）

| 任务 | 说明 |
|------|------|
| 子代理 SDD 模式在批量写作场景落地 | 并行写多章 + 两轮审查 |
| 卷完成收尾流程标准化 | 整合 finishing-a-development-branch 模式 |
| 过程铁律入库 | 把 4 条写作过程铁律写到 constitution.yaml 的 process_rules 段 |

---

## 5. 关键差异总结图

```
Superpowers (软件开发)
┌─────────────────────────────────────────────┐
│ ① brainstorming     ← HARD-GATE: 不写代码   │
│ ② using-git-worktrees                        │
│ ③ writing-plans     ← bite-sized 拆任务      │
│ ④ subagent-driven-dev ← 子代理+两轮审查      │
│ ⑤ test-driven-dev   ← 铁律: 先失败测试       │
│ ⑥ requesting-review  ← 子代理互审            │
│ ⑦ verification       ← 铁律: 先验证再声称    │
│ ⑧ finishing-branch   ← 结构化收尾            │
└─────────────────────────────────────────────┘

novel-agent-pro (网文写作) 可嫁接点
┌─────────────────────────────────────────────┐
│ ① skill-project-bootstrap                    │
│    ← 加 HARD-GATE: 不允无 PRD 直接开写       │ ← 新品
│ ② skill-opening-arc                          │
│    ← 加 过程铁律: 黄金三章不走 normal 流程     │ ← 新品
│ ③ skill-plot-architecture                    │
│    ← 加 HARD-GATE: 不写无幕纲的章             │ ← 新品
│ ④ [子代理批量写作]  ← 借鉴 SDD 模式           │ ← 新品
│ ⑤ skill-emergent-writer                      │
│    ← bite-sized 步骤拆分                      │ ← 优化
│    ← 完工声明的 4 项验证                       │ ← 新品
│ ⑥ skill-market-test                          │
│    ← 子代理两轮审查加强                        │ ← 优化
│ ⑦ 卷完成收尾流程                              │ ← 新品
└─────────────────────────────────────────────┘
```

---

## 6. 一句话结论

**novel-agent-pro 的内容功力已经很强（L1-L3 设定、幕纲设计、爽点体系），但缺的是 Superpowers 那一套"过程约束"——用 HARD-GATE、Iron Law、Red Flags 这些机制让 AI 严格按工序走，防止跳步和走捷径。**

最值得优先落地的 3 件事：
1. **HARD-GATE**：3 个核心 SKILL.md 加过程铁律
2. **Red Flags**：AI 理性化自查表
3. **完工验证**：声称完成前的 4 项必检
