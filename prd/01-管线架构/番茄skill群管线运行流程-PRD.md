# 番茄 skill 群管线运行流程 PRD

> 版本：v1.2 | 日期：2026-07-20
> 对应 skill 版本快照：pipeline v1.0.0 / seed v13.2.0 / plot v9.1.0 / write v8.0.0 / review v4.1.0 / dna-style v1.0.0 / research v1.2.0 / decon v20.1.0 / shared-dna v4.1.0 / download v7.0.0

---

## 1. 管线全貌

番茄 skill 群是一条从"用户一句话方向"到"可连载正文"的创作管线，由 10 个 skill 协作完成。总控是 **pop-fanqie-pipeline**（项目初始化 + project-state.md 状态追踪 + 5 个 phase 路由），主线是 seed → plot → write → review 的四章循环。前置供给环节（参考书下载/文风 DNA 提取/拆书）由 pipeline 的 Phase 0 作为**必选闸门**强制执行——用户给方向后，agent 必须主动引导参考书（要么用户给书名，要么 agent 帮找同赛道热门推荐），参考书就绪后才进入 seed 主流程。

```mermaid
flowchart TD
    User([用户一句话方向])

    subgraph 总控
        PIPE[pop-fanqie-pipeline<br/>初始化+状态追踪+phase路由]
        PIPE0[Phase 0: 参考书闸门<br/>必选·用户给书或agent推荐]
    end

    subgraph 前置供给
        DL[tool-download-webnovel<br/>下载参考书]
        DECON[pop-decon<br/>拆书精拆·可选]
        DNA[pop-dna-style<br/>文风DNA提取]
    end

    subgraph 主线四章循环
        SEED[pop-fanqie-seed<br/>创意+黄金首章]
        PLOT[pop-fanqie-plot<br/>世界构筑+剧情白描]
        WRITE[pop-fanqie-write<br/>正文渲染 ch002+]
        REVIEW[pop-fanqie-review<br/>四维审核+沉淀]
    end

    subgraph 横切·被调用方
        RESEARCH[pop-research<br/>调研·按需]
    end

    User --> PIPE
    PIPE --> PIPE0
    PIPE0 -->|用户给书名/agent推荐| DL
    PIPE0 -->|想精拆做立项圣经| DECON
    PIPE0 -->|用户拒绝·标注风险| SEED
    DL -->|参考书txt| DNA
    DL -->|参考书txt| DECON
    DNA -->|涌现/文风锚定.md| WRITE
    DECON -->|设定库/剧情库| PLOT
    DNA -.->|可选: 创意前部署DNA| SEED
    DECON -->|设定库/剧情库| SEED
    RESEARCH -.->|知识沉淀| SEED
    RESEARCH -.->|知识沉淀| PLOT
    RESEARCH -.->|采风| WRITE

    PIPE0 -->|参考书就绪| SEED
    SEED -->|创意.md+ch001| PLOT
    PLOT -->|骨架+剧情白描+章锚点表| WRITE
    WRITE -->|chNNN正文+交付面板| REVIEW
    REVIEW -->|审核-chNNN.md| WRITE
    REVIEW -->|通过| NEXT[下一章 chNNN+1]
    NEXT --> WRITE
```

前置供给的触发入口已从 seed 1a 的"被动识别"改为 pipeline Phase 0 的"必选闸门"。用户给方向后，pipeline 强制执行参考书摸底：用户给书名则下载+提取 DNA；用户没想好则调用 pop-research 调研同赛道热门推荐书单，用户选书后再下载+提取 DNA；用户明确拒绝才标注风险放行。参考书就绪后 pipeline 路由到 seed 的 Phase 1 继续 1c 市场调研。

横切环节（图中虚线）的特点是"被调用方"：pop-research 不主动触发，由 seed / plot / write 在遇到信息缺口时按需调用，传入领域+具体问题+期望深度，执行完返回路径指针。

---

## 2. 各 skill 定位与边界

### 2.1 总控

| skill | 版本 | 定位 | 输入 | 产出 |
|:--|:--|:--|:--|:--|
| pop-fanqie-pipeline | v1.0.0 | 项目初始化+状态追踪+phase路由 | 项目名/当前目录 | `project-state.md`（管线地图） |

### 2.2 主线四章循环

