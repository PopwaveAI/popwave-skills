---
name: novel-init
description: 用于初始化一个新的小说项目。当用户说"我想写小说"、"开始写小说"、"新建小说项目"、"创建一本新小说"、"start a new novel" 时触发。会引导用户完成基本信息确认后，搭建标准的 vault 目录结构（story.md / characters / worldbuilding / plot / chapters / style / .memory），并可选地 git init。
---

# Novel Init —— 项目初始化

## 功能

引导用户用对话方式确定小说的基础信息，然后在文件系统中搭建一个符合 novel-suite 规范的 vault（标准 Obsidian 友好结构 + git 仓库）。

完成后，用户可以继续触发其他 skill（`novel-brainstorm` / `novel-worldbuilding` / `novel-characters`）展开后续工作。

## 什么时候用 / 什么时候不用

**用**：
- 新项目从 0 开始
- 已有零散想法但还没建项目结构

**不用**：
- 已经有 `story.md` 的目录里（说明已初始化过，改用领域 skill）
- 用户只想随便聊小说点子（不想动文件系统）→ 引导他先用 `novel-brainstorm`

## 工作流

### Step 1 - 问基本信息（一次性收齐，不要拆成多轮）

用一次问答收齐以下 7 个字段。建议用 `AskUserQuestion` 工具一次问 3-4 题，剩下的让用户自由补充：

| 字段 | 类型 | 说明 |
|---|---|---|
| `title` | string | 书名（用户自己取，可以是临时的） |
| `length-target` | enum | 短篇（<3万）/ 中篇（3-15万）/ 长篇（15-100万）/ 超长篇（>100万） |
| `genre` | string | 主题材（玄幻 / 仙侠 / 都市 / 悬疑 / 历史 / 言情 / 科幻 / 奇幻 / 现实主义 / 其他） |
| `sub-genre` | string | 子类型（如：玄幻→修真升级流；都市→职场；悬疑→社会派） |
| `pov` | enum | 第一人称 / 第三人称限知 / 第三人称全知 / 双视角 |
| `tense` | enum | 过去时 / 现在时（中文默认过去时） |
| `tone` | string | 情感基调（爽 / 悬 / 燃 / 治愈 / 沉重 / 黑色幽默 / ...） |

**注意**：
- 这一步**不要**问世界观、角色、剧情——那些是 `novel-brainstorm` 的事
- 文风（动词驱动 / 克制典雅 / 幽默吐槽 / 热血燃向 / 悬疑压抑）也**不要**在这步问，留给 `novel-brainstorm` 配合 `novel-style-engine` 处理
- 如果用户已经在前面对话里说过某个字段，直接复用，不要重复问

### Step 2 - 确认项目路径

询问用户：

```
项目目录建议放在哪里？
1. 当前目录（默认）：./{书名}/
2. 用户文档：~/Documents/{书名}/
3. Obsidian vault：~/Obsidian/{书名}/  （若用户有 Obsidian）
4. 自定义路径
```

把书名转成目录名时遵循以下规则（按优先级）：
- 中文书名：直接用，例如 `《他养大了皇帝》` → `他养大了皇帝/`
- 英文/混合：转 kebab-case，例如 `"The Last Ember"` → `the-last-ember/`
- 不要清理特殊字符（除非是文件系统非法字符），保留可读性

### Step 3 - 创建目录结构

执行下面的 bash 命令一次性建好所有目录：

```bash
mkdir -p {书名}/{style/samples,style/compiled,characters,worldbuilding/locations,worldbuilding/systems,plot/arcs,chapters,deliverables,.memory/checkpoints}
```

### Step 4 - 写入种子文件

逐一创建以下文件。**全部使用 YAML frontmatter + markdown 内容**。Frontmatter 是机器读的，正文是人读的。

#### `{书名}/story.md` —— 故事圣经

```markdown
---
title: "{书名}"
length-target: {长篇等}
genre: {玄幻等}
sub-genre: {修真升级流等}
pov: {第三人称限知等}
tense: {过去时}
tone: {爽 / 悬 等}
status: planning  # planning / drafting / completed / shelved
created: {YYYY-MM-DD}
---

# {书名}

## 一句话简介
<!-- 用户提供，或在 novel-brainstorm 阶段填充 -->

## 写作目标
<!-- 完成度目标、发表平台、读者画像 -->

## 题材定位
<!-- 类型、子类型、市场参照（同题材爆款） -->

## 核心矛盾
<!-- 全书最大的对立。在 novel-brainstorm 中完善 -->

## 30 章承诺
<!-- 前 30 章读者会得到什么爽感 / 情绪体验。在 novel-plot 中完善 -->
```

#### `{书名}/status.md` —— 状态文件（唯一真相源）

```markdown
# {书名} - 创作状态

**当前阶段**: init
**当前任务**: 项目已初始化，等待 brainstorm
**最后更新**: {YYYY-MM-DD HH:MM}

## 进度统计
- 已完成章节：0 章
- 当前字数：0
- 目标字数：{根据 length-target 推算}

## 确认记录
- {YYYY-MM-DD HH:MM}: 项目初始化完成

## 检查点
（暂无）

## 待办
- [ ] 完成 brainstorm（运行 `novel-brainstorm`）
- [ ] 搭建世界观（运行 `novel-worldbuilding`）
- [ ] 创建主要角色（运行 `novel-characters`）
- [ ] 设计卷纲（运行 `novel-plot`）
```

