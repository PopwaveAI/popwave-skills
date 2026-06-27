# CHANGELOG — expert-writer

## [9.7.0] - 2026-06-28
### Added
- 全文注入铁律红线（❌8禁止摘要注入子agent）
- manifest.md新增「全文注入铁律」章节：禁止主agent提炼/摘要后注入，所有文件类注入项必须全文
- create manifest新增L2卡全文注入+文风DNA全文注入（仅参考）
- revise manifest新增L2卡嵌套子线全文注入+文风DNA全文注入
- receipt新增injection_verified字段（确认收到的是全文不是摘要）
- receipt检查从6项扩展为7项（新增L2卡全文注入验证）
### Changed
- step-2-3 dispatch文件全面重写：manifest_version 1.0→1.1，所有注入项新增injection: full标注
- create manifest注入项从6项扩展为8项（新增L2卡全文+文风DNA全文）
- create receipt从three_questions确认改为five_questions确认
- revise manifest的element_slices改为l2_sublines（L2卡嵌套子线全文）
- revise receipt导演意图验证从5项改为6项

## [9.6.0] - 2026-06-28
### Added
- 网文写作铁律红线（❌6直接易懂爽感优先+❌7世界观卖点前置）
- 导演意图验证从5项扩展为6项（新增世界观传递验证）
- 5步循环门禁表更新（Step3/Step4验证项更新）
### Changed
- step-2-0导演意图组装：三问→五问（新增worldview+clarity）
- step-2-0导演意图新增worldview_delivery字段

## v9.5.0 | 2026-06-28

### v3.5涌现式写作管线重构：6步→5步+L2卡替代种子文档+context manifest白盒

**核心变化：**

| 维度 | v9.4.0 (v3.4) | v9.5.0 (v3.5) |
|:-----|:--------------|:--------------|
| 循环步数 | 6步 | 5步 |
| 活文档 | 种子文档.md | L2剧情单元卡 |
| 种子文档 | 存在 | 取消（功能被L2卡+写作参考吸收） |
| 结构约束 | 种子文档任务表 | L2卡（跨章）+导演意图（单章） |
| 设定读取 | 靠agent自觉 | L2卡设定指针→主会话强制读→manifest验证 |
| 状态管理 | 活记忆7组件结构化YAML | 活记忆自然语言段落 |
| 子agent上下文 | 黑盒 | context manifest白盒 |
| 素材库+设定库 | 分开 | 合并为写作参考/ |
| arc触发 | 每10-20章 | 每个L2单元结束时 |
| 种子生长 | 8种场景 | 删除（L2卡每单元由arc更新） |

**5步循环结构（替代6步）：**
- Step0：导演意图提取（从L2卡结构分析表取本章行→组装导演意图≤150字）
- Step1：状态快照投影（从活记忆+L2卡物理坐标投影≤400字）
- Step2：信息获取（设定指针强制读取+library按需查询+pop-research如需）
- Step3：子agent创作（create涌现→revise重写，一次调度，context manifest白盒）
- Step4：receipt检查（manifest vs receipt一致性+导演意图验证）
- Step5：活记忆更新+落盘（合并原memory+commit两步）

**文件变更：**
- `SKILL.md`：v9.4.0→v9.5.0，6步门禁表→5步门禁表，5条红线更新，文件加载规范更新（L2卡+写作参考替代种子文档+素材库+设定库），管线顺序新增plot+pop-research，emerge标注废弃
- `skill.json`：v9.4.0→v9.5.0，downstream新增pop-research
- `steps/step-0-init.md`：项目空间结构更新（卷纲/L2/L3+写作参考替代素材库+设定库）
- `steps/step-1-think.md`：管线锚定更新（L2卡替代种子文档），5步循环路由
- `steps/step-2-execute.md`：6步循环→5步循环执行流程
- `steps/step-2-0-director-intent.md`：新建（导演意图提取，替代step-2-0-chapter-plan.md）
- `steps/step-2-1-state-snapshot.md`：新建（状态快照投影，替代step-2-1-info-forced.md）
- `steps/step-2-2-info-acquisition.md`：新建（信息获取：设定指针强制读取+library查询）
- `steps/step-2-3-dispatch-create-revise.md`：新建（合并dispatch-create+dispatch-revise，create→revise一次调度）
- `steps/step-2-4-receipt-check.md`：新建（receipt一致性检查，context manifest白盒）
- `steps/step-2-5-memory-commit.md`：新建（合并memory-direction+commit，活记忆自然语言追加+落盘）
- `steps/step-3-reflect.md`：更新引用（5步循环+L2卡）
- `references/pipeline/manifest.md`：v3.3→v3.5，阶段表新增plot和pop-research
- `references/project/master-control.tpl.md`：管线身份更新为v9.5.0，种子文档引用改为L2卡
- `references/think/typical-paths.md`：路径更新（新增plot阶段）

