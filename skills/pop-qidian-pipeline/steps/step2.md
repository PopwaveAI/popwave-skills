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
| Phase 2 | ph-2 | ln-2 | lb-2 |
| Phase 3 | ph-3 | ln-3 | lb-3 |
| Phase 3.5 | ph-3_5 | ln-3_5 | lb-3_5 |
| Phase 4 | ph-4 | ln-4 | lb-4 |
| Phase 5 | ph-5 | ln-5 | lb-5 |
| Phase 6 | ph-6 | — | lb-6 |

#### 3c. 就绪状态更新（按phase产出更新对应badge）

| Phase完成 | 需要更新的badge |
|:--|:--|
| Phase 0 | deck_0(用户意图)→✅, deck_1(赛道调研)→✅, deck_2(参考书)→✅或跳过, deck_3(笔触DNA)→✅或跳过, deck_4(decon-lite)→✅或跳过 |
| Phase 1 | skel_0(力量体系)→✅, skel_1(动力引擎)→✅, skel_2(骨架自洽)→✅ |
| Phase 2 | prot_0(主角设计)→✅, prot_1(金手指)→✅, prot_2(爽感矛盾)→✅ |
| Phase 3 | flesh_0(全书设定)→✅ |
| Phase 3→3.5 | flesh_1(DNA综合)→✅ |
| Phase 3.5 | flesh_2(角色库)→✅ |
| Phase 4 | flesh_3(卷纲)→✅, chapter→ch002 |

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

- Phase 0 → Phase 1：底牌就绪（用户意图+赛道调研）+ **产出真实性门禁**（decon-lite包含≥3处原文段落引用 + 文风锚定包含≥500字原文采样片段；若用户选择跳过拆书则跳过此项检查，但需在立项决策表标注"无拆书参考"）
- Phase 1 → Phase 2：骨架就绪（力量体系+动力引擎+骨架自洽）
- Phase 2 → Phase 3：主角就绪（主角设计+金手指+爽感矛盾）
- Phase 3 → Phase 3.5：全书设定就绪
- Phase 3.5 → Phase 4：角色库就绪
- Phase 4 → Phase 5：剧情白描+章锚点表就绪
- Phase 5 → Phase 6：正文产出
- Phase 6 → Phase 5（通过→下一章 / 打回→重写本章）

**Phase 6→Phase 5循环时**：只更新chapter值和next_step，不修改phase circle（Phase 5和6已在循环中交替）。

### Phase 0 详细规则

**Phase 0-1并行设计**：Stage1深问完成后，拆书任务和seed Step 0交互同时推进。S0前置收集+S1世界构筑仅需用户意图.md，不依赖拆书结果，可立即开始。S2力量体系设计消费拆书结果（decon-lite表1/表9），需等拆书完成或用已有信息先生成选项。主agent在seed交互间隙执行拆书任务。

**Phase 0执行顺序**：下载完成→主agent依次执行dna-style和decon-lite（串行，非并发）；赛道调研独立第一优先级执行。

**产出真实性门禁**：进入Phase 1前必须验证拆书产出基于真实原文，而非记忆/书评/评论重构。检查项：①decon-lite产出包含≥3处原文段落引用（非摘要复述） ②文风锚定产出包含≥500字原文采样片段。未通过=Phase 0未完成，禁止进入Phase 1。

**下载失败中断机制**：下载任务返回失败后，**禁止**执行decon-lite和dna-style。必须向用户报告下载失败并给出三个选项：①换一本可下载的参考书 ②用户手动提供txt文件路径 ③用户明确选择跳过拆书（后续seed基于通用知识生成，需用户确认接受质量降级）。用户未决策前，Phase 0 Stage 2的拆书分支暂停，seed交互分支可继续。

### Phase 1-4执行模式：交互型step主agent执行 + 执行型step子agent派发

Phase 1-4在进入自动生成前，必须先完成Step 0交互式决策。核心轮用户确认后，进入执行型step。

| Phase | Step 0交互轮次 | 核心必答/可选 | 决策表产出 | 完成后执行 |
|:--|:--|:--|:--|:--|
| 1 seed | S0-S5（6轮） | S1-S4核心必答+S5可选 | 设计/立项决策表.md | 主agent派发子agent执行step3-7 |
| 3 world | W1-W2（2轮） | W1核心必答+W2可选 | 设计/世界决策表.md | 主agent派发子agent执行step1-3（待改造） |
| 3.5 character | C1-C2（2轮） | C1核心必答+C2可选 | 设计/角色库/角色库决策表.md | 主agent派发子agent执行角色库生成（待改造） |
| 4 plot | R1-R5（5轮） | 前3轮核心必答+后2轮可选 | 设计/第一卷剧情/卷纲决策表.md | 主agent派发子agent执行step1-3（待改造） |

