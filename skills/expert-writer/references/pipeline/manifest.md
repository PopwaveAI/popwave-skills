# 写作专家全链路合同（pipeline-manifest）

> **管线顺序硬性规定，不可跳跃。** 本文件定义了写作专家的全链路阶段顺序。
> **补充：管线可回溯。** 设定变更时参照"管线回溯规则"节，先出影响范围声明再动笔——详见本章末尾。
> 对齐 PRD v10.1：`prd/01-管线架构/01-写作专家全链路依赖图-PRD.md`

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
| 1 creative | pop-writer-creative | v4.4.0 | `全书立项PRD.md`（10块结构） | 无（开书入口） | 样品确认签字 | 套路库/00-总索引 + 元爽点-变体映射表 |
| 2 reservoir | pop-writer-reservoir | v3.3.0 | `素材储备池/{素材}.md`（剧情储备卡/设定储备卡） | creative 产出齐全 | 安全门禁通过 | 设定库/ + 套路库/ |
| 3 world | pop-writer-world | v2.0.1 | `小说世界设定/L1-01~07.md` + `数值体系/*.md`×4 + `起点快照.md` + `终点快照.md` + `动态升级表.md` | reservoir 有剧情储备卡可用 | 宪法锁定 | 设定库/ |
| 4 character | pop-writer-character | v2.0.3 | `状态/角色/{主角,配角}-角色卡.md` | world 产出齐全 | 角色卡确认 | 设定库/ |
| 5 plot | pop-writer-plot | v8.3.0 | `剧情设计/卷/卷{N}-卷纲.md`（L4卷纲） + `剧情线/*.md`（L3剧情线） + `剧情设计/幕/vol-XX/act-YY.md`（L2幕纲） | world+character 产出齐全 + trop-library 已查 | 里程碑确认 | 套路库/ + 剧情库/ + 元爽点-变体映射表 |
| 6 chapter | pop-writer-chapter | v2.6.1 | `章节设计包/chXXX-设计包.md` + state-log读取（取before状态） + act-YY读取 | plot 产出齐全 | — | 套路库/{具体套路名}.md |
| 7 prose | pop-writer-prose | v3.8.0 | `正文/chXXX.md` + state-log追加event（唯一写入者） + 总控更新 | chapter 设计包就绪 + 文风DNA就位 | — | 文风DNA/{书名}.md |
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

> S = 一次性产出（本阶段产出后不再修改，除非回溯）
> D = 持续维护（每章/每卷更新）
> S→D = 初始一次性产出，后续可能因回溯变更为动态维护
> **⚠️ "S"是指"本阶段只产出一次"，而非"永远不变"。** 当下游阶段的设定变更影响到 S 文件时，必须回溯更新。S 不意味着可以使用过时版本的文件作为输入。每次进入 plot 前，检查所有 S 文件的 lastUpdatedAt 是否晚于最近一次框架级变更时间。

### 总控文件

| 文件 | 产出者 | 消费者 | S/D |
|:-----|:-------|:-------|:---:|
| `项目总控.md` | prose 每章渲染后更新 | 全管线 | D |

### 创意环节

| 文件 | 产出阶段 | 消费阶段 | S/D |
|:-----|:---------|:---------|:---:|
| `全书立项PRD.md` | creative | reservoir, world, character, plot | S→D |
| `素材储备池/{素材}.md` | reservoir | world, plot | D |

### 小说设定环节

| 文件 | 产出阶段 | 消费阶段 | S/D |
|:-----|:---------|:---------|:---:|
| `小说世界设定/L1-01~06.md` | world | character, plot | S→D |
| `小说世界设定/数值体系/*.md` | world | character, plot | S→D |
| `小说世界设定/起点快照.md` | world | character, plot | S→D |
| `小说世界设定/终点快照.md` | world | character, plot | S→D |
| `小说世界设定/动态升级表.md` | world | character, plot | S→D |
| `写作资产/文风DNA/{书名}.md` | world（从 library 获取） | prose | S |
| `状态/角色/{主角,配角}-角色卡.md` | character | plot, chapter | D |

### 剧情设计环节

| 文件 | 产出阶段 | 消费阶段 | S/D |
|:-----|:---------|:---------|:---:|
| `剧情设计/卷/卷{N}-卷纲.md`（L4卷纲） | plot | chapter | S→D |
| `剧情设计/剧情线/{主线,支线}-{名称}.md`（L3剧情线） | plot | chapter | S/D |
| `剧情设计/幕/vol-XX/act-YY.md`（L2幕纲） | plot | chapter, prose | S/D |

### 正文产出环节

