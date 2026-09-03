# 长线剧情连贯性 · 外部技能调研盘点

> 调研日期：2026-09-03 ｜ 范围：GitHub 开源 · SkillHub 技能商店 · 国际 Agent 生态
> 目标：为 popwave 长篇小说创作管线找到强化「长线剧情连贯性」的外部参考
> 配套：本目录为「外部参考skill」资产，可放下载到本目录的第三方 skill 副本、或借鉴笔记

***

## 一、核心结论（一句话）

外部主流方案解决长跑剧情跑偏，靠的不是"写得更好"，而是**三件外挂物**：

1. **状态/账本文件** —— 每章创作前强制读取的"唯一真相源"（当前状态、待解决伏笔、支线进度、物资账、情绪弧线），让 AI 不必全靠记忆。
2. **外挂式连续性校验脚本** —— 用确定性规则（死角色行走 / 契诃夫枪未触发 / 道具链 / 时间锚 / 关键数字）在改写后机械化扫描，替代"让模型脑内自查"。
3. **伏笔/承诺生命周期台账** —— 把"埋线→生长→回收"从自由发挥变成显式状态机（planted → building → paid / dropped）。

***

## 二、★ 长线连贯机制聚合清单（跨项目提炼，最值得借鉴）

| 机制                | 出处                               | 做法要点                                                                  | 对我们价值                               |
| ----------------- | -------------------------------- | --------------------------------------------------------------------- | ----------------------------------- |
| **伏笔生命周期台账**      | NovelForge Agent / Story Skills  | 每根线记 planted→building→paid/dropped；承诺(promise)与回收(payoff)一一对账，埋1揭1硬底线 | 高 —— 强化 plot/outline 的"线账本"         |
| **每章必读状态文件**      | Novel Assistant / Novelix        | 写章前强制读"当前状态+待解决伏笔+上一章摘要"，写后回写                                         | 中高 —— 我们的 write 已读近5白描卡，可补"伏笔池/支线板" |
| **跨章一致性四表**       | Novel Writer Workflow            | 道具链表 / 时间锚表 / 术语表 / 关键数字表，脚本机械扫描                                      | 高 —— 可直接进 review 做脚本化校验             |
| **确定性连续性引擎**      | Story Skills                     | 死角色行走、回报早于铺垫、未触发契诃夫枪、陈旧故事状态，规则检测                                      | 高 —— 外挂式质量门禁典范                      |
| **37维/33维分级校稿**   | Novel Suite / Novelix            | 统计学脚本 + LLM 评估；OOC/时间线/战力崩坏/流水账等维度                                    | 中 —— 我们的 review 可扩维度清单              |
| **章节接受门 + 检查点**   | NovelForge / Novel Suite         | 章纲未确认不准写；每章快照可 rollback                                               | 中 —— 我们已有人体门禁，可加强 rollback          |
| **向量/BM25 回捞片段**  | NovelForge / Novelix / OpenNovel | 写章时按相关性检索过去文件片段，注入上下文                                                 | 中 —— 长线设定一致性增强                      |
| **subject+时间戳审计** | NeuroBook / Bookwright           | 每个角色/物品/势力当作有状态主体，记录"何时获得/改变"，可审计                                     | 中 —— 匹配我们"金手指/养成"状态追踪               |
| **卷节奏板**          | NovelForge                       | promise / midpoint / climax / payoffs / lingering mysteries           | 高 —— 匹配我们的"卷纲锚点区"                   |
| **八段式分形结构**       | SkillHub long-novel-creator      | 全书八段式 + 每章八段式层层嵌套，节奏自洽                                                | 中 —— 结构防失控，非本管线重点                   |
| **信息边界矩阵**        | Novelix                          | 每角色"已知/未知"信息边界                                                        | 中高 —— 服务 POV 与反转严谨性                 |

***

## 三、候选清单 · GitHub 开源可跑

| # | 名称                        | 地址                                                     | 类型                     | 长线连贯核心                                                | 可借鉴度  |
| - | ------------------------- | ------------------------------------------------------ | ---------------------- | ----------------------------------------------------- | ----- |
| 1 | **Novel Suite**           | <https://github.com/alonegg/novel-suite>               | Claude Skills 套件 (MIT) | 8 Bank 长期记忆 + 37维校稿 + 伏笔账(埋1揭1) + 章纲确认门 + 每章快照        | ★★★★★ |
| 2 | **Novelix**               | <https://github.com/zxerai/novelix>                    | Agent 框架 / npm         | 7 真相文件(物资账/伏笔池/情绪弧线/信息矩阵/支线板) + 33维审计闭环               | ★★★★★ |
| 3 | **Story Skills**          | <https://github.com/danjdewhurst/story-skills>         | Agent Skills (MIT)     | promises/payoffs 承诺回收账 + 确定性连续性引擎                     | ★★★★★ |
| 4 | **Novel Writer Workflow** | <https://github.com/GonsonInter/novel-writer-workflow> | Claude Skills (MIT)    | 跨章一致性四表 + 硬约束脚本 + 钩子/正文核对，实战13万字                      | ★★★★★ |
| 5 | **NovelForge Agent**      | <https://github.com/zlx362211854/novelforge-agent>     | Agent 框架               | 角色状态表每章必查 + BM25检索 + 伏笔生命周期 + 章节接受门 + 卷节奏板            | ★★★★★ |
| 6 | **Webnovel Writer**       | <https://github.com/lingfengQAQ/webnovel-writer>       | 中文网文插件                 | 初始化→卷纲→写章→审查→记忆沉淀→状态查询；Consistency/Continuity Checker | ★★★★  |
| 7 | **Bookwright**            | <https://github.com/jmorenobl/bookwright>              | Python CLI             | Spec-Driven(先写规范再写文) + 知识图谱确定性验证                      | ★★★★  |
| 8 | **NeuroBook**             | <https://github.com/notnotype/neuro-book>              | Python 桌面应用            | 主体+时间戳审计记录，Agent 读写分权，自定义历法                           | ★★★   |
| 9 | **OpenNovel**             | <https://github.com/Yaemikoreal/OpenNovel>             | Python CLI             | 四Agent + Machine Shadow + SQLite事件账本                  | ★★★   |