| skill | 版本 | 定位 | 输入 | 产出 |
|:--|:--|:--|:--|:--|
| pop-fanqie-seed | v13.2.0 | 创意到首章 | 参考书摸底+用户一句话方向 | `0-立项/创意.md` + `2-正文/ch001.md` |
| pop-fanqie-plot | v9.1.0 | 创意到完整故事世界 | 创意.md + ch001 | `1-骨架/骨架.md` + `剧情白描.md` + `章锚点表.md` |
| pop-fanqie-write | v8.0.0 | 逐章渲染正文 | 剧情白描+骨架+current-state+前章+笔触DNA | `2-正文/chNNN.md`（2000-2500字）+交付面板 |
| pop-fanqie-review | v4.1.0 | 每章审核+沉淀 | chNNN正文+交付面板+剧情白描本章段 | `审核-chNNN.md`（四维审核+剧情沉淀） |

**边界纪律**：seed 只产创意+首章，不碰世界构筑；plot 只产骨架+白描，不写正文；write 只渲染不审稿；review 只审核不重写。每个 skill 的产出是下游的输入，不得越界。

### 2.3 前置供给环节

| skill | 版本 | 定位 | 何时调用 | 产出 |
|:--|:--|:--|:--|:--|
| tool-download-webnovel | v7.0.0 | 网文搜索下载 | 用户给参考书但无本地文件 | `downloads/{书名}.txt` |
| pop-dna-style | v1.0.0 | 文风 DNA 提取（笔触供给方） | pipeline Phase 0 参考书闸门 | `涌现/文风锚定.md`（笔触DNA）+ 可选 `涌现/剧情DNA-brief.md` |
| pop-decon | v20.1.0 | 拆书精拆（可选） | 想精拆一本书做立项圣经时 | `项目本地/设定库/`+`剧情库/`+`立项库/` |
| pop-research | v1.2.0 | 调研（被调用方） | seed/plot/write 遇到信息缺口时按需调用 | `写作参考/知识沉淀/{主题}.md` |

**pop-dna-style 和 pop-decon 的边界**：两者读同一本参考书但粒度不同。decon 是重拆（8 维度全拆+Beat Sheet+全书剧情白描），用于精拆一本书做立项圣经；pop-dna-style 是轻采（笔触 DNA 必做+剧情 brief 可选），用于拿参考书当灵感源。产出路径也不同：decon 沉淀到项目本地 `设定库/剧情库/立项库/`，pop-dna-style 部署到项目本地 `涌现/文风锚定.md`。

**pop-dna-style 和 pop-shared-dna 的边界**：pop-shared-dna v4.1.0 是老管线（pop-qidian-write 等）的文风 DNA 引擎，产出到 `写作资产/文风库/{书名}.md`；pop-dna-style v1.0.0 是番茄新管线的笔触 DNA 供给方，产出到 `涌现/文风锚定.md`。两者服务不同管线，共存不冲突。

---

## 3. 数据流转

### 3.1 主线数据流

```
pipeline（project-state.md 路由）→ seed 产出 → plot 消费 → write 消费 → review 消费 → write 消费（下一章）
```

| 产出文件 | 生产方 | 消费方 | 说明 |
|:--|:--|:--|:--|
| `project-state.md` | pipeline（初始化 + 每 phase 更新） | pipeline（每次对话路由）+ 所有 skill（上下文感知） | 管线唯一状态源。当前 phase / 参考书状态 / 创意摘要 / 最近产出 |
| `0-立项/创意.md` | seed | plot | 创意方向+金手指+散文体简介+轻量主角轮廓 |
| `2-正文/ch001.md` | seed | plot / write | 黄金首章试读章，write 从 ch002 开始 |
| `1-骨架/骨架.md` | plot | write | 第一卷详规（幕序列/悬念/高潮/势力/反派） |
| `1-骨架/剧情白描.md` | plot | write / review | 整卷故事流，write 最关键输入，review 对照核心事件 |
| `1-骨架/章锚点表.md` | plot | write | 章节顺序锁定，禁止跳章 |
| `2-正文/chNNN.md` | write | review | 2000-2500字正文+交付面板 |
| `审核-chNNN.md` | review | write（下一章） | 事件白描+主角变化五项+钩子追踪+下章建议 |

### 3.2 笔触 DNA 数据流

```
参考书 txt → pop-dna-style → 涌现/文风锚定.md → write（笔触DNA标准插槽）
```

write v8.0.0 的笔触层完全靠 DNA 驱动，自身只保留结构约束（章型骨架+字数+节奏物理量+爽感引擎）。DNA 加载遵循三态协议：

