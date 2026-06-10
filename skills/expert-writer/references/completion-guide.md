# completion-guide.md — 完成后引导

> 加载时机：Reflect 阶段末尾，渲染下一轮引导。
> 加载方式：`Get-Content -Encoding UTF8 -Raw`，不用 Read 工具。

---

## 引导模板

> 状态数据来源优先级：① entity-snapshot.yaml ② {paths.chapters}/ch*.md 文件计数 ③ workspace-index.yaml

| 项目状态（读实际文件判断） | 引导语 |
|--------------------------|-------|
| phase == "bootstrapped"，无正文 | 「设定已完成。需要调整吗？需要我帮你规划剧情吗？」 |
| phase == "plotted"，无正文 | 「剧情已规划。需要调整吗？需要我帮你写开头几章吗？」 |
| phase == "writing"，entity-snapshot.total_chapters == N | 「第 N 章已完成。需要修改吗？需要继续写第 N+1 章吗？还是先质检本章？」 |
| qa 刚完成（本轮任务为 qa） | 「质检完成。需要我根据反馈修改吗？」 |
| 参考书分析刚完成（本轮任务为 deconstructor） | 「参考书分析已完成。可以基于分析结果开始开书设定，要开始吗？」 |
| entity-snapshot 缺失或不一致 | 追加：「⚠️ entity-snapshot 与实际章数不一致，建议触发 Writer Step 3.3 重新聚合。」 |
| pre_read_status.verified == false | 追加：「⚠️ 精读闸门未通过，建议下次写作前先补精读。」 |
| file_registry[项目].deprecated 非空 | 追加：「📦 有 {N} 个废弃文件，需要清理吗？」 |

## 引导纪律

1. 每轮先问「需要修改或调整吗？」，再建议下一步
2. 修改完成后自动重新读取文件状态再做引导（不是从上一轮记忆推导）
3. 引导是建议不是催促。用户说不需要 → 停在这里
4. 刚完成 qa 后只问是否修改，不跳下一步
