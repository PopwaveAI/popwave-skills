---
name: pop-emergent
description: Pop 涌现式小说项目初始化、修复和规范审计 skill。用于新建或校准涌现式写作项目、创建/修复 current-state.md 与 soul.md、补齐文档元数据、检查 skill scope/版本、判断下一步应使用 seed/research/write/review 哪个执行 skill；不作为每轮正文写作的常驻总控。
---

# Pop Emergent

本 skill 不是每轮写作总控。它只在项目初始化、项目跑偏、入口资产缺失或用户要求检查规范时使用。每轮正文由 `pop-emergent-write` 执行；中长线记忆由 `pop-emergent-review` 压缩进 `current-state.md`。

## 核心定位

- **初始化**：创建涌现式项目骨架和文档元数据。
- **修复**：补齐或重写 `current-state.md`、`soul.md`、`content-mechanics.md`。
- **审计**：检查 skill scope、版本号、execution.mode、正文落盘、review/ledger 闭环。
- **路由建议**：判断下一步应执行 seed、research、write 还是 review。

不要代替 seed/research/write/review 产出正文、燃料、审稿报告或长篇设定。

## 项目骨架

初始化或修复时，目标目录采用：

```text
涌现/
  current-state.md          # 下一章 write 唯一入口包
  soul.md                   # 主卖点 + 叙事魂 + 正文气口
  seed-种子文档.md          # 长期承诺和故事宪法
  research-写作燃料.md      # 燃料池，由 review 筛入 current-state
  content-mechanics.md      # 题材机制和参考机制分流
  设定库.md                 # 已确认设定事实
  人物库.md                 # 人物最新状态
  剧情线.md                 # 伏笔、债务、中长线推进
  review-沉淀.md            # 审稿历史和修正规则
  压缩归档/
```

## 文档元数据

长期文档开头必须有元数据块：

```markdown
---
doc_type: current-state | soul | seed | research | setting | character | plotline | fuel | mechanics | review-log | chapter
role: 本文档在管线里的定位
read_policy: full-required | full-if-targeted | summary-allowed | index-only
compression: forbid | allow-into-current-state | archive-after-10
primary_consumer: write | review | seed | research | human
source_of_truth: true | false
last_updated: YYYY-MM-DD
---
```

读取策略：

| read_policy | 含义 |
| --- | --- |
| `full-required` | 消费者每次必须全量读，不能用摘要替代 |
| `full-if-targeted` | 本轮直接相关才全量读 |
| `summary-allowed` | 可被 review 压缩进 current-state |
| `index-only` | write 不直接读，只供 review/人类按需查 |

## 必备入口文件

### current-state.md

定位：下一章写作唯一入口包。write 每次 full-required。

必须包含：

- 当前章位
- 不可改事实
- 人物状态
- 设定状态
- 可用燃料队列
- 伏笔债务
- 下一章硬推进
- 禁止漂移

控制在 1000-2500 字。写不下的放库文件，不塞给 write。

### soul.md

定位：主卖点 + 叙事魂 + 正文气口。write 每次 full-required。

必须包含：

- 主卖点/元爽点
- 读者追读承诺
- 主角主动方式
- 爽点外显方式
- 叙事人格
- 句子气口和段落呼吸
- 对白方式
- 信息释放
- 禁区

soul 不记录可变事实、具体剧情节点、角色当前状态、数值、招式名、系统规则。这些进入 current-state 或库文件。

## 规范审计

检查项目时输出：

```markdown
## 涌现项目审计
- skill scope：
- skill version：
- current-state：存在/缺失/过大/缺字段
- soul：存在/缺失/空泛/越权写事实
- write 输入闭环：是否只读 current-state+soul+最近正文+用户要求
- review 闭环：是否更新 current-state
- execution.mode：是否有过度 formal
- 下一步建议：
```

若目标 skill 不在当前可用 scope，必须明说“不可执行该 skill”，不得沿用历史自称采用。

## 路由建议

| 情况 | 下一步 |
| --- | --- |
| 没有 seed 或主卖点不清 | `pop-emergent-seed` |
| 缺现实/题材/机制燃料 | `pop-emergent-research` |
| 缺 current-state 或 current-state 过期 | `pop-emergent-review` 初始化或修复 |
| 缺 soul 或 soul 空泛 | `pop-emergent-review` 提出 soul 修复，用户确认后更新 |
| 入口文件齐全且要写正文 | `pop-emergent-write` |
| 写完一章 | `pop-emergent-review` 更新 current-state |

## 红线

- 不调用 `pop-writer-v3-create` 处理涌现式写作。
- 不把自己当常驻总控；执行层必须交给子 skill。
- 不让 write 全量扫项目库；库文件必须由 review 筛进 current-state。
- 不把“本次采用 skill”当合规证据；必须检查 scope 里真实存在。
- 不把文风锚定当剧情素材库；题材机制进入 research/content-mechanics/设定库。
