# Phase 5：数值体系模板升级

## 前置条件
project.yaml 已嵌入 reader_profile。

## 加载参考
先加载 `phases/phase-5.ref.md`，再加载 `references/网文力量体系大全.md`。

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
