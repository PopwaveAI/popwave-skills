---
name: novel-agent-pro
description: 全链路网文创作系统，包含拆书/开书/剧情架构/正文写作(emergent-writer v9.3)/QC质检/HTML发布等完整管线。Invoke when user wants to write a novel from scratch, continue a book, or needs full writing pipeline support.
version: 3.3.0
---

# SKILL — novel-agent-pro 子Skill 索引总纲

> 版本：**v4.2** · 更新：2026-05-26
> 用途：**Agent 索引文件**。查找各子 Skill 的路径、职责、版本、调用方式。
>
> Agent 在收到"写章节/拆书/质检/开书"等任务时 → 读取此文件的"模块划分"和"各模块详细描述" → 确定子 Skill 路径和调用入口。
>
> **版本矩阵和版本历史请查 `VERSION.md` 和 `CHANGELOG.md`**

---

## 目录

- [一、项目定位](#一项目定位)
- [二、模块划分（按写作流水线）](#二模块划分按写作流水线)
- [三、各模块详细描述](#三各模块详细描述)
- [四、全流程贯通检查](#四全流程贯通检查)
- [五、链路审计](#五链路审计)
- [六、胶水代码方案](#六胶水代码方案)
- [七、已接入项目一览](#七已接入项目一览)

---

## 一、项目定位

**novel-agent-pro** 是一套全链路网文 AI 创作引擎，基于 WorkBuddy 平台运行。  
已实战验证的项目：渊界V3、灰骑士之主、诡异游戏v2、诡异人生v2、海贼法典。

### Spec 模式深度整合（v4.0 — 2026-05-31）

本系统已深度整合 **Spec 模式**——一种"先规格后实现"的结构化开发/写作范式。

**核心理念**：在 AI 动手之前，先把"对的事"定义清楚；在 AI 完成之后，用"可判定的标准"验证它做对了。

**新增 spec-bridge 桥接层**：位于 POP-ROUTER 和 dispatcher 之间，生成三文件（spec.md / tasks.md / checklist.md），经人工审批后贯穿六阶段管线。详情见 `spec-bridge/SKILL.md`。

```
用户需求 → [spec-bridge ★] → 审批闸门 → dispatcher → six-stage pipeline → checklist 验证
              ├─ spec.md        → 为什么写、写什么、不写什么
              ├─ tasks.md       → 按什么顺序写、依赖什么
              └─ checklist.md   → 写到什么程度才算完成
```

### v3.3 最终管线（六阶段 · 14 项输入包）

```
Phase 0 · 提前完成的设定（开书阶段）：
  └── 读 拆解报告/ → 设定层/大纲层校准基准
  └── Boss设计（超越性检查）+ 数值体系（敌我映射+幕级时间表）
  └── 锚定章片段库 + 角色行为锚定 + 经验日志

        │ reader_profile 穿透全管线
        ▼

Phase 1 · Director Agent（设计说明 + 决策日志）
  → 锚定章引用 + 字数目标 + 爽点触发方式 + 描写密度指南
  → ⭐ 大纲层 QC → 通过才进入下一阶段

Phase 2 · Pass 1 骨架 Agent（事实骨架 + 预估字数）
  → {实体名} ≥ 8 + 预估字数 ≥ 1800
  → ⭐ 骨架层 QC → 通过才渲染

Phase 3 · ESM before（零LLM · 14 项输入包）
  第0项: reader_profile（new）
  第1-5: SQLite 固定查询
  第6-8: 骨架推断 + 文件加载
  第9项: Director 决策日志（含锚定引用）
  第10项: 锚定章片段（new — 从库中加载）
  第11项: 场景模板
  第12项: K1-K4 知识注入
  第13项: 经验日志匹配（new — scene_type 自动匹配）
  第14项: 上轮 QC 反馈
  → bundle.md

Phase 4 · Pass 2 渲染 + 写后自评
  → 正文 chXXX.md
  → 自评: "差在哪？补一段核心缺失（不重写）"

Phase 5 · ⭐ QC Agent · 三层介入
  大纲层 QC: "这幕计划想翻吗？" → 退回 Director
  骨架层 QC: "信息量够撑一章吗？" → 退回 Pass 1
  正文层 QC: "读完了还是刷过去了？会弃书吗？" → 退回 Pass 2

Phase 6 · ESM after（零LLM）
  → SQLite state_changelog + 全局摘要追加
  → 如有 QC 红线 → 追加经验日志
```

---

## 二、模块划分（按写作流水线）

```
★ 规格层（v4.0 新增）：
  spec-bridge v1.0（Spec 桥接层 — "先规格后实现"）
  ├── 生成 spec.md（需求规格 — Goals/Non-Goals/Requirements/AC）
  ├── 生成 tasks.md（任务分解 — 依赖关系）
  ├── 生成 checklist.md（验证清单 — 可判定通过条件）
  └── 审批闸门 — spec 未审批不进入实现

调研层：
  cnovel-research v1.3 / book-opinion-tracker v1.7 / web-access v2.4

开书启动：
  project-bootstrap v2.8（reader_profile + 数值体系 + 超越性检查）
  └── 消费拆解报告: book-deconstructor v4.8 的模式D+E

拆书素材：
  book-deconstructor v4.8（场景/体系/大纲密度 五模式）
  └── 产出: 01-写作资产/拆解报告/ + 锚定章库/

剧情设计：
  plot-architecture v2.7（事件数≥3/章 + scene_type 多样性 + 字数基线）

正文写作：
  emergent-writer v9.2 · 六阶段管线 · 14 项输入包
  ├── [spec 注入] Director Agent（决策日志 + spec 约束响应）
  ├── [spec 注入] Pass 1 · 骨架 Agent（spec 合规检查）
  ├── [spec 注入] ESM before（零LLM · 14+1 项输入包 — +spec.md）
  ├── [spec 注入] Pass 2 · 渲染 Agent（写后自评 + AC 对照）
  ├── [spec 注入] QC Agent · 三层介入（纯感受 + spec 合规备注）
  └── [spec 注入] ESM after（零LLM · 双写 + checklist 更新）

质检：
  qa-payoff v0.4.1（纯感受报告 · 三层介入）
  └── [spec 可选] 增加 spec 合规备注层
  emergent-writer 内嵌 autocheck（字数/否定句/钩子自动化检查）

发布：
  html-renderer v1.3（HTML化发布）
```

---

## 三、各模块详细描述

### 模块A：基础设施层

#### A1. web-access v2.4.3

| 项 | 说明 |
|:---|:------|
| **职责** | 所有联网操作的唯一入口 |
| **能力** | WebSearch、WebFetch、curl、Chrome CDP（登录态操作）、Jina预处理 |
| **胶水需求** | ⚪ 无——独立工具箱 |

#### A2. cnovel-research v1.3.0 / book-opinion-tracker v1.7

| 项 | 说明 |
|:---|:------|
| **职责** | 覆盖12+平台的作者社区调研 + 舆情追踪 + 小说正文抓取 |
| **胶水需求** | ⚪ 无 |

---

### 模块B：开书启动层

#### B1. project-bootstrap v2.8

| 项 | 说明 |
|:---|:------|
| **职责** | 从"一个想法"到可执行项目骨架 |
| **核心升级（v2.8）** | reader_profile 嵌入 project.yaml、数值体系模板升级（combat_capability/monster_rank_map/act_rank_schedule）、超越性硬检查 |
| **产出自定义** | 01-写作资产/拆解报告/（消费 book-deconstructor 模式D+E） |
| **胶水需求** | 🔗 Prompt约定 — 产出路径在不同项目中不一致 |

---

### 模块C：拆书与素材层

#### C1. book-deconstructor v4.8

| 项 | 说明 |
|:---|:------|
| **职责** | 将参考书拆解为可复用的写法规则、体系设计逻辑、大纲密度基线 |
| **五模式** | A节奏地图 / B对标拆解 / C主题定向 / **D体系拆解(新增)** / **E大纲密度拆解(新增)** |
| **产出物位置** | 01-写作资产/拆解报告/（统一） |
| **胶水需求** | 🔗🔗🔗 脚本约束 — DB写入（唯一一条脚本硬链） |

#### C2. 锚定章片段库

| 项 | 说明 |
|:---|:------|
| **位置** | 01-写作资产/锚定章库/ |
| **使用** | Director 选中 + ESM before 按引用加载 |
| **胶水需求** | ⚪ 手动提取 3-5 个片段即可 |

---

### 模块D：剧情设计层

#### D1. plot-architecture v2.7

| 项 | 说明 |
|:---|:------|
| **职责** | 全书→卷→幕的爽点分布设计 |
| **v2.7 新增** | 事件数基准（≥3/章）、scene_type 多样性（同类型≤2章连续）、字数基线（2000-2500） |
| **输出** | 02-大纲/卷XX/act-XX.yaml（含 fun_level / scene_time / event_density 字段） |
| **胶水需求** | 🔗🔗 格式契约 — act-XX.schema.yaml |

---

### 模块E：正文写作层

#### E1. emergent-writer v9.2（★ 核心引擎）

| 项 | 说明 |
|:---|:------|
| **版本** | **v9.2** · 六阶段管线 · v3.3 |
| **架构** | Director(1次LLM) → 大纲层QC → Pass 1(1次LLM) → 骨架层QC → ESM before(零LLM) → Pass 2(1次LLM+自评) → 正文层QC → ESM after(零LLM) |
| **数据层** | v3.db（characters/weirds/skills/items + relationships + state_changelog） |
| **脚本集** | `main.py`（CLI · 含 autocheck）、`loader.py`、`updater.py`、`validator.py` |
| **模板集** | Director-prompt / Pass1-chapter-planner / Pass2-renderer / QC-checklist / experience-log-schema / global-summary-schema |
| **知识注入** | K1核心理论 / K2平台画像 / K3量化基准 / K4题材感知 |
| **v3.3 升级** | ① reader_profile 全管线穿透 ② 锚定章注入 ③ 写后自评 ④ QC 三层介入 ⑤ autocheck 自动化检查 ⑥ 经验日志结构化匹配 |
| **依赖** | project.yaml、v3.db、01-写作资产/锚定章库/、拆解报告/ |
| **旧项目兼容** | 省略 `--db-path` 自动降级 YAML 实体卡模式 |
| **胶水需求** | 🔗🔗 格式契约 — 事实骨架格式（{实体名}标记 + 场景权重 + 导演设计说明） |

---

### 模块F：质检层

#### F1. qa-payoff v0.4.1

| 项 | 说明 |
|:---|:------|
| **职责** | 针对正文的纯感受型质检 |
| **哲学** | 不评分、不提修改建议、不规律验证——只回答"我读的时候怎么了" |
| **三层介入** | 大纲层 QC（Director输出后，骨架前）/ 骨架层 QC（骨架输出后，渲染前）/ 正文层 QC（渲染+自评后，ESM after前） |
| **触发条件** | reader_profile 从 project.yaml 读入 |
| **产出** | 纯感受报告（不包含评分/建议） |
| **红线** | "想跳过"≥2处 或 "会弃书"=是 → 退回 Pass 2 重写 |
| **胶水需求** | ⚪ 独立子Agent调用 |

#### F2. autocheck（内嵌 emergent-writer v9.2）

| 项 | 说明 |
|:---|:------|
| **职责** | 字数/否定句/钩子 自动化检查 |
| **CLI** | `python main.py autocheck <章号> --project <路径>` |
| **胶水需求** | ⚪ 内嵌于 main.py |

---

### 模块G：市场验证层

#### G1. market-test v1.2

| 项 | 说明 |
|:---|:------|
| **职责** | 发书前最后一道市场防线 |
| **胶水需求** | ⚪ 无 |

---

### 模块H：发布层

#### H1. html-renderer v1.3

| 项 | 说明 |
|:---|:------|
| **职责** | HTML化发布引擎。27套html-anything SKILL融合 |
| **胶水需求** | ⚪ 无 |

---

## 四、全流程贯通检查

### 4.1 v3.3 全链路

```
Step 1: 拆书（book-deconstructor v4.8）
  → 产出：拆解报告/ + 锚定章库/
  → 消费：project-bootstrap 开书时校准设计基准

Step 2: 开书启动（project-bootstrap v2.8）
  → 产出：L0-L1设定、reader_profile、数值体系、project.yaml
  → 粘合：→ plot-architecture

Step 3: 黄金三章（opening-arc v1.1）
  → 产出：ch001-ch003 正文

Step 4: 幕纲设计（plot-architecture v2.7）
  → 产出：act-XX.yaml (含 event_count / scene_type / 字数基线)
  → 依赖：project.yaml、PRD.md、L1元设定层
  → 胶水：glue/validate.py → 校验 act-XX.yaml schema

Step 5: 正文写作循环（emergent-writer v9.2）
  → Director → 大纲层QC → 骨架 → 骨架层QC
  → ESM before → 14项输入包
  → Pass 2 + 写后自评 → 正文层QC
  → ESM after → state_changelog + 全局摘要
  → 依赖：v3.db、拆解报告/、锚定章库/、experience-log
  → 胶水：ESM CLI（main.py before/after/autocheck）
```

### 4.2 引用强度矩阵

| 模块A → 模块B | 强度 | 保障方式 |
|:---|:---:|:---:|
| fragment-pipeline → scene_fragments.db | 🔗🔗🔗 | 脚本写DB（唯一硬链） |
| plot-arch → emergent-writer | 🔗🔗 | act-XX.schema.yaml + v3.db |
| emergent-writer → 事实骨架 | 🔗🔗 | 骨架格式约定（{实体名}标记） |
| ESM before → v3.db | 🔗🔗 | 5条固定SQL（零LLM） |
| ESM after → v3.db | 🔗🔗 | INSERT + UPDATE 写回 |
| bootstrap → plot-arch | 🔗 | Prompt约定 |
| bootstrap → market-test | 🔗 | Prompt约定（可选降级） |
| Director → 锚定章库 | 🔗 | Director 引用 + ESM before 加载 |

---

## 五、链路审计

### 5.1 已处理（v3.3 清理）

| 清理项 | 原因 | 状态 |
|:-------|:-----|:----:|
| `skill测试区/` (~200+文件) | 非管线，测试内容 | ✅ 已删 |
| `_archive/` (~20文件) | 旧版引擎/脚本 | ✅ 已删 |
| `skill-novel-pipeline/` | emergent-writer 的旧版重复 | ✅ 已删 |
| `skill-chapter-outline/` | 已废弃 | ✅ 已删 |
| `skill-qc/` | 被 qa-payoff 取代 | ✅ 已删 |
| `_abandoned/skill-reader-qa/` | 已废弃 | ✅ 已删 |
| emergent-writer 内部冗余目录 | prompt-templates 已有 | ✅ 已删 |
| 全局 `__pycache__/` | 编译缓存 | ✅ 已删 |
| `VIBE_CREATING_PRD.md` | 死跳转，指向内容已清理 | ✅ 已删 |
| `skills/skill-mapping.yaml` + `sync.ps1` + `sync.sh` | 不再使用 | ✅ 已删 |

### 5.2 待定

| 文件 | 状态 | 建议 |
|:-----|:-----|:-----|
| `glue/schemas/chXXX.schema.yaml` | ⚠️ 保留 | 历史参考 |
| `glue/schemas/writer-metadata.schema.yaml` | ⚠️ 保留 | 历史参考 |
| `glue/orchestrate.py` | ⚠️ 保留 | 功能不完整，未来可能淘汰 |

---

## 六、胶水代码方案

### 6.1 ESM CLI（v3.3 升级）

| 命令 | 作用 | 零LLM |
|:-----|:-----|:------:|
| `main.py before` | 构建14项输入包（reader_profile 第0项 + 锚定章 + 经验日志匹配） | ✅ |
| `main.py after` | SQLite state_changelog + 全局摘要追加 | ✅ |
| `main.py autocheck` | 字数/否定句/钩子自动化检查 | ✅ |
| `main.py list` | 列出实体清单 | ✅ |
| `main.py validate` | 一致性校验 | ✅ |
| `main.py check-refs` | 引用覆盖率 | ✅ |

### 6.2 glue 脚本

| 脚本 | 作用 | 零LLM | 状态 |
|:-----|:-----|:-----:|:----:|
| `validate.py` | 校验 act-XX.schema.yaml + fun_level 分布检查 | ✅ | 已启用 |
| `check_db.py` | 检查 scene_fragments.db + v3.db 双数据库 | ✅ | 已启用 |
| `pre_flight.py` | 写前环境检查 | ✅ | 已启用 |
| `project_config.py` | project.yaml 读取 + paths 解析 | ✅ | 已启用 |
| `orchestrate.py` | 全流程编排 | — | ⚠️ 未启用 |

---

## 七、已接入项目一览

| 项目 | 引擎版本 | 数据层 | 状态 |
|:-----|:--------:|:------:|:----:|
| 渊界V3 | emergent-writer v7.8 | YAML | ✅ 已完成 |
| 灰骑士之主 | emergent-writer v8.0 | YAML | ✅ 已完成 |
| 海贼法典 | emergent-writer v9.2 | SQLite | ✅ 验证中 |
| 诡异游戏v2 | emergent-writer v9.2 | SQLite v3.db | ✅ 第一幕完成 |
| 诡异人生v2 | emergent-writer v8.0 | YAML | ✅ 已完成 |
