---
name: pop-writer-v3-emerge
description: 涌现写作环。本章规划→信息需求判断→涌现写作(chapter+prose合并)→反思五问→活记忆更新+种子生长→方向提示
pipeline:
  upstream: [pop-writer-v3-seed]
  downstream: [pop-writer-v3-arc]
  references: [pop-trope-library, pop-shared-dna]
version: 1.1.0
---

# 涌现写作环

v3管线的第二阶段。每章执行六步循环：先规划再查再写，agent自由创作无章纲约束，文风DNA硬阻塞，网文爽感机制强制对照，活记忆唯一写入者，活种子可生长。

## 红线

| 编号 | 红线 | 检查方式 |
|------|------|----------|
| 1 | 文风DNA缺失=硬阻塞终止 | 扫描种子文风DNA字段+文风库文件，空=终止 |
| 2 | 反思不通过=回退重写本章 | 五问任一不达标，回退Step 2重写 |
| 3 | 活记忆唯一写入者 | 只有emerge的Step 4可追加event，其他skill只读 |
| 4 | 种子生长时必须更新版本号+变更日志 | minor+1 + 变更日志追加记录 |
| 5 | 本章规划必须对照网文爽感机制10条法则 | Step 0的law_check全部✅才能进Step 1 |

## 步骤加载

| 步骤 | 文件 | 说明 |
|------|------|------|
| step-0 | steps/step-0-chapter-plan.md | 本章规划（种子+上章+活记忆+方向提示+网文法则→5决策点+法则对照） |
| step-1 | steps/step-1-info-need.md | 信息需求判断（基于本章规划，4类检查，agent自主决定查不查） |
| step-2 | steps/step-2-emerge-write.md | 涌现写作（chapter+prose合并，DNA硬阻塞，80/20） |
| step-3 | steps/step-3-reflect.md | 反思五问（每个问题须有正文引用作证据） |
| step-4 | steps/step-4-memory-seed.md | 活记忆更新+种子生长（七组件刷新+自主生长） |
| step-5 | steps/step-5-direction.md | 方向提示生成+落盘+项目总控更新 |

## references/ — 知识层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 0 本章规划 | `references/网文爽感机制.md` | 10条法则对照检查（写作法则配置文件，可替换为其他领域） |
| Step 1 信息需求判断 | `references/信息需求判断SOP.md` | 4类检查标准+判断逻辑+获取流程 |
| Step 2 涌现写作 | `references/涌现写作指南.md` | 文风DNA硬阻塞+场景流渲染+80/20规则 |
| Step 4 种子生长 | `references/活种子生长触发规则.md` | 生长场景+判断原则+版本管理 |

## templates/ — 模板层

| 什么时候 | 加载 | 产出 |
|:---------|:-----|:-----|
| Step 1 产出记录 | `templates/信息需求判断记录-模板.md` | YAML格式info_needs记录 |
| Step 3 产出报告 | `templates/反思五问-模板.md` | 五问+正文引用证据 |

## 路由

upstream `pop-writer-v3-seed`（种子+活记忆baseline） → **本skill** → downstream `pop-writer-v3-arc`（弧线校准）

每章完成六步循环后，回到step-0开始下一章。弧线校准触发时中断循环，交给pop-writer-v3-arc。

---
v1.1.0 | 2026-06-26 | 新增Step 0本章规划（先想再查再写）+ 网文爽感机制配置文件 + 红线❌5
v1.0.0 | 2026-06-26 | v3涌现写作环初始创建
