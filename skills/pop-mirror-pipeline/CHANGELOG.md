# CHANGELOG

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