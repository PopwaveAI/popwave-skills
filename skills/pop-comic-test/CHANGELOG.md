# CHANGELOG

## v1.2.0 — 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v1.2.0。

## v1.1.0 — 2026-08-05

### 生图改走 image_generate 工具，移除内置 API Key

老板要求所有 skill 生图环节改用 `image_generate` 工具，清理硬编码 API Key（Pinterest 搜索保持不动）：

- `SKILL.md` Step 3：由「批量生成」改为「`batch_test.py` 导出 `generation_tasks.json` + `image_generate` 工具逐条生成」
- 版本同步：SKILL.md / skill.json 至 v1.1.0

## v1.0.0 — 2026-08-04

### 新增：画风三组测试引擎

把「三组画风测试」沉淀为独立 skill，对画风库做逐画风内容形态验证：

- 三组固定模板（控制变量）：T1场景向 / T2角色立绘向 / T3多格剧情向
- 非画风部分（构图/光影/场景/角色）永久固定统一，只有 DNA+constraint 随画风变化
- `scripts/build_3test.py`：从 DNA 库批量生成三组 config，支持单画风（`--style-name`）与全库（`--all`）
- 复用 `pop-visual-shared/scripts/batch_test.py` 并发批量生成 + 自动 PE 日志
- 产出"画风通过判定表"：T1/T2/T3 各过/不过 + 偏科项标注
- 试点验证：双城之战三组全过（T1 85% / T2 100% / T3 95%），确认画风在三种内容形态下稳定执行