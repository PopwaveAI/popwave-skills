# CHANGELOG

## v3.11.0 | 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v3.11.0
- **CHANGELOG.md**：新增本条版本记录

---

## v3.10.0 (2026-08-12)

### 剧情记录双文件收束：导入/反推/判定改双文件，废 current-state

**背景**：老板定调——剧情记录只保留「白描卡（存发生）+ 剧情累计卡（存状态）」。番茄系 pipeline 的导入/续写判定与 0f-1 正文反推原引用 current-state，随 review v4.9.0 废 current-state 后，需同步改为双文件（流水账=白描卡 + 剧情累计卡）。

**改动**：
- **step0-import.md**：
  - 资产识别表：`*current-state*/入口包` → `*状态*/累计卡/钩子台账` → `审核/剧情累计卡.md`（白描卡+剧情累计卡两行并存）
  - 内容结构标准化表：`current-state.md` 行 → `审核/剧情累计卡.md`（全书累计视图，replace）
  - 缺口分析 Phase 5：`流水账存在` → `双文件都有=✅`
  - 落地Phase决策：`正文+流水账有` → `正文+双文件有`；`正文+双文件缺`→先反推补建
  - 0f-1 正文反推：触发条件改双文件任一缺失；b) 从"生成current-state"改为"生成剧情累计卡"（全书进度/未回收钩子台账含信息差+预期回收/角色当前状态表/读者已知信息池/禁止漂移/DNA执行包）
  - 0f-3 降级模式引用：current-state → 剧情累计卡
- **SKILL.md**：版本 v3.9.0→v3.10.0；Phase 5 产出补双文件；版本描述更新
- **skill.json**：version 3.9.0→3.10.0，description 补双文件收束

**保留不动**：Phase 0→5 调度骨架/project-state 可视化/路由逻辑——只改剧情记录依赖

---

## v3.9.0 (2026-08-11)

### 知识地图试点

**背景**：reference 是"可选读物"，agent 默认跳过。pipeline 作为调度器，补统一知识地图区块。

**改动**：
- **SKILL.md**：速查表补 `references/onboarding-guide.md` 条目；新增「🗺️ 知识地图」区块（onboarding-guide🔴强触发）；版本描述更新 v3.8.0→v3.9.0
- **skill.json**：version 3.8.0→3.9.0，description 补知识地图

---

## v3.8.0 (2026-08-11)

### 小说快照 → 剧情白描流水账

**背景**：review v4.8.0 将小说快照（三档压缩）改为每章剧情白描流水账（append-only），write v8.6.0 增加流水账长线锚。pipeline 的导入/续写判定与 0f-1 正文反推需同步，避免引用已废弃的 `审核/小说快照.md`。

**改动**：
- **step0-import.md**：小说快照引用全部改为剧情白描流水账
  - 资产识别表/内容结构标准化表/缺口分析表：`小说快照.md` → `剧情白描流水账.md`
  - 落地Phase决策：`正文+流水账有`续写 / `正文有流水账无`先反推补建
  - 0f-1 正文反推：从生成"全书累计快照"改为按章追加"每章剧情白描流水账"（白描+信息差+涌现/角色状态+埋设/回收钩子）
  - current-state 生成：人物状态/伏笔债务改为从流水账提取
- **SKILL.md**：版本 v3.7.0→v3.8.0
- **skill.json**：version 3.7.0→3.8.0，description更新

**保留不动**：Phase 0→5 调度骨架/project-state 可视化/路由逻辑——只改快照依赖

---

## v3.7.0 (2026-08-10)

### skill.json 补可调度 Skill 清单 + SKILL.md 新增素材表

**背景**：老板定调——pipeline 是整个专家的入口和调度器，机器层面（skill.json）应有一份"我能调哪些 skill"的统一清单，后台配置系统才能读取。此前番茄 skill.json 无 `skills` 字段，清单只散落在 SKILL.md 的 Phase 路由表。

**改动**：

- `skill.json`：新增 `skills` 完整可调度清单（seed/world/plot/character/write/review/dna-style/research/download-webnovel）
- `SKILL.md`：新增「📦 可调度 Skill 清单（素材表）」区块——每个 skill 的定位 + 何时调用，标注复用项
- 版本至 v3.7.0

