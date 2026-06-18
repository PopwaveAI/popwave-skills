# Step 0：项目初始化 — 创建完整目录骨架

> **调用时机**：路由到 `pop-writer-creative`（开新书）之前，必须执行此步骤。
> **产出**：项目目录下创建完整骨架，每个目录含 `.gitkeep` 或空占位（不写入 `README.md` 注释以外的大文件）。
> **门禁**：❌ 不可跳过。不初始化骨架就开书 = 文件散落无归档、后续 skill 找不到目标目录。

## 目录骨架

> 参考：`D:\popwave-skills\prd\01-管线架构\01-全链路依赖图-PRD.md` 附录A

```
{项目根目录}/
│
├── README.md                       ← 自动生成，内容：「{项目名} - 本地 AI 写作工作区」
│
├── 00-总控/                         ← 工程层（expert-writer 独占维护）
│   ├── workspace-index.yaml        [expert-writer] {M}  全局索引
│   ├── project.yaml                [creative] {M}       项目元数据
│   ├── entity-snapshot.yaml        [chapter-design] {D} 角色状态快照
│   ├── 世界宪法.md                   [world] {S}          约束集清单
│   └── 数值体系/                    [world] {S}
│       ├── combat_capability.yaml
│       ├── monster_rank_map.yaml
│       ├── act_rank_schedule.yaml
│       └── collision_curve.yaml
│
├── 00-原始设定/                      ← 创意层（creative + world 产出）
│   ├── 爽点引擎.md                   [creative] {S}      元爽点星座（v3.0 NEW）
│   ├── PRD.md                       [creative] {S}      基本法
│   ├── 故事引擎.md                   [creative] {S}      创意宪法
│   ├── 素材储备池.md                 [creative → reservoir] {D}  剧情储备卡
│   ├── 样品试读.md                   [creative] {S}      方向验证
│   ├── 对标分析摘要.md               [creative] {S}      对标书差异分析
│   ├── L1-01~06.md                  [world] {S}          世界设定六件套
│   ├── 融合适配清单.md               [world] {S}          跨域融合记录
│   ├── 起点快照.md                   [world] {S}          卷1开始时状态
│   └── 动态升级表.md                 [world] {S}          主角能力成长路径
│
├── 状态/                            ← 跨卷动态追踪（chapter-design 持续维护）
│   ├── 角色/                        [world 初版 → plot 回写]
│   │   ├── {主角}-角色卡.md
│   │   ├── {配角}-角色卡.md
│   │   └── 龙套池.md
│   ├── 势力/                        [world]
│   ├── 卷摘要/                       [plot]
│   └── 世界状态.md                   [chapter-design] {D}
│
├── 设计/                            ← 剧情层（plot 产出）
│   ├── 卷/                          [plot Step 0]
│   │   └── 卷{编号}-战略定位.md
│   ├── 卷/卷{编号}-剧情种子拉取清单.md [plot Step 1]
│   ├── 剧情线/                      [plot Step 2]
│   │   ├── 主线-01-{名称}.md
│   │   ├── 主线-02-{名称}.md
│   │   ├── 主线-03-{名称}.md
│   │   ├── 支线-{编号}-{名称}.md
│   │   └── {卷}-套路偏好分析.md
│   └── 幕/vol-XX/                  [plot Step 3-5]
│       ├── 分幕规划.md               [plot Step 3] {S}
│       ├── act-YY.md                [plot Step 4] {D}
│       └── chekhov-tracker.md      [plot Step 5 → chapter 更新] {D}
│
├── 写作资产/                         ← 写作层（chapter-design + prose-render 消费）
│   ├── 设计包/chXXX-设计包.md        [chapter-design] {D}
│   ├── 文风DNA/                     [deconstructor/pop-dna] {S}
│   └── 锚定章库/                    [用户] {D}
│
├── 正文/chXXX.md                    [prose-render] {D}
│
├── _路由记录/                        ← 调度层（expert-writer 临时产出）
├── _素材聚合/                        ← creative 临时产出
├── _创意元素/                        ← creative W0.5 产出
├── _设计笔记/                        ← creative 04 产出
├── _参考书分析/                      ← creative W2 产出（有对标书时）
├── _样品试读/                        ← creative 0.5 产出
│
└── _参考书/                          ← 拆书专家产出
    └── {书名}/
        ├── Lv1-拆解摘要.md
        ├── Lv4-{主角}-参考卡.md
        ├── 卷1-起点/终点快照.md
        ├── 快速文风指纹-top5.md
        ├── T1~T7 分析报告
        └── 三维拆书档案.md
```

## 文件类型标记

| 标记 | 含义 |
|:-----|:------|
| **{S}** | 静态 — 一次产出，只读不写 |
| **{D}** | 动态 — 持续维护，可被追加/修改 |
| **{M}** | 元数据 — expert-writer 独占维护，其他 skill 只读 |
| **[skill]** | 产出者 — 哪个 skill 负责产出/维护该文件 |

## 初始化操作

1. 检查 `{项目根目录}/README.md` 是否存在
   - 存在 → 项目已初始化，跳过本步
   - 不存在 → 继续执行

2. 创建上述所有目录（排除 `_路由记录/` 等 creative 运行时自动创建的目录）

3. 写入 `README.md`

4. 写入空的 `00-总控/workspace-index.yaml`（初始骨架：`projects: [{id, name, phase: initialized, created_at}]`）

5. 初始化完成 → 路由到 pop-writer-creative

## 目录定位说明

分层逻辑：

| 层级 | 用途 | 谁写 | 生命周期 |
|:-----|:------|:-----|:---------|
| **00-总控/** | 工程元数据：索引、宪法、数值 | expert-writer/world | 全书级，几乎不改 |
| **00-原始设定/** | 创意宪法：PRD、引擎、储备池、世界观 | creative/world | 首版锁定后极少改 |
| **状态/** | 跨卷动态：角色状态、势力、世界 | world初版→持续更新 | 每卷更新 |
| **设计/** | 剧情层：卷目标、剧情线、幕、枪链 | plot | 每卷新增 |
| **写作资产/** | 执行层：设计包、DNA、锚点 | chapter-design/decon | 每章新增 |
| **正文/** | 最终输出 | prose-render | 每章新增 |
| **\_\*/** | 运行时临时产出 | 各skill | 阶段性，可归档 |

## 注意

- `00-原始设定/` 下的 `L1-01~06.md` 是 **6 个独立文件**（01-世界蓝图 ~ 06-资源与物品），不是 `L1-元设定层/` 子目录
- `设计/幕/vol-XX/` 中的 `XX` 是卷号（如 `vol-01`），每卷一个子目录
- `_` 开头的目录是运行时临时目录，不在初始化时创建，各 skill 按需创建
