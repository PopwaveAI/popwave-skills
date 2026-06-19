# 拆书专家全链路依赖图 — 文件依赖与产出全景

> 版本：v1.0 | 2026-06-19
> 基于各 skill 当前 SKILL.md 的 pipeline 字段现状构建。
> 写作专家见 `01-写作专家全链路依赖图-PRD.md`。

---

## 拆书专家管线顺序（硬性）

```
download → decon(orchestrator) → design-pack(Phase1) → volume(Phase2) → setting(Phase3) → trace(Phase4)
                                                                                         ↓（可选）
                                                                                    pop-shared-dna → prose-render
```

| 标记 | 含义 |
|:----:|:------|
| ✅ | 已完成 |
| ⬜ | 未开始 |
| ❌ | 阻塞 |

---

## 一、拆书专家架构总览

### 1.1 拆书专家 skill 清单

| Skill | 版本 | 定位 |
|:------|:----:|:------|
| **tool-download-webnovel** | v2.0.1 | TXT 直链下载。搜直链→下直链，不爬目录页 |
| **pop-decon** | v13.8.0 | 管线调度中枢(orchestrator)。按 scope（前N章/全书）路由到子阶段 |
| **pop-decon-design-pack** | v3.0.0 | Phase 1：章节设计包提取。ETL → 分章 → 4层精度设计包 |
| **pop-decon-volume** | v2.1.0 | Phase 2：卷/幕纲。识别卷边界、幕边界、剧情线、契诃夫枪链 |
| **pop-decon-setting** | v1.1.0 | Phase 3：设定世界观。L1六件套 + 宪法 + 战力 |
| **pop-decon-trace** | — | Phase 4：创作溯源（forthcoming）|
| **pop-shared-dna** | v4.0.3 | 文风DNA蒸馏。下游→pop-writer-prose |
| **pop-shared-reader** | v0.15.0 | 独立拆书阅读器。产出叙事笔记+结构化数据→pop-shared-html |

### 1.2 拆书专家全链路

```
┌─────────────────────────────────────────────────────┐
│           tool-download-webnovel v2.0.1              │
│  搜直链 → 下载 → 质检                               │
│  → 产出: {书名}.txt                                 │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────┐
│  pop-decon v13.8.0 (Orchestrator)                    │
│  按 scope 路由: 前N章(快速) / 全书(全量)             │
│  → 产出: 路由决策 + 各阶段调度                       │
└──────┬──────────────────────────────────────────────┘
       │
       ▼ (Phase 1)
┌─────────────────────────────────────────────────────┐
│  pop-decon-design-pack v3.0.0                        │
│  ETL → 分章 → 每章 v3 设计包 (4层精度)             │
│  → 产出: chXXX-设计包.md xN                          │
└──────────────────────┬──────────────────────────────┘
                       ▼ (Phase 2)
┌─────────────────────────────────────────────────────┐
│  pop-decon-volume v2.1.0                             │
│  卷边界 → 幕边界 → 剧情线 → 契诃夫枪链              │
│  → 产出: 幕纲.md + 卷纲.md + Canvas矩阵              │
└──────────────────────┬──────────────────────────────┘
                       ▼ (Phase 3)
┌─────────────────────────────────────────────────────┐
│  pop-decon-setting v1.1.0                            │
│  L1六件套 + 世界宪法 + 战力数值                      │
│  → 产出: L1-01~06 + 世界宪法 + 战力体系              │
└──────────────────────┬──────────────────────────────┘
                       ▼ (Phase 4 - forthcoming)
┌─────────────────────────────────────────────────────┐
│  pop-decon-trace                                     │
│  创作溯源追踪                                        │
└──────────────────────┬──────────────────────────────┘
                       ▼（可选）
┌─────────────────────────────────────────────────────┐
│  pop-shared-dna v4.0.3                               │
│  文风DNA蒸馏 (从 >=20 章均匀采样)                   │
│  → 产出: 写作资产/文风DNA/{书名}.md                 │
│  → 下游: pop-writer-prose                            │
└─────────────────────────────────────────────────────┘
```

### 1.3 与写作专家的交互关系

```
拆书专家产出                    ->       写作专家消费
  设计包 + 卷纲 + 幕纲           pop-writer-creative（PRD/引擎参考）
  Lv4-主角参考卡                 pop-writer-creative（主角设计参考）
  卷起终点快照                   pop-writer-creative（节奏参考）
  文风DNA                       pop-writer-prose（风格渲染）
  T1/T2/T3（力量/世界观/角色）    pop-writer-world（L1设定参考）
```

