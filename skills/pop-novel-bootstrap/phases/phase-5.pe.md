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
