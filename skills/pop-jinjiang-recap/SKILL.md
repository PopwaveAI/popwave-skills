# pop-jinjiang-recap

> 剧情 review 环节（晋江）：从已落盘正文提取事件、新事实、人物状态、伏笔与下一章钩子。
> 当前版本 2.0.0。

## 负责什么

输入：本章正文、本章章纲、`人物/人物索引.md`、上一版 recap。

输出：

- `.popwave/metrics/recap.json`：每章一条事件 + 一份当前状态，覆盖更新。
- `.popwave/metrics/characters.json`：人物索引的结构化镜像（状态、关系阶段、来源章节）。
- `剧情日志/全书日志.md` 增量：本章事件与新事实，追加，不改旧行。

不调写作工具：本环节由主 agent 按模板提取，避免正文与摘要混在同一产出里。

## 流程

### Step 1 读料

- `正文/ch{NNN}.md` 全文。
- `章纲/ch{NNN}.md`：核对章纲声明的事件是否都有落点。
- 用 `popwave_project_site_read` 读 `/pages/characters` 与 `/pages/plot`：只核对本章出场人物、未解决伏笔。
- 读 `/pages/snapshots/plot` 与最近两条 `/pages/snapshots/chapters`。
- 数据结构见 `templates/recap.schema.json`。

### Step 2 提取

按 schema 生成本章对象：

- `events`：本章真正发生的事，一句话一条；写清时间、地点、结果。
- `newFacts`：正文新出现且会影响后文的事实，带原文证据短语；推测写「待核」，不写进事实。
- `characterStates`：出场人物的位置、处境、关系阶段、已知信息、持有物品的变化；只写变化项。
- `openThreads`：伏笔与未兑现承诺，标 `open / advanced / resolved`，记首次与最近章节。
- `nextHooks`：章末钩子，指向下一章。
- `conflicts`：与章纲、人物卡、世界底线不一致的地方；只记录，不自行改设定。

### Step 3 落盘

1. 用 `popwave_project_site_update` 写 `pages.snapshots`：
   - `plot`：本章结束时的当前局面（summary 150–400 字、chapterId、openThreads ≤5）；
   - `chapters`：追加本章（chapterId／title／summary 60–160 字／openThreads）。
2. 同步人物状态到 `pages.characters.roles`（只写变化项；不确定的不写）。
3. `recap.json`：保留最近章节条目，作为工具/排查用的本地镜像。
4. `剧情日志/全书日志.md`：追加本章事件与新事实；旧行不改。

### Step 4 门禁

1. 章纲声明的每个事件在 `events` 里都有落点，没有就记 `conflicts`。
2. 正文出现的每个名字，在 `characters.json` 里有对应条目或有别名映射。
3. 新事实带证据短语；没有证据的写「待核」。
4. 伏笔状态不倒退：`resolved` 不被改回 `open`。

## 红线

1. 不反写设定、章纲、人物卡；派生数据只读回填。
2. 不把计划写成已发生。
3. 不总结正文感悟，只记可核对的数据。
4. 不覆盖旧章节的事件与旧日志行。
