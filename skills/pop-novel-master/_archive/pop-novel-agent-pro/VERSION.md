# Vibe Creating · Popwave — 版本体系

> 当前版本：**v0.4**（2026-05-26）
> 项目定位：创造者操作系统 · 全管道编排者

---

## 项目版本体系

| 版本 | 日期 | 核心变更 |
|:---:|:---:|:---|
| **v4.0** | 2026-05-31 | **Spec 模式深度整合**。新增 spec-bridge 桥接层（spec.md/tasks.md/checklist.md）。审批闸门机制。Spec 贯穿六阶段管线。checklist 自动化验证。POP-ROUTER 新增 spec 路由。 |
| **v3.3** | 2026-05-26 | **Gap修复 + 管线硬化 + 设定结构化 + 健壮性全量加固**。第一轮：基于全量Gap曝光报告（25项）系统性修复。修复 P0 注入层（原始设定注bundle、bundle 9项→14项、锚定章正则）。修复 P0 数据层（EntityUpdater双格式检测、state_changelog写入、智能实体自动创建）。修复 P0 执行层（字数/否定句硬闸门RuntimeError阻断）。修复 验证层（否定句2→5变体）。升级 元设计层（Director-prompt前置检查6项强制）。第二轮：57处硬编码路径清除、resolve_path桥接11条路径、pre_flight 7项→15项检查、init_project.py 新建（单命令创建完整项目骨架）、setting-index.yaml 结构化设定注入（0→17实体）、context-bundle自动加载。新增 `_工具配置/_SKILL_DESIGN_STANDARD.md` 通用Skill设计规范（8条原则）。emergent-writer v9.3.0。 |
| **v3.2** | 2026-05-25 | 全 Skill 升级 + 标准化 + 结构规范 + 强依赖代码化。book-deconstructor v4.8。project-bootstrap v2.8。plot-architecture v2.7。qa-payoff v0.4.1。emergent-writer scripts升级（reader_profile注入+锚定章加载+autocheck）。opening-arc v1.2。market-test v1.3。_continuation v2.0。book-opinion-tracker v1.8。全15个SKILL.md标准化。文件夹瘦身。 |
| **v3.1** | 2026-05-25 | ESM v2.0 bugfix + 否定句全覆盖 + act-01.yaml 硬件约束升级。emergent-writer v9.2。 |
| **v3.0** | 2026-05-24 | ESM v2.0 SQLite 全书数据中台 + Pass 1/Pass 2 分离。 |

---

## Skill 版本对照表

| Skill | 版本 | 状态 | 管道位置 | 描述 |
|:-----|:---:|:----:|:--------:|:-----|
| **spec-bridge** | **1.0.0** | ✅ 已迁至 _soul/spec-bridge/ | 0 | ★ Spec 桥接层 — 统一合并至 `_soul/spec-bridge/`（v3.3.1 去重行动） |
| **pop-orchestrator** | **1.0.0** | ✅ | 0 | ★ 全管道编排引擎 |
| **project-bootstrap** | **2.8.0** | ✅ **v3.3** | 1 | 开书启动：reader_profile模板 + 数值体系升级 + 超越性硬检查 |
| **plot-architecture** | **2.7.0** | ✅ **v3.3** | 2 | 剧情架构：新增事件数/scene_type/字数3项基线检查 |
| **opening-arc** | **1.2.0** | ✅ **v3.3** | 3 | 黄金三章专用引擎 + reader_profile感知 + 字数基线2200-2500 |
| **emergent-writer** | **9.3.0** | ✅ **v3.3** | 4 | ★ 正文写作引擎（六阶段管线。Hard闸门+否定句5变体+锚定章3格式+14项完整bundle+原始设定注入+autocheck） |
| **market-test** | **1.3.0** | ✅ **v3.3** | 5 | 市场验证：reader_profile感知 + 拆解报告注入 |
| **qa-payoff** | **0.4.1** | ✅ **v3.3** | 6 | ★ QC纯感受报告 + 三层介入（大纲层/骨架层/正文层）+ QC-renderer.md 模板 |
| **book-deconstructor** | **4.8.0** | ✅ **v3.3** | 7 | ★ 模式D体系拆解 + 模式E大纲密度拆解，产出物统一至拆解报告/ |
| **horror-game-writer** | 2.0.0 | ⏸️ 待定 | 8 | 诡异游戏写作引擎 |
| **html-renderer** | 1.3.0 | ✅ | 9 | HTML化发布引擎 |
| **cnovel-research** | 1.3.0 | ✅ 顶层 skill | 10 | 网文调研 — 内部副本已删除（v3.3.1），使用顶层 `skills/cnovel-research/` |
| **book-opinion-tracker** | **1.8.0** | ✅ 已迁至顶层 | 11 | 网文舆情追踪 — 已提升为顶层 `skills/book-opinion-tracker/`（v3.3.1） |
| **自动化质检** | **1.0.0** | ✅ **v3.3 新建** | — | ★ 元技能——对任何Skill做结构化质量检测（审计追溯+LLM验证+质量闸门） |
| **web-access** | 2.4.3 | ✅ | 0 | 联网统一入口 |
| **continuation** | **2.0.0** | ✅ **v3.3** | 0 | 续写适配（一次性）：reader_profile + 数值体系 + 写作资产路径对齐 |
| **novel-bootstrap** | 2.2.0 | ❌ **废弃** | 99 | 被 project-bootstrap v2.8 完全覆盖 |

---

## 废弃/排出版本

| Skill | 最后版本 | 状态 | 原因 |
|:-----|:-------:|:----:|:-----|
| novel-bootstrap | v2.2 | ❌ 废弃 | 被 project-bootstrap v2.8 完全覆盖 |
| skill-chapter-outline | v2.0 | ❌ 废弃 | 目录已删除 |
| skill-novel-pipeline | v1.0 | ❌ 废弃 | 被 emergent-writer 取代 |
| skill-qc | v1.0 | ❌ 废弃 | 被 qa-payoff 取代 |
| skill-reader-qa | v3.0 | ❌ 废弃 | 被 market-test 取代 |

---

## 版本规则

1. **项目主版本**（v3.x）只在有跨层架构变更时递增
2. **Skill 版本**独立迭代，遵循语义化版本
3. 废弃的 Skill 在版本表中保持不变，状态标记为 ❌
4. 每个 Skill 的 `SKILL.md` 中的版本号是真实版本来源

---

> 最后更新：v3.3 · 2026-05-26
