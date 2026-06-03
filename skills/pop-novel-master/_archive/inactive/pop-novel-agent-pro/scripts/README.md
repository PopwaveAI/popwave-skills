# scripts — 工具脚本（待整理）

> ⚠️ **状态**：PRD v6 重构中，部分脚本将迁移至 `engine/` 或 `skills/`

## 当前脚本清单

| 脚本 | 用途 | 计划去向 |
|------|------|----------|
| `auto_fragment.py` | 自动场景分片 | 待评估 |
| `fragment_searcher.py` | 片段搜索 | 待评估 |
| `hybrid_search.py` | 混合搜索（语义+关键词）| engine/pipeline/ |
| `semantic_searcher.py` | 语义搜索 | 待评估 |
| `reference_engine.py` | 引用引擎 | 待评估 |
| `tag_chapters.py` | 章节标签化 | 待评估 |
| `text_normalizer.py` | 文本规范化 | engine/pipeline/ |
| `ingest_to_db.py` | 数据导入通用脚本 | data/ 或 engine/ |
| `ingest_huijin.py` | 灰骑士数据导入 | 项目专属，待归档 |
| `ingest_shoumo_horror.py` | 狩魔猎人数据导入 | 项目专属，待归档 |

## ARCHIVED/

已归档的旧版本和临时文件：
- RAG 原型 v1-v5
- 章节中间文件 (_chXXX_segments.md)
- 旧版正文草稿 (_v2chXXX.txt)

## 使用建议

新开发优先使用 `engine/pipeline/` 中的标准化工具。
