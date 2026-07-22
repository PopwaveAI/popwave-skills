# CHANGELOG

## v3.1.0 - 2026-07-22

### 新增：小说快照（全书累计视图）
- **Step 4c 新增小说快照更新**——每章review完成后更新`审核/小说快照.md`（replace模式），产出全书累计视图
- 小说快照包含6个维度：全书进度/涌现设定累计/角色状态总表/剧情线进度/读者已知信息池/待回收伏笔总表
- 与current-state.md（面向下一章write的即时信息）和状态快照（单章视角）互补，小说快照是全书累计视图
- 新增红线11：小说快照每章必更新，不更新=沉淀未完成
- 速查表更新：Step 4沉淀产出新增"小说快照"

## v3.0.0 - 2026-07-21

### 版本升级：四维审核框架 + 骨架维度检查
- 引入四维审核框架（符合性/笔触/好看度/沉淀），审核优先级：符合性 > 笔触 > 好看度 > 沉淀。前面不通过后面不审。
- SOP 骨架重组为四维：
  - **维度一 符合性检查**：1a 核心事件对照（保留 v2.0.1 gap 逐 beat 对比）/1b 骨架一致性（新增：1b-1 力量体系一致性 + 1b-2 动力引擎一致性）/1c 天赋约束检查（新增：金手指是否喧宾夺主 + 限制/代价兑现）/1d 剧情映射检查（新增：地图/势力/人物/剧情是否映射坐标系）/1e 角色一致性（含攀登方式一致性）/1f 爽感闭环（触发→爆发→后果三段式 + 爽感因子检查：坐标系门槛×天赋加速×代价约束至少触发两个）
  - **维度二 笔触检查**：2a AI 味 7 项（从番茄 review 移植：句式重复/情绪直给/结尾收束/描写堆叠/信息重复/对话死板/高疲劳词）+ 2b 笔触 DNA 一致性（保留 v2.0.1 的 8 维度笔触审核）
  - **维度三 好看度检查（新增）**：定性 4 问（有没有劲/记忆点/哪里无聊/代入感），从番茄 review 移植
  - **维度四 剧情沉淀**：保留 v2.0.1 的 current-state.md 更新机制 + 历史层归档（压缩归档/ + review-沉淀.md）+ 新增主角变化五项（位置/能力/资产/心态/关系，从番茄 review 移植）+ 新增钩子追踪（待回收 >3 章标红，从番茄 review 移植）
- 产出文件审核-chXXX.md 新增字段：骨架一致性结论 / 天赋约束结论 / 剧情映射结论 / 好看度 4 问结论 / 主角变化五项 / 钩子追踪
- 新增红线：骨架一致性检查不通过=废章，必须打回重写 / 天赋约束检查发现金手指取消坐标系意义=废章。保留 v2.0.1 现有红线。
- 输入新增骨架.md + 主角设计.md（来自 seed），用于骨架维度检查（力量体系四层结构 + 动力引擎六组成 + 金手指梗×机制×限制 + 爽感矛盾公式）。
- 保留 v2.0.1 的 gap 分析 5 种类型（提速/延迟/偏离/遗漏/新增）+ gap 质量判断 5 维度 + current-state 更新机制 + 历史层归档 + execution.mode 三档 + 红线 7 项 + 笔触 DNA 8 维度。
- 参考来源：pop-fanqie-review v4.2.1（四维审核框架/好看度 4 问/主角变化五项/钩子追踪/AI 味 7 项）+ pop-qidian-seed v8.1.0（骨架.md/主角设计.md 格式）。
- 未修改 steps 目录下的 step-1-audit.md 和 step-2-commit.md。
- 版本三处一致：SKILL.md + skill.json + CHANGELOG.md = 3.0.0。

## v2.0.0 - 2026-07-14

### 版本升级：番茄 review 覆盖
- 番茄小说创作 skill 群覆盖替换 pop-qidian 系列。
- SKILL.md 采用番茄 review 全文（逐beat对比/gap分类/质量判断5维度/笔触审核8维度/状态快照/红线/速查表），保留全部原始内容不变。
- 新增 frontmatter（name: pop-qidian-review）。
- 新增 execution.mode 三档（formal/draft/trial）。
- 新增 current-state 更新章节（吸收自 pop-qidian 架构资产：更新规则/历史层规则/沉淀分流）。
- 保留 steps/step-2-commit.md（current-state 更新逻辑）和 templates/current-state.tpl.md（current-state 模板）。

## v3.7.0 - 2026-07-09

### 调整：章内文风DNA审计
- 审稿 SOP 从三层审计改为章内笔触和单章套路审计。
- current-state 的 `本章DNA执行包` 改为章型、笔触目标、章内套路、可见反馈、禁止误用。
- 下一章执行包禁止迁移全书架构、角色口癖、开篇专用机制和特殊高光章。

## v3.6.0 - 2026-07-08

### 新增：文风DNA三层审计
- 审稿 SOP 从 6 步升级为 7 步，新增文风DNA三层执行检查。
- 新增层1笔触、层2叙事组织、层3商业反馈、角色/口癖污染检查。
- current-state 模板新增 `本章DNA执行包`，供下一轮 write 消费。
- step-2 新增下一章DNA执行包写入规则，避免 DNA 停留在审稿建议里。

## v3.5.0 - 2026-07-06

### 重构：四层架构对齐
- SKILL.md 重写为 ≤60 行入口文件，删除自有 execution.mode 三档表，改引 PRD §4.5。
- skill.json 补全 version/displayName/entry/activation/permissions 字段。
- 新增 steps/step-1-audit.md：审稿 6 步 SOP + 归因规则表 + 门禁。
- 新增 steps/step-2-commit.md：沉淀分流执行，归档/覆盖/沉淀职责分离。
- 新增 templates/current-state.tpl.md：current-state 空模板（元数据块 + 章节结构）。

### 核心修复（问题 9：历史层职责分离）
- current-state 更新前先归档旧版到 `涌现/压缩归档/current-state-{YYYYMMDD}-{章位}.md`，再覆盖 current-state.md。
- review-沉淀.md 改为 append-only：每次审稿在末尾追加一段，不删改历史。
- 两者不重叠：沉淀记"判断和规则"，归档存"旧版入口包全文"（见 PRD §4.4）。

### 核心修复（问题 8：燃料文件引用统一）
- 燃料文件唯一名 `research-写作燃料.md`，删除"或 燃料库.md"别名（见 PRD §4.3）。

### 契约对齐
- 骨架/owner/命名/execution.mode/回复格式引用 PRD §4（../pop-qidian/references/v3.5-pipeline-prd.md）。
- 版本三处一致：SKILL.md + skill.json + CHANGELOG.md = 3.5.0。

## v1.1.0
- 旧版单文件 SKILL.md，含自有 execution.mode 三档表、current-state 模板内联、库文件更新建议表，燃料文件出现 `燃料库.md` 别名，无四层架构，无步骤文件，无归档/沉淀职责分离。