---
name: pop-video-brand
description: "当用户说'素材做成品宣视频/品牌宣传片/产品视频/把产品图做成视频/一键出片'时启用。读品牌素材包（规范+截图+logo）→定叙事脚本→HTML动效时间线→Playwright逐帧→ffmpeg合成MP4→火山TTS口播配音+混音。确定性渲染，不走AI视频。v1.0.0"
---

# pop-video-brand

> 品牌物料 → 品宣视频的确定性渲染管线：**读品牌素材包**（视觉规范+文案口径+产品截图+logo/吉祥物）→ 定叙事脚本 → HTML 动效时间线 → Playwright 逐帧渲染 → 完整版 ffmpeg 合成 MP4 → 火山 TTS 口播配音 + 混音。v1.0.0：steps 七件全合入单文件精炼。

**核心定位**：把"品牌素材精简包"（一堆静态图 + 品牌规范文档）组装成一支 30-40s 横版品宣视频——痛点开场 + 产品核心 + 证据/闭环 + 扩展能力 + 收尾 CTA。**不是** AI 视频生成（Seedance/GenerateVideo），是 HTML+Playwright+ffmpeg 的确定性渲染，保证文字与 UI 精确可控。

**执行模式**：Step 0 盘素材与 Step 3 预览帧审查（只读类）可派子agent执行回报、主agent落盘决策；Step 1 脚本创作（老板确认立意口播）、Step 2 动效、全量渲染、Step 4-6 合成配音混音主agent直执。

## 做什么

输入：品牌素材包（`00-先看这里` 说明 + `01-品牌规范` + `02-品牌资产` + `03-产品截图` + `04-横版版式参考`）。
输出：一支 1920×1080 30fps 的品宣视频 MP4。

核心管线：**Step 0 盘素材** → **Step 1 定脚本** → **Step 2 搭动效** → **Step 3 渲染** → **Step 4 合成** → **Step 5 TTS 配音** → **Step 6 混音**。

## 怎么操作（SOP全内联）

### Step 0 盘素材

1. **LS 递归扫描素材包**，识别四类资产：品牌规范（视觉规范/文案口径/版式参考结论）、品牌资产（logo/wordmark/吉祥物）、产品截图（每张代表一个功能价值点）、版式参考（16:9 母版/3:2 可延展构图/超宽工作流）。
2. **读品牌规范（铁律）**：视觉规范→品牌定位、色板（主色/辅助/文字/背景/线框）、吉祥物边界、截图使用规则；文案口径→一句话人设、首选叙事结构、常用表达原则、频道差异、禁用对照；版式筛选结论→默认母版、推荐保留构图、不建议做法。
3. **读关键素材+量尺寸**：Read 读 1-2 张核心截图（母版+主价值）理解界面视觉与可放大局部；Python/PIL 批量量候选图片尺寸与格式（PNG/RGBA）；确认哪些截图能支撑价值点、哪些文字密度过高不宜放大。
4. **圈定价值点与镜头组**：主价值点一句话 + 截图清单 3-4 张（主证据镜头/闭环镜头/扩展能力镜头）+ 是否用团队故事图（仅当讲"我们是谁"）。

产出 `素材清单.md`：素材包结构、品牌要点摘要、价值点、截图清单、图片尺寸表。

### Step 1 素材驱动脚本创作（本 skill 最重要的一步）

用 `references/brand-video-method.md` 的 6 步创作法，**先想清楚再写分镜**：

| 步 | 要点 |
|:--|:--|
| 1 提炼真相 | 从素材反推三问：他在解决什么（最痛问题非功能罗列）/证据是什么（哪 1-2 张截图证明被解决）/凭什么是他（差异化点）→ 写下"价值点真相"一句话 |
| 2 立定立意 | 把真相压成**一句**观众能带走的话（北极星，所有分镜服务它）；检验：删掉这句视频还成立吗？不成立才真是立意 |
| 3 选择角度 | 从角度表选一个：痛点共鸣/能力展示/成长故事/对比反差，一支视频只选一个 |
| 4 铺设结构 | 按标准五场景（开场/产品核心/证据闭环/扩展差异/收尾CTA）映射，每场景问"它推进立意吗"，不推进的砍掉不凑数；逐场景定起始时间/时长/画面元素/构图类型 |
| 5 逐镜写作 | 每镜头写三件套：**画面**（素材+构图+动效意图，供 Step 2）/ **口播**（灿灿念的旁白，承担叙事主线，口语化≤30 字/句；必须写出可配音的完整口播稿，不能只写画面）/ **字幕**（与口播互补，不逐字重复） |
| 6 闸门自检 | 删掉画面/动效描述只看字幕+口播稿逐条核对（见下），任一为否回对应小节重写，不带含糊进渲染 |

