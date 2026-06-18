# Step 0：项目初始化 — 创建完整目录骨架

> **调用时机**：路由到 `pop-writer-creative`（开新书）之前，必须执行此步骤。
> **产出**：项目目录下创建完整骨架，每个目录含 `.gitkeep` 或空占位（不写入 `README.md` 注释以外的大文件）。
> **门禁**：❌ 不可跳过。不初始化骨架就开书 = 文件散落无归档、后续 skill 找不到目标目录。

## 目录骨架

> 参考：`D:\\popwave-skills\\prd\\01-管线架构\\01-全链路依赖图-PRD.md` 附录A

```
{项目根目录}/
│
├── README.md                       ← 自动生成
│
├── 00-总控/                         ← 工程层（expert-writer 独占维护）
│   ├── workspace-index.yaml        [expert-writer] {M}  全局索引
│   ├── project.yaml                [creative] {M}       项目元数据
│   └── entity-snapshot.yaml        [chapter-design] {D} 角色状态快照
│
├── 创意种子/                        ← 创意宪法层（creative 产出，全卷不变）
│   ├── 爽点引擎.md                  [creative] {S}      元爽点星座
│   ├── PRD.md                      [creative] {S}      基本法
│   ├── 故事引擎.md                  [creative] {S}      创意宪法
│   ├── 样品试读.md                  [creative] {S}      方向验证
│   └── 对标分析摘要.md              [creative] {S}      对标书差异
│
├── 小说世界设定/                    ← 世界设定层（world 产出，锁定后极少改）
│   ├── 世界宪法.md                  [world] {S}          全书不可违反规则
│   ├── 融合适配清单.md              [world] {S}          跨域融合记录
│   ├── L1-01~06.md                 [world] {S}          世界设定六件套
│   │   （01-世界蓝图 / 02-力量体系 / 03-历史与驱力 / 04-物种与天赋 / 05-势力格局 / 06-资源与物品）
│   ├── 起点快照.md                  [world] {S}          卷1开始时主角/世界状态
│   ├── 动态升级表.md                [world] {S}          主角全书能级路径
│   └── 数值体系/                    [world] {S}          ★ .md 格式，非 .yaml
│       ├── combat_capability.md    战力金字塔
│       ├── monster_rank_map.md     怪物等级映射
│       ├── act_rank_schedule.md    幕级数值排期
│       └── collision_curve.md      碰撞曲线
│
├── 储备剧情池/                      ← 资源池层（creative 首版 → reservoir 持续注入）
│   └── 素材储备池.md                [creative→reservoir] {D}  剧情储备卡
│
├── 状态/                            ← 跨卷动态追踪层（chapter-design 持续维护）
│   ├── 角色/                        [world 初版 → plot 回写]
│   │   ├── {主角}-角色卡.md
│   │   ├── {配角}-角色卡.md
│   │   └── 龙套池.md
│   ├── 势力/                        [world]
│   ├── 卷摘要/                       [plot]
│   └── 世界状态.md                   [chapter-design] {D}
│
├── 剧情设计/                        ← 剧情层（plot 产出，每卷新增）
│   ├── 卷/                          [plot Step 0-1]
│   │   ├── 卷{编号}-战略定位.md
│   │   └── 卷{编号}-剧情种子拉取清单.md
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
├── 章节设计包/                      ← 执行层（chapter-design 产出，每章新增）
│   ├── chXXX-设计包.md              [chapter-design] {D}
│   ├── 文风DNA/                     [deconstructor/pop-dna] {S}
│   └── 锚定章库/                    [用户] {D}
│
├── 正文/                            ← 最终输出（prose-render 产出，每章新增）
│   └── chXXX.md                     [prose-render] {D}
│
├── _路由记录/                        ← 调度层（expert-writer 临时产出）
├── _素材聚合/                        ← creative 临时产出
├── _创意元素/                        ← creative W0.5 产出
├── _设计笔记/                        ← creative 0.4 产出
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

| 层级 | 目录 | 用途 | 谁写 | 变更频率 |
|:-----|:-----|:------|:-----|:---------|
| **工程层** | `00-总控/` | 元数据索引、快照 | expert-writer | 每阶段更新 |
| **创意宪法层** | `创意种子/` | PRD、爽点、引擎、样品 | creative | 锁定后不改 |
| **世界设定层** | `小说世界设定/` | 宪法、L1六件套、数值 | world | 锁定后极少改 |
| **资源池层** | `储备剧情池/` | 剧情储备卡 | creative→reservoir | 持续追加 |
| **动态追踪层** | `状态/` | 角色/势力/卷摘要 | world→持续更新 | 每卷更新 |
| **剧情层** | `剧情设计/` | 卷目标、剧情线、幕、枪链 | plot | 每卷新增 |
| **执行层** | `章节设计包/` | 设计包、DNA、锚点 | chapter-design | 每章新增 |
| **输出层** | `正文/` | 最终正文 | prose-render | 每章新增 |
| **临时层** | `_*/` | 运行时临时产出 | 各skill | 阶段性 |

## 注意

- `小说世界设定/L1-01~06.md` 是 **6 个独立文件**（01-世界蓝图 ~ 06-资源与物品），不是子目录
- `剧情设计/幕/vol-XX/` 中的 `XX` 是卷号（如 `vol-01`），每卷一个子目录
- `_` 开头的目录是运行时临时目录，不在初始化时创建，各 skill 按需创建
- 数值体系全部使用 **.md** 格式，不使用 .yaml
