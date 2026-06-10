# 审计报告：6-10项目 Read 截断问题

> 版本：v1.0 | 2026-06-10
> 项目：6-10项目测试（深渊主宰·外神低语同人）
> 来源：`C:\Users\AWMPRO\.paopao\projects\6-10项目测试\`
> 方法：按 `prd/排查技巧手册.md` 的 Tier 1 路径全量分析

---

## 一、审计目标

1. **Skill 是否被正确注入** — expert-writer 的路由表/Think/Reflect 关键段落是否完整进入 system prompt
2. **SKILL.md 是否被截断** — 子 skill 的 Read 操作是否完整取得文件内容
3. **长会话惰性是否存在** — 连续"继续任务"时 agent 是否跳过重新 Read

---

## 二、项目概况

| 项 | 值 |
|:---|:----|
| 项目名 | 深渊主宰·外神低语（DND × 克苏鲁同人） |
| 会话 | 1 个（`54f55360`），共 14 个 runs |
| 时间 | 2026-06-10 08:32 → 09:05（约 33 分钟） |
| 模型 | deepseek/deepseek-v4-flash |
| 已注册 Skill | expert-writer v2.3.0, pop-novel-bookstrap v4.0.0, pop-novel-deconstructor v8.0.0, pop-novel-writer v12.0.0 等 22 个 |
| 完成管线 | deconstructor（拆书分析）→ bookstrap（开书设定）→ 完成，未进 plot |

### 会话流程

| # | RunID | 用户指令 | Agent 动作 |
|:-:|:------|:---------|:-----------|
| 1 | b30e175e | 我想写一本网络小说 | Think 阶段：追问题材/基调/参考书 |
| 2 | a7993386 | 展示 skill 群全貌 | 扫 remote-skills 和 D 盘，对比版本差异 |
| 3 | 123a181f | 你读的链路是 C 盘还是 D 盘 | 修正路径，确认 D 盘是最新 |
| 4 | a37471f5 | 我要写深渊主宰同人文 | 追问同人方向（方案 A 拆书 / 方案 B 直接搭） |
| 5 | c04cfa8c | 方案 A 先拆书 | WebSearch 找全文 → 读 download-webnovel-txt SKILL.md |
| 6 | 078afb07 | @了 TXT 文件 "已经给你准备了" | 读前 100 章 → 产出 Phase 0 采样日志 |
| 7 | eee8cf70 | 继续任务 | 读 Phase 1 诊断 → 产出 Phase 1 |
| 8 | 3aa81131 | 继续任务 | Python 批量提取数据 → 产出 T1/T3/T5 深度拆解 |
| 9 | 37f6ae7a | 继续任务 | 补完 T2/T4/T6 → 全部拆解完成 |
| 10 | b995e45a | 继续任务 | Phase 3 验证 + Phase 4 整合 + 起点/终点快照 |
| 11 | d915d30c | 继续任务 | **进入 bookstrap 阶段**：读 bookstrap SKILL.md |
| 12 | bb417888 | B. 改写索伦+克系外神+原书同时 | 产出 story-engine.yaml |
| 13 | 82c29e3e | 继续任务 | **产 L1 六件套**：读 bookstrap SKILL.md |
| 14 | 5a3c361e | 没问题 继续这个方案 | 补完 constitution + 稳定性 + 起点/终点快照 |

---

## 三、问题 1：Skill 注入 ✅ 正常

### 证据

所有 14 个 run 的 `input.json` 均显示：

```json
{
  "skills": [{"name": "写作专家", "path": "D:\\popwave-skills\\skills\\expert-writer"}],
  "input": {"skillNames": ["expert-writer"]}
}
```

### 关键段落注入检查（5/5 完整）

| 检查项 | 14 个 run 全部 |
|:-------|:--------------:|
| 路由表（"继续前进"） | ✅ 全部存在 |
| Think（需求审视） | ✅ 全部存在 |
| Reflect（四层递进审视） | ✅ 全部存在 |
| writer SKILL.md 引用 | ✅ 全部存在 |

**结论**：expert-writer 元 Skill 的注入机制正常。子 skill（deconstructor/bookstrap/writer 等）不注入 prompt 是设计行为——它们通过 expert-writer 路由后由 agent 手动 Read。

---

## 四、问题 2：Read 截断 ⚠️ P0 — 确认存在

### 4.1 核心发现

14 个 run 中，**3 个 run 的 SKILL.md/step 文件被严重截断**（`82c29e3e`、`5a3c361e`、`d915d30c`）。加上 deconstructor 模板文件被截断的 run，共有 **7 个 run 出现截断**。

### 4.2 SKILL.md 主文件截断

| RunID | 上下文 | 文件 | 实际大小 | 读到多少 | **截断比例** |
|:------|:-------|:----|:--------:|:--------:|:----------:|
| `82c29e3e` | 用户"继续任务"→ 产 L1 六件套 | bookstrap SKILL.md | 10,604B | 2,416B | **22.8%** |
| `82c29e3e` | 同上（第二次重读） | bookstrap SKILL.md | 10,604B | 3,824B | **36.1%** |
| `5a3c361e` | "继续这个方案"→ 收尾管线 | bookstrap SKILL.md | 10,604B | 2,416B | **22.8%** |
| `5a3c361e` | 同上（第二次重读） | bookstrap SKILL.md | 10,604B | 3,824B | **36.1%** |
| `d915d30c` | "继续任务"→ 进入 bookstrap | bookstrap SKILL.md | 10,604B | 2,416B | **22.8%** |
| `d915d30c` | 同上（第二次重读） | bookstrap SKILL.md | 10,604B | 3,824B | **36.1%** |

**Agent 每次只能读到 SKILL.md 文件的前 22-36%**：

```
10,604 bytes 的 bookstrap SKILL.md
├── 读到 2,416-3,824B (22-36%) ← agent 可见
│   ├── YAML frontmatter
│   ├── 质量红线（前几条）
│   ├── 什么时候使用
│   └── 执行顺序（部分）
└── 丢失 6,780-8,188B (64-78%) ← agent 看不到
    ├── 执行顺序后半部分
    ├── 全部 Forward/Reverse 路径的 Step 细节
    ├── 全部异常处理规则
    ├── Phase 文件索引表（16 个 phase 的引用路径）
    └── CHANGELOG 引用
