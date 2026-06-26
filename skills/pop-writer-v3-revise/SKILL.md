---
name: pop-writer-v3-revise
description: 涌现写作修订子skill。context隔离，文风DNA硬阻塞+人设丰富（含行为准则对齐）+爽点验证+bug修复+AI观感词清理。v3.4：完全重写模式（基于正文+文风DNA）+文风DNA终验+事实信息一致性+字数终检。qa剔除后承担全部质检职责。
pipeline:
  upstream: [pop-writer-v3-create]
  downstream: []
version: 1.1.0
---

# 修订子skill

> 由 pop-writer-v3-emerge Step 3 调度，context隔离。

v3.2管线涌现写作的修订子skill。基于正文初稿+文风DNA完全重写渲染层：保留创作层产出的全部事实信息（人名/动作/事件顺序/对话内容/场景/数值），仅重做渲染层（句式/叙事距离/感官密度/对话留白/8020比例）。文风DNA在此层完整加载并硬阻塞（红线❌1）。v3.4剔除qa后，本skill承担全部质检职责：完全重写+文风DNA终验+事实信息一致性检查+AI观感词清理+字数终检。

## 红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| 1 | 文风DNA缺失=修订层硬阻塞终止 | 修订前扫描文风库文件，空=终止（文风DNA为项目资产，不进种子） |
| 2 | context隔离——传入精简context，不传会话历史 | emerge调度时只传该步骤所需最小context |
| 3 | 重写时改写事实信息（人名/动作/事件顺序/对话内容/场景/数值）=退回重写 | 重写后逐项比对初稿，事实信息任一被改写即退回重写 |
| 4 | 文风DNA用limit截断=退回重载 | DNA加载必须Get-Content -Raw完整加载，发现limit截断即退回重载 |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-revise.md | 完全重写+事实一致性检查+文风DNA终验+AI观感词清理+字数终检 |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 修订执行 | `references/修订指南.md` | 完全重写规范+事实一致性检查+文风DNA终验+AI观感词清理+字数终检 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 修订产出 | `templates/修订checklist-模板.md` | 完全重写checklist+修订记录YAML（含rewrite_mode/fact_consistency/dna_final_check/word_count_check） |

## 输入/输出契约

- **输入：** 正文初稿+文风DNA+种子/（主角引擎+金手指+冲突轴）+活记忆+修订checklist
- **输出：** 重写稿+修订记录（含rewrite_mode/fact_consistency/dna_final_check/word_count_check）

## 路由

upstream `pop-writer-v3-create`（创作子skill，产出正文初稿） → **本skill** → downstream 无（v3.4剔除qa，revise是终点，重写稿交付用户验收CHECK 2）

**调度架构：** 本skill由emerge调度器Step 3调用，context隔离——只接收精简context（正文初稿+文风DNA+种子+活记忆+修订checklist），不接收会话历史。完全重写完成后返回重写稿+修订记录给expert-writer调度器，交付用户验收（CHECK 2），验收后传Step 4记忆+生长。

---

v1.0.0 | 2026-06-26 | 从pop-writer-v3-emerge v1.2.0拆分出修订子skill；人设丰富新增行为准则对齐检查；context隔离红线（红线❌2）
v1.1.0 | 2026-06-27 | v3.4重构：逐行修改→完全重写模式（基于正文骨架+文风DNA）；剔除qa，revise成为终点交付用户验收CHECK 2；新增红线❌3（重写改写事实信息=退回重写）+❌4（DNA用limit截断=退回重载）；新增文风DNA终验+事实信息一致性检查+字数终检
