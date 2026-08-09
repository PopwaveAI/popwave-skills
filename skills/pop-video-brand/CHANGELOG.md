# CHANGELOG

## v0.4.0 | 2026-08-09

### 新增首次对话引导（onboarding）

**背景**：老板定调——每个 C 端专家需要一份面向品牌运营/主理人（非产品经理/AI 专家）的首次对话引导语，用"你能把品牌素材变成什么"的场景快速建立认知，而非介绍内部架构。

**改动**：

- 新增 `references/onboarding-guide.md`：C 端口吻引导语（一句话说清 + 你有这些玩法 + 你不用担心 + 就这样开始），覆盖静态素材→宣传视频/自动口播/一条龙出片
- `SKILL.md`：新增「🚪 首次对话引导」区块——用户首次触发时直接输出引导语全文，再进 Step 0 盘素材
- 版本至 v0.4.0

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

## v0.1.0 | 2026-08-06

首版发布：品牌物料 → 品宣视频的确定性渲染 skill。用 Popwave 品宣视频实操验证通过。

### 新增
- 五步管线：Step 0 盘素材 → Step 1 定脚本 → Step 2 搭动效 → Step 3 渲染 → Step 4 合成
- 品牌合规：Step 0 必读品牌规范，Sky Bubble 色板 + 品牌文案口径（`references/sky-bubble-palette.md`）
- 叙事方法论：一个价值点、3-4 张截图，四要素镜头结构（痛点/核心/证据/扩展/收尾，`references/brand-video-method.md`）
- 动效模式：JS 驱动 render(t) 逐帧渲染（非 CSS keyframes），含 seg/ease/app/out/slide/set 辅助函数（`references/motion-timeline-guide.md`）
- 渲染：`scripts/render_frames.py`，preview 抓关键帧校验 + full 全量逐帧
- 合成：`scripts/encode.py`，用 imageio-ffmpeg 完整版 ffmpeg 合成 H.264 MP4

### 铁律
- ❌1 品牌合规（色板+文案口径，禁止自创）
- ❌2 一个价值点、3-4 张截图
- ❌3 确定性渲染，不走 AI 视频（Seedance/GenerateVideo）
- ❌4 先预览帧校验后全量出片

### 实操验证
- 用 Popwave 素材精简包 V2（佩戴 2026-08-06）产出 33s 品宣视频：痛点开场→产品核心→写作闭环→出圈→CTA，1920×1080 30fps。