写作专家 **不依赖** 拆书专家——没有拆书产出时使用默认节奏兜底。
拆书专家 **不消费** 写作专家——独立运行。

---

## 二、Skill 管线流程

### 2.1 拆书专家：参考书拆解

```
用户说"拆解这本书"
  |
  ▼
Step 0 - expert-writer 全局感知
  -> 读取 workspace-index.yaml -> 检查 _参考书/{书名}/ 下是否有已有产出
  -> 若无 -> 路由到 tool-download-webnovel
  |
Step 1 - tool-download-webnovel
  -> 搜索直链 -> 下载 -> 质检 -> {书名}.txt
  |
Step 2 - pop-decon (orchestrator)
  |- Phase 1: pop-decon-design-pack
  |   ETL -> 分章 -> 每章 v3 设计包（4层：骨架+释放+角色+感官）
  |   -> 产出: chXXX-设计包.md xN
  |- Phase 2: pop-decon-volume
  |   卷边界 -> 幕边界 -> 反推剧情线 -> 契诃夫枪链
  |   -> 产出: 幕纲.md + 卷纲.md + Canvas矩阵
  |- Phase 3: pop-decon-setting
  |   L1六件套 + 世界宪法 + 战力数值
  |   -> 产出: L1-01~06 + 世界宪法 + 战力体系
  +- Phase 4: pop-decon-trace（forthcoming）
      创作溯源追踪
  |（可选）
Step 3 - pop-shared-dna
  -> 从 >=20 章均匀采样 -> 全书搜索验证
  -> 产出: 写作资产/文风DNA/{书名}.md -> 供 prose-render 消费
```

---

## 三、各 Skill 详细文件依赖表

### 3.1 tool-download-webnovel v2.0.1

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:-----------|
| 搜索 | 书名 | 搜索结果 | 下载 |
| 下载 | 搜索结果 | `{书名}.txt` | pop-decon |

### 3.2 pop-decon v13.8.0（管线调度中枢）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:-----------|
| 路由决策 | {书名}.txt + scope(前N章/全书) | 阶段规划 | decon-design-pack / volume / setting / trace |

### 3.3 pop-decon-design-pack v3.0.0（Phase 1）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:-----------|
| ETL | {书名}.txt | 结构化章节数据 | 分章 |
| 分章 | 结构化数据 | 逐章原始数据 | 设计包提取 |
| 4层设计包 | 逐章数据 + 模板 | `chXXX-设计包.md` xN | pop-decon-volume |

4层精度：skeleton（骨架） + payoff（释放） + character（角色） + sensory（感官）

### 3.4 pop-decon-volume v2.1.0（Phase 2）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:-----------|
| 卷边界识别 | 设计包 chXXX 数据 | 卷划分 | 幕边界、剧情线 |
| 幕边界识别 | 卷划分 | 幕划分 | 剧情线 |
| 剧情线反推 | 卷/幕划分 | 剧情线文档 | 契诃夫枪链 |
| 契诃夫枪链 | 剧情线 | chekhov-tracker | pop-decon-setting |

### 3.5 pop-decon-setting v1.1.0（Phase 3）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:-----------|
| L1 六件套 | 设计包 + 卷/幕数据 | `L1-01~06.md` | world（写作专家）|
| 世界宪法 | L1 六件套 | `世界宪法.md` | world |
| 战力数值 | L1 力量体系 | `战力体系.md` | world |

### 3.6 pop-decon-trace（Phase 4 - forthcoming）

创作溯源追踪。从章节数据反向追查作者的 craft recipe 和叙事策略。

### 3.7 pop-shared-dna v4.0.3（文风DNA蒸馏）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:-----------|
| 采样（>=20章） | 设计包 + 章节数据 | 采样数据集 | 风格分析 |
| 风格分析 | 采样数据 | 场景维度笔触分析 | 全书验证 |
| 全书验证 | 风格分析 + 全书数据 | `写作资产/文风DNA/{书名}.md` | pop-writer-prose |

> 独立调起：不从拆书管线走时，直接从正文采样蒸馏文风DNA。

### 3.8 pop-shared-reader v0.15.0（独立拆书阅读器）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:-----------|
| Phase A | 全书txt | 叙事笔记.md + 结构化数据.yaml | pop-shared-html |

