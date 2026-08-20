---
name: short-plot-structurer
description: "当用户完成开篇设计后进入剧情结构设计时启用。推荐模板→弧线设计→角色设计→骨架卡片。先定剧情再配角色（角色服务于剧情）。"
---
# short-plot-structurer
> 短篇剧情结构器。选模板→画弧线→配角色→输出骨架卡片。v1.1.0
## 做什么
输入：导语 + 黄金三句 + 付费钩子策略（来自 opening-designer 流转上下文）
输出：骨架卡片（结构模板+剧情弧线+角色清单）+ 流向 body-generator 的流转上下文
## 核心原则
短篇的核心是**情节节奏和情绪释放**，不是人物深度。先定剧情、再根据剧情需要设计角色。
> 逻辑链："这个反转需要什么样的人设来撑？谁来承受这个情绪爆发效果最有力？" ——角色是剧情的函数。
## 怎么操作（SOP骨架）
> execution.mode: 串行 | 强保障：本 SKILL.md 由 host 层每次 run 强制注入 | 弱保障：steps/ 需 agent 主动 Read

| 步骤 | 做什么 | 产出 | step 文件 |
|:-----|:-----|:-----|:----------|
| Step 1 | 根据平台×题材×卖点推荐结构模板 | 模板选定 | `steps/step1-select-template.md` |
| Step 2 | 设计全篇剧情弧线（按免费/付费分段，含情绪走向） | 剧情弧线表 | `steps/step2-arc-design.md` |
| Step 3 | 根据剧情需要设计角色（≤5人，主角四维+配角功能） | 角色清单 | `steps/step3-character-design.md` |
| Step 4 | 输出骨架卡片+流转上下文 | 骨架卡片 | `steps/step4-output-card.md` |

## 4种结构模板
| 模板 | 字数 | 最适合 |
|:--|:--|:--|
| 知乎反转体 | 1-3万字 | 知乎悬疑/反转，第一人称+层层剥洋葱 |
| 番茄单元剧体 | 6000-15000字 | 番茄爽文，每单元一个完整爽点 |
| 经典三幕式 | 全平台 | 最通用，建立日常→冲突升级→最终对决 |
| 情绪爆发体 | 5000-8000字 | 每天读点故事，情绪线为主事件为副 |

## 红线
| # | 红线 | 违反后果 |
|:-:|:-----|:---------|
| 1 | 角色不超过5个有名有姓的（短篇铁律） | 角色过多、读者记不住 |
| 2 | 不在人设上铺陈过多——每维度一句话 | 正文空间被挤占 |
| 3 | 功能重复的配角必须合并 | 浪费有限篇幅 |
| 4 | 剧情弧线钩子位置必须与付费钩子策略对齐 | 钩子错位，付费策略失效 |
| 5 | 骨架确定前不进入 body-generator | 正文生成失去结构约束 |

## 速查表
| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step1-select-template.md` | Step 1 | 平台×题材匹配表+推荐逻辑 |
| `steps/step2-arc-design.md` | Step 2 | 弧线分段字段+情绪走向设计 |
| `steps/step3-character-design.md` | Step 3 | 主角四维+配角功能分类 |
| `steps/step4-output-card.md` | Step 4 | 骨架卡片格式+流转上下文 |
| `references/structure-guide.md` | Step 1-2 | 4套结构模板详解 |
| `references/character-card.md` | Step 3 | 人设构建方法论 |
| `references/golden-three.md` | Step 2 对齐时 | 付费钩子设计原则 |
| `templates/skeleton-card.tpl.md` | Step 4 输出时 | 骨架卡片模板 |

## 版本
v1.1.0 | 2026-08-13 | skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
