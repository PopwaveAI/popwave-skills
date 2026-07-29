---
name: pop-novel-comic
description: "当用户说'网文转漫画/章节漫画/小说漫画/漫画生成'时启用。读取网文章节原文，Agent拆解分镜脚本，调用 Seedream 生成角色定妆图+逐格分镜画面，HTML 层叠加对白气泡组装成完整漫画页面。"
---

# pop-novel-comic

> 网文章节转漫画生成器。输入一章网文，输出一页多格漫画 HTML 页面。Agent 做编剧（拆分镜），Seedream 做画师（生成画面），HTML 做排版（组装漫画页）。v1.0.0

## 这个 Skill 做什么

输入：网文章节原文（.txt / .md，~3000字）+ 可选角色描述/参考图。
输出：HTML 漫画页面（含 6-8 格分镜画面 + 对白气泡 + 旁白框 + 拟声词）+ 角色定妆图 + 分镜脚本。

核心价值：把一章网文变成一页可分享的漫画。**Agent 负责"想"**（章节解构→分镜脚本），**Seedream 负责"画"**（角色定妆+逐格分镜），**HTML 负责"排"**（对白叠加+页面组装）。三者分工，各司其职。

## 模型说明

| 模型 | 版本 | 用途 | 模型 ID |
|:-----|:-----|:-----|:--------|
| Seedream | 5.0 lite | 角色定妆+分镜生成（速度优先） | `doubao-seedream-5-0-lite-260128` |
| Seedream | 5.0 Pro | 角色定妆+分镜生成（质量优先，可选） | `doubao-seedream-5-0-pro-260628` |

> 复用 `pop-novel-visual` 的 API 脚本和提示词指南。API 信息见 `pop-novel-visual/scripts/generate.py` 和 `pop-novel-visual/references/seedream-prompt-guide.md`。

## 怎么运作

### Step 1: 章节解构 → 分镜脚本 → `steps/step1-deconstruct.md`

- 读取章节原文
- 提取角色清单（名字+视觉特征）
- 拆出 6-8 个关键帧，每帧确定：场景、角色动作、机位（全景/中景/近景/特写）、情绪、对白/旁白/拟声词
- 确定风格锚定串（全章统一的风格描述，每格提示词末尾追加）
- 输出分镜脚本表 + 角色视觉规格表
- **🚪 门禁A：分镜确认** → 向用户呈现分镜脚本，用户确认/调整后继续

### Step 2: 生成画面 + HTML 组装 → `steps/step2-generate.md`

- **角色定妆**：为主角生成 1-2 张角色立绘（纯文生图），作为后续分镜的参考图
- **逐格分镜**：每格传入角色定妆图作为参考（图生图模式），提示词≤300字，追加风格锚定串
- **HTML 组装**：将生成的分镜画面用 CSS Grid 排版，叠加对白气泡/旁白框/拟声词，输出完整漫画 HTML 页面

## 产出文件结构

```
{输出目录}/
├── storyboard.md          # 分镜脚本（Step 1 产出）
├── output/
│   ├── char-{角色名}.png  # 角色定妆图
│   ├── frame1.png         # 分镜画面 1~8
│   ├── frame2.png
│   ├── ...
│   └── frame8.png
└── 漫画-{章节名}.html     # 最终漫画页面
```

## ❌ 铁律

| # | 铁律 | 违反后果 |
|:-:|:-----|:---------|
| ❌1 | **先解构再生成** — 必须先读章节原文、拆出分镜脚本、用户确认后才能生成。禁止跳过解构直接翻译原文为提示词 | 画面各格之间无叙事逻辑，精确地画错了故事 |
| ❌2 | **角色定妆图先行** — 必须先生成角色定妆图作为参考图，再逐格生成分镜。禁止无参考图直接文生图 | 角色跨格外观不一致，8格画的是8个不同的人 |
| ❌3 | **风格锚定串全章统一** — 所有分镜格共用同一条风格描述串，追加在每格提示词末尾。禁止每格换不同风格 | 8格风格割裂，不像同一部漫画 |
| ❌4 | **对白用 HTML 叠加不用 Seedream 渲染** — 对白气泡、旁白框、拟声词用 CSS 定位叠加在画面上。禁止让 Seedream 在画面内渲染文字 | 模型文字渲染不可控，气泡位置挡画面 |
| ❌5 | **下载后格式保真** — Seedream API 返回的 URL 资源实际为 JPEG，脚本保存为 .png 时必须检测 magic bytes 并转码为真 PNG。禁止直接写入 JPEG 字节流到 .png 文件 | popwave webview 按 MIME 校验，假 PNG 被判定为图片损坏 |

## 速查表

| 我要 | 读什么文件 | 什么时候读 |
|:-----|:----------|:----------|
| 执行章节解构+分镜脚本 | `steps/step1-deconstruct.md` | Step 1 开始时读取 |
| 执行生成+HTML组装 | `steps/step2-generate.md` | Step 2 开始时读取 |
| 查 Seedream 提示词写法 | `../pop-novel-visual/references/seedream-prompt-guide.md` | Step 2 写提示词前必读 |
| 调用 Seedream API 生成图片 | `../pop-novel-visual/scripts/generate.py` | Step 2 生成单张图片时执行 |
| 批量生成分镜 | `scripts/generate_storyboard.py` | Step 2 批量生成8帧时执行 |
| HTML 漫画页模板 | `templates/comic-page.tpl.html` | Step 2 组装漫画页时参考 |
| 查分镜脚本写法指南 | `references/storyboard-guide.md` | Step 1 拆分镜时参考 |

## 前置条件

1. Python 3.8+ 环境
2. `ARK_API_KEY` 环境变量（火山引擎方舟 API Key）
3. 网文章节原文文件（.txt / .md）
4. 输出目录可写

## 已验证的参数

| 参数 | 值 | 说明 |
|:-----|:---|:-----|
| 模型 | `doubao-seedream-5-0-lite-260128` | R15 测试验证，速度优先 |
| 尺寸 | `1728x2304`（3:4） | API 最小像素要求 3686400 |
| 格数 | 6-8 格 | 一章 ~3000 字的最佳分镜密度 |
| 角色定妆 | 1-2 张 | 主角必出，重要配角可选 |
| 提示词上限 | 300 字/格 | Seedream 中文提示词上限 |

## 版本

v1.1.0 | 2026-07-29 | 格式保真修复：Seedream API 返回 JPEG 资源但脚本以 .png 命名保存，导致严格 webview 判定为图片损坏。新增 ensure_png_format() 在下载后自动检测 magic bytes 并转码为真 PNG。同步修复 pop-novel-visual/scripts/generate.py。新增铁律5。
