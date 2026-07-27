# Step 0: 导入/续写模式

> 当用户已有历史资料/设定/正文时，将已有资料归位到 pipeline 标准位置，调度对应 skill 进行深度拆解/补全，重建项目状态并路由到正确Phase。
> 核心理念：pipeline 是调度员不是制造者——只做资产清点和文件归位，深度内容转换交给对应 skill 的 reconstruct 模式。

## 触发条件（任一满足即进入本Step）

1. 用户明确说"导入/续写/已有/接续/迁移"
2. Step 1初始化时检测到 `正文/` 或 `设计/` 已有文件
3. 项目目录已有内容但无项目总控.html

---

## 执行

### 0a. 资产扫描

用LS扫描项目目录（或用户指定的源目录），列出所有已有文件。

 输出：**原始资产清单**（文件名 + 位置 + 内容摘要1句话）

### 0b. 资产归位

> pipeline 只做文件名/目录归位，不做内容结构标准化。内容深度转换由对应 skill 在 reconstruct 模式下完成（见0f）。

#### 0b-1. 文件名+目录归位

将用户文件映射到标准位置并重命名：

| 用户文件（模糊匹配） | → 标准位置 | 标准文件名 | 对应Phase |
|:--|:--|:--|:--|
| *意图* / *方向* / *想法* / 用户口述 | `素材/` | `用户意图.md` | Phase 0 |
| *调研* / *市场* / *赛道* / *排行* | `素材/` | `赛道调研.md` | Phase 0 |
| *文风* / *DNA* / *笔触* / *风格* | `素材/` | `文风锚定.md` | Phase 0 |
| *decon* / *拆书* / *力量分析* | `素材/` | `decon-lite-{书名}.md` | Phase 0 |
| *骨架* / *体系* / *力量* / *设定大纲* | `设计/` | `力量体系.md`+`动力引擎.md` | Phase 1 |
| *创意* / *故事* / *纲领* / *简介* | `设计/` | `创意.md` | Phase 1 |
| *立项* / *决策* / *选择* | `设计/` | `立项决策表.md` | Phase 1 |
| *主角* / *角色设计* / *人物* | `设计/` | `主角设计.md` | Phase 2 |
| *世界* / *地图* / *势力* / *危机* / *敌人* / *圣经* | `设计/全书设定/` | 各自对应文件名 | Phase 3 |
| *世界决策* | `设计/` | `世界决策表.md` | Phase 3 |
| *角色库* / *NPC* / *配角* | `设计/角色库/` | `角色库.md` | Phase 3.5 |
| *卷纲* / *大纲* / *分幕* | `设计/第一卷剧情/` | `卷纲.md` | Phase 4 |
| *章锚点* / *章节表* / *章节规划* | `设计/第一卷剧情/` | `章锚点表.md` | Phase 4 |
| *正文* / *章节* / ch* / 第*章 | `正文/` | `ch{NNN}.txt` | Phase 5 |
| *快照* / *状态* / *进度* | `审核/` | `小说快照.md` | Phase 6 |
| *current-state* / *入口包* | 项目根 | `current-state.md` | Phase 6 |

**操作**：
1. 匹配不上的文件归入"未分类资产"，询问用户映射到哪个标准位置
2. 格式转换：.docx/.txt → .md（用Read读取内容→Write写入标准位置标准文件名）
3. 正文文件统一编号：`第一章.txt` / `chapter1.md` → `正文/ch001.txt`
4. 询问用户是否保留原文件

#### 0b-2. 文件来源标记

每个归位文件在资产清单中标记来源和质量状态，写入 `项目总控.html` 产出表：

| 来源标记 | 含义 | 后续处理 |
|:--|:--|:--|
| `user-original` | 用户已有文件，直接归位 | 标注"⚠️需校验"，后续可调度skill校验 |
| `pipeline-relocated` | pipeline做了格式转换(.docx→.md等) | 标注"⚠️需校验" |
| `skill-generated` | 对应skill正向产出 | 正常消费 |
| `skill-reconstruct` | 对应skill reconstruct模式产出 | 正常消费 |

> 后续 skill 消费文件时可查看来源标记决定信任程度。`user-original`/`pipeline-relocated` 的设计层文件应标注"⚠️需校验"。

### 0c. 缺口分析

归位完成后，对照依赖链逐Phase检查：

