---
name: pop-novel-bootstrap
display_name: "开书启动"
category: bootstrap
scenario: design
mode: project
recommended: 1
tags: ["开书", "设定", "初始化", "骨架"]
fidelity: production
description: "开书启动 v2.9。从L0灵魂对齐→核心卖点深度研究→跨域素材聚合（强制）→L1-L3分层设定→L1深度展开（逐篇扩写+交叉关联）→稳定性检验→项目骨架创建。"
version: v2.9
novel_agent_version: v3.3
orchestration:
  preflight: []
  dependencies: []
  inject_context: []
  subagent_required: true
directory: pop-novel-bootstrap

produces:
  - 00-原始设定/L0-产品层/PRD.md
  - 00-原始设定/_参考书分析/{书名}.md
  - 00-原始设定/L1-元设定层/01-06.md
  - 00-原始设定/world-stability-check.md
  - 02-大纲/卷01/（地理/势力/角色/剧情/装备/爽点设计）
  - 02-大纲/L3-角色层/（角色卡）
  - 00-总控/project.yaml chapter-state.yaml project-status.html
  - 00-总控/数值体系/（combat_capability/monster_rank_map/act_rank_schedule）
  - 03-正文/
  - 04-数据库/novel.db
  - constitution.yaml
---

# 开书启动 — 初始化管线

> 版本：v2.9 | 日期：2026-06-03 | 分类：bootstrap | 执行顺序：Phase 1

## 什么时候使用

| 场景 | 说明 |
|------|------|
| **新书开坑** | 从零到一搭建完整的小说项目骨架 |
| **创意可行性验证** | 不确定创意能不能撑起长篇，需系统检验 |
| **设定规范化** | 已有零散设定，需结构化、分层化、标准化 |

**不适用**：短篇（<10万字）→ 用 light-bootstrap；仅需稳定性检查 → 用 world-stability-check skill。

## 输入表

| 输入项 | 必需 | 说明 | 示例 |
|--------|:----:|------|------|
| 书名 | ✅ | 作品正式名称 | 《深渊归途》 |
| 核心创意 | ✅ | 一句话概括 | 主角在1000层深渊中寻找回家的路 |
| 平台 | ✅ | 发布平台 | qidian / fanqie |
| 对标书 | ✅ | 至少1本同类作品 | 按作品类型搜索 |
| 核心爽点 | ✅ | 2-5个类型 | 战力升级/智商碾压 |
| 金手指 | 可选 | 一句话描述 | 无限复活+记忆保留 |

## 执行顺序（按依赖链依次执行）

```
Phase 0 (L0灵魂层)
    ↓
Phase 0.3 (参考书甄别)
    ↓
Phase 0.4 (金手指设计)
    ↓
Phase 0.5 ★ (跨域素材聚合)  ← 强制不可跳过
    ↓
Phase 1 (L1设定层推演)
    ↓
Phase 1.2 ★ (L1深度展开)   ← v2.9 逐篇扩写
    ↓
Phase 1.3 ★ (L1交叉关联)   ← v2.9 14对关联
    ↓
Phase 1.5 (世界稳定性检验)
    ↓
Phase 2 (L2卷级展开)
    ↓
Phase 3 (项目骨架创建)
    ↓
Phase 4 (reader_profile嵌入)
    ↓
Phase 5 (数值体系模板升级)
    ↓
Phase 6 (超越性硬检查)
```

## Phase 指令索引

当前处于第几步，就只加载对应文件：

| Phase | 文件 | 类型 |
|:------|:-----|:-----|
| Phase 0 | `phases/phase-0.md` | 灵魂对齐 + PRD + 压力测试 |
| Phase 0.3 | `phases/phase-0.3.md` | 参考书筛选 + 拆解 + 差异化 |
| Phase 0.4 | `phases/phase-0.4.md` | 金手指设计 + 四级评估 + 约束检查 |
| Phase 0.5 ★ | `phases/phase-0.5.md` | 跨域素材聚合（强制） |
| Phase 1 | `phases/phase-1.md` | L1六件套骨架 |
| Phase 1.2 ★ | `phases/phase-1.2.md` | L1深度展开（逐篇扩写） |
| Phase 1.3 ★ | `phases/phase-1.3.md` | L1交叉关联矩阵 |
| Phase 1.5 | `phases/phase-1.5.md` | 世界稳定性检验 |
| Phase 2 | `phases/phase-2.md` | L2卷级展开 + 爽点设计 |
| Phase 3 | `phases/phase-3.md` | 项目骨架 + 角色卡 + 数据库 |
| Phase 4 | `phases/phase-4.md` | reader_profile嵌入 |
| Phase 5 | `phases/phase-5.md` | 数值体系模板 |
| Phase 6 | `phases/phase-6.md` | 超越性硬检查 |

## 质量标准与版本

参见 `references/质量标准.md` | `references/版本历史.md` | `references/产出目录结构.md`

<pop-category>bootstrap</pop-category>
<pop-position>1</pop-position>