**闸门自检 6 条**：单靠文字能讲清"这是什么/解决什么问题/怎么用"？开头 3 秒有钩子观众不划走？每句都推进立意无废话？文案全部来自品牌口径无虚构？删掉品牌名后仍像真人说话？收尾有明确 CTA？

产出 `叙事脚本.md`：立意一句话 + 镜头结构表 + 每镜头（画面/口播/字幕）+ 逐秒时间轴。**确认闸门：先给老板确认立意与口播，再进渲染。**

### Step 2 搭动效时间线

按 `references/motion-timeline-guide.md` 的 render(t) 模式写单页 HTML（1920×1080）：

- **技术模式**：单页 `<body>` 固定 1920×1080、`overflow:hidden`；所有动效元素绝对定位；`window.render(t)`（t 为秒）驱动，只改 `opacity` 与 `transform`；用 `seg/ease/app/out/slide/set` 辅助函数做缓动插值。
- **品牌合规（铁律）**：色板严格用 Sky Bubble——主蓝 `#2F64FF`、泡泡青 `#26D7E8`、波浪紫 `#7B59FF`、主墨 `#141824`、正文 `#343B4D`、画布白 `#FBFDFF`、线框 `#DCE8F2`；中文字体 `"PingFang SC","Microsoft YaHei","Noto Sans CJK SC",sans-serif`；文案照抄 `叙事脚本.md`，禁止自创。
- **元素与坐标**：每场景一个 `.scene` 容器，元素用 `.el`（opacity:0 起步）；产品截图装圆角卡片（`object-fit:contain` 白底）叠浮层标签；大标题/卖点/功能矩阵绝对定位放右侧信息区；`left:50%` 居中元素在 render 里用 `translateX(-50%)` 补正。
- **时间轴**：`render(t)` 里按 `app(t,a,b)`（进场）+ `out(t,a,b)`（出场）组合每元素透明度与位移；序列元素（功能矩阵等）用循环按 `a+i*step` 逐个点亮；收尾标版吉祥物可加 `Math.sin(t)` 轻微浮动。
- **常见坑**：居中微调用 `translateX(calc(-50% + Npx))`；避免除零/NaN 变换（折算用 `app()` 值不直接除）；图片用相对路径（`assets/…`），assets 与 index.html 同目录。

### Step 3 逐帧渲染

1. **抓预览帧（铁律）**：在关键时间点（每场景中途帧+收尾定格）抓 8-12 张，逐张 Read 审查构图完整协调/文案合规对齐/无元素重叠溢出错位：
   ```
   python scripts/render_frames.py --html index.html --out preview --mode preview --times 0.5,2.0,3.5,7.0,9.6,15.0,22.0,28.0,30.0
   ```
   发现布局问题 → 回 Step 2 改 `index.html` 再抓预览，直到通过。
2. **全量渲染**：按总时长×fps 逐帧渲染：
   ```
   python scripts/render_frames.py --html index.html --out frames --mode full --fps 30 --start 0 --end 33
   ```
3. **渲染规范**：视口 1920×1080、`device_scale_factor=1`；fps 默认 30，时长以 `叙事脚本.md` 为准；中间帧放本项目 `frames/`，不污染素材包。

### Step 4 合成 MP4

- 用 `imageio-ffmpeg` 自带的完整版 ffmpeg：
  ```
  python scripts/encode.py --frames frames --out 成品.mp4 --fps 30 --crf 18
  ```
- **校验成片（铁律）**：用完整版 ffmpeg probe 成片（`ffmpeg -i 成品.mp4` 读 Duration/Stream 行）核对：分辨率 1920×1080、fps 30、时长=总时长、H.264+yuv420p、movflags faststart。时长对不上（帧数=时长×fps ±1）说明 timeline 边界有误，回查 Step 2。
- **交付**：成片放用户指定目录（默认 `d:\popwave-skills\`）+ 本地预览页（`<video controls>` 内嵌成片）。

### Step 5 TTS 配音

- **前置**：老板已确认口播文案（Step 1 产出）；火山语音已开通「豆包语音合成大模型」+ **X-Api-Key**（单头鉴权；无 Key 则提示老板到 `https://console.volcengine.com/voice` 开通并在「API Key 管理」复制）。
- **逐句生成**（每句对应一个画面/场景段）：
  ```
  python scripts/tts_generate.py --api-key <X-Api-Key> --text "口播句文案" --out "{项目}/audio/seg01.mp3"
  ```
  每句一个 `seg{N}.mp3`；默认音色**知性灿灿 2.0**（`zh_female_cancan_uranus_bigtts`，温暖专业女声），`--speaker` 可换（如 `zh_female_zhixingnv_uranus_bigtts` 知性女声）；`--speech-rate/--loudness-rate/--pitch-rate` 微调语速/音量/音调。
