---
name: pop-writer-v3-revise
description: 涌现写作修订子skill。context隔离，文风DNA硬阻塞+人设丰富（含行为准则对齐）+爽点验证+bug修复+AI观感词清理。
pipeline:
  upstream: [pop-writer-v3-create]
  downstream: [pop-writer-v3-qa]
version: 1.0.0
---

# 修订子skill

> 由 pop-writer-v3-emerge Step 3 调度，context隔离。

v3.2管线涌现写作的修订子skill。对创作初稿做5项修订任务：文风对齐、人设丰富（含行为准则对齐）、爽点验证、bug修复、AI观感词清理。文风DNA在此层加载并硬阻塞（红线❌1）。修订层不改变故事结构（不增删场景/不改线索走向），只做渲染层面的打磨。

## 红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| 1 | 文风DNA缺失=修订层硬阻塞终止 | 修订前扫描文风库文件，空=终止（文风DNA为项目资产，不进种子） |
| 2 | context隔离——传入精简context，不传会话历史 | emerge调度时只传该步骤所需最小context |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-revise.md | 5项修订任务（文风对齐+人设丰富含行为准则对齐+爽点验证+bug修复+AI观感词清理） |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 修订执行 | `references/修订指南.md` | 5项修订任务详解：文风对齐+人设丰富+爽点验证+bug修复+AI观感词清理 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 修订产出 | `templates/修订checklist-模板.md` | 5项checklist（含行为准则对齐）+修订记录YAML |

## 输入/输出契约

- **输入：** 正文初稿+文风DNA+种子/（主角引擎+金手指+冲突轴）+活记忆+修订checklist
- **输出：** 修订稿+修订记录

## 路由

upstream `pop-writer-v3-create`（创作子skill，产出正文初稿） → **本skill** → downstream `pop-writer-v3-qa`（质检子skill，接收修订稿）

**调度架构：** 本skill由emerge调度器Step 3调用，context隔离——只接收精简context（正文初稿+文风DNA+种子+活记忆+修订checklist），不接收会话历史。修订完成后返回修订稿+修订记录给emerge调度器，由调度器传递给Step 4调度qa。

---

v1.0.0 | 2026-06-26 | 从pop-writer-v3-emerge v1.2.0拆分出修订子skill；人设丰富新增行为准则对齐检查；context隔离红线（红线❌2）
