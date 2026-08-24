---
name: pop-qidian-pipeline
description: 起点管线总控。当用户说"管线""pipeline""继续写""下一步""导入""续写"时启用。读项目总控.html→按Phase 0-6路由调度各子skill（seed/world/character/plot/write/review）。
---

# pipeline

> 起点管线总控。Phase 0→6路由调度。v3.16.0：Phase 5 改派发子agent执行write（派发指令硬清单+验收门禁查文件系统不信口头），红线4从"主agent直接执行所有step"翻案为分环执行模式。v3.15.0：step2 路由循环合入 SKILL.md（每次对话零跳转自包含），HTML 更新协议下沉 `references/html-update-protocol.md` 单源化（原 step0/step1/step2 三处字段表归一）。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

---

## 做什么

pipeline只做路由不干活——读项目总控.html判断phase→路由到对应子skill→完成后更新html。不写正文、不创意、不审核、不提取DNA。

输入：项目名或当前项目目录（mode=fresh/import/resume）
输出：标准化目录结构 + `项目总控.html`（唯一状态文件）

---

## 怎么操作（SOP骨架）

1. **Step 0**（导入/续写）→ `steps/step0-import.md`：资产清点→文件归位（不做内容转换）→调度skill reconstruct补跑→落地Phase决策。当用户说"导入/续写/已有"或目录已有文件时触发
2. **Step 1**（初始化）→ `steps/step1.md`：创建8个子目录+生成项目总控.html+自检
3. **Step 2**（路由循环·每次对话）→ **直接执行本文件下方「路由循环」节**，html 更新操作按 `references/html-update-protocol.md` 执行

### 路由循环（每次对话开始时）

1. 用Read读取项目根 `项目总控.html`，从 `<!--STATE:xxx -->` 标记提取 phase 值、chapter 值、next_step
2. 对照下方「Phase调度表」路由到对应Phase执行（skill红线以其自身SKILL.md为唯一源，本文件不复述）
3. Phase完成后按 `references/html-update-protocol.md` 更新html（通用字段+phase circle+badge+产出表），再回到第1步判断下一步

### Phase调度表（路由+调度卡合一）

| Phase | skill（执行体） | 前置/门禁 | 输入 | 产出 | 完成后动作 |
|:--|:--|:--|:--|:--|:--|
| 0-Stage1 | 主agent深问四层（赛道/标签/参考书/现有设定） | state=init/phase0 | — | 素材/用户意图.md | 进Stage2 |
| 0-Stage2 | ①tool-download-webnovel→pop-qidian-research(decon-lite)→pop-dna-style（串行） ②seed Step1-3交互并行 | Stage1完成；参考书txt存在否则报错中止 | 用户意图.md | 素材/（赛道调研.md+文风锚定.md v1+decon-lite-{书名}.md+downloads/{书名}.txt） | badge deck_0-4→✅ |
| 1 | pop-qidian-seed（Step1灵感→Step2种子碰撞→Step3立项PRD定型） | 灵感就绪+产出真实性门禁通过 | 素材/灵感收集.md+用户意图.md+赛道调研.md+decon-lite（如有） | 立项/01-立项PRD.md（六要素） | badge prd_0→✅+创意摘要更新→Phase 3 |
| 3 | pop-qidian-world（step0-decision→step0.5-skeleton→step1-flesh[含3个part]→step2-fullbook→step3-output） | PRD六要素就绪 | 立项PRD+设计/世界决策表.md | 设计/力量体系.md+动力引擎.md+全书设定/（10个闭环文件） | badge skel_0/skel_1/flesh_0→✅→Phase 3→3.5 |
| 3→3.5 | pop-dna-style（Stage 2，steps/step5-synthesize.md） | 全书设定就绪 | 文风锚定v1（如有）+全书设定（战斗系统/物理规则/民风民俗/世界设计原则）+用户意图+决策表+力量体系+PRD | 素材/文风锚定.md v2（覆盖v1） | badge deck_3标"v2-综合产出"+flesh_1→✅→Phase 3.5 |
| 3.5 | pop-qidian-character（step0决策→step1金手指+角色库） | 全书设定+力量体系+动力引擎就绪 | PRD人物方向句+力量体系+动力引擎+全书设定各卷切片+角色库决策表 | 设计/金手指.md+设计/角色库/角色库.md | badge prot_0/flesh_2→✅→Phase 4 |
| 4 | pop-qidian-plot（step0决策→step1-3主线+卷纲+章锚点表） | PRD+全书设定+角色库+金手指就绪 | PRD起因/经过/结果方向句+力量体系+动力引擎+各卷切片+角色库+金手指+卷纲决策表 | 设计/主线.md+第一卷剧情/卷纲.md+章锚点表.md | badge main_0/flesh_3→✅、chapter→ch002→Phase 5 |
| 5 | pop-qidian-write（v4.2.0起**派发子agent执行**，主agent只做：核对输入路径→按write SKILL.md「派发指令硬清单」组装指令→派发→验收门禁） | 卷纲+章锚点表+角色库+current_chapter存在 | 派发指令硬清单（章节号+输入文件逐项路径+落盘三件+回报格式） | 正文/chXXX.txt+产出/白描卡/chNNN.md+状态快照.md | phase→phase6。**验收门禁：主agent查文件系统不信口头（正文≥1800字+白描卡新建+快照更新），缺任一幂等重派**。不得连续写两章不review |
| 6 | pop-qidian-review（四步审核，结论对话内输出，Step 4核对修正沉淀） | 正文/chXXX.txt存在 | 正文 | 白描卡/状态快照核对修正（write已产出） | 通过→phase5+chapter+1；打回→phase5重写本章 |