#### `{书名}/characters/_index.md` —— 角色注册表

```markdown
---
type: character-registry
story: "{书名}"
---

# 角色注册表

## 总览

| 角色 | 角色定位 | 状态 | 文件 |
|---|---|---|---|
| *暂无角色* | | | |

## 家族 / 阵营关系

*暂未定义。*

## 角色关系图

*暂未定义。*
```

#### `{书名}/worldbuilding/_index.md` —— 世界观注册表

```markdown
---
type: world-registry
story: "{书名}"
---

# 世界观

## 世界总览

<!-- 用 1-3 段描述这个世界的大致样子（在 novel-worldbuilding 中完善） -->

## 地点

| 名称 | 类型 | 区域 | 文件 |
|---|---|---|---|
| *暂无地点* | | | |

## 体系

| 名称 | 类型 | 文件 |
|---|---|---|
| *暂无体系* | | |
```

#### `{书名}/plot/_index.md` —— 情节注册表

```markdown
---
type: plot-registry
story: "{书名}"
structure: three-act  # three-act / hero-journey / kishotenketsu / web-novel-escalation 等
---

# 情节结构

## 全书结构模型

**模型**: 三幕结构（可在 novel-plot 中调整）

## 卷 / 故事弧

| 名称 | 类型 | 状态 | 文件 |
|---|---|---|---|
| *暂无* | | | |

## 主题追踪

| 主题 | 关联卷 | 关联章节 |
|---|---|---|
| *暂无* | | |
```

#### `{书名}/plot/timeline.md` —— 时间线

```markdown
---
type: timeline
story: "{书名}"
---

# 全书时间线

| 时间 | 事件 | 卷 | 章节 |
|---|---|---|---|
| *暂无事件* | | | |
```

#### `{书名}/plot/foreshadowing.md` —— 伏笔总表

```markdown
---
type: foreshadowing-ledger
story: "{书名}"
---

# 伏笔账

> 借鉴 inkos hook-ledger 设计。每条伏笔有四态：open（已埋）/ advance（推进中）/ resolve（已回收）/ defer（暂搁）。
> 硬底线：每章 resolve 多少个，必须至少 open 同样多个。

## 已埋伏笔（open）

| ID | 描述 | 埋设章 | 计划回收 | 重要度 |
|---|---|---|---|---|
| *暂无* | | | | |

## 推进中（advance）

*暂无。*

## 已回收（resolve）

*暂无。*

## 暂搁（defer）

*暂无。*
```

#### `{书名}/chapters/_index.md` —— 章节注册表

```markdown
---
type: chapter-registry
story: "{书名}"
---

# 章节

| # | 标题 | POV | 状态 | 字数 | 文件 |
|---|---|---|---|---|---|
| *暂无章节* | | | | | |

**总字数**: 0
```

#### `{书名}/style/_index.md` —— 写法档案注册表

```markdown
---
type: style-registry
story: "{书名}"
---

# 写法档案

> 投喂样本到 `samples/`，运行 `novel-style-engine` 抽取特征。
> 编译后的写作约束在 `compiled/` 目录，会被 novel-chapter 自动注入。

## 当前生效的写法档案

*暂未配置。在 novel-style-engine 中投喂样本并提取特征。*

## 样本清单

| 样本 ID | 来源 | 描述 |
|---|---|---|
| *暂无* | | |
```

### Step 5 - git init（可选，默认开启）

询问"是否要把这个项目初始化为 git 仓库？（推荐 - 方便版本追溯）"，默认 yes：

```bash
cd {书名} && git init && git add . && git commit -m "init: novel-suite scaffold"
```

如果用户拒绝，跳过此步。

### Step 6 - 给用户摘要 + 下一步建议

输出：

```
✅ 项目《{书名}》初始化完成。

📂 目录位置：{abspath}
📋 当前状态：planning（等待 brainstorm）

下一步建议（任选）：
1. 讨论世界观和故事走向 → 说 "讨论一下世界观" 或 "开始 brainstorm"
2. 直接创建主要角色 → 说 "加一个主角"
3. 投喂参考文风样本 → 说 "学这个文风" + 粘贴样本
4. 跳过准备，直接试写一章 → 说 "写第 1 章"（不推荐，建议先 brainstorm）

可以随时说 "看一下进度" 查看 status.md。
```

## 错误处理

- **目标目录已存在且非空**：询问用户"目录 {path} 已存在并非空，是要：(a) 在原基础上继续；(b) 选另一个路径；(c) 终止"。**绝对不要**默认覆盖。
- **目标路径不可写**：报错并要求用户换路径。
- **书名包含文件系统非法字符**：自动清理为最近的合法字符（如 `:` → `：`，`/` → `-`），并告诉用户改了什么。

## 与其他 skill 的关系

- 此 skill **只做脚手架**，不做内容创作。任何关于"世界长什么样"、"角色是什么人"的对话都要明确说"这是 novel-brainstorm / novel-worldbuilding / novel-characters 的事，先把项目建起来"。
- 完成后**显式**把控制权交回主对话，不要自己接着进入下一步。让用户主动触发下一个 skill。
