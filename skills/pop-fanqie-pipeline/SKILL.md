---
name: pop-fanqie-pipeline
description: "当用户说'初始化项目/管线总控/番茄pipeline/导入/续写'时启用。Phase 0→5全链路安装，项目空间标准化，状态.md为唯一机器状态源，html为可选展示面板。"
---

# pop-fanqie-pipeline

> 番茄管线总控。Phase 0→5全链路安装，pipeline只做安装/导入、不常驻路由。v4.2.0：日常路由上移专家提示词；状态源统一为 状态.md（唯一机器状态源），html仅供展示、agent不读。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

## 做什么

输入：项目名或当前项目目录。mode=fresh（从零开始）/import（导入已有设定）/resume（续写已有正文）
输出：标准化目录结构（素材/设计[全书设定/角色库/第一卷剧情]/正文/审核）+ 状态.md（机器读，唯一状态源，含mode/phase/current_chapter/底牌就绪）。总控.html 是供老板查看的可选展示面板（按需导出，不参与任何路由/决策）

pipeline不写正文、不创意、不审核——只负责把agent指向正确的phase和skill。所有下游skill由pipeline按phase调度。

**执行模式**：主agent直执——路由决策/状态.md管理/Phase 0用户意图深问/导入模式资产确认均为对话内主agent工作；子agent派发点已内置在Phase调度表（Phase 0 Stage2调研并发、Phase 4 write必须子agent），不另造派发点。

## 怎么操作（SOP全内联）

> execution.mode: 串联式 | 强保障：本SKILL.md由host层强制注入（SOP全内联） | 弱保障：references/scripts/templates需agent主动读取，设计时假设可能没读到

- **Step 0** 导入/续写模式 → 见下方「Step 0 导入/续写模式」节（检测已有资产→缺口分析→落地Phase→状态重建→正文反推。用户说"导入/续写/已有"或目录已有文件时触发）
- **Step 1** 初始化项目目录+状态.md → 见下方「Step 1 初始化项目」节（创建四文件夹+state=init。**如果检测到已有文件→重定向到Step 0**）
- **Step 2** 日常路由 → 见下方「日常路由」节（已上移专家提示词，pipeline 不常驻）

### Step 0 导入/续写模式（资产标准化→重建状态→路由）

> 触发条件（任一）：①用户明确说"导入/续写/已有/接续/迁移" ②Step 1初始化时检测到`正文/`或`设计/`已有文件 ③项目目录已有内容但无状态.md。
> 核心理念：不是"检测+跳Phase"，而是"检测→标准化转换→补缺→路由"的完整初始化过程。

**0a 资产扫描**：LS扫描项目目录（或用户指定源目录），输出**原始资产清单**（文件名+位置+内容摘要1句话）。

**0b 资产标准化转换**（核心步骤：将非标准文件转换为标准文件名+标准目录位置+标准内容结构）：

0b-1 文件名+目录归位——按模糊匹配映射：

| 用户文件（模糊匹配） | → 标准位置 | 标准文件名 | 对应Phase |
|:--|:--|:--|:--|
| *意图*/*方向*/*想法*/用户口述 | `素材/` | 用户意图.md | Phase 0 |
| *调研*/*市场*/*赛道*/*排行* | `素材/` | 赛道调研.md | Phase 0 |
| *文风*/*DNA*/*笔触*/*风格* | `素材/` | 文风锚定.md | Phase 0 |
| *decon*/*拆书*/*力量分析* | `素材/` | decon-lite-{书名}.md | Phase 0 |
| *市场校准*/*对标* | `素材/` | 市场校准.md | Phase 1 |
| *创意*/*故事*/*纲领*/*简介* | `设计/` | 创意.md | Phase 1 |
| *力量体系*/*力量*/*体系* | `设计/全书设定/` | 力量体系.md | Phase 2 |
| *地图*/*地理*/*城市* | `设计/全书设定/` | 地图.md | Phase 2 |
| *势力*/*组织*/*帮派* | `设计/全书设定/` | 势力.md | Phase 2 |
| *危机*/*威胁*/*危险* | `设计/全书设定/` | 危机.md | Phase 2 |
| *配角*/*全书角色* | `设计/全书设定/` | 全书配角.md | Phase 2 |
| *各卷切片*/*卷设定* | `设计/全书设定/` | 各卷切片.md | Phase 2 |
| *剧情白描*/*大纲*/*分幕* | `设计/第一卷剧情/` | 剧情白描.md | Phase 3 |
| *角色库*/*NPC*/*角色* | `设计/角色库/` | 角色库.md | Phase 3.5 |
| *正文*/*章节*/ch*/第*章 | `正文/` | ch{NNN}.txt | Phase 4 |
| *流水账*/*快照*/*进度* | `审核/` | 剧情白描流水账.md（白描卡） | Phase 5 |
| *状态*/*当前状态*/*钩子台账* | `审核/` | 状态快照.md | Phase 5 |

