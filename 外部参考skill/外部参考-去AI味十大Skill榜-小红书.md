# 去AI味十大 Skill 榜（小红书 VOL.02）

> 采源：小红书笔记截图「GITHUB · 可下载 SKILL 清单」
> 副标题：TOP 10 · 让 AI 写的稿不再一眼假
> 抓取日期：2026-09-06
> 交叉验证：CSDN「盘点AI工作流中去AI味的10大skill（GitHub Stars实测排行）」（赛马AI运营实验室，2026-07-21），10 个 skill 与描述逐一对应
> 仓库定位：全部经 GitHub API 按 star 数+描述匹配验证

---

## 榜单全录（已全部下载）

| # | Skill | 笔记描述 | 标签 | 仓库 | 落地位置 |
|---|---|---|---|---|---|
| 01 | humanizer | 去AI写作痕迹的元老级 skill | 去味 | blader/humanizer | 外部参考-去AI味01-humanizer |
| 02 | Humanizer-zh | 中文版，专治中文AI腔 | 中文 | op7418/Humanizer-zh | 外部参考-去AI味02-Humanizer-zh |
| 03 | stop-slop | 去掉文字里的AI套路腔 | 去腔 | hardikpandya/stop-slop | 外部参考-去AI味03-stop-slop |
| 04 | taste-skill | 给AI审美，不写无聊套话 | 审美 | Leonxlnx/taste-skill | 外部参考-去AI味04-taste-skill |
| 05 | ai-flavor-remover | AI味去除 | 去味 | hylarucoder/ai-flavor-remover | 外部参考-去AI味05-ai-flavor-remover |
| 06 | shuorenhua | 说人话，中文去味改写 | 说人话 | MrGeDiao/shuorenhua | 外部参考-去AI味06-shuorenhua |
| 07 | nuwa-skill | 蒸馏任何人的表达风格 | 文风 | alchaincyf/nuwa-skill | 外部参考-去AI味07-nuwa-skill |
| 08 | writing-agent | 去AI味全栈写作系统 | 系统 | dongbeixiaohuo/writing-agent | 外部参考-去AI味08-writing-agent |
| 09 | chatgpt-comparison-detection | 看出文本是不是AI写的 | 检测 | Hello-SimpleAI/chatgpt-comparison-detection | 外部参考-去AI味09-chatgpt-comparison-detection |
| 10 | De-AI-Prompt-Enhancer | 去AI味提示词增强 | 提示词 | OUBIGFA/De-AI-Prompt-Enhancer-Writer-Booster-SKILL | 外部参考-去AI味10-De-AI-Prompt-Enhancer |

## 各仓库要点（定位时实测）

| 仓库 | Stars | 说明 |
|---|---|---|
| blader/humanizer | 43.9k | 元老级。基于 Wikipedia「Signs of AI writing」35 模式，先改结构再校验事实，纯 Markdown 可移植 |
| op7418/Humanizer-zh | — | blader/humanizer 中文汉化版（Guizang 出品），24 类中文 AI 写作模式 |
| hardikpandya/stop-slop | — | 8 条核心规则+违禁短语目录（references/phrases），定点清除套路表达 |
| Leonxlnx/taste-skill | 65k+ | Anti-Slop 前端/表达品味框架，9 套反模板技能，3 旋钮调风格强度 |
| hylarucoder/ai-flavor-remover | — | prompt 型（非 skill 结构），实测 5000 字重写可将 AI 味 70%→17% |
| MrGeDiao/shuorenhua | ~1.3k | 中英双语去 slop，Tier1/2/3 分层词表防误伤，核心主张「改语气之前先锁事实」 |
| alchaincyf/nuwa-skill | 32.1k | 思维蒸馏：从表达DNA/心智模型/决策启发式/反模式/诚实边界五层提炼人物 skill |
| dongbeixiaohuo/writing-agent | ~0.4k | Claude Code（Skills+Subagents）去AI味全栈写作系统，支持 DeepSeek/GLM/MiniMax |
| Hello-SimpleAI/chatgpt-comparison-detection | — | HC3 语料库+AI 检测器（学术派，检测而非改写） |
| OUBIGFA/De-AI-Prompt-Enhancer-Writer-Booster-SKILL | 753 | 去AI味提示词+写作增强，含朱雀检测对抗实践（issue 区有朱雀实测讨论） |

## 与既有资产的关系

- **deai_gate.py 对口**：01/02/03/05/06 是同一赛道的直接对标（中文去AI味规则+分层改写+误伤控制），shuorenhua 的 Tier 分级防误伤与咱们的「滥用类仅检测不判级」思路同源
- **09 检测派**：HC3 提供学术级检测基准，可作 deai_gate 阈值校准的参考语料源
- **07 文风蒸馏**：与文风DNA管线（pop-dna-style）同赛道，五层蒸馏法值得对照
- **10 提示词派**：从输入端防AI味，与 sepia（外部参考-sepia-去AI味写作skill.md）的「校准到人类分布而非反转AI分布」原则互补

## 备注

- 原榜单 star 数为笔记发布时数据，上表为 2026-09-06 实测，有出入属正常增长
- nuwa-skill 仓库较大（>10MB），git clone 直连易超时，采用 zip 归档方式下载，故无 .git 目录
