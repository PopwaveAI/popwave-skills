---
name: pop-decon
description: 拆书专家入口。当用户说'拆书/解构/分析/对标/提取模板'时启用。下载txt→征询范围→路由单书深度wiki拆解(dimension)→沉淀。不常驻调度。
---

# pop-decon · 拆书专家入口

> 拆书专家入口：下载 txt → 征询范围 → 路由 `pop-decon-dimension`（单书深度wiki拆解）→ 沉淀。不常驻调度。当前版本 v26.1.0，完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

## 做什么

| 输入 | 输出 | 下游 |
|:--|:--|:--|
| 用户拆书需求 + 源文件 | 征询范围 + 路由到 dimension（传范围+书信息） | pop-decon-dimension（单书深度wiki拆解） |

**执行模式**：主 agent 直执——下载/征询/路由/沉淀均为交互编排环节，无自然子 agent 适配点；拆解整体路由给 pop-decon-dimension。

**路由地图**：下载txt → ★征询范围★ → 路由 dimension（范围）→ L1批次拆解→L2六模块成品 → 沉淀 + 提醒少测

## 怎么操作（SOP全内联）

> execution.mode: 按需路由 | 强保障：本 SKILL.md 每次 run 强制注入

### Step 0：源文件检查 + 下载

| 情况 | 动作 |
|:--|:--|
| 用户已提供路径（TXT/EPUB/PDF） | 确认存在 → 进 Step 1 |
| 未提供文件 | 路由 `tool-download-webnovel` 下载 → 进 Step 1 |
| 说"网上有"但无 URL | 搜索 `{书名} txt 下载` 找 URL 后交 tool-download-webnovel |

**门禁**：无源文件且未完成下载不得进 Step 1（下载失败处理见红线 5）。

### Step 1：征询范围（强制，禁止默认全量跑）

| 范围选项 | 说明 |
|:--|:--|
| 全书 | 全量拆解 → 六模块深度wiki |
| 某一卷 / 前N章 | 指定范围拆解（产出该范围对应的模块/切片） |

征询话术：「老板，这本《{书名}》要拆多大范围？（全书 / 某一卷给章节范围 / 前N章给N）产出对齐《深渊主宰》重建标准——**六模块深度wiki成品**（剧情库分卷/角色与势力库/力量与战斗/世界观/赛道特色/文风DNA）。范围确定后即按 L1批次拆解→L2成品整合推进。」

**门禁**：用户未明确选择范围 → 退回征询，不得擅自开始拆解。

### Step 2：路由到主拆解

范围传入 `pop-decon-dimension`（单书深度wiki拆解），由其承载 L1 批次拆解（硬门禁）+ L2 六模块成品整合。产出前 dimension 自行征询「先样板验收再铺 / 一步到位铺全」。

### Step 3：沉淀 + 提醒少测

全部分解完成后，确认六模块成品已沉淀到 `{书名}/` 目录并更新索引。原子候选由 dimension Step 8 自动归集入库 `剧情周期表/`，入口不重复处理。未指定项目时询问沉淀到哪个项目；完成后告知用户产出已沉淀。

## 🚪 首次对话引导（onboarding）

首次触发（无拆书项目、非续写）时，先直接粘贴 `references/onboarding-guide.md` 全文（声明为功能介绍+引导、未执行任务），补一句"报书名+想学那块就开始"；用户已明确要拆则跳过。

## 📦 可调度 Skill 清单

`tool-download-webnovel`（下载txt）/ `pop-decon-dimension`（单书深度wiki拆解·L1批次拆解+L2六模块成品）

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **未征询就全量跑** — 必须先征询范围，只拆所选范围，禁止默认全量跑
3. **跳过原文直读** — 拆书必须走 L1 批次拆解（直读原文）再进 L2 成品，禁止无证据直接写成品
4. 产出物不经质量门禁直接交付 — L1 批次硬门禁不过关不得进 L2（见 dimension）
5. 无源文件先路由 tool-download-webnovel 下载，不得跳过；换源全失败 → 终止告知，不得空文件硬跑
6. 产出沉淀到 `{书名}/` 六模块目录，不入库 pop-trope-library
7. **未提醒少测即切入全书** — 拆书启动或完成时必须提醒用户"本拆解服务较耗算力，建议先用一卷/前N章少量测试，确认效果后再拓展到全书"

## 速查表（外部文件）

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `references/pipeline-context.md` | 需要管线上下文时 | 管线位置与前置条件 |
| `references/onboarding-guide.md` | 首次对话引导时 | 引导语全文 |
| `references/维度路由清单.md` | 征询范围后 | 模块检索词路由 |
| `references/output-quality-standards.md` | 路由前 | 双层质量门禁速览 |

## 版本

当前版本 v26.1.0。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。