# 写作专家全链路依赖图 — 文件依赖与产出全景

> 版本：v11.1 | 2026-06-24
> 说明：本文档覆盖写作专家（pop-writer-*）全链路。基于各 skill 当前 skill.json 版本构建。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`。
> **v11.1 迭代**：creative+reservoir 合并。creative v6.0.0 吸收 reservoir v3.3.0 全部能力（素材储备池产出+储备池确认闸门+研究档案/）。管线顺序去 reservoir，creative 成为立项+素材储备统一入口。
> **v11.0 迭代**：L0-L5 深度结构对齐。plot v9.0.0：新建 L4 全书事件模板（跨卷大事件）；L3 剧情线重构（L3-ID/parent_saga/组成单元/物理坐标/骨架承载单元）；L2 幕纲重构为剧情单元卡（结构分析 7 阶段+情绪弧线+主题表达+嵌套子线+单元边界信号，保留 Canvas/章锚点执行调度层）；引入 L4/L3/L2 强 ID 系统和双向链接；卷纲去 L4 标签改为每卷战略文档；模板重命名对齐拆书管线。chapter v2.7.0：消费侧同步更新。
> **v10.1 迭代**：叙事结构层级对齐。plot 内部 L1/L2/L3 分类去 L 化（主线大类/具体剧情线/剧情节点）。产出文档加 L4/L3/L2 层级标注。新增"叙事结构层级术语映射表"。与拆书管线 L0-L5 对齐。
> **v10.0 迭代**：state.yaml + state-history → state-log.yaml（append-only 叙事日志）。核心变化：①单文件 append-only 日志替代 state.yaml + state-history 目录；②prose 成为 state-log 唯一写入者（章末追加 event）；③chapter 不再写状态文件，只读 log 取 before 状态；④expert-writer 定期压缩（baseline+event 合并）；⑤回滚 = 删 entries（零脚本）。涉及 skill：chapter v2.6.0、plot v8.2.0、prose v3.8.0、expert-writer v4.9.0。

## 写作专家管线顺序（硬性）

```
creative → world → character → plot → chapter → prose → qa
   ↑         ↑         ↑         ↑        ↑       ↑      ↑
pop-writer pop-writer pop-writer pop-writer pop-writer pop-writer pop-writer
-creative  -world    -character -plot     -chapter  -prose   -qa
  v6.0.0    v2.0.1    v2.0.3     v9.0.0    v2.7.0    v3.8.0   v1.0.1
