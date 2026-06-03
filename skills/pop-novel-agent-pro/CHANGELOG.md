# CHANGELOG — pop-novelagent

> 版本规则：主版本.次版本.修订号
> 每次调优产生一个新版本号

---

## v3.3.1 (2026-06-03)

**根因**: Skill 群拆分与去重 — pop 批量清理行动
**类型**: cleanup
**改动**:
- **🗑️ 删除重复**：移除了 `skills/cnovel-research/` 内部副本（顶层 `skills/cnovel-research/` 已存在）
- **🗑️ 合并去重**：`spec-bridge/` 统一迁移至 `_soul/spec-bridge/`（原位置留 README.md 桥接）
- **📝 边界声明**：`skill-book-deconstructor/SKILL.md` 新增协作边界声明，标注"拆书为写"定位，区分于 `pop-reader-making` 的"拆书为读"
- **📝 定位声明**：`html-renderer/SKILL.md` 新增定位声明，标注为"novel-agent-pro 内部专用"
- **📦 独立提升**：`book-opinion-tracker` 从内部子 skill 提升为顶层 `skills/book-opinion-tracker/`
**效果**: 子 skill 从 12+ 精简至 7 核心模块；外围重复全部清理；定位边界清晰化

## v3.3.0 (2026-06-02)

**根因**: —（初始版本记录）
**类型**: —
**改动**: 当前稳定版本。全功能写作 Agent，六阶段写作管线。具备 VERSION.md + 根因库 + 复盘目录的完整知识沉淀体系。
**效果**: —
