# Skill 规范化重构计划

> 目标：将全部 28 个 skill 按 v5 规范对齐（目录结构 + SKILL.md 格式 + metadata）
> 范围：所有 skill，分批执行
> 原则：不改变 SKILL.md 的逻辑内容，只改结构和格式

---

## 0. 当前状态总览

### 已对齐（3 个，不在此计划内）

| skill | 理由 |
|-------|------|
| `pop-skill-create` | 刚修完：steps/ + 红线表 + 边界 + 落盘 + WRONG |
| `09-pop-novel-chapter-design` | 刚修完：红线表 + 速查表5列 + 边界 + 落盘 + WRONG |
| `02-pop-novel-deconstructor` | 刚修完：红线表 + ETL红线 + boundary + WRONG |

### 需重构（25 个）

按 SKILL.md 行数和结构复杂度分级：

```
Tier A（~30min）:  4个行数<150 的结构基本可用的 skill
Tier B（~1h）:    8个行数150-300 的结构半对齐的 skill  
Tier C（~2h）:    7个行数>300 或长期未维护的大 skill
Tier D（独立）:   6个工具/支撑 skill
```

---

## 1. Tier A — 轻量修补（4 个）

这些 skill 已有较好结构，缺少数个 v5 强制要素。

### 01-download-webnovel-txt（129 行）

| 缺什么 | 补什么 |
|:-------|:-------|
| ❌ CHANGELOG.md 不存在 | 创建，根据 SKILL.md 版本行推第一条 |
| ❌ 缺少 steps/ 目录 | 创建，从 SKILL.md 主流程拆出 1 个 step 文件 |
| ❌ 缺少落盘检查点 | 追加表格 |
| ❌ 指向 steps/ 的引用 | SKILL.md 核心流程段改指向 steps/ |
| ❌ skill.json 缺 pipeline 字段 | 补 `{ downstream: ["pop-deconstructor"] }` |

### 05-pop-novel-creative（151 行）

| 缺什么 | 补什么 |
|:-------|:-------|
| ❌ 缺少 WRONG 示例 | 追3条（从 changelog 或实际 agent 错误中提取） |
| ❌ 缺少模板目录 | 创建 templates/（它有 phases/ 变体 W0/W1/Phase0/0.3/0.4/0.5 → 有产出模板） |
| ❌ skill.json 缺 pipeline | 补 `{ downstream: ["pop-world"] }` |

### 06-pop-novel-world（117 行）

| 缺什么 | 补什么 |
|:-------|:-------|
| ❌ 缺少 WRONG 示例 | 追3条 |
| ❌ 缺少模板目录 | 创建 templates/（L1六件套的产出模板） |
| ❌ skill.json 缺 pipeline | 补 `{ upstream: ["pop-creative"], downstream: ["pop-plot"] }` |

### 07-pop-novel-continue（107 行）

| 缺什么 | 补什么 |
|:-------|:-------|
| ❌ CHANGELOG.md 不存在 | 创建 |
| ❌ 缺少 WRONG 示例 | 追3条（已有1条，不够） |
| ❌ skill.json 缺 pipeline | 补 `{ upstream: ["pop-world"], downstream: ["pop-plot"] }` |

---

## 2. Tier B — 中等重构（8 个）

### 03-pop-dna（206 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 红线格式非表格 | checklist 格式 → `| # \| 红线 \|` 表格 |
| ❌ 缺落盘检查点 | 追加 |
| ❌ 缺 steps/ 目录 | 创建，步骤0~4 从 SKILL.md 拆到 `steps/step-0-sampling.md` 等 5 个文件 |
| ❌ SKILL.md 核心流程段改指向 steps/ | 每步加 `详细指令 → steps/step-N.md` |
| ❌ v4 vs v3 变化表太长 | 缩到 3 行或直接移到 CHANGELOG |
| ❌ skill.json 缺 pipeline | 补 |

