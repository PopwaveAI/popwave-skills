---
name: pop-writer-v3-world-foundation
description: 小说长篇结构工程、世界底盘与设定涌现。用于"做世界观/Foundation/世界金字塔/L1世界包/角色储备池/金手指/文风DNA/读者表达偏好/项目资料总目录"。消费 seed 的长篇承诺和交接包，先建立商业爽点、世界尺度、卷级质变、势力战力资源金字塔，再冻结 plot/create 可消费的世界底盘。
---

# Pop Writer V3 World Foundation

world-foundation 负责把 seed 的创意宪法和长篇承诺变成可运行的世界机器。它不是百科设定生成器，也不是 plot。它先做 Foundation 结构工程，再做 World 设定冻结。

核心链路：

```text
长篇承诺 -> Foundation结构工程 -> 世界金字塔 -> 设定涌现 -> L1冻结 -> 主角/金手指 -> plot交接
```

重点是：**世界规模决定卷数，每卷一次大质变；势力、战力、资源、社会地位必须同表校准；设定冻结必须有外部燃料和内部一致性证据。**

## 执行模式

- `formal`：本 `SKILL.md` 和必要 step 文件已读取，输入材料齐全，Foundation结构工程、世界金字塔、设定涌现、L1、金手指竞技、文风DNA继承和交接门全部通过。
- `draft`：本 skill 已读取，但上游输入或任一质量门有缺口。
- `trial`：未完整加载本 skill，或用户只要快速设定草案。

只有 `formal` 可以称为 world 底盘完成并交给 plot。`draft/trial` 不得把 L1、金手指或文风DNA标为正式冻结。

## 输入

必须读取：

```text
library/设定账本/新书立项PRD.md
library/设定账本/长篇承诺书.md
library/设定账本/seed-to-world交接包.md
library/设定账本/研究档案/00-研究索引.md
library/设定账本/研究档案/01-种子展开图.md
library/设定账本/研究档案/02-外部母版卡.md
library/设定账本/研究档案/03-多元素整合记录.md  # 存在多元素/参考书输入时读取
library/设定账本/研究档案/04-复刻路由表.md  # 存在复刻/嫁接意图时读取
library/设定账本/研究档案/05-资料覆盖率声明.md
library/设定账本/运行/00-故事概念候选PK.md
```

