---
name: pop-emergent-seed
description: Pop 涌现式 seed 执行 skill。用于碰撞 idea、做全书种子、本轮种子、故事方向、核心快感、主卖点、相似/相反/盲区、题材承诺和禁区；产出轻量 seed，并可初始化 soul/current-state 的上游内容；不写世界设定大全、卷纲、章纲或正文。
---

# Pop Emergent Seed

seed 只回答：这个故事靠什么成立、靠什么长期爽、哪些判断不能丢。它不替作者锁死剧情。

## 分层原则

把输入拆成三层：

| 层 | 问题 | 下游 |
| --- | --- | --- |
| 主卖点/soul | 这本书最核心的读者承诺是什么？主角怎么主动？爽点怎么外显？正文气口是什么？ | `soul.md` |
| 题材机制 | 世界、系统、武学、诡异、DND面板、组织运营等靠什么规则运转？ | research / content-mechanics / 设定库 |
| 剧情承诺 | 长线期待、伏笔债务、主角阶段性推进是什么？ | current-state / 剧情线 |

## 执行模式

| 模式 | 条件 |
| --- | --- |
| `formal` | 核心承诺、主卖点、禁区、待 research 问题齐全 |
| `draft` | 有方向但主角驱动、世界压迫、主卖点或禁区缺口仍在 |
| `trial` | 快速脑暴，不落盘，不称 seed 完成 |

## 输出

优先写入 `涌现/seed-种子文档.md`，文件开头必须带元数据：

```markdown
---
doc_type: seed
role: 故事长期承诺和判断宪法；供 seed/research/review 使用，不作为 write 直接输入
read_policy: full-if-targeted
compression: allow-into-current-state
primary_consumer: review
source_of_truth: true
last_updated: YYYY-MM-DD
---

# 涌现种子文档

execution.mode: formal|draft|trial

## 一句话主卖点

## 核心承诺
- 元爽点：
- 读者追读理由：
- 主角主动方式：
- 爽点外显方式：
- 世界如何逼主角行动：
- 题材承诺：

## 候选PK
| 候选 | 一句话卖点 | 核心快感 | 主角驱动 | 世界压迫 | 风险 |
| --- | --- | --- | --- | --- | --- |

## 推荐方案
- 推荐：
- 理由：
- 吸收的败者强点：
- 淘汰项：

## Soul 草案
- 主卖点：
- 叙事人格：
- 句子气口：
- 信息释放：
- 禁区：

## 题材机制待 research

## 伏笔/长线债务

## 不可牺牲项

## 禁区
```

## 质量门

- 主卖点必须一句话说清。
- 必须说明主角如何主动，不只写世界很压迫。
- 必须输出待 research 的题材机制。
- 混合参考必须分清“主卖点/soul、题材机制、剧情承诺”。
- 不写正文、不写章纲、不冻结世界设定。
