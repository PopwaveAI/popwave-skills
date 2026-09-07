# Novel Suite —— 写作 skill 套件设计图 v2.0

> 面向中文长篇小说创作的 Claude Code skill 套件。一本小说 = 一个 Obsidian vault / git 仓库。
>
> **本设计基于代码级审计**（见 `AUDIT.md`），融合 5 个候选项目的最强模块，全部独立重写。

---

## 0. 设计原则

1. **借鉴最强，全部重写**：从 5 个项目中挑出每个模块的最佳实现，独立重写为我们的 skill + Python 脚本。不抄代码，抄设计和算法。
2. **Markdown is source of truth**：所有长期记忆是人能读、能编、可 git diff 的 markdown。
3. **Scripts only for verification**：Python 只做客观可验证的检查（字数、文件存在、统计规律、硬规则匹配）。主观判断（情节是否合理、文风是否到位）交给 LLM。
4. **No vector DB at v0.1**：先用文件检索 + frontmatter tag 过滤 + 章节摘要。跑通后再视需要加向量层。
5. **Skill 之间通过文件系统通信**，不通过运行时参数传递。
6. **Obsidian-first**：所有产物兼容 Obsidian vault，可拖进去直接看 graph view。

---

## 1. 模块借鉴矩阵

| 我们的 skill / 模块 | 借鉴自 | 借鉴的具体东西 | 我们独立重写实现 |
|---|---|---|---|
| **Vault 骨架** | story-skills | kebab-case + frontmatter 双向链 + `_index.md` 注册表 + 每实体一文件 | 加中文路径、Obsidian vault 检测、可选 git init |
| **领域规则库** | novel-writer SKILL.md | 章节四大推进原则、文风五大类型表、禁用 AI 句式清单、章节权重标记（⭐~⭐⭐⭐⭐⭐） | 用 markdown reference 文件重写 |
| **写法引擎** | AI-NWA `docs/design/style-engine-*.md` | 描述层/执行层分离、源统一/应用统一、绑定层级（全书/卷/章/角色视角/任务）、anti-AI 三态（encourage/forbidden/watch）、检测/修正闭环 | 用 skill + Python 脚本实现，规模缩到 v0.1 |
| **校稿 ai-tells 统计层** | inkos `ai-tells.ts` | 4 维：段落长度变异系数<0.15 / 套话密度>3每千字 / 同转折词重复≥3次 / 列表式开头≥3句 | Python 重写，加汉字句长统计 |
| **校稿硬规则层** | inkos `post-write-validator.ts` | "不是…而是…"句式禁、破折号禁、转折词密度上限、疲劳词每章≤1次、元叙事禁、分析报告术语禁（"核心动机/锚定效应"等）、说教词禁、全场震惊集体反应禁 | Python 重写硬规则表 |
| **校稿 hook 账层** | inkos `hook-ledger-validator.ts` | 揭1埋1硬底线、关键词回声证据检查、open/advance/resolve/defer 四态语义、CJK 2-gram 关键词提取 | Python 重写，跟 plot/foreshadowing.md 对接 |
| **记忆库分类** | NovelClaw `memory_system.py` CLAW_BANKS | 16 bank 命名：session_profile / language_profile / user_preferences / task_briefs / story_premise / style_guide / chapter_briefs / scene_cards / entity_state / relationship_state / world_state / continuity_facts / tool_observations / decision_log / revision_notes / working_set | 用作 `.memory/` 子目录命名，v0.1 暂不全建（按需展开） |
| **检查点机制** | novel-writer `checkpoint.py` | JSON 序列化关键文件做快照、create/rollback/list/delete 四操作、按 milestone 触发 | Python 重写，路径可配置 |
| **写作流程编排** | inkos 多 agent 管线 | 概念：Planner → Composer → Writer → Observer → Auditor → Reviser 顺序 | 简化为 skill 间调用，不引入运行时 agent |
| **格式转换-剧本** | bybren `story-systems-template` | Fountain 标准格式 | skill + Python parser |
| **格式转换-分镜** | （无现成参考） | — | 全部原创 |

