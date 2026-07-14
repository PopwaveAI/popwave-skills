# CHANGELOG

## v4.0.0 (2026-07-14)

- 骨架从 5 skill 扩展为 7 skill：新增 pop-emergent-plot、pop-emergent-write-dndlike、pop-emergent-write-onepiece。
- 番茄小说创作 skill 群覆盖替换 pop-emergent 系列。
- 标准流程更新：新增 plot 幕纲+施工卡环节，review 初始化 current-state，write↔review 循环。
- PRD 同步更新 skill 列表和流程描述，契约层规则不变。

## v3.7.0 (2026-07-09)

- 文风DNA通道从"三层文风DNA源"收束为"章内文风DNA源"，只承接文笔笔触和单章剧情套路。
- 骨架与路由表同步改为章内DNA口径，避免把全书架构、卷级节奏或商业体验层塞进文风资产。

## v3.6.0 (2026-07-08)

- 初始化骨架增加文风DNA通道：`soul.md` 预留"文风DNA融合策略"，`current-state.md` 预留"本章DNA执行包"。
- 骨架目录增加 `写作资产/文风库/`，用于承接 pop-shared-dna 产出的文风DNA源。
- 审计描述新增 DNA 执行包闭环检查。

## v3.5.0 (2026-07-06)

- 四层架构对齐：SKILL.md 瘦身为入口 + 红线 + 速查表 + 加载声明，骨架/owner/命名/execution.mode/版本统一引用 PRD §4 契约层。
- 路由建议改为初始化/修复/审计时的一次性诊断，不再作为每轮正文调度总控。
- 补文件契约层引用：`references/v3.5-pipeline-prd.md` 作为 5 skill 共同真相源。
- 新增 `steps/step-1-init-audit.md`（骨架建立 + 审计报告）、`steps/step-2-fix-route.md`（补缺口 + 一次性路由）、`templates/skeleton-init.tpl.md`（骨架初始化模板）。
- skill.json 补全 displayName/entry/activation/permissions 字段，版本升至 3.5.0。