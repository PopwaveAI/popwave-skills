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

| 场景 | 模式 | 说明 |
|------|:----:|------|
| **新书开坑** | `forward` | 从零到一搭建完整的小说项目骨架 |
| **创意可行性验证** | `forward` | 不确定创意能不能撑起长篇，需系统检验 |
| **已有正文需续写** | `reverse` | 已有 N 章正文但无标准设计层，逆向提取设定再续写 |
| **设定规范化** | `forward` | 已有零散设定，需结构化、分层化、标准化 |

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

## 模式选择

本 skill 支持两种运行模式：

| 模式 | 入口相位 | 适用场景 |
|:-----|:---------|:---------|
| **`forward`** | Phase 0（正向设计） | 新书开坑、从零设定 |
| **`reverse`** | Phase r1（逆向工程） | 已有正文需续写、从正文提取设定 |

**`forward`** 走标准相位 0→0.3→0.4→0.5→1→1.2→1.3→1.5→2→3→4→5→6

**`reverse`** 走逆向相位 r1→r2→r3→r4→r5→r6

---

## Forward 相位索引（新书开坑）

| Phase | 执行 | 参考 | 说明 |
|:------|:-----|:-----|:------|
| Phase 0 | `phases/phase-0.pe.md` | `phases/phase-0.ref.md` | 灵魂对齐 + PRD + 压力测试 |
| Phase 0.3 | `phases/phase-0.3.pe.md` | `phases/phase-0.3.ref.md` | 参考书筛选 + 拆解 + 差异化 |
| Phase 0.4 | `phases/phase-0.4.pe.md` | `phases/phase-0.4.ref.md` | 金手指设计 + 评估框架 |
| Phase 0.5 ★ | `phases/phase-0.5.pe.md` | `phases/phase-0.5.ref.md` | 跨域素材聚合（强制） |
| Phase 1 | `phases/phase-1.pe.md` | `phases/phase-1.ref.md` | L1六件套骨架 |
| Phase 1.2 ★ | `phases/phase-1.2.pe.md` | `phases/phase-1.2.ref.md` | L1深度展开 |
| Phase 1.3 ★ | `phases/phase-1.3.pe.md` | — | L1交叉关联矩阵 |
| Phase 1.5 | `phases/phase-1.5.pe.md` | — | 世界稳定性检验 |
| Phase 2 | `phases/phase-2.pe.md` | — | L2卷级展开 + 爽点设计 |
| Phase 3 | `phases/phase-3.pe.md` | `phases/phase-3.ref.md` | 项目骨架 + 模板产出 |
| Phase 4 | `phases/phase-4.pe.md` | — | reader_profile嵌入 |
| Phase 5 | `phases/phase-5.pe.md` | `phases/phase-5.ref.md` + `references/网文力量体系大全.md` | 数值体系 |
| Phase 6 | `phases/phase-6.pe.md` | — | 超越性硬检查 |

## Reverse 相位索引（续写适配）

| Phase | 执行 | 参考 | 说明 |
|:------|:-----|:-----|:------|
| Phase r1 | `phases/phase-r1.pe.md` | `phases/phase-r1.ref.md` | 逆向工程：逐章事件日志 |
| Phase r2 | `phases/phase-r2.pe.md` | `phases/phase-0.ref.md` | L0产品层提取（含 reader_profile） |
| Phase r3 | `phases/phase-r3.pe.md` | `phases/phase-1.ref.md` | L1元设定层提取 |
| Phase r4 | `phases/phase-r4.pe.md` | `phases/phase-3.ref.md` | 宪法提取 |
| Phase r5 | `phases/phase-r5.pe.md` | — | 卷大纲确认 |
| Phase r6 | `phases/phase-r6.pe.md` | — | 交接验证 |

> reverse 模式的产出格式与 forward 完全一致。走完 reverse 后，项目状态等同于新书走完 forward。`pop-novel-master` 感知不到区别。

---

## 参考文件索引

以下参考文件（`.ref.md`）在执行对应 Phase 前自动加载：

| 文件 | 包含内容 |
|:-----|:---------|
| `phases/phase-0.ref.md` | PRD六要素、灵魂三问示例、压力测试判断标准 |
| `phases/phase-0.3.ref.md` | 四维度分析模板、差异化决策三元组 |
| `phases/phase-0.4.ref.md` | 四级评估质量标准、文化根系检查、番茄验证标准 |
| `phases/phase-0.5.ref.md` | 六大搜索领域、种子蒸馏模板、量化自查表 |
| `phases/phase-1.ref.md` | L1六件套覆盖内容定义、核心矛盾总纲 |
| `phases/phase-1.2.ref.md` | 各文件深度标准表（字数/子维度门槛） |
| `phases/phase-3.ref.md` | project.yaml / chapter-state.yaml / constitution.yaml 完整schema |
| `phases/phase-5.ref.md` | 四段框架总览表、断级差标准、跨级战约束 |
| `phases/phase-r1.ref.md` | 逐章事件日志模板、批次摘要格式 |
| `references/网文力量体系大全.md` | 20+经典体系深度拆解、赛道匹配指南、十大设计戒律 |

<pop-category>bootstrap</pop-category>
<pop-position>1</pop-position>
