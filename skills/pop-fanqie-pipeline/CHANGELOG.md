# CHANGELOG

## v4.0.0 — 2026-08-24

### steps 2件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline（起点系）改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step0-import.md / step1.md 两件全部合入 SKILL.md 对应节
- **内容合入**：Step 0 五环节（0a资产扫描/0b标准化转换含16行归位映射表/0c缺口分析/0d落地Phase决策/0e状态重建/0f补缺生成含正文反推+降级模式）+质量门全内联；Step 1（前置检测/目录结构/state落盘）全内联
- **模板合一**：step1 与 step0-import 的 project-state.md 重复模板合并为「标准模板+填写规则」（覆盖 fresh/import/resume 三模式差异）
- **执行模式明确**：主agent直执（路由决策/state管理/Phase 0意图深问/导入模式用户确认）；子agent派发点已在Phase调度表内置（Phase 0 Stage2调研并发、Phase 4 write），不另造派发点
- **内容精炼**：step1 PowerShell命令压缩为目录用途表；速查表/知识地图中 steps 引用清除（import-structures 读取时机改指「Step 0 0b-2 环节」）
- skill.json version 3.13.0→4.0.0

---

## v3.13.0 | 2026-08-18

### step2 路由循环合入 SKILL.md，删除 step2.md

**改动**：
- **SKILL.md**：新增「路由循环」节（读project-state.md→对照Phase调度表路由→按state更新方法落盘），Phase调度表与state更新方法合入，每次对话零跳转自包含
- **steps/step2.md**：删除，step1 指针改为指向 SKILL.md「路由循环」节
- skill.json version 3.12.1→3.13.0，版本三处一致

---

## v3.12.1 | 2026-08-18

### step0-import 结构表下沉：16个标准文件内容结构表移至references

**改动**：
- **step0-import.md**：0b-2内容结构标准化改为引用 references/import-structures.md（弱加载，仅本环节读取），step只保留引用和转换原则
- **新增 references/import-structures.md**：16个标准文件的分节定义+转换方式
- 消除与子skill结构定义的重复维护，结构正源归子skill
- skill.json version 3.12.0→3.12.1，版本三处一致

---

## v3.12.0 | 2026-08-13

### 剧情沉淀轻量化：Phase 5 产出白描卡+状态快照

**背景**：review 侧剧情沉淀轻量化（v4.11.0），剧情累计卡改为状态快照、审核报告落盘废除。pipeline 作为调度器同步对齐 Phase 5 产出。

**改动**：
- **SKILL.md**：Phase 5 路由表产出改「双文件（剧情白描流水账.md + 状态快照.md），审核结论对话内输出」；版本 v3.11.0→v3.12.0
- **steps/step0-import.md**：资产映射表/结构标准化/缺口检测/落地Phase决策/0f正文反推/降级模式 全部改指 状态快照，删除审核报告
- **steps/step1.md**：Phase 5 检查项改指 白描卡+状态快照
- **steps/step2.md**：Phase 5 产出改指 白描卡+状态快照
- **skill.json**：version 3.11.0→3.12.0

---

## v3.11.0 | 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v3.11.0
- **CHANGELOG.md**：新增本条版本记录

---

## v3.10.0 (2026-08-12)

### 剧情记录双文件收束：导入/反推/判定改双文件，废 current-state

**背景**：老板定调——剧情记录只保留「白描卡（存发生）+ 剧情累计卡（存状态）」。番茄系 pipeline 的导入/续写判定与 0f-1 正文反推原引用 current-state，随 review v4.9.0 废 current-state 后，需同步改为双文件（流水账=白描卡 + 剧情累计卡）。

**改动**：
- **step0-import.md**：
  - 资产识别表：`*current-state*/入口包` → `*状态*/累计卡/钩子台账` → `审核/剧情累计卡.md`（白描卡+剧情累计卡两行并存）
  - 内容结构标准化表：`current-state.md` 行 → `审核/剧情累计卡.md`（全书累计视图，replace）
  - 缺口分析 Phase 5：`流水账存在` → `双文件都有=✅`
  - 落地Phase决策：`正文+流水账有` → `正文+双文件有`；`正文+双文件缺`→先反推补建
  - 0f-1 正文反推：触发条件改双文件任一缺失；b) 从"生成current-state"改为"生成剧情累计卡"（全书进度/未回收钩子台账含信息差+预期回收/角色当前状态表/读者已知信息池/禁止漂移/DNA执行包）
  - 0f-3 降级模式引用：current-state → 剧情累计卡
- **SKILL.md**：版本 v3.9.0→v3.10.0；Phase 5 产出补双文件；版本描述更新
- **skill.json**：version 3.9.0→3.10.0，description 补双文件收束

**保留不动**：Phase 0→5 调度骨架/project-state 可视化/路由逻辑——只改剧情记录依赖

---

---

> 历史版本条目已归档：`_archive/changelog-history/pop-fanqie-pipeline/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
