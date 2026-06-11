---
name: pop-novel-bookstrap
description: 从故事引擎到可执行项目骨架的开书管线。当用户说"开书"/"新书"/"启动项目"/"设世界观"/"续写"时启用。支持 forward（新书）和 reverse（续写）两种模式。新增 Phase 0.6(拆书融合)+Phase 6(起点)+Phase 7(终点)。
pipeline:
  upstream: [pop-novel-deconstructor, download-webnovel-txt]
  downstream: [pop-novel-plot]
---

# 开书启动

从故事引擎到可执行项目骨架的完整开书管线。产出 story-engine.yaml、L1 设定层、数值体系。

---

## ❌ 质量红线（开工前→完工后自检）

开工前：先看红线，知道什么不能碰。完工后：勾 [ ]，确认达标。不过则退回重改。

### forward 模式

| # | 标准 | 完工确认 |
|:-:|:-----|:--------:|
| ❌1 | **story-engine.yaml 已锁定** — 追问 2-3 轮后用户确认 engine 方向。未锁定不进 L1 设定 | [ ] |
| ❌2 | **跨域素材聚合已完成** — Phase 0.5 不可跳过。至少聚合 3 个不同领域的素材（不限于网文） | [ ] |
| ❌3 | **L1 六件套闭环** — 世界蓝图→力量体系→历史驱动力→物种天赋→势力格局→资源物品形成逻辑环。断环即退回 | [ ] |
| ❌4 | **世界稳定性检验通过** — 7 项 checklist 全部通过。未通过不进 Phase 3 | [ ] |
| ❌5 | **数值体系已生成** — combat_capability + monster_rank_map + act_rank_schedule 齐全 | [ ] |
| ❌6 | **project.yaml 路径注册** — 产出文件路径已注册 | [ ] |
| ❌7 | **不准用二手资料代替原文** — 参考书分析必须基于原文 | [ ] |
| ❌8 | **不准在无故事引擎的情况下直接设计设定** — 用户要求"先写设定"→ 回 Phase 0 | [ ] |
| ❌9 | **拆书成果已消费** — 有锚点书 deconstructor 产出但不读取不融合 → 退回 Phase 0.6 | [ ] |
| ❌10 | **起点快照已锁定** — Phase 6 产出未经用户确认不进 plot | [ ] |
| ❌11 | **终点快照已锁定** — Phase 7 产出未经用户确认不进 plot | [ ] |

### reverse 模式（额外的检查）

| # | 标准 | 完工确认 |
|:-:|:-----|:--------:|
| ❌R1 | **事件日志覆盖全部正文** — 每 10 章至少 1 条日志，不得跳过阅读直接提取设定 | [ ] |
| ❌R2 | **产出格式与 forward 一致** — 走完 reverse 后项目状态等同于 forward | [ ] |
| ❌R3 | **交接验证报告已输出** | [ ] |

---

## 什么时候使用

| 场景 | 模式 | 说明 |
|:-----|:-----|:------|
| **新书开坑** | forward | 从零搭建完整的小说项目骨架 |
| **创意可行性验证** | forward | 不确定创意能否撑起长篇，需系统检验 |
| **已有正文需续写** | reverse | 已有 N 章正文但无标准设计层，逆向提取设定再续写 |
| **设定规范化** | forward | 已有零散设定，需结构化、分层化、标准化 |

**不适用**：短篇（<10万字）→ 用 light-bootstrap；仅需稳定性检查 → 用 world-stability-check。

---

## 执行顺序（两条决策路径）

```
用户的场景？
   ├─ 新书/从零启动 → forward 路径（3步）
   └─ 续写/已有正文 → reverse 路径（3步）
```

### Forward 路径（新书三部曲）

