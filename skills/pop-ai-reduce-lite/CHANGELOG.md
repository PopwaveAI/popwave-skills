# CHANGELOG — pop-ai-reduce-lite

## v6.0.0 | 2026-09-20

### 大幅简化：按「降分 ＋ 少量语感 ＋ 快」重定位

**定位变更（老板拍板）**：去AI味现阶段不追求真正跑通，只要三件——标点与字形归位（主力）、少量语感改写、速度快。原来的八条规则与整套检查面按此收缩。

**SKILL.md 重写**：八条规则收到三条（长句串动作、同义短语重复、情绪直说）；走法由七步收到五步；删掉强度分级、前后对照、脚本预扫步骤，以及三条铁律的展开。

**脚本精简（1648 → 591 行）**：删掉 338 条套话与软信号词库及其检查；删掉只报数的统计项（句长CV／段长CV／TTR／顿号密度／成语连排／意象连排／抽象标签／语气句／标点节奏CV／语气词密度）；删掉 `--profile` 参数与 profile 装载、递归 `-r` 与聚合 summary。报告只留「位置 ＋ 命中 ＋ 建议」。`--fix` 的行为逐字节不变。

**skill.json**：version 5.2.0 → 6.0.0。

## v5.2.0 | 2026-09-20

### 砍掉 doc profile：脚本 1648 → 1393 行，配置 747 → 328 行

**改动**：`deai_gate.py` 的 `doc` profile 整块移除。它的调用方（seed／stage／plot／outline／review／research／decon／dna-style／critic-panel）在 v5.1.0 已全部摘除，此前只剩脚本自己的文档里还提它，属死代码。删掉 `DOC_NAMES`、`DEFAULT_DOC_CFG`，以及各函数里的 doc 分支与参数、CLI 取值；`deai_profiles.json` 的 `doc` 段一并删除。文件头版本改为 v3.5.0，自称由「去AI味门禁」改为「正文检查与标点规范化」。

**body 路径行为不变**：改前改后对 3 份真实章节跑 4 种命令，stdout／stderr 逐字节一致，`--fix` 后的文本 SHA256 一致，80 项检查的名称、顺序、取值、判定、阈值全部相同。仅 4 处与 doc 相关的文案随之消失（不带 `--fix` 的提示行、空目录错误提示、`--help`、`--profile doc` 由可用变为被拒绝）。

**skill.json**：version 5.1.2 → 5.2.0。

## v5.1.2 | 2026-09-20

### 随包文件清理：只留运行与维护必需的内容

**改动**：内部维护记录（来源标注、改动项清单、外部依据）从本包移出，另存到不随包发布的归档目录 `temp/pop-ai-reduce-lite-内部记录-20260920/`；本包内只留改动与用法说明。涉及文件：`CHANGELOG.md`（本文件）、`scripts/deai_gate.py` 的注释与提示文案、`scripts/deai_profiles.json` 的说明、`prd/` 两份档案、`resources/banned-words.md`、`resources/examples.md`、`SKILL.md` 的两条红线。

**脚本行为未变**：改动只落在注释与文案。代码 token 逐条比对完全一致；同一份样例修复后字节相同，80 项检查的名称、取值、阈值、判定、退出码全部一致。

**skill.json**：version 5.1.1 → 5.1.2。

## v5.1.1 | 2026-09-20

### 标点那一轮收进脚本，文档不再列改动项

**改动**：`SKILL.md` 的「标点规范化」一节删掉逐条清单，改成一句「跑一次脚本，动哪些项由脚本定，本文件不逐条列，也不在别处解释」。走法第 4、5 步、红线、以及「一次交付做完两件事」里点到具体标点项的地方一并撤下，交给脚本。新增一条：这一轮的口径不写进回执，也不讲给作者听。`skill.json` 的描述同步去掉同类字句。

**skill.json**：version 5.1.0 → 5.1.1。

## v5.1.0 | 2026-09-20

### 三套写作链路摘除去AI味环节，本 skill 收成唯一宿主

> **背景（老板拍板）**：snow／lantern／emergent 三套专家链路此前各自带一套「存档质量检查」，由 `deai_gate.py` 执行，并要求每个 skill 存档后回报一行确认。去AI味收口到本 skill，链路上不再有这一环。

**改动**：

- **脚本换宿主**：`deai_gate.py` 与 `deai_profiles.json` 由 `pop-snow-pipeline/scripts/` 移到 `pop-ai-reduce-lite/scripts/`，原目录删除。脚本按自身目录读配置，搬迁后功能不变，已冒烟验证。
- **三套链路摘除**：`pop-snow-*`、`pop-lantern-*`、`pop-emergent-*`、`pop-write`、`pop-review`、`pop-outline` 共 15 份 SKILL.md，删掉「存档质量检查」整节、速查表里的脚本行、以及「存档后执行检查」与「回报确认行」的全部要求。写作质量要求（不写套话、不写 AI 腔）保留，只把措辞改成直述。另清理 `pop-critic-panel`、`pop-decon`、`pop-decon-dimension`、`pop-dna-style` 里各一条同类条目。
- **新增「一次交付做完两件事」**：语感改写与标点规范化必须在同一次交付完成，只做一件算半成品。
- **skill.json**：version 5.0.0 → 5.1.0；description 同步；slashCommands 去掉一个把判定口径写在用户可见菜单里的触发词。