| 状态 | 条件 | write 行为 |
|:--|:--|:--|
| 启用态 | `涌现/文风锚定.md` 存在 | 笔触层从 DNA 取，禁止凭空发挥 |
| 缺失态 | `涌现/文风锚定.md` 不存在 | Step1 提示用户部署 DNA |
| trial 模式 | 用户拒绝部署 | 不内置默认风格，用户须显式声明基础风格 |

DNA 在 write 加载优先级排第一位，10 万字裁剪时也不裁剪。

### 3.3 调研数据流

```
seed/plot/write 遇到信息缺口
    → 调用 pop-research（传入领域+具体问题+期望深度）
    → pop-research 执行（三界框架 or 采风级）
    → 产出 写作参考/知识沉淀/{主题}.md
    → 返回路径指针给调用方
```

pop-research 支持 4 个期望深度档位：种子级（三界全量）/场景级（单界深入）/缺口级（定向补缺）/采风级（真实质感采集）。采风级跳过三界框架，直接做真实质感采集，产出可复用细节片段，供 write 渲染质感使用。

---

## 4. 理论运行流程

### 4.1 完整首次运行（含 Phase 0 参考书闸门）

以下是一次完整首次运行的理论流程，从用户给出方向到写出第一章正文。pipeline 作为总控接管全程——agent 每次对话先读 `project-state.md` 知道当前 phase，按路由规则执行，每 phase 完成后更新 state。

**Phase 0：参考书闸门（pipeline · 必选）**

管道接手用户方向后的第一步，强制执行参考书摸底。不完成摸底不进入 Phase 1。agent 主动问用户是否已有想参考笔触的书，三条路由：

| 用户回答 | pipeline 路由 | 执行环节 |
|:--|:--|:--|
| 给了书名（"参考《深渊主宰》的笔触"） | → tool-download-webnovel 下载 → pop-dna-style 提取 DNA（档位 A 笔触必做 + 档位 B 剧情 brief 可选） | 参考书下载 + 文风 DNA 提取 |
| 没想好，需要推荐 | → pop-research（种子级）调研同赛道热门 → 推荐书单 → 用户选 1-2 本 → download + dna-style | 调研 + 推荐 + 下载 + DNA |
| 想精拆做立项圣经 | → download → pop-decon Phase 1-4 精拆 → 沉淀到设定库/剧情库/立项库 → 仍需 dna-style 提取笔触 DNA | 下载 + 拆书 + DNA |
| 明确拒绝 | → 二次确认风险（write 将因缺失 DNA 进 trial 模式，风格由 API 自由发挥）→ 坚持拒绝 → 标注风险放行 | 跳过，进 Phase 1 |

Phase 0 具体执行步骤：

1. 参考书下载：`tool-download-webnovel` 三阶段下载（脚本搜索 → web 搜索兜底 → 验证交付）→ `downloads/{书名}.txt`
2. 文风 DNA 提取：`pop-dna-style` 场景定向采样 25-30 章 → 按 v4 模板提取笔触 DNA（通用维度 ≥4 + 场景卡 ≥8）→ 部署到 `涌现/文风锚定.md`
3. 拆书（可选）：`pop-decon` 初始化 + 一次性路由 → Phase 1-4 精拆 → 沉淀到项目本地 `设定库/剧情库/立项库/`

步骤 2 和 3 可并行，都依赖步骤 1 的参考书 txt。Phase 0 完成后更新 `project-state.md`（phase=phase1，参考书条目填"就绪"），pipeline 路由到 Phase 1。

**Phase 1：创意（seed）**

4. 市场调研：seed Phase 1 内置 WebSearch 3 轮，产出借鉴点/避雷点清单
5. 纯自由发散：基于一句话方向，纯自由产出 5-6 个差异化方向（不注入搜索数据/格式模板）
6. 市场校准：用借鉴点/避雷点清单事后校准（踩避雷点=淘汰，用到借鉴点=加分）
7. 用户选定 1 个方向
8. 结构化打磨：行为引擎检查 → 合成金手指（梗×机制×限制）→ 四眼法验证（画面/限制/场景量/行为引擎）→ 散文体简介 → 轻量主角轮廓 → 落盘 `0-立项/创意.md`
9. 黄金首章：基于创意.md 写 2000-2500 字试读章 → `2-正文/ch001.md`

**Phase 2：世界构筑（plot）**

10. 加载创意文档+黄金首章
11. 世界构筑：四张地图（地理/力量/势力/危机）+ 完整人物包 + 第一卷敌人 4 层梯度
12. 第一卷详规：终点+配角+幕序列+悬念+高潮+势力+反派+世界危机
13. 四图叠加推演剧情白描：基于四图+人物包推演整卷故事流 → `1-骨架/剧情白描.md`（投入 50% 注意力）
14. 落盘：骨架.md + 剧情白描.md + 章锚点表.md

