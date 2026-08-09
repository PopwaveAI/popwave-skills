---
name: pop-video-brand
description: "当用户说'素材做成品宣视频/品牌宣传片/产品视频/把产品图做成视频/一键出片'时启用。读品牌素材包（规范+截图+logo）→定叙事脚本→HTML动效时间线→Playwright逐帧→ffmpeg合成MP4→火山TTS口播配音+混音。确定性渲染，不走AI视频。v0.2.0"
---

# pop-video-brand

> 品牌物料 → 品宣视频的确定性渲染管线。**读品牌素材包**（视觉规范+文案口径+产品截图+logo/吉祥物）→ 定叙事脚本 → HTML 动效时间线 → Playwright 逐帧渲染 → 完整版 ffmpeg 合成 MP4 → 火山 TTS 口播配音 + 混音。v0.4.0：新增首次对话引导（references/onboarding-guide.md，C端口吻，面向品牌运营/主理人）。v0.2.0

**核心定位**：把"品牌素材精简包"（一堆静态图 + 品牌规范文档）组装成一支 30-40s 横版品宣视频——痛点开场 + 产品核心 + 证据/闭环 + 扩展能力 + 收尾 CTA。**不是** AI 视频生成（Seedance/GenerateVideo），是 HTML+Playwright+ffmpeg 的确定性渲染，保证文字与 UI 精确可控。

**先校验后出片（铁律）**：Step 3 先抓预览帧人工（agent）逐张校验构图与文案，通过后才全量渲染合成。禁止跳过预览直接出片。

## 做什么

输入：品牌素材包（`00-先看这里` 说明 + `01-品牌规范` + `02-品牌资产` + `03-产品截图` + `04-横版版式参考`）。
输出：一支 1920×1080 30fps 的品宣视频 MP4。

核心管线：**Step 0 盘素材** → **Step 1 定脚本** → **Step 2 搭动效** → **Step 3 渲染** → **Step 4 合成** → **Step 5 TTS 配音** → **Step 6 混音**。

## 怎么运作

### Step 0：盘素材 → `steps/step0-inventory.md`
LS 扫素材包 + 读品牌规范 + 量图片尺寸 + 圈定价值点与镜头组（每片一个价值点、3-4 张截图）。产出 `素材清单.md`。

### Step 1：素材驱动脚本创作 → `steps/step1-script.md`
**本 skill 最重要的一步。** 用 `references/brand-video-method.md` 的 6 步创作法：从素材提炼真相 → 立定立意 → 选角度 → 铺设结构 → 逐镜写作（画面+口播+字幕）→ 闸门自检。先想清楚再写分镜，每镜头三件套，口播承担叙事主线。产出 `叙事脚本.md`，**先确认立意与口播再进渲染**。

### Step 2：搭动效 → `steps/step2-timeline.md`
按 `references/motion-timeline-guide.md` 的 render(t) 模式写单页 HTML（1920×1080），严格用 `references/sky-bubble-palette.md` 色板与文案。产出 `index.html` + `assets/`。

### Step 3：渲染 → `steps/step3-render.md`
`render_frames.py` 先 `--mode preview` 抓关键帧校验构图/文案/溢出，通过后 `--mode full` 逐帧渲染。产出 `preview/` + `frames/`。

### Step 4：合成 → `steps/step4-encode.md`
`encode.py` 用 imageio-ffmpeg 完整版 ffmpeg 合成 H.264 MP4，probe 校验分辨率/时长/fps。产出 `成品.mp4`。

### Step 5：TTS 配音 → `steps/step5-tts.md`
`tts_generate.py` 调火山语音「豆包语音合成」按口播文案逐句生成人声 MP3。默认音色**知性灿灿 2.0**（`zh_female_cancan_uranus_bigtts`，温暖专业女声）。产出 `audio/seg{N}.mp3` + `时长清单.json`。

### Step 6：混音 → `steps/step6-mix.md`
用完整版 ffmpeg 把配音轨（+可选 BGM）混入 `成品.mp4`，口播音量 1.0、BGM 0.3-0.5 不压人声。产出 `成品-配音.mp4`。

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

## 🚪 首次对话引导（onboarding）

> 用户第一次触品牌宣视频专家（无任何品牌视频项目、非续写场景）时，**先输出 `references/onboarding-guide.md` 的引导语内容**给用户建立认知，再进入 Step 0 盘素材。
>
> 展示方式：在回复中**直接粘贴 `references/onboarding-guide.md` 全文**（声明本次为功能介绍+引导、未执行 skill 任务），用 1-2 句口头补充"报素材位置+想讲什么卖点就开始"。若用户已明确要出片，可跳过引导直接干活。

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
| 盘素材 | `steps/step0-inventory.md` | Step 0 开始时 |
| 定脚本 | `steps/step1-script.md` | Step 1 开始时 |
| 搭动效 | `steps/step2-timeline.md` | Step 2 开始时 |
| 动效写法 | `references/motion-timeline-guide.md` | Step 2 编写 HTML 时 |
| 色板/文案 | `references/sky-bubble-palette.md` | Step 1/2 文案与配色时 |
| 叙事方法论 | `references/brand-video-method.md` | Step 1 定镜头结构时 |
| 渲染帧 | `scripts/render_frames.py` | Step 3 执行 |
| 合成视频 | `scripts/encode.py` | Step 4 执行 |
| TTS 配音 | `scripts/tts_generate.py` | Step 5 执行 |
| 混音 | `steps/step6-mix.md` | Step 6 执行 |
| 中文字体 | `Noto Sans CJK SC` / `WenQuanYi Micro Hei` | HTML 排版时设置 |

## 前置条件

1. Python 3.8+ + Pillow + numpy
2. Playwright + Chromium（HTML 逐帧截图）
3. `imageio-ffmpeg`（自带完整版 ffmpeg，能处理 PNG + libx264）
   - 系统精简版 ffmpeg（仅 scale/fps 滤镜）**不够用**，必须用 imageio-ffmpeg 的完整二进制
4. 火山语音「豆包语音合成大模型」已开通 + X-Api-Key（Step 5 配音用，不需要则跳过配音）
5. 品牌素材包存在（规范 + 截图 + logo）

## 版本

**当前版本**：v0.4.0 | 2026-08-09
> 优化：Step 1 升级为素材驱动脚本创作（最重要环节），新增 6 步创作法 + 口播作为第一叙事线。

> 完整版本历史见 `CHANGELOG.md`。