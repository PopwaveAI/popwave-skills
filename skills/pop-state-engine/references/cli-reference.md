# pop-state-engine CLI 命令参考

## 调用方式

```bash
python scripts/command_executor.py -p {project_path} -a {action} -j '{json_params}'
```

| 参数 | 说明 |
|------|------|
| `-p, --project-path` | 项目根目录路径（必填） |
| `-a, --action` | 要执行的命令名或别名（必填） |
| `-j, --params` | 命令参数，JSON 字符串（默认 `{}`） |
| `-o, --output` | 输出文件路径（仅 `dump-dashboard` 使用） |

所有命令均输出 JSON 格式结果。命令名支持英文别名和中文别名，下文各命令处标注。

---

## 1. 系统

系统级聚合命令，由 `command_executor.py` 内置实现，不依赖外部引擎模块。

### help

**别名**：`帮助`、`指令列表`、`命令列表`、`指令详情`、`?`

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 否 | 查看特定命令的模块和动作详情 |
| `topic` | 否 | 查看特定分类下的命令列表（系统/初始化/存储/查询/事实管理/伏笔追踪/弧线管理/上下文） |

```bash
-a help -j '{"topic": "存储"}'
```

**返回**：命令分类字典和总命令数；或特定命令的 module/action 信息；或特定分类的命令列表。

---

### catalog

**别名**：`目录`

| 参数 | 必填 | 说明 |
|------|------|------|
| 无 | — | — |

```bash
-a catalog
```

**返回**：数据库表目录（表名、描述、行数、可查询维度、样本数据）、分组统计（节点类型/事实重要性/伏笔状态/摘要层级）、快速查询建议列表。

---

### dump-dashboard

**别名**：`仪表盘`

| 参数 | 必填 | 说明 |
|------|------|------|
| `output` | 否 | HTML 输出路径，默认 `data/dashboard.html` |

```bash
-a dump-dashboard -j '{"output": "data/dashboard.html"}'
```

**返回**：`success`（布尔）、`output`（文件路径）、`size_bytes`（文件大小）。

---

### project-status

**别名**：`项目状态`

| 参数 | 必填 | 说明 |
|------|------|------|
| 无 | — | — |

```bash
-a project-status
```

**返回**：`total_chapters`、`total_scenes`、`next_chapter`、`current_arc`、`active_phase`、`current_volume`、`protagonist_state`、`critical_hooks`（关键伏笔列表）、`open_hooks_count`、`overdue_hooks_count`、`kg_node_count`、`fact_count`。

---

## 2. 初始化

项目初始化与状态查询，由 `project_initializer.ProjectInitializer` 实现。

### init

**别名**：`创建项目`

| 参数 | 必填 | 说明 |
|------|------|------|
| `title` | 否 | 小说标题（默认"未命名小说"） |
| `genre` | 否 | 题材类型（默认"玄幻"） |
| `author` | 否 | 作者 |
| `description` | 否 | 简介 |

```bash
-a init -j '{"title": "我的小说", "genre": "玄幻", "author": "作者"}'
```

**返回**：`project_path`、`created_files`（project_config.json、novel_memory.db）、`created_dirs`（data/）、`errors`。

---

### status

**别名**：`状态`

| 参数 | 必填 | 说明 |
|------|------|------|
| 无 | — | — |

```bash
-a status
```

**返回**：`project_path`、`exists`（项目目录是否存在）、`initialized`（是否已初始化）、`config`（项目配置）、`stats`（数据库大小和路径）。

---

## 3. 存储

场景与摘要的存储、检索、弧线管理，由 `memory_engine.MemoryEngine` 实现。

### store-chapter

**别名**：`写`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 是 | 章节编号 |
| `content` | 是 | 章节全文（与 `content_file` 二选一） |
| `content_file` | 否 | 内容文件路径，读取后覆盖 `content` |
| `tags` | 否 | 关键词标签（逗号分隔） |
| `characters` | 否 | 出场角色（逗号分隔） |
| `events` | 否 | 关键事件（逗号分隔） |
| `replace` | 否 | 布尔，True 时先删除该章节旧场景再录入 |

