# CHANGELOG — pop-decon-clean

## v1.0.0 — 2026-06-15

### 初始版本

- **定位**：Phase 1 of deconstruction pipeline：原始 TXT → 逐章清洗 → 逐章 JSON
- **四步流程**：ETL (extract.py) → 按章拆分 → LLM 逐章清洗 → 逐章结构化 JSON
- **6 条质量红线**：覆盖 ETL 前置校验、跳步拆分、广告混入、章序号混乱、JSON 无数据、产出只留摘要
- **完整落盘检查点**：metadata.json / chapters/chXXX.txt / chapter-data/chXXX.json
- **边界条件**：空文件、无规律标题、非法字符、超长章节、非 TXT 输入
