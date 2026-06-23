# 拆书专家全链路依赖图 — 文件依赖与产出全景

> 版本：v3.0 | 2026-06-23
> 说明：本文档覆盖拆书专家（pop-decon-* / pop-shared-*）全链路。基于各 skill 当前 SKILL.md 的 pipeline 字段现状构建。
> 写作专家见 `01-写作专家全链路依赖图-PRD.md`。
> **v3.0 迭代**：拆书管线从"卷纲/幕纲"物理结构改为"L2剧情单元卡/L3剧情线/L4全书事件"5级叙事结构。Phase S（快速扫描）废弃删除，其功能被 Phase 5 PRD 吸收。新增 Phase 5（全书立项PRD）作为管线最后环节，基于全管线数据深度综合产出立项PRD。L1=章节设计包=1章=2k~3k字=12~15个L0事件。

## 拆书专家管线顺序（硬性）

```
download → decon(orchestrator) → design-pack(Phase1) → volume(Phase2) → setting(Phase3) → trace(Phase4) → prd(Phase5)
   ↑            ↑                    ↑                    ↑                  ↑                 ↑                ↑
tool-download  pop-decon            pop-decon            pop-decon          pop-decon         pop-decon        pop-decon
-webnovel      v15.0.0              -design-pack         -volume            -setting          -trace           -prd
v2.0.1                              v3.3.0               v3.0.0             v1.2.0            (forthcoming)    v1.0.0
                                                    ↓（可选）
                                              pop-shared-dna v4.0.3 → prose-render
```

**辅助skill（独立调起，不改变主线进度）：**
- `pop-shared-reader` v0.15.0 — 独立拆书阅读器。产出叙事笔记+结构化数据→pop-shared-html
- `pop-shared-dna` v4.0.3 — 文风DNA蒸馏。可从管线走，也可独立调起

**拆书专家产出 → 写作专家消费：**
- 设计包 + L2/L3/L4叙事结构 → creative（PRD/引擎参考）、plot（节奏参考）
- L1-01~06 + 世界宪法 + 战力体系 → world（L1设定参考）
- 文风DNA/{书名}.md → prose（风格渲染）
- 入库 pop-trope-library → 各环节查询消费（详见第三章）

写作专家 **不依赖** 拆书专家——没有拆书产出时使用默认节奏兜底。
拆书专家 **不消费** 写作专家——独立运行。

---

## 一、管线文件接口

> S = 静态（一次产出）/ D = 动态（持续维护）

### 下载环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| download-webnovel v2.0.1 | 书名 | `{书名}.txt` | S | decon | TXT 直链下载，搜直链→下直链，不爬目录页 |

### Phase 1 设计包环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| design-pack ① ETL | `{书名}.txt` | 结构化章节数据 | S | design-pack ② | 清洗+标准化 |
| design-pack ② 分章 | 结构化数据 | 逐章原始数据 | S | design-pack ③ | 章节切分 |
| design-pack ③ 4层设计包 | 逐章数据 + 模板 | `chXXX-设计包.md` xN（L1 章节设计包：1章=2k~3k字=12~15个L0事件） | S | volume, creative | 4层：骨架+爽点+角色+感官 |

### Phase 2 叙事结构环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| volume ① L2剧情单元识别 | 设计包 chXXX 数据 | L2单元卡 | S | volume ② | 识别L2剧情单元边界 |
| volume ② L3剧情线追踪 | L2单元卡 | L3剧情线卡 | S/D | volume ③, plot | 追踪L3剧情线 |
| volume ③ L4全书事件识别 | L3剧情线 | L4全书事件卡 | S | pop-trope-library(剧情库) | 识别跨线交汇全书事件 |
| volume ④ 套路聚合 | 套路库 | 套路分析段 | S | plot | L3线套路偏好分析 |
| volume ⑤ L2/L3双轨入库 | L2单元卡 + L3剧情线 | 剧情库条目 | S | pop-trope-library(剧情库) | L2+L3双轨入库 |

### Phase 3 设定环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| setting ① L1六件套 | 设计包 + L2/L3数据 | `L1-01~06.md` | S | world, pop-trope-library(设定库) | 世界蓝图/力量/历史/物种/势力/资源 |
| setting ② 世界宪法 | L1 六件套 | `世界宪法.md` | S | world | 世界运转核心规则 |
| setting ③ 数值体系 | L1 力量体系 | `战力体系.md` `动态升级表.md` | S | world | 静态金字塔 + 动态升级曲线 |

### Phase 4 溯源环节（forthcoming）

> 已规划但未独立建仓。从章节数据反向追查作者的 craft recipe 和叙事策略。

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| trace（forthcoming） | 全管线数据 | 创作溯源文档 | S | creative | 反向追查作者叙事策略 |

