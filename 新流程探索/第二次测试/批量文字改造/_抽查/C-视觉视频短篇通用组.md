# C · 视觉 / 视频 / 短篇通用组 — 文字质量抽查报告

- 抽查性质：只读质量抽查，未修改 `skills\` 与 `外部参考skill\` 下任何文件。
- 基准：`d:\popwave-skills\外部参考skill\镜界的skill\`（读 8 份）。
- 对象：D 盘当前 `d:\popwave-skills\skills\` 下 8 份 SKILL.md + 2 份 references。
- 判定口径：语序 / 语病 / 措辞 / 书面化 四条。
- 行号即文件真实行号；原句照抄或截取，未概括、未编造。

---

## 一、镜界基准摘要（尺子）

镜界句子是书面语，主谓完整，一句一义，不靠短句硬切；祈使句用「不要 / 须 / 不得 / 禁止」承载硬约束；判断给数字锚点；术语直用现有词（POV、便签、连线、Reference），不自造比喻；标点全角，符号克制，全篇无 emoji。

三条真实引文：

1. `00-系统提示词-Mirroric.md:25`
   > 3. 精准修改：只改必须改的，不顺手改相邻段落，匹配现有风格和语气。
2. `03-章节写作.md:32`
   > **禁止上帝视角**：不要直接写非 POV 角色的真实想法、隐藏动机、远处同步事件、未来结果或世界真相。需要让读者知道的信息，必须通过 POV 角色能接触到的动作、对白、表情、环境痕迹、传闻、文件、回忆或合理推断呈现。
3. `14-画布构图指南.md:67`
   > **一行最多 6 个节点。** 6 列约 2400px 宽，在典型画布区里适配全图后缩放已经掉到 0.4 上下，便签正文接近看不清；再多就只剩色块。超过就分幕：把一幕的标题写成 stone 便签，放在该段主干上方且**不连线**，下一幕从新的列继续。

（另注：镜界 `14-画布构图指南.md:27` "**先打开再动手。**" 是四字硬句，但后接完整解释；它硬切短句仅在强调句上出现，不整篇使用。）

---

## 二、逐 skill 评分表

5 = 与镜界同水位；4 = 接近；3 = 有可见差距；2 = 明显不如；1 = 差距大。

| 文件 | 语序 | 语病 | 措辞 | 书面化 | 总判：是否对齐镜界 |
|:--|:--:|:--:|:--:|:--:|:--|
| `pop-visual-comic\SKILL.md` | 3 | 3 | 2 | 3 | 未对齐（措辞拖后腿最重） |
| `pop-visual-pipeline\SKILL.md` | 4 | 4 | 2 | 3 | 未对齐（黑名单词成体系） |
| `pop-visual-cover\SKILL.md` | 4 | 4 | 2 | 3 | 未对齐 |
| `short-reviewer\SKILL.md` | 4 | 4 | 2 | 3 | 未对齐 |
| `short-text-deconstructor\SKILL.md` | 4 | 3 | 2 | 3 | 未对齐 |
| `pop-content-card\SKILL.md` | 4 | 4 | 2 | 3 | 未对齐 |
| `pop-ai-reduce-lite\SKILL.md` | 3 | 3 | 2 | 2 | 未对齐（文体离镜界最远） |
| `tool-download-webnovel\SKILL.md` | 4 | 4 | 3 | 2 | 未对齐（书面化最弱） |
| `pop-visual-pipeline\references\落盘规范.md` | 4 | 4 | 3 | 3 | 未对齐（轻，措辞偶有口语） |
| `short-text-deconstructor\references\writing-styles.md` | 5 | 4 | 4 | 4 | 基本对齐（本组最接近镜界） |

---

## 三、逐句抽检证据

### 1）pop-visual-comic\SKILL.md

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| pop-visual-comic\SKILL.md:3 | HTML 承担长条滚动展示与文字叠加层。 | 轻微 | 语病：动宾搭配不当，"承担"接"层"不成搭配；"**页漫模式**。"独立成残句 | 改"HTML 负责长条滚动展示与文字叠加层。" |
| pop-visual-comic\SKILL.md:14 | **核心铁律**：画风（来自美术设定集）与排版这两项"底盘"是固定的，换题材只换配色与内容，不换画风底盘与排版结构。 | 轻微 | 措辞：装饰性比喻"底盘"，黑名单禁比喻式自我定位 | 改"画风基准与排版结构是固定的" |
| pop-visual-comic\SKILL.md:38 | Step 2 生成、HTML、脚本与记忆沉淀（调用工具并写入文件）**由主 agent 直接执行**； | 不合格 | 语病：并列项词性不一（"生成"是动词，"HTML"是名词），搭配不当；单句过长 | 改"Step 2 出图、生成 HTML、执行脚本与写入记忆沉淀，由主 agent 直接执行" |
| pop-visual-comic\SKILL.md:44 | ...不做门禁 0 的画风与 OC 重确认（art-bible ❌4：...） | 不合格 | 措辞：黑名单命中"门禁"（门禁→检查条件） | 改"不再做第 0 道画风与 OC 重确认" |
| pop-visual-comic\SKILL.md:54 | 不得自建画风基准（art-style-baseline 自选）、自建 OC 规格表、做门禁 0 重确认——这些是基建层职责。 | 不合格 | 措辞：黑名单"门禁" | 改"...做第 0 道画风与 OC 重确认——这些是基建层职责。" |
| pop-visual-comic\SKILL.md:86 | **先讲清，再拍，再画。** 写入仍为一张导演卡（白描段内嵌顶部 §「剧情白描」，...）。 | 不合格 | 语病：缺主语，"写入仍为一张导演卡"指代不明（谁写入？） | 改"本节产出仍为一张导演卡（...）" |
| pop-visual-comic\SKILL.md:94 | 通读原文，用白描式叙述（画面、情绪、内心融入叙事，用像给朋友讲故事那样自然流畅的方式）写出整章完整故事弧线，... | 不合格 | 语序：介词结构错位，"用像……那样……的方式"读不通 | 改"以像给朋友讲故事那样自然流畅的方式叙述" |
| pop-visual-comic\SKILL.md:102 | ...（第1章6页实测：章节预算给少是讲不清故事的核心根因）。 | 不合格 | 措辞+语病：口语"给少"；"核心根因"语义重复（核心=根因） | 改"（第1章6页实测：章节预算给少了，是故事讲不清的主因）" |
| pop-visual-comic\SKILL.md:113 | **文字量反检门禁（页数规划后立即做）**：... | 不合格 | 措辞：黑名单"门禁"；"反检"为自造压缩词 | 改"**文字量反向检查（页数规划后立即做）**" |
| pop-visual-comic\SKILL.md:117 | **以页思路拆采摘表**（内嵌导演卡「原文采摘」段）。 | 不合格 | 语序：动宾搭配不通，"以页思路拆……表" | 改"按页拆分采摘表" |
| pop-visual-comic\SKILL.md:137 | - **叙事引擎识别**：引擎类型（渐进揭示、感官逼近、时间线断裂、因果链驱动、反转颠覆，可多选）... | 不合格 | 措辞：黑名单命中「XX引擎」 | 改"叙事手法识别：手法类型（渐进揭示、感官递进、时间线断裂、因果推进、反转）" |
| pop-visual-comic\SKILL.md:140 | 旁白浓缩（旁白条每条上限80字；关键旁白——因果链、关键剧情、恐怖前提、章末钩子——可直接放宽至80字，...） | 不合格 | 语病：上限 80 字又"放宽至80字"，前后矛盾，执行会读错 | 改"关键旁白可放宽上限至 120 字" |
| pop-visual-comic\SKILL.md:224 | 门禁不通过时，按编号打回对应小节 | 不合格 | 措辞：黑名单"门禁" | 改"检查不通过时，按编号打回对应小节" |
| pop-visual-comic\SKILL.md:240 | 逐张调用（发一张→结束turn→重复守卫警告→返回时只收到第一张）会导致**后续页全部漏掉** | 轻微 | 书面化：中英夹杂"结束turn"；箭头串联代句 | 改"结束本轮（turn）" |
| pop-visual-comic\SKILL.md:266 | **0基础可读性检查（审稿门禁，不通过不得进入记忆沉淀）**：... | 不合格 | 措辞：黑名单"门禁" | 改"审稿检查" |
| pop-visual-comic\SKILL.md:328 | （老板校准：第4章实测S级保真仅43%含虚构补写；...） | 轻微 | 措辞：内部口头语"老板校准"入文档 | 改"（实测校准：第4章...）" |

### 2）pop-visual-pipeline\SKILL.md

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| pop-visual-pipeline\SKILL.md:9 | ...生成或重建 `状态.md`（唯一机器状态源）、执行三态写入迁移...；**日常视觉路由与意图闸口上移专家提示词**... | 不合格 | 措辞：黑名单"机器状态源"（→状态总账）、"闸口"（闸→检查） | 改"（唯一状态总账）...日常视觉路由与意图检查上移专家提示词" |
| pop-visual-pipeline\SKILL.md:12 | 输出：标准化目录结构、`状态.md`（唯一机器状态源），以及可选的 `视觉项目总控.html` 展示面板 | 不合格 | 措辞：同上 | 改"（唯一状态总账）" |
| pop-visual-pipeline\SKILL.md:16 | 先过意图闸口确认本次目标（cover/oc/comic/full/asset-only，不默认推漫画）...与就绪门禁直接选择 skill。 | 不合格 | 措辞：黑话"意图闸口""就绪门禁" | 改"先过意图确认...与就绪检查直接选择 skill" |
| pop-visual-pipeline\SKILL.md:20 | 该文件写入项目根目录，agent 每轮只读取它获取状态片段。 | 合格 | 主谓完整，一句一义 | — |
| pop-visual-pipeline\SKILL.md:54 | **2. 🚪 意图闸口（前置步骤，决定基建档位）**：... | 不合格 | 措辞：黑话"意图闸口"；emoji 入标题（镜界全篇无 emoji） | 改"**2. 意图确认（前置步骤，决定基建档位）**" |
| pop-visual-pipeline\SKILL.md:71 | **4. 生成 状态.md**：读取 `templates/状态.md` 并写入项目根目录，按「状态更新协议 §1」填充：... | 合格 | 动词开头，一步一动作 | — |
| pop-visual-pipeline\SKILL.md:85 | 有资产、无画风或设定集→**phase1**（补做 Phase 1 定画风） | 轻微 | 语序/歧义："无画风或设定集"可读成"无（画风或设定集）"，与本意不同 | 改"无画风、或无设定集" |
| pop-visual-pipeline\SKILL.md:91 | ### Step 2 日常路由（不经常驻循环） | 轻微 | 措辞：标题括号补语与正文重复（正文已两处写"不参与每轮路由"），冗余 | 改"### Step 2 日常路由" |
| pop-visual-pipeline\SKILL.md:129 | **由主 agent 直接执行**。Step 0/1 的初始化与导入均由主 agent 直接执行；...pipeline 自身无产出，不存在可派发的只读子任务。 | 合格 | 主语明确，硬约束清楚（本文件写得最稳的一段） | — |
| pop-visual-pipeline\SKILL.md:135 | `状态.md` 是唯一机器状态源，不得另建 project-state.md，也不得读取 html 获取状态。 | 不合格 | 措辞：黑名单"机器状态源" | 改"`状态.md` 是唯一状态总账" |
| pop-visual-pipeline\SKILL.md:137 | 3. **基建依赖链与就绪检查不可跳**——资产未就绪不得进入定画风，画风未就绪不得进入美术设定集 | 合格 | 书面化达标，"不得"承载硬约束 | — |
| pop-visual-pipeline\SKILL.md:148 | 唯一机器状态源（mode/phase/intent/next_step、就绪态、最近产出） | 不合格 | 措辞：同上 | 改"唯一状态总账（...）" |

### 3）pop-visual-cover\SKILL.md

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| pop-visual-cover\SKILL.md:3 | 网文封面与场景视觉资产生成器。两种起点，同一个终点。 | 不合格 | 措辞：黑名单命中「XX器」自我定位；后半句口号化 | 改"网文封面与场景视觉资产工具。" |
| pop-visual-cover\SKILL.md:10 | **两道用户对齐门禁**确保方向不跑偏。 | 不合格 | 措辞：黑名单"门禁"；口语"不跑偏" | 改"**两道用户对齐检查**，防止方向偏离" |
| pop-visual-cover\SKILL.md:28 | **门禁交互由主 agent 直接执行，只读侦察可派发子 agent**：... | 不合格 | 措辞：黑话"门禁"；比喻"侦察" | 改"**检查环节的交互由主 agent 直接执行，只读探查可派发子 agent**" |
| pop-visual-cover\SKILL.md:36 | ...先搜图、选图、对齐参考点，再出方案——参考图决定设计方向，不是方案定了再找图配。 | 轻微 | 书面化：句尾"再找图配"口语缩略 | 改"不是方案定了再找参考图" |
| pop-visual-cover\SKILL.md:40 | - **提取视觉意图**：赛道、**IP 背景**（是否基于已有 IP？源 IP 是什么？）...无法从书名和描述判断是否同人时，**须问用户** | 合格 | 检查条件+须，符合"判断给锚点" | — |
| pop-visual-cover\SKILL.md:43 | **检查条件：无法判断目标读者画像时，须问用户"你的目标读者是哪个年龄段"，不得默认"甜宠就等于可爱卡通"** | 合格 | 给检查条件+"须/不得"，反例具体 | — |
| pop-visual-cover\SKILL.md:48 | 无 IP 指向时用"角色加风格"两维；有 IP 指向时三维全开；**总量控制在 6 张以内**。 | 合格 | 数字锚点清楚 | — |
| pop-visual-cover\SKILL.md:60 | - **对齐参考点（核心环节，不固定选项，由用户选择，可多选）**：□全面参考（...）□色系（...） | 轻微 | 书面化：正文用"□"符号充当列表标记 | 改"可选：全面参考；色系；构图；画风……" |
| pop-visual-cover\SKILL.md:111 | **典型选择：动作交接点（前一动作刚完成、后一动作将开始）通常视觉张力最强——既保留前因的暗示，又预示后果的方向。** | 合格 | 一句一义，判断给理由 | — |
| pop-visual-cover\SKILL.md:157 | **铁律：用户选了什么参考点，提示词就在那个维度放弃控制权，交给参考图**——不得既说"参考色系"又写"暖粉七成" | 合格 | 硬约束用"不得"，反例具体 | — |
| pop-visual-cover\SKILL.md:208 | ...**放权维度的翻译规则：某维度交给参考图时，该维度不写任何描述词**（如色系参考→"暖粉""暖黄""暖色调"全部删除）。 | 合格 | 条目化、可执行 | — |
| pop-visual-cover\SKILL.md:215 | 引擎 | 轻微 | 措辞：表头"引擎"近黑名单（引擎→具体环节名） | 改"模型" |

### 4）short-reviewer\SKILL.md

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| short-reviewer\SKILL.md:2 | 本技能为短篇评审器，流程依次为：读草稿、对照骨架、逐维诊断、输出报告。 | 不合格 | 措辞：黑名单「XX器」自我定位 | 改"本技能用于短篇评审" |
| short-reviewer\SKILL.md:2 | ...九维诊断可派子 agent（审查官）执行，由主 agent 校验并归位。 | 不合格 | 措辞：黑话"归位"（→移入项目目录） | 改"...校验并移入项目目录" |
| short-reviewer\SKILL.md:5 | 输出：诊断报告，含 X.X/10 评分、总览、亮点与不足、分维诊断、AI味儿参考、修改建议、总结 | 不合格 | 措辞：口语"AI味儿"，书面应为"AI 痕迹" | 改"AI 痕迹参考" |
| short-reviewer\SKILL.md:14 | 三项均通过后以 Move-Item 归位到项目目录。 | 不合格 | 措辞：中英夹杂"以 Move-Item"+"归位"黑话 | 改"通过后用 Move-Item 移入项目目录" |
| short-reviewer\SKILL.md:26 | 话术："默认全篇九维诊断。要限制范围吗？还是直接开始？" | 合格 | 引语自然；口语仅出现在话术示例中，合理 | — |
| short-reviewer\SKILL.md:28 | 通过（7.0 及以上）者以一行确认；不通过（低于 7.0）者须标注具体问题与建议方向。 | 合格 | 分数锚点+"须"，符合"判断给锚点" | — |
| short-reviewer\SKILL.md:30 | 分差达 2.0 及以上者标 🔴 优先修复 | 轻微 | 书面化：以 emoji 作状态标记，镜界用文字 | 改"标记为高优先修复" |
| short-reviewer\SKILL.md:39 | 最后情绪高峰之后，超过全文 10% 字数的篇幅仍在叙事，即判定为拖沓 | 合格 | 数字锚点+判据，优于镜界同类原则句 | — |
| short-reviewer\SKILL.md:41 | 同类情绪事件（同类反转、打脸）连续使用时，须标注冲击力递减点 | 合格 | 行业词直用，"须"到位 | — |
| short-reviewer\SKILL.md:51 | **总结**：综合评分、等级、结论（推荐提交、修完可提交或需要大修）、最强武器、最弱一环。 | 轻微 | 措辞：不当比喻"最强武器""最弱一环" | 改"最强项、最弱项" |
| short-reviewer\SKILL.md:52 | 6. **流转确认**："以上是我完整的诊断。你想改哪些？确认后进入润色。" | 合格 | 引语清楚 | — |
| short-reviewer\SKILL.md:67 | 只诊断不修改，不替用户直接改正文 | 合格 | 一句一义，后果具体 | — |

### 5）short-text-deconstructor\SKILL.md

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| short-text-deconstructor\SKILL.md:2 | 本技能为短篇拆文分析器，流程依次为：选深度、拆结构、拆角色、拆开篇、拆文风、评价、影响后续。 | 不合格 | 措辞：黑名单「XX器」自我定位 | 改"本技能用于短篇拆文分析" |
| short-text-deconstructor\SKILL.md:14 | 三项均通过后以 Move-Item 归位到项目目录。 | 不合格 | 措辞：中英夹杂+"归位"黑话 | 改"通过后用 Move-Item 移入项目目录" |
| short-text-deconstructor\SKILL.md:17 | ...主 agent 校验后归位；Step 0 的深度选择需要用户交互，由主 agent 直接执行。 | 不合格 | 措辞：黑话"归位" | 改"主 agent 校验后移入项目目录" |
| short-text-deconstructor\SKILL.md:19 | 本技能独立于主线 Step 1-6，用户可在任何阶段触发。 | 合格 | 主谓完整 | — |
| short-text-deconstructor\SKILL.md:24 | 触发时须先暂停当前主线流程，并告知用户："收到，我先暂停当前的[当前Step名称]，专注拆解这篇例文。..." | 合格 | 引语为话术示例，口语合理 | — |
| short-text-deconstructor\SKILL.md:36 | 开篇风格（知乎知性沉稳、番茄网感快、每天情感细腻等）判断平台归属。 | 不合格 | 语病：成分残缺，"番茄网感快"应为"网感快节奏" | 改"（知乎知性沉稳、番茄网感快节奏、每天情感细腻等）" |
| short-text-deconstructor\SKILL.md:39 | **弧线还原**：反向还原例文的剧情弧线，输出五列表（段落、字数、核心事件、信息释放、情绪走向） | 合格 | 一句一义，术语直用 | — |
| short-text-deconstructor\SKILL.md:47 | 第 1 句的功能为甩冲突、拉近距或留钩子。 | 不合格 | 语病：成分残缺，"拉近距"应为"拉近距离" | 改"第 1 句的功能为甩冲突、拉近距离或留钩子。" |
| short-text-deconstructor\SKILL.md:61 | 输出贴合 writing-styles.md 的风格描述格式，并标注与五种标准文风的异同。话术："这篇例文的文风可以概括为：..." | 合格 | 动词开头，引语清楚 | — |
| short-text-deconstructor\SKILL.md:63 | 等级为现象级、爆款区、潜力带、过关线、危险区、别急着投。 | 轻微 | 措辞：等级名"别急着投"口语，与其余五级不同质 | 改"暂不建议投稿" |
| short-text-deconstructor\SKILL.md:65 | 拆文评价为"样本分析"，评审为"诊断"，两者不冲突；例文质量明显偏低时须标注，但不得模仿。 | 合格 | 边界定义清楚，用"须/不得" | — |
| short-text-deconstructor\SKILL.md:77 | 拆解出的弧线与角色作为基础框架，微调后使用 | 合格 | 表列对齐，无冗余 | — |

### 6）pop-content-card\SKILL.md

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| pop-content-card\SKILL.md:5 | ## 这个 Skill 做什么 | 轻微 | 书面化：中英夹杂"这个 Skill"；同组其他文件用"本技能" | 改"## 本技能做什么" |
| pop-content-card\SKILL.md:18 | 定义内容价值，即素材卡对读者有什么用 | 合格 | 新概念用"即"界定，边界清楚 | — |
| pop-content-card\SKILL.md:20 | 把数据传导为读者0.5秒可感知的视觉 / body class切换 | 轻微 | 语病+书面化：缺空格"读者0.5秒""body class切换"；"可感知的视觉"搭配生硬 | 改"把数据传导为读者 0.5 秒内可感知的版式 / body class 切换" |
| pop-content-card\SKILL.md:22 | **质量传导链**：三可先传导为68字段与8项校验，再落到版式呈现。...脱离三可的工程检查（如"字段数对"但不"可截图"），即为不通过。 | 不合格 | 措辞："传导链"属黑名单"链路"类黑话 | 改"**质量标准的传递**：三可先落为 68 字段与 8 项校验，再落到版式呈现。" |
| pop-content-card\SKILL.md:24 | **执行模式**：由主agent直接执行。素材内容生产与模板填充是一条连续的创作链（...中间隔着8项校验门禁），没有可交给子agent的环节。 | 不合格 | 措辞："创作链""校验门禁"双黑话；书面化：主agent/子agent 缺空格 | 改"由主 agent 直接执行。素材生产与模板填充是一条连续流程（...中间隔 8 项校验），没有可交给子 agent 的环节。" |
| pop-content-card\SKILL.md:30 | **1. 读方法论**：`references/content-method.md`（生产前必读，含4类型生产原则、字段清单、自检门禁全表）。 | 不合格 | 措辞："自检门禁"黑话；"4类型"缺空格 | 改"含 4 类生产原则、字段清单、自检检查全表" |
| pop-content-card\SKILL.md:41 | **4. 按JSON格式组织产出**：产出格式为JSON（不是Markdown），字段名与HTML母版占位符一一对应。 | 轻微 | 书面化：按JSON/为JSON/与HTML 三处缺空格 | 改"按 JSON 格式...为 JSON（不是 Markdown）...与 HTML 母版..." |
| pop-content-card\SKILL.md:54 | **5. 字段校验门禁**（JSON产出后必须逐项校验，任一项不通过即回到第3步补内容，不得进入Step 2） | 不合格 | 措辞："门禁"黑话；缺空格 | 改"**5. 字段校验**（JSON 产出后须逐项校验，任一项不通过即回第 3 步补内容，不得进入 Step 2）" |
| pop-content-card\SKILL.md:88 | 统计母版中 `{{...}}` 占位符的数量与JSON key的数量，两者必须一致。 | 轻微 | 书面化："与JSON key"缺空格 | 改"与 JSON key 的数量" |
| pop-content-card\SKILL.md:100 | **完成检查**：页面数和页码一致（5页）〔可截图〕｜每页主内容占比约75%-85%〔三可基础〕 | 合格 | 每条检查回指"三可"标准，判据清楚（反向证据） | — |
| pop-content-card\SKILL.md:122 | 切换方式是改 `<body>` 的 class，不得手改 CSS 变量。 | 合格 | 用"不得"承载硬约束 | — |
| pop-content-card\SKILL.md:145 | **设计原则**：核心流程骨架和铁律在 SKILL.md 中自包含 | 合格 | 主谓完整 | — |

### 7）pop-ai-reduce-lite\SKILL.md

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| pop-ai-reduce-lite\SKILL.md:1 | # 李白.Skill:润色专家 v2.0 | 轻微 | 书面化：标题中英混合、"李白.Skill:"体例与全仓技能名不一致 | 改"# 润色专家（去 AI 味）v2.0" |
| pop-ai-reduce-lite\SKILL.md:3 | **适用场景**: 自媒体文章、公关稿件、日常沟通、学术随笔等中文文本的去AI化改写 | 轻微 | 书面化：半角冒号": "；"去AI化"缺空格 | 改"**适用场景**：……的中文文本去 AI 化改写" |
| pop-ai-reduce-lite\SKILL.md:11 | **减法只做在「虚」的地方**：模板化连接词、空洞升华、机械对称句式，一律删去；原作的口语表达、具体细节、个人语气、感官描写，一律保留。 | 合格 | 正反清单，边界清楚 | — |
| pop-ai-reduce-lite\SKILL.md:17 | 删虚词必然减字，加泥土必然增字，追求零波动不现实。 | 不合格 | 措辞：自造比喻"加泥土" | 改"补具象细节必然增字" |
| pop-ai-reduce-lite\SKILL.md:99 | 若只是"换皮不增加信息"（把压迫叫作账、把世界叫作迷宫），则改为直陈。 | 轻微 | 措辞："换皮"口语 | 改"只换说法不增加信息" |
| pop-ai-reduce-lite\SKILL.md:110 | **1 搜黑话** 全局搜索 找「赋能/闭环/底层逻辑/深刻/交织/画卷/交响乐/...」 | 合格 | 术语直用，方法可执行 | — |
| pop-ai-reduce-lite\SKILL.md:112 | **3 加泥土** 加入具象 在最干瘪处强行加入具体物品（「一杯冷掉的咖啡」） | 不合格 | 措辞：自造比喻"加泥土"；"最干瘪处"比喻 | 改"**3 补具象**：在最空泛处加入具体物品" |
| pop-ai-reduce-lite\SKILL.md:113 | **4 保血肉** 止损检查 通读：口语、孩子气口吻、动作描写、场景细节、语气词，一个不丢。 | 不合格 | 措辞：自造比喻"保血肉" | 改"**4 保原味**：通读并保留口语、具体动作、场景细节、语气词" |
| pop-ai-reduce-lite\SKILL.md:127 | 删 80% 观点只留最痛一个；加入私人记忆；允许逻辑跳跃 | 轻微 | 措辞："只留最痛一个"口语 | 改"只留最有力的一个" |
| pop-ai-reduce-lite\SKILL.md:149 | **标点呼吸**：适当使用破折号、省略号、问号制造停顿 | 轻微 | 措辞：自造比喻"标点呼吸" | 改"**标点节奏**" |
| pop-ai-reduce-lite\SKILL.md:258 | ## 核心口诀 | 轻微 | 书面化：口号式栏目与镜界克制风格不符；下文"人味是灵魂，真诚是底线"为宣传语 | 改"## 写作要点"，删口号句只留可执行四条 |
| pop-ai-reduce-lite\SKILL.md:286 | v2.0.0：P10 CTO 战略重构——SKILL.md 从 753 行压缩至 ~300 行；... | 不合格 | 措辞：内部黑话"P10 CTO 战略重构"指代不明；书面化："~300" 用波浪号 | 改"v2.0.0：结构调整——SKILL.md 从 753 行压缩至约 300 行；..." |

### 8）tool-download-webnovel\SKILL.md

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| tool-download-webnovel\SKILL.md:2 | 网文搜索下载TXT v7.3.1。三阶段流程：脚本搜索、web搜索兜底、验证交付。 | 轻微 | 书面化：缺空格"下载TXT"；"web搜索"小写 | 改"网文搜索下载 TXT v7.3.1。三阶段流程：脚本搜索、Web 搜索兜底、验证交付。" |
| tool-download-webnovel\SKILL.md:6 | 书名与作者(可选) / TXT文件与JSON状态 / pop-decon(拆书管线第一步) | 轻微 | 书面化：半角括号"(可选)"；缺空格"TXT文件与JSON状态" | 改"书名与作者（可选） / TXT 文件与 JSON 状态 / pop-decon（拆书管线第一步）" |
| tool-download-webnovel\SKILL.md:9 | 直链下载后自动扫描内容污染并截断尾部垃圾。 | 轻微 | 措辞："尾部垃圾"口语 | 改"截断尾部冗余内容" |
| tool-download-webnovel\SKILL.md:12 | execution.mode: 顺序执行Phase 1→2→3，Phase 1失败后强制进入Phase 2。 | 不合格 | 书面化：整句中英混杂+多处缺空格+箭头串联 | 改"执行顺序：Phase 1→2→3；Phase 1 失败后强制进入 Phase 2。" |
| tool-download-webnovel\SKILL.md:13 | 强加载：红线与速查表（每轮必读）；弱加载：scripts按需调用。 | 不合格 | 措辞：自造词"强加载/弱加载"；缺空格"scripts按需" | 改"必读：红线与速查表（每轮必读）；按需：scripts 按需调用。" |
| tool-download-webnovel\SKILL.md:16 | 执行 `python3 scripts/download_novel.py "书名" --author "作者" --output-dir downloads` | 合格 | 命令照抄，无歧义 | — |
| tool-download-webnovel\SKILL.md:17 | status=success 或 success_with_warnings → 检查preview与warnings → 交付；status=error → **进入Phase 2** | 不合格 | 书面化：多处缺空格，状态名与中文无分隔 | 改"status=success 或 success_with_warnings → 检查 preview 与 warnings → 交付；status=error → 进入 Phase 2" |
| tool-download-webnovel\SKILL.md:21 | 至少尝试3组关键词：... | 轻微 | 书面化：缺空格"尝试3组" | 改"至少尝试 3 组关键词" |
| tool-download-webnovel\SKILL.md:29 | warnings含"尾部污染" → 脚本已自动截断，检查preview确认 | 轻微 | 书面化：warnings含、检查preview 缺空格 | 改"warnings 含…检查 preview 确认" |
| tool-download-webnovel\SKILL.md:32 | 强加载为红线与速查表（每轮必读）；弱加载为scripts按需调用。Phase 1失败后必须加载Phase 2指令。 | 不合格 | 措辞：自造"强加载/弱加载"；缺空格 | 改"1. **读取协议**：必读红线与速查表（每轮）；scripts 按需调用。Phase 1 失败后必须加载 Phase 2 指令。" |
| tool-download-webnovel\SKILL.md:33 | Phase 1失败后不得直接放弃 — 必须执行Phase 2 web搜索，至少尝试3组关键词 | 合格 | 用"不得/必须"，硬约束明确 | — |
| tool-download-webnovel\SKILL.md:34 | 不得搜索或使用付费墙正版站 — 起点、晋江、纵横等，`--source-url`传入会被自动拦截 | 合格 | 一句一约束，用"不得" | — |

### 9）pop-visual-pipeline\references\落盘规范.md

> 说明：文件名与标题含"落盘"，按纪律豁免，不计缺陷；正文内"落盘位置"同样不报。

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| pop-visual-pipeline\references\落盘规范.md:3 | 本文件由 **pop-visual-pipeline 定义，全 visual 子 skill 须遵守**，是文件写入的唯一权威源。 | 合格 | 用"须"，责任与效力写清 | — |
| pop-visual-pipeline\references\落盘规范.md:4 | 目的：根治三类乱象——过程文件、测试文件与成品确认文件不分 | 轻微 | 措辞："乱象"是评价性词，非行为描述 | 改"目的：解决三类问题——..." |
| pop-visual-pipeline\references\落盘规范.md:9 | ## 一、核心原则：三态分离（生命周期 = 最高分区维度） | 轻微 | 书面化：标题内用半角等号" = " | 改"生命周期即最高分区维度" |
| pop-visual-pipeline\references\落盘规范.md:11 | 视觉产出按「生命周期」分三态写入，**全 skill 统一遵守**： | 合格 | 一句一义 | — |
| pop-visual-pipeline\references\落盘规范.md:19 | 基建真源（`素材/`）与漫画工程（`漫画/`）、视频工程（`视频/`）、内容物料（`内容/`）不属三态，属"生产参考/自体系/内容成品" | 合格 | 边界用"不属/属"锁定 | — |
| pop-visual-pipeline\references\落盘规范.md:30 | **`素材/视觉/` 扁平大杂烩** → 封面、OC、画册页、定妆、场景全部塞进同一个目录 | 不合格 | 措辞：口语降档词"大杂烩""塞进" | 改"**`素材/视觉/` 扁平目录** → 封面、OC、画册页、定妆、场景混放同一目录" |
| pop-visual-pipeline\references\落盘规范.md:48 | 统一小写 `v1` `v2` `v3`… 递增，**不得 `-V1`/`--v1`/`v1.0` 等变体** | 合格 | 用"不得"，反例列举 | — |
| pop-visual-pipeline\references\落盘规范.md:51 | **画册页主视觉**（HTML 组装版候选底图）统一用 `画册主视觉` 作用途 | 轻微 | 语序："作用途"动宾生硬 | 改"统一以 `画册主视觉` 作为用途字段" |
| pop-visual-pipeline\references\落盘规范.md:67 | `-final` 是**唯一成品态标记**；`测试/` 内不标 final，`_过程/` 内不讨论版本 | 合格 | 定义+边界，一句一义 | — |
| pop-visual-pipeline\references\落盘规范.md:123 | 1. **三态不混落** — ...不得把三种文件塞进同一目录。 | 不合格 | 措辞：自造"不混落"；口语"塞进" | 改"1. **三态不混放** — ...不得把三类文件放进同一目录。" |
| pop-visual-pipeline\references\落盘规范.md:126 | **基建真源只读消费，改动回 skill 升级版本** — 派生层只消费 `素材/美术设定集.md` 等冻结真源，不得各自重建。 | 合格 | 用"不得"，一句一约束 | — |
| pop-visual-pipeline\references\落盘规范.md:127 | **`_过程/` 默认 gitignore / 不提交** — 过程产物不进版本库，避免污染。 | 轻微 | 书面化：用半角斜杠" / "充当并列词 | 改"`_过程/` 默认 gitignore，不提交" |

### 10）short-text-deconstructor\references\writing-styles.md

| 定位 | 原句（照抄/截取） | 判定 | 病类或理由 | 建议改法 |
|:--|:--|:--:|:--|:--|
| short-text-deconstructor\references\writing-styles.md:3 | 此文件供正文生成器（Step 5）在文风选择阶段加载，提供五种平台对应的写作风格特征与实际范例 | 轻微 | 措辞：以「器」指代 skill，与镜界器物化禁令同向 | 改"供正文生成环节（Step 5）加载" |
| short-text-deconstructor\references\writing-styles.md:11 | 强人设、快节奏、高情绪密度与精准钩子。第一人称绝对主导。知性沉稳，靠克制和留白营造张力，不煽情、不泛滥。 | 合格 | 短句，一句一义 | — |
| short-text-deconstructor\references\writing-styles.md:18 | 语言特点：短句为主，拒绝形容词堆砌，多用可验证细节代替心理描写 | 合格 | 规则写成行为指令 | — |
| short-text-deconstructor\references\writing-styles.md:20 | 不写"她很绝望"，写"她反复擦手机屏幕，因为指纹解锁失败了 7 次" | 合格 | 正反例对照，给判据 | — |
| short-text-deconstructor\references\writing-styles.md:46 | 前三段立"有刺"人设，读者偏爱有缺陷但有行动力的主角 | 合格 | 行为指令 | — |
| short-text-deconstructor\references\writing-styles.md:89 | 开头 300 字内无冲突，则须重写 | 合格 | 数字锚点+"须" | — |
| short-text-deconstructor\references\writing-styles.md:101 | "原生、奇崛、动人"。每篇两千字左右，有泪有笑、温馨治愈。心理描写饱满、有温度、适合朗读，暖甜治愈。 | 轻微 | 语病：相邻两句重复"治愈" | 改"有泪有笑、温馨治愈。心理描写饱满、有温度、适合朗读。" |
| short-text-deconstructor\references\writing-styles.md:133 | 故事讲求"情理之中意料之外"的戏剧性 | 轻微 | 措辞：套语"情理之中意料之外" | 改"故事须有反转，但反转要有铺垫" |
| short-text-deconstructor\references\writing-styles.md:171 | 不得用年代和天气开头 | 合格 | 用"不得" | — |
| short-text-deconstructor\references\writing-styles.md:183 | 开篇三句即须切中要害，五句之内完成一次反转。每屏 150 字一个钩子，每 600 字一次打脸。...不铺垫、不解释、不灌水。 | 合格 | 数字锚点；"打脸"为行业词 | — |
| short-text-deconstructor\references\writing-styles.md:219 | 每屏 150 字一个钩子，不得让读者停下来喘气 | 合格 | 用"不得"，修辞可读 | — |
| short-text-deconstructor\references\writing-styles.md:252 | 加入感官细节 — AI 偏重视觉，须补充听觉、嗅觉、触觉 | 合格 | 一句一义，用"须" | — |

---

## 四、问题归类统计

按本次命中的最严重一类归属，去重后：

### A. 措辞（黑话 / 生造 / 器物化 / 不当比喻 / 口语降档）— 约 38 处

- **黑名单词「门禁」「闸口」「机器状态源」（16 处）**
  - pop-visual-comic:44、54、113、224、266
  - pop-visual-pipeline:9、12、16、54、135、148
  - pop-visual-cover:10、28
  - pop-content-card:24、30、54
- **「XX器」自我定位（4 处）**
  - pop-visual-cover:3「生成器」、short-reviewer:2「评审器」、short-text-deconstructor:2「分析器」、writing-styles.md:3「正文生成器」
- **「引擎 / 链路」类黑话（3 处）**
  - pop-visual-comic:137「叙事引擎」、pop-content-card:22「传导链」、pop-content-card:24「创作链」
- **自造比喻（6 处）**
  - pop-visual-comic:14「底盘」、pop-ai-reduce-lite:17、112、113、149（加泥土/保血肉/标点呼吸）、落盘规范:123「混落」
- **口语降档词 / 内部口头语 / 不明黑话（9 处）**
  - pop-visual-comic:102「给少」、328「老板校准」
  - pop-visual-cover:10「不跑偏」
  - short-reviewer:2、14「归位」，5「AI味儿」
  - short-text-deconstructor:14「归位」
  - tool-download-webnovel:9「尾部垃圾」、13「强加载/弱加载」、12「execution.mode」
  - 落盘规范:30「大杂烩」、123「塞进」
  - pop-content-card:5「这个 Skill」
  - pop-ai-reduce-lite:286「P10 CTO 战略重构」

### B. 语病（缺主 / 残缺 / 搭配不当 / 前后矛盾）— 5 处

- pop-visual-comic:38（并列项词性不一，搭配不当）
- pop-visual-comic:86（缺主语，指代不明）
- pop-visual-comic:140（上限 80 字 ↔ 放宽至 80 字，自相矛盾）
- short-text-deconstructor:36（"番茄网感快"成分残缺）
- short-text-deconstructor:47（"拉近距"成分残缺）

### C. 语序 — 3 处

- pop-visual-comic:94（"用像……那样……的方式"介词结构错位）
- pop-visual-comic:117（"以页思路拆采摘表"动宾不通）
- 落盘规范:51（"作用途"动宾生硬，轻微）

### D. 书面化（中英空格 / 半角符号 / emoji / 符号当句 / 口语人称）— 19 处

- **中英空格与半角符号（12 处）**
  - pop-content-card:20、24、30、41、54、88、5
  - tool-download-webnovel:2、6、12、13、17、21、29、32
  - pop-ai-reduce-lite:3、286
- **emoji 作状态/标记（2 处）**
  - short-reviewer:30（🔴）、pop-visual-pipeline:54（🚪）；另 pop-visual-comic 全篇用 🚪/❌/⚠️ 作章节号与状态（:38、:224、:266、:318-331）
- **符号当句 / 半角结构符（3 处）**
  - pop-visual-comic:240（箭头串联代句）
  - pop-visual-cover:60（用"□"充当列表标记）
  - 落盘规范:9、127（半角"="与" / "）

> 口径外说明：`03-章节写作.md` 等镜界文件也使用全角顿号、破折号，故「破折号」本身不算缺陷；本组破折号未计入。

---

## 五、反向证据（popwave 比镜界更清楚的地方）

1. **判据优于镜界。** `short-reviewer\SKILL.md:39`「最后情绪高峰之后，超过全文 10% 字数的篇幅仍在叙事，即判定为拖沓」——给出可判定的数字阈值。镜界 `03-章节写作.md:11` 同类只写到「节奏有呼吸感」，无判定标准。
2. **检查项与标准回指。** `pop-content-card\SKILL.md:100` 每条完成检查后标〔可截图〕〔可回看〕〔三可基础〕，把检查与上游标准一一挂钩。镜界 `14-画布构图指南.md:145-153` 自检清单只有问句，未标回指来源。
3. **硬约束成对、可查。** `pop-visual-comic\SKILL.md:158`「恐怖、灵异、悬疑→须用张力布局，不得用等分布局；高潮、名场面→须用大单页或张力布局，不得用等分多格页」，三组"条件→须/不得"并列。镜界 `14-画布构图指南.md:63-68` 同类内容夹叙夹议，指令密度更低。
4. **分支写法更省。** `pop-visual-pipeline\SKILL.md:85` 用"清点结果→对应动作"的竖线串把四路分支压进一句。镜界 `12-创作工具管理.md:3-13` 用表格+段落两层，同样信息占更多行。
5. **约束语气更硬。** `tool-download-webnovel\SKILL.md:33-35` 三条红线一律用"不得 / 必须"，镜界 `13-图像生成工具指南.md:38` 同类场景用「用户明确表示……时……无需重复追问」，语气偏建议。

（说明：第 2 条正是用户"判断给锚点"的正面样板，第 3 条是"硬约束用须/不得"的正面样板，这两处已达到或超过镜界水位。）

---

## 六、一句话结论

这批 skill 与镜界的差距**集中在「措辞」这一条**——语序、语病、书面化只是零散瑕疵（合计 27 处，多为缺空格与个别残句），真正成体系的是黑名单词仍在服役：「门禁 / 闸口 / 机器状态源」16 处、「叙事引擎 / 传导链」3 处、「XX器」自我定位 4 处、自造比喻 6 处，镜界通篇不用这一类词。

**最该先修的三处：**

1. `pop-visual-comic\SKILL.md:140` ——「旁白条每条上限80字……可直接放宽至80字」自相矛盾，是唯一会直接误导执行者读错的硬伤，改一个数字即可。
2. `pop-visual-comic\SKILL.md:137` 与 `:44`、`:54` ——「叙事引擎」「门禁 0」两处黑名单词，出现频次最高、最显眼；换成"叙事手法""第 0 道检查"。
3. `pop-visual-cover\SKILL.md:3`、`short-reviewer\SKILL.md:2`、`short-text-deconstructor\SKILL.md:2` ——三处「XX器」自我定位，是三条 skill 的开篇首句，改一句话即可对齐镜界命名风格。
