---
name: short-opening-designer
description: "当用户确定脑洞后进入开篇设计时启用。卖点主轴→6种导语公式择最优→黄金三句→完整导语→付费钩子策略。"
---
# short-opening-designer
> 短篇开篇设计器。定卖点→选公式→黄金三句→完整导语→付费钩子。v1.1.0
## 做什么
输入：脑洞一句话 + 平台 + 文章性质（来自 idea-refiner 流转上下文）
输出：开篇卡片（卖点主轴+黄金三句+完整导语+付费钩子）+ 流向 plot-structurer 的流转上下文
## 怎么操作（SOP骨架）
> execution.mode: 串行 | 强保障：本 SKILL.md 由 host 层每次 run 强制注入 | 弱保障：steps/ 需 agent 主动 Read

| 步骤 | 做什么 | 产出 | step 文件 |
|:-----|:-----|:-----|:----------|
| Step 1 | 确定卖点主轴（2-3个候选，标注优先级） | 卖点主轴确定 | `steps/step1-sell-point.md` |
| Step 2 | 根据平台×卖点选择最适配的导语公式 | 公式选定+理由 | `steps/step2-choose-formula.md` |
| Step 3 | 用三要素法生成2-3组黄金三句 | 黄金三句候选 | `steps/step3-golden-three.md` |
| Step 4 | 用户选定后补完整导语（100-200字） | 完整导语 | `steps/step4-full-opener.md` |
| Step 5 | 设计付费钩子策略（位置+类型+断点） | 付费钩子策略 | `steps/step5-pay-hook.md` |

## 红线
| # | 红线 | 违反后果 |
|:-:|:-----|:---------|
| 1 | 导语不是正文第一句话——是平台展示页上的故事简介 | 读者困惑，导语无吸引力 |
| 2 | 不做"交代背景""抒情议论""解释说明" | 3个致命禁忌，读者直接划走 |
| 3 | 导语最后一句话必须是最强的悬念或钩子 | 没有钩子=没有付费转化 |
| 4 | 一稿多发多个平台时提醒导语需按平台重写 | 导语与平台调性不匹配 |
| 5 | 导语确定前不进入 plot-structurer | 骨架建立在不确定的开篇上 |

## 速查表
| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step1-sell-point.md` | Step 1 | 卖点候选表+优先级逻辑 |
| `steps/step2-choose-formula.md` | Step 2 | 6公式+平台匹配表 |
| `steps/step3-golden-three.md` | Step 3 | 三要素法+2-3组生成 |
| `steps/step4-full-opener.md` | Step 4 | 补句规则+100-200字约束 |
| `steps/step5-pay-hook.md` | Step 5 | 钩子位置/类型/断点设计 |
| `references/golden-three.md` | Step 2-3 | 导语公式+钩子技法手册 |
| `references/platform-rules.md` | Step 2/5 | 平台开篇铁律+付费比例 |
| `templates/opening-card.tpl.md` | Step 5 输出时 | 开篇卡片模板 |

## 版本
v1.1.0 | 2026-08-13 | skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
