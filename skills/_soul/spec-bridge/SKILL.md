---
name: spec-bridge
display_name: "Spec 桥接层 — 规格驱动写作"
category: spec
scenario: pre-production
mode: bridge
recommended: 0
tags: ["spec", "规格", "审批", "验证", "质量闸门"]
fidelity: production
description: "Spec 桥接层。在任何写作任务进入现有管线之前，先生成归一化规格文档（spec.md），经审批确认后再拆解为可执行任务（tasks.md），并产出验证清单（checklist.md）。三文件贯穿后续所有写作阶段。"
version: v1.0.0
orchestration:
  preflight: ["check_project_dir", "check_spec_not_exists"]
  dependencies: ["project.yaml"]
  inject_context: ["project.yaml#reader_profile"]
  subagent_required: false
produces:
  - spec.md（需求规格 — Guide/Non-Goals/Requirements/Acceptance Criteria）
  - tasks.md（任务分解 — 按阶段拆解为可独立执行的任务，标注依赖）
  - checklist.md（验证清单 — 每个检查项对应 spec.md 中的一条 AC）
---

# Spec 桥接层 — 先规格后实现 · 深度整合

> 版本：**v1.0.0** · 2026-05-31
>
> 改造自 Trae Spec 模式 + pop-novelagent 六阶段管线融合。
> **核心理念**：在 AI 动手之前，先把"对的事"定义清楚；在 AI 完成之后，用"可判定的标准"验证它做对了。
>
> 本桥接层不修改任何现有管线逻辑，在管线入口前增加一道「提案 → 审批 → 拆解」闸门。

---

## 一、设计定位

### 1.1 Spec 桥接层 vs 现有管线

```
【现有流程】
用户需求 → POP-ROUTER → dispatcher → sub-agent（六阶段管线）

【Spec 深度整合流程】                    ★新增部分
用户需求 → POP-ROUTER 
          → 【spec-bridge ★】          ← ◈ 提案 + 审批闸门
              ├─ 生成 spec.md
              ├─ 等待人工审批
              └─ 产出 tasks.md + checklist.md
          → dispatcher
          → sub-agent（六阶段管线）       ← ◈ 每个阶段引用 spec.md
          → 【spec-verify ★】           ← ◈ checklist 验证
```

### 1.2 两层级 Spec

| 层级 | 作用域 | 生成时机 | 说明 |
|:----|:-------|:---------|:-----|
| **宏观 Spec** | 项目级（整本书） | 开书启动时 | 定义全书愿景、目标读者、平台、类型、非目标、验收标准 |
| **微观 Spec** | 章节级（单章写作） | 每章写作前 | 定义本章目的、场景分配、字数、基调、约束 |

微观 Spec 取代现有 Director Agent 的"设计说明"，将设计说明**形式化**为 spec.md 结构。

---

## 二、三文件规范

### 2.1 spec.md — 需求规格

每份 spec.md 包含以下结构（对应模板见 `templates/`）：

```
# [任务名称] — 规格文档

## Overview                ← 一句话概括本次任务
## Goals                   ← 要达成的目标（2-5条）
## Non-Goals (Out of Scope)← 明确不做什么（防止AI自由发挥）
## Context                 ← 当前状态、已知约束
## Requirements            ← FR-1, FR-2... 具体功能/内容需求
## Constraints             ← 字数、格式、风格等硬约束
## Assumptions             ← 前提假设
## Acceptance Criteria     ← Given/When/Then 可判定验收标准
```

### 2.2 tasks.md — 任务分解

将 spec.md 拆解为可独立执行的 sub-task，标注依赖关系：

```
## Spec 来源
引用 spec.md 中的 Requirements 编号

## 任务列表
- [ ] Task 1: [任务名] — [完成标准]（依赖: None）
- [ ] Task 2: [任务名] — [完成标准]（依赖: Task 1）
- [ ] Task 3: [任务名] — [完成标准]（依赖: Task 1）
...
```

### 2.3 checklist.md — 验证清单

从 spec.md 的 Acceptance Criteria 直接映射，每个检查项可判定通过/不通过：

```
## Spec 来源
引用 spec.md 的 AC 编号

## 实现验证
- [ ] AC-1: [可判定的通过条件]
- [ ] AC-2: [可判定的通过条件]
...

## 代码/内容质量
- [ ] Q-1: [质量检查项]
...
```

---

