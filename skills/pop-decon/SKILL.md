---
name: pop-decon
description: "当用户说'拆书/解构/分析/对标/提取模板'时启用。拆书专家入口：下载txt→征询拆解范围+维度→路由到维度拆解skill（方案B联合Grep共享锚点池）。不常驻调度。"
---

# pop-decon · 拆书专家入口

> 拆书专家入口：下载 txt → 征询拆解范围+维度 → 路由（方案B 联合Grep共享锚点池）。不常驻调度。v24.1.0：死资产清理——旧ETL脚本包extractor+wiki残留references移至归档区（方案B现用dimension联合Grep直读原文）。

## 做什么

| 输入 | 输出 | 下游 |
|:-----|:-----|:-----|
| 用户拆书需求 + 源文件 | 征询拆解范围+维度 + 路由到 dimension（传 dims+scope） | pop-decon-dimension / pop-decon-prd |

## 路由地图（征询后按需调度）

```
用户: "拆这本书"
    ↓
pop-decon (下载 → 征询范围+维度 → 路由)
    ├── Step 0  下载txt（tool-download-webnovel）
    ├── Step 1  ★征询用户：拆什么范围？拆哪些维度？★
    ├── Step 2  路由到 pop-decon-dimension（传 dims=[维度列表] + scope=[章节范围]）
    ├── Step 3  pop-decon-dimension 联合Grep→共享锚点池→多维提取→分维度产出
    └── Step 4  沉淀 + 提醒"先用第一卷少测再拓展"

可拆解维度（pop-decon-dimension 联合Grep，共享精读）：
    ├── plot      剧情线（主线/支线/暗线/卷纲/转折）
    ├── romance   情感线（CP/暧昧/信任/背叛/羁绊演变）
    ├── character 人物角色（角色卡+弧线+动机+成长）
    ├── power     力量体系（力量/升级/战斗）
    ├── world     世界观（地理/历史/物种/势力/物品）
    ├── beat      爽点体验（名场面/读者体验/爽点分布）
    ├── style     文风（对白/笔触，场景定向采样，共享精读章）
    └── prd       全书立项设计（消费各维度产出）
```

## 怎么操作

> execution.mode: 按需路由（不固定全跑） | 强保障：本 SKILL.md 由 host 层每次 run 强制注入 | 弱保障：steps/ + references/ 需 agent 主动 readFile

### 入口流程 → `steps/step-1-pipeline.md`
懒加载：源文件检查 → 下载 → 征询拆解范围+维度 → 按需路由到 pop-decon-dimension → 沉淀确认

## 🚪 首次对话引导（onboarding）

> 用户第一次触发拆书专家（无任何拆书项目、非续写场景）时，**先输出 `references/onboarding-guide.md` 的引导语内容**给用户建立认知，再进入 Step 0 下载。
>
> 展示方式：在回复中**直接粘贴 `references/onboarding-guide.md` 全文**（声明本次为功能介绍+引导、未执行 skill 任务），用 1-2 句口头补充"报书名+想学那块就开始"。若用户已明确要拆，可跳过引导直接干活。

## 📦 可调度 Skill 清单（素材表）

> 本拆书专家入口与调度器，可调度的子 skill 总清单如下（与 `skill.json` 的 `skills` 数组一致）。维度拆解统一走 `pop-decon-dimension`。

| Skill | 定位 | 何时调用 |
|:--|:--|:--|
| `tool-download-webnovel` | 下载源书 txt | Step 0 |
| `pop-decon-dimension` | 维度拆解（7 维度合一，直读原文） | 征询后按需（传维度参数） |
| `pop-decon-design-pack` | 白描卡（可选加速器，非必选） | 需快速全书骨架时 |
| `pop-decon-prd` | 全书立项设计（消费各维度产出） | 征询后按需 |

## 红线

1. **读取协议**：读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具
2. **未征询就全量跑** — 必须先征询用户要拆哪些维度，只跑被选中的，禁止默认全量跑
3. **跳过原文直读** — 方案B 默认直读原文，不得要求先产白描卡（白描卡仅可选加速器）
4. 产出物不经质量门禁直接进下一级
5. 无源文件时先路由 tool-download-webnovel 下载，不得跳过
6. 产出沉淀到项目本地文件夹，不入库 pop-trope-library
7. **未提醒少测即切入全书** — 拆书启动时必须提醒用户"建议先用第一卷少量测试再拓展全书"

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:-----|:----------|:----------|
| `steps/step-1-pipeline.md` | 执行拆书时必读 | 下载→征询→路由流程 |
| `references/维度路由清单.md` | 征询用户拆什么时 | 各维度+触发词+路由到 dimension |
| `references/output-quality-standards.md` | 每个维度完成后自检 | 质量门禁标准 |
| `references/delegation-orchestration.md` | ≥50章并行提取时 | delegate_task 编排策略 |
| `references/small-book-phase2-strategy.md` | <100章时 | 小书拆解策略 |

## 版本

v24.1.0 | 2026-08-18
- **死资产清理**：scripts/extractor全家族+extract*.py+wiki残留references（6文件）移至 _archive/pop-decon/
v24.0.0 | 2026-08-13 | 方案B 重构：增加scope征询，改为一次性传入所有维度，dimension 联合Grep+多维提取 → [CHANGELOG.md](CHANGELOG.md)
