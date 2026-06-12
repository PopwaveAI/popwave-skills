> **状态：已合并 ✅** ｜ 本文档由「网文创作管线 · 全链路优化 PRD」和「写作专家全链路 — 文件依赖与产出全景 PRD」合并而成，统一呈现管线全景与优化方案。

# 写作专家全链路 — 文件依赖与产出全景 PRD

> 版本：v1.4 | 2026-06-11  
> 更新说明：v1.4 — 目录重构：03-前缀消除（03-正文→正文、03-写作资产→写作资产/设计包）；L3-角色层→状态/（角色+势力+卷摘要+世界状态）；数值体系→00-总控/；文风DNA+锚定章→写作资产/；幕/按卷分组(vol-XX/)卷内编号；info-release合并进act#info_release_plan段；起点/终点快照→00-原始设定/。  
> 说明：本文档展示 popwave 写作全链路的完整管线结构，每个节点标注上游依赖文件、下游产出文件、以及跨 skill 共享的关键文件。

---

## 目录

- 一、全链路总览图
- 二、Skill 管线流程
- 三、各 Skill 详细文件依赖表
- 四、跨 Skill 共享文件清单
- 五、管线调度与索引体系
- 六、典型路径速查

---

## 一、全链路总览图

```
                         ┌───────────────┐
                         │ download-      │
                         │ webnovel-txt   │
                         │ TXT 直链下载   │
                         └───────┬───────┘
                                 │ 产出: {书名}.txt
                                 ▼
   ┌─────────────────────────────────────────────────────┐
   │                  pop-novel-deconstructor             │
   │                  拆书分析 (Phase 0→4)                │
   │  输入: {书名}.txt                                   │
   │  产出: T1~T6 + 采样日志 + 诊断报告 + 验证报告 + 文风DNA  │
   │         + 卷1起点/终点快照 + 三维拆书档案             │
   └──────────┬──────────┬──────────────────────────────┘
              │          │
              │          ▼
              │    ┌──────────────────┐
              │    │    pop-dna       │
              │    │  文风DNA蒸馏     │
              │    │  产出: 写作资产/  │
              │    │  文风DNA/{书名}.md│
              │    └────────┬─────────┘
              │             │
              ▼             ▼
   ┌─────────────────────────────────────────────────────┐
  │               pop-novel-bookstrap                    │
  │              开书设定 (forward/reverse)              │
  │  FWD: Phase 0→7 · REV: Phase r1→r6                 │
  └──────────┬──────────────────────────────────────────┘
             │
             │ 产出: story-engine.yaml + L1-01~06
             │       + L3角色卡 + project.yaml
             │       + 数值体系 x4 + 起点/终点快照
             ▼
  ┌─────────────────────────────────────────────────────┐
  │               pop-novel-plot                         │
  │              剧情架构 (Step 1→12)                    │
  │  输入: story-engine.yaml + 起点/终点快照              │
  │        + L3角色卡 + L1-01~06                         │
  └──────────┬──────────────────────────────────────────┘
             │
             │ ★Phase 0: 全卷蓝图 → 设计/全书架构.md
             │ Step 4.5: 逐卷 → 设计/卷/volume-XX.md
             │ Step 9: 逐幕 → 设计/幕/act-XX.yaml
              ▼
   ┌─────────────────────────────────────────────────────┐
   │           pop-novel-chapter-design  ★NEW             │
   │          章纲/导演卡 (Step 1→3)                      │
   │  输入: act-XX.yaml(含info_release_plan) + volume-XX.md │
   │        + entity-snapshot + 状态/角色/{主角}-角色卡     │
   │  ⚠️ 不碰文风 — 只产出事件骨架                         │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: chXXX-设计包.md
              │       + entity-snapshot.yaml (更新)
              ▼
   ┌─────────────────────────────────────────────────────┐
   │           pop-novel-prose-render  ★NEW               │
   │          正文渲染/上色 (Step 1→4)                     │
   │  输入: 设计包 + 写作资产/文风DNA/{style}.md            │
   │  ⚠️ 不碰剧情 — 只管写好                             │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: chXXX.md (含章末状态更新块)
              ▼
   ┌─────────────────────────────────────────────────────┐
   │               pop-novel-qa                           │
   │              爽点质检 (Step 1→3)                     │
   │  输入: 正文 + chXXX-设计包.md + act-XX.yaml + reader_profile      │
   │  产出: QC 报告 (纯感受型，不存盘)                     │
   └─────────────────────────────────────────────────────┘
              │
              ▼ (可选)
   ┌─────────────────────────────────────────────────────┐
   │          pop-novel-html-renderer                     │
   │         HTML 发布                                    │
   │  输入: 正文数据 + 设定数据 + style_profile            │
   │  产出: 宣传/*.html                                   │
   └─────────────────────────────────────────────────────┘
```

### 管线入口（调度层）

```
expert-writer（元 Skill）
 ├─ §0 全局感知 → workspace-index.yaml
 ├─ §3.1 Think → 意图识别 + 审视框架加载
 ├─ §3.1.5 信息增强 → ROUTE-AUGMENT.md
 ├─ §3.1.6 管道前置校验 → pipeline_deps
 ├─ §3.2 Execute → 路由子 Skill
 └─ §3.3 Reflect → 四层审视 + 索引回写
```

---

## 二、Skill 管线流程

### 2.1 新书启动全流程