- **记录每句时长**：用 imageio-ffmpeg 的 ffmpeg 或 `ffprobe` 读时长，产出 `时长清单.json`（seq/file/duration_sec）。
- **完成判定**：每句文案都有对应 mp3｜时长清单含全部句的 seq/file/duration｜总时长与视频场景时长偏差可接受（口播不超画面太多）。
- **失败处理**：某句失败只重试该句不中断整批；重试仍失败则 `--speaker` 换备用音色或对文案做口语化微调。

### Step 6 混音

1. **拼接配音轨**：按 `时长清单.json` 顺序，用 ffmpeg `concat` 把 `seg*.mp3` 拼成完整 `narration.wav`（句间可加 0.2-0.4s 静音呼吸）。
2. **混音**（完整版 ffmpeg；BGM 可选——老板已选定才加，否则跳过 BGM 只配音）：
   ```
   ffmpeg -y \
     -i 成品.mp4 -i narration.wav [-i bgm.mp3] \
     -filter_complex [三路音量/淡入淡出/叠加] \
     -map 0:v -map [mix] -c:v copy -c:a aac -b:a 192k \
     -shortest 成品-配音.mp4
   ```
   口播音量 1.0、BGM 0.3-0.5 不压人声（实操验证：BGM 盖过口播时压至 0.15、口播提至 1.1）；BGM 淡入 0.8s、淡出 2.5s；需精确卡点时用 `adelay=ms|ms` 为每句配音设起始偏移再 `amix` 合成——品宣口播通常整段铺在画面上即可，不必逐字卡点。
3. **完成判定**：视频+口播+BGM 三轨混音正常｜probe 校验 1920×1080、时长正常、有音轨｜试听口播清晰、BGM 不压人声。

## 产出文件结构

```
{video项目}/
├── 素材清单.md               # Step 0 产出
├── 叙事脚本.md               # Step 1 产出（立意+分镜+画面/口播/字幕+时间轴）
├── index.html                # Step 2 产出（动效时间线，单文件）
├── assets/                   # Step 2 拷贝的截图/logo/吉祥物
├── preview/                  # Step 3 校验帧
├── frames/                   # Step 3 全量帧 f_%05d.png
├── audio/                    # Step 5 配音 seg{N}.mp3 + 时长清单.json
├── 成品.mp4                  # Step 4 无音轨视频
└── 成品-配音.mp4             # Step 6 最终视频（口播+可选BGM）
```

## ❌ 铁律

| # | 铁律 | 违反后果 |
|:-:|:-----|:---------|
| ❌1 | **品牌合规** — Step 0 必须读品牌规范（视觉+文案）；色板严格用 Sky Bubble，文案严格用品牌口径，禁止自创配色或夸大文案 | 品牌识别崩塌，物料不可对外 |
| ❌2 | **一个价值点、3-4 张截图** — 每支视频只讲一个价值点，最多 3-4 张界面图，不把全部截图塞进一支片 | 信息过载，观众记不住主卖点 |
| ❌3 | **确定性渲染，不走 AI 视频** — 用 HTML+Playwright+ffmpeg 合成，禁止 Seedance/GenerateVideo 按秒生成的 AI 视频 | 文字/UI 被 AI 扭曲、成本失控、版式不可控 |
| ❌4 | **先预览后出片** — Step 3 必须抓预览帧逐张校验，通过后才全量渲染合成 | 构图/文案错误带进成品，整片返工 |

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 动效写法 | `references/motion-timeline-guide.md` | Step 2 编写 HTML 时 |
| 色板/文案 | `references/sky-bubble-palette.md` | Step 1/2 文案与配色时 |
| 叙事方法论 | `references/brand-video-method.md` | Step 1 定镜头结构时 |
| 渲染帧 | `scripts/render_frames.py` | Step 3 执行 |
| 合成视频 | `scripts/encode.py` | Step 4 执行 |
| TTS 配音 | `scripts/tts_generate.py` | Step 5 执行 |
| 中文字体 | `Noto Sans CJK SC` / `WenQuanYi Micro Hei` | HTML 排版时设置 |

## 前置条件

1. Python 3.8+ + Pillow + numpy
2. Playwright + Chromium（HTML 逐帧截图）
3. `imageio-ffmpeg`（自带完整版 ffmpeg，能处理 PNG + libx264）
   - 系统精简版 ffmpeg（仅 scale/fps 滤镜）**不够用**，必须用 imageio-ffmpeg 的完整二进制
4. 火山语音「豆包语音合成大模型」已开通 + X-Api-Key（Step 5 配音用，不需要则跳过配音）
5. 品牌素材包存在（规范 + 截图 + logo）

## 版本

**当前版本**：v1.0.0 | 2026-08-24 — steps 七件全合入单文件精炼，执行模式明确。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。
