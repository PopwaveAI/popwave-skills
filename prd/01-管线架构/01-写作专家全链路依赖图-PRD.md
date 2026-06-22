# 写作专家全链路依赖图 — 文件依赖与产出全景

> 版本：v7.0 | 2026-06-23
> 说明：本文档覆盖写作专家（pop-writer-*）全链路。基于各 skill 当前 skill.json 版本构建。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`。
> **v7.0 迭代**：pop-state-engine v0.1.0 已实现并接入 6 个 skill（prose/chapter/plot/world/reservoir + expert-writer）；管线顺序图新增引擎层；新增第五节"pop-state-engine 引擎层"（从预告转为已实现，含调用机制+CLI 触发点+数据流）；更新全部版本号；附录 A 文件树新增 `data/` 目录；总控进度锚点数据源从 entity-snapshot.yaml 切换为引擎 project-status 命令。

## 写作专家管线顺序（硬性）

```
                                    ┌─────────────────────────────────┐
                                    │   pop-state-engine v0.1.0       │
                                    │   (SQLite 状态引擎，贯穿全程)     │
                                    └──────┬──┬──┬──┬──┬──┬───────────┘
                                           │  │  │  │  │  │
creative → reservoir → world → character → plot → chapter → prose → qa
   ↑          ↑         ↑         ↑         ↑        ↑       ↑      ↑
pop-writer pop-writer pop-writer pop-writer pop-writer pop-writer pop-writer
-creative  -reservoir -world    -character -plot     -chapter  -prose   -qa
  v4.4.0    v3.4.0    v2.1.0    v2.0.3     v8.1.0    v2.5.0    v3.7.0   v1.0.1
