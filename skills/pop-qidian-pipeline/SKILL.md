---
name: pop-qidian-pipeline
description: 起点项目安装器（一次性）。当用户说"初始化项目""新建项目""导入""续写""迁移已有资料"时启用。一次性建目录+生成项目总控.html+资产归位+缺口分析；日常写作路由由项目总控.html的Phase路线图承载，写正文/审核不经过本skill。
---

# pipeline（一次性安装器）

> v4.0.0：从"每次加载的常驻路由"瘦身为一次性安装器——Phase路由表外置到项目总控.html「Phase路线图」节，日常写作不再加载本skill；step0-import/step1 全量合入本文并删除 steps/。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

## 做什么

| 职责 | 说明 |
|:--|:--|
| 一次性安装 | 新建项目：标准化目录+项目总控.html+README |
| 一次性导入 | 已有资料：资产清点→归位→缺口分析→落地Phase→调度补跑 |
| 格式维护 | 总控.html 更新一律按 `references/html-update-protocol.md`（STATE字段规范单源） |

**日常路由不经此skill**：用户说"继续写/下一步/写正文/审核"时，主agent直接读项目根 `项目总控.html`——STATE区拿 phase/chapter/next_step，「Phase路线图」节拿路由（执行skill+门禁+产出），各子skill按自身SKILL.md干活。pipeline不写正文、不做内容转换、不常驻。

---

## SOP

### Step 1：初始化（新建项目）

触发：用户说"新建/初始化项目"且目录为空。

1. **前置检测**：LS扫描——若 `正文/` 有 ch* 文件或 `设计/` 有 .md → 转Step 2导入模式
2. **创建10目录**（PowerShell `-Force` 一次建齐）：`素材/` `素材/downloads/` `素材/知识沉淀/` `设计/` `设计/全书设定/` `设计/角色库/` `设计/第一卷剧情/` `产出/` `产出/白描卡/` `正文/` `审核/`
3. **生成总控**：读 `templates/项目总控.html` 写入项目根，按 html-update-protocol §1 更新 project_name/created_at/updated_at/genre
4. **README.md**：项目信息+目录说明+指向总控.html
5. **LS自检**：10目录+总控.html+README 共12项全存在，缺任一=初始化失败
6. 首次对话输出 `references/onboarding-guide.md` 引导语，然后进入Phase 0（用户意图深问；拆书与seed交互并行，详见总控.html Phase 0 卡）

### Step 2：导入/续写（已有资料）

触发：用户说"导入/续写/接续/迁移"，或初始化时检测到已有文件。

1. **资产扫描**：LS全部文件 → 原始资产清单（文件名+位置+一句话摘要）
2. **资产归位**（只归位不转换内容，格式转换仅 .docx/.txt→.md；正文统一编号 ch{NNN}.txt；匹配不上的问用户）：

| 用户文件（模糊匹配） | → 标准位置 |
|:--|:--|
| 意图/方向/想法 | `素材/用户意图.md` |
| 调研/市场/赛道/排行 | `素材/赛道调研.md` |
| 文风/DNA/笔触 | `素材/文风锚定.md` |
| 拆书/力量分析 | `素材/decon-lite-{书名}.md` |
| 立项/PRD/种子/创意 | `立项/01-立项PRD.md` |
| 力量/体系/骨架 | `设计/力量体系.md`+`动力引擎.md` |
| 金手指/外挂 | `设计/金手指.md` |
| 角色库/NPC | `设计/角色库/角色库.md` |
| 主线/剧情大纲 | `设计/主线.md` |
| 卷纲/大纲/分幕 | `设计/第一卷剧情/卷纲.md` |
| 章锚点/章节表 | `设计/第一卷剧情/章锚点表.md` |
| 正文/章节/ch*/第*章 | `正文/ch{NNN}.txt` |
| 白描卡/状态快照 | `产出/白描卡/ch{NNN}.md`+`产出/状态快照.md` |

3. **来源标记**：user-original/pipeline-relocated→⚠️需校验；skill-generated/reconstruct→✅
4. **缺口分析**（就绪判定=文件存在，查文件系统）：Phase 0 意图+调研 → 1 立项PRD → 3 力量体系+动力引擎+全书设定/ → 3.5 金手指+角色库 → 4 主线+卷纲+章锚点表 → 5 正文（当前章=最大编号+1） → 6 白描卡+状态快照
5. **落地Phase决策**：状态全（正文+白描卡+快照）→Phase 5续写；有正文缺状态→先review reconstruct再Phase 5；无正文→按就绪的最高Phase+1（全无→fresh Phase 0）
6. **补跑调度**（pipeline只识别+调度，深度转换由对应skill reconstruct完成）：有正文缺白描卡/快照→pop-qidian-review reconstruct（采样：≤10章全审/11-30章最近5章+每5取1/>30章最近5章+首章+每10取1）；缺设计文档→对应skill（seed/world/character/plot）reconstruct。输出补跑建议清单，**用户确认后执行**
7. **重建总控**：按 html-update-protocol §2 更新 mode/phase/chapter+circle+badge，展示资产清单+缺口报告+落地建议

### Step 3：总控.html 格式维护（协议指针）

所有html更新（初始化/导入重建/phase推进）按 `references/html-update-protocol.md`：STATE标记SearchReplace规范+Phase ID表+badge表，单源不复述。

---

## 红线（3条）

1. **只安装不生产**——pipeline不做内容转换/正文反推/设计补全，深度工作调度对应skill reconstruct完成。
2. **就绪判定查文件系统**——Phase推进条件=产出文件存在（不信口头声明）；三层骨架依赖链不可跳过（骨架→主角→血肉→写作）。
3. **user-original资产必须标⚠️需校验**——未经对应skill校验，设计层用户文件不得直接消费。

---

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `templates/项目总控.html` | Step 1 初始化时 | 状态文件模板（含Phase路线图） |
| `references/html-update-protocol.md` | 任何html更新时 | STATE字段规范（单源） |
| `references/onboarding-guide.md` | 用户首次触发专家时 | 首次对话引导语 |
| `项目总控.html`（项目空间） | 日常路由时（不经本skill） | STATE+Phase路线图=路由唯一源 |
