---
name: pop-writer-v3-seed
description: 小说新书创意立项 skill。用于“开书/做种子/故事概念碰撞/新书PRD/题材方向/商业卖点/用户立项确认”。只负责调研水下层、种子展开、外部母版、2-3个故事概念PK、用户选择和全书立项PRD，并输出给 world-foundation 的交接包；不做L1世界包、不设计金手指、不写文风DNA、不进剧情幕纲。
---

# Pop Writer V3 Seed

seed 只回答“这本书是否成立、靠什么卖、往哪里长”。它是创意立项 skill，不是世界设定 skill。

拆分后的职责边界：

- seed：研究档案 -> 概念候选 PK -> 用户确认 -> 新书立项 PRD -> seed-to-world 交接。
- world-foundation：设定涌现 -> L1 世界包 -> 主角引擎 -> 金手指竞技 -> 文风DNA -> plot 交接。

## 核心原则

- 先调研后立项：没有水下资料层，不写 PRD。
- 先概念 PK 后定书：至少 2-3 个互斥故事概念，用户确认后才能锁 PRD。
- 只锁商业宪法，不锁世界细节：世界规则、金手指、势力、资源由 world-foundation 涌现。
- 保留用户断点：Step 1 后确认概念，Step 2 后确认 PRD。
- 证据先于灵感：用户提到作品/角色/桥段必须消歧并绑定证据；证据不足时标“模型推断”。

## 输出位置

正式产物：

```text
library/设定账本/新书立项PRD.md
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
library/设定账本/研究档案/03-参考书案例消化摘要.md
library/设定账本/运行/00-故事概念候选PK.md
library/设定账本/新书立项PRD.md
library/设定账本/seed-to-world交接包.md
library/设定账本/seed-产物索引.md
```

## 执行步骤

1. 读 `steps/step-0-research-iceberg.md`：输入消歧、library/外部母版调研、种子展开。
2. 读 `steps/step-1-concept-collision.md`：生成 2-3 个故事概念候选并 PK，设置用户断点。
3. 读 `steps/step-2-prd-lock.md`：把胜出概念锁成全书立项 PRD。
4. 读 `steps/step-3-seed-to-world-handoff.md`：输出给 world-foundation 的交接包和 seed 产物索引。

## 用户断点

- Step 1 后必须让用户确认故事概念，除非用户明确要求“自动继续”。
- Step 2 后必须让用户确认 PRD 的篇幅、主角起终点、元爽点、世界机器草案和禁区，除非用户明确要求“自动继续”。

## 红线

- 不做调研就写 PRD。
- 不给用户故事概念选项就锁书。
- 不做 L1 世界包。
- 不设计金手指。
- 不输出文风DNA。
- 不把“世界危险/敌人强/氛围好”当元爽点。
- 用户给出参考书/对标书时，不得只抽“题材标签/设定关键词”。必须读取相关 L2/L3 剧情卡、任务索引或拆书资料，产出 `03-参考书案例消化摘要.md`，说明学到的叙事语法、爽点兑现链、主角行动逻辑、可迁移机制和不可照搬项。
- 不说“seed 完成”，除非研究档案、参考书案例消化摘要、候选PK、PRD、交接包和索引齐全。
