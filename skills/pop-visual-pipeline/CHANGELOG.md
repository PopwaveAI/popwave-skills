# CHANGELOG

## v3.0.0 — 2026-08-24

### steps 两件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step0-init / step1-import 两件全合入 SKILL.md 对应 SOP 节（Step 0 初始化 / Step 1 导入续写）
- **执行模式明确**：主 agent 直执——pipeline 是路由总控，初始化（目录/清点/迁移/意图闸口）与路由循环均主 agent 直执；子 skill 干活环节由主 agent 读其 SKILL.md 操作或（派生层）派发子 agent，pipeline 自身无产出不派"扮演 pipeline"的子 agent
- **内容精炼**（三轮重压，合入后体量 85.3%→65.5% 达标带内）：项目空间探测表/意图闸口表/STATE 初始值表转行内列举（5 档 intent+档位映射全保留）；step1 迁移表 8 条映射转行内、落地 Phase 决策 5 分支行内（分支全保留）；⚓意图闸口与基建档位两条 blockquote 并入 Step 0 意图闸口行内版与路由循环（信息无损去重）；可调度 Skill 清单表并入 Phase 路由表；红线3+4 合并为「基建依赖链+就绪门禁」；「唯一状态文件禁止另建 project-state.md」并入红线1；与红线2/执行模式重复句删除；速查表删除 steps/ 两行与模板行；正文与路由循环中 step0-init §1.5 / step1-import §2.5 节点引用改为 Step 0 / Step 1 内部引用
- skill.json version 2.6.0→3.0.0

---

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
