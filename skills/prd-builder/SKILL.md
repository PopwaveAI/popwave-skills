---
name: "prd-builder"
description: "Takes any product idea and generates: (1) a structured PRD, (2) syncs it to Feishu, (3) processes Feishu feedback to refine it, (4) produces a standalone interactive HTML demo. Invoke when user wants to turn a product concept into a complete PRD with demo, or asks to build a PRD, create a product prototype, or make an interactive demo from an idea."
pipeline:
  upstream: []
  downstream: []
---

# PRD Builder -- 从想法到 PRD 到交互 Demo

## 概述

该 Skill 覆盖产品从概念到可演示原型的全流程：

```
用户想法 -> 需求澄清 -> PRD(.md) -> 飞书文档 -> 反馈迭代 -> 单HTML交互Demo
```

核心原则：
- **通用性**：适用于任何产品类别，KOL 评估平台仅为参考案例
- **真实数据优先**：Demo 中使用的数据应从网络搜索获取真实信息，辅以预置模板库
- **零依赖交付**：最终 Demo 为单文件 HTML（Chart.js 内联），可直接在浏览器打开

---

## PRD 结构（8 章，自由扩展）

按 WHY -> WHO -> HOW -> WHAT -> UI -> DATA -> QUALITY 逻辑链组织：

| 章 | 标题 | 回答的问题 |
|:--:|------|-----------|
| 1 | 产品概述 | 为什么要做？ |
| 2 | 用户角色与场景 | 谁来用、怎么用？ |
| 3 | 核心业务流程 | 用户完成一件事经过哪些步骤？ |
| 4 | 产品架构 | 系统分几大块？ |
| 5 | 功能详述 | 每块具体做什么？ |
| 6 | 页面交互设计 | 用户看到什么界面、怎么操作？ |
| 7 | 数据模型 | 存什么数据、数据间什么关系？ |
| 8 | 非功能需求 | 要多快、多安全、多稳？ |

> 以上为最小必要章节。如果产品涉及权限体系、多角色协作、合规等，可自由追加。如果产品无显式工作流，第 3 章可改名为「核心用户路径」或跳过。

---

## Phase 1: 需求澄清

收到用户 product idea 后，问 3-4 个关键问题（AskUserQuestion）：

| 必须问 | 为什么 |
|--------|--------|
| 产品类型/领域 | 决定 Demo 内容主题、示例数据、用户场景 |
| 目标受众 | 内部团队 / 管理层 / 客户 -- 影响 PRD 深度和 Demo 风格 |
| Demo 深度 | 精简版(3-4页) / 标准版(5-7页) / 深度版(含数据看板+交互看板) |
| 特殊功能要求 | 如果用户提到了特定功能模块，确认优先级 |

如果用户 idea 已清晰，可跳过提问直接进入 Phase 2。

---

## Phase 2: PRD 生成 + 飞书同步

### 2.1 生成 PRD

读取 references/prd_structure.md 获取模板结构，基于用户 idea 定制完整 PRD (Markdown)。

按 8 章结构生成：产品概述 -> 用户角色与场景 -> 核心业务流程 -> 产品架构 -> 功能详述 -> 页面交互设计 -> 数据模型 -> 非功能需求。

**页面交互设计（第 6 章）**必须包含：
- 页面路由图（ASCII）
- 页面线稿（ASCII 网格布局）
- 组件-状态矩阵（空态/正常态/异常态）
- 关键交互说明
- 可有数据契约（衔接第 7 章，TypeScript 风格）

### 2.2 同步到飞书

1. Skill("feishu-docs") 加载技能
2. 获取 token
3. POST /docx/v1/documents 创建空文档
4. 解析 MD -> blocks，**逐个追加**（批量 >10 块会报 1770006）
5. descendant API 构建表格
6. PATCH /permissions/{id}/public -> anyone_can_edit

已验证的 Block API 规则：
- ordered/bullet 列表不支持 text_element_style.link -> 去除链接
- H4-H6 降级为粗体文本
- 代码块逐行转 inline_code text block

---

## Phase 3: 飞书反馈处理

触发词：处理飞书反馈 / 查看飞书评论 / 根据反馈修改

### 模式 A：汇总模式（默认）

1. GET /drive/v1/files/{doc_id}/comments?file_type=docx 拉取评论
2. 逐条展示，分类为「修改建议」和「问题追问」
3. 等待用户逐条指示如何处理

### 模式 B：自动处理模式

用户说"自动处理"触发：
- 所有修改请求 -> 直接改 PRD + 更新飞书
- 所有补充请求 -> 回复评论给出补充信息
- **关键**：回复时不要设置 is_solved=true
- 完成后输出修改摘要

---

## Phase 4: 生成交互 Demo

用户确认 PRD 后说"生成 Demo"触发。

### 4.1 数据准备

| 层次 | 来源 |
|------|------|
| 业务数据 | 网络搜索行业案例、基准数据、竞品 |
| 角色模板 | references/kol_templates.json (12 个预置角色) |
| 平台基准 | references/platform_benchmarks.json |

Demo 使用真实名称。如果产品领域不涉及 KOL，替换为对应领域的真实案例对象。

### 4.2 Demo 结构

参照 references/demo_framework.md，根据第 6 章的页面设计生成：

| 页面 | 来源 |
|------|------|
| 工作台 Dashboard | 第 6 章线稿 -> Dashboard 页 |
| 列表页 | 第 6 章线稿 -> List 页 |
| 详情页 (每对象独立) | 第 6 章线稿 -> Detail 页，4 Tab：评估/风险/案例/数据 |
| 看板页 | 第 3 章流程 + 第 6 章线稿 -> Kanban 页 |
| 评估/对比中心 | 第 6 章线稿 -> Compare 页 |

### 4.3 技术约束

- 单文件 HTML，数据 JS 内嵌
- 左侧固定导航 + 右侧内容区
- 详情 Tab 切换，showPage()/goDetail() 驱动（必须空值保护）
- 最终用 Python 内联 Chart.js -> Standalone 版本

---

## 注意事项

1. MD 文件 -> workspace；脚本 -> 临时目录
2. 飞书批量 blocks 单批 >10 可能失败 -> 逐个追加
3. feishu_token.py 崩溃 -> 直接 POST /auth/v3/tenant_access_token/internal
4. Demo 实体名用真实姓名
5. 非 KOL 领域 -> 替换为对应领域真实案例，保持页面结构不变
6. PRD 章节按需自由追加或跳过（如无工作流则跳第 3 章）
