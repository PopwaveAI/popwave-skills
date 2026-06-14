# Phase 2.3：剧情架构模板提取 — decon-plot

> **对齐写作端**：pop-novel-plot Step 0~2 → `设计/全书架构.md` + `设计/卷/volume-XX.md` + `设计/幕/act-XX.yaml`
> **消费关系**：本相位产出 → pop-novel-plot 加载 → 按新书长度调参 → 规划卷/幕
> **前置条件**：Phase 2.1 + Phase 2.2 已完成

## 速查表

| 步骤 | 操作 | 读什么 | 产出(文件) | 门禁 |
|:-----|:-----|:-------|:----------|:-----|
| 1 | 分卷/分幕 | 全书逐章 | `设计/卷/volume-template.yaml` | ❌ Act<3退回 |
| 2 | 情绪弧线+钩子 | 每章结尾 | `设计/幕/act-template.yaml`（情绪+钩子曲线） | ❌ 数组<80%退回 |
| 3 | 全书架构 | 汇总 | `设计/全书架构-template.yaml` | ❌ 缺卷拆分退回 |
| 4 | 契诃夫枪 | 每条情节线 | `设计/幕/chekhov-template.yaml` | ❌ 悬空不标注退回 |
| 5 | 终点快照 | 全书 | `设计/终点快照-template.yaml` | ❌ 缺数据退回 |

## 产出到 _template_library/ 的文件

```
_template_library/{书名}/
└── 设计/
    ├── 全书架构-template.yaml
    ├── 卷/volume-template.yaml
    ├── 幕/
    │   ├── act-template.yaml          ← 幕纲骨架（情绪/钩子/Canvas参考）
    │   └── chekhov-template.yaml      ← 契诃夫枪追踪模板
    └── 终点快照-template.yaml
```

## 模板文件示例

写入 `设计/全书架构-template.yaml`：

```yaml
# Template: 全书架构
# @consumed_by: pop-novel-plot (Phase 0)
# @对应项目文件: 设计/全书架构.md

total_volumes: 3
avg_chapters_per_volume: 60

plotlines:
  main1: "世界危机线——圣者浩劫背景下主角的博弈"
  main2: "主角成长线——从贫民窟小偷到深渊主宰"
  main3: "主角行动线——为了薇薇安的每一个主动决策"
```

写入 `设计/卷/volume-template.yaml`：

```yaml
# Template: 卷级设计
# @consumed_by: pop-novel-plot (Step 1)
# @对应项目文件: 设计/卷/volume-XX.md
# 每卷一个block，卷间复制改值

volumes:
  - volume: 1
    chapters: [1, 17]
    m1_density: 3
    m2_density: 14
    core_theme: "生存·觉醒"
    purpose:
      for_book: "建立困境和主角基调"
      for_reader: "贫民窟生存压迫+第一次升级爽感"
    conflict:
      stakes: "妹妹被绑/自己被杀"
      escalation: "饥饿→帮派→杀人→名声扩散→更致命对手上门"
```

写入 `设计/幕/act-template.yaml`：

```yaml
# Template: 幕纲骨架
# @consumed_by: pop-novel-plot (Step 2)
# @对应项目文件: 设计/幕/vol-XX/act-YY.yaml

per_chapter_emotional_goal: ["绝望", "坚持", "恐惧", "渴望", "温暖", "紧张", "压抑", "爆发", "释放", "困惑", "兴奋", "压抑", "恐惧", "紧张", "希望", "满足", "震撼"]

hook_density_curve: [L1, L1, L2, L2, L1, L2, L3, L4, L2, L3, L3, L2, L4, L3, L2, L3, L5]
hook_types_used: ["imminent_crisis", "dilemma", "sudden_reveal", "mysterious_clue"]

climax_distribution:
  s_climaxes: [17]
  a_climaxes: [8, 14]
  b_climaxes_density: 3.1
```

写入 `设计/终点快照-template.yaml`：

```yaml
# Template: 终点快照
# @对应项目文件: 设计/终点快照.md

protagonist_final:
  identity: "半精灵之神/深渊主宰"
  domains: ["杀戮", "阴影", "深渊"]

world_final:
  event: "圣者浩劫已爆发"
  territory: "摩多城已建立"
```

## 落盘检查点

| 路径 | 状态 |
|:-----|:-----|
| `_template_library/{书名}/设计/全书架构-template.yaml` | [ ] |
| `_template_library/{书名}/设计/卷/volume-template.yaml` | [ ] |
| `_template_library/{书名}/设计/幕/act-template.yaml` | [ ] |
| `_template_library/{书名}/设计/终点快照-template.yaml` | [ ] |

## 下一步

完成 → 进入 Phase 2.4 (decon-prose)
