# CHANGELOG — 02-pop-novel-deconstructor

## v20.2.0 | 2026-07-22

### 按规范重写 SKILL.md

- 按pop-shared-skill-create v6.1.0规范重写SKILL.md
- 新增frontmatter（name+description含触发条件）
- 新增"做什么"输入/输出/下游表
- 新增"怎么操作"section含execution.mode+强弱加载声明
- 红线#1改为读取协议（Get-Content -Encoding UTF8 -Raw，禁用Read工具）
- 速查表改为全文件目录引导（文件+读取时机+核心内容），补全iceberg-theory+wiki-skeleton
- 版本只留最新一条，其余保留在本文件
- skill.json版本同步至20.2.0，description更新为入口定位
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

## v20.1.0 | 2026-07-20

### 移除pop-trope-library入库，改为沉淀本地文件夹

**根因**：library库已优化掉（不再建立pop-trope-library），decon拆解产出应直接沉淀到项目本地文件夹，而非入库到library库。

**改动**：
- SKILL.md红线6：从"全管线完成不执行入库确认"改为"产出沉淀到项目本地文件夹，不入库pop-trope-library"
- SKILL.md管线地图：从"入库: pop-trope-library 四库"改为"沉淀: 项目本地文件夹（不入库pop-trope-library）"
- step-1-pipeline.md路由建议第5条：从"入库确认"改为"沉淀确认"
- step-1-pipeline.md入库确认章节：改为"沉淀到项目本地文件夹"，沉淀路径从`剧情库/{标签}/`改为`项目本地/剧情库/{标签}/`，删除入库速查引用，完成提示语改为"产出已沉淀到项目本地文件夹"
- step-1-pipeline.md管线完成确认：从"入库状态"改为"沉淀状态"

## v20.0.0 | 2026-07-18

### Phase 3 以"服务续写/同人"为原目的重构

- Phase 3 从平面 11 step 重构为四层：设定层/角色层/势力层/叙事资产层
- 新增 3 个续写/同人专用产出物：伏笔追踪表、对白风格库、经典场景拆解
- 世界宪法→世界观弹性边界（从"叙事规律"改为"哪些能改不能改"）
- 起点快照/combat_capability 降为可选
- L1-04 人物动机→人物卡，L1-05 冲突表→伏笔追踪（消除重叠）

## v19.0.0 | 2026-07-18

### 管线地图更新：金手指+人物卡+立项设计

- Phase 3 新增 `L1-07-金手指设计` + `主要角色人物卡`（含敌人卡）
- Phase 4 从"全书立项PRD"升级为"全书立项设计"（含商业分析+连载规划+风险预警+启动检查清单）

## v18.0.0 | 2026-07-06

### 改为初始化+一次性路由入口

- SKILL.md 从 orchestrator 瘦身为初始化入口；红线增至 7 条（含"不当常驻调度""无源文件先下载"）
- step-1-pipeline.md 从 142 行调度 SOP 改为初始化（源文件检查+量级+语言）+ 一次性路由建议
- skill.json expert 从 pop-novel 改为 pop-decon（拆书专家独立）
- agents/openai.yaml 新建，含拆书专家 PE system_prompt
- 管线地图增加 tool-download-webnovel 作为第一步

## v17.0.0 | 2026-07-01

### 按v6.0.0规范重构SKILL.md

- SKILL.md 从358行精简到59行（≤60行规范）。frontmatter从7行精简到2行（只保留name+description）。
- 红线从9条精简到4条（≤7条规范），第一条改为读取协议。
- 新增强弱加载保障声明。
- 速查表从量级路由改为全文件目录引导（11个文件）。
- 操作细节下沉：新建 `steps/step-1-pipeline.md`（管线完整操作步骤）、`references/iceberg-theory.md`（冰山理论）、`references/naming-normalization.md`（命名归一化）、`references/format-consistency-audit.md`（跨卷格式审计）。
- skill.json downstream 补充缺失的 pop-decon-prd。

