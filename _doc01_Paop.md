> **📌 修复状态** ｜ 本文档 7 个问题的修复进展（数据截至 2026-06-12）：
> - **P0-Read截断** → expert-writer v2.4.0 修复 ✅（exec Get-Content 替代 Read）
> - **P1-SKILL.md膨胀** → expert-writer v3.0.0 修复 ✅（21K→9K，5块提取到 references/）
> - **P0-历史冻结** → workspace-index v2.0 补偿注入 ✅
> - **P2-无动态压缩** → 平台层问题，暂停
> - **P1-持久状态不注入** → workspace-index.yaml 修复 ✅
> - **P2-跨项目泄露** → 已修复 ✅
> - **P1-会话隔离缺失** → 子 agent 架构（Hermes 迁移后彻底解决）

# Paopao 上下文管理问题 PRD

> 版本：v1.0 | 2026-06-11  
> 数据来源：`6-10项目测试`（42 runs）+ `未命名项目`（38 runs）的 input.json / events.jsonl 全量审计  
> 分类：系统级问题报告

---

## 目录

- 一、问题总览
- 二、问题 1：文件读取截断
- 三、问题 2：SKILL.md 体积膨胀
- 四、问题 3：对话历史冻结
- 五、问题 4：无动态压缩机制
- 六、问题 5：无持久状态自动注入
- 七、问题 6：跨项目信息泄露
- 八、问题 7：会话隔离缺失
- 九、修复状态
- 十、附录：证据索引

---

## 一、问题总览

| # | 问题 | 严重性 | 影响范围 | 已修复 |
|-|-|-|-|-|
| 1 | Read 工具输出截断 | **P0** | 所有子 skill 的 SKILL.md 读取 | ✅ expert-writer v2.4.0 |
| 2 | SKILL.md 体积膨胀 → 上下文窗口挤压 | **P1** | 每次注入占 21K，挤占历史空间 | ✅ expert-writer v3.0.0 (21K→9K) |
| 3 | 对话历史冻结（injectedHistoryTurns 封顶） | **P0** | 所有长对话项目 | ⛔ 平台层问题，skill 层通过 workspace-index 补偿 |
| 4 | 无动态压缩 | **P2** | 长对话场景 | ⛔ 平台层问题 |
| 5 | 项目持久状态不自动注入 | **P1** | 跨轮次记忆一致性 | ✅ workspace-index.yaml v2.0 (requirements + change_log) |
| 6 | SKILL.md 中含跨项目名示例 | **P2** | agent 思维链泄露其他项目信息 | ✅ expert-writer v3.0.0 (全部删除) |
| 7 | 会话间无上下文传递 | **P2** | 新建会话需重新扫描 | ⛔ 设计如此，由 workspace-index 补偿 |

---

## 二、问题 1：文件读取截断 — Read 工具输出截断 bug

### 发现

在 6-10项目测试（42 runs）的审计中首次发现。

### 根因

Paopao 的 Read 工具有固定的输出长度上限。实测数据显示：

```
Read 工具返回的最大字符数: ≈2,416 chars
exec 工具 stdout 上限:     ≈30,000 chars
```

对比：expert-writer v2.3.0 的 SKILL.md 大小为 21,298 字符（无 frontmatter），Read 工具只能读到 **2,416 / 21,298 = 11.3%**。这意味着 SKILL.md 尾部大约 89% 的内容（包括质量红线、Reflect 审视、修改路由步骤）全部不可见。

### 证据链

**6-10项目（v2.3.0）42 runs 全量审计结果：**

| Run | Read 次数 | 截断文件数 | 典型截断率 |
|-|-|-|-|
| baaf4df2 | 9 | 7/9 | 9%～35%（workspace-index.yaml） |
| d2b5d0b4 | 17 | **15/17** | 仅 2 个文件完整 |

```
被截断的关键文件：
  workspace-index.yaml       → 9~35%（4次读取全部截断）
  深渊主宰-三维拆书档案.md     → 55%
  深渊主宰-T4-剧情全貌.md     → 10%
  deconstructor SKILL.md     → 36%
```

**定性分析（bookstrap SKILL.md 为例）：**