```

**引擎接入点**（↓ = 写入引擎，↑ = 从引擎读取）：
- world Phase 1d ↓ `add-node` + `set-fact` + `store-summary`（L1 设定入库）
- plot Step 1 ↓ `create-arc` + `store-summary`（卷弧线）；Step 3 ↓ `plant-hook` + `add-edge`（伏笔+咬合）
- chapter Step 1 ↑ `for-creation`（上下文组装，替代全量加载）
- prose 章末 ↓ `store-chapter` + `add-node` + `set-fact` + `resolve-hook`（5步登记）
- reservoir ↓ `add-node` + `set-fact`（储备卡注册）
- expert-writer step-3 ↑ `project-status`（总控进度锚点聚合）

**辅助skill（独立调起，不改变主线进度）：**
- `pop-writer-game` v2.0.2 — 文游化
- `pop-writer-html` v1.3.2 — HTML发布

**写作专家消费的拆书专家产出：**
- `pop-decon` 系列 → 拆解数据入库 pop-trope-library → creative、world 以 library 注入方式消费
- `pop-shared-dna` v4.0.3 → 文风DNA档案 → prose-render 消费
- `tool-download-webnovel` → {书名}.txt → deconstructor 消费

---

## 一、管线文件接口

> S = 静态（一次产出）/ D = 动态（持续维护）

### 创意环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| creative v4.4.0 | 用户 + library + WebSearch | `全书立项PRD.md` | S | reservoir, world, character, plot | 唯一立项宪法（10块） |
| reservoir v3.4.0 | PRD + 外部素材 | `素材储备池/{素材}.md`（剧情储备卡/设定储备卡） + ↓引擎 add-node/set-fact | D | world, plot | 剧情储备卡（元卖点+冲突引擎+剧情线发展链条8~20节点）；设定储备卡（设定内核+可衍生冲突空间，标注对应L1维度）；储备卡实体注册到引擎 |

### 小说设定环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| world v2.1.0 ① L1设定 | PRD + 素材储备池 + library | `小说世界设定/L1-01~07.md` + ↓引擎 add-node/set-fact/store-summary | S | character, plot | 世界蓝图/力量/历史驱力/物种/势力/资源/术语文明底色；Phase 1d 将主要实体和世界规则入库引擎 |
| world ② 数值+升级表 | PRD宪法 + L1力量体系 | `小说世界设定/数值体系/*.md` `动态升级表.md` | S | character, plot | 战斗数值 + 每卷力量膨胀曲线 |
| world ③ 起终点快照 | PRD + L1 + 数值体系 | `小说世界设定/起点快照.md` `终点快照.md` | S | character, plot | 卷1初态 + 卷N终态 |
| world（library获取） | pop-trope-library | `文风库/{书名}.md` → fallback `文风DNA/{书名}.md` | S | prose | 文风DNA档案 |
| character v2.0.3 | PRD + L1 + 数值 + 快照 + library | `状态/角色/{主角,配角}-角色卡.md` | D | plot, chapter | 主角与主要配角设定卡 |

### 剧情设计环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| plot v8.1.0 Step 0 设计意图 | PRD + 角色卡 + 项目总控 | 用户设计意图模型（内存） | — | plot Step1 | L1大类确认（世界大事件/主角成长/主角行动）+ 卷节奏+爽点优先级+角色弧线 |
| plot Step 1 卷战略 | `step-1-volume-strategy.md` + `volume-outline.md` | `剧情设计/卷/卷{N}-卷纲.md` + ↓引擎 create-arc/store-summary | S | plot Step2 | 卷定位+起终点+爽点设计+篇幅预算+线数预算；卷弧线入库引擎 |
| plot Step 2 候选线产出 | `step-2-seed-pull.md` + 储备池 + library | `卷/卷{N}-卷纲.md`（追加） | D | plot Step3 | 候选线雏形≥卷纲预算数量（储备池+库不够自己生成） |
| plot Step 3 剧情线成文 | `step-3-plotline-docs.md` + `plotline-doc.md` | `剧情设计/剧情线/{主线,支线,设定线}-{编号}-{名称}.md` + 回填卷纲剧情线总览 + ↓引擎 plant-hook/add-edge | S/D | chapter | L1/L2/L3三层结构；剧情发展骨架（主线≥12节点/支线≥5节点/设定线≥3节点）；伏笔种入引擎+线间咬合关系入库 |
| plot Step 4 分幕 | `step-4-act-plan.md` + `act-outline.md` + 全部剧情线 | `剧情设计/幕/vol-XX/act-YY.md` | S/D | chapter | 幕定位+活跃线+篇幅预算 |
| plot Step 5 章锚点+Canvas | `step-5-chapter-anchors.md` + 剧情线债务 | `幕/vol-XX/act-YY.md`（追加） | D | chapter | 章锚点+Canvas矩阵+叙事债务追踪 |
| plot Step 6 Canvas验核 | `step-6-canvas-audit.md` + `references/prd-payoff-audit.md` | `幕/vol-XX/act-YY.md`（追加验核报告） | D | chapter | 爽点密度+大爽点间隔+承诺兑现+线间平衡+债务回收 |

### 正文产出环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| chapter v2.5.0 | act-YY + 剧情线 + ↑引擎 for-creation（fallback: entity-snapshot） | `章节设计包/chXXX-设计包.md` + entity-snapshot更新 + act-YY枪链更新 | D | prose | 回合级事件骨架（含剧情推进点≥3/章，推进≥3条不同L2）；Step 1 优先从引擎获取上下文包（~5-8KB），引擎为空时退回全量加载 |
| prose v3.7.0 | 设计包 + 文风DNA | `正文/chXXX.md` + ↓引擎 store-chapter/add-node/set-fact/resolve-hook + 总控更新 | D | qa | 正文渲染 + 章末5步引擎登记（设计包入库→实体标注→提取验证→写入实体和状态→伏笔回收检测） |
| qa v1.0.1 | 正文 + 设计包 + act-YY | （不留盘） | — | — | L1硬门禁→L2三层介入→L3原文对照 |

---

## 二、辅助 Skill — 独立调起

| Skill | 入 | 出 | → |
|:---|---:|---:|:---|
| game v2.0.2 | 世界观 + 人设 + 剧情设定 | AI 互动文字游戏 | — |
| html v1.3.2 | 正文/设定/场景卡 | 单文件 HTML 发布页 | — |

---

## 三、pop-trope-library 公共知识库集成

> `pop-trope-library` 不是 skill，是公共知识库。当前本地存储，未来云端化。
> **拆书专家（pop-decon-* / pop-shared-*）产出先入库（按五库文件分类），写作专家（pop-writer-*）各环节按需查询消费。**
> 查询协议详见 `skills/pop-trope-library/references/调用匹配SOP.md`（分模块查询：立项库/设定库/文风库/剧情库/套路库）。

### 五库结构

| 模块 | 内容 | 服务本环节 | 入库来源 |
|:-----|:-----|:---------|:---------|
| `立项库/` | PRD 级经验：立项模式/元爽点组合/题材焊接/加工哲学/失败案例 | creative | 拆书 Phase 4 trace + 写书复盘 |
| `设定库/` | **按书整包**的 L1 设定：PRD.md + L1-01~07 + 世界宪法 + 角色与关系 | reservoir, world, character | 拆书 Phase 3 setting |
| `文风库/` | 文风笔触档案（场景卡+通用维度+时间演变），**canonical 路径** | prose | pop-shared-dna |
| `剧情库/` | **标准剧情线**（六段格式），按内容标签分目录 | plot | 拆书 Phase 2 volume |
| `套路库/` | 抽象叙事模式卡（10字段：模式家族+变体+跨书案例） | creative, plot, chapter, qa | 原始素材晋升 |
| `文风DNA/` | 历史兼容路径（fallback） | prose | pop-shared-dna（兼容） |

> **路径约定**：`文风库/` = canonical 主路径；`文风DNA/` = fallback 兼容路径。prose 先查 `文风库/`，不存在时降级到 `文风DNA/`。

### 各管线环节查询矩阵

> 每个环节路由到子 skill 前，expert-writer 应确认子 skill 会查询对应模块。
> 查询方法：按 `调用匹配SOP.md` 分模块查询（立项库/设定库/文风库/剧情库/套路库各走各的查询键）。

| 管线阶段 | 查询模块 | 查什么 | 用途 |
|:---------|:---------|:-------|:-----|
| creative | `立项库/00-索引.md` + `套路库/00-总索引.md` + `references/元爽点-变体映射表.md` | 立项经验 + 元爽点匹配 | 确定本书书型 + 2-3个主元爽点 |
| reservoir | `设定库/`（先查 PRD 卖点→读书级 L1）+ `套路库/` | 跨域设定素材源 + 冲突公式/原型/套路 | 剧情储备卡的素材注入 |
| world | `设定库/{书名}/`（先查 00-索引→读 PRD→读 L1） | 力量体系/制度/数值/命名创意池 | L1 设定+数值体系的创意参考 |
| character | `设定库/{书名}/` + `设定库/角色与关系/` | 角色身份张力/关系结构/说话风格 | 角色卡设计的文化质感和关系模式参考 |
| plot | `剧情库/{标签}/` + `套路库/` + `references/元爽点-变体映射表.md` | 标准剧情线 + 套路链配套 | 卷战略/剧情线/分幕的剧情参考 |
| chapter | `套路库/{具体套路名}.md` | 套路公式+节奏控制 | 章设计包的事件链设计 |
| prose | `文风库/{书名}.md` → fallback `文风DNA/{书名}.md` | 风格渲染场景卡（按 scene 匹配） | 正文渲染的文风锚定 |
| qa | `套路库/{具体套路名}.md` 使用红线段 | L3 原文对照 | 质检时对照套路使用红线 |

### 查询纪律

1. **先查库再创作** — 每个环节进入子 skill 后，先查 trope-library 对应模块，再开始创作
2. **库缺时声明** — 查询无匹配素材时标注"本赛道/元爽点库缺"，降级到通用素材，不静默跳过
3. **查到的是参考不是模板** — trope-library 提供创意参考和套路公式，不直接复制，需根据本书 PRD 改写转化
4. **入库与消费分离** — 拆书管线产出先入库 pop-trope-library（按五库文件分类），写作管线从 library 按协议消费。两条线不交叉。写作管线不直接从拆书项目目录读取文件

---

## 四、项目级知识库路径约定

> 在项目总控模板中固化的 `📚 知识库路径` 区块。解决 agent 找不到 library 路径的反复询问问题。
> 执行者：expert-writer v4.6.0+ 的 `step-0-init.md` 3a。

### 4.1 两类路径声明

项目总控头顶一个固定区块，记录两类知识来源的绝对路径：

| 类型 | 用途 | 初始化行为 | 后续维护 |
|:-----|:-----|:----------|:---------|
| **skill 公共库** | pop-trope-library 本地安装目录（设定库/剧情库/套路库/文风库） | step-0-init 自动解析绝对路径 + 扫描设定库书目 | 公共库迁移时手动更新路径 |
| **用户私藏参考** | 原书拆解数据、wiki骨架、文风DNA等 — 精度更高的原文分析 | 初始留空（`❌待补充`），不猜测 | 用户主动填入或 Agent 追问后填入 |

### 4.2 公共库内容速览

初始化时自动扫描 `{pop-trope-library}/设定库/` 下所有子目录，列出书名。如本书是对标/移植某已有书目，标注 ★。

Agent 进入 reservoir/world/plot 阶段时，从此表直接定位对标书的完整设定包，不再询问 "library 在哪"。

### 4.3 Agent 使用规则（硬约定）

1. **首次加载总控时**，检查知识库路径是否已填写 → 未填写则提示用户补充
2. **reservoir / world / plot 阶段启动前**，必须先确认公共库路径可用（文件系统存在）
3. **用户私藏参考路径 ≠ 空时**，优先消费私藏数据（精度更高）；skill 公共库作为 fallback
4. **路径写入后**，Agent 不再询问「library 在哪」——直接读

### 4.4 与 pop-trope-library 查询矩阵的关系

本区块是 **"去哪找"**（路径元数据），三的查询矩阵是 **"找什么"**（内容路由）。两者互补：
- Agent 启动 → 读总控 → 拿到路径 → 按查询矩阵路由 → 读对应模块
- 路径缺失时阻塞查询矩阵，路径就位后查询矩阵可正常运转

### 4.5 落地文件

此约定落地于 `项目总控.md`（模板源头：`expert-writer/references/project/master-control.tpl.md`），非独立文件。

---

## 五、pop-state-engine 引擎层（v0.1.0 已实现）

> **状态：已实现并接入 6 个 skill。** 详见 `skills/pop-state-engine/SKILL.md`。
> 引擎是 SQLite 驱动的运行时状态引擎，贯穿写作管线全程，解决设定全量加载、涌现实体无处登记、身份与状态混合三个结构性问题。

### 5.1 调用机制

引擎不是 skill，不被 expert-writer 路由调度。它是**基础设施层**，由各 skill 在特定步骤中通过 CLI 调用：

```
expert-writer（调度器）
    │
    ├── step-0-init → 创建项目目录骨架（不含引擎初始化）
    ├── step-1-think → 路由到子 skill
    ├── step-2-execute → 子 skill 执行（子 skill 内部调用引擎 CLI）
    └── step-3-reflect → ↑引擎 project-status（总控进度锚点）
```

**引擎 CLI 调用方式**（所有 skill 统一）：
```bash
python {engine_scripts}/command_executor.py -p {项目路径} -a {动作} -j '{JSON参数}'
```

`{engine_scripts}` = `skills/pop-state-engine/scripts/`

**引擎初始化时机**：world skill 的 Phase 1d（L1 设定产出后）。step-0-init 不初始化引擎——因为 creative 阶段还没有任何叙事数据需要存储。world Phase 1d 是第一个有实体和世界规则需要入库的环节。

### 5.2 各 skill 的引擎触发点

| skill | 步骤 | 方向 | CLI 命令 | 触发条件 | 说明 |
|:------|:-----|:-----|:---------|:---------|:-----|
| world | Phase 1d | ↓ | `add-node` × N + `set-fact` × N + `store-summary` | L1 六篇全部产出后 | 主要实体注册到知识图谱；permanent 级世界规则写入事实表；book 级摘要入库。此后 L1 文档不再每章加载 |
| plot | Step 1 | ↓ | `create-arc` + `store-summary` | 卷纲落盘后 | 创建卷弧线（arc_type=volume）；存储卷级摘要 |
| plot | Step 3 | ↓ | `plant-hook` + `add-edge` | 每条剧情线落盘后 | 种埋叙事债务（契诃夫枪）；注册剧情线间咬合关系 |
| chapter | Step 1 | ↑ | `for-creation` | 每章设计开始时 | 引擎返回 ~5-8KB 上下文包（book→volume→arc 摘要+活跃实体+事实+伏笔+连续性笔记），替代全量加载 act-YY + entity-snapshot |
| prose | 章末 | ↓ | `store-chapter` → `extract-entities` → `add-node` + `set-fact` → `list-hooks` / `resolve-hook` | 正文写入 chXXX.md 后 | 5 步登记：设计包入库→agent标注新实体→脚本辅助验证→写入实体和状态变化→伏笔回收检测 |
| reservoir | 产出后 | ↓ | `add-node` + `set-fact` | 每张储备卡落盘后 | 储备卡实体注册（properties 标注 source）；permanent 级设定规则写入 |
| expert-writer | step-3 | ↑ | `project-status` | 每次 skill 执行后 | 聚合查询返回总章数/当前弧线/下一章/主角状态/关键伏笔，写入总控进度锚点段 |

### 5.3 数据流全景

```
                    ┌─────────── pop-state-engine (SQLite) ───────────┐
                    │                                                  │
                    │  pop_scenes_content ← store-chapter (prose)      │
                    │  pop_scenes (FTS5) ← 自动同步                     │
                    │  pop_summaries ← store-summary (world/plot)      │
                    │  pop_facts ← set-fact (world/plot/prose/res)     │
                    │  pop_kg_nodes ← add-node (world/plot/prose/res)  │
                    │  pop_kg_edges ← add-edge (plot)                  │
                    │  pop_hooks ← plant-hook (plot) / resolve (prose) │
                    │  pop_arcs ← create-arc (plot)                    │
                    │                                                  │
                    │  for-creation → chapter (读)                     │
                    │  project-status → expert-writer (读)             │
                    │  catalog / dump-dashboard → 诊断 (读)            │
                    └──────────────────────────────────────────────────┘
```

### 5.4 核心变化（引入前后对比）

| 维度 | 引入前 | 引入后 |
|:-----|:-------|:-------|
| 设定加载 | chapter 每章全量加载 L1-01~07.md（~100-200KB） | 不加载，建世界时已入库 SQLite，`for-creation` 按需返回 ~5-8KB |
| 实体状态 | `entity-snapshot.yaml` 全量读写（随章数线性膨胀） | 双写过渡期并行；最终退役 yaml，身份→kg_nodes（永久），状态→facts表（带版本链） |
| 涌现实体 | 无处可去 | prose 章末 5 步登记自动入库 |
| 伏笔追踪 | plot 枪链表 + act-YY 追踪 | hook_tracker 引擎（种埋/回收/超期检测），plot 仍维护枪链表（双写） |
| 上下文组装 | chapter Step 1 手动拼凑 | `for-creation` CLI 返回预算内上下文包 |
| 数据可发现性 | 无 | `catalog` 自描述（9表+可查维度+快捷查询）+ `dump-dashboard` HTML 仪表盘（知识图谱+伏笔+时间线可视化） |
| 总控进度锚点 | step-3 读 entity-snapshot.yaml 提取 | step-3 调用 `project-status` 聚合查询，yaml 作为 fallback |
| FTS5 搜索 | 无 | bigram 双字分词 + AND 匹配 ≈ 子串匹配，零依赖高精度 |

### 5.5 总控文件与引擎的关系

`项目总控.md` 不被引擎替代。总控 10 个区段中：

| 区段 | 数据源 | 引擎是否参与 |
|:-----|:-------|:-------------|
| 📚 知识库路径 | 手动填写 + 文件系统扫描 | ❌ |
| 📊 首屏仪表盘 | 文件系统扫描 | ❌ |
| 📈 项目统计 | 文件系统扫描 + **引擎 project-status** | ⚠️ 部分 |
| 实际阶段执行 | 文件系统扫描 | ❌ |
| 产出物清单 | 文件系统扫描 | ❌ |
| 目录结构 | 文件系统扫描 | ❌ |
| **当前进度锚点** | **引擎 project-status**（fallback: entity-snapshot.yaml） | **✅ 核心数据** |
| ⚠️ 待处理/风险 | 手动 | ❌ |
| 🗺️ 所属管线 | 静态参考 | ❌ |
| 执行顺序日志 | step-3-reflect 追加 | ❌ |

引擎只提供数据（`project-status` 只读聚合），expert-writer step-3-reflect 负责写入总控。职责分离：引擎管数据（SQLite），expert-writer 管文档（Markdown）。

### 5.6 双写双读过渡策略

每个 skill 接入引擎时保持 entity-snapshot.yaml 和引擎并行：

1. **双写期**：prose 章末既跑引擎 CLI，chapter step-4 仍更新 entity-snapshot.yaml
2. **双读期**：chapter Step 1 优先查引擎，引擎为空时 fallback 到 yaml
3. **退役期**：确认引擎数据稳定后，停止 yaml 维护（计划在 prose v3.8.0 + chapter v2.6.0）

当前状态：双写期。entity-snapshot.yaml 仍是 canon，引擎是补充。

### 5.7 引擎不做什么

- 不写正文（prose 的职责）
- 不做角色建模 / 质量审计 / 连续性检查 / 风格学习 / 情节分支（OnKos 的 5 个流程层模块未迁移）
- 不写总控文件（expert-writer step-3-reflect 的职责）
- 不创建项目目录结构（expert-writer step-0-init 的职责）
- 不替代 pop-trope-library（引擎管本项目运行时状态，library 管跨项目知识库）

---

## 附录 A：写作项目文件全貌

```text
{项目名}/
│
├── 全书立项PRD.md                      [creative] 唯一立项宪法（10块结构）
│
├── 素材储备池/                          [reservoir] 每素材独立.md（剧情储备卡/设定储备卡）
│   └── 素材储备池.md                   [reservoir] 索引页
│
├── 小说世界设定/                        [world]
│   ├── L1-01世界蓝图.md
│   ├── L1-02力量体系.md
│   ├── L1-03历史驱力.md
│   ├── L1-04物种天赋.md
│   ├── L1-05势力格局.md
│   ├── L1-06资源物品.md
│   ├── L1-07术语文明底色.md
│   ├── 起点快照.md
│   ├── 终点快照.md
│   ├── 动态升级表.md
│   └── 数值体系/
│       ├── combat_capability.md
│       ├── rank_schedule.md
│       ├── monster_map.md
│       └── collision.md
│
├── 状态/
│   ├── 角色/{主角}-角色卡.md            [character]
│   ├── 角色/{配角}-角色卡.md
│   └── entity-snapshot.yaml            [chapter 每章更新] ← 双写过渡期保留，引擎稳定后退役
│
├── 剧情设计/                            [plot]
│   ├── 卷/
│   │   └── 卷{N}-卷纲.md               [plot Step1~3 渐进填充：战略→候选线→剧情线总览]
│   ├── 剧情线/
│   │   ├── 主线-{编号}-{名称}.md        [plot Step3] L1大类下L2，≥12节点
│   │   ├── 支线-{编号}-{名称}.md        [plot Step3] 无L1，≥5节点
│   │   └── 设定线-{编号}-{名称}.md      [plot Step3] ≥3递送节点
│   └── 幕/vol-XX/
│       └── act-YY.md                    [plot Step4~6 渐进填充：分幕→章锚点+Canvas→验核报告]
│
├── 章节设计包/                          [chapter]
│   └── chXXX-设计包.md
│
├── 正文/                                [prose]
│   └── chXXX.md
│
├── 写作资产/
│   └── 文风DNA/{书名}.md                [world 从 library 获取]
│
├── data/                                [pop-state-engine v0.1.0]
│   ├── novel_memory.db                  [SQLite 状态引擎数据库（9张pop_前缀表）]
│   └── project_config.json              [引擎配置（title/genre/author/engine_version）]
│
└── 项目总控.md                          [expert-writer step-3 每次skill执行后更新；进度锚点数据源=引擎project-status]
```

---

> 本文档基于各 skill 当前 skill.json 版本构建（2026-06-23）。
> 写作专家 skill 清单：expert-writer(v4.8.0)、pop-writer-creative(v4.4.0)、pop-writer-reservoir(v3.4.0)、pop-writer-world(v2.1.0)、
> pop-writer-character(v2.0.3)、pop-writer-plot(v8.1.0)、pop-writer-chapter(v2.5.0)、pop-writer-prose(v3.7.0)、pop-writer-qa(v1.0.1)、
> pop-writer-game(v2.0.2)、pop-writer-html(v1.3.2)。
> 引擎：pop-state-engine(v0.1.0) — 基础设施层，非 skill，不被 expert-writer 路由调度，由各 skill 通过 CLI 调用。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`（pop-decon-* / pop-shared-*）。
