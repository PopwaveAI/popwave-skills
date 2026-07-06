# Step 1：审稿 SOP

> 触发：写完一章正文后进入 review，或用户要求审稿/更新 current-state。
> 目标：对待审正文做体感+硬推进+爽文+Soul+连续性+沉淀分流六步审计，产出审稿判断与沉淀分流清单，供 step-2 落盘。

## 前置确认（execution.mode，引用 PRD §4.5）

- formal：已读待审正文、`涌现/current-state.md`、`涌现/soul.md` 齐全，输出审稿判断并落盘新版 current-state。
- draft：缺 current-state 或 soul，但能从正文和用户要求生成临时 current-state，产出标记 draft。
- trial：只做快速体感，不更新项目状态、不落盘。

读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具。

## 必读输入

- 待审正文原文。
- 上一版 `涌现/current-state.md`（如存在）。
- `涌现/soul.md`，检查主卖点和表达是否执行。
- 按需读取：`seed-种子文档.md`、`research-写作燃料.md`、`设定库.md`、`人物库.md`、`剧情线.md`、`content-mechanics.md`。

只在需要更新对应信息时读库文件，不要为 review 把全项目全部塞进上下文。燃料文件唯一名 `research-写作燃料.md`，禁用 `燃料库.md` 别名（PRD §4.3）。

## 审稿 SOP（6 步）

### 1. 裸读体感
哪里想继续看，哪里跳读，哪里像 AI。先不查设定，只记录阅读节律和出戏点。

### 2. 硬推进检查
对照上一版 current-state 的"下一章硬推进"是否兑现；伏笔债务是否有推进或新增。未兑现项必须进 step-2 沉淀。

### 3. 爽文审计
按链路逐项判定：压力/诱因 -> 主角主动 -> 阻碍 -> 可见反馈 -> 收益/损失 -> 追读。断在哪一环，归因进下表。

### 4. Soul 执行检查
主卖点、主角主动方式、爽点外显、句子气口是否落到正文。soul 缺位或弱执行产 soul 修改建议（待用户确认，不直接改）。

### 5. 连续性检查
人物、设定、资源、时间线、伏笔是否冲突。冲突项进 step-2 库文件更新或 current-state 禁止漂移。

### 6. 沉淀分流判断
把审计发现分两类：哪些更新库文件（设定库/人物库/剧情线/燃料），哪些压入 current-state（事实、人物状态、硬推进、伏笔债务、禁止漂移）。不得只写体感长评不落 current-state。

## 归因规则表

| 问题 | 归因 | 处理 |
| --- | --- | --- |
| 中长线失控 | current-state 硬推进/伏笔债务缺口 | 重写 current-state |
| 设定或人物状态错 | 设定库/人物库未更新或 current-state 漏写 | 更新库文件并压入 current-state |
| 燃料没有入场 | research 到 current-state 的筛选失败 | 更新可用燃料队列 |
| 主卖点弱 | soul 不清或 write 未执行 | 给 soul 修改建议或下一章硬规则 |
| 文风弱 | soul 气口/文风锚定问题 | 给 soul 修改建议（待用户确认） |

不得把所有问题都归因到文风或模型能力。

## 门禁

- [ ] 6 步 SOP 均已执行，不只是体感。
- [ ] 每个最影响阅读的问题都有归因和去向（库文件 / current-state / soul 建议）。
- [ ] 已产出沉淀分流清单（供 step-2 执行）。
- [ ] execution.mode 已判定。

## 下一步

通过门禁后进入 `steps/step-2-commit.md` 执行沉淀分流与落盘。回复采用 PRD §4.7 统一格式。