| Phase | 产出 | 就绪判定 |
|:--|:--|:--|
| Phase 0 | 用户意图.md + 赛道调研.md | 两者都有=✅ |
| Phase 1 | 力量体系.md + 动力引擎.md + 创意.md | 三者都有=✅ |
| Phase 2 | 主角设计.md | 存在=✅ |
| Phase 3 | 全书设定/ 有文件 | 目录有文件=✅ |
| Phase 3.5 | 角色库/角色库.md | 存在=✅ |
| Phase 4 | 第一卷剧情/卷纲.md + 章锚点表.md | 两者都有=✅ |
| Phase 5 | 正文/ch*.txt | 有正文=✅ |
| Phase 6 | 审核/小说快照.md | 存在=✅ |

**正文进度检测**：如果 `正文/` 有文件，提取最大章节号。例如有 ch001.txt~ch015.txt → current_chapter = ch016（下一章待写）。

**质量来源检测**：对每个已就绪的Phase，检查文件来源标记。`user-original`或`pipeline-relocated`的文件标注"⚠️需校验"，`skill-generated`或`skill-reconstruct`的标注"✅已验证"。

 输出：**缺口报告**（哪些Phase已就绪/哪些缺失 + 每个文件的质量来源标记）

### 0d. 落地Phase决策

根据缺口报告 + 正文进度，按下表决定落地Phase：

| 条件 | mode | 落地Phase | 说明 |
|:--|:--|:--|:--|
| 正文有 + 小说快照有 + current-state有 | resume | Phase 5（续写下一章） | 状态完整，直接接续 |
| 正文有 + 状态文件缺失 | resume | 先执行0f调度review reconstruct → Phase 5 | 需补建状态文件 |
| 正文无 + Phase 4就绪 | import | Phase 5（开始写） | 设定+剧情完整 |
| 正文无 + Phase 3.5就绪 | import | Phase 4（plot） | 缺剧情 |
| 正文无 + Phase 3就绪 | import | Phase 3.5（character） | 缺角色库 |
| 正文无 + Phase 2就绪 | import | Phase 3（world） | 缺世界设定 |
| 正文无 + Phase 1就绪 | import | Phase 2（主角） | 缺主角设计 |
| 正文无 + Phase 0就绪 | import | Phase 1（seed） | 缺骨架 |
| 全无 | fresh | Phase 0 | 从零开始（走正常step1流程） |

→ **向用户展示资产清单（含来源标记）+ 缺口报告 + 落地Phase建议 + 补跑建议清单（见0f-4），用户确认后进入0e**

### 0e. 状态文件重建

#### 创建/更新项目总控.html

如果 `项目总控.html` 不存在，读取模板 `templates/项目总控.html` 写入项目根目录。如果已存在，直接SearchReplace更新。

用SearchReplace更新以下字段：

| 标记 | 替换值 |
|:--|:--|
| `<!--STATE:mode -->fresh<!--/STATE:mode -->` | `<!--STATE:mode -->{import/resume}<!--/STATE:mode -->` |
| `<!--STATE:phase -->init<!--/STATE:phase -->` | `<!--STATE:phase -->{落地Phase}<!--/STATE:phase -->` |
| `<!--STATE:chapter -->ch000<!--/STATE:chapter -->` | `<!--STATE:chapter -->{current_chapter}<!--/STATE:chapter -->` |
| `<!--STATE:project_name -->未命名项目<!--/STATE:project_name -->` | `{用户给的项目名}` |
| `<!--STATE:updated_at -->--<!--/STATE:updated_at -->` | `{当前时间}` |

#### 标记已完成Phase circle + 就绪badge

将已就绪的Phase circle从 `pending` 改为 `done`，将落地Phase从 `pending` 改为 `current`。将已有资产对应的badge从❌改为✅。参照step2.md的更新规则。

Phase ID对照表（同step2.md）：

| Phase | circle id | line id | label id |
|:--|:--|:--|:--|
| Phase 0 | ph-0 | ln-0 | lb-0 |
| Phase 1 | ph-1 | ln-1 | lb-1 |
| Phase 2 | ph-2 | ln-2 | lb-2 |
| Phase 3 | ph-3 | ln-3 | lb-3 |
| Phase 3.5 | ph-3_5 | ln-3_5 | lb-3_5 |
| Phase 4 | ph-4 | ln-4 | lb-4 |
| Phase 5 | ph-5 | ln-5 | lb-5 |
| Phase 6 | ph-6 | — | lb-6 |

### 0f. 调度skill补跑

> pipeline 不自行做内容结构标准化、正文反推、设计文档补建。这些深度工作由主agent加载对应 skill 的 reconstruct 模式完成。pipeline 只负责识别缺口 + 调度skill执行 + 汇报结果。

#### 0f-1. 补跑策略

根据缺口报告，对以下情况调度 skill 补跑：

