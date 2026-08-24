# CHANGELOG

## v7.0.0 — 2026-08-24

### steps 四件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step-0-source-acquire / step-1-etl-split / step-2-batch-process / step-3-verify 四件全合入 SKILL.md 对应节（Step 0 源文件获取+下载后校验 / Step 1 ETL正则拆分+验证 / Step 2 模式确认+precision/fast 两套子agent派发任务包+v4格式+beat粒度+质量卡尺+实测性能 / Step 3 双维度验证清单 precision 9项+fast 6项）
- **执行模式明确**：全部走子agent派发（本skill核心机制保留，派发任务包模板内联进SKILL.md）——主agent负责源文件获取/ETL/模式确认/切批/派发/汇总验证，子agent读原文产出；模式确认环节主agent与用户直执
- **内容精炼**：SKILL.md 双维度表与 step-2 模式确认两张重复表合并（保留得失一句话）；fast/precision 派发流程同构部分（绝对路径写入/汇总验证只重派缺失批次）合并表述；实测性能 quality/performance 两表合一；红线从 step 文件 10 条 + 骨架 7 条去重收敛为 10 条，门禁全保留
- **修复死引用**：step-1 引用的 `skills/pop-decon/_scripts/extract.py` 已随 pop-decon v24.1.0 死资产清理归档，改为正则拆分内联说明；step-2「默认 performance+fast」与骨架双维度表「precision默认」矛盾，以骨架表标注为准
- skill.json version 6.5.0→7.0.0

---

## v6.5.0 | 2026-08-13

### A-2 档重构：从「必选前置」降级为「可选加速器」

- **核心变化**：方案A 拆书以直读原文为主，本 skill 从拆书管线「必选前置」降级为「可选加速器」。默认拆书走 pop-decon-dimension 直读原文，不产白描卡；仅当用户明确要逐章白描卡/设计包时才调用本 skill
- **SKILL.md**：头部定位改为「可选加速器」，新增定位说明块，下游改为 pop-decon-dimension（可选加速），版本 6.4.0→6.5.0
- **skill.json**：description 同步可选加速器定位，downstream 由 pop-decon-volume/pop-decon-prd 改为 pop-decon-dimension，版本 6.4.0→6.5.0
- **版本三处一致**：SKILL.md + skill.json + CHANGELOG.md 统一为 6.5.0

## v6.4.0 | 2026-08-06

### 执行方式从「脚本直连 DS API」改为「派发子 agent 执行」

- **核心变化**：Phase 1 白描卡/设计包提取不再依赖 `slim_card_batch.py` 脚本直连 DS API，改为由主 agent **派发子 agent** 执行。每个子 agent 读取 `_temp/chapters/` 原文章节、产出白描卡/设计包，**无需 DEEPSEEK_API_KEY**
- **删除 `scripts/slim_card_batch.py`**：彻底移除对 DS API 的依赖，管线纯子 agent 驱动
- **双模式映射为派发粒度**：
  - 质量模式（quality）= 每章 1 个子 agent 逐章精拆，精度最高、跨章不串扰
  - 性能模式（performance）= 每 30 章 1 个子 agent 合并产出，成本最低（187章=7个子agent，省约30%）
- **step-2-batch-process.md**：重写为子 agent 派发流程（Step 2A-1~5 / 2B-1~5），含子 agent 任务包模板、绝对路径写入要求、主 agent 汇总验证；新增红线❌8「子agent落盘错误目录」
- **SKILL.md**：双维度表、速查表、红线改为子 agent 方式，删除脚本引用行
- **references/batch-scaling.md**：命令示例改为派发方式说明，脚本参数改为派发参数
- **references/slim-card-format-spec.md**：v4 对照表处理方式行改为子 agent 派发
- **templates/slim-card-template.md**：生产方式说明改为子 agent
- **skill.json**：description 同步子 agent 派发说明，版本 6.3.0→6.4.0
- **版本三处一致**：SKILL.md + skill.json + CHANGELOG.md 统一为 6.4.0
