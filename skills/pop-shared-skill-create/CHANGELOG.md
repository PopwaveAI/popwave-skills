# CHANGELOG — pop-shared-skill-create

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
