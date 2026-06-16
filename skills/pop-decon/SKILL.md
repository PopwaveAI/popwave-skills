---
name: pop-decon
description: "Orchestrator for novel deconstruction pipeline. Executes Phase 1 (design-pack) → Phase 2 (volume) → Phase 3 (setting) → Phase 4 (creative trace). Routes to sub-skills based on scope (first N chapters vs full book). Core philosophy: iceberg theory — extract the 1/8 above water, trace the 7/8 below."
version: 13.5.0
author: Popwave
license: MIT
metadata:
  hermes:
    tags: [deconstruction, pipeline, orchestration, novel-analysis]
    related_skills: [pop-decon-design-pack, pop-decon-volume, pop-decon-setting, pop-decon-trace]
---

# pop-decon · 拆书管线调度 v13.4.0

> **定位：拆书管线的元 skill。执行管线调度（Phase 1→4），不直接产出文件。**
> **核心约束：按章节量级决定管线长度。全管线顺序推进，不得跳号。**
>
> **冰山理论 · 拆书哲学**
>
> ```
> 水面之上（占文本的1/8）—— 我们能提取的：
>   ├── 事件链 ✓ (发生了什么)
>   ├── 关键对白 ✓ (说了什么)
>   ├── 套路识别 ✓ (作者选了的那个公式)
>   ├── 感官锚点 ✓ (实际写出来的画面)
>   └── 战斗数值 ✓ (属性/HP/伤害——但只是数字本身)
>
> 水面之下（占创作的7/8）—— 我们必须反向破译的：
>   ├── 作者调用了他储备的哪些跨域参考？  → Phase 4 创意溯源
>   ├── 数值体系的金字塔工程？              → 静态+动态表（数值体系反拆）
>   ├── 为什么选这个套路而非另一个？        → 套路库偏好分布
>   ├── 这个情节模板来自哪部作品的什么场景？ → 跨域参考索引
>   ├── 角色命名背后有文化原型吗？          → 专有名词溯源
>   └── 作者"感觉这里该这样写"的直觉从哪来？  → 持续积累
> ```
>
> **我们不是机械的1:1还原机器。** 每篇网文的水面之下都藏着一座冰山——作者读过的书、追过的番、玩过的游戏、浸染的文化土壤。好的拆书不止拆出"写了什么"，更拆出"从哪来、怎么变、为什么这样写"。
>
> **跨越冰山** = 从 Phase 1 的事件提取，走到 Phase 4 的创意溯源。从"看到文本"走到"看到作者"。

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
| **前N章** | 用户指定（默认前100章） | Phase 1→2→3（不足100章Phase 2跳过） | design-pack → volume → setting | ~1-3h |
| **全书** | 全部章节 | Phase 1→2→3→4 | design-pack → volume → setting → **trace** | ~3-9h |

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
    │   └── ⚠️ delegate_task 批量提取时，不同子agent可能用不同命名/格式
    │         → Phase 1 完成后必须执行 Step 2.6 命名归一化
    │
    ├── Phase 2: pop-decon-volume        → 幕纲/卷纲（Markdown）
    ├── Phase 3: pop-decon-setting       → L1六件套 + 宪法 + 数值
    └── Phase 4: pop-decon-trace         → 创意溯源·跨域参考索引
```

每 Phase 产出 → 消费关系见各子 skill 的 `references/pipeline-context.md`。

---

## 核心流程

### Step 1：判断量级
**做什么：** 询问用户需要拆多少章。默认前100章，用户说"全本/全书/全部"=全书。
**❌ 门禁：** 用户未确认量级 → 退回询问。

### Step 2：Phase 1 — 设计包（强制前置）
**做什么：** 调用 `pop-decon-design-pack`。运行 extract.py → 按章拆分 → 逐章或5章一批 LLM 提取设计包。
**中文网文注意：** extract.py 不识别中文「第X章」格式。中文 TXT 文件需手动 ETL（详见 pop-decon-design-pack 的 `references/chinese-novel-etl.md`）。
**❌ 门禁：** `写作资产/设计包v3/`（或 `设计包v2/`）为空 → 退回。

### Step 2.5：Phase 1 质量门禁（不可跳过）
**做什么：** 在 Phase 1 完成后、Phase 2 开始前，强制执行一次全量质量门禁扫描。

| # | 检查项 | 通过标准 | 失败处理 |
|:-:|:-------|:---------|:---------|
| 1 | **覆盖率** | `设计包v3/` 文件数 ≥ `_temp/chapters/` 文件数 × 95% | 缺太多 → 退回补充 |
| 2 | **命名一致性** | 全部文件名为 `chXXX-设计包.md`，无变体 | 不一致 → 先执行 Step 2.6 命名归一化，再重新检查 |
| 3 | **首行格式** | 抽检后30%文件，首行匹配 `# 设计包 —` | 不匹配 → 低质量警告 |
| 4 | **事件密度** | 抽检后期5章，每章事件数≥5 | <5 → 低密度警告 |
| 5 | **Phase 2 前置条件** | 章节数 ≥ 100（否则不执行 Phase 2） | 不足100章 → 跳过，通知用户 |

