# 写作专家全链路依赖图 — 文件依赖与产出全景

> 版本：v4.0 | 2026-06-19
> 说明：本文档覆盖写作专家（pop-writer-*）全链路。基于各 skill 当前 SKILL.md 的 pipeline 字段现状构建。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`。

## 写作专家管线顺序（硬性）

```
creative → reservoir → world → plot → chapter → prose → qa
   ↑           ↑          ↑       ↑        ↑       ↑      ↑
pop-writer  pop-writer  pop-writer pop-writer pop-writer pop-writer pop-writer
-creative  -reservoir  -world     -plot      -chapter   -prose    -qa
  v3.0.0    v2.2.0     v1.5.0     v7.0.0     v2.0.0     v3.0.1    v1.0.1
```

**辅助skill（独立调起，不改变主线进度）：**
- `pop-writer-character` v2.0.1 — 角色分级标准，world 消费
- `pop-writer-continue` v1.0.1 — 续写场景，读正文→产出状态卡+续写锚点
- `pop-writer-game` v2.0.2 — 文游化
- `pop-writer-html` v1.3.2 — HTML发布

**写作专家消费的拆书专家产出：**
- `pop-decon` 系列 → Lv1 拆解摘要、T1~T7 分析 → creative、world 消费
- `pop-shared-dna` v4.0.3 → 文风DNA档案 → prose-render 消费
- `tool-download-webnovel` → {书名}.txt → deconstructor 消费

---

## 一、各 Skill 详细文件依赖表

### 1.1 pop-writer-creative v3.0.0（创意打磨 — 写作专家入口）

**上游：** `[pop-decon]`
**下游：** `[pop-writer-world, pop-writer-plot]`

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| Phase R 路由 | 用户初始输入 | `创意种子/路由记录-{项目}.md` | — |
| Phase 爽点引擎 | 用户方向碰撞（Q&A） | `创意种子/爽点引擎.md`（元爽点星座 + 占比 + 变体家族） | story-engine |
| A/B/C 分支执行 | 用户想法/素材 | （各分支不同，见子skill SOP） | — |
| PRD 撰写 | 用户方向（A先行）/ 素材堆积（B浮现）/ 方向提炼（C碰撞） | `创意种子/PRD.md`（6维度：定位/类型/承诺/加工/DNA/边界） | story-engine、world、plot |
| W0 元素交叉库 | 用户/套路库(pop-trope-library) | `创意种子/元素复用建议.md` | 素材储备池 |
| W0.5 问作者 | 用户本人 | `创意种子/作者想法.md` | 素材储备池 |
| W1 跨域素材 | WebSearch / 知识库 | `创意种子/跨域素材蒸馏.md` | 素材储备池 |
| W2 拆书融合 | deconstructor Phase S（如有对标书） | `创意种子/拆书融合摘要.md` | 素材储备池、world |
| 素材储备池（首版） | 全部 W 产出 + 碰撞剩余 | `创意种子/素材储备池.md`（四类归档，首版由creative手工触发reservoir） | plot（剧情种子） |
| Phase 0 故事引擎 | PRD.md + 素材储备池 + W产出 | `创意种子/故事引擎.md`（宪法约束） | world、plot |
| 主角设计 | 碰撞点 + 方向 | `创意种子/主角设计.md`（四维） | — |
| 样品试读 | 故事引擎.md | `创意种子/样品试读.md`（500-2000字） | 用户确认、world |
| **Phase Delta**（注入） | PRD.md + 故事引擎.md + 素材储备池.md | 素材储备池追加（或冲突报告） | plot（剧情种子更新） |

> **核心定位：创意宪法 + 素材储备 + 样品验证。** 双产出：故事引擎.md（硬约束）+ 素材储备池.md（软资源池）。样品签字后→world。

---

### 1.2 pop-writer-reservoir v2.2.0（创意转换引擎 ★ 剧情储备卡）

**上游：** `[pop-writer-creative]`
**下游：** `[pop-writer-plot]`

> v2.2.0 — 产出为剧情储备卡格式（含冲突公式+人物原型+配套套路+契诃夫枪链+预期情绪基调）。
> 被 creative 拉动产出首版池子，也可通过 Phase Delta 独立调起注入新素材。

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| Step 0 前置检查 | 项目目录 | 项目状态判定（有PRD/有引擎/无项目） | — |
| Step 1 读已有产出 | PRD.md + 故事引擎.md + 世界宪法.md + 现有池子 | — | Step 2 |
| Step 2 素材采集 | 用户输入 / WebSearch（不足时补采） | 素材摘要 | Step 3 |
| Step 3 解吸+品类路由 | 素材摘要 + 品类判断 | 品类路由记录 → 走 1A~1E 子流程 | 安全门禁 |
| Step 3A~3E 品类拆解 | 品类路由 → 对应子流程 | 品类专属产出（光谱/冲突/翻译/脱敏/原型） | 统一母题 |
| Step 3.5 叙事母题统一 | 品类拆解产出 | 主母题+底色（2条线） | 世界观映射 |
| Step 3.6 世界观映射 | 叙事母题 + 目标作品已有机制 | 映射总表（★零世界观修改原则） | Step 4 |
| **Step 4 ★ 安全门禁** | 素材摘要 + 大众舆论 | 三方立场分析 + 情绪能量检测 + 安全等级(✅/⚠️/🔴/☠️/⚡) | Step 5 |
| Step 5 PRD契合度评估 | PRD.md 加工哲学 | 匹配度标记（高/中/低/冲突） | Step 6 |
| Step 6 宪法冲突检测 | 故事引擎.md + 世界宪法.md | 冲突标记（无冲突/有冲突标注） | Step 7 |
| Step 7 适配方式判定 | 素材类型 × 项目类型 + 多路线评估 | 适配策略 + ≥2条可选路线 | Step 8 |
| Step 8 四类归档 | 全部 Step 产出 | 主线/支线/背景/剩余焊接点分类 | Step 9 |
| Step 9 写入储备池 | 归档结果 | `创意种子/素材储备池.md` 追加 | plot（剧情种子） |

> **核心定位：创意转换引擎。** 三模式：反应式（用户提供素材）、主动式（自主跨域搜索丰富池子）、混合式。

---

### 1.3 pop-writer-world v1.5.0（世界构筑）

**上游：** `[pop-writer-creative, pop-writer-character, pop-writer-reservoir]`
**下游：** `[pop-writer-plot]`

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| Phase 0 融合适配 | 故事引擎.md + 跨域素材蒸馏.md | `小说世界设定/融合适配清单.md` | L1 设定 |
| Phase 1 L1 设定 | 故事引擎.md + 样品试读 + 拆书 T1/T2（如有） | `小说世界设定/L1-01~06.md` | plot |
| Phase 2 稳定性检验 | L1 六件套 | `小说世界设定/稳定性检验.md` | — |
| Phase 3 角色初版 | 故事引擎 + character-schema Lv1~Lv4 + 拆书 T3（如有） | `状态/角色/{角色名}-角色卡.md` | plot、chapter |
| Phase 4 数值体系 | 故事引擎 + L1 力量体系 | `小说世界设定/数值体系/combat_capability.md` + `rank_schedule.md` + `monster_map.md` + `collision.md` | plot |
| Phase 5 起点快照 | 故事引擎 + L1 + 角色 | `小说世界设定/起点快照.md` | plot |
| Phase 6 世界宪法 | 全部 world 产出 | `小说世界设定/世界宪法.md` | plot（审计） |
| Phase 7 动态升级表 | 宪法已锁定 | `小说世界设定/动态升级表.md` | plot |

> **核心定位：从宪法推导世界参数。** 不在"发明"世界——在兑现宪法。
> 消费 reservoir 的剧情储备卡做设定参考。写作前必须确认力量体系命名方向。

---

### 1.4 pop-writer-plot v7.0.0（剧情架构 — 剧情线设计）

**上游：** `[pop-writer-creative, pop-writer-reservoir]`
**下游：** `[pop-writer-chapter]`

| Step | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| **Step 0 卷目标** | 故事引擎.md + L1 + 角色卡 + 数值体系 | `剧情设计/卷/卷{编号}-战略定位.md` | Step 1 |
| **Step 1 拉种子+配套路** | 素材储备池.md（剧情储备卡）+ pop-trope-library | `剧情设计/卷/卷{编号}-剧情种子拉取清单.md` | Step 2 |
| **Step 2 剧情线文档** | 种子清单 + 角色池 + 数值体系 | `剧情设计/剧情线/{主线/支线}-{编号}-{名称}.md` ×N | chapter |
| **Step 2.5 套路偏好** | 全部剧情线文档 | `剧情设计/卷{编号}-套路偏好分析.md` | 自检 |
| **Step 3 分幕切割** | 剧情线文档 + 卷战略定位 | `剧情设计/幕/vol-XX/分幕规划.md` | Step 4 |
| **Step 4 章锚点** | 分幕规划 + rank_schedule | `剧情设计/幕/vol-XX/act-YY.md` | chapter |
| **Step 5 枪链** | 全部剧情线文档 + 章锚点 | `剧情设计/幕/vol-XX/chekhov-tracker.md` | chapter（每章更新） |

> ★ 废除 Canvas 矩阵为主输出。每条剧情线独立 .md 文档——含数值门槛/植入时间轴/人物/套路链/契诃夫枪链/起终点切片。

---

### 1.5 pop-writer-chapter v2.0.0（章纲设计）

**上游：** `[pop-writer-plot]`
**下游：** `[pop-writer-prose]`

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| Step 1 读入上下文 | act-YY.md + 剧情线文档 + entity-snapshot + chekhov-tracker | context 基线 | Step 2 |
| Step 2 事件链设计（含情绪+爽点+钩子+枪链） | Step 1 基线 + 剧情线文档套路链 | 完整事件链（scene/POV/对白/感官/情绪/爽点/枪引用） | Step 3 |
| Step 3 产出落盘 | Step 2 事件链 | `章节设计包/chXXX-设计包.md` + entity-snapshot 更新 + chekhov-tracker 更新 | prose |

> **核心约束：不碰文风。** 只产出事件骨架。设计包含本章套路/情绪弧线可视化/爽点机制表/章末钩子预期回收/契诃夫枪表/关键对白语气潜台词。

---

### 1.6 pop-writer-prose v3.0.1（正文渲染）

**上游：** `[pop-writer-chapter, pop-shared-dna]`
**下游：** `[pop-writer-qa]`

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| 正文渲染 | 设计包 + 文风DNA/`{书名}.md` | `正文/chXXX.md`（正文 + 章末状态更新块） | qa |

> **核心约束：不碰剧情。** 只管把设计包+文风DNA渲染成可读正文。

---

### 1.7 pop-writer-qa v1.0.1（爽点质检）

**上游：** `[pop-writer-prose]`
**下游：** `[]`

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|-|-|-|-|
| L1 硬门禁 | 正文 + 设计包 | 红线检查（不留盘） | — |
| L2 感觉型三层介入 | 正文 + 读者画像 | 情绪感受报告（不留盘） | — |
| L3 原文对照 | 正文 + 设计包 + act-YY | 对齐检查（不留盘） | — |

---

## 二、写作专家辅助 Skill

### 2.1 pop-writer-character v2.0.1（角色分级标准）

**上游：** `[pop-writer-creative, pop-writer-plot]`
**下游：** `[]`

定义角色卡分级标准（Lv1~Lv4），不含具体执行流程。world 消费此标准生成角色卡。

### 2.2 pop-writer-continue v1.0.1（续写搭档）

**上游：** `[pop-writer-world]`
**下游：** `[pop-writer-plot]`

读已有正文 → 产出状态卡 + 续写锚点 + 未被兑现的伏笔 + 快速设定还原。
不执行数据提取工程——做叙事理解。

### 2.3 pop-writer-game v2.0.2（文游化）

将世界观、人设、剧情设定转化为 AI 驱动的互动文字游戏。

### 2.4 pop-writer-html v1.3.2（HTML发布引擎）

将正文/设定/场景卡等结构化数据 → 高质量单文件 HTML 发布页。

---

## 三、跨 Skill 共享文件清单

> 类型：**S**-静态（一次产出，只读不写）/ **D**-动态（持续维护）

| 文件 | 类型 | 产出者 | 消费者 | 用途 |
|-|-|-|-|-|
| **PRD.md** | S | creative | story-engine, world, plot | 基本法 — 6维度约束 |
| **爽点引擎.md** | S | creative | story-engine | 元爽点星座 + 占比 + 变体家族 |
| **故事引擎.md**（★ md 非 yaml） | S | creative | world, plot | 创意宪法 — PRD 展开深化 |
| **素材储备池.md**（★ 剧情储备卡格式） | D | creative 首版/reservoir 注入 | plot | 剧情种子池 |
| **样品试读.md** | S | creative | world, 用户 | 创意验证 — world 做设定时对照 |
| **L1-01~06.md** | S | world | plot | 世界规则 + 资源体系 |
| **状态/角色/{角色}-角色卡.md** | D | world 初版 → plot 卷间回写 | plot, chapter | 按 character-schema Lv1~Lv4 |
| **数值体系 x4**（★ .md） | S | world | plot | combat_capability + rank_schedule + monster_map + collision |
| **起点快照.md** | S | world | plot | 卷1开始时主角/世界状态 |
| **世界宪法.md** | S | world | plot | 约束集清单 |
| **终点快照.md** | S | plot | chapter | 卷N结束时目标状态 |
| **剧情线文档 ×N**（★ 独立 .md） | S/D | plot Step 2 | chapter, prose | 每条线数值门槛/时间轴/人物/套路链/枪链/切片 |
| **分幕规划.md** | S | plot Step 3 | plot Step 4 | 剧情线→幕分配表 |
| **chekhov-tracker.md** | D | plot Step 5 → chapter 每章更新 | plot, chapter | 契诃夫枪追踪 |
| **act-YY.md** | D | plot Step 4 | chapter, qa | 章锚点 + 情绪弧 + 爽点密度 |
| **entity-snapshot.yaml** | D | chapter | chapter（下章）, expert-writer | 角色状态 + event_log |
| **chXXX-设计包.md** | D | chapter | prose | 回合级事件链 |
| **正文/chXXX.md** | D | prose | qa, html | 完成正文 |
| **文风DNA/{书名}.md** | S | pop-shared-dna | prose | 文风DNA档案 |
| **项目总控.md** | D | expert-writer（每阶段回写） | human, agent | 管线进度 + 执行顺序日志 + 产出物公示表 + 理想文件树 |

---

## 四、写作专家闸门与调度

### 4.1 闸门

| 闸门 | 位置 | 条件 |
|-|-|-|
| **样品确认** | creative → world | 用户确认样品试读 |
| **力量体系命名确认** | world Phase 4 前 | 用户选择命名方向（畸变系/意象系等） |
| **安全门禁** ★ | reservoir Step 4 | 受众立场与情绪评估通过 |
| **宪法审计** | world → plot | plot Step 0 发现冲突 → 退回 world |
| **里程碑确认** | plot Step 3 | 用户确认里程碑 |
| **注入确认** ★ | Phase Delta D2 | 用户确认 PRD 微调方案 |

### 4.2 修宪回路

```
plot Step 0 宪法审计发现冲突
    → 是 world 设定违反宪法？ → 退回 world 修正
    → 是宪法本身需要修订？    → 退回 creative 重审
    → 不冲突，继续

