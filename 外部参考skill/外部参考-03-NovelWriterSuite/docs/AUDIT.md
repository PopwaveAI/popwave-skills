# 代码级评估报告

> README 和实现的真实差距。每个项目按"宣传声称"vs"实际能力"打分。
> 评分：A=production-grade / B=可用但有限 / C=能跑但浅 / D=只是骨架

---

## 1. novel-writer — 评分 **B-**

**README 宣传**："强制验证 + 检查点 + 进化机制 + 优秀网文10大标准审查"

**代码真相**（已读完 7 个 Python 脚本共 1320 行）：

| 模块 | 实际实现 | 真实评价 |
|---|---|---|
| `checkpoint.py` (214 行) | 用 JSON 序列化几个关键文件做快照 | ✅ 简洁可用，**可直接借鉴设计** |
| `validate_step.py` (336 行) | 步骤检查（文件存在性、字数下限、字段存在性） | ✅ 跑得通，但全是 `file.exists()` 级别检查 |
| `validate_chapter_quality.py` (308 行) | **10 维评分，全部是正则匹配** | ⚠️ **能识破"开头有问号 → 算有钩子"，骗不过它的章节也骗得过它**。每个维度满分 2 分用 4-5 个正则计算，没有 LLM 判断 |
| `character_check.py` (162 行) | 用百家姓正则提取人名 → 跟角色卡对照 | ⚠️ 中文人名识别精度堪忧（已硬编码"陛下/小子/什么"等过滤词） |
| `validate_chapter_outline.py` (112 行) | 章纲字段存在性检查 | ⚠️ 浅 |
| `validate_outline_confirmation.py` (68 行) | 检查 status.md 有没有"已确认"字样 | ⚠️ 浅 |
| `workflow.py` (120 行) | 状态机轮转工具 | ⚠️ 浅 |

**真实价值**：
- ✅ **领域知识库值钱**（SKILL.md 里的"章节四大原则"、"文风类型表"、"禁用AI句式表"是几个月写作经验沉淀，自己写要重新填）
- ✅ **checkpoint.py 设计简洁**，可直接移植
- ❌ **质量验证脚本是启发式 fig leaf**——它的作用更像"防止 LLM 写得过于离谱"，不是真的能保证质量
- ❌ **无 license**，任何代码移植都有版权风险

**借鉴策略**：复制其 prompt 中的**规则列表**（用文字形式重写），不要复制其 Python 代码。

---

## 2. story-skills — 评分 **C**（结构良好但能力薄弱）

**README 宣传**："End-to-end story writing powered by markdown"

**代码真相**（5 个 SKILL.md + 完整 example vault）：

| 模块 | 实际实现 | 真实评价 |
|---|---|---|
| 5 个 SKILL.md | 纯 prompt 模板，无任何脚本 | ⚠️ **就是 5 个对话流程的写法说明**，没有任何验证、强制、记忆管理 |
| Example vault `the-last-ember/` | 真实的 4 个角色 + 2 地点 + 1 魔法系统 + 1 卷 + 1 章 | ✅ **数据模型示例非常清晰**（看一眼就能学会） |
| `.claude-plugin/` | 标准 Claude Code plugin 元信息 | ✅ 即插即用 |
| `references/` 模板 | 角色/地点/弧/系统的 markdown 模板 | ✅ 结构干净 |

**真实价值**：
- ✅ **唯一能直接 fork 的项目**（MIT）
- ✅ **数据结构是教科书级别的 Obsidian-friendly**（frontmatter 双向链 + kebab-case + `_index.md` 注册表）
- ❌ **核心写作流程很弱**——chapter-writing skill 只有"读上下文 → 写章纲 → 等用户确认 → 写正文 → 更新引用"五步，没有任何质量保证、写法控制、记忆策略
- ❌ **没有针对中文/网文的任何优化**

**借鉴策略**：**fork 它的骨架**，把领域逻辑（中文规则、文风学习、网文校验）填进去。它是个好框架但是个空壳。

---

## 3. inkos — 评分 **A**（远超 README 宣称）

**README 宣传**："33-dimension audit, hook ledger, multi-agent pipeline"

**代码真相**（核心 packages/core 有 35 个 agent + 工具文件）：

