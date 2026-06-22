---
name: pop-writer-chapter
description: "章纲设计/导演卡。消费 plot v7.6 的幕纲(act-YY.md)+剧情线文档，产出含事件链/情绪弧/爽点机制/章末钩子/契诃夫枪/调味空间的设计包。"
pipeline:
  upstream: [pop-writer-plot]
  downstream: [pop-writer-prose]
  references: [pop-trope-library]
version: 2.2.0
---

# pop-writer-chapter · 章纲设计 / 导演卡 v2.2.0

> **定位：消费 plot 的幕纲 + 剧情线，产出回合级事件链设计包。**
> **核心约束：不碰文风。不写叙事者声音、不写句子节奏、不写修辞风格。**

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| 1 | **上游未就绪** — `剧情设计/幕/vol-XX/act-YY.md` 或 `剧情设计/剧情线/` 缺失 → 终止 |
| 2 | **entity-snapshot 不存在也未初始化** — 终止（CH1 由本章 step-1 初始化） |
| 3 | **出场角色不可追溯** — 事件引用角色不在剧情线登场人物中 → 退回 |
| 4 | **事件密度不达标** — 事件数 < 章字数 ÷ 200 → 退回 |
| 5 | **缺 scene/POV/关键对白/感官锚点** — 任缺一 → 退回 |
| 6 | **爽点未标注** — 每个 ◆小爽点 / ★中爽点事件必须标注 |
| 7 | **情绪弧线缺失** — 设计包缺情绪弧线可视化段 → 退回 |
| 8 | **章末钩子缺预期回收章** — 钩子必须有预期回收位置 → 退回 |
| 9 | **契诃夫枪未同步** — 本章设伏/回收的枪必须在 act-YY.md 枪链段同步 |
| 10 | **关键对白缺语气/潜台词** — 不可替换对白必须标注 |
| 11 | **调味空间缺失** — 设计包缺调味空间段 → prose 不知道调味边界 |
| 12 | **未查套路库就定事件链** — `pop-trope-library/套路库/{套路名}.md` 有公式和节奏控制，不查=重新发明 |

## 速查表（完整目录引导）

### steps/ — 执行层

| 什么时候 | 读什么文件 | 产出 | 门禁 |
|:---------|:----------|:-----|:-----|
| 第 1 步 | `steps/step-1-read-canvas.md` | 基线（内存，6 块结构） | ❌ 幕纲/entity-snapshot/剧情线 缺一终止 |
| 第 2 步 | `steps/step-2-event-chain.md` | 完整设计包 | ❌ 密度/爽点/字段 不达标退回 |
| 第 3 步 | `steps/step-3-output.md` | 设计包落盘 + entity-snapshot 更新 + 枪链同步 | ❌ 缺落盘退回 |

### templates/ — 模板层

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| Step 1 | `templates/baseline.tpl.md` | 基线（6 块结构，内存） |
| Step 2/3 | `templates/fact-skeleton.md` | 设计包（事件链 + 全部设计层） |

### references/ — 知识层（读后理解，指导操作）

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| Step 2 设计爽点时 | `references/payoff-guide.md` | 四级爽点承接规则（◆小爽点≥5 + ★中爽点≥1） |
| Step 2 标注情绪时 | `references/emotional-beats.md` | 情绪词汇表 + 弧线检查规则 |
| Step 2 设计角色时 | `references/character-scheduling.md` | 角色调度：before 状态 / 台词风格 |
| Step 2 设计地点时 | `references/location-orchestration.md` | 空间编排：地点来源 / 地理可达 |
| Step 2 信息释放时 | `references/info-release.md` | 信息释放：分配规则 / 密度检查 |
| 批量 / 连续章节 | `references/continuous-chapter-workflow.md` | 连章顺序 + 并行委托 |

### 外部依赖

| 什么时候 | 读什么文件 | 产出 |
|:---------|:----------|:-----|
| Step 2 部署套路时 | `pop-trope-library/套路库/{套路名}.md` | 套路公式 + 节奏控制 |

## 核心流程

