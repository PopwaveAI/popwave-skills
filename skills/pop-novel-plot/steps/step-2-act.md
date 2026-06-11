# Step 2：幕纲编排

> 产出: `设计/幕/vol-XX/act-YY.yaml`
> 模板: `templates/act-skeleton.yaml`
> 参考: `templates/act-guide.md`（字段计算公式）
> 管线: pop-novel-plot v6.1 — 每幕执行一次，重复直到所有幕完成

---

## 目的

在卷战略（volume-XX.md）已就绪的基础上，编排当前幕的每章具体设计。
一幕 = 20-35 章，卷内的一个战术执行阶段。

---

## 前置条件

- [ ] `设计/卷/volume-XX.md` 已产出并用户确认
- [ ] 当前幕的章节范围已确定（从卷设计的幕划分取）

---

## 执行

### 1. 信息释放规划（★ 已内嵌至 act-skeleton.yaml#info_release_plan）

在填充 `act-XX.yaml` 时，填写 `info_release_plan` 段（无需独立文件）：

- 从 L1-01~06 中扫描本章段需要的设定信息
- 标记 P0（不释放就看不懂剧情）和 P1（拓展读者体验）
- 分配到当前幕的各章（第 1 章 ≤ 2 个新概念；连续 2 章无信息释放 → 第 3 章必须追加）

### 2. 幕纲设计（核心）

产出 `设计/幕/vol-XX/act-YY.yaml`，按 `templates/act-skeleton.yaml` 骨架填充。

**先填充 Canvas 矩阵（★ v6.0 新增）：**

> Canvas 矩阵 = 章节行 × 剧情线列 交叉表。一口气看清整幕的节奏密度。

```
填写步骤：
① 遍历本幕所有章节（ch1 ~ chN）
② 对每章，逐一确认每条线（M1/M2/M3/S1/S2）是否推进：
   - 推进了 → 写一句话摘要："发生了什么"
   - 没推进 → 留空
③ 填写节奏笔记（如"双线并行"、"M2推进高潮"）
④ ★ 标注每条线在本章的 payoff_level（详见 `references/payoff-guide.md`）：
    - 空 = 铺垫/建设/埋伏笔
    - 小 = 干脆利落的斩杀/升级/打脸/梗植入。chapter-design 据此设计小爽点事件
    - 中 = 有铺垫的可感知释放。**plot 确保每章 ≥1 条线=中，chapter-design 据此设计中爽点事件**
    - 大 = ★ 爆发——这条线的蓄力全部释放。故事从这章起进入新阶段
    - 特大 = ★★ 全书承诺兑现。多线大汇聚 + 全卷情绪极值
④☆ 跟踪铺垫→释放节奏（★ 中爽点跨章设计关键）：
    - 每条线（M1/M2/M3/S1/S2）连续 ≥3 章只有空/小 → 下一章必须让该线释放
    - 释放后允许再铺垫 2-3 章（波浪节奏：蓄力→释放→蓄力→释放）
    - 如果某章所有线都是空/小 → 把最近一条快释放的线提前到这里
⑤ 汇总 payoff_map：逐章统计 ≥ 中 的 payoff → total + 线号列表 + note
⑥ 从 payoff_map 反推大爽点位置（某线=大）→ payoff_distribution.大.positions
⑦ 从 payoff_map 反推特大爽点位置（≥2 线=大 汇聚）→ payoff_distribution.特大.positions
⑧ 用 rhythm_check 自检：大爽点间隔 ≤ 5 章？特大爽点 ≥ 1 个/卷？
```

**然后设计幕级定义：**

| 字段 | 来源 |
|:-----|:-----|
| `core_conflict` | 本幕的主冲突。从 volume-XX.md §四 的 M1/M3 提取 |
| `stakes` | 本幕失败 = 失去什么 |
| `escalation_path` | 本幕内第 1 章到最后一章如何升级 |
| `goal` | "读者从「X」到「Y」" |
| `tone_note` | 1-3句散文，本幕情绪配比 |
| `payoff_distribution` | 密度约束：小≥5/章 / 中≥1/章 / 大间隔≤5章 / 特大≥1/卷。positions 从 Canvas 反推。完整定义 → `references/payoff-guide.md` |
| `emotional_arc.checkpoints` | 从 Canvas 矩阵反推 4-6 个情绪转折点 |

**然后填充 20-35 个章级切片：**

每章必须填：
- `ch` / `title` / `word_count`
- `emotional_goal` — 第一性
- `payoff.type/trigger/reader_feeling` — 与幕级 payoff_distribution 对齐
- `reader_emotion_path` — [起点, 中间, 终点]。终点必须衔接到下一章起点
- `end_hook` — 悬念/信息/情绪 + 具体驱动力 + 内容
- `plotlines_active` — 推进了哪些线（line id 对应 volume-XX.md §四）
- `characters_active` — 必须在 volume-XX.md §三 中存在
- `locations` — 必须在 volume-XX.md §三 中存在

**条件填充场景规格字段**（根据本章类型选填）：
- 战斗章 → `combat.scale/purpose/result/reward`
- 对话章 → `dialogue.relation/stakes/result/reward`
- 发现章 → `discovery.what/how/world_expands/new_options`
- 危机章 → `crisis.threat/scale/cannot_escape_because/cost_of_involvement`

> 复杂字段的计算方式见 `templates/act-guide.md`。

### 3. 自检

用 Canvas 矩阵的 `rhythm_check` + `templates/rhythm-check.md` 快速过一遍：

**Canvas 矩阵检查：**
- 每条剧情线的最大连续留白章数 ≤ max_gap 值？
  - 不留白 → 密度过高，需要合并
  - 超限留白 → 该线在读者记忆中消失，需要提前插一帧
- 每章活跃线数是否在 `min: 1, max: 3` 范围内？
- 连续 3+ 章只有一条线在推进 → 单调，需要加副线

**常规检查：**
- 无中爽点空白章（每章 ≥ 1 个中爽点）？
- 连续无新信息章节 ≤ 2 章？
- 高强度章间距 ≥ 3 章？
- end_hook 衔接检查：chN 的钩子 → chN+1 的情绪路径[0]？
- 主角等级 = act_rank_schedule.end_rank？
- 战斗章连续 ≤ 2 章？

**首卷黄金窗口检查（★ vol-01/act-01 时强制执行）：**
- 番茄平台标准。对照 `templates/rhythm-check.md` 平台校准表：
  - ch01 核心卖点是否在第 1 章内亮相？未亮相 → P0 退回
  - ch01 章末是否有可感知钩子？无钩子 → P0 退回
  - ch02 是否发生第一次战斗/重大矛盾？未发生 → P0 退回
  - ch01-ch02 连续纯铺垫 ≤ 1 章？超过 → P0 退回
  - 回填 `act-skeleton.yaml#rhythm_check.first_volume_gate` 各字段

---

## 完成后

→ 跳到 Step 2 设计下一幕（输出 `vol-XX/act-YY.yaml` 幕号+1）
→ 所有幕完成后 → 通知下游 chapter-design，附上 `volume-XX.md` + 第 1 幕的 `vol-XX/act-YY.yaml`
