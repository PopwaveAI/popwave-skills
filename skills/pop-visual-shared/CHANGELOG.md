# CHANGELOG

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

## v1.4.0（2026-08-05）

### 升级：生图改走 image_generate 工具，移除内置 API Key

老板要求所有 skill 生图环节改用 `image_generate` 工具，清理硬编码 API Key（Pinterest 搜索保持不动）：

- `generate.py` image 子命令彻底改为**任务导出**模式（`export_image_task`）：不再直连 `images/generations` API，不内置任何 key，只导出单条任务（id/prompt/size/ref_images/output_path）供主 agent 用 `image_generate` 工具生成
- `batch_test.py` 改为**任务清单导出**：移除 `API_URL`/`API_KEY`/`MODEL`/HTTP 直连，`export_tasks()` 导出 `generation_tasks.json`；保留 `_assert_size_safe` 尺寸校验与 `pe-log.json` 可复现日志
- `generate.py` video 子命令（Seedance）保留但**不再内置 key**，必须显式设置 `ARK_API_KEY` 环境变量，否则拒绝执行
- 移除内置 Seedream key `b597f4e5-2370-...`；Pinterest 的 BRIGHTDATA key 保持不变（未授权改动）
- 消费方（cover/oc/style/comic/character）的 step 文档与 SKILL.md 统一更新为 `image_generate` 工具流程

## v1.3.0（2026-08-04）

### 新增：出图尺寸硬上限（防止报价翻倍）

老板要求营销出图全部约束总像素 ≤ 236 万（Seedream 5.0 Pro 计费临界，超 236 万输出图从 0.3 元/张翻倍到 0.6 元/张）。

- `generate.py` 新增 `MAX_PIXELS = 2360000` + `assert_size_safe()`：payload 组装前校验，超限/无法解析直接报错中止
- `batch_test.py` 新增 `MAX_PIXELS` + `_assert_size_safe()`，默认尺寸 1125x1500（169 万）；`2K`/`4K` 档位超上限被拒绝
- `references/seedream-prompt-guide.md` §八 尺寸表新增铁律：所有出图总像素 ≤ 236 万，仅支持 1K 档位
- 文档尺寸示例统一为安全尺寸 1125x1500 / 1500x1500 / 1500x1125

## v1.2.0（2026-08-04）

### 升级：`batch_test.py` 支持画风×项目角色联合测试

老板实测发现"固定中性素材"无法验证画风能否撑起项目角色（玄鉴仙族用中性"现代青年+木屋"测画风，测不出"黑金甲衣+金瞳"主角的适配度）。画风测试默认用项目真实角色当测试素材：

- `batch_test.py` 新增 `--character`（项目角色描述，替换标准测试角色）+ `--character-image`（角色参考图，转 data URI 图生图，保证角色一致性）
- 仅排查"画风本身是否被执行"时才用中性素材（`--character` 不传）
- PE 日志新增 `test_mode` / `character_desc` / `character_image` 字段，可复现
- 被 `pop-visual-style` step4（v1.4.1）与 `pop-visual-comic` pe-test-sop（v1.6）消费

## v1.1.0（2026-08-04）

### 新增：固定画风测试脚本 `batch_test.py`

把画风测试固化为"固定 SOP + 并发批量"，杜绝每次测试全新设计、不稳定、慢：

- 新增 `scripts/batch_test.py`：固定测试素材（标准角色+标准场景）+ 固定 6 段式模板 + 并发批量（默认 8 线程）+ 自动 `pe-log.json`
- 画风测试唯一标准入口：`--style-names` 从 DNA 库批量取变体，或 `--config` 精调变体；`--seed` 固定种子，输出按 `seed-{seed}` 分级，同 seed 重跑即复现对比
- 被 `pop-visual-style` step4 画风定标与 `pop-visual-comic` pe-test-sop 消费

## v1.0.0（2026-08-04）

新建共享底层资产层。收敛视觉 skill 群中重复、分化、过时的底层资产为唯一权威源：
- `scripts/generate.py`：Seedream 生成脚本（合并自 cover/oc/style/base 4 份字节相同副本）
- `scripts/pinterest_search.py`：Pinterest 参考搜索脚本（合并自 cover/oc/base 3 份字节相同副本）
- `references/seedream-prompt-guide.md`：统一提示词指南（合并 pop-visual-style 的 6 段式 + pop-visual-oc 的 V3/高精度/Seedance，消除 4 份分化副本）
- 定义画风 DNA 库（`style-dna-library.json`）跨 skill 引用协议，归属仍为 pop-visual-style

本 skill 不独立落地生成，仅被其他视觉 skill 引用。