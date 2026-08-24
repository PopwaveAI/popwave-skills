# CHANGELOG — pop-shared-skill-create

## v7.0.0 — 2026-08-24

### 规范口径升级为单文件自包含：steps/ 目录废除，step-1-design.md 规范正文全合入 SKILL.md

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）——skill 注入链只把 SKILL.md 全文注入 prompt，SKILL.md 里对 steps/xxx.md 的引用形同虚设。全仓 41 个 skill 的 steps/ 已于 2026-08-24 全部合入单文件，本规范（教别人怎么建 skill 的规范本身）必须同步改口径。

**改动**：
- **steps/ 目录删除**：step-1-design.md（规范完整正文）全部合入 SKILL.md 一~十节
- **规范口径修改**（规范级，覆盖正文所有 steps/ 目录设计位置）：
  - 「SOP骨架 + steps 展开层」教法 → 「单文件自包含」教法：SKILL.md 骨架节直接内联执行要点，不再建 steps/ 目录
  - 目录结构/层级职责表去掉 steps/ 展开层；「steps vs references vs templates vs scripts 区别表」缩为三类资源表
  - 删除「steps/ 文件拆分原则（按独立阶段拆）」与「step 文件自传导（加载门禁+下一步指引）」两节，新增「执行要点内联写法」（合入精炼原则：50-65% 体量控制/门禁与脚本调用方式不丢）
  - 红线❌3 改口径：自带 SOP 骨架 → 单文件自包含 + 禁止 steps/ 目录与引用
  - 检查清单/落盘检查点/创建流程/改造流程同步：新增"无 steps/ 目录、无 steps/ 引用残留"检查项，改造流程新增"发现 steps/ 合入并删目录清引用"步骤
- **保留**：资源分层原则（references/templates/scripts 外部文件合法）、scripts 代码目录规范、精简原则（红线≤7/注意力预算/信息不重复）、强弱加载保障（弱保障集合从 steps/references/templates/scripts 缩为 references/templates/scripts）
- **执行模式明确**：主agent直执（规范理解与落盘一体）
- skill.json version 6.2.0→7.0.0，description 补"单文件自包含+资源分层"口径

---

## v6.2.0 — 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v6.2.0。

## v6.1.0 — 2026-07-09

### 对齐 Skill 知识工程 PRD：SKILL.md 骨架化 + scripts 一级代码目录

**核心变化**：将 v6.0.0 的"SKILL.md 只做路由"口径修正为"SKILL.md 必须自带完整 SOP 骨架"。因为 SKILL.md 是强保障文件，必须让 agent 在不读取弱保障资源时也能理解完整流程。

**新增一级目录规范**：补充 `scripts/` 作为代码层，用于存放可执行脚本、工具代码、批处理逻辑。代码不再散落在 `references/`、`templates/` 或 skill 根目录中。

**变更清单**：

| 操作 | 文件 | 说明 |
|:-----|:-----|:-----|
| 更新 | `SKILL.md` | 增加"这个 Skill 做什么"和"怎么运作"两段；新增 SOP 骨架红线与 `scripts/` 红线 |
| 更新 | `steps/step-1-design.md` | 四层架构升级为"骨架层 + 五类资源"；补充 `scripts/` 定位、拆分原则、创建流程、检查清单 |
| 更新 | `skill.json` | 版本号更新为 v6.1.0；description 增加 SOP 骨架与 scripts 代码目录触发信息 |

---

## v6.0.0 — 2026-07-01

### 从四模式工具重构为纯规范文档

**核心变化**：pop-shared-skill-create 从"四模式工具（设计/改造/评估/审计）"重构为"一份 skill 设计规范"。

**根因**：四模式工具定位错误——这不是工具，是规范。规范的核心价值是格式规范/内容定位/路由指引/精简原则/强弱加载保障，不是分模式操作。

**变更清单**：

| 操作 | 文件 | 说明 |
|:-----|:-----|:-----|
| 重写 | `SKILL.md` | 四模式路由器 → 规范摘要（红线4条 + 强弱加载保障声明 + 速查表） |
| 重写 | `steps/step-1-design.md` | 设计模式 step → 规范主体（格式/内容定位/路由/精简原则/强弱加载/检查清单） |
| 删除 | `steps/step-2-refactor.md` | 改造模式 step，内容合并到 step-1 的"改造流程"段 |
| 删除 | `steps/step-3-evaluate.md` | 评估模式 step，审计模式整体删除 |
| 删除 | `steps/step-4-session-audit.md` | 审计模式 step，整体删除 |
| 删除 | `references/session-data-guide.md` | 审计专属 |
| 删除 | `references/toolcall-bloat-analysis.md` | 审计专属 |
| 删除 | `references/prd-specification.md` | 审计报告专属 |

**红线精简**：24条（D1-D20 + B1-B6 + C1-C5）→ 4条（读取协议/双文件/红线≤7条/版本三处一致）。格式细节降级为检查清单（4组）。

**新增**：强弱加载保障认知（SKILL.md=强保障 host注入，step=弱保障 agent可能不读）、step 文件自传导（末尾加下一步指引）。

---

---

> 历史版本条目已归档：`_archive/changelog-history/pop-shared-skill-create/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