Phase Delta 冲突
    → 输出微调方案 → 用户签字 → 更新 PRD
    → 通知 world 检查受影响的 L1 维度
```

### 4.3 索引更新

```
写作专家完成某阶段
  → workspace-index.yaml.projects[].phase 更新
  → entity-snapshot._meta.total_chapters 更新
  → 项目总控.md 更新（管线进度 + 执行顺序日志 + 产出物公示表 + 理想文件树）
```

---

## 五、典型路径速查

| 场景 | 管线路径 | 关键闸门 |
|:-|:---------|:---------|
| **新书启动** | creative → reservoir → world → plot → chapter → prose → qa | 样品确认 / 卷目标确认 / 剧情线设计确认 |
| **有对标书新书** | deconstruct Phase S → creative（加载拆书）→ reservoir → world → plot → ... | Lv1 拆完可选继续深拆或直接开书 |
| **项目中注入新元素** | Phase Delta: creative 触发 → reservoir 执行注入(9步) → creative 判定 D1/D2/D3 | 安全门禁 / 注入确认（D2） |
| **外部素材→储备剧情卡** | pop-writer-reservoir 独立调起 → 9步注入 → 归档 | 安全门禁（不可跳过） |
| **已有项目续写** | pop-writer-continue（读正文→状态卡）→ plot → chapter → prose → qa | 叙事理解闸门 |
| **正文修改（骨架级）** | chapter → prose → qa | — |
| **正文修改（渲染级）** | prose → qa | — |
| **文风分析→应用** | pop-shared-dna → prose-render | style_executed 验证 |
| **角色储备设计** | pop-writer-character（独立调起） | — |

---

## 六、关键架构决策

### 6.1 为什么拆为双专家

| 决策 | 理由 |
|-|-|
| **独立调用** | 拆书专家不需要写作专家上下文即可独立运行 |
| **产出可复用** | 拆书产出存于 _参考书/{书名}/，多个写作项目可同时消费 |
| **职责隔离** | 写作专家专注"创作"，拆书专家专注"分析" |
| **调度清晰** | expert-writer 通过意图识别路由到对应专家 |

### 6.2 为什么 creative 升级 v3.0（Phase 爽点引擎）

| 决策 | 理由 |
|-|-|
| **Phase 爽点引擎** | 元爽点共创 Q&A 保证产出聚焦"怎么让读者停不下来"而非"工程规范" |
| **Phase R 路由** | 用户想法清晰走 A、碎片灵感走 B、空白走 C。避免千篇一律的追问 |
| **Phase Delta** | 项目中注入新元素不走全流程，只做轻量注入诊断 |
| **素材储备池** | 采集的大量素材归档为剧情种子供 plot 消费，避免每次从零编冲突 |
| **story-engine.md 替代 yaml** | 用户偏好 .md 叙事格式，适合编辑和跨 session 阅读 |

### 6.3 为什么创意与工程分离

| 决策 | 理由 |
|-|-|
| **创意做"什么叫好"** | creative 定义方向、宪法、样品。不做具体实现 |
| **工程做"能不能做"** | world 在宪法约束内兑现世界参数 |

### 6.4 为什么 reservoir 吸收 fuse

| 决策 | 理由 |
|-|-|
| **职能重叠** | 两者本质是一条流程的两端：先加工、后归档 |
| **安全门禁不可绕过** | 品类拆解若无安全门禁前置，可能产出洗白方案 |
| **单一认知入口** | 用户说"融进书里"只走一个 skill |

### 6.5 为什么 plot v7.0 重构

| 决策 | 理由 |
|-|-|
| **废除 Canvas 矩阵** | 表格无法承载每条剧情线的完整复杂度，且无法跨卷追踪 |
| **每条线独立 .md** | 可以写数值门槛/时间轴/套路链/契诃夫枪链/切片 |
| **契诃夫枪链必修** | 没有系统化的设伏→回收管理，跨卷伏笔必然遗忘 |
| **先做卷战略目标** | 先定位再执行——不做盲目的路线设计 |

---

## 附录 A：写作项目文件全貌

```text
{项目名}/
│
├── 项目总控.md                        ← expert-writer（管线进度+顺序日志+产出公示+理想文件树+风险）
│
├── 00-总控/                           ← 工程层
│   ├── workspace-index.yaml          [expert-writer]
│   ├── project.yaml                  [creative]
│   └── entity-snapshot.yaml          [chapter-design]
│
├── 创意种子/                          ← 创意宪法层（creative→reservoir）
│   ├── 爽点引擎.md                    [creative]
│   ├── PRD.md                        [creative]
│   ├── 故事引擎.md                    [creative]
│   ├── 素材储备池.md                  [creative首版→reservoir注入]
│   ├── 样品试读.md                    [creative]
│   ├── 主角设计.md                    [creative]
│   ├── 跨域素材蒸馏.md                [creative]
│   └── 拆书融合摘要.md                [creative]
│
├── 小说世界设定/                      ← 世界设定层（world）
│   ├── 融合适配清单.md                [world]
│   ├── 世界宪法.md                    [world]
│   ├── L1-01世界蓝图.md               [world]
│   ├── L1-02力量体系.md               [world]
│   ├── L1-03历史驱力.md               [world]
│   ├── L1-04物种天赋.md               [world]
│   ├── L1-05势力格局.md               [world]
│   ├── L1-06资源物品.md               [world]
│   ├── 起点快照.md                    [world]
│   ├── 动态升级表.md                  [world]
│   ├── 稳定性检验.md                  [world]
│   └── 数值体系/                      [world]
│       ├── combat_capability.md
│       ├── rank_schedule.md
│       ├── monster_map.md
│       └── collision.md
│
├── 状态/                              ← 动态追踪层
│   ├── 角色/{主角}-角色卡.md           [world→plot回写]
│   ├── 角色/{配角}-角色卡.md
│   ├── 势力/
│   └── 世界状态.md
│
├── 剧情设计/                          ← 剧情层（plot）
│   ├── 卷/
│   │   ├── 卷{编号}-战略定位.md       [plot Step 0]
│   │   └── 卷{编号}-剧情种子拉取清单.md [plot Step 1]
│   ├── 剧情线/
│   │   ├── 主线-01-{名称}.md          [plot Step 2]
│   │   ├── 支线-{编号}-{名称}.md
│   │   └── {卷}-套路偏好分析.md       [plot Step 2.5]
│   └── 幕/vol-XX/
│       ├── 分幕规划.md                [plot Step 3]
│       ├── act-YY.md                 [plot Step 4]
│       └── chekhov-tracker.md        [plot Step 5→chapter]
│
├── 章节设计包/                        ← 执行层（chapter→prose）
│   └── chXXX-设计包.md               [chapter]
│
├── 正文/                              ← 渲染层（prose）
│   └── chXXX.md                      [prose]
│
└── 写作资产/
    └── 文风DNA/{书名}.md              [pop-shared-dna→prose]
```

---

> 本文档基于各 skill 当前 SKILL.md 的实际 pipeline 字段构建（2026-06-19）。
> 写作专家 skill 清单：pop-writer-creative(v3.0.0)、pop-writer-reservoir(v2.2.0)、pop-writer-world(v1.5.0)、
> pop-writer-plot(v7.0.0)、pop-writer-chapter(v2.0.0)、pop-writer-prose(v3.0.1)、pop-writer-qa(v1.0.1)、
> pop-writer-character(v2.0.1)、pop-writer-continue(v1.0.1)、pop-writer-game(v2.0.2)、pop-writer-html(v1.3.2)。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`（pop-decon-* / pop-shared-*）。