```bash
-a store-chapter -j '{"chapter": 1, "content": "第一章正文...", "tags": "入门,修炼", "characters": "林凡,苏瑶"}'
```

**返回**：`scene_ids`（场景ID列表）、`scene_count`（场景数量）。章节按段落自动拆分为多个场景。

---

### store-scene

**别名**：`存储`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 是 | 章节编号 |
| `content` | 是 | 场景原文（与 `content_file` 二选一） |
| `content_file` | 否 | 内容文件路径 |
| `tags` | 否 | 关键词标签 |
| `location` | 否 | 场景地点 |
| `characters` | 否 | 出场角色 |
| `mood` | 否 | 情感基调 |
| `events` | 否 | 关键事件 |
| `replace` | 否 | 布尔，True 时先删除该章节旧场景 |

```bash
-a store-scene -j '{"chapter": 1, "content": "场景内容...", "location": "玄天峰", "mood": "紧张"}'
```

**返回**：`scene_id`（场景ID）。

---

### delete-chapter-scenes

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 是 | 要删除场景的章节编号 |

```bash
-a delete-chapter-scenes -j '{"chapter": 5}'
```

**返回**：`deleted_count`（删除的场景数）、`chapter`。同时删除 FTS 索引和 embedding。

---

### search

**别名**：`搜索`

| 参数 | 必填 | 说明 |
|------|------|------|
| `query` | 是 | 搜索关键词（支持 `OR` 分词） |
| `top_k` | 否 | 返回结果数量（默认 5） |
| `chapter` | 否 | 精确章节过滤 |
| `chapter_range` | 否 | 章节范围过滤，格式 `"start,end"`，优先于 `chapter` |

```bash
-a search -j '{"query": "突破筑基", "top_k": 10, "chapter_range": "1,50"}'
```

**返回**：`results`（场景列表，含 id/content/tags/chapter/location/characters/mood/events/rank）。优先使用 ONNX 语义搜索，不可用时回退 FTS5 关键词搜索。

---

### store-summary

**别名**：`更新摘要`

| 参数 | 必填 | 说明 |
|------|------|------|
| `level` | 是 | 摘要层级：`book`/`phase`/`arc`/`volume`/`chapter`/`scene` |
| `content` | 是 | 摘要内容（与 `content_file` 二选一） |
| `content_file` | 否 | 内容文件路径 |
| `range_desc` | 否 | 范围描述。未提供时从 `chapter`/`volume`/`arc_id`/`phase_id` 自动推断 |
| `chapter` | 否 | 章节号（用于自动推断 `range_desc`） |
| `volume` | 否 | 卷号（用于自动推断） |
| `arc_id` | 否 | 弧线ID（用于自动推断） |
| `phase_id` | 否 | 阶段ID（用于自动推断） |

```bash
-a store-summary -j '{"level": "chapter", "chapter": 5, "content": "第五章：主角突破筑基..."}'
```

**返回**：`summary_id`（摘要ID）。

---

### mem-stats

**别名**：`统计`

| 参数 | 必填 | 说明 |
|------|------|------|
| 无 | — | — |

```bash
-a mem-stats
```

**返回**：`total_scenes`、`total_summaries`、`active_facts`、`total_embeddings`、`chapters`（章节号列表）、`pop_kg_nodes`、`pop_kg_edges`、`open_hooks`、`total_arcs`、`onnx_available`。

---

### create-arc

| 参数 | 必填 | 说明 |
|------|------|------|
| `arc_id` | 是 | 弧线ID |
| `title` | 是 | 弧线标题 |
| `start_chapter` | 是 | 起始章节 |
| `arc_type` | 否 | 弧线类型（默认 `arc`） |
| `end_chapter` | 否 | 结束章节 |
| `phase_id` | 否 | 所属阶段ID |
| `description` | 否 | 描述 |

```bash
-a create-arc -j '{"arc_id": "arc_001", "title": "初入宗门", "start_chapter": 1, "end_chapter": 30}'
```

