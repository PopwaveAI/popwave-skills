# CHANGELOG — 08-pop-novel-plot

## v7.9.0 — 2026-06-22

### 补线型职责和每卷线数建议

**问题**：剧情线设计仍缺少“主线/支线/设定线到底怎么区分”和“每卷该设计多少条线”的硬规则，导致 agent 容易把支线写成主线、把设定线漏掉，或一次性设计太多线让 Canvas 过载。

**改动**：
- `templates/volume-outline.md`：新增「剧情线配置建议」「线型职责判定」「本卷线数决策」，按短卷/标准卷/长卷给出建议线数。
- `templates/plotline-doc.md`：新增「线型判定」，用删除测试区分主线、支线、设定线。
- `steps/step-1/2/3/4`：新增线数配置、候选线预算、主线数量、支线职责、设定线事件化、幕内活跃线过载门禁。
- `SKILL.md`：同步 Step1/4 门禁，要求线数配置和幕内线数控制。

**效果**：剧情线从“能写”进一步变成“知道写几条、每条干什么、什么时候该合并/降级/升级”。

---
## v7.8.0 — 2026-06-22

### 剧情线模板从登记表升级为设计闭环

**问题**：剧情线模板虽然补了线型、地点、叙事债务，但整体仍偏“登记表”，缺少真正驱动剧情线成立的设计判断：为什么好看、如何持续升级、读者为什么追、和其他线怎么咬合、如何交给 Canvas 调度。

**改动**：
- `templates/plotline-doc.md`：新增「一句话剧情线」「读者追问」「冲突引擎」「剧情发展骨架」「角色变化」「与其他线的咬合」「Canvas 投放合同」「质量自检」。
- `steps/step-3-plotline-docs.md`：从七件套改为“剧情线设计闭环”，新增追问、冲突引擎、发展骨架、线间咬合、Canvas 投放合同门禁。
- `templates/volume-outline.md` 与 `steps/step-2-seed-pull.md`：候选线雏形补充读者主追问和建议咬合线，避免 Step3 输入太薄。
- `steps/step-5-chapter-anchors.md` 与 `templates/act-outline.md`：Canvas 设计必须对照剧情线的投放合同和线间咬合。

**效果**：剧情线不再只是字段集合，而是能从候选种子发展成“可追问、可升级、可咬合、可调度”的剧情发展线。

---
## v7.7.0 — 2026-06-22

### 补回设定/背景线 + 契诃夫枪升级为叙事债务

**问题**：剧情线体系只强调主线/支线，漏掉设定/背景线；同时把“契诃夫枪链”当成总概念，容易让 agent 只追道具伏笔，忽略信息差、制度、地点规则、人物选择、设定递送等更常见的叙事债务。

**改动**：
- `templates/plotline-doc.md`：线型补 `设定线/背景线`；新增「线型功能」；把「契诃夫枪链」改为「叙事债务与回收链」。
- `templates/volume-outline.md`：候选线型补设定/背景线；候选线雏形支持「递送承诺 / 递送机制 / 理解收益」。
- `templates/act-outline.md`：Canvas 增加设定线列；枪链追踪改为叙事债务追踪。
- `steps/step-3/5/6` 与 `SKILL.md`：同步“叙事债务”为总概念，契诃夫枪仅作为道具型债务。`steps/step-6-chekhov.md` 更名为 `steps/step-6-canvas-audit.md`。

**效果**：剧情线可以正式承担世界观、历史背景、势力逻辑、社会常识的穿插递送；Canvas 追踪的是所有必须兑现的叙事承诺，而不是只追“枪”。

---
## v7.6.1 — 2026-06-22

### 剧情线模板补地点与场域

**问题**：剧情线只有时间轴、人物、套路和枪链，缺少地点/场域，后续幕纲与章节设计无法判断冲突发生的物理边界、势力规则和场景功能。

**改动**：
- `templates/plotline-doc.md`：新增「地点与场域」和「地点变化」段。
- `steps/step-3-plotline-docs.md`：Step3 从六件套改为七件套，新增地点与场域要求。
- `SKILL.md`：同步门禁口径，剧情线文档缺七件套退回。

**效果**：剧情线不再只说明“谁在什么时候做什么”，还必须说明“在哪里发生、地点为什么能制造冲突、对幕纲/章节有什么要求”。

