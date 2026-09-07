---
name: novel-memory
description: 管理长篇小说的长期记忆 —— 写章节前的上下文组装（memory_load），写完后的状态更新（memory_update）。这是百万字小说一致性的核心基础设施。**通常不由用户直接触发**，而是由 novel-chapter 在写作循环中自动调用。当用户说"看一下当前记忆状态"、"更新记忆"、"导出章节摘要" 等显式管理操作时也可触发。
---

# Novel Memory —— 长期记忆管理

## 功能

为长篇小说的"百万字一致性"提供基础设施。两大核心操作：

1. **memory_load**（写新章前）：根据本章计划，组装最相关的上下文喂给 writer
2. **memory_update**（写完章后）：从新写的章节中抽取事实，回灌到长期记忆

辅助操作（用户可显式触发）：
- 查看当前记忆状态
- 手动添加 / 修正某条记忆
- 导出章节摘要

## 数据模型：`.memory/` 8 个银行

借鉴 NovelClaw 的 16 bank 设计，v0.1 用 8 个核心 bank：

| Bank | 文件 | 内容 | 何时更新 |
|---|---|---|---|
| chapter-briefs | `.memory/chapter-briefs.md` | 每章 1-2 段摘要 | post-write |
| scene-cards | `.memory/scene-cards.md` | 重要场景的索引（"第 5 章地下室对峙"）| 章节中标记的"重要场景" |
| entity-state | `.memory/entity-state.md` | 实体当前状态（人在哪 / 持有什么 / 受了什么伤）| post-write |
| relationship-state | `.memory/relationship-state.md` | 当前关系状态（X 和 Y 现在啥关系）| post-write 或关系变化时 |
| continuity-facts | `.memory/continuity-facts.md` | 已确立的设定细节（"主角左手有伤疤"）| 首次出现时 |
| decision-log | `.memory/decision-log.md` | 作者重要决定的日志（"决定让 X 在卷二死掉"）| 用户主动 |
| revision-notes | `.memory/revision-notes.md` | 用户修改意见累积（用于"经验进化"）| 用户审稿后 |
| tool-observations | `.memory/tool-observations.md` | （v0.2+）外部工具调用记录 | v0.1 暂留空 |

## 工作流

### A. memory_load —— 写新章前的上下文组装

**输入**：本章的章节大纲（含 POV、出场角色、预定场景）。
**输出**：拼装好的上下文 blob，准备塞进 writer prompt。

**加载策略**（按优先级，token 不够就从下往上砍）：

```
PRIORITY 0 - 必载（无条件，无截断）
  - story.md frontmatter + 一句话简介 + 核心矛盾 + 30 章承诺
  - style/compiled/*.md（写法约束）
  - plot/_index.md（卷纲）

PRIORITY 1 - 强相关
  - 前 1 章完整正文 chapters/ch-{N-1}.md
  - 当前 arc 的 plot/arcs/{arc}.md（含本章对应的 plot points）
  - 本章 POV 角色的 characters/{x}.md

PRIORITY 2 - 中相关
  - 前 3 章摘要（从 chapter-briefs.md 读）
  - 本章预定出场角色的 characters/{x}.md
  - .memory/entity-state.md 中本章涉及实体的当前状态
  - .memory/relationship-state.md 中本章人物之间的关系
  - plot/foreshadowing.md 中 status=planted / advancing 的未回收伏笔

PRIORITY 3 - 弱相关
  - 后 3 章摘要（让 writer 知道方向，避免越界写）
  - 本章涉及地点 worldbuilding/locations/{x}.md
  - 本章涉及体系 worldbuilding/systems/{x}.md
  - .memory/continuity-facts.md 全部
  - .memory/decision-log.md（如果有相关条目）
  - .memory/revision-notes.md 最近 5 条

PRIORITY 4 - 装饰
  - 前 4-10 章的摘要（如果 token 还够）
```

