# CHANGELOG

## v4.11.0 | 2026-08-13

### 剧情沉淀轻量化：只沉淀剧情白描

**背景**：老板定调——review 只沉淀剧情白描，砍掉冗余沉淀物，满足"写剧情冲突 + 不OOC"的最小要求（对齐起点 review v3.9.0）。

**改动**：
- **SKILL.md**：产出表改为 白描卡（流水账 append）+ 状态快照（3段）；Step 4 改只沉淀双文件；红线7 改「白描卡+状态快照每章必更新」；速查表改指 状态快照；版本 v4.10.0→v4.11.0
- **steps/step1.md**：formal 前提与必读输入改指 白描卡/状态快照
- **steps/step2.md**：重写为只沉淀白描卡（流水账 append）+ 状态快照（replace 3段），删除审核报告/verdict 落盘（审核结论对话内输出）
- **skill.json**：version 4.10.0→4.11.0，description 改轻量白描卡+状态快照

---

## v4.10.0 | 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v4.10.0
- **CHANGELOG.md**：新增本条版本记录

---

## v4.9.0 (2026-08-12)

### 剧情记录双文件收束：白描卡 + 剧情累计卡，废除 current-state / review-沉淀 / 压缩归档

**背景**：老板定调——剧情记录只保留「白描卡（存发生）+ 剧情累计卡（存状态）」。番茄系的剧情白描流水账即白描卡（append，每章白描），另新增剧情累计卡（replace，全书累计视图）承接 current-state 的状态职责。废除 current-state.md / review-沉淀.md / 压缩归档/ 等冗余文档。

**改动**：
- **SKILL.md**：产出表改为 审核报告 + 白描卡（剧情白描流水账，append）+ 剧情累计卡（replace）；Step 4 描述改双文件；红线7 改为「双文件每章必更新」；速查表 step2.md 描述更新；新增双文件职责说明（白描卡存发生/剧情累计卡存状态）
- **steps/step1.md**：formal 前置与必读输入改指 上一章白描卡 + 剧情累计卡
- **steps/step2.md**：删除"归档旧版→更新current-state→追加review-沉淀"逻辑，改为「追加剧情白描流水账（append，白描卡）→ 更新剧情累计卡（replace，钩子台账/角色状态/读者已知池/禁止漂移/DNA执行包）→ 落盘审核报告+verdict」；落盘后检查新增"未产出任何旧文档"
- **skill.json**：version 4.8.0→4.9.0，description 改双文件叙事记录

---

> 历史版本条目已归档：`_archive/changelog-history/pop-fanqie-review/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
