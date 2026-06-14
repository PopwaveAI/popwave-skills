# Phase 2.2：世界构筑模板提取 — decon-world

> **对齐写作端**：pop-novel-world Phase 1~6 → `L1-元设定层/01-06.md` + `00-总控/数值体系/*.yaml` + `状态/角色/*.md` + `设计/起点快照.md`
> **消费关系**：本相位产出 → pop-novel-world 加载 → 按新书宪法调参 → 生成世界设定
> **前置条件**：Phase 2.1 (decon-creative) 已完成

## 速查表

| 步骤 | 操作 | 读什么 | 产出(文件) | 门禁 |
|:-----|:-----|:-------|:----------|:-----|
| 1 | 力量体系 | 全书前100章 | `L1-元设定层/02-力量体系-template.yaml` | ❌ level_count=0退回 |
| 2 | 世界观展开 | 全书 | `L1-元设定层/01-世界蓝图-template.yaml` + `03-历史驱动力-template.yaml` | ❌ <3区间退回 |
| 3 | 数值体系 | 战斗章+升级章 | `00-总控/数值体系/combat_capability-template.yaml` + 3个配套 | ❌ combat_power_range空退回 |
| 4 | 角色卡参考 | 全书 | `状态/角色/{主角}-角色卡-template.md` + `{配角}-角色卡-template.md` | ❌ 空信息退回 |
| 5 | 起点快照 | L1转化 | `设计/起点快照-template.yaml` | ❌ 缺段退回 |
| 6 | 世界宪法 | 汇总 | `00-原始设定/世界宪法-template.yaml` | ❌ <3条退回 |

## 产出到 _template_library/ 的文件

```
_template_library/{书名}/
├── L1-元设定层/
│   ├── 01-世界蓝图-template.yaml       ← 世界观展开节奏+核心法则+力量来源+世界基调
│   ├── 02-力量体系-template.yaml       ← 职业等级+属性+升级节奏+瓶颈
│   ├── 03-历史与驱动力-template.yaml    ← 纪元划分+前提大事件+核心矛盾(→M1线)
│   ├── 04-物种与天赋-template.yaml     ← 主要种族+异兽怪物+特殊血脉
│   ├── 05-势力格局-template.yaml       ← 前期/中期/后期势力+权力分布+势力关系
│   └── 06-资源与物品-template.yaml     ← 修炼资源+关键道具+货币体系
├── 00-总控/
│   └── 数值体系/
│       ├── combat_capability-template.yaml
│       ├── monster_rank_map-template.yaml
│       ├── act_rank_schedule-template.yaml
│       └── collision_curve-template.yaml
├── 状态/
│   └── 角色/
│       ├── {主角}-角色卡-template.md
│       └── {配角}-角色卡-template.md
├── 00-原始设定/
│   └── 世界宪法-template.yaml
└── 设计/
    └── 起点快照-template.yaml
```

## 模板文件示例

写入 `L1-元设定层/02-力量体系-template.yaml`：

```yaml
# Template: 力量体系
# @consumed_by: pop-novel-world (Phase 1)
# @source_book: 深渊主宰
# @对应项目文件: 00-原始设定/L1-元设定层/02-力量体系.md
#
# 使用说明：加载后按新书力量类型调参。层数可增减，gap_mode可调。

level_count: 12
level_gap_model: "线性(1-5) → 指数(5+)"
chapters_per_level_early: 3
chapters_per_level_late: 8
bottleneck_chapter: 17
bottleneck_mechanism: "职业进阶需特定条件触发"
upgrade_rhythm:
  chapters_between_upgrades: [3, 5, 8, 5, 12, 4, 6, 7, 15, 5, 10]
  upgrade_density_early: "3-5章/级"
  upgrade_density_late: "8-15章/级"
```

写入 `00-总控/数值体系/combat_capability-template.yaml`：

```yaml
# Template: 战力数值体系
# @consumed_by: pop-novel-world (Phase 4)
# @对应项目文件: 00-总控/数值体系/combat_capability.yaml

combat_power_range: [1, 100]
chapter_power_gain: 3
monster_power_curve: "同步增长(±2级)"

ranks:
  - level: 1
    name: "平民/1级游荡者"
    min_attack: 1
    max_attack: 5
    breakthrough: "完成第一个战斗任务"
```

写入 `00-总控/数值体系/act_rank_schedule-template.yaml`：

```yaml
# Template: 等级排期
# @对应项目文件: 00-总控/数值体系/act_rank_schedule.yaml

schedule:
  - act: 1
    end_rank: "3级游荡者"
    milestone: "第一次杀人"

  - act: 2
    end_rank: "5级刺客"
    milestone: "藏宝洞生存"
```

写入 `00-总控/数值体系/collision_curve-template.yaml`：

```yaml
# Template: 碰撞曲线
# @对应项目文件: 00-总控/数值体系/collision_curve.yaml

battle_type_distribution:
  assassination: 25
  duel: 20
  skirmish: 30
  war: 15
  god_war: 10

emotional_arc:
  act_1: "压抑→爆发（卷末打脸高潮）"
  act_2: "探索→压迫→逆袭"
```

写入 `设计/起点快照-template.yaml`：

```yaml
# Template: 起点快照
# @consumed_by: pop-novel-world (Phase 5)
# @对应项目文件: 设计/起点快照.md

protagonist:
  level: "5平民/1游荡者"
  equipment: "无"
  money: 0
  cognition: "灵魂融合中，模糊的记忆"

world:
  location: "琥珀城·贫民区"
  situation: "动荡前夜，圣者浩劫即将到来"
  threats: ["大盗萨沙", "帮派争斗升级"]

mystery:
  - topic: "妹妹的血统(恐惧力量)"
    hinted_at: "ch3墓园事件"
```

## 落盘检查点

| 路径 | 状态 |
|:-----|:-----|
| `_template_library/{书名}/L1-元设定层/01-世界蓝图-template.yaml` | [ ] |
| `_template_library/{书名}/L1-元设定层/02-力量体系-template.yaml` | [ ] |
| `_template_library/{书名}/L1-元设定层/03-历史与驱动力-template.yaml` | [ ] |
| `_template_library/{书名}/L1-元设定层/04-物种与天赋-template.yaml` | [ ] |
| `_template_library/{书名}/L1-元设定层/05-势力格局-template.yaml` | [ ] |
| `_template_library/{书名}/L1-元设定层/06-资源与物品-template.yaml` | [ ] |
| `_template_library/{书名}/00-总控/数值体系/combat_capability-template.yaml` | [ ] |
| `_template_library/{书名}/00-总控/数值体系/monster_rank_map-template.yaml` | [ ] |
| `_template_library/{书名}/00-总控/数值体系/act_rank_schedule-template.yaml` | [ ] |
| `_template_library/{书名}/00-总控/数值体系/collision_curve-template.yaml` | [ ] |
| `_template_library/{书名}/状态/角色/{主角}-角色卡-template.md` | [ ] |
| `_template_library/{书名}/状态/角色/{配角}-角色卡-template.md` | [ ] |
| `_template_library/{书名}/状态/角色/龙套池-template.md` | [ ] |
| `_template_library/{书名}/设计/起点快照-template.yaml` | [ ] |
| `_template_library/{书名}/00-原始设定/世界宪法-template.yaml` | [ ] |

## 下一步

完成 → 进入 Phase 2.3 (decon-plot)
