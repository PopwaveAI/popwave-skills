# Audit Agent 项目全量对齐审计模板

> 基准：`skills/expert-writer/references/pipeline-arch.md`（全链路总览 + S/D/M 矩阵 + 规范目录树）
> 输入：项目根目录路径 + project.yaml
> 产出：一份结构化的 Gap Report，不分级、不给建议、只记录事实

---

## 前提条件

- 项目根目录已指定（project.yaml 的 `workspace_root` 或用户提供）
- pipeline-arch.md 已加载（Get-Content -Encoding UTF8 -Raw）
- project.yaml 已读入（获取 reader_profile、paths、phase 信息）
- 不评价设计好坏，只回答「有没有」和「对齐了吗」

---

## 审计维度

### A. 文件树完整性

以 pipeline-arch.md §二「规范目录树」为基准，逐目录比对：

```
基准目录            → 实际存在的文件           → 结果
─────────────────────────────────────────────────────────
00-总控/            → [列出实际文件]           → ✅/⚠️/❌
00-原始设定/        → [列出实际文件]           → ✅/⚠️/❌
状态/角色/          → [列出实际文件]           → ✅/⚠️/❌
状态/势力/          → [列出实际文件]           → ✅/⚠️/❌
状态/卷摘要/        → [列出实际文件]           → ✅/⚠️/❌
状态/世界状态.md    → [存在/不存在]            → ✅/⚠️/❌
设计/全书架构.md    → [存在/不存在]            → ✅/⚠️/❌
设计/卷/            → [列出实际文件]           → ✅/⚠️/❌
设计/幕/vol-*/      → [列出实际文件]           → ✅/⚠️/❌
写作资产/设计包/    → [列出实际文件]           → ✅/⚠️/❌
写作资产/文风DNA/   → [列出实际文件]           → ✅/⚠️/❌
写作资产/锚定章库/  → [列出实际文件]           → ✅/⚠️/❌
正文/               → [列出实际文件]           → ✅/⚠️/❌
```

判定规则：
- ✅ = 文件存在且路径对齐
- ⚠️ = 文件存在但路径/命名偏离规范
- ❌ = 缺失（当前阶段应有但没有）

---

### B. 文档质量逐件审查

对每个存在的产出文件，读入内容并回答以下问题：

| 文件 | 应来自哪个 Skill | 读入后判断 |
|:-----|:----------------|:----------|
| story-engine.yaml | bookstrap Phase 0 | 含 core_premise/reader_profile 等关键字段？ |
| L1-01~06 | bookstrap Phase 1 | 六件套内容互不重复？有交叉引用标记？ |
| project.yaml | bookstrap Phase 3 | 含 paths/reader_profile/phase_progress？路径字段对齐 v1.4？ |
| 状态/角色/角色卡 | bookstrap Phase 3 → plot 回写 | 含 core_desire(external_goal+internal_need)？有快照段预留位？ |
| 数值体系 x4 | bookstrap Phase 5 | 文件完整（4个YAML）？字段结构合理？ |
| 起点/终点快照 | bookstrap Phase 6/7 | 含时间/位置/等级/矛盾/已知信息等维度？ |
| 设计/全书架构.md | plot Phase 0 | 含卷拆分/地理全图/角色出场/主线全览/钩子？ |
| 设计/卷/volume-XX.md | plot Step 1 | 含四节（定义/快照/背景/剧情线）？§〇全书隶属段存在？ |
| 设计/幕/vol-XX/act-YY.yaml | plot Step 2 | 含 info_release_plan 段？Canvas 矩阵有 rhythm_check？有章级切片？ |
| 写作资产/设计包/chXXX-设计包.md | chapter-design Step 3 | 含事件链（每事件有冲突层次）？事件数 ≥ 字数÷200？ |
| entity-snapshot.yaml | chapter-design Step 3 | _meta.total_chapters 与正文数一致？ |
| 正文/chXXX.md | prose-render Step 4 | 含章末状态更新块？字数在目标范围内？ |
| 写作资产/文风DNA/ | deconstructor/pop-dna | 含原文证据 + 规则？有试写验证？ |

每个文件输出一行的审查结论：

```
{文件路径}  ✅ 合格 / ⚠️ {具体问题} / ❌ {缺失原因}
```

---

### C. 管线阶段对齐

| 当前 phase（来自 project.yaml） | 检查 |
|:-------------------------------|:-----|
| bootstrapped | bookstrap 产出全部齐全？起点/终点快照用户已确认？ |
| plotted | 全书架构 + volume-XX × 当前卷 + act-YY × 当前幕 齐全？ |
| writing | 设计包对齐当前章节号？entity-snapshot 章数一致？ |
| paused | 暂停原因已记录？精读闸门状态？ |

输出阶段判断：
```
当前阶段: {phase}
阶段完整性: ✅ 全部就位 / ⚠️ 部分缺失 / ❌ 关键文件缺失
缺失项:
  - {文件}: {缺少什么}
  - ...
```

---

### D. 文件分类正确性

以 pipeline-arch.md §一「S/D/M 矩阵」为基准，检查每个文件的类型标注是否与实际一致：

| 文件 | 基准类型 | 实际情况 | 判定 |
|:-----|:--------|:--------|:----:|
| story-engine.yaml | S | 是否未被后续修改？ | ✅/⚠️ |
| 状态/角色/角色卡 | D | 是否在卷末被回写？快照段是否更新？ | ✅/⚠️ |
| entity-snapshot.yaml | D | 是否逐章更新？_meta.total_chapters 递增？ | ✅/⚠️ |
| 正文/chXXX.md | D | 是否含章末状态更新块？ | ✅/⚠️ |

---

## 输出格式

```
# 项目全量对齐审计报告 — {项目名}

> 审计时间: {timestamp}
> 基准版本: PRD v1.4 + pipeline-arch.md
> 当前阶段: {phase}

---

## A. 文件树完整性

| 目录 | 基准 | 实际 | 判定 |
|:-----|:-----|:-----|:----:|
| ... | ... | ... | ✅/⚠️/❌ |

缺失项汇总：{list or "无"}

---

## B. 文档质量审查

| 文件 | 判定 | 问题 |
|:-----|:----:|:-----|
| ... | ✅/⚠️/❌ | ... |

---

## C. 管线阶段对齐

当前阶段: {phase} · 完整性: {判定}
缺失项: {list or "无"}

---

## D. 文件分类正确性

| 文件 | 判定 | 问题 |
|:-----|:----:|:-----|
| ... | ✅/⚠️ | ... |

---

## Gap Summary

| 优先级 | 数量 | 关键项 |
|:-------|:---:|:------|
| ❌ 阻断 | {n} | {前3项} |
| ⚠️ 偏离 | {n} | {前3项} |
| ✅ 合格 | {n} | — |

> 本报告不包含建议。修复方案由作者自行决定。
```
