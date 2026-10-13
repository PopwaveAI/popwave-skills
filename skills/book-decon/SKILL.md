---
name: book-decon
description: Book deconstruction entry skill (Phase 0, T1.1). Reads the book-level 拆书总控.json ledger first (what was uploaded, which chapters each file covers, what has already been deconstructed, what is still uncovered), then confirms the source package is ready, validates manifest.json and the merged chapter index, reads the frozen 拆解配置.json, then routes to book-decon-dimension. Falls back to in-conversation scope intake when no config exists. Self-contained; does not read or depend on popwave-skills.
---

# book-decon · 拆书入口（第零期 T1.1）

> 本书入口 skill 把原来的「确认文件存在 + 征询范围」升级为「**确认源包就绪 + 读配置**」：先校验源包的 `manifest.json` 与 `合并章节索引.json`，再读宿主冻结的 `拆解配置.json`，然后按 `processingProfile` **分交付物**路由到 `book-decon-dimension`：`standard` / `deep` 走 L1/L2 完整交付，`outline` 走**骨架交付**（卷级骨架），不进入 L2 六模块。无配置时保留对话征询作为兜底。
>
> 本 skill **自包含**：规则参考 `pop-decon` 复刻而来，但运行时**不读取、不依赖、也不修改** `popwave-skills` 的任何 skill 或其版本。原 skill 继续服务既有对话场景，两条链路互不影响。

## 做什么

| 输入 | 来源 | 输出 | 下游 |
|:--|:--|:--|:--|
| 源包目录（`manifest.json`、`合并章节索引.json`、`指纹.json`、`批次计划.json`、`chapters/`）与 `拆解配置.json` | 分章归一脚本 `tool-split-chapters` 产出的源包；宿主冻结的配置 | 已校验的覆盖范围、书信息与重点，以及一份可判读的校验结论 | `book-decon-dimension`（完整交付：L1 批次拆解 + L2 六模块成品；骨架交付：卷级骨架） |

**执行模式**：主 agent 直接执行。入口只做「确认源包就绪 → 读并校验契约 → 冻结配置 → 按交付物分流并路由」，**不做分章、不做八维提取、不写成品**。

**路由地图**：确认源包就绪 → 校验 manifest 与合并章节索引 → 读 `拆解配置.json` 并冻结 → **按 `processingProfile` 分交付物分流**：`standard` / `deep` 走完整规程（L1 七项门禁 → L2 六模块），`outline` 走骨架规程（按卷抽样 → 六项骨架门禁 → `骨架/` 三份产物）→ 收尾核对并汇报。

## 不做什么

- **不做分章归一**。分章由确定性脚本承担且全仓只此一份：`tool-split-chapters` 的 `scripts/split-chapters.mjs`（Node ESM，零第三方依赖）。入口只**消费**源包，不解析裸 TXT。
- **不做八维提取与成品整合**，全部交给 `book-decon-dimension`。
- **不改写正文、不写源包、不改动原 skill**（见「红线」）。

## 契约与路径口径

四份文件契约全部**走文件、不走消息通道**，JSON 键名统一 **camelCase**（出现下划线即为非法契约）。入口只读前四份，第二份由宿主冻结后读入。

| 契约 | 位置 | 入口动作 |
|:--|:--|:--|
| `拆书总控.json` | 书目录根（源包目录根，书级） | **第一步先读**：拿到「这本书上传了什么、每个文件覆盖 xx-xx 章、已拆解了哪些范围、还有哪些章没拆」 |
| `manifest.json` | 源包目录根 | 读并校验合法性与章覆盖 |
| `合并章节索引.json` | 源包目录根（参考书级） | 读并与 manifest 交叉校验 |
| `指纹.json` | 源包目录根 | 读并核对资产指纹 |
| `批次计划.json` | 源包目录根 | 读切批结果，交给执行 skill 按批推进 |
| `拆解配置.json` | 本次拆解版本目录（`<outputRoot>/<taskId>-<范围>/`） | 读、校验、冻结 |
| 批次完成标志 | 版本目录 `_temp/batches/<批次档案名>.批次完成标志.json` | 由执行 skill 产出，入口收尾时核对 |

