# 写作专家全链路依赖图 — 文件依赖与产出全景

> 版本：v5.4 | 2026-06-22
> 说明：本文档覆盖写作专家（pop-writer-*）全链路。基于各 skill 当前 SKILL.md 的 pipeline 字段现状构建。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`。
> **v5.4 迭代**：pop-trope-library 集成从"四模块"升级为"五库"，对齐 library 实际文件分类。查询矩阵新增立项库/文风库 canonical 路径。设定库从"框架+质感"改为"按书整包消费"。入库与消费分离原则强化。

## 写作专家管线顺序（硬性）

```
creative → reservoir → world → character → plot → chapter → prose → qa
   ↑          ↑         ↑         ↑         ↑        ↑       ↑      ↑
pop-writer pop-writer pop-writer pop-writer pop-writer pop-writer pop-writer
-creative  -reservoir -world    -character -plot     -chapter  -prose   -qa
  v4.2.0    v2.2.0    v1.5.0    v2.0.1     v7.0.0    v2.0.0    v3.0.1   v1.0.1
```

**辅助skill（独立调起，不改变主线进度）：**
- `pop-writer-continue` v1.0.1 — 续写场景，读正文→产出状态卡+续写锚点
- `pop-writer-game` v2.0.2 — 文游化
- `pop-writer-html` v1.3.2 — HTML发布

**写作专家消费的拆书专家产出：**
- `pop-decon` 系列 → 拆解数据入库 pop-trope-library → creative、world 以 library 注入方式消费
- `pop-shared-dna` v4.0.3 → 文风DNA档案 → prose-render 消费
- `tool-download-webnovel` → {书名}.txt → deconstructor 消费

---

## 一、管线文件接口

> S = 静态（一次产出）/ D = 动态（持续维护）

### 创意环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| creative v4.3.0 | 用户 + library + WebSearch | `全书立项PRD.md` | S | reservoir, world, character, plot | 唯一立项宪法（10块） |
| reservoir v2.2.0 | PRD + 外部素材 | `素材储备池/{素材}.md` | D | world, plot | 剧情储备卡（冲突公式+原型+套路+枪链） |

### 小说设定环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| world ① L1设定 | PRD + 素材储备池 + library | `小说世界设定/L1-01~06.md` | S | character, plot | 世界蓝图/力量/历史/物种/势力/资源 |
| world ② 数值+升级表 | PRD宪法 + L1力量体系 | `小说世界设定/数值体系/*.md` `动态升级表.md` | S | character, plot | 战斗数值 + 每卷力量膨胀曲线 |
| world ③ 起终点快照 | PRD + L1 + 数值体系 | `小说世界设定/起点快照.md` `终点快照.md` | S | character, plot | 卷1初态 + 卷N终态 |
| world（library获取） | pop-trope-library | `文风库/{书名}.md` → fallback `文风DNA/{书名}.md` | S | prose | 文风DNA档案 |
| character v2.0.1 | PRD + L1 + 数值 + 快照 + library | `状态/角色/{主角,配角}-角色卡.md` | D | plot, chapter | 主角与主要配角设定卡 |

### 剧情设计环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| plot ① 卷战略+拉种子 | PRD + L1 + 角色卡 + 数值 + 素材储备池 + library | `剧情设计/卷/卷{N}-战略定位.md` `剧情种子拉取清单.md` | S | plot ② | 卷级目标 + 种子选择 |
| plot ② 剧情线 | 种子清单 + 角色池 + 数值 + 素材储备池 + library | `剧情设计/剧情线/{主线,支线}-{名称}.md` | S/D | chapter | 数值门槛/时间轴/人物/套路链/枪链 |
| plot ③ 分幕+锚点+枪链 | 剧情线 + 卷战略 + rank_schedule | `剧情设计/幕/vol-XX/{分幕规划,act-YY,chekhov-tracker}.md` | S/D | chapter, prose | 幕切割 + 章锚点 + 契诃夫枪 |

### 正文产出环节

| Skill | 入 | 出 | S/D | → | 用途 |
|:------|:----|:----|:---:|:---|:-----|
| chapter v2.2.0 | act-YY + 剧情线 + entity-snapshot | `章节设计包/chXXX-设计包.md` + entity-snapshot更新 + act-YY枪链更新 | D | prose | 回合级事件骨架 |
| prose v3.0.1 | 设计包 + 文风DNA | `正文/chXXX.md` + 总控更新 | D | qa | 正文渲染 + 状态同步 |
| qa v1.0.1 | 正文 + 设计包 + act-YY | （不留盘） | — | — | L1硬门禁→L2三层介入→L3原文对照 |

---

## 二、辅助 Skill — 独立调起

| Skill | 入 | 出 | → |
|:---|---:|---:|:---|
| continue v1.0.1 | 已有正文 | 状态卡 + 续写锚点 + 未兑现伏笔 | plot |
| game v2.0.2 | 世界观 + 人设 + 剧情设定 | AI 互动文字游戏 | — |
| html v1.3.2 | 正文/设定/场景卡 | 单文件 HTML 发布页 | — |

---

## 三、pop-trope-library 公共知识库集成

> `pop-trope-library` 不是 skill，是公共知识库。当前本地存储，未来云端化。
> **拆书专家（pop-decon-* / pop-shared-*）产出先入库（按五库文件分类），写作专家（pop-writer-*）各环节按需查询消费。**
> 查询协议详见 `skills/pop-trope-library/references/调用匹配SOP.md`（分模块查询：立项库/设定库/文风库/剧情库/套路库）。

### 五库结构

| 模块 | 内容 | 服务本环节 | 入库来源 |
|:-----|:-----|:---------|:---------|
| `立项库/` | PRD 级经验：立项模式/元爽点组合/题材焊接/加工哲学/失败案例 | creative | 拆书 Phase 4 trace + 写书复盘 |
| `设定库/` | **按书整包**的 L1 设定：PRD.md + L1-01~06 + 世界宪法 + 角色与关系 | reservoir, world, character | 拆书 Phase 3 setting |
| `文风库/` | 文风笔触档案（场景卡+通用维度+时间演变），**canonical 路径** | prose | pop-shared-dna |
| `剧情库/` | **标准剧情线**（六段格式），按内容标签分目录 | plot | 拆书 Phase 2 volume |
| `套路库/` | 抽象叙事模式卡（10字段：模式家族+变体+跨书案例） | creative, plot, chapter, qa | 原始素材晋升 |
| `文风DNA/` | 历史兼容路径（fallback） | prose | pop-shared-dna（兼容） |

> **路径约定**：`文风库/` = canonical 主路径；`文风DNA/` = fallback 兼容路径。prose 先查 `文风库/`，不存在时降级到 `文风DNA/`。

### 各管线环节查询矩阵

> 每个环节路由到子 skill 前，expert-writer 应确认子 skill 会查询对应模块。
> 查询方法：按 `调用匹配SOP.md` 分模块查询（立项库/设定库/文风库/剧情库/套路库各走各的查询键）。

| 管线阶段 | 查询模块 | 查什么 | 用途 |
|:---------|:---------|:-------|:-----|
| creative | `立项库/00-索引.md` + `套路库/00-总索引.md` + `references/元爽点-变体映射表.md` | 立项经验 + 元爽点匹配 | 确定本书书型 + 2-3个主元爽点 |
| reservoir | `设定库/`（先查 PRD 卖点→读书级 L1）+ `套路库/` | 跨域设定素材源 + 冲突公式/原型/套路 | 剧情储备卡的素材注入 |
| world | `设定库/{书名}/`（先查 00-索引→读 PRD→读 L1） | 力量体系/制度/数值/命名创意池 | L1 设定+数值体系的创意参考 |
| character | `设定库/{书名}/` + `设定库/角色与关系/` | 角色身份张力/关系结构/说话风格 | 角色卡设计的文化质感和关系模式参考 |
| plot | `剧情库/{标签}/` + `套路库/` + `references/元爽点-变体映射表.md` | 标准剧情线 + 套路链配套 | 卷战略/剧情线/分幕的剧情参考 |
| chapter | `套路库/{具体套路名}.md` | 套路公式+节奏控制 | 章设计包的事件链设计 |
| prose | `文风库/{书名}.md` → fallback `文风DNA/{书名}.md` | 风格渲染场景卡（按 scene 匹配） | 正文渲染的文风锚定 |
| qa | `套路库/{具体套路名}.md` 使用红线段 | L3 原文对照 | 质检时对照套路使用红线 |

### 查询纪律

1. **先查库再创作** — 每个环节进入子 skill 后，先查 trope-library 对应模块，再开始创作
2. **库缺时声明** — 查询无匹配素材时标注"本赛道/元爽点库缺"，降级到通用素材，不静默跳过
3. **查到的是参考不是模板** — trope-library 提供创意参考和套路公式，不直接复制，需根据本书 PRD 改写转化
4. **入库与消费分离** — 拆书管线产出先入库 pop-trope-library（按五库文件分类），写作管线从 library 按协议消费。两条线不交叉。写作管线不直接从拆书项目目录读取文件

---

## 四、项目级知识库路径约定

> 在项目总控模板中固化的 `📚 知识库路径` 区块。解决 agent 找不到 library 路径的反复询问问题。
> 执行者：expert-writer v4.6.0+ 的 `step-0-init.md` 3a。

### 4.1 两类路径声明

项目总控头顶一个固定区块，记录两类知识来源的绝对路径：

| 类型 | 用途 | 初始化行为 | 后续维护 |
|:-----|:-----|:----------|:---------|
| **skill 公共库** | pop-trope-library 本地安装目录（设定库/剧情库/套路库/文风库） | step-0-init 自动解析绝对路径 + 扫描设定库书目 | 公共库迁移时手动更新路径 |
| **用户私藏参考** | 原书拆解数据、wiki骨架、文风DNA等 — 精度更高的原文分析 | 初始留空（`❌待补充`），不猜测 | 用户主动填入或 Agent 追问后填入 |

### 4.2 公共库内容速览

初始化时自动扫描 `{pop-trope-library}/设定库/` 下所有子目录，列出书名。如本书是对标/移植某已有书目，标注 ★。

Agent 进入 reservoir/world/plot 阶段时，从此表直接定位对标书的完整设定包，不再询问 "library 在哪"。

### 4.3 Agent 使用规则（硬约定）

1. **首次加载总控时**，检查知识库路径是否已填写 → 未填写则提示用户补充
2. **reservoir / world / plot 阶段启动前**，必须先确认公共库路径可用（文件系统存在）
3. **用户私藏参考路径 ≠ 空时**，优先消费私藏数据（精度更高）；skill 公共库作为 fallback
4. **路径写入后**，Agent 不再询问「library 在哪」——直接读

### 4.4 与 pop-trope-library 查询矩阵的关系

本区块是 **"去哪找"**（路径元数据），三的查询矩阵是 **"找什么"**（内容路由）。两者互补：
- Agent 启动 → 读总控 → 拿到路径 → 按查询矩阵路由 → 读对应模块
- 路径缺失时阻塞查询矩阵，路径就位后查询矩阵可正常运转

### 4.5 落地文件

此约定落地于 `项目总控.md`（模板源头：`expert-writer/references/project/master-control.tpl.md`），非独立文件。

---

## 附录 A：写作项目文件全貌

```text
{项目名}/
│
├── 全书立项PRD.md                      [creative] 唯一立项宪法（10块结构）
│
├── 素材储备池/                          [reservoir] 每素材独立.md
│
├── 小说世界设定/                        [world]
│   ├── L1-01世界蓝图.md
│   ├── L1-02力量体系.md
│   ├── L1-03历史驱力.md
│   ├── L1-04物种天赋.md
│   ├── L1-05势力格局.md
│   ├── L1-06资源物品.md
│   ├── 起点快照.md
│   ├── 终点快照.md
│   ├── 动态升级表.md
│   └── 数值体系/
│       ├── combat_capability.md
│       ├── rank_schedule.md
│       ├── monster_map.md
│       └── collision.md
│
├── 状态/
│   ├── 角色/{主角}-角色卡.md            [character]
│   ├── 角色/{配角}-角色卡.md
│   └── entity-snapshot.yaml            [chapter 每章设计后更新]
│
├── 剧情设计/                            [plot]
│   ├── 卷/
│   │   ├── 卷{N}-战略定位.md            [plot ①]
│   │   └── 卷{N}-剧情种子拉取清单.md     [plot ①]
│   ├── 剧情线/
│   │   ├── 主线-{编号}-{名称}.md
│   │   └── 支线-{编号}-{名称}.md
│   └── 幕/vol-XX/
│       ├── 分幕规划.md                  [plot ③]
│       ├── act-YY.md
│       └── chekhov-tracker.md          [plot ③ → prose 更新]
│
├── 章节设计包/                          [chapter]
│   └── chXXX-设计包.md
│
├── 正文/                                [prose]
│   └── chXXX.md
│
├── 写作资产/
│   └── 文风DNA/{书名}.md                [world 从 library 获取]
│
└── 项目总控.md                          [prose 每章渲染后更新]
```

---

> 本文档基于各 skill 当前 SKILL.md 的实际 pipeline 字段构建（2026-06-22）。
> 写作专家 skill 清单：expert-writer(v4.6.0)、pop-writer-creative(v4.3.0)、pop-writer-reservoir(v2.2.0)、pop-writer-world(v1.5.0)、
> pop-writer-character(v2.0.1)、pop-writer-plot(v7.6.0)、pop-writer-chapter(v2.2.0)、pop-writer-prose(v3.0.1)、pop-writer-qa(v1.0.1)、
> pop-writer-continue(v1.0.1)、pop-writer-game(v2.0.2)、pop-writer-html(v1.3.2)。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`（pop-decon-* / pop-shared-*）。