---
name: pop-qidian-pipeline
description: 起点项目安装器（一次性）。当用户说"初始化项目""新建项目""导入""续写""迁移已有资料"时启用。一次性建目录+生成 状态.md（唯一机器状态源）+资产归位+缺口分析；日常写作路由由专家提示词阶段地图承载，html为可选展示面板，写正文/审核不经过本skill。
---

# pipeline（一次性安装器）

> 起点项目安装器。**v4.3.0：状态源收敛 `状态.md`**（唯一机器状态源）+ 日常写作路由上移专家提示词，pipeline 只做一次性安装/导入。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

## 做什么

| 职责 | 说明 |
|:--|:--|
| 一次性安装 | 新建项目：标准化目录 + `状态.md`（薄机器状态）+（可选）导出展示面板 + README |
| 一次性导入 | 已有资料：资产清点→归位→缺口分析→落地Phase→状态重建→调度补跑 |
| 状态文件维护 | `状态.md` = 唯一机器状态源，agent 只读/写它的状态片段；`项目总控.html` 为仅供老板查看的展示面板，按需由 agent 套 状态.md 值导出，**agent 不参与渲染也不读它** |

**日常路由不经此skill**：用户说"继续写/下一步/写正文/审核"时，主agent按**专家提示词阶段地图**直接选 skill（默认顺序：立项→世界→角色→剧情→正文→审核；门禁：就绪态查文件系统、底牌就绪），先读项目根 `状态.md` 取状态片段（mode/phase/current_chapter/next_step/就绪态），各子skill按自身SKILL.md干活。pipeline不写正文、不做内容转换、不常驻。

### 状态.md（薄机器状态，唯一状态源）

写入项目根，agent 每轮只读它取状态片段。模板见 `templates/状态.md`，内容：

```markdown
mode: fresh            # fresh/import/resume
phase: init            # init/0/1/3/3.5/4/5/6
current_chapter: ch000 # 下一章待写（本章写完后+1）
next_step: Phase 0: 用户意图深问
project_name: 未命名项目
genre: 待指定
created_at: --
updated_at: --

## 书目
book_name: 待seed产出
one_line: 待seed产出
write_skill: 待Phase 5指定

## 就绪态（[x]=就绪 / [ ]=未就绪；就绪判定查文件系统）
底牌就绪: 用户意图[ ] 赛道调研[ ] 参考书[ ] 笔触DNA[ ] decon-lite[ ]
立项就绪: 立项PRD[ ]
世界就绪: 力量体系[ ] 动力引擎[ ] 全书设定[ ]
角色就绪: 金手指[ ] 角色库[ ]
剧情就绪: 主线[ ] 卷纲[ ]
文风就绪: DNA综合[ ]

## 最近产出
- {Phase名}: {产出文件路径} | {时间}
```

---

## SOP

### Step 1：初始化（新建项目）

触发：用户说"新建/初始化项目"且目录为空。

1. **前置检测**：LS扫描——若 `正文/` 有 ch* 文件或 `设计/` 有 .md → 转Step 2导入模式
2. **创建10目录**（PowerShell `-Force` 一次建齐）：`素材/` `素材/downloads/` `素材/知识沉淀/` `设计/` `设计/全书设定/` `设计/角色库/` `设计/第一卷剧情/` `产出/` `产出/白描卡/` `正文/` `审核/`
3. **生成 状态.md**：读 `templates/状态.md` 写入项目根，按「状态更新协议 §1」更新 project_name/created_at/updated_at/genre（机器状态源）
4. **展示面板（可选）**：仅当老板要看可视化面板时，按 `templates/项目总控.html` 套 状态.md 值导出 html——agent 只写 状态.md，不读 html
5. **README.md**：项目信息+目录说明+指向 状态.md（和可选 html）
6. **LS自检**：10目录+状态.md+README 共12项全存在，缺任一=初始化失败
7. 首次对话输出 `references/onboarding-guide.md` 引导语，然后进入Phase 0（用户意图深问；拆书与seed交互并行，详见 状态.md next_step）

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
7. **状态重建**：按「状态更新协议 §2」更新 状态.md 的 mode/phase/current_chapter/就绪态，展示资产清单+缺口报告+落地建议

### Step 3：状态.md 格式维护（协议指针）

所有 状态.md 更新（初始化/导入重建/phase推进/每章推进）按 `references/状态更新协议.md`：字段 SearchReplace 规范+就绪态标记+单源不复述。**phase 推进由对应 skill（write/review/seed/world/character/plot）完成后更新 状态.md，pipeline 只在初始化/导入时碰它。**

---

## 红线（4条）

1. **只安装不生产**——pipeline不做内容转换/正文反推/设计补全，深度工作调度对应skill reconstruct完成。
2. **就绪判定查文件系统**——Phase推进条件=产出文件存在（不信口头声明）；三层骨架依赖链不可跳过（骨架→主角→血肉→写作）。
3. **user-original资产必须标⚠️需校验**——未经对应skill校验，设计层用户文件不得直接消费。
4. **状态源**——`状态.md`=唯一机器状态源，agent 每轮只读/写它；`项目总控.html` 仅供老板查看的展示面板，按需导出，**agent 不读 html**、不承担渲染成本。

---

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `templates/状态.md` | Step 1 初始化时 | 机器状态模板（唯一状态源） |
| `templates/项目总控.html` | 老板要看展示面板时（按需可选） | 展示面板模板（由 状态.md 套值导出，agent 不读） |
| `references/状态更新协议.md` | 任何 状态.md 更新时 | 字段规范+就绪态标记（单源） |
| `references/onboarding-guide.md` | 用户首次触发专家时 | 首次对话引导语 |
| `状态.md`（项目空间） | agent 每轮只读它 | 唯一机器状态源（mode/phase/current_chapter/next_step/就绪态/brief/最近产出） |
