# step2 · 读项目总控路由 + 完成后更新

> 本文件是 pop-qidian-pipeline 第二步执行指令。每次对话开始时执行。

## 目标

读 项目总控.html → 判断当前 phase → 路由到对应 skill → 完成后用SearchReplace更新html

**v1.2.0核心变化**：不再有project-state.md。项目总控.html是唯一状态文件。agent直接用SearchReplace更新html中的`<!--STATE:xxx -->`标记字段和phase circle的CSS class。

## 执行

### 1. 读 项目总控.html

用Read工具读取项目根目录的 `项目总控.html`。

从HTML注释标记中提取当前状态：
- phase值：找 `<!--STATE:phase -->xxx<!--/STATE:phase -->`
- chapter值：找 `<!--STATE:chapter -->xxx<!--/STATE:chapter -->`
- next_step：找 `<!--STATE:next_step -->xxx<!--/STATE:next_step -->`

### 2. 按 phase 路由

对照 SKILL.md 速查表"启动时判断"，根据 phase 值路由到对应 Phase 流程。

### 3. Phase 完成后更新 项目总控.html

每个Phase完成后，用SearchReplace更新以下字段（不是全部，只更新本phase涉及的）：

#### 3a. 通用更新（每次phase完成都必须更新）

| 操作 | SearchReplace示例 |
|:--|:--|
| 更新phase | old: `<!--STATE:phase -->phase0<!--/STATE:phase -->` → new: `<!--STATE:phase -->phase1<!--/STATE:phase -->` |
| 更新timestamp | old: `<!--STATE:updated_at -->2026-07-22 14:00<!--/STATE:updated_at -->` → new: `<!--STATE:updated_at -->{当前时间}<!--/STATE:updated_at -->` |
| 更新next_step | old: `<!--STATE:next_step -->Phase 0: ...<!--/STATE:next_step -->` → new: `<!--STATE:next_step -->{下一步}<!--/STATE:next_step -->` |

#### 3b. Phase circle更新（标记完成+当前阶段）

把已完成的phase circle从`pending`改为`done`，把新阶段的circle从`pending`改为`current`：

| 操作 | SearchReplace示例 |
|:--|:--|
| 标记完成 | old: `class="phase-circle pending" id="ph-0"` → new: `class="phase-circle done" id="ph-0"` |
| 同上连线 | old: `class="phase-line" id="ln-0"` → new: `class="phase-line done" id="ln-0"` |
| 标记当前 | old: `class="phase-circle pending" id="ph-1"` → new: `class="phase-circle current" id="ph-1"` |
| 标记label活跃 | old: `<div class="phase-label" id="lb-1">` → new: `<div class="phase-label active" id="lb-1">` |

**Phase ID对照表**：

| Phase | circle id | line id | label id |
|:--|:--|:--|:--|
| Phase 0 | ph-0 | ln-0 | lb-0 |
| Phase 1 | ph-1 | ln-1 | lb-1 |
| Phase 3 | ph-3 | ln-3 | lb-3 |
| Phase 3.5 | ph-3_5 | ln-3_5 | lb-3_5 |
| Phase 4 | ph-4 | ln-4 | lb-4 |
| Phase 5 | ph-5 | ln-5 | lb-5 |
| Phase 6 | ph-6 | — | lb-6 |

#### 3c. 就绪状态更新（按phase产出更新对应badge）

| Phase完成 | 需要更新的badge |
|:--|:--|
| Phase 0 | deck_0(用户意图)→✅, deck_1(赛道调研)→✅, deck_2(参考书)→✅或跳过, deck_3(笔触DNA)→✅或跳过, deck_4(decon-lite)→✅或跳过 |
| Phase 1 | prd_0(立项PRD)→✅ |
| Phase 3 | skel_0(力量体系)→✅, skel_1(动力引擎)→✅, flesh_0(全书设定)→✅ |
| Phase 3→3.5 | flesh_1(DNA综合)→✅ |
| Phase 3.5 | prot_0(金手指)→✅, flesh_2(角色库)→✅ |
| Phase 4 | main_0(主线)→✅, flesh_3(卷纲)→✅, chapter→ch002 |

