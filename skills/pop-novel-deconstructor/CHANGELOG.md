# CHANGELOG — pop-novel-deconstructor

## v4.8.1 (2026-06-03)
- **name/directory 字段对齐**：`name: book-deconstructor`→`pop-novel-deconstructor`，`directory: skill-book-deconstructor`→`pop-novel-deconstructor`
- **内部旧 skill 名修复**：`emergent-writer`→`pop-novel-writer`、`project-bootstrap`→`pop-novel-bootstrap`
- **死路径修复**：`_工具配置/novel-agent-pro/skills/...`→`skills/pop-novel-deconstructor/fragment-pipeline/`
- **书数据污染清理**：`novel-agent-pro 内部拆书引擎`引用指向 `_archive`

## v4.8.0 (2026-06-03)
- 从 novel-agent-pro/skills/skill-book-deconstructor 独立提升
- 修复路径引用（_工具配置/novel-agent-pro/ → skills/pop-novel-deconstructor/）
