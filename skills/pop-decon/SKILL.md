---
name: pop-decon
description: "当用户说'拆书/解构/分析/对标/提取模板'时启用。拆书管线orchestrator，调度Phase 1→4产出入库pop-trope-library。"
---

# pop-decon · 拆书管线调度

> 拆书管线元 skill。执行管线调度（Phase 1→4），不直接产出文件。

## ❌ 质量红线

| # | 红线 |
|:-:|:-----|
| ❌1 | **读取 skill 文件禁止用 Read 工具** — 用 `Get-Content -Encoding UTF8 -Raw`，Read 有行数限制会截断 |
| ❌2 | **不跳过 Phase** — 顺次推进 Phase 1→2→3→4，Phase 1 未完成不准进 Phase 2 |
| ❌3 | **产出物不经质量门禁直接进下一 Phase** — 每个 Phase 产出必须对照质量标准自检 |
| ❌4 | **全管线完成不执行入库确认** — Phase 1~4 全部跑完后必须逐模块确认入库 pop-trope-library |

## 强弱加载保障

- **强保障**：本 SKILL.md 由 host 层每次 run 强制注入
- **弱保障**：`steps/` + `references/` 需 agent 按 SKILL.md 指引主动 readFile

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 查管线操作步骤 | `steps/step-1-pipeline.md` | 执行拆书时必读 |
| 查冰山理论哲学 | `references/iceberg-theory.md` | 理解拆书设计理念时 |
| 查质量门禁标准 | `references/output-quality-standards.md` | 每个 Phase 完成后自检 |
| 查命名归一化操作 | `references/naming-normalization.md` | Phase 1 命名不一致时 |
| 查跨卷格式审计 | `references/format-consistency-audit.md` | 多卷拆解时 |
| 查delegate_task编排 | `references/delegation-orchestration.md` | ≥50章并行提取时 |
| 查小书Phase 2策略 | `references/small-book-phase2-strategy.md` | <100章时 |
| 查Wiki抓取策略 | `references/wiki-scraping-strategies.md` | 知名书Wiki骨架时 |
| 查Wiki注入案例 | `references/wiki-injection-case-study.md` | Wiki注入参考时 |
| 查数值体系反拆 | `references/numerical-system-reverse-engineering.md` | Phase 3扩展时 |
| 填Wiki骨架模板 | `templates/wiki-skeleton.tpl.md` | 产出Wiki骨架时 |

## 管线地图

```
用户: "拆这本书"
    ↓
pop-decon (orchestrator)
    ├── 判断量级: 前N章 or 全书
    │   └── 判断语言: 中文 → 手动 ETL；英文 → extract.py
    ├── Phase 1: pop-decon-design-pack → 设计包v4
    │   └── 质量门禁 + 命名归一化
    ├── Phase 1.5 (可选): Wiki骨架
    ├── Phase 2: pop-decon-volume → L2单元卡 + 卷纲（含溯源燃料台）
    ├── Phase 3: pop-decon-setting → L1六件套 + 宪法 + 数值
    ├── Phase 4: pop-decon-prd → 全书立项PRD
    └── Step 6: 入库确认 → pop-trope-library 四库
```

## 版本

v17.0.0 | 2026-07-01 | 按v6.0.0规范重构 → [CHANGELOG.md](CHANGELOG.md)
