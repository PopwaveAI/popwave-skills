# POP-ROUTER.md — pop 编排路由表

> pop 收到需求后，根据用户意图通过路由表匹配子 skill。
> 本文件为静态参考。实际路由在 SKILL.md 中由 pop agent 根据 Think→Execute 流程执行。

---

## 一、路由总表

| 用户意图 | 路由 skill | 前置条件 | 产出 |
|:---------|:-----------|:---------|:-----|
| 新书启动 / 开书 / 设世界观 | `pop-novel-bookstrap` (forward) | 一个故事想象 | story-engine.yaml + L1 设定 + 宪法 + 数值体系 + 起点快照 + 终点快照 |
| 设计幕纲 / 剧情架构 | `pop-writer-plot` | project.yaml + story-engine.yaml + L1 设定 | act-XX.yaml（含M1/M2/M3+里程碑） |
| 写正文 / 下一章 | `pop-writer-chapter` → `pop-writer-prose` | act-XX.yaml + L1 设定 + 宪法 + 章状态 | 设计包.md + chXXX.md |
| 拆书 / 分析参考书 | `pop-decon` | 参考书原文 | 模式分析报告+卷1起点/终点快照 |
| 审稿 / QA / 质检 | `pop-writer-qa` | 正文 MD | QA 报告 |
| HTML化 / 发布 | `pop-writer-html` | 任意文档 | 可视化 HTML |
| 续写 / 交接已有项目 | `pop-novel-bookstrap` (reverse) | 已有正文 | event logs + 逆向 L1 + 宪法 |

---

## 二、关键词 → 路由映射

| 用户输入包含 | 路由 skill |
|:---|:---|
| 开书 / 启动 / 新书 / 设定 | `pop-novel-bookstrap` (forward) |
| 幕纲 / 大纲 / 剧情 / 架构 | `pop-writer-plot` |
| 写 / 正文 / 第N章 / 下一章 | `pop-writer-chapter` → `pop-writer-prose` |
| 拆书 / 解构 / 分析 / 对标 | `pop-decon` |
| 审稿 / QA / 质检 / 审一下 | `pop-writer-qa` |
| HTML化 / 发布 / 渲染 | `pop-writer-html` |
| 续写 / 交接 / 已有正文 | `pop-novel-bookstrap` (reverse) |
