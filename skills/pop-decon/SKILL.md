---
name: pop-decon
description: "当用户说'拆书/解构/分析/对标/提取模板'时启用。拆书专家入口：初始化项目（量级+语言+源文件检查）、一次性路由建议（Phase 1→4），不常驻调度。"
---

# pop-decon · 拆书专家入口

> 拆书专家入口，初始化项目 + 一次性路由建议，不常驻调度。v20.2.0

## 做什么

| 输入 | 输出 | 下游 |
|:-----|:-----|:-----|
| 用户拆书需求 + 源文件 | 一次性路由建议（Phase 1→4） | design-pack → volume → setting → prd |

## 怎么操作

> execution.mode: 一次性路由 | 强保障：本 SKILL.md 由 host 层每次 run 强制注入 | 弱保障：steps/ + references/ 需 agent 主动 readFile

### 初始化+路由 → `steps/step-1-pipeline.md`
检查源文件 → 判断量级+语言 → 一次性路由建议 → 退出，agent 按 description 自主调度子 skill

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. 不当每轮常驻调度；路由建议仅初始化时一次性给出，子 skill 调度由 agent 按 description 自主判断
3. 不跳过 Phase — Phase 1 未完成不准进 Phase 2
4. 产出物不经质量门禁直接进下一 Phase
5. 无源文件时先路由 tool-download-webnovel 下载，不得跳过
6. 产出沉淀到项目本地文件夹，不入库 pop-trope-library
7. 不把"本次采用 skill"当合规证据；必须检查 scope 真实存在

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-pipeline.md` | 执行拆书时必读 | 初始化+路由操作流程 |
| `references/output-quality-standards.md` | 每个 Phase 完成后自检 | 质量门禁标准 |
| `references/naming-normalization.md` | Phase 1 命名不一致时 | 命名归一化规则 |
| `references/format-consistency-audit.md` | 多卷拆解时 | 跨卷格式审计 |
| `references/delegation-orchestration.md` | ≥50章并行提取时 | delegate_task 编排策略 |
| `references/small-book-phase2-strategy.md` | <100章时 | 小书 Phase 2 策略 |
| `references/wiki-scraping-strategies.md` | 知名书 Wiki 骨架时 | Wiki 抓取策略 |
| `references/numerical-system-reverse-engineering.md` | Phase 3 扩展时 | 数值体系反拆 |
| `references/iceberg-theory.md` | 理解拆书方法论时 | 冰山理论参考 |
| `templates/wiki-skeleton.tpl.md` | 知名书 Wiki 骨架时 | Wiki 骨架模板 |

## 管线地图

```
用户: "拆这本书"
    ↓
pop-decon (初始化 + 一次性路由)
    ├── 检查源文件 → 无 → tool-download-webnovel 下载
    ├── 判断量级 + 语言
    ├── 一次性路由建议：Phase 1→4 顺序
    └── 退出，agent 按 description 自主调度子 skill

Phase 1: pop-decon-design-pack → 设计包v4
Phase 2: pop-decon-volume → L2单元卡 + 卷纲
Phase 3: pop-decon-setting → 设定层+角色层+势力层+叙事资产层
Phase 4: pop-decon-prd → 全书立项设计
沉淀: 项目本地文件夹（不入库 pop-trope-library）
```

## 版本

v20.2.0 | 2026-07-22 | 按规范重写 SKILL.md：补全做什么/怎么操作/强弱加载声明，速查表改为全文件目录引导，版本只留最新 → [CHANGELOG.md](CHANGELOG.md)