**badge SearchReplace示例**：
- old: `<!--STATE:skel_0 -->❌<!--/STATE:skel_0 -->` → new: `<!--STATE:skel_0 -->✅<!--/STATE:skel_0 -->`

#### 3d. 创意摘要更新（Phase 1完成后）

Phase 1 seed产出后，更新书名和一句话简介：
- old: `<!--STATE:book_name -->待seed产出<!--/STATE:book_name -->` → new: `<!--STATE:book_name -->{实际书名}<!--/STATE:book_name -->`
- old: `<!--STATE:one_line -->待seed产出<!--/STATE:one_line -->` → new: `<!--STATE:one_line -->{实际一句话}<!--/STATE:one_line -->`

#### 3e. 最近产出追加（每次phase完成都追加一行）

在`<!--STATE:outputs_start-->`和`<!--STATE:outputs_end-->`之间追加新行：

SearchReplace:
- old: `<!--STATE:outputs_start-->`
- new: `<!--STATE:outputs_start-->\n        <tr><td>{Phase名}</td><td class="file-path">{产出文件路径}</td><td>{时间}</td></tr>`

#### 3f. 流派记录（Phase 5开始时）

- old: `<!--STATE:write_skill -->待Phase 5指定<!--/STATE:write_skill -->` → new: `<!--STATE:write_skill -->pop-qidian-write（流派: {流派名}）<!--/STATE:write_skill -->`

### 路由规则要点

- Phase 0 → Phase 1：底牌就绪（用户意图+赛道调研）+ **产出真实性门禁**（decon-lite包含≥3处原文段落引用 + 文风锚定包含≥500字原文采样片段；若用户选择跳过拆书则跳过此项检查，但需在立项/01-立项PRD.md标注"无拆书参考"）
- Phase 1 → Phase 3：seed立项PRD就绪（立项/01-立项PRD.md六要素齐全）
- Phase 3 → Phase 3.5：全书设定+力量体系+动力引擎就绪
- Phase 3.5 → Phase 4：角色库+金手指就绪
- Phase 4 → Phase 5：主线+剧情白描+章锚点表就绪
- Phase 5 → Phase 6：正文产出
- Phase 6 → Phase 5（通过→下一章 / 打回→重写本章）

**Phase 6→Phase 5循环时**：只更新chapter值和next_step，不修改phase circle（Phase 5和6已在循环中交替）。

### Phase 0 详细规则

**Phase 0-1并行设计**：Stage1深问完成后，拆书任务和seed Step 0交互同时推进。S0前置收集+S1世界构筑仅需用户意图.md，不依赖拆书结果，可立即开始。S2力量体系设计消费拆书结果（decon-lite表1/表9），需等拆书完成或用已有信息先生成选项。主agent在seed交互间隙执行拆书任务。

**Phase 0执行顺序**：下载完成→主agent依次执行dna-style和decon-lite（串行，非并发）；赛道调研独立第一优先级执行。

**产出真实性门禁**：进入Phase 1前必须验证拆书产出基于真实原文，而非记忆/书评/评论重构。检查项：①decon-lite产出包含≥3处原文段落引用（非摘要复述） ②文风锚定产出包含≥500字原文采样片段。未通过=Phase 0未完成，禁止进入Phase 1。

**下载失败中断机制**：下载任务返回失败后，**禁止**执行decon-lite和dna-style。必须向用户报告下载失败并给出三个选项：①换一本可下载的参考书 ②用户手动提供txt文件路径 ③用户明确选择跳过拆书（后续seed基于通用知识生成，需用户确认接受质量降级）。用户未决策前，Phase 0 Stage 2的拆书分支暂停，seed交互分支可继续。

