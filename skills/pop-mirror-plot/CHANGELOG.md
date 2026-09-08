# CHANGELOG

## v1.1.0 | 2026-09-08

### 修订：节奏硬尺并入 write 后的交叉引用清理

pop-mirror-rhythm 已并入 pop-mirror-write，本 skill 同步更新：

- 前置输入移除「pop-mirror-rhythm 给的字数断章约束」，字数断章改由 06write 内嵌节奏硬尺承担。
- 编排说明中"按 AgentSkills 匹配正文写作/长篇连续性技能"的顶替由 pop-mirror-rhythm/write/review 调整为 write/review。

版本三处一致：SKILL.md / skill.json（version 1.1.0）/ CHANGELOG。

## v1.0.0 | 2026-09-08

### 初始化：Mirror 规划专家 skill

基于镜界 `02-章节规划.md`，提示词精华逐字直贴、未增删改写。新增编排壳（做什么/红线/速查表）与精华分隔。

- 链路位置：开篇定锣后进入逐章规划；本章大纲连同 06rhythm 节奏硬尺一起作为 07write 的输入。
- 原文"按 AgentSkills 匹配正文写作/长篇连续性技能"的运行时动作，在本系列由 pop-mirror-rhythm/write/review 顶替；事实冲突裁决顺序为方法核心，逐字保留。

同步三件套：SKILL.md / skill.json（version 1.0.0）/ CHANGELOG。