# CHANGELOG — pop-novel-qa

## v1.0.0 (2026-06-11)

### 定位重构：三层阅读QC → 单一工程审计

工作流全面重构后，原三层介入（大纲层/骨架层/正文层 纯感受QC）的设计已不匹配当前管线。现回归单一目的：

- **只做工程级对齐审计** — 以 `pipeline-arch.md` 为基准，四维扫描：A.文件树完整性 / B.工程级文件质量 / C.管线阶段对齐 / D.文件分类正确性
- **删除全部三层 QC** — Step 1（大纲层）/ Step 2（骨架层）/ Step 3（正文层）全部移除。正文审阅归给写作 skill 自检
- **删除 reader_profile 依赖** — 不再以读者身份阅读，不再输出"纯感受报告"
- **删除 Spec 合规备注层** — 不再跨验 spec.md
- **skill.json**：displayName→项目审计、scenario→audit、slashCommands 更新、recommended 降级、subagentRequired→false
- **QC-renderer.md** 移入 deprecated/
- **audit-renderer.md** 精简为唯一输出模板

## v0.6.0 (2026-06-11)

- 新增 Step 0 全量对齐审计（四维度扫描）
- 新建 audit-renderer.md
- 四层介入架构

## v0.5.0 (2026-06-04)

- 完整重构 SKILL.md：质量红线/什么时候用/前置条件/三层介入/错误示例/异常处理
- skill.json 元数据迁移

## v0.4.2 (2026-06-03)

- name/directory 字段对齐

## v0.4.1 (2026-06-03)

- 从 novel-agent-pro/skills/skill-qa-payoff 独立提升