```
用户说"开书"
  │
  ▼
Step 0 · expert-writer 全局感知
  → 读取 workspace-index.yaml → 锚定项目（新项目/现有）
  ↓
Step 1 · pop-novel-bookstrap (forward)
  ├─ Phase 0:     故事引擎 → story-engine.yaml
  ├─ Phase 0.3:   参考书甄别
  ├─ Phase 0.4:   金手指设计
  ├─ Phase 0.5:   跨域素材聚合 (HARD-GATE)
  ├─ Phase 0.6:   ⬅ 消费 deconstructor 拆书成果 → deconstruct-融合摘要.md
  ├─ Phase 1:     L1 六件套 (01~06)
  ├─ Phase 1.2:   L1 深度展开
  ├─ Phase 1.3:   L1 交叉关联
  ├─ Phase 1.5:   世界稳定性检验
  ├─ Phase 3:     project.yaml + L3角色卡
  ├─ Phase 4:     reader_profile 校对
  ├─ Phase 5:     数值体系 x4
  ├─ Phase 6:     起点快照.md
  └─ Phase 7:     终点快照.md  [用户确认闸门 → 进入 plot]
  ↓
Step 2 · pop-novel-plot (剧情架构)
  ├─ Step 1:  前置 + 节点B → 节点B-XX.md
  ├─ Step 1.5: ★全书架构 → 设计/全书架构.md（消费 story-engine + 快照 + L1 → 输出4卷蓝图）
  ├─ Step 2:  锚点确认 (口述)
  ├─ Step 3:  里程碑 → 里程碑设计.md [用户确认闸门]
  ├─ Step 4:  情节线 → 情节线草案-XX.md [用户确认闸门]
  ├─ Step 4.5: ★卷设计 → 设计/卷/volume-XX.md（角色池/地点池/剧情线/势力动机/快照）
  ├─ Step 9:  ★幕纲 → 设计/幕/vol-XX/act-YY.yaml（Canvas矩阵 + info_release_plan 段内嵌 + per-chapter info_release 字段）[核心产出]
  ├─ Step 10: 场景卡 → _temp/  [用户确认闸门]
  ├─ Step 11: 节奏自检 → 节奏自检报告.md
  └─ Step 12: 产出自检
  ↓
Step 3 · pop-novel-chapter-design (章纲设计/导演卡)  ★NEW
  ├─ Step 1:  读入 Canvas + 状态 → 建立本章设计基线
  ├─ Step 2:  事件链设计（★ 核心）
  │           逐个回合设计事件，同步确定地点/角色/情绪/信息释放/字数
  └─ Step 3:  产出 → 事实骨架.md + 登场人物卡.md + entity-snapshot 更新
  ↓
Step 4 · pop-novel-prose-render (正文渲染/上色)  ★NEW
  ├─ Step 1:  读入设计包 + 文风DNA + 锚定章 → 建立风格感知
  ├─ Step 2:  正文渲染 — 事件链 × 文风DNA → chXXX.md
  ├─ Step 3:  风格验证 — P0禁句扫描 + 视角一致性 + 解说员句式检查
  └─ Step 4:  最终输出 → 正文/chXXX.md（含章末状态更新块）
  ↓
Step 5 · pop-novel-qa (爽点质检)
  ├─ Step 1: 大纲层 QC (写前)
  ├─ Step 2: 骨架层 QC (渲染前)
  └─ Step 3: 正文层 QC → 纯感受报告
```

### 2.2 已有项目续写流程

```
用户说"续写"
  │
  ▼
Step 0 · expert-writer 全局感知
  → 读取 workspace-index.yaml
  → 检查 pre_read_status (精读闸门)
  → 检查 entity-snapshot 一致性
  ↓
Step 1 · pop-novel-bookstrap (reverse)
  ├─ Phase r1: 事件日志 (逐章读正文)
  ├─ Phase r2: L0 提取
  ├─ Phase r3: L1 提取
  ├─ Phase r4: 大纲提取 (volume-XX + act-XX 还原)
  ├─ Phase r5: 卷大纲确认
  └─ Phase r6: 交接验证报告
  ↓
Step 2 → Step 3 → Step 4 → Step 5 (同新书启动的 plot → design → render → qa)
```

### 2.3 参考书拆解流程

```
用户说"拆解这本书"
  │
  ▼
Step 1 · download-webnovel-txt
  → 搜索直链 → 下载 → 质检 → {书名}.txt
  ↓
Step 2 · pop-novel-deconstructor
  ├─ Phase 0:  采样日志.md
  ├─ Phase 1:  诊断报告.md
  ├─ Phase 2:  T1~T7 独立产出
  ├─ Phase 3:  验证报告.md
  └─ Phase 4:  三维拆书档案.md + 卷1起点/终点快照
  ↓ (可选)
Step 3 · pop-dna (文风DNA蒸馏)
  → 均匀采样 ≥20 章 → 全书搜索验证 → 写作资产/文风DNA/{书名}.md
```

---

## 三、各 Skill 详细文件依赖表

### 3.1 pop-novel-bookstrap（开书设定）

| Phase | 上游依赖（输入） | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Phase 0** | — | `L0-产品层/story-engine.yaml` | Phase 1、plot、chapter-design |
| **Phase 0.3** | — | 参考书清单（口述） | Phase 0.5 |
| **Phase 0.4** | — | 金手指设计（口述+记录） | Phase 0.5 |
| **Phase 0.5** | Phase 0.3 + 0.4 产出 | 跨域素材聚合摘要 | Phase 0.6 |
| **Phase 0.6** | deconstructor 的 T1\~T7（如有锚点书） | `L0-产品层/deconstruct-融合摘要.md` | Phase 1 |
| **Phase 1** | story-engine.yaml | `L1-元设定层/01-世界蓝图.md` \~ `06-资源物品.md` | Phase 1.2 / 1.3 / plot |
| **Phase 1.2** | L1-01\~06 | L1 各文件深度展开补充 | Phase 1.3 |
| **Phase 1.3** | L1-01\~06 (深度展开) | `_交叉引用记录.md` | Phase 1.5 |
| **Phase 1.5** | L1-01\~06 + 交叉引用 | 稳定性检验 checklist | — |
| **Phase 3** | L1-01\~06 | `project.yaml` + `状态/角色/角色卡`（含 core_desire + 快照段预留位） | plot、chapter-design |
| **Phase 4** | project.yaml | reader_profile 校对确认 | plot、chapter-design、qa |
| **Phase 5** | L1-01\~06 | `combat_capability.yaml` + `monster_rank_map.yaml` + `act_rank_schedule.yaml` + `collision_curve.yaml` | plot、chapter-design |
| **Phase 6** | story-engine + 起点状态 | `设计/起点快照.md` [用户确认闸门] | plot (Step 2 锚点) |
| **Phase 7** | story-engine + 终点构想 | `设计/终点快照.md` [用户确认闸门] | plot (Step 2 锚点)、chapter-design |
| **Phase r1** | 已有正文文件（N章） | `事件日志.md` + 批次摘要 | Phase r2 |
| **Phase r2** | 事件日志 | `L0-产品层/` 提取文件 | Phase r3 |
| **Phase r3** | L0 提取 | `L1-元设定层/` 提取文件 | Phase r4 |
| **Phase r4** | L1 提取 | `volume-XX + act-XX` 还原 | Phase r5 |
| **Phase r5** | 卷大纲确认 | 交接验证报告 | Phase r6 |
| **Phase r6** | 全部 reverse 产出 | `交接验证报告.md` | plot |

### 3.2 pop-novel-plot（剧情架构）

| Step | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Step 1** | story-engine.yaml + 起点/终点快照 + L1-01\~06 | `设计/幕/节点B-XX.md` | — |
| **Step 2** | 起点/终点快照 | 锚点确认（口述） | Step 3 |
| **Step 3** | 锚点确认 | `设计/里程碑设计.md` [用户确认闸门] | Step 4 |
| **Step 4** | 里程碑设计 | `设计/幕/情节线草案-XX.md` [用户确认闸门] | Step 4.5/9 |
| **Step 4.5** | story-engine + L1 + 状态/角色/角色卡 + 起点/终点快照 | `设计/卷/volume-XX.md`（角色池/地点池/剧情线/势力动机/快照） | chapter-design |
| **Step 9** | Steps 1-4.5 全部产出 + volume-XX.md | `设计/幕/vol-XX/act-YY.yaml`（Canvas矩阵 + info_release_plan 段内嵌） | chapter-design 核心输入 |
| **Step 10** | act-XX.yaml | `_temp/场景卡` [用户确认闸门] | — |
| **Step 11** | act-XX.yaml + act_rank_schedule | `设计/幕/节奏自检报告.md` | — |
| **Step 12** | 全部 Steps 1-11 产出 | —（校验不产出新文件） | — |