**返回**：`arc_id`。

---

### list-arcs

**别名**：`列出弧线`

| 参数 | 必填 | 说明 |
|------|------|------|
| `arc_type` | 否 | 过滤类型：`arc` 或 `phase` |

```bash
-a list-arcs -j '{"arc_type": "arc"}'
```

**返回**：`arcs`（弧线列表，含 id/title/arc_type/start_chapter/end_chapter/phase_id/description）。

---

### chapter-complete

**别名**：`完成章节`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 是 | 章节编号 |
| `content` | 是 | 章节全文（与 `content_file` 二选一） |
| `content_file` | 否 | 内容文件路径 |
| `tags` | 否 | 关键词标签 |
| `characters` | 否 | 出场角色 |
| `events` | 否 | 关键事件 |

```bash
-a chapter-complete -j '{"chapter": 5, "content": "第五章正文..."}'
```

**返回**：`scene_ids`、`scene_count`。等同于 `store-chapter` 且 `replace=true`，先删除旧场景再录入。

---

## 4. 查询

上下文检索与预算分析，由 `context_retriever.ContextRetriever` 实现。`search` 命令见上方存储分类。

### for-creation

**别名**：`续写`、`获取上下文`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 否 | 目标章节（省略时自动推断为最新章节+1） |
| `query` | 否 | 创作意图/大纲描述，用于语义搜索相关场景 |
| `entities` | 否 | 大纲中提及的实体名（逗号分隔） |
| `max_chars` | 否 | 上下文字符预算上限（默认 12000） |
| `format` | 否 | 输出格式：`structured`（默认，结构化字典）或 `text`（可读文本） |

```bash
-a for-creation -j '{"chapter": 10, "query": "主角突破筑基", "entities": "林凡,苏瑶", "format": "text"}'
```

**返回**：6 级分层上下文字典，包含 `book_summary`、`current_state`、`phase_summary`、`arc_summary`、`volume_summary`、`prev_chapter_summary`、`current_chapter_summary`、`related_scenes`、`relevant_facts`、`hooks`、`continuity_notes`、`metadata`（含 chapter/volume/total_chars/budget_used_pct/facts_count/hooks_count/scenes_count）。

---

### context-hierarchy

**别名**：`覆盖检查`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 否 | 目标章节（省略时自动推断） |

```bash
-a context-hierarchy -j '{"chapter": 10}'
```

**返回**：各层级摘要是否存在（布尔值）：`L0_book`、`L0_current_state`、`L1_phase`、`L2_arc`、`L3_volume`、`L4_prev_chapter`、`L4_current_chapter`，以及 `chapter`、`volume`。

---

### budget-report

**别名**：`预算`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 否 | 目标章节（省略时自动推断） |
| `query` | 否 | 创作意图（影响相关场景搜索） |

```bash
-a budget-report -j '{"chapter": 10}'
```

**返回**：各上下文层级的预算使用报告，每项含 `budget`（预算字符数）、`used`（已用字符数）、`pct`（使用百分比）。覆盖 book_summary/current_state/phase_summary/arc_summary/volume_summary/prev_chapter_summary/current_chapter_summary/related_scenes/relevant_facts/hooks/continuity_notes。

---

## 5. 事实管理

事实的录入、查询、相关性筛选、矛盾检测与归档，由 `fact_engine.FactEngine` 实现。

### set-fact

**别名**：`录入事实`、`更新事实`

| 参数 | 必填 | 说明 |
|------|------|------|
| `entity` | 是 | 实体名 |
| `attribute` | 是 | 属性名 |
| `value` | 是 | 属性值 |
| `chapter` | 是 | 确立该事实的章节 |
| `category` | 否 | 类别（character/world/item/event，默认"默认"） |
| `importance` | 否 | 重要性：`permanent`/`arc-scoped`/`chapter-scoped`（默认 `chapter-scoped`） |
| `valid_from` | 否 | 生效起始章节（默认同 chapter） |
| `valid_until` | 否 | 失效章节（默认永久，直到被替代） |

