---
name: pop-decon-style
description: "当拆书时用户说'文风/对白/笔触/风格/文风DNA'时启用。消费章节白描+原文→产出文风拆解：文风DNA档案，复用文风DNA蒸馏方法论。"
---
# pop-decon-style · 文风拆解

> 拆书独立维度 skill。从章节白描+原文拆解文风：文风DNA档案，复用文风DNA蒸馏方法论。v1.1.0

## 做什么

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 章节白描（必）+ 原文采样 | pop-decon-design-pack / `_temp/chapters/` | `设计/文风DNA档案.md` | pop-decon-prd |

## 怎么操作

> execution.mode: 串行 | 强保障：本 SKILL.md 每次 run 强制注入 | 弱保障：steps/ 需 agent 主动读取

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 1 | 原文采样 | `文风采样` | 采样≥500字原文引用 | `steps/step-1-sampling.md` |
| 2 | 文风DNA提取 | `文风DNA档案` | 笔触层各维度有原文证据 | `steps/step-2-dna-extract.md` |
| 3 | 对白风格提炼 | `对白风格` | 逐字摘录原文对白 | `steps/step-3-dialogue.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具；文风拆解需读原文，原文存在性必须优先验证
2. **无白描就拆** — 必须先有章节白描，文风拆解不得跳过白描
3. **采样无原文引用** — 文风DNA必须基于≥500字原文引用，不得凭空描述
4. **只摘笔触层** — 只提取句法结构/叙事距离/感官序列/信息释放节奏，丢弃世界观专属要素
5. **对白风格凭空描述** — 对白风格必须逐字摘录原文，不得概括"他说话很酷"

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-sampling.md` | Step 1 | 原文采样方法 |
| `steps/step-2-dna-extract.md` | Step 2 | 文风DNA提取 |
| `steps/step-3-dialogue.md` | Step 3 | 对白风格提炼 |
| `references/pipeline-context.md` | 需要管线上下文时 | 维度skill在拆书体系的位置 |
| `pop-dna-style/references/methodology.md` | 需要方法论时 | 文风DNA蒸馏方法论 |
| `pop-dna-style/references/style-dna-profile.md` | 需要模板时 | 精简模板（操作特征+精选原文+场景卡矩阵） |

## 版本

v1.1.0 | 2026-08-13 | skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步 → [CHANGELOG.md](CHANGELOG.md)