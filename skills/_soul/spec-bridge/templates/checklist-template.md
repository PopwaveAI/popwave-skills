# [任务名称] — 验证清单

> Spec 来源：.trae/specs/[change-id]/spec.md
> 生成时间：YYYY-MM-DD
> 状态：⏳ 待验证 / ✅ 已通过 / ❌ 未通过

---

## Spec 验收标准映射

| checklist 项 | 来源 AC | 验证方式 | 状态 |
|:------------|:--------|:---------|:----|
| Check-01 | AC-1 | programmatic | ⏳ |
| Check-02 | AC-2 | human-judgment | ⏳ |
| Check-03 | AC-3 | programmatic | ⏳ |
| Check-04 | AC-4 | human-judgment | ⏳ |
| Check-05 | AC-5 | programmatic | ⏳ |

---

## 实现验证（自动可判）

- [ ] Check-01: **字数合规**
  - 验证：目标字数 ±15% 范围内
  - 来源：spec.md FR-3
  - 命令：`python spec-bridge/scripts/spec_to_prompt.py --mode verify --check word_count`

- [ ] Check-02: **场景覆盖**
  - 验证：正文覆盖了 spec.md FR-1 定义的所有场景
  - 来源：spec.md FR-1
  - 命令：`python spec-bridge/scripts/spec_to_prompt.py --mode verify --check scenes`

- [ ] Check-03: **实体计数**
  - 验证：{实体名} 计数 ≥ spec.md Constraints 中的要求
  - 来源：spec.md C-2
  - 命令：`python spec-bridge/scripts/spec_to_prompt.py --mode verify --check entities`

- [ ] Check-04: **章末钩子**
  - 验证：最后 3 行符合 FR-5 定义的钩子类型
  - 来源：spec.md FR-5
  - 命令：`python spec-bridge/scripts/spec_to_prompt.py --mode verify --check hook`

- [ ] Check-05: **无越界实现**
  - 验证：没有涉及 spec.md Non-Goals 中排除的内容
  - 来源：spec.md NG-1 ~ NG-3
  - 命令：`python spec-bridge/scripts/spec_to_prompt.py --mode verify --check non_goals`

- [ ] Check-06: **无违禁句式**
  - 验证：无否定式描写（"不是A而是B"）、无冗余前缀（"他感到"）
  - 来源：spec.md C-3, C-4
  - 命令：`python spec-bridge/scripts/spec_to_prompt.py --mode verify --check forbidden_patterns`

- [ ] Check-07: **对话占比**
  - 验证：对话占比 ≥ 25%
  - 来源：spec.md C-3
  - 命令：`python spec-bridge/scripts/spec_to_prompt.py --mode verify --check dialogue_ratio`

---

## 质量验证（需人工判断）

- [ ] Check-Q1: **爽点可感知**
  - 验证：QC 纯感受报告中提及了 spec.md FR-2 设计的爽点类型
  - 来源：spec.md AC-2
  - 方法：阅读 QC 报告，确认爽点落地

- [ ] Check-Q2: **风格一致**
  - 验证：画面密度和叙事效率接近锚定章水平
  - 来源：spec.md AC-4
  - 方法：对比锚定章片段和正文相关段落

- [ ] Check-Q3: **读者情绪达标**
  - 验证：本章完成后，读者情绪是否达到 G-2 目标
  - 来源：spec.md G-2
  - 方法：结合 QC 报告判断

---

## 管线过程验证

- [ ] Check-P1: **Director 设计说明合规**
  - 验证：设计说明中有 6 项前置检查确认 + 锚定章引用
  - 来源：emergent-writer HARD-GATE

- [ ] Check-P2: **骨架 QC 通过**
  - 验证：骨架层 QC 不包含 NOT_PASS

- [ ] Check-P3: **正文 QC 通过**
  - 验证：正文层 QC 不包含"会弃书"红线

- [ ] Check-P4: **状态已更新**
  - 验证：global-summary.md ✅ / experience-log.yaml ✅ / state_changelog ✅

---

## 汇总

| 类别 | 总数 | ✅ 通过 | ❌ 未通过 | ⏳ 待验证 |
|:----|:----|:-------|:---------|:---------|
| 实现验证 | 7 | 0 | 0 | 0 |
| 质量验证 | 3 | 0 | 0 | 0 |
| 管线验证 | 4 | 0 | 0 | 0 |
| **总计** | **14** | **0** | **0** | **0** |

> 所有检查项为通过 → 交付完成
> 1-2 项不过 → 定向修复后重验
> ≥3 项不过 → 回退到 spec 阶段
