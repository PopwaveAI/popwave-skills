# Skill 分类表

> 依据专家配置图（2026-08-13）整理的 skill 分类索引。图中 5 位专家各自绑定一组 skill；未在图中分配、但属于某专家命名空间家族的 skill 归入「通用·子组件」区，可按需提升到对应专家。

## 一、五大专家 → Skill 对应

| # | 专家 | 消耗 | 说明 | 对应 Skill |
|:--|:--|:--|:--|:--|
| 1 | 番茄长篇网文专家 | 中 | 番茄/七猫等长篇网文创作（完整创作管线：立项→舞台→剧情→正文→审核） | `pop-snow-seed` `pop-snow-stage` `pop-snow-plot` `pop-outline` `pop-write` `pop-snow-review` `pop-snow-pipeline` `pop-snow-research` `pop-dna-style` |
| 2 | 小说推书与IP化专家 | 高 | 网文→漫画/IP 化改编与视觉资产生产（跨平台视觉改编） | `pop-visual-style` `pop-visual-shared` `pop-visual-pipeline` `pop-visual-oc` `pop-visual-cover` `pop-visual-comic` `pop-visual-asset` `pop-comic-content` `pop-visual-art-bible` |
| 3 | 起点长篇网文专家 | 中 | 起点长篇网文创作（测试调整中；写作含 dnlike/海贼王类 流派专属） | `pop-snow-seed` `pop-snow-stage` `pop-snow-plot` `pop-outline` `pop-write` `pop-snow-review` `pop-snow-pipeline` `pop-snow-research` |
| 4 | 网文拆书专家 | 高 | 长篇网文解构/逆向分析（计算密集） | `pop-decon` `pop-decon-dimension` |
| 5 | 短篇小说专家 | 低 | 知乎/豆瓣/每日阅读等短篇创作 | `short-body-generator` `short-idea-refiner` `short-opening-designer` `short-plot-structurer` `short-platform-orientation` `short-reviewer` `short-text-deconstructor` |
| 6 | Mirror 创作专家 | — | 镜界（Mirroric）创作方法论专家系列——**已归档 `temp/`（2026-09-11），方法论由灯塔流系列承接** | （归档）`pop-mirror-pipeline` `pop-mirror-onboard` `pop-mirror-world` `pop-mirror-character` `pop-mirror-opening` `pop-mirror-plot` `pop-mirror-write` `pop-mirror-deai` `pop-mirror-review` → `d:\popwave-skills\temp\` |
| 7 | 灯塔流专家 | 中 | 滚动化长篇规划（只锁灯塔四样、开篇读者验证前置、方向总表每卷一句话、滚动两卷；snow 完全体承接 outline/write/research） | `pop-lantern-pipeline` `pop-lantern-seed` `pop-lantern-world` `pop-lantern-character` `pop-lantern-opening` `pop-lantern-plot` `pop-lantern-review`（复用 `pop-outline` `pop-write` `pop-snow-research`） |
| 8 | 涌现流专家 | 低 | 先写后补试味流（只锁主角立身一句话+文风承诺+模糊灯塔；黄金三章直接写试味；滚动写章循环；阶段性回看；试味成功可转灯塔流稳定长跑） | `pop-emergent-pipeline` `pop-emergent-seed` `pop-emergent-opening` `pop-outline` `pop-write` `pop-emergent-review`（复用 `pop-snow-research`、`pop-write` 脚本） |

> 注（2026-09-11 outline 收敛）：三线 outline（`pop-lantern-outline`/`pop-snow-outline`/`pop-emergent-outline`）同理由收敛为**一份共用中性名 skill `pop-outline`**（蓝本＝灯塔）。线间差异收进其 `§0 系列适配表`（认线／上游输入源／章纲输出路径／配置哪套库／线内纪律：灯塔＝单章自补位｜雪花＝情绪标准先行·无独立套路库｜涌现＝一次排1-3章·舞台只从装配单取·新设定从模板库选）；库并入本包（`references/剧情-情绪打分表.md` 消费副本＋`references/内容库/套路库.md`）。三线 pipeline 依赖、plot/state/research 下游指针同步改指。旧三包删除。
>
> 注（2026-09-11 write 收敛）：三线 write（`pop-lantern-write`/`pop-snow-write`/`pop-emergent-write`）骨架同质、三份副本反复陈旧，收敛为**一份共用中性名 skill `pop-write`**（不带系列中缀，蓝本＝灯塔）。线间差异全部收进其 `§0 系列适配表`（认线／上游输入源／章纲日志路径／文风资源／线内纪律）；文风资源并入 `pop-write/references/`（`夜无疆.md`＋`文风兜底/` 22 赛道档＋辰东写死档）；`word-count.ps1` 随包，去AI味脚本沿用共用宿主 `pop-snow-pipeline/scripts/deai_gate.py`。三线 pipeline 依赖清单、seed/outline 指针同步改指。旧三包删除。
>
> 注（2026-08-31 snow 定名）：统一管线八件定名 snow 家族（雪花流，L0→L1→L2→L3 逐层扩写）——`pop-snow-seed`（四层共创全书大纲）/ `pop-snow-stage`（首喷+卷级刷新）/ `pop-snow-plot`（卷需求brief/卷纲/幕白描）/ `pop-outline`（章纲组装）/ `pop-write`（章纲消费+文风兜底23份）/ `pop-snow-review`（四步审核三范式）/ `pop-snow-pipeline`（phase 链+卷循环 2a-2g）/ `pop-snow-research`（三模式+wiki主源）。test 系列 5 件（adapt/lite/plot/research/write）已删除；旧族 7 件（`pop-fanqie-seed/plot/write`、`pop-qidian-seed/plot/write/research`）同日删除退役（备份 temp/_backup-oldfamily-20260831/）。
>
> 注（2026-08-31 合并史）：world/character 两轮合并落定——先三族各自合并，再按喷漆模型合并为舞台引擎（首喷/卷级刷新双模式），旧 `pop-world` `pop-character` 及三族 world/character 共 8 件废弃删除；review 三族合并为通用四步审核，旧 `pop-qidian-review` `pop-fanqie-review` `test-review` 3 件废弃删除；pipeline 三族合并（统一 phase 链 1→2→卷循环 2a-2g），旧 `pop-qidian-pipeline` `pop-fanqie-pipeline` `test-pipeline` 3 件废弃删除。
>
> 注（2026-08-31 全书大纲架构）：`pop-snow-seed` v3.0.0 重构——立项产出从"六要素PRD"改为与用户共创四层全书大纲（`00-L0核心卖点`/`01-命运图`/`02-命运图plus`/`03-全书大纲`），定全书即宪法；L0 核心卖点从 `卖点引擎库`（wiki.popwave.cn 顶层库）选已验证引擎杂交，过三关后进 L1。下游对齐——`pop-snow-stage` v1.1.0 首喷消费全书大纲，`pop-snow-plot` v2.0.0 在大纲本卷切片批额内展开（新增六问之"大纲批额对齐"防数值失控），`pop-snow-pipeline` v1.1.0 归位/就绪/可调度清单同步改指。
>
> 注（2026-09-11 灯塔流定名）：mirror 系列（pop-mirror-* 9 件）归档 `temp/`；灯塔流建独立系列 `pop-lantern-*`（pipeline/seed/world/character/opening/plot/review），照 snow 工程规范（SKILL.md + skill.json + CHANGELOG.md + templates/references）——只锁方向、滚动细化：方向总表（每卷一句话）为全书唯一半固定卷级规划，卷级硬约束滚动细化该卷时才执行，开篇读者验证前置、先于卷方向；outline/write/research 直接复用 snow（雪花流为完全体），不建双份。
>
> 注（2026-09-11 涌现流定名）：涌现流建独立系列 `pop-emergent-*`（pipeline/seed/opening/outline/write/review 六件），照 snow 工程规范——先写后补试味：只锁主角立身一句话＋文风承诺＋模糊灯塔（结局方向一句话），黄金三章直接写试味（opening 融合写与评），滚动写章循环（轻量章纲→直接写→三源审查回填账本），阶段性回看四问（味道/连续性/灯塔清晰化/转灯塔流）。与灯塔流是两段式不是并列：涌现流负责最快试出味道，试味成功确定写长后转灯塔流（反推方向总表→回填卷1卷纲→设定交接→状态迁移）。research 复用 snow，write 的检查脚本（word-count/deai_gate）复用 snow-pipeline 包。

## 二、共享工具

| Skill | 作用 | 归属专家 |
|:--|:--|:--|
| `tool-download-webnovel` | 网文搜索下载 | 番茄 / 起点 / 拆书共用 |

## 三、通用 Skill（图中未分配）

按命名空间家族分组，建议归入对应专家的子组件：

### 拆书子组件（decon 家族，供「网文拆书专家」调用）
家已精简为 2：`pop-decon`（入口） / `pop-decon-dimension`（单书深度wiki主引擎：L1批次拆解→L2六模块成品）。旧维度/设计包/立项子 skill 已总部内吸合并。

### 视频与物料（推书/IP 化延伸）
`pop-video-brand` `pop-video-comic` `pop-content-card` `pop-comic-test`

### 推书
`pop-recommend`

### 降AI味
`pop-ai-reduce-lite`

### 元能力（skill 开发）
`pop-shared-skill-create`

## 四、命名空间速查

| 前缀 | 家族 | 归属 |
|:--|:--|:--|
| `pop-write` | **正文写作（三线共用·中性名）** | 灯塔/雪花/涌现共用（线间差异见其 §0 系列适配表） |
| `pop-outline` | **章纲（三线共用·中性名）** | 灯塔/雪花/涌现共用（线间差异见其 §0 系列适配表） |
| `pop-snow-*` | 统一写作管线（雪花流） | 番茄/起点专家共用 |
| `pop-lantern-*` | 灯塔流（滚动化规划，只锁方向） | 独立专家家族（复用 snow outline/write/research） |
| `pop-emergent-*` | 涌现流（先写后补试味，设定从账本长出来） | 独立专家家族（复用 snow research/write 脚本；试味成功转灯塔流） |
| `pop-mirror-*` | Mirror 创作专家（镜界/Mirroric 方法论） | 独立专家家族（**已归档 temp/，2026-09-11**） |
| `pop-decon-*` | 网文拆解 | 拆书专家（子组件在通用区） |
| `pop-visual-*` `pop-comic-content` | 视觉/IP | 推书与IP化专家 |
| `short-*` | 短篇 | 短篇专家 |
| `pop-video-*` `pop-content-card` `pop-comic-test` `pop-recommend` | 视频物料/推书 | 通用·视频物料 |
| `pop-ai-reduce-lite` | 降AI味 | 通用 |
| `pop-shared-skill-create` | skill 元能力 | 通用 |
| `tool-*` | 共享工具 | 跨专家共用 |

> `pop-fanqie-*` `pop-qidian-*`（起点/番茄旧族）已随 snow 定名（2026-08-31）删除退役，命名空间不再占用。