```
Step 1 ─ 故事引擎设计（Phase 0）
  接住用户想象 → 追问 2-3 轮 → 输出 story-engine.yaml
  ★ 输出: L0-产品层/story-engine.yaml
  ★ 前置: 已有参考书拆解报告 → 必须先读 T1+T4+T5+T7 再写。禁止凭记忆写原著事实。
  ❌ 用户说"直接写设定"：退回，故事引擎没锁定就不进设定

Step 2 ─ 素材采集 + 拆书融合（Phase 0.3 → 0.4 → 0.5 → 🆕0.6）
  参考书甄别 → 金手指设计 → 跨域素材聚合 → 拆书成果融合
  ★ 输出: L0-产品层/deconstruct-融合摘要.md
  ✅ Phase 0.5 是 HARD-GATE，不可跳过
  ✅ 至少聚合 3 个不同领域的素材
  ✅ Phase 0.6 如有锚点书 deconstructor 产出则不可跳过

Step 3 ─ 设定与验证（Phase 1 → 1.2 → 1.3 → 1.5 → 3 → 4 → 5）
  L1 六件套（新分类） → 深度展开 → 交叉关联
  → 稳定性检验（checklist） → 项目骨架 → 读者画像校对 → 数值体系
  ★ 输出 Phase 3: chapter-state.yaml + project.yaml + 状态/角色/角色卡
    ★ 主角卡末尾: 成长轨迹 22 行逐章段（字段名从 combat_capability 读取·不确定的留{待plot填充}）
  ★ 输出 Phase 5: combat_capability + monster_rank_map + act_rank_schedule + collision_curve
    ★ 数值体系文件必须从本项目的 L1 力量体系推导——不照搬任何参考书的段位命名

Step 4 ─ 锚点设计（🆕Phase 6 → 🆕Phase 7）
  起点快照 → 终点快照 → 两者均需用户确认才能进 plot
  ★ 输出: 设计/起点快照.md + 设计/终点快照.md
```

### Reverse 路径（续写三部曲）

```
Step 1 ─ 逆向工程（Phase r1）
  逐章读取原文，产出事件日志 + 批次摘要
  ❌ 只读梗概不读原文：退回

Step 2 ─ 设计层提取（Phase r2 → r3）
  提取 L0 产品层 + L1 元设定层

Step 3 ─ 宪法 + 大纲 + 交接（Phase r4 → r5 → r6）
  写作宪法 → 卷大纲 → 交接验证报告
```

---

## ❌ 错误示例

### WRONG 1：故事引擎没锁定就写设定

```
用户：我要写穿越到修仙世界的小说
Agent：直接开始写 L1 世界观设定
❌ 错误：没有先跟用户完善故事方向就直接进入执行
✅ 正确：先接住用户的话 → 追问 2-3 轮（冲突？角色？基调？）→ 锁定 story-engine.yaml
   用户说"对"再进 Phase 1
```

### WRONG 2：续写跳过逐章阅读

```
用户：这里有 388 章正文，帮我续写
Agent：直接提取设定开始写大纲
❌ 错误：没有事件日志就直接提取设定
✅ 正确：先跑 Phase r1，至少细读前 10 章
```

### WRONG 3：跨域素材聚合跳过了

```
用户：我要写克苏鲁修仙
Agent：只拆了 3 本网文参考书
❌ 错误：同质素材聚合 = 信息茧房
✅ 正确：网文参考书 + 志怪文学 + 民俗学纪录片
```

---

## 异常与边界条件

管线假设环境理想，但实操常遇异常。以下预定义 fallback，保证过程不会"一跑就卡住"。

