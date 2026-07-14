# Step 2：沉淀分流执行

> 触发：step-1 审稿 SOP 通过门禁后进入。
> 目标：执行沉淀分流，更新库文件与 current-state，归档旧版，追加审稿日志。落盘必须达 formal 或 draft，trial 不落盘。

## 核心约束：历史层职责分离（PRD §4.4）

`review-沉淀.md` 与 `压缩归档/` 不重叠：
- 沉淀记"判断和规则"——append-only，每次追加一段。
- 归档存"旧版入口包全文"——current-state 更新前先复制旧版，再覆盖。

两者顺序固定：先归档旧版，再覆盖 current-state，最后追加沉淀。不可颠倒、不可跳过。

## 执行步骤

### 1. 归档旧版（核心修复）

读取当前 `涌现/current-state.md`，复制到：

```
涌现/压缩归档/current-state-{YYYYMMDD}-{章位}.md
```

- `{YYYYMMDD}` 用本次审稿日期，`{章位}` 用被归档版对应的下一章章位（如 第12章）。
- 首次初始化无旧版时跳过本步，并在 step-5 沉淀日志注明"首版无归档"。
- 归档保留旧版完整入口包，不做删改。

### 2. 更新 current-state

参照 `templates/current-state.tpl.md` 空模板，写入新版 `涌现/current-state.md`：

- 元数据块：`doc_type: current-state` / `read_policy: full-required` / `primary_consumer: write` / `compression: forbid` / `source_of_truth: true` / `last_updated`。
- 章节结构：当前章位 / 不可改事实 / 人物状态 / 设定状态 / 可用燃料队列 / 伏笔债务 / 下一章硬推进 / 禁止漂移。
- 若启用文风DNA，必须包含 `## 本章DNA执行包`，供下一轮 write 消费。
- 控制在 1000-2500 字。写不下的内容留在库文件，不进入 write 入口。

### 3. 更新库文件

按 step-1 分流清单按需更新（owner=review，PRD §4.2）：

| 信息 | 文件 |
| --- | --- |
| 已确认设定 | `涌现/设定库.md` |
| 人物最新状态 | `涌现/人物库.md` |
| 伏笔和长线 | `涌现/剧情线.md` |
| 可入场燃料池 | `涌现/research-写作燃料.md`（唯一名，禁用 `燃料库.md`） |
| 题材机制 | `涌现/content-mechanics.md` |

库文件允许大，write 不直接读；review 负责筛选进 current-state。

### 4. 追加 review-沉淀（append-only，核心修复）

在 `涌现/review-沉淀.md` **末尾追加**一段，不删改任何历史段落。每段含：

- 日期 / 章位
- 总判断（可用等级 / 爽文兑现 / AI味 / 最大问题）
- 最影响阅读的 3 个问题（含归因与去向）
- current-state 是否更新（含归档文件名）
- 修正规则（本次审稿沉淀出的可复用规则）

元数据块：`doc_type: review-log` / `read_policy: index-only` / `primary_consumer: human`。

### 5. 标记 soul 修改建议

如有 soul 修正建议（文风/气口/主卖点），列出待用户确认项，不直接改 `涌现/soul.md`。soul 落盘需用户确认后由 seed 重构或 review 修正（owner 见 PRD §4.2）。

### 6. 写入下一章DNA执行包（启用时）

把 step-1 产出的下一章DNA执行包写入新版 `current-state.md`：

```markdown
## 本章DNA执行包
- DNA源：
- 本章DNA模式：适配 | 强嫁接 | 轻触
- 本章章型：
- 本章笔触目标：
- 本章章内套路：
  1. 起笔：
  2. 第一信息变化：
  3. 压力/诱因：
  4. 主角动作或判断：
  5. 阻碍升级：
  6. 可见反馈：
  7. 章末钩子：
- 禁止误用：
- 验收点：
```

约束：

- 只写下一章要执行的 DNA，不把整份 DNA 复制进 current-state。
- 章型和章内套路必须服务下一章硬推进，不能为了文风而脱离剧情。
- 强嫁接必须写清"迁移章内套路，不迁移名词/口癖/全书架构/特殊章节机制"。

## 落盘后检查

- [ ] 旧版 current-state 已归档到 `压缩归档/`（首版除外）。
- [ ] 新版 `涌现/current-state.md` 已写入，元数据块完整，1000-2500 字。
- [ ] 如启用文风DNA，新版 current-state 已包含 `本章DNA执行包`。
- [ ] 库文件按需更新，燃料文件名仅为 `research-写作燃料.md`。
- [ ] `涌现/review-沉淀.md` 已追加一段，历史未被删改。
- [ ] soul 修改建议已列出，未擅自改 soul。
- [ ] 版本与 SKILL.md/skill.json/CHANGELOG 一致（3.7.0）。

## 回复

采用 PRD §4.7 统一格式：

```markdown
本次采用 skill：pop-qidian-review
execution.mode：{formal|draft|trial}

总判断 / 最影响阅读的 3 个问题 / current-state 更新与归档状态 / 待确认修改

下一步：{建议执行 pop-qidian-write 写下一章，或先确认 soul 修改建议}
```
