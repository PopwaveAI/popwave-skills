---
name: pop-writer-v3-seed
description: 小说新书创意立项与长篇承诺。用于"开书/做种子/新书PRD/长篇尺度规划"。从调研到概念PK、商业爽点金字塔、长篇尺度推导、立项PRD，输出给 world-foundation 的交接包。
---

# Pop Writer V3 Seed

seed 只回答“这本书是否成立、靠什么卖、能长多大、每卷为什么会发生质变”。它是创意立项 skill，不是世界设定 skill。

拆分后的职责边界：

- seed：研究档案 -> 概念候选 PK -> 用户确认 -> 商业爽点金字塔 -> 长篇尺度推导 -> 新书立项 PRD -> seed-to-world 交接。
- world-foundation：Foundation 结构工程 -> 世界金字塔 -> 设定涌现 -> L1 世界包 -> 主角引擎 -> 金手指竞技 -> 文风DNA -> plot 交接。

## 执行模式

- `formal`：本 `SKILL.md` 和必要 step 文件已读取，研究档案、概念 PK、PRD、交接包按门槛完成。
- `draft`：本 skill 已读取，但研究、证据、候选 PK、PRD 或交接包有缺口。
- `trial`：未完整加载本 skill，或用户只要快速脑暴。

只有 `formal` 可以称为 seed 完成。`draft/trial` 只能输出草案、缺口报告或对齐稿，不得把 PRD/交接包标为正式可用。

## 核心原则

- 先调研后立项：没有水下资料层，不写 PRD。
- 先概念 PK 后定书：至少 2-3 个互斥故事概念，用户确认后才能做长篇尺度推导。
- 先长篇承诺后 PRD：PRD 的卷数、章数、第一卷终点必须来自商业爽点金字塔和卷级质变草案，不得拍脑袋填默认值。
- 只锁商业宪法，不锁世界细节：世界规则、金手指、势力、资源由 world-foundation 涌现。
- 保留用户断点：Step 1 后确认概念，Step 2 后确认 PRD。
- 证据先于灵感：用户提到作品/角色/桥段必须消歧并绑定证据；证据不足时标“模型推断”。

## 输出位置

正式产物：

```text
library/设定账本/新书立项PRD.md
library/设定账本/长篇承诺书.md
library/设定账本/seed-to-world交接包.md
library/设定账本/seed-产物索引.md
```

过程产物：

```text
library/设定账本/研究档案/
library/设定账本/运行/
```

seed 禁止写入 `卷纲/运行/`，也禁止写入 L1 世界包、金手指、文风DNA。

## 必须产物

```text
library/设定账本/研究档案/00-研究索引.md
library/设定账本/研究档案/01-种子展开图.md
library/设定账本/研究档案/02-外部母版卡.md
library/设定账本/研究档案/03-多元素整合记录.md
library/设定账本/研究档案/04-复刻路由表.md  # 用户要求复刻/嫁接时必需
library/设定账本/研究档案/05-资料覆盖率声明.md  # 使用参考作品/library/wiki/模型常识时必需
library/设定账本/运行/00-故事概念候选PK.md
library/设定账本/运行/00b-长篇尺度与商业爽点金字塔.md
library/设定账本/新书立项PRD.md
library/设定账本/长篇承诺书.md
library/设定账本/seed-to-world交接包.md
library/设定账本/seed-产物索引.md
```

## 执行步骤

1. 读 `steps/step-0-research-iceberg.md`：输入消歧、library/外部母版调研、种子展开。
2. 读 `steps/step-1-concept-collision.md`：生成 2-3 个故事概念候选并 PK，设置用户断点。
3. 读 `steps/step-2-longform-architecture.md`：把胜出概念推导成商业爽点金字塔、世界规模假设和卷级质变草案。
4. 读 `steps/step-3-prd-lock.md`：把胜出概念和长篇承诺锁成全书立项 PRD。
5. 读 `steps/step-4-seed-to-world-handoff.md`：输出给 world-foundation 的交接包和 seed 产物索引。

## 用户断点

- Step 1 后必须让用户确认故事概念，除非用户明确要求“自动继续”。
- Step 2 后必须让用户确认商业爽点金字塔、世界规模假设、全书卷数区间和每卷质变草案，除非用户明确要求“自动继续”。
- Step 3 后必须让用户确认 PRD 的篇幅、主角起终点、元爽点、世界机器草案和禁区，除非用户明确要求“自动继续”。

## 红线

- 不做调研就写 PRD。
- 不给用户故事概念选项就锁书。
- 不做商业爽点金字塔和长篇尺度推导就写 PRD。
- 不解释世界规模为何支撑对应卷数，就填写全书卷数。
- 不说明每卷质变，就把“动态升级表/卷级结构”交给 world 或 plot 补。
- 不做 L1 世界包。
- 不设计金手指。
- 不输出文风DNA。
- 不把“世界危险/敌人强/氛围好”当元爽点。
- 用户给出多个元素、参考书/对标书、题材母版或金手指方向时，不得只抽“题材标签/设定关键词”。必须按 `expert-writer/references/多元素整合范式.md` 产出 `03-多元素整合记录.md`。该文件只处理元素碰撞，不判定 L1-L4 复刻深度。
- 使用参考书、library拆书卡、wiki、百科、书评或模型常识时，必须按 `expert-writer/references/资料覆盖率协议.md` 先写资料覆盖率声明。只读到第一卷/少量样本时，只能说“样本显示”，不得外推成全书结论。
- 用户表达“像/照着/复刻/高保真/一比一/拿某体系/嫁接某世界观”等意图时，必须先按 `expert-writer/references/复刻协议.md` 产出 `04-复刻路由表.md`。seed 只锁定 PRD 层意图和下游路由，不设计 L1 世界包、金手指细节或章节链。
- 不说“seed 完成”，除非研究档案、资料覆盖率声明、多元素整合记录（如需）、复刻路由表（如需）、候选PK、长篇承诺书、PRD、交接包和索引齐全。
- 没有 `execution.mode: formal` 或等价执行凭证时，不得称 seed 完成。