```

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
| creative v6.0.0 | 用户 + library + WebSearch | `全书立项PRD.md` + `素材储备池/{素材}.md`（剧情储备卡/设定储备卡） | S/D | world, character, plot | 唯一立项宪法（10块）；剧情储备卡（元卖点+冲突引擎+剧情线发展链条8~20节点）；设定储备卡（设定内核+可衍生冲突空间，标注对应L1维度）；闸门：储备池确认 |

### 小说设定环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| world v2.0.1 ① L1设定 | PRD + 素材储备池 + library | `小说世界设定/L1-01~07.md` | S | character, plot | 世界蓝图/力量/历史驱力/物种/势力/资源/术语文明底色 |
| world ② 数值+升级表 | PRD宪法 + L1力量体系 | `小说世界设定/数值体系/*.md` `动态升级表.md` | S | character, plot | 战斗数值 + 每卷力量膨胀曲线 |
| world ③ 起终点快照 | PRD + L1 + 数值体系 | `小说世界设定/起点快照.md` `终点快照.md` | S | character, plot | 卷1初态 + 卷N终态 |
| world（library获取） | pop-trope-library | `文风库/{书名}.md` → fallback `文风DNA/{书名}.md` | S | prose | 文风DNA档案 |
| character v2.0.3 | PRD + L1 + 数值 + 快照 + library | `状态/角色/{主角,配角}-角色卡.md` | D | plot, chapter | 主角与主要配角设定卡 |

### 剧情设计环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| plot v9.0.0 Step 0 设计意图 | PRD + 角色卡 + 项目总控 | 用户设计意图模型（内存）+ L4全书事件识别 | — | plot Step1 | 主线大类确认（世界大事件/主角成长/主角行动）+ 卷节奏+爽点优先级+角色弧线+跨卷大事件识别 |
| plot Step 1 卷战略+L4 | `step-1-volume-strategy.md` + `volume-outline.md` + `L4-全书事件.tpl.md` | `剧情设计/卷/L4-{编号}-{事件名}.md` + `剧情设计/卷/卷{N}-卷纲.md` | S | plot Step2 | L4全书事件规划（演化阶段）+卷定位+起终点+爽点设计+篇幅预算+线数预算 |
| plot Step 2 候选线产出 | `step-2-seed-pull.md` + 储备池 + library | `卷/卷{N}-卷纲.md`（追加） | D | plot Step3 | 候选线雏形≥卷纲预算数量（储备池+库不够自己生成） |
| plot Step 3 剧情线成文 | `step-3-plotline-docs.md` + `L3-剧情线.tpl.md` | `剧情设计/剧情线/L3-{编号}-{名称}.md` + 回填L4组成线 + 回填卷纲剧情线总览 + `状态/state-log.yaml`（baseline #0） | S/D | chapter | L3-ID/parent_saga/物理坐标/骨架承载单元；剧情发展骨架；创建 state-log baseline #0（弧线+伏笔+世界状态） |
| plot Step 4 分幕+结构分析 | `step-4-act-plan.md` + `L2-剧情单元卡.tpl.md` + 全部剧情线 | `剧情设计/幕/vol-XX/L2-{编号}-{单元名}.md` + 回填L3组成单元 | S/D | chapter | L2-ID/所属线/结构分析(7阶段+情绪弧线+主题表达+嵌套子线+单元边界信号)+活跃线+篇幅预算 |
| plot Step 5 章锚点+Canvas | `step-5-chapter-anchors.md` + 剧情线债务 | `幕/vol-XX/L2-{编号}-{单元名}.md`（追加） | D | chapter | 章锚点+Canvas矩阵+叙事债务追踪 |
| plot Step 6 Canvas验核 | `step-6-canvas-audit.md` + `references/prd-payoff-audit.md` | `幕/vol-XX/L2-{编号}-{单元名}.md`（追加验核报告） | D | chapter | 爽点密度+大爽点间隔+承诺兑现+线间平衡+债务回收 |

### 正文产出环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| chapter v2.7.0 | L2单元卡 L2-{编号} + L3剧情线 + state-log.yaml | `章节设计包/chXXX-设计包.md` **(L1)** | D | prose | 回合级事件骨架；CH1补充state-log baseline #0角色状态；不写state-log（prose负责） |
| prose v3.8.0 | 设计包 + 文风DNA | `正文/chXXX.md` + `状态/state-log.yaml`（追加event） + 总控更新 | D | qa | 正文渲染；章末追加event到state-log（事件+变化+伏笔），成为state-log唯一写入者 |
| qa v1.0.1 | 正文 + 设计包 + L2-{编号} | （不留盘） | — | — | L1硬门禁→L2三层介入→L3原文对照 |

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
| `设定库/` | **按书整包**的 L1 设定：PRD.md + L1-01~07 + 世界宪法 + 角色与关系 | creative, world, character | 拆书 Phase 3 setting |
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
| creative | `立项库/00-索引.md` + `套路库/00-总索引.md` + `references/元爽点-变体映射表.md` + `设定库/`（先查 PRD 卖点→读书级 L1） | 立项经验 + 元爽点匹配 + 跨域设定素材源 + 冲突公式/原型/套路 | 确定本书书型 + 2-3个主元爽点 + 剧情储备卡的素材注入 |
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

Agent 进入 creative/world/plot 阶段时，从此表直接定位对标书的完整设定包，不再询问 "library 在哪"。

### 4.3 Agent 使用规则（硬约定）

1. **首次加载总控时**，检查知识库路径是否已填写 → 未填写则提示用户补充
2. **creative / world / plot 阶段启动前**，必须先确认公共库路径可用（文件系统存在）
3. **用户私藏参考路径 ≠ 空时**，优先消费私藏数据（精度更高）；skill 公共库作为 fallback
4. **路径写入后**，Agent 不再询问「library 在哪」——直接读

### 4.4 与 pop-trope-library 查询矩阵的关系

本区块是 **"去哪找"**（路径元数据），三的查询矩阵是 **"找什么"**（内容路由）。两者互补：
- Agent 启动 → 读总控 → 拿到路径 → 按查询矩阵路由 → 读对应模块
- 路径缺失时阻塞查询矩阵，路径就位后查询矩阵可正常运转

### 4.5 落地文件

此约定落地于 `项目总控.md`（模板源头：`expert-writer/references/project/master-control.tpl.md`），非独立文件。

---

## 五、状态管理：state-log.yaml（append-only 叙事日志）

> **状态：已实现。** 单文件 append-only 日志，替代旧 entity-snapshot.yaml / state.yaml + state-history。零脚本，纯 YAML。

### 5.1 文件结构

```
状态/
├── state-log.yaml              ← 唯一的状态文件（append-only 日志）
│                                 entries 数组：baseline（全量快照）+ event（每章变化）
└── 角色/                       ← 角色卡（永久身份，不动）
    ├── {主角}-角色卡.md
    └── {配角}-角色卡.md
```

### 5.2 日志结构

两种条目类型：
- **baseline**：全量快照（弧线+角色+伏笔+世界状态），~30-50 行。plot 创建 #0，expert-writer 定期压缩产出新的
- **event**：每章变化（事件+变化+伏笔），~5-10 行。prose 章末追加

agent 读 = 最后一条 baseline + 它之后的 event（~100-200 行，一目了然）
agent 写 = 追加一条 event（只写变化，不写全量）

### 5.3 谁读谁写

| skill | 步骤 | 操作 |
|-------|------|------|
| plot | Step 3 | 创建 state-log.yaml（baseline #0：弧线+伏笔+世界状态，角色待 CH1 补充） |
| chapter | CH1 Step 1 | 读 baseline #0 → 补充角色卡初始状态到 baseline #0 |
| chapter | Step 1 | 读 state-log（最后 baseline + event）→ 取 before 状态 + open 伏笔 |
| chapter | Step 4 | 不写 state-log（只写设计包 + 伏笔预判） |
| prose | 章末 | 追加 event 到 state-log（事件+变化+伏笔）—— **唯一写入者** |
| expert-writer | step-3 | 读 state-log（进度锚点）+ 压缩检查（每 20 章） |
| expert-writer | step-3.3 | 回滚 = 删 entries 中 chapter > N 的条目 |

### 5.4 压缩机制（expert-writer step-3 触发）

每 20 章 event 累积后：
1. 读最后一个 baseline + 之后全部 event
2. 合并成新 baseline（角色变化、伏笔状态、世界状态全部体现在叙事中）
3. 删掉旧 baseline 及其后的 event
4. 追加新 baseline + 更新 last_compacted_at

压缩后文件回到 ~5-10KB，不随章数膨胀。

### 5.5 回滚（零脚本，纯文本操作）

| 场景 | 操作 |
|------|------|
| 回滚到第 N 章 | 删 entries 中 chapter > N 的条目 |
| 回滚到 plot 完成 | 删 entries 中 chapter > 0 的条目（只留 baseline #0） |
| 回滚到 world | 删 state-log.yaml 文件 |
| 回滚到 creative | 删 状态/ 整个目录 |

### 5.6 对比历次方案

| 维度 | entity-snapshot.yaml | state.yaml + history | state-log.yaml |
|------|---------------------|---------------------|----------------|
| 文件数 | 1（膨胀） | 1 + N 个 history | 1（稳定） |
| 写的方式 | 全量覆盖 | 覆盖 + 复制 | 追加 |
| 读的方式 | 读全量 YAML 字段 | 读 YAML 字段 | 读叙事（agent 最自然） |
| schema | YAML 字段 | YAML 字段 | 无（叙事表达） |
| 回滚 | ❌ 无历史 | Copy-Item 快照 | 删 entries |
| 膨胀 | 线性膨胀 | state.yaml 稳定 + history 膨胀 | 压缩后稳定 |
| agent 友好度 | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 5.7 pop-state-engine（搁置）

SQLite 引擎方案搁置。state-log.yaml 以零脚本方式解决了全部痛点。

---

## 六、叙事结构层级术语映射表

> 写作管线与拆书管线共享 L0-L5 叙事结构层级。本表明确两侧产出的对应关系，消除术语歧义。

### 6.1 L0-L5 层级映射

| 层级 | 写作侧产出 | 拆书侧提取 | 关系 |
|:-----|:-----------|:-----------|:-----|
| L0 事件 | chapter 设计包内的回合级事件 | design-pack 逐章拆解的最小事件 | 同维度 — 写作正向设计，拆书逆向提取 |
| L1 章节设计包 | chapter 产出的 `chXXX-设计包.md`（1章=2k~3k字=12~15个L0事件） | design-pack 产出的 `chXXX-设计包.md` | 同格式 — 写作和拆书共享设计包结构 |
| L2 剧情单元卡 | plot Step4~6 产出的 `L2-{编号}-{单元名}.md`（结构分析层+执行调度层双层架构） | volume 产出的 L2单元卡（可迁移部分） | 超集关系 — 写作L2单元卡是拆书单元卡的前向设计扩展 |
| L3 剧情线 | plot Step3 产出的 `剧情线/L3-{编号}-*.md` | volume 产出的 L3剧情线卡（六段格式） | 同维度 — 写作正向设计，拆书逆向提取 |
| L4 全书事件 | plot Step1 产出的 `L4-{编号}-{事件名}.md` | volume 产出的 L4全书事件卡 | 同维度 — 写作正向规划，拆书逆向提取。卷纲=每卷战略文档（非L层级，引用L4） |
| L5 书PRD | creative 产出的 `全书立项PRD.md` | prd 产出的 `全书立项PRD.md` | 同格式 — 写作正向立项，拆书逆向破解 |

### 6.2 plot 内部分类声明

> plot skill 内部的"主线大类/具体剧情线/剧情节点"是剧情分类概念（主线大类=世界大事件/主角成长/主角行动，全书固定；具体剧情线=每卷动态激活2-3条；剧情节点=剧情线内的发展节点），**不使用 L 标记**，与上述 L0-L5 叙事结构是不同维度。

### 6.3 world L1 澄清

> world skill 产出的 L1-01~07 是设定六件套的编号（L1-01 世界蓝图、L1-02 力量体系、... L1-07 术语与文明底色），与叙事结构 L0-L5 中的 L1（章节设计包）是不同维度。world SKILL.md 已内置术语澄清段落。

---

## 附录 A：写作项目文件全貌

```text
{项目名}/
│
├── 全书立项PRD.md                      [creative] 唯一立项宪法（10块结构）
│
├── 素材储备池/                          [creative] 每素材独立.md（剧情储备卡/设定储备卡）
│   └── 素材储备池.md                   [creative] 索引页
│
├── 研究档案/                            [creative] 种子展开法深度调研产出
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
├── 状态/                                [chapter 读 / prose 写 / expert-writer 压缩]
│   ├── state-log.yaml                  [append-only 叙事日志：baseline（全量快照）+ event（每章变化）]
│   └── 角色/                           [character 产出，永久身份]
│       ├── {主角}-角色卡.md
│       └── {配角}-角色卡.md
│
├── 剧情设计/                            [plot]
│   ├── 卷/                              [L4 全书事件 + 每卷战略]
│   │   ├── L4-{编号}-{事件名}.md        [plot Step1] 跨卷大事件规划
│   │   └── 卷{N}-卷纲.md               [plot Step1~3 渐进填充：战略→候选线→剧情线总览]
│   ├── 剧情线/                          [L3 剧情线]
│   │   └── L3-{编号}-{名称}.md          [plot Step3] 具体剧情线，≥12节点
│   └── 幕/vol-XX/                       [L2 剧情单元卡]
│       └── L2-{编号}-{单元名}.md        [plot Step4~6 渐进填充：结构分析→章锚点+Canvas→验核报告]
│
├── 章节设计包/                          [chapter]
│   └── chXXX-设计包.md
│
├── 正文/                                [prose]
│   └── chXXX.md
│
├── 写作资产/
│   └── 文风DNA/                         [world 从 library 获取] {S}
│       └── {书名}.md
│
└── 项目总控.md                          [prose 每章渲染后更新]
```

---

> 本文档基于各 skill 当前 skill.json 版本构建（2026-06-24）。
> 写作专家 skill 清单：expert-writer(v4.9.0)、pop-writer-creative(v6.0.0)、pop-writer-world(v2.0.1)、
> pop-writer-character(v2.0.3)、pop-writer-plot(v9.0.0)、pop-writer-chapter(v2.7.0)、pop-writer-prose(v3.8.0)、pop-writer-qa(v1.0.1)、
> pop-writer-game(v2.0.2)、pop-writer-html(v1.3.2)。
> 状态管理：state-log.yaml（append-only 叙事日志，零脚本，prose 唯一写入者）。
> pop-state-engine：方案搁置，代码保留为可选诊断工具。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`（pop-decon-* / pop-shared-*）。