## 三、工作流程

### Phase A：提案（spec-bridge 执行）

收到用户需求后（如"写第8章"），执行：

1. **读取上下文**：现有文件、reader_profile、act-XX.yaml、上一章状态
2. **生成 spec.md**：按 `templates/spec-micro-template.md` 结构，填充内容
3. **生成 tasks.md**：将 spec.md 的 Requirements 拆解为任务
4. **生成 checklist.md**：将 spec.md 的 Acceptance Criteria 直接映射
5. **展示三文件**：让用户审阅

### Phase B：审批（人工介入）

用户审阅通过 → 进入管线。不通过 → 修改 spec.md 后重审。

### Phase C：注入（spec-bridge → 管线）

审批通过后，spec-bridge 将 spec.md 内容注入到每个阶段的 Agent Prompt 头部：

```
# 每个 sub-agent 的 prompt 头部追加：
"""
## 本次写作的规格约束
引自 .trae/specs/chXXX/spec.md

### Overview
[一句话目的]

### Goals
- [目标1]
- [目标2]

### Acceptance Criteria（必须满足）
- [ ] AC-1: ...
- [ ] AC-2: ...
"""
```

### Phase D：验证（spec-verify）

所有任务完成后，对照 checklist.md 逐项验证。每项标记 PASS/FAIL。
如有 FAIL → 创建修复任务，重新执行对应 sub-agent。

---

## 四、与现有管线的融合点

| 管线阶段 | 当前行为 | Spec 增强 |
|:---------|:---------|:----------|
| **Director Agent** | 输出设计说明 + 决策日志 | **输出 spec.md 格式**的设计说明，Acceptance Criteria 被 Pass2/QC 引用 |
| **Pass 1 骨架** | 遵循导演约束 | **增加"spec 合规检查"**：骨架事件是否覆盖 spec 的 Requirements |
| **ESM before** | 装配 14 项输入包 | **增加第15项：spec.md** 作为上下文注入 Pass2 |
| **Pass 2 渲染** | 渲染正文 + 自评 | **自评增加"AC 对照"**：逐条检查是否满足 Acceptance Criteria |
| **QC 三层介入** | 纯感受报告 | **增加"Spec 合规层"**：检查正文是否偏离 spec 定义的范围 |
| **ESM after** | 更新状态 | **更新 checklist.md**：标记已验证项 |

---

## 五、HARD-GATE（不可跳过）

| # | 铁律 | 违反后果 | 检查时机 |
|:-|:-----|:---------|:--------|
| S-01 | **写任何正文前必须先过 spec-bridge** | 管线入口无规格约束 → AI 自由发挥 | 每次写作前 |
| S-02 | **spec.md 必须经过人工审批** | 规格未确认 → 后续验证无依据 | 审批阶段 |
| S-03 | **checklist.md 必须全部通过才能声称完成** | 质量失控 → 边界情况无人发现 | 管线出口 |
| S-04 | **tasks.md 的任务必须按依赖顺序执行** | 乱序执行 → 上下文不一致 | 编排阶段 |
| S-05 | **每个 sub-agent 必须读到 spec.md 的对应段** | Agent 不知道规格边界 → 越界实现 | Agent 注入时 |

---

## 六、存储约定

所有 Spec 三文件存放在项目的 `.trae/specs/<change-id>/` 目录下：

```
<project-root>/
└── .trae/
    └── specs/
        ├── 01-book-bootstrap/       # 宏观 Spec：开书启动
        │   ├── spec.md
        │   ├── tasks.md
        │   └── checklist.md
        ├── ch001-ch003/             # 宏观 Spec：前三章
        │   ├── spec.md
        │   ├── tasks.md
        │   └── checklist.md
        └── ch008/                   # 微观 Spec：第8章
            ├── spec.md
            ├── tasks.md
            └── checklist.md
```

---

## 七、调用方式

```bash
# pop agent 内部调用
spec-bridge:
  1. python spec-bridge/scripts/spec_to_prompt.py --mode generate --project <dir>
  2. AskUserQuestion "请审阅 spec.md，确认是否通过？"
  3. if approved: python spec-bridge/scripts/spec_to_prompt.py --mode inject --project <dir> --target director|pass1|pass2|qc
  4. else: 修改 spec.md 后重审
  5. python spec-bridge/scripts/spec_to_prompt.py --mode verify --project <dir> --checklist
```
