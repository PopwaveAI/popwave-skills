---
name: novel-plot
description: 管理小说情节结构 —— 卷纲、故事弧（arc）、时间线、伏笔账（hook ledger）。当用户说"做卷纲"、"设计故事弧"、"加伏笔"、"伏笔账"、"时间线"、"plot outline"、"design arc" 时触发。包含中文网文章节情节推进四大原则，以及借鉴 inkos hook-ledger 的 open/advance/resolve/defer 四态伏笔语义和"揭1埋1"硬底线。
---

# Novel Plot —— 情节结构管理

## 功能

管理三类情节资产：
1. **故事弧 / 卷**（`plot/arcs/{arc-kebab}.md`）—— 每个主要叙事单元一个文件
2. **时间线**（`plot/timeline.md`）—— 全书事件按时间排序
3. **伏笔账**（`plot/foreshadowing.md`）—— 借鉴 inkos hook-ledger，open/advance/resolve/defer 四态

## 前置条件

- `plot/_index.md` / `plot/timeline.md` / `plot/foreshadowing.md` 存在
- 建议先有主要角色（`novel-characters`）和核心地点（`novel-worldbuilding`），否则卷纲里的引用会指向空

## 工作流

### A. 选定全书结构模型

**首次使用此 skill 时，确认全书 structure（写入 `plot/_index.md` frontmatter）**：

参考 `references/structure-models.md`，常见 5 种：
- **三幕结构**（western 默认）
- **英雄之旅**（成长向史诗）
- **起承转合**（东方传统）
- **救猫咪 15 拍**（影视化友好）
- **网文升级流**（爽文专用，10-30 章一卷的节奏模型）

如果用户没拍板，按 genre 默认：
- 玄幻 / 修真 / 都市爽文 → 网文升级流
- 历史 / 权谋 / 悬疑 → 三幕结构
- 言情 / 成长 → 起承转合 或 英雄之旅

### B. 创建一个故事弧（arc）

1. **读取上下文**：
   - `story.md`：核心矛盾、30 章承诺
   - `plot/_index.md`：已有弧的列表，避免冲突
   - `characters/_index.md`：可能涉及的角色

2. **问基本信息**：
   - 弧名（如"卷一-初临世界"或"sera-reclamation"）
   - 弧类型：main（主线）/ subplot（支线）/ character（角色弧）/ thematic（主题弧）
   - 涉及哪些角色
   - 服务哪些主题

3. **对话填充弧内容**（用 `references/arc-template.md` 作骨架）：

   **A. Setup（开局状态）**
   - 起点情境，主角处于什么状态
   - 这一弧的"问题"是什么

   **B. Rising Action（铺垫升级）**
   - 主角做了什么尝试
   - 遭遇了哪些升级的阻力
   - 每个阻力如何让主角付出代价

   **C. Climax（高潮）**
   - 这一弧的决定性时刻
   - 主角的关键抉择（含**代价**）

   **D. Resolution（解决）**
   - 解决方式
   - 主角变成了什么
   - 给下一弧留下了什么（伏笔 / 新格局）

4. **填充 Plot Points 表**（章节级事件追踪）：

   ```markdown
   | # | 事件 | 幕 | 章节 | 状态 |
   |---|---|---|---|---|
   | 1 | {事件} | Act 1 | Ch 1 | Planned |
   | 2 | {事件} | Act 1 | Ch 2 | Planned |
   | 3 | {事件} | Act 2 | Ch 3 | Written |
   ```

5. **填充 Foreshadowing 表**（弧内伏笔）：

   每个伏笔包含：
   - **Plant**（埋设的具体表象）
   - **Payoff**（兑现的内容）
   - **Planted-at**（章节号）
   - **Payoff-at**（章节号 或 TBD）
   - **Status**：`planted` / `advancing` / `paid-off` / `deferred`

6. **写文件**：路径 `plot/arcs/{arc-kebab}.md`

7. **更新 `plot/_index.md`** 的弧表

8. **同步到全书伏笔总表**：把本弧的伏笔合并写到 `plot/foreshadowing.md`（详见下方"伏笔账管理"）

### C. 时间线管理

**`plot/timeline.md` 是全书事件按时间顺序的总览**。

每次创建 / 写章节 / 跑 `novel-chapter` 都会更新它。

格式：

