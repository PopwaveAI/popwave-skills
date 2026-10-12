## v0.4.0 | 2026-10-12

**拆书入口 skill 迁入技能仓库，与桌面端解耦。**

- 从桌面端内置目录（`apps/desktop/skills/book-decon/`）迁入本仓库 `skills/book-decon/`，此后只在本仓库维护；桌面端不再打包副本，改为按 skill id 从技能库解析。
- 与既有主流程 skill（`pop-decon`、`pop-decon-dimension`）互不修改、互不依赖：本 skill 只服务桌面端拆书链路，沿用独立 id 与独立版本线。
- 本次只换发布位置，SKILL.md 内容未改。
