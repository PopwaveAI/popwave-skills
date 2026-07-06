# Step 2: 补缺口与一次性路由

> 触发：step-1 审计后用户确认修复 current-state / soul 缺口
> 前置：step-1 审计报告已完成

## 1. 补 current-state / soul 骨架

emergent 只补骨架与元数据，不填写正文内容。

### current-state.md 空壳

按 PRD §3.2 补元数据块 + 以下字段标题（正文待 review 填充）：

- 当前章位
- 不可改事实
- 人物状态
- 设定状态
- 可用燃料队列
- 伏笔债务
- 下一章硬推进
- 禁止漂移

### soul.md 空壳

按 PRD §3.3 补元数据块 + 以下字段标题（正文待 seed 填充）：

- 主卖点/元爽点
- 读者追读承诺
- 主角主动方式
- 爽点外显方式
- 叙事人格
- 句子气口和段落呼吸
- 对白方式
- 信息释放
- 禁区

soul 不记录可变事实、具体剧情节点、人物当前状态、数值、招式名、系统规则。

## 2. 一次性路由建议

本 step 的路由建议是**一次性诊断建议**，非每轮正文调度总控。正文写作轮次由用户或 PE 提示词直接调用 pop-emergent-write。

路由建议表（参照 PRD §7）：

| 情况 | 下一步 |
| --- | --- |
| 没有 seed 或主卖点不清 | `pop-emergent-seed` |
| 缺现实/题材/机制燃料 | `pop-emergent-research` |
| 缺 current-state 或 current-state 过期 | `pop-emergent-review` 初始化或修复 |
| 缺 soul 或 soul 空泛 | `pop-emergent-review` 提出 soul 修复，用户确认后更新 |
| 入口文件齐全且要写正文 | `pop-emergent-write` |
| 写完一章 | `pop-emergent-review` 更新 current-state |

输出路由建议后，emergent 本轮职责结束。后续执行由用户调用对应 skill。

## 3. 加载门禁

路由建议输出后，emergent 不再常驻。用户确认下一步 skill 后，emergent 退出，由目标 skill 接管。

强调：emergent 不是每轮调度器。每轮正文由 write 执行，写完由 review 更新 current-state，循环不需要 emergent 介入。