SKILL.md 中定义了 Phase 1 → 1.2 → 1.5 → 3 → 4 → 5 → 6 → 7 共 8 个 phase。Phase 5（数值体系）定义在文件的 64-78% 区域。当 Read 工具只能读取前 22% 时：

```
Agent 看到的：Phase 1(L1六件套) → Phase 3(宪法) → …后面没了
Agent 没看到的：Phase 1.2(深度展开) / Phase 5(数值体系) / Phase 6-7(起点/终点快照)
→ 直接跳过了数值体系
→ 用户说"数值体系也需要 一切需要的前置文件都补全"时才补上
```

**未命名项目（v2.5.0/v3.0.0）对比验证：**

应用 §0.1 元纪律（禁止 Read 工具，改用 `exec + Get-Content`）后：

| 版本 | Read 次数 | 截断文件数 | 违反 §0.1 |
|-|-|-|-|
| v2.3.0 (d2b5d0b4) | 17 | 15/17 | ❌ 全部违反 |
| **v2.5.0 (628fd83c)** | **0** | **0/30** | **✅ 完全合规** |

所有 v2.5.0 及以上版本的 runs 中，SKILL.md 和文档文件的读取全部通过 `Get-Content -Encoding UTF8 -Raw` 完成，截断率为 0。

### 修复

**expert-writer v2.4.0** 新增 **§0.1 元纪律**：

```
禁止使用 Read 工具读取子 skill 的文档型文件和 YAML 文件。
改为统一用 exec 工具执行 `Get-Content -Encoding UTF8 -Raw` 读取。
仅当文件字符数 > 25,000 时，才回退到 Read 工具 + offset 分段读取。
```

---

## 三、问题 2：SKILL.md 体积膨胀 — 文件太大致上下文污染

### 发现

expert-writer 作为元 Skill，每次 Paopao 注入对话时都会携带完整的 SKILL.md 内容。当 SKILL.md 过大时，直接挤占对话历史的空间。

### 数据

| 版本 | SKILL.md 大小 | 占 prompt 比例 | 历史空间余额 |
|-|-|-|-|
| v2.3.0 | 17,008 chars | \~47% | 约 13K |
| v2.5.0 | 21,298 chars | \~54% | 约 9K |
| **v3.0.0** | **8,871 chars** | **\~25%** | **约 21K** |

### 膨胀来源

v2.5.0 的 21,298 字符构成：

```
§0 纪律表                    1,345c (6%)
§2 Skill 清单                1,266c (6%)
§3.0 全局感知                 2,456c (11%)
§3.1 Think（含动态融合示例）  5,116c (23%)  ← 最大块
§3.1.5 信息增强               1,187c (5%)
§3.1.6 管道校验               1,682c (8%)
§3.2 Execute（含闸门表）      1,437c (7%)
§3.3 Reflect（四层审视）      3,688c (17%)
§4 典型路径 + §5 修改路由      1,459c (7%)
§6 完成后引导 + §7 输出规范    1,661c (8%)
```

**可提取部分**：5 个 code block 占 \~9,246c（43%），这些不是每轮需要的核心指令。

### 影响

```
SKILL.md 占 21K → 对话历史只剩 9K（约 7-8 轮对话）
SKILL.md 降到 9K → 对话历史有 21K（约 15-18 轮对话）
→ 瘦身后的 SKILL.md 让历史容量翻倍
```

### 修复

**expert-writer v3.0.0** 将 5 个非核心 code block 提取到 `references/`：

| 提取内容 | 原大小 | 提取到 | 加载时机 |
|-|-|-|-|
| Reflect L1-L4 审视清单 | 3,565c | `references/reflection.md` | Reflect 阶段按需加载 |
| 动态融合（含示例） | 3,149c | `references/dynamic-fusion.md` | 用户追加核心设定时 |
| 管道校验 + 大环节自检 | 3,205c | `references/pipeline-check.md` | 路由前校验 |
| 完成后引导模板 | 1,775c | `references/completion-guide.md` | Reflect 阶段末尾 |
| 典型路径速查 | 907c | `references/typical-paths.md` | 首次路由时 |