---

## 2. 总体架构

```
┌───────────────────────────────────────────────────────────┐
│              novel-suite (Claude Code Plugin)             │
│                                                           │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Skill 编排层（自然语言 → skill 调度）            │    │
│  └──────────────────────────────────────────────────┘    │
│                       │                                   │
│         ┌─────────────┼─────────────┐                    │
│         ▼             ▼             ▼                    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐           │
│  │ 创作 skills│ │ 写作 skills│ │ 产出 skills│           │
│  │ - init     │ │ - chapter  │ │ - adapt    │           │
│  │ - brain... │ │ - memory   │ │            │           │
│  │ - world... │ │ - review   │ │            │           │
│  │ - chars    │ │ - style    │ │            │           │
│  │ - plot     │ │            │ │            │           │
│  └─────┬──────┘ └─────┬──────┘ └─────┬──────┘           │
│        │              │              │                   │
│        └──────────────┼──────────────┘                   │
│                       ▼                                   │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Python 工程脚本层                                │    │
│  │  - checkpoint.py（快照/回滚 ← novel-writer）     │    │
│  │  - validate_structure.py（vault 结构合规）       │    │
│  │  - extract_style.py（写法特征提取 ← AI-NWA）     │    │
│  │  - compile_style.py（写法规则编译 ← AI-NWA）     │    │
│  │  - check_ai_tells.py（4 维统计 ← inkos）         │    │
│  │  - check_post_write.py（硬规则 ← inkos）         │    │
│  │  - check_hook_ledger.py（伏笔账 ← inkos）        │    │
│  │  - check_consistency.py（设定/人物一致性）       │    │
│  │  - to_screenplay.py（小说→fountain）             │    │
│  └──────────────────────────────────────────────────┘    │
│                       │                                   │
│                       ▼                                   │
│  ┌──────────────────────────────────────────────────┐    │
│  │  Vault 文件系统（Obsidian / git / 任何 md 编辑器）│    │
│  └──────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────┘
```

---

## 3. Vault 结构（你朋友实际操作的就是这个）

```
{书名}/                                  # 一本小说 = 一个 git repo（自动 git init）
│
├── story.md                             # ★ 故事圣经（顶层 frontmatter + 题材定位 + 30 章承诺）
├── status.md                            # ★ 当前状态唯一真相源
│
├── style/                               # 【功能 2：写法引擎 ★ 差异化核心】
│   ├── _index.md                        # 写法档案注册表
│   ├── samples/                         # 用户投喂的原文样本
│   │   ├── ref-001-{slug}.md            #   样本可带 frontmatter 标注来源
│   │   └── ref-002-{slug}.md
│   ├── features.md                      # 抽取出的特征池（每项可启用/停用/编辑权重）
│   ├── anti-ai.md                       # 反 AI 规则（三态：encourage/forbidden/watch）
│   └── compiled.md                      # 编译后注入 prompt 的最终约束
│
├── characters/                          # 【功能 3：记忆-结构化层】
│   ├── _index.md                        # 角色注册表 + 关系图谱 + 家族树
│   └── {name-kebab}.md                  # 每个角色一文件（frontmatter + 详情）
│
├── worldbuilding/
│   ├── _index.md
│   ├── locations/{place-kebab}.md
│   └── systems/{system-kebab}.md        # 力量/社会/科技/宗教...
│
├── plot/
│   ├── _index.md                        # 卷纲 + 主题追踪
│   ├── arcs/{arc-kebab}.md
│   ├── timeline.md
│   └── foreshadowing.md                 # 伏笔总表（hook 账：open/advance/resolve/defer）
│
├── chapters/
│   ├── _index.md
│   ├── ch-001.md                        # 单章：frontmatter + 章纲 + 正文 + hook 账
│   └── ...
│
├── deliverables/                        # 【功能 5：格式转换】
│   ├── novel.md / novel.docx
│   ├── screenplay.fountain
│   └── storyboard.md
│
└── .memory/                             # 【功能 3：记忆-过程层 ← NovelClaw 16 banks 启发】
    ├── checkpoints/                     # 检查点快照（JSON）
    ├── chapter-briefs.md                # 章节摘要（写新章前检索用）
    ├── scene-cards.md                   # 场景卡（重要场景索引）
    ├── entity-state.md                  # 实体当前状态（人在哪/有什么道具/受了什么伤）
    ├── relationship-state.md            # 关系当前状态（X 跟 Y 现在啥关系）
    ├── continuity-facts.md              # 一致性事实（已确立的设定细节）
    ├── decision-log.md                  # 作者重要决定的日志
    ├── revision-notes.md                # 用户修订意见累积（进化机制）
    └── tool-observations.md             # （v0.2+）工具调用记录
```

