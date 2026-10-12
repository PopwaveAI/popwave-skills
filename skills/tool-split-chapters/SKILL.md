---
name: tool-split-chapters
description: Deterministic chapter splitter for book deconstruction. Turns raw TXT volumes into a standard source package (manifest.json + chapters/ + indexes) with zero model calls.
---

# tool-split-chapters · 分章归一（第零期 T1.3）

把「一坨 TXT 文本」变成「可寻址的章」，产出标准源包。分章主路径是**纯脚本、零 token、可复现**的：同一组输入加同一组参数，除 `generatedAt` 外产物逐字节一致。

## 什么时候用它

- 拿到整册 TXT（爬取产物、直链整册、用户自带文件），需要在进入 L1 精读前先切出可寻址的章。
- 需要一份给 UI 与拆解层共用的稳定契约（`manifest.json`）：卷章边界、每章字数、质量问题、编码、置信度。
- 需要按档位切批，产出可恢复的批次计划。

## 不做什么

- 不做拆解。八维提取与 7 项门禁不在这里，本 skill 只负责「把文本变成章」。
- 不做下载、不做抓取。源清洗（`--clean`）只做**确定性**的噪声行清理与结构改写，不改正文用词、不做语义判断。
- 不写源包之外的东西。源包（`manifest.json` / `chapters/` / 索引 / 指纹 / 批次计划）**只能由本脚本写出**，Agent 不允许手写或改这些文件。
- 不替用户做清洗决定。清洗默认不启用，只在 `manifest.cleaning` 里给出「可清洗项」预览；是否真正清洗由调用方按用户的选择传入 `--clean`。

## 用法

脚本：`scripts/split-chapters.mjs`（纯 Node ESM，零第三方依赖，Node >= 20）。对话路径用 `node` 执行（`skill.json` 里 `permissions.shell = true` 就是为此）。

```bash
node scripts/split-chapters.mjs \
  --input <卷1.txt> [--input <卷2.txt> ...] \
  --out <源包目录> \
  [--profile standard|deep|outline] \
  [--reference-book-id <id>] [--title <书名>] \
  [--scope full|volume|chapters] [--from N] [--to N] \
  [--revisions <内联JSON|revisions.json 路径>] \
  [--json] [--dry-run] [--clean]
```

| 参数 | 说明 |
| --- | --- |
| `--input` | 必填，可重复。**每个 TXT 视为一卷资产**，顺序即拼接顺序 |
| `--out` | 必填（`--dry-run` 时可省略）。产物目录，会重建其下 `chapters/` |
| `--profile` | 档位，默认 `standard`；`deep` 走「质量优先」六模块切批（≤20 章/批），`outline` 走「卷级骨架」另一种交付物（≤40 章/批） |
| `--reference-book-id` | 参考书 ID，写入 manifest，并作为书名兜底 |
| `--title` | 书名，默认取首资产文件名 |
| `--scope` / `--from` / `--to` | 范围类型与起止。`chapters` 按全书章号，`volume` 按卷号，闭区间 |
| `--revisions` | 边界修订（内联 JSON 或 `.json` 文件路径），见下文「Agent 裁决回灌」 |
| `--json` | 只输出机器可读的 JSON 运行摘要 |
| `--dry-run` | 只计算不写盘，用于人机预览 |
| `--clean` | 先做确定性源清洗再分章。**默认不启用**：不启用时仍会算出 `manifest.cleaning` 里的「可清洗项」预览（只读、不改盘），供调用方展示给用户决定要不要洗 |

退出码：`0` 成功 / `1` 运行期错误 / `2` 参数或范围非法（如 6 章的书要「前 10 章」，直接拒绝且不写任何产物）。

## 产物契约

```
<out>/
  manifest.json          唯一对外契约：章清单、卷边界、每章字数、质量问题、编码、置信度、裁决标记、revisions、非章标题、内部卷标记
  chapters/ch001.txt …   按章正文（首行为标题行，正文中的 CRLF 已归一为 LF）
  章节索引.json           逐资产视图：卷内序号、标题、文件、字数、标记
  合并章节索引.json       多资产按序拼接：每章带 globalNo / volumeNo / volumeLocalNo / assetId
  指纹.json              每资产 SHA-256 与后 8 位、重复分组
  批次计划.json          三档切批结果（standard / deep / outline）
```

`manifest.json` 关键字段：

