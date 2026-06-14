# Phase 2.4：叙事技法模板提取 — decon-prose

> **对齐写作端**：pop-novel-prose-render Step 1~3 → `写作资产/设计包/chXXX-设计包.md`
> **明确边界**：pop-dna 提取文风指纹（句式/词汇/感官）。decon-prose 只提取叙事结构（章纲/战斗/密度）。
> **消费关系**：本相位产出 + pop-dna 产出 → prose-render Step 1 加载
> **前置条件**：Phase 2.3 (decon-plot) 已完成

## 速查表

| 步骤 | 操作 | 读什么 | 产出(文件) | 门禁 |
|:-----|:-----|:-------|:----------|:-----|
| 1 | 章纲结构 | 抽样12章 | `写作资产/设计包/chXXX-设计包-template.md` | ❌ <6章退回 |
| 2 | 战斗公式 | ≥5场战斗 | 嵌入设计包中的战斗公式节 | ❌ <3场退回 |
| 3 | 信息密度 | 抽样章 | 嵌入设计包中的密度节 | ❌ 缺ratio退回 |
| 4 | pop-dna 参考 | 全书 | `写作资产/文风DNA/{书名}-文风参考.yaml`（结构侧） | ❌ 可选 |

## 产出到 _template_library/ 的文件

```
_template_library/{书名}/
├── 写作资产/
│   ├── 设计包/chXXX-设计包-template.md    ← 章级设计包骨架
│   └── 文风DNA/
│       └── {书名}-文风参考-template.yaml    ← 结构侧文风参考
│                                           （pop-dna产出独立的文风DNA文件）
```

## 模板文件示例

写入 `写作资产/设计包/chXXX-设计包-template.md`：

```yaml
# Template: 章级设计包
# @consumed_by: pop-novel-prose-render (Step 1~3)
# @对应项目文件: 写作资产/设计包/chXXX-设计包.md

scene:
  type: ""
  location: ""
  time: ""

battle_formula:                          # 战斗章参考
  phases:
    - "战前准备(avg段落2)"
    - "对峙(avg段落3)"
    - "攻防交替(avg段落6)"
    - "转折(avg段落2)"
    - "终击(avg段落3)"
    - "战后处理(avg段落2)"
  sensory_mix: {visual: 50, auditory: 15, tactile: 25, emotional: 10}

chapter_structure:                       # 章纲结构参考
  avg_paragraphs: 35
  avg_scenes: 4
  scene_transition: "空间跳(直接切黑)"

info_density:                            # 信息密度参考
  per_chapter:
    event_count: 5
    dialogue_ratio: 35
    description_ratio: 30
    inner_monologue_ratio: 15
    combat_ratio: 20

render_strategy:                         # 渲染策略参考
  pov_switch: "固定视角(主角) + 偶尔切妹妹"
  narrator_distance: "近(贴主角脑内) - 战斗时中距"
  timeline: "纯顺序"
```

写入 `写作资产/文风DNA/{书名}-文风参考-template.yaml`：

```yaml
# Template: 文风参考（结构侧）
# @consumed_by: pop-novel-prose-render (Step 3 风格验证)
# @source_book: 深渊主宰
#
# 注意：此文件仅覆盖叙事结构层面。
# 句法/词汇/感官等文风DNA由 pop-dna 独立执行。

opening_chapter_pattern:
  first_line_type: "动作句(雨声+厨房动作)"
  hook_position_in_first_1000_words: 600

climax_construction:
  buildup_chapters: 3
  climax_paragraphs: 12
  cooldown_chapters: 1

first_volume_gate:
  ch01_hook: true
  ch01_core_selling: true
  ch02_first_conflict: true
  max_pure_setup_chapters: 1
```

## 落盘检查点

| 路径 | 状态 |
|:-----|:-----|
| `_template_library/{书名}/写作资产/设计包/chXXX-设计包-template.md` | [ ] |
| `_template_library/{书名}/写作资产/文风DNA/{书名}-文风参考-template.yaml` | [ ] |

## 下一步

完成 → 进入 Phase 3（验证采样）
