# PRD：跨 Skill 值一致性硬保障 + Skill 调用机制修复

> 版本：v1.0 | 2026-06-09
> 来源：6-9测试全流程审计 + PRD-Skill调用机制失效.md + 层1/2/3方案推演
> 状态：待评审

---

## 一、两条诊断结论

### 结论 A：跨文件值冲突的根因不是"Agent 没读"——是指令不在 Agent 能可靠拿到的地方

| 根因 | 来源 |
|------|------|
| Paopao 只注入 SKILL.md 主文件到 system prompt | PRD-调用机制 E1 |
| Agent Manual Read 子文件 → 截断到 ~50% | PRD-调用机制 E4 |
| 长会话惰性 → Agent 连续 5 轮不读任何子 skill 文件 | PRD-调用机制 E5 |
| 输出路径在 step 子文件里——即使 skill 在 system prompt 里也看不到 | PRD-调用机制 E6 |

**关键推断**：之前所有"上游不消费"的修复（@source、step 前置条件、ROUTE-AUGMENT 注入路径）——如果这些约束写在 steps/*.md 而非 SKILL.md 主文件——Agent 有 ~50% 概率根本看不到。

### 结论 B：管线文件构成有向无环图——但图的边是软约束，每条边都可能断裂

~73 个文件，12+ 条跨 skill 依赖边。全部靠 Agent "读模板 → 读上游文件"来维持。

---

## 二、方案设计

### 2.1 不做的

- ❌ **层 3 schema 硬约束**——叙事柔性与跨世界通用性损失大
- ❌ **层 1 单独用**——把"没读"换成了"摘取值可能错但下游盲信"
- ❌ **12 步走完统一校验**——修一个文件触发联动 revert

### 2.2 要做的

| # | 方案 | 解决什么 | 优先级 |
|:--:|------|------|:--:|
| **A** | 关键输出路径 + 硬性约束从 step 子文件提升到 SKILL.md 主文件 | "Agent 修了 4 轮前置条件但 Agent 根本看不到" | **P0** |
| **B** | Step 级即时校验脚本（每步产出后立即跑） | "跨文件值冲突等 12 步走完才发现" | **P1** |
| **C** | Expert-writer Think：任务类型切换时强制重新加载子 skill 全部文件 | "ch011-014 连续 5 轮不读 writer" | **P1** |

---

## 三、方案 A：关键指令提升到 SKILL.md 主文件

### 原理

Paopao 通过 system prompt 注入 SKILL.md 主文件——100% 完整、每轮必在。steps/ 子文件不在注入范围。

**把每个 step 的关键信息（输出路径、硬性前置条件、硬性产出约束）提升到主文件。**

### 3.1 Writer SKILL.md 改动

```
Step 1 — Design（LLM · 产出八块 chXXX-design.md）
  ★ 输出文件: 03-写作资产/chXXX-design.md（必须写入磁盘，不可只口头汇报）
  ★ 每章必须新建 design 文件，不得复用上一章 design
  ★ 前置必读: entity-snapshot.yaml + act-XX.yaml + canvas + constitution + story-engine + L1
  ★ 硬性产出: 块A(设计说明) + 块B(本章空间) + 块C(登场人物) + 块D(事件链) + 块E(设定嵌入表)
  详细模板 → steps/step-1-design.md

Step 2 — Render（LLM / 三阶段）
  ★ 输出文件: 03-正文/chXXX.md
  ★ 章末必须附带 # === 状态更新 === 块（entity_updates + world_updates + event_log + style_report）
  ★ Phase 1 必须读 styles/{项目风格}.md → 语感对齐 → 产生调音叉
  详细流程 → steps/step-2-render.md

Step 3 — State Update（零 LLM）
  ★ 输出文件: 00-总控/entity-snapshot.yaml（覆盖写入·从所有章 delta 聚合）
  ★ 同时更新 03-写作资产/global-summary.md（叙事摘要·轻量追加）
  详细算法 → steps/step-5-state-update.md
```

**质量红线追加**：
```
| ❌10 | Design 文件已写入磁盘 — 03-写作资产/chXXX-design.md 存在且非空 | [ ] |
| ❌11 | Entity-snapshot 已更新 — 00-总控/entity-snapshot.yaml 被覆盖写入 | [ ] |
```

### 3.2 Plot SKILL.md 各 step 追加

```
Step 4 — 情节线草案
  ★ 输出: 设计/幕/情节线草案-XX.md
  ★ 硬约束: M1≥3子线 / S≥3条 / 逐章22列交叉图式 / M3拆等级+面板双行 + 逐章摘要22行
  ★ 前置必读: 角色卡(动机/关系冲突) + story-engine + 里程碑设计

Step 5 — 本卷人物设计
  ★ 输出: 设计/幕/act-XX-人物.md
  ★ 硬约束: A级主角逐章22行状态表 / B级≥5关键节点 / C级出场章号
  ★ 前置必读: L3-角色层/{主角卡}.md + {配角卡}.md + combat_capability(段位范围)

Step 7 — 本卷世界设计（势力/装备）
  ★ 输出: 设计/幕/act-XX-势力.md + 设计/幕/act-XX-装备.md
  ★ 硬约束: 装备攻击力必须在 combat_capability 对应段位 min~max 区间内
  ★ 前置必读: combat_capability + act_rank_schedule + collision_curve + T6(装备数值风格)
  ★ 数值格约束: 禁止输出原著不存在的数值格式

Step 9 — 幕纲设计
  ★ 输出: 设计/幕/act-XX.yaml
  ★ 硬约束: prototype.level = act_rank_schedule.end_rank / 爽点频率: 战斗≤2 & 成长≤2 / 高潮章含 enemy_level + 子节拍 + equipment_reward
  ★ 前置必读: combat_capability + act_rank_schedule + collision_curve
```

### 3.3 Bookstrap SKILL.md 追加

```
Phase 0 — 故事引擎
  ★ 输出: L0-产品层/story-engine.yaml
  ★ 前置: 已有参考书拆解报告 → 必须先读 T1+T4+T5+T7 再写。禁止凭记忆写原著事实。

Phase 3 — 项目骨架
  ★ 输出: constitution.yaml + chapter-state.yaml + project.yaml + 角色卡
  ★ 主角卡末尾: ★ 成长轨迹 22 行逐章段（字段名从 combat_capability 读取）

Phase 5 — 数值体系
  ★ 输出: combat_capability + monster_rank_map + act_rank_schedule + collision_curve
```

---

## 四、方案 B：Step 级即时校验脚本

### 原理

在对应 step 的产出指令末尾标注"产出完成后跑校验脚本"。脚本读原始上游文件，对下游产出做机械比对——不依赖 agent 是否读了上游、prompt 里有没有。

### 4.1 校验点

| 校验点 | 触发时机 | 检查内容 | 容忍度 |
|:------|:--------|:--------|:--:|
| 装备数值在段位内 | plot S7 产出后 | 每件装备攻击力 ∈ combat_capability 段位 min~max | ±20% |
| 卷末等级一致 | plot S9 产出后 | act_end_state.protagonist.level = act_rank_schedule.end_rank | 精确匹配 |
| BOSS 掉落段位 | plot S7 产出后 | monster_rank_map 中标记"掉落"的怪物 → 装备阶位 ≥ 怪物段位-1 | 精确匹配 |
| 爽点频率 | plot S11 产出后 | 情节线草案 M2 行连续 ☐≤1 / M3 行连续 ☐≤1 | 精确匹配 |
| 正文数值格式 | writer S2 产出后 | 正文不含项目禁止的数值格式（从 T6 读取） | 精确匹配 |
| Design 文件存在 | writer S1 产出后 | 03-写作资产/chXXX-design.md 存在且非空 | 精确匹配 |
| entity-snapshot 一致 | writer S3 产出后 | _meta.total_chapters = ch*.md 文件数 | 精确匹配 |

### 4.2 校验失败处理

| 阶段 | 退回 |
|------|------|
| plot S7 | 退回 S7 重做。S5/S6 已完成不受影响 |
| plot S9 | 退回 S9 重做。Canvas 已完成不受影响 |
| plot S11 | 退回对应 step 修正 |
| writer S1 | 退回 S1 重做 |
| writer S2 | 退回 S2 重做（该章） |

---

## 五、方案 C：Expert-writer Think 增强

### 5.1 任务类型切换检查（§3.1 追加）

当本轮 intent 与上一轮不同（诊断→写作 / 修订→写作 / 补全→写作 / 开书→写正文）：

```
□ 重新进入完整 Think 流程——不得因"已有相似产出"跳过
□ 重新 Read 目标子 skill 的 SKILL.md + 全部 steps/*.md
□ 重新验证前置条件（管线前置校验 §3.1.6）
```

### 5.2 Skill 加载完整性协议（§0 追加 §0.8）

```
| 0.8 | 路由到子 skill 后 steps 加载不完整 | Read 子 skill SKILL.md 后必须再 Read 该 skill 的全部 steps/*.md。若 Read 输出被截断 → 用 offset 续读至全部加载。 |
```

---

## 六、影响评估

| 维度 | 评价 |
|------|------|
| **解决根因** | A 解决"指令不在 Agent 可靠读取范围内"（50% 截断 + 长会话惰性）|
| **token 膨胀** | 无。A 只改 SKILL.md 内部结构——不改 prompt 长度 |
| **校验有效性** | B 的脚本读原始文件——不依赖 agent 是否读取、prompt 里有无。机械执行 |
| **维护成本** | 中。每次产出格式变更需同步主文件摘要 + 校验脚本。但变更频率低 |
| **叙事弹性** | 保留——校验脚本设 ±20% 容忍度，不断合法模糊值 |
| **新增依赖** | 校验脚本需 Python/PowerShell 运行时——sol 已具备 |
| **回滚风险** | 低。所有改动增量式——不改现有 step 文件内容，只在主文件追加摘要 |

---

## 七、执行清单

| # | 文件 | 改动 | 优先 |
|:-:|------|------|:--:|
| 1 | `pop-novel-writer/SKILL.md` | Step 1/2/3 各增加 ★ 输出路径 + 前置必读 + 硬性产出 + 新红线#10/#11 | P0 |
| 2 | `pop-novel-plot/SKILL.md` | Step 4/5/7/9/10/11 各增加 ★ 输出路径 + 硬约束 + 前置必读 | P0 |
| 3 | `pop-novel-bookstrap/SKILL.md` | Phase 0/3/5 各增加 ★ 输出路径 + 前置约束 | P0 |
| 4 | `expert-writer/SKILL.md` §3.1 | 任务类型切换检查 | P1 |
| 5 | `expert-writer/SKILL.md` §0 | §0.8：子 skill steps 加载完整性 | P1 |
| 6 | `pop-novel-plot/steps/step-12-output.md` | 追加"校验脚本触发点"表 | P1 |
| 7 | `pop-novel-writer/steps/step-5-state-update.md` | 追加 S3 校验触发点 | P1 |
| 8 | `scripts/check-*.py`（新建） | 3-4 个校验脚本 | P1 |