操作要点：匹配不上的归"未分类资产"询问用户映射到哪个标准位置；非md文件（.docx/.txt/.json）先Read读取内容再Write写入标准位置；正文统一编号（`第一章.txt`/`chapter1.md`→`ch001.txt`）；询问用户是否保留原文件。

0b-2 内容结构标准化——逐文件对照 `references/import-structures.md`（弱加载，仅本环节读取）的16个标准文件分节结构补全缺失分节（结构正源在各子skill产出规范，冲突以子skill为准）。转换原则：保留用户原始内容不删除不篡改；用标准结构重新组织（加标准标题/分节标记）；缺失分节标"⏳待补"不编造。

→ 输出：**标准化资产清单**（每个文件标 ✅已标准化 / ⚠️部分标准化(缺分节已标待补) / ❌无法转换(需人工处理)）。

**0c 缺口分析**：标准化完成后对照依赖链逐Phase检查：

| Phase | 就绪判定 |
|:--|:--|
| Phase 0 | 用户意图.md+赛道调研.md 两者都有=✅ |
| Phase 1 | 设计/创意.md+正文/ch001.txt 两者都有=✅ |
| Phase 2 | 设计/全书设定/ 有文件=✅ |
| Phase 3 | 设计/第一卷剧情/剧情白描.md 存在=✅ |
| Phase 3.5 | 设计/角色库/角色库.md 存在=✅ |
| Phase 4 | 正文/ch*.txt 有正文=✅ |
| Phase 5 | 流水账+状态快照 双文件都有=✅ |

正文进度检测：`正文/`有文件→提取最大章节号（ch001~ch015→current_chapter=ch016下一章待写）。
→ 输出：**缺口报告**（哪些Phase已就绪/哪些缺失）。

**0d 落地Phase决策**（缺口报告+正文进度）：

| 条件 | mode | 落地Phase |
|:--|:--|:--|
| 正文有+双文件有（流水账+状态快照） | resume | Phase 4 续写下一章（状态完整直接接续） |
| 正文有+双文件缺 | resume | 先执行0f-1正文反推→Phase 4 |
| 正文无+Phase 3.5就绪 | import | Phase 4（write，设定+剧情+角色完整） |
| 正文无+Phase 3就绪 | import | Phase 3.5（character，缺角色库） |
| 正文无+Phase 2就绪 | import | Phase 3（plot，缺剧情白描） |
| 正文无+Phase 1就绪 | import | Phase 2（world，缺世界设定） |
| 正文无+Phase 0就绪 | import | Phase 1（seed，缺创意+首章） |
| 全无 | fresh | Phase 0 从零开始（走正常Step 1流程） |

→ 向用户展示 标准化资产清单+缺口报告+落地Phase建议，**用户确认后**进0e。

**0e 状态文件重建**：状态.md不存在→按「状态.md标准模板」创建；已存在→SearchReplace更新。mode/phase/current_chapter按0d决策填，已就绪Phase标[x]；已有素材对应底牌❌→✅/done/skipped。html展示面板**可选**：仅在用户要看可视化面板时按「state更新方法」运行脚本导出，日常不要求。

**0f 补缺生成**（按需，落地Phase前置依赖缺失时；有正文→从正文反推，无正文→标注待补由下游skill生成）：

