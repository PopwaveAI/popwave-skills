# CHANGELOG — test-research

## v6.0.3 | 2026-08-31

### stage 合并，包配方消费方改指 pop-stage

> **根因**：pop-world + pop-character 再合并为 pop-stage（喷漆模型重构），旧 2 skill 废弃删除。

- `templates/金标准-包配方.md` 消费映射：`pop-world Step1`→`pop-stage Step1`、`pop-world Step2-4`→`pop-stage Step2`、`pop-character`→`pop-stage Step3-4`；表头「test-skill」改「消费 skill」
- skill.json version 6.0.2→6.0.3

## v6.0.2 | 2026-08-31

### review 三族合并，包配方消费方改指

> **根因**：pop-qidian-review + pop-fanqie-review + test-review 合并为 pop-review，旧 3 skill 废弃删除。

- `templates/金标准-包配方.md` 消费映射：`test-review`→`pop-review`
- skill.json version 6.0.1→6.0.2

## v6.0.1 | 2026-08-31

### world/character 三族合并，包配方消费方改指

- `templates/金标准-包配方.md` 消费映射：`test-world Step1/Step2`→`pop-world Step1/Step2-4`、`test-character`→`pop-character`（旧 6 skill 废弃删除）
- skill.json version 6.0.0→6.0.1

## v6.0.0 | 2026-08-24

### steps 两件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1-decon / step2-distill 两件全部合入 SKILL.md 对应节——DL0原文验证→DL1采样→DL2九表拆解→DL3质量门禁→DL4存盘返回→DL5转写七文件夹（14行转写表+转写铁律4条全保留）、Step 2五表蒸馏（数据源+提炼要点+末尾两节+质量门禁）
- **执行模式明确**：DL0验证+DL2九表拆解可派子agent执行并回报结果（只读原文采样+分析）；DL5转写/Step 2蒸馏/落盘归主agent；采样范围确认等轻交互主agent直执
- **内容精炼**：DL2九表执行要点整理为单表（表1执行步骤与拆解陷阱合并）；范式判据压缩为单行；DL4返回格式压缩为要点行；速查表steps行删除、金标准本地副本（templates/金标准-包配方.md）入表
- **修复死链**：原引用 `templates/素材/decon-lite.tpl.md` 实际不存在，底稿格式（元数据块+9表各一节）已内联DL4
- skill.json version 5.2.0→6.0.0

---

## v5.2.0 | 2026-08-19

### 包结构重构：七文件夹（一个包=一个skill）

- **根因**：旧`设计/`三层结构（设计/力量体系.md、设计/全书设定/、卷纲/）不符合「包=自描述知识单元」原则——单文件过大（战斗表现40KB）导致agent加载过载，且目录语义不按消费者组织
- **新结构**：立项/赛道特色/力量与战斗/世界观/角色库/剧情库/补充参考（按需）七文件夹；单文件≤15KB，超限按「消费者×加载时机」拆分
- **step1-decon DL5**：转写表按七文件夹重排——战斗表现拆5件（通用层+凡人期/超凡期/神明级+特殊条件战）；主线/动力引擎/各卷切片归入剧情库；类型风味基线归入赛道特色；金手指/战斗系统归入力量与战斗；新增转写铁律4（单文件≤15KB）；DL4返回 23→28文件
- **step2-distill**：五表数据源路径同步新结构（剧情库/主线、剧情库/卷纲/卷一-卷纲、力量与战斗/力量体系等）
- **SKILL.md**：产出表 23→28文件，头部声明同步
- **金标准包同步**：深渊主宰包重构为七文件夹+战斗表现5件拆分，包配方新增「包结构与 test-skill 消费映射」节（v1.0.0→v1.1.0，consumers seed→adapt）
- skill.json version 5.1.0→5.2.0

## v5.1.0 | 2026-08-18

### 剧情层产出对齐 plot v8 双层颗粒度

- **根因**：plot v8.1.1 消费路径已硬切换到 `卷一-卷纲.md`+`卷一-幕N-章白描.md`×5，但 DL5 转写表仍产出旧 `卷一-幕纲.md`——新建书包将缺失 plot 消费文件，链路断裂
- **step1-decon DL5**：主产出改为卷纲（战略层：卷定位+幕框架5幕+章节流指针）+幕白描×5（幕头节奏参数+快爽密度统计行[场次口径+时代特征警示]+逐区间锚点卡）；旧幕纲/章锚点表合并为一行废弃格式（默认不产出）；格式锚指向 test-plot 两模板；DL4 返回文件数 17→23
- **step2-distill**：表1数据源改卷纲战略层、表2改幕白描（新增每幕战斗场次密度参数）、表4改卷纲/幕白描爽感公式节
- **SKILL.md**：产出表 17文件→23文件（卷纲2→6），头部声明同步
- skill.json version 5.0.0→5.1.0

## v5.0.0 | 2026-08-16

### 架构重构：设定包构建器

- **定位重塑**：燃料档/赛道调研档/题材机制档全部废弃，重构为建包器——一本成功书→设定包全套+包配方
- **decon-lite升级**：step-decon-lite改名step1-decon，新增DL5转写节（按消费端格式转写立项/设计15/卷纲2/角色库共17文件到`KB/设定包/{书名}/`）
- **新增step2-distill**：从包文件蒸馏包配方5表（卷幕骨架/节奏参数/颗粒度/爽点配方/角色配置）+硬对齐达标线+包准入标准，结构对齐金标准（深渊主宰包）
- **新增红线**：5表齐全才准入（缺任一表管线拒绝启动）/参数数值化/推断降权标注
- **删除文件**：step-1-find/step-2-output/step-track-research/燃料文档.tpl/赛道调研.tpl/题材机制.tpl/用户意图.tpl
- skill.json version 4.6.0→5.0.0；slashCommands改为"建包/拆书建包"

---

## v4.6.0 — 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v4.6.0
- **CHANGELOG.md**：新增本条版本记录

---

## v4.5.0 — 2026-08-12

### 燃料筛入目标对齐剧情累计卡

**背景**：剧情记录双文件收束——review 只产出「白描卡（单章历史）+ 剧情累计卡（全书累计视图）」，废除 current-state.md。research 燃料文档原以"筛入 current-state"为目标，需同步为剧情累计卡。

**改动**：
- **templates/fuel-doc.tpl.md**：元数据 role/compression 从"筛入 current-state"改为"筛入剧情累计卡"；章节标题"可筛入 current-state 的近期燃料"→"可筛入剧情累计卡的近期燃料"
- **steps/step-1-find.md**：燃料分级"近期可用"从"筛入 current-state"改为"筛入剧情累计卡"
- **steps/step-2-output.md**：落盘清单与回复格式的 current-state 引用同步改为剧情累计卡
- **skill.json**：version 4.4.0→4.5.0，description 更新

---

> 历史版本条目已归档：`_archive/changelog-history/test-research/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
