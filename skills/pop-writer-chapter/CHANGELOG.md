# CHANGELOG — 09-pop-novel-chapter-design

## v2.4.0 (2026-06-23)

### 剧情推进点概念 + L2 关联门禁

**问题**：chapter 只有"事件"概念，没有"剧情推进点"概念。事件可以是过渡/铺垫/氛围渲染（不推进任何线），也可以是推进点（对应某条 L2 骨架节点变动）。没有门禁检查"每章至少推进几条 L2"，导致章节可能在所有剧情线上"空转"。

**改动**：
- `steps/step-2-event-chain.md`：事件表新增"剧情推进点"字段（是/否）；新增定义"事件 ≠ 剧情推进点"；新增设计规则"每章至少推进3条不同L2"；新增2条门禁（剧情推进点<3退回、推进L2不足3条退回）
- `templates/baseline.tpl.md`：预期字数从2500改为2000~3000

---
## v2.3.0 — 2026-06-22

### 全量对齐 plot v7.6 + PRD v5.3 + entity-snapshot 归属 chapter

**路径全局替换**：全部文件从旧目录规范（`00-总控/`、`设计/卷/volume-XX.md`、`设计/幕/act-XX.yaml`、`写作资产/设计包/`）迁移到当前 PRD v5.3 规范（`状态/`、`剧情设计/卷/卷{N}-卷纲.md`、`剧情设计/幕/vol-XX/act-YY.md`、`章节设计包/`）。

**entity-snapshot 所有权明确**：chapter 创建（CH1 初始化）并每章更新 entity-snapshot，prose 仅读取。删除了与 prose `first-chapter-init.md` 的冲突路径。

**SKILL.md 瘦身**：195 行 → 120 行。删除内联设计包模板（107 行），前置阻断检查压缩为红线表，# 引用 `templates/fact-skeleton.md`。

**references 全量更新**：4 个参考文件（character/location/info/emotional）路径对齐 + 移除过时的 yaml 字段引用。continuous-chapter-workflow 重写。

**新增**：Step1/Step2 读什么补 `pop-trope-library/套路库/{套路名}.md`（PRD 查询矩阵要求）。Step3 chekhov-tracker → act-YY.md 枪链段。

**版本**：frontmatter v2.1.0 / 标题 v2.0.0 / skill.json v1.5.0 / CHANGELOG v1.6.0 → 统一 v2.2.0。

---

## v1.6.0 — 2026-06-15

### entity-snapshot 创建时机修复（CH1 首次运行专用）

- **step-1-read-canvas.md 前置条件重构**：将 entity-snapshot.yaml 从硬性前置条件改为「已存在→正常读取 / 不存在→初始化创建」的分支逻辑
  - 新增「★ entity-snapshot 初始化分支」章节，含完整的初始化 SOP（从 volume-XX.md 角色池 + 角色卡提取初始状态 → 组装初始 yaml → 写入 00-总控/）
  - 初始化操作为一次性动作（CH1 触发），后续章节走正常读取路径
  - 设计依据说明：Step 1 必须读到 entity-snapshot 才能设计事件链，但 Step 3 才写入第一次更新——CH1 必须在这里初始化
- **step-3-output.md 更新**：增加 CH1 特殊情况说明——Step 1 已创建骨架，Step 3 填入 after 状态即可
  - timeline 字段追加说明（追加本章时间节点而非覆盖）
- **expert-writer/references/pipeline-check.md**：新增第⑤项——当路由目标为 chapter-design 时，输出 entity-snapshot 存在性检查提示
- **skill_view 截断排查结论**：L1-06.tpl.md 等文件的 skill_view 返回与 read_file 对比验证，结果为正常。210 bytes = 98 chars（UTF-8 中文 3字节/字），文件完整无截断。为误报。

### 输入精简 + 路径对齐 PRD v1.4

- **constitution.yaml 移除**：Canvas 字段（combat.scale/payoff/chekhov_set）已隐含所有约束，不再单独读取
- **info-release-XX.md 移除**：info-release 已内嵌于 act-XX.yaml#info_release_plan，step-1 从每章 chapters[].info_release 直接取
- **新增输入：状态/角色/{主角}-角色卡.md**：step-1 前置条件新增，提取 core_desire
- **追溯引用全部更新**：act-XX-人物.md / act-XX-地图.md → volume-XX.md#角色池 / volume-XX.md#地点池
- **路径重构**：03-写作资产→写作资产/设计包、03-正文→正文
- **references/character-scheduling.md + location-orchestration.md**：追溯引用同步更新

### 中爽点事件级标记（★ 爽点体系对齐）

- **step-2-event-chain.md**：逐事件设计新增「中爽点标记」字段 — 读者读完认知有没有变化？有变化 → ★中爽点事件。整章累计 ≥ 1
- **step-3-output.md**：自检新增「中爽点事件 ≥ 1」检查项
- **fact-skeleton.md**：爽点等级注释补充责任说明：大/终极由 plot 指定，中爽点逐事件标记。交叉引用 payoff-guide.md
- **中爽点定义基准** → `08-pop-novel-plot/references/payoff-design-guide.md`

## v1.4.0 — 2026-06-10

### 步骤结构重构：7步→3步 + 4个references

