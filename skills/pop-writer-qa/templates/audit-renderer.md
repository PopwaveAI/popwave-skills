# Audit Agent 项目全量对齐审计模板

> 基准：`skills/expert-writer/references/pipeline-arch.md`（全链路总览 + S/D/M 矩阵 + 规范目录树）
> 输入：项目根目录 + project.yaml
> 产出：结构化 Gap Report。不评分、不给建议、不评价设计。

---

## 前提

- 项目根目录已指定（project.yaml 的 `workspace_root` 或用户提供）
- pipeline-arch.md 已加载（Get-Content -Encoding UTF8 -Raw）
- project.yaml 已读入

---

## A. 文件树完整性

以 pipeline-arch.md §二「规范目录树」为基准，逐目录比对。

```
基准目录            → 实际文件               → 判定
─────────────────────────────────────────────────────────
00-总控/            → [列出]                → ✅/⚠️/❌
创意种子/          → [列出]                → ✅/⚠️/❌
状态/角色/          → [列出]                → ✅/⚠️/❌
状态/势力/          → [列出]                → ✅/⚠️/❌
状态/卷摘要/        → [列出]                → ✅/⚠️/❌
状态/世界状态.md    → [有/无]               → ✅/⚠️/❌
设计/全书架构.md    → [有/无]               → ✅/⚠️/❌
剧情设计/卷/        → [列出]                → ✅/⚠️/❌
剧情设计/幕/vol-*/      → [列出]                → ✅/⚠️/❌
章节设计包/        → [N个文件]             → ✅/⚠️/❌
章节设计包/文风DNA/ → [列出]                → ✅/⚠️/❌
写作资产/锚定章库/  → [列出]                → ✅/⚠️/❌
正文/               → [N个文件]             → ✅/⚠️/❌
```

判定：✅ 存在且对齐 / ⚠️ 存在但路径/命名偏离 / ❌ 缺失

---

## B. 工程级文件质量审查

> ⚠️ 边界：仅审查工程层面文件。单章产物（chXXX-设计包 / chXXX.md）不逐文件读入，仅在 A 中计数验证一致性。

逐文件读入，判断是否达到对应 skill 的产出标准：

| 文件 | 应来自 | 检查项 |
|:-----|:------|:------|
| story-engine.yaml | pop-writer-creative | core_premise 等关键字段存在？ |
| L1-01~06 | bookstrap P1 | 六件套互不重复？有交叉引用标记？ |
| project.yaml | bookstrap P3 | paths / reader_profile / phase_progress 字段齐全？ |
| 状态/角色/角色卡 | bookstrap P3 → plot 回写 | core_desire(external_goal+internal_need)？快照段预留？ |
| 数值体系 x4 | bookstrap P5 | 4 个 YAML 全部存在？字段结构合理？ |
| 起点/终点快照 | bookstrap P6/7 | 时间/位置/等级/矛盾/已知信息等维度？ |
| 设计/全书架构.md | plot P0 | 卷拆分/地理全图/角色出场/主线全览/钩子？ |
| 剧情设计/卷/XX.md | plot S1 | 四节齐全？§〇 全书隶属段存在？ |
| 剧情设计/幕/vol-XX/act-YY.yaml | plot S2 | info_release_plan 段？Canvas 矩阵有 rhythm_check？有章级切片？ |
| entity-snapshot.yaml | pop-writer-chapter | _meta.total_chapters 与目录文件数一致？ |
| 写作资产/文风DNA/ | deconstructor/pop-shared-dna | 含原文证据 + 规则？ |

单章产物一致性：章节数 = 设计包数 = entity-snapshot.total_chapters？

---

## C. 管线阶段对齐

| project.yaml#phase | 应有文件 |
|:-------------------|:--------|
| bootstrapped | bookstrap 全产出 + 快照用户确认 |
| plotted | 全书架构 + volume-XX × 当前卷 + act-YY × 当前幕 |
| writing | 设计包对齐章节号 + entity-snapshot 章数一致 |
| paused | 暂停原因已记录 |

---

## D. 文件分类正确性

以 pipeline-arch.md §一 S/D/M 矩阵为基准：

| 文件 | 基准类型 | 实测 | 判定 |
|:-----|:--------|:----|:----:|
| story-engine.yaml | S | 是否未被后续修改？ | ✅/⚠️ |
| 状态/角色/角色卡 | D | 是否在卷末被回写？ | ✅/⚠️ |
| entity-snapshot.yaml | D | 是否逐章更新？ | ✅/⚠️ |

---

## 输出格式

```
# 项目全量对齐审计 — {项目名}

> {时间} · 基准: PRD v1.4 + pipeline-arch.md · 阶段: {phase}

## A. 文件树完整性
| 目录 | 判定 |
|:-----|:----:|
| ... | ✅/⚠️/❌ |
缺失: {list}

## B. 工程级文件质量
| 文件 | 判定 | 问题 |
|:-----|:----:|:-----|
| ... | ✅/⚠️/❌ | ... |

## C. 管线阶段对齐
阶段: {phase} · 完整性: {判定}
缺失: {list}

## D. 文件分类正确性
| 文件 | 判定 |
|:-----|:----:|
| ... | ✅/⚠️ |

## Gap Summary
| 严重度 | 数量 | 关键项 |
|:------|:---:|:------|
| ❌ 阻断 | N | ... |
| ⚠️ 偏离 | N | ... |
```
