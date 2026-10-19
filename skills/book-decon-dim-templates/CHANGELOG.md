## 0.1.1 - 2026-10-19

- 补充市场卡面 summary 与精选元数据。

# book-decon-dim-templates 更新日志

## v0.1.0 | 2026-10-13

**自 `book-decon-dimension` 拆出，模板内容零改动。**

- runner 容器注入单技能总量限制 ≤128KB，原 `book-decon-dimension`（含 31 份模板）约 175KB 超限；`templates/` 整目录原样迁入本包，未压缩、未改写任何模板内容（含各模板头部的 `template_id` / `template_version`）。
- 引用方 `book-decon-dimension` 同步升 v0.2.1：其 SKILL.md 的模板路径引用改指本包（`<book-decon-dim-templates 包根>/templates/`），执行逻辑与门禁不变。