**删除文件（6个旧step文件）：**
- `steps/step-2-0-chapter-plan.md` → 替换为 `step-2-0-director-intent.md`
- `steps/step-2-1-info-forced.md` → 替换为 `step-2-1-state-snapshot.md`
- `steps/step-2-2-dispatch-create.md` → 合并入 `step-2-3-dispatch-create-revise.md`
- `steps/step-2-3-dispatch-revise.md` → 合并入 `step-2-3-dispatch-create-revise.md`
- `steps/step-2-4-memory-direction.md` → 合并入 `step-2-5-memory-commit.md`
- `steps/step-2-5-commit.md` → 合并入 `step-2-5-memory-commit.md`

## v9.4.0 | 2026-06-27
- v3.5修复：管线顺序前置+无大纲声明（任务表内化大纲功能）
- Step0从"做chapter plan"改为"更新种子文档任务表+本章聚焦"
- Step1新增三问前置验证（信息/压力/钩子，未回答=退回Step0）
- 管线新增pop-writer-v3-plot（任务链设计skill）
- 种子文档统一化（单文件活文档替代6分文件+_index+_log）

## v9.3.0 | 2026-06-27
- v3.4修复：SKILL.md内联6步核心门禁表+文件加载规范（框架加载即生效，解决skill一次性消费）
- 7步→6步剔除qa调用（质检职责下沉revise层）
- plan重构为任务list（Markdown格式，定义"达成什么"非"怎么达成"）
- revise重构为完全重写（基于正文+文风DNA直接重写，禁止改写事实信息）
- create→revise自动连贯，仅双check点（plan确认+最终正文验收）
- 子agent降级策略B（重试1次→降级主会话但必须重读完整种子context+DNA完整加载+独立质检）
- 资料总索引标准化（取代散落的素材库/索引.md和设定库/_index.yaml）
- 字数硬门禁（2500-3500字/章）
- step-2-5/6重命名为step-2-4/5（qa剔除后序号前移）
- references全量stale清理（manifest/活种子生长规则/typical-paths/typical-errors）

## v9.2.0 | 2026-06-26
- expert-writer 吸收 emerge 调度职能，消除两层调度器冗余
- step-2-execute.md 重写为7步循环执行流程（Step 0/1/5/6主会话执行 + Step 2/3/4调度3子skill）
- emerge 的 7个step文件 + 3个references文件迁移到 references/emerge-loop/（作为参考文档，已更新路径引用）
- SKILL.md：管线顺序移除emerge；路由表"继续/下一步"改为expert-writer(7步循环)；references速查表新增emerge-loop条目；版本9.2.0
- skill.json：downstream移除pop-writer-v3-emerge，新增pop-writer-v3-create/revise/qa
- manifest.md：管线阶段2从pop-writer-v3-emerge改为expert-writer（7步循环主会话+调度3子skill）
- pop-writer-v3-emerge 标记为废弃（SKILL.md添加deprecated标记）
- v3.3管线：种子文件夹结构 + 三界压力框架 + 设定库按需读取 + expert-writer唯一调度器

