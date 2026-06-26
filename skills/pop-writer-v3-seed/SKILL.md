---
name: pop-writer-v3-seed
description: "v3涌现式种子设计。5步流程：step-0创意共创（元素融合+核心卖点+用户QA）→step-1三界压力调研→压力矩阵+冲突轴（研究档案持久化）→step-2金手指→step-3文风DNA蒸馏→step-4种子组装（主角引擎含行为准则）。六要素与用户逐步共创。种子文件夹结构（_index+_log+分要素文件）。活种子初始化。"
pipeline:
  upstream: [pop-decon, pop-shared-dna]
  downstream: [pop-writer-v3-emerge]
  references: [pop-trope-library]
version: 1.4.0
---

# 种子设计（v3涌现式）

5步流程：创意共创→生态调研→压力矩阵→金手指→文风DNA→种子组装。step-0吸收creative最佳实践（元素融合+搜索SOP），在调研前与用户共创核心卖点和创作方向。六要素不是agent自己产出，是和用户逐步共创出来的——每步产出后强制用户QA确认。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 文风DNA未蒸馏→项目初始化终止 | 扫描写作资产/文风库/，空=终止 |
| ❌2 | 金手指必须含≥1个行动驱动机制 | 任务/技能/经验/血量/战宠 |
| ❌3 | 压力矩阵≥3压力源 | 替代creative的生态图谱≥3角色群 |
| ❌4 | 种子写驱动力不写设定清单 | 决策导向，非设定堆砌 |
| ❌5 | 六要素必须经用户QA确认 | 每步产出后用户确认才进下一步 |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-0 | steps/step-0-creative-co-creation.md | 创意共创（元素融合+核心卖点+用户QA） |
| step-1 | steps/step-1-ecology-to-pressure.md | 三界压力调研→压力矩阵+冲突轴（用户QA确认） |
| step-2 | steps/step-2-golden-finger.md | 金手指行动引擎→种子金手指（用户QA确认） |
| step-3 | steps/step-3-dna-lock.md | 文风DNA蒸馏→文风库文件（不写入种子）（用户QA确认） |
| step-4 | steps/step-4-seed-assembly.md | 主角引擎+成长路径+目的地+种子组装+验证（用户QA确认） |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 1 压力矩阵调研 | `references/种子搜索法SOP.md` | 三界压力调研标准流程（社会界/自然界/超自然界） |
| Step 2 金手指设计 | `references/金手指设计指南.md` | 5维度行动引擎设计规范 |

## 路由

upstream `pop-decon` → **本skill** → downstream `pop-writer-v3-emerge`

## 产出

- `种子/`文件夹（活种子·核心卖点+六要素·_index.yaml+_log.md+分要素文件）
- 写作资产/文风库/{书名}.md
- 写作资产/设定库/（可选，复杂世界观才产出：世界宪法.md+力量体系.md+社会结构.md+角色档案/+卷纲路标/+_index.yaml）
- 活记忆/活记忆.yaml（baseline #0）
- 素材库/研究档案/种子展开图-{书名}.md（三界压力调研详情）
- 素材库/研究档案/交叉困境分析-{书名}.md（交叉困境详细分析，含同界/跨界标注）
