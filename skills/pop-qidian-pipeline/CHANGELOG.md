# CHANGELOG

## v3.15.0 | 2026-08-18

### step2 路由循环合入 SKILL.md，删除 step2.md

**改动**：
- **SKILL.md**：新增「路由循环」节（读总控STATE→对照Phase调度表路由→按协议更新html），Phase调度表与执行协议合入，每次对话零跳转自包含
- **references/html-update-protocol.md**（新增）：HTML 更新协议单源化——STATE字段/Phase ID对照表/badge表从 step0/step1/step2 三处归一
- **steps/step2.md**：删除，step0/step1 指针改为指向 SKILL.md「路由循环」节
- skill.json version 3.14.1→3.15.0，版本三处一致

---

## v3.14.1 | 2026-08-18

### step2 调度卡化：砍子skill红线/SOP复述段

**改动**：
- **step2.md**：412行复述段改为"更新协议+门禁+Phase调度卡"结构，调度卡只含四要素（目标skill+step、输入、产出、完成后动作）
- 红线与SOP细节一律读子skill SKILL.md，此处不复述（防双源漂移）
- 路由表去版本号（版本正源=CHANGELOG）
- skill.json version 3.14.0→3.14.1，版本三处一致

---

## v3.14.0 | 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v3.14.0
- **CHANGELOG.md**：新增本条版本记录

---

## v3.13.2 | 2026-08-13

### 势力边界收敛版本同步

**背景**：world v5.2.0势力边界收敛（势力人物.md删全书配角，只做势力组织+代表人物一句话锚定），character同步为全部"人"的唯一产出方。

**改动**：
- **SKILL.md Phase 表版本同步**：world v5.1.0→v5.2.0、character v2.1.0→v2.2.0
- 势力=棋盘（world·组织），角色=棋子（character·个体），消灭两层皮

## v3.13.1 | 2026-08-13

### 广度先行三补丁：world/character/plot 版本同步

**背景**：老板定调"广度先行圈定，深度后置深化"——三个skill都先处理全书格局（广度），再深做第一卷（深度），不排除后卷追加世界观/剧情。pipeline 同步 Phase 路由表版本号。

**改动**：
- **SKILL.md Phase 表版本同步**：world v5.0.0→v5.1.0（W1拆两层：W1a全书世界格局+W1b首卷舞台）、character v2.0.0→v2.1.0（新增全书角色版图前置）、plot v5.0.0→v5.1.0（新增全书卷级目录）
- 三个skill均新增"广度先行·深度递归"红线：先圈定全书格局，再深做首卷；后卷递归拓展（追加非重写）

---

> 历史版本条目已归档：`_archive/changelog-history/pop-qidian-pipeline/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
