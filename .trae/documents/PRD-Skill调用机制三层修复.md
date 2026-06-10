# PRD：Skill 调用机制三层修复

> 版本：v1.0 | 2026-06-09
> 来源：6-9测试 ch001-015 全量 run 审计
> 状态：待执行

---

## 一、三层独立问题

| # | 现象 | 受影响章 | 根因 | 修复层 |
|:--:|------|:--:|------|:--:|
| 1 | Agent 读了 steps/ 文件但只拿到 ~50% 内容 | ch001-009 | Paopao Read tool result 有输出上限，agent 不续读 | **工具层**（你改 Paopao） |
| 2 | Agent 连续 5 轮不读任何子 skill 文件 | ch011-014 | 长会话惰性——ch010 有预存 design 文件 → agent 跳过完整管线 → 形成惯性 | **Think 层**（我们改 expert-writer） |
| 3 | 即使 skill 在 prompt 里，关键指令（输出路径）仍不可见 | ch015 | 输出路径在 steps/*.md 里，不在 SKILL.md 主文件里 | **主文件层**（我们改 writer/plot/bookstrap） |

---

## 二、修复 1：Paopao Read 透明分片（工具层）

### 原理

sol Read 不截断——截断在 Paopao 的 Read wrapper。Read 工具输出超过某个上限时被截断。

Paopao 在 Read wrapper 里加**透明分片**——一次 Read 调用，内部读完整文件，如果超过 tool result 上限就拆成 N 个返回：

```
[Tool Result 1/3] Read: step-1-design.md
(前 4,000 chars)

[Tool Result 2/3] Read: step-1-design.md (continued)
(中间 4,000 chars)

[Tool Result 3/3] Read: step-1-design.md (continued)
(最后 ~3,000 chars)
```

**不改任何 skill 文件结构。** step 文件仍独立，主文件仍轻量。

### 为什么这个就够了

修复 1 后，agent 每次 Read 都能拿到完整内容 → 之前 4 天加在 steps/*.md 里的所有约束（@source、前置条件、22 列逐章颗粒度、爽点红线、禁止 D&D 骰子）→ agent 完整可见。

---

## 三、修复 2：Expert-writer 任务类型切换检查（Think 层）

### 原理

ch010 有一个预存 design 文件（开书阶段顺手产的）→ agent 推断"不用走 Design 流程"→ 形成惯性 → ch011-014 连续 5 轮不读任何子 skill 文件。

这是 **Think 层没有"任务类型切换"感知**——上一轮在做 gap 分析（非创作类），这一轮要写正文（创作类），agent 应该重置管线状态，但它用"检查文件是否存在"替代了"检查应该用什么管线执行"。

### 改动

`expert-writer/SKILL.md` §3.1 Think 追加：

```
**第三步：任务类型切换检查（v2.3）**

当本轮 intent 与上一轮不同（诊断→写作 / 修订→写作 / 补全→写作 / 开书→写正文）：
  □ 重新进入完整 Think 流程——不得因"已有相似产出"跳过
  □ 重新 Read 目标子 skill 的 SKILL.md + 全部 steps/*.md
  □ 重新验证前置条件（管线前置校验 §3.1.6）
  □ 理由：任务类型切换意味着管线上下文完全不同。上一轮的捷径不适用。
```

---

## 四、修复 3：关键输出路径提升到 SKILL.md 主文件（主文件层）

### 原理

System prompt 只注入 SKILL.md 主文件。输出路径在 step 子文件里 → 即使路由正确、skill 在 prompt 里，agent 也看不到"必须写 design 文件到磁盘"这条指令。

ch015 就是这种情况——writer SKILL.md 完整在 prompt 里，但 `03-写作资产/chXXX-design.md` 这个路径写在 step-1-design.md 最后一行。

### 改动

三个 skill 的主文件各追加输出路径摘要（每条 ≤1 行）：

**Writer SKILL.md**：
```
Step 1 ★ 输出: 03-写作资产/chXXX-design.md（必须写入磁盘·每章新建）
Step 2 ★ 输出: 03-正文/chXXX.md（章末附 # === 状态更新 === 块）
Step 3 ★ 输出: 00-总控/entity-snapshot.yaml（覆盖写入·从全部章 delta 聚合）
```

质量红线追加：
```
| ❌10 | Design 文件已写入磁盘 — 03-写作资产/chXXX-design.md 存在且非空 | [ ] |
| ❌11 | Entity-snapshot 已更新 — 00-总控/entity-snapshot.yaml 被覆盖写入 | [ ] |
```

**Plot SKILL.md**：
```
Step 4 ★ 输出: 设计/幕/情节线草案-XX.md（逐章22列·M3拆双行·S≥3条）
Step 5 ★ 输出: 设计/幕/act-XX-人物.md（A级逐章22行·B级≥5节点）
Step 7 ★ 输出: 设计/幕/act-XX-装备.md + act-XX-势力.md
        ★ 硬约束: 装备攻击力 ∈ combat_capability 段位 min~max
Step 9 ★ 输出: 设计/幕/act-XX.yaml
        ★ 硬约束: protagonist.level = act_rank_schedule.end_rank
```

**Bookstrap SKILL.md**：
```
Phase 0 ★ 输出: story-engine.yaml（已有拆解报告→先读 T1+T4+T5+T7）
Phase 3 ★ 输出: 角色卡 + constitution.yaml + chapter-state.yaml
Phase 5 ★ 输出: combat_capability + monster_rank_map + act_rank_schedule + collision_curve
```

---

## 五、三个修复各自解决什么

| 修复 | ch001-009 截断 | ch011-014 惰性 | ch015 缺 design |
|:--:|:--:|:--:|:--:|
| 修复 1 (Paopao 分片) | ✅ | — | — |
| 修复 2 (Think 切换检查) | — | ✅ | — |
| 修复 3 (输出路径提升) | — | — | ✅ |

---

## 六、执行清单

| # | 修复 | 文件 | 改动者 |
|:-:|:--:|------|:--:|
| 1 | Paopao Read 透明分片 | Paopao Read tool wrapper | 你 |
| 2 | 任务类型切换检查 | `expert-writer/SKILL.md` §3.1 | 我们 |
| 3a | writer 输出路径 + 新红线 | `pop-novel-writer/SKILL.md` | 我们 |
| 3b | plot 输出路径 + 硬约束 | `pop-novel-plot/SKILL.md` | 我们 |
| 3c | bookstrap 输出路径 | `pop-novel-bookstrap/SKILL.md` | 我们 |