```markdown
| 时间 | 事件 | 弧 | 章节 |
|---|---|---|---|
| 12 年前 | sera 父母被杀 | (背景) | (Backstory) |
| 现在 | sera 回归北境 | seras-reclamation | Ch 1 |
| 现在 + 3 天 | sera 与 kael 重逢 | seras-reclamation | Ch 2 |
```

**插入规则**：按时间排序插入。检查时间冲突。如果某事件被多个章节引用（比如同一事件被多个 POV 写过），用 `(Ch 5, Ch 7)` 标注。

### D. 伏笔账管理（hook ledger）

> 借鉴 inkos hook-ledger 设计。每条伏笔有 4 态生命周期，全书必须维持"揭 1 埋 1"硬底线。
> 详见 `references/hook-ledger-spec.md`。

**4 态语义**：

| 状态 | 含义 |
|---|---|
| `open` | 已埋下，未推进，未回收 |
| `advance` | 已推进（给了新线索 / 加深了悬念）但未完整回收 |
| `resolve` | 已完整回收 |
| `defer` | 暂时搁置（明确说明：不在这一卷处理）|

**伏笔账位置**：

- `plot/foreshadowing.md`（全书总表）—— 所有伏笔
- 每个弧 `plot/arcs/{arc}.md` 的 `## Foreshadowing` 段 —— 本弧内的伏笔
- 每个章节 `chapters/ch-XXX.md` 的 frontmatter `## hook-账` 段 —— 本章 advance / resolve / defer 的伏笔

**操作**：
- 加伏笔（plant）→ 写入全书 + 对应弧的伏笔表，状态 `open`
- 章节里推进了一个伏笔 → 章节 frontmatter 标 `advance`，全书表更新
- 章节里回收了一个伏笔 → 章节 frontmatter 标 `resolve`，全书 + 弧 + 时间线（标注 payoff-at）都更新
- 章节里决定暂搁 → 章节 frontmatter 标 `defer`，给出搁置原因

**硬底线**（由 `novel-review` 的 `check_hook_ledger.py` 自动检查）：
- 每章 `resolve` N 个伏笔，必须至少 `open` N 个新伏笔
- 不允许"只揭不埋"——读者会觉得故事在收缩
- 例外：全书末章可以只 resolve 不 open

### E. 卷级章节大纲（volume chapter outline）

**当用户准备好开始写某一卷的章节**（即将进入 `novel-chapter` 循环），需要先做"卷级章节大纲"。

每卷一份，路径 `plot/arcs/{arc}-chapters.md`（或在 `arc.md` 的 `## Chapter Outline` 段）。

每章一行：

```markdown
## 第 1 章：{标题}
- 时间：具体时间点
- POV：{character-id}
- 地点：{location-id}
- 权重：⭐⭐⭐（详见下方权重规范）
- 危机来源：来自{上一章/前情}的{什么隐患}
- 核心冲突：本章要解决什么 / 不解决什么
- 主角抉择：做什么选择
- 埋下隐患：这个抉择埋下了什么新危机（→ 下一章的危机来源）
- 推进的 hook：{hook-id-list}
- 兑现的 hook：{hook-id-list}
- 暂搁的 hook：{hook-id-list}
```

**章节情节推进四大原则**（详见 `references/pacing-principles.md`）：

1. **因果链原则**：每章的危机必须从上一章的隐患发展而来
2. **抉择+代价原则**：主角每章必须做出明确抉择，每个抉择都有代价
3. **升级递进原则**：危机必须层层升级
4. **节奏权重原则**：用章节数量体现节奏（⭐ 过渡 / ⭐⭐ 铺垫 / ⭐⭐⭐ 转折 / ⭐⭐⭐⭐ 高潮前奏 / ⭐⭐⭐⭐⭐ 大高潮）

**禁止**：
- ❌ 越界写下一卷的内容
- ❌ 重复展开上一卷的内容（只能在"前情衔接"简要提及）
- ❌ 章节没有抉择 / 没有代价 / 没有钩子

## 与其他 skill 的边界

- **不写章节正文**：那是 `novel-chapter`
- **不创建角色 / 地点**：使用 `novel-characters` / `novel-worldbuilding`
- **不评判情节合不合理**：那是 `novel-review`

## 输出

每次完成创建后：
- 给用户看新写的文件内容
- 列出本次更新涉及的所有文件（弧 + 全书伏笔表 + 时间线）
- 提示是否准备进入章节写作（进入 `novel-chapter` 循环前必须有"卷级章节大纲"）
