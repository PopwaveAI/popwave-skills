---
name: pop-writer-v3-emerge
description: "[已废弃 v2.1.0] 调度职能已吸收到 expert-writer v9.2.0。7步循环参考文档已迁移至 expert-writer/references/emerge-loop/。本skill保留文件供回溯，不再激活。"
pipeline:
  upstream: [pop-writer-v3-seed]
  downstream: [pop-writer-v3-arc]
  references: [pop-trope-library, pop-shared-dna]
version: 2.1.0
deprecated: true
---

# ⚠️ 已废弃 — 调度职能已吸收到 expert-writer v9.2.0

> **本 skill 不再激活。** 涌现写作环的7步循环由 expert-writer 主会话直接执行。
> - 7个step文件已迁移到 `expert-writer/references/emerge-loop/`（作为参考文档）
> - 3个references文件已迁移到 `expert-writer/references/emerge-loop/`
> - expert-writer `steps/step-2-execute.md` 重写为7步循环执行流程
> - 调度 create/revise/qa 子skill 的职能由 expert-writer 直接执行
>
> 以下内容保留供历史回溯，不再维护。

v3.2管线的第二阶段。emerge降为纯调度器：主会话调度Step 0-1和Step 5-6；Step 2/3/4调度3个独立子skill（pop-writer-v3-create/revise/qa），context隔离。文风从创作端拆出到修订层，创作子skill专注故事涌现。信息获取强制化——每章必须读素材库索引，不可跳过。v3.3新增设定库按需读取——emerge Step 1检查设定库索引，涉及力量体系/社会结构/已建档角色时按需读取。种子文件夹六要素（文风DNA为项目资产，设定库为可选参考层）。

**v3.2核心改动：** 3子agent从emerge内嵌step拆为3个独立skill，emerge降为纯调度器。context隔离从纪律约束变为架构边界。素材库替代散落知识库。搜索深度标准+无需求门槛提高。

## 红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| 1 | 文风DNA缺失=修订层硬阻塞终止 | revise子skill扫描文风库文件，空=终止（文风DNA为项目资产，不进种子） |
| 2 | 质检不通过=回退重写本章 | qa子skill五问任一不达标或行为一致性终验❌，回退create子skill(故事层)或revise子skill(文风层) |
| 3 | 活记忆唯一写入者 | 只有emerge的Step 5可追加event，其他skill只读 |
| 4 | 种子生长时必须更新版本号+变更日志 | minor+1 + 变更日志追加记录 |
| 5 | 本章规划必须对照网文爽感机制10条法则 | Step 0的law_check全部✅才能进Step 1 |
| 6 | 信息获取必须读索引——素材库/索引.md未读取=退回补读 | Step 1强制读 素材库/索引.md，未读=退回补读 |
| 7 | 子skill调度context隔离——传入精简context，不传会话历史 | Step 2/3/4各自只传入该步骤所需的最小context，不传递主会话历史 |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-0 | steps/step-0-chapter-plan.md | 本章规划（种子六要素+上章+活记忆+方向提示+网文法则→5决策点+法则对照） |
| step-1 | steps/step-1-info-forced.md | 信息获取强制化（读素材库索引→读设定库索引→有则读→无则WebSearch→写入素材库/知识沉淀→更新索引） |
| step-2 | steps/step-2-dispatch-create.md | 调度create子skill（context隔离：组装精简context→调用pop-writer-v3-create→收集产出→门禁） |
| step-3 | steps/step-3-dispatch-revise.md | 调度revise子skill（context隔离：组装精简context→调用pop-writer-v3-revise→收集产出→门禁） |
| step-4 | steps/step-4-dispatch-qa.md | 调度qa子skill（context隔离：组装精简context→调用pop-writer-v3-qa→收集质检报告→门禁） |
| step-5 | steps/step-5-memory-direction.md | 记忆更新+种子生长+方向提示（主会话机械执行，读质检报告→机械写入） |
| step-6 | steps/step-6-commit.md | 落盘+项目总控更新+弧线触发检查 |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 0 本章规划 | `references/网文爽感机制.md` | 10条法则对照检查（写作法则配置文件，可替换为其他领域） |
| Step 1 信息获取强制化 | `references/信息获取强制化SOP.md` | 强制化流程+素材库目录结构+索引格式+写入流程+搜索深度标准 |
| Step 5 种子生长 | `references/活种子生长触发规则.md` | 生长场景+判断原则+版本管理 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 1 产出记录 | `templates/信息获取记录-模板.md` | YAML格式info_acquired记录+素材库目录结构+索引格式+搜索深度标准 |

## 路由

upstream `pop-writer-v3-seed`（种子六要素+文风库文件+活记忆baseline） → **本skill** → downstream `pop-writer-v3-arc`（弧线校准）

**调度架构**：主会话调度Step 0-1和Step 5-6；Step 2/3/4调度3个独立子skill（pop-writer-v3-create/revise/qa），context隔离。每章完成七步循环后，回到step-0开始下一章。弧线校准触发时中断循环，交给pop-writer-v3-arc。

**子skill路由：**
- Step 2 → `pop-writer-v3-create`（创作子skill，场景流+压力源+钩子+行为一致性）
- Step 3 → `pop-writer-v3-revise`（修订子skill，文风对齐+人设丰富+爽点验证+bug修复+AI观感词清理）
- Step 4 → `pop-writer-v3-qa`（质检子skill，五问反思+种子生长判断+爽点终验+行为一致性终验）

---

v2.1.0 | 2026-06-26 | step-1新增设定库按需读取（1.5步）+种子文件夹路径更新+creative引用清理为v3-seed SOP
v2.0.0 | 2026-06-26 | 3子agent拆为3独立skill（create/revise/qa），emerge降为纯调度器；context隔离从纪律变架构边界；素材库替代知识库（红线❌6路径更新）；搜索深度标准+无需求门槛提高
v1.2.0 | 2026-06-26 | 调度+3子agent架构重构（创作/修订/质检context隔离）+文风拆到修订层+信息获取强制化+种子六要素
v1.1.0 | 2026-06-26 | 新增Step 0本章规划（先想再查再写）+ 网文爽感机制配置文件 + 红线❌5
v1.0.0 | 2026-06-26 | v3涌现写作环初始创建