### Phase 1-4执行模式：主agent直接执行所有step

Phase 1-4在进入自动生成前，必须先完成Step 0交互式决策。核心轮用户确认后，进入执行型step，由主agent直接执行。

| Phase | Step 0交互轮次 | 核心必答/可选 | 决策表产出 | 完成后执行 |
|:--|:--|:--|:--|:--|
| 1 seed | Step1-3（灵感问答→种子碰撞+六要素PK→立项PRD定型） | Step2-3核心必答 | 立项/01-立项PRD.md | 主agent直接执行Step3立项PRD定型 |
| 3 world | Step0 W1-W2（2轮）+ Step0.5展开力量体系+动力引擎 | W1核心必答+W2可选 | 设计/世界决策表.md | 主agent直接执行step0.5-3 |
| 3.5 character | C1-C2（2轮） | C1核心必答+C2可选 | 设计/角色库/角色库决策表.md | 主agent直接执行金手指+角色库生成 |
| 4 plot | R1-R5（5轮） | 前3轮核心必答+后2轮可选 | 设计/第一卷剧情/卷纲决策表.md | 主agent直接执行主线展开+step1-3 |

**Phase 3.5 Character必须执行**——world完成后必须经过character建角色库，plot和write才能消费角色库。

**step分类与执行方式**：

| step类型 | 执行方式 | 示例 |
|:--|:--|:--|
| 交互型 | 主agent直接执行（需与用户多轮对话） | seed step1灵感/step2世界/step3决策轮、world step0决策、character step0决策、plot step0决策 |
| 执行型 | 主agent直接执行 | seed step3展开轮/step4主线、world step1-3、character step1、plot step1-3 |

**交互型step执行流程**：主agent读取skill SKILL.md+step文件 → 与用户多轮交互（给选项不给空白） → 产出决策表落盘

**执行型step执行流程（主agent直接执行）**：
1. 主agent读取skill SKILL.md → 提取红线（按红线清单执行）
2. 主agent读取对应step文件 → 按SOP逐步执行
3. 主agent读取项目输入文件 → 消费输入
4. 主agent按SOP执行生成 → 落盘产出
5. 主agent检查产出 → 更新项目总控 → 衔接下一step

---

## seed 执行型step执行指南（主agent直接执行）

> 主agent直接加载seed skill执行每个执行型step，禁止派发子agent。主agent读取skill SKILL.md+step文件 → 提炼红线+操作要点 → 消费项目输入文件 → 按SOP执行生成并落盘 → 检查产出 → 衔接下一step。

### 执行步骤（主agent直接执行）

1. 读取 `skills/pop-qidian-seed/SKILL.md` → 提取红线
2. 读取 `skills/pop-qidian-seed/steps/stepX-{name}.md` → 提炼操作要点
3. 读取输入文件：`素材/灵感收集.md` + `素材/用户意图.md` + `素材/赛道调研.md` + `素材/decon-lite-{书名}.md`（如有）
4. 按SOP执行生成 → 落盘产出
5. 检查产出 → 更新项目总控 → 衔接下一step

### Step3 立项PRD定型（主agent直接执行）

**执行时机**：Step1-2完成，种子候选+六要素骨架就绪后

**执行步骤**：
1. 读取 `skills/pop-qidian-seed/SKILL.md` → 提取红线
2. 读取 `skills/pop-qidian-seed/steps/step3-lixiang.md` → 提炼操作要点
3. 读取 `素材/灵感收集.md` → 提炼用户意图+种子候选摘要
4. 把Step 2用户最满意的种子，打磨成一份完整的六要素立项PRD（世界[含时间/地点/类型]+力量体系+人物+起因+经过+结果），一个能讲清楚的故事idea，落盘 `立项/01-立项PRD.md`

**红线（必须遵守）**：六要素是seed的最终产出；六要素说不清=立项失败；seed只做立项，不产设计/子文档（world/character/plot后续消费PRD里属于它的要素）

