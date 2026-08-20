---
name: pop-decon-dimension
description: "当拆书时用户说'剧情线/情感线/人物/力量/世界观/爽点/文风'等维度词时启用。方案B维度拆解：联合Grep共享锚点池，单次精读多维提取，7维度合一。产出供给pop-decon-prd。"
---
# pop-decon-dimension · 维度拆解（方案B · 共享锚点池）

> 方案B 维度拆解 skill。7 个维度联合检索、共享精读：所有选中维度的检索词合并为一次 Grep，命中章去重形成联合锚点池，每章只读一次同时提取所有维度设定，最后分维度各自产出。v1.2.0

## 做什么

| 输入 | 来源 | 输出 | 下游 |
|:-----|:-----|:-----|:-----|
| 原文 `_temp/chapters/` + `dims=[维度列表]` + `scope=[章节范围]` | 原文（必）+ pop-decon 征询 | `设计/{维度}拆解-{范围}.md` × N | pop-decon-prd、创作参考 |

7 个维度联合检索、共享精读：所有选中维度的检索词合并为一次 Grep，命中章去重形成联合锚点池，每章只读一次同时提取所有维度设定，最后分维度各自产出。style 维度走场景定向采样，不参与联合 Grep 但共享精读章。

## 怎么操作

> execution.mode: 按维度参数驱动 | 强保障：本 SKILL.md 每次 run 强制注入 | 弱保障：steps/ + templates/ 需 agent 主动读取

| 步骤 | 操作 | 产出 | 门禁 | step 文件 |
|:-----|:-----|:-----|:-----|:----------|
| 1 | 预扫描 + 联合 Grep（所有选中维度检索词合并）→ 去重 → 联合锚点池 | 术语表 + 联合锚点池 | 命中≥20 锚点章 | `steps/step-1-grep-scan.md` |
| 2 | 分批精读联合锚点池（每批≤8章，每章多维提取）→ 分维度笔记 | 分维度抽取笔记 | 每条带 ch 证据 | `steps/step-2-precision-read.md` |
| 3 | 按维度分别产出（各填各的模板） | `设计/{维度}拆解-{范围}.md` × N | 结构完整+锚点覆盖 | `templates/{维度}.tpl.md` |
| 4 | 自检（各维度分别自检） | 自检报告 | 通过 | `references/output-quality-standards.md` |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **凭空发明内容** — 无 chXX 证据且未标注「原文未展开」的设定=编造
3. **前N章产出全书级文件** — 文件名不得含"全书"，必须有 scope 声明
4. **正文内联 chXX** — 正文中不得出现内联章节号，证据归表格列或段落末尾证据行
5. **量化数值丢失** — 关键数值必须用 🔒 标出，不得省略
6. **未确认维度就全跑** — 必须先由 pop-decon 征询确认维度，只跑被选中的
7. **单批精读超8章** — 精读锚点章时每批≤8章，超限强制拆批，避免子 agent 超时

## 速查表

| 我要 | 读/执行什么文件 | 什么时候用 |
|:-----|:----------|:----------|
| 执行 Grep 检索 | `steps/step-1-grep-scan.md` | Step 1 预扫描+检索时 |
| 执行精读+产出 | `steps/step-2-precision-read.md` | Step 2-4 精读+产出+自检时 |
| 查维度路由/检索词 | `references/维度路由清单.md` | Step 1 确认维度时 |
| 查质量门禁 | `references/output-quality-standards.md` | Step 4 自检时 |
| 查并行编排策略 | `pop-decon/references/delegation-orchestration.md` | 锚点章>8章需委派时 |
| 查小书策略 | `pop-decon/references/small-book-phase2-strategy.md` | 全书<100章时 |
| 查管线上下文 | `pop-decon/references/pipeline-context.md`（规范源） | 需要理解管线位置时 |
| 填剧情线模板 | `templates/plot.tpl.md` | 维度=剧情线时 |
| 填情感线模板 | `templates/romance.tpl.md` | 维度=情感线时 |
| 填人物模板 | `templates/character.tpl.md` | 维度=人物时 |
| 填力量模板 | `templates/power.tpl.md` | 维度=力量时 |
| 填世界观模板 | `templates/world.tpl.md` | 维度=世界观时 |
| 填爽点模板 | `templates/beat.tpl.md` | 维度=爽点时 |
| 填文风模板 | `templates/style.tpl.md` | 维度=文风时 |

## 强弱加载保障

- **强保障**：本 SKILL.md 由 host 层每次 run 强制注入，100% 到达 agent 上下文
- **弱保障**：`steps/`、`templates/`、`references/` 需 agent 按 SKILL.md 指引主动读取，天然弱保障
- **设计原则**：SKILL.md 假设模板/参考文件可能没被读到，SOP 骨架与断裂级红线必须自包含

## 版本

v1.2.0 | 2026-08-13 | 方案B 重构：从逐维度独立检索改为联合 Grep 共享锚点池；每章单次精读多维提取；分维度产出 → [CHANGELOG.md](CHANGELOG.md)

