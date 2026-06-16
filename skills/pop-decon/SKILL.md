---
name: pop-decon
description: "Orchestrator for novel deconstruction pipeline. Executes Phase 1 (design-pack) → Phase 2 (volume) → Phase 3 (setting) → Phase 4 (planned: creative trace). Routes to sub-skills based on scope (first N chapters vs full book)."
version: 13.3.0
author: Popwave
license: MIT
metadata:
  hermes:
    tags: [deconstruction, pipeline, orchestration, novel-analysis]
    related_skills: [pop-decon-design-pack, pop-decon-volume, pop-decon-setting]
---

# pop-decon · 拆书管线调度 v13.2.0

> **定位：拆书管线的元 skill。执行管线调度（Phase 1→3），不直接产出文件。**
> **核心约束：按章节量级决定管线长度。全管线顺序推进，不得跳号。**

---

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **不跳过 Phase** — 只能顺次推进 Phase 1→2→3→4，不得跳号 |
| ❌2 | **跳过清洗直接写设计包** — Phase 1 未完成不准进 Phase 2 |
| ❌3 | **编造事件** — 设计包事件必须有原文 chXX 证据 |
| ❌4 | **子 skill 不可用时静默跳过** — 找不到子 skill → 终止，告知用户 |
| ❌5 | **中文网文硬跑 extract.py** — Phase 1 前必须判断源文件语言。中文 TXT 不支持 extract.py 章节检测 → 走手动 ETL |
| ❌6 | **产出物不经质量门禁直接交付** — 每个 Phase 的产出物必须对照质量标准表自检，不达标不准进下一 Phase |

---

## 速查表

| 量级 | 范围 | 执行管线 | 触发子 skill | 预期耗时 |
|:-----|:-----|:---------|:------------|:--------|
| **前N章** | 用户指定（默认前100章） | Phase 1 → 2 → 3（不足100章Phase 2跳过） | design-pack → volume → setting | ~1-3h |
| **全书** | 全部章节 | Phase 1 → 2 → 3 → 4 | design-pack → volume → setting → **trace** | ~3-9h |

---

## 管线地图

```
用户: "拆这本书"
    ↓
pop-decon (orchestrator)
    ├── 判断量级: 前N章 or 全书
    │   └── 判断语言: 中文网文 → 手动 ETL；英文 → extract.py
    │
    ├── Phase 1: pop-decon-design-pack   → ETL → 拆分 → 设计包v3 + 套路库
    │   └── ⚠️ 使用 delegate_task 批量提取时，不同子agent可能采用不同命名/
    ├── Phase 1: pop-decon-design-pack   → ETL → 拆分 → 5章一批设计包
    ├── Phase 2: pop-decon-volume        → 幕纲/卷纲（不足100章不跑）
    ├── Phase 3: pop-decon-setting       → L1六件套+宪法+数值
    └── Phase 4: pop-decon-trace         → 创意溯源·跨域参考索引（新）
         ↑ Phase 4 目标：反向破译作者的创意参考版图
           （DND设定/LOTR地名/Frozen角色原型/网文套路等）
           这是 iceberg theory 的自然推论——
           设计包密度来自蒸馏原文（水面之上），
           但作者创作的"水下冰山"（跨域参考储备）需要单独反向破译。
           当前 Pipeline 无此环节，属于已知缺口。
```

每 Phase 产出 → 消费关系见各子 skill 的 `references/pipeline-context.md`。

---

## 核心流程

### Step 1：判断量级
**做什么：** 询问用户需要拆多少章。默认前100章，用户说"全本/全书/全部"=全书。
**❌ 门禁：** 用户未确认量级 → 退回询问。

### Step 2：Phase 1 — 设计包（强制前置）
**做什么：** 调用 `pop-decon-design-pack`。运行 extract.py → 按章拆分 → 5章一批 LLM 直接提取设计包。
**中文网文注意：** extract.py 不识别中文「第X章」格式。中文 TXT 文件需手动 ETL（详见 pop-decon-design-pack 的 `references/chinese-novel-etl.md`），agent 必须在 Phase 1 开始时判断源文件语言，选择 extract.py 或手动 ETL。
**❌ 门禁：** `写作资产/设计包v3/`（或 `设计包v2/`）为空 → 退回。

