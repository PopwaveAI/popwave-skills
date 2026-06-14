# pipeline-arch.md — 管线架构锚定参考

> 用途：路由决策 + Reflect 校验时的文件结构锚定
> 来源：`prd/写作专家全链路文件依赖图-PRD.md` §一~§四~§附录A（精炼版）
> 加载方式：`Get-Content -Encoding UTF8 -Raw`，不用 Read 工具。

---

## 〇、全链路总览

```
                        ┌───────────────┐
                        │ download-      │
                        │ webnovel-txt   │
                        │ TXT 直链下载   │
                        └───────┬───────┘
                                │ 产出: {书名}.txt
                                ▼
  ┌─────────────────────────────────────────────────────┐
  │               pop-decon (v12)         │
  │         雪花倒推：正文→事实→卷幕→世界观→故事引擎        │
  │  产出: 角色卡 + L1六件套 + 卷/幕/Canvas + 故事引擎(Lv3)  │
  └──────────┬──────────┬──────────────────────────────┘
             │          │
             │          ▼
             │    ┌──────────────────┐
             │    │    pop-shared-dna       │
             │    │  文风DNA蒸馏     │
             │    │  产出: 写作资产/  │
             │    │  文风DNA/{书名}.md│
             │    └────────┬─────────┘
             │             │
             ▼             ▼
  ┌─────────────────────────────────────────────────────┐
  │               pop-novel-bookstrap                    │
  │              开书设定 (forward/reverse)              │
  │  产出: story-engine + L1-01~06 + 角色卡 + project    │
  │         + 数值体系x4 + 起点/终点快照                  │
  └──────────┬──────────────────────────────────────────┘
             │
             ▼
  ┌─────────────────────────────────────────────────────┐
  │               pop-writer-plot                         │
  │              剧情架构                                │
  │  输入: story-engine + 快照 + L1 + 角色卡              │
  │  产出: ★全书架构 → volume-XX → act-YY.yaml           │
  └──────────┬──────────────────────────────────────────┘
             │
             ▼
  ┌─────────────────────────────────────────────────────┐
  │          pop-writer-chapter  ★NEW              │
  │         章纲/导演卡 (Step 1→3)                       │
  │  输入: act-XX.yaml + volume-XX.md + entity-snapshot   │
  │        + 状态/角色/{主角}-角色卡    ⚠️ 不碰文风        │
  │  产出: chXXX-设计包.md + entity-snapshot 更新         │
  └──────────┬──────────────────────────────────────────┘
             │
             ▼
  ┌─────────────────────────────────────────────────────┐
  │          pop-writer-prose  ★NEW                │
  │         正文渲染/上色 (Step 1→4)                      │
  │  输入: 设计包 + 写作资产/文风DNA/   ⚠️ 不碰剧情       │
  │  产出: 正文/chXXX.md（含章末状态更新块）              │
  └──────────┬──────────────────────────────────────────┘
             │
             ▼
  ┌─────────────────────────────────────────────────────┐
  │               pop-writer-qa                           │
  │              爽点质检 (Step 1→3)                     │
  │  输入: 正文 + 设计包 + act-XX.yaml + reader_profile   │
  └──────────┬──────────────────────────────────────────┘
             │
             ▼ (可选)
  ┌─────────────────────────────────────────────────────┐
  │          pop-writer-html                     │
  │         HTML 发布                                    │
  └─────────────────────────────────────────────────────┘
```

> **调度入口**：expert-writer（元 Skill）→ §0 全局感知 → §3.1 Think 路由 → §3.2 Execute 派发子 Skill → §3.3 Reflect 审视 + 索引回写

---

## 一、文件分类矩阵（S/D/M + 消费者速查）