## v9.0.0 | 2026-06-26
- 去掉v2双轨，全方面服务于v3.1涌现式写作管线
- v2 skill文件本身不动（pop-writer-creative/world/character/plot/chapter/prose/qa不修改不删除），expert-writer不再引用
- SKILL.md：version→9.0.0；description改为"v3.1涌现式写作管线调度引擎"；删除管线模式声明表v2行+"模式存储在项目总控.md"段；红线❌5改为"子agent调度必须context隔离"；查询矩阵删除v2列，v3-emerge改为"创作层(按需)+修订层(文风)"；删除v2路由表；v3路由表emerge行更新为"调度3子agent"；核心流程只描述v3.1逻辑
- step-0-init：删除步骤1a管线模式选择+v2目录骨架段；v3骨架新增知识库目录；初始化直接创建v3目录；路由直接到v3-seed
- step-1-think：删除v2管线锚定分支+"字段不存在→按v2处理"兼容逻辑；状态感知为唯一逻辑（种子六要素）；删除v2意图识别+闸门；v3为唯一
- step-2-execute：删除v2强制加载分支+v2执行段+§3.1-3.4全部v2修改路由(影响范围/回溯触发/回滚/常规修改)；重写为3子agent调度逻辑(6要点)；v3修改路由+项目回滚为唯一
- step-3-reflect：删除v2验收表+弃书风险章标注+v2 8阶段仪表盘+state-log压缩检查+v2引导模板；v3验收/方向提示/弧线校准/活记忆压缩/引导为唯一
- manifest.md：删除v2全管线合同段(管线顺序/入口规则/文件接口/回溯规则/变更传播/DQTC约170行)；v3为唯一管线合同；新增3子agent调度架构+种子六要素+知识库目录接口+信息获取强制化产物
- master-control.tpl.md：删除管线模式字段+v2 8阶段仪表盘；v3 3阶段仪表盘为唯一；文风DNA路径解析适配v3.1（空=待蒸馏，不阻塞初始化）
- "七要素"全部改为"六要素"（文风DNA从种子要素变为项目资产）

## v8.0.0 | 2026-06-26
- 重新引入双轨支持（v2雪花式/v3涌现式），用于AB测试
- v3涌现式管线独立新建：pop-writer-v3-seed(种子设计) + pop-writer-v3-emerge(涌现写作环) + pop-writer-v3-arc(弧线校准)
- SKILL.md：新增管线模式声明段(v2/v3对比表) + 红线❌5(v3项目不可混用v2 skill) + v3路由表 + version→8.0.0
- step-0-init：新增模式询问步骤 + v3目录骨架(5目录简化版)
- step-1-think：模式感知路由(v2→8阶段/v3→3阶段+v3信息需求判断+智能调度)
- step-2-execute：按模式加载不同skill集 + v3信息获取调度+种子生长调度
- step-3-reflect：模式感知审视 + v3方向提示+弧线校准检查+种子生长判断
- manifest.md：新增v3管线合同段(3阶段循环+活种子+活记忆七组件+信息需求判断)
- master-control.tpl.md：新增管线模式字段 + v3项目总控模板(3阶段仪表盘)
- registry.json：新增3个v3 skill条目 + expert-writer→8.0.0 + pop-shared-dna→4.1.0
- 新增PRD：prd/01-管线架构/10-涌现式写作专家全链路-PRD.md v2.0（实施级PRD）

## v7.0.0 | 2026-06-25
- v2管线转正为默认模式，移除v1/v2双轨切换机制
- SKILL.md：管线模式段替换为单管线声明，删除红线❌5，version→7.0.0
- step-0-init：删除步骤1a模式询问，路由简化为单一pop-writer-creative
- step-1-think：删除管线模式感知，路由简化为pop-writer-{阶段}
- step-2-execute：删除管线模式感知，修改路由表从双列改为单列
- manifest.md：主管线表更新为v2.0.0版本，删除v2独立管线表和模式选择规则
- master-control.tpl.md：删除管线模式字段，理想全流程表从双列(v1/v2)改为单列
- registry.json：删除7个v1写作skill条目，7个v2条目去-v2前缀并更新为v2.0.0
- v1写作skill封存至skills/_deprecated/（7个目录+README.md）
- 新增PRD：prd/01-管线架构/09-涌现反馈环写作管线-PRD.md（未来架构愿景）

