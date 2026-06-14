# Phase 2.2：世界构筑模板提取（Lv2）

> 对齐写作端：06-pop-novel-world Phase 1~6 → L1六件套 + 数值体系 + 起点快照 + 世界宪法
> 使用模板：`templates/L1-01~06.tpl.md` + `templates/combat-capability.tpl.yaml` + `templates/starting-snapshot.tpl.md`
> 前置条件：Phase 0 采样日志 + Phase 1 诊断报告

---

## 🔥 开工前必读：原文验证门禁

**第一条：原文必须已读取。** 未读完前100章就来写 → 退回。不得凭记忆编造。

**第二条：每一条写入产出文件的信息，都必须能在原文中找到对应章节的证据。** 找不到原文证据 → 不准写。留空比编造安全。

**第三条：所有推断必须标注「推断」标签。** 不得把推断写成事实。

**第四条：L1 六件套中每个维度的数据必须从原文提取。** 不得编造"境界名"、"势力名"、"货币名称"等事实性内容。

---

## 🔧 数据提取前置命令（硬性！先执行再写产出）

执行世界观提取脚本，结果写入 `_temp/world-data.json` 和 `_temp/baseline-data.json`。此 JSON 是写 L1 六件套和数值体系的唯一数据来源。

### 第一步：执行基线提取（ch1-20，角色/地名基线）
```powershell
python "..\_scripts\extract.py" baseline "{$TXT_FILE_PATH}" ".\_temp\"
```
输出：`_temp/baseline-data.json`

### 第二步：执行世界观提取（ch1-100，7大类世界观数据）
```powershell
python "..\_scripts\extract.py" world "{$TXT_FILE_PATH}" ".\_temp\"
```
输出：`_temp/world-data.json`

字段说明：
| 字段 | 内容 |
|:-----|:-----|
| `categories.deity.entries[]` | 神祇/圣者/神格提及 + 出处 chXX |
| `categories.magic.entries[]` | 法术/魔法/环级体系 + 出处 chXX |
| `categories.class.entries[]` | 等级/职业/进阶路径 + 出处 chXX |
| `categories.species.entries[]` | 种族/血脉/特异生物 + 出处 chXX |
| `categories.faction.entries[]` | 势力/组织/神殿 + 出处 chXX |
| `categories.item.entries[]` | 物品/装备/货币 + 出处 chXX |
| `categories.geography.entries[]` | 地名/地理特征 + 出处 chXX |

### 第三步：逐件套匹配（将 JSON 数据填入对应模板）

| 模板文件 | 对应 JSON 字段 |
|:---------|:---------------|
| L1-01-世界蓝图.tpl.md | `geography` + `deity` + 部分 `magic` |
| L1-02-力量体系.tpl.md | `class` + `magic` |
| L1-03-历史与驱动力.tpl.md | `deity` + `faction` + `geography` |
| L1-04-物种与天赋.tpl.md | `species` |
| L1-05-势力格局.tpl.md | `faction` + `geography` |
| L1-06-资源与物品.tpl.md | `item` |
| combat-capability.tpl.yaml | `class` + 手动从战斗章提取数值 |

### 规则
1. **每个模板填写的每个事实都必须能在对应 JSON 字段中找到**，标注 chXX
2. JSON 中某类别无条目 → 说明原文中该维度数据极少 → 产出中必须标注"（前100章未显露）"
3. 写数值体系时，等级/段位数据来自 `class` 字段，不得凭记忆编造境界链
4. 写一半发现缺数据 → 返回修改提取脚本扩大范围 → 重新提取 → 再填

---


## 速查表