**Phase 3：正文渲染（write，从 ch002 开始）**

15. 全文加载：剧情白描.md + 骨架.md + current-state.md + 前章正文 + 设定库精选（≤1000字）+ 笔触 DNA（三态协议）
16. 选章型+章意图思考：从 4 种章型（opening_shift / confrontation_pressure / combat_reversal / reveal_hook）选 1 个
17. 写正文：三层指导（结构/节奏/爽感）+ 笔触层从 DNA 取 → 2000-2500 字
18. 篇幅硬限制检查+落盘 → `2-正文/chNNN.md`
19. 交付面板+人机共创

**Phase 4：审核沉淀（review）**

20. 符合性检查：正文 vs 剧情白描核心事件（偏离=废章）+ 设定一致性 5 项 + 爽感闭环三段式
21. 笔触检查：AI 味 7 项 + 笔触 DNA 一致性（启用态查 DNA 一致 8 项 / trial 模式查未套错误风格 4 项）
22. 好看度 4 问：有没有劲 / 记忆点 / 哪里无聊 / 代入感
23. 剧情沉淀：事件白描 + 主角变化五项（位置/能力/资产/心态/关系）+ 钩子追踪 + 下章建议 → `审核-chNNN.md`
24. 通过 → 进入下一章（回到 Phase 3 步骤 15）；不通过 → 打回重写

### 4.2 稳态运行（章节循环）

首次运行完成后，进入稳态循环。每写一章走 Phase 3 + Phase 4：

```
ch002 → write → review → 通过？
                        ├─ 是 → ch003 → write → review → ...
                        └─ 否 → 打回 ch002 重写
```

稳态运行中，review 产出的 `审核-chNNN.md` 是下一章 write 的关键输入（事件白描+主角变化+钩子追踪+下章建议），确保连续性不断裂。

### 4.3 横切环节触发时机

| 横切环节 | 触发时机 | 典型场景 |
|:--|:--|:--|
| pop-research（种子级） | pipeline Phase 0 参考书摸底 或 seed Phase 1 发散前 | 用户没想好参考书 → 调研同赛道热门推荐；或种子级世界观调研 |
| pop-research（场景级） | plot Step 2 世界构筑时 | 某个势力/场景需要深入调研 |
| pop-research（缺口级） | write 写作中 | 发现某个设定/规则信息缺口 |
| pop-research（采风级） | write 写作中 | 某职业/场景的真实质感缺口（如急诊室/黑帮谈判） |
| pop-dna-style | pipeline Phase 0 参考书闸门 | 参考书下载完成后提取笔触 DNA |
| pop-decon | pipeline Phase 0（用户主动要求精拆时） | 用户想精拆一本书做立项圣经 |
| tool-download-webnovel | pipeline Phase 0 参考书闸门 | 用户给书名但无本地文件 |

---

## 5. 关键设计决策

### 5.0 pipeline 总控 + project-state.md（v1.0.0 核心改动）

7-20 项目 a 实际运行诊断发现三个结构性缺口：① 没有"我在哪"的文件——agent 启动时不知道该进哪个 phase；② skill 之间盲调度——每个 skill 只知道自己的 SOP；③ 参考书是"用户提了才触发"的可选项——seed 1a 不问就永远跳过。

pipeline v1.0.0 解决这三个缺口：
- `project-state.md` 是管线唯一状态源——agent 每次对话第一件事读它，知道当前 phase / 参考书状态 / 创意摘要 / 当前章节
- Phase 路由规则：init → phase0（参考书闸门）→ phase1（seed）→ phase2（plot）→ phase3（write）↔ phase4（review 循环）
- Phase 0 是必选闸门——参考书从被动识别改为主动引导。不完成摸底不进入 Phase 1，用户明确拒绝是唯一跳过允许

### 5.1 笔触 DNA 可插拔（write v8.0.0 核心改动）

write v8.0.0 做减法，移除了 8 项内置风格倾向（短句为主/道引导词/【】面板/动作链必选/多感官必选/感官优先级表/情绪外化/碎片化思考），只留结构约束。笔触层完全靠 `涌现/文风锚定.md` 驱动。这个设计基于 R42 测试验证：DNA 可插拔方案在公平测试（排除原文章节采样范围）中真实有效。