- **步骤数从7步压缩为3步**：
  - 旧：Step 1 读入 → Step 2 事件链 → Step 3 角色 → Step 4 空间 → Step 5 信息 → Step 6 情绪 → Step 7 产出
  - 新：Step 1 读入 → Step 2 事件链（★核心，同步完成角色/空间/信息/情绪） → Step 3 产出
- **Step 1 重写**：对齐 plot skill v4.1+ 的 14 个必读字段
  - 新增 `reader_emotion_path` / `chekhov_set` / `chekhov_fire` — 之前缺失
  - 新增场景规格字段：combat/dialogue/discovery/crisis — 按场景类型条件读取
  - payoff 确认仍然是最新的章级字段（payoff.type/trigger/reader_feeling）
- **steps/3/4/5/6 → references/**：降级为 Step 2 消费的参考文档
  - character-scheduling.md / location-orchestration.md / info-release.md / emotional-beats.md
  - 每个 reference 文件开头声明"此文件不独立执行，Agent 在 Step 2 逐事件设计时参考"
- **SKILL.md 完全重写**：目录结构、错误示例（5条）、引用关系图同步更新

## v1.3.0 — 2026-06-10

### 事件定义清晰化 + 硬性下限回归

- **事件定义明确为「一个回合 = 一个事件」**："一刀一事件；一轮信息交换一事件；一次发现一事件"
  - 给出正例和反例的对照说明
  - 战斗/对话/探索/过渡四种场景各有明确粒度
- **硬性下限回归**：`Design 事件数 ≥ 章预期字数 ÷ 200`
  - 2500字章 ≥ 12 事件，低于此值是设计缺陷
  - 多线场景额外加法（双线+4/三线+6）
- **情绪目标重新定位**：从"Design 自检指标"改为"给 Render 的创作靶心"
  - Design 提供足够数量的有情绪靶心的事件 → Render 才有材料激发读者情绪波动
  - 以前用 ÷300 校验情绪密度（上限检查），现在用 ÷200 约束事件数量（下限硬性）。两处都留，职责不同
- **战斗章事件链示例重写**：科尔帮据点暗杀，19 事件对照，每事件 100-120 字
- **红线新增**："战斗事件写成模糊概括"和"事件写成 Render 微节拍"两条退回规则

## v1.2.0 — 2026-06-10

### 事件密度从「定数字」改为「情绪密度校验」

- **核心理念变更**：不再用固定事件数（如"战斗章15-20"）约束 Design，改为「情绪密度校验」
  - 情绪节点 ≥ 章字数 ÷ 300（来源：番茄编辑"300字一个爽点"）
  - 悬念/钩子节点 ≥ 章字数 ÷ 500（"500字一个钩子"）
  - 章末事件必须是钩子（"一章一个悬念"）
- **Design 事件 vs Render 微节拍分离**：Design 管故事节拍（"发生了什么、为什么"），Render 管渲染节拍（"怎么写、什么质感"）
  - Design 事件粒度：每事件 ~100-250 字渲染量，描述结果而非具体写法
  - Render 在此范围内自主拆 3-5 个微节拍
- **事件数据验证**：逆向拆解《深渊主宰》第16章——61个Render微节拍⇒15个Design事件，验证了双层架构
- **场景复杂度对事件数的影响**：
  - 单线叙事 基线×1.0-1.3 / 双线×1.3-1.6 / 多线×1.6-2.5
- **事实骨架模板自检重构**：分为情绪密度校验、结构完整性、Design事件质量三层
- **红线新增**：情绪密度达标检查

## v1.1.0 — 2026-06-10

### 事件密度大幅提升 + 跨章弧线

- **事件密度基线**：从 3-5 事件/章 → 8-20 事件/章。粒度标准：每事件 150-400 字渲染量
  - 战斗章 12-20 / 对话章 8-14 / 探索章 10-16 / 过渡章 6-10 / 混合章 14-20
  - 基线公式：章预期字数 ÷ 200 ≈ 基准事件数
- **新增跨章剧情弧线识别**：Design agent 自动检测一个剧情弧线是否跨越多章
  - 标注 `arc_span: [N, M]` + 本章位置 + 情绪分工
  - 决战/高潮自动拆为上中下或①②③
  - 整条弧线的事件链统一设计后按章切分
- **事实骨架模板新增跨章弧线字段**：arc_span / 本章位置 / 弧内总事件数 / 本章切出范围 / 情绪分工
- **红线新增**：战斗章 ≤ 8 事件退回、跨章弧线未标注退回、跨章弧线的章末不是情绪止点警告

## v1.0.0 — 2026-06-09

### 初始版本：从 pop-novel-writer 拆出 Design 层

- **核心定位**：导演卡阶段——只做结构设计，不碰文风
- **输入**：Canvas（act-XX.yaml + 人物 + 地图 + 势力 + info-release + 里程碑）+ entity-snapshot
- **产出**：事实骨架.md + 登场人物卡.md + entity-snapshot 更新
- **7 步流程**：读入 Context → 事件链 → 角色调度 → 空间编排 → 信息释放 → 情绪节拍 → 产出
- **与 writer 的根本差异**：不知道文风DNA存在，不被风格规则约束设计决策
- **子 agent 架构**：由 expert-writer 派子 agent 独立执行
