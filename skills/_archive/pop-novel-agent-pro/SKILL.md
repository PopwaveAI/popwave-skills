---
name: novel-agent-pro
description: 全链路网文创作系统，包含拆书/开书/剧情架构/正文写作/QC质检/HTML发布等完整管线。Invoke when user wants to write a novel from scratch or needs full writing pipeline support.
version: 3.3.0
---

# novel-agent-pro — 子Skill 索引总纲

> 版本：**v4.2** · 更新：2026-06-03
> 用途：agent 路由索引。收到"写章节/拆书/开书"等任务 → 查此文件的模块划分 → 确定子 Skill 路径。

---

## 一、管线总览（六阶段 · 14 项输入包）

```
Phase 0: 提前完成的设定（开书阶段— project-bootstrap）
  └── 拆解报告 / 设定层 / 大纲层校准
  └── Boss设计 + 数值体系 + 锚定章库 + 经验日志
        │ reader_profile 穿透全管线
        ▼
Phase 1: Director Agent → 设计说明 + 决策日志 → ⭐ 大纲层QC
Phase 2: Pass 1 骨架 Agent → 事实骨架 → ⭐ 骨架层QC
Phase 3: ESM before（零LLM·14项输入包）→ bundle.md
Phase 4: Pass 2 渲染 + 写后自评 → 正文 chXXX.md
Phase 5: ⭐ QC Agent · 三层介入（大纲/骨架/正文）
Phase 6: ESM after（零LLM）→ state_changelog + 全局摘要
```

---

## 二、模块划分（按流水线）

收到用户请求时，根据关键词路由到对应子 Skill。

### 调研层
| 子 Skill | 路径 | 关键词 |
|:---------|:-----|:-------|
| cnovel-research | `skills/cnovel-research/` | 调研、搜索、研究 |
| book-opinion-tracker | `skills/book-opinion-tracker/` | 舆情、书评、口碑 |

### 开书启动
| 子 Skill | 路径 | 版本 |
|:---------|:-----|:-----|
| project-bootstrap | `skills/skill-project-bootstrap/` | v2.9 |
| book-deconstructor | `skills/skill-book-deconstructor/` | v4.8 |

### 剧情设计
| 子 Skill | 路径 | 版本 |
|:---------|:-----|:-----|
| plot-architecture | `skills/skill-plot-architecture/` | v2.7 |
| opening-arc | `skills/skill-opening-arc/` | v1.1 |

### 正文写作（★ 核心）
| 子 Skill | 路径 | 版本 |
|:---------|:-----|:-----|
| emergent-writer | `skills/skill-emergent-writer/` | v9.3 · 六阶段管线 |

### 质检与发布
| 子 Skill | 路径 | 版本 |
|:---------|:-----|:-----|
| qa-payoff | `skills/skill-qa-payoff/` | v0.4.1 |
| html-renderer | `skills/skill-emergent-writer/html-renderer/` | v1.3 |

### 其他
| 子 Skill | 路径 | 版本 |
|:---------|:-----|:-----|
| market-test | `skills/skill-market-test/` | v1.2 |
| _continuation | `skills/_continuation/` | 续写适配 |
| horror-game-writer | `skills/skill-horror-game-writer/` | — |

---

## 三、全流程贯通

```
Step 1: 拆书（book-deconstructor）→ 拆解报告 + 锚定章库
Step 2: 开书（project-bootstrap）→ L0-L1设定 + reader_profile + 数值体系
Step 3: 黄金三章（opening-arc）→ ch001-ch003
Step 4: 幕纲设计（plot-architecture）→ act-XX.yaml
Step 5: 正文循环（emergent-writer）→ Director → 骨架 → ESM → 渲染 → QC → 状态更新
```

## 四、版本

各模块详细版本、链路审计、胶水代码方案 → 参见 `references/`