**Obsidian 适配**：
- 整个目录直接当 vault 打开
- frontmatter 的 `relationships / tags / location` 字段 → graph view 自动连线
- `_index.md` 可用 Obsidian dataview 插件自动维护（也支持手编）
- entity ID 用 kebab-case，跟 wiki link `[[name]]` 完全兼容

---

## 4. Skill 套件清单（10 个 skill）

| Skill | 触发短语 | 借鉴源 | 优先级 |
|---|---|---|---|
| **novel-init** | "开始写小说" / "新建项目" | story-skills 骨架 | P0 |
| **novel-brainstorm** | "讨论世界观" / "想剧情" | novel-writer 文风/视角清单 | P0 |
| **novel-worldbuilding** | "构建世界观" / "加地点" | story-skills/worldbuilding | P0 |
| **novel-characters** | "加角色" / "角色关系" | story-skills + novel-writer character_check + AI-NWA 动态角色资产 | P0 |
| **novel-plot** | "卷纲" / "伏笔" / "时间线" | story-skills/plot + novel-writer 四大原则 + inkos hook 账语义 | P0 |
| **novel-style-engine** ★ | "学这个文风" / "提取写法" | **AI-NWA 写法引擎设计文档** | P1 |
| **novel-memory** | （自动触发） | NovelClaw 16 banks + novel-writer memory-load | P0 |
| **novel-chapter** | "写第 X 章" / "继续写" | inkos 写作管线概念 | P0 |
| **novel-review** ★ | "校稿" / "审一遍" | **inkos ai-tells + post-write + hook-ledger** | P1 |
| **novel-adapt** | "转剧本" / "做分镜" | bybren fountain 模板 + 原创分镜模板 | P2 |

★ = 我们相对其他开源项目的**差异化模块**

**编排关系**：

```
novel-init ─→ novel-brainstorm ─→ novel-worldbuilding ─┐
                                                       ├─→ novel-plot ─→ novel-chapter ⇆ novel-memory
              novel-characters ──────────────────────┘                          ↑↓
                                                                          novel-style-engine
              novel-review（任何时候可手动触发）                              （写作时注入）
                                                                                ↓
                                                              （全书写完）→ novel-adapt
```

---

## 5. 关键模块详细设计

### 5.1 novel-style-engine（写法引擎）★ 差异化核心

**借鉴**：完整搬 AI-NWA 设计文档的概念架构，v0.1 简化版。

**数据模型**（保存到 `style/`）：

```yaml
# style/features.md（特征池）
---
type: style-features
sources:
  - ref-001-诡秘之主第1章
  - ref-002-某网文某章
---

## 客观特征（脚本提取）
- avg-sentence-length: 12  # 字
- avg-paragraph-length: 35
- punctuation-density:
    semicolons: 0.05
    em-dashes: 0.0
- top-words: [...]
- dialogue-narrative-ratio: 0.3

## 主观特征（LLM 一次提取，可编辑）
- enabled: true
  weight: 0.85
  rule: "用动作和神态表现情绪，不用形容词直述"
  example-good: "他握紧拳头，指节发白"
  example-bad: "他很愤怒"
- enabled: true
  weight: 0.70
  rule: "段落控制在 3 句话以内"
- enabled: false  # ← 用户停用了这条
  weight: 0.50
  rule: "对话句末避免叹号"
```