### 04-pop-novel-character-schema（256 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ 目录 | 创建（有 schema/ + examples/ + references/，但无可执行 steps/） |
| ❌ 缺落盘检查点 | 追加 |
| ❌ SKILL.md 过长 | 方法论（选级规则）→ references/；SKILL.md 只留路由+速查+红线+指向 |
| ❌ schema/ 目录 → references/ | schema/Lv4-core.md → references/Lv4-core.md（v5 说 schema 是角色系统 skill 的事） |
| ❌ skill.json 缺 pipeline | 补 |

### 08-pop-novel-plot（213 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 红线格式非表格 | checklist 改 `| # \| 红线 \|` |
| ❌ 速查表缺「读什么」列 | 追加文件路径列 |
| ❌ 缺落盘检查点 | 已有产出段落 → 格式化 |
| ❌ templates/ volume-design 无 .tpl 后缀 | 不改内容，加后缀或注释（视消费端决定） |
| ❌ skill.json 缺 pipeline | 补 |

### 10-pop-novel-prose-render（176 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 红线格式非表格 | checklist 红线 → 表格 |
| ❌ 缺落盘检查点 | 已有产出物段落 → 格式化为表格 |
| ❌ skill.json 缺 pipeline | 补 |

### 11-pop-novel-qa（187 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ 目录 | 创建，L1 硬门禁 + L2 感觉型两层各拆一步 |
| ❌ prompt-templates/ 目录 → templates/ | 重命名目录 |
| ❌ SKILL.md 缺指向 steps/ | 补引用 |
| ❌ skill.json 缺 pipeline | 补 |

### 12-pop-novel-html-renderer（165 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ 目录 | 创建 |
| ❌ 缺落盘检查点 | 追加 |
| ❌ SKILL.md 缺指向 steps/ | 补 |
| ❌ skill.json 缺 pipeline | 补 |

### 13-pop-novel-game（406 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ method/ 中文目录名 | → references/ |
| ❌ 缺 steps/ 目录 | 创建，按执行流程拆 |
| ❌ SKILL.md 过长（406行） | 方法论→ references/，步骤→ steps/，SKILL.md 缩到 ≤150 行 |
| ❌ 缺落盘检查点 | 追加 |
| ❌ 缺指向 steps/ 引用 | 补 |
| ❌ skill.json 缺 pipeline | 补 `{ upstream: ["pop-prose-render"] }` |

### expert-writer（~600 行 → ~100 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ SKILL.md 太长 | Think→Execute→Reflect 各下一步到 `steps/step-1-think.md` 等 |
| ❌ 路由表硬编码32处 | 加读 registry.json 的逻辑 |
| ❌ 5个路由文件手动同步 | POP-CALL.md POP-ROUTER.md typical-paths.md pipeline-arch.md 保留但 SKILL.md 只引用 |
| ❌ 红线格式非表格 | 补齐 |
| ❌ 身份声明在 SKILL.md | → `_shared/pop/identity.md` |
| ❌ skill.json 缺 pipeline | 补（无 upstream/downstream，但标记自身为 expert） |

---

## 3. Tier C — 大部头重构（7 个）

### pop-book-promo（339 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建，按管线拆 3-4 步 |
| ❌ SKILL.md 过长，方法论内嵌 | → references/ |
| ❌ 缺红线表格 | 补 |
| ❌ 缺落盘检查点 | 补 |
| ❌ 缺 CHANGELOG.md 引用 | 补 |
| ❌ 缺指向 steps/ | 补 |

### pop-html-anything（592 行 — 最长的）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建 |
| ❌ SKILL.md 592行 → ≤200行 | 拆到 steps/，方法论链 → references/ |
| ❌ _design/ 和 _tooling/ 目录 | → references/ 或 templates/ |
| ❌ 缺红线表格 | 补 |
| ❌ 缺落盘检查点 | 补 |
| ❌ 缺指向 steps/ | 补 |

### pop-reader-making（297 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ method/ 中文目录 → references/ | 重命名 |
| ❌ 缺 steps/ | 创建 |
| ❌ SKILL.md 内嵌方法论 | → references/ |
| ❌ 缺红线表格 | 补 |
| ❌ 缺落盘检查点 | 补 |

