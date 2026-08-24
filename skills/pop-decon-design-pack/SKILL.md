---
name: pop-decon-design-pack
description: "当用户说'拆书/提取设计包/ETL拆分/白描卡'时启用。可选加速器（非必选前置）：方案A 直读原文为主，本 skill 仅在需要逐章白描卡/设计包时按需调用。双维度：输出格式 precision(v4设计包3层+1区)/fast(瘦身白描卡4段式) × 处理方式 quality(每章1子agent)/performance(每30章1子agent合并)。全部走子agent派发，无API脚本。任务开启前强制确认模式。产出供下游 pop-decon-dimension 可选加速消费。"
---

# pop-decon-design-pack · 章节设计包（可选加速器）

> 可选加速器（非必选前置）。方案A 拆书以直读原文为主，本 skill 仅在需要逐章白描卡/设计包时按需调用。双维度提取设计包：输出格式（precision/fast）× 处理方式（quality/performance）。全部走子 agent 派发执行。v7.0.0：steps 四件全合入单文件精炼。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

> ⚠️ **定位说明**：在 A-2 档重构后，本 skill 已从「必选前置」降级为「可选加速器」。默认拆书走 pop-decon-dimension 直读原文，不产白描卡；仅当用户明确要逐章白描卡/设计包时才调用本 skill，产出作为维度拆解的可选加速输入。

## 做什么

| 输入 | 输出 | 下游 |
|:-----|:-----|:-----|
| 源文件（TXT/EPUB） | precision: 设计包v4 / fast: 瘦身白描卡 | pop-decon-dimension（可选加速） |

### 双维度

**维度1：输出格式（execution.mode）**

| mode | 格式 | 单章字数 | 压缩比 | 适用场景 |
|:-----|:-----|:---------|:------:|:---------|
| `precision`（默认） | v4 设计包（3层+1区） | 1-2K | 80-100% | 精品拆书/拆书为写/prose-render |
| `fast` | 瘦身白描卡（4段式） | 150-400 | ~11% | 大规模拆书/快速验证/全书骨架 |

**维度2：处理方式（execution.strategy）**

| strategy | 派发方式 | 精度 | 成本 | 耗时(187章) | 适用 |
|:---------|:---------|:-----|:-----|:-----------|:-----|
| `quality`（质量模式） | 每章1子agent逐章精拆 | 最高，跨章不串扰 | 高（187个子agent） | ~35-45分钟 | 精品拆书/精读关键章 |
| `performance`（默认） | 每30章1子agent合并产出 | 略降，后段粗 | 低（7个子agent，省~30%） | ~3-4分钟 | 大规模拆书/全书骨架 |

> **得失一句话**：质量模式得精度、失成本与速度——每章独立上下文、无跨章串扰；性能模式得成本与速度、失部分精度——30章合并一次产出，后段章节细节略粗，适合先跑全书骨架再精修关键章。

**执行模式**：全部走子 agent 派发（本 skill 核心机制，无 API 脚本、无 DEEPSEEK_API_KEY 依赖）——主 agent 负责源文件获取/ETL/模式确认/切批/派发/汇总验证；子 agent 读原文章节并产出白描卡/设计包。模式确认环节必须主 agent 与用户直执。

## 怎么操作（SOP全内联）

> execution.mode: precision/fast | execution.strategy: quality/performance

### Step 0：源文件获取

1. 检测项目目录是否已有 .txt：有 → 记 `$TXT_PATH={项目根}/{书名}.txt`，进 Step 1（多个 .txt 询问用户选哪个，或取最大文件）；无 → 走下载。
2. 下载（委派 `tool-download-webnovel`，按其 SKILL.md 完整执行搜索→下载→校验）。书名获取：用户显式给出 / 从项目目录名推断（**目录名常为简写，歧义必须与用户确认**）。委派指令必须明确：
   - 产出 TXT 落位到**当前拆书项目根目录**（非该 skill 默认的 `downloads/`），文件名 `{书名}.txt`
   - 完成其 Step 3 校验（含付费墙检测）
3. **下载后校验**：TXT 存在于项目根目录｜文件大小 > 50KB（过小多为错误页/付费墙截断）｜预览前 200 字可读（非 HTML/HTTP 错误）｜章节数 ≥ 用户指定拆章数。未通过 → 退回换源重试；全部来源失败 → 终止告知用户。

**门禁**：产出 TXT 不存在/大小为 0/内容为 HTTP 错误页 → 退回；源文件缺失不得硬跑 Step 1；下载失败不得静默继续。

### Step 1：ETL + 按章拆分（机器操作，不用 LLM）

