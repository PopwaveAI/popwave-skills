# 拆书专家全链路依赖图 — 文件依赖与产出全景

> 版本：v2.0 | 2026-06-22
> 说明：本文档覆盖拆书专家（pop-decon-* / pop-shared-*）全链路。基于各 skill 当前 SKILL.md 的 pipeline 字段现状构建。
> 写作专家见 `01-写作专家全链路依赖图-PRD.md`。

## 拆书专家管线顺序（硬性）

```
download → decon(orchestrator) → [Phase S] → design-pack(Phase1) → volume(Phase2) → setting(Phase3) → trace(Phase4)
   ↑            ↑                   ↑              ↑                  ↑                 ↑                ↑
tool-download  pop-decon      pop-decon       pop-decon          pop-decon         pop-decon        pop-decon
-webnovel      v14.1.0        -design-pack    -volume            -setting          -trace           (调度)
v2.0.1                        v3.3.0          v2.3.0             v1.2.0            (forthcoming)
                                                    ↓（可选）
                                              pop-shared-dna v4.0.3 → prose-render
```

**辅助skill（独立调起，不改变主线进度）：**
- `pop-shared-reader` v0.15.0 — 独立拆书阅读器。产出叙事笔记+结构化数据→pop-shared-html
- `pop-shared-dna` v4.0.3 — 文风DNA蒸馏。可从管线走，也可独立调起

**拆书专家产出 → 写作专家消费：**
- 设计包 + 卷纲 + 幕纲 → creative（PRD/引擎参考）、plot（节奏参考）
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

### Phase S 快速扫描环节（Lv1）

> Phase S 是完整拆解前的快速扫描层，~25分钟跑完，产出6个轻量文件让用户尽快拿到可开书素材。
> Phase 0~4 全部保留不受影响。详见 `04-PhaseS改造-PRD.md`。

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| decon ① 确认赛道 | {书名}.txt + 目录/简介 | 赛道判定 | S | Phase S ② | 选角色卡示例对照 |
| decon ② 精读前10-20章 | {书名}.txt | 主角初始/终点状态 + 核心驱动事件 + 5条文风特征 | S | Phase S ④ | 快速提取核心假说 |
| decon ③ 目录级概览 | {书名}.txt | 全书卷数 + 卷1占比 + 核心矛盾暗示 | S | Phase S ④ | 宏观结构判断 |
| decon ④ 产出6文件 | ②③数据 | `Lv1-拆解摘要.md` `story-engine.yaml` `Lv4-{主角}-参考卡.md` `卷1-起点快照.md` `卷1-终点快照.md` `快速文风指纹-top5.md` | S | creative, world, bookstrap | 入口文件+核心假说+主角卡+起终点+文风指纹 |

Phase S 红线：❌ 不编造（前10章未显示的信息一律留空）❌ 不做 validation（不需要 Phase 3 式验证回环）

### Phase 1 设计包环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| design-pack ① ETL | `{书名}.txt` | 结构化章节数据 | S | design-pack ② | 清洗+标准化 |
| design-pack ② 分章 | 结构化数据 | 逐章原始数据 | S | design-pack ③ | 章节切分 |
| design-pack ③ 4层设计包 | 逐章数据 + 模板 | `chXXX-设计包.md` xN | S | volume, creative | 4层：骨架+爽点+角色+感官 |

### Phase 2 卷幕环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| volume ① 卷边界识别 | 设计包 chXXX 数据 | 卷划分 | S | volume ② | 识别卷边界 |
| volume ② 幕边界识别 | 卷划分 | 幕划分 | S | volume ③ | 识别幕边界 |
| volume ③ 剧情线反推 | 卷/幕划分 | `剧情线文档.md` | S/D | volume ④, plot | 反推剧情线 |
| volume ④ 契诃夫枪链 | 剧情线 | `chekhov-tracker.md` | D | setting, plot | 追踪契诃夫枪链 |
| volume ⑤ 剧情单元提取 | 卷/幕/剧情线数据 | `剧情单元卡.md` xN | S | pop-trope-library(剧情库) | 章级剧情单元卡入库 |

### Phase 3 设定环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| setting ① L1六件套 | 设计包 + 卷/幕数据 | `L1-01~06.md` | S | world, pop-trope-library(设定库) | 世界蓝图/力量/历史/物种/势力/资源 |
| setting ② 世界宪法 | L1 六件套 | `世界宪法.md` | S | world | 世界运转核心规则 |
| setting ③ 数值体系 | L1 力量体系 | `战力体系.md` `动态升级表.md` | S | world | 静态金字塔 + 动态升级曲线 |