```

**致命后果**：`phase-*.pe.md` 文件索引表在截断区域，agent 根本不知道去哪加载相位文件。

### 4.3 模板文件截断

deconstructor 的模板文件全部被截断：

| 文件 | 实际大小 | 读到多少 | **比例** |
|:-----|:-------:|:--------:|:--------:|
| T1-力量体系模板.md | 4,113B | 704B | 17.1% |
| T2-世界观展开模板.md | 5,376B | 948B | 17.6% |
| T3-角色系统设计模板.md | 8,810B | 542B | **6.2%** |
| T4-剧情全貌模板.md | 9,889B | 896B | **9.1%** |
| T5-叙事技法综合模板.md | 6,841B | 548B | **8.0%** |

### 4.4 小文件也被截断（系统性问题）

甚至不到 100B 的 README.md 也出现截断：

| RunID | 文件 | 实际大小 | 读到 | 比例 |
|:------|:----|:-------:|:----:|:---:|
| `5a3c361e` | README.md | 94B | 40B | 42.6% |
| `82c29e3e` | README.md | 94B | 40B | 42.6% |
| `a37471f5` | README.md | 94B | 40B | 42.6% |
| `b30e175e` | README.md | 94B | 40B | 42.6% |
| `eee8cf70` | README.md | 94B | 40B | 42.6% |

94B 的文件只能读到 40B——说明截断不是文件大小问题，而是 **Paopao 的 Read tool result 有固定的输出上限**，与文件大小无关。这是工具层的 bug。

### 4.5 证据链

以 `82c29e3e` 的 events.jsonl 为例：

```json
// tool-call: Read bookstrap SKILL.md
{"kind":"tool-call","toolName":"read","input":"{\"path\":\"D:\\popwave-skills\\skills\\pop-novel-bookstrap\\SKILL.md\"}"}

// tool-result: 只返回了前 2,416B
{"kind":"tool-result","toolName":"read","output":"---\nname: pop-novel-bookstrap\n...(仅前 22.8%)...（以下内容省略...（截断标记也可能被截掉...）"}
```

agent 拿到截断后的内容后，在 thinking 链中写：

```
"Let me read the bookstrap SKILL.md to understand the process"
→ 只读了前 22.8% → 看不到 Phase 索引表 → "I'll proceed based on what I know"
```

agent **并不知道自己拿到的内容不完整**。

---

## 五、问题 3：长会话惰性 ⚠️ P1 — 存在

### 证据

连续 4 次"继续任务"（`37f6ae7a` → `b995e45a` → `d915d30c` → `eee8cf70`），agent 的 thinking 链直接复用了前一轮的上下文：

```json
// b30e175e (首次) → 正常 thinking，有 Read 调用
// 37f6ae7a (第4次"继续") → 直接从上一轮的 thinking 链末尾继续
// b995e45a (第5次"继续") → thinking 链开头是 "...The user keeps saying '继续任务'..."