若 `长篇承诺书.md` 缺失，必须输出 Foundation 输入缺口，不得冻结 L1 或动态升级表。

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
library/设定账本/Foundation-商业爽点金字塔.md
library/设定账本/Foundation-世界尺度金字塔.md
library/设定账本/Foundation-势力战力资源总表.md
library/设定账本/Foundation-卷级质变阶梯.md
library/设定账本/Foundation-主角穿透模型.md
library/设定账本/主角引擎.md
library/设定账本/角色储备池.md
library/设定账本/金手指.md
library/设定账本/开局契约.md
library/设定账本/Library查询方向.md
library/设定账本/跨媒介母版雷达.md
library/文风DNA/文风DNA.md
library/写作配置/读者表达偏好.md
library/项目资料总目录.md
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
library/设定账本/设定涌现/08-Foundation外部燃料台.md
library/设定账本/设定涌现/08a-本书涌现燃料扫描.md
library/设定账本/设定涌现/09-世界金字塔一致性审计.md
library/设定账本/设定涌现/10-金手指候选竞技.md
```

## 执行步骤

1. 读 `steps/step-0-consume-seed.md`：消费 seed，区分不可改写项和可涌现项。
2. 读 `steps/step-1-foundation-fuel.md`：建立 Foundation 外部燃料台，校准长篇体量、组织层级、资源经济、升级结构。
3. 读 `steps/step-2-foundation-engineering.md`：生成商业爽点金字塔、世界尺度金字塔、势力战力资源总表、卷级质变阶梯、主角穿透模型。
4. 读 `steps/step-3-emergence-ledger.md`：基于 Foundation 建立设定涌现目录，生成设定问题清单和候选规则池。
5. 读 `steps/step-4-l1-world-package.md`：通过碰撞矩阵和 L1 方案竞技，冻结 L1 世界包、起点快照、世界宪法、动态升级表。
6. 读 `steps/step-5-protagonist-goldfinger.md`：基于世界金字塔和 L1 设计主角引擎、角色储备池、金手指候选竞技和开局契约。
7. 读 `steps/step-6-style-plot-handoff.md`：从文风库选择并复制文风DNA原件，输出读者表达偏好、Library 查询方向、跨媒介母版雷达、项目资料总目录、world 产物索引。

## 设定涌现规则

- 不凭空拍板。每个冻结设定都必须出现在候选池、碰撞矩阵或方案竞技中。
- 不跳过 Foundation。没有世界尺度金字塔和卷级质变阶梯，不得冻结 L1 世界包。
- 不让卷数漂浮。动态升级表必须由卷级质变阶梯推导，不得从 plot 临时补。
- 不让势力、战力、资源分家。组织人数、干部水平、资源类型、社会地位、响应速度必须在同一张总表中校准。
- 不全量百科。只冻结第一卷和长篇结构必须依赖的规则。
- 不把候选删干净。淘汰项也要留在冻结决策日志里，说明为什么不用。
- 不让金手指先行。金手指必须晚于 L1 世界包。
- 不让角色散落在 plot 临时发明。world 必须产出角色储备池，但只保存弱剧情耦合的稳定锚点；剧情弧线、登场幕、死亡/背叛/晋升由 plot 决定。
- 不平均展开角色。S/A/B/C 必须按资源预算分层，S 级也只保留 120-200 字稳定锚点。
- 不让质感覆盖机制。术语、命名、文风必须能追溯到世界规则或网文爽点。
- 不原创文风DNA。文风DNA必须从公共 `pop-trope-library/文风库/` 或用户提供的 library 文风文件中选取合适原件复制下来；world 只能追加项目化适配说明，不得用抽象标签重写成自创风格总结。
- 不让文风DNA独占正文表达。world 必须额外产出 `library/写作配置/读者表达偏好.md`，明确目标读者的直白度、旁白/心理/独白许可、环境描写长度、爽点外显频率和严肃文学偏移禁区；当它与文风DNA冲突时，create 以读者表达偏好裁决。
- 不让资料散落。world 必须产出 `library/项目资料总目录.md`，按 seed/world/plot/create/review 场景列出“必读/按需读/禁止误读”，而不是只列文件清单。
- 如存在 `04-复刻路由表.md`，world 只消费“复刻位置=world”的条目，例如世界观骨架、力量体系、势力资源、金手指基础规则；plot 和 create/revise 条目只作为下游提醒，不在 world 阶段展开。

## 红线

- PRD/交接包缺失时不得进入 L1。
- 长篇承诺书缺失时不得进入 Foundation。
- 没有 Foundation 外部燃料台，不得生成世界尺度金字塔。
- 没有世界尺度金字塔、势力战力资源总表、卷级质变阶梯、主角穿透模型，不得冻结 L1。
- 没有 `设定涌现/` 全量追踪目录，不得称 world 完成。
- 没有候选规则池和碰撞矩阵，不得冻结世界宪法。
- 没有 L1 方案竞技，不得说世界机器成立。
- 没有三候选金手指竞技，不得冻结金手指。
- 没有角色储备池，不得交给 plot；只有主角引擎不足以支撑卷纲选角。
- 没有起点快照、动态升级表、开局契约，不得交给 plot。
- 没有文风库原件路径、复制范围和项目化适配说明，不得把 `library/文风DNA/文风DNA.md` 标记为正式可用；只能标记为“文风DNA缺口”。
- 没有 `library/写作配置/读者表达偏好.md`，不得交给 create；只有文风DNA不足以约束小白文直白度和爽点外显。
- 没有 `library/项目资料总目录.md`，不得交给 plot/create；只有 seed/world 产物索引不足以保证 agent 找到正确资料。
- 没有 `execution.mode: formal` 或等价执行凭证时，不得称 world 底盘完成。
