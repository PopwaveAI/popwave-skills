# CHANGELOG

## v1.0.0 (2026-07-30)

从 `pop-novel-visual` v2.6.0 拆分独立。专注 OC 角色立绘，新增角色调研管线和系列化输出。

### 从 pop-novel-visual 继承
- 人物立绘设计方法论（六层信息架构+五种布局模板）
- 高精度提示词模板（4块结构）
- IP背景提取（同人/改编视觉DNA）
- Pinterest 搜索（可选，角色气质参考）
- 迭代模式（快速路径）
- mode-character.md 完整保留

### 新增
- **角色调研管线**（step0-character-research.md）：原文关键词搜索→上下文采样→10维度角色档案→门禁A确认
- **调研方法论**（character-research-guide.md）：系统化角色信息采样策略，10维度档案模板
- **系列化输出**：一份角色档案驱动N张系列图（形态演变/核心场景/群像关系），冻结核心特征+变化服饰场景
- **OC专属设计方案模板**（design-plan-oc.tpl.md）

### 移除
- 封面图模式（已拆分到 `pop-novel-cover`）
- 场景图模式（已拆分到 `pop-novel-cover`）
- 普通素材模式（已拆分到 `pop-novel-cover`）
- 视觉模式路由总览（单一模式无需路由表）
- novel-visual-design.md（封面设计库，OC不需要）

### 文件结构
- SKILL.md / skill.json / CHANGELOG.md
- steps/: step0-character-research.md, step1-design.md, step2-generate.md
- references/: mode-character.md, character-research-guide.md, seedream-prompt-guide.md
- templates/: design-plan-oc.tpl.md
- scripts/: generate.py, pinterest_search.py
