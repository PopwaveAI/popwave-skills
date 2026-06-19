---
name: expert-writer
description: "当用户说'开书/拆书/设计剧情/写正文/审稿/继续/下一步'时启用。自动路由到对应子Skill，产出子Skill的完整执行结果。"
version: 3.4.0
pipeline: { up: [], down: [pop-writer-creative, pop-writer-reservoir, pop-writer-world, pop-decon, pop-writer-plot, pop-writer-chapter, pop-writer-prose, pop-writer-qa, pop-shared-dna, pop-writer-character, pop-writer-html, pop-writer-game, pop-shared-reader, pop-shared-html, tool-download-webnovel, tool-cnovel-research, tool-opinion-tracker] }
---

# expert-writer

> 网文创作元 Skill（专家模式）。Think → Execute → Reflect 三层工作流：自动识别创作意图并路由子 Skill，集成修改路由（三层联动影响评估）、决策点闸门（人必须在场的拦截点）、完成后引导（基于项目文件状态的跨轮引导）。

## 管线全景

```
[开书]     [注入素材]       [构筑世界]      [设计剧情]       [设计章节]      [写正文]    [质检]
creative  → reservoir  →  world  →  plot v7.0  →  chapter v2.0  →  prose  →  qa
 ↑            ↑               ↑
Phase R      剧情储备卡格式   L1+角色+数值
→爽点引擎    （9步注入）      +起点快照+宪法
→A/B/C
→PRD
→故事引擎
→样品
```

下游路由必须验证**全链前置条件**：进入 plot 前先确认 world 已产出 + reservoir 有卡 + trope-library 已查。遗漏 = 项目B 事故（跳过了 reservoir 和 world，creative 直接到 world 手动摸路）。

## 管线stage顺序表（全链路合同）

此表是写作专家全链路的**单一真相源**。每次阶段交接时**必须查询此表确定下一步**，不依赖子 skill 的 pipeline 字段（因为子 skill 的 pipeline 只声明相邻关系，不声明全链顺序——6.18项目B事故的直接根因）。

| 步骤 | Skill | 产出 | 前置条件 | 完成后检查 |
|:----:|:------|:-----|:---------|:-----------|
| 1 | pop-writer-creative | 爽点引擎+PRD+故事引擎+样品 | 无 | creative 产出全部到位? |
| 2 | pop-writer-reservoir | 剧情储备卡(含安全门禁通过) | PRD+故事引擎已产出 | 安全门禁已执行? 储备卡格式完整? |
| 3 | pop-writer-world | L1+角色+数值+宪法+升级表 | creative+reservoir 已产出 | world 落盘检查点全通过? |
| 4 | pop-writer-plot | 卷定位+剧情线+幕+锚点+枪链 | world+reservoir+trope-library 已就位 | plot 六步全完成? |
| 5 | pop-writer-chapter | chXXX-设计包 | plot 全部产出 | 设计包容情绪弧/爽点/钩子/枪链? |
| 6 | pop-writer-prose | 正文 | chapter-design 已产出 | 正文已落盘? |
| 7 | pop-writer-qa | QC报告 | prose 已产出 | — |

**使用规则**：
1. **不查此表就跳阶段 = 项目B事故**。从 Step N 完成到 Step N+1 启动之间，必须先查此表确认 N+1 是什么，再加载 N+1 的 SKILL.md。
2. **从表推断自己的位置**：首次加载时扫描项目文件，看最后一个阶段产出物存在于哪个 step 的路径中，从表中定位当前位置。如果同时有多个阶段产出物，以最后修改时间戳为准。
3. **同人/跨界融合项目**：在 creative 完成后、reservoir 执行前，执行 `references/derivative-gap-analysis.md`（同人场景）或 `references/dynamic-fusion.md`（跨界融合）。此检查插入 Step 1→2 之间。

## 速查表