## v6.2.0 | 2026-06-25
- 新增v1/v2管线模式切换（AB测试支持）
- SKILL.md：新增管线模式声明+红线❌5（模式未确定不可路由）
- step-0-init：新增步骤1a询问用户选择v1/v2模式
- step-1-think：管线模式感知，按模式选择对应skill前缀
- step-2-execute：按模式加载对应skill目录+修改路由表双列
- manifest.md：新增v2管线skill映射表（7个v2 skill）
- master-control.tpl.md：新增管线模式字段+理想全流程双列（v1/v2）

## v6.1.0 | 2026-06-25
- step-0-init 新增步骤3b：文风DNA路径强制解析（扫描写作资产/文风库/，空=硬阻塞）
- master-control.tpl.md 新增文风DNA自动解析规则
- 文风DNA路径未解析 = creative 阶段不可启动

## v6.0.0 | 2026-06-24
- creative 合并 reservoir：8阶段管线→7阶段管线
- creative v4.4.0→v6.0.0：种子展开法替代域研究SOP，新增Phase 3储备卡产出
- reservoir skill 已删除，能力被 creative 吸收
- 下游配套文件全部更新引用

---

## v4.6.0 (2026-06-22)

### 项目总控新增 📚知识库路径 固定区块

**问题**：用户说"library里有XX设定"，agent 找不到路径——因为项目总控没有记录 library 的约定。pop-trope-library 公共库和用户私藏参考被混用同一个词"library"，agent 无法区分。

**改动**：
- `references/project/master-control.tpl.md`：在头部（📊项目现状之前）新增固定区块 `## 📚 知识库路径`，包含：
  - 两类路径声明表（skill 公共库 + 用户私藏参考，各自独立的状态标记）
  - skill 公共库内容速览（初始化时自动扫描设定库/剧情库/文风库/套路库）
  - Agent 使用规则（4条硬约定：首次加载必查、阶段启动前确认、私藏优先、路径写入后不再追问）
- `steps/step-0-init.md`：初始化步骤新增 3a，自动解析 pop-trope-library 绝对路径、扫描设定库书目、标注对标书

**效果**：Agent 加载项目总控时直接读到 library 路径，不再重复询问"library 在哪"。两类路径（公共库 vs 私藏参考）明确区分，不再混淆。

---

## v4.5.0 (2026-06-22)

### pop-trope-library 集成：查询矩阵系统化

**问题**：PRD v5.0 只在"入"列写了"library"一词，没有系统化定义每个环节查什么模块。expert-writer 也没有 trope-library 查询引导。

**PRD 迭代（v5.0 → v5.1）**：新增"三、pop-trope-library 公共知识库集成"章节 — 四模块定义 + 8 阶段查询矩阵 + 4 条查询纪律。

**expert-writer 更新**：
- `SKILL.md`：新增 `## pop-trope-library 查询矩阵` 段落（8 阶段×查询模块×用途），管线版本标注从 v5.0 改为 v5.1
- `references/pipeline/manifest.md`：阶段表新增 `library 查询` 列，8 个阶段全部标注查询模块
- `steps/step-2-execute.md`：强制加载部分新增 library 查询提醒

**查询矩阵覆盖 7 个阶段**：creative（元爽点匹配+设定+套路）→ world（设定创意池）→ character（质感参考）→ plot（套路链+剧情库）→ chapter（套路公式）→ prose（文风DNA）→ qa（使用红线）

---

## v4.4.0 (2026-06-22)

### project/ 精简：health-check.md + state-discovery.md 删除

**问题**：`project/` 下 3 个文件中 2 个冗余。health-check.md 的全部步骤已被 step-1-think.md（管线锚定+断裂检测+进度摘要）和 step-3-reflect.md（文件系统扫描+总控回写）覆盖。state-discovery.md 的阶段推断逻辑可内联到 step-1-think.md（4 行替代 106 行）。

