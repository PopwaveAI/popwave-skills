---
name: tool-seo-anything
description: 当用户说"写一篇 SEO 文章""帮我优化这篇""生成可发布的博客""写教程/指南/对比/测评/FAQ""重写旧文""整理 SEO 元数据"时启用。从关键词/文章链接/选题方向出发，自动完成 SERP 调研→竞品分析→生成→双轮 QC→发布包，产出可直接发布的英文 SEO 文章。
version: 1.1.0
---

# SEO Article Automation v1.1.0

> **定位：** 一个关键词进来 → 一篇可直接发布的 SEO 文章出去。不是"写文章"，而是 7 阶段、双轮审核的自动化内容生产线。
>
> **默认输出：** 英文、可直接发布到网站的完整文章（含 title/meta/body/FAQ/SEO Pack）。不是思路，不是提纲。

---

## 速查表

| 步骤 | 操作 | 输入 | 产出 | 耗时 |
|:-----|:-----|:-----|:-----|:-----|
| Step 0 | Backlog 检查 | 主题/关键词 | `new_article` / `update_existing` / `needs_manual_decision` | ~30s |
| Step 1 | 任务识别 | keyword/URL/topic | 任务定义 + 文章类型 + 缺失信息清单 | ~1min |
| Step 2 | 关键词调研 | 主关键词+次要关键词 | 关键词清单 + 关键词矩阵 + 候选标题角度 | ~3min |
| Step 3 | SERP 竞品分析 | 主关键词 | 竞品摘要 + 内容缺口 + 选定框架 | ~5min |
| Step 4 | 证据收集 | 关键词+框架 | 可引用证据包 + 风险/待确认项 | ~3min |
| Step 5 | 生成框架 | 关键词+证据+竞品 | 可审阅框架 + 模块问题 + 证据放置建议 | ~2min |
| Step 6 | Draft v1 | 框架 | 完整可发布草稿 + 文中引用 | ~10min |
| Step 7 | Critique R1 | Draft v1 | `critical_bug` / `factual_risk` / `logic_break` 清单 | ~3min |
| Step 8 | Revision R1 | Critique R1 | 修复后版本 | ~5min |
| Step 9 | Critique R2 | 修订版 | 7维度 Scorecard（平均≥8.3） | ~3min |
| Step 10 | Final + SEO Pack | 终稿 | 完整发布包 | ~3min |

---

## 管线总览

```
输入（关键词/URL/选题方向）
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│  Stage 1: 调研层                                              │
│  ├── Step 0 Backlog 检查 — 避免重复覆盖                      │
│  ├── Step 1 任务识别 — 确定文章类型与发布目标                  │
│  ├── Step 2 关键词调研 — 关键词矩阵+意图分类                  │
│  ├── Step 3 SERP 分析 — 抓取Google真实SERPs+竞品结构分析      │
│  └── Step 4 证据收集 — 一手/第三方来源分层                    │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│  Stage 2: 生产层                                              │
│  ├── Step 5 框架 — 适配搜索意图的7模块结构                    │
│  ├── Step 6 Draft v1 — 完整可发布正文                         │
│  ├── Step 7  Critique R1 — 事实安全拦截                       │
│  ├── Step 8  Revision — 修复 critical_bug                     │
│  ├── Step 9  Critique R2 — 7维度评分拉至≥8.3                  │
│  └── Step 10 Final + SEO Pack — 终稿+发布包                   │
└──────────────────────────────────────────────────────────────┘
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│  Stage 3: 发布层                                              │
│  ├── Publish Gate — 10项检查                                  │
│  ├── Unified Scorecard — 7维度评分 （≥8.3通过）               │
│  └── 发布包 — title/slug/meta/body/FAQ/citations              │
└──────────────────────────────────────────────────────────────┘
```

---

## 核心流程

详细 SOP 请阅读对应步骤文件。每个步骤含完整操作指令、门禁条件和输出规范。

| Step | 文件 | 说明 |
|:-----|:-----|:-----|
| 0 | `steps/step-0-backlog.md` | Backlog 检查 — 去重校验 |
| 1 | `steps/step-1-task-identification.md` | 任务识别 — 输入分流与任务定义 |
| 2 | `steps/step-2-keyword-research.md` | 关键词调研 — 关键词矩阵 |
| 3 | `steps/step-3-serp-analysis.md` | SERP 竞品分析 — 竞品结构与框架选定 |
| 4 | `steps/step-4-evidence-collection.md` | 证据收集 — 一手/第三方素材分层 |
| 5 | `steps/step-5-framework-generation.md` | 框架生成 — 8模块结构 |
| 6 | `steps/step-6-draft-v1.md` | Draft v1 — 完整可发布正文 |
| 7 | `steps/step-7-critique-r1.md` | Critique R1 — 事实安全拦截 |
| 8 | `steps/step-8-revision-r1.md` | Revision R1 — 修复重大问题 |
| 9 | `steps/step-9-critique-r2.md` | Critique R2 — 7维度评分 |
| 10 | `steps/step-10-final-seo-pack.md` | Final + SEO Pack — 发布包组装 |

---

## 红线