**Anti-AI 规则**（保存到 `style/anti-ai.md`）—— 三态借鉴 AI-NWA：

```yaml
---
type: anti-ai-rules
---

## forbidden（绝对禁止）
- pattern: "不是.+而是"
  description: "AI 特征句式"
- pattern: "——"
  description: "破折号在中文网文中是 AI 痕迹"
- pattern: "值得注意的是|核心在于|关键在于"
  description: "学术报告腔"

## watch（频次监控，超阈值警告）
- pattern: "突然|忽然|猛然"
  max-per-3000: 1
- pattern: "似乎|可能|或许"
  max-density-per-1000: 3

## encourage（鼓励出现）
- description: "感官描写（视/听/嗅/触/味）每场景至少 2 类"
```

**编译输出**（`style/compiled.md`）—— 注入到 chapter 写作 prompt：

```markdown
# 本书写法约束（编译后）

## must keep（weight >= 0.85）
- 用动作和神态表现情绪，不用形容词直述
- ...

## keep preferred（weight 0.65-0.85）
- 段落控制在 3 句话以内
- ...

## forbid
- 句式：不是…而是…
- 标点：破折号
- ...

## watch
- 突然/忽然/猛然：每 3000 字最多 1 次
- ...
```

**流程**：
1. 用户投喂样本到 `style/samples/`（手放或粘贴）
2. 跑 `extract_style.py`：
   - 客观特征用 Python 统计算（句长、段长、词频、标点）
   - 主观特征调一次 LLM 提取（修辞/句式/视角偏好）
3. 写入 `style/features.md`，用户编辑（启用/停用/调权重）
4. 跑 `compile_style.py`：把启用的特征 + anti-ai 规则编译成自然语言约束
5. `novel-chapter` 写作时自动把 `compiled.md` 塞进 system prompt

### 5.2 novel-review（校稿）★ 三层验证

**借鉴**：inkos 三大武器全部独立重写。

**Layer 1: 客观脚本检查**（秒级返回）

`check_ai_tells.py` — 4 维统计（inkos `ai-tells.ts` 重写）：
- dim 1：段落长度变异系数 < 0.15 → AI 痕迹（自然写作有节奏起伏）
- dim 2：套话密度（"似乎/可能/或许…"）> 3 次/千字
- dim 3：同一转折词（"然而/不过/与此同时…"）≥ 3 次
- dim 4：连续 ≥ 3 句相同开头模式（列表化结构）

`check_post_write.py` — 硬规则表（inkos `post-write-validator.ts` 重写）：
- "不是…而是…"句式：error
- "——"破折号：error
- 转折词密度上限：每 3000 字 ≤ 1 次
- 疲劳词每章 ≤ 1 次（清单从书的 style/compiled.md 读）
- 元叙事禁词："读者可能"、"接下来就是"
- 分析报告术语禁：核心动机/锚定效应/沉没成本（学术词漏到正文）
- 说教词禁：显然/毋庸置疑/不言而喻
- 集体反应禁：全场震惊/众人皆惊

`check_hook_ledger.py` — 伏笔账核对（inkos `hook-ledger-validator.ts` 重写）：
- 解析章纲的 "hook 账" 段：open/advance/resolve/defer 四态
- 每条 advance/resolve 必须在正文中有关键词回声（用 CJK 2-gram 提取）
- "揭1埋1" 硬底线：本章 resolve 多少个钩子，必须至少 open 同样多个新钩子
- 跟 `plot/foreshadowing.md` 状态同步

`check_consistency.py` — 设定一致性（自创）：
- 本章出场人物 → 跟 `characters/{x}.md` 的 frontmatter 比对（年龄/能力/关系）
- 本章涉及地点 → 跟 `worldbuilding/locations/{x}.md` 比对
- 本章涉及力量体系动作 → 跟 `worldbuilding/systems/{x}.md` 规则比对

**Layer 2: 主观 LLM 校验**

