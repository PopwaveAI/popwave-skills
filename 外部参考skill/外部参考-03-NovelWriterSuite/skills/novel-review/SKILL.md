---
name: novel-review
description: 章节 / 全书校稿。37 维质量审查：4 维统计学（Python 脚本）+ 33 维主观（LLM 评估）+ 一致性 + 伏笔账 + 硬规则。当用户说"校稿"、"审一遍"、"检查第 X 章"、"看看哪里有问题"、"全书审查"、"review chapter"、"audit" 时触发。审稿只评结构和完成度，**不评文笔**（文笔由 novel-style-engine + novel-chapter 在生成阶段控制）。
---

# Novel Review —— 章节校稿

## 功能

**37 维质量审查**（借鉴 inkos continuity.ts，独立重写）。
四种检查并行：

| 层 | 检查类型 | 实现 | 维度数 |
|---|---|---|---|
| 1 | 客观统计 | Python 脚本 | 4 维 |
| 2 | 硬规则违规 | Python 脚本 | 10+ 条规则 |
| 3 | 伏笔账核对 | Python 脚本 | 1 维（伏笔回声 + 揭 1 埋 1）|
| 4 | 一致性 / 完成度 | LLM 评估 | ≥ 17 维 |

输出统一的批注式问题列表，**不直接改稿**。

## Reviewer 边界（重要）

> 借鉴 inkos：审稿只看 **结构 + 完成度**，**不审文笔**。

文笔由 `novel-style-engine` + `novel-chapter` 的 writing-guidelines 在生成阶段控制。
本 skill 不应该说"这一句不好看 / 这一段啰嗦"——那种主观品味问题留给作者本人。

本 skill 评判的是：
- 章节有没有偏离大纲（结构）
- 角色有没有失格（一致性）
- 设定有没有矛盾（一致性）
- 伏笔账有没有兑现（完成度）
- 句式 / 节奏 / AI 痕迹有没有客观可识别的问题（统计）

## 触发场景

1. **写完一章自检**（`novel-chapter` Step 6.5 自动调用 Python 脚本部分）
2. **用户手动单章校稿**："校稿第 8 章"
3. **全书审查**："全书过一遍"
4. **定期质检**：建议每 5-10 章跑一次全章校稿
5. **卷尾检查**：在卷完结前必跑

## 工作流

### A. 单章校稿（默认）

输入：章节号 N
输出：`chapters/ch-NNN.review.md`（批注列表）

**Step 1 - 跑 4 个 Python 脚本**

```bash
python3 .../check_ai_tells.py --chapter chapters/ch-008.md
python3 .../check_post_write.py --chapter chapters/ch-008.md --vault {vault}
python3 .../check_hook_ledger.py --chapter chapters/ch-008.md --vault {vault}
python3 .../check_consistency.py --chapter chapters/ch-008.md --vault {vault}
```

每个脚本输出 JSON：
```json
{
  "passed": true/false,
  "issues": [
    {
      "severity": "critical|warning|info",
      "dimension": "ai-tells.paragraph-uniformity",
      "location": "L 23-25",
      "description": "...",
      "suggestion": "..."
    }
  ]
}
```

**Step 2 - LLM 主观维度评估**

把 4 类脚本结果合并后，调 LLM 跑剩余 LLM 维度（详见 `references/audit-dimensions.md`）：

- OOC 检查（vs character.md 的 voice patterns）
- 时间线检查（vs plot/timeline.md）
- 设定冲突（vs worldbuilding/）
- 战力崩坏（vs worldbuilding/systems/）
- 信息越界（角色不应该知道的事）
- 节奏检查（vs pacing-principles）
- 流水账（vs writing-guidelines）
- ...

LLM 输出 JSON：
```json
{
  "passed": true/false,
  "overall_score": 0-100,
  "issues": [...],
  "summary": "一句话总结"
}
```

**Step 3 - 合并 + 输出**

把所有 issue 合并，按位置排序，生成 `chapters/ch-NNN.review.md`：

```markdown
---
type: review
chapter: 8
reviewed-at: 2026-05-20 14:30
overall-score: 82
passed: true
critical-count: 0
warning-count: 3
info-count: 5
---

# Ch 8 校稿报告

## 总评（一句话）

结构稳，节奏 OK，但 sera 力量使用的描写过度（与角色克制基调有偏离）。

## Critical（0）

无。

## Warning（3）

### [L 23] 节奏 / pacing-monotony
段落变异系数 0.12（阈值 < 0.15），段落长度过于均匀。
建议：在 L 18-30 之间插入一个 1-2 句的短段，制造节奏起伏。

### [L 67] OOC / character-fidelity
sera 在对峙时主动说出"我可以放过你们"，与其 character-voice "嘴硬主角型 + 沉默克制" 不符。
建议：把这句改为动作（如把武器收起来）或沉默。

### [L 88] hook-ledger / advance-evidence
hook H001 在 advance 列表，但正文中关键词"皇家纹章"、"金线"均未出现。
建议：在 L 80-95 之间加入 sera 注意到斥候腰间纹章的细节。

## Info（5）

### [L 5] ai-tells / hedge-density
套话词"似乎"出现 2 次。低于上限 3 次，仅作记录。

...
```