**删除文件（2 个）**：

| 文件 | 删除原因 |
|:-----|:---------|
| `references/project/health-check.md` | Step 0→3 全部与 step-1-think.md §1 + step-3-reflect.md 重复 |
| `references/project/state-discovery.md` | 阶段推断逻辑内联到 step-1-think.md §1（4 行替代 106 行） |

**`step-1-think.md` 更新**：§1 "加载项目总控"的不存在分支从引用 state-discovery.md 改为内联 4 步推断逻辑（扫描文件→推断阶段→初始化总控→提示确认）。

**`project/` 目录现在只剩 `master-control.tpl.md` 一个文件**（项目总控模板）。

---

## v4.3.0 (2026-06-22)

### pipeline/ 合并：arch.md 删除 + manifest.md 精简

**问题**：`pipeline/` 下两个文件 95% 内容重复。arch.md 222 行中：文件分类矩阵与 manifest.md 文件接口表几乎完全重复，目录树与 step-0-init.md 重复，Reflect 校验基线是越权内容（L1-L4 级检查，已从 step-3 删除）。

**删除**：`references/pipeline/arch.md`（222 行）

**精简 `references/pipeline/manifest.md`**（97→91 行）：
- 删除对已删文件 `pipeline-design-rationale.md` 的引用
- 删除截断检测协议（与 step-1-think.md 读取协议重复）
- 补充前置链路说明（decon/dna 独立于写作管线，从 arch.md ASCII 图压缩为 2 行文字）
- 目录骨架改为引用 `steps/step-0-init.md`（不再重复）

---

## v4.2.0 (2026-06-22)

### _shared/ 清理 + soul 内联 SKILL.md + step-0 目录骨架修正

**删除 `_shared/` 整个目录（8 文件）**：

| 文件 | 删除原因 |
|:-----|:---------|
| `_shared/pop/IDENTITY.md` | 身份声明协议已在系统 user_rules 中，重复三份 |
| `_shared/pop/SOUL.md` | 精炼后内联 SKILL.md（KGF认知栈/Dual-Phase/风格路由是 prose 级，归子 skill） |
| `_shared/pop/POP-CALL.md` | 声明模板与 IDENTITY.md 重复，路由表与 SKILL.md 重复 |
| `_shared/pop/POP-ROUTER.md` | 路由表与 SKILL.md 完全重复，引用废弃路径（project.yaml） |
| `_shared/pop/ROUTE-AUGMENT.md` | 全部基于已废弃的 workspace-index.yaml，路径引用 `00-总控/` |
| `_shared/universal-knowledge/timeline-tripartition.md` | 叙事设计知识，属于 world/plot 子 skill |
| `_shared/project_config.py` | 读取已废弃的 project.yaml |
| `_shared/thinking-mode-template.md` | 通用思考模板，非 pop soul |

**SKILL.md 新增 `## pop 身份` 段落**：从 SOUL.md 73 行精炼为 8 行（身份+纪律+边界），内联到 SKILL.md 标题下方。

**`steps/step-0-init.md` 目录骨架修正**：完全重写对齐 PRD v5.0 附录A — 删除 `00-总控/`、`创意种子/`、6个`_*/`临时目录；修正 `储备剧情池/`→`素材储备池/`；补 `终点快照.md`；修正 3 个数值文件名；`文风DNA/` 移到 `写作资产/` 下。

**`references/pipeline/arch.md`**：修正 3 个数值文件名（`act_rank_schedule.md`→`rank_schedule.md` 等）。

---

## v4.1.0 (2026-06-22)

### 越权精简：expert-writer 回归纯调度器

**核心问题**：expert-writer 越权承担了子 skill 的职能（L1-L4 详细检查、前置条件校验、落盘检查、一致性校验、QA 质检），导致内容冗余、与子 skill 职责重叠。

**精简原则**：expert-writer 只做 6 件事 — 路由决策、管线顺序管理、项目状态感知、子 skill 加载、闸门确认、项目总控回写+引导。L1-L4 详细检查、前置条件校验、落盘检查、状态协议校验等全部由子 skill 自管。

