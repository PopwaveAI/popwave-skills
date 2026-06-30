---
name: pop-writer-v3-world-foundation
description: 小说世界底盘与设定涌现 skill。用于“做世界观/L1世界包/力量体系/势力资源/主角引擎/金手指/开局契约/文风DNA/设定涌现追踪”。消费 seed 的新书PRD、研究档案和 seed-to-world 交接包，通过设定问题清单、候选规则池、碰撞矩阵、方案竞技、冻结日志和设定债务目录，全量追踪世界设定如何涌现，再输出 plot 可消费的世界底盘；不写卷纲幕纲正文。
---

# Pop Writer V3 World Foundation

world-foundation 负责把 seed 的创意宪法变成可运行的世界机器。它不是百科设定生成器，也不是 plot。它的重点是：**设定涌现必须可追踪，设定冻结必须有理由，设定缺口必须留下债务。**

## 执行模式

- `formal`：本 `SKILL.md` 和必要 step 文件已读取，输入材料齐全，设定涌现、L1、金手指竞技、文风DNA继承和交接门全部通过。
- `draft`：本 skill 已读取，但上游输入或任一质量门有缺口。
- `trial`：未完整加载本 skill，或用户只要快速设定草案。

只有 `formal` 可以称为 world 底盘完成并交给 plot。`draft/trial` 不得把 L1、金手指或文风DNA标为正式冻结。

## 输入

必须读取：

```text
library/设定账本/新书立项PRD.md
library/设定账本/seed-to-world交接包.md
library/设定账本/研究档案/00-研究索引.md
library/设定账本/研究档案/01-种子展开图.md
library/设定账本/研究档案/02-外部母版卡.md
library/设定账本/研究档案/04-复刻路由表.md  # 存在复刻/嫁接意图时读取
library/设定账本/运行/00-故事概念候选PK.md
```

若缺失，输出缺口报告，不得冻结 L1。

## 输出目录

正式底盘：

```text
library/设定账本/L1-世界蓝图.md
library/设定账本/L1-力量体系.md
library/设定账本/L1-势力格局.md
library/设定账本/L1-资源物品.md
library/设定账本/L1-术语与文明底色.md
library/设定账本/起点快照.md
library/设定账本/世界宪法.md
library/设定账本/动态升级表.md
library/设定账本/主角引擎.md
library/设定账本/金手指.md
library/设定账本/开局契约.md
library/设定账本/Library查询方向.md
library/设定账本/跨媒介母版雷达.md
library/文风DNA/文风DNA.md
library/设定账本/world-产物索引.md
```

设定涌现全量追踪：

```text
library/设定账本/设定涌现/00-涌现索引.md
library/设定账本/设定涌现/01-PRD消费确认.md
library/设定账本/设定涌现/02-设定问题清单.md
library/设定账本/设定涌现/03-候选规则池.md
library/设定账本/设定涌现/04-设定碰撞矩阵.md
library/设定账本/设定涌现/05-L1方案竞技.md
library/设定账本/设定涌现/06-冻结决策日志.md
library/设定账本/设定涌现/07-设定债务与待验证.md
```

## 执行步骤

1. 读 `steps/step-0-consume-seed.md`：消费 seed，区分不可改写项和可涌现项。
2. 读 `steps/step-1-emergence-ledger.md`：建立设定涌现目录，生成设定问题清单和候选规则池。
3. 读 `steps/step-2-l1-world-package.md`：通过碰撞矩阵和 L1 方案竞技，冻结 L1 世界包、起点快照、世界宪法、动态升级表。
4. 读 `steps/step-3-protagonist-goldfinger.md`：基于 L1 设计主角引擎、金手指候选竞技和开局契约。
5. 读 `steps/step-4-style-plot-handoff.md`：从文风库选择并复制文风DNA原件，输出 Library 查询方向、跨媒介母版雷达、world 产物索引。

## 设定涌现规则

- 不凭空拍板。每个冻结设定都必须出现在候选池、碰撞矩阵或方案竞技中。
- 不全量百科。只冻结第一卷和长篇结构必须依赖的规则。
- 不把候选删干净。淘汰项也要留在冻结决策日志里，说明为什么不用。
- 不让金手指先行。金手指必须晚于 L1 世界包。
- 不让质感覆盖机制。术语、命名、文风必须能追溯到世界规则或网文爽点。
- 不原创文风DNA。文风DNA必须从公共 `pop-trope-library/文风库/` 或用户提供的 library 文风文件中选取合适原件复制下来；world 只能追加项目化适配说明，不得用抽象标签重写成自创风格总结。
- 如存在 `04-复刻路由表.md`，world 只消费“复刻位置=world”的条目，例如世界观骨架、力量体系、势力资源、金手指基础规则；plot 和 create/revise 条目只作为下游提醒，不在 world 阶段展开。

## 红线

- PRD/交接包缺失时不得进入 L1。
- 没有 `设定涌现/` 全量追踪目录，不得称 world 完成。
- 没有候选规则池和碰撞矩阵，不得冻结世界宪法。
- 没有 L1 方案竞技，不得说世界机器成立。
- 没有三候选金手指竞技，不得冻结金手指。
- 没有起点快照、动态升级表、开局契约，不得交给 plot。
- 没有文风库原件路径、复制范围和项目化适配说明，不得把 `library/文风DNA/文风DNA.md` 标记为正式可用；只能标记为“文风DNA缺口”。
- 没有 `execution.mode: formal` 或等价执行凭证时，不得称 world 底盘完成。