把章节正文 + 相关 vault 文件喂给 LLM，输出：
- 偏离大纲（vs `plot/arcs/{arc}.md` 中本章应推进的情节点）
- OOC（vs 角色卡的 voice & speech patterns）
- 设定矛盾（vs worldbuilding）
- 文风漂移（vs `style/compiled.md`）

**Layer 3: 综合报告**

输出 `chapters/ch-XXX.review.md`，按位置列出问题：
```
[L 23] 严重: hook 账未兑现 - H007 "胖虎借条" 在 advance 列表但正文无关键词回声
[L 45] 错误: 出现"不是…而是…"句式
[L 67] 警告: 段落变异系数 0.12，过于均匀
[L 89] 主观: 主角说"明白了"不符合其 voice（一向不正面回答）
```

### 5.3 novel-memory（长期记忆）

**借鉴 NovelClaw 的 bank 分类**，但全用文件系统（不上向量库）。

**写新章前的 load 流程**：
1. **必载**（无条件）：`story.md`、`style/compiled.md`、`plot/_index.md`
2. **上下文窗口**：前 3 章正文 + 前后各 3 章章纲摘要（从 `.memory/chapter-briefs.md` 读）
3. **实体加载**：从本章预定出场角色名单 → 读对应 `characters/{x}.md`
4. **状态加载**：`.memory/entity-state.md` 中相关实体的当前状态
5. **伏笔加载**：`plot/foreshadowing.md` 中 status=planted 但未 paid-off 的项
6. **关系加载**：`.memory/relationship-state.md` 中本章出场人物之间的关系
7. **Token 预算超限**：按相关性截断（先去远处章节摘要，再去次要角色）

**写完后的 update 流程**：
1. 提取本章新出现的人物 → 追加到 `characters/_index.md`（重要的提醒用户填写角色卡）
2. 提取本章新埋的伏笔 → 加到 `plot/foreshadowing.md`
3. 标记本章回收的伏笔 → 更新 status
4. 生成本章摘要（LLM 一次调用）→ 追加到 `.memory/chapter-briefs.md`
5. 更新 `.memory/entity-state.md`（伤亡/位置/物品变化）
6. 更新 `.memory/relationship-state.md`（关系演变）
7. 用户审阅意见 → 追加到 `.memory/revision-notes.md`

### 5.4 novel-chapter（章节写作核心循环）

**借鉴 inkos 多 agent 管线概念**，简化为 skill 内串行步骤：

```
6.1 outline        - 读取卷纲 + 前后章节情景 → 生成单章章纲（含 hook 账）
6.2 user_confirm   - 强制等用户确认章纲（不可跳过）
6.3 memory_load    - 调 novel-memory load
6.4 write          - 拼装上下文 + style/compiled.md → 写作
6.5 self_check     - 跑客观脚本检查（hook ledger / ai-tells / post-write）
6.6 fix_loop       - 若有 critical violation 自动修复，最多 3 轮
6.7 memory_update  - 调 novel-memory update
6.8 checkpoint     - 创建 chapter_X_complete 检查点
6.9 user_review    - 等用户审阅；意见写入 revision-notes
```

**借鉴 novel-writer 的"用户强制确认门"**：6.2 是硬阻断，章纲不确认不写作。

**借鉴 inkos 的"两阶段温度"**：6.4 写作用高 temp（创作）；6.5 自检和 6.6 修复用低 temp（确定性）。

### 5.5 novel-adapt（格式转换）

**小说 → fountain 剧本**：
- 借 bybren 的 fountain 模板，简化到中文场景
- LLM 拆场景 → 标 INT/EXT → 提取对白 → 转动作描写为 sluglines + scene description
- 输出 `deliverables/screenplay.fountain`，可用现成 fountain renderer 出 PDF

**小说 → 动漫分镜**：
- 自定义 markdown 表格模板：`| 场次 | 镜号 | 景别 | 运镜 | 画面描述 | 对白 | 时长 |`
- LLM 按章节拆镜，标注景别（特写/中景/远景/全景）和运镜（推/拉/摇/移/跟/甩）
- 用户审阅修改
- 输出 `deliverables/storyboard.md`