0f-1 正文反推（`正文/`有文件 且 双文件任一缺失时）：读取已有正文（全部章节，量大时取最近5章+第一章）按章提取——
- 生成`审核/剧情白描流水账.md`（每章白描append，参考review流水账格式）：每章含 **白描**（3-5句叙事流：主角做了什么→冲突转折→结果留下什么）/ **信息差**（读者以为/角色以为/实际，如有）/ **涌现·角色状态**（新确立设定/关键角色状态变化，如有）/ **埋设钩子**（一句话，如有）/ **回收钩子**（标注埋设章，如有）。文首标注"导入反推生成，未经逐章review校验，需人工审核确认；导入完成后后续章节由review按章追加"。
- 生成`审核/状态快照.md`（replace，跨章状态）：未回收钩子台账（从流水账各章埋设钩子汇总的待回收伏笔，含信息差类型+预期回收）+ 角色当前状态表（最近几章关键活跃角色）+ 禁止漂移（正文已发生关键事实：人名/地名/阶位/已死角色/已废设定）。单章细节（白描）留在流水账，不写入状态快照。

0f-2 缺失设计文档补建（`正文/`有文件 但 `设计/`下关键文档缺失）：

| 缺失文档 | 补建方式 |
|:--|:--|
| 创意.md | 从正文提取故事核心→按创意模板分节生成 |
| 全书设定/力量体系.md | 从正文提取力量规则→按四层结构生成 |
| 全书设定/势力.md | 从正文提取势力信息→按4层表格生成 |
| 角色库.md | 从正文提取出场角色→按角色库模板总表+详细卡生成 |

以上补建文档均标注"⏳反推，需校验"。

0f-3 无法反推的文档处理：

| 缺失文档 | 处理方式 |
|:--|:--|
| 剧情白描.md | **必须询问用户**：①提供大纲（标准化转换）②跳过plot直接续写（降级模式） |
| 全书设定/各卷切片.md | 标注"⏳导入模式跳过，由后续world补跑" |
| 全书设定/危机.md | 部分可从正文反推，部分需用户补充 |
| 全书设定/世界矛盾轴.md | 需用户补充 |

降级模式：用户选择跳过plot直接续写→write将无剧情白描约束，需在`审核/状态快照.md`中手动指定下一章核心事件和爽感节点，write按状态快照指导续写；后续可补跑plot生成正式剧情白描。

**质量门**：原始资产清单已生成｜资产标准化转换完成（文件名+目录+内容结构）｜标准化资产清单已生成（✅/⚠️/❌）｜缺口报告已生成｜落地Phase已确定并经用户确认｜状态.md已创建/更新（mode+phase+chapter+阶段完成情况全部正确）｜补缺生成已完成（正文反推+缺失设计文档补建+无法反推文档已处理）。html展示面板不在质量门内（可选）。

→ 状态.md重建完成+用户确认落地Phase后，进入「日常路由」：日常写正文/审核由专家提示词阶段地图承载，pipeline 不常驻。

### Step 1 初始化项目（fresh模式）

> 只在状态.md不存在时执行。**前置检测**：任何创建操作前先LS扫描——`正文/`有ch*.txt/ch*.md或`设计/`有.md文件→已有历史资料，**跳转Step 0**导入/续写模式；目录为空或仅有状态.md→继续正常初始化。

**1a 确认项目目录**：用户指定项目名→以项目名为目录名；在当前项目目录下对话→用当前目录。当前工作目录已有状态.md→跳过初始化直接进日常路由。

**1b 创建标准目录结构**：`素材/`（含`downloads/`、`知识沉淀/`）+ `设计/`（含`全书设定/`、`角色库/`、`第一卷剧情/`）+ `正文/` + `审核/`（PowerShell `New-Item -ItemType Directory -Force` 逐个创建）。目录用途：

| 文件夹 | 存什么 | 对应Phase |
|:--|:--|:--|
| 素材/ | 调研+DNA+拆书+原书（downloads/存下载原书，知识沉淀/存沉淀） | Phase 0产出 |
| 设计/ | 创意.md（根目录）+全书设定/+角色库/+第一卷剧情/ | Phase 1-3.5产出 |
| 正文/ | 逐章渲染 ch{NNN}.txt | Phase 4产出 |
| 审核/ | 白描流水账+状态快照 | Phase 5产出 |

