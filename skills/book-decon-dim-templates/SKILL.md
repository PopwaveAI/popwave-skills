---
name: book-decon-dim-templates
description: book-decon-dimension 的产物模板资源包：产出 L2 六模块、爽点、立项 L0-L3 等成品需读取模板时，按本包根 templates/ 路径按需读取对应 .tpl.md；本包不含执行规程。
---

# book-decon-dim-templates · 拆书执行模板集

> `book-decon-dimension` 的 L2 产物模板资源包，只存模板、不含执行规程。v0.1.0：自 book-decon-dimension 拆出，模板内容零改动。完整版本历史见 CHANGELOG.md。

## 是什么

本包存放 `book-decon-dimension`（单书拆解执行 skill）产出**完整交付 L2 成品**所用的逐文件模板，共 31 份 `.tpl.md`，覆盖：剧情库（4）、角色与势力库（7）、力量与战斗（3）、世界观（5）、赛道特色（3）、文风DNA（1）、收尾（爽点、立项 ×5、索引、CHANGELOG，共 8）。每份模板头部自带 `template_id` 与 `template_version`。

执行规程、门禁、产物目录契约与模板稳定契约（改模板须升 `template_version` 并同步文档与 CHANGELOG）均在 `book-decon-dimension` 的 SKILL.md，以那边为准；本包不重复。

## 目录结构

- `templates/` — 31 份 `.tpl.md`（分布见上）。
- 骨架交付（`outline`）的三份卷级骨架模板尚未提供，与执行 skill 的「待补清单」一致。

## 谁在引用、怎么读

- 引用方：`book-decon-dimension`（入口 skill `book-decon` 不读模板，只在收尾核对版本目录 `_meta/templates.json` 留痕）。
- 跨包读取写法：`<book-decon-dim-templates 包根>/templates/<模板名>.tpl.md`；包根 = 本 SKILL.md 所在目录（系统提示 `<available_skills>` 中本 skill 的 `<location>`）。