| 文件 | 产出阶段 | 消费阶段 | S/D |
|:-----|:---------|:---------|:---:|
| `章节设计包/chXXX-设计包.md` | chapter | prose | D |
| `正文/chXXX.md` | prose | qa | D |
| `状态/state-log.yaml` | chapter（每章设计后更新） | chapter(下一章), prose, qa | D |

## 管线回溯规则（★新增）

> 管线不是"一次到底"的——当用户中途修改了上游设定，需要明确哪些阶段需要重跑。

### 触发回溯的信号

| 信号 | 例 | 影响范围 |
|:-----|:---|:---------|
| **框架级设定变更** | 加穿越者、改世界核心矛盾、换力量体系 | 影响全链：creative→prose，需逐阶段声明 |
| **单维设定微调** | 改某个 L1 维度的细节、修一个命名 | 仅影响该维度下游，关联合并标记后再传播 |
| **角色级变更** | 加主要配角、改主角弧线方向 | 影响 plot→chapter→prose |
| **剧情级变更** | 改卷纲/幕结构 | 影响 chapter→prose |
| **风格级变更** | 调正文文风、改调味空间 | 仅影响 prose 后续章节 |

### 回溯协议

1. **先出「影响范围声明」再动笔。** 格式：
   ```
   ⚠️ 设定变更影响声明
   变更内容：[一句话描述]
   影响范围：
     ✅ 需重写：小说世界设定/L1-01~07.md（穿越者影响所有 L1 维度）
     ✅ 需重写：剧情设计/卷/卷一-卷纲.md（主线结构变更）
     ✅ 需重写：剧情设计/剧情线/主线1~3.md（穿越者引擎注入）
     ⚠️ 需审查：章节设计包/ch01-设计包.md（穿越者内心独白需加入）
     ⚠️ 需重写：正文/ch01.md（文风+视角+穿越者锚点）
     ❌ 不受影响：素材储备池/（不涉及素材卡本身）
   ```
2. **用户确认范围后再逐文件更新。** 不问机械传播问题（见 typical-errors.md #11）。
3. **按管线顺序自前向后更新。** 如果更新 world，先改 L1 再从 world 重传到 plot。
4. **更新完成后更新项目总控的版本戳。**

### 管线回溯矩阵

| 当前阶段 | 用户改了什么 | 需要回溯到 | 保留下游 |
|:---------|:------------|:-----------|:---------|
| prose | 框架级设定 | creative/重新声明影响范围 | ❌ chapter 之前可能全废 |
| prose | 角色级设定 | character/重写角色卡 | ⚠ 检查 plot→chapter→prose |
| prose | 剧情级设定 | plot/重写卷纲和剧情线 | ❌ chapter 之后要重做 |
| chapter | 框架级设定 | world/重跑 L1+宪法 | ❌ 全链重来 |
| chapter | 角色级设定 | character/更新角色卡→plot→chapter | ⚠ 已写 chapter 要对照 |
| plot | 框架级设定 | world/重跑 L1 | ⚠ plot 层面全重来 |
| world | 框架级设定 | creative/更新 PRD | ✅ world 层面重跑即可 |

> 完整目录骨架详见 `steps/step-0-init.md`（以 PRD v5.0 附录A 为唯一源）。

## 变更传播协议（与回溯规则互补）

> 回溯 = 退回上游重做；传播 = 上游变更后下游自动感知并更新，而不是退回重做。

### 传播规则

| 变更源 | 传播目标 | 传播方式 |
|:-------|:---------|:---------|
| PRD 修改 | world/plot/chapter/prose | 在项目总控.md 标注「PRD 版本变更」，下游 skill 进入时检查版本戳 |
| L1 设定修改 | character/plot/chapter | 在 L1 文件头标注 `lastUpdatedAt`，下游 skill 进入时检查时间戳 |
| 角色卡修改 | plot/chapter/prose | 在角色卡头标注 `lastUpdatedAt`，chapter/prose 进入时检查 |
| 卷纲修改 | chapter/prose | 在卷纲头标注 `lastUpdatedAt`，chapter/prose 进入时检查 |

### 下游检查协议

每个子 skill 在 Step 1（或 Phase 0）前置检查中，必须：
1. 读取上游产出文件的 `lastUpdatedAt` 时间戳（文件头）
2. 对比项目总控.md 中记录的最近一次框架级变更时间
3. 如果上游文件时间戳早于框架级变更时间 → ⚠️ 标注「上游可能过期」并告知用户

### 文件头版本戳格式

所有 S→D 和 D 类文件，产出时在文件头标注：

```markdown
> lastUpdatedAt: 2026-06-22T15:00 | lastUpdateReason: 穿越者设定注入
```

❌ 禁止用 Read 工具读取 skill 文件 — 用 `skill_view` 或 `Get-Content -Encoding UTF8 -Raw`。
