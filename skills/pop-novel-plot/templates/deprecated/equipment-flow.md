# 本卷装备/资源变化模板

> 产出路径: `设计/幕/act-XX-装备.md`
> 下游消费: pop-novel-chapter-design → 事件中装备变化参考

---

# act-XX · 本卷装备/资源变化

> 所属幕: act-XX · 第X幕
> 产出管线: pop-novel-plot v4.1+
> @source: combat_capability.yaml → ranks[本卷段位].min_attack/max_attack
> @source: monster_rank_map.yaml → 掉落怪物的段位
> @source: act_rank_schedule.yaml → schedule[本卷].end_rank

---

## 一、装备变化清单

### 获得

| 物品 | 获得章 | 来源 | 攻击力/效果 | 对应段位 | 对剧情的影响 |
|:-----|:-----:|:-----|:----------|:-------|:------------|
| | | 购买/掉落/奖励/制作 | | 角色当前段位±1 | |
| | | | | | |

### 消耗/遗失

| 物品 | 遗失章 | 原因 | 影响 |
|:-----|:-----:|:-----|:-----|
| | | 被毁/被盗/交换/用尽 | |

### 升级

| 物品 | 升级章 | 升级前 | 升级后 | 触发条件 |
|:-----|:-----:|:-------|:-------|:---------|

## 二、资源变化

| 资源 | 卷初 | 卷末 | 变化原因 |
|:-----|:----:|:----:|:---------|
| 金币 | | | |
| 消耗品 | | | |
| 人情/情报 | | | |

## 三、装备流检查

- [ ] 所有获得装备的攻击力在 combat_capability.yaml → ranks[对应段位] 的 min/max 范围内
- [ ] BOSS掉落装备的阶位 ≥ monster_rank_map 中该 BOSS 段位 - 1
- [ ] 卷末装备状态 = act_end_state.protagonist.equipment_gained/lost
- [ ] 卷内无装备"通货膨胀"（≥5次获得且≥3次消耗）