**1c 落盘状态.md**：按「状态.md标准模板」写入，mode: fresh / phase: init / current_chapter: ch000，全部Phase标[ ]。

**1d 生成总控.html（可选）**：仅当用户要看可视化面板时，按「state更新方法」运行脚本导出；日常 fresh 初始化不强制。**禁止手动写HTML**。完成后路由到 Phase 0 用户意图深问（日常路由由专家提示词阶段地图承载）。

### 状态.md 标准模板

```markdown
# 项目：{项目名}

> 管线：番茄skill群 | 创建：{YYYY-MM-DD HH:MM} | 更新：{YYYY-MM-DD HH:MM}

## 当前阶段
mode: fresh
phase: init
current_chapter: ch000

## 阶段完成情况
- [ ] Phase 0: 用户意图 + 并发前置准备
- [ ] Phase 1: Seed → 设计/创意.md + 正文/ch001.txt
- [ ] Phase 2: World → 设计/全书设定/（多文件）
- [ ] Phase 3: Plot → 设计/第一卷剧情/剧情白描.md
- [ ] Phase 3.5: Character → 设计/角色库/角色库.md
- [ ] Phase 4: Write → 正文/chXXX.txt (当前: ch000)
- [ ] Phase 5: Review → 审核/剧情白描流水账.md + 审核/状态快照.md

## 底牌就绪
- 用户意图：素材/用户意图.md ❌
- 赛道调研：素材/赛道调研.md ❌
- 参考书下载：skipped
- 笔触DNA：素材/文风锚定.md ❌
- decon-lite：素材/decon-lite-{书名}.md ❌

## 创意摘要
- 书名(暂)：待seed产出
- 一句话：待seed产出

## 最近产出
| 阶段 | 产出文件 | 落盘时间 |
|------|---------|---------|
| pipeline | 状态.md | {timestamp} |
```

**填写规则**（Step 0重建时）：mode填import/resume（按0d决策）、phase填落地Phase、current_chapter填下一章待写；已就绪Phase标`[x]`、未就绪标`[ ]`、落地Phase为当前进行中；已有素材对应底牌从❌改为✅/done/skipped。

### 日常路由（已上移专家提示词，pipeline 不常驻）

**日常写作路由不再经过本 skill**——由专家提示词规则1/2承载：先读 `状态.md` 状态片段（phase/current_chapter/底牌就绪），按阶段地图（立项→世界→角色→剧情→正文→审核）+ 灵活调度直接选 skill。下方「Phase调度表」仅作安装/导入时的一次性路由参考，日常不按它每轮循环。html 展示面板仅在老板要看时按需导出，agent 不读。

### Phase调度表

| Phase | 调用Skill | 前置检查 | 产出 | 完成后更新 |
|:--|:--|:--|:--|:--|
| init | （执行Step 1初始化） | — | 四文件夹+state文件 | phase→phase0，进Phase 0 |
| 0 Stage1 | 主agent用户意图深问（四层递进：赛道方向必答→标签/元素→参考书群→现有设定，后三层可跳过） | phase=phase0 | 素材/用户意图.md | 进Stage2 |
| 0 Stage2 | 子agent并发：下载参考书（用户给书名+无本地文件）/笔触DNA提取（已下载）/decon-lite拆书（力量体系参考书+已下载）/赛道定位调研（必有） | Stage1完成 | 素材/downloads/{书名}.txt+文风锚定.md+decon-lite-{书名}.md+赛道调研.md | phase→phase1 |
| 1 | pop-fanqie-seed | 用户意图已落盘（或明确跳过）+赛道调研已落盘（如有） | 设计/创意.md+正文/ch001.txt | phase→phase2、current_chapter=ch001、创意摘要填seed产出 |
| 2 | pop-fanqie-world | 设计/创意.md+正文/ch001.txt 存在 | 设计/全书设定/（力量体系.md+地图.md+势力.md+危机.md+各卷切片.md+全书配角.md） | phase→phase3 |
| 3 | pop-fanqie-plot | 设计/全书设定/ 存在 | 设计/第一卷剧情/剧情白描.md | phase→phase3.5 |
| 3.5 | pop-fanqie-character | 剧情白描.md存在（含分幕出场角色清单） | 设计/角色库/角色库.md（消费分幕出场清单+势力.md敌人梯度+创意主角轮廓） | phase→phase4、current_chapter=ch002 |
| 4 | pop-fanqie-write（**必须子agent**） | 剧情白描.md+角色库.md 存在 | 正文/chXXX.txt（写current_chapter指定章） | phase→phase5 |
| 5 | pop-fanqie-review | 正文/chXXX.txt 存在 | 审核/剧情白描流水账.md（append白描卡）+审核/状态快照.md（replace），结论对话内输出 | 通过→phase4+ch{NNN+1}；打回→phase4重写本章 |