| 用户说 | 路由到 | 前置条件 | 本阶段不做什么 |
|--------|--------|---------|--------------|
| "开新书/启动项目/设世界观" | pop-writer-creative | 无。自动按流程走: Phase R → ★ Phase 爽点引擎(共创元爽点) → A/B/C分支 → PRD → 故事引擎 → 样品 | 产完后应调起 reservoir 产出剧情储备卡，而非 creative 自己手写储备池 |
| "注入素材/融进书里/帮我把XX加进去" ★NEW | pop-writer-reservoir (v2.1.0) | 项目已有 PRD.md + 故事引擎.md + 素材储备池.md（即已跑过 creative 阶段）| 不修改 PRD/宪法/故事引擎（仅标注冲突）|
| "构筑世界观/建世界/设定力量体系" ★NEW | pop-writer-world | 必须先完成 creative（有故事引擎+样品签字）| 不设计剧情线（那是 plot v7.0 的活）|
| "拆这本书/分析这本书/拆解" | pop-decon | 若 TXT 未下载 → 先调 tool-download-webnovel | 不写正文（那是 prose-render 的活） |
| "设计剧情/规划大纲/情绪弧线" | pop-writer-plot (v7.0 重构) | 必须先完成 world(L1+角色+数值) + reservoir 有剧情储备卡可用 + trope-library 已查 | 不设计章级细节（那是 chapter-design 的活）。新6步流程: 卷目标→拉种子+配套路→剧情线独立.md→分幕→章锚点→契诃夫枪链 |
| "设计第X章/章纲/骨架" | pop-writer-chapter (v2.0 升级) | 必须先完成 plot v7.0(剧情线设计文档 + 幕锚点 + chekhov-tracker) | 不纠结渲染用词（那是 prose-render 的活）。设计包含情绪弧/爽点机制/钩子回收/契诃夫枪/对白潜台词 |
| "写第X章/渲染这章/上色/写正文" | pop-writer-prose | 必须先完成 chapter-design | 不判断剧情逻辑（那是 QA 的活） |
| "从第X章开始写N章/批量写N章/风格迁移N章" | pop-writer-prose + 并行委托（delegate_task） | 源文本存在（原文或设计包）→ 若无设计包，从原文提取事件链创建复合设计包（N章合1文件或逐章独立）→ 然后并行渲染。详见 references/batch-style-migration.md | 不逐章走 creative→plot→chapter 流水线 — 批量场景走旁路 |
| "审查/审稿/QA/检查质量/看看" | pop-writer-qa | 无（可随时触发） | 不直接改正文（问题标记后由上游修复） |
| "快速检测/检查项目状态/健康检查/看看进度/看看差什么/查一下" ★NEW | project-health-check（本地模式）| 项目目录存在 | 不产出文件。报告对话内输出，按需更新项目总控.md |
| "chNNN / 第N章"（如"ch002""ch03""第8章" — 紧接在上一章产出后的裸章号） | pop-writer-prose（精简模式） | 上一章正文存在 + entity-snapshot 章号连续 | 不暂停确认，不绕回 creative/plot/chapter — 直接读设计包渲染 |
| "分析文风" | pop-shared-dna | 需有成文样本 | — |
| "设计角色储备" | pop-writer-character | 无 | — |
| "继续/下一步/继续任务" | 检查 progress.next_skill | 若 ready=true → 执行；若 ready=false → 设为 true 后执行 | — |
| "调研/什么火/社区" | tool-cnovel-research | 无 | — |

精简模式开关：用户说"直接写/快一点/跳过解释/后面不用问我了"或裸章号（"ch002""ch03""第8章"）→ 少解释、多执行、**后续流程不暂停等待确认**，持续执行到完整产出或遇到必须用户介入的错误。用户说"/pop-writer-prose"或"继续下一章" = 同上，直接执行不请示。

## 红线

