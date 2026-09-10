# CHANGELOG

## v2.0.0 | 2026-09-10

### SOP 迁移：管线全貌-SOP + research 调用

按迁移方案（`新流程探索/sop文档/迁移方案-SOP到mirror系列.md` 3.5/5）更新总控：

- 新增「第 0 节 · 四阶段心智模型」：创意 → 核心设定设计（锁根，近乎不可逆）→ 主线剧情设计（骨架，决定全书形状）→ 逐卷展开（展开）→ 写章期（写章，临场造）；判断标准只问"主路径必踩、牵一发动全身，还是用到才够"；剧情产出顺序为硬约束。
- **保真红线分区**：正文循环区（04 opening/06 write/07 deai/08 review）镜界精华逐字直贴不变；覆盖区（01 onboard/02 world/03 character/05 plot 卷级）以 SOP 为权威，镜界原文降为参考。
- **子专家清单更新**：01/02/03/05 描述与内容权威改为 SOP；05 升级为卷级+章节级两级。
- **research 路由**：路由表新增 pop-snow-research 行（立项调研/设定考据/剧情素材，跨系列只读调用，存档统一 `素材/采风/`）；覆盖区子专家存档前过资料门（资料不够必派 research 补采再存档）。
- 主流程图更新：加入四阶段（核心设定设计 → 主线剧情设计 → 开篇 → 每章循环）。

同步三件套：SKILL.md / skill.json（version 2.0.0）/ CHANGELOG。

## v1.1.0 | 2026-09-08

### 合并 rhythm 进 write，系列 10 → 9

老板确认 write（渲染正文）与 rhythm（单章节奏硬尺）都是单章级任务、且 write 原已内含引用 rhythm 核心指标，存在重叠维护。本轮合并：

- **移除子专家** pop-mirror-rhythm；其单章硬尺全部并入 pop-mirror-write 成「节奏硬尺」节（源文件 01-章节节奏 精华逐字直贴保留）。
- **专家清单重排**：01 onboard / 02 world / 03 character / 04 opening / 05 plot / 06 write（含节奏硬尺）/ 07 deai / 08 review。原"九个子专家"更新为"七个写作子专家 + 本总控共 8 个 skill"。
- **链路更新**：每章循环由「05规划 + 06节奏 先行」改为「05规划 先行 → 06写作（节奏内嵌）→ 07清洗 → 08审查」。
- **路由表/速查表**同步移除 rhythm 行；节奏验收阈值随迁至 06 write。

同步三件套：SKILL.md / skill.json（version 1.1.0）/ CHANGELOG。

## v1.0.0 | 2026-09-08

### 初始化：Mirror创作专家系列总控 skill

将镜界（Mirroric 小说创作应用）系列 AgentSkill 的提示词精华改造成可直接跑通的专家 skill 系列。本 skill 为总控，负责专家清单维护、源映射、创作链路编排与通用约定；九个子专家（onboard/world/character/opening/plot/rhythm/write/deai/review）+ 本总控共 10 个 skill 一起构成完整专家系列。

- 专家清单 9 项，各对应镜界源文件，精华逐字直贴不改写；「面板番茄榜单」源非写作流程，不转 skill。
- 保真红线：各 skill 的「怎么操作·精华」节 = 镜界对应 skill 文件原文逐字直贴；新增编排内容只出现在「做什么/红线/速查表」等编排节，与精华分隔。
- 创作链路：立项→世界观→人设→ (黄金三章) → 每章循环【规划→节奏→写作→去AI味→审查】。

同步三件套：SKILL.md / skill.json（version 1.0.0）/ CHANGELOG。