**删除文件（8 个）**：

| 文件 | 删除原因 |
|:-----|:---------|
| `references/guide/dynamic-fusion.md` | 追加核心设定的融合检查是 world 阶段 Phase 0 的职责 |
| `references/guide/derivative-gap-analysis.md` | 同人二创 Gap 分析是 creative/world 的职责 |
| `references/pipeline/check.md` | 前置条件详细检查由子 skill 自管，与 step-1-think.md 重复 |
| `references/think/开书设定.md` | Think 部分重复 step-1-think.md，Reflect 部分是 creative 子 skill 职责 |
| `references/think/审稿.md` | Think+Reflect 全是 qa 子 skill 自管职责 |
| `references/think/续写.md` | Think 部分重复 step-1-think.md，Reflect 部分是 creative/prose 职责 |
| `references/think/正文写作.md` | Think 部分是 prose 子 skill 自管，Reflect 部分是 L1-L4 详细检查（已从 step-3 删除） |
| `references/guide/batch-style-migration.md` | delegate context 重复 prose 的 step-0-delegation-contract.md，风格映射是 DNA 职责，设计包格式是 chapter 职责 |

**精简文件（6 个）**：

| 文件 | BEFORE | AFTER | 精简内容 |
|:-----|:-------|:------|:---------|
| `steps/step-1-think.md` | 118 行 | 59 行 | 删除详细前置条件检查，只保留状态感知+路由+闸门 |
| `steps/step-2-execute.md` | 96 行 | 70 行 | 简化修改路由为"退回子skill"原则，删除重复边界条件 |
| `steps/step-3-reflect.md` | 189 行 | 73 行 | 删除 L1-L4 详细检查清单，只保留通用 3 问+项目总控回写+引导 |
| `references/think/reflection.md` | 142 行 | 43 行 | 删除 L1-L4 审视清单，只保留通用层 |
| `references/think/typical-errors.md` | 89 行 | 62 行 | 删除子 skill 级错误，只保留 8 条调度器级错误 |
| `references/project/health-check.md` | 204 行 | 113 行 | 删除 Python 代码和截断扫描，精简初始化流程 |

**SKILL.md 速查表同步更新**：删除已删文件引用，补上 `step-0-init.md`，修正典型错误条数（12→8），删除 guide/ 子目录（已空）。

---

## v4.0.0 (2026-06-22)

### 全量重构：三层架构 + 读取协议 top1 + 管线对齐 PRD v5.0

**核心问题**：SKILL.md 202 行混合三层内容（路由+执行+知识），无读取协议红线，管线缺 character 阶段，版本号 5 处不一致。

**重构原则**：

| 原则 | 说明 |
|:-----|:-----|
| 三层架构 | 路由层（SKILL.md ≤85行）→ 执行层（steps/）→ 知识层（references/） |
| 读取协议 top1 | ❌1 红线 = 禁止 Read 工具，强制 skill_view / Get-Content -Raw |
| 管线对齐 PRD | 7 步含 character（creative→world→character→plot→chapter→prose→qa） |
| 速查表=全文件目录引导 | 24 个文件全部列出读取时机 |
| 版本统一 | SKILL.md / skill.json / CHANGELOG 三处版本号一致 |

**文件变更**：

| 文件 | BEFORE | AFTER | 变更 |
|:-----|:-------|:------|:-----|
| `SKILL.md` | 202 行 | 83 行 | 砍掉 59%：典型错误/核心原则/边界条件/落盘检查点/版本历史全部下沉 |
| `skill.json` | v3.1.1 | v4.0.0 | 版本更新 + downstream 补全 world/character + description 改触发式 |
| `steps/step-1-think.md` | 121 行 | 118 行 | 新增读取协议红线，管线对齐 PRD（8步含character） |
| `steps/step-2-execute.md` | 96 行 | 96 行 | 新增读取协议红线，截断检测精简引用 |
| `steps/step-3-reflect.md` | 181 行 | 189 行 | 新增读取协议红线 |
| `references/pipeline-manifest.md` | 46 行 | 77 行 | 新增 character 阶段 + 版本号列 + 文件接口表（对齐 PRD v5.0） |
| `references/typical-errors.md` | — | 新建 | 从 SKILL.md 下沉 12 条典型错误防范 |
| `references/core-principles.md` | — | 新建 | 从 SKILL.md 下沉 3 条核心原则 |
| `README.md` | 53 行 | 删除 | 内容过时（v1.0.0），已被 SKILL.md 速查表替代 |