```jsonc
{
  "generator": { "id": "tool-split-chapters", "version": "0.1.0", "node": "v22.x" },
  "referenceBookId": "…",
  "profile": "standard", "activeTier": "standard",
  "book": { "name": "…", "source": ["卷1.txt"], "sourcePaths": ["…"] },
  "totalChapters": 120, "totalChars": 312345,
  "encoding": { "primary": "gbk", "assets": { "卷1": "gbk" }, "methods": { "卷1": "fallback" } },
  "splitMethod": "title-regex",
  "confidence": 0.94,
  "confidenceSignals": { "unrecognizedRatio": 0, "detectedRatio": 1, "…": "…" },
  "agentArbitrationRequired": false,
  "reasons": [],
  "arbitrationReasons": [],
  "revisionsApplied": [ { "op": "split", "asset": "卷1", "line": 812, "title": "…", "status": "applied", "note": "" } ],
  "scope": { "type": "chapters", "from": 1, "to": 30, "selectedChapters": 30 },
  "volumes": [ { "no": 1, "name": "第一卷 …", "from": 1, "to": 60, "assetId": "卷1", "chapterCount": 60 } ],
  "chapters": [ { "no": 1, "title": "第一章 …", "file": "ch001.txt", "chars": 2680, "flags": [],
                  "volumeNo": 1, "volumeLocalNo": 1, "assetId": "卷1", "assetChapterNo": 1,
                  "lineStart": 3, "lineEnd": 62, "number": 1, "weakTitle": false, "selected": true } ],
  "quality": { "missing": [], "duplicated": [], "truncated": [], "contamination": [],
               "outOfOrder": [], "weakTitles": [], "unrecognizedHeadings": [], "encodingFallbacks": [] },
  "cleaning": { "applied": false, "version": 1, "rulesVersion": "2026-10-09.1", "assetsChanged": 0,
                "removedLines": 0, "removedByRule": {}, "trimmedLines": 0, "mergedPageDuplicates": 0,
                "droppedTocBlocks": 0, "droppedTocLines": 0, "suspicion": [], "samples": [], "cleanedTextHash": null },
  "nonChapterHeadings": [ { "assetId": "全书", "line": 5658, "title": "上架感言", "type": "author-note" },
                          { "assetId": "全书", "line": 63036, "title": "番外：清旺来", "type": "side-story" } ],
  "volumeMarkers": [ { "assetId": "全书", "line": 11148, "name": "第一卷", "complete": true } ],
  "duplicates": [ { "assetId": "卷1副本", "duplicateOf": "卷1", "sha256": "…", "shortHash": "…" } ],
  "meta": { "leadingText": {}, "numberedHeadingsAdopted": {}, "internalVolumeAssets": ["全书"] },
  "batchSummary": { "activeTier": "standard", "batchSize": 30, "batchCount": 4 },
  "artifacts": { "chaptersDir": "chapters", "chapterIndex": "章节索引.json", "mergedChapterIndex": "合并章节索引.json",
                 "fingerprints": "指纹.json", "batchPlan": "批次计划.json" }
}
```

契约里的三条硬规则：

1. `agentArbitrationRequired` / `reasons`（别名 `arbitrationReasons`）是裁决开关与理由列表，一票即可让调用方停下来找 Agent。
2. `chapters[].chars` 是**正文非空白字符数（不含标题行）**；`flags` 是质量问题标记数组（`preface` / `no-boundary` / `weak-title` / `revision-boundary` / `revision-title` / `duplicated-title` / `out-of-order` / `missing-before:N` / `empty-body` / `short-body` / `contamination` / `contains-non-chapter-heading` / `title-residue:<残留词>` / `encoding:fallback`）。
3. `chapters/` **始终全量写出**（源包完整、可复现）；`--scope` 只决定 `chapters[].selected` 与批次计划的覆盖范围，不裁剪源包。

## 识别与判定口径