**Phase 3.5 Character必须执行**——world完成后必须经过character建角色库，plot和write才能消费角色库。

**step分类与执行方式**：

| step类型 | 执行方式 | 示例 |
|:--|:--|:--|
| 交互型 | 主agent直接执行（需与用户多轮对话） | seed step1底牌/step2决策、world step0决策、character step0决策、plot step0决策 |
| 执行型 | 主agent派发子agent执行 | seed step3-7、world step1-3、character step1、plot step1-3 |

**交互型step执行流程**：主agent读取skill SKILL.md+step文件 → 与用户多轮交互（给选项不给空白） → 产出决策表落盘

**执行型step执行流程**（方案3·混合执行）：
1. 主agent读取skill SKILL.md → 提取红线（3-5条）
2. 主agent读取对应step文件 → 提炼操作要点（50-100行摘要）
3. 主agent读取项目输入文件 → 提炼项目上下文摘要
4. 主agent组装instruction（核心层：红线+操作要点+上下文 / 引用层：文件路径）
5. 主agent派发子agent（general_purpose_task，research模式）
6. 子agent按instruction读取skill文件+输入文件 → 执行SOP → 落盘产出
7. 主agent检查产出 → 更新项目总控 → 衔接下一step

---

## seed 执行型step子agent派发模板

> 主agent按以下模板为seed的每个执行型step组装instruction，派发子agent。每个step一个子agent，子agent执行完返回后主agent检查产出再派发下一个。

### 通用instruction结构

每个step的instruction包含以下部分：

```
## 任务
执行 pop-qidian-seed 的 stepX-{name}（{step名称}），产出 {产出文件路径}。

## 执行方式
1. 读取 skill 文件获取完整SOP：
   - skills/pop-qidian-seed/SKILL.md（骨架+红线）
   - skills/pop-qidian-seed/steps/stepX-{name}.md（详细操作）
2. 按SOP执行，消费输入文件，产出落盘

## 红线（必须遵守）
{主agent从SKILL.md提取的3-5条红线}

## 操作要点摘要
{主agent从step文件提炼的关键操作，50-100行}

## 项目上下文
{主agent从项目文件提炼的上下文摘要}

## 输入文件路径
- {文件1路径}: {用途}
- {文件2路径}: {用途}

## 产出要求
- 落盘路径: {路径}
- 完成后报告: {报告内容}
```

### step3 骨架展开

**派发时机**：Step 0交互决策（S0-S5）完成，立项决策表落盘后

**主agent准备**：
1. 读取 `skills/pop-qidian-seed/SKILL.md` → 提取红线
2. 读取 `skills/pop-qidian-seed/steps/step3-skeleton.md` → 提炼操作要点
3. 读取 `设计/立项决策表.md` → 提炼S1世界+S2力量体系决策摘要

**instruction要点**：
- 任务：消费立项决策表S1+S2决策，展开为力量体系.md（四层结构）+动力引擎.md（六组成）+骨架自洽检查
- 红线：骨架先行/动力引擎世界级（众生攀登分层+掉落机制）/金手指不喧宾夺主/决策表是硬输入（S2已定方向不可推翻，如发现缺陷回Step 0重走S2）
- 输入文件：`设计/立项决策表.md` + `素材/用户意图.md` + `素材/decon-lite-{书名}.md`（如有）+ `素材/市场校准.md`
- 产出：`设计/力量体系.md` + `设计/动力引擎.md`
- 完成后报告：力量体系子境界数、动力引擎范式、骨架自洽检查结果

### step4 创意发散

**特殊**：step4产出候选PK，需要用户确认后才能进step5

**派发时机**：step3骨架展开完成，力量体系.md+动力引擎.md落盘后

**主agent准备**：
1. 读取 `skills/pop-qidian-seed/steps/step4-diverge.md` → 提炼操作要点
2. 读取 `设计/力量体系.md` + `设计/动力引擎.md` → 提炼骨架摘要

**instruction要点**：
- 任务：在骨架框架内双轨发散（王道轨5个+猎奇轨5个），三眼法判断，PK推荐1个
- 红线：骨架先行（创意必须在力量体系+动力引擎框架内，不能推翻坐标系）
- 输入文件：`设计/力量体系.md` + `设计/动力引擎.md` + `素材/市场校准.md` + `素材/用户意图.md`
- 产出：`设计/创意候选PK.md`（候选清单+三眼法判断+推荐）
- 完成后报告：王道轨5个方向+猎奇轨5个方向+推荐方向

**用户确认环节**：子agent产出候选PK后 → 主agent读取 `设计/创意候选PK.md` → 呈现给用户选择 → 用户选择后追加到 `设计/立项决策表.md`