### Phase 5 立项PRD环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| prd ① 收集全管线产出 | L1-L4全部产出 | `_temp/prd-collected-data.md` | S | prd ② | 汇集全管线数据 |
| prd ② 综合产出立项PRD | 收集数据 | `全书立项PRD.md` | S | creative, pop-trope-library(立项库) | 逆向破解总结报告 |

### 文风DNA环节（可选/独立调起）

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| dna ① 采样（>=20章） | 设计包 + 章节数据 | 采样数据集 | S | dna ② | 均匀采样 |
| dna ② 风格分析 | 采样数据 | 场景维度笔触分析 | S | dna ③ | 按场景类型提取笔触 |
| dna ③ 全书验证 | 风格分析 + 全书数据 | `写作资产/文风DNA/{书名}.md` | S | prose, pop-trope-library(文风DNA) | 全书搜索验证+产出档案 |

> 独立调起：不从拆书管线走时，直接从正文采样蒸馏文风DNA。

---

## 二、辅助 Skill — 独立调起

| Skill | 入 | 出 | → | 用途 |
|:---|---:|---:|:---|:-----|
| reader v0.15.0 | 全书txt | `叙事笔记.md` + `结构化数据.yaml` | pop-shared-html | 独立拆书阅读器。Phase 0/A/B/B+/C 五段式阅读，产出双格式 |
| dna v4.0.3 | 正文（>=20章） | `文风DNA/{书名}.md` | prose | 可独立调起，不走拆书管线 |

> pop-shared-reader 采用五段式阅读方法论（Phase 0 预检 → Phase A 按卷深度阅读 → Phase B 跨卷关联 → Phase B+ 方案复盘 → Phase C 按需结构化），核心理念："你拆得越碎，读者越看不懂"——叙事节奏、伏笔链、角色弧光必须在阅读连贯性中感知。

---

## 三、pop-trope-library 公共知识库入库协议

> `pop-trope-library` 不是 skill，是公共知识库。当前本地存储，未来云端化。
> **拆书专家（pop-decon-* / pop-shared-*）产出入库，写作专家（pop-writer-*）各环节按需查询消费。**
> 入库协议详见 `skills/pop-trope-library/references/入库清洗SOP.md`，查询协议详见 `skills/pop-trope-library/references/调用匹配SOP.md`。
>
> **核心原则：拆书产出先入库（按 library 五库文件分类），写入后再被写作管线按协议消费。两条线不交叉。**

### 五库结构

| 模块 | 内容 | 服务对象 | 入库来源 |
|:-----|:-----|:---------|:---------|
| `立项库/` | PRD 级经验：立项模式/元爽点组合/题材焊接/加工哲学/失败案例 | creative, expert-writer | Phase 4 trace（SOP转化）+ Phase 5 prd + 写书复盘 |
| `设定库/` | **按书整包**的 L1 设定：PRD.md + L1-01~06 + 世界宪法 + 角色与关系 | reservoir, world, character | Phase 3 setting |
| `文风库/` | 文风笔触档案（场景卡+通用维度+时间演变），**canonical 路径** | prose | pop-shared-dna |
| `剧情库/` | **L2可迁移单元卡 + L3剧情线卡**（双轨），按内容标签分目录 | plot | Phase 2 volume（L2/L3双轨提炼） |
| `套路库/` | 抽象叙事模式卡（10字段：模式家族+变体+跨书案例） | creative, plot, chapter, qa | 原始素材晋升 |
| `原始素材/` | L3 具体套路卡（拆书中间层，非消费层） | 套路库晋升 | Phase 1 design-pack |
| `文风DNA/` | 历史兼容路径，存放现有文风档案；新入库优先写 `文风库/` | prose（fallback） | pop-shared-dna（兼容） |

> **路径约定**：`文风库/` = canonical 主路径；`文风DNA/` = fallback 兼容路径。新 DNA 入库优先写 `文风库/`，`文风DNA/` 保持只读兼容。

### 拆书管线 → 五库入库矩阵

> 每个阶段产出后，decon 应确认是否触发入库流程。
> 入库前提：满足对应质量门槛（见 `入库清洗SOP.md`）。**入库是拆书专家产出的最终落点，不是可选步骤。**

