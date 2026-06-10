# CHANGELOG — pop-novel-plot

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
- **name/directory 字段对齐**：`name: plot-architecture`→`pop-novel-plot`，`directory: skill-plot-architecture`→`pop-novel-plot`
- **路径引用修复**：`glue/check_db.py`→`scripts/check_db.py`、`glue/validate.py`→`scripts/validate.py`、`skills/_shared/`→`skills/pop-novel-master/_shared/`
- **书数据污染清理**：`沈渊降临渊界，激活铭牌`→`主角穿越异界，激活金手指`
- **旧 skill 名修复**：`emergent-writer`→`pop-novel-writer`、`skill-plot-architecture`→`pop-novel-plot`

## v2.7.0 (2026-06-03)
- 从 novel-agent-pro/skills/skill-plot-architecture 独立提升
- 修复路径引用（glue/ → scripts/，_shared/ → pop-novel-master/_shared/）