### Phase 4 溯源环节（forthcoming）

> 已规划但未独立建仓。从章节数据反向追查作者的 craft recipe 和叙事策略。

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| trace（forthcoming） | 全管线数据 | 创作溯源文档 | S | creative | 反向追查作者叙事策略 |

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
> 拆书专家（pop-decon-*）产出入库，写作专家（pop-writer-*）各环节查询消费。
> 入库协议详见 `skills/pop-trope-library/references/入库清洗SOP.md`，查询协议详见 `references/调用匹配SOP.md`。

### 四模块

| 模块 | 内容 | 入库来源 |
|:-----|:-----|:---------|
| `套路库/` | 抽象叙事模式（模式家族+变体+跨书案例） | 原始素材晋升 |
| `设定库/` | 赛道设定创意（框架层=力量体系/制度/数值，质感层=命名/术语/文明底色） | decon-setting Phase 3 |
| `剧情库/` | 章级剧情单元卡（事件链+冲突弧线+复用要点） | decon-volume Step ⑤ |
| `文风DNA/` | 文风笔触特征档案（场景卡+通用维度+时间演变） | pop-shared-dna |

### 拆书管线入库矩阵

> 每个阶段产出后，decon 应确认是否触发入库流程。
> 入库前提：满足对应质量门槛（见 `入库清洗SOP.md`）。

| 管线阶段 | 入库模块 | 入什么 | 质量门槛 |
|:---------|:---------|:-------|:---------|
| Phase 1 design-pack | `原始素材/` | L3 具体套路卡（8字段齐全） | 触发条件/套路公式/核心张力/情绪收益/运作机制/使用注意/下游期待/复用记录 |
| Phase 2 volume ⑤ | `剧情库/` | 剧情单元卡（事件链+结构解析+金句+复用要点） | ❌不写方法论，只写结构化数据 |
| Phase 3 setting | `设定库/` | 整本 L1 设定（L1-01~06 + 世界宪法 + PRD.md） | 以整本为单位入库，不拆散 |
| dna ③ | `文风DNA/` | 文风DNA档案 | 满足 pop-shared-dna 6条红线（原文>=500字/场景卡>=6/通用维度>=4/有时间演变/无降级替换/只留摘要） |

### 入库五步流程

1. **打三标签**（仅原子化素材）：`layer`(框架/质感) + `track`(修仙/西幻/都市/科幻/武侠/通用) + `meta_joy`(7元爽点之一/无)
2. **去重检查**：已有抽象模式卡→追加案例/变体；无→提炼新卡。不同赛道不强行归并
3. **抽象层级判定**：L3具体卡入`原始素材/`，抽象模式卡入`套路库/`。独特模式比常见模式更有入库价值，不重复即可晋升
4. **写入对应模块**：按素材类型写入指定路径
5. **更新索引**：各模块 00-索引.md / 目录.md 同步更新

### 入库红线

1. ❌ 质量门槛不达标就入库
2. ❌ 三标签缺失（仅原子化素材）
3. ❌ 强行归并不同模式
4. ❌ 已有重复模式不归并
5. ❌ 入库不更新索引

### 入库与消费分离

拆书管线负责入库（按 `入库清洗SOP.md`），写作管线负责消费（按 `调用匹配SOP.md`），两条线不交叉。

---

## 四、三级拆解体系

> 详见 `02-三级拆解-PRD.md`（储备方案索引）。

| 级别 | 名称 | 状态 | 对应阶段 | 产出 |
|:-----|:-----|:-----|:---------|:-----|
| **Lv1** | 快速扫描 | ✅ 已落地 | Phase S | 6个轻量文件，~25分钟 |
| **Lv2** | 标准拆解 | ✅ 已落地 | Phase 1~3 | 设计包+卷幕+设定，数小时 |
| **Lv3** | 深度溯源 | ⬜ 待推进 | Phase 4 | 创作溯源追踪（forthcoming） |

Lv2/Lv3 的格式对齐+消费端协议待 plot/character-schema 稳定后推进。

---

## 五、典型路径速查

