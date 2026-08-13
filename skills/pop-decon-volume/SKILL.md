---
name: pop-decon-volume
description: "当用户说'聚类/卷幕/cluster'时启用。从叙事白描产出故事机制DNA+名场面库+读者体验曲线+卷纲，产出供下游setting/prd消费。"
---

# pop-decon-volume · 叙事结构与故事DNA提取

> Phase 2 of 拆书管线。从叙事白描产出故事机制DNA+名场面库+读者体验曲线+卷纲。v8.1.0

## 做什么

| 输入 | 输出 | 下游 |
|:-----|:-----|:-----|
| 叙事白描 + Phase 1设计包 | 故事机制DNA + 名场面库 + 读者体验曲线 + 卷纲 | pop-decon-setting, pop-decon-prd |

## 怎么操作

> execution.mode: 串行 | 强保障：本 SKILL.md 由 host 层每次 run 强制注入 | 弱保障：steps/ + references/ 需 agent 主动 readFile

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 0 | 叙事白描 | 叙事白描.md | 因果链完整+卷末钩子 | `steps/step-0-叙事白描.md` |
| 1 | 故事机制DNA提取 | 故事机制DNA-卷N.md | 有效事件清单有原文证据 | `steps/step-1-story-dna.md` |
| 2 | 名场面深度拆解 | 名场面库.md | 叙事式拆解有原文锚点 | `steps/step-2-iconic-scenes.md` |
| 3 | 读者体验曲线 | 读者体验曲线-卷N.md | 爽点分布覆盖全部章节 | `steps/step-3-reader-experience.md` |
| 4 | 卷纲精简+入库 | 卷纲/卷N-卷纲.md | 幕序列含故事DNA映射 | `steps/step-4-volume-outline.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **故事DNA有效事件清单必须有原文证据** — 每条必须标注chXX原文来源，不得编造
3. **名场面叙事式拆解不拆表格** — 产出是自然叙事文，前置铺垫必须标注chXX，爽感必须点出公式
4. **卷纲从故事DNA逆向归纳** — 不得跳过故事DNA直接从原文推导
5. **不编造溯源来源** — 已删除溯源燃料台，不得在其他模块恢复溯源猜测

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-0-叙事白描.md` | 将白描卡串联为叙事白描时 | 叙事白描流程 |
| `steps/step-1-story-dna.md` | 提取故事机制DNA时 | 两层结构提取流程 |
| `steps/step-2-iconic-scenes.md` | 拆解名场面时 | 叙事式拆解流程 |
| `steps/step-3-reader-experience.md` | 提取读者体验曲线时 | 爽点分布+情绪曲线+信息释放 |
| `steps/step-4-volume-outline.md` | 归纳卷纲时 | 卷纲精简+入库流程 |
| `references/pipeline-context.md` | 理解Phase间消费关系时 | 管线上下文 |
| `references/跨卷边界处理.md` | 多卷拆解时 | 跨卷边界处理 |
| `templates/故事机制DNA.tpl.md` | 产出故事DNA时 | 故事DNA模板 |
| `templates/名场面库.tpl.md` | 产出名场面库时 | 名场面库模板 |
| `templates/读者体验曲线.tpl.md` | 产出读者体验曲线时 | 读者体验曲线模板 |
| `templates/卷纲-拆书版.tpl.md` | 产出卷纲时 | 精简卷纲模板 |

## 版本

v8.1.0 | 2026-08-13 | skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步 → [CHANGELOG.md](CHANGELOG.md)
