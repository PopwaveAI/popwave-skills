# 写作专家全链路合同（pipeline-manifest）

> **管线顺序硬性规定，不可跳跃。** 本文件定义了写作专家的全链路阶段顺序。为什么采用此方案代替分散的 SKILL.md pipeline 声明→见 `references/pipeline-design-rationale.md`。

## 管线顺序

**硬性顺序，不可跳跃。** 跳过 = 管线断裂，需回退重走。

```
creative → reservoir → world → plot → chapter → prose → qa
```

| 阶段 | 调用 skill | 核心产出 | 前置条件 | 闸门 |
|:-----|:-----------|:---------|:---------|:-----|
| 1 creative | pop-writer-creative | PRD.md, 层架构.md, 故事引擎.md, 素材储备池(首版), 爽点引擎.md, 样品试读.md | 无（开书入口） | 样品确认签字 |
| 2 reservoir | pop-writer-reservoir | 素材储备池(升级为剧情储备卡, 含安全门禁) | creative 产出齐全 | 安全门禁通过 |
| 3 world | pop-writer-world | L1-01~07(含L1-07术语与文明底色), 角色卡, 数值体系×4, 起点快照, 世界宪法, 动态升级表 | reservoir 有剧情储备卡可用 | 宪法锁定 |
| 4 plot | pop-writer-plot | 卷战略定位, 剧情线文档独立.md×N, 分幕规划, act-YY.md, chekhov-tracker | world 产出齐全 + trop-library 已查 | 里程碑确认 |
| 5 chapter | pop-writer-chapter | chXXX-设计包, entity-snapshot更新, chekhov-tracker更新 | plot 产出齐全 | — |
| 6 prose | pop-writer-prose | 正文/chXXX.md | chapter 设计包就绪 | — |
| 7 qa | pop-writer-qa | QC 报告（不留盘，纯感受型） | prose 正文产出 | — |

## 入口规则

| 用户说 | 路由 | 对管线进度的影响 |
|:-------|:-----|:-----------------|
| "开新书/启动项目" | → creative（首次管线起点） | 初始化项目总控.md，标记 creative 为 current |
| "继续/下一步" | → 查项目总控.md 的 current_stage | 不改变进度，按 current 路由 |
| "注入素材/融进书里" | → reservoir（独立调起） | 不改变 current_stage。注入完退回原阶段 |
| "拆解这本书" | → pop-decon（拆书专家） | 不改变写作管线进度。独立运行 |

## 截断检测协议（强制）

每次用 `Get-Content` 或 `Read` 工具加载文件后，必须执行：

```
1. 获取读取结果的实际字符数 → content.length
2. 获取文件系统大小 → (Get-Item '{path}').Length
3. if content.length < file_size × 0.9:
     标记 ⚠️ 截断警告
     回退用 Get-Content -Encoding UTF8 -Raw 重新读取
     （注意：不回退用 Read+limit，回退只用 Raw 模式）
4. if 截断反复出现（同一文件连续 2 次检查不通过）:
     终止操作，告知用户"文件过大，需要分段处理"
     不要基于不完整内容继续执行
```