**允许引用的真实路径只有源包目录与本次版本目录**：`拆书总控.json`、`manifest.json`、`合并章节索引.json`、`指纹.json`、`批次计划.json`、`chapters/`、`_temp/batches/`、六模块目录、骨架交付目录 `骨架/`（仅 `outline`）。**禁止引用不存在的路径**，尤其是 `_temp/chapters/` 这类幽灵引用（分章产物在源包的 `chapters/`，不在版本目录）。

#### 拆书总控台账（`拆书总控.json`）

书籍级台账，**续拆的唯一入口依据**。两段都由宿主在分章/状态变化时重建，**入口只读、不回写、不修补**：

| 段 | 内容 |
|:--|:--|
| `source` | `mergeCount`（合并过几次）；`files[]` 每个上传文件的 `batchNo`（第几次上传）/`fileName`/`shortHash`/`state`（`active` 或 `fingerprint-duplicate`）/`chapterCount`/`fromGlobalNo`…`toGlobalNo`（**本书内 xx 章-xx 章**）/`volumeNos`；`relations[]` 逐文件续接关系（`continues`/`restarts`/`overlaps`/`gap`/`unnumbered`）；`duplicateTitles[]` 跨卷重复章名；`warnings[]` 待裁决提示 |
| `deconstruction` | `runs[]` 每次拆解（`runId`/`versionDir`/`phase`/`stage`/`scope`/`processingProfile`/`assetIds`/`batches`（total/completed/passed/failed/partial）/`artifactCount`）；`coveredRanges[]` 已拆解区间（带 `runId` 溯源）；`uncoveredRanges[]` **尚未拆解的区间** |

判定口径（入口按此决定「续拆 / 新建 / 拒绝」）：

- `uncoveredRanges` 非空 → 存在没拆过的章，续拆时**只需覆盖这一段**，不必重跑已拆范围；
- 同一个 `scope` 已存在 `phase` 为 `completed` 的 run → 该范围已有成品，重复拆解必须先说明理由或换范围；
- `source.relations` 里出现 `overlaps`、或 `duplicateTitles` 非空 → **疑似重复上传的同一卷**，属于源侧待裁决项，入口不得自行认定，按 Step 0.6 分流；
- `source.files[].state` 为 `fingerprint-duplicate` 的文件不计章，但必须在汇报中显式提及（用户以为传了、实际被去重跳过）。

---

## 怎么操作（规程全内联）

### Step 0：确认源包就绪并校验契约

先定位源包目录（参考书受管目录下的资产目录，或宿主/用户显式给出的源包路径），**先读 `拆书总控.json` 建立"这本书的现状"**，再按 0.1 → 0.5 顺序校验。**任何一项不通过都不得进入 Step 1。**

#### 0.0 先读拆书总控台账（每次进入的第一步）

`拆书总控.json` 是这本书的**唯一现状入口**。读它拿到三件事，再决定本次是「续拆」还是「新建」：

| 读什么 | 用来判断 |
|:--|:--|
| `source.files[]` | 这本书由哪几个上传文件组成，**每个文件覆盖本书内第 xx–xx 章**（含上传批次 `batchNo` 与是否被指纹去重） |
| `source.relations[]` / `source.duplicateTitles[]` / `source.warnings[]` | 各文件是不是接着上一卷、有没有重叠或重复上传的迹象（待裁决证据） |
| `deconstruction.runs[]` / `coveredRanges[]` / `uncoveredRanges[]` | **已经拆解过哪些范围、拆到什么程度、还剩哪些章没拆** |

分流口径：

- 台账不存在 → 视为首次拆解，继续 0.1 校验源包；**不得凭猜测补一份台账**（台账由宿主产出）。
- `uncoveredRanges` 非空 → 本次是**续拆**：优先只覆盖未拆区间，并在汇报里写清「本次续拆 xx–xx 章，此前已拆 xx–xx 章」。
- `uncoveredRanges` 为空但用户仍要求拆解 → 全书范围都已有成品，必须先说明「该范围已拆过（列出 runId 与版本目录）」，由用户确认是否重拆；**不得静默重拆、不得覆盖既有版本目录**。
- `source.warnings[]` 非空 → 属于源侧待裁决项（重叠、重复上传、指纹去重），按 0.6 分流处理，**入口不自行认定**。
- 台账与 `manifest.json` 不一致（如 `source.totalChapters` ≠ `manifest.totalChapters`）→ 视为源包已变更，**停止并要求重新分章**，不就地修补台账。

