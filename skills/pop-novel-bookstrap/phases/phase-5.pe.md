# Phase 5：数值体系模板升级

> 该文件同时作为执行指令和参考指南，无需加载外部 ref 文件。
> 完整四段框架参考 `references/网文力量体系大全.md`。

## 前置条件
project.yaml 已嵌入 reader_profile。

## 执行步骤

### combat_capability.yaml

```yaml
ranks:
  - name: "炼气"          # 段位名
    min_attack: 100       # 攻击范围下限
    max_attack: 500       # 攻击范围上限
    breakthrough: "灵力积累到一定程度 → 筑基"  # 突破条件
    combat_role: "群战辅"  # 单挑/群战/辅助
    weakness: "灵力不足，持久战劣势"
    iconic_scene: "一拳打碎青石"  # 标志性画面锚点
```

### monster_rank_map.yaml

```yaml
mapping:
  - monster: "铁背熊"
    rank: "炼气中期"      # 对应段位
    difficulty: "中等"     # 简单/中等/困难/Boss
    notes: "皮厚攻低，适合练手"
```

### act_rank_schedule.yaml

```yaml
schedule:
  - act: 1
    end_rank: "炼气巅峰"   # 每卷结束时的段位
    milestone: "筑基成功"
    note: "第一卷末达到筑基"
  - act: 2
    end_rank: "筑基中期"
    milestone: "获得本命法器"
    note: ""
```

### collision_curve.yaml（NEW v2.1）

```yaml
# 碰撞曲线——基于 deconstructor T6(数据流) + T5(叙事技法) 提取的节奏模板
# 如果无锚点书，则用平台基准节奏

overview:
  platform: "起点"          # 番茄节奏颗粒度更密（每3章小高潮/起点每5章）
  total_chapters_first_volume: 50

battle_type_distribution:
  assassination: 20%       # 暗杀/潜袭（前期低资源主导）
  duel: 20%                # 单挑（同级碰撞）
  skirmish: 30%            # 群战（带队）
  war: 15%                 # 战争（后期）
  god_war: 5%              # 神战（终局）
  by_act:                  # 每卷峰值类型
    act_1: "assassination" # 第一卷以暗杀/偷袭为主（低等级盗贼逻辑）
    act_2: "duel"          # 进入正面战斗
    act_3: "skirmish"

tension_curve:             # 前100章逐章张力值（1-10参考）
  chapter_tension: []      # ← 如无锚点书T6数据，使用平台默认密度（5→3→6→4→8循环）
  note: "如有 deconstructor T6 产出，用其提取的张力值覆盖此空白列表"

combat_density:
  per_volume:              # 每卷战斗章占比（不得低于30%）
    act_1: 50%             # 第一卷高密度留存（番茄≥50%）
    act_2: 35%
    act_3: 30%

emotional_arc:
  act_1: 压抑→爆发（卷末打脸高潮）
  act_2: 探索→压迫→逆袭
  act_3: 压抑→绝境→突破→新生
  anchor_per_volume: 1     # 每卷至少1个情感锚点（兄妹/友情/守护）

fatigue_management:
  rule: "连续2章高强度战斗后必须插入≥1章缓冲章（日常/升级/设定释放）"
  penalty: "连续战斗→体能下降→战力×0.7→需道具/休息恢复"
```

产出到 `00-总控/数值体系/`

## 四段框架参考

| 阶段 | 机制 | 质变标志 |
|:-----|:------|:---------|
| 凡人 | 打基础 | 第一次使用超凡 |
| 超凡 | 激活自身力量 | 飞行/外放/金身 |
| 破格 | 杠杆放大外部超凡 | 空间/法则/影响天象 |
| 神话 | 概念层面 | 自成世界/操纵因果 |

## 断级差参考

| 跨级 | 预期 |
|:-----|:------|
| 同级 | 五五开（装备/战术定胜负） |
| 越1级 | 需合理解释（装备/环境/代价） |
| 越2级 | 极特殊情境，不可复用 |
| 越3级 | 体系崩了 |

完整分析见 `references/网文力量体系大全.md`。