---
## v7.6.0 — 2026-06-22

### 剧情线枪链：不指定章号（未分幕）

**问题**：剧情线模板的契诃夫枪链表列了 `vol-XX/act-YY/chXXX`，但 Step 3 产剧情线时还没分幕（分幕是 Step 4），agent 被迫提前编造章号。

**改动**：
- `templates/plotline-doc.md`：契诃夫枪链重写——从「设伏位置/预期回收章号」改为「节点序号+角色（设伏/回收）+事件 brief+卷内故事位置（前/中/后段）+回收方式」。枪点成对（设伏→回收），一对 = 1 个枪。章号由 Step5 Canvas 设计时确定。
- `steps/step-3-plotline-docs.md`：六件套中契诃夫枪链的要求从「设伏位置、预期回收、回收方式」改为「节点事件 brief+卷内位置，不指定章号」
- 版本 7.5.0 → 7.6.0

**效果**：枪链在 Step 3 只定义「有什么枪、在哪段故事里」，不编造章号。Step 5 Canvas 设计时读到枪链，再分配具体回收章。

---

## v7.5.0 — 2026-06-22

### 卷纲+幕纲 新增篇幅预算

**问题**：卷纲和幕纲都缺章节数量约束——plot 设计剧情时可以无限延展，没有「多少章」的硬上限。这导致 Canvas 设计和 chapter 阶段失去结构边界。

**改动**：
- `templates/volume-outline.md`：Step1 战略层新增「篇幅预算」表——本卷预估章数、幕数、各幕章数分配、篇幅约束（每幕 ≥ 8 章、幕间章差 ≤ 1.5×）
- `templates/act-outline.md`：Step4 分幕层新增「篇幅预算」表——本幕章数、占卷比例、各线章数分配、篇幅约束（主线占幕 ≥ 40%）
- `steps/step-1-volume-strategy.md`：做什么新增第 5 条「锁定篇幅预算」
- `steps/step-4-act-plan.md`：做什么新增第 5 条「标注幕篇幅」
- `SKILL.md`：速查表 + 核心流程 Step1/Step4 同步；Step6 引用修正为 Canvas 验核报告
- 版本 7.4.0 → 7.5.0

**效果**：卷纲有「卷 N 计划写 X 章，分 Y 幕」的硬约束，幕纲有「本幕 X 章，占卷 Y%，主线 ≥ 40%」的分配约束。按 ~2.5k 字/章估算。

---

## v7.4.0 — 2026-06-22

### Step6 重构：Canvas 爽点密度验核

**问题**：Step 6 定位为「契诃夫枪链验证」，但枪链只是 Canvas 质量的一个子项。Canvas 真正的质量指标在 `payoff-design-guide.md` 里——中爽点密度（每章 ≥1 中、连续空 ≤3）、大爽点间隔（≤5 章）、特大爽点汇聚（每卷 ≥1）、全书承诺兑现、线间平衡。这些在 Step 5 设计完 Canvas 后没有系统化验核。

**改动**：
- `steps/step-6-chekhov.md` 全量重写：从「契诃夫枪链」→「Canvas 节奏与爽点密度」，六节验核（§一中爽点密度 / §二大爽点间隔 / §三特大汇聚 / §四承诺兑现 / §五线间平衡 / §六枪链子项）。唯一硬阻塞：主线无枪链退回 Step3；其余标 ⚠️ 不阻塞
- `SKILL.md`：速查表 + 核心流程 + 文件索引同步更新
- 版本 7.3.0 → 7.4.0

**效果**：Step 6 从「查枪链有没有回收窗口」变为「Canvas 整体质量验收」——对照 payoff-design-guide 的完整规范逐项打分，枪链降级为 §六 子项。

---

## v7.3.0 — 2026-06-22

### Step5 Canvas 纳入枪链输入 + Step6 退化为纯验证

**问题**：Step 3 剧情线成文时已经产出了每条线的契诃夫枪链，但 Step 5（章锚点与 Canvas）设计 Canvas 时是「盲的」——不读枪链。到了 Step 6，枪链对照 Canvas 发现回收章没有 payoff 容量 → 退回 Step 5 重做，形成无意义的返工循环。