```bash
-a set-fact -j '{"entity": "林凡", "attribute": "境界", "value": "筑基", "chapter": 5, "importance": "arc-scoped", "category": "character"}'
```

**返回**：`fact_id`。同实体同属性的旧事实自动标记为已替代（版本链）。

---

### get-fact

**别名**：`查事实`

| 参数 | 必填 | 说明 |
|------|------|------|
| `entity` | 是 | 实体名 |
| `attribute` | 是 | 属性名 |

```bash
-a get-fact -j '{"entity": "林凡", "attribute": "境界"}'
```

**返回**：`entity`、`attribute`、`value`（当前有效值，可能为 null）。

---

### get-facts

| 参数 | 必填 | 说明 |
|------|------|------|
| `entity` | 否 | 按实体名过滤 |
| `category` | 否 | 按类别过滤 |
| `limit` | 否 | 最大返回数量 |

```bash
-a get-facts -j '{"entity": "林凡", "limit": 20}'
```

**返回**：`facts`（当前有效事实列表，按章节倒序）。

---

### relevant-facts

**别名**：`相关事实`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 否 | 当前章节（省略时自动推断） |
| `entity` | 否 | 提及实体名（逗号分隔多个） |
| `limit` | 否 | 最大返回数量（默认 80） |

```bash
-a relevant-facts -j '{"chapter": 10, "entity": "林凡,苏瑶"}'
```

**返回**：`facts`（按相关性排序的事实列表）、`count`、`current_chapter`。相关性优先级：permanent 事实 > 提及实体事实 > 当前弧线 arc-scoped 事实 > 近 10 章 chapter-scoped 事实。

---

### list-all-facts

**别名**：`查所有事实`

| 参数 | 必填 | 说明 |
|------|------|------|
| `entity` | 否 | 按实体名过滤 |
| `category` | 否 | 按类别过滤 |
| `limit` | 否 | 最大返回数量 |

```bash
-a list-all-facts
```

**返回**：`facts`（所有当前有效事实，按章节倒序）。与 `get-facts` 行为一致，语义上用于无过滤的全量列举。

---

### archive-facts

**别名**：`归档事实`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 是 | 当前章节 |
| `limit` | 否 | 归档阈值，超过多少章前的事实被归档（默认 200） |

```bash
-a archive-facts -j '{"chapter": 250, "limit": 200}'
```

**返回**：`archived_count`（归档数量）。将超旧的 chapter-scoped 事实标记为已归档。

---