***

## 四、候选清单 · SkillHub 可直接安装

> 老板已装 skillhub CLI，以下可用 `skillhub install <name> --namespace <user>` 直接落地试用

| # | 技能名                        | 作者/可用名                                    | 类型    | 长线连贯核心                                       | 可借鉴度  |
| - | -------------------------- | ----------------------------------------- | ----- | -------------------------------------------- | ----- |
| 1 | **Novel Assistant**        | `@clawhub_cnskycn/novel-assistant`        | 带规则库  | 每章必读记忆文件 + 4维连贯检查(因果/人物/时间线/伏笔P1P2P3) + 冲突预警 | ★★★★★ |
| 2 | **长篇小说技能组合**               | `@user_bd09b0e3/long-novel-creator`       | 带规则库  | 八段式分形 + 伏笔追踪表 + 信息差分布图 + 人物小传/关系图            | ★★★★  |
| 3 | **长篇大纲设计专家包**              | skillhub 专家包                              | 6技能组合 | 伏笔清单+回收点+冲突检测 + 分卷结构+卷间衔接+时间线表+章节卡           | ★★★★  |
| 4 | **长篇小说创作助手**               | `@user_6d3be094/full-length-novel-writer` | 带规则库  | 大纲.md(关键事件时间线+伏笔清单)，续写强制读核心文档                | ★★★   |
| 5 | **Chinese Novelist Skill** | skillhub 站内                               | 带规则库  | 人物档案 + 连贯性检查 + check\_chapter\_wordcount.py  | ★★★   |
| 6 | 完整框架自动迭代网文(wangwen)        | `@user_3b54b400/wangwen`                  | 带规则库  | 风格学习库(文风一致) / 平台规范，长线台账较弱                    | ★★    |

***

## 五、与 pop-snow 管线映射（外部机制 → 我们环节）

| 外部机制                                 | 我们对应环节                                | 建议强化点                                                |
| ------------------------------------ | ------------------------------------- | ---------------------------------------------------- |
| 伏笔生命周期台账 / 承诺回收账                     | `pop-snow-plot` 线账本、`outline` 线账本/锚点区 | 把"线"从一句话账本升级为 planted→building→paid 状态机，卷末强制对账"埋1揭1" |
| 每章必读状态文件(待解决伏笔/支线板)                  | `pop-snow-write` 读近5白描卡+状态快照          | 状态快照里补"待解决伏笔池 + 支线进度板"，写章前强制过一遍                      |
| 跨章一致性四表 + 确定性连续性引擎                   | `pop-snow-review`                     | 加脚本化校验:道具链/时间锚/术语/关键数字 + 死角色行走/未触发契诃夫枪扫描             |
| 卷节奏板 promise/midpoint/climax/payoffs | `pop-snow-outline/plot` 卷纲锚点区         | 卷纲锚点区显式列"本卷承诺 vs 已回收/欠账"                             |
| subject+时间戳审计                        | `pop-snow-stage` 人物养成/金手指             | 养成节点带时间戳记录 get/change，可审查"何时获得"                      |
| BM25/向量回捞片段                          | `pop-snow-write` 信息注入                 | 长线写章时按相关性检索过去设定/白描片段                                 |

***

## 六、推荐行动

**下一步分两档，老板拍板：**

- **A 立即试用（低风险）**：`skillhub install` 装 **Novel Assistant** 与 **long-novel-creator**，拿一个真实章节实操，看它的伏笔台账/连贯校验长什么样再决定借鉴哪块。

- **B 机制借鉴（进咱管线）**：从 GitHub Top5 中挑 **Novel Writer Workflow 的四表一致性脚本** 与 **Story Skills 的连续性引擎**，翻代码落地成 pop-snow-review 的脚本化校验；把 **伏笔生命周期状态机** 补进 plot/outline 的线账本项目。

> 说明：所有来源均为真实检索结果；仓库"可运行性"以实际 clone 验证为准，本盘点只做机制研判未逐一下载核对。

