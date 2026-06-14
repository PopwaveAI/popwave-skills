# CHANGELOG — book-opinion-tracker

> 版本规则：主版本.次版本.修订号

---

## v1.8.0 (2026-06-03)

**根因**: Skill 群拆分 — 从 pop-novel-agent-pro 内部提升为顶层独立 skill
**类型**: migration
**改动**:
- 从 `pop-novel-agent-pro/skills/book-opinion-tracker/` 迁移至顶层 `skills/book-opinion-tracker/`
- 新增 `skill.json` 注册文件
- POP-CALL 路径更新为 `_soul/pop/POP-CALL.md`
- 依赖声明更新：cnovel-research 指向顶层 `skills/cnovel-research/`
**效果**: 独立 skill，可被任何项目直接调用，不依赖 novel-agent-pro