#### 0.1 定位与"就绪"定义

源包"就绪"＝同时满足：

1. 源包目录存在，且含 `manifest.json`、`合并章节索引.json`、`指纹.json`、`批次计划.json`、`chapters/`；
2. `manifest.json` 合法（见 0.2）；
3. `合并章节索引.json` 与 `manifest.json` 一致（见 0.3）；
4. 章覆盖与范围自洽（见 0.4）；
5. 资产指纹与配置可核对（见 0.5）。

#### 0.2 `manifest.json` 合法性

| 校验项 | 通过判据 |
|:--|:--|
| 产出方 | `generator.id` 为 `tool-split-chapters`；非该脚本产出的 manifest 视为来源不明，不启动 |
| 标识 | `referenceBookId` 非空；`book.name` 非空 |
| 章总数 | `totalChapters` 为正整数，且等于 `chapters` 长度 |
| 卷边界 | `volumes[]` 每项含 `no` / `name` / `from` / `to` / `assetId` / `chapterCount`；卷区间连续、不重叠、不越界 |
| 章清单 | `chapters[]` 每项含 `no` / `title` / `file` / `chars` / `flags` / `volumeNo` / `volumeLocalNo` / `assetId` / `selected`；`no` 从 1 连续 |
| 质量问题 | `quality` 对象存在，且 `missing` / `duplicated` / `truncated` / `contamination` / `outOfOrder` 字段齐全 |
| 边界置信 | `agentArbitrationRequired` 必须为 `false`，且 `confidence` ≥ 0.6；否则边界未收敛，默认停下（见 0.6 与 0.7 分流） |
| 产物指针 | `artifacts` 指向 `chaptersDir` / `chapterIndex` / `mergedChapterIndex` / `fingerprints` / `batchPlan`，且这些文件确实存在 |
| 键名 | 全部键名匹配 `^[a-z][A-Za-z0-9]*$`（camelCase，不含下划线） |

#### 0.3 `合并章节索引.json` 合法性与交叉校验

必需字段：`referenceBookId`、`bookName`、`totalChapters`、`volumes[]`（`no` / `name` / `from` / `to` / `assetId` / `chapterCount`）、`chapters[]`（`globalNo` / `volumeNo` / `volumeLocalNo` / `assetId` / `title` / `file` / `chars` / `flags` / `selected`）。

交叉校验（两条索引必须是同一份事实）：

- `totalChapters` 与 manifest 相等；`volumes[]` 逐卷对齐；
- 逐章：`globalNo` 等于 manifest 对应章的 `no`，且 `title` / `file` / `assetId` / `chars` 一致；
- `globalNo` 从 1 连续；`volumeLocalNo` 逐卷重置；`assetId` 能在 `volumes[]` 里找到归属卷；
- 任一不一致 → 视为「索引与清单不同源」，**停止并要求重新分章**，不就地修补。

#### 0.4 章覆盖与范围校验

以 `合并章节索引.json` 为唯一基准，按 `拆解配置.json` 的 `scope` 判定：

| scope | 通过判据 |
|:--|:--|
| `full` | 覆盖全部章；`chapters[].selected` 全为 `true` |
| `volume` | 卷号在 `volumes[]` 中存在；范围落在该卷 `from..to` 之内 |
| `chapters` | 起止落在 `1..totalChapters`，且 `from ≤ to`（闭区间，按全书序号） |

附加硬规则：

- **越界即拒绝**，不自动收敛、不静默截断（例如 6 章的书要「前 10 章」必须被拒绝，并回报实际总章数与请求范围）；
- 覆盖章数不设下限，任意章数均可启动（锚点池等门禁按实际覆盖范围判定，不因章数少而放宽）。
- 覆盖章必须落在 `assetIds` 覆盖的资产集合内，且每章 `selected` 与范围一致。

#### 0.5 资产指纹校验

读 `指纹.json`（`algorithm` / `shortHashLength` / `assets[]`（含 `assetId` / `fileName` / `sha256` / `shortHash` / `duplicateOf`）/ `duplicateGroups` / `uniqueCount`），与 `拆解配置.json` 的 `assetIds`、`assetFingerprints` 逐项核对：

