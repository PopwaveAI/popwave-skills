---
name: pop-writer-v3-seed
description: "v3涌现式种子设计。从creative复制重建，生态图谱→压力矩阵+冲突轴，金手指→种子金手指，文风DNA→种子文风DNA，PRD→种子组装。活种子初始化。"
pipeline:
  upstream: [pop-decon, pop-shared-dna]
  downstream: [pop-writer-v3-emerge]
  references: [pop-trope-library]
version: 1.0.0
---

# 种子设计（v3涌现式）

从 creative 复制重建，独立不耦合。4 步涌现式改造：生态图谱→压力矩阵+冲突轴、金手指→种子金手指、文风DNA→种子文风DNA、PRD→种子组装（主角引擎+成长路径+目的地）。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 文风DNA未锁定→硬阻塞 | 扫描写作资产/文风库/，空=终止 |
| ❌2 | 金手指必须含≥1个行动驱动机制 | 任务/技能/经验/血量/战宠 |
| ❌3 | 压力矩阵≥3压力源 | 替代creative的生态图谱≥3角色群 |
| ❌4 | 种子写驱动力不写设定清单 | 决策导向，非设定堆砌 |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-ecology-to-pressure.md | 生态图谱→压力矩阵+冲突轴 |
| step-2 | steps/step-2-golden-finger.md | 金手指行动引擎→种子金手指 |
| step-3 | steps/step-3-dna-lock.md | 文风DNA锁定→种子文风DNA |
| step-4 | steps/step-4-seed-assembly.md | 主角引擎+成长路径+目的地+种子组装+验证 |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 1 压力矩阵调研 | `references/种子搜索法SOP.md` | 制度性压迫维度调研标准流程 |
| Step 2 金手指设计 | `references/金手指设计指南.md` | 5维度行动引擎设计规范 |

## 路由

upstream `pop-decon` → **本skill** → downstream `pop-writer-v3-emerge`

## 产出

- 种子文档.md（活种子·七要素·含版本元数据+变更日志）
- 写作资产/文风库/{书名}.md
- 活记忆/活记忆.yaml（baseline #0）
