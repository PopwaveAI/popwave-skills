---
name: pop-writer-v3-seed
description: "v3.5涌现式初始设定设计。5步流程：step-0创意共创（元素融合+核心卖点+用户QA）→step-1委托pop-research调研→压力矩阵全量+冲突轴全量+研究档案→step-2金手指→写作参考/设定/金手指.md→step-3文风DNA蒸馏→step-4设定产出（主角引擎+核心卖点+活记忆baseline#0）；step-5维护SOP。六要素与用户逐步共创。v3.5取消种子文档，产出改为写作参考/设定/下的独立设定文件。活记忆改为自然语言格式。调研委托pop-research。"
pipeline:
  upstream: [pop-decon, pop-shared-dna]
  downstream: [pop-writer-v3-plot, expert-writer]
  references: [pop-trope-library, pop-research]
version: 1.6.0
---

# 初始设定设计（v3.5涌现式）

5步流程：创意共创→生态→压力→金手指→文风DNA→设定产出。step-0吸收creative最佳实践（元素融合+搜索SOP），在调研前与用户共创核心卖点和创作方向。六要素不是agent自己产出，是和用户逐步共创出来的——每步产出后强制用户QA确认。

v3.5核心变化：**取消种子文档**。L2剧情单元卡成为唯一运行时活文档。seed产出的六要素不再是种子文档的字段，而是写作参考/设定/下的独立设定文件。调研工作委托pop-research。活记忆改为自然语言段落格式。seed完成后进入plot环节，plot读取写作参考/设定/下的全局设定设计L2卡。

## ❌ 质量红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| ❌1 | 文风DNA未蒸馏→项目初始化终止 | 扫描写作资产/文风库/，空=终止 |
| ❌2 | 金手指必须含≥1个行动驱动机制 | 任务/技能/经验/血量/战宠 |
| ❌3 | 六要素必须经用户QA确认 | 每步产出后用户确认才进下一步 |
| ❌4 | 产出为写作参考/设定/下的独立文件 | 不再产出种子文档 |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-0 | steps/step-0-creative-co-creation.md | 创意共创（元素融合+核心卖点+用户QA） |
| step-1 | steps/step-1-ecology-to-pressure.md | 委托pop-research调研→压力矩阵全量+冲突轴全量+研究档案（用户QA确认） |
| step-2 | steps/step-2-golden-finger.md | 金手指行动引擎→写作参考/设定/金手指.md（用户QA确认） |
| step-3 | steps/step-3-dna-lock.md | 文风DNA蒸馏→文风库文件（项目资产）（用户QA确认） |
| step-4 | steps/step-4-setting-output.md | 主角引擎+核心卖点+活记忆baseline#0+设定验证（用户QA确认） |
| step-5 | steps/step-5-maintenance.md | 写作参考/设定/维护SOP（供下游调用参考） |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 2 金手指设计 | `references/金手指设计指南.md` | 5维度行动引擎设计规范 |

> 注：v3.5将种子搜索法SOP提取为独立skill（pop-research），seed不再内嵌调研SOP。step-1调用pop-research时传入书型+核心卖点，pop-research产出压力矩阵全量.md+研究档案。

## 路由

upstream `pop-decon` → **本skill** → downstream `pop-writer-v3-plot`/`expert-writer`

> seed完成后进入plot环节。plot读取写作参考/设定/下的全局设定，设计L2卡。

## 产出

seed产出的六要素不再是种子文档的字段，而是写作参考/设定/下的独立设定文件：

| 产出 | 路径 | 说明 |
|:-----|:-----|:-----|
| 主角引擎设定 | 写作参考/设定/主角引擎.md | 驱动力+行为准则 |
| 金手指设定 | 写作参考/设定/金手指.md | 能力+限制+行动驱动 |
| 压力矩阵全量 | 写作参考/设定/压力矩阵全量.md | 三界压力源+交叉困境 |
| 冲突轴全量 | 写作参考/设定/冲突轴全量.md | 四层生态+活跃线索 |
| 核心卖点 | 写作参考/设定/核心卖点.md | 一句话+核心爽点+情绪承诺 |
| 文风DNA | 写作资产/文风库/{书名}.md | 项目资产（不变） |
| 活记忆baseline#0 | 活记忆/活记忆.yaml | 初始状态（自然语言格式） |
| 研究档案 | 写作参考/知识沉淀/ | 种子展开图+交叉困境分析（pop-research产出） |