每次注入节省 **12,427 chars**（43% 的上下文窗口）。

---

## 四、问题 3：对话历史冻结 — 注入极限后的静默失忆

### 发现

Paopao 的 `injectedHistoryTurns` 字段上限为 \~20 轮。达到上限后，对话历史不再更新——后续所有新对话都无法注入历史中。

### 机制

通过分析未命名项目的 38 个 runs 的 input.json，发现历史注入的行为模式：

```
prompt 结构：
  ├── Paopao 平台指令 (~900c) 
  ├── SKILL.md 完整内容 (~9-21K)
  └── Conversation history (User: / Assistant: 格式，纯文本)
  └── User instruction: (当前消息)
```

注入方式：**从头开始填充，到上限后冻结。**

```
injectedTurns=0  → 无历史（新会话）
injectedTurns=2  → 包含最早的 2 轮对话
injectedTurns=10 → 包含最早的 10 轮对话
injectedTurns=18 → 包含最早的 18 轮对话（接近上限）
injectedTurns=20 → 包含最早的 20 轮对话 ← 达到上限
```

**超过 20 轮后：**

```
injectedTurns=20 → 历史 = 最早的 20 轮（~25K chars）
injectedTurns=20 → 历史 = 同上（冻结！后续 7 次 run 不变）
injectedTurns=20 → 历史 = 同上（冻结！）
...
```

### 证据

未命名项目 `89c730e0` 会话的时间线：

| 时间 | Run | turns | 历史尾部内容 |
|-|-|-|-|
| 12:51 | first | 0 | — |
| 13:09 | bac2 | 8 | 清空项目后的初始设定 |
| 13:27 | 430c | 12 | bookstrap 阶段 |
| 13:56 | efb5 | 20 | 外神线融合完成 |
| **14:09** | **6ca6** | **20** | **外神线融合完成（冻结！）** |
| **14:12** | **939e** | **20** | **外神线融合完成（冻结！）** |
| **14:14** | **95e9** | **20** | **外神线融合完成（冻结！）** |
| **14:16** | **8b55** | **20** | **外神线融合完成（冻结！）** |
| **14:18** | **2ed4** | **20** | **外神线融合完成（冻结！）** |
| **14:20** | **9aed** | **20** | **外神线融合完成（冻结！）** |

14:09 之后又跑了 7 次 run，**历史内容完全相同**——agent 不知道用户后面说了"进入 plot"、"数值体系补齐"、"进入下一阶段"等信息。

### 影响

```
冻结前（13:56）：  agent 知道"外神线融合完成，下一步进入数值体系"
冻结后（14:09~）：  agent 停留在"外神线融合完成"  
                   → 用户说"进入下一阶段"
                   → agent 收到的当前指令是"进入下一阶段"
                   → 但参考的历史是 6 轮之前的对话上下文
                   → 只能靠扫描文件系统重新判断当前状态
```

### 与 v2.5.0 的 SKILL.md 瘦身联动

SKILL.md v2.5.0 占 21K → 历史空间只有 \~9K（约 7 轮对话），7 轮后即冻结。

SKILL.md v3.0.0 降到 9K → 历史空间有 \~21K（约 17 轮对话），17 轮后才冻结。

瘦身约**翻倍**了对话历史容量，但不能根本解决——长对话项目（100+ 轮）仍然会冻结。

### 修复

⛔ **平台层问题**，skill 层面无法修复。补偿方案：

**workspace-index.yaml v2.0** 新增：

- `change_log` — 记录每次 skill 执行完成后的产出摘要（语义级 git log）
- `requirements` — 记录用户提出的所有核心需求及状态
- `progress` — 记录管线进度（last_completed_skill / next_skill / checkpoints）
- `runtime.last_session` — 记录上轮会话的项目/任务/状态

Agent 通过读 workspace-index.yaml 可恢复大部分被冻结的上下文。

---

## 五、问题 4：无动态压缩机制

### 发现

Paopao 在 injectedHistoryTurns 达到上限后，既不截断最早的历史（丢弃老的保留新的），也不压缩消息（用摘要替代完整内容），而是直接冻结。

