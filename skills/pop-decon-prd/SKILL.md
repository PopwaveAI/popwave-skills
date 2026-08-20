---
name: pop-decon-prd
description: 全书立项设计。当用户说'拆书PRD''立项破解''立项设计'时启用。消费各维度拆解产出（方案A）→产出立项级文档含逆向破解总结+商业可行性+连载规划+风险预警。
---
# pop-decon-prd
> 全书立项设计 v2.0.0。方案A 拆书管线最后环节，消费 pop-decon-dimension 各维度产出。

## 做什么
| 输入 | 来源 | 输出 | 下游 |
|------|------|------|------|
| 各维度拆解产出（剧情/情感/人物/力量/世界观/爽点/文风） | pop-decon-dimension | 全书立项设计.md | 无（拆书终点） |

核心哲学：拆书=逆向破解。PRD是破解完成后的总结报告，不产生新数据，只综合已有数据。

## 怎么操作（SOP骨架）
> execution.mode: Step 1数据收集可并行2-3个子agent；Step 2必须主agent综合执行。
> 强加载：红线+速查表（每轮必读）；弱加载：steps/templates/references按步骤按需加载。

### Step 1: 收集各维度产出 → `steps/step-1-collect.md`
- 收集 pop-decon-dimension 各维度产出（剧情线/情感线/人物/力量/世界观/爽点/文风档案）→ `_temp/prd-collected-data.md`

### Step 2: 综合产出立项设计 → `steps/step-2-synthesize.md`
- 全维度交叉验证 → `全书立项设计.md`（逆向破解总结+全书结构+商业可行性+连载规划+风险预警+启动检查清单）

## 红线
1. **读取协议**：强加载=红线+速查表（每轮必读）；弱加载=steps/templates/references按步骤按需加载。Step 1可并行，Step 2必须串行。
2. **维度产出缺失就执行** — 剧情/力量/世界观等维度产出缺失 → 退回 pop-decon-dimension
3. **核心假说无证据支撑** — 核心假说必须有维度产出的 chXX 证据，不得凭书名/直觉编造
4. **赛道判定凭书名猜测** — 赛道必须基于实际拆解数据（设定+名场面爽感公式）
5. **PRD与各维度数据矛盾** — 结论必须与各维度产出一致，不得自行推翻已有结论

## 速查表
| 文件 | 读取时机 | 核心内容 |
|------|----------|----------|
| SKILL.md | 每轮必读 | 红线+SOP骨架+速查表 |
| steps/step-1-collect.md | Step 1执行时 | 各维度产出收集方法 |
| steps/step-2-synthesize.md | Step 2执行时 | 立项设计综合产出方法 |
| pop-decon/references/pipeline-context.md（规范源） | 需要管线上下文时 | 管线位置与前置条件 |
| templates/book-prd.tpl.md | Step 2产出时 | 立项设计模板 |

## 版本
v2.0.0 | 2026-08-13 | 方案A 重构：消费源从 Phase1-3 全产出改为 pop-decon-dimension 各维度产出 → [CHANGELOG.md](CHANGELOG.md)

