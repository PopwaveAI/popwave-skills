# Step 2-3：调度 create / 按需 revise

> 兼容旧文件名。新流程不再 create→revise 必经。

## create 调度

1. 完整读取 `pop-writer-v3-create/SKILL.md`。
2. 装配：
   - 当前章运行日志段落。
   - 单元卡当前章导演指令。
   - 设定账本。
   - 引用硬设定。
   - 上章末尾。
   - 活记忆。
   - 文风 DNA。
3. 交给 create 正文化。

## revise 调度

只有以下情况触发：

- 用户明确要求修改。
- create 正文明显偏离运行日志结算。
- 正文新增未入账重大设定。

触发时：

1. 完整读取 `pop-writer-v3-revise/SKILL.md`。
2. 注入原正文、用户要求、当前章运行日志、单元卡当前章、设定账本、文风 DNA。
3. 交给 revise 按需修订。

## 禁止

- 禁止默认 revise。
- 禁止额外审计链路。
- 禁止给 revise 塞入与用户修改目标无关的检查清单。
