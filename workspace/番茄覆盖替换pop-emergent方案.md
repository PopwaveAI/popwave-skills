# 番茄覆盖替换 pop-emergent：替换方案

> 方向变更：番茄 skill 群是主体（产出效果更好），覆盖替换 pop-emergent 系列
> 日期：2026-07-14

---

## 一、为什么反过来

上一版分析结论是"以 pop-emergent 为骨架注入番茄内容"——但用户实际使用中番茄 skill 群产出效果更好。原因：

1. **番茄有完整的剧情规划层**（plot-design：6道门禁+剧情白描+反拆维度+施工卡），pop-emergent 这个层是空白
2. **番茄有深度写作技法体系**（6章型/17微观技法/五层指导），pop-emergent-write 太轻
3. **番茄有流派专属完整引擎**（dndlike/onepiece），pop-emergent 的 DNA 执行包深度不够
4. **番茄有完整设定体系**（seed 世界展开：主角引擎/角色储备池/世界圣经），pop-emergent-seed 只做 seed+soul

pop-emergent 的优势在**架构层**而非**内容层**——它的 current-state/soul/execution.mode/PRD契约层/历史层规则是番茄缺失的。

**结论：番茄内容做主体，覆盖替换 pop-emergent；同时吸收 pop-emergent 的架构资产。**

---

## 二、pop-emergent 中值得保留的架构资产

通读 pop-emergent 全部 step/template/PRD 后，以下 7 项是番茄确实没有的：

| # | 架构资产 | 来源 | 番茄现状 | 保留价值 |
|---|---------|------|---------|---------|
| 1 | **current-state.md 唯一入口包** | pop-emergent-review 产出，write 消费 | 番茄用施工卡+事实快照直接对接，无 1000-2500 字压缩 | ★★★★★ 解决长线连载信息膨胀 |
| 2 | **soul.md 独立文风文件** | pop-emergent-seed 产出 | 番茄文风嵌在 seed-种子文档.md 中 | ★★★★☆ 文风与内容分离更清晰 |
| 3 | **execution.mode 三档** | PRD §4.5 | 番茄没有 | ★★★☆☆ 灵活性 |
| 4 | **review-沉淀.md append-only** | pop-emergent-review step-2 | 番茄有状态快照但无 append-only 日志 | ★★★★☆ 审稿历史可追溯 |
| 5 | **压缩归档/ 机制** | pop-emergent-review step-2 | 番茄无旧版归档 | ★★★☆☆ 版本安全 |
| 6 | **PRD 契约层统一管理** | pop-emergent/references/ | 番茄各自定义 SOP/红线/速查表 | ★★★★☆ 多 skill 一致性 |
| 7 | **pop-emergent 初始化/审计入口** | pop-emergent | 番茄无项目初始化 | ★★★☆☆ 项目管理 |

以下 3 项**不保留**（番茄方案更优）：

| # | pop-emergent 机制 | 不保留原因 |
|---|------------------|-----------|
| A | DNA 执行包机制 | 番茄的流派专属 skill 更完整更深，直接用流派 skill |
| B | pop-emergent-research 独立燃料 skill | 番茄的素材收集内嵌在 plot-design Step 1，与剧情设计紧密耦合，拆开反而损失协同 |
| C | "轻 write"哲学 | 番茄是"重 write"——17微观技法+五层指导是产出质量的保障，不应减轻 |

---

## 三、替换映射

### 3.1 总览

```
番茄 skill 群                        →  pop-emergent 系列（覆盖后）
─────────────                        ──────────────────────
seed                                 →  pop-emergent-seed（覆盖+吸收soul.md）
plot-design                          →  pop-emergent-plot（新增，填补空白）
prose-render (兜底)                   →  pop-emergent-write（覆盖+吸收current-state消费）
prose-render-dndlike                 →  保留为独立流派skill（更名为pop-emergent-write-dndlike）
prose-render-onepiece                →  保留为独立流派skill（更名为pop-emergent-write-onepiece）
review                               →  pop-emergent-review（覆盖+吸收current-state更新+历史层）
(无)                                 →  pop-emergent（保留，更新骨架定义）
```

### 3.2 逐 skill 替换详情

#### 替换1: seed → pop-emergent-seed

**覆盖内容（番茄 seed 主体）：**
- 完整 SOP（Step 0-10）：种子构建(0-7) + 世界展开(8-10)
- 主角引擎9字段
- 角色储备池SABC四级
- 世界圣经8模块
- 金手指巧思设计（6维度+4反模式）
- 三阶段走向声明
- 体量规划+全书故事弧
- 全部红线（9条）+ 速查表
- templates/（世界圣经模板/主角引擎模板/角色储备池模板）