**完成后报告**：六要素摘要（世界/力量体系/人物/起因/经过/结果各一句话）

### seed 执行型step串联流程

```
Step1 灵感收集完成 → 素材/灵感收集.md
  ↓
Step2 种子碰撞（交互·六要素骨架+PK）→ 种子候选
  ↓
主agent直接执行 Step3 立项PRD定型（六要素故事）
  ↓ 产出 立项/01-立项PRD.md
主agent呈现给用户 → 用户确认立项 → seed完成
  ↓
主agent检查产出 → 更新项目总控 → 进入Phase 3 world
```

---

## Phase 3/3.5/4 主agent执行指南

> 主agent直接加载对应skill执行生成任务。执行前必须读取skill的SKILL.md获取骨架，再按Step加载step文件。

### Phase 3 world执行指南

**执行步骤**：
1. 读取 `skills/pop-qidian-world/` 下的 SKILL.md 和 steps/ 下所有step文件（step0-decision/step0.5-skeleton/step1-flesh/step2-fullbook/step3-output）了解完整SOP
2. 消费输入文件：立项/01-立项PRD.md + 设计/世界决策表.md
3. Step 0.5从PRD「力量体系+世界」方向句自己展开力量体系.md+动力引擎.md（四层+六组成）
4. 骨架消费验证门禁：验证力量体系.md+动力引擎.md 5项完整性（力量体系四层/动力引擎六组成/众生攀登方式分层/金手指不喧宾夺主/运转逻辑理解），任何一项不通过=报错中止
5. 按SOP执行：Step 1原则推导+因果链推演7维度→Step 2全书展开→Step 3落盘10个最小闭环文件（设计/全书设定/目录）

关键红线（必须遵守）：
- world从PRD方向句展开工程级——力量体系/动力引擎/7维度由world自己展开，金手指由character展开（world按PRD力量体系方向句展开，不落盘金手指）
- 地图必须有空间叙事价值（不是地名列表，每区域必须有空间法则+主角核心行为+信息差来源）
- 势力必须从引擎生长且4层全具名（有资源/没资源/爬到顶/掉下来，每层至少2个具名势力+领袖/代表）
- 危机是引擎阻力非随机威胁（必须对应动力引擎组成）
- 敌人是攀登方式代表非脸谱反派（弱点必须是攀登方式的结构性弱点）
- 各卷切片.md提供按卷导航（全书展开表覆盖3-8卷），下游按需读取对应设定文件

产出路径: 设计/力量体系.md + 设计/动力引擎.md + 设计/全书设定/（10个最小闭环文件）
完成后报告：力量体系子境界数、动力引擎范式、地图区域数、势力数、敌人阶梯层数、矛盾轴数。

### Phase 3→3.5 DNA重构调度

> **触发条件**：Phase 3（world）完成，全书设定文件落盘后，进入Phase 3.5之前
> **执行者**：主agent加载pop-dna-style Stage 2执行
> **为什么需要**：Stage 1（Phase 0）从参考书提取笔触层时，世界设定还没产出。现在世界设定有了，需要用世界画风+用户需求对笔触层做校验重构——笔触层的某些维度可能和本书世界画风矛盾（如弹窗式面板在生存记录感世界里不自然），需要修改或删除。

**执行步骤**：
1. 读取 `skills/pop-dna-style/SKILL.md` → 提取Stage 2红线（红线❌6重构权限+红线❌7单一文件）
2. 读取 `skills/pop-dna-style/steps/step5-synthesize.md` → 提炼操作要点
3. 读取输入文件：
   - `素材/文风锚定.md`（Stage 1产出v1，如存在）
   - `设计/全书设定/战斗系统.md`（战斗画风——产出E战斗画风表）
   - `设计/全书设定/物理规则.md`（环境画风——物理规则+源力量特性）
   - `设计/全书设定/民风民俗.md`（日常画风——民风民俗+政治经济调性）
   - `设计/全书设定/世界设计原则.md`（世界整体调性）
   - `素材/用户意图.md`（用户需求——面板偏好/主角姿态/节奏偏好）
   - `设计/世界决策表.md`（世界方向约束）
   - `设计/力量体系.md`（源力量特性）
   - `立项/01-立项PRD.md`（故事调性——六要素/起因经过结果/命运终点）
