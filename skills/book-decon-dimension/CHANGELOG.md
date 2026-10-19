## 0.2.2 - 2026-10-19

- 补充市场卡面 summary 与精选元数据。

## v0.2.1 | 2026-10-13

**产物模板拆出为独立技能包 `book-decon-dim-templates`（v0.1.0），本包减重。**

- runner 容器注入单技能总量限制 ≤128KB，原包（SKILL.md + references + 31 份模板）约 175KB 超限；`templates/` 整目录原样迁入新技能包 `book-decon-dim-templates`，模板内容零改动。
- 本包仅剩 SKILL.md、`references/`（三份交付格式）与元数据；SKILL.md 中所有 `templates/` 路径引用改为 `<book-decon-dim-templates 包根>/templates/`，仅改路径归属表述，执行逻辑与门禁不变。
- 模板契约不变：改模板仍按「模板与稳定契约」节三同步（模板升 `template_version` + 文档 + CHANGELOG 留痕），只是模板落在新包内。

## v0.2.0 | 2026-10-12

**拆书执行 skill 迁入技能仓库，与桌面端解耦。**

- 从桌面端内置目录（`apps/desktop/skills/book-decon-dimension/`）迁入本仓库 `skills/book-decon-dimension/`，含 `references/`（三份交付格式）与 `templates/`（31 份 L2 模板），此后只在本仓库维护。
- 桌面端的成品体检（结构核对、模板留痕）改为按 skill id 解析本 skill 的 `templates/` 目录，不再依赖应用内副本。
- 与既有 `pop-decon-dimension` 互不修改、互不依赖，沿用独立 id 与独立版本线。
- 本次只换发布位置，SKILL.md 与模板内容未改；`skill.json` 的 description 去掉了迁移后已不成立的「不依赖 popwave-skills」表述，改为「与本仓库既有 pop-decon 系列各自独立」。
