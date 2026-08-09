# CHANGELOG

## v3.10.0 | 2026-08-09

### 新增首次对话引导（onboarding）

**背景**：老板定调——每个 C 端专家需要一份面向作者本人（非产品经理/AI 专家）的首次对话引导语，用"你能把小说写成什么"的场景快速建立认知，而非介绍内部架构。

**改动**：

- 新增 `references/onboarding-guide.md`：C 端口吻引导语（一句话说清 + 你有这些玩法 + 你不用担心 + 就这样开始），覆盖立项/世界观/逐章成文/自查把关四类玩法
- `SKILL.md`：新增「🚪 首次对话引导」区块——用户首次触发时直接输出引导语全文，再进 Step 0 意图深问
- 版本至 v3.10.0

## v3.9.0 | 2026-07-29

### 文件全景图对齐——修复残留引用+补全产出列+HTML模板更新

**根因**：v3.8.0完成了world产出从单文件到10个最小闭环文件的重构，但pipeline自身文件中仍残留5处`设计/骨架.md`引用（实际应为`设计/力量体系.md`+`设计/动力引擎.md`），Phase路由表产出列缺失7个中间/最终文件，HTML模板文件夹树和badge名称未同步更新，初始化缺少`产出/`目录（plot事实快照落盘需要）。

**改动**：

**骨架.md残留修复（5处）**：
- step2.md Phase 3 world执行指南：`设计/骨架.md`→`设计/力量体系.md`+`设计/动力引擎.md`
- step2.md Phase 3.5 character执行指南：同上
- step2.md Phase 4 plot执行指南：同上
- step2.md Phase 5 write执行指南：同上
- step2.md Phase 3红线引用：`见骨架.md`→`见力量体系.md+动力引擎.md`

**Phase路由表产出列补全（7个文件）**：
- Phase 0-Stage2：`素材/（调研+文风锚定+decon-lite）`→`素材/（赛道调研.md+文风锚定.md v1+decon-lite-{书名}.md+downloads/{书名}.txt）`+`设计/立项决策表.md（S0-S3部分）`
- Phase 1：新增`创意候选PK.md`
- Phase 3.5：新增`角色库决策表.md`
- Phase 4：新增`卷纲决策表.md`+`产出/正文/事实快照-幕NNN.md`
- Phase 6：新增`review-沉淀.md`+`current-state.md（项目根）`

**HTML模板更新**：
- badge名称：`flesh_0(地图)`→`flesh_0(全书设定)`、`flesh_1(势力)`→`flesh_1(DNA综合)`、`flesh_3(剧情白描)`→`flesh_3(卷纲)`
- write_skill字段标签：`当前write`→`流派`，值简化为`pop-qidian-write（流派: {流派名}）`
- 文件夹树重写为完整文件全景图（含10个全书设定文件+决策表+事实快照+current-state.md+review-沉淀.md等全部文件）

**step2.md badge更新表**：
- `Phase 3 | flesh_0(地图)→✅, flesh_1(势力)→✅`→`Phase 3 | flesh_0(全书设定)→✅`+`Phase 3→3.5 | flesh_1(DNA综合)→✅`
- `Phase 4 | flesh_3(剧情白描)→✅`→`Phase 4 | flesh_3(卷纲)→✅`

**step2.md Phase 6产出**：补上`审核/review-沉淀.md`追加

**step0-import.md更新**：
- 0c缺口分析表：Phase 1新增立项决策表.md检查、Phase 3新增世界决策表.md检查、新增Phase 3→3.5行（文风锚定v2）、Phase 6新增current-state.md检查
- 0f-3设计文档补跑表：`骨架`→`力量体系+动力引擎`

**step1.md更新**：
- 初始化目录从8个增至10个：新增`产出/`+`产出/正文/`（plot事实快照落盘目录）
- 自检清单从11项增至13项
- 质量门从"8个目录"改为"10个目录"

- skill.json version 3.8.0→3.9.0
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

## v3.8.0 | 2026-07-29

### Phase 3产出更新为10个最小闭环文件（world v4.4.0同步）

**根因**：world v4.4.0将产出从单文件"世界圣经.md"重构为`设计/全书设定/`目录下10个最小闭环文件。pipeline作为路由总控需同步更新Phase路由表的产出列、Phase 3执行指南、Phase 3→3.5 DNA重构调度的输入文件、Phase 3.5 character和Phase 4 plot的消费引用。

