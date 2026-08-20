# CHANGELOG

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