> Phase 0并发规则：下载先返回→再同时派发DNA+decon-lite，赛道调研第一优先级独立启动。
> Phase 4子agent指令模板：你扮演 pop-fanqie-write，读取 skills/pop-fanqie-write/SKILL.md 了解完整SOP。项目目录：{projectDir}。当前章节：{current_chapter}。按SOP执行：加载输入→选章型→写正文→字数自检→落盘。注意：必须加载设计/角色库/角色库.md，战斗/升级场景必须使用DNA面板格式。

### state更新方法（每次Phase完成后）

**1. 更新 状态.md**（SearchReplace）：①`phase:` 行 ②`current_chapter:` 行 ③`更新：` 行→当前时间 ④阶段完成情况→勾选完成的phase ⑤底牌就绪区块→更新状态 ⑥创意摘要→填写seed产出 ⑦最近产出表→追加新行

**2. 导出 总控.html（可选，按需）**：仅当用户要看可视化状态面板时运行：

```bash
python skills/pop-fanqie-pipeline/scripts/generate-state-html.py {projectDir}/状态.md
```

脚本自动解析状态.md字段→替换模板占位符→同目录生成 总控.html。**禁止手动写HTML**。日常更新状态不要求运行；html不参与任何路由/决策。

## 📦 可调度 Skill 清单（素材表）

> 本 pipeline 整个专家入口与调度器，可调度的子 skill 总清单如下（与 `skill.json` 的 `skills` 数组一致）。这些 skill 按 Phase 调度表调度，**部分 skill 会被其他专家复用**（如 `pop-dna-style` / `pop-research` / `tool-download-webnovel`）。

| Skill | 定位 | 何时调用 |
|:--|:--|:--|
| `pop-fanqie-seed` | 种子创意+首章 | Phase 1 |
| `pop-fanqie-world` | 世界构筑（全书设定） | Phase 2 |
| `pop-fanqie-plot` | 剧情白描 | Phase 3 |
| `pop-fanqie-character` | 角色库 | Phase 3.5 |
| `pop-fanqie-write` | 正文渲染 | Phase 4 |
| `pop-fanqie-review` | 审核+沉淀 | Phase 5 |
| `pop-dna-style` | 文风综合重构 | Phase 0 |
| `pop-research` | 赛道调研/decon-lite/采风 | Phase 0 |
| `tool-download-webnovel` | 下载对标书 | Phase 0 |

## 🚪 首次对话引导（onboarding）

> 用户第一次触发番茄网文专家（无任何写作项目、非续写场景）时，**先输出 `references/onboarding-guide.md` 的引导语内容**给用户建立认知，再进入 Step 0 意图深问。
>
> 展示方式：在回复中**直接粘贴 `references/onboarding-guide.md` 全文**（声明本次为功能介绍+引导、未执行 skill 任务），用 1-2 句口头补充"报书号+想法就开始"。若用户已明确要开做，可跳过引导直接干活。

## 红线

