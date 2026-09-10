# CHANGELOG

## v1.0.0 | 2026-09-11

### 灯塔流系列审查首版：基于 pop-mirror-review v1.1.0 改造

老板拍板：mirror 系列归档 temp，灯塔流照 snow 工程规范建独立系列。本 skill 承接 mirror-review 的审查存档语义，命名空间与交接对象适配：

- **保留不动**：三源合一审查（角色/设定/连续性）＋满意判别标准七条＋打回四要素；三件事存档（确认满意→本章日志→全书日志→退出档案）；账本职责（全书日志承载方向总表进度/跨卷钩子）；卷末回看（兑现核对/方向总表进度/跨卷钩子/下一卷方向建议，交 plot 滚下一卷）；去AI味核验与存档后半步（deai_gate doc）；三源精华（04/09/08）逐字直贴；批量回溯流程。
- **交接对象适配（跨系列复用）**：正文审查承接 pop-mirror-write → **pop-snow-write**；章纲去AI味结果查 pop-mirror-outline → **pop-snow-outline**；卷末回看报告交 pop-mirror-plot → **pop-lantern-plot**；事实回流对象 pop-mirror-world/character → **pop-lantern-world/character**。
- **落盘路径统一**：剧情进度记录目录由 `小说日志/` 统一为 pipeline 约定的 `章节日志/`（卷末回看 = `章节日志/卷末回看-卷{N}.md`），与灯塔流 pipeline 资产归位表一致。
- **版本与元数据**：version 1.0.0；templates 四件（chapter-card/state-snapshot/exit-archive/卷末回看）同步迁移，卷末回看模板 primary_consumer 改指 pop-lantern-plot。

同步三件套：SKILL.md / skill.json / CHANGELOG（＋ templates 四件）。