**改动**：
- Phase路由表Phase 3产出从"设计/世界决策表.md+全书设定/世界圣经.md"更新为"设计/世界决策表.md+设计/全书设定/（10个最小闭环文件）"
- Phase路由表Phase 3版本从v4.3.0更新为v4.4.0
- Phase 3→3.5前置检查从"世界圣经就绪"更新为"全书设定文件就绪"
- Phase 3→3.5 DNA重构调度的世界画风源从单一"世界圣经.md"拆分为4个具体文件（战斗系统.md/物理规则.md/民风民俗.md/世界设计原则.md）
- Phase 3.5 character消费引用更新为"各卷切片.md（按需加载）"
- Phase 4 plot消费引用更新为"各卷切片.md（导航→按需加载）"
- 红线4混合执行模式中"世界圣经"更新为"世界设定"
- skill.json version 3.7.0→3.8.0
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

## v3.7.0 | 2026-07-28

### Phase 3→3.5新增DNA综合重构调度

**根因**：文风DNA从参考书纯提取（Stage 1，Phase 0）存在局限性——参考书的笔触可能和本书世界画风矛盾（如深渊主宰的弹窗式面板在生存记录感世界不自然），且用户需求（面板偏好/主角姿态/节奏偏好）无法在纯提取阶段注入。需要在世界圣经产出后，用世界画风+用户需求对笔触层进行校验重构。

**改动**：
- Phase路由表新增"3→3.5"行：pop-dna-style v1.4.0 Stage 2，世界圣经就绪后执行
- step2.md新增"Phase 3→3.5 DNA重构调度"执行指南
- 主agent在Phase 3完成后、进入Phase 3.5之前，加载pop-dna-style Stage 2执行
- Stage 2对Stage 1笔触层拥有写权限（可修改/删除/保留），每个修改/删除需世界画风的因果依据
- 文风锚定.md从单层（笔触层）升级为三层（笔触层+世界画风层+用户需求层）
- world版本号Phase路由表对齐：v4.1.0→v4.3.0

**关联skill改动**：
- pop-dna-style v1.4.0：新增Stage 2 + step5-synthesize.md + 红线❌6/❌7
- 涉及文件：pipeline SKILL.md + step2.md + skill.json + pop-dna-style SKILL.md + step5-synthesize.md + skill.json + CHANGELOG.md

## v3.6.0 | 2026-07-27

### seed 从主agent直接执行改为混合执行模式（方案3）

**根因**：主agent直接执行所有step会导致上下文信息衰减——越长越衰减，到后期step时指令权重下降，agent跳过红线、省略产出。这是模型注意力机制的物理限制，无法通过"强调红线"或"加门禁"解决。

**方案3·混合执行**：主agent做调度器（读skill→提炼红线+操作要点+项目上下文→组装instruction→派发子agent→检查产出→衔接下一step），子agent做执行器（拿到干净上下文+完整执行指南，专注生成）。不依赖harness层skillNames传参——主agent用Read工具自行读取skill文件。

**改动**：
- SKILL.md：
  - 红线#4从"主agent直接执行所有skill SOP"改为"混合执行模式"——交互型step主agent执行，执行型step主agent派发子agent执行
- step2.md：
  - "Phase 1-4执行模式"从"先交互→再生成（主agent直接执行）"改为"交互型step主agent执行 + 执行型step子agent派发"
  - 新增"seed 执行型step子agent派发模板"——为step3-7各设计instruction模板（通用结构+派发时机+主agent准备+instruction要点）
  - 新增"seed 执行型step串联流程"——展示step3→step4（用户确认）→step5→step6→step7的完整派发链路
  - Phase 3/3.5/4执行指南标注"待改造"（后续逐步改造）
- 涉及文件：SKILL.md + steps/step2.md

**seed step分类**：
- 交互型（主agent执行）：step1底牌摸底、step2交互决策
- 执行型（子agent执行）：step3骨架展开、step4创意发散（产出候选PK→主agent让用户确认）、step5故事纲领、step6黄金首章、step7主角展开

**后续计划**：world/character/plot/write/review 逐步改造为相同的混合执行模式

## v3.5.0 | 2026-07-27

### 全系列从子agent派发改为主agent直接执行