| 步骤 | 操作 | 读什么 | 产出 | 门禁 |
|:-----|:-----|:-------|:-----|:-----|
| 1 | L1-01 世界蓝图 | 全书前100章 | `L1-元设定层/01-世界蓝图.md`（5子字段，800-1500字） | ❌ 缺地理总览退回 |
| 2 | L1-02 力量体系 | 全书设定密集章 | `L1-元设定层/02-力量体系.md`（5子字段，800-2000字） | ❌ 缺境界链退回 |
| 3 | L1-03 历史与驱动力 | 全书 | `L1-元设定层/03-历史与驱动力.md`（3子字段，500-1000字） | ❌ 缺核心矛盾退回 |
| 4 | L1-04 物种与天赋 | 全书 | `L1-元设定层/04-物种与天赋.md`（3子字段，600-1500字） | ❌ 缺主要种族退回 |
| 5 | L1-05 势力格局 | 全书 | `L1-元设定层/05-势力格局.md`（3子字段，500-1200字） | ❌ 缺势力列表退回 |
| 6 | L1-06 资源与物品 | 全书 | `L1-元设定层/06-资源与物品.md`（3子字段，400-800字） | ❌ 缺货币体系退回 |
| 7 | 数值体系 | 战斗章+升级章 | `00-总控/数值体系/*.yaml`（4文件） | ❌ 缺数据退回 |
| 8 | 起点快照 | L1转化 | `设计/起点快照.md`（5段） | ❌ 缺主角状态退回 |


## 产出结构

```
项目根/
├── 00-原始设定/L1-元设定层/
│   ├── 01-世界蓝图.md       ← 按 templates/L1-01-世界蓝图.tpl.md（地理/位面规则/核心法则/力量来源/基调）
│   ├── 02-力量体系.md       ← 按 templates/L1-02-力量体系.tpl.md（境界/路径/突破/天花板/跨级）
│   ├── 03-历史与驱动力.md    ← 按 templates/L1-03-历史与驱动力.tpl.md（纪元/前提事件/核心矛盾）
│   ├── 04-物种与天赋.md     ← 按 templates/L1-04-物种与天赋.tpl.md（种族表/异兽/特殊血脉）
│   ├── 05-势力格局.md       ← 按 templates/L1-05-势力格局.tpl.md（主要势力/权力分布/势力关系）
│   └── 06-资源与物品.md     ← 按 templates/L1-06-资源与物品.tpl.md（修炼资源/关键道具/货币）
├── 00-原始设定/世界宪法.md
├── 00-总控/数值体系/
│   ├── combat_capability.yaml  ← 按 templates/combat-capability.tpl.yaml（段位/攻击/突破/角色/弱点/标志画面）
│   ├── monster_rank_map.yaml   ← 怪物-段位映射
│   ├── act_rank_schedule.yaml  ← Act-等级排期
│   └── collision_curve.yaml    ← 战斗类型分布+情绪弧线+疲劳管理
└── 设计/起点快照.md            ← 按 templates/starting-snapshot.tpl.md（主角/配角/世界/伏笔/关系）
```

## 格式规则

- **L1 六件套全部 .md** — 叙事优先，含 `[主角]` 标签标注
- **数值体系全部 .yaml** — 结构化，创作端可直接 parse
- **起点快照 .md** — 5段完整

## 落盘检查点

| 路径 | 状态 |
|:-----|:-----|
| `00-原始设定/L1-元设定层/01-世界蓝图.md` | [ ] |
| `00-原始设定/L1-元设定层/02-力量体系.md` | [ ] |
| `00-原始设定/L1-元设定层/03-历史与驱动力.md` | [ ] |
| `00-原始设定/L1-元设定层/04-物种与天赋.md` | [ ] |
| `00-原始设定/L1-元设定层/05-势力格局.md` | [ ] |
| `00-原始设定/L1-元设定层/06-资源与物品.md` | [ ] |
| `00-原始设定/世界宪法.md` | [ ] |
| `00-总控/数值体系/combat_capability.yaml` | [ ] |
| `00-总控/数值体系/monster_rank_map.yaml` | [ ] |
| `00-总控/数值体系/act_rank_schedule.yaml` | [ ] |
| `00-总控/数值体系/collision_curve.yaml` | [ ] |
| `设计/起点快照.md` | [ ] |


## 下一步

完成 → 进入 Phase 2.3 (decon-plot)
