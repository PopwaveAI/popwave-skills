# 写作专家全链路 — 文件依赖与产出全景 PRD

> 版本：v1.1 | 2026-06-10
> 更新说明：拆分 `pop-novel-writer` 为 `pop-novel-chapter-design`（设计环节）+ `pop-novel-prose-render`（正文渲染环节），全线更新依赖关系
> 说明：本文档展示 popwave 写作全链路的完整管线结构，每个节点标注上游依赖文件、下游产出文件、以及跨 skill 共享的关键文件。

---

## 目录

- [一、全链路总览图](#一全链路总览图)
- [二、Skill 管线流程](#二skill-管线流程)
- [三、各 Skill 详细文件依赖表](#三各-skill-详细文件依赖表)
- [四、跨 Skill 共享文件清单](#四跨-skill-共享文件清单)
- [五、管线调度与索引体系](#五管线调度与索引体系)
- [六、典型路径速查](#六典型路径速查)

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
   │  产出: T1~T7 + 采样日志 + 诊断报告 + 验证报告        │
   │         + 卷1起点/终点快照 + 三维拆书档案             │
   └──────────┬──────────┬──────────────────────────────┘
              │          │
              │          ▼
              │    ┌──────────────────┐
              │    │    pop-dna       │
              │    │  文风DNA蒸馏     │
              │    │  产出: styles/   │
              │    │  {书名}.md       │
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
              │       + constitution.yaml + project.yaml
              │       + 数值体系 x4 + 起点/终点快照
              ▼
   ┌─────────────────────────────────────────────────────┐
   │               pop-novel-plot                         │
   │              剧情架构 (Step 1→12)                    │
   │  输入: story-engine.yaml + 起点/终点快照              │
   │        + constitution.yaml + L1-01~06                │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: act-XX.yaml + 人物/地图/势力/装备
              │       + info-release + 里程碑 + 节奏自检
              ▼
   ┌─────────────────────────────────────────────────────┐
   │           pop-novel-chapter-design  ★NEW             │
   │          章纲/导演卡 (Step 1→3)                      │
   │  输入: act-XX.yaml + 人物/地图/势力/装备              │
   │        + info-release + entity-snapshot + 里程碑      │
   │  ⚠️ 不碰文风 — 只产出事件骨架                         │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: chXXX-事实骨架.md + chXXX-登场人物卡.md
              │       + entity-snapshot.yaml (更新)
              ▼
   ┌─────────────────────────────────────────────────────┐
   │           pop-novel-prose-render  ★NEW               │
   │          正文渲染/上色 (Step 1→5)                     │
   │  输入: 事实骨架 + 登场人物卡 + styles/{style}.md      │
   │  ⚠️ 不碰剧情 — 只管写好                             │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: chXXX.md (含章末状态更新块)
              ▼
   ┌─────────────────────────────────────────────────────┐
   │               pop-novel-qa                           │
   │              爽点质检 (Step 1→3)                     │
   │  输入: constitution.yaml + 正文 + reader_profile      │
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
  ├─ Phase 3:     project.yaml + constitution.yaml + L3角色卡
  ├─ Phase 4:     reader_profile 校对
  ├─ Phase 5:     数值体系 x4
  ├─ Phase 6:     起点快照.md
  └─ Phase 7:     终点快照.md  [用户确认闸门 → 进入 plot]
  ↓
Step 2 · pop-novel-plot (剧情架构)
  ├─ Step 1:  前置 + 节点B → 节点B-XX.md
  ├─ Step 2:  锚点确认 (口述)
  ├─ Step 3:  里程碑 → 里程碑设计.md [用户确认闸门]
  ├─ Step 4:  情节线 → 情节线草案-XX.md [用户确认闸门]
  ├─ Step 5:  人物 → act-XX-人物.md
  ├─ Step 6:  地图 → act-XX-地图.md
  ├─ Step 7:  世界 → act-XX-势力.md + act-XX-装备.md
  ├─ Step 8:  info_release → info-release-XX.md
  ├─ Step 9:  幕纲 → act-XX.yaml  [核心产出]
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
  ├─ Phase 1:  风格锚定 ⬅ 读 styles/{style}.md → 风格契约
  ├─ Phase 2:  正文渲染 — 事件链 × 风格契约 → chXXX.md
  ├─ Phase 3:  风格验证 — P0禁句扫描 + 调音叉对照
  └─ → 章末状态更新块
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
  ├─ Phase r4: 宪法提取 (constitution.yaml)
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
  → 均匀采样 ≥20 章 → 全书搜索验证 → styles/{书名}.md
```

---

## 三、各 Skill 详细文件依赖表

### 3.1 pop-novel-bookstrap（开书设定）

| Phase | 上游依赖（输入） | 产出文件 | 下游消费者 |
|-------|-----------------|---------|-----------|
| **Phase 0** | — | `L0-产品层/story-engine.yaml` | Phase 1、plot、chapter-design |
| **Phase 0.3** | — | 参考书清单（口述） | Phase 0.5 |
| **Phase 0.4** | — | 金手指设计（口述+记录） | Phase 0.5 |
| **Phase 0.5** | Phase 0.3 + 0.4 产出 | 跨域素材聚合摘要 | Phase 0.6 |
| **Phase 0.6** | deconstructor 的 T1~T7（如有锚点书） | `L0-产品层/deconstruct-融合摘要.md` | Phase 1 |
| **Phase 1** | story-engine.yaml | `L1-元设定层/01-世界蓝图.md` ~ `06-资源物品.md` | Phase 1.2 / 1.3 / plot |
| **Phase 1.2** | L1-01~06 | L1 各文件深度展开补充 | Phase 1.3 |
| **Phase 1.3** | L1-01~06 (深度展开) | `_交叉引用记录.md` | Phase 1.5 |
| **Phase 1.5** | L1-01~06 + 交叉引用 | 稳定性检验 checklist | — |
| **Phase 3** | L1-01~06 | `project.yaml` + `constitution.yaml` + `L3-角色层/角色卡`（含 core_desire: external_goal + internal_need） | plot、chapter-design、qa |
| **Phase 4** | project.yaml | reader_profile 校对确认 | plot、chapter-design、qa |
| **Phase 5** | L1-01~06 + constitution | `combat_capability.yaml` + `monster_rank_map.yaml` + `act_rank_schedule.yaml` + `collision_curve.yaml` | plot、chapter-design |
| **Phase 6** | story-engine + 起点状态 | `设计/起点快照.md` [用户确认闸门] | plot (Step 2 锚点) |
| **Phase 7** | story-engine + 终点构想 | `设计/终点快照.md` [用户确认闸门] | plot (Step 2 锚点)、chapter-design |
| **Phase r1** | 已有正文文件（N章） | `事件日志.md` + 批次摘要 | Phase r2 |
| **Phase r2** | 事件日志 | `L0-产品层/` 提取文件 | Phase r3 |
| **Phase r3** | L0 提取 | `L1-元设定层/` 提取文件 | Phase r4 |
| **Phase r4** | L1 提取 | `constitution.yaml` | Phase r5 |
| **Phase r5** | constitution.yaml | 卷大纲确认 | Phase r6 |
| **Phase r6** | 全部 reverse 产出 | `交接验证报告.md` | plot |

### 3.2 pop-novel-plot（剧情架构）

| Step | 上游依赖 | 产出文件 | 下游消费者 |
|------|---------|---------|-----------|
| **Step 1** | story-engine.yaml + 起点/终点快照 + constitution.yaml + L1-01~06 | `设计/幕/节点B-XX.md` | — |
| **Step 2** | 起点/终点快照 | 锚点确认（口述） | Step 3 |
| **Step 3** | 锚点确认 | `设计/里程碑设计.md` [用户确认闸门] | Step 4 |
| **Step 4** | 里程碑设计 | `设计/幕/情节线草案-XX.md` [用户确认闸门] | Step 5-9 |
| **Step 5** | L3-角色卡 + combat_capability | `设计/幕/act-XX-人物.md` | chapter-design |
| **Step 6** | L1-世界蓝图 | `设计/幕/act-XX-地图.md` | chapter-design |
| **Step 7** | L1-势力格局 + 资源物品 | `设计/幕/act-XX-势力.md` + `act-XX-装备.md` | chapter-design、info-release |
| **Step 8** | act-XX-人物/地图/势力/装备 + constitution | `设计/幕/info-release-XX.md` | chapter-design |
| **Step 9** | Steps 1-8 全部产出 | `设计/幕/act-XX.yaml` | chapter-design 核心输入 |
| **Step 10** | act-XX.yaml | `_temp/场景卡` [用户确认闸门] | — |
| **Step 11** | act-XX.yaml + act_rank_schedule | `设计/幕/节奏自检报告.md` | — |
| **Step 12** | 全部 Steps 1-11 产出 | —（校验不产出新文件） | — |

### 3.3 pop-novel-chapter-design（章纲设计/导演卡 ★NEW）

| Step | 上游依赖 | 产出文件 | 下游消费者 |
|------|---------|---------|-----------|
| **Step 1 读入上下文** | act-XX.yaml + volume-XX.md + info-release-XX.md + entity-snapshot.yaml + 里程碑设计.md + constitution.yaml + L3-角色卡(core_desire) | —（建立基线：角色池/地点池/信息清单/幕纲字段/场景规格/角色欲望） | Step 2 |
| **Step 2 事件链设计** | Step 1 基线 + references/ 四个参考文档 | —（逐个回合设计事件，同步确定角色/地点/情绪/信息释放/字数） | Step 3 |
| **Step 3 产出+状态** | Step 2 事件链 | `03-写作资产/chXXX-设计包.md`（含事实骨架+登场人物卡） | pop-novel-prose-render |
| | | `00-总控/entity-snapshot.yaml`（更新） | 下一章 design |

> **核心约束：不碰文风。** 不知道文风DNA的存在。不写叙事者声音、不写句子节奏、不写修辞风格。
>
> **硬性质量下限：** 事件数 ≥ 章字数 ÷ 200 — "靶心不够，Render 没材料"。
>
> **新增变更：** 事实骨架 + 登场人物卡合并为 `chXXX-设计包.md` 单文件。事件链每个事件增加 `conflict_layers`（冲突层次：external/internal/interpersonal）。

### 3.4 pop-novel-prose-render（正文渲染/上色 ★NEW）

| Step | 上游依赖 | 产出文件 | 下游消费者 |
|------|---------|---------|-----------|
| **Step 1 读入输入** | chXXX-事实骨架.md + chXXX-登场人物卡.md + styles/{style}.md + 锚定章片段 + 宪法 | — | Step 2 |
| **Step 2 正文渲染** | 事实骨架 + 登场人物卡 + context 中的 styles 规则 | `03-正文/chXXX.md`（正文，含视角选择） | Step 3、qa |
| **Step 3 风格验证** | chXXX.md + styles/ 原文 + 宪法 | 风格验证报告（P0禁句扫描 + 视角一致性 + 先否定再肯定频率检查 + 宪法检查） | — |
| **Step 4 最终输出** | chXXX.md（修正后） | `03-正文/chXXX.md`（含章末状态更新块） | qa |

> **核心约束：不碰剧情。** 不读 Canvas/plot、不验证设定、不判断角色出场是否合理。Design 说了这章发生什么 → 只管写好。
>
> Render 消费 pop-dna 产出的 styles/{书名}.md 做风格对齐。
>
> **新增验证：** Step 3 风格验证新增「视角一致性检查」与「先否定再肯定句式频率检查（P1→P0升级）」

### 3.5 pop-novel-qa（爽点质检）

| Step | 上游依赖 | 产出 | 下游消费者 |
|------|---------|------|-----------|
| **Step 1**（大纲层） | act-XX.yaml + project.yaml#reader_profile | 大纲层 QC 报告（纯感受） | chapter-design(修改反馈) |
| **Step 2**（骨架层） | chXXX-事实骨架.md + reader_profile | 骨架层 QC 报告 | chapter-design(修改反馈) |
| **Step 3**（正文层） | chXXX.md + reader_profile + QC-renderer.md | 正文层 QC 报告（纯感受） | prose-render(修改反馈)、expert-writer Reflect 判定 |

> QC 产出**不做文件存档**，由用户自行决定是否保留。

### 3.6 pop-novel-deconstructor（拆书分析）

| Phase | 上游依赖 | 产出文件 | 下游消费者 |
|-------|---------|---------|-----------|
| **Phase 0** | {书名}.txt（来自 download-webnovel-txt） | `{书名}-Phase0-采样日志.md` | Phase 1 |
| **Phase 1** | Phase 0 采样日志 | `{书名}-Phase1-诊断报告.md` + 任务清单 | Phase 2 |
| **Phase 2** | 诊断报告 + 模板 (T1~T7) | `{书名}-T1-力量体系规则手册.md` ~ `T7-文风DNA指纹.md` × 7 | Phase 3、bookstrap Phase 0.6 |
| **Phase 3** | T1~T7 | `{书名}-Phase3-验证报告.md` | Phase 4 |
| **Phase 4** | 全部 T 文件 + Phase 0/1/3 | `{书名}-三维拆书档案.md` + `{书名}-卷1起点快照.md` + `{书名}-卷1终点快照.md` | bookstrap Phase 0.6 |

### 3.7 pop-dna（文风DNA蒸馏）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|------|---------|---------|-----------|
| **取样** | 全文 TXT / 章节文件 | 采样清单 | Step 1 |
| **精读** | ≥20 章原文（≥10,000行） | 逐章精读笔记（临时） | Step 2 |
| **全书搜索验证** | 精读笔记 + 全文搜索 | 验证记录（临时） | Step 3 |
| **产出风格文件** | 所有精读 + 验证数据 | `styles/{书名}.md` | prose-render Phase 1 |
| **试写验证** | styles/{书名}.md | 300-500字试写 | — |

### 3.8 download-webnovel-txt（TXT下载）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|------|---------|---------|-----------|
| **Step 1-3** | 书名 | `{书名}.txt`（GB18030→UTF-8 转码） | deconstructor Phase 0 |
| **Step 4** | {书名}.txt | 质量验证结果（HTML检查/章节数/内容量） | — |

### 3.9 pop-novel-html-renderer（HTML发布）

| 阶段 | 上游依赖 | 产出文件 | 下游消费者 |
|------|---------|---------|-----------|
| **NodeF 决策** | doc_type + audience + goal | 设计系统决议 | render 阶段 |
| **渲染** | 正文/设定结构化数据 + style_profile + reader_profile | `宣传/{产出名}.html` | 读者/编辑 |

---

## 四、跨 Skill 共享文件清单

### 4.1 核心共享文件（被 ≥2 个 Skill 消费）

| 文件 | 产出者 | 消费者 | 用途 |
|------|-------|-------|------|
| **story-engine.yaml** | bookstrap Phase 0 | plot, chapter-design | 故事引擎——core_premise、主题、冲突方向 |
| **constitution.yaml** | bookstrap Phase 3 | plot, chapter-design, prose-render, qa | 写作宪法——世界规则、力量约束、角色行为守则 |
| **project.yaml** | bookstrap Phase 3 | plot(chapter-design增强), qa, chapter-design, html-renderer | 项目配置文件——reader_profile、paths、平台 |
| **L1-01~06 六件套** | bookstrap Phase 1 | plot (Steps 1-7), chapter-design | 元设定层——世界蓝图/力量体系/历史/物种/势力/资源 |
| **act-XX.yaml** | plot Step 9 | chapter-design (核心输入), qa(大纲层) | 幕级章纲——情绪弧线、爽点分布、信息释放 |
| **act-XX-人物.md** | plot Step 5 | chapter-design | 本卷登场人物设计 |
| **act-XX-地图.md** | plot Step 6 | chapter-design | 本卷地图/空间设计 |
| **entity-snapshot.yaml** | chapter-design (持续更新) | chapter-design (下一章), expert-writer | 角色状态/时间线/伏笔的全量快照 |
| **起点快照.md** | bookstrap Phase 6 | plot Step 2 | 卷开始时主角/世界状态 |
| **终点快照.md** | bookstrap Phase 7 / deconstructor | plot Step 2, chapter-design | 卷结束时目标状态 |
| **chXXX-设计包.md**（含 fact-skeleton + character-card） | chapter-design Step 3 | prose-render | 回合级事件链 + 角色状态（含冲突层次/信息释放） |
| **styles/{书名}.md** | pop-dna | prose-render Phase 1 | 文风DNA档案 |

### 4.2 可选/增强共享文件

| 文件 | 产出者 | 消费者 | 用途 |
|------|-------|-------|------|
| **combat_capability.yaml** | bookstrap Phase 5 | plot Step 7/9, chapter-design (战斗章) | 段位战力范围 |
| **monster_rank_map.yaml** | bookstrap Phase 5 | chapter-design (怪物出场时) | 怪物等级对照 |
| **act_rank_schedule.yaml** | bookstrap Phase 5 | plot Step 9 | 卷级段位排期 |
| **collision_curve.yaml** | bookstrap Phase 5 | plot Step 9 | 碰撞曲线/战斗章分布 |
| **T1~T7 拆解报告** | deconstructor Phase 2 | bookstrap Phase 0.6 (融合), plot(增强) | 参考书拆解成果 |
| **卷1起点/终点快照** | deconstructor Phase 4 | bookstrap Phase 0.6 (融合) | 参考书卷1结构参考 |

### 4.3 调度层私有文件

| 文件 | 读写者 | 用途 |
|------|-------|------|
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
    │  L2: entity-snapshot ↔ constitution 一致性
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
|------|---------|---------|
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

## 附录 A：项目目录结构参考

```
{项目根}/
├── 00-总控/
│   ├── project.yaml               # [bookstrap] 项目配置
│   └── entity-snapshot.yaml        # [chapter-design/更新] 全量快照
├── 00-原始设定/
│   ├── L0-产品层/
│   │   ├── story-engine.yaml       # [bookstrap] 故事引擎
│   │   ├── deconstruct-融合摘要.md  # [bookstrap] 拆书融合
│   │   └── PRD.md                  # [用户/可选] 产品PRD
│   └── L1-元设定层/
│       ├── 01-世界蓝图.md
│       ├── 02-力量体系.md
│       ├── 03-历史与驱动力.md
│       ├── 04-物种与天赋.md
│       ├── 05-势力格局.md
│       └── 06-资源物品.md
├── 数值体系/
│   ├── combat_capability.yaml      # [bookstrap] 段位战力
│   ├── monster_rank_map.yaml       # [bookstrap] 怪物等级
│   ├── act_rank_schedule.yaml      # [bookstrap] 段位排期
│   └── collision_curve.yaml        # [bookstrap] 碰撞曲线
├── 设计/
│   ├── 起点快照.md                 # [bookstrap] 起点
│   ├── 终点快照.md                 # [bookstrap] 终点
│   ├── 里程碑设计.md               # [plot] 里程碑
│   └── 幕/
│       ├── act-01.yaml             # [plot] 幕纲
│       ├── act-01-人物.md          # [plot] 人物设计
│       ├── act-01-地图.md          # [plot] 地图设计
│       ├── act-01-势力.md          # [plot] 势力
│       ├── act-01-装备.md          # [plot] 装备流
│       ├── info-release-01.md      # [plot] 信息释放
│       ├── 节点B-01.md             # [plot] 节点B
│       └── 情节线草案-01.md        # [plot] 情节线
├── 03-正文/
│   ├── ch001.md                    # [prose-render] 正文 (含章末delta)
│   └── ...
├── 03-写作资产/
│   ├── ch001-事实骨架.md           # [chapter-design] 事件骨架
│   ├── ch001-登场人物卡.md         # [chapter-design] 人物卡
│   ├── ch002-事实骨架.md
│   ├── ch002-登场人物卡.md
│   ├── ...
│   ├── global-summary.md           # [可选] 叙事摘要
│   └── experience-log.md           # [可选] 经验日志
├── L3-角色层/
│   └── 角色卡/                     # [bookstrap] 角色卡
└── _archive/                       # [可选] 废弃版本归档
```

---

## 附录 B：拆分前后对照

| 维度 | 旧版 pop-novel-writer (v15.0) | 新版 (v1.0 拆分) |
|------|-----------------------------|------------------|
| **Design 产出** | `chXXX-design.md`（八块：A~H） | `chXXX-事实骨架.md` + `chXXX-登场人物卡.md` |
| **Render 输入** | 读取 Canvas/plot + 直接读 L1 设定 | 只读骨架 + 人物卡，不碰上游 Canvas |
| **entity-snapshot 更新** | writer Step 3 负责 | chapter-design Step 3 负责 |
| **State Update** | 独立 Step 3（零 LLM） | 合并到 chapter-design 的 Step 3 |
| **文风锚定** | writer Step 2 Phase 1 | prose-render Phase 1 |
| **章节状态更新块** | writer Step 2 产出 | prose-render Step 5 产出（正文末尾） |
| **核心约束** | 无严格隔离 | **Design 不碰文风** / **Render 不碰剧情** |
| **向上依赖** | 依赖 plot 全部 Canvas | Design 依赖 plot Canvas；Render 只依赖 Design |

---

> **本文档通过实地读取以下 Skill 的 SKILL.md 和 Steps 构建：**
> expert-writer, pop-novel-bookstrap, pop-novel-plot,
> pop-novel-chapter-design, pop-novel-prose-render,
> pop-novel-qa, pop-novel-deconstructor, pop-dna,
> download-webnovel-txt, pop-novel-html-renderer,
> workspace-index.yaml, ROUTE-AUGMENT.md
