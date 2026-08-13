# CHANGELOG

## v3.10.0 | 2026-08-13

### DNA三态协议缺失态改为内置兜底文风

**核心改动**：用户项目未指定文风DNA（`素材/文风锚定.md` 不存在）时，write 不再"提示用户部署、不内置默认风格"，而是**必须从内置兜底文风DNA里选一个**，禁止跳过DNA直接写作。

**改动**：
- **新增 `references/文风兜底/`（5文件）**：深渊主宰（西幻）/夜无疆（玄幻修仙）/诡秘之主（西幻诡秘流）/捞尸人（民俗恐怖）/东京医途（都市），从 `popwave知识库/备选/文风库` 复制
- **step-1-consume.md**：DNA源文件扩展为 `素材/文风锚定.md`（项目指定）+ `references/文风兜底/`（内置兜底）；缺失态触发条件+读取规则+写作包DNA约束/文风DNA执行+execution.mode判定+门禁全部更新为"缺失态必须选兜底"
- **SKILL.md**：Step 2.5 + 红线5 + 速查表 + 知识地图（文风兜底=🔴写崩级）更新
- **skill.json**：version 3.9.0→3.10.0

---

## v3.9.0 | 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v3.9.0
- **CHANGELOG.md**：新增本条版本记录

---

## v3.8.0 (2026-08-12)

### 剧情记录双文件收束：write 回溯锚改为 白描卡 + 剧情累计卡

**背景**：老板定调——剧情记录只保留「白描卡 + 剧情累计卡」，废除 current-state.md / 小说快照.md / review-沉淀.md / 压缩归档/ 等冗余文档。write 作为回溯卡消费方，同步对齐。

**改动**：
- **SKILL.md**：输入与 Step 1 从 `current-state.md`（回溯锚）改为 `产出/白描卡/ch{NNN-1}.md`（上一章白描卡，回溯锚）+ `产出/剧情累计卡.md`（钩子台账/角色当前状态/读者已知池/禁止漂移）；红线2「禁止漂移」改指剧情累计卡
- **steps/step-1-consume.md**：§1.2 改为上一章白描卡（事件白描/关键数据/爽点·钩子/本章DNA执行包）+ 新增 §1.2b 剧情累计卡（钩子台账/角色状态/读者已知池/进度）；DNA触发源改为上一章白描卡执行包；写作包字段按双文件重构；execution.mode formal 判定与门禁改指双文件
- **steps/step-2-write.md**：钩子吞并/对话锚点/新增事实/移交 review 全部改指 剧情累计卡 + 白描卡
- **templates/chapter-record.tpl.md**：已读输入与下一步改指双文件
- **agents/openai.yaml**：short_description 更新
- **skill.json**：version 3.7.0→3.8.0，description 补双文件回溯锚

## v3.7.0 (2026-08-12)

### 新增知识地图 + 触发锚定

**背景**：write 仓库 550KB（51 文件），流派专属库 349KB 是互斥分支，agent 分不清哪些该读。补知识地图把触发式读取落明面。

**改动**：
- **SKILL.md**：新增「🗺️ 知识地图」区块——references 分级（章型定义/爽点引擎/爽点链条矩阵/爽文剧情设计SOP🔴写崩级；战斗规划/格局/位阶/微观技法/通用/情境/流派专属/番茄读者心理🟡提品级）；流派专属库标注"只读当前流派一档文件，不整包加载"
- **steps/step-2-write.md**：新增「0. 加载 references（Step 4，写前必做）」触发锚定段——写崩级4文件绑定到 step 内，已读输入字段必须如实列出加载文件
- **skill.json**：version 3.6.0→3.7.0，description 补知识地图

## v3.6.0 (2026-08-11)

### current-state 白描化：回溯与向前分离
- **current-state 从字段堆叠改为剧情白描驱动**：回溯"过去发生了什么"由 `## 上一章白描` 叙事流承担（3-5句，write 全量读），替代原人物状态/设定状态/可用燃料队列等字段
- **白描承接不了的三样单独留区**：信息差锚（读者/角色/实际，防信息错位穿帮）+ 钩子回收表（埋设章号/预期回收/强度）+ 禁止漂移（不可改事实硬清单）
- **向前推进移交章锚点表**：删除"下一章硬推进"字段，write 改读 `设计/第一卷剧情/章锚点表.md` 本章条目（4硬锚点+3软指导）作为向前唯一来源
- **输入从4类增至5类**：current-state（回溯）+ 章锚点表（向前）+ 最近正文 + 用户要求 + 文风DNA
- **废除"下一章硬推进"**：step-1 写作包、step-2 正文规则、SKILL.md 红线2 全部改为章锚点表硬锚点 + current-state 禁止漂移
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