| # | 红线 |
|:-:|:-----|
| 1 | **不读子 SKILL.md 就路由** → 必须先 `Get-Content -Encoding UTF8 -Raw` 目标子 skill 的全文 |
| 2 | **entity-snapshot 过期仍续写** → 先检查最后更新章号 vs 当前目标章号。脱节 → 提示用户 |
| 3 | **决策点跳过用户确认** → 4 个闸门必须等待用户点头（bookstrap/plot/chapter-design/prose-render） |
| 4 | **管道前置条件不满足硬跳** → 上游产出物缺失时告知用户缺什么，不直接跳过 |
| 5 | **子 skill SKILL.md 找不到** → 终止，静默跳过 = 违规 |
| 子 skill 文档读取 | 每次路由 | 统一 ``Get-Content -Encoding UTF8 -Raw``。>25K 回退 Read+offset |
| **workspace-index.yaml 不存在** | **会话恢复/继续任务时** | **先调 ``references/project-state-discovery.md`` 从文件系统推断阶段，再初始化索引** |
| 7 | **长文产出全量贴入对话** — 文件写入后对话中只留摘要（≤ 200 字）。正确格式：`已写入 {路径}。摘要：{核心内容一句话}。` **非写入产出（Gap 分析/阶段总结/对比报告等正文型汇报）≤ 500 字，表格型 ≤ 300 字。超过 → 写入独立文件，对话只留摘要指针。** |
| 8 | **delegate prose 任务时不传委托协议** — 父agent delegate 前未加载子 skill 的 step-0-delegation-contract.md → 凭自己理解过滤指令写 context → 子agent缺失关键约束（上下章衔接/剧情不变门禁/角色不可篡改）→ 输出偏离原文剧情。正确做法：先加载子 skill 的 step-0-delegation-contract.md → 按 D1-D6 自检清单准备路径矩阵+门禁+连续性摘要 → 6项全通过才 delegate。详见 references/batch-style-migration.md §Step 3。 |

## 核心流程

| Step | 做什么 | 详细文档 |
|:-----|:-------|:---------|
| 1. Think | 感知项目状态 + 意图识别 + 管道前置校验 | `steps/step-1-think.md` |
| 2. Execute | 加载子 Skill + 决策点闸门 + 按 SOP 执行 + 修改路由 | `steps/step-2-execute.md` |
| 3. Reflect | 四层审视 + 索引回写 + 状态协议校验 + 完成后引导 | `steps/step-3-reflect.md` |

## 典型错误

1. **跳过管线检查直接写正文**：用户说"写正文" → agent 没检查 plot→chapter-design→prose-render 管线 → 缺失上游产出物。正确做法：检查上游产出物 → 缺失则路由到缺失 skill。
2. **凭记忆判断子 skill 内容**：agent 跳过 Get-Content → 版本不一致产出格式不匹配。正确做法：每次都 Get-Content 最新版本。
3. **entity-snapshot 脱节仍续写**：entity-snapshot 最后更新 ch05，用户要写 ch08 → agent 基于 ch05 续写 → 角色状态脱节。正确做法：检查快照章号 vs 目标章号 → 脱节则提示用户。
4. **方向sketch 全被拒仍硬推进 world**：用户的创意方向未锁定 → agent 引导进入世界构建 → 浪费 work。正确做法：退回 pop-writer-creative Phase 0 重新碰撞。如果已拒 2+ 轮 → 引导缩小范围到单个场景而非完整方向。
5. **同人二创不做 gap 分析直接进 plot**：基于源作品的二创 → creative 阶段的 L1 六件套产出后 → agent 直接进 plot 卷设计 → 漏了对照源作品 deconstructor 产出补齐设定层差异 → 剧情设计基于有 gap 的设定展开，后续返工成本高。正确做法：在 creative 完成后、plot 开工前，执行 `references/derivative-gap-analysis.md` 中的双层 gap 分析（设定层 1:1 对齐 → 设计层用户确认）。
6. **非写入产出未做摘要化**：Gap 分析 / 阶段完成总结完整贴在对话中（1,700+ chars），挤占上下文窗口。正确做法：正文型汇报 ≤ 500 字，表格型 ≤ 300 字。完整内容写入独立文件，对话只留指针+摘要。
7. **子 skill 的 step 文件未加载，凭记忆执行 SOP**：加载子 skill 时只调了 skill_view(name) 读 SKILL.md 描述，没有逐个调 skill_view(name, file_path="steps/step-*.md") 加载具体的步骤文件。凭 SKILL.md 速查表执行 → 遗漏 step 文件中的具体规则（如 chapter Step 2 要求的 scene/POV/关键对白/数据四字段、prose Step 3 的文本脉冲密度检查）。正确做法：路由到子 skill 后，列出其 steps/ 目录，用 skill_view 逐个加载所有步骤文件，确认完整了解执行指令后再开工。
8. **skill_view 截断未被发现**：skill_view 返回的内容可能少于文件实际大小（如 L1-06.tpl.md 210 bytes 只返回 98 chars）。未交叉校验返回字符数 vs 文件实际大小 → 基于不完整指令执行。正确做法：skill_view 加载文件后，将返回内容的字符数与 `(Get-Item '{path}').Length` 对比。如果明显偏短 → 标记 "⚠️ 截断"，回退用 Read 工具重新读取。
9. **批量写作时用单章流水线逐章串行**：用户说"从ch01写10章" → agent 走 pop-writer-prose 的 Step 0→1→2→3→4 循环 10 次 → 耗时数小时。正确做法：识别批量意图 → 创建复合设计包（N章事件链合并）→ 用 delegate_task 分发给 N 个子 agent 并行渲染。详见 references/batch-style-migration.md。

