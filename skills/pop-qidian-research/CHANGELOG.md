# CHANGELOG — pop-qidian-research

## v4.6.0 — 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v4.6.0
- **CHANGELOG.md**：新增本条版本记录

---

## v4.5.0 — 2026-08-12

### 燃料筛入目标对齐剧情累计卡

**背景**：剧情记录双文件收束——review 只产出「白描卡（单章历史）+ 剧情累计卡（全书累计视图）」，废除 current-state.md。research 燃料文档原以"筛入 current-state"为目标，需同步为剧情累计卡。

**改动**：
- **templates/fuel-doc.tpl.md**：元数据 role/compression 从"筛入 current-state"改为"筛入剧情累计卡"；章节标题"可筛入 current-state 的近期燃料"→"可筛入剧情累计卡的近期燃料"
- **steps/step-1-find.md**：燃料分级"近期可用"从"筛入 current-state"改为"筛入剧情累计卡"
- **steps/step-2-output.md**：落盘清单与回复格式的 current-state 引用同步改为剧情累计卡
- **skill.json**：version 4.4.0→4.5.0，description 更新

## v4.3.0 — 2026-07-22

### 新增 decon-plot 剧情拆解档（第五档）

**核心改动**：在现有四档基础上新增第五档"剧情拆解档"（decon-plot），针对参考书进行6维度剧情结构拆解，服务下游 seed 和 plot 模块。

### 新增内容

- **SKILL.md 新增 decon-plot 剧情拆解档**：
  - 触发条件：用户提供参考书
  - 产出路径：`素材/decon-plot-{书名}.md`
  - 消费方：seed S1+S2 / plot R2+R3+R4+R5 / character C1
  - SOP骨架：DP1接收+采样 → DP2 6维度拆解 → DP3-DP4质检+存盘
  - 6个拆解维度：
    1. 力量体系对比（→seed S1）：参考书做法/优缺点/爽感差异
    2. 金手指设计对比（→seed S2）：加速比/限制设计/代价平衡
    3. Boss战设计（→plot R2）：铺垫时长/战斗阶段数/破局方式/临终反扑/爽感爆发点
    4. 爽感场景拆解（→plot R3）：信息差铺设/面板爆发节奏/越级杀节奏
    5. 分幕转折手法（→plot R4）：转折事件/节奏变化/读者冲击
    6. NPC登场效果（→character C1+plot R5）：出场方式/关系建立节奏/伏笔埋设手法
- **红线新增❌8**：decon-plot 6维度必须全拆，每个维度必须标注消费方。缺维度=不合格
- **速查表新增**：`steps/step-decon-plot.md`（decon-plot档·DP1采样+6维度拆解+质检门禁）
- **frontmatter description 更新**：新增"用户提供参考书时启用decon-plot剧情拆解"触发条件
- **header 更新**：三档→四档，版本标注 v4.3.0
- **execution.mode 更新**：decon-plot 加入"必须完整执行"列表

### 保留不动

- 现有四档（燃料+题材机制/decon-lite 9表拆书/赛道定位调研）的所有内容不动
- 红线1-7保留不动（仅新增红线8）
- step文件（step-1-find.md / step-2-output.md / step-decon-lite.md / step-track-research.md）未改
- templates/（fuel-doc.tpl.md / mechanics-doc.tpl.md）未改
- agents/openai.yaml 未改
- `steps/step-decon-plot.md` 待创建（SKILL.md已引用，详细执行指令后续补充）

### 版本

- SKILL.md + skill.json + CHANGELOG.md 三处版本号同步为 4.3.0

---

> 历史版本条目已归档：`_archive/changelog-history/pop-qidian-research/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
