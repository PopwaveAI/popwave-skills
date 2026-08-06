---
name: pop-decon-plot
description: "当拆书时用户说'剧情线/主线/支线/暗线/卷纲/转折'时启用。消费章节白描→产出剧情线拆解：故事机制DNA+主线/支线/暗线+卷纲+转折点+核心矛盾链。"
---
# pop-decon-plot · 剧情线拆解

> 拆书独立维度 skill。从章节白描拆解剧情线：故事机制DNA + 主线/支线/暗线 + 卷纲 + 转折 + 核心矛盾链。v1.0.0

## 做什么

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 章节白描（必） | pop-decon-design-pack | `设计/故事机制DNA-卷N.md`、`设计/卷纲/卷N-卷纲.md` | pop-decon-character、pop-decon-beat、pop-decon-prd |

## 怎么操作

> execution.mode: 串行 | 强保障：本 SKILL.md 每次 run 强制注入 | 弱保障：steps/ 需 agent 主动读取

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 1 | 故事机制DNA | `故事机制DNA-卷N.md` | 有效事件清单有原文证据 | `steps/step-1-story-dna.md` |
| 2 | 主线/支线/暗线 | `剧情线-主线支线暗线.md` | 每条线有起始/激化/收束章 | `steps/step-2-plot-lines.md` |
| 3 | 卷纲归纳 | `卷纲/卷N-卷纲.md` | 幕序列含故事DNA映射 | `steps/step-3-volume-outline.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **无白描就拆** — 必须先有章节白描，剧情线不得直接读原文
3. **有效事件清单无原文证据** — 每条必须标注chXX原文来源，不得编造
4. **卷纲从故事DNA逆向归纳** — 不得跳过故事DNA直接从原文推导
5. **剧情梗概到场景级** — 不得概括为"主角变强了"，必须是"主角做了什么具体事件"

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-story-dna.md` | Step 1 | 故事机制DNA两层结构提取 |
| `steps/step-2-plot-lines.md` | Step 2 | 主线/支线/暗线拆解 |
| `steps/step-3-volume-outline.md` | Step 3 | 卷纲逆向归纳 |
| `references/pipeline-context.md` | 需要管线上下文时 | 维度skill在拆书体系的位置 |

## 版本

v1.0.0 | 2026-08-06 | 新建：剧情线独立拆解维度 skill，从 pop-decon-volume 拆分 → [CHANGELOG.md](CHANGELOG.md)