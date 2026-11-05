# pop-fanqie-recap

> 剧情 review 环节（番茄）：从已落盘正文提取事件、新事实、人物状态、伏笔与下一章钩子。
> 当前版本 2.2.0。

## 负责什么

输入：本章正文、本章章纲、`人物/人物索引.md`、上一版 recap。

输出：

- `.popwave/metrics/recap.json`：每章一条事件 + 一份当前状态，覆盖更新。
- `.popwave/metrics/characters.json`：人物索引的结构化镜像（基础设定之外的状态、关系阶段、来源章节）。
- `剧情日志/全书日志.md` 增量：本章事件与新事实，追加，不改旧行。

本环节是唯一写「当前状态」的地方：每章写人物卡 `currentState`（8 项）与 `timeline` 一条，并把剧情线 beat 标成 `done`。

不调写作工具：本环节由主 agent 按模板提取，避免正文与摘要混在同一产出里。

## 流程

### Step 1 读料

- 先看提示词里的「创作循环」段：当前节点是「剧情快照」时由本环节继续；写完本章快照后流程会自动走到下一章或下一卷。
- `正文/ch{NNN}.md` 全文。
- `章纲/ch{NNN}.md`：核对章纲声明的事件是否都有落点。
- 用 `popwave_project_site_read` 读 `/pages/characters` 与 `/pages/plot`：只核对本章出场人物、未解决伏笔。
- 读 `/pages/snapshots/plot` 与最近两条 `/pages/snapshots/chapters`。
- 数据结构见 `templates/recap.schema.json`。

### Step 2 提取

按 schema 生成本章对象：

- `tags`：本章命中的类型，可多选——`角色动态 / 新事实 / 伏笔钩子 / 冲突 / 场景 / 时间`；没有的类型不写。
- `characters`：本章实际出场的人名；`presentCharacters` 章末仍在场的人。
- `facts`：正文新出现且会影响后文的事实，一条一句，带原文证据短语；推测写「待核」，不写进事实。
- `hooks`：本章新埋或推进的伏笔钩子，指向后文。
- `conflicts`：与章纲、人物卡、世界底线不一致的地方；只记录，不自行改设定。
- `events`：本章真正发生的事，一句话一条；写清时间、地点、结果。
- `characterStates`：出场人物的位置、处境、关系阶段、已知信息、持有物、伤损、目标变化；只写变化项。
- `openThreads`：伏笔与未兑现承诺，标 `open / advanced / resolved`，记首次与最近章节。
- `nextHooks`：章末钩子，指向下一章。

### Step 3 落盘

1. 用 `popwave_project_site_update` 写 `pages.snapshots`：
   - `plot`：本章结束时的当前局面（summary 150–400 字、chapterId、openThreads ≤5、presentCharacters 本章仍在场的人）；
   - `chapters`：追加本章（chapterId／title／summary 60–160 字／tags／characters／facts／hooks／conflicts／openThreads）。
2. 回流人物状态到 `pages.characters.roles`：只写出场人物的 `currentState`（location／situation／relationStage／knowledge／items／injuries／goalChange／chapter），并追加一条 `timeline`（chapter／change）；不改 `base` 与历史行。
   - `currentState` 用 `merge` 覆盖对应角色的字段；`timeline` 用 `op: "append"` 追加到 `/pages/characters/roles/{下标}/timeline`，不要整段重写。
3. 回流剧情线：把本章推进的 `pages.plot.volumes[].lines[].beats` 中对应 beat 标 `done`；没写进正文的标 `dropped`，未推进的保持 `planned`。
4. 回流伏笔状态：`foreshadows` 的 `state` 按正文推进或回收更新；新埋的补进清单。
5. `recap.json`：保留最近章节条目，作为工具/排查用的本地镜像。
6. `剧情日志/全书日志.md`：追加本章事件与新事实；旧行不改。
7. 不再手写流程待办：下一步由宿主按创作循环生成；只有用户明确要求的事项才写进 `todos`。

### Step 4 门禁

1. 章纲声明的每个事件在 `events` 里都有落点，没有就记 `conflicts`。
2. 正文出现的每个名字，在章快照的 `characters` 里有对应条目或有别名映射。
3. 新事实带证据短语；没有证据的写「待核」。
4. 伏笔状态不倒退：`resolved` 不被改回 `open`。
5. 人物 `currentState` 的 8 项只按本章正文写；没有变化的字段继承上一版，不凭推测补。

## 红线

1. 不反写设定、章纲、人物卡基础设定；派生数据只读回填。
2. 不把计划写成已发生。
3. 不总结正文感悟，只记可核对的数据。
4. 不覆盖旧章节的事件与旧日志行。
5. 人物当前状态只由本环节写；其他环节不得越权覆盖。
