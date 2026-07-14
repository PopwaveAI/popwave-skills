# PRD: Context / Harness Engineering - AI Agent 的上下文工程（截图原文转写版）

> 沉淀日期：2026-07-06
>
> 来源：用户提供的两张腾讯学堂 AI 前沿培训长截图。
>
> 处理方式：按截图内容进行原文 OCR 转写，尽量保留原文顺序、标题、卡片、表格和 Q&A 内容；仅做必要 OCR 错字修正与 Markdown 分段，不做观点概括或二次扩写。

---

## 截图 1 原文转写


---


腾讯学堂 腾讯学堂·AI前沿培训

Context / Harness Engineering: AI Agent 的上下
文工程

从 Function Call、MCP、Skill 到 Context、Memory、Harness- 理解Agent如何获取信
息、执行任务、验证结果并持续运行

两个视角并行：作为 Agent 构建者怎么搭、作为 Agent 使用者怎么用。结合 WorkBuddy 与 CodeBuddy 的
实战案例，把 Agent 的基础组件、上下文工程、Harness 工程和下一阶段的 Loop Engineering 一次讲透。

分享时间： 2026.6.23 分享人： annelywu（武丽媛）·CodeBuddy  & WorkBuddy策略产品经理 主题：

AI Agent 的上下文工程

以下内容基于直播转写稿+PPT整理，由AI辅助生成，可能存在疏漏或表述偏差，最终以分享人原始材料为准。

annelywu （武丽媛）
CodeBuddy & WorkBuddy团队·策略产品经理
负责CodeBuddy与WorkBuddy研发与办公场景AI Agent的上下文策略设计与落地，主导两大产品
的核心上下文工程与场景化迭代。
从产品视角拆解Agent的运行机制：模型如何被引l导、上下文如何被管理、Harness如何让执行更可
靠，是这一线程在腾讯内部最贴近一线的实践者之一。

本次分享的两条主线：①Agent构建者视角 团队如何打造 Context 层与 Harness 层；② Agent 使用者
视角一 团队自己怎么用CodeBuddy/WorkBuddy把研发与办公流程harness化。


## QUOTE WALL·金句速览

模型=一个无状态的函数 System Prompt 负责引l Function Call 是 Agent 的
给什么上下文，就生成什么回 导，不能负责约束 基石
答；产品可以有状态，把状态挑 权限边界必须由系统执行，不能 模型负责决定调什么，Host 负
出来塞进上下文。 只写在 Prompt 里。 责真正执行—一Host 才是模型
的手和脚。

MCP不只是工具协议 按Agent意图组织工具 Skill ≠ MCP
包含 Resources / Tools / Pro 不要把四个API暴露成四个工 MCP 接入外部能力，Skill 保存
mpts 三类，是「Model Conte 具；create_issue一个工具就 经过验证的工作方法—一一段
xt Protocol」 而非 「Model To 够，把动作收敛成参数。 Markdown 写清楚步骤、约
ol Protocoll . 束、失败处理。

Context Engineering 的核 Prompt Cache的稳定性是 长内容留在文件，主上下文只
心追求 KPI 放摘要
相关、准确、及时——不是单 稳定内容放前面、历史只追加、 工具结果与工具定义都要渐进式
纯增加 token。 动态内容放后面，省钱也省延 加载，主上下文只保留诊断入
迟。

聊天历史≠Memory 为什么 Procedural Memor Humans steer, Agents ex
聊天历史记录发生过什么，Me y不进V1 ecute
mory决定哪些历史还能继续 容易把局部经验升为通用策略 十为通用荣略 人类掌舵，Agent 执行。目
用。 这种沉淀更适合做成Skil 标、验收标准和最终责任，仍然
，按需加载。 需加载 在人。 在

Agent = Model + Harnes Harness跟着模型一起进化 实现和测试可能共享同一个误
老约束要随模型升级删除；不同 解
实际评估的从来不是单独模型， 模型适配不同Harness（Claud 核心业务正确性的反馈信号缺
而是「模型+Harness」的组 e 用 edit，GPT 用 apply_patc 失，是当前 AI编码最难的缺
合。 h) 口。

代码库的Harnessability决 AI会反向促使技术方案标准 LoopEngineering的前提
定建设难度 化 Context与Harness 都成立且
越是急需 Harness 的老系统, 选技术栈时多问一句「是否便于 运行良好，否则只是AI帮你把
往往越难 Harness 化。 AI理解、修改、验证」。 token用掉。


## TABLE OF CONTENTS·内容纲要


