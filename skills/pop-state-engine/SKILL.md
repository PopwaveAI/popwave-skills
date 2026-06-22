# pop-state-engine

> Popwave 写作管线的运行时状态引擎。SQLite 驱动的叙事状态管理，解决长篇项目的设定全量加载、涌现实体无处登记、身份与状态混合三个结构性问题。

## 引擎是什么

一个 SQLite 数据库 + 11 个 Python 脚本，提供 47 条 CLI 命令，覆盖：

- **场景存储** — 设计包入库 + FTS5 全文索引 + 6 级分层摘要
- **事实管理** — 3 级重要性 + superseded_by 版本链 + 矛盾检测
- **知识图谱** — 节点/边/路径 + 实体提取辅助
- **伏笔追踪** — plant/resolve/abandon + 超期/遗忘检测
- **弧线管理** — phases/arcs/progress + 下一步建议
- **上下文组装** — 6 级递进检索，自动裁剪到目标 token 预算

## 引擎不是什么

- 不写正文（prose 的职责）
- 不做角色建模（character_simulator 未迁移）
- 不做质量审计（quality_auditor 未迁移）
- 不做连续性检查（continuity_checker 未迁移）
- 不做风格学习（style_learner 未迁移）
- 不做情节分支（plot_brancher 未迁移）
- 不写总控文件（expert-writer step-3-reflect 的职责）

## CLI 调用方式

```bash
python scripts/command_executor.py -p {项目路径} -a {动作} -j '{JSON参数}'
```

示例：

```bash
# 初始化引擎
python scripts/command_executor.py -p /path/to/project -a init -j '{"title":"我的小说","genre":"玄幻"}'

# 存储设计包
python scripts/command_executor.py -p /path/to/project -a store-chapter -j '{"chapter":1,"content":"...","characters":"李明"}'

# 查询上下文
python scripts/command_executor.py -p /path/to/project -a for-creation -j '{"chapter":5}'

# 项目状态聚合
python scripts/command_executor.py -p /path/to/project -a project-status
```

## 4 层查询路径

| 层级 | 命令 | 用途 | 何时用 |
|------|------|------|--------|
| L0 | `for-creation` | 自动组装上下文包 | 每章设计/写作前 |
| L1 | `catalog` | 运行时 DB 自描述 | 不确定有什么数据时 |
| L2 | `help --topic {类别}` | 按类别浏览命令 | 不确定用什么命令时 |
| L3 | `get-fact` / `find-node` / `list-hooks` 等 | 精确查询单条数据 | 知道要查什么时 |

### L0: for-creation — 自动上下文包

```bash
python scripts/command_executor.py -p {项目} -a for-creation -j '{"chapter": 5}'
```

返回 JSON 包含：book_summary → volume_summary → arc_summary → recent_summaries → active_entities → active_facts → open_hooks → continuity_notes。自动裁剪到 ~5-8KB。

### L1: catalog — 运行时自描述

```bash
python scripts/command_executor.py -p {项目} -a catalog
```

返回 JSON 包含：9 张表的描述 + 行数 + 样本数据 + 分组统计 + 7 条快捷查询。

### L2: help — 命令浏览

```bash
python scripts/command_executor.py -p {项目} -a help
python scripts/command_executor.py -p {项目} -a help -j '{"topic": "伏笔追踪"}'
```

8 个类别：系统 / 初始化 / 存储 / 查询 / 事实管理 / 伏笔追踪 / 弧线管理 / 上下文。

### L3: 精确查询

```bash
# 查事实
python scripts/command_executor.py -p {项目} -a get-fact -j '{"entity":"李明","attribute":"修为"}'

# 查节点
python scripts/command_executor.py -p {项目} -a find-node -j '{"name":"李明"}'

# 查伏笔
python scripts/command_executor.py -p {项目} -a list-hooks
```

## 何时调用引擎