## v3.5.0 (2026-07-26)

### 对齐pipeline标准架构（整体性改造）
- **目录路径对齐**：正文落盘路径从 `涌现/正文/{书名}-第{N}章-{标题}.txt` 改为 `正文/ch{NNN}.txt`，对齐pipeline 8目录标准
- **DNA三态协议修复**：删除 soul 依赖，`素材/文风锚定.md` 存在即可直接触发DNA加载（续写模式适用）；current-state.md 的 DNA执行包仍为正向模式优先源
- **current-state.md 路径对齐**：从 `审核/current-state.md` 改为 `current-state.md`（项目根），对齐pipeline标准
- **创作记录模板对齐**：soul约束 → DNA约束（来源素材/文风锚定.md），文风DNA约束 → 文风DNA执行包，路径对齐
- **SKILL.md Step 1 描述对齐**：从"读取种子文档+幕纲"改为对齐step-1-consume.md实际逻辑
- **配套修复-review**：step-2-commit.md 库文件名对齐pipeline标准路径（设定库.md→世界圣经.md/人物库.md→角色库.md/剧情线.md→卷纲.md/research-写作燃料.md→素材/写作燃料.md）；压缩归档路径从 `压缩归档/` 改为 `审核/压缩归档/`
- **配套修复-pipeline**：step0-import.md 的 current-state 反推模板补 DNA执行包字段
- skill.json displayName 从"涌现 Write"改为"起点 Write"
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

## v3.4.0 (2026-07-22)

### SKILL.md按skill-create规范重写
- SKILL.md从501行压缩至≤100行，补frontmatter description（含触发条件"当用户说…时启用"）
- 红线第一条改为读取协议（强弱加载规则），红线从12条+条件红线压缩至7条（只保留违反后断裂下游的），其余降级为质量约束
- 速查表从合格/不合格对照表改为文件目录引导（文件+读取时机+核心内容）
- SOP骨架每个Step压缩至1-2行，详细方法保留在step文件中
- 补强弱加载保障声明，版本历史只留最新一条
- skill.json version同步至3.4.0，description同步更新
- 业务方法论不变，step文件和references不动

## v3.3.0 (2026-07-22)

### write→review链路改硬约束
- step-2-write.md第6节"建议用户执行review"改为"**必须**执行review，未review不得写下一章"
- 明确review的三个职责：四维审核 + current-state更新 + 小说快照更新
- pipeline Phase 5→6路由增加红线7（write完成后必须进入review）

## v3.2.0 (2026-07-22)

### 合并流派专属write skill

- **合并dndlike和onepiece为流派技法包**——两个独立skill的独有内容（流派技法文件+专属红线+判断表）迁移到`references/流派专属/{流派名}/`目录
- 本skill成为**唯一write skill**——pipeline Phase 5永远调本skill，不再有流派选择分支
- 新增**流派技法包加载表**（Step 4）——用户声明流派后按需加载对应目录的技法文件
- 新增**流派专属红线**（条件触发）——D&D流5条+海贼王流3条，仅在加载对应技法包时生效
- 新增**流派技法包加载红线**（红线12）——声明流派后必须加载对应技法文件
- 迁移文件清单：dndlike 9个文件（含面板弹出判断表）+ onepiece 7个文件（含金手指触发判断表）
- 删除`pop-qidian-write-dndlike`和`pop-qidian-write-onepiece`两个skill目录

## v3.0.0 - 2026-07-21