### 3.3 pop-novel-chapter-design（章纲设计/导演卡 ★NEW）

| Step | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Step 1 读入上下文** | act-XX.yaml（含 info_release_plan + chapters[].info_release + Canvas）+ volume-XX.md（角色池/地点池/剧情线）+ entity-snapshot.yaml（当前状态）+ 状态/角色/{主角}-角色卡.md（core_desire） | —（建立基线：角色池/地点池/信息清单/幕纲字段/场景规格/角色欲望） | Step 2 |
| **Step 2 事件链设计** | Step 1 基线 + references/ 四个参考文档 | —（逐个回合设计事件，同步确定角色/地点/情绪/信息释放/字数） | Step 3 |
| **Step 3 产出+状态** | Step 2 事件链 | `写作资产/设计包/chXXX-设计包.md`（含事实骨架+登场人物卡） | pop-novel-prose-render |
|  |  | `00-总控/entity-snapshot.yaml`（更新） | 下一章 design |

> **核心约束：不碰文风。** 不知道文风DNA的存在。不写叙事者声音、不写句子节奏、不写修辞风格。
> 
> **硬性质量下限：** 事件数 ≥ 章字数 ÷ 200 — "靶心不够，Render 没材料"。
> 
> **新增变更：** 事实骨架 + 登场人物卡合并为 `chXXX-设计包.md` 单文件。事件链每个事件增加 `conflict_layers`（冲突层次：external/internal/interpersonal）。

### 3.4 pop-novel-prose-render（正文渲染/上色 ★NEW）

| Step | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Step 1 读入输入** | chXXX-设计包.md + 写作资产/文风DNA/{style}.md + 锚定章片段 | — | Step 2 |
| **Step 2 正文渲染** | 设计包 + context 中的文风DNA规则 | `正文/chXXX.md`（正文，含视角选择） | Step 3、qa |
| **Step 3 风格验证** | chXXX.md + 文风DNA原文 | 风格验证报告（P0禁句扫描 + 视角一致性 + 先否定再肯定频率检查） | — |
| **Step 4 最终输出** | chXXX.md（修正后） | `正文/chXXX.md`（含章末状态更新块） | qa |

> **核心约束：不碰剧情。** 不读 Canvas/plot、不验证设定、不判断角色出场是否合理。Design 说了这章发生什么 → 只管写好。
> 
> Render 消费 `写作资产/文风DNA/{书名}.md` 做风格对齐。
> 
> **新增验证：** Step 3 风格验证新增「视角一致性检查」与「先否定再肯定句式频率检查（P1→P0升级）」

### 3.5 pop-novel-qa（爽点质检）

| Step | 上游依赖 | 产出 | 下游消费者 |
|-|-|-|-|
| **Step 1**（大纲层） | act-XX.yaml + project.yaml#reader_profile | 大纲层 QC 报告（纯感受） | chapter-design(修改反馈) |
| **Step 2**（骨架层） | chXXX-设计包.md + reader_profile | 骨架层 QC 报告 | chapter-design(修改反馈) |
| **Step 3**（正文层） | 正文/chXXX.md + reader_profile + QC-renderer.md | 正文层 QC 报告（纯感受） | prose-render(修改反馈)、expert-writer Reflect 判定 |

> QC 产出**不做文件存档**，由用户自行决定是否保留。

### 3.6 pop-novel-deconstructor（拆书分析）

| Phase | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Phase 0** | {书名}.txt（来自 download-webnovel-txt） | `{书名}-Phase0-采样日志.md` | Phase 1 |
| **Phase 1** | Phase 0 采样日志 | `{书名}-Phase1-诊断报告.md` + 任务清单 | Phase 2 |
| **Phase 2** | 诊断报告 + 模板 (T1\~T7) | `{书名}-T1-力量体系规则手册.md` \~ `T7-文风DNA指纹.md` × 7 | Phase 3、bookstrap Phase 0.6 |
| **Phase 3** | T1\~T7 | `{书名}-Phase3-验证报告.md` | Phase 4 |
| **Phase 4** | 全部 T 文件 + Phase 0/1/3 | `{书名}-三维拆书档案.md` + `{书名}-卷1起点快照.md` + `{书名}-卷1终点快照.md` | bookstrap Phase 0.6 |

### 3.7 pop-dna（文风DNA蒸馏）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **取样** | 全文 TXT / 章节文件 | 采样清单 | Step 1 |
| **精读** | ≥20 章原文（≥10,000行） | 逐章精读笔记（临时） | Step 2 |
| **全书搜索验证** | 精读笔记 + 全文搜索 | 验证记录（临时） | Step 3 |
| **产出风格文件** | 所有精读 + 验证数据 | `写作资产/文风DNA/{书名}.md` | prose-render Step 1 |
| **试写验证** | 写作资产/文风DNA/{书名}.md | 300-500字试写 | — |

### 3.8 download-webnovel-txt（TXT下载）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Step 1-3** | 书名 | `{书名}.txt`（GB18030→UTF-8 转码） | deconstructor Phase 0 |
| **Step 4** | {书名}.txt | 质量验证结果（HTML检查/章节数/内容量） | — |

### 3.9 pop-novel-html-renderer（HTML发布）

| 阶段 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **NodeF 决策** | doc_type + audience + goal | 设计系统决议 | render 阶段 |
| **渲染** | 正文/设定结构化数据 + style_profile + reader_profile | `宣传/{产出名}.html` | 读者/编辑 |

---

## 四、跨 Skill 共享文件清单

> 每条标注文件类型：**S**-静态（一次产出，只读不写）/ **D**-动态（持续维护，有更新者）/ **M**-元数据（工程索引）

### 4.1 核心共享文件（被 ≥2 个 Skill 消费）