**SKILL.md 砍了什么**：

| 段落 | BEFORE 行数 | AFTER | 去向 |
|:-----|:----:|:----:|:-----|
| 典型错误 12 条 | 16 | 0 | → `references/typical-errors.md` |
| 核心原则 3 条 | 44 | 0 | → `references/core-principles.md` |
| 边界条件表 | 20 | 0 | 已在 `steps/step-2-execute.md`（去重） |
| 落盘检查点 | 8 | 0 | 已在 `steps/step-3-reflect.md`（去重） |
| 版本历史 | 18 | 1 | → CHANGELOG.md（只留当前版本号） |
| 读取协议 | 0 | 0 | 新增在红线 ❌1（所有 step 文件也有） |
| 速查表 | 4 行路由 | 24 行目录引导 | 扩展为全文件目录引导 |

**管线对齐 PRD v5.0**：

| 阶段 | BEFORE（v3.x） | AFTER（v4.0） |
|:-----|:-------|:------|
| 管线步骤 | 7 步（缺 character） | 8 步（含 character） |
| 子 skill 版本号 | 未标注 | 标注（creative v4.3.0 / world v1.5.0 / character v2.0.1 / plot v7.0.0 / chapter v2.0.0 / prose v3.0.1 / qa v1.0.1） |
| 文件接口表 | 无 | 新增（静态文件 + 动态文件，对齐 PRD） |

---

## v3.1.1 (2026-06-14)

- **v5 结构重构**：SKILL.md 瘦身至 ≤120 行（从 176 行缩减），Think/Execute/Reflect 核心内容拆分至 `steps/step-1-think.md`、`steps/step-2-execute.md`、`steps/step-3-reflect.md`
- **红线表格化**：从列表格式转为 `| # | 红线 |` 表格格式，7 条核心红线
- **核心流程指针化**：SKILL.md 中只保留 3 步指针表，指向 steps/ 文件
- **身份声明迁移**：pop 身份声明协议（每次新任务输出格式）从 SKILL.md 移至 `_shared/pop/IDENTITY.md`
- **pipeline 字段**：skill.json 新增 `pipeline.upstream`（空数组，元 skill 无上游）和 `pipeline.downstream`（15 个子 skill 完整列表）

## v3.1.0 (2026-06-11)

- **constitution.yaml 移除**：全链路删除，act-XX.yaml Canvas 字段（chekhov_set/combat.scale/payoff/plotlines_active）已全覆盖约束
- **路径重构**：03-正文→正文、03-写作资产→写作资产/设计包、L3-角色层→状态/角色、幕按卷分组(vol-XX/)
- **Reflect L2 一致性对象变更**：entity-snapshot ↔ constitution → entity-snapshot ↔ 角色卡
- **pipeline-check**：去 constitution/act-XX-人物检查，新增状态/角色/目录检查
- **ROUTE-AUGMENT**：constitution_ok → state_ok，constitution 路径删除

## v3.0.0 (2026-06-10)

