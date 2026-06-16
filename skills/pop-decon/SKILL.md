---
name: pop-decon
description: "Orchestrator for novel deconstruction pipeline. Executes Phase 1 (design-pack) → Phase 2 (volume) → Phase 3 (setting). Routes to sub-skills based on scope (first N chapters vs full book)."
version: 13.2.0
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
| **前N章** | 用户指定（默认前100章） | Phase 1 → 2 → 3 | design-pack → volume → setting | ~1-3h |
| **全书** | 全部章节 | 同上，覆盖更完整 | 同上 | ~3-8h |

---

## 管线地图

```
用户: "拆这本书"
    ↓
pop-decon (orchestrator)
    ├── 判断量级: 前N章 or 全书
    │   └── 判断语言: 中文网文 → 手动 ETL；英文 → extract.py
    │
    ├── Phase 1: pop-decon-design-pack   → ETL → 拆分 → 5章一批设计包
    ├── Phase 2: pop-decon-volume        → 幕纲/卷纲（不足100章不跑）
    └── Phase 3: pop-decon-setting       → L1六件套+宪法+数值
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
**❌ 门禁：** `写作资产/设计包/` 为空 → 退回。

### Step 3：Phase 2 — 幕纲卷纲
**做什么：** 调用 `pop-decon-volume`。从设计包数据中识别卷边界、幕边界、剧情线。**不足100章不跑此Phase。**
**❌ 门禁：** 设计包产出缺失 → 退回 Phase 1。

### Step 4：Phase 3 — 设定世界观
**做什么：** 调用 `pop-decon-setting`。归纳 L1 六件套 + 宪法 + 数值。
**❌ 门禁：** 卷幕产出缺失 → 退回 Phase 2。

### Step 5：完成后引导
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

v13.2.0 | 2026-06-15 | 添加中文网文手动 ETL 引导（Phase 1），Phase 2 门禁明确标注不足100章不跑

---

## 参考文件

| 文件 | 用途 |
|:-----|:------|
| `scripts/extract.py` | 英文小说 ETL 脚本（中文 TXT 不走此脚本） |
| `references/output-quality-standards.md` | 各 Phase 产出物的质量门禁标准（含 L1/L2/L3 分级） |