**Token 预算**（v0.1 经验值）：
- 总预算 32k tokens（留 8k 给输出）
- P0+P1 不能超过 16k
- 如果 P2 加进去超过 24k，从 P2 末尾开始砍
- P3 / P4 是"有空间就塞"

**输出格式**：

把所有加载内容按 markdown 区块拼接，每块前面加 `## SECTION: {name}` 头，便于 LLM 区分。

### B. memory_update —— 写完章后的状态更新

**输入**：刚写完的章节正文 + 章纲。
**输出**：更新若干 memory bank 文件。

**步骤**（按依赖顺序）：

#### Step 1 - 实体抽取

读章节正文，让 LLM 输出本章涉及的：
- 新出现的人物名（不在 characters/ 中的）
- 新出现的地点名（不在 worldbuilding/locations 中的）
- 新提到的体系（不在 worldbuilding/systems 中的）

输出 JSON：

```json
{
  "new-characters": ["{name-1}", "{name-2}"],
  "new-locations": ["{place-1}"],
  "new-systems": [],
  "appeared-characters": ["{existing-1}", "{existing-2}"]
}
```

#### Step 2 - 重要度判定

对每个新人物，搜索后续章纲（`plot/arcs/*.md` + `plot/arcs/{arc}-chapters.md`）：
- 出现 ≥ 2 次 → **重要**，强烈建议用户用 `novel-characters` 创建角色卡
- 出现 1 次 → **工具人**，可选创建（默认不强求）

输出给用户：

```
本章出场了 3 个新角色：
  - 老王（重要 - 后续 5 章会再出现，建议创建角色卡）
  - 小李（工具人 - 仅本章）
  - 一名酒馆侍者（cameo - 跳过）

要现在创建"老王"的角色卡吗？(yes / 稍后再说)
```

#### Step 3 - 状态更新

更新 `.memory/entity-state.md`：

```markdown
## 本章变化（{date}）

### sera-voss
- 位置：{从 雾林 → 落雁城}
- 持有：{获得"血咒匕首"}
- 状态：{右肩中箭，未处理}

### kael-voss
- 位置：{继续在雾林扎营}
- 状态：{无变化}
```

每条变化记录格式：`{字段}：{从 X → Y}` 或 `{字段}：{描述}`

把这些变化追加到 entity-state.md（追加，不覆盖）。

#### Step 4 - 关系变化

如果本章有关系变化（比如 A 救了 B 命，B 对 A 态度从 hostile → grudging-respect），更新 `.memory/relationship-state.md`：

```markdown
### sera-voss ↔ kael-voss
- 之前：sibling, 信任度高
- 现在：sibling, **kael 开始警惕 sera 的力量失控**
- 触发：第 8 章的 ember 失控事件
```

#### Step 5 - 伏笔账更新

读章节 frontmatter 的 `## hook-账` 段（这是 `novel-chapter` 在写作时写入的），按 advance / resolve / open / defer 更新 `plot/foreshadowing.md` 总表。

#### Step 6 - 章节摘要

生成本章 1-2 段摘要，追加到 `.memory/chapter-briefs.md`：

```markdown
## Ch 8 - 雾林夜遇 (3210 字)

sera 与 kael 在雾林边缘扎营时遭遇一队 maren 的斥候。
sera 第一次主动使用 ember 力量，但失控烧死了一名斥候 + 烧伤 kael 的手。
kael 第一次表达对 sera 的恐惧。两人裂痕初现。
H012 推进，H001 advance。

POV: sera-voss
出场：sera-voss, kael-voss, 3 名 maren-scout（cameo）
地点：whispering-vale-edge
权重：⭐⭐⭐
```

每章 1-2 段，**不超过 200 字**。摘要是为了下次写作时快速回忆，不是写读后感。

#### Step 7 - 重要场景标记（条件性）

