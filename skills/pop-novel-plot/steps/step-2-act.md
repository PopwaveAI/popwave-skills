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
| `conflict.stakes` | 本幕输 = 失去什么。从 volume-XX.md §四 M1/M3 提取 |
| `conflict.escalation` | 本幕 ch1 → chN 冲突如何升级 |

### 2. Canvas 矩阵填充（★ 核心）

> Canvas 矩阵 = 章节行 × 剧情线列交叉表。一口气看清整幕：节奏密度 + 爽点分布 + 各线联动。

```
填写步骤：
① 遍历本幕所有章节（ch1 ~ chN）
② 对每章，逐一确认每条线（M1/M2/M3/S1/S2）是否推进：
   - 推进了 → 写一句话摘要："这条线在本章发生了什么"
   - 没推进 → 留空
③ 填写节奏笔记（如"双线并行""蓄力章"）
④ ★ 标注每条线的 payoff_level（详见 `references/payoff-design-guide.md` §三）：
    - 空 = 铺垫/建设/埋伏笔
    - 小 = 干脆斩杀/升级/打脸/梗（可选标注）
    - 中 = 有铺垫的可感知释放。**确保每章 ≥1 条线=中**
    - 大 = ★ 爆发。蓄力全部释放。故事从这章进入新阶段
    - 特大 = ★★ 全书承诺兑现
④☆ 跟踪铺垫→释放节奏：
    - 每条线连续 ≥3 章只有空/小 → 下一章必须让该线释放
    - 释放后允许再铺垫 2-3 章（波浪节奏）
    - 某章所有线都是空/小 → 把最近一条快释放的线提前到这里
⑤ 填写 payoff_summary：逐章统计 ≥中 的线数
    - payoff_summary=0 → chapter-design 自行制造中爽点
⑥ 通过 rhythm_check 自检
```

### 3. 节奏自检（canvas.rhythm_check）

填完 Canvas 后：

**基础检查：**
- 每条线连续留白 ≤ max_gap？
- 每章活跃线数在 min:1 / max:3 范围？
- `payoff_constraints.mid_every_chapter`：每章 ≥1 线 payoff≥中？
- `payoff_constraints.no_line_dormant_over_3`：无线连续 ≥3 章只铺垫无释放？
- `payoff_constraints.big_max_gap`：大爽点间隔 ≤ 5 章？
- `payoff_constraints.ultimate_min_per_volume`：每卷 ≥1 特大？

**首卷黄金窗口（★ vol-01/act-01 时强制执行）：**
- 番茄平台标准。对照 `templates/rhythm-check.md` 平台校准表：
  - ch01 核心卖点是否在第 1 章内亮相？未亮相 → P0 退回
  - ch01 章末是否有可感知钩子？无钩子 → P0 退回
  - ch02 是否发生第一次战斗/重大矛盾？未发生 → P0 退回
  - ch01-ch02 连续纯铺垫 ≤ 1 章？超过 → P0 退回
  - 回填 `canvas.rhythm_check.first_volume_gate` 各字段

### 4. 填写章级设计意图（chapters[]）

> **从 v6.2 起大幅精简。** 此段只传 plot 才知道的设计意图——不传事件细节（归 chapter-design）。

| 字段 | 来源 |
|:-----|:-----|
| `ch` / `title` / `word_count` | Canvas entry 对应 |
| `emotional_goal` | 本章想让读者感受什么。从 Canvas 各线推进方向 + payoff 级别推导 |
| `payoff_note` | **仅大/特大时填。** 蓄力上下文。如"M1线ch5-7蓄力，本章幕级爆发" |
| `end_hook.type` | 悬念 / 信息 / 情绪 |
| `end_hook.drive` | 驱动因素。如"XX的生死未卜" |
| `chekhov_set` / `chekhov_fire` | 本章埋/收的契诃夫枪 |

---

## 完成后

→ 跳到 Step 2 设计下一幕（输出 `vol-XX/act-YY.yaml` 幕号+1）
→ 所有幕完成后 → 通知下游 chapter-design，附上 `volume-XX.md` + 第 1 幕的 `vol-XX/act-YY.yaml`