### Reconstruct 调度卡（导入模式用）

| 任务 | skill | 模式 | 产出 |
|:--|:--|:--|:--|
| 旧稿审核重建 | pop-qidian-review（steps/step-reconstruct.md） | reconstruct | 产出/白描卡/（采样章节）+ 产出/状态快照.md |
| 设计文档补跑 | {对应skill} | reconstruct（只校验+补全，不覆盖已有内容） | 该skill标准产出文件（标注source: skill-reconstruct） |

### 门禁链（Phase推进条件）

- Phase 0 → Phase 1：底牌就绪（用户意图+赛道调研）+ **产出真实性门禁**（decon-lite包含≥3处原文段落引用 + 文风锚定包含≥500字原文采样片段；用户跳过拆书则跳过此项，但PRD标注"无拆书参考"）
- Phase 1 → Phase 3：seed立项PRD就绪（六要素齐全）
- Phase 3 → Phase 3.5：全书设定+力量体系+动力引擎就绪
- Phase 3.5 → Phase 4：角色库+金手指就绪
- Phase 4 → Phase 5：主线+剧情白描+章锚点表就绪
- Phase 5 → Phase 6：正文产出
- Phase 6 → Phase 5（通过→下一章 / 打回→重写本章）

### Phase 0 详细规则

- **Phase 0-1并行设计**：Stage1深问完成后，拆书任务和seed Step 0交互同时推进。S0前置收集+S1世界构筑仅需用户意图.md，不依赖拆书结果，可立即开始。S2力量体系设计消费拆书结果（decon-lite表1/表9），需等拆书完成或用已有信息先生成选项。主agent在seed交互间隙执行拆书任务。
- **执行顺序**：下载完成→主agent依次执行dna-style和decon-lite（串行，非并发）；赛道调研独立第一优先级执行。
- **产出真实性门禁**：进入Phase 1前必须验证拆书产出基于真实原文，而非记忆/书评/评论重构。检查项：①decon-lite产出包含≥3处原文段落引用（非摘要复述）②文风锚定产出包含≥500字原文采样片段。未通过=Phase 0未完成，禁止进入Phase 1。
- **下载失败中断机制**：下载任务返回失败后，**禁止**执行decon-lite和dna-style。必须向用户报告并给三选项：①换一本可下载的参考书 ②用户手动提供txt路径 ③跳过拆书（seed基于通用知识生成，需用户确认接受质量降级）。用户未决策前拆书分支暂停，seed交互分支可继续。

### Phase 1-4执行模式：主agent直接执行所有step（Phase 5 除外，见红线4）

Phase 1-4在进入自动生成前，必须先完成Step 0交互式决策。核心轮用户确认后，进入执行型step，由主agent直接执行。**Phase 5 写正文是重任务，不适用本模式——必须派发子agent执行（见调度表+红线4+write SKILL.md「执行模式」节）。**

| Phase | Step 0交互轮次 | 核心必答/可选 | 决策表产出 | 完成后执行 |
|:--|:--|:--|:--|:--|
| 1 seed | Step1-3（灵感问答→种子碰撞+六要素PK→立项PRD定型） | Step2-3核心必答 | 立项/01-立项PRD.md | 主agent直接执行Step3立项PRD定型 |
| 3 world | Step0 W1-W2（2轮）+ Step0.5展开力量体系+动力引擎 | W1核心必答+W2可选 | 设计/世界决策表.md | 主agent直接执行step0.5-3 |
| 3.5 character | C1-C2（2轮） | C1核心必答+C2可选 | 设计/角色库/角色库决策表.md | 主agent直接执行金手指+角色库生成 |
| 4 plot | R1-R5（5轮） | 前3轮核心必答+后2轮可选 | 设计/第一卷剧情/卷纲决策表.md | 主agent直接执行主线展开+step1-3 |

