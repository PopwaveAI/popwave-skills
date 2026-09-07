# 伏笔账规范（Hook Ledger Spec）

> 借鉴 inkos hook-ledger-validator 的设计，独立重写为 markdown 协议。
> 这是 `novel-plot` / `novel-chapter` / `novel-review` 共同遵守的伏笔追踪协议。

---

## 1. 概念定义

**伏笔（Hook）**：作者埋下的一个"未兑现承诺"，让读者期待后续会有相关的回报 / 揭秘 / 反转。

**伏笔账（Hook Ledger）**：以表格形式记录所有伏笔及其状态的账本，分别存在三处：
- `plot/foreshadowing.md`（全书总账）
- `plot/arcs/{arc}.md` 的 `## Foreshadowing` 段（本弧账）
- `chapters/ch-XXX.md` frontmatter 的 `## hook-账` 段（本章操作）

---

## 2. 四态生命周期

每条伏笔有 4 种状态之一：

### `open` —— 已埋设，未推进

伏笔被埋下，等待后续推进或回收。

### `advance` —— 已推进

给读者提供了新线索 / 加深了悬念 / 提升了相关性，但伏笔本身**没有完整回收**。

例子：第 1 章埋下"神秘老人来历不明"，第 5 章主角偶然发现老人腰间有皇家纹章 → 这是 `advance`，让读者更想知道老人是谁。

### `resolve` —— 已完整回收

伏笔被完全揭开，读者得到完整答案。

例子：第 20 章揭开"神秘老人是太上皇"。

### `defer` —— 暂时搁置

明确告诉账本"本卷不处理"，留到后续卷再说。

注意：`defer` 不是"忘了"——是**显式的延期决定**。每条 defer 必须给原因（如"重点放在 sera 主线，maren 的过去搁到卷二"）。

---

## 3. 伏笔的 ID 与字段

```yaml
# 一条伏笔记录
id: H001                   # 全书唯一 ID（H + 序号）
description: "神秘老人腰间纹章"
plant-at: ch-001           # 埋设章
payoff-at: ch-020          # 计划兑现章（可为 TBD）
priority: core             # core / supporting / decorative
status: planted            # planted / advancing / resolved / deferred
keywords:                   # 用于 novel-review 关键词回声检查
  - 神秘老人
  - 皇家纹章
  - 腰间饰物
depends-on: []             # 依赖的其他伏笔 ID
related-arc: arc-1         # 关联的故事弧
note: "暗示老人是失踪的太上皇"
```

### 优先级三档

| priority | 含义 | 数量限制 |
|---|---|---|
| `core` | 主线核心伏笔，决定全书走向 | 全书 3-7 条 |
| `supporting` | 支线伏笔，丰富故事 | 全书 10-30 条 |
| `decorative` | 装饰性伏笔，增加细节 | 不限 |

---

## 4. 章节级 hook 账操作

每写一章，在章节文件 `chapters/ch-XXX.md` 的 frontmatter 下面加一段 `## hook-账`：

```markdown
## hook-账

### open（本章新埋）
- H012 "胖虎的借条" → 暗示胖虎家里有秘密
- [new] 主角发现父亲日记里夹着一张地图

### advance（本章推进）
- H001 "神秘老人腰间纹章" → 主角偶然看到纹章上的金线，确认皇家工艺

### resolve（本章回收）
- H007 "为什么村长每周三晚上出门" → 揭开村长去地下教堂

### defer（本章暂搁）
- H003 "母亲的字条" → 推到卷二再处理（原因：本卷重点是 sera，母亲线先冻结）
```

### `[new]` 占位符

如果埋下一个新伏笔但还没分配全局 ID（先记账后补 ID），用 `[new]` 占位。后续在全书账中分配正式 ID 时再回填章节文件。

---

## 5. "揭 1 埋 1" 硬底线

> 源自番茄文学 10 大原则之"徐二家的猫"——掀开一个伏笔的同时再埋两个伏笔（理想），至少埋一个（硬底线）。
> "只揭不埋"会让读者读完豁然开朗后**索然无味**，故事失去前进拉力。

### 硬规则

每章 `resolve` 多少个伏笔，必须至少 `open` 同样多个新伏笔。

例外：
- 全书末章可以只 resolve 不 open
- 卷末章可以"延至下一卷"标注，但要确实在下一卷的开头章再 open 出来

### 软规则（推荐）

理想是"揭 1 埋 2"（每回收 1 个伏笔，新埋 2 个），但 v0.1 不强制——开埋太多会冲淡注意力。

---

## 6. 关键词回声检查（keyword echo）

> 借鉴 inkos hook-ledger-validator.ts 的算法。

**问题**：作者在 章纲 hook 账里写"本章 resolve H007 胖虎借条"，但正文里完全没有提到借条、胖虎、欠钱等关键词 → 这是**承诺没兑现**，账本和正文脱节。

**算法**：
1. 解析 hook description 中的关键词（CJK 取 2-gram，ASCII 取小写整词）
2. 检查正文是否包含其中至少一个关键词
3. 不包含 → critical violation

**例子**：
- description: `"H007 胖虎借条"` → keywords: `["胖虎", "借条", "胖虎借", "虎借条"]`
- 正文必须包含至少一个

由 `novel-review/scripts/check_hook_ledger.py` 自动执行。

---

## 7. 伏笔状态过期检测

伏笔不能一直 `open` / `advance` 下去。

### 阈值（v0.2 实现）

| 优先级 | open 状态最长时长 | 超过则 |
|---|---|---|
| core | 10 章 | warning（核心伏笔超 10 章未推进，故事可能在跑偏） |
| core + open > 20 章 | | critical（烂尾前兆） |
| supporting | 30 章 | info（提醒处理） |
| decorative | 不强求 | （读者通常不记得） |

由 `novel-review` 在每章 / 每卷尾的"伏笔健康检查"自动触发。

---

## 8. 一些常见错误

1. **伏笔被回收了但全书账没更新** → `novel-chapter` 在 post-write memory_update 应自动更新
2. **同一个伏笔在两个地方有不同描述** → 全书账是单一真相源，章节账只标 ID + 操作
3. **defer 后忘了** → 全书账定期扫描 `defer` 项，提醒
4. **decorative 伏笔被当 core 处理** → 浪费读者注意力。priority 字段要慎重

---

## 9. 例：完整的伏笔档案

```markdown
# 伏笔账 - 沉默的忠诚

## 已埋伏笔（open）

| ID | 描述 | 优先级 | 埋设 | 计划回收 | 关联弧 |
|---|---|---|---|---|---|
| H001 | 神秘老人腰间纹章 | core | Ch 1 | Ch 20 | arc-1 |
| H003 | 母亲的字条 | core | Ch 2 | TBD | arc-2 |
| H012 | 胖虎家里的秘密 | supporting | Ch 5 | Ch 15 | arc-1 |

## 推进中（advance）

| ID | 描述 | 优先级 | 推进章 | 进展 |
|---|---|---|---|---|
| H001 | 神秘老人腰间纹章 | core | Ch 5 | 主角看清纹章是皇家金线 |

## 已回收（resolve）

| ID | 描述 | 优先级 | 埋设 | 回收 | 回收方式 |
|---|---|---|---|---|---|
| H007 | 村长每周三晚上去哪 | supporting | Ch 3 | Ch 10 | 揭开是去地下教堂 |

## 暂搁（defer）

| ID | 描述 | 搁置原因 | 计划恢复 |
|---|---|---|---|
| H003 | 母亲的字条 | 本卷重点是 sera，母亲线冻结 | 卷二开头 |
```

这是 `plot/foreshadowing.md` 的标准模板。