1. 从 `$TXT_PATH` 提取纯文本 → `_temp/full_text.txt`（非空）+ `_temp/metadata.json`（含 chapter_count / word_count）。中文 TXT 编码优先 GBK → GB18030 → UTF-8；ETL 细节见 `references/chinese-novel-etl.md`。
2. 按正则 `^(第[零一二三四五六七八九十百千]+章|Chapter\s+\d+|第\d+章|ch\d+)|第\d+节` 拆章 → `_temp/chapters/ch001.txt ~ chNNN.txt`。
3. **验证**：章节文件数 == metadata.json.chapter_count；每文件非空；章序号与正文标题号一致。未通过 → 退回重新拆分。

> 注：旧版 extract.py 已随 pop-decon v24.1.0 死资产清理归档，拆分按上述正则直接执行。

### Step 2：模式确认 + 派发子 agent 提取

**0. 任务开启前：模式确认（必做，禁止擅自默认）**：向用户展示上面两张双维度表 + 得失一句话，询问「本次拆书用质量模式还是性能模式？输出用 precision 还是 fast？」用户明确答复后记录 `execution.strategy` + `execution.mode` 才进入提取；与默认值一致确认后即继续，不一致按用户指定调整。

**派发粒度**：

| strategy | 派发方式 | 子agent数（187章） | 每子agent任务 |
|:---------|:---------|:--------------------|:-------------|
| quality | 每章 1 个子 agent | 187 | 读 chXXX.txt → 产出单章文件 |
| performance | 每 30 章 1 个子 agent | 7 | 读连续30章 → 逐章产出30份文件（最后一批按实际章数） |

#### Step 2A：precision mode（v4 设计包）

派发流程：
1. 主 agent 读 `references/v3-format-quick-reference.md`（v4 格式快照）作为派发子 agent 的 context 模板。
2. 按 strategy 切分派发批（quality 每批=1章 / performance 每批=30章）。
3. 派发子 agent，任务包（goal + context）：

```
goal: 读取 {绝对路径} 目录下的原文章节，输出 v4 设计包到 {绝对路径} 目录
context:
  - 读取章节：_temp/chapters/chXXX.txt 至 chYYY.txt（quality 单章 / performance 连续30章）
  - 对齐格式：遵循 v3-format-quick-reference.md 的 v4 设计包模板（3层+1区）
  - 每章独立产出：写作资产/设计包v4/chXXX-设计包.md，首行 `# 设计包 — chXXX「章节标题」`
  - 事件链用表格（列：# | beat | 类型 | scene | POV | 参与角色 | 原文证据），
    原文证据列只写定位指针，🔒 标记关键对白/数据
  - 不发明 beat，事件链必须来自原文
  - 完成后在回复中确认：产出文件路径 + 章节范围 + 是否全部落地
```

4. **写入绝对路径**：子 agent workdir 可能与主 agent 不同，读章节与产出都必须用绝对路径（如 `D:\{项目根}\_temp\chapters\chXXX.txt` / `D:\{项目根}\写作资产\设计包v4\chXXX-设计包.md`），避免落盘到临时目录。
5. **主 agent 汇总验证**：对比 `_temp/chapters/` 与 `写作资产/设计包v4/` 文件数，一致 → 进 Step 3；缺失 → 列出缺失章节，只重派缺失批次。

**v4 格式**（3层+1区，详见 `references/v3-format-quick-reference.md`）：

```markdown
# 设计包 — chXXX「章节标题」

## 1. beat链 (L1beat链层) - 表格格式
| # | beat | 类型 | scene | POV | 参与角色 | 原文证据 |
（至少8个beat，原文证据列只写定位指针，🔒 标记关键对白/数据）

## 2. 爽点设计 (L2爽点层)
- 情绪弧线 / 爽点机制 / 章末钩子(L1-L5)

## 3. 角色与人设 (L3角色层)
- 登场角色行为锚定 / 关键对白(语气+潜台词)