**改动**：
- `steps/step-5-chapter-anchors.md`：读什么明确标注「含每条线的契诃夫枪链」；做什么新增第 6 条——从剧情线提取枪点，为回收章预留 Canvas payoff 容量（≥ 中 payoff、同章 ≤ 2 个枪点、跨度 > 60% 标风险）
- `steps/step-6-chekhov.md`：从「更新 + 阻塞退回」退化为「验证 + 风险标注」——主线无枪链仍退回 Step3，其余枪点问题标 ⚠️ 不阻塞管线
- `SKILL.md`：速查表 + 核心流程同步更新

**效果**：Canvas 设计和枪链部署变成同一屏决策（Step 5），Step 6 变成安全检查而非设计步骤。消除了「盲排 Canvas → 枪链对不上 → 退回重做」的返工回路。

---

## v7.2.0 — 2026-06-22

### 文件收敛：卷纲 / 剧情线 / 幕纲

- **三类文件落盘**：取消单独产出 `卷{N}-战略定位.md`、`卷{N}-剧情种子拉取清单.md`、`分幕规划.md`、`chekhov-tracker.md`；统一收敛为 `卷{N}-卷纲.md`、`剧情线/*.md`、`act-YY.md`
- **卷纲渐进升级**：Step1 创建战略层，Step2 在同一份卷纲中追加剧情卡筛选、卷级特化和候选线雏形
- **幕纲渐进升级**：Step4 创建分幕层，Step5 追加章锚点与 Canvas，Step6 追加契诃夫枪链追踪
- **枪链并入幕纲**：不再独立维护 `chekhov-tracker.md`，避免枪链和 Canvas/payoff 节奏脱节
- **模板收敛**：新增 `templates/volume-outline.md` 与 `templates/act-outline.md`，移除旧拆分模板

---

## v7.1.0 — 2026-06-22

### PRD 对齐：剧情线独立文档 + Canvas 节奏总控并存

- **纠正 Canvas 口径**：Canvas 不废除，定位为剧情密度、每条线按章节奏、payoff 释放与多线汇聚的节奏仪表盘
- **补正 Step2/Step3 边界**：Step2 负责剧情卡筛选与卷级特化，只产出候选线雏形；Step3 才负责主支线剧情线成文
- **SKILL.md 重构**：从 363 行压缩为路由层，按 v6 skill 规范保留定位、红线、速查表、步骤索引、边界条件、落盘检查点
- **流程对齐 PRD**：重构为 6 步：卷战略定位 → 剧情卡筛选与卷级特化 → 主支线剧情线成文 → 分幕规划 → 章锚点与 Canvas → 契诃夫枪链
- **steps 全量替换**：移除旧 `step-0-architecture.md`、`step-1-volume.md`、`step-2-act.md`，新增 `step-1-volume-strategy.md` 到 `step-6-chekhov.md`
- **templates 全量替换**：移除旧 `volume-design.md`、`act-skeleton.md`、`act-skeleton.yaml`、`act-guide.md`、`rhythm-check.md`，新增六个 PRD 对齐模板
- **skill.json 对齐**：版本升至 `7.1.0`，补齐真实上游 `creative/reservoir/world/character/trope-library` 和 PRD 产出路径

---

## v6.3.0 — 2026-06-12

### D 线（设定穿透）落地

- **Canvas 新增 D 线列**：`act-skeleton.yaml` 每章 block 的 canvas 段新增 `D` + `D_load` 字段。D 不设 payoff_level（非叙事弧），D_load=0 无新设定 / 1 适量 / ≥2 过载警告
- **volume-design.md 新增 §五 设定穿透·D 线**：定义 + 填空原则 + 设定披露承诺表（信息项/最晚章节/披露方式/载体）
- **rhythm_check 新增 disclosure 段**：`max_consecutive_zero_load`（默认 2） / `d_load_overage[]` / `per_info_deadlines` deadline 扫描
- **step-2-act.md**：逐章流程第②步改填 D 线；自检新增 D 线三项检查
- **step-1-read-canvas.md**：design agent 必读字段新增 `canvas.D` + `canvas.D_load`

### act-skeleton.yaml 全盘重构（v6.2 → v6.3）

