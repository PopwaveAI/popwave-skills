# pop-jinjiang-outline

> 晋江平台大纲技能 v1.0.0（2026-10-29）。

- 从 `pop-snow-seed` 复制内容并改名，首版与 snow 大纲总控一致。
- 只保留大纲角色；正文交给 `pop-jinjiang-write`。

## v1.0.1 | 2026-10-30

- 完整立项包改为 idea 一次生成，setting/outline 只在用户要求深化时调用。
- brief 三选一改为带 detail 的长方案卡，并标记 critical；超时不再自动选推荐。

## v1.0.2 | 2026-10-30

- 回滚 idea 一次生成完整立项包，恢复 idea → setting → outline 多次方案；避免单次输出撞模型额度。
- brief 仍保留 detail 长方案卡与 critical 标记。