### 版本升级：DNA三态协议 + 设定库精选注入 + 角色库消费 + 爽感坐标系跃迁
- 顶部版本说明改为 v3.0.0，列出四项核心变化。
- Step 1 加载项目上下文新增：`设计/主角设计.md`（爽感矛盾公式：坐标系门槛×天赋加速×代价约束）+ `设计/角色库/角色库.md`（角色唯一源）。
- Step 2 从"全文加载 seed+世界圣经"改造为 **设定库精选注入**：禁止全文注入，每章最多注入3个维度，每维度≤500字，总计≤1500字，角色库维度必选；按章型/章号选择注入维度（战斗章注入力量体系+敌人生态；日常章注入势力+地图）。
- 新增 Step 2.5 **DNA三态协议**（`素材/文风锚定.md`）：启用态按需加载通用维度+本章场景卡；缺失态提示用户部署，不内置默认风格；trial模式用户声明基础风格，不加载DNA文件。保留现有 dna/ 目录与流派技法。
- Step 5 写作·爽感层新增"坐标系跃迁锚定"硬约束：爽感爆发必须锚定坐标系位置跃迁，体现天赋加速vs代价约束的张力（爽感矛盾公式来自主角设计.md）。笔触层来源更新为DNA三态协议。修正微观层"16类技法"为17类。
- Step 6 验收新增三项检查：角色库一致性（本章出场角色是否在角色库中）/ DNA三态执行 / 爽感坐标系跃迁。
- 红线新增4条：设定库精选注入红线 / DNA三态协议红线 / 爽感坐标系跃迁红线 / 角色库唯一源红线；保留v2.0.1现有7条，共11条。
- 验收表新增4行：设定库精选注入 / DNA三态执行 / 角色库一致性 / 爽感坐标系跃迁。
- 新增版本块（SKILL.md末尾），版本三处一致（SKILL.md + skill.json + CHANGELOG.md）。
- 保留v2.0.1存量资产：6种章型骨架 / 17类微观技法（通用6+情境6+流派5）/ 五层指导 / dna/目录与流派技法目录 / steps目录原文件未改。

## v2.0.0 - 2026-07-14

### 版本升级：番茄 prose-render 覆盖
- 用番茄小说创作skill群的 prose-render 完整覆盖替换 pop-qidian-write 的 SKILL.md。
- 新增 frontmatter（name: pop-qidian-write）。
- 新增 execution.mode（formal/draft/trial 三档，引用 PRD §4.5）。
- Step 1 适配：将"读取施工卡"改为"读取 current-state.md（含下一章硬推进+人物状态+燃料队列+伏笔债务）+ dna/ 目录下的笔触DNA文件"。
- 新增正文落盘规则：正文落盘到 `涌现/正文/{书名}-第{N}章-{标题}.txt`，对话中只回摘要+钩子+创作记录。
- 保留番茄 prose-render 全部内容：6章型骨架/17微观技法/五层指导/章意图思考/微观技法选择/验收表等。
- references/ 目录从番茄 prose-render 源完整复制（含情境技法/流派专属/通用技法子目录 + 8个根文件）。
- dna/ 目录从番茄 prose-render 源完整复制（4个笔触DNA文件）。
- 保留现有 templates/chapter-record.tpl.md 和 steps/ 目录。

## v3.7.0 - 2026-07-09

### 调整：章内文风DNA消费
- `文风DNA执行` 从 scene 卡、层1/2/3约束改为 DNA源、模式、章型、笔触目标、章内套路、可见反馈和禁止误用。
- 正文门禁改为检查章内笔触和单章套路是否参与生成，强嫁接只迁移章内套路和笔触手感。
- 创作记录模板同步为章内DNA字段。

## v3.6.0 - 2026-07-08

### 新增：文风DNA三层消费
- 当 soul/current-state/用户要求启用 DNA 时，write 必须消费 `本章DNA执行包` 和对应 DNA 源片段。
- 本章写作包新增 `文风DNA执行` 字段，要求列出 DNA源、模式、scene 卡序列、层1/2/3约束和禁止误用。
- 正文规则新增 DNA 落地门禁：不能只替换形容词，必须影响场景组织和商业反馈。
- 创作记录模板新增"执行的文风DNA约束"。

## v3.5.0 - 2026-07-06

### 重构：对齐 PRD 契约层
- 四层架构对齐：SKILL.md 引用 PRD §4 作为单一真相源，删除自有 execution.mode 三档表、自有骨架定义、自有 owner 表。
- 正文落盘路径明确为 `涌现/正文/{书名}-第{N}章-{标题}.txt`（修复问题 7）。
- "新增事实待 review" 措辞修正：write 只在对话创作记录里列清单（声明），不落盘到任何库文件；由 review 读取后落库（修复问题 10）。
- 新增 steps/ 目录：step-1-consume.md（消费 4 类输入 + 末尾门禁）、step-2-write.md（写正文 + 落盘 + 创作记录）。
- 新增 templates/chapter-record.tpl.md（统一回复模板，对齐 PRD §4.7）。
- skill.json 补全 displayName / entry / activation / permissions 字段。
- 版本从 2.3.0 升至 3.5.0，版本三处一致（SKILL.md + skill.json + CHANGELOG.md）。

## v2.3.0

- 旧版单文件 SKILL.md，自有 execution.mode 三档表、自有骨架与 owner 定义。