## v3.6.0 (2026-08-09)

### 新增首次对话引导（onboarding）

**背景**：老板定调——每个 C 端专家需要一份面向作者本人（非产品经理/AI 专家）的首次对话引导语，用"你能把小说写成什么"的场景快速建立认知，而非介绍内部架构。

**改动**：

- 新增 `references/onboarding-guide.md`：C 端口吻引导语（一句话说清 + 你有这些玩法 + 你不用担心 + 就这样开始），覆盖立项/世界观/逐章成文/自查把关四类玩法
- `SKILL.md`：新增「🚪 首次对话引导」区块——用户首次触发时直接输出引导语全文，再进 Step 0 意图深问
- 版本至 v3.6.0

## v3.5.0 (2026-08-05)

### 全链路质量升级（world/plot/write/character/review）

**背景**：老板批准番茄写作专家从起点写作专家方法论中汲取质量增益经验。保持番茄"脑洞驱动+章纲流"的核心方法论不变，只做质量层面的升级。

**升级总览**：

| Skill | 版本变化 | 升级内容 |
|:--|:--|:--|
| pop-fanqie-world | v1.x→v1.7.0 | 5项：战斗可写性约束+维度好坏标准+分段落盘检查点+势力攀登标注+轻量原则推导 |
| pop-fanqie-plot | v3.x→v3.7.0 | 6项：卷纲精彩度五问+主角主动3项自检+每幕2-4条故事弧线+多视角叙事+四段式模板+本幕结构要素表 |
| pop-fanqie-write | v8.x→v8.5.0 | 3项：章型4→6种+微观技法3类16种索引+三态协议对齐细化 |
| pop-fanqie-character | v1.1→v1.2.0 | 3项：攀登方式类型标注+角色三问自检+关系网分层 |
| pop-fanqie-review | v4.5→v4.6.0 | 4项：6章型7节拍审核+战斗可写性审核+主角主动性审核+多视角覆盖审核 |

**pipeline自身改动**：路由逻辑不变，版本号同步升级记录
- skill.json version 3.4.0→3.5.0
- SKILL.md版本描述更新

---

## v3.4.0 (2026-07-24)

### 新增导入/续写模式（Step 0）——标准化转换为核心
- **问题背景**：原pipeline只支持从零开始的写作流程，用户已有历史资料/设定/正文时无法接入
- **核心理念**：不是"检测+跳Phase"，而是"检测→标准化转换→补缺→路由"的完整初始化过程
- **新增 `steps/step0-import.md`**：6步执行链路：
  - 0a 资产扫描（LS列出所有已有文件）
  - 0b 资产标准化转换（0b-1文件名+目录归位 / 0b-2内容结构标准化——对照每个文件的标准模板结构重组）
  - 0c 缺口分析（逐Phase检查就绪状态）
  - 0d 落地Phase决策（8种场景决策表+用户确认）
  - 0e 状态文件重建（project-state.md mode+phase+chapter+阶段完成情况 + 脚本生成html）
  - 0f 补缺生成（0f-1正文反推 / 0f-2缺失设计文档补建 / 0f-3无法反推文档处理）
- **三种mode**：fresh（从零开始）/import（导入已有设定）/resume（续写已有正文）
- **标准化转换覆盖全部16个标准文件**：每个文件都有标准文件名映射表+标准内容结构定义+转换方式（适配番茄文件结构：创意.md/力量体系.md/剧情白描.md等）
- **step1.md增加前置检测**：LS扫描项目目录，检测到 正文/ 或 设计/ 已有文件→重定向到Step 0
- **project-state.md模板新增mode字段**：`mode: fresh`
- **generate-state-html.py新增mode解析**：解析mode字段→替换模板`{{MODE}}`占位符
- **project-state.html.tpl新增mode显示**：phase-badge行增加"模式：{{MODE}}"
- **正文反推功能**：有正文但缺小说快照时，从正文提取角色/剧情/设定/伏笔→生成小说快照.md+current-state.md
- **降级模式**：缺剧情白描时，用户可选择跳过plot直接续写，在current-state.md中手动指定下一章核心事件
- **新增红线第8条**：导入/续写模式不可跳过资产扫描
- **速查表新增step0-import.md条目**
- skill.json版本更新：3.3.0→3.4.0