- 配置里的每个 `assetId` 必须在 `指纹.json` 中存在；
- `assetFingerprints` 的取值必须与 `sha256`（或 8 位短指纹）一致；
- **指纹重复不重复计入覆盖**：`duplicateOf` 非空、或被 `duplicateGroups` 去重的资产不重复算章；
- 指纹对不上（源包被替换或改动）→ **提示重新分章，不静默沿用旧索引，不启动**。

#### 0.6 分流结论（必须显式给出其中一条）

| 情况 | 动作 |
|:--|:--|
| 源包齐备且全部校验通过 | 进入 Step 1 |
| 台账不存在 | 视为首次拆解，按源包校验继续；**不补台账、不猜台账** |
| 台账与 manifest 章数/资产不一致 | 停止，视为源包已变更，要求重新分章 |
| `uncoveredRanges` 非空 | 按**续拆**处理：本次只覆盖未拆区间，汇报里写明此前已拆范围 |
| 请求范围已有 `completed` 的 run | 先列出已拆 runId 与版本目录，需用户确认是否重拆；不静默重拆 |
| `source.warnings` 含重叠或重复上传 | 停止并转人工确认（源侧待裁决项，入口不自行认定） |
| 未提供源包 / 源包不存在 | 给出去缺了什么，回退对话征询（Step 3）；**不报错、不崩溃** |
| manifest 或索引非法（字段/结构/键名） | 列出非法字段与文件，停止，不进入 Step 1 |
| `agentArbitrationRequired` 为 `true` 或 `confidence` < 0.6 | 停止，转人工确认（边界修订只由脚本 `--revisions` 回灌，入口不猜边界）；**`拆解配置.json.qualityOverride` 为 `true` 时改走 0.7 强制分支** |
| 两条索引互相矛盾 | 停止，要求重新分章 |
| 范围非法/越界 | 停止，给出实际总章数与请求范围 |
| 指纹不一致 | 停止，提示重新分章 |

#### 0.7 强制拆解（`qualityOverride`）

宿主在配置页把「分章边界未收敛」的判定与风险摆给用户看，用户勾选「仍然强行拆解」后，`拆解配置.json.qualityOverride` 写为 `true`。这是**用户决策的留痕**，不是让入口跳过校验的开关。

| 项 | 口径 |
|:--|:--|
| 放行范围 | 只放行 0.2「边界置信」这一条：`agentArbitrationRequired = true` 或 `confidence < 0.6`，不再据此中止 |
| 明确不放行 | `source.warnings` 含重叠或重复上传：那是**源数据本身错了**（同一章会被算两遍），不是边界不确定，只能回源处理。宿主界面同样拦它并给出「移除重复分卷后重新上传」的指引，不提供强制入口 |
| 照旧拦截 | `generator.id` 非 `tool-split-chapters`、`referenceBookId` / `book.name` 为空、`totalChapters` 与 `chapters` 长度不符、两条索引互相矛盾、章清单字段缺失或 `no` 不连续、范围越界、指纹对不上 —— 这些是**完整性**问题，`qualityOverride` 一律不放行 |
| 必须先说清 | 进入 Step 1 前用一段话回报：边界未收敛的具体理由（读 `manifest.reasons` 与 `quality` 各项计数）、被接受的风险、本次将如何留痕 |
| 必须留痕 | 根 `索引.md` 与 `CHANGELOG.md` 各写明「本次为强制拆解」并列出来源问题；L2 成品里凡锚点落在边界存疑处的结论，一律标「待复核」 |
| 不得扩权 | 不得把本分支当作放宽门禁、减少 L1 维度或降低 7 项检查的理由；每批门禁照常执行，没过就是没过 |
| 汇报口径 | 汇报里保留 `qualityOverride = true` 与理由原文，便于事后判断这批结论能不能用 |

### Step 1：读 `拆解配置.json` 并冻结

`拆解配置.json` 由宿主冻结后传入，**启动即不可变**：本 skill 只读，不在运行中改写任何字段，也不允许后续表单改动影响已开始的运行。