## v5.0.0 | 2026-09-20

### 主干重写：废早期的外部包流程，换三条铁律 ＋ 八条规则 ＋ 标点规范化

> **根因（老板拍板）**：v4.0.0 采用外部社区包流程的判断被实测推翻——那套「往口语化、往啰嗦改」的方向在真实正文上要么不达预期要么反向，且必然牺牲质量；旧流程还贵，8 步脚本流水线每跑一次要多次调模型。

**改动**：

- **SKILL.md 主干重写**：废掉外部包原文（步骤 0-4、四步排雷法、破式五层法、A/B/C 三模式、风格注入规则），换成三条铁律 ＋ 八条规则 ＋ 一组标点规范化机械项。
- **规则来源收口**：八条规则只写进 SKILL.md 一处；标点规范化交给 `deai_gate.py --fix`（机械项，零 LLM 成本），不再由规则 JSON 驱动模型自算。
- **保留**：三条铁律（立场守恒／血肉不丢／篇幅容差）、抽象对偶比喻（降为附则）、`banned-words.md`、`examples*.md`、`structures.md`。
- **旧资源已物理删除**：8 步流水线脚本、`zh_rules.json`、`zh_rules_archived.json`、`synonyms.json`。原稿另存归档。
- **标点口径统一到一处**：`deai_gate.py` 的同类处理收敛为单一方向，相关判据文案同步对齐，改动面最小。
- **三种调用场景写死**：管线内（write 之后，写回 ＋ 留档 ＋ 回执）、独立调用（功能区／外部工具，给文本）、只查不改。
- **skill.json**：displayName 与 description 全部改写为新定位；version 4.1.0 → 5.0.0。

**实测依据**：本轮改动据以成立的实测记录不随包发布，存于 `temp/pop-ai-reduce-lite-内部记录-20260920/`。

**待办（未完成，勿当作已做）**：

- 调用点收口：`pop-decon`／`pop-dna-style`／`pop-critic-panel`／`pop-snow-*`／`pop-lantern-*`／`pop-emergent-*`／`pop-outline`／`pop-review` 里各自散落的规则表述与词库来源，改指本 skill 与 `deai_gate` 正本。
- `prd/PRD.md` 与 `prd/进度与待探索.md` 的设计预期等四节，按 v4.1.0 的约定填实。
- 回归：阈值调校所需的样例回归尚未跑。改 `deai_profiles.json` 之前必须先跑。

## v4.1.0 | 2026-09-13

### 新增 `prd/` 骨架（设计档案）

`pop-shared-skill-create` v9.0.0 把 `prd/`（设计预期／解决思路／进度／后续方向）立为 skill 标配，本 skill 先落两份骨架：`prd/PRD.md`、`prd/进度与待探索.md`。

**内容状态**：设计预期、解决思路、边界、关键取舍四节标「待补（2026-09-13）」，等下一次改到这个 skill 时填实。**不编设计预期**——编出来的比没有更坏，下一轮会拿它当依据。

## v4.0.0 | 2026-09-02

### 整包换用外部社区包的实现

> **根因**：对比评测后老板拍板——外部包的检测与改写能力全面强于自研 lite 的表层规则降噪。与其在自研浅层上补短板，不如整包采用成熟实现。维持「非 snow 默认流程」定位不动。

**改动**：

- **实现整包替换**：本目录清空旧实现，铺入外部包全部内容（SKILL.md / resources 规则库 / scripts Python 检测改写引擎）。
- **去掉两级闸门**：删除原「表层降噪→表层后询问→路由深度技法」链路，改为一次到位。
- **skill.json 重写**：id 与中文触发词保留；version 3.0.0 → 4.0.0。
- **脚本运行时**：由 Node(.mjs) 切换为该包的 Python 引擎；依赖 Python ≥3.8。
- **旧实现已备份**：`temp/backup_pop-ai-reduce-lite_20260902_170039/`（project-source + runtime-copy 双份）。

---

## v3.1.0 | 2026-08-31

### 去AI味
- 「交互闭环」改为「在同一流程内完成」，去空洞名词
- 同步 skill.json（version）

---

## v3.0.0 | 2026-08-24

### steps 单件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：pipeline-execute.md 全文合入 SKILL.md「四步执行管线」节（Step 1-4 执行细节+词表+示例全保留）
- **执行模式明确**：主agent直执——单章4步改写+脚本验证+表层后询问用户是同一交互闭环，无自然子agent适配点
- **内容精炼**：字数保留率回查规则收敛进红线第 5 条（补上step文件中"重点查Step 1/Step 4过度删除"的指向）；速查表三条全部并入「输出与验证」节正文（去独立表）；加载门禁节随链式加载架构废除删除；表层后询问模板压缩（提醒两点+选项保留）
- skill.json version 2.4.0→3.0.0

---

> 历史版本条目已归档：`temp/backup_pop-ai-reduce-lite_20260902_170039/project-source/CHANGELOG.md`
> 本轮撤下的内部维护记录：`temp/pop-ai-reduce-lite-内部记录-20260920/`