## 4. 设定/物品提取区 (S1)
- 本章新揭示的世界设定、力量体系、规则、物品
```

**不同章型的 beat 粒度**（先判断章型再定粒度，同一套 beat 数不能套所有章）：

| 章型 | 特征 | 每章beat数 | beat粒度 |
|:-----|:-----|:----------|:---------|
| 战斗 | 回合制对抗、有胜负有转折 | 8-12 | 每一轮交锋=一个beat |
| 对话/信息 | 两人/多人交谈、信息交换 | 5-8 | 每轮信息释放=一个beat |
| 探索/发现 | 新地点、新发现、世界观披露 | 6-10 | 每个地点/每个发现=一个beat |
| 过渡/日常 | 赶路、修炼、日常 | 3-5 | 每段日常/每段修炼=一个beat |
| 高潮/转折 | 重大beat、多线汇合 | 10-15 | 可拆到每人每线一个beat |

**质量检验**：主 agent 抽检后 10%（至少 3 章）执行质量检查（beat表7列/精度锚点/🔒标记等，标准同 Step 3 precision 验证清单），全部通过才视为完成。

#### Step 2B：fast mode（瘦身白描卡）

格式规范见 `references/slim-card-format-spec.md`，4 段式结构：

```
# chXXX「标题」
POV: xxx | 章型: xxx | 原文: XXXX字
## 事件白描（3-5句，覆盖本章核心）
## 关键数据
🔒 一行式摘要+原文定位指针
## 爽点·钩子
## 人物关系变化（可选）
```

派发流程同行 2A：主 agent 读 `references/slim-card-format-spec.md` 作 context 模板 → 按 strategy 切批 → 派发子 agent，任务包：

```
goal: 读取 {绝对路径} 目录下的原文章节，输出瘦身白描卡到 {绝对路径} 目录
context:
  - 读取章节：_temp/chapters/chXXX.txt 至 chYYY.txt（quality 单章 / performance 连续30章）
  - 对齐格式：遵循 slim-card-format-spec.md 的 4 段式白描卡模板
  - 每章独立产出：写作资产/白描卡/chXXX.md，首行 `# chXXX「章节标题」`
  - 事件白描 3-5 句，覆盖全部核心转折
  - 🔒 关键数据为一行式摘要+原文定位指针（禁止全文引用）
  - 爽点/钩子/关系变化无则省略，不写"无"；单章总字数 ≤500 字
  - 不发明内容，事件必须来自原文
  - 完成后在回复中确认：产出文件路径 + 章节范围 + 是否全部落地
```

写入绝对路径 + 主 agent 汇总验证（对比 `写作资产/白描卡/` 文件数，缺失只重派缺失批次）同行 2A-4/2A-5。

**fast 质量卡尺（5项）**：

| # | 检查项 | 通过标准 | 扣分规则 |
|:-:|:-------|:---------|:---------|
| 1 | 事件白描完整 | 3-5句，覆盖全部核心转折 | 缺1转折 -1 |
| 2 | 🔒关键数据 | 有🔒标记且为一行式摘要+指针 | 缺标记 -2 |
| 3 | 章型正确 | 7型之一且与内容匹配 | 错误 -1 |
| 4 | 钩子标注 | 有钩子或合理省略 | 缺钩子且无说明 -1 |
| 5 | 字数控制 | ≤500字 | >500字 -1 |

**实测性能参考**（fast 压缩比 ~11%，全书 ~8%）：

| 量级 | quality（子agent数/耗时） | performance（子agent数/耗时） |
|:-----|:--------|:--------|
| 10-30 章 | 10-30个 / ~15s-60s | 1个 / ~60s |
| 187 章（✅实测·深渊主宰第一卷） | 187个 / ~35-45分钟 | 7个 / ~3-4分钟 |
| 678 章（全书·预估） | 678个 / ~2-3小时 | 23个 / ~12分钟 |

### Step 3：验证（双维度）

1. **文件数对比**：precision 对比 `_temp/chapters/` vs `写作资产/设计包v4/ch*-设计包.md`；fast 对比 vs `写作资产/白描卡/ch*.md`。产出数 = 章节数 → 通过；产出数 < 章节数 → 列缺失章节号退回 Step 2。
2. **完整性检查 + 抽检后 10%（至少 3 章）**：按下方验证清单逐项执行。
3. **命名与首行格式**：precision 文件名 `chXXX-设计包.md`（三位数补零）+ 首行 `# 设计包 — chXXX「章节标题」`；fast 文件名 `chXXX.md` + 首行 `# chXXX「章节标题」`。
4. 全部通过 → 通知 orchestrator（pop-decon）Phase 1 完成，产出可供 pop-decon-dimension 可选加速消费；未通过 → 列出缺失/不合规文件清单退回 Step 2。

**precision 验证清单（9项）**：

| # | 检查项 | 通过标准 | 失败处理 |
|:-:|:-------|:---------|:---------|
| 1 | 文件数对比 | 设计包文件数 = 章节文件数 | 缺文件退回 Step 2 |
| 2 | 3层+1区小节标题 | beat链/爽点/角色/设定 4 个小节标题全存在 | 缺层退回重写 |
| 3 | beat表7列 | 表格格式，7列 | 退回重写 |
| 4 | 每beat精度锚点 | scene + POV + 原文证据 + 感官锚点 | 缺锚点退回重写 |
| 5 | 🔒不可替换标记 | 每beat有 🔒 标记 | 缺标记 → 警告 |
| 6 | 设定区非空 | 有内容或显式说明 | 空且无说明 → 退回 |
| 7 | 命名一致性 | 全部 chXXX-设计包.md | 统一重命名 |
| 8 | 首行格式 | `# 设计包 — chXXX「标题」` | post-hoc 脚本修复（scripts/normalize-headlines-from-source.py） |
| 9 | beat数下限 | 前70%≥8，后30%≥5 | 标注低密度警告 |