1. **读取协议**——读取skill文件用`Get-Content -Encoding UTF8 -Raw`，Read工具有行数限制会截断丢内容
2. **状态.md是唯一状态源**——所有phase切换以它为准；路由只读它的状态片段（phase/current_chapter/底牌就绪），不读html展示面板。html仅为按需导出的人看面板，不在质量门内，不承担每轮同步成本
3. **Phase 0必须先深问再并发**——不完成Stage 1用户意图深问，不进入Stage 2
4. **pipeline只做路由不干活**——不写正文/不创意/不审核/不提取DNA
5. **Phase 4必须用子agent调write**——主agent只做路由，主agent执行write会导致skill读取不全+正文质量退化
6. **Phase 3.5 Character必须执行**——plot完成后必须经过character建角色库，跳过=角色设计丢失
7. **agent每次对话第一件事是读状态.md**
8. **导入/续写模式不可跳过资产扫描**——用户说"导入/续写/已有"时必须走Step 0（资产扫描→缺口分析→落地Phase决策→用户确认），禁止直接凭空设置phase

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `SKILL.md` | 每次run强制注入 | SOP全内联：Step 0导入+Step 1初始化+日常路由+Phase调度表+state更新方法+红线 |
| `scripts/generate-state-html.py` | 仅用户要看可视化面板时（按需可选） | 读取state.md→导出总控.html；日常更新状态不运行 |
| `templates/总控.html.tpl` | 脚本自动使用 | HTML可视化模板 |
| `references/onboarding-guide.md` | 用户第一次触发（首次对话引导）时 | C端口吻引导语——「🚪 首次对话引导」区块强触发输出全文 |
| `references/import-structures.md` | 导入/续写模式 Step 0 0b-2 环节 | 16个标准文件的内容分节结构+转换方式（导入转换视角，结构正源在各子skill） |

## 🗺️ 知识地图（reference 读取索引）

> pipeline 有 2 个 reference，均为场景触发式（首次对话引导/导入结构转换），无需分级。**看就记住，别读全文**。

| 参考 | 级别 | 什么时候必须读（触发条件） |
|:--|:--|:--|
| `references/onboarding-guide.md` | 🔴强触发 | **用户第一次触发番茄专家时必读**——SKILL.md「首次对话引导」区块声明输出全文 |
| `references/import-structures.md` | 🟡场景触发 | 导入/续写模式 Step 0 0b-2 环节（16个标准文件结构转换） |

## 版本

v4.2.0 | 2026-08-27
- **日常路由上移专家提示词**：删除「路由循环（每次对话开始时）」常驻 loop，改为「日常路由」参照节——pipeline 只管一次性安装/导入，日常写正文/审核不经过本skill
- **状态源统一为 状态.md**：project-state.md → 状态.md（机器）；html 展示面板仅供老板查看，按需导出，agent 不读（收敛：三族状态源统一命名）
- skill.json version 4.1.0→4.2.0
v4.1.0 | 2026-08-27
- **status.html降级为可选展示面板**：状态.md确认为唯一机器状态源；路由循环/红线#2 明确只读其状态片段，不读html
- html从「每次更新state强制同步」改为「仅用户要看时按需导出」；0e/1d/质量门/速查表/state更新方法同步去强制化
- 与番茄专家提示词收敛对齐：prompt第1条「先读状态片段」、不舔html全量
- skill.json version 4.0.0→4.1.0
v4.0.0 | 2026-08-24
- **step0-import / step1 全合入 SKILL.md 单文件精炼**：Step 0 五环节（资产扫描/标准化转换/缺口分析/落地Phase决策/状态重建/补缺生成）+质量门全内联；steps 目录删除
- **模板合一**：step1与step0-import的状态.md重复模板合并为「标准模板+填写规则」（覆盖fresh/import/resume三模式差异）
- 执行模式明确：主agent直执（路由/状态管理/意图深问/导入确认），子agent派发点已在Phase调度表内置
- skill.json version 3.13.0→4.0.0
v3.13.0 | 2026-08-18
- **step2 路由循环合入 SKILL.md**：路由分流/state更新/脚本调用全部上提，每次对话零跳转自包含；Phase调度表合并前置检查+完成后更新两列；下一步文案映射表删除（脚本内置单源）；知识地图补import-structures条目
- 删除 step2.md 文件
v3.12.1 | 2026-08-18 | step0-import 结构表下沉 → [CHANGELOG.md](CHANGELOG.md)