### 对比：理想方案 vs 实际行为

| 方案 | 行为 | Paopao 是否实现 |
|-|-|-|
| **FIFO 丢弃** | 超过上限后丢弃最早的 1 轮，追加最新的 1 轮 | ❌ |
| **摘要压缩** | 用摘要压缩早于 N 轮前的消息 | ❌ |
| **重要性排序** | 保留关键消息（用户需求/产出记录），丢弃非关键消息 | ❌ |
| **当前行为** | 达到上限后停止更新，不丢不压 | — |

### 影响

```
FIFO 丢弃方案下：
  agent 可能丢掉"清空项目"但收到"写了 ch005"
  → 不知道项目初始状态，但知道当前状态
  → 通过扫描文件系统可恢复

冻结方案下：
  agent 记得"清空项目"和"写 ch001"  
  → 不知道当前已写到 ch005
  → 以为自己在写 ch002
  → 更糟糕——它以为自己知道当前状态，但其实是错的
```

### 修复

⛔ **平台层问题**。skill 层面无法影响 Paopao 的历史注入逻辑。

---

## 六、问题 5：无持久状态自动注入

### 发现

Paopao 每次 run 只注入两样东西：**SKILL.md + 对话历史**。项目文件（workspace-index.yaml / project.yaml / entity-snapshot.yaml / memory.md 等）**不自动注入**。

### 验证

通过分析未命名项目最新 5 个 run 的 input.json，对 prompt 全文搜索关键文件名：

| 文件 | 在 prompt 中出现？ | 原因 |
|-|-|-|
| memory.md | ❌ | 不存在 |
| workspace-index.yaml | ❌ 作为注入内容 | 文件中出现该字符串，但它在 SKILL.md 指令的引用中，不是注入的文件内容 |
| project.yaml | ❌ 同 | 同上 |
| constitution.yaml | ❌ 同 | 同上 |

### 影响

```
对话历史冻结后，agent 只能通过自行扫描文件系统恢复上下文。
这依赖于 agent 主动执行 Get-Content / LS 操作。
如果 agent 偷懒（"根据我的了解，项目状态是…"），就依赖错误的历史缓存。
```

### 修复

**方案已就位**：

- workspace-index.yaml 作为唯一的全局状态文件
- expert-writer §3.0 在 Think 阶段主动读取
- 首次运行时如果不存在则自动初始化

但它是**主动读取**不是自动注入——agent 需要记得去读。对比自动注入（像 SKILL.md 那样自动附加在 prompt 中）和主动读取（agent 自己去 Get-Content），当前采用的是后者。

---

## 七、问题 6：跨项目信息泄露

### 发现

Agent 在思维链（thinking）中展示其他项目（"海贼法典"、"北帝镇诡录"）的小说名字。

### 根因

通过全量分析未命名项目的 3 份会话记录（共 38+ 条消息）：

| 会话 | 消息数 | 其他项目名出现？ |
|-|-|-|
| `89c730e0` (清空→写作) | \~20 | **0 条** |
| `3b4153e4` (check→ch006) | \~18 | **0 条** |
| `6f041a19` (新对话) | 0 | 未开始 |

**user 消息中完全没有提到任何其他项目名。**

进一步查 agent 的 thinking 中"海贼法典"的来源——定位到 `expert-writer v2.5.0` SKILL.md 中 §3.0 的示例：

```
例：用户说"续写海贼法典" → 自动提示 L002（精读倒数20章）
```

**泄露路径**：

```
SKILL.md 中含"海贼法典" → Paopao 注入 prompt → agent 读取 SKILL.md
→ agent thinking 中看到该示例 → 展示在思维链中
```

### 影响

- 用户在未命名项目中看到 agent 提到"海贼法典" → 困惑
- 技术上是**指令中的示例文本被误认为实际信息**
- 不涉及用户隐私泄露（不泄露其他项目的内容，只泄露了项目名）

### 修复

**expert-writer v3.0.0** 已删除 SKILL.md 中所有具体项目名示例：

```
v2.5.0: "例：用户说"续写海贼法典" → 自动提示 L002"
v3.0.0: 已删除该行
```