| 字段 | 语义 | 入口校验 |
|:--|:--|:--|
| `taskId` | 本次拆解任务 ID，**也是版本目录名的前缀**（版本目录 = `<taskId>-<范围>`，宿主冻结为 `V<序号>` 形式，例 `V1`） | 非空 |
| `referenceBookId` | 参考书 ID | 必须等于 `manifest.referenceBookId` |
| `assetIds` | 本次覆盖的资产 ID 集合（顺序即资产顺序） | 非空、每项在指纹表中存在、不重复 |
| `assetFingerprints` | 逐资产指纹（`assetId → sha256/短指纹`） | 与 `指纹.json` 一致（见 0.5） |
| `scope` | `full \| volume \| chapters`；卷/章范围用起止字段表达 | 与 0.4 判定一致 |
| `focusDimensions` | 七个产品标签的子集（见下表） | 只允许白名单标签，至少一项；`standard` / `deep` 下**不得反向裁剪 L1**；`outline` 下只作骨架重点序 |
| `processingProfile` | `standard \| deep \| outline` | **决定交付物与切批档位（三值，见下方「交付物口径」）** |
| `qualityOverride` | 用户是否已确认「明知分章边界未收敛仍继续」（强制拆解） | 布尔恒在；为 `true` 时按 0.7 强制分支执行并留痕，不得当作放宽门禁的许可 |
| `skillVersions` | 三份拆书 skill 的版本记录 | 记录实际解析到的版本，供宿主核对 |
| `outputRoot` | 本次拆解的输出根（版本目录的父目录） | 非空、可写；版本目录由宿主给出 |

#### 交付物口径（`processingProfile` 三值）

`processingProfile` 决定的是**交付物**（以及随之而来的切批与门禁），不只是速度档位：

| 取值 | 交付物 | 切批 | 门禁 | 产出 |
|:--|:--|:--|:--|:--|
| `standard` | **六模块完整** | 约 30 章/批 | 完整 7 项 | 六模块 + `爽点.md` + `立项/` + 根 `索引.md` + `CHANGELOG.md` |
| `deep` | **六模块完整**（质量优先） | ≤ 20 章/批 | 完整 7 项 | 同上 |
| `outline` | **卷级骨架（另一种交付物）** | ≤ 40 章/批（按卷归档） | 骨架 6 项 | 版本目录 `骨架/` 下 `卷级骨架.md`、`索引.md`、`_未取证声明.md`；**不产出六模块与立项** |

> **`outline` 是另一种交付物，不是"更快的六模块"。** 它只做**按卷抽样**的**卷级骨架**（卷级九字段 + 主线链 + 主要角色 + 力量体系要点 + 世界观要点），**不做八维全提、不做 L2 六模块、不产出立项**，走的是**另一套 6 项门禁**（见执行 skill 的「骨架交付」节）。骨架产物默认**未取证**，只能用于快速判卷与范围决策，**不得当作六模块证据**；需要六模块时必须另起一次 `standard` / `deep` 拆解并新建版本。

**七个产品标签（`focusDimensions` 白名单）与其 L2 落点**：

| 标签 | L2 落点 |
|:--|:--|
| 剧情结构 | 剧情库（分卷、动力引擎、各卷切片、索引） |
| 人设&关系 | 角色与势力库 |
| 力量体系 | 力量与战斗 |
| 世界观 | 世界观 |
| 爽点&钩子 | 爽点.md |
| 赛道特色 | 赛道特色 |
| 文本DNA | 文风DNA |

`focusDimensions` 的作用范围**仅限结果呈现与组织**（`standard` / `deep` 下决定 L2 六模块的产出顺序与深度；`outline` 下只决定卷级骨架各要点的呈现顺序与侧重），**不改变 L1 的八维提取，也不减少 L2 的六模块交付**，更不减少 7 项门禁；`outline` 下也不改变骨架的提取范围与骨架 6 项门禁。

### Step 2：按交付物分流并路由到执行 skill

路由目标都是 `book-decon-dimension`，但**交付物不同 → 规程不同**，入口必须按 `processingProfile` 显式分流，两套规程不可混用：

| 交付物 | `processingProfile` | 执行规程 | 门禁与产出 |
|:--|:--|:--|:--|
| 六模块完整 | `standard` / `deep` | L1 批次拆解（八维全提）→ L2 六模块成品 | 7 项完整门禁；六模块 + `爽点.md` + `立项/` + 根索引 + CHANGELOG |
| 卷级骨架 | `outline` | 骨架交付规程（按卷抽样；见执行 skill 的「骨架交付」节与 `references/骨架交付.md`） | 6 项骨架门禁；`骨架/卷级骨架.md`、`骨架/索引.md`、`骨架/_未取证声明.md` |