### 1.01 基本组成:模型、Function Call、System Prompt、MCP、Skill、Plugin
··模型为什么没有状态、能力如何形成的三阶段、把模型看成一个函数
··Function Call 五步协议；System Prompt 的角色与边界；MCP 三类资源；Skill 与 Plugin 的职
责差异


### 2.02 全景视图：用一个调研任务把Agent串起来
·一次完整的ReAct循环=判断+行动+观察
··Sub-Agent怎么用、为什么每多走一轮上下文都会越堆越大

3. 03 Context Engineering：模型看什么、什么时候看、看多少
··五类动作：写入／选择／检索／压缩／隔离
··Prompt Cache 的稳定性、工具与工具结果的渐进式加载、高质量 MCP Server 的设计原则

4. 04 Memory：让 Al 越用越懂你
··WorkBuddy 长期 Memory 的五类记忆与作用域分层
··为什么V1不收Procedural Memory；记忆为什么必须可撤销

5. 05 Harness Engineering：引导、约束、整合

··业界三家实践：OpenAl（Codex大规模生产）、Anthropic（长任务+对抗式评估）、
LangChain (Agent = Model + Harness)
··WorkBuddy自己的两个目标／五个层次；团队作为使用者的四类组件实践

6. 06 真实落地的反思：六类问题与AI自治边界
··业务正确性验证缺口、Harnessability门槛、案例适用边界
··Al推动技术方案标准化、Harness是持续投入、人仍然负责主线任务

7. 07 下一阶段：Loop Engineering 与 Q&A 总结
··从单次 Prompt扩展到长期运行的任务循环
··Q&A 精选：Cache、压缩、Sub-Agent、Memory 提取、评测策略

Foundations·基本组成
01
Agent的基石：模型、工具、提示词与协议

在讲 Context 与 Harness 之前，先把 Agent 的底层零件讲清楚 模型为什么需要外挂、Function Call
怎么往返、System Prompt 该写什么不该写什么、MCP与Skill的职责边界，是后面所有结论的前提。

模型本身没有状态

模型只看得到这一次调用中被放进上下文的内容一 一没有长期记忆，不主动访问世界，也不天然执
行动作。模型提供语言和推理能力；Agent产品负责补上信息、工具与状态。

没有长期记忆 不主动访问世界 不天然执行动作
每次调用都是独立的 不会自己上网、查文件 无法直接改文件、发请求
不依赖上一次会话，除非显 所有对外M信息必须由Host 动作要通过FunctionCall
式塞进上下文。 喂给模型。 协议交给 Host 完成.


### 1.2 模型能力的三个形成阶段

预训练·阅读海量文本，学习语言、世界知识与基础推理。这一阶段的模型像「饱读诗书但
只会续写」。

后训练·通过问答、工具调用与安全边界数据，把模型从「会续写」变成「会听指令］ 后训练·通过可答、工具调用与安全边界数据，把模型从「会续与」变成「会听指令
你问中国首都在哪，它能答北京。

偏好优化与强化学习·在多条候选路径中选最优解。比如训练做咖啡的机械臂，按口感、效
率、规范打分，让模型收敛到最优做法。

Key Insight
训练塑造模型的能力，上下文提供当前任务的材料一一能力是先天，上下文是后天。


### 1.3 把模型看成一个函数

‘‘（+上++工+）=
可以有状态一一每次调用前把有状态的内容挑出来，塞进上下文。

系统提示词 工具定义 会话历史 其他上下文 用户指令 生成结果


### 1.4 FunctionCall：模型与外部系统之间的结构化协议
OpenAl 提出 Function Call，本质是一个约定：模型按 JSON Schema 输出意图，Host 收到意图后替
模型执行一—Host是模型的手和脚。一次完整的 Tool Call走五步:

提供工具定义·Host把工具的名称、描述、参数、必填字段告诉模型。

模型生成调用请求·模型按Schema 输出tool_call，比如 模型生成调用请求·模型按Scnema输出toolcali，比如
get_match_status（{competition:"世界杯"，team:"A 队"})。 get_match_status（{competition:"世界杯"，team:"A 队"}）。

Host 验证并执行·检查权限、调用真实 APl（关键步骤一—执行权限只在Host）。

返回 Tool Result+把结果塞回上下文，比如「A 队 2:1，22:51 更新」。

模型回答或继续调用·得到结果后生成自然语言回答，或继续下一轮工具调用。

Warning
名称含糊、说明重叠、参数缺少约束，都会让模型选错工具或填错参数一一工具描述本身就是上
下文。


### 1.5 SystemPrompt：稳定的工作角色，不是安全边界

不同产品的基调不一样：Coding产品、General Work产品、Design 产品的角色目标都不同。
System Prompt一般包含：角色与目标、能力清单、工作原则、安全规则、交互方式、当前环境等。