| 模块 | 实际实现 | 真实评价 |
|---|---|---|
| `hook-ledger-validator.ts` (277 行) | **完整的"hook 账"解析器 + 揭1埋1规则强制 + 关键词回声检测** | ✅✅ **真正的工程作品**。引用了番茄文章10、徐二家的猫等具体写作流派理论 |
| `ai-tells.ts` (161 行) | **4 维统计学结构性 AI 检测**：段落长度变异系数<0.15 / 套话密度>3每千字 / 同转折词≥3次 / 列表式开头≥3句 | ✅✅ **统计驱动、可解释、双语**。每个维度都有具体阈值 + 改进建议 |
| `post-write-validator.ts` (873 行) | **十几条硬规则**："不是…而是…"句式禁、破折号禁、转折词密度上限、疲劳词每章≤1次、元叙事禁、分析报告术语禁（"核心动机/锚定效应"等）、说教词禁、全场震惊式集体反应禁 | ✅✅ **从中文网文批评文化中提炼的具体规则**，远超 README 宣称 |
| `continuity.ts` (824 行) | 连贯性检查 | ✅ 未细读但规模可信 |
| `style-analyzer.ts` (93 行) | 风格分析 agent | ⚠️ 小，可能只是 prompt 包装 |
| 35 个 agent 文件 | 完整的多 agent 管线（planner/composer/writer/observer/reflector/normalizer/auditor/reviser/...） | ✅ 真实的 LangGraph 风格管线 |

**真实价值**：
- ✅✅ **代码质量是研究对象**（typed, well-commented, 引用具体文学理论）
- ✅✅ **post-write-validator 的硬规则表 + ai-tells 的统计学方法可直接对应中文化重写**
- ❌ **AGPL-3.0**：任何"代码改编"都会污染我们项目；只能**完全独立重新实现**算法

**借鉴策略**：把 inkos 当**论文**读，不当代码用。提取它的**规则 + 算法**，用 Python/markdown 自己实现。具体可借鉴：
1. hook-ledger 的"揭1埋1"硬底线 + 关键词回声证据检查
2. ai-tells 的 4 个统计维度（段落变异系数、套话密度、转折重复、列表化结构）
3. post-write-validator 的中文硬禁令清单（"不是…而是…"、破折号、转折词、元叙事、报告术语）

---

## 4. AI-Novel-Writing-Assistant — 评分 **A-**（概念深、规模大、不易直接用）

**README 宣传**："写法引擎、自动导演、整本生产主链"

**代码真相**（写法引擎 = 20 个 service 文件 + 3 份共 2541 行设计文档）：

| 模块 | 实际实现 | 真实评价 |
|---|---|---|
| `docs/design/style-engine-v1.md` (1001 行) | **写法引擎完整设计文档**：描述层/执行层分离、源统一/应用统一、可绑定可组合可分层、模板/规则分离、检测/修正闭环 | ✅✅ **是行业级 PRD 水准**。比代码本身更有价值 |
| `docs/design/style-engine-prompt-compiler-v1.md` (1021 行) | Prompt 编译器设计 | ✅✅ |
| `StyleCompiler.ts` (353 行) | **真实的规则→prompt 编译器**：权重 0.85+="must keep" / 0.65+="preferred" / else="when natural"；anti-AI 三态 encourage/forbidden/watch | ✅✅ 工程实现完整 |
| `StyleProfileService.ts` (911 行) | 写法档案 CRUD + 绑定管理 | ✅ 规模真实 |
| `styleExtraction.ts` (355 行) | 从样本中提取写法特征 | ✅ |
| 18 个其他 styleEngine service | 包括 anti-AI 规则服务、检测服务、生成服务、改写服务、运行时解析器、绑定服务、推荐服务等 | ✅ 模块化清晰 |
| 章节生产链 | 完整的"导演→项目设定→宏观规划→角色准备→卷骨架→拆章→章节执行→质量修复"流水线 | ✅ 但是嵌在 Electron 全栈里，剥不出来 |

**真实价值**：
- ✅✅ **设计文档本身就是 800 字的"功能 2 怎么做"答案**，我们直接搬概念即可
- ✅ "写法层级可绑定"（全书/卷/章/角色视角/任务）是我们想不到的精妙
- ✅ "encourage/forbidden/watch" 三态 anti-AI 比 novel-writer 的"禁/不禁"二态更细
- ❌ **代码是 TypeScript + Prisma + LangGraph 全栈架构**，不能搬到 skill
- ❌ **License = "Other"**，需查 `LICENSE` 文件——保守起见只搬概念

**借鉴策略**：**精读 3 份设计文档**，把"写法引擎"的概念用 markdown skill + Python 抽取脚本重新实现。AI-NWA 是"概念金矿"，不是代码源。

---

## 5. NovelClaw — 评分 **B**（学术项目，但实际能用）

