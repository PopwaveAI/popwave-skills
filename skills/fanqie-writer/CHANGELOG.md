# CHANGELOG

## v1.29.9 | 2026-09-24

**建包：收录 fanqie-writer（番茄小说写作技能）。**

来源是维护者发布的 `fanqie-writer-v1.29.9-fork.48.zip`（2026-09-24 15:09，45 个文件）。本包是上游 SkillHub `@laoxi/fanqiexiaoshuoxiezuo` v1.0.1（fanqie-crafter by davtime）的 fork，自我定位为上游的「补充层」——只补上游没有的能力，不重复其已覆盖流程。

### 收录方式

- `SKILL.md`、`references/`（31 件）、`templates/`（8 件）、`scripts/`（4 件）、`assets/`（1 件）**逐字节按原样收录**，逐文件哈希核对无差异，未改一字。
- 新增 `skill.json`（本仓清单）、`CHANGELOG.md`（本文件）、`prd/PRD.md` 与 `prd/进度与待探索.md`（官方包标配的设计档案）。
- 补写 `UPSTREAM-INHERITANCE.md`：`SKILL.md` 与 `references/plot-structures.md` 都引用该件，但来源包未随包提供。补写件只写可从本包原文核到的事实，并声明逐文件继承登记表需向原维护者索取，不代填。
- 来源包另有 1 份 README.md（写的是「解压 zip 后上传」的交付方说明），本仓库官方包不带 README，未收录。

### 版本号口径

上游包标的版本是 `v1.29.9-fork.48`，入库取 `1.29.9`。依据 `scripts/build-registry.mjs` 的 `isPrerelease()`——版本串含 `-` 即归入 beta 通道；官方包要进 stable 通道，入库版本取稳定号段。来源串记录在本条与 `prd/进度与待探索.md`。

### 内容语义变更

无。本包内容与来源包一致；本仓库只补清单与设计档案。

### 已知缺口（收录时即存在，非本仓库造成）

1. `UPSTREAM-INHERITANCE.md` 的逐文件登记表未随包提供（本仓库已补说明件）。
2. `references/my-methodology.md` 是空骨架，标「待作者确认」的字段按原文设计由作者本人填。
3. `references/benchmark-writing.md` 引用的 8 本文笔样本是第三方文本，按原文说明归档在项目工作区，不进技能包。
4. 交付前自检清单编号从 4 直接跳到 6，实际 14 条，但 `SKILL.md` 与源包 README 均写「15 条」。
