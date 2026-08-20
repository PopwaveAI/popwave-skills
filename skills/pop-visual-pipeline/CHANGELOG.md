# CHANGELOG

## v2.6.0 | 2026-08-18

### step2-route 路由循环合入 SKILL.md，删除 step2-route.md

**改动**：
- **SKILL.md**：新增「路由循环」节（读视觉项目总控.html STATE→先读intent再路由→按协议更新html），每次对话零跳转自包含
- **references/html-update-protocol.md**（新增）：HTML 更新协议单源化——STATE字段/Phase circle对照表/badge表归一
- **steps/step2-route.md**：删除，step0/step1 指针改为指向 SKILL.md「路由循环」节与 html-update-protocol.md
- skill.json version 2.5.0→2.6.0，版本三处一致

---

## v2.5.0 | 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v2.5.0。

## v2.4.0 (2026-08-10)

### SKILL.md 新增可调度 Skill 清单（素材表）

**背景**：老板定调——pipeline 是整个专家的入口和调度器，应有一份"我能调哪些 skill"的统一清单。视觉 skill.json 已有 `skills` 数组，SKILL.md 补齐同内容的人读表格，与其余 pipeline 格式对齐。

**改动**：

- `SKILL.md`：新增「📦 可调度 Skill 清单（素材表）」区块——asset/style/art-bible/cover/oc/comic 六个 skill 的定位 + Phase，标注视觉 group 是小说漫画专家的一部分而非独立专家
- `skill.json`：`skills` 数组已存在不改动
- 版本至 v2.4.0

## v2.3.0 (2026-08-09)

### onboarding 引导语 C 端口吻重写（去技术化、场景化）

**背景**：老板实测 v2.2.0 引导语不合格——满屏 `skill`/`基建`/`派生`/`Phase`/`模块表` 是给产品经理/AI 专家看的，对「写作作者 / 漫画作者 / 同人爱好者」这类 C 端用户不吸引、不建立场景认知。

**目标**：用户不是产品经理、不是 AI 专家，只是作者 / 漫画人 / 同人爱好者。引导语要**快速建立「我的小说能变成什么」的认知 + 场景能力**，而不是介绍内部架构。

**改动**：

- `references/onboarding-guide.md` 整篇重写：
  - 标题改为「你的小说，能变成什么样？」——开场即给场景感
  - 删掉 `模块表`/`数据流向`/`基建→派生`/`Phase`/`意图闸口` 全部技术黑话
  - 改为三大「玩法」场景卡（封面 / 人物立绘·OC / 漫画连载），每个都讲"你会拿到什么成品"而非内部机制
  - 「你不用担心」三连（画风一致 / 不用懂技术 / 先小样再开整）消解使用顾虑
  - 「就这样开始」一句话引导：丢「书名 + 想做什么」即可，给出 3 个零门槛示例
  - 全程以「你写文字，我变作品」的口吻直接对话用户，无任何技术名词

> 效果：C 端用户 30 秒内建立"我能把小说变成封面/立绘/漫画"的认知，知道怎么开口互动，不被技术架构劝退。

---

> 历史版本条目已归档：`_archive/changelog-history/pop-visual-pipeline/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
