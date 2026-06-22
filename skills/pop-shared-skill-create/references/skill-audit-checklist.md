# Skill 全量审计清单

> 所属: pop-shared-skill-create · B 改造模式
> 适用: 改造存量 skill 前 / 改造后验收 / 定期健康检查
> 来源: 2026-06-22 全量对齐 session（chapter v2.2 / plot v7.6 / world 层架构清理）

## 审计步骤

### 1. 文件完整性

- [ ] 列出 skill 目录下所有文件（`search_files target=files`）
- [ ] 对照 `SKILL.md` 的速查表/文件索引，确认每个文件都有入口
- [ ] 标记死文件（存在但速查表未引用的文件）→ 删除或补索引

### 2. 版本一致性

- [ ] `SKILL.md` frontmatter `version` vs 标题中的版本号 vs `skill.json` version — 三处一致
- [ ] `CHANGELOG.md` 最新条目版本号匹配
- [ ] 所有 step/reference/template 文件头部的 `管线:` 行版本一致

### 3. 路径有效性

- [ ] 所有文件内引用的路径使用当前 PRD 规范（如 `状态/` 而非 `00-总控/`，`剧情设计/` 而非 `设计/`）
- [ ] 引用上游 skill 产出时，路径格式与上游实际产出一致（如 plot 产出 `.md` 非 `.yaml`）
- [ ] 不引用已删除/已合并的独立文件（如 `chekhov-tracker.md` 已并入 `act-YY.md`）

### 4. 输入/产出对齐 PRD

- [ ] `skill.json` 的 `pipeline.upstream` / `downstream` vs PRD 管线表 — 一致
- [ ] SKILL.md 的输入列表 vs PRD 的「入」列 — 不缺失、不多余
- [ ] SKILL.md 的产出列表 vs PRD 的「出」列 — 不缺失、不多余
- [ ] 共享状态文件（如 entity-snapshot.yaml）的归属方唯一——不能两个 skill 都声称维护

### 5. 死引用清理

- [ ] 全局搜索已废弃的概念名（如 `层架构`、`chekhov-tracker` 独立文件）
- [ ] 被引用文件的路径确实存在
- [ ] 被引用的上游产出在上游 skill 中确实会产出

### 6. 速查表规范

- [ ] 速查表覆盖所有 Step / Template / Reference 文件（不含 CHANGELOG、skill.json 等元数据文件）
- [ ] 每行含「什么时候用」列——agent 知道何时加载
- [ ] Steps 有门禁列，Templates/References 标 `—`
- [ ] 速查表和文件索引不重复——合并为一张表

### 7. 模板内联检查

- [ ] SKILL.md 中不内联完整模板（应放在 `templates/` 下，SKILL.md 只写引用路径）
- [ ] 模板版本号与 SKILL.md 一致

## 审计报告模板

```markdown
## 审计报告 · {skill名} v{版本}

### 文件完整性
- 文件总数: {N}
- 死文件: {列出} 或 无

### 版本一致性
- frontmatter: {v} / 标题: {v} / skill.json: {v} → {一致/不一致}
- CHANGELOG 最新: {v} → {一致/不一致}

### 路径有效性
- 过期路径: {列出} 或 无
- 引用不存在: {列出} 或 无

### 输入/产出 PRD 对齐
- 与 PRD 差异: {列出} 或 一致

### 死引用
- 已废弃概念引用: {列出} 或 无