| 文件 | 类型 | 产出者 | 消费者 |
|:-----|:----:|:-------|:------|
| story-engine.yaml | S | bookstrap Phase 0 | plot（内化→卷命题） |
| L1-01~06 | S | bookstrap Phase 1 | plot（幕设计参考） |
| 数值体系 x4 | S | bookstrap Phase 5 | plot + chapter-design(战斗章) |
| project.yaml | M | bookstrap Phase 3 | expert-writer 路由 |
| 状态/角色/角色卡.md | **D** | bookstrap初版 → plot卷间回写 | plot(core_desire) + chapter-design |
| 状态/势力/{势力}.md | **D** | plot 卷间 | plot + expert-writer |
| 状态/卷摘要/volume-XX.md | **D** | plot 卷末 | expert-writer + 人 |
| 状态/世界状态.md | **D** | plot 卷间 | plot + chapter-design |
| 起点/终点快照.md | S | bookstrap | plot Step 2 |
| 设计/全书架构.md | S+D | plot Phase 0 | volume-XX × N |
| 设计/卷/volume-XX.md | S | plot Step 4.5 | chapter-design Step 1 |
| 设计/幕/vol-XX/act-YY.yaml | **D** | plot Step 9 | chapter-design + qa |
| 00-总控/entity-snapshot.yaml | **D** | chapter-design(逐章) | chapter-design(下章) + expert-writer |
| 写作资产/设计包/chXXX-设计包.md | **D** | chapter-design | prose-render |
| 正文/chXXX.md | **D** | prose-render | qa + html-renderer |
| 写作资产/文风DNA/{书名}.md | S | deconstructor/pop-shared-dna | prose-render |

> **S** = 静态（一次写入，只读不写） | **D** = 动态（持续维护，有更新者） | **M** = 元数据

---

## 二、规范目录树（7卷全貌）

```
{项目}/
├── 00-总控/                    ← 工程层
│   ├── project.yaml           [bookstrap] {M}
│   ├── entity-snapshot.yaml   [chapter-design] {D}
│   └── 数值体系/              [bookstrap] {S}
├── 00-原始设定/                ← bookstrap 静态产出，仅 plot 消费
│   ├── L0-产品层/ (story-engine + 融合摘要 + PRD)
│   ├── L1-元设定层/ (01~06)
│   ├── 起点快照.md
│   └── 终点快照.md
├── 状态/                      ← 全书跨卷动态追踪 {D}
│   ├── 角色/ (主角+配角卡, per-volume 快照段)
│   ├── 势力/ (渗透阶段/规模/事件)
│   ├── 卷摘要/ (一章一句话, ~7个)
│   └── 世界状态.md (领土/裂缝/城市)
├── 设计/                      ← plot 产出层
│   ├── 全书架构.md             [S+D]
│   ├── 卷/ (volume-01~07.md)  [S]
│   └── 幕/ vol-XX/            [D]
│       ├── act-01.yaml        (含 info_release_plan 段)
│       └── ...
├── 写作资产/                   ← design + render 共用
│   ├── 设计包/ (ch001~800-设计包.md) [D]
│   ├── 文风DNA/ ({书名}.md)    [S]
│   └── 锚定章库/              [D]
├── 正文/ chXXX.md             [D]
└── _参考书分析/               [S]
```

---

## 三、Reflect 校验基线指引

### entity-snapshot 与 状态/ 的校验对应

| entity-snapshot 字段 | 状态/中的对照源 | 一致性检查 |
|:---------------------|:---------------|:----------|
| protagonist.level | 状态/角色/索伦-主角卡.md#快照 | 等级偏差→P1 |
| protagonist.sanity | 状态/角色/索伦-主角卡.md#快照 | 理智值偏差→WARN |
| protagonist.flags | 状态/角色/索伦-主角卡.md#伏笔 | 事件log是否反映在角色卡→WARN |
| sister.status | 状态/角色/薇薇安-配角卡.md#快照 | 薇薇安死亡→P0 |

### pipeline 阶段 → 应有文件（Deps 速查）

| 阶段 | 必须存在 | 建议存在 |
|:-----|:---------|:---------|
| bookstrap 完成 | project.yaml + L1-01~06 + 角色卡 + 数值体系 + 快照 | deconstruct-融合摘要 |
| plot 完成 (卷N) | volume-NN.md + 幕/vol-NN/act-*.yaml × N幕 | 全书架构.md |
| chapter-design 完成 (chN) | 写作资产/设计包/chN-设计包.md + entity-snapshot 更新 | — |
| prose-render 完成 (chN) | 正文/chN.md | 章末状态更新块合规 |

### 双消费提醒

- **Agent 友好文件**：act-XX.yaml（YAML结构化）、00-总控/entity-snapshot.yaml（YAML）、story-engine.yaml（YAML）、状态/角色/（YAML frontmatter）
- **人友好文件**：起点/终点快照（表格+叙述）、状态/角色/主角卡（九节结构化）、正文/chXXX.md（最终消费品）
- **Markdown 文件关键信息靠前放**：YAML frontmatter 用于 agent 精确定位；正文表格+标题用于人扫读