### step5 故事纲领

**派发时机**：step4创意发散完成且用户已确认创意方向后

**主agent准备**：
1. 读取 `skills/pop-qidian-seed/steps/step5-story-brief.md` → 提炼操作要点
2. 读取 `设计/立项决策表.md` → 提炼S1+S3决策摘要+用户确认的创意选择

**instruction要点**：
- 任务：消费S1世界+S3主角+用户确认的创意方向，产出故事纲领（三核心+营销层）+创意.md
- 输入文件：`设计/立项决策表.md` + `设计/力量体系.md` + `设计/动力引擎.md` + `设计/创意候选PK.md`
- 产出：`设计/创意.md`
- 完成后报告：三核心摘要+最大钩子

### step6 黄金首章

**派发时机**：step5故事纲领完成，创意.md落盘后

**主agent准备**：
1. 读取 `skills/pop-qidian-seed/steps/step6-first-chapter.md` → 提炼操作要点
2. 读取 `设计/创意.md` → 提炼故事纲领摘要
3. 读取 `素材/文风锚定.md`（如有） → 确认DNA笔触可用

**instruction要点**：
- 任务：DNA笔触写黄金首章（2000-2500字），体现坐标系展示+金手指激活
- 输入文件：`设计/创意.md` + `设计/力量体系.md` + `设计/动力引擎.md` + `素材/文风锚定.md`（如有）
- 产出：`正文/ch001.txt`
- 完成后报告：字数+章型+金手指激活方式

### step7 主角展开

**派发时机**：step6黄金首章完成，ch001.txt落盘后

**主agent准备**：
1. 读取 `skills/pop-qidian-seed/steps/step7-protagonist.md` → 提炼操作要点
2. 读取 `设计/立项决策表.md` → 提炼S3决策摘要
3. 读取 `设计/力量体系.md` + `设计/动力引擎.md` → 提炼骨架摘要

**instruction要点**：
- 任务：消费S3决策+骨架+ch001，展开为主角设计.md（2a主角展开+2b金手指展开+2c爽感矛盾展开）
- 红线：决策表是硬输入（S3已定方向不可推翻，如发现缺陷回Step 0重走S3）
- 输入文件：`设计/立项决策表.md` + `设计/力量体系.md` + `设计/动力引擎.md` + `设计/创意.md` + `正文/ch001.txt`
- 产出：`设计/主角设计.md`
- 完成后报告：主角三定位+金手指限制代价+爽感矛盾公式

### seed 执行型step串联流程

```
Step 0交互决策完成 → 立项决策表落盘
  ↓
主agent派发 step3 子agent（骨架展开）
  ↓ 子agent产出 力量体系.md + 动力引擎.md
主agent检查产出 → 更新项目总控
  ↓
主agent派发 step4 子agent（创意发散）
  ↓ 子agent产出 创意候选PK.md
主agent读取候选PK → 呈现给用户 → 用户确认创意方向
  ↓
主agent派发 step5 子agent（故事纲领）
  ↓ 子agent产出 创意.md
主agent检查产出 → 更新项目总控
  ↓
主agent派发 step6 子agent（黄金首章）
  ↓ 子agent产出 ch001.txt
主agent检查产出 → 更新项目总控
  ↓
主agent派发 step7 子agent（主角展开）
  ↓ 子agent产出 主角设计.md
主agent检查产出 → 更新项目总控 → Phase 2完成 → 进入Phase 3
```

---

## Phase 3/3.5/4 主agent执行指南（待改造为子agent派发模式）

> 主agent直接加载对应skill执行生成任务。执行前必须读取skill的SKILL.md获取骨架，再按Step加载step文件。

### Phase 3 world执行指南

**执行步骤**：
1. 读取 `skills/pop-qidian-world/` 下的 SKILL.md 和 steps/ 下所有step文件（step0-decision/step1-flesh/step2-fullbook/step3-output）了解完整SOP
2. 消费输入文件：设计/力量体系.md + 设计/动力引擎.md + 设计/主角设计.md + 设计/世界决策表.md
3. 骨架消费验证门禁：验证力量体系.md+动力引擎.md4项完整性（力量体系四层/动力引擎六组成/众生攀登方式分层/金手指不喧宾夺主），任何一项不通过=报错中止
4. 按SOP执行：Step 1生长血肉（地图空间化→势力具名化→危机引擎化→敌人生态化+矛盾轴化）→Step 2全书展开→Step 3落盘10个最小闭环文件（设计/全书设定/目录）

