# PRD-03: Skill加载弱保障

> **严重级别：** P0 / 严重
> **来源文档：** 01, 05, 06, 15, 17
> **最后更新：** 2026-07-01

---

## 问题概述

Popwave（OpenClaw）的 skill 加载分两层——强保障（程序硬注入）仅覆盖元 skill 的 SKILL.md，弱保障（prompt 唤起）覆盖所有 step / references / 下游 skill 文件。跨 14 个项目 435 个 runs 的数据证实，3 轮对话后 skill 文件读取率从 11.1% 骤降至 0-3%，agent 完全切换到对话记忆模式运行。这是 skill 机制"存在但 agent 感知不到"的系统性问题。

---

## 根因分析

### 强保障（100%保证）

仅元 skill（如 expert-writer / pop-decon）的 SKILL.md 由 host 层每次 run 强制注入 prompt。

### 弱保障（依赖 agent 主动 readFile）

元 skill 的 step 文件、references 文件，以及所有下游 skill（plot / create / seed 等）的全部文件。

### agent 行为退化路径

agent 在第 1 轮被注入元 skill SKILL.md，第 2-3 轮可能主动读取一次下游 skill，但从第 3 轮起完全切换到对话记忆模式：cacheRead 积累到 100K tokens 时判断"不需要再读"，后续行为基于对话历史中的摘要理解和错误推断。

### Context 管理机制不覆盖 skill 生命周期

会话剪枝后不重注入 skill 文件，bootstrap files 限制只管启动时加载。

---

## 证据链

### 文档17（17-1, 17-2）

- 435 runs 中仅 16 个（3.7%）检测到 skill 读取
- 按对话轮次读取率：0-3 轮 11.1% → 3-6 轮 0.0% → 6-10 轮 1.7% → 10-15 轮 3.1% → 15-20 轮 2.2% → 20+ 轮 3.3%
- 按 cacheRead：100-200K tokens 区间读取率 0.0%
- 6-30-项目d turns=0 的 run 读了 7 个 skill 文件，但后续 15 轮全部不读
- OpenClaw 有 6 项 context 管理机制但 skill 文件注入不在覆盖范围

### 文档05（05-1 Gap-15）

- agent 完整加载 SKILL.md 看到速查表中全部路径，但只执行"产出"列——只加载 step-1 就完成整个 plot 阶段
- 消息 #36→#37 工具调用日志：SKILL.md ✅ → step-1 ✅ → step-2~6 ❌ → 3 个模板 ❌ → references ❌ → 直接 write 全部产出

### 文档06（06-1 G-P1）

- plot 阶段仅加载 SKILL.md + step-1 + volume-outline 模板，step-2~6、plotline-doc 模板、act-outline 模板、payoff-design-guide、套路库、剧情库全部未加载
- 剧情线模板要求 17 模块，agent 产出 3 个

### 文档15（15-2）

- 框架每个 assistant 回合注入 skillPath=expert-writer/9.2.0（122 次出现），但 SKILL.md 从未被显式读取（Grep 零匹配）
- step 文件仅在 ch001 阶段被读取（idx=31/37/41/43），ch002 / ch003 一次都没有读取 step 文件

---

## 影响表现

- 用户指令"飓风营救做主干"正是外部燃料台机制，但 agent 没读到该机制，把参考平权并列
- ch002 / ch003 凭记忆走流程 → 流程漂移 → Step4 质检退化为文本声明"全通过"
- 剧情线文档 17 模块只产出 3 个；ch01 正文未经验证直接交付
- 约束细节（红线/门禁/check）随章节推进逐章遗忘，执行从"按 skill 走"退化为"按惯性走"
- skill 被更新后 agent 不会感知到变化

---

## 历史演进时间线

| 时间 | 文档编号 | 发现 |
|:-----|:---------|:-----|
| 6-8 | 01-7 | 长会话惰性侵蚀，agent 放弃 Read 改用记忆 |
| 6-22 | 05-1 | 步骤链无加载门禁，只读 step-1 就完成整个阶段 |
| 6-22 | 06-1 | 逐 skill 证据：plot 阶段 17 模块仅产出 3 个 |
| 6-27 | 15-2 | skillPath 注入不保证每章参照，ch002/ch003 零 step 读取 |
| 7-1 | 17-1/17-2 | 435 runs 量化确认 + context 管理不覆盖 skill 生命周期 |

---

## 相关文档

- [01-20260608-Paopao上下文与Skill加载-问题分析](../01-20260608-Paopao上下文与Skill加载-问题分析.md)
- [05-20260622-东方版深渊主宰-问题分析](../05-20260622-东方版深渊主宰-问题分析.md)
- [06-20260622-东方版深渊主宰-逐Skill复盘-问题分析](../06-20260622-东方版深渊主宰-逐Skill复盘-问题分析.md)
- [15-20260627-v3.3项目d前三章复盘-核心根因分析](../15-20260627-v3.3项目d前三章复盘-核心根因分析.md)
- [17-20260701-Agent跳过Skill文件读取-跨项目435runs数据分析](../17-20260701-Agent跳过Skill文件读取-跨项目435runs数据分析.md)
