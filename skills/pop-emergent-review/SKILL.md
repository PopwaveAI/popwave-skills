---
name: pop-emergent-review
description: Pop 涌现式 review/ledger 执行 skill。用于审稿、检查爽不爽、AI味、种子兑现、燃料入戏、正文锚定漂移、bug/OOC，并把设定、人物、剧情线、燃料和伏笔压缩成下一次 write 必读的 current-state.md；不直接重写正文。
---

# Pop Emergent Review

review 的第一职责不是写长评，而是把“长出来的东西”变成下一次 write 必须消费的 `涌现/current-state.md`。

## 必读输入

- 待审正文原文。
- 上一版 `涌现/current-state.md`，如存在。
- `涌现/soul.md`，检查主卖点和表达是否执行。
- 按需读取：`seed-种子文档.md`、`research-写作燃料.md`、`设定库.md`、`人物库.md`、`剧情线.md`、`content-mechanics.md`。

只在需要更新对应信息时读取库文件。不要为了 review 把全项目全部塞进上下文。

## 执行模式

| 模式 | 条件 |
| --- | --- |
| `formal` | 已读待审正文、current-state/soul，并输出审稿判断和新版 current-state |
| `draft` | 缺 current-state 或 soul，但能从正文和用户要求生成临时 current-state |
| `trial` | 只做快速体感，不更新项目状态 |

## 审稿 SOP

1. 裸读体感：哪里想继续看，哪里跳读，哪里像 AI。
2. 硬推进检查：上一版 current-state 的硬推进是否兑现。
3. 爽文审计：压力/诱因 -> 主角主动 -> 阻碍 -> 可见反馈 -> 收益/损失 -> 追读。
4. Soul 执行检查：主卖点、主角主动方式、爽点外显、句子气口是否落到正文。
5. 连续性检查：人物、设定、资源、时间线、伏笔是否冲突。
6. 沉淀分流：更新库文件建议，并重写 current-state。

## 归因规则

| 问题 | 归因 | 处理 |
| --- | --- | --- |
| 中长线失控 | current-state 硬推进/伏笔债务缺口 | 重写 current-state |
| 设定或人物状态错 | 设定库/人物库未更新或 current-state 漏写 | 更新库建议并压入 current-state |
| 燃料没有入场 | research/fuel 到 current-state 的筛选失败 | 更新可用燃料队列 |
| 主卖点弱 | soul 不清或 write 未执行 | 更新 soul 建议或下一章硬规则 |
| 文风弱 | soul 气口/文风锚定问题 | 提出 soul 修改建议 |

不得把所有问题都归因到文风或模型能力。

## Current-State 输出

每次 formal review 必须写入或建议写入 `涌现/current-state.md`。结构固定：

```markdown
---
doc_type: current-state
role: 下一章写作唯一入口包；承载 write 必须消费的事实、人物、设定、燃料、伏笔、硬推进和禁区
read_policy: full-required
compression: forbid
primary_consumer: write
source_of_truth: true
last_updated: YYYY-MM-DD
---

# Current State

## 当前章位
- 已完成：
- 下一章：

## 不可改事实
-

## 人物状态
### 人物名
- 所知：
- 不知道：
- 当前目标：
- 当前状态：

## 设定状态
-

## 可用燃料队列
### 近期可用
-
### 中期保留
-

## 伏笔债务
- 未触发：
- 铺垫中：
- 兑现中：

## 下一章硬推进
-

## 禁止漂移
-
```

current-state 控制在 1000-2500 字。写不下的内容留在库文件，不进入 write 入口。

## 库文件更新建议

review 可以更新或建议更新：

| 信息 | 文件 |
| --- | --- |
| 已确认设定 | `涌现/设定库.md` |
| 人物最新状态 | `涌现/人物库.md` |
| 伏笔和长线 | `涌现/剧情线.md` |
| 可入场燃料池 | `涌现/research-写作燃料.md` 或 `涌现/燃料库.md` |
| 题材机制 | `涌现/content-mechanics.md` |
| 主卖点/表达魂 | `涌现/soul.md`，用户确认后改 |

库文件允许大，write 不直接读；review 负责筛选进 current-state。

## 回复格式

```markdown
本次采用 skill：pop-emergent-review

## 总判断
- 可用等级：
- 爽文兑现：
- AI味：
- 最大问题：

## 最影响阅读的 3 个问题
| 等级 | 位置 | 问题 | 归因 | 处理 |
| --- | --- | --- | --- | --- |

## Current-State 更新
- 已更新/建议更新：
- 下一章硬推进：
- 禁止漂移：

## 待确认修改
- 设定库：
- 人物库：
- 剧情线：
- soul：
- content-mechanics：
```

## 红线

- 不直接重写正文。
- 不把 review 写成只有体感、没有 current-state 的长评。
- 不让沉淀停留在 review 文件里；必须压成下一次 write 的入口。
- 不把临时比喻、一次性氛围词沉淀为设定。