如果本章包含"关键场景"（用户标记或权重 ≥ ⭐⭐⭐⭐），追加到 `.memory/scene-cards.md`：

```markdown
### 雾林夜遇（Ch 8）
- 关键性：力量失控转折点
- 涉及：sera-voss, kael-voss
- 后续应用：作为 sera 自我恐惧的回忆素材
```

#### Step 8 - continuity-facts 增量

如果本章首次确立了某个"以后必须保持一致"的事实（如"sera 左手有 ember 灼伤"），加到 `.memory/continuity-facts.md`：

```markdown
## sera-voss 身体特征

- 左手腕有 ember 灼伤（Ch 8 失控造成，永久）
- 头发左侧灰色（Ch 1 提及）
```

continuity-facts 是给 `novel-review` 做一致性检查用的——后续章节如果写"sera 的左手伸出，光滑无痕"，review 应该报错。

#### Step 9 - 用户审阅意见（可选）

如果用户在 `novel-chapter` 的 user_review 阶段提了修改意见，把意见追加到 `.memory/revision-notes.md`：

```markdown
## Ch 8 用户修改意见 ({date})

- 开头节奏太慢
- sera 的失控应该再克制一点
- kael 的恐惧反应不够具体

### 下次写作改进方向
- 章首 3 段内必须有动作 / 冲突
- 力量描写"压抑"而非"宣泄"
- 配角恐惧通过身体反应表达（颤抖、退后、不敢直视）
```

这些意见会在 `memory_load` 的 P3 中被加载到下章 writer prompt，实现"经验进化"。

## 显式管理操作（用户可触发）

### "看一下记忆状态"

读取 `.memory/` 下所有文件，给用户一个摘要：

```
📊 当前记忆状态（截至 Ch 8）

📂 章节摘要：8 条
📂 重要场景：3 个
📂 实体状态：12 个实体追踪中
📂 关系变化：5 对关系记录
📂 一致性事实：18 条
📂 决定日志：4 条
📂 用户修改意见：3 条（最近一次 Ch 8）

🔍 待处理：
- 2 个新角色未创建角色卡：老王、小李
- 1 条伏笔超期未推进：H003 母亲的字条（埋设至今 8 章）
```

### "更新记忆"

手动触发 memory_update 流程（通常 `novel-chapter` 已经自动跑过，这里给"重写章节后手动重跑"的入口）。

### "导出章节摘要"

把 `.memory/chapter-briefs.md` 整理成可阅读的"全书提纲"，输出到 `deliverables/synopsis.md`。

## Token 预算的处理细节

如果 P0+P1+P2 超过预算，按以下顺序砍：

1. 先砍 P2 中的"次要出场角色"（appear-count 最少的）
2. 再砍 P2 中的"中等距离 chapter briefs"（保留紧邻的 1 章）
3. 然后砍 P2 中的 entity-state 旧条目（只保留最近 5 章变化）

**绝对不能砍**：
- story.md 顶层
- style/compiled/
- 前 1 章完整正文
- 当前 arc.md 的本章对应 plot point
- 本章 POV 角色

## 与其他 skill 的边界

- **不写章节正文**：那是 `novel-chapter`
- **不创建任何 entity 文件**：只**建议**用户用相应 skill 创建
- **不做主观判断**：比如不评论"这个伏笔埋得好不好"，只如实记录
- **不自动做向量检索**：v0.1 全文件系统操作，向量层留给 v0.2

## 输出

每次 memory_update 完成后，给用户一个简短报告：

```
📝 Ch 8 记忆更新完成

✓ 章节摘要已追加
✓ 实体状态更新：sera (位置+持有+伤), kael (无变化)
✓ 关系变化：sera↔kael（兄妹信任→裂痕初现）
✓ 伏笔账：advance H001, advance H012
✓ continuity facts：sera 左手 ember 伤（永久）
⚠ 待办：建议为"老王"创建角色卡（后续会出现 5 次）
```