**Phase 3.5 Character必须执行**——world完成后必须经过character建角色库，plot和write才能消费角色库。

**统一执行流程**：主agent读取目标skill的SKILL.md+对应step文件 → 提取红线+操作要点（红线以子skill SKILL.md为唯一源） → 消费输入文件 → 按SOP执行落盘 → 检查产出 → 更新项目总控 → 衔接下一步。

---

## 📦 可调度 Skill 清单（素材表）

> 本 pipeline 整个专家入口与调度器，可调度的子 skill 总清单如下（与 `skill.json` 的 `skills` 数组一致）。这些 skill 按 Phase 调度表调度，**部分 skill 会被其他专家复用**（如 `pop-dna-style` / `pop-research` / `tool-download-webnovel`）。

| Skill | 定位 | 何时调用 |
|:--|:--|:--|
| `pop-qidian-seed` | 立项创意（六要素立项PRD） | Phase 0-1 |
| `pop-qidian-world` | 世界构筑（全书设定） | Phase 3 |
| `pop-dna-style` | 文风综合重构（笔触/画风/需求） | Phase 3→3.5 |
| `pop-qidian-character` | 角色库 | Phase 3.5 |
| `pop-qidian-plot` | 卷纲+章锚点 | Phase 4 |
| `pop-qidian-write` | 正文渲染 | Phase 5 |
| `pop-qidian-review` | 审核+沉淀 | Phase 6 |
| `pop-research` | 赛道调研/decon-lite/采风 | Phase 0 |
| `tool-download-webnovel` | 下载对标书 | Phase 0 |

---

## 🚪 首次对话引导（onboarding）

> 用户第一次触发起点网文专家（无任何写作项目、非续写场景）时，**先输出 `references/onboarding-guide.md` 的引导语内容**给用户建立认知，再进入 Step 0 意图深问。
>
> 展示方式：在回复中**直接粘贴 `references/onboarding-guide.md` 全文**（声明本次为功能介绍+引导、未执行 skill 任务），用 1-2 句口头补充"报书号+想法就开始"。若用户已明确要开做，可跳过引导直接干活。

---

## 红线

1. **读取协议**：每次对话第一件事读项目总控.html获取当前phase→按调度表路由；每次Phase完成后必按 `references/html-update-protocol.md` 更新html。禁止跳过读html直接干活。
2. **pipeline只做路由不干活**——所有产出由下游skill生成。pipeline不直接写正文/创意/审核/提取DNA。
3. **三层骨架依赖链不可跳过**——骨架没就绪不进主角层，主角没就绪不进血肉层，血肉没就绪不写作。
4. **分环执行模式**——Phase 1-4（设计层：交互决策+文档生成）由主agent直接执行step；Phase 5 写正文为重任务，**必须派发子agent执行**（主agent直写会背着全项目历史干重活→会话膨胀→compaction崩溃→expert配置丢失）。派发方职责：核对输入路径存在→按write SKILL.md「派发指令硬清单」组装指令（章节号+输入文件逐项路径+落盘三件+回报格式）→派发→**验收门禁（查文件系统不信口头：正文≥1800字+白描卡新建+快照更新，缺任一幂等重派，先查半成品防覆盖）**。子agent没有项目上下文，输入路径必须硬清单给出。

---

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `SKILL.md` | 每次对话必读 | 管线骨架+路由循环+Phase调度表+门禁链+红线 |
| `steps/step0-import.md` | 用户说"导入/续写/已有"或检测到已有文件时 | 资产清点→文件归位→调度skill reconstruct→落地Phase |
| `steps/step1.md` | 初始化时（state=init且无已有文件） | 目录创建+项目总控.html生成+自检 |
| `references/html-update-protocol.md` | phase完成后更新html时（含step0重建/step1初始化） | STATE字段SearchReplace规范+Phase ID表+badge表（单源） |
| `references/onboarding-guide.md` | 用户第一次触发专家时 | 首次对话引导语 |
| `templates/项目总控.html` | 初始化时读模板 | 状态文件模板 |
| `项目总控.html`（项目空间） | 每次对话第一件事 | 唯一状态源（phase+next_step+就绪状态+产出表） |