4. 按step5-synthesize.md SOP执行：世界画风提取→笔触层校验重构（三问每个维度）→三层综合产出
5. 产出覆盖 `素材/文风锚定.md`（v2·综合产出，替换v1）

**无参考书模式**：如果用户在Phase 0选择跳过拆书（文风锚定.md不存在），Stage 2从零构建——仅世界画风层+用户需求层，跳过笔触层校验。

**完成后报告**：校验结果汇总（保留N项/修改N项/删除N项）+ 画风层数量 + 用户需求覆盖情况
**完成后更新项目总控.html**：deck_3(笔触DNA)标记为"v2-综合产出"

### Phase 3.5 character执行指南

**执行步骤**：
1. 读取 `skills/pop-qidian-character/` 下的 SKILL.md 和 steps/ 下所有step文件了解完整SOP
2. 消费输入文件：立项/01-立项PRD.md（人物方向句）+ 设计/力量体系.md + 设计/动力引擎.md + 设计/全书设定/各卷切片.md（按需加载势力人物.md/危机敌人矛盾.md等） + 设计/角色库/角色库决策表.md
3. 按SOP执行：从PRD人物方向句展开主角深度卡+金手指（设计/金手指.md）→ 角色卡生成（配角/反派/盟友/中立角色）

关键红线（必须遵守）：
- 角色必须从世界矛盾中生长（欲望来自世界，阻碍来自危机，选择来自世界规则）
- 每个角色必须有攀登方式归属（对应骨架众生攀登方式分层4类）
- 金手指从PRD人物方向句展开，不喧宾夺主（key非生成器/赋能不越级/限制显性声明）
- 配角必须有独立性格+与主角的关系张力（不是工具人）
- 反派必须有自洽动机（动机=其攀登方式的必然冲突）
- 角色库是write的唯一角色源，正文不得引入角色库外的具名角色

产出路径: 设计/金手指.md + 设计/角色库/角色库.md
完成后报告：金手指限制代价、角色总数、各类型数量（主角/配角/反派/盟友/中立）。

### Phase 4 plot执行指南

**执行步骤**：
1. 读取 `skills/pop-qidian-plot/` 下的 SKILL.md 和 steps/ 下所有step文件了解完整SOP
2. 消费输入文件：立项/01-立项PRD.md（起因/经过/结果方向句）+ 设计/力量体系.md + 设计/动力引擎.md + 设计/全书设定/各卷切片.md（导航→按需加载物理规则.md/战斗系统.md/地理建筑.md/势力人物.md/危机敌人矛盾.md等） + 设计/角色库/角色库.md + 设计/金手指.md + 设计/第一卷剧情/卷纲决策表.md
3. 按SOP执行：主线展开（从PRD经过方向句展开设计/主线.md）→卷纲生成（四层结构+起承转合+精彩度五问自检）→章锚点表生成（4硬锚点+3软指导）

关键红线（必须遵守）：
- 主线从PRD「起因/经过/结果」方向句展开，不发明故事方向
- 起承转合四段式：每段必须填写事件+角色状态+目的，不能只写标签
- 章锚点表4硬锚点（章型/核心事件/爽感节点/章末钩子）不可更改，3软指导可调整
- 卷纲需通过精彩度五问自检（读者追读理由/意外性/情感投入/爽感密度/卷末高潮），任一问不通过需重做
- 剧情白描应基于四张地图叠加推演（地理/力量/势力/危机）
- 必须包含2-4条故事弧线，成长曲线分散在多个活动中，挫折需推动故事转向