- **Canvas entries 合入 chapters[]**：每章一个自包含 block（Canvas 数据+设计意图），design agent 一次读完。30 章从 ~720 行 → ~440 行（-40%）
- **删 7 段冗余**：`info_release_plan` 独立段 / `goal` / `tone_note` / `payoff_distribution` 独立段 / `emotional_arc` 独立段 / `payoff_map` 独立表 / chapters[] 8 个冗余字段（payoff.type/trigger/reader_feeling/reader_emotion_path/plotlines_active/info_release/characters_active/locations）
- **rhythm_check 提升为顶层段**：`canvas.entries` → 合入 chapters[]，rhythm_check 不再嵌套在 canvas 下
- **step-2-act.md / step-1-read-canvas.md / rhythm-check.md 同步更新**
- **版本号 v6.2 → v6.3**

### 剧情线体系重构（volume-design.md §四）

- **M3 重定义**："外部推进·主角被迫做什么" → "主角行动·主角应对 M1 的行动轨迹"。判定器：不做此行动 M1 会受影响吗？是→M3，否→支线/日常
- **三 M 关系明确化**：M1=被动端（威胁来源）/ M3=主动端（应对行动）/ M2=内部端（成长变化）
- **S 线开放化**：不再预设"羁绊/世界真相"两类——agent 自定名 + 强制说明"为什么需要这条线"。S 数量 = 0~3 条，链条 ≥3 章无线释放 → 追加一条 S
- **字段统一**：所有线用同一个公用字段组（一句话/本卷推进/预期释放节奏/活跃幕段）+ 各线追加特异字段
- **volumes-design.md §四 头注 + 判定器 + 示例** 全量更新
- **step-1-volume.md** 剧情线说明同步更新

## v6.1.0 — 2026-06-11

### 爽点体系标准化（★ v6.1 核心交付）

- **新建 `references/payoff-design-guide.md`**：全链路唯一爽点权威定义。四档定义（微/中/大/终极）+ 每种 4-5 个类型案例 + 设计方法 + 责任归属总表
- **责任归属明确化**：微 → prose-render / 中 → chapter-design 逐事件标记 / 大+终极 → plot 位置规划
- **act-guide.md**：1.3 节改为 plot 责任视角，交叉引用 payoff-design-guide.md
- **act-skeleton.yaml**：payoff_distribution 头部注释标注 plot 负责/不负责范围
- **rhythm-check.md**：头注交叉引用 payoff-design-guide.md 为爽点定义基准
- **SKILL.md**：产出树交叉引用 payoff-design-guide.md

### 文件消减 + info-release 内嵌 + 全书架构（Phase 0 step文件+卷模板+用户确认闸门）

- **新增 Step 0 step 文件**：`steps/step-0-architecture.md` — 全书架构设计完整执行步骤（卷拆分/地理全图/角色出场节奏/主线全览/用户确认闸门）
- **step-1-volume.md**：标为 v6.1，新增 `全书架构.md` 前置条件 + 上游引用
- **volume-design.md 模板**：新增「〇、全书隶属」段，从全书架构提取本卷定位
- **SKILL.md**：版本号 v6.0→v6.1、step 详情表增 Step 0、目录树增 step-0-architecture.md、执行流程增全书架构用户确认闸门
- **act-XX-人物/地图/势力/装备 四个文件彻底移除**：角色追溯→volume-XX.md#角色池，地点→volume-XX.md#地点池，势力→volume-XX.md#势力动机，装备→volume-XX.md#装备路线图
- **info-release-XX.md 合并进 act-XX.yaml#info_release_plan 段**：P0/P1清单 + 密度检查内嵌，不再独立文件
- **新增 Phase 0 全书架构**：产出 `设计/全书架构.md`（消费 story-engine + 快照 + L1 → 全卷蓝图）
- **幕按卷分组**：`设计/幕/vol-XX/act-YY.yaml`，卷内编号，路径即语义
- **constitution 引用移除**：Canvas 字段已全覆盖
- **5 个模板标注废弃**：character-list / map-design / faction-dynamics / equipment-flow / info-release
- **L3-角色层 → 状态/角色**：角色卡路径统一

## v6.0.0 — 2026-06-10

### 卷/幕分层重构 — v5→v6 核心差异

