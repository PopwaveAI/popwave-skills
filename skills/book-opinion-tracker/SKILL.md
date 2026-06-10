---
name: book-opinion-tracker
display_name: "网文舆情追踪"
category: research
scenario: research
mode: report
recommended: 8
tags: ["舆情", "调研", "报告", "追踪"]
pipeline:
  upstream: []
  downstream: []
fidelity: production
description: 网文舆情追踪 v1.8。输入书名扫8平台舆情，输出标准化舆情报告至 `.trae/archives/book-opinion-reports/`。v1.8对齐v3.3：报告与skill分离，仅保留模板于skill内。报告模板见 `舆情报告模板.md`。
version: 1.8.0
novel_agent_version: v3.3
dependencies:
  - cnovel-research (顶层 skill，提供平台采集能力矩阵。已从本包内移至 skills/cnovel-research/)
  - anysearch (搜索引擎，`tools/anysearch/`)
  - crawl4weibo (微博专用)
  - aiotieba (贴吧专用)

orchestration:
  preflight: []
  dependencies: ["cnovel-research"]
---