| 场景 | 触发条件 | 处理动作 |
|:-----|:---------|:---------|
| **正文文件找不到**（reverse） | Phase r1 读取 ch001 时文件不存在 | 提示用户提供正文文件，**不退回到编造数据**。暂停管线，等文件就绪后再继续 |
| **WebSearch 不可用**（Phase 0.3/0.5） | 搜索参考书或跨域素材时搜索工具返回不可用 | 降级为本地知识库 + 内置素材库。搜索降级不影响后续相位，但产出需标注"未做在线搜索" |
| **对标书用户未提供** | Phase 0.3 入口检查发现对标书数量为 0 | 提示用户至少需要 1 本同类参考书。用户拒绝提供 → 使用通用节奏模板代替拆书，标注"无参考书" |
| **L1 设定与 story-engine.yaml 冲突** | Phase 1 推演时发现设定方向偏离 engine.core_premise | 暂停 Phase 1，输出冲突说明返回用户决策。不自行修正，不静默覆盖 |
| **世界稳定性检验发现不可逆断裂** | Phase 1.5 checklist 有多项不通过 | 暂停推进。输出"断裂报告"并标注严重程度。用户决定修复方向（调整设定 / 接受断裂 / 重新开书） |
| **用户中途改变平台**（如番茄→起点） | Phase 3+ 阶段用户明确表示平台变更 | 退回 Phase 0 重建 reader_profile + 平台节奏基准。不追加补丁，不假装兼容 |
| **数值体系与剧情阶段不匹配** | Phase 5 数值模板生成后发现跨级战约束与 L1 设定冲突 | 优先遵守数值体系约束（段位差≥2 不可战）。冲突输出到 project.yaml 的异常备注字段，标注"体系规则优先" |
| **reverse 模式正文不足 10 章** | Phase r1 发现正文少于 10 章（如仅 8 章） | 改为全部细读模式（不按 10 章分批）。如果正文少于 3 章 → 建议切换为 forward 模式 |
| **phase-*.pe.md 文件缺失** | 执行某 Phase 时相位文件不存在 | 从 SKILL.md 的步骤描述中自行推导执行流程。产出标注"无 .pe.md 文件，手动执行" |
| **子 agent 启动失败** | preflight 检查通过但子 agent 无法创建 | master 手动执行，必须声明"子agent不可用，master手动执行"，并在产出后走验收清单 |

**原则**：异常先告知用户，再按规则处理。绝不静默跳过或静默编造数据。

以下相位文件包含各步骤的详细 guide 和模板。SKILL.md 没有列出全部细节，按需加载。

### Forward 参考

| 阶段 | 执行指令 | 参考文档 |
|:-----|:---------|:---------|
| Phase 0 — 故事引擎 | `phases/phase-0.pe.md` | 内嵌 |
| Phase 0.3 — 参考书甄别 | `phases/phase-0.3.pe.md` | 内嵌 |
| Phase 0.4 — 金手指设计 | `phases/phase-0.4.pe.md` | 内嵌 |
| Phase 0.5 — 跨域素材 | `phases/phase-0.5.pe.md` | 内嵌 |
| Phase 1 — L1 骨架 | `phases/phase-1.pe.md` | 内嵌（含完整 schema+示例） |
| Phase 1.2 — L1 深度展开 | `phases/phase-1.2.pe.md` | — |
| Phase 1.3 — L1 交叉关联 | `phases/phase-1.3.pe.md` | — |
| Phase 1.5 — 稳定性检验 | `phases/phase-1.5.pe.md` | — |
| Phase 3 — 项目骨架 | `phases/phase-3.pe.md` | 内嵌（含完整 schema） |
| Phase 4 — reader_profile 校对 | `phases/phase-4.pe.md` | — |
| Phase 5 — 数值体系 | `phases/phase-5.pe.md` | 内嵌（含模板+四段框架） |
| 🆕 Phase 0.6 — 拆书融合 | `phases/phase-0.6.pe.md` | 内嵌 |
| 🆕 Phase 6 — 起点快照 | `phases/phase-6.pe.md` | 内嵌 |
| 🆕 Phase 7 — 终点快照 | `phases/phase-7.pe.md` | 内嵌 |

### Reverse 参考

| 阶段 | 执行指令 | 参考文档 |
|:-----|:---------|:---------|
| Phase r1 — 事件日志 | `phases/phase-r1.pe.md` | 内嵌（含模板+格式） |
| Phase r2 — L0 提取 | `phases/phase-r2.pe.md` | — |
| Phase r3 — L1 提取 | `phases/phase-r3.pe.md` | — |
| Phase r4 — 宪法提取 | `phases/phase-r4.pe.md` | — |
| Phase r5 — 卷大纲确认 | `phases/phase-r5.pe.md` | — |
| Phase r6 — 交接验证 | `phases/phase-r6.pe.md` | — |

---

## 版本

v3.0.0 | 2026-06-05 | 完整变更记录 → [CHANGELOG.md](CHANGELOG.md)