System Prompt 负责 外部系统负责
引导模型行为 强制执行约束
指定模型在产品里扮演什么角色、什么时候查 权限校验、Approval Gate、审计日志——这
资料、什么时候验证结果、回答要简短还是详 些必须由代码而不是Prompt来保证.
细。

Boundary
不可以写在 Prompt里：删数据、发布命令、敏感内容审批一一这些必须由工程层强制约束。


### 1.6 MCP：外部能力的标准化接入协议

Anthropic 在 2024 年底发布的 Model Context Protocol，是Agent 调用外部能力时的「USB 接
口」一 同一接口接入 GitHub、腾讯文档、知识库等不同系统。

MCP不是「ModelToolProtocol」，三类资源缺一不可:

组件 说明 由谁驱动

Resource 由 URI 标识、可被 Agent 读取的资源（文件、数据库、实时数 MCP Server 更
据) 新

Tools 模型可调用的function -MCP最被熟知的部分 模型驱动

Prompts 预先组织好、可复用的一组消息(类似MCPServer自带的Skill) 用户驱动

Standard
MCP 统一连接协议，但不自动解决认证、数据授权、网络隔离与高危审批一—这些仍是产品层
的责任。


### 1.7 为Agent 设计可用、可控、可继续的工具

引l用Anthropic「用MCP构建可落地生产系统的Agent」一文：要按Agent意图组织工具，而不是
把底层API 一一暴露。

X 反面做法 正面做法
把四个API暴露成四个工具 按用户意图收敛
create_issue / add_description / add_tag / 只做一个create_issue，把描述、tag、附件
add_attachment 各做一个tool—模型选择 作为参数；甚至 issue 的 create ／ update / d
困难、上下文膨胀。 elete／close 都可以收敛成一个 action 参
数。

设计标准：让 Agent 容易选、参数容易填、失败后知道怎么修正——三件事缺一不可。MCP Apps 还
允许返回结构化数据+Ul（看板、图表、表单），WorkBuddy右侧panel就是这种模式。


### 1.8 Skill：定义一类任务的稳定做法

工具定义一个动作；Skill定义一类任务的做法 一比如「在某仓库提交PR」需要读规则、检查
git status、阅读 diff、运行测试、生成标题说明、push 并创建 PR—一这一连串没法用一个工具
完成。

Tool Skill
一个入口、一组参数、一次执行 一组参数、一次执行 步骤+约束+脚本 +失败处理+验收标准 步骤+ 约束 + 脚本+ 失败处理+ 验收标准
细粒度、可被任意组合调用 细粒度、可被任意组合调用。 本质是一段SKILL.md，可以调用MCP工具或 本质是一段SKILL.md，可L以调用MCP工具或
本地脚本，是「经过验证的工作方法」。

Position
MCP接入外部能力；Skill保存经过验证的工作方法。两者可以组合一一比如「发周报」SkilI调
用腾讯文档 MCP + 知识库 MCP + 本地脚本。


### 1.9 Plugin：能力的打包与分发

Plugin 把一组相关能力打包成可安装、可分发的单位，包含 MCP／Connector、Skills、Rules、
Hooks、Assets 五类组件。作用域和 Skill、MCP一样，可以装在用户级、Workspace 级或当前会话
级。

Function Call MCP Skill Plugin
请求动作 接入外部系统 定义任务方法 安装与分发

TheBigPicture·全景视图
02
把零件串起来：一次完整的Agent调研任务

没有一个工具能直接完成「调研OpenAl/Anthropic/LangChain的Harness实践，输出带弓I用的大
纲」这样的任务。Agent 要编排上下文、工具与流程，而每多走一轮，对话历史就越堆越大一 -Context Context
Engineering 由此登场。

2. 1 用一个Case走完全链路
用户输入：「调研 OpenAl、Anthropic、LangChain 的 Harness 实践，整理核心观点／解决的问题/
团队借鉴，输出带引l用的大纲。」Agent 会经历多轮ReAct（判断+行动+观察）:

检查Workspace·有没有相关的项目规则、已有调研、输出格式约定？避免重复调研。

读取相关Memory·用户希望先给结论、不要AI 味、采用什么参考来源。

加载调研Skill·先看官方博客／论文／演讲，再看哪些网站一一沉淀过的研究方法。

查询内部资料·内部资料的可信度通常更高，先扫一遍。

分配 Sub-Agent-派出三个 Sub-Agent 分别调研 OpenAl、Anthropic、LangChain
（Sub-Agent的上下文与主Agent隔离，独立完成任务后只回传结果）。

汇总与补充证据·主Agent拿到三份调研结果后做汇总、交叉补证。

