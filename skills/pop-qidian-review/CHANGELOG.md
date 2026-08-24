# CHANGELOG

## v4.0.0 | 2026-08-24

### steps 全合入 + 子agent审计分工落地

**背景**：70 run 实测 step 文件送达率=0（harness 只注入 SKILL.md，step 永不上桌、agent 永不 Read）——step 化在当前 harness 下是死代码；review 的 step 隔离率高达 81%，四步审核细节全部锁在死区。同期实测发现 paopao_subagent_run 是审查型通道（只读约束），而 review 的 Step 1-3 恰好是纯只读审计——通道与任务天然匹配。

**改动**：
- **steps 三件全合入 SKILL.md**（13.4K→7.9K，-41%）：step-1-audit→Step 1-3 内联（正向符合性/正文质量/反向充足性全部检查项与表格保留）；step-2-commit→Step 4 内联（沉淀核对+落盘清单+验收门禁）；step-reconstruct→Reconstruct模式内联（采样策略+简化审核）。删除 steps/ 目录
- **执行模式新增**：子agent审计官（Step 1-3 只读审计，派发 verification/implementation-check）+ 主agent落盘（Step 4）——全家族唯一与审查型通道天然适配的 skill；含派发审计指令硬清单；主agent直执模式保留为合法降级
- **字数检查脚本化**（Step 2d）：以 pop-qidian-write/scripts/word-count.ps1 实测为准，实测输出原文必须贴进审核结论，禁转述/引用生成侧数字（write v4.2.2 实测虚报 2476 vs 实际 1620 的教训）
- **验收门禁新增**：查文件系统不信口头（白描卡存在含四节/快照 mtime 更新/无废弃文档产出）
- **红线 7→5 收拢**：读取协议红线作废（无steps）→并入输入清单；AI味证据+好看度证据合并；主角变化五项并入双文件红线；新增字数实测红线
- **对齐 pipeline v4.0.0**：reconstruct 完成后回项目总控.html Phase 路线图（原指向已删除的 pipeline step2.md 死链修复）
- **skill.json**：3.10.1→4.0.0

---

## v3.10.1 | 2026-08-24

### 输入清单加项目总控.html

**背景**：pipeline v4.0.0 瘦身为一次性安装器，Phase路由外置到项目总控.html。review 需自带章节授权确认。

**改动**：输入清单首位加"项目根/项目总控.html（STATE区确认phase=phase6+chapter）"；SKILL.md 头注同步。skill.json：3.10.0→3.10.1。

---

## v3.10.0 | 2026-08-24

### 沉淀职责前移：Step 4 从唯一产出方改为核对修正方

**背景**：write v4.1.0 正确性基线重构——沉淀挪入 write（写完即沉淀白描卡+状态快照）。理由：实测用户 11-15 章连写时 review 全跳（57 章仅 2 份叙事记录），沉淀挂在"review 必跑"前提上=大概率不发生；write 是唯一必然执行环节。

**改动**：
- **SKILL.md**：Step 4「剧情沉淀」→「沉淀核对」——对照正文核对 write 沉淀双文件的事实准确性（关键数据🔒/钩子状态/角色状态/禁止漂移），有误修正，缺失补产；输入清单新增"write 沉淀的白描卡+状态快照（待核对）"；产出表标注（核对修正/补产）
- **skill.json**：3.9.0→3.10.0，description 同步
- **steps/step-2-commit.md**：职责头注同步（正文未改，模板与核对规则沿用）

**核心洞察**：write 记事实（发生什么/数据/钩子），review 对账。沉淀必发生由 write 保证，准确性由 review 交叉核对——两道防线不再互相依赖。

---

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
