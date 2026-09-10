# CHANGELOG

## v2.0.0 | 2026-09-10

### SOP 迁移：立项创意-SOP + 篇幅与卷规划-SOP（篇幅部分）

按迁移方案（`新流程探索/sop文档/迁移方案-SOP到mirror系列.md` 3.1）重写操作主体，SOP 为权威，镜界 `11-创作向导` 原精华降为参考。

- 新增「故事脉络设计」环节（第 4 步，核心）：需求卡五字段（基调/主角欲望线/世界线/篇幅/X元素清单，用户原话不润色）＋ story 脉络五元素公式（主角是谁→世界哪里失衡→欲望串→谁挡着→落什么结局）＋ 越界边界（身份/处境放故事脉络，凭什么/能力归角色设计）＋ research 资料门（指向 pop-snow-research 跨系列只读调用）。
- 新增「篇幅推导」环节（第 5 步）：总字数→卷数 N→质变点数/地图升级次数/矛盾解锁层数推导链，作为锁根设定的顶层总参数。
- 去掉"仿写技法附件"分支：仿写另走拆书类 skill（pop-decon / pop-decon-dimension）；fanfic/sequel 附件分流保留。
- 故事脉络产出去向明确：主角欲望线/世界线/谁挡着 → world/character/plot；X元素清单 → world 设定钩子。
- 存档规范：项目空间 `01-需求卡.md / 02-调研文档.md / 03-故事脉络.md`，前缀书名或代号不写日期。

同步三件套：SKILL.md / skill.json（version 2.0.0）/ CHANGELOG。

## v1.0.0 | 2026-09-08

### 初始化：Mirror 立项专家 skill

基于镜界 `11-创作向导.md`，提示词精华逐字直贴、未增删改写。新增编排壳（做什么/红线/速查表）与精华分隔。

- 链路起点：新书 Onboarding，确定根决策后再把世界观/人设交给 02world / 03character。
- 精华含运行时能力（`Read /novel`、`Run agent-rules/agent-skills/novel`、`AskUser` 等）为镜界运行时；纯本地落地视为需轻量化的人为输入，方法精化不变。

同步三件套：SKILL.md / skill.json（version 1.0.0）/ CHANGELOG。