产出路径:
- 设计/第一卷剧情/卷纲.md
- 设计/第一卷剧情/章锚点表.md
完成后报告：章数、故事弧线数、爽感节点分布。

### Phase 5 执行流程

```
触发条件：state.phase = phase5
前置检查：设计/第一卷剧情/卷纲.md + 设计/第一卷剧情/章锚点表.md + 设计/角色库/角色库.md + current_chapter 存在
```

1. **主agent直接加载write skill执行**——读取`skills/pop-qidian-write/`下的SKILL.md+step文件，按SOP执行正文写作
2. **永远调pop-qidian-write**（唯一write skill）。用户声明流派后，在write的Step 4自动加载`references/流派专属/{流派名}/`技法包
3. 执行指南见下方「Phase 5 write执行指南」
4. 产出`正文/chXXX.txt`
5. 更新项目总控.html：`phase=phase6`
6. **write完成后必须进入Phase 6 review**——不得连续写两章不review

### Phase 6 执行流程

```
触发条件：state.phase = phase6
前置检查：正文/chXXX.txt 存在
```

1. 调pop-qidian-review v3.7.0，产出`审核/chNNN-审核报告.md`（四步审核+骨架维度检查）
2. review Step 4沉淀产出：产出本章白描卡（`产出/白描卡/ch{NNN}.md`，只增不改）+ 更新剧情累计卡（`产出/剧情累计卡.md`，replace——钩子台账/角色当前状态/读者已知信息池/禁止漂移）。已废弃 current-state/小说快照/review-沉淀/压缩归档
3. 通过 → 更新项目总控.html：`phase=phase5`，`chapter=chNNN+1`
4. 打回 → 更新项目总控.html：`phase=phase5`（重写本章）

## Reconstruct主agent执行指南

> 导入模式 step0-import.md 0f 调度时使用。主agent直接加载对应skill的reconstruct模式执行。

### review reconstruct执行指南

**执行步骤**：
1. 读取 `skills/pop-qidian-review/` 下的 SKILL.md 和 steps/step-reconstruct.md 了解reconstruct模式完整SOP
2. 用LS扫描 正文/ 目录，获取所有章节文件列表，确定最大章节号
3. 按采样策略确定审核范围（≤10章全审 / 11-30章最近5章+每5章取1章 / >30章最近5章+第一章+每10章取1章）
4. 按SOP执行：逐章审核（信息提取+正向符合性简化+正文质量简化）→ 汇总生成状态文件

关键红线（必须遵守）：
- 采样章节必须做完整审核（信息提取+正向符合性简化+正文质量简化），非采样章节只快速提取关键信息
- 每章产出白描卡（只增不改），剧情累计卡 replace 更新（钩子台账含信息差类型+角色当前状态+读者已知池+禁止漂移）
- 未产出任何旧文档（current-state/小说快照/review-沉淀/压缩归档）

产出路径:
- 审核/chNNN-审核报告.md（每个采样章节一份，简版）
- 产出/白描卡/ch{NNN}.md（每个采样章节一张）
- 产出/剧情累计卡.md（replace模式，全书累计视图）
完成后报告：审核章数范围、采样策略、采样章数、总体质量判断。

### skill reconstruct执行指南（设计文档补跑）

**执行步骤**：
1. 读取 `skills/{skill名}/` 下的 SKILL.md 和 steps/ 下所有step文件了解完整SOP
2. 读取已有文件：{输入文件列表}
3. 按SOP执行reconstruct模式：读取已有文件 → 按skill方法论校验 → 缺失项补全 → 输出标准格式
4. 保留用户原始内容，只做校验+补全，不覆盖已有内容

关键红线（必须遵守）：
- reconstruct模式只校验+补全，不重新生成（保留用户已有内容）
- 产出必须符合该skill的标准格式和分节结构
- 产出文件标注source: skill-reconstruct