### Step 2.6：命名归一化（批量修正）

**执行时机：** Step 2.5 检查到命名不一致时强制执行。也可作为预防性步骤在 Phase 1 完成后无条件执行一次。

**做什么：** 扫描 `写作资产/设计包v3/` 目录，将所有设计包文件重命名为统一格式 `chXXX-设计包.md`。

**已知的命名变体（必须覆盖）：**

| 变体格式 | 例子 | 归一化后 |
|:---------|:-----|:---------|
| `chXXX_v3设计包.md` | `ch036_v3设计包.md` | `ch036-设计包.md` |
| `chXXX-v3设计包.md` | `ch171-v3设计包.md` | `ch171-设计包.md` |
| `v3_设计包_chXXX-chYYY.md` | `v3_设计包_ch111-ch115.md` | 拆分为5个单章文件并重新提取 |
| `chXXX-设计包-v3.md` | — | `chXXX-设计包.md` |

**批量重命名命令（bash）：**
```bash
cd 写作资产/设计包v3/
# Remove _v3 suffix
for f in *_v3设计包.md; do
  [ -f "$f" ] && mv "$f" "$(echo $f | sed 's/_v3设计包/-设计包/')"
done
# Remove -v3 suffix
for f in *-v3设计包.md; do
  [ -f "$f" ] && mv "$f" "$(echo $f | sed 's/-v3设计包/-设计包/')"
done
```

**批次文件处理：** 对于 `v3_设计包_chXXX-chYYY.md` 这类多章合一文件，不能简单重命名——必须拆分为单章文件后补全内容。标注"需人工干预"并通知用户。

**验证：** 重命名完成后重新执行 Step 2.5 的命名一致性检查。

### Step 3：Phase 2 — 幕纲卷纲
**做什么：** 调用 `pop-decon-volume`。从设计包数据中识别卷边界、幕边界、剧情线。**不足100章不跑此Phase。**
**⏰ 调度时机：** Phase 1 + 质量门禁完成后立即调度。不得因对话中断/用户切换话题而遗忘。
**❌ ❌ ❌ 历史教训：** 前次187章拆解后设计包全部产出完毕，但由于 orchestrator 未主动调度 Phase 2，volume-01.md 和 act-*.md 完全未产出，整套拆书降级为半成品。**Phase 2 必须作为 pipeline 的自动下一步执行，而非等待用户提示。**

### Step 4：Phase 3 — 设定世界观
**做什么：** 调用 `pop-decon-setting`。归纳 L1 六件套 + 宪法 + 数值。

> ⚠️ **数值体系的完整定义**：Phase 3 的"数值"包含两个维度——
> 1. **正向构建（pop-writer-world Phase 4）**：战斗数值榜（combat_capability.yaml/怪物映射/碰撞曲线）
> 2. **反向破译（数值体系反拆）**：静态金字塔（人口×地位×破坏力分布）+ 动态升级表（主角跃迁防崩）
>
> 反向破译的方法论详见 `references/numerical-system-reverse-engineering.md`。

**❌ 门禁：** 卷幕产出缺失 → 退回 Phase 2。

### Step 5：Phase 4 — 创意溯源
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

v13.4.0 | 2026-06-16 | Phase 4 创意溯源正式实装，新增子 skill `pop-decon-trace`。管线扩展为 Phase 1→2→3→4。新增 Step 2.6 命名归一化（批量重命名+批次文件拆分）。核心红线：化用≠照抄。冰山理论嵌入拆书哲学。YAML frontmatter 更新 description/related_skills。管线地图去重。

## 参考文件

| 文件 | 用途 |
|:-----|:------|
| `references/numerical-system-reverse-engineering.md` | 数值体系反拆方法论——静态金字塔+动态升级表，用于 Phase 3 扩展 |
| `references/output-quality-standards.md` | 各 Phase 产出物的质量门禁标准（含 L1/L2/L3 分级） |
| `references/output-quality-standards.md` | 各 Phase 产出物的质量门禁标准（含 L1/L2/L3 分级） |