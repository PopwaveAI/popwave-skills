# CHANGELOG

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