> 独立调起，不走拆书管线。用于读书记录/结构化标注/角色统计/名场面提取。

---

## 四、拆书产出 -> 写作专家消费协议

| 产出 | 来源 Skill | 消费方 | 用途 |
|:-----|:-----------|:-------|:-----|
| chXXX-设计包 | decon-design-pack | creative（PRD参考）、world（L1参考） | 参考书结构分析 |
| 幕纲/卷纲 | decon-volume | creative（节奏参考） | 卷幕节奏模板 |
| L1-01~06 | decon-setting | world | 力量体系/世界观参考 |
| 战力数值 | decon-setting | world | 力量金字塔防崩参考 |
| 文风DNA/{书名}.md | pop-shared-dna | prose-render | 风格渲染参考 |

---

## 五、典型路径速查

| 场景 | 管线路径 | 关键闸门 |
|:-----|:---------|:---------|
| **快速拆解（前N章）** | download -> decon -> design-pack(Phase1) -> volume(Phase2) -> setting(Phase3) | scope 确认 |
| **全量拆解** | download -> decon -> Phase1->2->3->4 | 阶段间验证报告 |
| **提取文风DNA** | decon（>=20章）-> pop-shared-dna | 20章采样下限 |
| **独立阅读/标注** | pop-shared-reader（独立调起） | -- |

---

## 六、关键架构决策

### 6.1 为什么拆为双专家

| 决策 | 理由 |
|:-----|:------|
| **独立调用** | 拆书专家不需要写作专家上下文。用户说"拆这本书"不与某个写作项目绑定 |
| **产出可复用** | 拆书产出存于 _参考书/{书名}/，多个写作项目同时消费同一份拆书数据 |
| **职责隔离** | 写作专家专注"怎么创作"，拆书专家专注"怎么分析"。能力集不同 |
| **调度清晰** | expert-writer 通过意图识别路由到对应专家，不耦合两个域 |

### 6.2 为什么用 pop-decon-* 前缀而非 pop-novel-*

实战沉淀。decon 系列（decon-design-pack / decon-volume / decon-setting / decon-trace）是拆书管线的主干，各自独立维护版本和步骤文件。pop-novel-* 是旧命名，已被 pop-decon-* 取代。

### 6.3 为什么 bookstrap 被移除

bookstrap 的 forward 模式（从设定到正文）已迁移至 creative + world。reverse 模式（从正文到设定还原）的能力被 pop-decon-setting 覆盖。整个 skill 不再有独立存在的职责。

### 6.4 pop-decon-trace 状态

已规划但未落地。Phase 4 的创作溯源追踪将由新 skill 承担。当前拆书管线在 Phase 3（setting）结束后产出已足够写作专家消费。

---

## 附录 A：拆书项目文件全貌

```text
_参考书/{书名}/
|
|-- {书名}.txt                       <- download-webnovel
|
|-- Phase1/                          <- pop-decon-design-pack
|   |-- ch001-设计包.md
|   |-- ch002-设计包.md
|   +-- ...
|
|-- Phase2/                          <- pop-decon-volume
|   |-- 幕纲.md
|   |-- 卷纲.md
|   |-- 剧情线文档.md
|   +-- chekhov-tracker.md
|
|-- Phase3/                          <- pop-decon-setting
|   |-- L1-01-世界蓝图.md
|   |-- L1-02-力量体系.md
|   |-- L1-03-历史驱力.md
|   |-- L1-04-物种天赋.md
|   |-- L1-05-势力格局.md
|   |-- L1-06-资源物品.md
|   |-- 世界宪法.md
|   +-- 战力体系.md
|
+-- 写作资产/                          <- pop-shared-dna
    +-- 文风DNA/{书名}.md
```

---

> 本文档基于各 skill 当前 SKILL.md 的实际 pipeline 字段构建（2026-06-19）。
> 拆书专家 skill 清单：tool-download-webnovel(v2.0.1)、pop-decon(v13.8.0)、pop-decon-design-pack(v3.0.0)、
> pop-decon-volume(v2.1.0)、pop-decon-setting(v1.1.0)、pop-shared-dna(v4.0.3)、pop-shared-reader(v0.15.0)。
> pop-novel-bookstrap 已移除。pop-novel-character-schema 职责已迁移至 pop-writer-character。
> pop-decon-trace 已规划（forthcoming）。写作专家见 `01-写作专家全链路依赖图-PRD.md`。
