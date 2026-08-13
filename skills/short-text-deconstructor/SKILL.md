---
name: short-text-deconstructor
description: "当用户上传例文需要拆解学习时启用。拆解例文→结构/角色/开篇/文风/评价。支持选择拆解深度（完整/仅开篇/仅文风/仅题材）。拆解结论直接影响后续Steps的决策。独立于主线流程，随时可调用。"
---
# short-text-deconstructor
> 短篇拆文分析器。选深度→拆结构→拆角色→拆开篇→拆文风→评价→影响后续。v1.1.0
## 做什么
输入：用户上传的例文全文（文本/PDF/截图文本）
输出：拆解报告（结构分析+角色分析+开篇拆解+文风画像+9维评价+对后续Steps的影响）+ 流向各Step的影响信号
## 定位
独立于主线 Step 1-6。用户可以在任何阶段触发此 Skill。拆解完成后恢复并应用结论到各步骤。
## 怎么操作（SOP骨架）
> execution.mode: 串行 | 强保障：本 SKILL.md 由 host 层每次 run 强制注入 | 弱保障：steps/ 需 agent 主动 Read

| 步骤 | 做什么 | 产出 | step 文件 |
|:-----|:-----|:-----|:----------|
| Step 0 | 确认拆解深度（完整/仅开篇/仅文风/仅题材） | 深度确认 | `steps/step0-choose-depth.md` |
| Step 1 | 结构分析（平台判断+题材分类+模板匹配+弧线还原） | 结构+弧线 | `steps/step1-structure.md` |
| Step 2 | 角色分析（主角公式判断+人设还原+配角清单） | 角色清单 | `steps/step2-character.md` |
| Step 3 | 开篇拆解（导语公式+黄金三句+付费钩子还原） | 开篇分析 | `steps/step3-opening.md` |
| Step 4 | 文风画像（句长/段落/对话占比/描写密度/特有词汇） | 文风画像 | `steps/step4-style.md` |
| Step 5 | 评价（9维评分+亮点/不足） | 评价表 | `steps/step5-evaluation.md` |
| Step 6 | 汇总报告+标注对后续Steps的影响 | 拆解报告 | `steps/step6-impact.md` |

## 四种拆解深度
| 选项 | 输出模块 | 适用场景 |
|:---|:---|:---|
| ① 完整拆解 | 结构+角色+开篇+文风+评价 | 想全面学习一篇精品 |
| ② 只学开篇 | 开篇拆解（导语公式+黄金三句+付费钩子） | 开篇不知道怎么写 |
| ③ 学文风和句式 | 文风画像 | 想模仿某作者的笔触 |
| ④ 参考题材和人设方向 | 结构分析+角色分析 | 找同类题材的切入点 |

## 对后续Steps的影响
| 步骤 | 影响 |
|:---|:---|
| Step 1 平台定位 | 拆解出的平台=直接确认或强烈推荐 |
| Step 2 脑洞提炼 | 拆解出的题材→在该品类找变体/升级方向 |
| Step 3 开篇设计 | 拆解出的导语公式→推荐同类或展示不同公式作为对比 |
| Step 4 剧情结构 | 拆解出的弧线和角色→作为基础框架微调 |
| Step 5 正文生成 | 拆解出的文风画像→作为一个独立的自定义文风选项 |
| Step 6 评审 | 拆解出的评价→作为例文vs作品各维度差距参照 |

## 红线
| # | 红线 | 违反后果 |
|:-:|:-----|:---------|
| 1 | 拆文不替代评审——例文评价是"样本分析"，评审是"诊断" | 把例文标准直接套用到用户作品 |
| 2 | 例文质量明显偏低时标注但不模仿 | 劣质例文的套路被复刻 |
| 3 | 拆解结论应如实反映例文特征，不做过度美化 | 用户对例文产生不切实际的预期 |
| 4 | 暂停主线流程时告知用户，拆完后恢复 | 主线流程状态丢失 |

## 速查表
| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step0-choose-depth.md` | Step 0 | 4种深度选项+跳过逻辑 |
| `steps/step1-structure.md` | Step 1 | 平台判断+题材分类+模板匹配+弧线还原 |
| `steps/step2-character.md` | Step 2 | 主角公式判断+人设还原+配角清单 |
| `steps/step3-opening.md` | Step 3 | 导语公式+黄金三句+付费钩子还原 |
| `steps/step4-style.md` | Step 4 | 句长/段落/对话占比/描写密度/特有词汇 |
| `steps/step5-evaluation.md` | Step 5 | 9维评分+亮点/不足 |
| `steps/step6-impact.md` | Step 6 | 汇总报告+影响标注 |
| `references/platform-rules.md` | Step 1/3/5 | 平台规则/调性/字数/付费 |
| `references/structure-guide.md` | Step 1 | 结构模板匹配 |
| `references/character-card.md` | Step 2 | 角色类型分类 |
| `references/writing-styles.md` | Step 4 | 文风特征提取对照 |
| `references/genre-guide.md` | Step 1 | 题材大类+子方向 |
| `templates/deconstruct-report.tpl.md` | Step 6 输出时 | 拆解报告模板 |

## 版本
v1.1.0 | 2026-08-13 | skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
