# CHANGELOG — pop-novel-chapter-design

## v1.0.0 — 2026-06-09

### 初始版本：从 pop-novel-writer 拆出 Design 层

- **核心定位**：导演卡阶段——只做结构设计，不碰文风
- **输入**：Canvas（act-XX.yaml + 人物 + 地图 + 势力 + info-release + 里程碑）+ entity-snapshot
- **产出**：事实骨架.md + 登场人物卡.md + entity-snapshot 更新
- **7 步流程**：读入 Context → 事件链 → 角色调度 → 空间编排 → 信息释放 → 情绪节拍 → 产出
- **与 writer 的根本差异**：不知道文风DNA存在，不被风格规则约束设计决策
- **子 agent 架构**：由 expert-writer 派子 agent 独立执行
