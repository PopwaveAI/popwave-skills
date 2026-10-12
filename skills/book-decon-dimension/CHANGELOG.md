## v0.2.0 | 2026-10-12

**拆书执行 skill 迁入技能仓库，与桌面端解耦。**

- 从桌面端内置目录（`apps/desktop/skills/book-decon-dimension/`）迁入本仓库 `skills/book-decon-dimension/`，含 `references/`（三份交付格式）与 `templates/`（31 份 L2 模板），此后只在本仓库维护。
- 桌面端的成品体检（结构核对、模板留痕）改为按 skill id 解析本 skill 的 `templates/` 目录，不再依赖应用内副本。
- 与既有 `pop-decon-dimension` 互不修改、互不依赖，沿用独立 id 与独立版本线。
- 本次只换发布位置，SKILL.md 与模板内容未改。
