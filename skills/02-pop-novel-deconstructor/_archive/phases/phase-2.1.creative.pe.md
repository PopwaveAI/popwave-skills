# Phase 2.1：故事引擎模板提取 — decon-creative

> **对齐写作端**：pop-novel-creative → `00-原始设定/故事引擎.md` + `_样品试读/样品-v1.md`
> **消费关系**：本相位产出 → pop-novel-creative Phase 0 加载 → 按新书调参 → 生成故事引擎.md
> **前置条件**：Phase 0 采样日志 + Phase 1 诊断报告已产出

## 速查表

| 步骤 | 操作 | 读什么 | 产出 | 门禁 |
|:-----|:-----|:-------|:-----|:-----|
| 1 | 核心假说提取 | 全书前100章采样日志 | 一句话+碰撞点+世界锚点 | ❌ 碰撞点无互否退回 |
| 2 | 宪法约束提取 | 全书阅读记录 | 基调/主角/世界/叙事四类约束 | ❌ 缺原文证据退回 |
| 3 | 卖点+读者分析 | 前1000字+全书 | 核心爽点/对标差异/读者画像/前三章承诺 | ❌ 无章节数据支撑退回 |
| 4 | 结构预期提取 | 全书卷/幕结构 | 卷1-4的起点/终点/核心追问 | ❌ 少于2卷标注"单卷" |
| 5 | 主角蓝图 | 全书 | 四维（身份/驱力/缺陷/唯一性） | ❌ 缺填充退回 |
| 6 | 产出模板 | 步骤1-5全部产出 | `_template_library/{书名}/00-原始设定/story-engine-template.yaml` | ❌ 非YAML退回 |

## 产出到 _template_library/ 的文件

```
_template_library/{书名}/
└── 00-原始设定/
    └── story-engine-template.yaml     ← 对应项目中的 00-原始设定/故事引擎.md
```

## 模板文件示例

写入 `00-原始设定/story-engine-template.yaml`：

```yaml
# Template: 故事引擎
# @consumed_by: pop-novel-creative (Phase 0)
# @source_book: 深渊主宰
# @source_chapters: [1, 187]
# @template_version: 1.0.0
# @对应项目文件: 00-原始设定/故事引擎.md
#
# 使用说明：
#   1. 创作端creative Phase 0 加载此文件
#   2. 按新书卖点修改每个字段的值
#   3. 产出到新项目的 00-原始设定/故事引擎.md

core_premise:
  one_liner: "游戏高玩索伦穿越到DND世界，带着妹妹在圣者浩劫中从贫民窟刺客成长为深渊主宰"
  core_hypothesis: "DND规则数据化+前世游戏经验可以直接使用"
  collision_point:
    elements: [穿越者灵魂融合, DND游戏面板真实化, 守序邪恶主角, 妹妹养成线, 圣者浩劫]
    mutual_negation: "想保护妹妹→必须变强→变强的方式是杀戮→杀戮越多离"普通人"越远→最终成为主宰时已不是那个只想保护妹妹的少年"
    intensity: "★★★"
  world_anchor:
    era: "动荡之年（圣者浩劫前夜）"
    region: "费伦·琥珀城·贫民区 → 剑湾 → 深渊"
    power_scale: "凡人(5平民/1游荡者) → 传奇 → 神灵(深渊主宰)"

protagonist_profile:
  identity: "穿越者+游戏高玩，DND面板觉醒"
  drive: "保护妹妹薇薇安 + 变强活下来"
  flaw: "守序邪恶路径依赖——遇到问题就想杀了"
  uniqueness: "穿越者+DND面板+守序邪恶+妹妹养成=独特配方"

selling_points:
  core_pleasure: "DND面板数据化的硬核升级体验 + 妹妹养成的情感锚点 + 守序邪恶的独特主角视角"
  differentiation: "守序邪恶主角(罕见) + 妹妹养成线(情感锚点) + 面板流数据化(规整可预见)"
  reader_profile:
    age_group: "18-30"
    pleasure_preference: "数据化升级/战斗反馈/妹妹互动"
    drop_threshold: "连续5章无升级"
  opening_3_chapters_promise: "ch1情感困境(妹妹视角)→ch2面板觉醒+世界观→ch3第一次超凡接触"

constitutional_bounds:
  tone:
    forbidden: ["纯黑无温暖——妹妹线崩了书就毁了"]
  protagonist:
    never: ["主动出卖薇薇安", "无缘无故滥杀"]
    always: ["保护妹妹优先于一切", "遇到问题先想破坏性方案"]
  world_rule:
    never: ["DND面板规则在关键时刻失效而不给解释"]
  narrative:
    never: ["连续5章无面板数据", "妹妹连续消失超过10章"]
    always: ["每3-5章一次升级或战力反馈", "每条剧情线连续留白 ≤ 3章"]

first_page:
  opening_scene: "薇薇安在贫民窟厨房给昏迷的索伦煮粥。门外的雨。老狗希斯守在门口。"
  signature_scene: "索伦第一次杀人的雨夜——匕首划过贫民区混混的喉咙，血溅在墙上的月光里"

structural_expectation:
  volumes:
    - volume: 1
      start: "贫民窟，索伦昏迷苏醒"
      end: "藏宝洞中拿到万象无常牌"
      core_question: "怎么活下来"
    - volume: 2
      start: "琥珀城冒险者工会"
      end: ""
      core_question: "怎么变强"
    - volume: 3
      start: ""
      end: ""
      core_question: "谁在猎杀谁"
```

## 落盘检查点

| 路径 | 状态 |
|:-----|:-----|
| `_template_library/{书名}/00-原始设定/story-engine-template.yaml` | [ ] |

## 下一步

完成 → 进入 Phase 2.2 (decon-world)