**README 宣传**："Dynamic-memory-first collaborative AI framework"

**代码真相**（`memory_system.py` 910 行）：

| 模块 | 实际实现 | 真实评价 |
|---|---|---|
| `MemorySystem.CLAW_BANKS` | **16 个独立记忆库**：session_profile / language_profile / user_preferences / task_briefs / story_premise / style_guide / chapter_briefs / scene_cards / entity_state / relationship_state / world_state / continuity_facts / tool_observations / decision_log / revision_notes / working_set | ✅ **记忆分类比 novel-writer 完整得多**——尤其 `tool_observations / decision_log / revision_notes` 是其他项目没有的"过程性记忆" |
| Vector store | ChromaDB + 索引 + 旧库迁移逻辑 | ✅ 真实实现，有"生产成熟度迹象"（迁移代码） |
| FastAPI workspace | Docker 部署、web UI、run inspection、storyboard | ⚠️ 全栈 web app，不能搬 |

**真实价值**：
- ✅ **16 银行的记忆分类法可直接抄到 vault 结构里**（每个 bank = 一个 markdown 文件或目录）
- ✅ 配套学术论文（CoLong-Idea-Studio），可作为理论参考
- ❌ 实际"dynamic"在哪里看不出来——更像 16 个分类的静态 RAG，不像自适应学习
- ❌ FastAPI app 不可移植

**借鉴策略**：**直接抄 16 个 bank 的命名 + 分类**，作为我们 `.memory/` 目录的子分类。

---

## 终极结论

```
                Strong code              Weak code
                +----------------+------------------+
   MIT (safe)   | story-skills C | NovelClaw B      |
                | (空壳但结构好)  | (架构概念可抄)    |
                +----------------+------------------+
   AGPL/无/Other| inkos A        | novel-writer B-  |
                | AI-NWA A-      | (规则可抄,代码弃) |
                | (要重写算法)    |                  |
                +----------------+------------------+
```

**修正后的方案**：

| 我们的 skill | 主借鉴对象 | 借鉴形式 |
|---|---|---|
| `novel-init` | story-skills/story-init | **fork** |
| `novel-brainstorm` | novel-writer SKILL.md 文风/视角清单 | 概念重写 |
| `novel-worldbuilding/characters/plot` | story-skills 三个对应 skill | **fork** 改中文 |
| `novel-style-engine` | **AI-NWA 写法引擎设计文档** | 完全按设计文档自己实现 |
| `novel-memory` | NovelClaw 16 banks 命名 + novel-writer memory-load 流程 | 抄分类 + 重写策略 |
| `novel-chapter` | inkos 写作管线概念（planner→writer→observer→auditor） | 简化版自己实现 |
| `novel-review` | **inkos post-write-validator + ai-tells + hook-ledger-validator** | 算法独立重写为 Python |
| `novel-adapt` | bybren fountain 模板 | 几乎全自己写 |

**关键差别**：原 DESIGN.md 把 inkos 标为 "AGPL 谨慎借鉴"，AUDIT 后发现它的**规则和算法本身是金子**，应该作为 review skill 的**首要重写目标**（不是 novel-writer）。novel-writer 的章节质量评分是 regex 启发式，inkos 的 ai-tells/post-write-validator 是统计学+硬规则的工程作品。

---

## 我对原 DESIGN.md 的修正项

1. **novel-review skill**：原本"借鉴 novel-writer 10 维评分"——改为"重写 inkos 的 ai-tells 4 维统计 + post-write-validator 硬规则表 + hook-ledger 验证算法"。inkos 的代码深度碾压 novel-writer。
2. **novel-style-engine skill**：原本"借鉴 AI-NWA 概念"——改为"严格按 AI-NWA 的 3 份设计文档实现，特别是描述层/执行层分离 + 三态 anti-AI"。
3. **.memory/ 目录结构**：原本只有 4 个子目录——改为**采用 NovelClaw 的 16 bank 分类**作为子目录命名。
4. **优先级调整**：写法引擎从 Phase 2 提到 Phase 1 末——因为它是真正的差异化，比单纯校稿更重要。

---

## 后续动作建议

1. 读完 inkos 的 `continuity.ts` (824 行) — 是否还有更多可借鉴的连贯性检查规则
2. 读完 AI-NWA 的 `style-engine-prompt-compiler-v1.md` (1021 行) — 编译器细节
3. 查 AI-NWA `LICENSE` 文件确认是否真的不可商用
4. 在 _research/ 跑一次 novel-writer 真实流程（写一章），看脚本的实际拦截力度