| 文件 | 类型 | 产出者 | 消费者 | 用途 |
|-|-|-|-|-|
| **story-engine.yaml** | S | bookstrap Phase 0 | plot | 故事引擎——plot 内化拆成每卷核心命题。chapter-design 不直接读 |
| **L1-01\~06 六件套** | S | bookstrap Phase 1 | plot | 元设定层，plot 做幕设计时引用。chapter-design 不直接读 |
| **project.yaml** | M | bookstrap Phase 3 | expert-writer 路由 | 项目配置文件——reader_profile、paths、平台。子skill不读 |
| **状态/角色/{角色名}-角色卡.md** | **D** | bookstrap Phase 3 → plot 卷间回写 | plot（core_desire→volume角色池）+ chapter-design 参考 | 含 per-volume 快照段。初版bookstrap → 卷末plot回写（基于entity-snapshot） |
| **状态/势力/{势力名}.md** | **D** | plot 卷间回写 | plot（volume势力动机→状态）+ expert-writer 参考 | 渗透阶段/规模/关键事件 |
| **状态/卷摘要/volume-XX-摘要.md** | **D** | plot 卷末写入 | expert-writer + 人 | 一章一句话，约5KB/卷 |
| **状态/世界状态.md** | **D** | plot 卷间更新 | plot + chapter-design 参考 | 领土/裂缝/城市所有权跨卷追踪 |
| **起点快照.md** | S | bookstrap Phase 6 | plot Step 2 | 卷开始时主角/世界状态。chapter-design 不读源头 |
| **终点快照.md** | S | bookstrap Phase 7 / deconstructor | plot Step 2 | 卷结束时目标状态。chapter-design 不读源头 |
| **卷设计/volume-XX.md** | S | plot Step 4.5 | chapter-design Step 1 | **核心卷级输入**——角色池/地点池/剧情线/势力动机 |
| **幕设计/act-XX.yaml** | **D** | plot Step 9 | chapter-design (核心输入), qa(大纲层) | 幕级章纲——情绪弧线、爽点分布、Canvas矩阵。**§info_release_plan 段内嵌信息释放规划**，chapter-design 从每章 chapters[].info_release 取字段 |
| **entity-snapshot.yaml** | **D** | chapter-design (逐章更新) | chapter-design (下章读before状态), expert-writer Reflect L2 | 角色 current 状态、event_log 累积。逐章唯一的数字权威来源 |
| **chXXX-设计包.md** | **D**（每章新建） | chapter-design Step 3 | prose-render Step 1 | 回合级事件链 + 角色状态（含冲突层次/信息释放） |
| **正文/chXXX.md** | **D**（每章新建） | prose-render Step 4 | qa + html-renderer + expert-writer | 完成正文 + 章末状态更新块 |
| **写作资产/文风DNA/{书名}.md** | S | deconstructor / pop-dna | prose-render Step 1 | 文风DNA档案 |

### 4.2 可选/增强共享文件