### supersede-chapter-facts

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` | 是 | 要清理的章节编号 |

```bash
-a supersede-chapter-facts -j '{"chapter": 5}'
```

**返回**：`superseded_count`（废弃数量）、`chapter`。将指定章节确立的有效事实标记为系统废弃（superseded_by=-2），用于修订章节时清理旧事实。

---

### detect-contradictions

**别名**：`矛盾`

| 参数 | 必填 | 说明 |
|------|------|------|
| 无 | — | — |

```bash
-a detect-contradictions
```

**返回**：`contradictions`（矛盾列表，含 entity/attribute/cnt）。检测同实体同属性存在多个未替代事实的情况。

---

### fact-history

| 参数 | 必填 | 说明 |
|------|------|------|
| `entity` | 是 | 实体名 |
| `attribute` | 否 | 属性名。提供时返回该属性的完整变更历史；省略时返回该实体的所有当前有效事实 |

```bash
-a fact-history -j '{"entity": "林凡", "attribute": "境界"}'
```

**返回**：提供 `attribute` 时返回 `history`（含 id/value/chapter/importance/valid_from/valid_until/created_at/superseded_by 的版本链）；仅提供 `entity` 时返回 `entity` 和 `facts`。

---

## 6. 伏笔追踪

伏笔的种埋、收线、放弃与状态查询，由 `hook_tracker.HookTracker` 实现。

### plant-hook

**别名**：`种伏笔`

| 参数 | 必填 | 说明 |
|------|------|------|
| `desc` 或 `description` | 是 | 伏笔描述（`desc` 自动映射为 `description`） |
| `planted_chapter` 或 `chapter` | 是 | 种埋章节 |
| `expected_resolve` | 否 | 预期收线章节 |
| `priority` | 否 | 优先级：`critical`/`normal`/`minor`（默认 `normal`） |
| `tags` | 否 | 标签（逗号分隔） |
| `characters` | 否 | 关联角色（逗号分隔） |
| `hook_id` | 否 | 自定义伏笔ID（默认自动生成 `hook_XXXXXXXX`） |

```bash
-a plant-hook -j '{"desc": "神秘玉佩的来历", "planted_chapter": 3, "expected_resolve": 20, "priority": "critical"}'
```

**返回**：`hook_id`。同描述的 open 伏笔已存在时直接返回已有ID（自动去重）。

---

### resolve-hook

**别名**：`回收伏笔`

| 参数 | 必填 | 说明 |
|------|------|------|
| `hook_id` | 是 | 伏笔ID |
| `resolved_chapter` | 是 | 收线章节 |
| `how` 或 `resolution` | 否 | 收线描述（`how` 自动映射为 `resolution`） |

```bash
-a resolve-hook -j '{"hook_id": "hook_abc12345", "resolved_chapter": 20, "how": "玉佩原来是上古传承"}'
```

**返回**：`success`（布尔）。已回收的伏笔不会被重复回收。

---

### abandon-hook

**别名**：`放弃伏笔`

| 参数 | 必填 | 说明 |
|------|------|------|
| `hook_id` | 是 | 伏笔ID |
| `reason` | 否 | 放弃原因 |

```bash
-a abandon-hook -j '{"hook_id": "hook_abc12345", "reason": "剧情调整"}'
```

**返回**：`success`（布尔）。

---

### abandon-chapter-hooks

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` 或 `planted_chapter` | 是 | 种埋章节 |
| `reason` | 否 | 放弃原因（默认"章节修订"） |

```bash
-a abandon-chapter-hooks -j '{"chapter": 5}'
```

**返回**：`abandoned_count`（放弃数量）、`chapter`。放弃指定章节种埋的所有 open 伏笔。

---

### list-hooks

**别名**：`列出伏笔`

| 参数 | 必填 | 说明 |
|------|------|------|
| `current_chapter` | 否 | 当前章节，提供时按超期优先排序 |
| `priority` | 否 | 按优先级过滤：`critical`/`normal`/`minor` |

```bash
-a list-hooks -j '{"current_chapter": 15}'
```

**返回**：`hooks`（open 状态伏笔列表，含 id/desc/planted_chapter/expected_resolve/priority/tags/related_characters）。提供 `current_chapter` 时超期伏笔优先显示。

---

### overdue-hooks

**别名**：`伏笔`

| 参数 | 必填 | 说明 |
|------|------|------|
| `current_chapter` | 是 | 当前章节 |

```bash
-a overdue-hooks -j '{"current_chapter": 15}'
```

**返回**：`hooks`（超期未收的伏笔列表，即 expected_resolve < current_chapter 且 status=open）。

---

### forgotten-hooks

| 参数 | 必填 | 说明 |
|------|------|------|
| `current_chapter` | 是 | 当前章节 |

```bash
-a forgotten-hooks -j '{"current_chapter": 120}'
```

**返回**：`hooks`（可能被遗忘的伏笔列表，即种埋章节距当前超过 100 章且仍未收线）。

---

### hook-stats

**别名**：`伏笔统计`

| 参数 | 必填 | 说明 |
|------|------|------|
| 无 | — | — |

```bash
-a hook-stats
```

**返回**：`status_counts`（按状态计数：open/resolved/abandoned）、`open_priority_counts`（open 伏笔按优先级计数）、`total`。

---

## 7. 弧线管理

创作弧线与阶段的创建、完成、进度追踪，由 `arc_manager.ArcManager` 实现。

### create-phase

**别名**：`创建阶段`

