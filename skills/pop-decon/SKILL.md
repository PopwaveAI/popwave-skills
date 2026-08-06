---
name: pop-decon
description: "当用户说'拆书/解构/分析/对标/提取模板'时启用。拆书专家入口：下载txt→章节白描→征询用户要拆哪些维度→按需路由到对应拆解skill。不常驻调度。"
---

# pop-decon · 拆书专家入口

> 拆书专家入口：下载 txt → 章节白描 → 征询拆解维度 → 按需路由。不常驻调度。v22.0.0

## 做什么

| 输入 | 输出 | 下游 |
|:-----|:-----|:-----|
| 用户拆书需求 + 源文件 | 白描资产 + 征询拆解维度 + 按需路由到维度skill | plot/romance/character/power/world/beat/style/prd |

## 路由地图（征询后按需调度）

```
用户: "拆这本书"
    ↓
pop-decon (下载 → 白描 → 征询维度 → 路由)
    ├── Step 0  下载txt（tool-download-webnovel）
    ├── Step 1  章节白描（统一底层资产，子agent双模式）
    ├── Step 2  ★征询用户：要拆哪些维度？★（多选）
    ├── Step 3  按需路由到被选中的维度skill
    └── Step 4  沉淀 + 提醒"先用第一卷少测再拓展"

可拆解维度（独立skill，按需调用）：
    ├── pop-decon-plot      剧情线（主线/支线/暗线/卷纲/转折）
    ├── pop-decon-romance   情感线（CP/暧昧/信任/背叛/羁绊演变）★
    ├── pop-decon-character 人物角色（角色卡+弧线+动机+成长）
    ├── pop-decon-power     力量体系（力量/升级/战斗）
    ├── pop-decon-world     世界观（地理/历史/物种/势力/物品）
    ├── pop-decon-beat      爽点体验（名场面/读者体验/爽点分布）
    ├── pop-decon-style     文风（对白/笔触，对接pop-shared-dna）
    └── pop-decon-prd       全书立项设计（消费各维度产出）
```

## 怎么操作

> execution.mode: 按需路由（不固定全跑） | 强保障：本 SKILL.md 由 host 层每次 run 强制注入 | 弱保障：steps/ + references/ 需 agent 主动 readFile

### 入口流程 → `steps/step-1-pipeline.md`
懒加载：源文件检查 → 下载 → 章节白描 → 征询拆解维度 → 按需路由 → 沉淀确认

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **未征询就全量跑** — 必须先征询用户要拆哪些维度，只跑被选中的，禁止默认全量跑
3. 不跳过白描 — 白描是各维度拆解的底层资产，维度拆解前必须已有白描
4. 产出物不经质量门禁直接进下一级
5. 无源文件时先路由 tool-download-webnovel 下载，不得跳过
6. 产出沉淀到项目本地文件夹，不入库 pop-trope-library
7. **未提醒少测即切入全书** — 拆书启动时必须提醒用户"建议先用第一卷少量测试再拓展全书"

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-pipeline.md` | 执行拆书时必读 | 下载→白描→征询→路由流程 |
| `references/维度路由清单.md` | 征询用户拆什么时 | 各维度skill+触发词+白描深度 |
| `references/output-quality-standards.md` | 每个维度完成后自检 | 质量门禁标准 |
| `references/delegation-orchestration.md` | ≥50章并行提取时 | delegate_task 编排策略 |
| `references/small-book-phase2-strategy.md` | <100章时 | 小书拆解策略 |

## 版本

v22.0.0 | 2026-08-06 | 重构：从「固定Phase 1→4全量跑」改为「下载→白描→征询拆解维度→按需路由」。拆解维度拆分为独立skill（plot/romance/character/power/world/beat/style），新增情感线skill → [CHANGELOG.md](CHANGELOG.md)