# Phase r2：逆向提取 — L0 产品层

## 前置条件
Phase r1 全部完成（全本事件日志 + 批次摘要齐全）。

## 加载参考
先加载 `phases/phase-0.ref.md`，了解 PRD 六要素结构和压力测试标准。

## 执行步骤

### 1. 从事件日志提取
基于全本事件日志 + 批次摘要，提炼：
- **一句话卖点**：这本书到底卖什么
- **核心爽点类型**：打脸/获得/升级/守护/复仇/解谜，各占多少比例
- **目标读者定位**：谁在看这本书
- **reader_profile**：平台/性别/年龄/阅读习惯/读者期望

### 2. 产出
- `00-原始设定/L0-产品层/PRD.md`（按 phase-0.ref.md 的六要素结构）
- 在 project.yaml 中嵌入 reader_profile 字段

### 3. 用户确认
PRD 和 reader_profile 必须用户点头，不可跳过。

## 产出
- `00-原始设定/L0-产品层/PRD.md`
- `project.yaml`（含 reader_profile）

## 检查清单
- [ ] 一句话卖点从正文数据出发，不是凭空想象
- [ ] 爽点类型分布有事件日志支撑
- [ ] reader_profile 已嵌入 project.yaml
