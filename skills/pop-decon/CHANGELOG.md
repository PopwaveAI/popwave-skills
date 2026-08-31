# CHANGELOG

## v26.2.0 | 2026-08-31

### 去 AI 味 + 文档瘦身

- 身份词"单书深度wiki引擎/主引擎"→"单书深度wiki拆解/主拆解"
- 引语与版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- description 精简，同步 skill.json（version 26.1.0→26.2.0）

## v26.1.0 — 2026-08-28

### L1 提取维度 7→8 + 入口补原子候选说明

> **根因**：配合 pop-decon-dimension v3.1.0——L1 提取新增「功能位/原子候选」，拆书顺带提剧情周期表原子。

**改动**：
- `SKILL.md` Step 3 补充「原子候选由 dimension Step 8 自动归集入库，入口不重复处理」。
- `references/pipeline-context.md`、`references/delegation-orchestration.md` 七维→八维同步。
- skill.json version 26.0.0→26.1.0。

## v26.0.0 — 2026-08-25

### 家从 4 精简为 2：入口只路由单书深度wiki引擎

> **根因**：老板以《深渊主宰》重建（六模块深度wiki）为新标准，要求 decon 全家推翻重做；判定旧的独立 `pop-decon-prd`（立项）、`pop-decon-design-pack`（逐章设计包）不再是独立 skill，方法论内吸进 `pop-decon-dimension` 主引擎（v3.0.0）。

**改动**：
- **删除下游 skill 引用**：skill.json `skills` / `pipeline.downstream` 移除 `pop-decon-design-pack`、`pop-decon-prd`。
- **征询简化**：从「范围+维度多选」简化为「范围」（全书/卷/N章）；维度由主引擎 L1 七维固化为固定提取，不再让用户逐维选。
- **路由收敛**：Step 2 只路由 `pop-decon-dimension`（单书深度wiki引擎），由其承载 L1批次拆解（硬门禁）→L2六模块成品整合。
- **产出目标改**：沉淀从 `项目本地/设计/{维度}拆解-{范围}.md` 改为 `{书名}/{六模块目录}`。
- **references 清理**：维度路由清单/output-quality-standards/pipeline-context/onboarding-guide/delegation-orchestration 全量对齐新家与双层门禁（去 prd/design-pack/{维度}拆解 残留）。
- skill.json version 25.0.0→26.0.0，description 更新。

---

## v25.0.0 — 2026-08-24

### steps 1件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step-1-pipeline.md 合入 SKILL.md 对应节（Step 0 源文件检查+下载 / Step 1 征询范围+维度含征询话术 / Step 2 路由表+style特殊处理 / Step 3 沉淀+提醒少测 / 边界条件 7 场景）
- **执行模式明确**：主 agent 直执——下载路由/征询/路由派发/沉淀确认均为交互与编排环节，无自然子agent适配点；拆解工作整体路由给 pop-decon-dimension skill（skill 间调度，非子agent派发）
- **内容精炼**：路由地图内嵌的 8 维度清单与 Step 1b 维度表（含触发词）合并去重；征询话术压缩为单行引用；红线5 吸收"下载失败静默继续"门禁（原 step-0 红线 0b）
- skill.json version 24.1.0→25.0.0

---

## v24.1.0 | 2026-08-18

### 死资产清理：旧ETL脚本包+wiki残留移至归档区

**改动**：
- **scripts/**：extractor包（config/dependencies/exceptions/utils+parsers全家族+pycache）+extract.py+extract_cn_data.py 移至 _archive/pop-decon/scripts/——方案B现用dimension联合Grep直读原文，脚本不再使用
- **references/**：wiki残留6文件（format-consistency-audit/iceberg-theory/naming-normalization/numerical-system-reverse-engineering/wiki-injection-case-study/wiki-scraping-strategies）+templates/wiki-skeleton.tpl.md 移至 _archive/pop-decon/
- skill.json version 24.0.0→24.1.0，版本三处一致

---



### 方案B 重构：增加scope征询 + 联合Grep共享锚点池

- **核心变化**：拆书管线从方案A（逐维度独立检索）升级为方案B（联合Grep共享锚点池）。Step 1 新增scope征询（拆什么范围），所有维度一次性传入 pop-decon-dimension
- **SKILL.md**：路由地图更新为方案B流程，新增scope征询环节，路由参数改为 `dims=[维度列表] + scope=[章节范围]`
- **steps/step-1-pipeline.md**：Step 1 重写为"征询拆解范围+维度"（Step 1a 范围 + Step 1b 维度），Step 2 路由参数更新
- **references/delegation-orchestration.md**：子agent任务从单维度提取改为多维提取，上下文模板增加多维提取清单
- **references/small-book-phase2-strategy.md**：简化流程改为联合Grep+多维提取
- **红线更新**：新增"未征询就全量跑"红线，要求必须先征询范围和维度
- skill.json 版本 23.0.0→24.0.0，description 更新为方案B
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md 统一为 24.0.0）

## v23.0.0 | 2026-08-13

### 方案A 重构：砍白描卡链，维度拆解统一路由到 pop-decon-dimension

- **核心变化**：拆书管线从白描卡法改为方案A（直读原文反向抽取）。Step 1 由"产白描卡"改为"征询维度→路由 pop-decon-dimension"
- **skill.json**：可调度清单更新为 4 个（download-webnovel / dimension / design-pack / prd），版本 22.2.0→23.0.0
- **SKILL.md**：路由地图改为方案A，可调度 Skill 清单更新，新增红线"跳过原文直读"，版本 22.2.0→23.0.0
- **references/pipeline-context.md**：新增为统一共享资产（canonical），各维度引用读取
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md 统一为 23.0.0）

# CHANGELOG — 02-pop-novel-deconstructor

## v22.2.0 | 2026-08-10

### skill.json 补可调度 Skill 清单 + SKILL.md 新增素材表

**背景**：老板定调——pipeline 是整个专家的入口和调度器，机器层面（skill.json）应有一份"我能调哪些 skill"的统一清单。此前拆书只有 `pipeline.upstream/downstream` 声明，与其他 pipeline 的 `skills` 数组格式不统一。

**改动**：

- `skill.json`：新增 `skills` 完整可调度清单（download-webnovel + 9 个拆解维度 skill），保留 `pipeline.upstream/downstream` 不动
- `SKILL.md`：新增「📦 可调度 Skill 清单（素材表）」区块——每个 skill 的定位 + 何时调用，标注复用项
- 版本至 v22.2.0

---

> 历史版本条目已归档：`_archive/changelog-history/pop-decon/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
