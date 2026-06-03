# Spec Generator — 规格生成 Prompt

> 职责：从用户需求生成归一化的 spec.md + tasks.md + checklist.md
> 使用时机：用户提出任何写作任务后（开书/写章/续写/批量）

---

## 输入

- 用户原始需求（如"为渊界V3写第8章"）
- 项目现有上下文（project.yaml / act-XX.yaml / 上一章状态）
- reader_profile
- 已有宏/微观 Spec（如存在）

## 输出

三文件写入 `.trae/specs/<change-id>/` 目录。

---

## 生成步骤

### Step 1: 判断 Spec 层级

| 用户需求 | Spec 层级 | change-id |
|:---------|:----------|:----------|
| "开新书" / "设计设定" | 宏观 | 01-book-bootstrap |
| "写前三章" | 宏观 | ch001-ch003 |
| "写第N章" | 微观 | ch[N] |
| "批量写 N-M 章" | 宏观 | ch[N]-ch[M] |
| "续写已有项目" | 宏观 | continuation |

### Step 2: 生成 Overview + Goals

根据用户需求 + reader_profile，确定：
- 一句话目的
- 2-4 个可量化目标
- 明确 Non-Goals 边界（防止 AI 自由发挥）

### Step 3: 生成 Context

读取当前项目状态：
- 已有多少章、最近一章的内容
- 当前幕纲规划
- 上一章结尾状态
- 读者此刻的期待（基于经验日志和全局摘要）

### Step 4: 生成 Requirements

将用户需求拆解为 FR（功能需求）：

```
FR-1: [需求名]
  - [具体描述]
  - [具体描述]

FR-2: [需求名]
  ...
```

### Step 5: 生成 Constraints

基于：
- 项目 L1-core / constitution.yaml 的约束
- emergent-writer 的 HARD-GATE 铁律
- 平台的规则（字数、风格等）

### Step 6: 生成 Acceptance Criteria

每个 AC 使用 Given/When/Then 三段式，标注 Verification 方式：
- `programmatic` — 可自动化验证（字数、实体数、违禁句式）
- `human-judgment` — 需要人工判断（爽点落地、风格一致）

### Step 7: 生成 tasks.md

将 Requirements 拆解到现有管线的每个阶段，标注依赖关系。

### Step 8: 生成 checklist.md

将 Acceptance Criteria 直接映射为检查项，每项可判定通过/不通过。

---

## 质量基线

生成的 spec.md 必须满足：

1. **Goals 可量化** — 不是"写得好"，而是"字数≥2000、无违禁句式"
2. **Non-Goals 具体** — 不是"不要跑偏"，而是"不新增实体/不做回忆杀"
3. **AC 可判定** — 每个 AC 能给出明确的 PASS/FAIL 判定
4. **tasks 可执行** — 每个 task 对应一个已知的管线阶段
5. **checklist 全覆盖** — 每个 FR 至少有一个对应的检查项
