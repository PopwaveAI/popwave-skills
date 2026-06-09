# Step 12：产出自检（不是"产出时刻"——每个文件的产出在对应 Step）

> 所属管线: pop-novel-plot v4.3
> **核心原则：一步一产出。** Step 3 产出里程碑设计，Step 4 产出情节线草案……每个文件在对应 Step 结束时已写入磁盘。Step 12 不产出任何新文件——只做完整性校验。

---

## 分步产出对照（Agent 执行时对照此表，每完成一步就写一个文件）

| Step | 产出文件 | 完成标记 |
|:----:|:---------|:--:|
| 3 | `设计/里程碑设计.md` | [ ] |
| 4 | `设计/幕/情节线草案-XX.md` | [ ] |
| 5 | `设计/幕/act-XX-人物.md` | [ ] |
| 6 | `设计/幕/act-XX-地图.md` | [ ] |
| 7 | `设计/幕/act-XX-势力.md` + `设计/幕/act-XX-装备.md` | [ ] |
| 8 | `设计/幕/info-release-XX.md` | [ ] |
| 9 | `设计/幕/act-XX.yaml` | [ ] |
| 10 | 场景卡试读（交互品，`_temp/` 目录） | [ ] |
| 11 | `设计/幕/节奏自检报告.md` | [ ] |
| 12 | 本步 — 校验以上全部 | [ ] |

> **禁止等 12 步走完再批量产出。** Agent 执行 Step N 时，立即写入 Step N 对应的文件。Step 12 只是检查这些文件是否就位、是否通过各模板的产出自检。

---

## P0 产物完整性检查（Step 12 执行）

> 以下所有文件应在 Step 3~11 中已生成。Step 12 只做逐项确认。

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
- [ ] 爽点频率红线（§9）：战斗 ≤2 章间隔 & 成长 ≤2 章间隔
- [ ] 高潮章深度约束：enemy_level + 子节拍展开 + equipment_reward 全部填充
- [ ] 上游角色卡消费：主角等级/属性与 L3-角色层角色卡一致

---

## 下游消费入口

act-XX.yaml 的 info_release 字段是正文 writer 骨架 Agent 的消费入口：
> 按 source_doc 从 L1 设定提取具体内容

act-XX-人物.md 是章纲"登场人物卡"的消费入口：
> 章纲阶段从此文件读取本卷角色池

act-XX-地图.md 是正文场景设计的消费入口：
> 正文阶段从此文件读取场景描述基线
