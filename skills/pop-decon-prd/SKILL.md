---
name: pop-decon-prd
description: 全书立项设计。当用户说'拆书PRD''立项破解''立项设计'时启用。消费L1-L4全管线产出→产出立项级文档(逆向破解总结/商业可行性/连载规划/风险预警)。
---
# pop-decon-prd
> 全书立项设计 v1.2.0。Phase 4 of deconstruction，拆书管线最后环节。

## 做什么
| 输入 | 来源 | 输出 | 下游 |
|------|------|------|------|
| L1-L4全管线产出 | Phase 1-3 | 全书立项设计.md | 无（拆书终点） |

管线：Phase 1(设计包) → Phase 2(L2/L3) → Phase 3(设定) → **Phase 4(立项设计)**

核心哲学：拆书=逆向破解。PRD是破解完成后的总结报告，不产生新数据，只综合已有数据。

## 怎么操作（SOP骨架）
> execution.mode: Step 1数据收集可并行2-3个子agent；Step 2必须主agent综合执行。
> 强加载：红线+速查表（每轮必读）；弱加载：steps/templates/references按步骤按需加载。

### Step 1: 收集全管线产出 → `steps/step-1-collect.md`
- 收集L1-L4全部产出（设计包/单元卡/剧情线/全书事件/设定/创意溯源/文风档案/套路库）→ `_temp/prd-collected-data.md`

### Step 2: 综合产出立项设计 → `steps/step-2-synthesize.md`
- 全管线交叉验证 → `全书立项设计.md`（逆向破解总结+全书结构+商业可行性+连载规划+风险预警+启动检查清单）

## 红线
1. **读取协议**：强加载=红线+速查表（每轮必读）；弱加载=steps/templates/references按步骤按需加载。Step 1可并行，Step 2必须串行。
2. **Phase 3未完成就执行** — 金手指/人物卡/设定产出缺失 → 退回Phase 3
3. **核心假说无证据支撑** — 核心假说必须有L1-L4的chXX证据，不得凭书名/直觉编造
4. **赛道判定凭书名猜测** — 赛道必须基于实际拆解数据（设定+创意溯源）
5. **可复用资产引用未入库条目** — 必须引用已入库的pop-trope-library条目
6. **PRD与全管线数据矛盾** — 结论必须与L1-L4产出一致，不得自行推翻已有结论

## 速查表
| 文件 | 读取时机 | 核心内容 |
|------|----------|----------|
| SKILL.md | 每轮必读 | 红线+SOP骨架+速查表 |
| steps/step-1-collect.md | Step 1执行时 | 全管线数据收集方法 |
| steps/step-2-synthesize.md | Step 2执行时 | 立项设计综合产出方法 |
| references/pipeline-context.md | 需要管线上下文时 | 管线位置与前置条件 |
| templates/book-prd.tpl.md | Step 2产出时 | 立项设计模板 |

## 版本
v1.2.0 | 2026-07-22 | SKILL.md按设计规范重写：frontmatter补触发条件、红线重构为6条(首条读取协议)、速查表改为文件目录引导、版本历史移至CHANGELOG。
