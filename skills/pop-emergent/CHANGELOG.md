# CHANGELOG

## v3.5.0 (2026-07-06)

- 四层架构对齐：SKILL.md 瘦身为入口 + 红线 + 速查表 + 加载声明，骨架/owner/命名/execution.mode/版本统一引用 PRD §4 契约层。
- 路由建议改为初始化/修复/审计时的一次性诊断，不再作为每轮正文调度总控。
- 补文件契约层引用：`references/v3.5-pipeline-prd.md` 作为 5 skill 共同真相源。
- 新增 `steps/step-1-init-audit.md`（骨架建立 + 审计报告）、`steps/step-2-fix-route.md`（补缺口 + 一次性路由）、`templates/skeleton-init.tpl.md`（骨架初始化模板）。
- skill.json 补全 displayName/entry/activation/permissions 字段，版本升至 3.5.0。
