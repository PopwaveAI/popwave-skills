---
name: pop-novel-qa
pipeline:
  upstream: [expert-writer]
  downstream: []
description: "项目审计 / 全量对齐检查 / 文件体检 触发：以 pipeline-arch.md 为基准，对项目做四维工程级扫描（文件树/文档质量/管线阶段/分类正确性），输出 Gap Report。不评分、不给建议——只回答「有没有」和「对齐了吗」。"
---

# 项目全量对齐审计

> 版本：v1.0.0 | 2026-06-11

## 定位

**单一目的**：对整个项目做一次工程层面的合规扫描。以 `pipeline-arch.md` 为唯一基准，逐目录、逐文件检查项目是否符合全链路规范。

不审正文内容。不回答"读起来怎么样"——那是写作流程中的环节，交由具体写作 skill 的自检环节处理。

---

## 什么时候用

| 触发 | 说明 |
|:-----|:-----|
| 「审项目」「审计」「体检」「对齐检查」 | 显式要求时执行 |
| 开书完成后 | 用户说"开书完了" → 建议审计 |
| 每卷完成后 | 卷末做一次全局对齐确认 |
| 怀疑文件不对齐时 | 用户说"我感觉少东西了" |

---

## 前置条件

- [ ] 项目根目录已指定（project.yaml 路径或用户提供）
- [ ] `expert-writer/references/pipeline-arch.md` 存在且已加载
- [ ] project.yaml 已读入

---

## 执行流程

```
Step 1　读入基准
  ├─ Get-Content -Encoding UTF8 -Raw '{skill_root}/../expert-writer/references/pipeline-arch.md'
  ├─ 读入 project.yaml → 提取 phase / paths / reader_profile
  └─ 扫描项目根目录 → 列出全部文件

Step 2　四维扫描
  ├─ A. 文件树完整性 — 以 pipeline-arch.md §二 为基准，逐目录比对
  ├─ B. 工程级文件质量 — 逐文件读入，检查是否达标（不碰单章产物）
  ├─ C. 管线阶段对齐 — project.yaml#phase vs 实际文件
  └─ D. 文件分类正确性 — pipeline-arch.md §一 S/D/M 矩阵对照

Step 3　输出 Gap Report
  └─ 按 audit-renderer.md 模板格式化 → 输出
```

> 输出模板 → `prompt-templates/audit-renderer.md`
>
> 加载方式：`Get-Content -Encoding UTF8 -Raw`，不用 Read 工具。

---

## 四维详解

### A. 文件树完整性

以 pipeline-arch.md §二 目录树为准，逐目录比对：

| 基准目录 | 检查什么 |
|:---------|:---------|
| 00-总控/ | project.yaml + entity-snapshot.yaml + 数值体系/ x4 |
| 00-原始设定/ | L0-产品层/ + L1-元设定层/ + 起点/终点快照 |
| 状态/ | 角色/ + 势力/ + 卷摘要/ + 世界状态.md |
| 设计/ | 全书架构.md + 卷/volume-XX + 幕/vol-XX/act-YY |
| 写作资产/ | 设计包/ + 文风DNA/ + 锚定章库/ |
| 正文/ | chXXX.md 数量 |

每个目录输出：✅ 齐全 / ⚠️ 部分缺失 / ❌ 完全缺失

### B. 工程级文件质量

逐文件读入，回答"这个文件有没有达到对应 skill 要求的质量标准"。

| 文件 | 最低检查标准 |
|:-----|:------------|
| story-engine.yaml | 含 core_premise |
| L1-01~06 | 六件套互不重复，有交叉引用 |
| project.yaml | paths/reader_profile/phase_progress 字段齐全 |
| 状态/角色/角色卡 | core_desire(external_goal+internal_need) + 快照段预留 |
| 数值体系 x4 | 4 个 YAML 存在，字段结构合理 |
| 起点/终点快照 | 时间/位置/等级/矛盾/已知信息 维度齐全 |
| 设计/全书架构.md | 卷拆分/地理全图/角色出场/主线全览 |
| volume-XX.md | 四节齐全，§〇 全书隶属段存在 |
| act-YY.yaml | info_release_plan 段 + Canvas 矩阵 + 章级切片 |
| entity-snapshot.yaml | _meta.total_chapters 与文件数一致 |
| 文风DNA/ | 含原文证据 + 规则 |

> 不逐文件审查单章产物（设计包 / 正文），仅在 A 中做计数一致性验证。

### C. 管线阶段对齐

| project.yaml#phase | 应有文件 | 不做 |
|:-------------------|:--------|:-----|
| bootstrapped | bookstrap 全产出 + 快照用户确认 | — |
| plotted | 全书架构 + volume-XX + act-YY | — |
| writing | 设计包章节号对齐 + entity-snapshot 章数一致 | — |
| paused | 暂停原因已记录 | — |

### D. 文件分类正确性

以 pipeline-arch.md §一 S/D/M 矩阵为准，重点检查：
- **S 型文件**是否被意外修改？
- **D 型文件**是否有应有的维护者？
- **M 型文件**是否保持一致？

---

## 输出

按 `audit-renderer.md` 模板格式化，生成 Git 风格的 Gap Report：

```
# 项目全量对齐审计 — {项目名}
...
## A. 文件树完整性
## B. 工程级文件质量
## C. 管线阶段对齐
## D. 文件分类正确性
## Gap Summary
```

报告不存盘。是否保留由用户决定。

---

## 版本 v1.0.0 | 2026-06-11 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)
