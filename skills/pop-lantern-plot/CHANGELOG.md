# CHANGELOG

## v1.0.0 | 2026-09-11

### 灯塔流系列卷级规划首版：基于 pop-mirror-plot v2.5.0 改造

老板拍板：mirror 系列归档 temp，灯塔流照 snow 工程规范建独立系列（snow 吸收 mirror 后为完全体雪花流）。本 skill 承接 mirror-plot 的灯塔流卷级语义，命名空间与交接对象适配：

- **保留不动（灯塔流核心语义）**：主线脉络锁根（世界终点×欲望线绑定/洋葱/结算事件表）、方向总表（每卷一句话，开篇定调后首轮产，半固定）、滚动两卷（只细化当前卷＋下一卷）、卷内单元循环（5-7 单元三档节奏/三类职能/单元剧剧情库三查/生长性/参数递增/6 内容要素）、卷级旅程弧（卷末对手可命名且正面结算）、重大爽点 9 类与每章密度、自检三件、卷末回看滚动。
- **交接对象适配（跨系列复用）**：章节级章纲拆解 pop-mirror-outline → **pop-snow-outline**（复用雪花流，不建双份）；正文渲染 pop-mirror-write → **pop-snow-write**（复用雪花流，不建双份）；审查存档 pop-mirror-review → **pop-lantern-review**（本系列自有）；开篇 pop-mirror-opening → **pop-lantern-opening**（本系列自有）；research 仍为 pop-snow-research 跨系列只读调用。
- **命名空间适配**：pop-mirror-* → pop-lantern-*；账本称呼统一为「全书日志」（对应 pipeline 的 `章节日志/全书日志.md`）。
- **版本与元数据**：version 1.0.0；skill.json 依赖列表指向 pop-lantern-* 与本系列复用的 pop-snow-*；references/单元剧剧情库.md 同步迁移（pop-mirror-plot 引用改 pop-lantern-plot）。

同步三件套：SKILL.md / skill.json / CHANGELOG（＋ references/单元剧剧情库.md）。
