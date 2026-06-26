---
name: pop-writer-v3-emerge
description: 涌现写作环。本章规划→信息获取(强制化)→调度3子agent(创作/修订/质检)→记忆更新+种子生长→方向提示
pipeline:
  upstream: [pop-writer-v3-seed]
  downstream: [pop-writer-v3-arc]
  references: [pop-trope-library, pop-shared-dna]
version: 1.2.0
---

# 涌现写作环

v3管线的第二阶段。每章执行调度+3子agent架构：主会话调度Step 0-1和Step 5-6；Step 2/3/4为独立子agent（创作/修订/质检），通过expert-writer Execute层调度，context隔离。文风从创作端拆出到修订层，创作子agent专注故事涌现。信息获取强制化——每章必须读索引，不可跳过。种子六要素（文风DNA已移至项目资产）。

## 红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| 1 | 文风DNA缺失=修订层硬阻塞终止 | 修订子agent扫描文风库文件，空=终止（文风DNA为项目资产，不进种子） |
| 2 | 质检不通过=回退重写本章 | 质检子agent五问任一不达标，回退Step 2(故事层)或Step 3(文风层) |
| 3 | 活记忆唯一写入者 | 只有emerge的Step 5可追加event，其他skill只读 |
| 4 | 种子生长时必须更新版本号+变更日志 | minor+1 + 变更日志追加记录 |
| 5 | 本章规划必须对照网文爽感机制10条法则 | Step 0的law_check全部✅才能进Step 1 |
| 6 | 信息获取必须读索引——索引.md未读取=退回补读 | Step 1强制读 写作资产/知识库/索引.md，未读=退回补读 |
| 7 | 3子agent context隔离——传入精简context，不传会话历史 | Step 2/3/4各自只传入该步骤所需的最小context，不传递主会话历史 |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-0 | steps/step-0-chapter-plan.md | 本章规划（种子六要素+上章+活记忆+方向提示+网文法则→5决策点+法则对照） |
| step-1 | steps/step-1-info-forced.md | 信息获取强制化（读索引→有则读→无则WebSearch→写入知识库→更新索引） |
| step-2 | steps/step-2-create.md | 创作子agent（context隔离：场景流渲染+压力源逼近+章末钩子，不管文风） |
| step-3 | steps/step-3-revise.md | 修订子agent（context隔离：文风对齐/人设丰富/爽点验证/bug修复/AI观感词清理） |
| step-4 | steps/step-4-qa.md | 质检子agent（context隔离：五问反思引用正文证据+种子生长判断+爽点终验） |
| step-5 | steps/step-5-memory-direction.md | 记忆更新+种子生长+方向提示（主会话机械执行，读质检报告→机械写入） |
| step-6 | steps/step-6-commit.md | 落盘+项目总控更新+弧线触发检查 |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 0 本章规划 | `references/网文爽感机制.md` | 10条法则对照检查（写作法则配置文件，可替换为其他领域） |
| Step 1 信息获取强制化 | `references/信息获取强制化SOP.md` | 强制化流程+知识库目录结构+索引格式+写入流程 |
| Step 2 创作子agent | `references/创作指南.md` | 场景流渲染+压力源逼近+章末钩子（不含文风DNA/8020/AI观感词） |
| Step 3 修订子agent | `references/修订指南.md` | 5项修订任务详解：文风对齐+人设丰富+爽点验证+bug修复+AI观感词清理 |
| Step 5 种子生长 | `references/活种子生长触发规则.md` | 生长场景+判断原则+版本管理 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 1 产出记录 | `templates/信息获取记录-模板.md` | YAML格式info_acquired记录+知识库目录结构+索引格式 |
| Step 2 创作产出 | `templates/创作-模板.md` | 上下文确认表+正文涌现结构+创作决策记录YAML+门禁表 |
| Step 3 修订产出 | `templates/修订checklist-模板.md` | 5项checklist+修订记录YAML |
| Step 4 质检产出 | `templates/质检报告-模板.md` | 五问反思(每问须正文引用)+种子生长判断+爽点终验+回退目标 |

## 路由

upstream `pop-writer-v3-seed`（种子六要素+文风库文件+活记忆baseline） → **本skill** → downstream `pop-writer-v3-arc`（弧线校准）

**调度架构**：主会话调度Step 0-1和Step 5-6；Step 2/3/4为独立子agent，通过expert-writer Execute层调度，context隔离。每章完成七步循环后，回到step-0开始下一章。弧线校准触发时中断循环，交给pop-writer-v3-arc。

---

v1.2.0 | 2026-06-26 | 调度+3子agent架构重构（创作/修订/质检context隔离）+文风拆到修订层+信息获取强制化+种子六要素
v1.1.0 | 2026-06-26 | 新增Step 0本章规划（先想再查再写）+ 网文爽感机制配置文件 + 红线❌5
v1.0.0 | 2026-06-26 | v3涌现写作环初始创建
