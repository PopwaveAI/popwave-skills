# Phase r2：逆向提取 — 故事引擎

## 前置条件
Phase r1 全部完成（全本事件日志 + 批次摘要齐全）。

## 加载参考
先加载 `phases/phase-0.pe.md`，了解 story-engine.yaml 的 schema。

## 执行步骤

### 1. 从事件日志提取 engine
基于全本事件日志 + 批次摘要，提炼：
- **core_premise**：这本书到底卖什么，一句话概括
- **核心冲突类型**：战斗/解谜/生存/种田/复仇/守护/探索，各占多少比例
- **世-界定位**：power_tier 落在哪个区间
- **reader_profile**：平台/性别/年龄/阅读习惯/读者期望

### 2. 产出
`00-原始设定/L0-产品层/story-engine.yaml`（按 phase-0.pe.md 的 schema）
在 project.yaml 中嵌入 reader_profile 字段

### 3. 用户确认
story-engine.yaml 和 reader_profile 必须用户点头，不可跳过。

## 产出
- `00-原始设定/L0-产品层/story-engine.yaml`
- `project.yaml`（含 reader_profile）

## 检查清单
- [ ] core_premise 从正文数据出发，不是凭空想象
- [ ] 冲突类型分布有事件日志支撑
- [ ] reader_profile 已嵌入 project.yaml