---

## 6. 实施路线图

### Phase 1（MVP，2-3 周）—— 跑通核心循环

P0 模块全部完成：
- [ ] `novel-init`：fork story-skills/story-init 结构 + 中文化模板 + 自动 git init
- [ ] `novel-brainstorm`：基础对话，复用 novel-writer 的文风类型表
- [ ] `novel-worldbuilding` / `novel-characters` / `novel-plot`：fork story-skills 三个 skill + 中文化 + 加入 novel-writer 的四大原则
- [ ] `novel-chapter`：完整 9 步循环
- [ ] `novel-memory`：v0.1 文件系统直读
- [ ] 工程层：`checkpoint.py` 移植、`validate_structure.py` 自创

**里程碑**：能从 0 写出 5 章 ≥ 3000 字/章的连贯故事，记忆不漏关键设定。

### Phase 2（差异化模块，2 周）—— 写法 + 校稿

- [ ] `novel-style-engine`：完整三层（抽取 / 特征池 / 编译）
- [ ] `novel-review`：客观三脚本（ai-tells / post-write / hook-ledger）+ 主观 LLM 层
- [ ] 网文领域规则填充：禁用 AI 词表、疲劳词清单、四大推进原则模板

**里程碑**：
- 投喂 3 篇样本后能仿写到肉眼可辨
- 校稿能在已写章节中找出 ≥ 3 类 issue（句式 / hook / 文风漂移）

### Phase 3（输出适配，1-2 周）—— 转换

- [ ] `novel-adapt`：fountain 剧本 + 中文分镜模板

**里程碑**：单章小说能转出可读的剧本和分镜。

### Phase 4（按需扩展）

- 向量记忆层（章节数 > 30 时考虑）
- 市场调研模块（web search 集成）
- Obsidian dataview 自动注册表生成
- 多语言支持

---

## 7. 待和你朋友确认的几个问题

1. **vault 路径默认值**：cwd / `~/Documents/{书名}/` / `~/Obsidian/{书名}/`？建议默认 cwd，可在 init 时选。
2. **章节字数默认**：网文向 3000-4000，传统文学不限。题材主攻什么？
3. **目标平台**：起点 / 番茄 / 晋江 / 海外 / 不发表？影响题材规则库和文风类型清单的具体内容。
4. **格式转换优先级**：剧本和分镜哪个先做？还是 Phase 3 一起？
5. **LLM 主模型**：默认随 Claude Code 走 Claude。写法引擎和 LLM 校稿是大用量项，是否要走 DeepSeek/Kimi 降本？

---

## 8. 风险

- **写法仿写在短样本上效果有限**：v0.1 全靠 LLM in-context，3-5 篇样本可能学不到深层风格。**降级方案**：积累用户反馈到 `revision-notes.md`，每章迭代修正特征权重。
- **百万字一致性**：纯文件检索在章节数 > 30 后 token 压力大。**应对**：章节摘要 + 实体状态分离能撑到 50 章；之后引入向量层。
- **客观脚本会误伤**：inkos 的硬规则在中文网文圈内是共识，但在传统文学、海外向作品中可能不适用。**应对**：所有规则都做成可配置（书级 frontmatter 可关闭某条）。
- **写法编译可能"鸡同鸭讲"**：把权重 0.85 编译成 "must keep" 这种翻译，LLM 是否真的会遵守？需要在 Phase 2 实测调优。

---

## 9. 文件清单（最终设计）

