# 写作专家全链路合同（pipeline-manifest）

> **管线顺序硬性规定，不可跳跃。** 本文件定义了写作专家的全链路阶段顺序。
> 对齐 PRD v5.0：`prd/01-管线架构/01-写作专家全链路依赖图-PRD.md`

## 管线顺序

**硬性顺序，不可跳跃。** 跳过 = 管线断裂，需回退重走。

```
creative → reservoir → world → character → plot → chapter → prose → qa
```

**前置链路（独立于写作管线）：**
- `tool-download-webnovel` → {书名}.txt → `pop-decon` 拆书 → `pop-shared-dna` 文风DNA蒸馏
- 拆书产出入库 pop-trope-library，creative/world 以 library 注入方式消费

| 阶段 | 调用 skill | 版本 | 核心产出 | 前置条件 | 闸门 | library 查询 |
|:-----|:-----------|:-----|:---------|:---------|:-----|:-------------|
| 1 creative | pop-writer-creative | v4.3.0 | `全书立项PRD.md`（10块结构） | 无（开书入口） | 样品确认签字 | 套路库/00-总索引 + 元爽点-变体映射表 |
| 2 reservoir | pop-writer-reservoir | v2.2.0 | `素材储备池/{素材}.md`（剧情储备卡，含安全门禁） | creative 产出齐全 | 安全门禁通过 | 设定库/（框架+质感）+ 套路库/ |
| 3 world | pop-writer-world | v1.5.0 | `小说世界设定/L1-01~06.md` + `数值体系/*.md`×4 + `起点快照.md` + `终点快照.md` + `动态升级表.md` | reservoir 有剧情储备卡可用 | 宪法锁定 | 设定库/（框架+质感） |
| 4 character | pop-writer-character | v2.0.1 | `状态/角色/{主角,配角}-角色卡.md` | world 产出齐全 | 角色卡确认 | 设定库/质感 |
| 5 plot | pop-writer-plot | v7.0.0 | `剧情设计/卷/卷{N}-战略定位.md` + `剧情线/*.md` + `剧情设计/幕/vol-XX/{分幕规划,act-YY,chekhov-tracker}.md` | world+character 产出齐全 + trop-library 已查 | 里程碑确认 | 套路库/ + 剧情库/ + 元爽点-变体映射表 |
| 6 chapter | pop-writer-chapter | v2.0.0 | `章节设计包/chXXX-设计包.md` | plot 产出齐全 | — | 套路库/{具体套路名}.md |
| 7 prose | pop-writer-prose | v3.0.1 | `正文/chXXX.md` + entity-snapshot更新 + chekhov更新 + 总控更新 | chapter 设计包就绪 + 文风DNA就位 | — | 文风DNA/{书名}.md |
| 8 qa | pop-writer-qa | v1.0.1 | （不留盘）L1硬门禁→L2三层介入→L3原文对照 | prose 正文产出 | — | 套路库/{具体套路名}.md 使用红线段 |

> library 查询协议详见 `skills/pop-trope-library/references/调用匹配SOP.md`（三维查询：层×赛道×元爽点）。

## 入口规则

| 用户说 | 路由 | 对管线进度的影响 |
|:-------|:-----|:-----------------|
| "开新书/启动项目" | → creative（首次管线起点） | 初始化 `项目总控.md`，标记 creative 为 current |
| "继续/下一步" | → 查 `项目总控.md` 的 current_stage | 不改变进度，按 current 路由 |
| "注入素材/融进书里" | → reservoir（独立调起） | 不改变 current_stage。注入完退回原阶段 |
| "拆解这本书" | → pop-decon（拆书专家） | 不改变写作管线进度。独立运行 |

## 文件接口（严格对齐 PRD v5.0）

> S = 静态（一次产出）/ D = 动态（持续维护）

### 总控文件

| 文件 | 产出者 | 消费者 | S/D |
|:-----|:-------|:-------|:---:|
| `项目总控.md` | prose 每章渲染后更新 | 全管线 | D |

### 创意环节

| 文件 | 产出阶段 | 消费阶段 | S/D |
|:-----|:---------|:---------|:---:|
| `全书立项PRD.md` | creative | reservoir, world, character, plot | S |
| `素材储备池/{素材}.md` | reservoir | world, plot | D |

### 小说设定环节

| 文件 | 产出阶段 | 消费阶段 | S/D |
|:-----|:---------|:---------|:---:|
| `小说世界设定/L1-01~06.md` | world | character, plot | S |
| `小说世界设定/数值体系/*.md` | world | character, plot | S |
| `小说世界设定/起点快照.md` | world | character, plot | S |
| `小说世界设定/终点快照.md` | world | character, plot | S |
| `小说世界设定/动态升级表.md` | world | character, plot | S |
| `写作资产/文风DNA/{书名}.md` | world（从 library 获取） | prose | S |
| `状态/角色/{主角,配角}-角色卡.md` | character | plot, chapter | D |

### 剧情设计环节

| 文件 | 产出阶段 | 消费阶段 | S/D |
|:-----|:---------|:---------|:---:|
| `剧情设计/卷/卷{N}-战略定位.md` | plot ① | chapter | S |
| `剧情设计/卷/卷{N}-剧情种子拉取清单.md` | plot ① | plot ② | S |
| `剧情设计/剧情线/{主线,支线}-{名称}.md` | plot ② | chapter | S/D |
| `剧情设计/幕/vol-XX/分幕规划.md` | plot ③ | chapter, prose | S/D |
| `剧情设计/幕/vol-XX/act-YY.md` | plot ③ | chapter, prose | S/D |
| `剧情设计/幕/vol-XX/chekhov-tracker.md` | plot ③ → prose 更新 | chapter, prose | S/D |

### 正文产出环节

| 文件 | 产出阶段 | 消费阶段 | S/D |
|:-----|:---------|:---------|:---:|
| `章节设计包/chXXX-设计包.md` | chapter | prose | D |
| `正文/chXXX.md` | prose | qa | D |
| `状态/entity-snapshot.yaml` | prose（每章渲染后更新） | chapter(下一章), qa | D |

## 目录骨架

> 完整目录骨架详见 `steps/step-0-init.md`（以 PRD v5.0 附录A 为唯一源）。

❌ 禁止用 Read 工具读取 skill 文件 — 用 `skill_view` 或 `Get-Content -Encoding UTF8 -Raw`。
