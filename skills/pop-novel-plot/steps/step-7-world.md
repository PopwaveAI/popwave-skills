# Step 7：本卷世界设计 — 势力/装备/卷末状态（NEW v4.1）

> 所属管线: pop-novel-plot v4.1+
> 产出: `设计/幕/act-XX-势力.md` + `设计/幕/act-XX-装备.md`（act-XX.yaml 中已内嵌核心字段）
> 模板: `templates/faction-dynamics.md` + `templates/equipment-flow.md`

---

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
