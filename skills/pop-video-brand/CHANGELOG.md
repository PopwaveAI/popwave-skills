# CHANGELOG

## v1.1.0 | 2026-08-31

### 去AI味
- 五场景结构术语「证据/闭环」改为「证据收束」（空洞名词清理），共3处
- 同步 skill.json（version）

---

## v1.0.0 — 2026-08-24

### steps 七件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step0-inventory / step1-script / step2-timeline / step3-render / step4-encode / step5-tts / step6-mix 七件全部合入 SKILL.md「怎么操作（SOP全内联）」对应步骤节
- **执行模式明确**：Step 0 盘素材与 Step 3 预览帧审查（只读类）可派子agent执行回报、主agent落盘决策；Step 1 脚本创作（老板确认立意口播）、Step 2 HTML 动效、全量渲染、合成配音混音主agent直执
- **内容精炼**：Step 1 六步创作法整理为单表；各 step 的"目的/传导"过渡段删除（信息已在骨架管线中）；全部命令模板/色板值/音色参数/完成判定原样保留
- **口径补全**：混音音量并入 v0.3.0 实操验证值（BGM 过响压至 0.15、口播提至 1.1），消除 CHANGELOG 与正文不一致
- references/（brand-video-method / motion-timeline-guide / sky-bubble-palette）与 scripts/（render_frames / encode / tts_generate）保持外部文件不变
- skill.json version 0.4.0→1.0.0

---

## v0.4.0 | 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v0.4.0。

## v0.3.0 | 2026-08-06

重点优化脚本创作环节（老板定位为本 skill 最重要的一步）。

### 优化
- Step 1 升级为**素材驱动脚本创作**：`references/brand-video-method.md` 重写为 6 步创作法（提炼真相 → 立定立意 → 选择角度 → 铺设结构 → 逐镜写作 → 闸门自检）
- 逐镜三件套：画面 + 口播 + 字幕，口播承担叙事主线（配合 TTS）
- 新增闸门自检：删画面只看稿件，验证"讲得清/有钩子/无废话/口径合规/像真人说话/有CTA"
- 反对"套模板塞素材"，强调"先想清楚再写"、功能位为立意服务、不凑数

### 实操验证
- 修正 BGM 音量：0.35 → 0.15，口播 1.0 → 1.1，解决 BGM 盖过口播。

## v0.2.0 | 2026-08-06

新增 TTS 配音与混音，品宣视频可带口播人声。

### 新增
- Step 5 TTS 配音：`scripts/tts_generate.py` 调火山语音「豆包语音合成」（`seed-audio-1.0`），默认音色**知性灿灿 2.0**（`zh_female_cancan_uranus_bigtts`，温暖专业女声）
- Step 6 混音：完整版 ffmpeg 把配音轨 + 可选 BGM 混入 `成品.mp4`，口播 1.0 / BGM 0.3-0.5
- 火山语音接入说明写进 `steps/step5-tts.md` 前置（开通豆包语音合成大模型 + X-Api-Key）

### 铁律（新增）
- TTS 默认音色灿灿，可 `--speaker` 替换；口播不盖 BGM、BGM 不压人声

### 实操验证
- 用火山语音 X-Api-Key 实测后确定灿灿 2.0 为默认，生成 3 款音色试听，老板选定灿灿。

---

> 历史版本条目已归档：`_archive/changelog-history/pop-video-brand/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