10. **search_files 截断导致虚假结论**：用 search_files 发现设计包/章节目录时，返回50条截断结果（truncated: true），未做后续精确搜索就下结论说"没有ch01"。正确做法：每次 search_files 返回 truncation=true 时，先做精确搜索 (search_files pattern='ch001*') 确认目标是否存在。在确认前不说"没有"。

12. **参考素材结构复制而非设计哲学借鉴**：写样品/剧情线时从让魔门再次伟大的套路库或设计包中参考"死后金手指觉醒"模板 → 产出结构上过于相似（上线背叛→死后觉醒→布局复仇的三段式）。正确做法：从参考素材中**提取设计哲学而非拷贝结构**。读套路库的"核心张力"和"运作机制"段，理解为什么这个模式让读者爽，再自创差异化结构。问自己："如果让魔门是用A方式实现这个模式，我的书里还能用B/C/D什么方式？"

## 边界条件

| 场景 | 触发条件 | 动作 |
|:-----|:---------|:-----|
| 子 skill 文档读取 | 每次路由 | 统一 ``Get-Content -Encoding UTF8 -Raw``。>25K 回退 Read+offset |
| **workspace-index.yaml 不存在** | **会话恢复/继续任务时** | **先调 ``references/project-state-discovery.md`` 从文件系统推断阶段，再初始化索引** |
| SKILL.md 找不到 | 文件不存在 | 终止 + `SKILL.md 不存在` |
| 子 agent 不可用 | 环境不支持 | 声明 `master 手动执行` 在前 |
| 执行失败 | 任意异常 | 通知用户 + 原因 + 可操作建议 |
| 前置条件缺失 | 上游产物不存在 | 告知缺什么，建议调用前置 skill |
| 无法匹配路由 | 用户消息无匹配 | Think 追问补全信息 |
| 用户要跳步 | 用户明确表示 | 说清代价，给两个选项。确认后立即切换 |
| 未加载子 skill | agent 跳过加载 | 必须先加载再执行。跳过 = 退回 |
| 越界检测 | 当前阶段出现下一阶段内容 | 说"这属于 [X] 的范围，到那一步处理。先完成当前阶段。" |
| **同人二创路由** | 用户说"基于《XXX》写同人/衍生/跨界融合，主角替换为YYY" | 路由到 pop-writer-creative 时标注 `mode: fanfic`，触发其 Phase 0 分支 B（跳过方向sketch碰撞，直接锚点书解析+元素叠层）。creative 完成后 → 参考 `references/derivative-gap-analysis.md` 做双层 gap 分析再进 plot |
| **方向被拒退回** | 用户否定全部方向sketch，且仍在 creative 阶段 | 强制退回 pop-writer-creative Phase 0，不引导进入 world 阶段 |
| **裸章号续写** | 用户回复仅含章号（"ch002""03""第8章"），且上一轮刚产出对应章节的正文 | 路由到 pop-writer-prose 精简模式，不暂停确认，直接读设计包渲染。注意检查 entity-snapshot 章号连续性和上一章正文存在性。 |
| **批量风格迁移** | 用户说"用XX风格从ch01写N章/风格迁移N章/改写成XX风格" | 源文本存在（原文txt或已有正文）→ 不走 creative→plot→chapter 管线。直接读原文逐章提取事件链 → 创建复合设计包（N章合1）→ delegate_task 分发给子 agent 并行渲染（每批 5 章）。详见 references/batch-style-migration.md |

