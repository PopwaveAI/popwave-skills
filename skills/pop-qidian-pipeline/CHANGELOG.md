# CHANGELOG

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
