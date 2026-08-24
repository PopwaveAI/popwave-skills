# CHANGELOG

## v2.0.0 — 2026-08-24

### steps 四件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step0-research / step0-scene-understand / step1-design / step2-generate 四件全合入 SKILL.md 对应 SOP 节（Step 0 意图分析+搜图选图 / Step 0-Scene 原文理解管线 / Step 1 设计方案 / Step 2 生成资产）
- **执行模式明确**：门禁A（选图对齐/理解确认）与门禁B（方案对齐）用户多轮交互主 agent 直执；Pinterest 搜图+图片分析、原文解构与上下文补全（WebSearch）等只读类工作可派子 agent 回报结果、主 agent 整合落盘；翻译与生成是工具调用主 agent 直执
- **内容精炼**：门禁A/B 呈现模板与落盘格式、参考点选项清单、参考点→设计范围/提示词策略双表、放开吸收公式+四条关键原则、V3 结构化公式+11条翻译规则、Seedance 公式、反向强化技巧、data URI 注意事项、安全转换五规则、上下文补全三路径、叙事瞬间选取四依据、降级机制五档、自检清单全保留；SKILL.md 原 Step 0 摘要（资产优先/美术设定集唯一真源/cover 轻量档位）并入 Step 0-Scene；删两段长翻译示例（规则已编码同一逻辑）；迭代模式快速路径"进入 steps/step2-generate.md"改指 Step 2
- skill.json version 1.8.0→2.0.0

---

## v1.8.0 | 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v1.8.0。

## v1.7.0 | 2026-08-09

### 落盘三态对齐（候选→测试/封面，记录→_过程/提示词记录）

按 `pop-visual-pipeline/references/落盘规范.md`：封面/场景候选图从 `素材/视觉/` 迁到 `测试/封面/`，确认后复制到 `成品/封面/`（加 `-final`）；设计记录 `素材/视觉设计方案.md` 迁到 `_过程/提示词记录.md`。`step0-research/step0-scene-understand/step1-design/step2-generate` 与 `SKILL.md` ❌4 同步。

## v1.6.0 | 2026-08-05

### 消费链路对齐：cover 意图 = 轻量基建

老板审视全链路发现——cover 消费链路未声明档位，需明确 cover 意图只需基建到身份卡即可派生，不强制双角度定妆：

- `SKILL.md` Step 0-Scene 新增档位说明：Pipeline 语境下 cover 只需身份卡（轻量档），**不强制双角度定妆**；如需角色参考图用 character 单张定妆图
- 版本同步：SKILL.md / skill.json 至 v1.6.0

---

> 历史版本条目已归档：`_archive/changelog-history/pop-visual-cover/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
