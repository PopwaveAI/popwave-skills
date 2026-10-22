# 番茄完本流水线总表

## 两条 goal

| 阶段 | goal | 目标 | 结束 | 验收 |
| --- | --- | --- | --- | --- |
| 试读 | 试读 goal | 3 万字，约 12-15 章 | `completed` | 字数 ≥30000；章数=章日志数；phase ≥7；每章 ≥1800 字；`stop=false` |
| 完本 | 完本 goal | 15/30 万字 | `completed` | 全书字数 ≥目标；章数=章日志数；phase 7/8；无空章；`stop` 每 10 章 |

试读完成 → 用户确认 → 开完本 goal。完本从现有进度继续，不重写试读章。

## 阶段路由

| 阶段 | 结构技能 | 本技能 reference | 产出 | 硬门禁 |
| --- | --- | --- | --- | --- |
| 赛道诊断 | 无 | `genre-fit.md` | 2-3 个赛道建议 | 30 万字可行性五问 |
| 规划 | `pop-snow-seed` | `golden-three.md` | 立项稿、黄金开篇三版 | 前 300 字爆点、前 1/3 爽点 |
| 舞台 | `pop-snow-stage` | `emotion-and-payoff.md` | 人物、世界、金手指/替代驱动 | 主形态已定 |
| 卷纲 | `pop-snow-plot` | `emotion-and-payoff.md` | 卷纲、爽点分布表 | 不得连续 3 章无爽点 |
| 章纲 | `pop-outline` | `hook-and-reversal.md` | 逐章章纲 | 钩子五型、相邻不同型 |
| 正文 | `pop-write` | `quality-gate.md` | 正文 | 字数、章末钩子、承接四问 |
| 审稿 | `pop-review` | `quality-gate.md` | 章日志、批次报告 | 四块报告齐全 |
| 完本 | `pop-review` | `quality-gate.md` | 完本包 | 字数、章数、日志、phase |

## 状态.md

```text
mode: fanqie_complete
stage: trial | full
phase: 1-8
current_volume: N
current_chapter: N
word_count: N
goal_word_count: 150000 | 300000
last_confirmed_chapter: N
hook_type: A | B | C | D | E
payoff_form: 碾压 | 信息兑付 | 认可 | 关系兑付 | 整活兑付
paid_off_chapters: N
```

## goal.create 工具

如果宿主提供 `goal.create`：

- 只在用户明确同意开始下一阶段时调用。
- 只创建 `planning` 目标；不确认、不执行、不继续。
- 确认/继续/终止永远由用户操作。
- 一个对话只能有一个活动目标；创建失败就如实告诉用户，不重试刷目标。

## 恢复

- 每章落盘；`状态.md` 记录当前章与已确认章。
- 中断后从最后一章继续；不重复写已确认章。
- 连续 3 轮无推进，goal 会置 `blocked`；不要自己重启，等用户处理。
- 用户终止后不再自动续跑。

## 冲突裁决

- 番茄写法与雪花流结构冲突时：结构产物按 `pop-snow-*`，写法按本技能。
- 用户明确要求与技能规则冲突时：先说明代价，用户坚持就按用户，记录在 `状态.md` 的降级记录。
- 不静默降级；不记录就开写视为流程违规。