| 场景 | 管线路径 | 关键闸门 |
|:-----|:---------|:---------|
| **快速开书（Lv1）** | download → decon → Phase S（~25min）→ 6文件 → "老板，可以开书了" | 前10-20章精读 |
| **快速拆解（前N章）** | download → decon → Phase S → design-pack(Phase1) → volume(Phase2) → setting(Phase3) | scope 确认 |
| **全量拆解（Lv2）** | download → decon → Phase1→2→3 → 入库 pop-trope-library | 阶段间验证报告 |
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

实战沉淀。decon 系列（decon-design-pack / decon-volume / decon-setting / decon-trace）是拆书管线的主干，各自独立维护版本和步骤文件。pop-novel-* 是旧命名，已被 pop-decon-* 取代。pop-novel-deconstructor 是 pop-decon 的前身旧名，重命名后已从 v11.x 演进到 v14.1.0。

### 6.3 为什么 bookstrap 被移除

bookstrap 的 forward 模式（从设定到正文）已迁移至 creative + world。reverse 模式（从正文到设定还原）的能力被 pop-decon-setting 覆盖。整个 skill 不再有独立存在的职责。

### 6.4 为什么新增 Phase S

完整拆解管线（Phase 1~3）需要数小时，用户往往等不及。Phase S 在 ~25 分钟内产出6个轻量文件，让用户尽快拿到可开书的核心素材（主角卡、起终点快照、文风指纹、核心假说）。Phase 0~4 全部保留不受影响，用户可选继续深度拆解。

### 6.5 为什么 pop-shared-reader 独立于拆书管线

pop-shared-reader 面向"拆书为读"——产出人类可读的叙事笔记，而非工程化拆解数据。它的五段式方法论（Phase 0/A/B/B+/C）强调阅读连贯性，与 decon 系列的工程化拆解是两种范式。独立调起，不走 decon 管线。

### 6.6 pop-decon-trace 状态

已规划但未独立建仓。Phase 4 的创作溯源追踪将由新 skill 承担。当前拆书管线在 Phase 3（setting）结束后产出已足够写作专家消费。

---

## 附录 A：拆书项目文件全貌

```text
_参考书/{书名}/
│
├── {书名}.txt                           [download-webnovel]
│
├── PhaseS/                              [pop-decon Phase S — Lv1快速扫描]
│   ├── Lv1-拆解摘要.md                   入口文件：一句话核心+赛道+卷1概览+主角驱动
│   ├── story-engine.yaml                 核心假说提取，供 bookstrap Phase 0 对照
│   ├── Lv4-{主角}-参考卡.md              主角角色卡（宁空不编）
│   ├── 卷1-起点快照.md                    第1章开篇状态
│   ├── 卷1-终点快照.md                    第100章（卷末）状态
│   └── 快速文风指纹-top5.md               5条可执行文风规则
│
├── Phase1/                              [pop-decon-design-pack]
│   ├── ch001-设计包.md
│   ├── ch002-设计包.md
│   └── ...
│
├── Phase2/                              [pop-decon-volume]
│   ├── 幕纲.md
│   ├── 卷纲.md
│   ├── 剧情线文档.md
│   ├── chekhov-tracker.md
│   └── 剧情单元卡/                       → 入库 pop-trope-library/剧情库/
│       ├── unit-001.md
│       └── ...
│
├── Phase3/                              [pop-decon-setting]
│   ├── L1-01-世界蓝图.md                 → 入库 pop-trope-library/设定库/
│   ├── L1-02-力量体系.md
│   ├── L1-03-历史驱力.md
│   ├── L1-04-物种天赋.md
│   ├── L1-05-势力格局.md
│   ├── L1-06-资源物品.md
│   ├── 世界宪法.md
│   ├── 战力体系.md
│   └── 动态升级表.md
│
└── 写作资产/                              [pop-shared-dna]
    └── 文风DNA/{书名}.md                 → 入库 pop-trope-library/文风DNA/
```

---

> 本文档基于各 skill 当前 SKILL.md 的实际 pipeline 字段构建（2026-06-22）。
> 拆书专家 skill 清单：tool-download-webnovel(v2.0.1)、pop-decon(v14.1.0)、pop-decon-design-pack(v3.3.0)、
> pop-decon-volume(v2.3.0)、pop-decon-setting(v1.2.0)、pop-shared-dna(v4.0.3)、pop-shared-reader(v0.15.0)。
> pop-decon-trace 已规划（forthcoming）。Phase S 快速扫描层见 `04-PhaseS改造-PRD.md`。
> 三级拆解体系见 `02-三级拆解-PRD.md`。写作专家见 `01-写作专家全链路依赖图-PRD.md`。
