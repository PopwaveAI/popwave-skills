# CHANGELOG

## v1.7.0 | 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v1.7.0。

## v1.6.0（2026-08-08）

### 改造：`batch_test.py` 画风定标素材 = 小说次要视觉锚点

老板定调——画风 skill 不应出主要人物形象测画风（画风可能满意但形象不满意，而画风 skill 不是为设计人物而生）；但也**不用与小说无关的中性材料**（ahament 代入感会弱很多）。**画风定标默认用【和小说相关但无关紧要的次要元素】测画风**——某个战斗场景/地点、路人/NPC/龙套。

- `scripts/batch_test.py` 升级 v1.4：新增 `--scene`（小说场景/地点/战斗场景描述，替换变体场景段）+ `--side`（路人/NPC/龙套描述，替换变体角色段，非主角、不需一致性、纯文生图）；`--character`/`--character-image` 标记废弃（传入即警告并回退）；不传 scene/side 则兜底用脚本内置中性素材；PE 日志 test_mode 记录素材来源
- PE 日志 SOP 版本至 v1.4；头部文档化素材策略说明
- 同步 `pop-visual-style` step4/SKILL 铁律❌5（见其 v1.9.0）、`pop-visual-comic` pe-test-sop（v1.8）
- 版本同步：SKILL.md / skill.json 至 v1.6.0

## v1.5.0（2026-08-08）

### 新增：品牌水印脚本（图片一级像素级注入）

老板要求给所有生图产出叠加合理的 `popwave.cn` 水印，且不进提示词（避免污染 Seedream 文生图质量）。

- 新增 `scripts/watermark.py`：图后处理叠加半透明小字水印（默认右下角，alpha=80 约31%不透明，低调可见）
- **幂等**：通过元数据标记（PNG tEXt chunk / JPEG comment）判定已含水印，重复运行不叠加；经实测 JPG/PNG 首次加印、二次跳过、dry-run 检测均通过
- 源码级配置：文字/位置/透明度/字号/边距比例，支持多图批量、`--dry-run` 校验
- 共享组件清单 + 引用协议 + SKILL.md 速查更新；版本同步至 v1.5.0

---

> 历史版本条目已归档：`_archive/changelog-history/pop-visual-shared/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