**根因**：`paopao_subagent_run` 工具不支持 `skills` 参数（host层限制），导致子agent无法加载skill定义，只能凭记忆"扮演"skill，产出质量不达标。同时子agent无法获取主会话上下文，world/character/plot等需要上下文的环节产出脱节。

**改动**：
- SKILL.md：
  - Phase路由表删除所有「**子agent**生成」标注，改为「主agent加载skill执行」
  - 红线#4从"子agent派发必须遵守host约束"改为"主agent直接执行所有skill SOP"
  - 速查表step2.md描述从"子agent派发模板"改为"主agent执行指南"
- step2.md：
  - Phase 0并发规则从"同时派发dna-style+decon-lite"改为"主agent依次执行（串行）"
  - Phase 1-4从"交互决策完成后必须派发子agent"改为"主agent直接执行生成"
  - 所有子agent派发模板（Phase 3/3.5/4/5/0/reconstruct）改为主agent执行指南
  - 删除host约束说明（不再需要paopao_subagent_run参数约束）
  - 执行指南保留原有红线和执行步骤实质内容，仅改变执行方式
- step0-import.md：
  - 0f调度从"派发子agent"改为"主agent加载skill执行"
  - 表格header从"派发模板"改为"执行指南"
  - 交叉引用从"reconstruct子agent"改为"reconstruct执行指南"
- 涉及文件：SKILL.md + steps/step2.md + steps/step0-import.md

**关联skill改动**：
- pop-qidian-seed SKILL.md：Phase 0描述从"触发pipeline子agent并发"改为"主agent依次执行拆书任务"
- pop-qidian-seed steps/step1-brief.md：底牌就绪后从"子agent并发"改为"主agent依次执行"，描述原则从"告诉子agent扮演哪个skill"改为"主agent读取对应skill的SKILL.md"
- pop-qidian-research steps/step-track-research.md：触发条件从"自动派发子agent"改为"主agent执行"

## v3.4.0 | 2026-07-26

### 导入模式重构：pipeline从搬运工升级为调度员

**根因**：step0-import.md自己做内容结构标准化+正文反推+设计文档补建，但pipeline作为路由总控无法达到各skill深度方法论保证的产出质量。各skill的SOP/格式/校验逻辑深度思考，pipeline自行转换只是形式对齐。

**改动**：
- step0-import.md重构：
  - 0b简化为"资产归位"（只做文件名/目录归位+来源标记，删除0b-2内容结构标准化）
  - 0f重写为"调度skill补跑"（替代原0b-2/0f的pipeline自做内容转换/反推）
  - 新增文件来源标记机制（user-original/pipeline-relocated/skill-generated/skill-reconstruct）
  - 新增补跑建议清单（输出给用户决定补跑策略）
  - 0f-2 review reconstruct：有正文缺状态文件时调度review批量回溯
  - 0f-3 设计文档补跑：缺设计文档时调度对应skill reconstruct
- step2.md新增Reconstruct子agent派发模板：
  - review reconstruct子agent（批量回溯审核）
  - skill reconstruct子agent（设计文档校验+补全，通用模板）
- SKILL.md路由表review版本v3.2.0→v3.4.0
- SKILL.md Step 0描述更新为"调度员"架构
- 配套改造review v3.4.0：新增step-reconstruct.md（批量回溯审核模式）
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

**架构边界**：pipeline只做资产清点+文件归位+调度skill，深度内容转换由对应skill的reconstruct模式完成

## v3.3.0 | 2026-07-24

### 补全Phase 3/3.5/4子agent派发模板

**根因**：run日志分析发现world/character/plot在主会话中直接执行，未派发子agent。导致：①skillNames为空，skill定义未加载 ②主agent凭记忆"扮演"skill，自评偏乐观无人拦截 ③产出质量不达标（地图区域少/势力不够/剧情平淡）

**改动**：
- step2.md新增Phase 3 world/Phase 3.5 character/Phase 4 plot三个子agent派发模板
  - 均使用 `purpose: "research"`（执行类，可写文件）
  - instruction自包含：remote-skills路径+SKILL.md+steps/读取指令+关键红线+产出路径+「执行任务不是检查任务」声明
  - 每个模板包含该Phase特有的红线摘要（world: 骨架消费验证/地图空间叙事/势力4层具名/危机引擎化/敌人攀登方式代表；character: 角色从世界矛盾生长/攀登方式归属/反派自洽动机；plot: 四层结构/起承转合/4硬锚点/精彩度五问/四地图叠加推演）
