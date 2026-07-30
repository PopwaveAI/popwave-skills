# CHANGELOG

## v1.0.0 (2026-07-30)

从 `pop-novel-visual` v2.6.0 拆分独立。专注封面图 + 场景图 + 普通素材三种视觉模式。

### 从 pop-novel-visual 继承
- 三段流程（搜图选图/原文理解 → 设计方案 → 生成）
- 两个用户对齐门禁（门禁A选图+参考点 / 门禁B方案确认）
- 参考点驱动提示词策略
- 场景图原文理解管线（五层）
- 高精度提示词模板（4块结构）
- IP背景提取（同人/改编视觉DNA）
- Pinterest 3维度搜索
- 迭代模式（快速路径）

### 移除
- 人物立绘模式（已拆分到 `pop-novel-oc`）
- 视觉模式路由总览（visual-mode-guide.md，三模式无需路由表）
- 立绘相关的设计方法论和提示词结构

### 文件结构
- SKILL.md / skill.json / CHANGELOG.md
- steps/: step0-research.md, step0-scene-understand.md, step1-design.md, step2-generate.md
- references/: mode-cover.md, mode-scene.md, mode-scene-art.md, novel-visual-design.md, seedream-prompt-guide.md
- templates/: design-plan.tpl.md
- scripts/: generate.py, pinterest_search.py