## 落盘检查点

每次子 skill 执行完成后必须确认：
- 产出物文件已写入且路径正确
- workspace-index.yaml 已更新（file_registry / runtime / progress / change_log）
- **项目总控.md 已更新**（管线进度标记、当前阶段、关键产出索引、待处理风险）
- entity-snapshot.yaml 与章文件数一致
- 角色卡快照与 entity-snapshot 一致

## 核心原则

### 上瘾优于工程（2026-06-18 实战沉淀）

本会话的核心教训：**管线优化必须优先回答"这怎么让读者停不下来"，而非"这怎么让输出更规范"**。

v3.2 管线升级了情绪弧可视化、爽点机制表、契诃夫枪链、剧情线独立文档——这些都是"工程质量"，不是"上瘾设计"。用户一针见血指出了问题："网文核心是要爽，你给的方案爽在哪里？"

| 问题 | 正确的第一追问 |
|:-----|:--------------|
| "这个PRD写得好不好" | **"这书第一章就要让人睡不着吗？"** |
| "剧情线设计完整吗" | **"读者为什么会一章接一章停不下来？"** |
| "套路链搭配合理吗" | **"连续5章分别是哪几个元爽点的变体？"** |
| "幕划分合理吗" | **"每幕结束时的钩子让读者想立刻点下一章吗？"** |

回答不上的时候，不要继续优化"结构"——回头想"爽感"。

### 升级优先于新建（2026-06-18 实战沉淀）

本会话的教训：当需要增强管线能力时，**优先升级现有 skill，不新增 skill**。让魔门再次伟大拆书成果也证明了——更好的产出来自更丰富的 craft 层（升级现有 skill），而非新增功能节点。

| 场景 | 应做 | 不应做 |
|:-----|:-----|:-------|
| plot 需要剧情线文档而非 Canvas | 升级 plot | 新建 "plot-line-designer" skill |
| 设计包需要情绪弧/爽点/钩子 | 升级 chapter-design | 新建 "design-enricher" skill |
| 套路库需要 full craft recipe | 升级 trope-library | 新建 "trope-crafter" skill |
| 素材需要剧情储备卡格式 | 升级 reservoir | 已吸收 fuse 不另开 |

核查：每次想"新建"之前，先问——**现有哪个 skill 可以升级来完成这个需求？**

## 版本

v3.4.0 | 2026-06-19 | 项目全貌修复：项目总控模板追加理想文件树（对照PRD附录A）+ 健康检查Step 0新增无文件时自动初始化+Step 1b改为文件树比对。详见本行展开。
| 子项 | 改动 |
|:-----|:------|
| pipeline-manifest.md | 新建，管线硬顺序合同+截断检测协议 |
| project-master-control.tpl.md | 新建，含管线进度+执行顺序日志+理想文件树+产出索引+风险 |
| project-health-check.md | 新建，三优先级连续性检测+自动初始化+文件树比对+截断风险扫描 |
| step-1-think.md | 新增截断检测协议+管线锚定流程（加载manifest+比对项目总控+管线断裂检测） |
| step-2-execute.md | 强制加载段新增截断交叉校验 |
| step-3-reflect.md | 新增项目总控回写（含执行顺序日志+首创初始化） |
| SKILL.md | 速查表新增快速检测路由行，落盘检查点新增项目总控更新 |
v3.2.0 | 2026-06-18 | 更新 plot/chapter 路由表(v7.0/v2.0)；新增"升级优先于新建"原则。参考让魔门再次伟大拆书成果。

v3.1.4 | 2026-06-16 | 精简模式扩展：用户说"后面不用问我了"→不暂停执行；新增典型错误#10（search_files截断导致虚假结论）

v3.1.2 | 2026-06-16 | 新增批量写作/风格迁移路由+典型错误9+边界条件"批量风格迁移"，新增 references/batch-style-migration.md

v3.1.1 | 2026-06-14 | v5 结构重构：SKILL.md 瘦身至 ≤120 行，Think/Execute/Reflect 拆分至 steps/，红线表格化，pipeline 字段补全