## v3.3.0 (2026-07-22)

### 按Popwave Skill设计规范重写SKILL.md结构

**改动**：
- SKILL.md从329行压缩到60行（≤100行），frontmatter加触发条件式description
- 红线从8条改为7条（新增读取协议红线，合并原红线1+2+6为一条），保留全部业务红线
- 速查表从启动判断表+Skill调度表改为全文件目录引导（含steps/scripts/templates）
- 新增强弱加载保障声明
- 版本历史只留最新一条，其余在CHANGELOG.md
- SOP骨架每step压缩到1-2行，Phase路由压缩为表格
- skill.json版本3.2.0→3.3.0，description改为触发条件式

**保留不动**：Phase路由规则/项目空间结构/state.md模板/step1.md/step2.md——业务方法论不做改动

## v3.2.0 (2026-07-21)

### 设计文件夹拆为3个子文件夹 + 骨架.md拆为多文件 + 全链路路径同步

**改动**：
- 设计/ 下创建3个子文件夹：全书设定/（world产出）、角色库/（character产出）、第一卷剧情/（plot产出）
- 骨架.md拆为多文件落盘到 设计/全书设定/（力量体系.md+地图.md+势力.md+危机.md+各卷切片.md+全书配角.md）
- 路径映射表新增3行：骨架.md→全书设定/、剧情白描.md→第一卷剧情/、角色库.md→角色库/
- Phase路由规则所有路径引用更新：Phase 2产出→全书设定/、Phase 3产出→第一卷剧情/剧情白描.md、Phase 3.5产出→角色库/角色库.md
- Phase 4前置检查+子agent指令模板路径更新
- project-state.md模板阶段完成情况路径更新
- Skill调度表产出路径列更新
- step1.md初始化目录创建3个子文件夹
- step2.md所有路径引用更新
- 创意.md保持在 设计/根目录（所有设计的源头）

## v3.1.1 (2026-07-21)

### HTML可视化改为脚本生成

**根因**：v3.0.0的HTML可视化只写了占位符映射规则，没给agent可执行指令。agent不会自己去读模板文件、解析md字段、替换占位符——这是代码逻辑不是agent能自然执行的。项目b测试发现project-state.html从未被生成。

**改动**：
- 新增脚本 `scripts/generate-state-html.py`：读取project-state.md→解析字段→替换模板占位符→同目录生成project-state.html
- SKILL.md HTML可视化部分改为"运行脚本"的可执行指令，删除占位符映射表
- step1.md 1d改为运行脚本
- step2.md 更新state.md后改为运行脚本
- 红线2保持"每次更新state.md必须同步生成state.html"，执行方式改为脚本
- 已用项目b测试验证脚本可正确生成HTML

## v3.1.0 (2026-07-21)

### 新增Phase 3.5 Character + Phase 4子agent红线

- 新增Phase 3.5 Character：plot完成后、write之前，调pop-fanqie-character建角色库。消费分幕设计出场角色清单+骨架敌人梯度+创意主角轮廓，产出设计/角色库.md
- Phase 4 Write改为必须子agent执行：主agent只做路由，子agent指令模板含"必须加载角色库.md，战斗/升级场景必须使用DNA面板格式"
- 红线新增第5条"Phase 4必须用子agent调write"+第7条"Phase 3.5 Character必须执行"
- state模板/调度表/路由表/step2.md全部对齐Phase 3.5
- Skill调度表Phase 4标注"子agent"，Phase 3.5新增行

## v3.0.0 (2026-07-21)

### 项目空间重构 + project-state.html可视化

**根因**：老板在agent环境测试后发现项目空间文件夹分级不合理——0/1/2数字编号和downloads/写作参考/涌现功能名混用，1-骨架文件夹混了骨架+剧情白描两个phase的产出，Phase 0产出散落三处。同时project-state.md只有agent能读，人看进度不直观。

**改动**：