| 触发点 | 调用方 | 命令 | 说明 |
|--------|--------|------|------|
| 建世界后 | pop-writer-world | `add-node` × N + `set-fact` × N + `store-summary` | L1 设定入库 |
| 每卷开始 | pop-writer-plot | `create-arc` + `store-summary` + `plant-hook` | 卷弧线+伏笔种入 |
| 每章设计时 | pop-writer-chapter | `for-creation` | 替代全量加载 |
| 每章写完后 | pop-writer-prose | `store-chapter` + `add-node` + `set-fact` + `resolve-hook` | 章末5步登记 |
| 储备卡产出后 | pop-writer-reservoir | `add-node` + `set-fact` | 储备卡注册 |
| 每次 skill 执行后 | expert-writer | `project-status` | 总控进度锚点同步 |

## 数据库结构

9 张表，全部以 `pop_` 为前缀：

| 表 | 说明 | 关键字段 |
|----|------|---------|
| `pop_scenes_content` | 场景内容（设计包入库） | chapter, content, tags, characters, location |
| `pop_scenes` | FTS5 全文索引（自动同步） | content, tags, chapter, characters |
| `pop_embeddings` | ONNX 语义向量（可选） | scene_id, embedding |
| `pop_summaries` | 6 级分层摘要 | level, range_desc, content |
| `pop_facts` | 事实表（3级重要性+版本链） | entity, attribute, value, importance, superseded_by |
| `pop_kg_nodes` | 知识图谱节点 | type, name, tags, properties |
| `pop_kg_edges` | 知识图谱边 | source, target, relation |
| `pop_hooks` | 伏笔追踪 | desc, status, priority, planted_chapter, expected_resolve |
| `pop_arcs` | 弧线/阶段 | title, arc_type, start_chapter, end_chapter |

## 依赖

- **Python 3.10+**
- **jieba**（已 vendor 到 `scripts/jieba/`）— 用于 entity_extractor 词性标注，无需 pip install
- **onnxruntime**（可选）— 语义向量检索，未安装时跳过 embedding 相关功能

## FTS5 搜索方案

引擎使用 **bigram（双字）分词** 而非 jieba 分词进行 FTS5 索引：

- **索引时**：`"碎骨指功法"` → `"碎骨 骨指 指功 功法"`（bigrams 以空格分隔）
- **查询时**：`"碎骨指"` → `"碎骨 AND 骨指"`（bigrams 用 AND 连接 ≈ 子串匹配）
- **多词搜索**：`"李明 碎骨指"` → `"李明 OR 碎骨 AND 骨指"`（词间 OR，词内 AND）

bigram 是 CJK 搜索的标准技术，优势：
- 零依赖（FTS5 搜索不依赖 jieba）
- 索引和查询使用相同算法，保证一致性
- AND 匹配 bigrams ≈ 子串匹配，精度高
- 不会因分词不一致导致漏匹配

## 文件结构

```
pop-state-engine/
├── SKILL.md                    ← 本文件
├── skill.json                  ← skill 元数据
├── CHANGELOG.md                ← 版本记录
├── scripts/
│   ├── command_executor.py     ← 统一命令入口（589行）
│   ├── project_initializer.py  ← 项目初始化
│   ├── memory_engine.py        ← 场景存储 + FTS5(bigram) + 摘要
│   ├── fact_engine.py          ← 事实管理 + 版本链
│   ├── knowledge_graph.py      ← 知识图谱
│   ├── hook_tracker.py         ← 伏笔追踪
│   ├── arc_manager.py          ← 弧线管理
│   ├── context_retriever.py    ← 上下文组装
│   ├── entity_extractor.py     ← 实体提取（jieba POS）
│   ├── semantic_model.py       ← ONNX 语义模型
│   ├── dashboard_generator.py  ← HTML 仪表盘生成
│   └── jieba/                  ← vendor 的 jieba 分词库（18.6MB）
└── references/
    ├── cli-reference.md        ← 全部命令参数说明
    └── integration-guide.md    ← skill 接入指南
```

## 版本

v0.1.0 — 初始版本，从 OnKos v2 改编而来。