**禁止把 `outline` 当作 `standard` 的低成本替代去跑完整门禁与六模块**，也**禁止把 `standard` / `deep` 降级成骨架交付**；需要六模块就不得用 `outline` 交付。执行 skill 的切批唯一依据是 `批次计划.json`，不另行切批。

传入内容（不含正文，只传路径与范围）：

```
书名 / referenceBookId / 源包目录（绝对路径）
taskId / outputRoot（版本目录）
scope（type + 起止）
focusDimensions（七个标签的子集）
processingProfile   ← 决定交付物与规程：standard / deep 走完整交付，outline 走骨架交付
skillVersions
批次计划.json 路径（切批基准）
```

### Step 3：无配置时的对话征询兜底

没有 `拆解配置.json`（首次对话、或源包缺失需先补）时，保留对话征询，**不得默认全量执行**。按顺序问齐四项，缺一项就退回征询：

1. **书名与源包位置**（源包目录或待归一的 TXT；TXT 先经 `tool-split-chapters` 归一，入口不自行分章）；
2. **范围**：全书 / 某一卷 / 前 N 章（N 不得超过合并章节索引的实有章数，必须由用户显式确认）；
3. **拆书重点**：七个产品标签中至少选一项；
4. **交付物 / 档位**：`standard`、`deep` 或 `outline`（见「交付物口径」；`outline` 交付卷级骨架，**不是更快的六模块**，需向用户说明它不做六模块与立项）。

四项问齐后，按 Step 1 的 schema 落一份 `拆解配置.json` 交宿主确认并冻结，再进入 Step 2。**用户未明确范围时只退回征询**，不擅自开始。

### Step 4：收尾核对与汇报

按交付物核对，**两套口径不可混用**：

- **六模块完整（`standard` / `deep`）**：
  - 核对每批都有「批次完成标志」，且 `status` 为 `passed` 的批覆盖了本次全部范围；
  - 核对六模块、`爽点.md`、`立项/`（L0-L3 与逆向破解）、根索引与变更记录均已落盘；
  - 核对版本目录 `_meta/templates.json` 是否存在，且记录了本次使用的模板 id 与版本、以及哪些文件做了降级或待扩展（如范围非全书时 L3 未产出）。
  - 汇报：覆盖范围（资产与全书序号）、批次数、**7 项门禁结果**、产物清单、模板版本与降级 / 待扩展项、`warnings`（有则逐条列出，不悄悄当作通过）。
- **卷级骨架（`outline`）**：
  - 核对每卷都有骨架档案与「批次完成标志」，且 `status` 为 `passed`；
  - 核对 `骨架/卷级骨架.md`、`骨架/索引.md`、`骨架/_未取证声明.md` 均已落盘，且**未产出六模块与立项**；
  - 汇报：覆盖范围（资产与全书序号）、卷数与抽样比例、**6 项骨架门禁结果**、被跳过章节区间、产物清单、`warnings`。
  - 汇报中必须声明**本产物为未取证骨架**，不得据此对外称"六模块拆解已完成"。

## 红线（断裂级）

