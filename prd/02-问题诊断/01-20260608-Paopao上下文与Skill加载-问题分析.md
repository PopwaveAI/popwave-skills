# Paopao 上下文管理与 Skill 加载机制问题

> **合并来源：** 原 `01-Paopao上下文问题.md` + 原 `03-Skill调用失效.md`
> **合并日期：** 2026-06-23
> **原始日期：** 2026-06-08 ~ 2026-06-11
> **状态：** 大部分已修复，保留为历史参考

---

## 修复状态总览

| 问题 | 严重性 | 状态 | 修复版本 |
|:-----|:------:|:----:|:---------|
| Read 工具输出截断 | P0 | ✅ 已修复 | expert-writer v2.4.0（exec Get-Content 替代 Read） |
| SKILL.md 体积膨胀 | P1 | ✅ 已修复 | expert-writer v3.0.0（21K→9K，5块提取到 references/） |
| 对话历史冻结 | P0 | ⛔ 平台层问题 | workspace-index v2.0 补偿注入 |
| 无动态压缩 | P2 | ⛔ 平台层问题 | 暂停 |
| 持久状态不自动注入 | P1 | ✅ 已修复 | workspace-index.yaml v2.0 |
| 跨项目信息泄露 | P2 | ✅ 已修复 | expert-writer v3.0.0（删除所有项目名示例） |
| 会话隔离缺失 | P2 | ✅ 已解决 | Hermes Agent 迁移后彻底解决 |
| Manual Read 截断（~50%） | P0 | ✅ 已修复 | expert-writer v2.4.0 §0.1 元纪律 |
| 长会话惰性侵蚀 | P1 | ✅ 已修复 | workspace-index 注入 + 无条件路由前强制加载 |
| System prompt 不覆盖 steps/ | P1 | ✅ 已修复 | expert-writer §0.8 通用规则（读了就必须读完整） |
| 任务类型切换不强制路由 | P1 | ✅ 已修复 | expert-writer §3.1 Think 任务类型切换检查 |
| 「继续任务」意图未识别 | P1 | ✅ 已修复 | expert-writer §3.1 意图识别表补全 |

---

## Part A：Paopao 上下文管理问题（原 01 文档）

> 版本：v1.0 | 2026-06-11
> 数据来源：`6-10项目测试`（42 runs）+ `未命名项目`（38 runs）的 input.json / events.jsonl 全量审计

### 问题 1：Read 工具输出截断

Read 工具返回最大字符数 ≈2,416 chars，而 exec 工具 stdout 上限 ≈30,000 chars。expert-writer v2.3.0 的 SKILL.md 为 21,298 字符，Read 只能读到 11.3%。

**修复：** expert-writer v2.4.0 新增 §0.1 元纪律——禁止使用 Read 工具读取文档型文件，改用 `Get-Content -Encoding UTF8 -Raw`。截断率从 15/17 → 0/30。

### 问题 2：SKILL.md 体积膨胀

v2.5.0 的 SKILL.md 占 21,298 chars（~54% prompt），历史空间只剩 ~9K（约 7 轮对话）。

**修复：** expert-writer v3.0.0 将 5 个非核心 code block 提取到 `references/`，每次注入节省 12,427 chars（-57%），历史容量翻倍。

### 问题 3：对话历史冻结

Paopao 的 `injectedHistoryTurns` 上限为 ~20 轮，达到上限后历史不再更新——后续所有新对话都无法注入历史中。

**补偿方案：** workspace-index.yaml v2.0 新增 `change_log` + `requirements` + `progress` + `runtime.last_session`，agent 通过读取可恢复被冻结的上下文。

### 问题 4-7：无动态压缩 / 持久状态不注入 / 跨项目泄露 / 会话隔离

均为平台层问题或已通过 workspace-index 补偿解决。详见修复状态总览表。

---

## Part B：Skill 加载机制失效（原 03 文档）

> 版本：v4.0 | 2026-06-09
> 来源：6-9测试项目全量 47 次 run 的 input.json + events.jsonl 全量分析 + thinking 链深度审计

### 核心发现

1. **Manual Read 不是"50%执行"——是 50% 截断。** Read 工具输出的子 skill 文件只拿到 ~50% 内容
2. **长会话惰性侵蚀。** ch011-014 五轮连续零次 Read 子 skill 文件，agent 切换到"全凭记忆写"模式
3. **System prompt 注入也不够。** 关键输出指令在 step 子文件里，SKILL.md 主文件不覆盖

### 修复方案（已落地）

**§0.8 通用规则：** 技能目录中所有文档型文件（SKILL.md、steps/*.md、phases/*.md、templates/*.md、references/*.md 等），只要 Read 了就必须读完整。检测方法：检查最后一行行号，接近 250 则用 offset 续读。

**§3.1 Think 任务类型切换检查：** 当本轮 tasks 类型与上一轮不同（诊断→写作 / 修订→写作），强制重新进入完整 Think 流程，重新 Read 目标子 skill 的全部文档型文件。

**§3.1 意图识别表补全：** 新增「继续任务」「继续写」到典型说法，审视框架改为无固定框架——直接读 progress 判定路由。

### 排查技巧

**runs 目录信息最完整：**
- `input.json#prompt` → 完整 prompt（skill 有没有、版本对不对）
- `input.json#skills` → 本轮注入的 skill 列表及路径
- `events.jsonl` → 完整 thinking 链 + 所有 tool calls + Read 输出大小
- `response.md` → 最终输出

**Skill 定义位置：**
- `D:\popwave-skills\skills\{skill-id}\` → 源码（手动编辑）
- `C:\Users\AWMPRO\AppData\Roaming\paopao\remote-skills\{skill-id}\{version}\` → 缓存（Paopao 实际加载）

---

> **根因一句话：** Paopao 平台层的 Read 工具截断 + 对话历史冻结 + 无持久状态注入，导致 agent 在长会话中拿到残缺指令、丢失上下文、依赖错误记忆。Skill 层通过 §0.1 元纪律（禁用 Read）+ §0.8 通用规则（读了必须读完）+ workspace-index 补偿方案系统性修复。
