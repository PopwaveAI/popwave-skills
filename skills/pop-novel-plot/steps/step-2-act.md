# Step 2：幕纲编排

> 产出: `设计/幕/vol-XX/act-YY.yaml`
> 模板: `templates/act-skeleton.yaml`
> 管线: pop-novel-plot v6.2 — 每幕执行一次，重复直到所有幕完成

---

## 目的

在卷战略（volume-XX.md）已就绪的基础上，编排当前幕的每章设计。
一幕 = 20-35 章，卷内的一个战术执行阶段。

---

## 前置条件

- [ ] `设计/卷/volume-XX.md` 已产出并用户确认（含剧情线定义）
- [ ] 当前幕的章节范围已确定（从卷设计的幕划分取）

---

## 执行

### 1. 填写幕级目的（act.purpose）

| 字段 | 来源 |
|:-----|:-----|
| `purpose.for_book` | 本幕在全书中的叙事作用。从 volume-XX.md 的核心命题推 |
| `purpose.for_reader` | 本幕给读者的满足。核心情绪 / 悬念打开节奏 / 爽点密度方向 |
| `conflict.stakes` | 本幕输 = 失去什么。从 volume-XX.md §四 主线1/主线3 提取 |
| `conflict.escalation` | 本幕 ch1 → chN 冲突如何升级 |

### 2. 逐章填充（chapters[]）

> **v6.2 起 Canvas 数据合入每个 chapter block。** 每章一个自包含 block，plot agent 逐章过一遍就能填完。

```
逐章流程（每章重复）：
① 确认本章 title、word_count
② 填写 canvas.设定线 + 设线负载：
   - 设定线 = `{信息项名}: {本章交付了什么设定}`。如 "裂隙成因: 矿工交代了等级分级"
   - 设线负载 = 0（无新设定）| 1（适量）| ≥2（过载警告——≥2个新概念）
   - 参考 volume-XX.md §五 设定披露承诺的 deadline 表
③ 逐一确认每条线（主线1/主线2/主线3/支线1/支线2）是否推进：
   - 推进了 → 写一句话摘要 + payoff_level
   - 没推进 → 留空
   - payoff_level 空=铺垫 | 小=干脆斩杀/升级/打脸 | 中=可感知释放 | 大=爆发·格局重画 | 特大=全卷承诺兑现
④ 填写 canvas.payoff_summary：统计 ≥中 的线数。=0 → design 自行制造中爽点
⑤ 填写 canvas.note：节奏笔记（如"双线并行""蓄力章""设线有交付"）
⑥ 如果本章 canvas 中有 payoff≥中，填写 payoff_note：告诉 design 蓄力上下文
⑦ 填写 emotional_goal：本章情感方向
⑧ 填写 end_hook：钩子方向（悬念/信息/情绪 + 驱动因素）
⑨ 填写 chekhov_set / chekhov_fire
⑩ ¥ 跟踪铺垫→释放节奏：
    - 每条线连续 ≥3 章 payoff 都是空/小 → 把释放提前到这里
    - 释放后允许再铺垫 2-3 章（波浪节奏）
```

### 3. 节奏自检（rhythm_check）

全部 chapter blocks 填完后，全量扫描自检：

**基础检查：**
- 每条线连续留白 ≤ max_gap？（用 grep 扫所有 `canvas.{线号}_payoff` 字段）
- 每章活跃线数在 min:1 / max:3 范围？
- `payoff_constraints.mid_every_chapter`：每章 ≥1 线 payoff≥中？
- `payoff_constraints.no_line_dormant_over_3`：无线连续 ≥3 章只铺垫无释放？
- `payoff_constraints.big_max_gap`：大爽点间隔 ≤ 5 章？
- `payoff_constraints.ultimate_min_per_volume`：每卷 ≥1 特大？

**设定线检查：**
- 连续 设线负载=0 的章数 ≤ `设线穿透.max_consecutive_zero_负载`（默认 2）？超过 → 读者连续几章没搞懂新东西，需要插入设定
- 扫描 `设线穿透.per_info_deadlines`：每个信息项的 deadline 章之前，Canvas 设定线有没有提过这个信息？没到 → 回退插入
- 记录所有 设线负载≥2 的章到 `设线穿透.负载过载章[]`：不强制修但有记录——如果连续出现在同人章 → 需要重分配

**首卷黄金窗口（★ vol-01/act-01 时强制执行）：**
- 番茄平台标准。对照 `templates/rhythm-check.md` 平台校准表：
  - ch01 核心卖品是否在第 1 章内亮相？未亮相 → P0 退回
  - ch01 章末是否有可感知钩子？无钩子 → P0 退回
  - ch02 是否发生第一次战斗/重大矛盾？未发生 → P0 退回
  - ch01-ch02 连续纯铺垫 ≤ 1 章？超过 → P0 退回
  - 回填 `rhythm_check.first_volume_gate` 各字段

---

## 完成后

→ 跳到 Step 2 设计下一幕（输出 `vol-XX/act-YY.yaml` 幕号+1）
→ 所有幕完成后 → 通知下游 chapter-design，附上 `volume-XX.md` + 第 1 幕的 `vol-XX/act-YY.yaml`
