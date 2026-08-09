---
name: pop-video-comic
description: "当用户说'漫画转视频/漫画短视频/章节条漫做成视频/漫画口播视频/漫画配音视频'时启用。读图自理解漫画页→产出口播脚本→TTS配音→HTML+ffmpeg合成PPT放映式短视频。先脚本后出片，脚本经确认后再配音合成。"
---

# pop-video-comic

> 漫画转 PPT 放映式短视频管线。**模型读图自理解**（图片为主，`页面配置.json` 文字兜底）→ 口播脚本 → edge-tts 配音 → HTML+ffmpeg 合成。**先脚本后出片**，脚本是老板确认闸门。v0.1.0

**核心定位**：把已成稿的漫画页（page1~N.png + 页面配置.json + OC/封面）组装成"PPT 放映式"短视频——静态图 + Ken Burns 推拉 + 字幕 + 人声口播 + BGM，最终合成 MP4。**不是** AI 视频生成（Seedance 那种），是确定性渲染。

**先脚本后出片（铁律）**：Step 2 产出 `口播脚本.md` 后必须**停下来等老板确认**，脚本确认后才进入 Step 3 配音 + Step 4 合成。禁止跳过确认直接出片。

## 做什么

输入：漫画页图片（page1~N.png）+ `页面配置.json`（每页文字锚点）+ 可选 OC/封面。
输出：1 分钟级短视频 MP4（图+字幕+人声口播+Ken Burns）。

核心管线：**Step 0 收集** → **Step 1 读图理解** → **Step 2 脚本创作【确认闸门】** → **Step 3 TTS 配音** → **Step 4 渲染合成**。

## 模型说明

| 工序 | 工具/方式 | 说明 |
|:-----|:---------|:-----|
| 读图理解（画面白描） | 模型多模态读图 | 主 agent 直接 Read 图片，产出每页画面理解 |
| 脚本创作 | DeepSeek/主 agent | 叙事方法论，产出口播脚本 |
| TTS 配音 | `edge-tts`（免费） | 微软神经语音，中文音色多，无需 API Key |
| 视频合成 | Playwright 截图 + ffmpeg | 复用漫画 HTML 美学，纵向滚动→横向影片 |

> 视频合成**不**走 Seedance/GenerateVideo——那是 AI 生成视频（不可控、按秒计费），本 skill 是确定性 PPT 放映式渲染，纯本地。

## 怎么运作

### Step 0: 收集素材 → `steps/step0-collect.md`

- 扫描漫画章目录：`output/page1~N.png` + `index.html` + `页面配置.json`
- 读 `页面配置.json` 提取每页文字锚点（台词/旁白/OS）
- 定位 OC/封面图（开场用）
- 产出素材清单

### Step 1: 读图理解 → `steps/step1-understand.md`

- 逐页 Read 漫画图，产出每页【画面白描 + 氛围标签 + 镜头感】
- **审查兜底**：图片被安全拦截时，用 `页面配置.json` 对应文字补全画面理解，禁止因读图失败中断
- 产出 `画面理解.md`

### Step 2: 脚本创作 → `steps/step2-script.md` 【🚪 老板确认闸门】

- 基于画面理解 + 文字锚点，写口播脚本：**钩子开头 + 情绪线 + 每页对应 1-2 句口播**
- 每句口播明确绑定到具体某页（保证时长对齐）
- 估算总时长（目标 ~60 秒）
- 产出 `口播脚本.md` → **停下来等老板确认**，确认后才继续

### Step 3: TTS 配音 → `steps/step3-tts.md`

- `edge-tts` 按脚本逐句生成人声，记录每句音频时长
- 输出 `audio/` 目录分句音频 + 时长清单

### Step 4: 渲染合成 → `steps/step4-render.md`

- HTML/CSS 排版（复用漫画美学）+ Playwright 截图逐帧
- 图 + 字幕 + 人声 + Ken Burns + BGM → ffmpeg 合成 MP4
- 产出 `第{N}章-v{版本}-final.mp4`（配音版→`第{N}章-配音-v{版本}-final.mp4`，见落盘规范 §3.1b）

## 产出文件结构

> 落盘遵循 `pop-visual-pipeline/references/落盘规范.md` §3.1b §五 §六：视频成品必须版本化+`-final`，`preview/frames/audio/` 是过程。

```
{漫画项目}/视频/
├── 画面理解.md              # Step 1 产出（逐页白描+氛围）
├── 口播脚本.md              # Step 2 产出（脚本，确认闸门）
├── audio/                   # Step 3 产出（分句配音）
│   ├── seg01.mp3 ...
│   └── 时长清单.json
├── frames/                  # Step 4 中间帧（过程）
├── preview/                 # Step 4 预览帧（过程）
└── 第{N}章-v{版本}-final.mp4   # Step 4 最终视频（确认后，配音版→第{N}章-配音-v{版本}-final.mp4）
```

## ❌ 铁律

| # | 铁律 | 违反后果 |
|:-:|:-----|:---------|
| ❌1 | **先脚本后出片** — Step 2 产出 `口播脚本.md` 后必须停下来等老板确认，确认后才进 Step 3 配音 + Step 4 合成。禁止跳过脚本确认直接出片 | 方向跑偏，口播内容与画面不符，整段返工 |
| ❌2 | **读图为主、配置文字兜底** — 页面理解以模型读图为主，`页面配置.json` 文字做锚点；图片被安全审查拦截时用配置文字补全，禁止因读图失败中断管线 | 审查拦截页导致管线断裂，无法产出完整视频 |
| ❌3 | **每句口播必须绑定具体页** — 脚本中每句口播明确标注对应 `page{N}`，保证时长对齐与字幕同步 | 口播与画面错位，字幕不同步，成品不可用 |
| ❌4 | **视频合成走确定性渲染，不走 AI 视频** — 用 HTML+Playwright+ffmpeg 合成，禁止用 Seedance/GenerateVideo 按秒生成的 AI 视频 | 成本失控、画面不可控、与"PPT 放映式"定位相悖 |
| ❌5 | **视频成品版本化+final** — 确认后视频命名 `第{N}章(-配音)-v{版本}-final.mp4`，禁止裸名 `成品.mp4`；`preview/frames/audio/` 是过程不进成品态（见落盘规范 §3.1b §六） | 多版本无法区分、误当候选清掉 |

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 收集素材 | `steps/step0-collect.md` | Step 0 开始时读取 |
| 读图理解 | `steps/step1-understand.md` | Step 1 开始时读取 |
| 脚本创作 | `steps/step2-script.md` | Step 2 开始时读取 |
| TTS 配音 | `steps/step3-tts.md` | Step 3 开始时读取 |
| 渲染合成 | `steps/step4-render.md` | Step 4 开始时读取 |
| TTS 脚本 | `scripts/tts_generate.py` | Step 3 配音时执行 |
| 渲染脚本 | `scripts/render_video.py` | Step 4 合成时执行 |
| 中文字体 | `Noto Sans CJK SC` / `WenQuanYi Micro Hei` | 字幕与 HTML 排版时设置 |

## 前置条件

1. Python 3.8+ + Pillow + edge-tts（配音）
2. Playwright + Chromium（HTML 截图）
3. ffmpeg（视频合成）
4. 漫画项目已存在（`output/page1~N.png` + `页面配置.json`）
5. 输出目录可写

## 版本

**当前版本**：v0.2.0 | 2026-08-09

> 完整版本历史见 `CHANGELOG.md`。