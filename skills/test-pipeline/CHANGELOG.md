# CHANGELOG

## v6.2.0 | 2026-08-22

### Phase 4/5 路由对齐章纲组装层（plot v8.2 / write v7 联动）

**改动**：
- **Phase路由表**：Phase 4 升为 test-plot v8.2.0（4步：+Step2.5章纲组装+Step3七查），产出加 `卷纲/章纲/ch{NNN}-章纲.md`；Phase 5 升为 test-write v7.0.0（读3章章纲），就绪条件改为"本章章纲就绪（Step2.5组装+Step3绿灯）"
- **产出真实性检查**：Phase 4→5 门禁加章纲检查（叙事原子4-6+plot锚点区齐全+七查绿灯）
- **Phase 5/6写审循环**：write向前锚=本章章纲；幕推进流程加Step2.5组装环节
- skill.json version 6.1.0→6.2.0，版本三处一致

## v6.1.0 | 2026-08-18

### step2 路由循环合入 SKILL.md，删除 step2.md

**改动**：
- **SKILL.md**：新增「路由循环」「主agent执行协议」「Phase 5/6写审循环」「异常处理」节，每次对话零跳转自包含
- **steps/step2.md**：删除，step0/step1 指针改为指向 SKILL.md「路由循环」节
- skill.json version 6.0.0→6.1.0，版本三处一致

---

## v6.0.0 | 2026-08-16

### 适配 plot v8 章白描架构

- **Phase 4产出更新**：主线+卷纲战略层（幕框架+核心张力映射）+按幕章白描（`卷纲/卷一-幕N-章白描.md`）
- **Phase 5就绪检查**：`卷纲/章锚点表-卷一.md` 存在→「本章所属幕章白描存在且含本章卡」
- **产出真实性门禁**：Phase 4→5 改为「卷纲含幕框架5行+张力映射5行；首幕章白描每卡≥150字含对话锚/动作锚」
- **写审循环按幕滚动**：本幕写完→plot产下一幕章白描（产前读状态快照吸收正文偏差）→继续写；卷一5幕全完→plot产卷二
- step0-import：文件映射表/Phase就绪表/补跑建议同步新产物名
- skill.json version 5.0.0→6.0.0

---

## v5.0.0 | 2026-08-16

### 架构升级：设定包改编管线

- **从「仿写」升级为「改编」**：Phase 0新增改编强度A/B/C门禁（用户输入X后必问，禁止默认）
- **Phase 1换引擎**：test-seed→test-adapt（产改编计划+X DNA替换矩阵+新立项PRD）
- **下游按改编计划执行**：world/character/plot按改编计划决定每维度改多少（保留/类比切换/重写）
- **总控HTML新增改编强度显示**；skill.json version 4.0.0→5.0.0（skills清单 test-seed→test-adapt）

---

## v4.0.0 | 2026-08-16

### 架构重构：设定包仿写管线

- **包升级为主输入**：设定包（含包配方5表）从旁路参考升级为管线必备输入，包配方硬对齐贯穿全环节；包准入门禁红线（缺表拒绝启动）
- **Phase 0大幅瘦身**：深问四层/拆书链路/赛道调研/灵感收集/种子碰撞全部废弃，改为「包校验+X采集」（step1 §3-4）；文风DNA改为可选项
- **step2从25KB砍到精简骨架**：各Phase专属执行指南废弃（子skill已自传导1-2步直写），保留通用主agent执行协议+产出真实性门禁+Phase5/6写审循环
- **目录结构调整**：新增卷纲/与立项/目录，plot产出路径改为`卷纲/卷一-幕纲.md`+`卷纲/章锚点表-卷一.md`
- **总控HTML文件树同步**：删决策表/灵感收集/种子碰撞/赛道调研等废弃产出
- **可调度清单更新**：pop-research→test-research（建包器）
- skill.json version 3.15.0→4.0.0

---

## test分叉 | 2026-08-15

### 从 pop-qidian-pipeline v3.15.0 分叉为 test 系列

**背景**：KB三层架构（模板回迁/赛道包/参考答案层+本地优先回退）先在 test 系列验证，线上 pop-qidian-* 冻结在改造前，效果不好可整体回滚。
**改动**：仅前缀改名（pop-qidian-pipeline → test-pipeline，含互相引用），逻辑与 pop-qidian-pipeline v3.15.0 完全一致；共享同一 knowledge-base/。

---

---

> 历史版本条目已归档：`_archive/changelog-history/test-pipeline/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