| 缺口类型 | 调度skill | reconstruct做什么 | 执行指南 |
|:--|:--|:--|:--|
| 有正文 + 缺current-state/小说快照 | review | 批量回溯审核已有正文 → 生成current-state + 小说快照 + review-沉淀 | step2.md「review reconstruct执行指南」 |
| 缺Phase 1-4设计文档 | 对应skill（seed/world/character/plot） | 读取已有文件 → 按skill方法论校验+补全 → 输出标准格式 | step2.md「skill reconstruct执行指南」 |
| 已有设计文档但来源=user-original | 对应skill | 读取已有文件 → 按skill方法论校验 → 标注缺口或确认达标 | 按需调度（用户确认后） |

**不调度的情况**（pipeline自行处理）：
- 素材层文件（Phase 0）：用户意图.md/赛道调研.md等，pipeline按标准分节简单重组即可
- 文风锚定.md：用户已有则直接归位；缺失则需用户先跑 pop-dna-style（非reconstruct场景）

#### 0f-2. review reconstruct（有正文但缺状态文件时执行）

> 触发条件：`正文/` 有文件 且 `审核/小说快照.md` 或 `current-state.md` 不存在

**主agent必须加载review skill执行**——按review reconstruct模式的SOP执行正文反推。执行指南见 step2.md「review reconstruct执行指南」。

主agent执行 review 的 reconstruct 模式（见 `skills/pop-qidian-review/steps/step-reconstruct.md`）：
- 输入：已有正文章节
- 采样策略：≤10章全审 / 11-30章最近5章+每5章取1章 / >30章最近5章+第一章+每10章取1章
- 产出：
  - `审核/chNNN-审核报告.md`（每章一份，简版）
  - `current-state.md`（最新章位状态，含DNA执行包，来源标记`skill-reconstruct`）
  - `审核/小说快照.md`（全书累计视图）
  - `审核/review-沉淀.md`（append，合并所有章的判断）

#### 0f-3. 设计文档补跑（缺设计文档时执行）

> 触发条件：落地Phase > 1 且 前置Phase的设计文档缺失或来源为user-original

对缺失的设计文档，按依赖链顺序调度对应skill补跑：

| 缺失文档 | 调度skill | 输入 | 产出 |
|:--|:--|:--|:--|
| 力量体系.md+动力引擎.md | seed | 已有正文（如有）+用户设定 | 标准骨架文件 |
| 主角设计.md | seed | 骨架文件+已有正文（如有） | 标准主角设计 |
| 世界圣经.md | world | 骨架+主角+已有世界设定 | 标准世界圣经 |
| 角色库.md | character | 骨架+主角+世界圣经+已有正文 | 标准角色库 |
| 卷纲.md+章锚点表.md | plot | 骨架+主角+世界圣经+角色库+已有正文 | 标准卷纲+章锚点表 |

> **注意**：如果用户已有正文但缺卷纲+章锚点表，plot reconstruct模式会从正文反推卷纲。如果用户选择跳过plot直接续写（降级模式），需在current-state.md中手动指定下一章核心事件，write按current-state指导续写。后续可补跑plot生成正式卷纲。

#### 0f-4. 补跑建议清单（输出给用户）

```
⚠️ 导入模式质量报告：
- [文件名]：来源={user-original/pipeline-relocated/skill-reconstruct}，状态={✅已验证/⚠️需校验/❌缺失}，建议={正常消费/补跑XX skill}
- ...
- current-state.md：来源={skill-reconstruct/缺失}，状态={✅/⚠️/❌}
```

用户根据清单决定：
- 正常接续（接受当前文件质量）
- 按需补跑（指定哪些文件需要调度skill校验/补全）
- 全量补跑（所有"需校验"文件都过一遍对应skill）

---

## 质量门

- [ ] 原始资产清单已生成
- [ ] 资产归位已完成（文件名+目录归位 + 来源标记已标注）
- [ ] 缺口报告已生成（含质量来源标记）
- [ ] 落地Phase已确定并经用户确认
- [ ] 项目总控.html已创建/更新（mode + phase + chapter + circle + badge 全部正确）
- [ ] 补跑策略已确定（review reconstruct / 设计文档补跑 / 用户选择跳过）
- [ ] 补跑建议清单已展示给用户

## 下一步

> 根据落地Phase，加载 `steps/step2.md` 进入路由循环。
> 如果需要先执行0f补跑，在step2.md路由前先执行reconstruct任务。

---
## ⛔ 加载门禁 + 下一步指引
> 下一 step：`steps/step2.md`
> 什么时候进入下一步：项目总控.html重建完成 + 用户确认落地Phase + 补跑策略已确定