- step2.md Phase 1-4执行模式说明新增：交互决策完成后必须派发子agent执行生成（seed除外，因交互轮次多）
- SKILL.md路由表Phase 3/3.5/4标注「**子agent**生成」
- SKILL.md红线#4扩展：Phase 0/3/3.5/4/5的生成任务都必须派发子agent，禁止在主会话直接执行
- SKILL.md版本号3.2.0→3.3.0

**部署要求**：同步到 `C:\Users\AWMPRO\AppData\Roaming\popwave\remote-skills\pop-qidian-pipeline\3.3.0\`

## v3.2.0 | 2026-07-24

### 子agent派发host约束修正 + Phase 0产出真实性门禁

**根因**：run日志分析发现三个致命问题——
1. `paopao_subagent_run` 工具没有 `skills` 参数，step2.md模板里的 `skills: ["pop-qidian-research"]` 被host完全忽略
2. `purpose` 只支持 `verification/research/critique/implementation-check`，没有 `implementation`，agent回退到 `implementation-check`，导致子agent只产出检查报告不执行
3. 本地修改（v3.2.0）未部署到remote-skills缓存，agent加载的还是旧版3.1.0

**改动**：
- step2.md子agent派发模板全面重写：
  - 删除所有 `skills` 参数（host不支持）
  - `purpose: "implementation"` → `purpose: "research"`（host支持值）
  - instruction自包含：skill文件读取路径（remote-skills目录）+ 关键红线摘要 + 产出路径 + 「执行任务不是检查任务」声明
  - 新增Phase 5 write子agent模板（之前SKILL.md有但step2.md缺失）
- SKILL.md红线#14重写：从"必须用implementation模式"改为"必须遵守host约束"
- SKILL.md Phase 5指令模板引用step2.md（不再内联）
- SKILL.md版本标注更新3.1.0→3.2.0
- 新增Phase 0产出真实性门禁（decon-lite≥3处原文引用+文风锚定≥500字原文采样）
- 新增下载失败中断机制（下载失败→禁止派发拆书/DNA→等用户决策）

### 部署要求
- 必须同步到 `C:\Users\AWMPRO\AppData\Roaming\popwave\remote-skills\pop-qidian-pipeline\3.2.0\`
- 旧版3.1.0可保留但不再被加载（版本号自动选最新）

## v3.1.0 | 2026-07-24

### 新增导入/续写模式（Step 0）——标准化转换为核心
- **问题背景**：原pipeline只支持从零开始的写作流程，用户已有历史资料/设定/正文时无法接入
- **核心理念**：不是"检测+跳Phase"，而是"检测→标准化转换→补缺→路由"的完整初始化过程
- **新增 `steps/step0-import.md`**：6步执行链路：
  - 0a 资产扫描（LS列出所有已有文件）
  - 0b 资产标准化转换（0b-1文件名+目录归位 / 0b-2内容结构标准化——对照每个文件的标准模板结构重组）
  - 0c 缺口分析（逐Phase检查就绪状态）
  - 0d 落地Phase决策（9种场景决策表+用户确认）
  - 0e 状态文件重建（项目总控.html mode+phase+chapter+circle+badge）
  - 0f 补缺生成（0f-1正文反推 / 0f-2缺失设计文档补建 / 0f-3无法反推文档处理）
- **三种mode**：fresh（从零开始）/import（导入已有设定）/resume（续写已有正文）
- **标准化转换覆盖全部22个标准文件**：每个文件都有标准文件名映射表+标准内容结构定义+转换方式
- **step1.md增加前置检测**：LS扫描项目目录，检测到 正文/ 或 设计/ 已有文件→重定向到Step 0
- **项目总控.html模板新增mode字段**：`<!--STATE:mode -->fresh<!--/STATE:mode -->`
- **正文反推功能**：有正文但缺小说快照时，从正文提取角色/剧情/设定/伏笔→生成小说快照.md+current-state.md
- **降级模式**：缺卷纲/章锚点表时，用户可选择跳过plot直接续写，在current-state.md中手动指定下一章核心事件
- **新增红线第12条**：导入/续写模式不可跳过资产扫描
- **速查表新增step0-import.md条目**
- skill.json版本更新：3.0.0→3.1.0

## v3.0.0 | 2026-07-23

### seed v9.0.0引擎三要素重构（版本跳变说明）
- 版本从v1.x跳到v3.0.0，因seed引擎大重构导致pipeline同步升级
- 详细变更见seed CHANGELOG.md v9.0.0
- pipeline自身改动：Phase路由表更新seed版本，清理SKILL.md历史版本耦合

## v1.8.0 | 2026-07-22

### Phase 0-1并行设计 + seed故事先行
- **Phase 0-Stage2改为并行**：拆书子agent和seed Step 0交互同时启动，不再串行等待
- **seed故事先行**：S1故事创意对齐仅需用户意图.md，不依赖拆书，可立即开始；S2力量体系配套消费拆书结果
- Phase路由表更新：0-Stage2产出新增"设计/立项决策表.md（S1-S2部分）"
- seed版本更新：v8.4.0→v8.5.0（故事先行重构）

## v1.7.0 | 2026-07-22

### Phase 1-4改为"先交互→再生成"模式
- **Phase 1 seed新增Step 0交互式决策**——S1-S5（5轮，前4轮核心必答+S5可选）→产出`设计/立项决策表.md`→再执行骨架生成
- **Phase 3 world新增Step 0交互式决策**——W1-W2（2轮，W1核心必答+W2可选）→产出`设计/世界决策表.md`→再执行世界圣经生成
- **Phase 3.5 character新增Step 0交互式决策**——C1-C2（2轮，C1核心必答+C2可选）→产出`设计/角色库/角色库决策表.md`→再执行角色库生成
- **Phase 4 plot新增Step 0交互式决策**——R1-R5（5轮，前3轮核心必答+后2轮可选）→产出`设计/第一卷剧情/卷纲决策表.md`→再执行Step 1-3自动生成
- **Phase路由表更新**——Phase 1/3/3.5/4的调用Skill列标注"Step 0交互→"，产出列新增对应决策表文件
- **新增"Phase 1-4执行模式：先交互→再生成"章节**——含Step 0交互轮次/核心必答可选/决策表产出/完成后执行四列对照表
- **新增项目空间结构树**——恢复结构树（v1.6.0曾移除），含4个决策表文件路径标注
- **红线新增第8条**——"Phase 1-4的Step 0交互决策不可跳过——核心轮必须用户确认后才进入自动生成"
- **skill.json版本更新**——1.6.0→1.7.0，description补充"Phase 1-4先交互式决策再自动生成"
- **不改动Phase 0和Phase 5-6的任何内容**

## v1.6.0 | 2026-07-22

### 按skill-create规范重写SKILL.md
- frontmatter补description含触发条件（"当用户说'管线''pipeline''继续写''下一步'时启用"）
- SKILL.md从281行压缩到84行
- 红线从11条压缩到7条（第一条改读取协议，合并"agent每次对话第一件事读html"入读取协议）
- 速查表从"启动时判断"+"Skill调度表"双对照表改为文件目录引导（5行）
- 补强弱加载声明（SKILL.md必读/steps强加载/项目总控.html必读/Phase路由表弱加载）
- 版本只留最新一条（历史版本移至CHANGELOG.md）
- 项目空间结构树移除（step1.md已有目录创建逻辑）
- Phase路由从详细描述压缩为路由表+3条关键约束注释

## v1.5.0 | 2026-07-22

### plot v4.1.0调优
- Phase 4产出改名：剧情白描.md→卷纲.md
- Phase 4产出更新：章锚点表简化为4硬锚点+3软指导
- Phase 4调度表版本更新：plot v4.0.0→v4.1.0
- Phase 5前置检查更新：增加章锚点表.md

## v1.4.0 | 2026-07-22

### review小说快照 + write→review硬约束
- **review新增Step 4c小说快照**——每章review后更新`审核/小说快照.md`（全书累计视图：涌现设定/角色状态总表/剧情线进度/读者已知信息池/待回收伏笔总表）
- **write→review链路改硬约束**——Phase 5完成后必须进入Phase 6 review，不得连续写两章不review（新增红线7）
- **Phase 6产出新增小说快照.md**——调度表和项目空间结构更新
- **review skill调度表版本更新**——v3.0.0→v3.1.0

## v1.3.0 | 2026-07-22

### 合并流派write skill
- Phase 5路由简化为**永远调pop-qidian-write**——不再有dndlike/onepiece分支
- 用户声明流派后，将流派名称传给子agent，子agent在write Step 4自动加载`references/流派专属/{流派名}/`技法包
- Skill调度表从3行write合并为1行
- 删除`pop-qidian-write-dndlike`和`pop-qidian-write-onepiece`两个skill

## v1.2.0 | 2026-07-22

### 项目总控.html替代project-state.md
- **删除project-state.md**——项目总控.html成为唯一状态文件（agent读+人看）
- **agent直接用SearchReplace更新html**——所有可变字段用`<!--STATE:xxx -->`注释标记包裹，phase circle用CSS class控制（pending/done/current）
- **不用脚本**——删除scripts/generate-state-html.py依赖，agent直接操作html标记字段
- **新增模板文件** `templates/项目总控.html`——暗色主题，含项目简介/Phase进度条/下一步指引/就绪卡片/产出表/文件夹树

### 初始化修复
- **强制创建全部8个目录**（含审核/和知识沉淀/）——之前审核/目录初始化时不创建，导致Phase 6时才发现缺失
- **初始化自检**——创建完后必须用LS确认11项全部存在，任何缺失=初始化失败
- step1.md和step2.md完全重写

### write DNA方案对齐番茄
- write/write-dndlike/write-onepiece删除skill内部dna/目录
- DNA 100%从项目空间`素材/文风锚定.md`读取（pop-dna-style在Phase 0提取落盘）
- write成为通用skill，流派技法（章型节拍/战斗模式）保留在skill内部

## v1.1.0 | 2026-07-21

### 全链路联调
- 版本快照表更新，对齐所有已升级skill新版本号：
  - pop-qidian-research: v3.5.1 → v4.0.0（新增decon-lite 9表）
  - pop-qidian-seed: v7.0.0 → v8.1.0（骨架层+主角层）
  - pop-qidian-world: v1.0.0 → v2.0.0（收缩消费骨架）
  - pop-qidian-plot: v3.0.0 → v4.0.0（四层结构+困难三层面）
  - pop-qidian-write: v2.0.1 → v3.0.0（DNA三态+精选注入+角色库消费）
  - pop-qidian-review: v2.0.1 → v3.0.0（四维审核+骨架维度检查）
  - pop-qidian-character: 新建 v1.0.0
  - pop-qidian-write-dndlike: v1.0.1（保持不变，本次只微调）
  - pop-qidian-write-onepiece: v1.0.1（保持不变，本次只微调）

### Phase路由微调
- Phase路由各阶段标注下游skill版本号（research v4.0.0 / seed v8.1.0 / world v2.0.0 / plot v4.0.0 / write v3.0.0 / review v3.0.0 / character v1.0.0）
- Phase 0 Stage 2 子agent指令标注 research v4.0.0
- Phase 4 描述更新为"四层结构+困难三层面"（原2c分幕设计）
- Phase 5 流派write选择标注版本号（write v3.0.0 / write-dndlike v1.0.1 / write-onepiece v1.0.1）

### Skill调度表更新
- 新增"版本"列，标注所有skill版本号

### Bug修复
- 修正顶部版本说明"Phase 0→5路由"为"Phase 0→6路由"（v1.0.0遗漏Phase 6）

### 版本对齐
- SKILL.md / skill.json / CHANGELOG.md 版本三处一致

## v1.0.0 | 2026-07-21

### 新建
- 新建skill。起点管线总控，补齐起点skill群组缺失的pipeline总控。
- Phase 0→6路由：Phase 0素材准备 → Phase 1 seed骨架层 → Phase 2 seed主角层 → Phase 3 world → Phase 3.5 character → Phase 4 plot → Phase 5 write → Phase 6 review
- project-state.md状态追踪：三层就绪状态（骨架/主角/血肉）+ 底牌就绪 + 创意摘要 + 最近产出
- 三层骨架依赖链硬约束：骨架没就绪不进主角层，主角没就绪不进血肉层，血肉没就绪不写作
- 流派write选择路由：dndlike / onepiece / 兜底模板
- 基于番茄pipeline v3.2.0适配起点架构（三层骨架前移到seed + 流派write分离 + character在plot之前）