### pop-seo-anything（469 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建 |
| ❌ SKILL.md 过长 | 拆 steps/，方法论 → references/ |
| ❌ 缺红线表格 | 补 |
| ❌ 缺落盘检查点 | 已有 → 格式化 |
| ❌ 缺指向 steps/ | 补 |

### pop-YouTubewebbuilder（295 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建 |
| ❌ qa-output/ style-refs/ 目录 | → references/ |
| ❌ 缺红线表格 | 补 |
| ❌ 缺落盘检查点 | 已有 → 格式化 |
| ❌ 缺指向 steps/ | 补 |

### book-to-skill（373 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建 |
| ❌ SKILL.md 过长 | 拆 |
| ❌ 缺红线表格 | 补 |
| ❌ 缺落盘检查点 | 补 |
| ❌ tools/ 目录名 → scripts/ | 重命名 |
| ❌ 缺指向 steps/ | 补 |

### feishu-docs（426 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建 |
| ❌ SKILL.md 过长 | 拆 |
| ❌ 缺红线表格 | 补 |
| ❌ 缺落盘检查点 | 补 |
| ❌ 缺指向 steps/ | 补 |

---

## 4. Tier D — 工具 skill（6 个）

轻量修补为主。

### cnovel-research（297 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建 |
| ❌ tools/ 目录 → scripts/ | 重命名 |
| ❌ 缺红线表格 + 落盘 | 补 |
| ❌ 缺指向 steps/ | 补 |

### book-opinion-tracker（157 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ tools/ 目录 → scripts/ | 重命名 |
| ❌ 缺 steps/ | 创建 |
| ❌ 缺落盘检查点 | 补 |
| ❌ 缺指向 steps/ | 补 |

### knowledge-downloader（329 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建 |
| ❌ SKILL.md 过长 | 拆 steps/ |
| ❌ 缺红线表格 | 补 |
| ❌ 缺落盘检查点 | 已有 → 格式化 |
| ❌ 缺指向 steps/ | 补 |

### fanqie-skill（199 行, 无 skill.json）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 无 skill.json | 创建 |
| ❌ 无 CHANGELOG | 创建 |
| ❌ 无 steps/ | 创建 |
| ❌ 无红线表格 | 补 |
| ❌ 无边界条件表 | 补 |
| ❌ 缺落盘检查点 | 补 |

### web-access（144 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建 |
| ❌ 缺落盘检查点 | 补 |
| ❌ 缺指向 steps/ | 补 |

### prd-builder（238 行）

| 问题 | 改法 |
|:-----|:-----|
| ❌ 缺 steps/ | 创建 |
| ❌ SKILL.md 过长 | 方法论→ references/, 步骤→ steps/ |
| ❌ 缺红线表格 | 补（现在使用流程描述而非禁令） |
| ❌ 缺落盘检查点 | 补 |
| ❌ 缺指向 steps/ | 补 |

---

## 5. 施工顺序

```
Phase 1: Tier A（4个）→ 30min 每个
Phase 2: Tier B（8个）→ 1h 每个  
Phase 3: Tier C（7个）→ 2h 每个
Phase 4: Tier D（6个）→ 30min 每个
Phase 5: npm run skills:validate 全量验证
```

每 Tier 内按 SKILL.md 行数从小到大做。不做并行（避免依赖关系混乱）。

每完成一个 skill 执行 `npm run skills:validate` 确认不破坏构建。

---

## 6. 不做的事

| 不做 | 原因 |
|:-----|:-----|
| 不重写 SKILL.md 逻辑内容 | PRD ❌1：迁移只动结构命名 metadata |
| 不改编号前缀（本次不做目录重命名） | 那是 PRD Phase 2 的工作，独立 PR |
| 不改 `pop-novel-X` → `pop-X` | 同上 |
| 不合并 creative/world/continue → bookstrap | 独立 PRD 的活 |
| 不改 registry.json 引用 | 目录名不变，引用不动 |
