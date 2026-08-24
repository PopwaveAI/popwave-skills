# CHANGELOG

## v7.0.0 — 2026-08-24

### steps 两件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1-audit / step2-reconstruct 两件全合入 SKILL.md 对应 SOP 节
- **执行模式明确**：第0/0.5/1审纯只读审计可派子agent（verification）执行并回报三审报告，第2审沉淀双文件由主agent落盘；reconstruct逐章扫描/快速提取同理可派子agent，快照汇总落盘归主agent
- **内容精炼**：三审达标线表+沉淀双文件模板原样保留；reconstruct「与正常review区别」表压为要点句（触发/输入/简化审核/formal落盘四要素全保留）；采样策略表原样保留；简化版审核三查+审核结论模板+回复格式全量内联
- **体量说明**：合入后 SKILL.md 5073字=原1794+steps 4312合计6106的83%，高于70%放宽线——steps 内容为100%达标线表/沉淀模板/采样策略/审核结论模板硬内容，依"禁止丢内容硬压"原则仅压一处导航样板与区别表
- templates/（ch{NNN}.tpl.md / 状态快照.tpl.md）保持外部模板文件不变
- skill.json version 6.0.0→7.0.0

## v6.0.0 | 2026-08-16

### 适配 plot v8 章白描

- **第0审对照物更换**：从章锚点表条目（4硬锚点）改为本章白描卡（白描段：场景/事件/对话锚/动作锚/情绪转折/钩子落点 + 锚点6行：爽点/钩子/POV/X耦合/关键数据），缺任一=打回
- **审核输入路径**：`卷纲/章锚点表-卷一.md`→`卷纲/卷一-幕N-章白描.md`（step1-audit/step2-reconstruct/SKILL.md 同步）
- skill.json version 5.0.0→6.0.0

---

## v5.0.0 | 2026-08-16

### 设定包改编引擎适配：X 符合性审核

- **新增第0.5审 X 符合性**：按 `素材/改编计划.md` X体验层检查 X 深耦合（战斗/日常/剧情）+事件原创性（禁止复用包事件），X 浮于表面或换名复用=打回
- skill.json version 4.0.0→5.0.0

---

## v4.0.0 | 2026-08-16

### 设定包仿写引擎适配

- **新增配方符合性第0审**：对照包配方硬对齐达标线（4锚点兑现/爽点≥0.9章/钩子率100%），达标率<90%直接打回不做后续审
- **三步砍为两步**：step-1-audit重写为一次过三审（配方→质量+充足性→沉淀）；step-2-commit合并进主审沉淀节；step-reconstruct改名step2-reconstruct
- 路径对齐新plot产出（卷纲/章锚点表-卷一.md）
- skill.json version 3.9.0→4.0.0

---

## test分叉 | 2026-08-15

### 从 pop-qidian-review v3.9.0 分叉为 test 系列

**背景**：KB三层架构（模板回迁/赛道包/参考答案层+本地优先回退）先在 test 系列验证，线上 pop-qidian-* 冻结在改造前，效果不好可整体回滚。
**改动**：仅前缀改名（pop-qidian-review → test-review，含互相引用），逻辑与 pop-qidian-review v3.9.0 完全一致；共享同一 knowledge-base/。

---

---

> 历史版本条目已归档：`_archive/changelog-history/test-review/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
