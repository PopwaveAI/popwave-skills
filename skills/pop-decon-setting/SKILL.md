---
name: pop-decon-setting
description: Phase 3 拆书设定包。当用户说'归纳世界观''提取设定''力量体系'时启用。消费设计包+L2/L3→产出骨架层(力量体系)+血肉层+角色层+叙事资产层。
---
# pop-decon-setting
> Phase 3 设定世界观+角色+叙事资产 v3.4.0。骨架层(力量体系)先于血肉层完成。

## 做什么
| 输入 | 来源 | 输出 | 下游 |
|------|------|------|------|
| 设计包+L2/L3+Wiki骨架(可选) | Phase 1/2 | 骨架层+血肉层+角色层+叙事资产层 | pop-decon-trace |

管线：Phase 1(设计包) → Phase 2(L2/L3) → **Phase 3(设定)** → Phase 4(立项)

## 怎么操作（SOP骨架）
> execution.mode: 骨架层必须先单独完成；血肉层完成后可并行3-4个子agent。
> 强加载：红线+速查表（每轮必读）；弱加载：step/templates按步骤按需加载。

### 骨架层（第一优先级·必须先完成）
- Step 2 力量体系 → `steps/step-2-power-system.md`：核心力量定义+境界金字塔+主角路线图+拆解理解

### 血肉层（骨架完成后·可并行）
- Step 1 地理蓝图 → `steps/step-1-geography.md`（骨架锚点：力量层级空间投影）
- Step 3 历史与驱动力 → `steps/step-3-history.md`（骨架锚点：力量体系历史演化）
- Step 5 势力格局 → `steps/step-5-factions.md`（骨架锚点：势力力量层级定位）
- Step 6 资源与物品 / Step 4 物种与天赋 → `steps/step-6-items.md` / `steps/step-4-species.md`
- Step 10 金手指设计 → `steps/step-10-golden-finger.md`（与L1-02交叉验证）
- Step 7 世界观弹性边界 → `steps/step-7-elastic-boundary.md`（≥3原文证据）
- Step 8 数值体系(可选) → `steps/step-8-combat.md`

### 角色层
- Step 11 主要角色人物卡 → `steps/step-11-character-cards.md`（含敌人卡）
- Step 13 角色对白风格库 → `steps/step-13-dialogue-style.md`（逐字摘录原文对白）

### 叙事资产层（续写/同人专用）
- Step 12 伏笔与悬念追踪 → `steps/step-12-foreshadowing.md`（含续写入口清单）
- Step 14 经典场景拆解 → `steps/step-14-iconic-scenes.md`（含场景节奏分析）

## 红线
1. **读取协议**：强加载=红线+速查表（每轮必读）；弱加载=step/templates按步骤按需加载。骨架层未完成时不得加载血肉层step。
2. **Phase 2 未完成就归纳** — L2/L3产出缺失 → 退回 Phase 2
3. **骨架层未完成就写血肉层** — L1-02力量体系未产出时不得开始血肉层设定
4. **凭空发明设定/境界链** — 无chXX证据且未标注「数据极少」的名称或分级体系=编造
5. **前N章产出全书级文件** — 文件名不得含"全书"，必须有scope声明
6. **Wiki数据未标注置信度** — 从wiki-skeleton消费的设定必须标注「Wiki来源」
7. **正文内联chXX** — 正文中不得出现内联章节号，证据归表格列或段落末尾证据行

## 速查表
| 文件 | 读取时机 | 核心内容 |
|------|----------|----------|
| SKILL.md | 每轮必读 | 红线+SOP骨架+速查表 |
| steps/step-2-power-system.md | 骨架层执行时 | 力量体系归纳逻辑+落盘检查 |
| steps/step-1-geography.md | 血肉层执行时 | 地理蓝图+骨架锚点 |
| steps/step-3-history.md | 血肉层执行时 | 历史驱动力+骨架锚点 |
| steps/step-5-factions.md | 血肉层执行时 | 势力格局+骨架锚点 |
| steps/step-6-items.md | 血肉层执行时 | 资源与物品 |
| steps/step-4-species.md | 血肉层执行时 | 物种与天赋 |
| steps/step-10-golden-finger.md | 血肉层执行时 | 金手指设计 |
| steps/step-7-elastic-boundary.md | 血肉层执行时 | 世界观弹性边界 |
| steps/step-8-combat.md | 可选执行时 | 数值体系 |
| steps/step-11-character-cards.md | 角色层执行时 | 主要角色人物卡(含敌人卡) |
| steps/step-13-dialogue-style.md | 角色层执行时 | 角色对白风格库 |
| steps/step-12-foreshadowing.md | 叙事资产层执行时 | 伏笔与悬念追踪 |
| steps/step-14-iconic-scenes.md | 叙事资产层执行时 | 经典场景拆解 |
| references/pipeline-context.md | 需要管线上下文时 | 管线位置与前置条件 |
| templates/*.tpl.md | 对应步骤产出时 | 各产出物模板 |

## 版本
v3.4.0 | 2026-07-22 | SKILL.md按设计规范重写：frontmatter补触发条件、红线重构为7条(首条读取协议)、速查表改为文件目录引导、版本历史移至CHANGELOG。