```
novel-suite/                              # 我们要建的 skill 套件 repo
├── .claude-plugin/
│   ├── plugin.json                       # Claude Code plugin 元信息
│   └── marketplace.json                  # 可选：发到 marketplace
├── README.md
├── DESIGN.md                             # 本文档
├── AUDIT.md                              # 候选项目代码级审计（保留作设计依据）
│
├── skills/
│   ├── novel-init/SKILL.md
│   ├── novel-brainstorm/SKILL.md
│   ├── novel-worldbuilding/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── location-template.md
│   │       ├── system-template.md
│   │       └── world-element-types.md    # 含中文网文常见体系（修真/玄幻/科幻/...）
│   ├── novel-characters/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── character-template.md
│   │       ├── relationship-types.md
│   │       └── voice-patterns.md          # 各类角色的 voice 范式
│   ├── novel-plot/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── arc-template.md
│   │       ├── structure-models.md        # 三幕 / 英雄之旅 / 起承转合 / 网文升级流
│   │       ├── pacing-principles.md       # ← novel-writer 的四大原则
│   │       └── hook-ledger-spec.md        # ← inkos 的伏笔账规范
│   ├── novel-style-engine/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── extract_style.py
│   │   │   └── compile_style.py
│   │   └── references/
│   │       ├── style-feature-schema.md
│   │       ├── anti-ai-rules.md           # 默认禁用词表
│   │       ├── style-types.md             # 五大文风类型（动词驱动 / 克制典雅 / ...）
│   │       └── literary-techniques.md     # 文学技巧库（伏笔 / 钩子 / POV / ...）
│   ├── novel-memory/SKILL.md
│   ├── novel-chapter/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── chapter-template.md
│   │       └── writing-guidelines.md
│   ├── novel-review/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── check_ai_tells.py
│   │   │   ├── check_post_write.py
│   │   │   ├── check_hook_ledger.py
│   │   │   └── check_consistency.py
│   │   └── references/
│   │       └── quality-rubric.md
│   └── novel-adapt/
│       ├── SKILL.md
│       ├── scripts/
│       │   └── to_screenplay.py
│       └── references/
│           ├── fountain-spec.md
│           └── storyboard-template.md
│
└── shared/
    ├── checkpoint.py                     # 通用快照工具
    ├── validate_structure.py              # vault 结构合规检查
    └── vault-conventions.md               # vault 约定（统一规范）
```

---

## 10. 补丁（精读 inkos continuity.ts 824 行 + AI-NWA prompt-compiler v1 1021 行后）

### 10.1 校稿改为 37 维（不是 33）

inkos 实际维度是 37 个，分四组：

**A 组 - LLM 评估，通用 17 维**（基础校稿）
1. OOC 检查（角色失格）
2. 时间线检查
3. 设定冲突
4. 战力崩坏
5. 数值检查
6. 伏笔检查（含债务升级规则）
7. 节奏检查（含 3-5 章周期波形）
8. 文风检查
9. 信息越界（角色不该知道的事）
10. 词汇疲劳（含 AI 标记词密度）
11. 利益链断裂（动机不可信）
12. 年代考据（需要联网搜索）
13. 配角降智
14. 配角工具人化
15. 爽点虚化（含欲望驱动检测）
16. 台词失真
17. 流水账（含日常段落功能性）

**B 组 - 统计学，Python 脚本**（共 4 维，已规划）
20. 段落等长（变异系数<0.15）
21. 套话密度（>3/千字）
22. 公式化转折（同词≥3次）
23. 列表式结构（同开头≥3句）

**C 组 - 高级一致性，LLM 评估**（5 维）
19. 视角一致性
24. 支线停滞
25. 弧线平坦（角色情绪 3 问检查）
26. 节奏单调
27. 敏感词检查

**D 组 - 通用，LLM 评估**（2 维，强制开启）
32. 读者期待管理（含高潮后影响检查）
33. 章节备忘偏离（含稀疏 memo 豁免）

**E 组 - 番外/续作专用，LLM 评估**（4 维，仅 fanfic 模式开启）
28-31. 正传冲突 / 未来泄露 / 跨书规则 / 伏笔越权

**F 组 - 同人专用，LLM 评估**（4 维，仅 fanfic 模式开启）
34-37. 角色还原度 / 世界规则遵守 / 关系动态 / 正典事件一致性