**从 pop-emergent 吸收：**
- soul.md 首版落盘——seed 完成后额外产出 soul.md（从种子文档的风格关键词/数值表达方式中提取，独立为文风文件）
- execution.mode（formal/draft/trial）
- skill.json + CHANGELOG.md + agents/openai.yaml

**不吸收：**
- pop-emergent-seed 的轻量 seed 设计（番茄的更完整）
- PRD §4 契约引用（番茄自定 SOP，但命名规范对齐 pop-emergent 系列）

#### 替换2: plot-design → pop-emergent-plot（新增）

这是最关键的替换——番茄 plot-design 填补 pop-emergent 的最大结构性空白。

**覆盖内容（番茄 plot-design 主体）：**
- 完整 SOP（Step 0-4）：加载上下文→素材收集→幕纲(5步设计链路)→事实快照→施工卡
- 6道前置门禁
- 剧情白描环节（三段差异化→评估→整合+9项质量自检）
- 反拆维度系统
- 施工卡交接机制
- 微beat类型系统（8种类型×频率）
- 赛道文档体系（修仙流/都市异能/末世流/游戏入侵/悬疑流/通用）
- 设计原则库（开局/危机/成长/情感/战斗 5个文件）
- 全部红线（15条）+ 速查表
- steps/（step-1-material/step-2-act/step-3-snapshot/step-3-chapters）
- templates/（幕纲模板）

**从 pop-emergent 吸收：**
- 施工卡输出对接 current-state（而非直接对接 prose-render）——施工卡由 review 压缩进 current-state 的"下一章硬推进"
- execution.mode
- skill.json + CHANGELOG.md + agents/openai.yaml

#### 替换3: prose-render → pop-emergent-write

**覆盖内容（番茄 prose-render 主体）：**
- 完整 SOP（Step 1-7）：加载上下文→加载设定→选章型→加载references→章意图思考→微观技法选择→写作→验收→移交review
- 6种章型骨架（每种7节拍）
- 17类微观技法体系（通用6+情境6+流派专属5，每类独立文件含子技法+原文案例）
- 五层写作指导（笔触层/节奏层/格局层/爽感层/微观层，含优先级）
- 章意图思考环节（Step 3.5）
- 微观技法事前选择机制（Step 4.5，选2-3类+填写选择卡+必须加载技法文件）
- 全部参考文件（爽点引擎/格局手法/位阶表达工具箱/番茄读者心理/爽文剧情设计SOP/爽点链条矩阵/微观技法工具箱/章型定义）
- references/目录（通用技法6+情境技法6+流派专属5，17个独立文件）
- 全部红线（6条）+ 速查表（节奏约束/格局五支柱/爽感/验收表）
- dna/目录（深渊主宰-v8/v9/v10 + 遮天-v8）

**从 pop-emergent 吸收：**
- current-state.md 消费——write 读取 current-state（含下一章硬推进+人物状态+燃料队列+伏笔债务）替代直接读施工卡
- soul.md 消费——write 读取 soul.md（文风/笔触/风格）替代从 seed-种子文档.md 中提取
- 正文落盘到 `涌现/正文/`（不在对话中全文输出）
- execution.mode
- skill.json + CHANGELOG.md + agents/openai.yaml

**关键适配：**
- write 的 Step 1 从"读取施工卡"改为"读取 current-state.md + soul.md + 最近正文"
- 章型选择从"读 current-state.md 的本章硬锚点"改为"读 current-state.md 的下一章硬推进"
- 17类微观技法的加载方式不变（仍按需加载 references/）

#### 替换4: prose-render-dndlike → pop-emergent-write-dndlike

**保留为独立流派 skill**，更名对齐 pop-emergent 系列。

**覆盖内容（完整保留）：**
- 完整独立 SOP（8步）
- 6种章型骨架
- 笔触DNA（深渊主宰-笔触DNA.md）
- 流派技法（战斗模式×3等级段/面板叙事/数据化分析/场景卡/特殊条件战/多线叙事）
- 面板弹出判断表
- 全部红线（11条）+ 速查表
- 从 pop-emergent 吸收：current-state 消费 + 落盘 + execution.mode

#### 替换5: prose-render-onepiece → pop-emergent-write-onepiece

**保留为独立流派 skill**，更名对齐 pop-emergent 系列。