### Step 2.5：Phase 1 质量门禁（新增 — 不可跳过）
**做什么：** 在 Phase 1 完成后、Phase 2 开始前，强制执行一次全量质量门禁扫描。

| # | 检查项 | 通过标准 | 失败处理 |
|:-:|:-------|:---------|:---------|
| 1 | **覆盖率** | `设计包v3/` 文件数 = `_temp/chapters/` 文件数 | 缺文件 → 退回补充 |
| 2 | **命名一致性** | 全部文件名为 `chXXX-设计包.md`，无变体 | 不一致 → 退回修命名 |
| 3 | **首行模式** | 抽检后30%文件，首行匹配 `# 设计包 —` | 不匹配 → 标注低质量批次 |
| 4 | **事件密度** | 抽检后期5章，每章事件数≥5 | <5 → 低密度警告 |
| 5 | **Phase 2 前置条件** | 章节数 ≥ 100（否则不执行 Phase 2） | 不足100章 → 跳过，通知用户 |

**⏭ 跳过条件：** 仅当章节数 < 100 时可跳过 Phase 2。除此以外任何情况下不得跳过此门禁。

### Step 3：Phase 2 — 幕纲卷纲
**做什么：** 调用 `pop-decon-volume`。从设计包数据中识别卷边界、幕边界、剧情线。**不足100章不跑此Phase。**
**⏰ 调度时机：** Phase 1（设计包）+ 质量门禁完成后立即调度。不得因对话中断/用户切换话题而遗忘 Phase 2。如果 orchestartor 因用户提问而中断流程，在回答完用户问题后必须回到等待中的 Phase 2 调度点。
**❌ ❌ ❌ 历史教训：** 前次187章拆解后设计包全部产出完毕，但由于 orchestrator 未主动调度 Phase 2，volume-01.md 和 act-*.md 完全未产出，导致整套拆书产出物等级从「完整拆书」降级为「半成品设计包」。**Phase 2 必须作为 pipeline 的自动下一步执行，而非等待用户提示。**

### Step 4：Phase 3 — 设定世界观
**做什么：** 调用 `pop-decon-setting`。归纳 L1 六件套 + 宪法 + 数值。
**❌ 门禁：** 卷幕产出缺失 → 退回 Phase 2。

### Step 5：Phase 4 — 创意溯源（新增）

**做什么：** 调用 `pop-decon-trace`。从设计包+L1设定中反向破译作者的创意参考版图，产出跨域参考索引。

**核心红线：** 化用≠照抄。识别到索伦≈指环王索伦，不等于本作的索伦就是魔君。参考来源只是起点，创意转化才是重点。

**❌ 门禁：** Phase 3 未完成 → 退回。

### Step 6：完成后引导
输出摘要，告知用户产出位置，询问是否需要转换为写作项目。

---

## 边界条件

| 场景 | 处理 |
|:-----|:-----|
| 前N章跑完后用户要求升级全书 | 重新跑全书 design-pack → Phase 2-3 |
| extract.py 脚本不可用 | 若是中文 TXT，走手动 ETL；若是英文，终止并提示 Python 环境和依赖 |
| 子 skill SKILL.md 不可读 | 终止，输出具体哪个子 skill 缺失 |
| 用户中途改变量级 | 保存当前阶段产出，用户确认后再切 |
| 源文件编码不确定 | 中文 TXT 优先 GBK → GB18030 → UTF-8 |

---

## 版本

v13.3.0 | 2026-06-16 | Phase 4(creative trace)加入管线地图(计划中)。Iceberg theory设计原则文档化。delegate_task命名归一化警告。新增 Step 2.5 Phase 1质量门禁。Phase 2调度时机强制化。

v13.4.0 | 2026-06-16 | Phase 4 创意溯源正式实装。全书管线 Phase 1→2→3→4。Step 5 新增 Phase 4 调度。新子 skill `pop-decon-trace`。核心红线：化用≠照抄。新增前N章不足100章说明。

## 参考文件

| 文件 | 用途 |
|:-----|:------|
| `scripts/extract.py` | 英文小说 ETL 脚本（中文 TXT 不走此脚本） |
| `references/output-quality-standards.md` | 各 Phase 产出物的质量门禁标准（含 L1/L2/L3 分级） |