**v5.0 的问题**：卷层包含了版本里程碑、装备路线图、势力动态详情等偏战术的内容。幕层缺少剧情线交叉可视化，节奏检查靠感觉而非数据。

**v6.0 分层哲学**：
- **卷 = 战略** — 目标、背景（时间/地理/角色池/势力动机）、剧情线列表、开局→结束快照
- **幕 = 战术** — Canvas 矩阵（章节×剧情线交叉表）、情绪弧线、爽点分布、每章切片

**具体改动**：

| 改动 | 说明 |
|:-----|:------|
| **新增 Canvas 矩阵** | `act-XX.yaml#canvas` — 章节行 × 剧情线列交叉表，每章每条线填推进摘要 |
| **新增节奏自动检查** | `canvas.rhythm_check` — 每条线的最大连续留白章数、每章活跃线数密度的自动检查和对比 |
| **volume-XX.md 精简为 4 节** | 去掉里程碑/装备路线图/势力动态详情（§五~七）。保留：卷级定义/快照/背景(含势力动机)/剧情线 |
| **新增势力动机** | volume-XX.md §三 新增"本卷势力动机"——势力本卷想什么、动机是什么，而非全量动态表 |
| **step-1-volume.md 重写** | 卷 Canvas 设计 → 卷背景填充，去掉里程碑反推和装备路线图设计步骤 |
| **step-2-act.md 重写** | 新增 Canvas 矩阵填充步骤排在幕级定义之前。自检升级为双轨（Canvas 留白检查 + 常规检查）|
| **质量红线新增** | Canvas 矩阵填充检查 + 剧情线留白自检 |
| **产出目录更新** | volume-XX.md 描述改为"卷级战略"，act-XX.yaml 改为"Canvas 矩阵 + 章级切片 + 节奏检查"|
| **附录更新** | 标注里程碑/装备路线图/势力动态为"v6.0 删除"|

**旧文件处置**：
- volume-XX.md §五 里程碑 → ❌ 删除（幕级 Canvas 矩阵替代）
- volume-XX.md §六 势力动态 → ✅ 简化为势力动机（§三）
- volume-XX.md §七 装备路线图 → ❌ 删除
- act-XX-装备.md → ❌ 删除（归入 act-XX.yaml 场景规格选填字段）
- 里程碑设计.md → ❌ 删除

**版本**：5.0.0 → 6.0.0

## v5.0.0 — 2026-06-10

### 卷/幕分离重构 — 产出物从11个精简到3个

**核心问题解决**：卷和幕的信息冗余混在一起，下游不知道读哪个文件。

**方案**：
- 新增 `设计/卷/volume-XX.md` — 单文件包含全卷 Canvas（人物/地图/剧情线/版本/里程碑/势力/装备）
- `act-XX.yaml` 精简为只含幕级定义和章级切片（去掉 act_end_state / equipment_flow / plotlines — 这些移至 volume-XX.md）
- info-release-XX.md 保留（幕级，下游消费）

**流程精简**：12步→6步
- 第一阶段卷设计（Step 1-3）：卷级定义 → 产出 volume-XX.md → 用户确认闸门
- 第二阶段幕纲编排（Step 4-6）：每幕 info-release → act-XX.yaml → 自检

**废弃的产出文件**（不再产生，数据已合并入 volume-XX.md）：
- 节点B-XX.md（删除）
- 情节线草案-XX.md（合并入卷设计§四）
- act-XX-人物.md（合并入卷设计§三）
- act-XX-地图.md（合并入卷设计§三）
- act-XX-势力.md（合并入卷设计§六）
- act-XX-装备.md（合并入卷设计§七）
- 里程碑设计.md（合并入卷设计§五）
- 节奏自检报告.md（删除）
- 情节线纲汇总表.md（删除）
- 场景卡试读（可选）

**模板清理**：
- 新增: volume-design.md（卷设计模板）
- 保留: act-skeleton.yaml / act-guide.md / info-release.md / rhythm-check.md
- 废弃（已合并，不再维护）: checkpoint-b.md / character-list.md / map-design.md / faction-dynamics.md / equipment-flow.md / milestone-design.md / plotline-draft.md

**下游影响**：chapter-design 只需要读 2 个文件：
- `设计/卷/volume-XX.md` — 人物/地图/剧情线
- `设计/幕/act-XX.yaml` — 当前幕的章级切片

