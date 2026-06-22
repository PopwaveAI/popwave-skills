# 写作专家全链路依赖图 — 文件依赖与产出全景

> 版本：v5.1 | 2026-06-22
> 说明：本文档覆盖写作专家（pop-writer-*）全链路。基于各 skill 当前 SKILL.md 的 pipeline 字段现状构建。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`。

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
| world（library获取） | pop-trope-library | `文风DNA/{书名}.md` | S | prose | 文风DNA档案 |
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
| chapter v2.0.0 | act-YY + 剧情线 + chekhov-tracker | `章节设计包/chXXX-设计包.md` | D | prose | 回合级事件骨架 |
| prose v3.0.1 | 设计包 + 文风DNA | `正文/chXXX.md` + entity-snapshot更新 + chekhov更新 + 总控更新 | D | qa | 正文渲染 + 状态同步 |
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
> 拆书专家（pop-decon）产出入库，写作专家（pop-writer-*）各环节查询消费。
> 查询协议详见 `skills/pop-trope-library/references/调用匹配SOP.md`（三维查询：层×赛道×元爽点）。

### 四模块

| 模块 | 内容 | 入库来源 |
|:-----|:-----|:---------|
| `套路库/` | 抽象叙事模式（模式家族+变体+跨书案例） | 原始素材晋升 |
| `设定库/` | 赛道设定创意（框架层=力量体系/制度/数值，质感层=命名/术语/文明底色） | 拆书 world 阶段 |
| `剧情库/` | 章级剧情单元卡（事件链+冲突弧线+复用要点） | pop-decon-volume Step 3.5 |
| `文风DNA/` | 文风笔触特征档案（场景卡+通用维度+时间演变） | pop-shared-dna |

### 各管线环节查询矩阵

> 每个环节路由到子 skill 前，expert-writer 应确认子 skill 会查询对应模块。
> 查询方法：按 `调用匹配SOP.md` 三维查询（层×赛道×元爽点）。

| 管线阶段 | 查询模块 | 查什么 | 用途 |
|:---------|:---------|:-------|:-----|
| creative | `套路库/00-总索引.md` + `references/元爽点-变体映射表.md` | 元爽点匹配 | 确定本书 2-3 个主元爽点 |
| reservoir | `设定库/`（框架+质感） + `套路库/` | 跨域设定素材源 + 冲突公式/原型/套路 | 剧情储备卡的素材注入 |
| world | `设定库/`（框架+质感） | 力量体系/制度/数值/命名创意池 | L1 设定+数值体系的创意参考 |
| character | `设定库/质感` | 命名策略/身份/文化底色 | 角色卡设计的文化质感参考 |
| plot | `套路库/` + `剧情库/` + `references/元爽点-变体映射表.md` | 套路链配套 + 剧情改建参考 | 卷战略/剧情线/分幕的套路选择 |
| chapter | `套路库/{具体套路名}.md` | 套路公式+节奏控制 | 章设计包的事件链设计 |
| prose | `文风DNA/{书名}.md` | 风格渲染场景卡 | 正文渲染的文风锚定 |
| qa | `套路库/{具体套路名}.md` 使用红线段 | L3 原文对照 | 质检时对照套路使用红线 |

### 查询纪律

1. **先查库再创作** — 每个环节进入子 skill 后，先查 trope-library 对应模块，再开始创作
2. **库缺时声明** — 查询无匹配素材时标注"本赛道/元爽点库缺"，降级到通用素材，不静默跳过
3. **查到的是参考不是模板** — trope-library 提供创意参考和套路公式，不直接复制，需根据本书 PRD 改写转化
4. **入库与消费分离** — 拆书管线负责入库（按 `入库清洗SOP.md`），写作管线负责消费（按 `调用匹配SOP.md`），两条线不交叉

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
│   └── entity-snapshot.yaml            [prose 每章渲染后更新]
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
> 写作专家 skill 清单：pop-writer-creative(v4.3.0)、pop-writer-reservoir(v2.2.0)、pop-writer-world(v1.5.0)、
> pop-writer-character(v2.0.1)、pop-writer-plot(v7.0.0)、pop-writer-chapter(v2.0.0)、pop-writer-prose(v3.0.1)、pop-writer-qa(v1.0.1)、
> pop-writer-continue(v1.0.1)、pop-writer-game(v2.0.2)、pop-writer-html(v1.3.2)。
> 拆书专家见 `02-拆书专家全链路依赖图-PRD.md`（pop-decon-* / pop-shared-*）。