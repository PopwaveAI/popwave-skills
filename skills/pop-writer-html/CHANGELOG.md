# CHANGELOG — 12-pop-novel-html-renderer

## v1.3.1 (2026-06-04)
- **SKILL.md 全面重写**：精简 frontmatter 为 name + description 双字段；description 统一为触发条件格式（「发布/HTML化/渲染成网页」）
- **新增 ❌ 质量红线**：4 条硬性检查项（HTML 验证 / 设计系统决策理由 / NodeF 前置决策 / 输出路径 宣传/ 合规）
- **新增异常与边界条件表**：覆盖 pop-html-anything 未找到、NodeF.decide 输入不完整、渲染器异常、输出路径不存在、上游数据格式错误、设计系统匹配不到 6 种场景
- **定位声明保留并强化**：明确「本 renderer 是 pop-novel-master 内部专用的 Python 渲染层」及「通用 HTML 渲染 → pop-html-anything」
- **skill.json 元数据重构**：新增 name 字段，version `1.3.0` → `1.3.1`，produces 更新为「宣传/xxx.html」，description 与 SKILL.md 同步

## v1.3.0 (2026-06-03)
- **name 字段对齐**：`name: html-renderer` → `12-pop-novel-html-renderer`
- **死路径修复**：`glue/post_render.py` → `pop-novel-writer/scripts/post_render.py`、`novel-agent-pro` → `pop-novel-master`
- **内部引用修复**：`_shared/html-renderer/__init__.py` → `__init__.py`（自有文件）

## v1.2.0 (2026-06-03)
- 从 novel-agent-pro/skills/_shared/html-renderer 独立提升
- 修复路径引用