| 文件 | 类型 | 产出者 | 消费者 | 用途 |
|-|-|-|-|-|
| **combat_capability.yaml** | **S** | bookstrap Phase 5 | plot Step 7/9, chapter-design (战斗章) | 段位战力范围 |
| **monster_rank_map.yaml** | **S** | bookstrap Phase 5 | chapter-design (怪物出场时) | 怪物等级对照 |
| **act_rank_schedule.yaml** | **S** | bookstrap Phase 5 | plot Step 9 | 卷级段位排期 |
| **collision_curve.yaml** | **S** | bookstrap Phase 5 | plot Step 9 | 碰撞曲线/战斗章分布 |
| **deconstruct-融合摘要.md** | **S** | bookstrap Phase 0.6 | plot (增强) | 参考书拆解融合摘要 |
| **T1\~T7 拆解报告** | **S** | deconstructor Phase 2 | bookstrap Phase 0.6, plot(增强) | 参考书拆解成果 |
| **{书名}-卷1起点/终点快照** | **S** | deconstructor Phase 4 | bookstrap Phase 0.6 | 参考书卷1结构参考 |
| **锚定章库/** | **D** | （用户预设） | prose-render Step 1 | 场景类型锚定章 |

### 4.3 调度层私有文件

| 文件 | 读写者 | 用途 |
|-|-|-|
| **workspace-index.yaml** | expert-writer 独占 | 全局索引——项目列表、参考素材、风格档案、运行时状态、跨项目经验、管线进度、文件注册表 |
| **ROUTE-AUGMENT.md** | expert-writer (§3.1.5) | 路由增强映射表——不直接读写，作为规则加载 |

---

## 五、管线调度与索引体系

### 5.1 expert-writer 调度数据流

```
每次用户消息
    │
    ▼
§0 全局感知
    │  workspace-index.yaml
    │  ├─ projects[].phase (决定当前阶段)
    │  ├─ runtime.execution_mode (主agent/子agent)
    │  └─ cross_project_lessons (跨项目经验)
    ▼
§3.1 Think
    │  entity-snapshot._meta.total_chapters (确定进度)
    │  progress.next_skill (闸门路由)
    │  references/think-*.md (审视框架)
    ▼
§3.1.5 信息增强
    │  ROUTE-AUGMENT.md → 从 workspace-index.yaml 提取
    │  对应路由目标的增强信息（路径引用）
    ▼
§3.1.6 管道前置校验
    │  pipeline_deps.{路由目标}
    │  ├─ required (缺失→停止)
    │  └─ recommended (缺失→警告)
    ▼
§3.2 Execute → 路由子 Skill
    ▼
§3.3 Reflect
    │  references/reflection.md (四层审视)
    │  L1: 产出检查 + workspace-index.yaml 索引回写
    │  L2: entity-snapshot ↔ L3 角色卡一致性
    │  L3: QA 报告判断 (P0/P1/P2)
    │  L4: 活人感检查 (可选)
    ▼
完成后引导 (基于文件实际状态)
```

### 5.2 管线进度回写协议

```
chapter-design Step 3 完成后 → 自动更新:
  workspace-index.yaml#file_registry
    └─ [项目].active → 注册 chXXX-事实骨架.md + chXXX-登场人物卡.md
    └─ [项目].entity-snapshot → 更新版本号

prose-render Step 5 完成后 → 自动更新:
  workspace-index.yaml#file_registry
    └─ [项目].active → 注册新 chXXX.md
    └─ [项目].pre_read_status → 更新 verified 状态

Expert-writer Reflect L1 → 自动更新:
  workspace-index.yaml#progress
    └─ last_completed_skill: "pop-novel-prose-render"
    └─ last_completed_phase: "Step 5"
    └─ next_skill: "pop-novel-qa"
    └─ checkpoints.正文_exists: true

  workspace-index.yaml#runtime
    └─ last_session → 记录本轮回话摘要

  workspace-index.yaml#projects[]
    └─ current_chapter → +1
```

---

## 六、典型路径速查

| 场景 | 管线路径 | 关键闸门 |
|-|-|-|
| **新书启动** | bookstrap FWD → plot → chapter-design → prose-render → qa | story-engine确认 / 起终点快照确认 / 场景卡确认 |
| **拆解参考书** | download-webnovel-txt → deconstructor | TXT 质量验证 / 锚定章确认 |
| **拆书+文风** | download-webnovel-txt → deconstructor → pop-dna | — |
| **调研后开书** | cnovel-research → bookstrap → plot → design → render → qa | — |
| **已有项目续写** | bookstrap REV → plot → chapter-design → prose-render → qa | 精读闸门 (pre_read_status) |
| **正文修改（骨架级）** | chapter-design → prose-render → qa | 不改剧情只改骨架编排 |
| **正文修改（渲染级）** | prose-render → qa | 只改措辞/修辞/文风 |
| **设定修改** | bookstrap → plot → chapter-design → prose-render | 逐层评估连锁影响 |
| **文风分析→应用** | pop-dna → prose-render (携带 style 参数) | style_executed 验证 |
| **发布网页** | (任意阶段) → pop-novel-html-renderer | NodeF 设计决策 |
| **互动文游** | (设定完成后) → pop-novel-game | 资料解析完成 |

---

## 附录 A：项目文件全貌模拟（第7卷）

> 假设：800章 / 7卷 / 每卷3-6幕 / 按改良后PRD的S/D/M分类标注  
> 标注方式：`[产出者]{类型}(规模)`

```
深渊主宰·外神低语/
│
├── 00-总控/                           ← 工程层，expert-writer 路由 + chapter-design 读写
│   ├── project.yaml                  [bookstrap] {M}  项目配置（paths/平台/reader_profile）
│   ├── entity-snapshot.yaml          [chapter-design] {D}  逐章微状态快照（800章log累计，约200KB）
│   └── 数值体系/                     [bookstrap] {S}  plot + 战斗章 chapter-design 消费
│       ├── combat_capability.yaml
│       ├── monster_rank_map.yaml
│       ├── act_rank_schedule.yaml
│       └── collision_curve.yaml
│
├── 00-原始设定/                       ← bookstrap 静态产出，仅 plot 消费
│   ├── L0-产品层/
│   │   ├── story-engine.yaml         [bookstrap] {S}  核心假说
│   │   ├── deconstruct-融合摘要.md    [bookstrap] {S}  参考书融合
│   │   └── PRD.md                    [用户] {S}  可选
│   ├── L1-元设定层/
│   │   ├── 01-世界蓝图.md ~ 06-资源物品.md  [bookstrap] {S}  6个文件
│   ├── 起点快照.md                   [bookstrap] {S}  第1章开篇状态
│   └── 终点快照.md                   [bookstrap] {S}  目标终局（全书级，各卷终点在volume-XX内）
│
├── 状态/                             ← 全书跨卷动态追踪 {D}  [bookstrap初版 → plot卷间回写]
│   ├── 角色/                          ← 含 per-volume 快照段
│   │   ├── 索伦-主角卡.md            ← 满配（身份/欲望/能力/关系/快照）约40KB
│   │   ├── 薇薇安-配角卡.md
│   │   ├── 歌莉娅-配角卡.md
│   │   ├── 阿拉丁-配角卡.md
│   │   └── 龙套池.md                ← 出场≤5章的角色（纯备忘）
│   │
│   ├── 势力/                         ← 从 volume 势力动机 + entity-snapshot 反哺
│   │   └── 外神教团.md               ← 渗透阶段/规模/已知情报/关键事件
│   │
│   ├── 卷摘要/                       ← plot 在卷末写入（一章一句话 → 约5KB/卷）
│   │   ├── volume-01-摘要.md
│   │   ├── volume-02-摘要.md
│   │   └── ...(~7个)
│   │
│   └── 世界状态.md                   ← 跨卷领土/裂缝/关键城市状态（约3KB）
│
├── 设计/                             ← plot 产出层
│   ├── 全书架构.md                   [plot Phase 0] {S+D}  全卷蓝图（卷间可修订）
│   │
│   ├── 卷/                           [plot Step 4.5] {S}  每卷1个
│   │   ├── volume-01.md             ← ch001-080：琥珀城逃亡篇
│   │   ├── volume-02.md             ← ch081-200：白马城立足篇
│   │   ├── volume-03.md             ← ch201-350：荒野远征篇
│   │   ├── volume-04.md             ← ch351-500：海外群岛篇
│   │   ├── volume-05.md             ← ch501-630：裂缝探索篇
│   │   ├── volume-06.md             ← ch631-720：诸神黄昏篇
│   │   └── volume-07.md             ← ch721-800：终局决战篇
│   │
│   └── 幕/                           [plot Step 9] {D}  按卷分组，卷内编号
│       ├── vol-01/
│       │   ├── act-01.yaml
│       │   ├── act-02.yaml
│       │   └── act-03.yaml
│       ├── vol-02/
│       │   ├── act-01.yaml
│       │   ├── act-02.yaml           ← info_release_plan 段已内嵌于每个act
│       │   ├── act-03.yaml
│       │   └── act-04.yaml
│       ├── ...
│       └── vol-07/
│           ├── act-01.yaml
│           ├── act-02.yaml
│           └── act-03.yaml
│
├── 写作资产/                          ← chapter-design + prose-render 共用
│   ├── 设计包/                        [chapter-design] {D}  每章1个（约800个文件，~16MB）
│   │   ├── ch001-设计包.md
│   │   ├── ch002-设计包.md
│   │   ├── ...
│   │   └── ch800-设计包.md
│   ├── 文风DNA/                       [deconstructor/pop-dna] {S}
│   │   └── 深渊主宰-文风DNA档案-v3.md
│   └── 锚定章库/                      [用户/写作中积累] {D}
│       ├── 战斗锚定-001.md
│       └── 对话锚定-001.md
│
├── 正文/                              ← prose-render 产出 {D}  每章1个（约800个文件，~60MB）
│   ├── ch001.md
│   ├── ch002.md
│   ├── ...
│   └── ch800.md
│
└── _参考书分析/                       ← deconstructor 产出 {S}  开书后锁定
    ├── 深渊主宰-T1-力量体系规则手册.md
    ├── 深渊主宰-T2-世界观展开.md
    ├── ... (T3~T6)
    ├── 深渊主宰-三维拆书档案.md
    ├── 深渊主宰-卷1起点快照.md
    ├── 深渊主宰-卷1终点快照.md
    └── 跨域素材蒸馏.md                [bookstrap Phase 0.5]
```

### 文件统计

| 层级 | 文件数 | 说明 |
|-|-|-|
| 总控 | \~6 | project(1) + entity-snapshot(1) + 数值体系(4) |
| 原始设定 | \~11 | L0(3) + L1(6) + 起点快照(1) + 终点快照(1) |
| 状态 | \~10 | 角色(4-5) + 势力(1) + 卷摘要(7) + 世界状态(1) |
| 设计 | \~38 | 全书架构(1) + 卷(7) + 幕(31 act，info_release 内嵌) |
| 写作资产 | \~800 | 设计包(800) + 文风DNA(1) + 锚定章(5-10) |
| 正文 | \~800 | 每章1个 |
| 参考书分析 | \~10 | 开书后锁定 |
| **全书总计** | **\~1665个文件** | **\~80MB（纯文本）** |

### 简化后消除的文件

| 旧版文件 | 消除原因 | 节省 |
|-|-|-|
| constitution.yaml | Canvas字段已覆盖 | 1个文件 |
| act-XX-人物/地图/势力/装备 ×124 | L3角色卡+volume+act字段已替代 | 124个文件 |
| info-release-XX.md ×31 | 合并到 act-XX.yaml#info_release_plan 段 | 31个文件 |
| chXXX-事实骨架.md + 登场人物卡.md | 合并为设计包单文件 | 约800个文件 |
| **合计节省** |  | **\~956个文件** |

---

## 附录 B：拆分前后对照

| 维度 | 旧版 pop-novel-writer (v15.0) | 新版 (v1.0 拆分) |
|-|-|-|
| **Design 产出** | `chXXX-design.md`（八块：A\~H） | `chXXX-事实骨架.md` + `chXXX-登场人物卡.md` |
| **Render 输入** | 读取 Canvas/plot + 直接读 L1 设定 | 只读骨架 + 人物卡，不碰上游 Canvas |
| **entity-snapshot 更新** | writer Step 3 负责 | chapter-design Step 3 负责 |
| **State Update** | 独立 Step 3（零 LLM） | 合并到 chapter-design 的 Step 3 |
| **文风锚定** | writer Step 2 Phase 1 | prose-render Phase 1 |
| **章节状态更新块** | writer Step 2 产出 | prose-render Step 5 产出（正文末尾） |
| **核心约束** | 无严格隔离 | **Design 不碰文风** / **Render 不碰剧情** |
| **向上依赖** | 依赖 plot 全部 Canvas | Design 依赖 plot Canvas；Render 只依赖 Design |

---

## 附录 C：全局文件审计 v1（2026-06-11）

> 问题驱动：L3角色卡丢失 → 发现缺乏全局文件视图  
> 核心问题：哪些文件是静态的？哪些是动态的？谁在维护？谁在消费？Agent 和人各怎么用？

### C.1 分类框架

| 维度 | 含义 |
|-|-|
| **S-静态** | 产出后不改，只做参考。产出者写一次，消费者只读不写。 |
| **D-动态** | 随写作进展持续更新。有明确的维护者和更新时机。 |
| **M-元数据** | 描述结构/索引/路径。不属于内容层，属于工程层。 |

| 消费方 | 含义 |
|-|-|
| **🤖 Agent** | Skill 执行时读取。需要结构化、路径明确、字段无歧义。 |
| **👤 人** | 用户通读/审阅。需要可读、可快速扫描、关键信息突出。 |
| **🤖+👤** | 两者都读。格式需兼顾——结构化但不牺牲可读性。 |

### C.2 各产出区逐文件审计

#### C.2a bookstrap 静态产出

| 文件 | 类型 | 消费者 | 消费模式 | 现状 |
|-|-|-|-|-|
| story-engine.yaml | S | plot | 内化→拆成每卷核心命题。chapter-design不读 | ✅ |
| L1-01\~06 | S | plot | plot做幕设计时引用设定素材。chapter-design不读 | ✅ |
| deconstruct-融合摘要.md | S | plot(增强) | 参考书提取的可复用规则 | ✅ |
| 起点/终点快照.md | S | plot | 拆成每卷 start/end 状态。chapter-design不读源头 | ✅ |
| 数值体系 x4 | S | plot+chapter-design(战斗章) | plot用act_rank_schedule排期；chapter-design战斗章查段位 | ❌ 实际没产出 |
| project.yaml | M | expert-writer | 路由用。子skill不读 | ✅ |

#### C.2b L3 角色卡（动态区）

| 文件 | 类型 | 产出→维护 | 消费者 | 现状 |
|-|-|-|-|-|
| 状态/角色/{主角}-主角卡.md | **D** | bookstrap初版 → **plot卷末回写** | plot(core_desire→volume)+chapter-design参考 | ❌ 维护链缺失 |
| 状态/角色/重要配角.md | **D** | 同上 | 同上 | ❌ 同上 |

**核心问题：** 角色卡不是静态的——索伦从"守护妹妹"到"接受世界不可预测"，薇薇安从"被保护者"到"独立强者"，欲望在中途会转向。当前没有定义谁在什么时候更新。建议维护链：bookstrap初版 → plot写下一卷 volume 前回写（基于 entity-snapshot 累积状态）。

#### C.2d plot 产出

| 文件 | 类型 | 消费者 | 现状 |
|-|-|-|-|
| 设计/幕/act-XX.yaml | D | chapter-design 核心输入 | ✅ 存在 |
| 设计/幕/info-release-XX.md | D | chapter-design | ✅ 存在 |
| **设计/卷/volume-XX.md** | **S** | **chapter-design 核心卷级输入** | **❌ 最严重缺失** |
| **设计/全书架构.md** | **S+D** | **volume-XX.md 的输入** | **❌ 不存在** |

#### C.2e chapter-design / prose-render 产出

| 文件 | 类型 | 现状 |
|-|-|-|
| 写作资产/设计包/chXXX-设计包.md | **D**（每章新建） | ⚠️ 仅ch01-02合并，ch03-10仍是旧双文件 |
| 00-总控/entity-snapshot.yaml | **D**（逐章追加） | ✅ 但 total_chapters 未更新 |
| 正文/chXXX.md | **D**（每章新建） | ✅ ch01-10 存在但字数不达标 |

### C.3 总控层审计

#### workspace-index.yaml

| 职责 | 现状 | 问题 |
|-|-|-|
| 项目列表+phase追踪 | ✅ | — |
| 文件注册表(confirmed/active/deprecated) | ⚠️ | L3角色卡、文风DNA、ch01-10设计包/正文未注册 |
| 跨项目经验 | ⚠️ | 有字段但无数据 |
| pre_read_status(精读闸门) | ❌ | verified=false 从未被推进 |
| progress 追踪 | ⚠️ | 只在Reflect时回写，日常不维护 |
| 全书架构注册位 | ❌ | 尚无字段 |

#### entity-snapshot.yaml

| 职责 | 现状 |
|-|-|
| 角色当前状态追踪 | ✅ 索伦/薇薇安/希斯 都有 |
| event_log 累积 | ✅ ch01-10 完整 |
| 版本号管理 | ⚠️ total_chapters=0 实际到ch10 |
| 与L3角色卡的桥接 | ❌ entity-snapshot 有数据，L3有解释，但两个文件不知道对方存在 |

### C.4 双消费视角

#### 🤖 Agent 友好文件

| 文件 | 原因 |
|-|-|
| act-XX.yaml | 结构化YAML，路径可预测 |
| entity-snapshot.yaml | 同上 |
| story-engine.yaml | YAML结构清晰 |
| 状态/角色/角色卡 | 结构化+YAML frontmatter |

#### ⚠️ Agent 不友好 → 建议

| 文件 | 问题 | 建议 |
|-|-|-|
| L1-01\~06 | 纯Markdown叙述，不易精确定位 | 顶部加YAML frontmatter 或信息索引表 |
| 起点/终点快照.md | 同上 | 顶部加YAML摘要段 |
| 状态/角色/角色卡 | 表格+叙述混合，搜索core_desire需全文 | core_desire固定在第一节YAML块中 |
| chXXX-设计包.md | 事件链格式不统一（部分合并部分未合） | 统一为设计包单格式 |

#### 👤 人友好文件

| 文件 | 原因 |
|-|-|
| 起点/终点快照.md | 表格+叙述，扫一眼看完全书 |
| 状态/角色/主角卡.md | 九节结构化，信息密度高可读 |
| 正文/chXXX.md | 最终消费品 |

#### ⚠️ 人不友好 → 建议

| 文件 | 问题 | 建议 |
|-|-|-|
| act-XX.yaml | YAML几可读性差 | 每章切片顶部加纯文本摘要段 |
| entity-snapshot.yaml | 纯数据无意义 | 每角色加 summary行 |
| workspace-index.yaml | 字段过载 | 顶部加人类可读状态摘要块 |

### C.5 核心发现摘要

#### 紧迫修正（影响当前写作质量）

| # | 问题 | 方案 |
|-|-|-|
| 1 | **volume-01.md 不存在**——chapter-design 无卷级角色池/地点池 | 产出 volume-01.md 反推 |
| 2 | **数值体系 4文件全缺**——升级节奏无结构性约束 | 产出 combat_capability + act_rank_schedule |
| 3 | **全书架构.md 不存在**——4卷蓝图缺位 | 新增 plot Phase 0 |
| 4 | **ch03-10 设计包未合并**——格式不统一 | 统一为设计包单文件 |

#### 结构补齐（影响后续卷展开）

| # | 议题 | 方向 |
|-|-|-|
| 5 | 角色卡维护链 | bookstrap初版（含快照段预留位）→ plot写下一卷 volume 前，基于 entity-snapshot 累积状态回写（更新 core_desire / 能力里程碑 / 关系变化，追加卷快照段）→ chapter-design 从状态/角色/取 core_desire，从 entity-snapshot 取微状态 |
| 6 | workspace-index 文件注册全覆盖 | 每完成一个产出，注册到 confirmed |

#### 已解决（v1.3）

| # | 议题 | 方案 |
|-|-|-|
| — | constitution.yaml | 整文件移除——canvas字段已覆盖（act 的 chekhov_set/combat.scale/payoff/plotlines_active 已够用） |
| — | act-XX-人物/地图/势力/装备 ×4 | 移除——L3角色卡+volume角色池+act字段已替代 |
| — | ch03-10 设计包未合并 | 统一为设计包单文件 |

#### 双消费改进（不紧急但积重难返）

| # | 议题 | 方向 |
|-|-|-|
| 9 | Agent友好度：Markdown文件加YAML摘要 | 所有Markdown产出文件顶部加YAML frontmatter |
| 10 | 人友好度：YAML文件加纯文本摘要 | act-XX.yaml和entity-snapshot加人类扫读摘要段 |

---

> **本文档通过实地读取以下 Skill 的 SKILL.md 和 Steps 构建：**  
> expert-writer, pop-novel-bookstrap, pop-novel-plot,  
> pop-novel-chapter-design, pop-novel-prose-render,  
> pop-novel-qa, pop-novel-deconstructor, pop-dna,  
> download-webnovel-txt, pop-novel-html-renderer,  
> workspace-index.yaml, ROUTE-AUGMENT.md

---

# 二、全链路优化方案

# 网文创作管线 · 全链路优化 PRD

> 范围：deconstructor / bookstrap / plot / writer 四个 Skill 的产出模板 + 消费链路  
> 根因分析基于 2026-06-09 的 ch06 复盘 + 三 Skill 产出对照 + 5 个结构性病灶诊断

---

## §0 诊断总论

### 第一性：管线每个产出物必须回答三个问题

| Q | 说明 | 当前通过率 |
|-|-|-|
| **谁来填？** | 哪个 Agent 在什么 Phase 填这个字段 | ✅ 大部分有 |
| **填完谁读？** | 下游哪个管线 Agent 消费这个字段 | ⚠️ \~60% |
| **怎么读？** | 格式是散文/结构化/枚举，Agent 能不能解析 | ❌ \~40% |

当前 5 个病灶的根因全在"填完谁读"和"怎么读"两个环节——不是模板不够多，是每个产出物不知道自己为谁服务。

### 通用改进原则

1. **每个模板文件头部必须有"消费方声明"**——不是在末尾加摘要。Agent 打开文件第一眼看到"这个文件的下游消费者是 X，X 需要从这里取 Y 字段"，而不是读完 2000 字才在末尾发现。消费摘要放在文件开头（## 消费方 / ## 被谁消费），2026年06月09日之前的所有产出模板均需要在文件开头补充消费声明。
2. **每个字段必须在同一行标注消费方**：`## 字段名 → 消费方: SkillName.Phase.X`
3. **Agent 可解析优先于人类可读**：如果下游 Agent 需要一个布尔值（`是否战斗章`），模板不应该产出散文段落。
4. **条件存在优于空占位**：如果某个模板维度对特定赛道不适用（如仙侠赛道不需要 T2 的"技术/文明设定"），模板必须标注 `（非仙侠赛道可跳过）`，而不是让它产生垃圾填空。

## §1 病灶清单 × 改造方案

### 病灶 1 — L1 设定层：散文格式导致下游 Agent 找不到字段入口

**根因**：Bookstrap Phase 1 产出的 L1-01/03/04 是全散文文件。下游 plot 需要"地理信息"时没有一个叫 `geography` 的字段——它被埋在"时空结构"段落里。Agent 扫描全篇靠语义匹配"这个地方叫什么"——不可靠。

**改造范围**：3 个 L1 文件

| L1 文件 | 改造 | 原因 |
|-|-|-|
| `01-世界蓝图.md` | 在文件开头加消费声明；时空结构段拆为两个子段：`### 地理总览（→ act-XX-地图.md）` + `### 位面/时间规则`；世界基调改为枚举值 `tone: "暗黑生存"` | 当前所有子字段为散文，plot/writer 无法提取地理信息和世界基调 |
| `03-历史与驱动力.md` | 在文件开头加消费声明；核心矛盾改为独立 YAML 块 `core_conflict: "秩序vs混沌"` | plot 的 act.core_conflict 需要直接引用这个值 |
| `04-物种与天赋.md` | 在文件开头加消费声明；种族列表改为每条 4 字段（name/traits/playable/faction_affiliation） | character-list 创建 NPC 需要种族数据做源 |

**消费声明格式**（每个 L1 文件开头）：

```yaml
<!--
@consumed_by: plot.Step7(act-XX-地图.md), writer.Step1(chXXX-design.md 块B)
@fields_used: 地理总览 → plot 地图初始锚点; 位面规则 → constitution 引注
@updated: bookstrap.Phase1 → 每卷回顾可追加新区域
-->
```

---

### 病灶 2 — Deconstructor 产出：自创分类系统 + 产出格式不对齐消费侧

**根因**：T2 的 8 段分类是 deconstructor 自己发明的——"社会结构""政治格局""经济体系"——而 bookstrap Phase 0.6 需要的维度名是 L1 的"势力格局""资源与物品"。Phase 0.6 在做翻译，但翻译规则没写在模板里。T4 的起点/终点快照字段少于 B Phase 6/7。T7 仍然是量化分析格式。

**改造范围**：3 个 T 模板

| T 模板 | 改造 |
|-|-|
| **T2 世界观展开** | 文件开头加消费声明。子节标题改为 L1 维度名。每个子节只在"拆解对象确实有该维度内容时才产出"，不可空写。删除"技术/文明设定"独立节——在 DND 中世纪赛道无产出，改为含在"世界蓝图"段内<sup>（可选）</sup> |
| **T4 剧情全貌** | 文件开头加消费声明。起点快照 + 终点快照 → 对齐 B Phase 6/7 的字段结构（补"关系状态"段 + "读者感受"段）。已在拆解测试中发现 B 比 D 多 2 个字段 |
| **T7 文风DNA** | 文件开头加消费声明。从"8 维量化分析"重写为"按场景类型组织原文片段"——格式对齐刚重写的 abyss.md。删除：定量分析句（"便"44次、平均句长 34.4……）、优先级分级（P0/P1/P2） |

**消费声明格式**（以 T2 为例）：

```yaml
<!--
@consumed_by: bookstrap.Phase0.6(拆书成果融合) → L1-01/04/05/06
@fields_forwarded:
  势力格局段 → L1-05 势力格局 (势力列表+对抗关系)
  物种与天赋段 → L1-04 物种与天赋 (种族数据)
  资源与物品段 → L1-06 资源与物品 (货币/修炼资源)
  地理总览段 → plot.act-XX-地图.md (地图展开顺序+位面结构)
  信息释放时间表 → plot.info-release-XX.md (释放节奏参考)
-->
```

---

### 病灶 3 — 中游断链：数据存在但管线 Agent 不读取

**根因**：不是上游没产出，是下游 Agent 的输入列表里没包含这个文件路径。`combat_capability.yaml` 和 `monster_rank_map.yaml` 产出但 writer 不读。T5 产出但 plot 没有引用 T5 的字段。`source_doc` 路径格式无统一校验。

**改造范围**：3 个文件

| 文件 | 改造 |
|-|-|
| **expert-writer `ROUTE-AUGMENT.md`** | 为 plot 补充"预取 T4(双主线/节奏规律) + T5(高潮分布密度)"条目；为 writer 补充"预取 combat_capability.yaml + monster_rank_map.yaml + L1-04 对应种族条目"条目 |
| **plot `templates/act-guide.md`** | combat 段加 `capability_ref`（指向 combat_capability.yaml 对应条目）和 `monster_ref`（指向 monster_rank_map.yaml 对应条目）；新增 `rhythm_reference` 块声明"如有 T5 产出，读其高潮分布/张力值参考上限" |
| **writer `steps/step-1-design.md`** | 输入表增加：`combat_capability.yaml`（战斗章读）、`monster_rank_map.yaml`（涉及怪物时读）、L1-04 种族条目（非人类角色出场时读） |

---

### 病灶 4 — 渲染层：T7 和 abyss.md 不同步

**根因**：writer v14 重写了 abyss.md（从规则提取→原文片段集），但 deconstructor T7 模板还是旧的量化分析格式。产出的 T7 不能直接用作 styles/abyss.md。

**改造范围**：1 个文件

| 文件 | 改造 |
|-|-|
| **deconstructor `T7-文风DNA模板.md`** | 完全重写。从"8 维量化分析 + 写前规则"改为"按 4 类场景组织原文片段（战斗/对话/发现/危机）"。每个场景选 1-3 段原文。保留红线清单（7 条，已和 abyss.md 对齐） |

**新建文件**：`styles/abyss.md` 格式作为 T7 产出的标准格式。T7 产出 = 直接复制到 `styles/` 目录的"即用文件"。

---

### 病灶 5 — 命名空间不统一 + 跨 Skill 同名歧义

**根因**：T2 "政治格局" vs L1 "势力格局" vs plot "活跃势力" — 同一概念三个名字。T4 的 M1 是"锚点书分析" vs act-guide 的 M1 是"目标书设计" — 同名不同源。B `[主角]` 标签 vs D T3 独立模板 — 两种金手指组织方式互不引用。

**改造范围**：3 个变动

| 变动 | 内容 |
|-|-|
| **统一术语表** | 在项目根 `d:\popwave-skills\` 下新增 `_shared/terminology.yaml`，提供 12 个核心概念的权威名称（M1/势力/种族/资源/力量体系/Act/爽点/钩子……）。所有 Skill 引此表。一页 12 行。 |
| **B phase-0.6.pe.md** | 新增 step："读 T4 的 M1/M2 定义 → 用自己的 story-engine 重写本项目的 M1/M2。只继承节奏规律（密度/露出方式），不继承具体事件。" |
| **D T2/T3/T4 标题** | 子节标题对齐术语表。`政治格局`→`势力格局`。`种族体系`→`物种与天赋`。`经济体系`映射拆为`资源与物品`内的子段。 |

## §2 实施顺序

| 顺序 | 文件 | 新/改 | 预估行数 |
|-|-|-|-|
| 1 | **新建**`_shared/terminology.yaml` | 新 | 15 |
| 2 | Bookstrap `phases/phase-1.pe.md` — L1-01/03/04 增加消费摘要字段格式 | 改 | 60 |
| 3 | Deconstructor `templates/T2-世界观展开模板.md` — 标题对齐 + 消费声明 | 改 | 40 |
| 4 | Deconstructor `templates/T4-剧情全貌模板.md` — 快照对齐 + 消费声明 | 改 | 30 |
| 5 | Deconstructor `templates/T7-文风DNA模板.md` — 重写为原文片段集 | 重写 | 160 |
| 6 | Expert-writer `ROUTE-AUGMENT.md` — 补中游断链映射 | 改 | 30 |
| 7 | Plot `templates/act-guide.md` — combat 增加 capability_ref/monster_ref + rhythm_reference | 改 | 25 |
| 8 | Writer `steps/step-1-design.md` — 输入增加数值体系/L1-04 | 改 | 15 |
| 9 | Bookstrap `phases/phase-0.6.pe.md` — 增加 M1/M2 转译 step | 改 | 15 |

总计：1 新建 + 7 修改 + 1 重写。\~

所有改动不涉及管线架构变更——保持 deconstructor → bookstrap → plot → writer → qa 的现有流程。

## §3 验收标准

每个模板在提交前回答：

- [ ] 文件开头是否有消费方声明（`@consumed_by`）？

- [ ] 每个字段是否有下游消费路径（不落空）？

- [ ] Agent 能否直接解析该字段（不用语义猜测）？

- [ ] 有赛道条件判断的字段是否标注了"可跳过"？

- [ ] 名称是否与 `_shared/terminology.yaml` 对齐？

## §4 附录：翻车复盘

**ch06 三次迭代的体验教训**：

| v# | 问题 | 对应病灶 |
|-|-|-|
| v1(旧) | 空间无定义→虚空打架。人设无底线→小喽啰死不死摇摆 | 病灶 3（管线断链：writer 没读 canvas） |
| v2(重构) | 面板在 beat5 丢失 | 病灶 4（渲染层读了量化规则没读原文，记不住"数据嵌入动作中"） |
|  | 单章塞了 combat + crisis 两件事 | 病灶 5（plot 层 M1/M2 分配无下游约束——信息密度超载） |
| v3(最终) | 小喽啰真被打断骨头。文风接近深渊主宰。 | 病灶 4 修复（原文片段替换量化规则）生效 |

**核心教训**：不要相信 Agent 能"凭感觉"写出目标小说的质感。它需要原文片段的直接向量，不是抽象规则翻译。不要相信 Agent 能"猜到"下游需要什么数据——模板必须显式标注消费路径。