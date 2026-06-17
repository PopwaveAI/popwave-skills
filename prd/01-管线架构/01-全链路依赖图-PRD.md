# Popwave 双专家管线架构 — 全链路文件依赖图 PRD

> 来源：飞书文档 | [原文链接](https://n0mqbh938qa.feishu.cn/wiki/QdXSwE2ZAiAog6kz2bsc35rXnof)
> 同步时间：2026-06-17 | doc_id: BMCMduDqSonBcWxbdgLcmGl4ncc | rev: 5

# Popwave 双专家管线架构 — 文件依赖与产出全景 PRD

> 版本：v3.0 | 2026-06-17
> 更新说明：v3.0 — **双专家架构**：拆书专家（pop-novel-*）与写作专家（pop-writer-*）独立为两个可独立调用的域。creative 升级 v2.0.0：Phase R 路由/三分支(A/B/C)/Phase Delta 独立注入/双产出(PRD+素材储备池)。story-engine 从 .yaml 改为 .md。
> 说明：本文档展示 popwave 双专家管线的完整结构。每个节点标注上游依赖文件、下游产出文件、以及跨 skill 共享的关键文件。

---

## 目录

- 一、双专家架构总览
- 二、Skill 管线流程
- 三、各 Skill 详细文件依赖表
- 四、跨 Skill 共享文件清单
- 五、管线调度与索引体系
- 六、典型路径速查
- 七、关键架构决策
- 附录 A：项目文件全貌

---

## 一、双专家架构总览

### 1.1 为什么拆为两位专家

| 维度 | 写作专家（pop-writer-*） | 拆书专家（pop-novel-*） |
|:-----|:------------------------|:-----------------------|
| **目标** | 创作一本新书 | 拆解分析现有作品 |
| **输出** | 正文、设计包、世界观、剧情 | 拆书报告、文风DNA、参考数据 |
| **独立调用** | 开新书 / 续写 / 注入元素 | 拆解参考书 / 提取文风DNA |
| **消费关系** | 消费拆书专家的产出（Lv1/Lv2） | 独立运行，产出供写作专家消费 |
| **技能前缀** | `pop-writer-*` | `pop-novel-*` |

两位专家**不耦合**——拆书专家可以独立调起（用户说"拆解这本书"），写作专家也可以在没有拆书产出时独立运行。

### 1.2 写作专家全链路

```
┌──────────────────────────────────────────────────────────────┐
│                     写作专家（pop-writer-*）                    │
│                                                              │
│  pop-writer-creative  v2.0.0                                 │
│  创意打磨 (Phase R → A/B/C → Phase Delta)                    │
│  输入: 用户想法 + 拆书 Lv1（如有）                             │
│  产出: PRD.md + 故事引擎.md + 素材储备池 + 样品试读.md         │
│  ★ 路由诊断(Phase R): A:PRD先行 / B:广度浮现 / C:空白碰撞     │
│  ★ Phase Delta: 项目中后期独立注入新元素                       │
└──────────────────────┬───────────────────────────────────────┘
                       │ 产出: PRD.md + 故事引擎.md + 素材储备池.md
                       │       + 样品试读 + reader_profile + 对标分析摘要
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  pop-writer-world                                            │
│  小说世界构筑 (World Engineering)                             │
│  输入: 故事引擎.md + 样品试读 + reader_profile                │
│        + character-schema Lv1~Lv4 标准                       │
│        + 拆书 T1/T2/T3/T4（如有参考书）                       │
│  ★ 从宪法推导世界参数：L1设定 + 角色初版 + 数值体系           │
│  产出: L1-01~06 + 角色卡初版 + 数值体系 x4 + 起点快照        │
│        + 世界宪法文档                                         │
└──────────────────────┬───────────────────────────────────────┘
                       │ 产出: L1 设定 + 角色卡 + 数值体系
                       │       + 起点快照 + 世界宪法
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  pop-writer-plot                                             │
│  剧情架构 (Step 0→12)                                        │
│  ★ Step 0: 宪法一致性审计 → 验证 world 产出                  │
│  Step 1-12: 全书架构 → 卷设计 → 幕设计 → 终点快照            │
│  输入: 故事引擎.md + L1 + 角色卡 + 数值 + 起点快照           │
│  ★ 素材储备池作为剧情种子来源（从池中拉取，不从零编）         │
│  产出: 全书架构.md + volume-XX.md + act-XX.yaml             │
│        + 终点快照                                            │
└──────────────────────┬───────────────────────────────────────┘
                       │ 产出: 全书架构.md + 卷设计 + 幕设计
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  pop-writer-chapter-design                                    │
│  章纲/导演卡 (Step 1→3)                                      │
│  输入: act-XX.yaml + volume-XX.md                            │
│        + entity-snapshot + 状态/角色/角色卡                   │
│  ⚠️ 不碰文风 — 只产出事件骨架                                 │
└──────────────────────┬───────────────────────────────────────┘
                       │ 产出: chXXX-设计包.md + entity-snapshot 更新
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  pop-writer-prose-render                                      │
│  正文渲染/上色 (Step 1→4)                                    │
│  输入: 设计包 + 写作资产/文风DNA/{style}.md                   │
│  ⚠️ 不碰剧情 — 只管写好                                     │
└──────────────────────┬───────────────────────────────────────┘
                       │ 产出: chXXX.md
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  pop-writer-qa                                               │
│  爽点质检 (Step 1→3)                                         │
│  输入: 正文 + 设计包 + act-XX.yaml + reader_profile           │
│  产出: QC 报告 (纯感受型，不存盘)                             │
└──────────────────────┬───────────────────────────────────────┘
                       ▼ (可选)
┌──────────────────────────────────────────────────────────────┐
│  pop-writer-html-renderer                                     │
│  HTML 发布                                                   │
└──────────────────────────────────────────────────────────────┘
```

### 1.3 拆书专家全链路

```
┌──────────────────────────────────────────────────────────────┐
│                     拆书专家（pop-novel-*）                    │
│                                                              │
│  download-webnovel-txt                                        │
│  TXT 直链下载                                                 │
│  → 产出: {书名}.txt                                          │
└──────────────────────┬───────────────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────────────┐
│  pop-novel-deconstructor                                     │
│  拆书分析 (Phase S → Phase 0→4)                              │
│  ★ Phase S: Lv1 快速拆解（~25min，6个轻量文件）              │
│  ★ Phase 0-4: Lv2/Lv3 全量深拆（T1~T7 + 文风DNA）           │
│  → 产出: Lv1-拆解摘要 + T1~T7 + 三维拆书档案                 │
└──────────┬──────────┬───────────────────────────────────────┘
           │          │
           │          ▼
           │    ┌──────────────────────────────────────────────┐
           │    │  pop-dna                                     │
           │    │  文风DNA蒸馏 (从 ≥20 章均匀采样)              │
           │    │  → 产出: 写作资产/文风DNA/{书名}.md           │
           │    └──────────────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────────────────────┐
│  pop-novel-character-schema                                  │
│  角色分级标准 (Lv1~Lv4) — 静态标准定义 Skill                 │
│  产出: schema 模板 + 示例卡                                   │
│  ★ 消费方: world（写作专家）做角色卡时加载                    │
└──────────────────────────────────────────────────────────────┘

                ┌──────────────────────────────────────────────┐
                │  pop-novel-bookstrap (逆向工程)               │
                │  ★ 仅 reverse 模式保留                       │
                │  → 从已有正文逆向提取设定、还原卷纲（续写场景）│
                └──────────────────────────────────────────────┘
```

### 1.4 双专家交互关系

```
拆书专家产出          →       写作专家消费
  Lv1 拆解摘要                 creative（PRD/引擎参考）
  Lv4-主角参考卡                creative（主角设计参考）
  卷1起终点快照                 creative（节奏参考）
  快速文风指纹                  prose-render（风格感知）
  T1/T2/T3/T4                 world（L1设定参考）
  char-schema Lv1~Lv4          world（角色卡标准）
```

写作专家**不依赖**拆书专家——没有拆书产出时，使用通用模板和默认节奏兜底。

拆书专家**不消费**写作专家——独立运行，产出存于 `_参考书/{书名}/` 下供写作专家按需取用。

### 1.5 调度入口

两位专家共享同一个元 Skill 调度入口（expert-writer），通过意图识别路由：

```
用户消息
  │
  ▼
expert-writer（元 Skill）
  ├─ 意图识别
  │   ├─ "开新书/续写/注入元素" → 写作专家
  │   ├─ "拆解这本书/分析文风"  → 拆书专家
  │   └─ "帮我写/检查/发布"    → 写作专家对应子Skill
  │
  ├─ 写作专家路由:
  │   ├─ Phase R(路由) → A/B/C(开书) 或 Phase Delta(注入)
  │   ├─ world → plot → chapter-design → prose-render → qa
  │   └─ 处理期间检查 workspace-index.yaml 获取项目状态
  │
  └─ 拆书专家路由:
      ├─ download → deconstructor(Phase S/0-4) → pop-dna(可选)
      └─ 产出写入 _参考书/{书名}/，更新 reference_deconstructions[]
```

---

## 二、Skill 管线流程

### 2.1 写作专家：新书启动全流程

```
用户说"开书"
  │
  ▼
Step 0 · expert-writer 全局感知
  → 读取 workspace-index.yaml → 锚定项目（新项目/现有）
  → 检测 _参考书/{书名}/ 下是否有拆书 Lv1 产出
  ↓
Step 1 · pop-writer-creative v2.0.0（创意打磨）
  ├─ Phase R 路由诊断 → 走 A/B/C 分支
  │   ├─ A: PRD先行 → 定向采集
  │   ├─ B: 广度采集 → PRD浮现
  │   └─ C: 方向碰撞 → PRD提炼
  ├─ 产出：PRD.md（基本法，3-5条轻量约束）
  ├─ 产出：故事引擎.md（宪法约束，PRD的展开深化）
  ├─ 产出：素材储备池.md（剧情种子，四类归档）
  ├─ 产出：样品试读（500-2000字）★ 核心验证手段
  ├─ 产出：reader_profile + 对标分析摘要（如有拆书）
  └─ 用户确认样品："对就是这感觉" [闸门 → world]
  ↓
Step 2 · pop-writer-world（世界构筑）
  ├─ 加载 creative 产出：PRD.md + 故事引擎.md + 样品 + reader_profile
  ├─ 加载 character-schema Lv1~Lv4 标准
  ├─ 加载拆书 T1/T2/T3/T4（如有参考书）
  ├─ 从宪法推导世界参数：
  │   ├── L1 六件套（01-世界蓝图 ~ 06-资源物品）
  │   ├── 角色卡初版（按 character-schema Lv1~Lv4）
  │   ├── 数值体系（combat_capability + rank_schedule + monster_map + collision）
  │   └── 起点快照
  ├─ 产出：世界宪法文档（for plot 审计）
  └─ 用户确认 [闸门 → plot]
  ↓
Step 3 · pop-writer-plot（剧情架构）
  ├─ Step 0:  宪法一致性审计 → 验证 world 产出 vs 故事引擎
  ├─ Step 1:  前置 + 节点B（从素材储备池拉取剧情种子）
  ├─ Step 1.5: 全书架构 → 设计/全书架构.md
  ├─ Step 2:  锚点确认（含终点快照）
  ├─ Step 3:  里程碑设计 [闸门]
  ├─ Step 4:  情节线草案 [闸门]
  ├─ Step 4.5: 卷设计 → 设计/卷/volume-XX.md
  ├─ Step 9:  幕设计 → 设计/幕/vol-XX/act-YY.yaml
  ├─ Step 10: 场景卡 [闸门]
  ├─ Step 11: 节奏自检
  └─ Step 12: 产出自检
  ↓
Step 4 · pop-writer-chapter-design（章纲设计）
Step 5 · pop-writer-prose-render（正文渲染）
Step 6 · pop-writer-qa（爽点质检）
```

### 2.2 写作专家：独立调起 — 新元素注入

```
用户在项目中后期说"把这个XX融进书里"
  │
  ▼
Step 0 · expert-writer 全局感知
  → 读取 workspace-index.yaml → 锚定现有项目
  → 检查项目目录下是否有 PRD.md + 故事引擎.md + 素材储备池.md
  ↓
Phase Delta · pop-writer-creative（新元素注入）
  ├─ 读已有产出：PRD.md + 故事引擎.md + 世界宪法.md + 素材储备池.md
  ├─ PRD 契合度评估：新元素 vs PRD 加工哲学
  ├─ 宪法冲突检测：新元素 vs 已锁定约束
  ├─ 等级判定：
  │   ├─ ✅ D1: 直接注入 → 写入素材储备池
  │   ├─ ⚠️ D2: 微调后注入 → 输出 PRD 微调方案（用户签字）
  │   └─ ❌ D3: 冲突报告 → 建议弃用或修宪
  └─ 产出：素材储备池更新（含注入来源标记）或 冲突报告
```

### 2.3 写作专家：已有项目续写

```
用户说"续写"
  │
  ▼
Step 0 · expert-writer 全局感知
  → 读取 workspace-index.yaml → 检查 pre_read_status + entity-snapshot
  → 检查故事引擎版本是否与 plot 同步
  ↓
Step 1 · pop-novel-bookstrap (reverse) ← 拆书专家的逆向能力
  ├─ Phase r1: 事件日志（逐章读正文）
  ├─ Phase r2: L0 提取
  ├─ Phase r3: L1 提取
  ├─ Phase r4: 卷纲/幕 还原
  ├─ Phase r5: 卷大纲确认
  └─ Phase r6: 交接验证报告
  ↓
Step 2 → Step 3 → Step 4 → Step 5 → Step 6（同新书启动的 plot → design → render → qa）
```

### 2.4 拆书专家：参考书拆解

```
用户说"拆解这本书"
  │
  ▼
Step 1 · download-webnovel-txt
  → 搜索直链 → 下载 → 质检 → {书名}.txt
  ↓
Step 2 · pop-novel-deconstructor
  ├─ Phase S: Lv1 快速拆解（~25min）
  │   → 6 个轻量文件（story-engine + 主角参考卡 + 快照 + 文风指纹）
  │   → "老板可以开书了"
  ├─ Phase 0: 采样日志
  ├─ Phase 1: 诊断报告
  ├─ Phase 2: T1~T7 独立产出
  ├─ Phase 3: 验证报告
  └─ Phase 4: 三维拆书档案 + 起终点快照
  ↓ (可选)
Step 3 · pop-dna（文风DNA蒸馏）
  → 均匀采样 ≥20 章 → 全书搜索验证 → 写作资产/文风DNA/{书名}.md
```

---

## 三、各 Skill 详细文件依赖表

### 3.1 pop-writer-creative v2.0.0（创意打磨 — 写作专家入口）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| Phase R 路由 | 用户初始输入 | `_路由记录/分支选择.md`（含 mode: pipeline/delta） | — |
| PRD 撰写 | 用户想法（A先行）/ 素材堆积（B浮现）/ 方向（C提炼） | `00-原始设定/PRD.md`（6维度，1页） | story-engine |
| W0 元素交叉库 | 元素交叉库（pop-trope-library） | `_素材聚合/元素复用建议.md` | 素材储备池 |
| W0.5 问作者 | 用户本人 | `_创意元素/作者想法.md` | 素材储备池 |
| W1 跨域素材 | WebSearch / 知识库 | `_素材聚合/跨域素材蒸馏.md` | 素材储备池 |
| W2 拆书融合 | deconstructor Lv1（如有对标书） | `_参考书分析/拆书融合摘要.md` | 素材储备池、world |
| 素材储备池 | 全部 W 产出 + 碰撞剩余 | `00-原始设定/素材储备池.md`（四类归档） | plot（剧情种子） |
| Phase 0 故事引擎 | PRD.md + 素材储备池 + W产出 | `00-原始设定/故事引擎.md`（宪法约束） | world、plot |
| 0.3 参考书策略 | 碰撞点 | `_参考书分析/观察清单+差异化.md` | — |
| 0.4 主角设计 | 碰撞点 + 方向 | `_设计笔记/主角设计.md`（四维） | — |
| 0.5 样品试读 | 故事引擎.md | `_样品试读/样品-v{N}.md` | 用户确认、world |
| **Phase Delta** ★NEW | PRD.md + 故事引擎.md + 世界宪法.md + 素材储备池.md | 素材储备池追加（或冲突报告） | plot（剧情种子更新） |

> **核心定位：创意宪法 + 素材储备 + 样品验证。** 产出两件套：故事引擎.md（硬约束） + 素材储备池.md（软资源池）。

### 3.1-B pop-writer-reservoir v1.0.0（素材储备注入 — 写作专家伴侣）★NEW

> 从 creative 独立出来的素材储备注入 skill。可被 creative 调用产出首版池子，也可独立调起——任何时候作者刷到好东西，想给当前项目储备剧情种子时触发。

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| 首版池子（被 creative 调用） | PRD.md + W0/W1/W2 全部素材 | `00-原始设定/素材储备池.md`（首版，四类归档） | plot、world |
| 注入追加（独立调起） | PRD.md + 故事引擎.md + 世界宪法.md + 现有池子 | 素材储备池追加（injected 标记） | plot（剧情种子更新） |
| 素材解吸 | 用户输入（热点/民俗/IP/传说） | — | PRD 评估 |
| PRD 契合度评估 | PRD.md 加工哲学 | 匹配度标记（高/中/低/冲突） | 归档决策 |
| 适配方式判定 | 素材类型 x 项目类型 | 适配策略（原生改写/魔幻化/替换语境等） | 归档决策 |

**核心用途**：

| 场景 | 处理 |
|:-----|:-----|
| 作者刷到社会热点 | 提取核心冲突 → PRD 评估 → 归档为主/支线索材 |
| 作者看到民俗神话 | 提取独特设定 + 情感基调 → 评估适配方式 → 归档 |
| 作者想融其他 IP | 提取叙事规律而非设定 → 归档为剩余焊接点/背景素材 |
| 作者想用都市传说 | 评估基调是否匹配 → 适配方式判定 → 归档 |

> **定位：素材内化工场。** pop-writer-creative 负责生成故事引擎和首版池子，pop-writer-reservoir 负责持续注入——两者合用，素材永不浪费。

### 3.2 pop-writer-world（世界构筑 — 写作专家）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| Phase 0 融合适配 | 故事引擎.md + 跨域素材蒸馏.md | `00-原始设定/融合适配清单.md` | L1 设定 |
| L1 设定 | 故事引擎.md + 样品试读 + 拆书 T1/T2（如有） | `00-原始设定/L1-01~06.md` | plot |
| 稳定性检验 | L1 六件套 | world-stability-check.md | — |
| 角色初版 | 故事引擎 + character-schema Lv1~Lv4 + 拆书 T3（如有） | `状态/角色/{角色名}-角色卡.md`（按 Lv 分级） | plot、chapter-design |
| 数值体系 | 故事引擎 + L1 力量体系 | `00-总控/数值体系/combat_capability.yaml + act_rank_schedule.yaml + monster_rank_map.yaml + collision_curve.yaml` | plot Step 0、Step 9 |
| 起点快照 | 故事引擎 + L1 + 角色 | `设计/起点快照.md` | plot Step 2 |
| 世界宪法 | 全部 world 产出 | `00-总控/世界宪法.md`（约束集清单） | plot Step 0 |
| 动态升级表 | 宪法已锁定 | `00-原始设定/动态升级表.md` | plot |

> **核心定位：从宪法推导世界参数。** 不在"发明"世界——在兑现宪法。

### 3.3 pop-novel-character-schema（角色分级标准 — 拆书专家）

> 轻量标准定义 Skill，不执行具体角色设计流程。拆书专家产出，写作专家消费。

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| 模板定义 | — | `schema/Lv1-one-shot.md` ~ `Lv4-core.md` | world 角色产出阶段 |
| 示例卡 | 参考小说原文 | `examples/Lv1~Lv4 案例卡` | world 角色产出阶段（对照参考） |

### 3.4 pop-writer-plot（剧情架构 — 写作专家）

| Step | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Step 0 宪法审计** | 故事引擎.md + 世界宪法.md + L1 + 数值体系 + 素材储备池 | 审计报告（一致性校验） | — |
| **Step 1** | 故事引擎 + L1 + 起点快照 + **素材储备池** | `设计/幕/节点B-XX.md` | — |
| **Step 2** | 起点快照 + 世界宪法 | 锚点确认（含终点快照） | Step 3 |
| **Step 3** | 锚点确认 | `设计/里程碑设计.md` [闸门] | Step 4 |
| **Step 4** | 里程碑设计 + **素材储备池** | `设计/幕/情节线草案-XX.md` [闸门] | Step 4.5/9 |
| **Step 4.5** | 故事引擎 + L1 + 角色卡 + 数值 + 快照 | `设计/卷/volume-XX.md` | chapter-design |
| **Step 9** | Steps 1-4.5 全部产出 | `设计/幕/vol-XX/act-YY.yaml` | chapter-design 核心输入 |
| **Step 11** | act-XX + rank_schedule | `设计/幕/节奏自检报告.md` | — |

> ★ **素材储备池消费**：plot Step 1 和 Step 4 从池中拉取剧情种子，不再从零发明冲突。

### 3.5 pop-writer-chapter-design（章纲设计 — 写作专家）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| 设计包 | act-XX.yaml + volume-XX.md + entity-snapshot + 角色卡 | `写作资产/设计包/chXXX-设计包.md` | prose-render |
| entity-snapshot 更新 | 当前 entity-snapshot + 设计包事件 | `00-总控/entity-snapshot.yaml` | 下章、expert-writer |

### 3.6 pop-writer-prose-render（正文渲染 — 写作专家）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| 正文渲染 | 设计包 + 文风DNA/`{书名}.md` | `正文/chXXX.md` | qa、html-renderer |

### 3.7 pop-novel-deconstructor（拆书分析 — 拆书专家核心）

| Phase | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Phase S** ★ | {书名}.txt | `Lv1-拆解摘要.md` + `Lv4-{主角}-参考卡.md` + `卷1-起点/终点快照.md` + `快速文风指纹-top5.md` | creative、world |
| **Phase 0** | Phase S + {书名}.txt | `{书名}-Phase0-采样日志.md` | Phase 1 |
| **Phase 1** | Phase 0 | `{书名}-Phase1-诊断报告.md` | Phase 2 |
| **Phase 2** | 诊断报告 + T1~T7 模板 | `{书名}-T1~T7` × 7 | Phase 3、world |
| **Phase 3** | T1~T7 | `{书名}-Phase3-验证报告.md` | Phase 4 |
| **Phase 4** | 全部 Phase 产出 | `{书名}-三维拆书档案.md` | pop-dna、world |

### 3.8 pop-novel-bookstrap（逆向工程 — 拆书专家）

保留原 bookstrap 的 reverse 模式功能。forward 模式已迁移至 creative + world。

| Phase | 说明 |
|-|-|
| Phase r1~r6 | 从已有正文逆向提取设定、还原卷纲（续写场景） |

### 3.9 其他 Skill

pop-dna（拆书专家）、download-webnovel-txt（拆书专家）、pop-writer-qa（写作专家）、pop-writer-html-renderer（写作专家）。

---

## 四、跨 Skill 共享文件清单

> 每条标注文件类型：**S**-静态（一次产出，只读不写）/ **D**-动态（持续维护）

### 4.1 核心共享文件

| 文件 | 类型 | 产出者 | 消费者 | 用途 |
|-|-|-|-|-|
| **PRD.md**（★ v3 NEW） | S | creative | story-engine、world、plot | 基本法 — 6维度约束（定位/类型/承诺/加工/DNA/边界） |
| **故事引擎.md**（★ v3 从 yaml 改 md） | S | creative | world → plot | 创意宪法 — PRD 展开深化。含 constitutional_bounds |
| **素材储备池.md**（★ v3 NEW） | D | creative 首版 → plot 持续补充 | plot | 剧情种子池 — 四类归档（主线/支线/背景/剩余焊接点） |
| **样品试读.md** | S | creative | world、用户 | 创意验证 — world 做设定时对照样品的感觉 |
| **reader_profile** | S | creative | world、plot、qa | 读者画像 — 含爽点偏好、弃书阈值 |
| **L1-01~06** | S | world | plot | 世界设定层 — 世界规则+资源体系 |
| **状态/角色/{角色}-角色卡.md** | **D** | world 初版 → plot 卷间回写 | plot、chapter-design | 按 character-schema Lv1~Lv4 填写 |
| **数值体系 x4** | S | world | plot Step 0、Step 9 | combat_capability + rank_schedule + monster_map + collision |
| **起点快照.md** | S | world | plot Step 2 | 卷1开始时主角/世界状态 |
| **世界宪法.md** | S | world | plot Step 0 | 约束集清单 — plot 每卷前审计 |
| **终点快照.md** | S | plot Step 2 | chapter-design | 卷N结束时目标状态 |
| **设计/卷/volume-XX.md** | S | plot Step 4.5 | chapter-design | 角色池/地点池/剧情线/势力动机 |
| **设计/幕/act-XX.yaml** | **D** | plot Step 9 | chapter-design、qa | 幕级章纲 — Canvas矩阵 + info_release_plan |
| **entity-snapshot.yaml** | **D** | chapter-design | chapter-design（下章）、expert-writer | 角色当前状态 + event_log |
| **chXXX-设计包.md** | **D** | chapter-design | prose-render | 回合级事件链 |
| **正文/chXXX.md** | **D** | prose-render | qa、html-renderer | 完成正文 |
| **写作资产/文风DNA/{书名}.md** | S | deconstructor / pop-dna | prose-render | 文风DNA档案 |

### 4.2 拆书产出 → 写作专家消费协议

| 拆书 Lv | 拆书产出 | 消费 Skill | 消费阶段 | 用途 |
|-|-|-|-|-|
| Lv1 | 故事引擎（参考书核心假说） | creative | PRD/引擎 | 参考书核心假说对照 |
| Lv1 | Lv4-主角参考卡 | creative | 主角设计 | 锚点：参考书主角怎么设定的 |
| Lv1 | 卷1起终点快照 | creative | 方向感知 | 锚点：参考书卷1走了多远 |
| Lv1 | 快速文风指纹 | prose-render | 风格感知 | 5条可执行文风规则 |
| Lv2 | T1 力量体系 | world | L1 设定 | 参考书的阶层差/通胀/瓶颈 |
| Lv2 | T2 世界观展开 | world | L1 设定 | 参考书的世界展开节奏 |
| Lv2 | T3 角色系统 | world | 角色设计 | 参考书的角色配置对照 |

### 4.3 调度层私有文件

| 文件 | 读写者 | 用途 |
|-|-|-|
| **workspace-index.yaml** | expert-writer 独占 | 全局索引 — 项目列表、phase追踪、文件注册表、reference_deconstructions[] |
| **ROUTE-AUGMENT.md** | expert-writer (§3.1.5) | 路由增强映射表 |

---

## 五、管线闸门与调度

### 5.1 写作专家闸门

| 闸门 | 位置 | 条件 |
|-|-|-|
| **样品确认** | creative → world | 用户确认样品试读 |
| **宪法审计** | world → plot | plot Step 0 发现冲突 → 退回 world |
| **里程碑确认** | plot Step 3 | 用户确认里程碑 |
| **场景卡确认** | plot Step 10 | 用户确认场景卡 |
| **注入确认** ★NEW | Phase Delta D2 | 用户确认 PRD 微调方案 |

### 5.2 修宪回路

```
plot Step 0 宪法审计发现冲突
    → 是 world 设定违反宪法？ → 退回 world 修正
    → 是宪法本身需要修订？    → 退回 creative 重审
    → 不冲突，继续

Phase Delta D2 冲突
    → 输出微调方案 → 用户签字 → 更新 PRD（带版本标记）
    → 通知 world 检查受影响的 L1 维度
```

### 5.3 双专家索引更新

```
拆书专家完成拆解
  → 产出写入 _参考书/{书名}/
  → workspace-index.yaml.reference_deconstructions[] 追加条目
  → 写作专家下次感知时自动检测到可用拆书产出

写作专家完成某阶段
  → workspace-index.yaml.projects[].phase 更新
  → entity-snapshot._meta.total_chapters 更新
```

---

## 六、典型路径速查

| 场景 | 专家 | 管线路径 | 关键闸门 |
|-|-|-|-|
| **新书启动** | 写作专家 | creative → world → plot → design → render → qa | 样品确认 / 里程碑 / 场景卡 |
| **有对标书新书** | 拆书+写作 | deconstruct Lv1 → creative（加载拆书）→ world → plot → ... | Lv1 拆完后可选继续深拆或直接开书 |
|| **项目中注入新元素** | 写作专家（独立调起） | Phase Delta 注入诊断 → D1/D2/D3 | 注入确认（D2） |
|| **热点/IP内化到素材池** ★NEW | 写作专家（独立调起） | pop-writer-reservoir 素材解吸 → PRD评估 → 四类归档 | 归档完整性（必须四类之一） |
|| **拆解参考书** | 拆书专家 | download → deconstruct（Phase S 或 Phase 0-4）→ pop-dna（可选） | TXT 质量验证 |
| **已有项目续写** | 写作专家 | bookstrap REV → plot → design → render → qa | 精读闸门 |
| **正文修改（骨架级）** | 写作专家 | design → render → qa | — |
| **正文修改（渲染级）** | 写作专家 | render → qa | — |
| **文风分析→应用** | 拆书→写作 | pop-dna → prose-render | style_executed 验证 |

---

## 七、关键架构决策

### 7.1 为什么拆为双专家

| 决策 | 理由 |
|-|-|
| **独立调用** | 拆书专家不需要写作专家上下文即可独立运行。用户说"拆这本书"不与某个写作项目绑定 |
| **产出可复用** | 拆书产出存于 _参考书/{书名}/，多个写作项目可同时消费同一份拆书数据 |
| **职责隔离** | 写作专家专注于"怎么创作"，拆书专家专注于"怎么分析"。两个能力集不同，混在一个 skill 里难以维护 |
| **调度清晰** | expert-writer 通过意图识别路由到对应专家，不耦合两个域的执行逻辑 |

### 7.2 为什么 creative 升级 v2.0.0（路由 + 双产出）

| 决策 | 理由 |
|-|-|
| **Phase R 路由** | 用户不要总是同一种启动模式。有清晰想法走 A、碎片灵感走 B、空白走 C。路由诊断避免了千篇一律的追问 |
| **Phase Delta** | 书写到一半想注入新元素是高频场景。不重跑全流程，只做轻量注入诊断。素材储备池就是为这个设计的 |
| **PRD 独立** | PRD 是比故事引擎更早、更轻量的宪法。A分支作为素材筛选器、B分支从素材浮现、C分支方向后提炼。三种模式覆盖所有启动状态 |
| **素材储备池** | creative 采集的大量素材不应只服务当前方向。归档为剧情种子供 plot 消费，避免了"每次 plot 从零编冲突" |
| **story-engine.md 替代 yaml** | 用户偏好强调可读性。宪法约束用 .md 叙事格式替代 .yaml 配置格式，更适合编辑和跨 session 阅读 |

### 7.3 为什么创意与工程分离

| 决策 | 理由 |
|-|-|
| **创意做"什么叫好"** | creative 定义方向、宪法、样品。不做具体实现 |
| **工程做"能不能做"** | world 在宪法约束内兑现世界参数。两者混在一起导致产出物没有验证回路 |

### 7.4 为什么 character-schema 在拆书专家

| 决策 | 理由 |
|-|-|
| **标准 ≠ 执行** | character-schema 定义"角色卡长什么样"（标准），world 执行"具体角色卡填写"（实现） |
| **跨专家复用** | character-schema 被 world（写作专家）消费，但标准本身由拆书专家维护——从拆书积累中提炼分级标准 |
| **拆书对齐** | 拆出的角色参考卡按 character-schema Lv1~Lv4 分级，world 产出时自动对照 |

### 7.5 为什么数值体系在 world

| 决策 | 理由 |
|-|-|
| **不是工业决策** | 数值体系是世界规则的一部分，不是叙事设计的决策 |
| **plot 在约束内使用** | plot Step 9 使用 rank_schedule 做幕级排期，但不发明数值 |

### 7.6 为什么终点快照在 plot

| 决策 | 理由 |
|-|-|
| **不可提前知道** | 终点状态只有在做完卷级设计后才知道 |
| **plot 锚点的自然产出** | plot Step 2 锚点确认环节自然会产出终点快照 |

---

## 附录 A：项目文件全貌模拟（含 v3.0 新文件）

```
深渊主宰·外神低语/                          ← 写作项目
│
├── 00-总控/                               ← 工程层
│   ├── workspace-index.yaml               [expert-writer] {M}
│   ├── project.yaml                       [creative] {M}
│   ├── entity-snapshot.yaml               [chapter-design] {D}
│   ├── 世界宪法.md                         [world] {S}  约束集清单
│   └── 数值体系/                           [world] {S}
│       ├── combat_capability.yaml
│       ├── monster_rank_map.yaml
│       ├── act_rank_schedule.yaml
│       └── collision_curve.yaml
│
├── 00-原始设定/                            ← 创意层
│   ├── PRD.md                             [creative] {S}  基本法 v1 ★ NEW
│   ├── 故事引擎.md                         [creative] {S}  创意宪法 ★ (从 yaml 改 md)
│   ├── 素材储备池.md                       [creative] {D}  剧情种子池 ★ NEW
│   ├── 样品试读.md                         [creative] {S}
│   ├── 对标分析摘要.md                     [creative] {S}
│   ├── 融合适配清单.md                     [world] {S}
│   ├── L1-01~06.md                        [world] {S}
│   ├── 起点快照.md                         [world] {S}
│   └── 动态升级表.md                       [world] {S}
│
├── 状态/                                  ← 跨卷动态追踪 {D}
│   ├── 角色/
│   │   ├── {主角}-角色卡.md                [world 初版 → plot 卷间回写]
│   │   ├── {配角}-角色卡.md                [world 初版 → plot 卷间回写]
│   │   └── 龙套池.md
│   ├── 势力/
│   ├── 卷摘要/
│   └── 世界状态.md
│
├── 设计/
│   ├── 全书架构.md                         [plot Step 1.5] {S+D}
│   ├── 终点快照.md                         [plot Step 2] {S}
│   ├── 卷/volume-01~07.md                 [plot Step 4.5] {S}
│   └── 幕/vol-01~07/act-*.yaml            [plot Step 9] {D}
│
├── 写作资产/
│   ├── 设计包/chXXX-设计包.md               [chapter-design] {D}
│   ├── 文风DNA/                           [deconstructor/pop-dna] {S}
│   └── 锚定章库/                           [用户] {D}
│
├── 正文/chXXX.md                           [prose-render] {D}
│
└── _参考书/                                ← 拆书专家产出
    └── {书名}/
        ├── Lv1-拆解摘要.md                 ← Phase S
        ├── Lv4-{主角}-参考卡.md            ← Phase S
        ├── 卷1-起点/终点快照.md             ← Phase S
        ├── 快速文风指纹-top5.md            ← Phase S
        ├── T1~T7 分析报告                  ← Phase 2
        └── 三维拆书档案.md                 ← Phase 4
```

---

> **本文档通过实地读取以下 Skill 的 SKILL.md 构建：**  
> pop-writer-creative, pop-writer-reservoir, pop-writer-world, pop-writer-plot,  
> pop-writer-chapter-design, pop-writer-prose-render, pop-writer-qa,  
> pop-novel-deconstructor, pop-novel-character-schema, pop-dna,  
> download-webnovel-txt, pop-novel-bookstrap(reverse), expert-writer