---

## v16.0.0 | 2026-07-01

### 删除Phase 4创意溯源 + L2+L3双轨改为L2卡+卷纲双轨

- 删除 pop-decon-trace，Phase 5 PRD 重编号为 Phase 4。管线从 5 Phase 缩减为 4 Phase。
- Phase 2 从"L2单元卡+L3剧情线+L4全书事件"改为"L2单元卡+卷纲（含溯源燃料台）"。
- 入库从"L2+L3双轨"改为"L2卡+卷纲双轨"。
- 冰山理论中"Phase 4创意溯源"改为"溯源燃料台（Phase 2卷纲级）"。

---

## v11.0 | 2026-06-14

### 完整重构 —— 一级原则：写作端是甲方

**核心变化**：拆书端的产出格式完全对齐写作端（`.md` 对 `.md`，`.yaml` 对 `.yaml`）。产出镜像项目目录树，和 `pipeline-arch.md` 定义的规范结构完全相同。

### 三级分级体系

| 级别 | 范围 | 耗时 | 产出文件数 |
|:---|:-----|:----|:---------|
| Lv1 快速扫描 | 前20章精读 + 目录跳读 | ~25min | 6个文件（故事引擎+力量体系+角色卡+起/终点快照+拆解摘要） |
| Lv2 标准模板 | 前100章全读 | ~1-3h | ~20个文件（六件套完整+数值体系+全书架构+卷+幕+角色卡） |
| Lv3 工厂级 | 全书 + 03-pop-dna | ~3-8h | ~50+文件（Lv2全部 + 正文分章 + 设计包 + entity-snapshot） |

### 模板系统对齐写作端

14 个模板文件（`templates/*.tpl.md/.yaml`），全部从写作端对应模板克隆：

```
story-engine.tpl.md          → creative phase-0.pe.md 故事引擎.md 5区段模板
L1-01~06.tpl.md              → world phase-1.pe.md 六件套格式
character-lv4.tpl.md         → character-schema Lv4 模板（9节16维）
character-lv3.tpl.md         → character-schema Lv3 模板（6节）
volume-design.tpl.md         → plot templates/volume-design.md
act-skeleton.tpl.yaml        → plot templates/act-skeleton.yaml
combat-capability.tpl.yaml   → world phases/phase-5.pe.md
design-pack.tpl.md           → chapter-design templates/fact-skeleton.md
starting-snapshot.tpl.md     → world phases/phase-6.pe.md
```

### 产出路径对齐项目目录树

- 产出路径从 `_template_library/{skill分类}/` 改为直接镜像 `{项目根}/` 子目录
- 文件名不加 `-template` 后缀——和项目文件同名、同格式、同路径
- Lv3 产出可以直接 cp 到新项目根目录→创作端直接消费

### 相位文件重组

9 个相位文件替代旧的 4 个：

```
phase-s.lv1.pe.md            Lv1 快速扫描
phase-0.sampling.pe.md       Phase 0 分层扫描
phase-1.diagnosis.pe.md      Phase 1 自诊断
phase-2.1.engine.pe.md       Lv2 故事引擎模板
phase-2.2.world.pe.md        Lv2 世界构筑模板
phase-2.3.plot.pe.md         Lv2 剧情架构模板
phase-2.4.characters.pe.md   Lv2 角色卡模板
phase-3.lv3-full.pe.md       Lv3 工厂级深度
phase-4.validate.pe.md       Phase 4 验证+打包
```

### 清理

- 旧文件归档到 `_archive/`：`templates-old/`（T1-T7）、`templates-lv1-old/`、`fragment-pipeline/`
- 旧 `_template_library/` 归档

---

## v10.0.0 | 2026-06-14

- 模板工厂模式。Phase 2 从不带路由的子Skill改为带路由的子Skill再改为不带路由的相位文件（同天迭代3次）

## v9.0.0 | 2026-06-12

- 新增 Phase S 快速拆解（Lv1）
