# Changelog

## v0.1.0 (2025-06-23)

### 新增

- 从 OnKos v2 改编而来，保留 8 个核心引擎脚本（memory_engine / fact_engine / knowledge_graph / hook_tracker / arc_manager / semantic_model / context_retriever / entity_extractor）
- 全部 SQLite 表名和索引名加 `pop_` 前缀，避免与 OnKos 同环境冲突
- SCHEMA_VERSION 重置为 1（新项目起点）
- 改造 `command_executor.py`：删除 13 个流程层命令（character_simulator / quality_auditor / continuity_checker / style_learner / plot_brancher），新增 3 个内置命令：
  - `catalog` — 运行时 DB 自描述（表描述 + 行数 + 样本 + 分组统计 + 快捷查询）
  - `dump-dashboard` — HTML 仪表盘生成（5 面板：表概览 / 知识图谱 / 伏笔状态 / 事实版本链 / 按章时间线）
  - `project-status` — 总控聚合查询（总章数 / 当前弧线 / 下一章 / 主角状态 / 关键伏笔）
- 改造 `project_initializer.py`：删除 OnKos 特有目录结构（outline/drafts/revisions），精简 project_config.json
- 新增 `dashboard_generator.py`：自包含 HTML 仪表盘生成器，ECharts CDN 可视化
- 编写 SKILL.md + skill.json + cli-reference.md + integration-guide.md

### 修复

- 修复 context_retriever.py 中 `pop_facts` / `pop_hooks` 变量名误前缀化（应为 `facts` / `hooks`）
- 修复 hook_tracker.py 重复 `if __name__` 块
- 修复 arc_manager.py broken finally block（重复 close 调用）

### 已知限制

- onnxruntime 未安装时跳过 embedding 相关功能
- dashboard 使用 ECharts CDN，离线环境需改为本地引用

### FTS5 搜索方案变更

初始版本使用 jieba 分词 + FTS5 unicode61 组合，但发现两个问题：
1. jieba 分词不一致：同一词在不同上下文分词结果不同，导致索引和查询不匹配
2. OR 查询精度差：jieba 把"碎骨指"分成"碎骨 指"，OR 查询"碎骨 OR 指"会匹配所有含"指"的文本

改为 **bigram（双字）分词**：
- 索引：`"碎骨指功法"` → `"碎骨 骨指 指功 功法"`
- 查询：`"碎骨指"` → `"碎骨 AND 骨指"`（≈ 子串匹配）
- 零依赖、一致、高精度

jieba 仍保留给 entity_extractor 做词性标注（已 vendor 到 `scripts/jieba/`，18.6MB）。