### 步骤1：建立基线
**读什么：** `剧情设计/幕/vol-XX/act-YY.md`（全文）、`状态/entity-snapshot.yaml`、`剧情设计/剧情线/{活跃线}.md`
**做什么：** 建立结构化基线——本章位置/Canvas约束/角色现状/活跃线上下文/篇幅预算。基线在内存，不落盘。
**❌ 门禁：** 幕纲/entity-snapshot/剧情线 缺一终止。CH1 时初始化 entity-snapshot（从角色卡+起点快照组装）。

详细指令见 `steps/step-1-read-canvas.md`。

### 步骤2：正式设计
**预加载：** 基线 + `正文/ch{上一章}.md` 最后 ~500 字 + `references/payoff-guide.md` + `状态/角色/{登场角色}-角色卡.md`
**按需查：** `pop-trope-library/套路库/{套路名}.md`（用到套路时）+ `references/` 下各文件（设计到对应维度时）
**做什么：** ①预加载衔接+规则+角色 → ②逐事件设计事件链 → ③补充设计层（情绪弧/爽点表/钩子/调味空间/对白语气/枪表/信息释放）
**❌ 门禁：** 事件数不达标/缺字段/爽点不足/章首高潮/情绪断裂 任一 → 退回

详细指令见 `steps/step-2-event-chain.md`。
### 步骤3：产出落盘
**读什么：** Step2 事件链
**做什么：** 写入设计包（含事件链/情绪弧/爽点机制/钩子/枪链/调味空间/对白分析）+ 更新 `状态/entity-snapshot.yaml`（after 状态）+ 回写 act-YY.md 枪链段
**产出：** `章节设计包/chXXX-设计包.md`
**❌ 门禁：** 缺落盘退回；entity-snapshot 未更新退回

详细指令见 `steps/step-3-output.md`。

## ❌ WRONG 示例

| ❌ 错误 | ✅ 正确 |
|:--------|:-------|
| 事件内容写「一场激烈的战斗爆发了」 | 事件内容写「目标转身拔剑——刀从侧面切入他右腕」 |
| 关键对白写「主角嘲讽对方」 | 关键对白写原文「废物。」 |
| 凭记忆写角色 before 状态 | 从 `状态/entity-snapshot.yaml` 取 |
| 枪链更新写到独立 chekhov-tracker.md | 回写到 `剧情设计/幕/vol-XX/act-YY.md` 枪链段 |
| 不查套路库直接设计事件 | 先查 `pop-trope-library/套路库/{套路名}.md` 节奏控制段 |

## 本阶段边界

| 做什么 | 不做什么 |
|:-------|:---------|
| 事件链设计（含情绪/爽点/钩子/枪链） | ❌ 不渲染正文 |
| 爽点设计层（套路/情绪弧线/爽点机制） | ❌ 不验证剧情逻辑 |
| 调味空间标注 | ❌ 不修改剧情线文档 |
| entity-snapshot 更新 | ❌ 不替 prose 做文风决策 |

## 边界条件

| 场景 | 处理 |
|:-----|:-----|
| CH1 entity-snapshot 不存在 | step-1 初始化：从角色卡+起点快照组装 |
| 登场角色卡缺失 | 终止，不凭记忆编造 |
| Canvas 无 payoff 供给 | 兜底制造中爽点（微释放/对话揭示/内部抉择） |
| 连续 ≥3 章无释放 | 通知 plot 建议增加 S 线 |
| 跨章弧线 | 标注 arc_span + 本章位置 + 情绪分工 |

## 落盘检查点

| 确认项 | 状态 |
|:-------|:-----|
| `章节设计包/chXXX-设计包.md` 已写入 | [ ] |
| `状态/entity-snapshot.yaml` 已更新 | [ ] |
| `剧情设计/幕/vol-XX/act-YY.md` 枪链段已同步 | [ ] |
| 设计包含全部节（事件链/情绪弧/爽点机制/钩子/枪链/调味空间/对白分析） | [ ] |

## 版本

v2.2.0 | 2026-06-22 | 全量对齐 plot v7.6 + PRD v5.3：路径修复/entity-snapshot 归属 chapter/Step 拆分为基线+正式设计/瘦身 → [CHANGELOG.md](CHANGELOG.md)