| 管线阶段 | 入库模块 | 入什么 | 质量门槛 |
|:---------|:---------|:-------|:---------|
| Phase 1 design-pack | `原始素材/` | L3 具体套路卡（8字段齐全） | 触发条件/套路公式/核心张力/情绪收益/运作机制/使用注意/下游期待/复用记录 |
| Phase 2 volume | `剧情库/{标签}/{书}-{编号}-{名称}.md` | L2可迁移单元卡 + L3剧情线卡（双轨） | 剧情线提炼核查清单通过；❌不按卷/幕切片直接入库；L2结构分析+嵌套子线完整 |
| Phase 3 setting | `设定库/{书名}/` | 整本 L1 设定包（PRD.md + L1-01~06 + 世界宪法 + 起点快照 + 数值体系） | 以整本为单位入库，不拆散为单卡 |
| Phase 4 trace | `立项库/`（可选）| 创意溯源→设计模式 SOP 转化产物 | 需执行 `创意溯源-设计模式SOP.md` 后才可入库 |
| Phase 5 prd | `立项库/{书名}-立项PRD.md` | 全书立项PRD | 核心假说有chXX证据 |
| pop-shared-dna ③ | `文风库/{书名}.md`（canonical）| 文风DNA档案 | 满足 pop-shared-dna 6条红线（原文>=500字/场景卡>=6/通用维度>=4/有时间演变/无降级替换） |
| pop-shared-dna ③ | `文风DNA/{书名}.md`（fallback）| 文风DNA档案（兼容路径） | 同上；`文风库/` 写入后同步保留此 fallback |

### 入库五步流程

1. **打三标签**（原子化素材：原始素材/套路库/剧情库条目）：`layer`(立项/框架/质感/机制/调味) + `track`(修仙/西幻/都市/科幻/武侠/通用) + `meta_joy`(7元爽点之一/无)
   - 整本 L1 设定导入不需要打标签，卖点摘要和匹配逻辑在 `PRD.md` 中
   - 文风库主检索键是书名 + `scene`，不强制三标签
   - 立项库条目可选打标（`source_type/track/meta_joy/stage`）
2. **去重检查**：已有抽象模式卡→追加案例/变体；无→提炼新卡。不同赛道不强行归并。同一本书已有 L1 套件→只补 PRD.md 或索引
3. **抽象层级判定**：L3具体卡入`原始素材/`，抽象模式卡入`套路库/`。独特模式比常见模式更有入库价值，不重复即可晋升。PRD级经验入`立项库/`
4. **写入对应模块**：按素材类型写入指定路径（见上方入库矩阵）
5. **更新索引**：各模块 00-索引.md / 目录.md 同步更新。原始素材索引按书分表+入库日期

### 入库红线

1. ❌ 质量门槛不达标就入库
2. ❌ 三标签缺失（仅限原子化素材）
3. ❌ 强行归并不同模式
4. ❌ 已有重复模式不归并
5. ❌ 入库不更新索引
6. ❌ 设定库继续写入 `框架/`、`质感/` 新素材，破坏按书读取
7. ❌ 剧情库继续把卷/幕/章级切片当主资产
8. ❌ 立项库收桥段碎片，导致 PRD 层被素材噪音污染

### 入库与消费分离

**核心流程：**
```
拆书管线产出 → 入库清洗SOP → pop-trope-library（五库） → 调用匹配SOP → 写作管线消费
```

**原则：**
- 拆书管线负责入库（按 `入库清洗SOP.md`）：产出后先写进 library 对应用模块，完成后才可被消费
- 写作管线负责消费（按 `调用匹配SOP.md`）：从 library 按协议查询，不直接读拆书项目目录
- **两条线不交叉**：写作专家不直接从拆书项目目录读文件，拆书专家不预判写作消费方式
- library 是唯一的中间协议层——拆书端定义"产什么、存哪里"，library 定义"怎么存、怎么找"，写作端定义"真正需要什么"

---

## 四、三级拆解体系

> 详见 `02-三级拆解-PRD.md`（储备方案索引）。

| 级别 | 名称 | 状态 | 对应阶段 | 产出 |
|:-----|:-----|:-----|:---------|:-----|
| **Lv2** | 标准拆解 | ✅ 已落地 | Phase 1~5 | 设计包+叙事结构+设定+溯源+立项PRD，数小时 |
| **Lv3** | 深度溯源 | ⬜ 待推进 | Phase 4 | 创作溯源追踪（forthcoming） |

Lv2/Lv3 的格式对齐+消费端协议待 plot/character-schema 稳定后推进。

---

## 五、典型路径速查

| 场景 | 管线路径 | 关键闸门 |
|:-----|:---------|:---------|
| **快速拆解（前N章）** | download → decon → design-pack(Phase1) → volume(Phase2) → setting(Phase3) | scope 确认 |
| **全量拆解（Lv2）** | download → decon → Phase1→2→3→4→5 → 入库 pop-trope-library | 阶段间验证报告 |
| **提取文风DNA** | decon（>=20章）→ pop-shared-dna → 入库文风DNA | 20章采样下限 |
| **独立阅读/标注** | pop-shared-reader（独立调起） | — |
| **深度溯源（Lv3）** | download → decon → Phase1→2→3→4 | Phase 4 落地后 |

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

实战沉淀。decon 系列（decon-design-pack / decon-volume / decon-setting / decon-trace）是拆书管线的主干，各自独立维护版本和步骤文件。pop-novel-* 是旧命名，已被 pop-decon-* 取代。pop-novel-deconstructor 是 pop-decon 的前身旧名，重命名后已从 v11.x 演进到 v15.0.0。

