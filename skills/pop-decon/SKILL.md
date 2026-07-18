---
name: pop-decon
description: "当用户说'拆书/解构/分析/对标/提取模板'时启用。拆书专家入口：初始化项目（量级+语言+源文件检查）、一次性路由建议（Phase 1→4），不常驻调度。"
---

# pop-decon · 拆书专家入口

> 拆书专家入口。初始化项目 + 一次性路由建议，不常驻调度。agent 按 skill description 自主判断调用子 skill。

## 红线

| # | 红线 |
|:-:|:-----|
| 1 | 读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具 |
| 2 | 不当每轮常驻调度；路由建议仅初始化时一次性给出，子 skill 调度由 agent 按 description 自主判断 |
| 3 | 不跳过 Phase — Phase 1 未完成不准进 Phase 2 |
| 4 | 产出物不经质量门禁直接进下一 Phase |
| 5 | 无源文件时先路由 tool-download-webnovel 下载，不得跳过 |
| 6 | 全管线完成不执行入库确认 |
| 7 | 不把"本次采用 skill"当合规证据；必须检查 scope 真实存在 |

## 强弱加载保障

- **强保障**：本 SKILL.md 由 host 层每次 run 强制注入
- **弱保障**：`steps/` + `references/` 需 agent 按 SKILL.md 指引主动 readFile

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 查初始化+路由操作 | `steps/step-1-pipeline.md` | 执行拆书时必读 |
| 查质量门禁标准 | `references/output-quality-standards.md` | 每个 Phase 完成后自检 |
| 查命名归一化 | `references/naming-normalization.md` | Phase 1 命名不一致时 |
| 查跨卷格式审计 | `references/format-consistency-audit.md` | 多卷拆解时 |
| 查delegate_task编排 | `references/delegation-orchestration.md` | ≥50章并行提取时 |
| 查小书Phase 2策略 | `references/small-book-phase2-strategy.md` | <100章时 |
| 查Wiki抓取策略 | `references/wiki-scraping-strategies.md` | 知名书Wiki骨架时 |
| 查数值体系反拆 | `references/numerical-system-reverse-engineering.md` | Phase 3扩展时 |

## 管线地图

```
用户: "拆这本书"
    ↓
pop-decon (初始化 + 一次性路由)
    ├── 检查源文件 → 无 → tool-download-webnovel 下载 → 有 ↓
    ├── 判断量级 + 语言
    ├── 一次性路由建议：Phase 1→4 顺序
    └── 退出，agent 按 description 自主调度子 skill

Phase 1: pop-decon-design-pack → 设计包v4
Phase 2: pop-decon-volume → L2单元卡 + 卷纲
Phase 3: pop-decon-setting → 设定层(L1六件套+弹性边界) + 角色层(金手指+人物卡+对白库) + 势力层 + 叙事资产层(伏笔追踪+场景拆解)
Phase 4: pop-decon-prd → 全书立项设计（含商业分析+连载规划+风险预警）
入库: pop-trope-library 四库
```

## 版本

v20.0.0 | 2026-07-18 | Phase 3 重构为四层（设定/角色/势力/叙事资产），新增伏笔追踪+对白风格库+经典场景拆解，世界宪法→弹性边界，起点快照/combat_capability降为可选
v19.0.0 | 2026-07-18 | 管线地图更新：Phase 3 新增 L1-07金手指设计 + 主要角色人物卡；Phase 4 从"全书立项PRD"升级为"全书立项设计"（含商业分析+连载规划+风险预警+启动检查清单）
v18.0.0 | 2026-07-06 | 改为初始化+一次性路由入口，补 PE 区块 → [CHANGELOG.md](CHANGELOG.md)
