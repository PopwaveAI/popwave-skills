---
name: pop-writer-v3-create
description: 涌现写作创作子skill。context隔离，专注故事涌现——场景流渲染+压力源逼近+章末钩子+主角行为一致性。不论文风。
pipeline:
  upstream: [expert-writer]
  downstream: [pop-writer-v3-revise]
version: 1.1.0
---

# 创作子skill

> 由 expert-writer Step 2 调度，context隔离。

v3.2管线涌现写作的创作子skill。专注故事结构层：场景流渲染+压力源逼近+章末钩子+主角行为一致性。不做文风对齐（→修订层）、不做8020比例（→修订层）、不做AI观感词清理（→修订层）。文风从创作端拆出到修订层，创作子skill只管故事涌现。

## 红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| 1 | context隔离——传入精简context，不传会话历史 | expert-writer调度时只传该步骤所需最小context |
| 2 | 主角行为必须符合种子行为准则 | 创作前加载行为准则，逐场景检查行为一致性 |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-1 | steps/step-1-create.md | 涌现写作（场景流+压力源+钩子+行为一致性检查） |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 创作执行 | `references/创作指南.md` | 场景流渲染+压力源逼近+章末钩子+主角行为一致性检查 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| step-1 创作产出 | `templates/创作-模板.md` | 上下文确认表+正文涌现结构+创作决策记录YAML+门禁表 |

## 输入/输出契约

- **输入：** 种子/_index.yaml+种子六要素文件（压力矩阵/主角引擎/金手指/冲突轴/成长路径/目的地）+活记忆+上章末尾+chapter_plan（任务list：定位/目标/读者获得/剧情线/信息释放/信息需求/钩子方向，非场景list）+info_acquired+创作模板
- **输出：** 正文初稿+创作决策记录

## 路由

upstream `expert-writer`（调度器，Step 2组装精简context调用本skill） → **本skill** → downstream `pop-writer-v3-revise`（修订子skill，接收正文初稿）

**调度架构：** 本skill由expert-writer调度器Step 2调用，context隔离——只接收精简context，不接收会话历史。创作完成后返回正文初稿+创作决策记录给expert-writer调度器，由调度器传递给Step 3调度revise。

---

v1.0.0 | 2026-06-26 | 从pop-writer-v3-emerge v1.2.0拆分出创作子skill；新增主角行为一致性检查（红线❌2）；context隔离红线（红线❌1）
v1.1.0 | 2026-06-27 | v3.4：输入context从场景list改为任务list（释放涌现空间）；新增字数下限门禁；upstream改为expert-writer
