# 写作专家全链路 — 文件依赖与产出全景 PRD

> 版本：v2.0 | 2026-06-12
> 更新说明：v2.0 — **管线重构**：pop-novel-bookstrap 拆为 pop-novel-creative（创意打磨+样品试读） + pop-novel-world（小说世界构筑）；pop-novel-character-schema 作为角色创建标准被 world 消费；deconstructor 新增 Phase S Lv1 快速拆解；数值体系 → world 工程层；终点快照 → plot 锚点确认。
> 说明：本文档展示 popwave 写作全链路的完整管线结构，每个节点标注上游依赖文件、下游产出文件、以及跨 skill 共享的关键文件。

---

## 目录

- [一、全链路总览图](#一全链路总览图)
- [二、Skill 管线流程](#二skill-管线流程)
- [三、各 Skill 详细文件依赖表](#三各-skill-详细文件依赖表)
- [四、跨 Skill 共享文件清单](#四跨-skill-共享文件清单)
- [五、管线调度与索引体系](#五管线调度与索引体系)
- [六、典型路径速查](#六典型路径速查)
- [七、关键架构决策](#七关键架构决策)

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
   │             拆书分析 (Phase S → Phase 0→4)           │
   │  输入: {书名}.txt                                    │
   │  ★ Phase S: Lv1 快速拆解（~25min，6个轻量文件）       │
   │  ★ Phase 0-4: Lv2/Lv3 全量深拆（T1~T7 + 文风DNA）    │
   └──────────┬──────────┬──────────────────────────────┘
              │          │
              │          ▼
              │    ┌──────────────────┐
              │    │    pop-dna       │
              │    │  文风DNA蒸馏     │
              │    └────────┬─────────┘
              │             │
              │             ▼
              │    ┌──────────────────────────────┐
              │    │ pop-novel-character-schema   │
              │    │ 角色分级标准 (Lv1~Lv4)       │
              │    │ 产出: schema 模板 + 示例卡    │
              │    └────────┬─────────────────────┘
              │             │
              ▼             ▼
   ┌─────────────────────────────────────────────────────┐
   │                  pop-novel-creative                   │
   │         创意打磨 + onboarding + 样品试读              │
   │  输入: 用户模糊想法 + 拆书 Lv1 (如有对标/参考书)      │
   │  ★ 样品试读：写出来验证，不靠描述确认                   │
   │  产出: story-engine.yaml（宪法级约束）+ 样品试读.md    │
   │        + reader_profile + 对标书分析摘要               │
   │  用户确认样品 = "对就是这感觉" → 进入下一步            │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: story-engine（宪法约束）
              │       + 样品试读 + reader_profile
              │       + 对标分析摘要（如有）
              ▼
   ┌─────────────────────────────────────────────────────┐
   │                  pop-novel-world                     │
   │            小说世界构筑 (World Engineering)          │
   │  输入: story-engine + 样品试读 + reader_profile       │
   │         + character-schema Lv1~Lv4 标准               │
   │         + 拆书 T1/T2/T3/T4（如有参考书）              │
   │  ★ 从宪法推导世界参数：L1设定 + 角色初版 + 数值体系    │
   │  产出: L1-01~06 + 角色卡初版(Lv1~Lv4) + 数值体系 x4   │
   │        + 起点快照 + 世界宪法文档                      │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: L1 设定 + 角色卡 + 数值体系
              │       + 起点快照 + 世界宪法
              ▼
   ┌─────────────────────────────────────────────────────┐
   │               pop-novel-plot                         │
   │              剧情架构 (Step 0→12)                    │
   │  ★ Step 0: 宪法一致性审计 → 验证 world 产出           │
   │  Step 1-12: 全书架构 → 卷设计 → 幕设计 → 终点快照     │
   │  输入: story-engine + L1 + 角色卡 + 数值 + 起点快照   │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: 全书架构.md + volume-XX.md
              │       + act-XX.yaml + 终点快照
              ▼
   ┌─────────────────────────────────────────────────────┐
   │           pop-novel-chapter-design                    │
   │          章纲/导演卡 (Step 1→3)                      │
   │  输入: act-XX.yaml + volume-XX.md                    │
   │        + entity-snapshot + 状态/角色/角色卡           │
   │  ⚠️ 不碰文风 — 只产出事件骨架                         │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: chXXX-设计包.md + entity-snapshot 更新
              ▼
   ┌─────────────────────────────────────────────────────┐
   │           pop-novel-prose-render                      │
   │          正文渲染/上色 (Step 1→4)                     │
   │  输入: 设计包 + 写作资产/文风DNA/{style}.md            │
   │  ⚠️ 不碰剧情 — 只管写好                             │
   └──────────┬──────────────────────────────────────────┘
              │
              │ 产出: chXXX.md
              ▼
   ┌─────────────────────────────────────────────────────┐
   │               pop-novel-qa                           │
   │              爽点质检 (Step 1→3)                     │
   │  输入: 正文 + 设计包 + act-XX.yaml + reader_profile   │
   │  产出: QC 报告 (纯感受型，不存盘)                     │
   └─────────────────────────────────────────────────────┘
              │
              ▼ (可选)
   ┌─────────────────────────────────────────────────────┐
   │          pop-novel-html-renderer                     │
   │         HTML 发布                                    │
   └─────────────────────────────────────────────────────┘
```

### 管线入口（调度层）

```
expert-writer（元 Skill）
 ├─ §0 全局感知 → workspace-index.yaml
 ├─ §3.1 Think → 意图识别 + 审视框架加载
 ├─ §3.1.5 信息增强 → ROUTE-AUGMENT.md（含拆书产出路径注入）
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
  → 检测 _参考书/{书名}/ 下是否有拆书 Lv1 产出
  ↓
Step 1 · pop-novel-creative（创意打磨）
  ├─ 接住用户想法 → 追问 2-3 轮
  ├─ 加载拆书 Lv1 产出（如有对标书：story-engine + 主角参考卡 + 卷1快照）
  ├─ 产出：story-engine.yaml（宪法级约束 v3）
  ├─ 产出：样品试读（500-2000字）★ 核心验证手段
  ├─ 产出：reader_profile
  └─ 用户确认样品："对就是这感觉" [闸门 → world]
  ↓
Step 2 · pop-novel-world（世界构筑）
  ├─ 加载 creative 产出：story-engine + 样品 + reader_profile
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
Step 3 · pop-novel-plot（剧情架构）
  ├─ Step 0:  宪法一致性审计 → 验证 world 产出 vs story-engine
  ├─ Step 1:  前置 + 节点B
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
Step 4 · pop-novel-chapter-design（章纲设计）
Step 5 · pop-novel-prose-render（正文渲染）
Step 6 · pop-novel-qa（爽点质检）
```

### 2.2 已有项目续写流程

```
用户说"续写"
  │
  ▼
Step 0 · expert-writer 全局感知
  → 读取 workspace-index.yaml → 检查 pre_read_status + entity-snapshot
  → 检查 story-engine 宪法版本是否与 plot 同步
  ↓
Step 1 · pop-novel-bookstrap (reverse) ← 保留原逆向工程能力
  ├─ Phase r1: 事件日志（逐章读正文）
  ├─ Phase r2: L0 提取
  ├─ Phase r3: L1 提取
  ├─ Phase r4: 卷纲/幕 还原
  ├─ Phase r5: 卷大纲确认
  └─ Phase r6: 交接验证报告
  ↓
Step 2 → Step 3 → Step 4 → Step 5 → Step 6（同新书启动的 plot → design → render → qa）
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

### 3.1 pop-novel-creative（创意打磨）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:----------|
| 追问轮 | 用户模糊想法 | — | — |
| 对标参考 | 拆书 Lv1（_参考书/{书名}/story-engine.yaml + 主角参考卡 + 快照） | 参考锚点（口述对照） | — |
| 产出宪法 | 追问 + 参考锚点 | `00-原始设定/story-engine.yaml`（v3，含 `constitutional_bounds`） | world、plot |
| 样品试读 | story-engine 初版 | `样品试读/{书名}-样品.md`（500-2000字）| 用户确认 |
| reader_profile | story-engine | `00-总控/project.yaml#reader_profile` | world、plot、qa |
| 对标摘要 | 拆书 Lv1（如有） | `对标分析摘要.md` | world |

> **核心定位：创意宪法 + 样品验证。** 不碰 L1 设定、不碰数值、不碰角色卡。样品是天底下唯一不骗人的验证。

### 3.2 pop-novel-world（世界构筑）

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:----------|
| L1 设定 | story-engine.yaml + 样品试读 + 拆书 T1/T2（如有） | `00-原始设定/L1-01~06.md` | plot |
| 角色初版 | story-engine + character-schema Lv1~Lv4 + 拆书 T3（如有） | `状态/角色/{角色名}-角色卡.md`（按 Lv 分级）| plot、chapter-design |
| 数值体系 | story-engine + L1 力量体系 | `00-总控/数值体系/combat_capability.yaml + act_rank_schedule.yaml + monster_rank_map.yaml + collision_curve.yaml` | plot Step 0 审计、plot Step 9 |
| 起点快照 | story-engine + L1 + 角色 | `设计/起点快照.md` | plot Step 2 |
| 世界宪法 | 全部 world 产出 | `00-总控/世界宪法.md`（约束集清单，for plot 审计）| plot Step 0 |

> **核心定位：从宪法推导世界参数。** 不在"发明"世界——在兑现宪法。每一条设定都可以被 plot Step 0 反过来质问。

### 3.3 pop-novel-character-schema（角色分级标准）

> 轻量标准定义 Skill，不执行具体角色设计流程。

| 步骤 | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:----------|
| 模板定义 | — | `schema/Lv1-one-shot.md` ~ `Lv4-core.md` | world 角色产出阶段 |
| 示例卡 | 参考小说原文 | `examples/Lv1~Lv4 案例卡` | world 角色产出阶段（对照参考）|

消费方式：
- world 产出角色卡时加载对应 Lv 的模板 + 示例
- 有拆书产出时：人物参考卡对照拆书的角色卡做锚点
- 无拆书产出时：使用通用模板兜底

### 3.4 pop-novel-plot（剧情架构）

| Step | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:----------|
| **Step 0 宪法审计** ★NEW | story-engine.yaml + 世界宪法.md + L1 + 数值体系 | 审计报告（一致性校验）| — |
| **Step 1** | story-engine + L1 + 起点快照 | `设计/幕/节点B-XX.md` | — |
| **Step 2** | 起点快照 + 世界宪法 | 锚点确认（含终点快照） | Step 3 |
| **Step 3** | 锚点确认 | `设计/里程碑设计.md` [闸门] | Step 4 |
| **Step 4** | 里程碑设计 | `设计/幕/情节线草案-XX.md` [闸门] | Step 4.5/9 |
| **Step 4.5** | story-engine + L1 + 角色卡 + 数值 + 快照 | `设计/卷/volume-XX.md` | chapter-design |
| **Step 9** | Steps 1-4.5 全部产出 | `设计/幕/vol-XX/act-YY.yaml` | chapter-design 核心输入 |
| **Step 11** | act-XX + rank_schedule | `设计/幕/节奏自检报告.md` | — |

> **新增 Step 0：宪法一致性审计。** plot 开工前检查 world 产出与宪法是否冲突。发现冲突 → 退回 world 阶段修正。

### 3.5 pop-novel-chapter-design（章纲设计）

不变，参见 v1.4。section 3.3。

### 3.6 pop-novel-prose-render（正文渲染）

不变，参见 v1.4。section 3.4。

### 3.7 pop-novel-deconstructor（拆书分析）

| Phase | 上游依赖 | 产出文件 | 下游消费者 |
|:-----|:---------|:---------|:----------|
| **Phase S** ★NEW | {书名}.txt | `Lv1-拆解摘要.md` + `story-engine.yaml` + `Lv4-{主角}-参考卡.md` + `卷1-起点/终点快照.md` + `快速文风指纹-top5.md` | creative、world |
| **Phase 0** | Phase S + {书名}.txt | `{书名}-Phase0-采样日志.md` | Phase 1 |
| **Phase 1** | Phase 0 采样日志 | `{书名}-Phase1-诊断报告.md` | Phase 2 |
| **Phase 2** | 诊断报告 + T1~T7 模板 | `{书名}-T1~T7` × 7 | Phase 3、world |
| **Phase 3** | T1~T7 | `{书名}-Phase3-验证报告.md` | Phase 4 |
| **Phase 4** | 全部 Phase 产出 | `{书名}-三维拆书档案.md` + 文风DNA | pop-dna、world |

### 3.8 pop-novel-bookstrap（逆向工程·保留）

保留原 bookstrap 的 reverse 模式功能。forward 模式已迁移至 creative + world。

| Phase | 说明 |
|:-----|:------|
| Phase r1~r6 | 从已有正文逆向提取设定、还原卷纲（续写场景） |

### 3.9 其他 Skill

pop-dna、download-webnovel-txt、pop-novel-qa、pop-novel-html-renderer 保持不变。

---

## 四、跨 Skill 共享文件清单

> 每条标注文件类型：**S**-静态（一次产出，只读不写）/ **D**-动态（持续维护）

### 4.1 核心共享文件

| 文件 | 类型 | 产出者 | 消费者 | 用途 |
|:------|:----:|:-------|:-------|:------|
| **story-engine.yaml（v3）** | S | creative | world → plot | 创意宪法——含 `constitutional_bounds`（immutables/flexibles/forbidden）。lock once, touch rarely |
| **样品试读.md** | S | creative | world、用户 | 创意验证——唯一不骗人的验证手段。world 做设定时对照样品的感觉 |
| **reader_profile** | S | creative | world、plot、qa | 读者画像——含爽点偏好、弃书阈值 |
| **L1-01~06** | S | world | plot | 世界设定层——世界规则+资源体系 |
| **状态/角色/{角色}-角色卡.md** | **D** | world 初版 → plot 卷间回写 | plot、chapter-design | 按 character-schema Lv1~Lv4 填写。含 per-volume 快照段 |
| **数值体系 x4** | S | world | plot Step 0、Step 9 | combat_capability + rank_schedule + monster_map + collision |
| **起点快照.md** | S | world | plot Step 2 | 卷1开始时主角/世界状态 |
| **世界宪法.md** | S | world | plot Step 0 | 约束集清单——plot 每卷前审计 |
| **终点快照.md** | S | plot Step 2 | chapter-design | 卷N结束时目标状态（plot 锚点确认产出） |
| **设计/卷/volume-XX.md** | S | plot Step 4.5 | chapter-design | 核心卷级输入——角色池/地点池/剧情线/势力动机 |
| **设计/幕/act-XX.yaml** | **D** | plot Step 9 | chapter-design、qa | 幕级章纲——Canvas矩阵 + info_release_plan |
| **entity-snapshot.yaml** | **D** | chapter-design | chapter-design（下章）、expert-writer | 角色当前状态 + event_log |
| **chXXX-设计包.md** | **D** | chapter-design | prose-render | 回合级事件链 |
| **正文/chXXX.md** | **D** | prose-render | qa、html-renderer | 完成正文 |
| **写作资产/文风DNA/{书名}.md** | S | deconstructor / pop-dna | prose-render | 文风DNA档案 |

### 4.2 拆书产出 → 管线消费协议

| 拆书 Lv | 拆书产出 | 消费 Skill | 消费阶段 | 用途 |
|:------|:---------|:----------|:---------|:------|
| Lv1 | story-engine.yaml | creative | 创意打磨 | 参考书核心假说对照 |
| Lv1 | Lv4-主角参考卡 | creative | 创意打磨 | 锚点：参考书主角怎么设定的 |
| Lv1 | 卷1起终点快照 | creative | 创意打磨 | 锚点：参考书卷1走了多远 |
| Lv1 | 快速文风指纹 | prose-render | 风格感知 | 5条可执行文风规则 |
| Lv2 | T1 力量体系 | world | L1 设定 | 参考书的阶层差/通胀/瓶颈 |
| Lv2 | T2 世界观展开 | world | L1 设定 | 参考书的世界展开节奏 |
| Lv2 | T3 角色系统 | world | 角色设计 | 参考书的角色配置对照 |

### 4.3 调度层私有文件

| 文件 | 读写者 | 用途 |
|:------|:-------|:------|
| **workspace-index.yaml** | expert-writer 独占 | 全局索引——项目列表、phase追踪、文件注册表、reference_deconstructions[] |
| **ROUTE-AUGMENT.md** | expert-writer (§3.1.5) | 路由增强映射表 |

---

## 五、管线调度与索引体系

### 5.1 expert-writer 调度数据流（核心调整）

```
每次用户消息
    │
    ▼
§0 全局感知
    │  workspace-index.yaml
    │  ├─ projects[].phase (决定当前阶段)
    │  ├─ reference_deconstructions[] (拆书产出可用列表)
    │  └─ cross_project_lessons (跨项目经验)
    ▼
§3.1 Think
    │  entity-snapshot._meta.total_chapters (确定进度)
    │  progress.next_skill (闸门路由)
    │  creative 阶段 ← 检查是否有拆书 Lv1 产出 → 注入 context
    │  world 阶段    ← 检查是否有拆书 Lv2 产出 → 注入 context
    ▼
§3.2 Execute → 路由子 Skill
    │  creative → world → plot → design → render → qa
    ▼
§3.3 Reflect → 四层审视 + 索引回写
```

### 5.2 管线闸门

| 闸门 | 位置 | 条件 |
|:-----|:-----|:------|
| **样品确认** | creative → world | 用户确认样品试读 |
| **宪法审计** | world → plot | plot Step 0 发现冲突 → 退回 world |
| **里程碑确认** | plot Step 3 | 用户确认里程碑 |
| **场景卡确认** | plot Step 10 | 用户确认场景卡 |

### 5.3 修宪回路

```
plot Step 0 宪法审计发现冲突
    → 是 world 设定违反宪法？ → 退回 world 修正
    → 是宪法本身需要修订？    → 退回 creative 重审
    → 不冲突，继续
```

---

## 六、典型路径速查

| 场景 | 管线路径 | 关键闸门 |
|:------|:---------|:---------|
| **新书启动** | creative → world → plot → design → render → qa | 样品确认 / 里程碑 / 场景卡 |
| **有对标书新书** | download → deconstruct Lv1 → creative（加载拆书）→ world → plot → ... | Lv1 拆完后可选继续深拆或直接开书 |
| **拆解参考书** | download → deconstruct（Phase S 或 Phase 0-4）→ pop-dna（可选） | TXT 质量验证 |
| **已有项目续写** | bookstrap REV → plot → design → render → qa | 精读闸门 |
| **正文修改（骨架级）** | design → render → qa | — |
| **正文修改（渲染级）** | render → qa | — |
| **文风分析→应用** | pop-dna → render | style_executed 验证 |

---

## 七、关键架构决策

### 7.1 为什么拆 bookstrap

| 决策 | 理由 |
|:-----|:------|
| **创意与工程分离** | creative 做"什么叫好"，world 做"能不能做"。两者混在一起导致产出物没有验证回路 |
| **样品试读** | story-engine 的描述验证不可靠。只有让用户看到自己的创意变成文字才能确认方向 |
| **宪法约束** | story-engine 从描述型改为约束型（immutables/flexibles/forbidden）——world 和 plot 在约束内创作，不能超出 |
| **宪法审计** | plot Step 0 自动校验 world 产出 vs story-engine，防止设定偏离创意 |

### 7.2 为什么 character-schema 独立

| 决策 | 理由 |
|:-----|:------|
| **标准≠执行** | character-schema 定义"角色卡长什么样"（标准），world 执行"具体角色卡填写"（实现）|
| **跨管线复用** | character-schema 被 world（角色初版）、plot（角色更新）、chapter-design（登场人物卡）三个 skill 共用 |
| **拆书对齐** | 拆出的角色参考卡按 character-schema Lv1~Lv4 分级，world 产出时自动对照 |

### 7.3 为什么数值体系 move 到 world

| 决策 | 理由 |
|:-----|:------|
| **不是工业决策** | 数值体系（战力区间/升级排期/碰撞曲线）是世界规则的一部分，不是叙事设计的决策 |
| **plot 在约束内使用** | plot Step 9 使用 rank_schedule 做幕级排期，但不发明数值——发明权在 world |

### 7.4 为什么终点快照 move 到 plot

| 决策 | 理由 |
|:-----|:------|
| **不可提前知道** | 终点状态只有在做完卷级设计后才知道。bookstrap/creative 阶段猜测无意义 |
| **plot 锚点的自然产出** | plot Step 2 锚点确认环节自然会产出终点快照 |

---

## 附录 A：项目文件全貌模拟（第7卷）

```
深渊主宰·外神低语/
│
├── 00-总控/                           ← 工程层
│   ├── workspace-index.yaml           [expert-writer] {M}
│   ├── project.yaml                   [creative] {M}
│   ├── entity-snapshot.yaml           [chapter-design] {D}
│   ├── 世界宪法.md                     [world] {S}  约束集清单
│   └── 数值体系/                       [world] {S}
│       ├── combat_capability.yaml
│       ├── monster_rank_map.yaml
│       ├── act_rank_schedule.yaml
│       └── collision_curve.yaml
│
├── 00-原始设定/
│   ├── story-engine.yaml              [creative] {S}  创意宪法 v3
│   ├── 样品试读.md                     [creative] {S}
│   ├── 对标分析摘要.md                 [creative] {S}
│   ├── L1-01~06.md                    [world] {S}
│   └── 起点快照.md                     [world] {S}
│
├── 状态/                               ← 跨卷动态追踪 {D}
│   ├── 角色/
│   │   ├── {主角}-角色卡.md            [world 初版 → plot 卷间回写]
│   │   ├── {配角}-角色卡.md            [world 初版 → plot 卷间回写]
│   │   └── 龙套池.md
│   ├── 势力/
│   ├── 卷摘要/
│   └── 世界状态.md
│
├── 设计/
│   ├── 全书架构.md                     [plot Step 1.5] {S+D}
│   ├── 终点快照.md                     [plot Step 2] {S}
│   ├── 卷/volume-01~07.md             [plot Step 4.5] {S}
│   └── 幕/vol-01~07/act-*.yaml        [plot Step 9] {D}
│
├── 写作资产/
│   ├── 设计包/chXXX-设计包.md           [chapter-design] {D}
│   ├── 文风DNA/                        [deconstructor/pop-dna] {S}
│   └── 锚定章库/                        [用户] {D}
│
├── 正文/chXXX.md                       [prose-render] {D}
│
└── _参考书/                            [deconstructor] {S}
    └── {书名}/
        ├── Lv1-拆解摘要.md             ← Phase S
        ├── story-engine.yaml           ← Phase S
        ├── Lv4-{主角}-参考卡.md        ← Phase S
        ├── ...
        └── T1~T7 分析报告              ← Phase 2
```

---

> **本文档通过实地读取以下 Skill 的 SKILL.md 构建：**
> expert-writer, pop-novel-creative, pop-novel-world, pop-novel-plot,
> pop-novel-chapter-design, pop-novel-prose-render, pop-novel-qa,
> pop-novel-deconstructor, pop-novel-character-schema, pop-dna,
> download-webnovel-txt, pop-novel-bookstrap(reverse), workspace-index.yaml
