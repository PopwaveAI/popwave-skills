---
name: pop-decon-romance
description: "当拆书时用户说'情感线/感情线/CP/暧昧/信任/背叛/羁绊演变'时启用。消费章节白描→产出情感线拆解：CP关系网+暧昧/信任/背叛节点+羁绊演变时间线。"
---
# pop-decon-romance · 情感线拆解

> 拆书独立维度 skill。从章节白描拆解情感线：CP关系 + 暧昧/信任/背叛/羁绊演变。v1.0.0

## 做什么

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 章节白描（必）+ 剧情线（可选） | pop-decon-design-pack / pop-decon-plot | `设计/情感线-{卷N}.md` | pop-decon-prd、创作参考 |

## 怎么操作

> execution.mode: 串行 | 强保障：本 SKILL.md 每次 run 强制注入 | 弱保障：steps/ 需 agent 主动读取

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 1 | 情感关系网 | `情感关系网` | 每个角色有原文chXX证据 | `steps/step-1-relationship-map.md` |
| 2 | CP线拆解 | `CP线` | 暧昧/信任/背叛节点有因果链 | `steps/step-2-cp-line.md` |
| 3 | 羁绊演变时间线 | `羁绊演变` | 覆盖起点→终点，标注转折事件 | `steps/step-3-bond-evolution.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **无白描就拆** — 必须先有章节白描，情感线拆解不得直接读原文
3. **情感节点无因果** — 每个暧昧/信任/背叛/羁绊节点必须标注触发事件chXX，不得只写"感情升温"
4. **凭空推断角色动机** — 情感动机必须基于白描/原文证据，不得编造角色内心
5. **情感线≠剧情线** — 聚焦关系演变与情感张力，不展开主线剧情分析

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-relationship-map.md` | Step 1 | 情感关系网拆解 |
| `steps/step-2-cp-line.md` | Step 2 | CP线暧昧/信任/背叛节点 |
| `steps/step-3-bond-evolution.md` | Step 3 | 羁绊演变时间线 |
| `references/pipeline-context.md` | 需要管线上下文时 | 维度skill在拆书体系的位置 |

## 版本

v1.0.0 | 2026-08-06 | 新建：情感线独立拆解维度 skill → [CHANGELOG.md](CHANGELOG.md)