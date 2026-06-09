# Step 7：本卷世界设计 — 势力/装备/卷末状态（NEW v4.1）

> 所属管线: pop-novel-plot v4.1+
> 产出: `设计/幕/act-XX-势力.md` + `设计/幕/act-XX-装备.md`（act-XX.yaml 中已内嵌核心字段）
> 模板: `templates/faction-dynamics.md` + `templates/equipment-flow.md`

---

### 前置条件（填之前确认）

- [ ] act-XX-人物.md 已产出
- [ ] act-XX-地图.md 已产出
- [ ] 情节线草案-XX.md 已产出
- [ ] 里程碑设计.md 已产出
- [ ] info-release-XX.md 已产出
- [ ] `{项目}/00-总控/数值体系/combat_capability.yaml` — 段位战力范围。卷末 protagonist.level 必须在此范围内。
- [ ] `{项目}/00-总控/数值体系/act_rank_schedule.yaml` — 卷级段位排期。确认本卷主角目标段位。
- [ ] `{项目}/00-总控/数值体系/collision_curve.yaml` — 碰撞曲线。确认本卷战斗章分布与张力峰值。
- [ ] 参考书拆解 T6（数据流写法模板）— 确认原著的装备/伤害数值表述风格。禁止输出原著不存在的数值格式（如原著用扁平数值 +8 就不能写 1d8+1）。

## 目的

从「一卷」视角补全 act-XX.yaml 中已内嵌但需要展开的三个维度：

### A. 势力动态（产出: `设计/幕/act-XX-势力.md`）

按 `templates/faction-dynamics.md` 模板：
1. **本卷活跃势力总览**：哪些势力在本卷活动，各自目标是什么
2. **各势力详细动态**：卷初→卷末的变化
3. **势力关系网络**：势力间的矩阵关系
4. **势力行动时间线**：每章各势力在做什么
5. **势力冲突热点**：冲突在哪些章段升级/缓和

### B. 装备/资源变化（产出: `设计/幕/act-XX-装备.md`）

按 `templates/equipment-flow.md` 模板：
1. **装备变化清单**：获得/消耗/升级
2. **核心装备状态追踪**：卷初→卷末
3. **资源变化统计**：金钱、丹药、符箓、情报、人脉
4. **装备与剧情节点的对应**：每个装备的"高光时刻"
5. **装备设计红线**

### C. 卷末状态预期（act-XX.yaml 内嵌字段）

`act.act_end_state`:
```yaml
act_end_state:
  protagonist:
    level: "等级变化"
    equipment_gained: ["获得的装备"]
    equipment_lost: ["消耗/失去的装备"]
    mental_state: "心智状态变化"
    key_relationship_changes: ["关系变化描述"]
  world:
    crisis_level: "世界危机升级程度"
    faction_changes: ["势力格局变化"]
    revealed_info: ["新揭示的世界观信息"]
```

---

## 产出清单

| 产物 | 路径 | 强制等级 |
|:-----|:-----|:--------:|
| act-XX-势力.md | 设计/幕/ | P1（建议产出） |
| act-XX-装备.md | 设计/幕/ | P1（建议产出） |
| act_end_state 字段 | act-XX.yaml 内嵌 | P0（强制） |

---

## 引用

- 模板: `templates/faction-dynamics.md`
- 模板: `templates/equipment-flow.md`