**覆盖内容（完整保留）：**
- 三层架构（skill/project/seed）
- 完整独立 SOP（8步）
- 赛道定义8条特征
- 战斗模式×3阶段
- 海上战斗/多线叙事/场景卡
- API管道注入规范
- 全部红线（赛道级+书级）+ 速查表
- 从 pop-emergent 吸收：current-state 消费 + 落盘 + execution.mode

#### 替换6: review → pop-emergent-review

**覆盖内容（番茄 review 主体）：**
- 逐beat对比（正文 vs 施工卡，标注 ✅/⚠️/❌/➕）
- gap分类系统（提速/延迟/偏离/遗漏/新增）
- 质量判断5维度（叙事自然度/读者体验/爽感完整性/后续影响/字数合理）
- 笔触质量审核8维度
- 状态快照（面板/位置/物品/情报/已传递信息/结尾场景/下章起点）
- gap决策速查表
- 全部红线（5条）+ 速查表

**从 pop-emergent 吸收：**
- **current-state.md 更新作为核心产物**——review 审完后不只输出审核报告+状态快照，还要更新 current-state.md（将状态快照+下一章硬推进+伏笔债务压缩进 current-state）
- **review-沉淀.md append-only**——每次审稿追加一段（日期/章位/总判断/3个问题/current-state是否更新/修正规则），不删改历史
- **压缩归档/**——更新 current-state 前先归档旧版到 `压缩归档/current-state-{YYYYMMDD}-{章位}.md`
- **沉淀分流机制**——把审计发现分两类：哪些更新库文件（设定库/人物库/剧情线/燃料），哪些压入 current-state
- execution.mode
- skill.json + CHANGELOG.md + agents/openai.yaml

**关键适配：**
- review 的 Step 2（gap分析）保持番茄的逐beat对比+gap分类
- 新增 Step 3：将审核结果压缩进 current-state.md（吸收 pop-emergent-review 的 step-2-commit）
- 状态快照融入 current-state 的人物状态字段

#### 保留7: pop-emergent（初始化/审计入口）

**保留但更新**——更新骨架定义以反映新的 skill 结构：

```
pop-emergent（初始化/审计）
├── pop-emergent-seed（番茄seed覆盖，含世界展开+soul.md）
├── pop-emergent-plot（番茄plot-design迁移，新增）
├── pop-emergent-write（番茄prose-render覆盖，含current-state消费）
├── pop-emergent-write-dndlike（番茄dndlike更名，独立流派）
├── pop-emergent-write-onepiece（番茄onepiece更名，独立流派）
└── pop-emergent-review（番茄review覆盖，含current-state更新+历史层）
```

---

## 四、覆盖后的项目骨架

覆盖后，pop-emergent 系列的项目骨架升级为：

```
涌现/
  current-state.md          # 入口层：下一章写作唯一入口包（review产出，write消费）
  soul.md                   # 入口层：文风+笔触+风格（seed首版产出，review修正）
  seed-种子文档.md          # 库层：长期承诺和故事宪法
  主角引擎.md               # 库层：主角9字段行为模式表（seed阶段二产出）
  角色储备池.md             # 库层：SABC四级角色（seed阶段二产出）
  世界圣经.md               # 库层：8模块世界底座（seed阶段二产出）
  research-写作燃料.md      # 库层：燃料池（plot-design Step1素材收集产出）
  content-mechanics.md      # 库层：题材机制分流
  设定库.md                 # 库层：已确认设定事实（review更新）
  人物库.md                 # 库层：人物最新状态（review更新）
  剧情线.md                 # 库层：伏笔/债务/中长线推进（review更新）
  review-沉淀.md            # 历史层：审稿日志（append-only）
  压缩归档/                 # 历史层：current-state旧版
    current-state-{YYYYMMDD}-{章位}.md
  燃料库/                   # plot-design素材收集产出
    原始燃料/
  卷纲/                     # plot-design幕纲产出
    幕NNN-候选方案.md
    幕NNN-设计笔记.md
    幕纲-幕NNN-{标题}.md
  施工卡/                   # plot-design施工卡产出
    chNNN-施工卡.md
  事实快照/                 # plot-design事实快照产出
    事实快照-幕NNN.md
  正文/                     # write产出
    {书名}-第{N}章-{标题}.txt
写作资产/
  文风库/                   # 流派DNA源（如启用）
    {作品}.md
  dna/                      # 笔触DNA（流派skill内或项目内）
```

---

## 五、覆盖后的标准流程

```
pop-emergent 初始化骨架
→ pop-emergent-seed
  [碰撞idea → 锁定种子 → 世界展开(主角引擎/角色储备池/世界圣经)]
  [产出: seed-种子文档.md + soul.md + 主角引擎.md + 角色储备池.md + 世界圣经.md]
→ pop-emergent-plot
  [素材收集(11维度搜索) → 幕纲(6门禁+剧情白描+反拆维度) → 施工卡 → 事实快照]
  [产出: 燃料库/ + 卷纲/ + 施工卡/ + 事实快照/]
→ pop-emergent-review 初始化 current-state
  [将施工卡+事实快照压缩为 current-state.md(1000-2500字)]
  [归档旧版 + 追加review-沉淀.md]
→ pop-emergent-write (或流派专属skill)
  [消费 current-state+soul → 章意图思考 → 选章型 → 选技法 → 五层写作 → 落盘到正文/]
  [产出: 正文/{章节}.txt]
→ pop-emergent-review
  [逐beat对比 → gap分析(5分类+5维度) → 笔触审核(8维度) → 更新current-state → 历史层]
  [产出: 新版current-state.md + review-沉淀.md追加 + 压缩归档/]
→ 循环 write ↔ review
```

---

## 六、覆盖执行清单

### 6.1 文件操作

| 操作 | 源 | 目标 |
|------|----|------|
| 覆盖 SKILL.md | 番茄/seed/SKILL.md | pop-emergent-seed/SKILL.md（+soul.md吸收） |
| 覆盖 SKILL.md | 番茄/prose-render/SKILL.md | pop-emergent-write/SKILL.md（+current-state吸收） |
| 覆盖 SKILL.md | 番茄/review/SKILL.md | pop-emergent-review/SKILL.md（+current-state更新+历史层吸收） |
| 新建 SKILL.md | 番茄/plot-design/SKILL.md | pop-emergent-plot/SKILL.md（新增skill） |
| 复制+更名 | 番茄/prose-render-dndlike/ | pop-emergent-write-dndlike/ |
| 复制+更名 | 番茄/prose-render-onepiece/ | pop-emergent-write-onepiece/ |
| 迁移 references/ | 番茄/prose-render/references/ | pop-emergent-write/references/ |
| 迁移 references/ | 番茄/plot-design/references/ | pop-emergent-plot/references/ |
| 迁移 steps/ | 番茄/plot-design/steps/ | pop-emergent-plot/steps/ |
| 迁移 templates/ | 番茄/seed/templates/ | pop-emergent-seed/templates/ |
| 迁移 templates/ | 番茄/plot-design/templates/ | pop-emergent-plot/templates/ |
| 更新 | pop-emergent/SKILL.md | 更新骨架定义（6→7 skill） |
| 更新 | pop-emergent/references/v3.5-pipeline-prd.md | 更新PRD契约层 |

### 6.2 每个 skill 需要补的文件

每个覆盖后的 skill 需要补齐 pop-emergent 系列的标配文件：

- `skill.json`（如不存在则新建）
- `CHANGELOG.md`（如不存在则新建）
- `agents/openai.yaml`（如不存在则新建）

### 6.3 需要新增的文件

| 文件 | 位置 | 来源 |
|------|------|------|
| soul.tpl.md | pop-emergent-seed/templates/ | 从 pop-emergent-seed 保留 |
| current-state.tpl.md | pop-emergent-review/templates/ | 从 pop-emergent-review 保留 |
| step-2-commit.md | pop-emergent-review/steps/ | 从 pop-emergent-review 保留（current-state更新+历史层） |

---

## 七、风险与注意事项

| 风险 | 说明 | 缓解 |
|------|------|------|
| current-state 与施工卡的衔接 | 番茄施工卡是 plot→prose 直接对接，改为 current-state 间接对接需要适配 | review 负责将施工卡压缩进 current-state；write 读 current-state 而非施工卡 |
| 番茄 SOP 与 PRD 契约层冲突 | 番茄各自定义 SOP/红线/速查表，与 PRD §4 可能冲突 | 保留番茄 SOP 主体，只对齐命名规范/版本管理/回复格式 |
| 流派 skill 命名 | dndlike/onepiece 更名为 pop-emergent-write-* 后路径引用需更新 | 全局搜索替换路径引用 |
| soul.md 与 seed 文风字段重复 | 番茄 seed-种子文档.md 中有风格关键词，soul.md 也有 | seed 的风格关键词作为 soul.md 的输入源，soul.md 落盘后 seed 中只保留引用 |
