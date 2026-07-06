---
name: pop-emergent-research
description: Pop 涌现式 research 执行 skill。用于为涌现式小说找写作燃料、题材机制、外部事件、行业机制、原型事件、物件、术语、制度压力和可神话化素材；产出可被 review/ledger 筛入 current-state 的燃料池，不写正文，不排章纲。
---

# Pop Emergent Research

research 只找能进场面的燃料。它不是百科，不是长调研报告，也不直接喂给 write；write 只消费 review 压进 `current-state.md` 的燃料。

## 执行模式

| 模式 | 条件 |
| --- | --- |
| `formal` | 已读 seed/临时 seed，燃料不少于 3 条，主燃料有事件形状、主角操作点、可外显爽点 |
| `draft` | 有燃料但来源、入戏方式或主角操作点不足 |
| `trial` | 快速补燃料，只能供试写或人工判断 |

## 题材机制边界

参考书里的武学招式、系统面板、诡异规则、职业数值、战斗升级路径、组织运营模型，先当“内容机制”处理：

- 能进入本书的，转成可触发事件、主角操作点、可外显爽点。
- 不能直接迁移的，写入禁用燃料或 content-mechanics。
- 不得把内容机制伪装成文风特征交给 soul/write。

## 输出

优先写入 `涌现/research-写作燃料.md`，文件开头必须带元数据：

```markdown
---
doc_type: research
role: 可入场燃料池和题材机制来源；供 review/ledger 筛选进 current-state，不作为 write 直接输入
read_policy: full-if-targeted
compression: allow-into-current-state
primary_consumer: review
source_of_truth: true
last_updated: YYYY-MM-DD
---

# 涌现写作燃料

execution.mode: formal|draft|trial

## 资料覆盖声明
- 已读：
- 用户描述：
- 模型推断：
- 禁止外推：

## 本书涌现燃料
| 燃料 | 来源 | 可触发事件 | 主角操作点 | 可外显爽点 | 风险 |
| --- | --- | --- | --- | --- | --- |

## 外部燃料
| 燃料 | 已读范围/来源 | 短复述 | 本项目转译 | 不照搬 |
| --- | --- | --- | --- | --- |

## 可筛入 current-state 的近期燃料
-

## 中期保留燃料
-

## 禁用燃料
-

## Content Mechanics 分流建议
| 机制 | 来源 | 能否迁移 | 正确路由 | 禁止误用 |
| --- | --- | --- | --- | --- |
```

## 质量门

- 至少 3 条可写燃料。
- 每条主燃料有事件形状、主角操作点和可外显爽点。
- 明确哪些燃料近期可用，哪些中期保留，哪些禁用。
- 内容机制已分流，不进入 soul。
- research 不排剧情，不写正文。
