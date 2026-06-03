# Spec → Director 注入 Prompt

> 职责：将 spec.md 的约束注入 Director Agent 的 prompt 头部
> 使用时机：Director Agent 开始设计说明之前
> 注入方式：追加到 Director-prompt.md 的输入部分之后

---

## 注入内容

### 1. 章节级硬约束（从 spec.md 提取）

```
## ★ Spec 约束（来自 spec.md — 不可违反）

### Overview（本章目的）
[spec.md Overview]

### Goals（必须达成）
- G-1: [spec.md Goals 中的目标]
- G-2: [...]

### Non-Goals（边界 — 不要碰）
- NG-1: [spec.md Non-Goals — 动笔前先确认]
- NG-2: [...]

### Requirements（必须覆盖）
- FR-1 场景编排:
  [spec.md FR-1 内容]
- FR-2 爽点设计:
  [spec.md FR-2 内容]
- FR-3 字数预算:
  [spec.md FR-3 内容]
- FR-4 锚定章引用:
  [spec.md FR-4 内容]
- FR-5 章末钩子:
  [spec.md FR-5 内容]

### Acceptance Criteria（最终以这个为标准）
- [ ] AC-1: [spec.md AC-1]
- [ ] AC-2: [spec.md AC-2]
- [ ] AC-3: [spec.md AC-3]
```

### 2. Director 额外指令

Director 生成设计说明时，**必须**在输出中回应以下 spec 要求：

```
## Spec 回应（Director 自己写）

### FR-1 场景覆盖确认
□ 设计说明覆盖了 FR-1 的所有场景
□ 权重分配与 FR-1 一致

### FR-2 爽点设计确认
□ 选择了 FR-2 指定的爽点类型
□ 爽点等级与 act-XX.yaml 一致

### Non-Goals 排除确认
□ 设计说明没有涉及 NG-1, NG-2, NG-3
```