## v4.3.0 — 2026-06-09

### 有向图规范（act-guide.md）

从 6-9 测试暴露的三个问题（卷末阶位不一致/装备数值在段位范围外/跨文件值冲突）入手，根因诊断：项目文件是平面目录而非有向无环图。任意两个文件定义了同一概念的值时，Agent 各自独立填写，无一致性约束。

**修复**：
- **§1.5 新增：产出文件有向图规范** — 七个 Canvas 文件头部必须含 `@consumed_by` 和 `@source` 声明。不声明 `@source` 就填的数值 = 游离数据，冲突风险不可控。
- **§4.4 act_end_state 新增 @source 列** — `protagonist.level` 必须从 `act_rank_schedule.yaml` 取值。每个 act_end_state 子字段都有明确的 @source 标注。
- **§9 产出自检新增"值一致性"段** — 5 条跨文件校验规则（段位对齐/装备数值范围/BOSS掉落段位/情节线等级/势力卷末动态）。
- **§6 combat 规格强化** — `capability_ref` 和 `monster_ref` 增加"填写前必须先读 combat_capability/monster_rank_map 确认数值范围"约束。

### 原理

项目文件构成有向无环图：
```
L1 → canvas(人物/地图/势力/装备/info-release) → 情节线草案 → act-XX.yaml → writer
```
每个节点的值必须声明来源（@source），冲突在 act-XX.yaml 的产出自检中被捕获。

## v4.1.0 — 2026-06-08

### 架构重构：SKILL.md 拆分为 steps/ + templates/

- **SKILL.md 精简为路由层**（437行→147行）：只保留质量红线、执行顺序、步骤索引、错误示例
- **拆分 12 个 steps/ 子文件**：每个 Step 独立维护详细执行指令
- **新增 10 个 templates/ 模板文件**：提升产出物格式统一性和质量
- **Step 3-c 新增「本卷人物设计」**：产出 `act-XX-人物.md`（P0强制）
  - 主角卷初/卷末状态对照、盟友/对手角色卡、出场节奏图、角色红线
  - 下游消费：pop-novel-writer → chXXX-登场人物卡.md
- **Step 3-d 新增「本卷地图设计」**：产出 `act-XX-地图.md`（P0强制）
  - 空间总览、关键地点清单、移动线路、空间情绪对应
  - 下游消费：pop-novel-writer → 正文场景设计
- **Step 3-e 新增「本卷世界设计」**：产出 `act-XX-势力.md` + `act-XX-装备.md`（P1建议）
- **act-XX.yaml 新增三个字段**：
  - `core_conflict` — 幕级核心冲突定义
  - `act_end_state` — 卷末状态预期（主角+世界）
  - `equipment_flow` — 装备/资源变化表
- **act-template.yaml 模板**：完整字段模板，含所有 v4.1 新增字段
- **质量红线新增 2 项**：act-XX-人物.md 和 act-XX-地图.md 必须产出
- **错误示例新增 3 项**：无人物清单/无地图/跳过大纲直写正文

## v4.0.0 — 2026-06-05

### 三层框架整合：新增 info_release 规划系统

- **Step 3 拆分为 Step 3-a + Step 3-b**：新增 L1 设定目录扫描与 info_release 规划
- **Step 3-a 新增**：遍历 L1 设定目录（底层逻辑/表层规则/种族势力/金手指/物品）→ P0/P1/P2 分级 → 分配到各章
- **每章切片新增 info_release 字段**：item_id / title / source_doc / release_method / density / priority / chapter_context
- **Step 5 节奏自检新增「★ 信息释放检查」**：连续无新信息章节 ≤ 2 章、P0 全部分配、第1章新概念 ≤ 2 个、source_doc 标注检查
- **Step 6 产出物更新**：act-XX.yaml 说明新增 info_release 是骨架Agent消费入口
- **异常表 Step 引用更新**：不一致引用修复
- **版本号 3.1.0 → 4.0.0**

## v3.1.0 — 2026-06-05