// 更糟的是 82c29e3e (第6次"继续")：
// thinking 链直接复用了 b30e175e(首次) 的完整 thinking 文本
// → agent 以为自己已经确认过方向了，实际上方向是在当前轮之前才确定的
```

**模式识别**：

- 首次"继续任务"→ agent 会重新加载上下文做决策
- 连续 3 次以上"继续任务"→ agent 进入"全凭记忆写"模式
- 此时 agent 不 Read 任何子 skill 文件 → 前面的截断问题被放大
- 即使 SKILL.md 不被截断，agent 也不去读它的内容

---

## 六、综合分析

### 6.1 问题传播路径

```
Paopao Read 工具截断
  ↓ 影响
agent 只看到 SKILL.md 前 22-36%
  ↓ 导致
看不见 Phase 索引表 + 执行细节 + 异常处理
  ↓ 叠加
长会话惰性 → agent 不尝试重新 Read
  ↓ 结果
agent 在"文件不全 + 记忆模糊"的状态下执行流程
```

### 6.2 为何这次项目产出质量尚可

这是一个重要的观测点：本项目的产出质量并不差，原因在于 agent **用 Python 处理了大文本文件**，绕过了 Read 截断限制。具体来说：

- 拆书阶段：agent 直接 `python -c "with open('深渊主宰-前100章.txt') as f: text = f.read()"` → 34 万字的原文完整可读
- 模板文件虽然被截断，但 agent 在上一轮（`3aa81131`）的 thinking 链中已经缓存了模板结构
- 实际产出 deconstructor 的模板文件时 agent 用的是 `write` 工具新建文件，不是基于模板填空

**这是运气好，不是系统保障。** 如果模板中有限定字段名的 schema 约束（如 22 列逐章颗粒度），agent 看不到完整模板就会偏离规格。

### 6.3 与 6-9 测试的对比

| 维度 | 6-9测试（ch001-015） | 6-10项目测试（同人开书） |
|:-----|:--------------------|:----------------------|
| SKILL.md 截断 | writer SKILL.md ~50% | bookstrap SKILL.md 22-36% |
| 模板截断 | 未审计 | 确认 6-17%（5个模板） |
| 长会话惰性 | ch011-014 连续5轮零Read | 4轮连续无Read |
| 产出质量 | ch015 路径指令丢失 | 尚可（Python 绕开） |
| 根本原因 | 同一（Read 截断） | 同一（Read 截断） |

**结论**：Read 截断不是偶发，是 Paopao 的 Read tool result 有输出上限的系统性 bug。

---

## 七、修复建议

源自 `PRD-Skill调用机制三层修复.md`，对照本次证据更新优先级：

| 修复 | 解决 | 优先级 | 证据支撑 |
|:-----|:-----|:------:|:--------|
| **层 1：工具层** — Paopao Read 透明分片，一次 Read 内部拆多个 tool result 返回 | 所有文件截断 | **P0** | bookstrap SKILL.md 22-36%、模板 6-17%、94B README 42.6%——统一证据链至此修复 |
| **层 2：Think 层** — expert-writer 任务类型切换时强制重新加载子 skill 全部文件 | 长会话惰性 | **P1** | 4 轮连续"继续任务"无 Read |
| **层 3：主文件层** — 关键输出路径 + 硬性约束从 step 子文件提升到 SKILL.md 主文件 | "看不到指令" | **P1** | 本次未直接复现（因 bookstrap 未进 phase 执行），但根源相同 |
| **应急：95B 以下文件** — 检查 Read 返回是否 40B 封顶 | 小文件截断 | **P0** | README.md 94B → 40B，5 个 run 一致 |

---

## 八、附录

### 附录 A：审计方法

按 `prd/排查技巧手册.md` 的标准流程：

```python
# 审计脚本位置
c:\Users\AWMPRO\.trae-cn\work\6a2928955e61df95b4a97753\audit_runs.py
c:\Users\AWMPRO\.trae-cn\work\6a2928955e61df95b4a97753\audit_deep.py
```

分析数据源：14 个 run 的 `input.json` + `events.jsonl`，全量读取。

### 附录 B：参考文档

| 文档 | 关联 |
|:-----|:-----|
| `prd/排查技巧手册.md` | 审计方法论 |
| `prd/复盘问题清单-2026-06-08.md` | 问题总纲 |
| `prd/PRD-Skill调用机制失效.md` | v4.0 审计，Read 截断根因 |
| `.trae/documents/PRD-Skill调用机制三层修复.md` | 三层修复方案 |
| `.trae/documents/PRD-跨Skill校验+调用机制修复.md` | 跨 Skill 硬保障方案 |
| `.trae/documents/执行-PRD修复清单-2026-06-09.md` | 修复执行计划 |
