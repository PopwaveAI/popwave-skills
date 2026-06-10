# CHANGELOG — pop-novel-prose-render

## v1.0.0 — 2026-06-09

### 初始版本：从 pop-novel-writer 拆出 Render 层

- **核心定位**：正文渲染阶段——只做风格表达，不验证剧情
- **输入**：事实骨架 + 登场人物卡 + 文风DNA + 锚定章
- **产出**：chXXX.md 完成正文
- **三阶段渲染**：风格锚定 → 逐事件渲染 → 风格验证
- **与 writer 的根本差异**：不读 Canvas/L1，不判断剧情逻辑是否合理
- **子 agent 架构**：由 expert-writer 派子 agent 独立执行