形成大纲并保存·输出带引|用的最终大纲。


### 2.2 每多走一轮，对话历史就越堆越大

Context Window 容量固定，但多轮 ReAct会让会话历史持续膨胀一一这就是Context
Engineering 要解决的问题：在容量有限的情况下，决定哪些信息进、什么时候进、什么时候出。

问题 处理 底线
历史持续膨胀 压缩、移交文件 只留结论与证据位置
每轮请求都带着前文，长任 把工具结果离线到文件，主 必要时模型还能重新加载
务很快撞上上限。 上下文只留摘要与诊断入 —上下文是工作面，不是
档案库。

Context Engineering
03
模型看什么、什么时候看、看多少

一次模型决策之前，设计哪些信息能够进入上下文、以什么形式进入、放在什么位置、什么时候更新或移出
-目的是提高模型做出正确下一步决策的概率。追求的是相关、准确、及时，而不是单纯增加token。


### 3.1 Context Engineering 的五类动作

把目标、规则、环境、任务状态放进上下文一一模型不感知时间、不感知系统

## 01 写入 Write
类型，必须显式喂。

System Prompt、工具、Skill、MCP 全塞进去会爆一一只放当前步骤需要的信

## 02 选择Select
息。


## 03 检索 Retrieve 没塞进去的，提供按需查找能力 检索历史、资料、工具，再决定加载。


## 04 压缩 Compress 长任务必然膨胀一一保留结论、证据位置和下一步，剔除过时工具结果。


## 05 隔离Isolate Sub-Agent 旁支独立处理，只带回结果一一主上下文保持清量。


### 3.2 Prompt Cache：相同的前缀，不必重复计算

每次模型调用都要重新计算所有输入。但每次新增内容只在末尾 前缀如果稳定，模型方就可以复用
计算缓存。Cache 命中的 token 比正常 input 便宜很多。

稳定内容放前面 历史只追加 动态内容放后面
System Prompt 等 不替换旧消息 当前时间等
固定不动的内容，让Cache 会话历史从不删除中间，只 容易变化的内容放在Cache
全程命中。 append 新内容。 失效区。

User Feedback
近期不少用户反馈「Cache 怎么没命中、积分变多了」一一Cache 失效通常发生在模型方，产
品层会持续在系统提示词与模型方一起把命中率维持在高位。


### 3.3 渐进式加载：长内容留在文件，主上下文只留诊断入口

工具结果太长 工具定义太多
Bash 输出、长文件读取 Skill、MCP 工具列表
分页／截断／写文件一一只把首尾或关键片段 暴露能力类别／Server简介→②ToolSea
塞回上下文，并告诉模型完整内容存到了哪个 rch搜索候选→③只加载选中工具的Schem
文件，需要时去那里读。 a。Skill同理：先看名称与描述，再读 SKILL.
md.

Design Rule
错误信息要包含失败原因、可修正参数、是否可重试 错误信息要能指向下一步，而不只是报
告失败。


### 3.4 高质量McPServer：按Agent意图组织，减少上下文浪费

碎片化细粒度工具会带来三宗罪：多次调用、选择困难、上下文膨胀。少量高层任务工具一—按
Agent 意图设计、关键字段进入模型上下文、完整看板/图表交给 UI 层一一才是生产级做法。

少而不重叠 按任务意图设计 权限与破坏性标注
按任务意图收敛工具数量， 工具描述围绕「用户什么时 高危操作必须显式标记，触
避免相似工具互相干扰。 候用」，不是「底层API长 发审批流程。
什么样」 什么样」。

搜索文档+沙箱执行 用Eval验证可用性 关键字段→模型上下文
开放 ToolSearch 给 Agent 有评测集，避免 MCP 改动 结果分两路：精炼字段给模
自查能力，沙箱保证可回 后悄悄劣化。 型看，完整数据走 UI 渲
滚。 染。


### 3.5 WorkBuddy的外接能力：四种形态怎么选

没有一种形态对所有能力都最优。要看权限风险、更新频率、上下文成本、执行延迟 再决定接入方
式。

形态 典型场景 取舍

内置 Tool 读文件、执行命令 延迟低，权限与交互可深度集成

MCP / Connector / SDK 腾讯文档、IMA、网盘等外部系统 服务端集中维护与复用

Skill 团队高频、稳定工作流程 沉淀步骤、判断与失败处理

Plugin 组合+ 流程+ 规则+ Hook 组合与分发单位

Memory
04
聊天历史记录发生过什么； Memory i 决定哪些历史还能继续用

---

## 截图 2 原文转写

Memory
04
聊天历史记录发生过什么；Memory决定哪些历史还能继续用

