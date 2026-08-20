# CHANGELOG

## v3.9.0 | 2026-08-13

### 剧情沉淀轻量化：只沉淀剧情白描

**背景**：老板定调——review 只沉淀剧情白描，砍掉冗余沉淀物，满足"写剧情冲突 + 不OOC"的最小要求。

**改动**：
- **SKILL.md**：产出表改为 白描卡（~300-500字）+ 状态快照（3段）；Step 4 与 Reconstruct 描述改双文件；红线7 改为「白描卡+状态快照每章必更新」；速查表模板指向 chapter-card.tpl.md + state-snapshot.tpl.md
- **steps/step-2-commit.md**：重写为只沉淀白描卡（轻量4段）+ 状态快照（replace 3段），删除审核报告落盘（审核结论对话内输出）
- **steps/step-reconstruct.md**：产出改为逐章白描卡 + 状态快照，删除审核报告/全书进度/读者已知
- **steps/step-1-audit.md**：formal 前提与连续性/对话检查改指 白描卡/状态快照
- **templates/**：chapter-card.tpl.md 轻量化（删 DNA 执行包），accumulate-card.tpl.md → state-snapshot.tpl.md（3段）
- **skill.json**：version 3.8.0→3.9.0，description 改轻量白描卡+状态快照

---

## v3.8.0 | 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v3.8.0
- **CHANGELOG.md**：新增本条版本记录

---

## v3.7.0 (2026-08-12)

### 剧情记录双文件收束：白描卡 + 剧情累计卡，废除冗余文档

**背景**：老板定调——剧情记录只保留「白描卡（单章历史）+ 剧情累计卡（全书累计视图）」，废除 current-state.md / 小说快照.md / review-沉淀.md / 压缩归档/ 等冗余文档。

**改动**：
- **SKILL.md**：产出表改为 审核报告 + 白描卡（新增）+ 剧情累计卡（replace）；Step 4 与 Reconstruct 描述改双文件；红线7 改为「双文件每章必更新」；速查表模板指向 chapter-card.tpl.md + accumulate-card.tpl.md
- **steps/step-2-commit.md**：已改造为双文件落盘（产出本章白描卡 + replace 更新剧情累计卡，明确"未产出任何旧文档"检查项）
- **steps/step-reconstruct.md**：已改造为逐章白描卡 + 剧情累计卡生成模式
- **steps/step-1-audit.md**：formal 前提与对话个性区分改指 白描卡/剧情累计卡
- **templates/**：删除 current-state.tpl.md，新增 chapter-card.tpl.md + accumulate-card.tpl.md
- **agents/openai.yaml**：display_name 从"涌现 Review"改"起点 Review"，short_description 更新
- **skill.json**：version 3.6.0→3.7.0，description 改双文件叙事记录

---

> 历史版本条目已归档：`_archive/changelog-history/pop-qidian-review/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
