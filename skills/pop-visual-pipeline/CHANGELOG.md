# CHANGELOG

## v2.0.0 (2026-08-08)

### Art Bible 路由改造（character → art-bible）

**背景**：老板定调一阶段 L1 重构——`character` 改名升级为 `pop-visual-art-bible`（Art Bible · 美术设定集），产出 `素材/美术设定集.md`（画风/人物/场景/符号/一致性五篇合一）为全 IP 宇宙视觉唯一真源。pipeline 作为路由方需同步指向新引擎。

**改动**：

- `skill.json`：`skills` 数组 `pop-visual-character` → `pop-visual-art-bible`；description 同步"产美术设定集"；版本至 v2.0.0
- Phase 2 路由：`pop-visual-art-bible` 产出 `素材/美术设定集.md`（五篇合一 + 复现资产），不再产出离散 `视觉身份卡`
- 基建就绪门禁升级：派生层前验证 `素材/美术设定集.md` + `画风决策.md` 均签核 ✅ 已认可
- 派生层消费协议：cover/oc/comic 只消费美术设定集，禁止各自重建人物/场景/符号/画风
- 下游 `pop-visual-comic` 基建签核快速路径同步指向美术设定集

> 效果：一阶段 L1 基建统一成"一部美术设定集"，派生层只消费它，杜绝"三处各画各的"。

## v1.2.0 (2026-08-05)

### 意图闸口前置 + 基建档位路由（不默认推漫画）

**背景**：老板审视全链路发现——pipeline 基建完成后没有"派生意图询问"机制，agent 默认往漫画推；且基建深度一刀切全量，只想做封面/OC 的用户也白白跑完整 5 闸口。

**改动**：

**一、`steps/step0-init.md` §1.5 意图闸口（前置）**

- 初始化时先问本次目标 intent（cover/oc/comic/full/asset-only），写入总控 `<!--STATE:intent -->`
- 未明确意图时回问用户，不默认漫画
- 由 intent 决定基建档位：cover/oc 轻量（到身份卡即可派生），comic/full 完整（含双角度定妆）

**二、`steps/step1-import.md` §2.5 意图闸口（import 时确认）**

- 总控 intent 为空时用 AskUserQuestion 确认，已确认则沿用

**三、`steps/step2-route.md` 按 intent 路由**

- 路由表新增 intent 档位分流表（cover→3/5，oc→4，comic→6，full→loop，asset-only→停 phase0）
- §5 继续路由逻辑按 intent 判断基建深度与派生去向，不自动进漫画

**四、`SKILL.md`**

- Phase 路由表新增"意图闸口（前置）"+"基建档位（按 intent）"说明
- 新增红线#6：意图闸口前置，不默认推漫画
- 版本至 v1.2.0

**五、`templates/视觉项目总控.html`**

- Masthead 与项目简介新增 `intent` STATE 字段展示

**六、版本同步**

- `SKILL.md` / `skill.json` / `CHANGELOG.md` 至 v1.2.0

> 效果：意图前置后，pipeline 基建完成后按用户真实目标路由，封面/OC 用户不再被默认带进漫画完整基建。

## v1.1.0 (2026-08-04)

### 升级：基建产出签核为基线资产

- Phase 1 产出升级：`画风决策.md` + **画风定标图**（签核✅）
- Phase 2 产出升级：`视觉身份卡.md` + **角色定妆图**（签核✅）
- 基建就绪门禁升级：派生层前必须验证身份卡 + 画风决策均签核为 ✅ 已认可
- 红线 #4 升级：未签核=报错中止，提示先跑基建并完成定标/定妆
- 明确经签核冻结的图 + 文字定义即为全书基线资产，供派生层复用

## v1.0.0 (2026-08-04)

### 新增
- 视觉管线总控骨架（SKILL.md）：两段式架构（基建层 Phase 0-2 + 派生层 Phase 3-6）
- Phase 路由表：读小说→定画风→人物形象→（封面/OC/场景/漫画）
- 基建就绪门禁：派生层前必须验证角色视觉身份卡存在
- `steps/step0-init.md`：初始化视觉项目（创建标准目录+生成总控+自检）
- `steps/step1-import.md`：导入/续写已有项目（资产清点+归位+补跑）
- `steps/step2-route.md`：路由循环（读总控→调子 skill→更新总控）
- `templates/视觉项目总控.html`：唯一状态文件模板
- `skill.json`：元数据 + 激活触发词