1. **不引用不存在的路径** — 特别是 `_temp/chapters/` 这类幽灵引用；分章产物只走源包真实的 `chapters/`，批次档案只走版本目录的 `_temp/batches/`。
2. **不改写正文** — 源包与原文一律只读，任何"顺手改一下"都不允许。
3. **不写源包** — 不得改动 `manifest.json`、`合并章节索引.json`、`指纹.json`、`批次计划.json`、`chapters/`；源包只能由分章脚本写出。
4. **重点只作用交付物呈现** — `standard` / `deep` 下任何按重点裁剪 L1 八维提取、减少 7 项门禁或删减 L2 六模块交付的做法都被禁止；`outline` 按骨架 6 项门禁执行，属**另一交付物**，不得借"重点"名义把完整交付降级，也不得反向把骨架补齐成六模块。
5. **不伪造配置与范围** — 源包缺失/非法、范围越界、指纹不一致、边界未收敛时必须停止并说明原因，不猜测、不自动收敛、不默认全量。**唯一例外**是「边界未收敛」且 `拆解配置.json.qualityOverride === true`（用户在宿主界面签字认可，见 0.7）：此时继续执行，但必须按 0.7 留痕；其余各项没有任何例外。
6. **无配置不静默全量** — 走 Step 3 对话兜底，用户不回答就停在征询，不得先跑后问。
7. **不依赖原 skill** — 不读取、不引用 `popwave-skills` 的原 skill 路径与版本；本 skill 的规则全部内联。
8. **不设章节数下限** — 任意章数均可启动拆解，门禁按实际覆盖范围判定，不因章数少而放宽或降级。
9. **`outline` 产物未取证，不得作为六模块证据** — 骨架产物（版本目录 `骨架/` 下三份）默认**未取证**，只能用于快速判卷与范围决策；不得把卷级骨架当作六模块的事实依据，也不得据此写六模块成品。后续对同范围补做六模块时**必须新建版本**，并把骨架版本记为**父版本**，在档案中标注「输入为未取证骨架」，不得直接复制骨架结论充数。
10. **只读拆书总控台账** — `拆书总控.json` 的 `source` 与 `deconstruction` 两段都由宿主重建，入口与执行 skill 一律**只读**：不得改字段、不得补字段、不得因"看起来不对"就地修正。台账与源包不一致时按 Step 0.0 / 0.6 停止并回报，由宿主重新分章或重新同步。

## 速查表

| 我要 | 读什么 | 什么时候用 |
|:--|:--|:--|
| 这本书上传了什么、每个文件覆盖哪些章 | 书目录根 `拆书总控.json` 的 `source.files[]` | Step 0.0（每次进入的第一步） |
| 各卷是不是接着上一卷、有没有重复上传 | 书目录根 `拆书总控.json` 的 `source.relations[]` / `duplicateTitles[]` / `warnings[]` | Step 0.0 / 0.6 |
| 已经拆解了哪些范围、还剩哪些章没拆 | 书目录根 `拆书总控.json` 的 `deconstruction.coveredRanges[]` / `uncoveredRanges[]` | Step 0.0（决定续拆还是新建） |
| 源包契约字段与键名口径 | 源包根 `manifest.json` | Step 0.2 |
| 章清单与卷内序号基准 | 源包根 `合并章节索引.json` | Step 0.3 / 0.4 |
| 资产指纹与去重分组 | 源包根 `指纹.json` | Step 0.5 |
| 切批结果（约 30 / ≤20 / ≤40） | 源包根 `批次计划.json` | Step 2 传给执行 skill |
| 本次范围、重点、档位 | 版本目录 `拆解配置.json` | Step 1 |
| 交付物三值（完整 7 项门禁 / 骨架 6 项门禁） | 版本目录 `拆解配置.json` 的 `processingProfile` + 本文「交付物口径」 | Step 1 / Step 2 / Step 4 |
| 本次是否为用户确认的强制拆解 | 版本目录 `拆解配置.json` 的 `qualityOverride` + 本文 0.7 | Step 0.6 / Step 1 / Step 4 |
| 每批门禁结果 | 版本目录 `_temp/batches/*.批次完成标志.json` | Step 4 与续拆 |
| 模板版本与降级 / 待扩展留痕 | 版本目录 `_meta/templates.json` | Step 4 收尾核对 |

## 待补清单

| 缺什么 | 影响 | 临时口径 |
|:--|:--|:--|
| 入口侧无模板依赖 | 无 | 入口不产出成品也不读模板；L2 成品模板归独立技能包 `book-decon-dim-templates`（31 份，按 `<book-decon-dim-templates 包根>/templates/` 读取），入口只在 Step 4 核对版本目录 `_meta/templates.json` |
| 卷级骨架模板（在 `book-decon-dim-templates` 侧） | 骨架交付的呈现一致性 | 仍列在执行 skill 的待补清单；入口侧不阻塞 |

## 版本

当前版本 v0.4.0（第零期 T1.1；本版新增**强制拆解分支** 0.7：用户在宿主界面确认「明知分章边界未收敛仍继续」后，`拆解配置.json.qualityOverride` 为 `true`，入口只放行「边界置信」一条并强制留痕，红线第 5 条同步写明唯一例外）。上一版 v0.3.0 新增书籍级拆书总控台账 `拆书总控.json`。版本口径与同目录 `skill.json` 的 `version` 单点一致。