### 6.3 为什么 bookstrap 被移除

bookstrap 的 forward 模式（从设定到正文）已迁移至 creative + world。reverse 模式（从正文到设定还原）的能力被 pop-decon-setting 覆盖。整个 skill 不再有独立存在的职责。

### 6.4 为什么废弃 Phase S

Phase S的6个轻量文件功能被L5 PRD吸收。PRD作为最终总结而非快速扫描，基于全管线数据深度综合。完整拆解管线（Phase 1~5）需要数小时，但用户可通过前N章拆解快速获得阶段性产出。

### 6.5 为什么 pop-shared-reader 独立于拆书管线

pop-shared-reader 面向"拆书为读"——产出人类可读的叙事笔记，而非工程化拆解数据。它的五段式方法论（Phase 0/A/B/B+/C）强调阅读连贯性，与 decon 系列的工程化拆解是两种范式。独立调起，不走 decon 管线。

### 6.6 pop-decon-trace 状态

已规划但未独立建仓。Phase 4 的创作溯源追踪将由新 skill 承担。当前拆书管线在 Phase 5（立项PRD）结束后产出已足够写作专家消费。

---

## 附录 A：拆书项目文件全貌

```text
{项目目录}/{书名}-拆解/
│
├── {书名}.txt                           [download-webnovel]
│
├── _temp/                               [pop-decon-design-pack Step 1]
│   ├── chapters/ch001.txt ~ chNNN.txt    预拆分的独立章文件
│   └── metadata.json
│
├── 写作资产/                              [pop-decon-design-pack Step 2]
│   ├── 设计包v3/
│   │   ├── ch001-设计包.md
│   │   ├── ch002-设计包.md
│   │   └── ...
│   ├── 价值点分流/
│   │   ├── ch001-价值点.md
│   │   └── ...
│   └── 套路库/
│       └── {套路名}.md                    → 入库 `原始素材/{书前缀}_{套路名}.md`
│
├── 设计/                                 [pop-decon-volume]
│   ├── L2单元卡/
│   │   ├── L2-001-{单元名}.md
│   │   └── ...
│   ├── L3剧情线/
│   │   ├── L3-001-{线名}.md
│   │   └── ...
│   └── L4全书事件/
│       ├── L4-001-{事件名}.md
│       └── ...
│
├── 写作资产/剧情库/                        [pop-decon-volume — L2+L3双轨入库]
│   └── {书名}-{编号}-{名称}.md             → 入库 `剧情库/{标签}/{书}-{编号}-{名称}.md`
│
├── L1-设定/                               [pop-decon-setting]
│   ├── L1-01-世界蓝图.md                   → 入库 `设定库/{书名}/`
│   ├── L1-02-力量体系.md
│   ├── L1-03-历史与驱动力.md
│   ├── L1-04-物种与天赋.md
│   ├── L1-05-势力格局.md
│   ├── L1-06-资源与物品.md
│   ├── 世界宪法.md
│   ├── 起点快照.md
│   └── 数值体系/
│       ├── combat_capability.yaml
│       └── 动态升级表.md
│
├── 写作资产/创意溯源/                      [pop-decon-trace Phase 4]
│   ├── README.md
│   ├── 跨域参考索引.md
│   ├── 参考域-{Name}.md
│   ├── 作者原创贡献.md
│   └── 融合模式汇总.md                     → SOP转化后入库 `立项库/`
│
├── 全书立项PRD.md                          [pop-decon-prd Phase 5]
│                                          → 入库 `立项库/{书名}-立项PRD.md`
│
└── 写作资产/文风DNA/                       [pop-shared-dna]
    └── {书名}.md                           → 入库 `文风库/{书名}.md`（canonical）
                                            → 同步保留 `文风DNA/{书名}.md`（fallback）
```

> **入库约定**：箭头 `→` 标注了每类产出的 library 落点。拆书项目目录内的文件是工作副本，library 是 canonical 存储。入库后写作管线从 library 消费，不从项目目录直接读取。

---

> 本文档基于各 skill 当前 SKILL.md 的实际 pipeline 字段构建（2026-06-23）。
> 拆书专家 skill 清单：tool-download-webnovel(v2.0.1)、pop-decon(v15.0.0)、pop-decon-design-pack(v3.3.0)、
> pop-decon-volume(v3.0.0)、pop-decon-setting(v1.2.0)、pop-shared-dna(v4.0.3)、pop-shared-reader(v0.15.0)、pop-decon-prd(v1.0.0)。
> pop-decon-trace 已规划（forthcoming）。
> 三级拆解体系见 `02-三级拆解-PRD.md`。写作专家见 `01-写作专家全链路依赖图-PRD.md`。