确认：v3.0.0 SKILL.md 中不包含任何"海贼法典"、"北帝镇诡录"、"仙秦帝国"等字眼。新建会话不会出现此问题。

---

## 八、问题 7：会话隔离缺失

> 严重性：P2 | 已确认

### 发现

Paopao 的 `conversationId` 隔离机制正常工作。不同会话不共享对话历史。但 agent 读取的 `workspace-index.yaml` 是全局文件——同一项目的所有会话共享。

### 影响

```
会话 A：用户说"外神线改为主线" → workspace-index.yaml 记录 REQ-002
会话 B（新会话）：agent 读 workspace-index.yaml → 看到 REQ-002
         → 知道"外神线是主线"
         → 不依赖对话历史记忆
```

实际上是**正确行为**——workspace-index.yaml 的设计目标就是在会话间传递状态。不算问题，但需要注意：

- 如果用户在会话 A 中说了"放弃外神线"但没更新 requirements → 会话 B 会看到过时数据
- 依赖 agent 在 Reflect 阶段维护 requirements 的准确性

---

## 九、修复状态

### 已修复（skill 层面）

| 修复 | 版本 | 解决 | 效果 |
|-|-|-|-|
| Read 截断 | expert-writer v2.4.0 | §0.1 元纪律：禁止 Read 工具 | 截断率 15/17 → 0/30 |
| SKILL.md 瘦身 | expert-writer v3.0.0 | 5 块提取到 references/ | 21,298c → 8,871c (-57%) |
| 跨项目名泄露 | expert-writer v3.0.0 | 删除 SKILL.md 中所有项目名示例 | 新会话不再泄露 |
| 项目持久状态 | workspace-index v2.0 + expert-writer v3.0 | requirements + change_log | 被冻结的历史可通过索引恢复 |
| 项目初始化 | expert-writer v2.7 | Reflect L1 自动种子写入 | 新项目自动初始化索引 |

### 需平台修复

| 问题 | 期望行为 | 当前行为 |
|-|-|-|
| 对话历史冻结 | FIFO 丢弃或摘要压缩 | 冻结，不更新 |
| 无持久状态注入 | workspace-index.yaml 自动注入 prompt | 仅注入 SKILL.md + 对话历史 |
| Read 工具截断 | 返回完整内容或确认截断上限 | 静默截断，agent 无法感知 |

---

## 十、附录：证据索引

### 审计工具链

| 工具 | 用途 | 存储位置 |
|-|-|-|
| `audit_unnamed.py` | 全量 run 的 Read/Get-Content/截断审计 | `temp/` |
| `audit_v25.py` | v2.5.0 协议执行验证 | `temp/` |
| `check_ew_size.py` | expert-writer SKILL.md section 大小分析 | `temp/` |
| `check_history.py` | 对话历史注入模式分析 | `temp/` |
| `check_memory.py` | memory.md 注入检查 | `temp/` |
| `check_cross_proj.py` | 跨项目名泄漏根因定位 | `temp/` |

### 关键数据文件

| 文件 | 用途 |
|-|-|
| `workspace-index.yaml` | 全局索引（v2.0 新增 requirements + change_log） |
| `skills/expert-writer/SKILL.md` | 元 Skill 指令（v3.0 精简版 8,871c） |
| `skills/expert-writer/CHANGELOG.md` | 版本变更记录 |
| `prd/写作专家全链路文件依赖图-PRD.md` | 全链路管线蓝图 |

### 关键 run 索引

| Run ID | 项目 | 版本 | 用途 |
|-|-|-|-|
| baaf4df2 | 未命名 | v2.3.0 | Read 截断对照组 |
| d2b5d0b4 | 未命名 | v2.3.0 | 截断最严重（15/17 文件） |
| 628fd83c | 未命名 | v2.5.0 | §0.1 有效验证（0 次 Read） |
| efb59302 | 未命名 | v2.5.0 | 对话历史冻结起点（turns=20） |
| fa3eea39 | 未命名 | v2.5.0 | 历史冻结后续 run |
| 3311df5c | 未命名 | v3.0.0 | 最新 run |