| # | 红线 |
|:-:|:-----|
| 1 | 双轮审核（R1+R2）不可跳过。除非用户明确声明跳过 |
| 2 | `critical_bug` 未清零 → 不得交付 |
| 3 | 最终文章不可含过程痕迹（"Here is your draft"等） |
| 4 | 无可靠来源 → 不写具体数据或明确结论 |
| 5 | 禁止使用「—」破折号，用逗号/冒号/括号替代 |
| 6 | YMYL 内容（医疗/法律/金融）→ 默认增加人工确认环节 |

---

## Drop Check

交付前必须确认：

```
[ ] 双轮审核（R1+R2）已执行完毕
[ ] critical_bug/factual_risk/logic_break 均为 0
[ ] 7维度平均分 ≥ 8.3，seo_fitness ≥ 8.0
[ ] 文章无过程痕迹（Here is your draft / SEO-optimized 等）
[ ] 无「—」破折号
[ ] Publish Gate 10项全部 pass
```

任一项未通过 → 不可交付。

---

## WRONG 示例

### WRONG 1：单轮成稿直接交付
> ❌ 写文→输出，跳过 Critique R1+R2 双轮审核
> ✅ 默认启用多轮行为：写文→挑刺→修改→再挑刺→终稿。除非用户明确要求跳过。

### WRONG 2：最终文章暴露过程痕迹
> ❌ 文章里出现"Here is your draft"、"This article is SEO-optimized"
> ✅ 这些只允许出现在对用户的说明里，不允许混进文章正文

### WRONG 3：先给提纲再等回复再出正文
> ❌ 用户要求完整文章，Agent 先给 outline → 等回复 → 再给 body
> ✅ 除非用户明确要求展示过程，否则直接给完整发布包

### WRONG 4：在文章中使用「—」破折号
> ❌ "The tool — which is free — supports..."
> ✅ 用逗号或括号替代："The tool (which is free) supports..."

### WRONG 5：无来源支撑时仍写具体数据
> ❌ "Sales teams report 40-60% reduction in costs"（没来源）
> ✅ "Community discussions suggest potential time savings in routine tasks, though specific metrics are not independently verified"

---

## 异常与边界条件表

| 场景 | 处理 |
|:-----|:-----|
| **用户只给关键词，没给受众/地区/语气** | 按通用英文科技/内容站风格处理 |
| **用户要求"参考但不要照抄"** | 只吸收结构和信息，不复制表达 |
| **SERP 抓取工具不可用** | 回退用 WebSearch 获取 Google 结果 |
| **参考文章 URL 不可访问** | 要求用户提供原文或截图；不提供则暂停 |
| **工具数据冲突（ahrefs vs SERP 实际）** | 优先参考 SERP 实际结果和站点已有数据 |
| **Critic 与 Writer 评分差距 > 2.0** | 触发 Agent 3（Editor）仲裁 |
| **内容库不可用无法执行去重校验** | 明确说明"未执行去重校验" |
| **第一轮无 critical_bug 但有结构缺陷** | 在 R1 中一并标记，修复后再进 R2 |

---

## 阶段边界越界检测

| 边界场景 | 检测条件 | 处理 |
|:---------|:---------|:-----|
| Step 0 未执行就去调研 | 未输出 backlog 决策 | ❌ 退回 Step 0 |
| Step 3 SERP 未分析直接写框架 | 框架中无竞品参考 | ❌ 退回 Step 3 |
| R1 critical_bug 未清零进 R2 | critical_bug 列表非空 | ❌ 退回 Revision |
| R2 平均分 < 8.3 交付 | scorecard 平均分 < 8.3 | ❌ 退回 Revision |
| 最终文章含过程性文字 | 有 "Here is your draft" 等文字 | ❌ 退回清理 |
| YMYL 内容无人工确认标记 | 医疗/法律/金融无标记 | ❌ 添加"需人工确认"标记 |

---

## 落盘检查点

| 检查点 | 确认项 | 确认 |
|:-------|:-------|:-----|
| Step 0 Backlog | 已输出 `new_article` / `update_existing` / `needs_manual_decision` | [ ] |
| Step 2 关键词矩阵 | 已覆盖 5 类关键词 | [ ] |
| Step 3 SERP 分析 | 已阅读 SERP 结果并选定框架 | [ ] |
| Step 4 证据收集 | 已分层标记 first_party / third_party | [ ] |
| Step 6 Draft v1 | 完整正文，无占位符，无「—」破折号 | [ ] |
| Step 7 Critique R1 | critical_bug/factual_risk/logic_break 已标记 | [ ] |
| Step 8 Revision | 全部重大问题已修复 | [ ] |
| Step 9 Critique R2 | 7维度评分≥8.3，seo_fitness≥8.0 | [ ] |
| Step 10 Publish Gate | 10项检查全部 pass | [ ] |

---

## 关键差异化

| | 普通 AI 写作 | 本管线 |
|---|---|---|
| 调研 | 无 | 实时 SERP 抓取 + 5 个竞品深度读 |
| 事实核查 | 无 | 双轮自动化 QC + 来源审计 |
| SEO | 无 | 完整 SEO 包（meta/slug/FAQ/ALT/引用） |
| 输出 | 纯文本 | 品牌合规 HTML + 可视化 |
| 一致性 | 随机 | 7 维度评分卡，每篇文章打分 |

## 版本

v1.1.0 | 2026-06-14 | Tier C v5 结构重构：Steps 8-10 提取到 steps/ 目录，SKILL.md 瘦身至 ≤200 行，新增红线表+Drop Check。