关键红线（必须遵守）：
- world只展开骨架不发明骨架——力量体系/动力引擎/金手指只放引用指针（见力量体系.md+动力引擎.md/见主角设计.md），不重复落盘
- 地图必须有空间叙事价值（不是地名列表，每区域必须有空间法则+主角核心行为+信息差来源）
- 势力必须从引擎生长且4层全具名（有资源/没资源/爬到顶/掉下来，每层至少2个具名势力+领袖/代表）
- 危机是引擎阻力非随机威胁（必须对应动力引擎组成）
- 敌人是攀登方式代表非脸谱反派（弱点必须是攀登方式的结构性弱点）
- 各卷切片.md提供按卷导航（全书展开表覆盖3-8卷），下游按需读取对应设定文件

产出路径: 设计/全书设定/（10个最小闭环文件）
完成后报告：地图区域数、势力数、敌人阶梯层数、矛盾轴数。

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
   - `设计/创意.md`（故事调性）
4. 按step5-synthesize.md SOP执行：世界画风提取→笔触层校验重构（三问每个维度）→三层综合产出
5. 产出覆盖 `素材/文风锚定.md`（v2·综合产出，替换v1）

**无参考书模式**：如果用户在Phase 0选择跳过拆书（文风锚定.md不存在），Stage 2从零构建——仅世界画风层+用户需求层，跳过笔触层校验。

**完成后报告**：校验结果汇总（保留N项/修改N项/删除N项）+ 画风层数量 + 用户需求覆盖情况
**完成后更新项目总控.html**：deck_3(笔触DNA)标记为"v2-综合产出"

### Phase 3.5 character执行指南

**执行步骤**：
1. 读取 `skills/pop-qidian-character/` 下的 SKILL.md 和 steps/ 下所有step文件了解完整SOP
2. 消费输入文件：设计/力量体系.md + 设计/动力引擎.md + 设计/主角设计.md + 设计/全书设定/各卷切片.md（按需加载势力人物.md/危机敌人矛盾.md等） + 设计/角色库/角色库决策表.md
3. 按SOP执行：角色卡生成（主角已有→配角/反派/盟友/中立角色）

关键红线（必须遵守）：
- 角色必须从世界矛盾中生长（欲望来自世界，阻碍来自危机，选择来自世界规则）
- 每个角色必须有攀登方式归属（对应骨架众生攀登方式分层4类）
- 配角必须有独立性格+与主角的关系张力（不是工具人）
- 反派必须有自洽动机（动机=其攀登方式的必然冲突）
- 角色库是write的唯一角色源，正文不得引入角色库外的具名角色

产出路径: 设计/角色库/角色库.md
完成后报告：角色总数、各类型数量（主角/配角/反派/盟友/中立）。

### Phase 4 plot执行指南

**执行步骤**：
1. 读取 `skills/pop-qidian-plot/` 下的 SKILL.md 和 steps/ 下所有step文件了解完整SOP
2. 消费输入文件：设计/力量体系.md + 设计/动力引擎.md + 设计/主角设计.md + 设计/全书设定/各卷切片.md（导航→按需加载物理规则.md/战斗系统.md/地理建筑.md/势力人物.md/危机敌人矛盾.md等） + 设计/角色库/角色库.md + 设计/第一卷剧情/卷纲决策表.md
3. 按SOP执行：卷纲生成（四层结构+起承转合+精彩度五问自检）→章锚点表生成（4硬锚点+3软指导）

关键红线（必须遵守）：
- 卷纲必须包含四层结构（全书进度坐标+涌现设定累计+角色状态总表+剧情线进度+读者已知信息池+待回收伏笔总表）
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

1. 调pop-qidian-review v3.4.0，产出`审核/review-chXXX.md`（四维审核+骨架维度检查）
2. review Step 4沉淀产出：`current-state.md`更新（项目根） + `审核/小说快照.md`更新（全书累计视图——涌现设定/角色状态总表/剧情线进度/读者已知信息池/待回收伏笔总表） + `审核/review-沉淀.md`追加（审稿判断+规则沉淀，append-only）
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
- current-state.md必须包含DNA执行包（若素材/文风锚定.md存在）和source:skill-reconstruct标记
- 小说快照.md必须包含全书累计视图（涌现设定/角色状态总表/剧情线进度/读者已知信息池/待回收伏笔总表）
- review-沉淀.md append一段reconstruct汇总判断，不删改历史

产出路径:
- 审核/chNNN-审核报告.md（每个采样章节一份）
- current-state.md（项目根，含DNA执行包+source标记）
- 审核/小说快照.md（replace模式）
- 审核/review-沉淀.md（append）
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
2. 加载输入文件：设计/主角设计.md + 素材/文风锚定.md + 设计/力量体系.md + 设计/动力引擎.md + 设计/角色库/角色库.md + 设计/第一卷剧情/章锚点表.md + 设计/第一卷剧情/卷纲.md
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