- **编码**：BOM（UTF-8 / UTF-16）优先；其次严格 UTF-8 解码；失败后回退 `gbk → gb18030 → big5`，按「合法字符占比 - 替换字符惩罚」打分择优。无 full-icu 构建下解码器不可用时走 lossy 兜底，并在 `quality.encodingFallbacks` 里留痕（实现里所有解码都在 try/catch 内）。
- **标题行**：`第X章/节/回/话/集/幕`（中文数字与阿拉伯数字、全角归一、`【】（）` 等装饰可剥）、`Chapter N` / `Chap. N`、`楔子/序章/序言/引子/前言/尾声/终章/结局/番外/后记/外传`；**卷标记**：`第X卷/部/篇/册`、`Volume N`、`上/中/下(部|卷|册|篇)`。卷标记行后面只允许跟短卷名（不含句读、≤20 字），避免把「第二卷写完了，…」这类作者感言当成卷边界。
- **Markdown 标题**：行首 `#{1,6}` 前缀与整行加粗包裹（`# 第一章 师傅`、`## 第二章 雨落`、`**第三章 夜行**`）都会被剥掉后再匹配。**只有带章节号的 Markdown 标题才算章**；不带章节号的是作者的话/公告/番外，登记进 `manifest.nonChapterHeadings`（行号 / 原始标题 / 类型猜测 `author-note` / `side-story` / `other`），**不建边界、不打断编号**，其正文归入上一章并给该章打 `contains-non-chapter-heading`。
- **标题残留清理**：明文标题末尾若出现已知盗版站残留词（`免费阅读`/`全文免费阅读`/`全本免费阅读`/`无弹窗`/`请记住本站`/`最新章节`/`手机版阅读` 等），连同紧邻的尾部标点一起剥离（如 `第六百三十章 中阴庙免费阅读.` → `第六百三十章 中阴庙`），命中证据写进 `flags`（`title-residue:免费阅读`）。清理是保守的：只在**行尾**命中才剥、尾部标点必须紧邻残留、剥离后必须仍保留原编号 token，否则整条放弃（宁可留残留也不误删正常标题文字，如 `第一百二十三章 免费阅读的秘密` 原样保留）。
- **内部卷标记**：`第一卷（完）`、`（第三卷完）` 这类「卷号 + 完结标注」的纯标记行记为 `manifest.volumeMarkers`（行号 / 卷名 / 是否标注完），并在 `meta.internalVolumeAssets` 标出含内部卷的资产，**不改变「一个资产 = 一卷」的建模**——它只作为后续「按卷选择」的参考，不再当卷边界。
- **分隔符**：`******`、`------`、`_______` 等纯符号行不是标题，也不会进 `nonChapterHeadings`。
- **弱式数字标题**（`12、标题`）：只有当同一资产里出现 ≥3 行、编号大体递增、**且该资产没有任何强章边界**时才采纳（避免把作者公告里的「1、2、4、5、」清单当章节）；采纳情况记在 `meta.numberedHeadingsAdopted`。
- **正文前内容**：只有在确实存在章边界、且长度 ≥200 非空白字符时才单独成章（flag `preface`）；不足 200 字符只记在 `meta.leadingText`。
- **归一**：CRLF/CR → LF；标题行的全角数字/字母 → 半角；中文标点原样保留。
- **质量检查**：编号缺号（`missing`）、重复章名（`duplicated`）、正文过短或为空（`truncated`，阈值 20 非空白字符）、站点污染（`contamination`）、编号乱序（`outOfOrder`）。
- **源清洗（`--clean`，默认关闭）**：三类确定性动作，全部写入 `manifest.cleaning`，可解释、可复现、幂等。① 整行删噪声：站点声明、报错浮层（窗口内 ≥3 个不同固定文案才认）、压缩脚本、整行纯 URL、推广行；② 行内切首尾：`(第N/N页)` 分页标记、行尾站点尾巴、行首域名；③ 结构改写：分页重复标题合并（同标题同章号且至少一侧带分页标记）、目录块剔除（连续 ≥3 个自身无正文的标题，且这些标题在后文以「标题 + 正文」再次出现）。**标题行永不被整行删除**，行内只切首尾不切中间；命中噪声词但整行偏长、或正文占比过高时只记 `suspicion`、不动手。清洗后文本指纹写进 `指纹.json` 的 `cleanedTextHash`，原上传文件的 `sha256` 保持不变。
- **指纹去重**：相同 SHA-256 的资产只算一次章，后续资产记 `duplicates[].duplicateOf` 并写入 `ignoredInputs`；**同名不同内容**的资产用 `文件名~指纹后8位` 作为 `assetId` 区分，保证合并索引与指纹表里各自可寻址。

## Agent 裁决触发条件

