# CHANGELOG

## v1.1.0 | 2026-09-08

### 并入节奏硬尺：pop-mirror-rhythm 合并入本 skill

老板确认 write（渲染正文）与 rhythm（单章节奏硬尺）都是单章级别任务、且 write 原已内含引用 rhythm 核心指标，存在重叠维护。本轮合并：

- **吸收镜界 `01-章节节奏` 全套硬尺**：字数额度±10%、爽点/钩子/悬念密度（300/500/1000-1500字）、叙事段40-120字、>60%短段返工阈值、80/20断章、钩子六类轮换+下章前1/3反馈、节奏变化、场景规范、高潮前3-5章铺线+后1-2章后效。作为「精华·B」逐字直贴，与「精华·A（03-章节写作）」并列，双源均保真。
- **清除重复引用**：原「字数与密度」节由"pop-mirror-rhythm 提供"改为指向内嵌节奏硬尺（精华·B），避免双份数字打架。
- **验收标准随迁**：review 原以 rhythm 的"60%短段返工/断章80%"为验收阈值，现改以本 skill 的节奏硬尺验收，标准不丢失。
- **链路再编排**：执行态从"渲染→清洗→审查"变为 write 一并落节奏硬尺，交 deai→review 闭环。
- pop-mirror-rhythm skill 整体移除，系列 10 → 9 个专家。

同步三件套：SKILL.md / skill.json（version 1.1.0）/ CHANGELOG。

## v1.0.0 | 2026-09-08

### 初始化：Mirror 写作专家 skill

基于镜界 `03-章节写作.md`，提示词精华逐字直贴、未增删改写。新增编排壳（做什么/红线/速查表）与精华分隔。

- 链路位置：拿到 pop-mirror-plot 大纲 + pop-mirror-rhythm 节奏硬尺后渲染正文；本 skill 是系列核心执行态（临时实验版已验证可跑通出稿）。
- 原文"按 AgentSkills 匹配节奏密度断章/长篇连续性/去AI味技能"的运行时动作，在本系列由 pop-mirror-rhythm（06）/ pop-mirror-review（09）/ pop-mirror-deai（08）顶替，方法精化不变。

同步三件套：SKILL.md / skill.json（version 1.0.0）/ CHANGELOG。