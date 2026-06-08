# Step 12：输出清单

> 所属管线: pop-novel-plot v4.1+

---

## 正式产出

### 产出目录

### P0 强制产出（缺失则不进章纲）

| # | 产物 | 路径 | 模板 |
|:-:|:-----|:-----|:-----|
| 1 | **act-XX.yaml** | `设计/幕/act-XX.yaml` | `templates/act-guide.md` |
| 2 | **act-XX-人物.md** | `设计/幕/act-XX-人物.md` | `templates/character-list.md` |
| 3 | **act-XX-地图.md** | `设计/幕/act-XX-地图.md` | `templates/map-design.md` |

### P1 建议产出（有则更好）

| # | 产物 | 路径 | 模板 |
|:-:|:-----|:-----|:-----|
| 4 | **节点B-XX.md** | `设计/幕/节点B-XX.md` | `templates/checkpoint-b.md` |
| 5 | **情节线草案-XX.md** | `设计/幕/情节线草案-XX.md` | `templates/plotline-draft.md` |
| 6 | **info-release-XX.md** | `设计/幕/info-release-XX.md` | `templates/info-release.md` |
| 7 | **act-XX-势力.md** | `设计/幕/act-XX-势力.md` | `templates/faction-dynamics.md` |
| 8 | **act-XX-装备.md** | `设计/幕/act-XX-装备.md` | `templates/equipment-flow.md` |
| 9 | **节奏自检报告.md** | `设计/幕/节奏自检报告.md` | `templates/rhythm-check.md` |
| 10 | **里程碑设计.md** | `设计/里程碑设计.md` | `templates/milestone-design.md` |

### P2 可选产出

| # | 产物 | 路径 |
|:-:|:-----|:-----|
| 11 | **情节线纲汇总表.md** | `设计/幕/情节线纲汇总表.md` |

---

## P0 产物完整性检查

每个 P0 产物必须在 Step 12 结束时通过以下检查：

- [ ] act-XX.yaml 所有字段已填充（不可有空值或占位符）
- [ ] act-XX.yaml 包含 _meta.canvas_refs 声明
- [ ] act-XX.yaml 包含 core_conflict / act_end_state / equipment_flow 三个 v4.1 新增字段
- [ ] act-XX.yaml 每章有 plotlines_active / chekhov_set / chekhov_fire / info_release
- [ ] act-XX.yaml 每章有 characters_active / locations（★ v4.1 canvas 消费字段）
- [ ] act-XX.yaml 每章的 characters_active 角色在 act-XX-人物.md 中存在
- [ ] act-XX.yaml 每章的 locations 地点在 act-XX-地图.md 中存在
- [ ] act-XX-人物.md 主角卷初/卷末状态已填
- [ ] act-XX-人物.md 每个配角有"在本卷的角色"说明
- [ ] act-XX-人物.md 出场节奏图无过度空白
- [ ] act-XX-地图.md 每个关键地点有视觉印象描述
- [ ] act-XX-地图.md 移动线路覆盖主角所有位移

---

## 下游消费入口

act-XX.yaml 的 info_release 字段是正文 writer 骨架 Agent 的消费入口：
> 按 source_doc 从 L1 设定提取具体内容

act-XX-人物.md 是章纲"登场人物卡"的消费入口：
> 章纲阶段从此文件读取本卷角色池

act-XX-地图.md 是正文场景设计的消费入口：
> 正文阶段从此文件读取场景描述基线