review v4.1.0 同步这个改动：2b 技法落地检查改为笔触 DNA 一致性检查，启用态查 DNA 一致性 8 项，trial 模式查未套错误风格 4 项。

### 5.2 decon 入库改本地沉淀（v20.1.0）

library 库已优化掉（不再建立 pop-trope-library），decon 拆解产出直接沉淀到项目本地文件夹，路径从 `剧情库/{标签}/` 改为 `项目本地/剧情库/{标签}/`。这简化了管线：不再需要入库确认步骤，产出即沉淀。

### 5.3 seed 纯自由发散 + 市场校准 + 参考书主动摸底（v13.2.0）

seed v13.2.0 在 v13.1.0 的基础上增加：1a 参考书摸底（必问项，agent 主动引导而非被动识别）+ 1b 参考书闸门（pipeline Phase 0 出口，不完成摸底不进市场调研）。同时继承 v13.1.0 的核心设计：恢复 v6.0.0 的纯自由发散核心（R9 验证：纯自由模式产出的创意质量远高于注入搜索数据/格式模板的模式），同时保留 R13/R14 的市场调研环节（发散前 WebSearch 3 轮产出借鉴点/避雷点清单，发散后用清单做事后校准）。这兼顾了创意自由度、市场贴合度和笔触 DNA 的可插拔能力。

### 5.4 剧情白描是 plot 层核心

plot 投入 50% 注意力在剧情白描上。剧情白描是 write 最关键输入——它不是大纲，是"如果跟朋友讲故事会怎么说"的叙事流。review 的符合性检查也以剧情白描本章段的核心事件为对照基准。

### 5.5 review 四维审核优先级

review 的四维审核有明确优先级：符合性 > 笔触 > 好看度 > 沉淀。前面不通过，后面不审。符合性是第一闸门——正文偏离剧情白描核心事件（主线丢失）= 废章，必须打回重写。

---

## 6. 版本快照

| skill | 版本 | 核心改动 |
|:--|:--|:--|
| pop-fanqie-pipeline | v1.0.0 | 新建。项目初始化+project-state.md状态追踪+5 phase路由+Phase 0参考书闸门 |
| pop-fanqie-seed | v13.2.0 | 1a 参考书摸底（必问）+纯自由发散核心+市场调研事后校准 |
| pop-fanqie-plot | v9.1.0 | Step 1对齐seed v13创意.md字段，四图叠加推演剧情白描 |
| pop-fanqie-write | v8.0.0 | 减法版，移除8项内置风格倾向，笔触层移交DNA三态协议 |
| pop-fanqie-review | v4.1.0 | 同步write v8.0.0，2b技法落地改笔触DNA一致性检查 |
| pop-dna-style | v1.0.0 | 新建，笔触DNA供给方，双档位+场景定向采样 |
| pop-research | v1.2.0 | 新增采风级档位，pipeline Phase 0引用（同赛道推荐书单） |
| pop-decon | v20.1.0 | 入库改本地沉淀 |
| pop-shared-dna | v4.1.0 | 老管线文风DNA引擎，服务pop-qidian-write |
| tool-download-webnovel | v7.0.0 | 三阶段SOP，web搜索兜底 |

---

## 7. 已知限制与待解决项

- **project-state.md 跨对话续接**：当前 project-state.md 落盘到项目本地，agent 每次对话需手动读取。平台层是否自动注入 project-state.md 到对话上下文尚未对接
- **pipeline 路由依赖 agent 自觉**：pipeline 只定义了路由规则，但路由执行靠 agent 读 project-state.md 后自行判断。若 agent 跳过读 state 直接调 skill，路由规则将失效。尚未有强制路由机制
- **DNA 融合**：想把多本书的文风 DNA 融合（如深渊主宰的数据看板+玄鉴仙族的笔触）尚未支持，当前一笔触 DNA 对应一本参考书
- **对话趋同**：同一笔触 DNA 驱动不同剧情时，对话节奏可能趋同，尚未有差异化机制
- **字数弹性**：write v8.0.0 移除了感官连续/情绪连续的字数限制后，字数控制有波动，当前靠 agent 尽力控制，无硬约束
- **pop-dna-style 档位 B**：剧情 DNA brief 的消费方（seed/plot）尚未内置加载逻辑，当前需手动注入
- **横切 skill 调度**：pop-research 仍是被调用方——由 seed/plot/write 在遇到信息缺口时按需调用，但没有强制触发规则。pipeline v1.0.0 只接管了 Phase 0（pop-research 推荐书单场景），Phase 1-4 中的 pop-research 调用仍是自由触发