**fast 验证清单（6项）**：

| # | 检查项 | 通过标准 | 失败处理 |
|:-:|:-------|:---------|:---------|
| 1 | 文件数对比 | 白描卡文件数 = 章节文件数 | 缺文件重跑 |
| 2 | 3段必需小节 | 事件白描+关键数据+爽点钩子 | 缺段退回 |
| 3 | 🔒数据格式 | 一行式摘要+指针，非全文引用 | 退回重写 |
| 4 | 命名一致性 | 全部 chXXX.md | 统一重命名 |
| 5 | 首行格式 | `# chXXX「标题」` | 标记差异文件 |
| 6 | 字数控制 | ≤500字/章 | 超标标记警告 |

> fast 抽检另查：事件白描覆盖全部核心转折｜🔒格式正确｜无"本章无"（应省略而非标注）。

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. 源文件+ETL前置缺失 — 未获取源文件/未ETL/未按章拆分 → 退回
3. 凭空发明内容 — beat链/事件白描中出现原文不存在的内容 → 退回
4. 证据缺失或转录 — precision: 每beat必须有原文证据指针；fast: 🔒数据必须为一行式摘要+指针（禁止全文引用）
5. 精度模式锚点缺失 — precision: 每beat必须有 scene+POV+🔒关键对白/数据+感官锚点
6. 结构不完整 — precision: 3层+1区全部小节；fast: 事件白描+关键数据+爽点钩子三段必须存在
7. 命名与合并违规 — precision: chXXX-设计包.md / fast: chXXX.md（三位数补零）；广告等非正文内容混入 → 退回
8. 子agent落盘错误目录 — 子agent用相对路径产出了临时目录 → 退回用绝对路径重派
9. 产出遗漏 — 单批输出缺失章节 → 只重派缺失批次
10. **未确认模式擅自执行** — 任务开启前未与用户确认 strategy+mode 就提取 → 退回重确认

## 速查表（外部文件）

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `references/设计包v3-格式规范.md` | 精度模式理解设计包格式时 | v4格式规范（precision） |
| `references/slim-card-format-spec.md` | 快速模式理解白描卡格式时 | 瘦身白描卡格式规范（fast） |
| `references/v3-format-quick-reference.md` | 派发子agent context时 | v4格式快照 |
| `references/precision-anchor-format.md` | 理解scene/POV/🔒/感官锚点时 | 精度锚点格式 |
| `references/chinese-novel-etl.md` | 中文TXT拆分时 | 中文网文ETL |
| `references/batch-scaling.md` | 大规模拆书时 | 质量/性能双模式子agent派发策略 |
| `references/post-hoc-format-normalization.md` | 首行格式漂移修复时 | 格式归一化 |
| `references/cn-novel-format-injection-failure.md` | 多批次格式不一致时 | 格式注入失败案例 |
| `templates/fact-skeleton.md` | precision模式产出时 | v4设计包模板 |
| `templates/slim-card-template.md` | fast模式产出时 | 瘦身白描卡模板 |
| `scripts/normalize-headlines-from-source.py` | 首行格式修复时 | 标题归一化脚本 |

## 版本

v7.0.0 | 2026-08-24
- 四件 step 文件（step-0-source-acquire / step-1-etl-split / step-2-batch-process / step-3-verify）全合入 SKILL.md 单文件精炼，step 目录删除
- 执行模式明确：全部走子agent派发（precision/fast 两套派发任务包模板内联），模式确认环节主agent与用户直执
- 内容精炼：双维度表与 step-2 模式确认两张重复表合并；fast/precision 派发流程同构部分（绝对路径/汇总验证）合并；实测性能两表合一；红线从 step 文件 10 条 + 骨架 7 条收敛为 10 条（门禁全保留）
- 修复死引用：step-1 的 extract.py 已随 pop-decon v24.1.0 归档，改为正则拆分内联说明；step-2「默认 performance+fast」与骨架表「precision默认」矛盾，以骨架双维度表标注为准
- skill.json version 6.5.0→7.0.0
v6.5.0 | 2026-08-13 | A-2 档重构：从「必选前置」降级为「可选加速器」，下游改为 pop-decon-dimension（可选加速）→ [CHANGELOG.md](CHANGELOG.md)