### B. 全书审查

输入：vault 路径
输出：`deliverables/full-review.md`

跑每一章的 single chapter review，汇总：
- 总评分分布
- 各章 critical / warning 计数
- 跨章问题（如某伏笔 30 章未推进）
- 跨章 OOC 趋势（如某角色在多章中 voice 漂移）

### C. 卷尾检查

输入：卷 ID
输出：`plot/arcs/{arc}-review.md`

- 每章逐项审
- 卷级伏笔检查（卷尾仍 open 的 hook 是否合理）
- 卷级节奏检查（是否符合 pacing-principles 的节奏结构）
- 30 章承诺兑现（仅对前 30 章触发）

## 4 个 Python 脚本

详见各脚本文件头注释。

### `check_ai_tells.py`

4 维统计学检测（借鉴 inkos ai-tells.ts 重写）：
- dim 20: 段落长度变异系数 < 0.15 → warning
- dim 21: 套话密度 > 3 次/千字 → warning
- dim 22: 同转折词重复 ≥ 3 次 → warning
- dim 23: 连续相同开头句 ≥ 3 → info

### `check_post_write.py`

硬规则违规（借鉴 inkos post-write-validator.ts 重写）：
- 禁用句式（"不是…而是…"等）→ critical
- 禁用标点（破折号）→ critical
- 元叙事词 → critical
- 学术报告术语 → critical
- 全场震惊式 → critical
- 转折词密度上限 → warning
- 疲劳词每章 ≤ 1 次 → warning
- 详细规则见 `novel-style-engine/references/anti-ai-rules.md`

### `check_hook_ledger.py`

伏笔账核对（借鉴 inkos hook-ledger-validator.ts 重写）：
- 解析章节 `## hook-账` 段
- advance / resolve 必须在正文中有 CJK 2-gram 关键词回声 → critical
- 揭 1 埋 1 硬底线 → critical
- defer 必须给出原因 → warning

### `check_consistency.py`

跨实体一致性（自创 + 借鉴）：
- 出场角色是否都在 characters/ 中存在 → critical 若不在
- 角色当前状态 vs `.memory/entity-state.md` 是否冲突 → critical
- 涉及地点是否在 worldbuilding/locations/ 中 → warning 若不在
- 力量体系动作 vs systems/.md 规则边界 → warning 若越界
- continuity-facts 中的"永久事实"是否被违反 → critical

## LLM 维度（≥ 17 维）

LLM 评估部分用以下 prompt 模板：

```
你是中文网文结构编辑。审稿只看完成度 + 结构，不审文笔。
- ALL OUTPUT MUST BE 中文 JSON
- passed=false 仅当存在 critical issue
- overall_score 0-100 校准：
  - 95-100: 可直接发表
  - 85-94: 小瑕疵但顺畅
  - 75-84: 明显问题但骨架稳
  - 65-74: 多处问题影响阅读
  - <65: 结构崩坏需重写

审稿维度：
1. OOC 检查（vs character.md voice patterns）
2. 时间线检查（vs timeline.md）
3. 设定冲突（vs worldbuilding/）
4. 战力崩坏（vs systems/）
5. 数值检查
6. 伏笔检查（结构层；脚本已做表面检查）
7. 节奏检查（参考 pacing-principles）
8. 信息越界
9. 利益链断裂
10. 配角降智 / 工具人化
11. 爽点虚化
12. 台词失真
13. 流水账
14. POV 一致性
15. 支线停滞
16. 弧线平坦
17. 读者期待管理
18. 章节备忘偏离

[输入上下文]
- 章节正文：{...}
- 章纲：{...}
- 当前 arc：{...}
- 出场角色卡：{...}
- 涉及世界观：{...}
- 当前 .memory/entity-state.md：{...}

输出 JSON：
{
  "passed": ...,
  "overall_score": ...,
  "issues": [{"severity":"...","dimension":"...","location":"...","description":"...","suggestion":"..."}],
  "summary": "..."
}
```

完整 37 维清单见 `references/audit-dimensions.md`。

## 评分阈值（决定 passed）

- 任一 critical 存在 → passed = false
- warning 数 ≥ 5 → 提醒但不阻断
- info 数任意 → 不影响 passed
- overall_score < 65 → 即使无 critical 也建议重写

## 与其他 skill 的边界

- **不改正文**：只输出批注。改正文是 `novel-chapter` 的 `rewrite` / `fix-ai` 任务（或用户手改）
- **不评文笔好不好**：那是主观品味，留给作者
- **不重新跑写法引擎**：style 漂移问题报为 issue，让用户决定是否重跑 `compile_style.py` 或重新写章节

## 输出

每次跑完后：
- `chapters/ch-NNN.review.md` 写好
- 给用户简短摘要（critical / warning / info 计数 + overall_score）
- 列出**值得立即修复**的前 3 个 issue