**评分校准（直接抄 inkos）**：
- 95-100：可直接发表
- 85-94：小瑕疵但顺畅
- 75-84：明显问题但骨架稳
- 65-74：多处问题影响阅读
- <65：结构崩坏需重写

**Reviewer 边界（重要）**：审稿只看完成度 + 结构，**不审文笔**。文笔在 Polisher（润色）阶段。novel-review 不要做 prose 评判。

### 10.2 style-engine 编译器升级为 6 层结构

原 `style/compiled.md` 单文件 → 拆成 **5 个 prompt block**（AI-NWA 设计）：

```
style/compiled/
├── global-context.md         # 5.1 世界与任务基础层
├── style-rules.md            # 5.2 写法主规则层（叙事/人物表达/语言/节奏 4 块）
├── anti-ai.md                # 5.4 反AI约束层（forbidden/risk/encourage 3 段）
├── output-format.md          # 5.5 输出格式层
└── self-check.md             # 5.6 自检指令层（在 prompt 末尾极短）
```

5.3 角色表达校正层是动态的（按本章 POV 角色读对应 character.md）。

### 10.3 强度三档 + 差异化措辞

| 权重区间 | 措辞档 | 用语 | 适合场景 |
|---|---|---|---|
| 0.3-0.5 | 低强度 | "尽量 / 倾向 / 可适当" | 大纲阶段 |
| 0.6-0.8 | 中强度 | "优先 / 注意避免 / 警惕" | 正文生成 |
| 0.8-1.0 | 高强度 | "必须 / 禁止 / 不得 / 只能" | 改写、试写、风格实验 |

同一条规则在不同权重下措辞不同。compile_style.py 按权重选档输出。

### 10.4 不同任务用不同 prompt 模板

写法编译器对应 5 种任务模板：

| 任务 | 写法规则强度 | 反 AI 强度 | 自检 | 额外约束 |
|---|---|---|---|---|
| 章节正文生成 | 强 | 强 | 开 | — |
| 续写 | 强 | 强 | 开 | "保持前文气质，禁止突然升华" |
| 润色 | 中 | 中 | 开 | "不增剧情，不改人物关系" |
| 改写 | 高 | 高 | 开 | "保留事实，替换表达" |
| AI 味修正 | — | 高 | 关 | "只修违规点，附违规报告" |

### 10.5 规则标准化：用户口语 → 结构化字段

用户可能说"别太文青"、"多点脏话"，需要标准化器先转换：

```json
{
  "language.register": "colloquial",
  "language.roughness": 0.7,
  "language.allow_poetic_insert": false,
  "character.emotion_expression": "behavior_only",
  "anti.forbid_explicit_psychology": true
}
```

然后再编译成模型可读的自然语言。标准化器在 `scripts/standardize_rule.py`（v0.2，v0.1 直接让用户写结构化）。

### 10.6 多层绑定合并策略

写法可同时绑定到 5 个层级（全书 / 卷 / 章 / 角色视角 / 当前任务）。合并规则：
- 任务级 > 角色视角级 > 章级 > 卷级 > 全书级（越具体越优先）
- 同字段冲突时取高优先级
- forbidden 三态采用 union（任何层级 forbidden 即 forbidden）

---

## 11. 致谢

本设计独立实现，借鉴以下开源项目的设计与算法：

- [story-skills](https://github.com/danjdewhurst/story-skills) — vault 骨架结构
- [novel-writer](https://github.com/AI-Practical-Lab/novel-writer) — 中文网文领域规则、检查点机制
- [inkos](https://github.com/Narcooo/inkos) — ai-tells 统计检测、post-write 硬规则、hook-ledger 算法、多 agent 管线概念
- [AI-Novel-Writing-Assistant](https://github.com/ExplosiveCoderflome/AI-Novel-Writing-Assistant) — 写法引擎完整概念架构（描述/执行分离、anti-AI 三态、多级绑定）
- [NovelClaw](https://github.com/iLearn-Lab/NovelClaw) — 16 bank 记忆分类法
- [story-systems-template](https://github.com/bybren-llc/story-systems-template) — fountain 剧本格式参考
