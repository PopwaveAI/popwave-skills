# CHANGELOG

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