| 触发 | 阈值（`meta.thresholds` 里可见） |
| --- | --- |
| 未识别标题行占比 | > 5%（见 `quality.unrecognizedHeadings`） |
| 切出章数低于预期 | < 预期的 80% |
| 编号乱序或重复章名 | 出现任意一处 |
| 缺章号 | 出现任意一处（见 `quality.missing`，单个缺口的号列表截断到 50 个） |
| 正文为空 | 出现任意一章 `chars === 0`（只认完全空，避免误伤正常短章） |
| 置信度低于地板 | < 0.6（覆盖「完全没识别到标题行 → 单章整块正文」这类情形） |

任一命中：`agentArbitrationRequired = true`，`reasons` 逐条写明是哪个阈值被击穿。

**裁决流程（零 token 主路径 + 低成本裁决）**

1. 脚本先跑一遍，读 `manifest.reasons` 与 `quality.unrecognizedHeadings`，并顺带核对 `manifest.nonChapterHeadings`（非章标题是否认得合理）与 `manifest.volumeMarkers`（内部卷标记是否与「一个资产 = 一卷」相符）；
2. Agent 只看**候选边界清单**（疑似标题行 + 行列号 + 当前切分），给出结构化的边界修订，不改正文、不重写源包；
3. 把修订存成 JSON，用 `--revisions` 回灌重跑；被修订命中的行不再计入「未识别标题行」，`confidenceSignals.resolvedByRevision` 记录收敛数量，通常这一轮 `agentArbitrationRequired` 就会回到 `false`。

### `--revisions` 结构

顶层可以是：数组、`{ "ops": [...] }`、`{ "revisions": [...] }`、`{ "assets": [...] }`、或带 `titleOverrides`。`assets[]` 里可写 `ops` / `revisions` / `ranges` / `titleOverrides`。

操作类型（行号均为**该文件内的 1 基行号**）：

```jsonc
{
  "ops": [
    { "op": "split",  "line": 812, "title": "第三章 真正的标题", "level": "chapter" }, // 强制在 812 行开新章
    { "op": "merge",  "line": 260 },                                                  // 删除 260 行的边界（并入上一章）
    { "op": "rename", "chapter": 3, "title": "第三章 改名" },                          // 按资产内章号覆盖标题
    { "op": "range", "from": 800, "to": 900,                                          // 行号区间内批量重写边界
      "boundaries": [ { "line": 812, "title": "…" }, { "line": 880, "drop": true } ],
      "dropLines": [ 860 ] }
  ],
  "titleOverrides": { "1": "第一章 甲（覆盖）" }
}
```

- `asset` 可写 `assetId` / 文件名 / 文件名去扩展名 / 1 基资产序号；省略时单资产自动命中，多资产会被跳过并记 `status: "skipped"`。
- 所有修订（含未命中的）都会写进 `manifest.revisionsApplied`，用于复现与审计。

## 批次计划

`批次计划.json` 一次给三档，`--profile` 决定生效档位（`activeTier` 即所选档）。三档与交付物**一一对应，档位名就是交付物名**：

| 档位 | 每批上限 | 对应交付物 |
| --- | --- | --- |
| `standard` | 约 30 章/批 | 六模块完整交付（默认） |
| `deep` | ≤ 20 章/批 | 六模块完整交付、质量优先 |
| `outline` | ≤ 40 章/批 | 卷级骨架交付 |

`standard` 与 `deep` 是**同一交付物**（六模块完整交付）的两种切批粒度：`deep` 每批更小、批内上下文更宽裕，用于质量优先。`outline` **不是「更快的六模块」，而是另一种交付物**——只交付卷级骨架（卷级结构 / 章节骨架），不做六模块精读，因此每批可以更大（≤40 章/批）。

任何档位每批都不超过 40 章。

每批带 `batchNo` / `fromGlobalNo` / `toGlobalNo` / `chapterCount` / `volumeNos` / `files`，批次连续覆盖本次选中章，是续跑与重试的粒度单位（循环单元是「批」，不是「任务」）。

## 快速检查

```bash
node scripts/split-chapters.mjs --input 全书.txt --out ../源包 --dry-run --json   # 先看判定与「可清洗项」预览，不落盘
node scripts/split-chapters.mjs --input 全书.txt --out ../源包 --clean --json      # 先清洗噪声再分章
node scripts/split-chapters.mjs --input 全书.txt --out ../源包 --json              # 正式产出（不清洗）
```