产出路径: {产出文件路径}
完成后报告：校验结果、补全项清单、文件来源标记。

## Phase 0 主agent执行指南

> 主agent直接加载对应tool/skill执行素材准备任务。执行前必须读取对应skill的SKILL.md获取SOP。

### 下载执行指南

**执行步骤**：
1. 读取 `skills/tool-download-webnovel/` 下的 SKILL.md 了解下载SOP
2. 按SOP执行下载（脚本搜索→web搜索兜底→验证交付）
3. Phase 1脚本搜索失败后必须执行Phase 2 web搜索（至少3组关键词），禁止直接放弃

产出路径: 素材/downloads/{书名}.txt
完成后报告产出文件路径和文件大小。

### 拆书执行指南（decon-lite）

**执行步骤**：
1. 读取 `skills/pop-qidian-research/` 下的 SKILL.md 和 steps/step-decon-lite.md 了解完整SOP
2. 验证参考书txt存在：素材/downloads/{书名}.txt。文件不存在=报错中止，禁止基于记忆/书评/评论重构
3. 按decon-lite档位SOP执行9表拆解

关键红线（必须遵守）：
- 9张表必须全拆，禁止缩减表数量
- 表1必须拆到规则级（主养成线+子养成线+chXX出处）
- 表9动力引擎三组成（驱动逻辑/运转机制/代价结构）必须齐全
- 产出元数据必须包含「采样源文件: 素材/downloads/{书名}.txt」字段

拆解目标: 《{书名}》（作者: {作者}）
产出路径: 素材/decon-lite-{书名}.md

### 文风DNA执行指南

**执行步骤**：
1. 读取 `skills/pop-dna-style/` 下的 SKILL.md 和 steps/step1.md 了解完整SOP
2. 验证参考书txt存在：素材/downloads/{书名}.txt。文件不存在=报错中止，禁止基于记忆/书评/评论替代原文
3. 按SOP执行笔触DNA提取（场景定向采样→v4模板分析→落盘）

关键红线（必须遵守）：
- 采样必须场景定向覆盖≥8种场景类型
- 每个维度/场景卡必须按v4模板：观察(1-2句)+原文(≥500字)+时间演变(1-2句)
- 只学笔触不学内容（不抄剧情/人设/世界观）
- 产出元数据必须包含「采样源文件: 素材/downloads/{书名}.txt」字段

参考书: 《{书名}》
产出路径: 素材/文风锚定.md

### Phase 5 write执行指南

**执行步骤**：
1. 读取 `skills/pop-qidian-write/` 下的 SKILL.md 了解完整SOP
2. 加载输入文件：设计/角色库/角色库.md + 设计/金手指.md + 素材/文风锚定.md + 设计/力量体系.md + 设计/动力引擎.md + 设计/第一卷剧情/章锚点表.md + 设计/第一卷剧情/卷纲.md
3. 按SOP执行：选章型→写正文→字数自检→落盘

当前章节: ch{N}（标题: {标题}）
流派: {流派名}（如有，在Step 4自动加载对应技法包）
产出路径: 正文/ch{N}.txt

write完成后报告：字数、章型、爽感节点执行情况。

### 下载失败处理流程
1. 下载任务返回失败 → **禁止**执行decon-lite和dna-style
2. 向用户报告：下载失败，给出三个选项：
   - ①换一本可下载的参考书
   - ②用户手动提供txt文件路径（放到素材/downloads/目录下）
   - ③跳过拆书（seed基于通用知识生成，需用户确认接受质量降级）
3. 用户选择①→重新下载；选择②→验证txt后执行拆书；选择③→Phase 0标记"无拆书参考"，直接进Phase 1

## 质量门

- 每次路由前必读 项目总控.html
- 每次Phase完成后必更新 项目总控.html（至少更新phase+timestamp+next_step+circle）
- 三层骨架依赖链不可跳过