- **SKILL.md 瘦身：21K → 9K**（-57%），每次 Paopao 注入节省 12K 上下文窗口
- **5 个 references/ 文件提取**：reflection(L1-L4 审视) / dynamic-fusion(动态融合) / completion-guide(完成后引导) / pipeline-check(管道校验) / typical-paths(典型路径)
- **加载协议统一**：所有 reference 文件用 `Get-Content -Encoding UTF8 -Raw` 加载，同行标注"不用 Read 工具"
- **SKILL.md 保留骨架**：纪律/身份声明/Skill清单/路由表/工作流三步/修改路由 — 所有核心指令一律保留
- **references/reflection.md 合并**：原有 68 行 + SKILL.md L1-L4 审视清单 → 完整四层审视
- **新增 references/**：completion-guide.md, dynamic-fusion.md, pipeline-check.md, typical-paths.md

## v2.6.0 (2026-06-10)

- **动态融合检查（Think 第二步·A）**：追加核心设定后禁止打补丁。逐文件重新审视 L1 六件套每个字段，决定被新设定深度改写/不变/新建子段
- **大环节转换自检（§3.1.6 ⑥）**：bookstrap→plot→chapter-design→prose-render 切换前，agent 用 Get-Content 读取上一环节全部产出文件，回答三个语义级问题：深度是否足够、追加设定是否充分融合、是否有数据断点
- **明确禁令**：禁止"在末尾追加段落"、"只改一个文件"、"跳过逐字段检查"等打补丁行为
- **输出融合声明**：动态融合完成后输出每文件的受影响字段数

## v2.5.0 (2026-06-10)

- **路由前强制加载协议**：路由到任何子 skill 前无条件加载 4 项（子 skill SKILL.md + 全部文档文件 + 项目 YAML + 文风DNA）
- **去掉条件判断**：v2.3 "任务类型切换检查" 要求 agent 判断 intent 是否变化 → agent 判断失误极高（"都是写正文"→跳过）。v2.5 改为无条件加载，不依赖 agent 自觉
- **写为路由前置条件**：不加载 = 路由失败，agent 会被卡住，必须补加载才能继续
- **明确禁令**：禁止以"之前读过"、"我记住了"、"不需要"为理由跳过加载
- **"继续前进"路线更新**：执行路径第一条改为"先强制加载，再读进度判定路由"
- **Reflect 文件加载检查同步更新**

## v2.4.0 (2026-06-10)

- **读文件方式重构**：禁止使用 Read 工具读取子 skill 文档文件和 YAML 文件
- **全量改用 exec + Get-Content -Encoding UTF8 -Raw** — 彻底解决 Read 截断 bug
- **覆盖范围扩展**：SKILL.md、steps/*.md、phases/*.md、templates/*.md、references/*.md、README.md、*.yaml、*.yml
- **§0.8 重写**：从"Read+检查行号+offset续读"改为"优先 exec 完整加载"+"仅 >25K 文件回退 Read+offset"
- **§0.9 重写**：路由前文件完整性验证适配新方法
- **Think §3.1.6 ③ 更新**：管道前置校验升级为全量 Get-Content 验证
- **Reflect 检查更新**：行号追溯检查替换为 Get-Content 加载完整性检查
- **证据**：6-10项目测试 42 次 run 全部命中 Read 截断，最大仅返回 2,416 字符
- **exec stdout 上限**：~30,000 字符，所有 SKILL.md（最大 17K）和 YAML 文件均可完整读取

## v1.0.0 (2026-06-04)

- **首次发布**：V1 写作专家元 Skill
- **两步判断规则**：范围判断（创作/非创作）→ 意图路由（新建/继续/修改/质检/调研），Agent 一条链决策
- **修改路由（三层联动）**：
  - 定位修改层（bootstrap / plot / writer / opening-arc / qa）
  - 评估连锁影响（5 种修改类型 × 需联动层映射表）
  - 执行修改（最小影响原则，从上层到下层逐层更新）
- **完成后引导**：基于项目文件状态（非记忆）的跨轮引导。每轮产出后先问修改 + 建议下一步
- **10 个推荐 Skill + 4 个延伸 Skill**：覆盖完整网文创作管线
- **输出规范**：中文写作、不暴露内部 Skill 名称、必须追引导、非创作请求不强行关联

> 配套 PRD：`06_专家模式PRD_v1.md` | 架构文档：[06_专家模式PRD_v1 — 飞书](https://www.feishu.cn/docx/ImVQdtzSloSsbdxJsMAcwHCIn6c)