- **项目空间重构为四文件夹**：
  - 素材/ = Phase 0产出（调研+DNA+拆书+原书，合并旧写作参考/+涌现/+downloads/）
  - 设计/ = Phase 1-3产出（创意+骨架+剧情白描，合并旧0-立项/+1-骨架/）
  - 正文/ = Phase 4产出（逐章渲染，旧2-正文/改名）
  - 审核/ = Phase 5产出（审核记录，保持不变）
- **project-state.html可视化**（v3.0.0新增）：
  - 每次更新project-state.md时同步生成project-state.html
  - 自包含单文件（内联CSS+JS），浏览器直接打开
  - 内容板块：项目名+时间戳 → Phase进度条(6个phase可视化) → 下一步操作 → 底牌就绪卡片 → 创意摘要卡片 → 最近产出表格
  - 模板文件：templates/project-state.html.tpl（占位符替换方式生成）
- **路径映射表**：SKILL.md新增旧→新路径映射表，所有路径引用统一更新
- **step1.md**：初始化目录改为四文件夹（素材/素材/downloads + 素材/知识沉淀 + 设计 + 正文 + 审核）+ 1d新增生成project-state.html
- **step2.md**：路由分流对齐6 phase结构 + 新路径 + 每次更新state.md后同步生成state.html的规则
- **SKILL.md红线**：新增红线2"每次更新state.md必须同步生成state.html"
- **批量路径替换**：番茄skill群15个文件共89处路径引用统一更新（seed/world/plot/write/review/research/dna-style）
- **Skill调度表**：新增"产出路径"列，每个phase的产出文件路径一目了然

## v2.1.0 (2026-07-21)

### Phase 2拆分为World+Plot，设定设计与叙事创作分离

**根因**：原Phase 2=Plot聚合了设定设计（力量体系→地图→势力→危机→弧线）和叙事创作（剧情白描+章锚点表）两个能力域。混在一个skill里压力太大，设定设计的质量瓶颈会拖累叙事创作。

**改动**：
- **Phase拆分**：原Phase 2(Plot)拆为Phase 2(World)+Phase 3(Plot)
  - Phase 2: World → 调pop-fanqie-world，产出骨架.md
  - Phase 3: Plot → 调pop-fanqie-plot，消费骨架.md，产出剧情白描.md+章锚点表.md
- **后续phase重编号**：原Phase 3(Write)→Phase 4，原Phase 4(Review)→Phase 5
- **project-state.md模板**：phase枚举增加phase5，阶段完成情况拆分为6项
- **速查表**：启动判断表+Skill调度表同步更新
- **skill.json**：v2.0.0→v2.1.0

**关联改动**：
- 新建 pop-fanqie-world v1.0.0
- pop-fanqie-plot v2.1.1→v3.0.0（瘦身）

## v1.0.0 (2026-07-20)

### 新建pop-fanqie-pipeline skill

**根因**：R41全链路测试+7-20项目a实际运行诊断发现管线三大结构性缺口：
1. 没有"我在哪"的文件——agent启动时没有任何落盘文件告诉它当前在管线的哪个阶段
2. skill之间盲调度——每个skill只知道自己的SOP，不知道何时该调下游
3. 参考书是"用户提了才触发"的可选项——seed 1a不问参考书，用户不提就永远跳过

**设计**：
- SKILL.md：项目初始化+project-state.md模板+5个phase路由规则+红线5条+速查表
- step1.md：初始化。创建标准目录结构（8个子目录）+ 落盘project-state.md（phase=init）
- step2.md：路由。读project-state.md → 按phase值分流到5个phase执行，每个phase完成后更新state
- skill.json：v1.0.0

**Phase 0参考书闸门**（最关键的改动）：
- 进入Phase 1 Seed前，必须先通过Phase 0参考书摸底
- 三条路径：用户给书名→download+dna-style / 用户没想好→research推荐→download+dna-style / 用户明确拒绝→标注风险
- 不完成参考书摸底，不进入Phase 1

**项目目录结构**：
```
项目/
├── project-state.md        ← 管线状态追踪
├── 0-立项/
├── 1-骨架/
├── 2-正文/
├── 审核/
├── 涌现/
├── downloads/
└── 写作参考/知识沉淀/
```