| 参数 | 必填 | 说明 |
|------|------|------|
| `phase_id` 或 `arc_id` | 是 | 阶段ID |
| `title` 或 `arc_title` | 是 | 阶段标题 |
| `start_chapter` | 是 | 起始章节 |
| `end_chapter` | 否 | 结束章节 |
| `description` | 否 | 描述 |

```bash
-a create-phase -j '{"phase_id": "phase_1", "title": "第一卷：起步", "start_chapter": 1, "end_chapter": 100}'
```

**返回**：`phase_id`。

---

### create-arc-am

**别名**：`创建弧线`

| 参数 | 必填 | 说明 |
|------|------|------|
| `arc_id` | 是 | 弧线ID |
| `title` 或 `arc_title` | 是 | 弧线标题 |
| `start_chapter` | 是 | 起始章节 |
| `end_chapter` | 否 | 结束章节 |
| `phase_id` | 否 | 所属阶段ID |
| `description` | 否 | 描述 |

```bash
-a create-arc-am -j '{"arc_id": "arc_001", "title": "初入宗门", "start_chapter": 1, "phase_id": "phase_1"}'
```

**返回**：`arc_id`。

---

### complete-arc

**别名**：`完成弧线`

| 参数 | 必填 | 说明 |
|------|------|------|
| `arc_id` | 是 | 弧线ID |
| `end_chapter` | 是 | 结束章节 |

```bash
-a complete-arc -j '{"arc_id": "arc_001", "end_chapter": 30}'
```

**返回**：`success`（布尔）。设置弧线的 end_chapter 标记为已完成。

---

### arc-progress