### 流程新增 Step 2 情节线草案·用户确认闸门
- **核心流程 5步→6步**：节点B和 yaml 填充之间插入情节线设计确认步骤
- **Step 2 内容**：罗列候选线（1主线+1-3支线）→ 设计交叉节奏 → 契诃夫枪备忘 → 风险判断 → 用户/老板确认
- **节点B 第6项从"规划"降级为"预感"**：只靠直觉想几根线，不深入设计（设计交给 Step 2）
- **WRONG 6 新增**：跳过 Step 2 直接填每章字段
- **异常表引用更新**：Step 重编号
- **版本号 3.0.0 → 3.1.0**

## v3.0.0 — 2026-06-05

### 情节线规划系统（罗琳式汇总表 + 契诃夫枪链）

- **节点B 新增第 6 项**：情节线规划——主支线数量、期望频率、契诃夫枪设伏/回收计划
- **act-XX.yaml 模板重大更新**：
  - 顶部新增 `plotlines:` 幕级定义（id/desc/expected_frequency/chekhov_guns）
  - 每章新增 3 个字段：`plotlines_active`（支线推进）、`chekhov_set`（设伏）、`chekhov_fire`（回收）
- **节奏自检新增 3 项**：支线空白检查 / 契诃夫枪延期检查 / 汇总表一致性检查（7+3→7+3+3）
- **Step 5 新增产出**：`情节线纲汇总表.md`（从 yaml 自动渲染的罗琳式表格）
- **质量红线 +1**：plotlines ≥ 2 条，每章 plotlines_active 不为空
- **WRONG 5**：设计幕纲时不规划情节线
- **版本号 2.9.0 → 3.0.0**

## v2.9.0 — 2026-06-04

### 完整改革（SKILL.md 全量重写）

- **frontmatter 精简**：仅保留 name + description（共 3 行），触发条件式描述对齐 skill.json
- **质量红线改为 [ ] checkbox 列表**：从 markdown 表格转为 10 条可勾选清单，附"开工前画 [ ] / 完工后改 [x]" 使用说明
- **新增"什么时候用"第 5 行**：检查现有幕纲节奏问题
- **流程保持 5 步扁平结构**：前置检查→设计幕纲→场景卡闸门→自检+校准→输出
- **新增 WRONG 4 错误示例**：用户一开口直接写多幕
- **新增「异常与边界条件」表**：12 类异常场景（act 文件缺失 / L1 未就绪 / 节点B 跳过 / 场景卡退回 / 自检失败 / 平台校准失败 / Boss 战缺阶段 / 中途换平台 / 场景卡存档冲突 / 多幕命名冲突 / 老板设计缺阶段指示 / 中途换项目），每项含触发条件 + 处理方式
- **版本行格式化为三级标题**：`## 版本 v2.9.0 | 2026-06-04 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)`
- **输出路径不变**：`设计/幕/act-XX.yaml` + `设计/幕/节奏自检报告.md`

### skill.json 同步

- version: 2.8.0 → 2.9.0
- description 对齐 frontmatter 触发条件式

## v2.8.0 (2026-06-03)
- **场景卡改为交互闸门**：不再是产出步骤，改为幕纲设计完成后写1段中爽点试读输出给老板确认
- **SKILL.md 重写"交互闸门·场景卡试读"section**：流程/写哪一段/格式/用途全部更新
- **frontmatter 同步**：produces 从"爽点版场景卡（归档）"改为"场景卡试读（不归档）"，tags 新增"交互闸门"
- **管线图更新**：步骤名由"爽点版场景卡"改为"交互闸门·场景卡试读"

## v2.7.1 (2026-06-03)
- **name/directory 字段对齐**：`name: plot-architecture`→`08-pop-novel-plot`，`directory: skill-plot-architecture`→`08-pop-novel-plot`
- **路径引用修复**：`glue/check_db.py`→`scripts/check_db.py`、`glue/validate.py`→`scripts/validate.py`、`skills/_shared/`→`skills/pop-novel-master/_shared/`
- **书数据污染清理**：`沈渊降临渊界，激活铭牌`→`主角穿越异界，激活金手指`
- **旧 skill 名修复**：`emergent-writer`→`pop-novel-writer`、`skill-plot-architecture`→`08-pop-novel-plot`

## v2.7.0 (2026-06-03)
- 从 novel-agent-pro/skills/skill-plot-architecture 独立提升
- 修复路径引用（glue/ → scripts/，_shared/ → pop-novel-master/_shared/）