[Al越用越懂你」是用户最直观的诉求一一不希望反复交代背景。WorkBuddy把长期记忆拆成五类，并
明确为什么V1 不收 Procedural Memory；记忆按作用域分层、分阶段注入、必须可撤销。


### 4.1 WorkBuddy 长期 Memory 的五类

Semantic语义事实 UserKnowledge 用户知 BehaviorSignals行为信
识背景 号
稳定事实与长期偏好
专业背景与熟悉领域 从多次交互观察到的稳定使用习
与情景无关、长期稳定,
愤
例：「用户居住在中国深 让模型知道用户熟悉什么、
用作调节交互策略，例：
圳。 不熟悉什么，避免过深术语
「回答前先查看Workspac
或过浅回答。例：「熟悉C
el。
ontext Engineering」 .

Style表达偏好 Conversational 会话事
「怎么说」而不是「事实是什 实
么」 不是长期记忆，但用作 RAG 的
例：「先给结论，少空话, 对话事实
去 AI味」。 当前目标、决策与进度，已
完成什么、下一步做什么。


### 4.2 为什么 V1 不收 Procedural Memory

ProceduralMemory记录的是某次任务里的程序性策略（例：「调试任务都要重启服务、再查日
志」）一一风险是把局部经验升为通用策略，干扰泛化与可控性。

× 风险 替代方案
类似动态 System Prompt 沉淀为 Skill
①局部经验误升为通用策略；②机械复用历 稳定经验→人工确认适用范围→写成Skill
史步骤；③缺少版本、评测、审批与回滚； (步骤+约束+脚本+验证方法）→按需加
破坏泛化与可控性。 载。Memory 提供推理前提；Skill 提供经过
验证的行动方法。


### 4.3 同一类记忆，可以在不同范围内生效

作用范围越大，写入和晋升门槛越高。最强的注入是「冷启动注入」一一只放少量高置信、高相关的人
和项目记忆。其他记忆按需检索。

外 团队 团队流程、术语、权限边界一一 促进人和多Agent 的协作

用户 长期偏好、职业背景一一减少反复自我介绍

Workspace 架构约定、项目决策、活跃计划

Thread 当前进度、工具、未完成项

内 当前轮 选中的代码、上传的文件 临时上下文


### 4.4 分阶段注入+必须可撤销 分防段注入+必须可撤销

会话开始·冷启动注入少量高置信记忆（人和项目级别）。

理解请求·根据当前query做意图识别，按需注入相关记忆。

执行中·继续按需检索；任务结束后按结果提取记忆，做去重／冲突检查／作用域判定。

必须可撤销·查看来源、纠正替换、缩小作用域、停用删除、回滚一 记忆不断变化，可撤
销是底线。

Goal
让正确的历史记忆在正确的时候、以正确的作用域、用正确的方式重新出现。

Harness Engineering
05
Agent的引导、约束与整合

Context Engineering 解决 「Agent 看什么、什么时候看、看多少」；Harness Engineering 解决
「Agent 在执行过程中如何被引导、如何被约束、如何被组织成稳定系统」。Humans steer,Agents
execute一—人类掌舵，Agent 执行。


### 5.1 Harness的三层涵义

Steer挽具·引导 Constrain 安全带·约束 Integrate装备·整合
定义执行方向 限制操作范围 组织系统组件
System Prompt、规则文 权限、Sandbox、Approva Tools、MCP、Memory、S Tools、MCP、Memory、
件、Skills、Task——告诉 I、测试与审计——出错时影 ub-Agent、CI—把分散
Agent 该怎么走。 响有限。 能力组成可运行的整体。


### 5.2 业界三家实践

讲 Harness 之前，先看 OpenAl、Anthropic、LangChain 各自的实践—证明价值，但每家都漏掉
了一些东西。

OpenAl· Codex
Humans steer, Agents execute.3 人小组用 Codex 在 5 个月内从空仓库做出 100 万行代
码、1500+PR，并投入内外部使用。配套环境包括：浏览器／DOM／日志／监控、Linter+
结构化测试、AGENTS.md文档目录入口、周期性扫描自动开重构PR。证明大规模代码生产可
行；但业务正确性验证仍是缺口。

Anthropic · Long-running Harness
Claude 在跨多个上下文窗口执行长任务时有两种失败模式：一次承担过多（在一个窗口内试图
完成整个项目，中途上下文耗尽）和过早判定完成。解决方案：功能清单（JSON）、一次只处
理一项、init.sh 统一初始化、端到端验证、进度文件 + Git 历史。
WorkBuddy 自己的对应：增加 Task／TodoList 工具，让模型先拆解大任务，再逐步标记完
成。

Anthropic·对抗式评估三角色
借鉴 GAN 思路：Planner（规划，定义范围与交付物）→Generator（按 sprint 实现，自检
后提交）→Evaluator（独立验收，用Playwright按真实路径核查）。 口提父
用户级借鉴：执行和验收尽量分开一一用Sub-Agent或新会话切换不同模型独立验收，避免模
型对自己产物打高分； plan 模式+ WorkBuddy.md / CodeBuddy.md 写入标准。

LangChain · Agent = Model + Harness
LangChain 把模型之外的一切都纳入 Harness：System Prompt、Tools、Skills、MCP、文件
系统、Sandbox、Browser、Hooks、持久状态。核心要点：模型和 Harness 在共同进化。不
同模型适配不同Harness Claude 的 edit 工具与 GPT 的 apply_patch 工具不能互换;新工
具反哺训练数据，下一代模型就会更倾向调用它。


### 5.3 WorkBuddyAgentHarness：两个目标，五个层次

两个目标：①提高Agent 首次执行的正确率（前置弓l导Feedforward）；②提供反馈循环（让
模型从环境中拿到Feedback）。五层共同工作一运行环境是地基，迭代层是闭环。

Harness持续调整：随模型能力提升精简上下文；针对新问题增加约束；适配
L5 迭代层
不同模型的工具差异

编排层·Orchestration渐进式加载、意图识别、多模型路由、Teams 多Agent、并行工具调用

可纠正的 Tool Result、编辑前时间戳校验、外部验证信号（lint／类型检查/
L3 反馈层·Feedback 测试／构建）、Audit Log

L2 引导层·Feedforward项目上下文、环境上下文、规则与风格、工具使用规则、Skills 与规则文件

Sandbox、文件系统、Shell、浏览器、Allowlist / Denylist、Approval
运行环境层
Gate、Audit Log


### 5.4 引l导层Feedforward：信息放在合适层级，低频内容按需加载

结构上看是「稳定前缀+持续追加+本轮动态」三段式一一前两段进Prompt Cache，后一段处理动
态内容。

稳定前缀 持续追加
系统提示词、固定工具集 会话历史、本轮工具调用
全程Cache 命中，控制成本与延迟。 只 append，从不替换中间，保持 Cache 链。


### 5.5 反馈层Feedback：错误信息要能指向下一步

每次工具调用后，把执行结果（成功／失败）以清晰的方式回流给模型 成功时告诉文件存到哪、生
成了什么；失败时告诉参数类型错在哪、是否可重试。可纠正的Tool Result是反馈层的核心。


### 5.6 编排层Orchestration：明确调用顺序、上下文范围、触发条件

渐进式加载 意图识别&System Reminder
Skill／MCP／Tool 三类全部支持一—主上下 用户安装了多个Skill/MCP，靠意图识别选定
文只放摘要，按需展开。 可能用到的，注入 system_reminder 提醒模
型。

多模型路由 Teams 多 Agent
Claude／GPT适配不同的edit工具，按模型 WorkBuddy的「专家团」概念- —用户可以
分发。 创建自己的专家团并行协作。

并行工具调用
每次模型调用都是消耗，能并行的工具一次返
回，减少 LLM Call 次数。


### 5.7 Harness选代：随模型与场景持续进化

一个 project_layout 进上下文；后来模型学会用 glob ／ grep ／ list_directory 探索，就把
这个上下文删掉，让上下文更轻量。

新模型不一定全方位变好·GPT一段时间输出过长，加「精简、不啰嗦」的约束；Claude
一段时间过度输出markdown，加「只在必要时写markdown」的约束。约束随模型表
现增删，不是一次性写定。

能力越来越多，渐进式加载是必选·内置工具、MCP、Skill都越来越多 靠渐进式加载
+意图识别才能避免污染上下文。

Iteration Rule
一次失败先观察；重复失败或高风险问题再改Harness- 不要追每个偶发现象。


### 5.8 WorkBuddy团队自身的Harness实践（使用者视角）

作为 Agent 使用者，团队怎么用 CodeBuddy ／WorkBuddy 把研发流程 harness 化？归为四类
组件一一这个组合形成了一个持续过程。

组件 具体落地 解决的问题

1上 分层规则文件（根目录codebuddy.md写架构、子目录补模块规 提供规则与任务信
下文 则）、OpenSpec（大功能变更前必读必写）、Skills（agent-browse 息，让Agent 一
工程 r、dogfood、open-spec apply)、Slash 命令 (/commit、/create- 次拿对足够前提
issue)

2架 .mdc 规则文件、Git Hooks（提交 PR 时检查是否关联 issue ／ 是否有 把规则转化为可执
构约 OpenSpec）、Cl门禁、独立的「架构守护Agent』 行检查，阻止已知
束 违规进入仓库

3反 Post-edit checkpoint、本地检查 / Cl、Dogfood、Agent Browser 修正本次执行；把
馈循 -发现工具卡住或缺失就喂回 Agent，自动补 CI 测试 可观察证据回流给
环 Agent

4熵 重复检查、定时扫描、清理过期规则与代码漂移、定期对齐 OpenSpe 处理跨任务积累的
管理 c 与现网代码(不一致就提issue 或Agent自己开 MR 修复) 漂移，避免规则与
·GC 代码失同步

Loop
上下文工程提供信息；架构约束阻止已知违规；反馈循环修正本次执行；熵管理处理跨任务积累
的漂移- 一四件事形成一个闭环。

Reflections·真实落地反思
06
六个还没被解决的问题 个还没被解决的问题

OpenAl、Anthropic的文章夸得天花乱坠，但每家产品和基建都不一样一案例只能证明在他们的特定环
境中可执行。我们作为使用者仍然要关注实验条件、可复现细节，以及他们没有讲的部分。


### 6.1 问题一：功能和业务正确性的验证缺口

实现和测试可能共享同一个误解一一这是当前最难的问题。PRD通常描述单向功能，但很难覆盖
所有功能组合后的行为。

举个例子：会话有「归档archive」和「置顶 pin」两个功能。Agent可以分别实现，并通过单
元测试保证各自正确。但组合后的业务问题：已置顶的会话能否被archive？archive后是否保
留pin状态？恢复archived后是否仍出现在置顶区？这些组合行为很难在PRD里写全一—如
果没说清楚，Agent实现和测试会共享同一个误解，业务规则偏移时测试也跟着偏移。

Open Problem
当前只能靠测试同学和产品同学用人的知识来定义两功能合并时正确的产品表现是什么一一这个
问题暂时没有好解法。
「边界清晰、可验证、失败代价可控」的工作优先自动化。


### 6.2 问题二：代码库的Harnessability决定建设难度

越是急需Harness 的代码库，往往越难Harness 化一—因为harness 化需要清晰的数据上报、清
晰的看板、模块解耦、不耦合的业务逻辑作为前提。老系统恰恰不具备这些。

高 Harnessability 中 Harnessability 低 Harnessability
一次性脚本／内部工具 公开API／跨系统 核心业务／老系统
结构清晰，验证简单——优 有contract，可以约束，但 结构耦合、可观测性差
先在这一层落地Agent自 要谨慎。 先约束新增和修改部分，老
治。 的部分不要急着改。

Strategy
老系统：先从结构清晰、修改频繁、价值较高的子模块开始；先约束新增和修改部分；验证后再
逐步扩展一一避免给一段无法维护的复杂老结构盲目铺规则。


### 6.3 问题三：案例来源与适用边界
OpenAl 和 Anthropic 文章的案例来源都是模型厂商或 Agent 框架团队，结论都依赖他们特定的环境
证明了价值，但要在自己的环境里重新验证，关注实验条件、可复现细节和未覆盖问题。另一个角
度：这些厂商都做Al Coding，宣扬这一概念是自己的商业利益- -结论可信，但动机要看清楚。


### 6.4 问题四：AI可能促使技术方案更加标准化

选技术栈时除了考虑性能、开发效率、生态，还要多问一句「是否便于AI理解、修改、验证」
-Al友好的技术栈在Agent中的稳定性更高。

方案A·灵活但不标准 方案B·统一项目结构
不同项目接口与流程差异大 清晰架构规则、测试方法、发布流程，已配好Harnes
过去看是优势- 一 团队可以按场景定制；AI时
当两套方案都满足业务要求时，团队会优先选
代是劣势——Agent 需要重新理解每个项目。
3- 一因为它在Agent中的稳定性更高。

Open Question
模板更新如何同步到已有项目？自然语言规则如何做版本管理和测试？这些是Service
Template/标准工程方案接下来要解的问题。


### 6.5 问题五：Harness建设需要持续投入
OpenAlCodex那篇文章里：3人5个月，从空仓库到100万行代码 this isn't something you
can jump into for quick results.

3人 5个月 ~100万 1500+
小组规模 建设周期 行代码产出 PR 数量

Trend
工程严谨度正在转移到环境、反馈回路和控制系统 -Harness需要随模型、项目和用户反馈
持续维护，无法一次配置完成。


### 6.6 问题六：人仍然负责主线任务

Harness 优先覆盖重复、确定、可验证的工作。需要探索和业务判断的工作，仍然由人主导。

The danger is stopping having an opinion when loops run autonomously.
-HarnessEngineering实践反思 HarnessEngineering实践反思

Boundary
AI帮我们提高执行效率；但团队仍然需要保持对代码逻辑和架构的理解，并在出现问题时定位
到根因一—而不是「没有一个人清楚，只有AI清楚」。目标、验收标准、最终责任，仍然在

What's Next·Loop Engineering & Q&A
07
下一阶段：从单次请求到长期循环

继 Prompt Engineering、Context Engineering、Harness Engineering 之后，6 月份提出的Loop
Engineering 还没有形成统一定义一核心是Agent 如何被触发、连续执行、验证结果、记录、再度运
行。把工程对象从单次Prompt扩展到可长期运行的任务循环。


### 7.1 Loop Engineering 的位置

LoopEngineering·循环工程任务如何被触发、继续与停止

L3 HarnessEngineering·缰具工程Agent如何被引导、约束和验证

L2 ContextEngineering·上下文工程本次决策前模型该看什么

PromptEngineering·提示词工程本次请求怎么表达 ·提示词工柱 本次请求志么表达

Prerequisite
LoopEngineering 能实现的前提是Context Engineering与HarnessEngineering都成立且
运行良好一—否则只会变成「Al帮你把token用掉」。Loop不会自动产生正确目标，最终仍
需人审批。


### 7.2 Loop的典型形态：每天检查依赖安全更新

定时触发→独立环境→调SKilI与工具→状态记录→验证信号→通过则发PR草稿／失败则修正或
停止一一这就是一个Loop。但是否能让Agent 自动执行某个Loop，需要先定义「能做什么、不能做
什么、什么时候触发、操作什么」，再增加 Credit／Approval 限制。

Roll-out
不要一上来就让Loop自动跑一一先每天手工运行一次观察表现，有问题再加约束。这个自动化
过程需要人不断调整。


### 7.3 Q&A精选

Cache为什么没命中？ 多轮后约束怎么不丢？
来自用户的高频反馈 Skill / Memory的实战
Cache主要发生在模型方。系统提示词把固定 放在user消息里的约束随历史压缩会丢失；
内容放前面、变化内容（如当前时间）放后 放在codebuddy.md/agent.md里的不会被
面；ToolSearch结果追加到上下文末尾，不会 压缩。这是稳定约束的最佳位置。
影响 cache。

如何加速Agent输出？ 上下文压缩怎么做？
综合策略 两层策略
①大需求用并行Sub-Agent/ Teams;②简 ①工程压缩：剔除ToolResult 大对象（如写
单问题用flash模型；③用Ask模式（工具集 文件的完整内容）、保留file path 和工具
更小）。 名；② 模型压缩：精细的 system prompt 让
模型把关键步骤结构化保留下来。

怎么做评测？ Memory提取的触发条件？
建议从真实业务出发 异步离线
20-50个真实场景case即可；定义任务的ch 每天晚上触发用户当日任务记录与会话历史的
eckpoint/checklist；既有公开benchmark 整理、清洗、提取；冲突检查发生在 merge
（SWE-bench）也有自建评测集；每接入新 阶段，决定是update／delete／add哪条记
模型必跑评测。 忆。

CodeBuddy与Cursor的差异？ 不同模型怎么分工？
越来越在产品力 支持自定义Sub-Agent
Agent层和模型层各家差异越来越小；下一步 可以创建一个plan类型的Agent指定Claud
比拼的是产品力一—比如Codex的compute e，编码Agent指定GLM，reviewAgent再
ruse/browseruse能进一步解放coding时 指定Claude——通过自定义Sub-Agent完
的验证工作。 成多模型分工。


### 7.4 结语：模型决定上限，Context与Harness决定能不能稳定落地

Closing
模型能力决定AI产品的上限；②Context和Harness决定这个上限能不能稳稳的落地；
Agent 帮助我们快速执行、验证和加速迭代；④但人仍然是选择方向、定义标准、承担责任的
那一方。
「人：选择方向、定义标准、承担责任」「Agent：执行、验证、加速迭代」 「人：选择方向、定义标准、承担责任」 「Agent：执行、验证、加速迭代」

加入AI前沿学习交流群

更多AI好课开发中，第一时间获取AI分享信息和学习资料，与司内小伙伴交流。

---

## OCR 说明

- 本文档为截图原文转写，不是概括版。
- 少量极小字号、跨列卡片、英文专有名词可能存在 OCR 误识别；已对明显错误如 `Al` / `AI`、`PromptCache` / `Prompt Cache` 做了基础校正。
- 如后续拿到 PPT 或直播转写原文件，建议用源文件再做一次最终校对。
