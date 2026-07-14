# Step 1：消费输入

本步骤消费 write 的 4 类基础输入，并在项目启用文风DNA时消费本章DNA执行包，抽取本章写作包。引用 PRD §4.1（骨架）、§4.2（owner/read_policy）、§4.5（execution.mode）。

## 1. 必读输入（4 类基础输入 + DNA 条件输入）

按优先级消费，缺一项记入缺口：

### 1.1 用户本轮要求（优先）

用户本轮口头/文字要求是最优先输入，覆盖以下三类的默认取值。例如"把第 3 章重写得更狠"、"续写下一章"、"开篇样章"。

- 明确：把 X 写成 Y / 当前章位 / 续写或重写 / 特殊约束。
- 若用户要求与 current-state 冲突，以用户要求为准，但必须在创作记录里标注冲突。

### 1.2 current-state.md（全量读）

路径：`涌现/current-state.md`。read_policy = full-required（PRD §4.2）。

必须全量读取，不得用摘要替代。抽取本章写作包所需字段。

### 1.3 soul.md（全量读）

路径：`涌现/soul.md`。read_policy = full-required（PRD §4.2）。

必须全量读取。soul 同时管主卖点和正文风格，不得当作事实来源。

### 1.4 最近正文（全量读）

路径：`涌现/正文/{书名}-第{N-1}章-{标题}.txt`（上一章）或用户指定锚定正文。read_policy = full-if-targeted（PRD §4.2）。

必须全量读目标文件，不得凭对话历史替代。

### 1.5 文风DNA条件输入（启用时必读）

触发条件：

- `soul.md` 存在"文风DNA融合策略"、"DNA源"、"强嫁接"等声明。
- `current-state.md` 存在 `## 本章DNA执行包`。
- 用户本轮明确要求使用某个文风DNA。

读取规则：

- 必须先读取 `current-state.md` 中的 `## 本章DNA执行包`。
- 若执行包提供 `DNA源` 路径，读取该 DNA 文件中与本章章型相关的章型卡、笔触约束、章内套路、角色/口癖隔离；不要把整份 DNA 当剧情事实库。
- 如果 DNA 源过大，只读取目录、对应章型卡、章内笔触、单章套路、角色/口癖隔离、涌现式消费契约。
- 已启用文风DNA但缺本章DNA执行包时，execution.mode 不得为 formal；要求 review/seed 先把 DNA 执行包压入 current-state。

## 2. 禁止默认读取

以下文件 read_policy 为 index-only 或 full-if-targeted，write 不得默认读取（PRD §4.2）：

- `seed-种子文档.md`
- `research-写作燃料.md`
- `content-mechanics.md`
- `设定库.md`
- `人物库.md`
- `剧情线.md`
- `review-沉淀.md`
- `压缩归档/`
- 未被 `本章DNA执行包` 指向的其他文风DNA文件

仅当用户明确指定或处理缺口时才可读取，且必须在创作记录"已读输入"里如实标注。

## 3. 缺口处理

如果 current-state 明显缺关键事实：

- 不自行翻库补写。
- 停止并要求先执行 pop-qidian-review / ledger 更新 current-state。
- 若用户要求继续试写，execution.mode 降为 draft 或 trial（PRD §4.5）。

## 4. 抽取本章写作包

从 4 类输入抽取，不扩展成章纲表：

```markdown
## 本章写作包
execution.mode:
- 把 X 写成 Y：
- 当前章位：
- 不可改事实：
- 人物状态：
- 设定状态：
- 可用燃料：
- 伏笔债务：
- 下一章硬推进：
- 禁止漂移：
- 用户本轮新增要求：
- soul 约束：（列 3-5 条本章实际执行的约束）
- 文风DNA执行：（未启用填"未启用"；启用时列 DNA源、模式、章型、笔触目标、章内套路、可见反馈、禁止误用）
```

- `下一章硬推进` 是硬约束，必须至少兑现 1 条。
- `禁止漂移` 不得违反。
- `soul 约束` 必须列 3-5 条，且正文里能看出来。
- 禁止把 soul 当事实来源（soul 不能新增剧情事实、设定规则、数值、人物状态）。
- `文风DNA执行` 必须来自 current-state 的本章DNA执行包；不得临场把整本参考小说的特殊桥段当通用规则。

## 5. execution.mode 判定

引用 PRD §4.5：

- formal：current-state + soul + 最近正文 + 用户要求 齐全且达标；若启用文风DNA，本章DNA执行包和对应 DNA 源片段也齐全。
- draft：必读输入有缺口但用户要求继续。
- trial：快速试做，不落盘。

缺 current-state 或 soul 不得标 formal。已启用文风DNA但缺本章DNA执行包，不得标 formal。

## 6. 门禁

进入 step-2 前必须满足：

- [ ] 本章写作包已抽取完整。
- [ ] execution.mode 已判定。
- [ ] 下一章硬推进至少 1 条已锁定。
- [ ] soul 约束 3-5 条已选定。
- [ ] 如启用文风DNA，已锁定章型、笔触目标、章内套路、可见反馈和禁止误用项。
- [ ] 缺口已记录或已要求 review 修复。

## 7. 下一步

门禁通过后，读取 `steps/step-2-write.md` 开始写正文。