**别名**：`进度`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` 或 `current_chapter` | 否 | 当前章节（省略时自动推断为最新已存储章节） |

```bash
-a arc-progress
```

**返回**：`current_chapter`、`auto_inferred`（是否自动推断）、`active_phase`（当前阶段）、`active_arc`（当前弧线）、`phases`（所有阶段及状态）、`arcs`（所有弧线及状态）。状态为"进行中"/"已完成"/"未开始"。

---

### suggest-next

**别名**：`建议`

| 参数 | 必填 | 说明 |
|------|------|------|
| `chapter` 或 `current_chapter` | 否 | 当前章节（省略时自动推断） |

```bash
-a suggest-next
```

**返回**：下一个待开始的弧线信息（含 id/title/start_chapter/phase_id 等）和 `current_chapter`；无待开始弧线时返回 `suggestion: null` 和提示消息。

---

## 8. 知识图谱

实体关系网络管理，由 `knowledge_graph.KnowledgeGraph` 实现。

### add-node

**别名**：`添加节点`

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 实体名称 |
| `type` 或 `node_type` | 是 | 节点类型：`character`/`location`/`item`/`faction`/`concept` |
| `tags` | 否 | 标签（逗号分隔） |
| `properties` | 否 | 属性字典（JSON 字符串） |
| `node_id` | 否 | 自定义节点ID（默认自动生成 `{type}_{md5前8位}`） |

```bash
-a add-node -j '{"name": "林凡", "type": "character", "tags": "主角,修仙", "properties": "{\"age\": 18}"}'
```

**返回**：`node_id`。已存在同ID节点时执行更新（INSERT OR REPLACE）。

---

### add-edge

**别名**：`添加关系`

| 参数 | 必填 | 说明 |
|------|------|------|
| `source` | 是 | 源节点ID或名称（名称自动解析为ID） |
| `target` | 是 | 目标节点ID或名称（名称自动解析为ID） |
| `relation` | 是 | 关系类型 |
| `properties` | 否 | 属性字典（JSON 字符串） |

```bash
-a add-edge -j '{"source": "林凡", "target": "苏瑶", "relation": "师妹"}'
```

**返回**：`edge_id`。`source`/`target` 支持传入节点名称，自动通过 `find_node_by_name` 解析为节点ID。也支持 `from_name`/`to_name`/`from`/`to` 别名。

---

### find-node

**别名**：`查节点`

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 节点名称 |

```bash
-a find-node -j '{"name": "林凡"}'
```

**返回**：节点详情（id/type/name/tags/properties），未找到时返回 null。

---

### get-neighbors

**别名**：`查邻居`

| 参数 | 必填 | 说明 |
|------|------|------|
| `node_id` 或 `name` | 是 | 节点ID或名称（二选一，名称自动解析） |
| `depth` | 否 | 搜索深度（默认 1） |
| `relation` | 否 | 按关系类型过滤 |

```bash
-a get-neighbors -j '{"name": "林凡", "depth": 2}'
```

**返回**：`nodes`（邻居节点字典，key 为节点ID）、`edges`（涉及的边列表）。使用 BFS 遍历。

---

### find-path

**别名**：`查路径`

| 参数 | 必填 | 说明 |
|------|------|------|
| `source` 或 `from_name` 或 `from` | 是 | 源节点ID或名称 |
| `target` 或 `to_name` 或 `to` | 是 | 目标节点ID或名称 |

```bash
-a find-path -j '{"source": "林凡", "target": "苏瑶"}'
```

**返回**：`path`（边列表，表示从源到目标的最短路径）。使用 BFS，最大深度 5。未找到路径时返回空列表。

---

### list-nodes

**别名**：`列出节点`

| 参数 | 必填 | 说明 |
|------|------|------|
| `type` | 否 | 按节点类型过滤 |
| `tag` | 否 | 按标签过滤 |

```bash
-a list-nodes -j '{"type": "character"}'
```

**返回**：`nodes`（节点列表，含 id/type/name/tags/properties）。无过滤时返回全部节点。

---

### kg-stats

**别名**：`图谱统计`

| 参数 | 必填 | 说明 |
|------|------|------|
| 无 | — | — |

```bash
-a kg-stats
```

**返回**：`node_count`、`edge_count`、`node_types`（按类型计数字典）、`relation_types`（按关系类型计数字典）。

---

## 9. 实体提取

从文本中自动提取角色、地点、物品、事件等实体，由 `entity_extractor.EntityExtractor` 实现。

### extract-entities

**别名**：`提取实体`

| 参数 | 必填 | 说明 |
|------|------|------|
| `text` 或 `content` | 是 | 待提取文本（`content` 自动映射为 `text`；与 `text_file` 二选一） |
| `text_file` | 否 | 待提取文本文件路径 |
| `types` | 否 | 提取类型（逗号分隔，默认 `characters,locations,items,events`） |
| `genre` | 否 | 题材类型：`fantasy`/`urban`/`wuxia`/`scifi`（不指定则从项目配置读取，默认 `fantasy`） |

```bash
-a extract-entities -j '{"text": "林凡来到玄天峰，取出青锋剑，突破了筑基期。", "genre": "fantasy"}'
```

**返回**：`characters`（角色列表，含 name/confidence）、`locations`（地点列表）、`items`（物品列表）、`events`（事件列表，含 type/desc/confidence）、`new_entities`（未在知识图谱中出现的新实体列表）。提取策略含 jieba 分词词性标注、称谓模式匹配、对话归属识别、姓氏匹配，并支持题材自适应关键词集。

---

## 附录：参数重映射

部分命令支持参数别名，由 `PARAM_MAP` 自动转换：

| 命令 | 输入参数 | 映射为 |
|------|----------|--------|
| `extract-entities` | `content` | `text` |
| `resolve-hook` | `how` | `resolution` |
| `plant-hook` | `desc` | `description` |

此外，多个命令支持参数简写：

| 命令 | 简写参数 | 等同于 |
|------|----------|--------|
| `plant-hook` | `chapter` | `planted_chapter` |
| `abandon-chapter-hooks` | `chapter` | `planted_chapter` |
| `arc-progress` | `chapter` | `current_chapter` |
| `suggest-next` | `chapter` | `current_chapter` |
| `add-node` | `type` | `node_type` |
| `add-edge` | `from`/`to` | `source`/`target` |
| `create-phase` | `arc_id` | `phase_id` |
