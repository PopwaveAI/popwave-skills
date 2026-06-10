---
name: knowledge-downloader
pipeline:
  upstream: []
  downstream: []
display_name: "知识获取器 — 微信文章 + B站视频"
category: content-acquisition
scenario: analyze
mode: batch
recommended: 8
tags: ["微信", "公众号", "B站", "视频字幕", "文章下载", "OCR", "内容拆解", "价值提炼"]
fidelity: production
description: 统一的知识内容获取工具。支持两大数据源：微信公众号文章（CDP 操控 Chrome 下载）和 B 站视频（API 获取字幕）。下载后自动进入 Phase B 拆解阶段，按标准模板产出结构化拆解报告。依赖 web-access skill 进行微信下载。
---