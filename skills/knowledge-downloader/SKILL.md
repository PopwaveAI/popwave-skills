---
name: knowledge-downloader
pipeline:
  upstream: []
  downstream: []
display_name: "知识获取器 — 微信文章 + B站视频"
category: content-acquisition
scenario: analyze
mode: batch
recommended: 8
tags: ["微信", "公众号", "B站", "视频字幕", "文章下载", "OCR", "内容拆解", "价值提炼"]
fidelity: production
description: 当用户说"下载这篇微信文章""抓取B站字幕""把这个视频转成文章""保存这篇公众号""批量下载专辑""提取视频文字"时启用。统一的知识内容获取工具，支持微信公众号文章（CDP 操控 Chrome 下载）和 B 站视频（API 获取字幕）。下载后自动进入 Phase B 拆解阶段，按标准模板产出结构化拆解报告。依赖 web-access skill 进行微信下载。
---

# 知识获取器 v1.0.0

> **定位：** 从微信/公众号文章 + B站视频中提取原始内容，然后拆解为结构化报告。
> **核心管线：** 输入 URL → Phase A 下载 → Phase B 拆解报告。

---

## 速查表

| 操作 | 入口 | 产出 | 耗时 |
|:----|:-----|:-----|:-----|
| 单篇微信文章下载 | `py downloader.py <URL>` | `{标题}.md`（含正文+截图+OCR） | ~30s/篇 |
| 专辑/合集下载 | `py downloader.py <URL> --album` | `N×` `{标题}.md` | ~30s×N |
| 批量微信下载 | `py downloader.py --batch urls.txt` | 同上 | 同上 |
| B站单集字幕获取 | `py bili_subtitle.py <BV号/URL>` | `{标题}_字幕原始数据.json` | ~10s/集 |
| B站批量获取 | `py bili_subtitle.py --batch urls.txt` | N×上面 | ~10s×N |
| 生成拆解报告 | AI 读取原文. md + 模板 → `{标题}_拆解报告.md` | `_拆解报告.md` | ~2min/篇 |
| 目录整理 | `py report_agent.py --organize -o <dir>` | `原文/` + `拆解文/` 结构 | ~1s |
| 批量生成报告 | `py report_agent.py --batch <dir> -o <dir>` | 批量拆解报告 | ~2min×N |

---

## 管线总览

```
用户提供 URL
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Phase A: 下载                                   │
│  ├── 微信数据源: downloader.py（需 CDP + Chrome）│
│  │    ├── 单篇下载 → article.md + images/ + OCR │
│  │    ├── 专辑下载 → N 篇                        │
│  │    └── 批量下载 → 从 txt 去重后逐个下载       │
│  └── B站数据源: bili_subtitle.py（API + CDP）    │
│       ├── 单集获取 → 字幕上下文 JSON             │
│       ├── 批量获取 → N 个上下文包                │
│       └── CDP fallback（需登录的 AI 字幕）        │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Phase B: 拆解报告                               │
│  ├── 读取原文 .md（微信）或字幕 JSON（B站）      │
│  ├── 加载 report-prompt.md + report-template.md │
│  ├── AI 执行拆解（report_agent.py 编排上下文）   │
│  └── 产出 {标题}_拆解报告.md                     │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Phase C（可选）: 目录整理                       │
│  ├── py report_agent.py --organize              │
│  └── 产出 原文/ + 拆解文/ 双目录结构             │
└─────────────────────────────────────────────────┘
```

---

## Phase A-1: 微信文章下载 — SOP

> **前置依赖：** 必须运行 CDP Chrome Proxy（localhost:3456），Chrome 已登录微信公众平台。
> **依赖 skill：** web-access（提供 CDP 环境）

### 第一步：确认输入

| 输入格式 | 示例 | 说明 |
|:---------|:-----|:-----|
| 单篇 URL | `https://mp.weixin.qq.com/s/xxxxx` | 1 篇 → 1 个 `.md` |
| 专辑 URL | `https://mp.weixin.qq.com/album/...` | 1 专辑 → N 篇 |
| 批量文件 | `urls.txt`（每行一个 URL） | 自动去重 |

**❌ 门禁：** URL 必须是 `mp.weixin.qq.com` 域名。非微信链接 → 退回，提示用户提供微信文章 URL。

### 第二步：执行下载

```powershell
# 单篇下载（含 OCR）
py downloader.py "https://mp.weixin.qq.com/s/xxxxx" -o ./articles

# 专辑下载
py downloader.py "专辑URL" --album -o ./articles

# 批量下载
py downloader.py --batch urls.txt -o ./articles

# 跳过 OCR（节省时间）
py downloader.py "URL" --no-ocr -o ./articles

# 指定 Kimi API Key（OCR 用）
py downloader.py "URL" --kimi-key "sk-xxx" -o ./articles
```

### 第三步：验收产出

产出目录结构：

```
./articles/
├── {标题}.md              ← 原文（含正文）
├── images/                 ← 文章截图（可选）
│   ├── {标题}_01.jpg
│   └── {标题}_02.png
└── 拆解文/（Phase B 后产生）
```

**❌ 门禁：** 检查 `.md` 是否有正文内容（`# 正文` 部分非空）。正文为空 → 重试或标记失败。

---

## Phase A-2: B站字幕获取 — SOP

> **前置依赖：** 无（直连 API），AI 字幕需要 CDP Chrome Proxy（需 B站登录）。

### 第一步：确认输入

| 输入格式 | 示例 |
|:---------|:-----|
| BV 号 | `BV1GJ411x7sF` |
| 完整 URL | `https://www.bilibili.com/video/BV1GJ411x7sF` |
| 短链接 | `https://b23.tv/xxxxx` |

**❌ 门禁：** 无法提取 BV 号 → 退回，要求提供标准 B站视频链接。

### 第二步：执行获取

```powershell
# 单集获取
py bili_subtitle.py "https://www.bilibili.com/video/BV1GJ411x7sF" -o ./articles

# 批量获取
py bili_subtitle.py --batch urls.txt -o ./articles

# 仅输出 JSON（不做清洗）
py bili_subtitle.py "BV1GJ411x7sF" --json-only

# 禁用 CDP fallback
py bili_subtitle.py "URL" --no-cdp
```

### 第三步：验收产出

```
./articles/原文/
├── {标题}_字幕原始数据.json    ← AI 清洗输入
```

**❌ 门禁：** 检查 `subtitle_body` 是否非空。空数组 → 标记为"无字幕视频"。

### 第四步（可选）：AI 清洗字幕为文章

读取 `_字幕原始数据.json`，按 `subtitle-clean-prompt.md` 清洗规则：

1. 去掉时间戳
2. 合并碎片句子
3. 去除废话互动语（保留 UP 主语气）
4. 按语义智能分段
5. 保留口语化风格

产出 `{标题}.md`（标准 frontmatter + 正文）。

---

## Phase B: 拆解报告生成 — SOP

### 第一步：准备上下文

```powershell
# 单篇生成上下文（输出到 stdout）
py report_agent.py "原文/{标题}.md" -o "拆解文/"
```

脚本自动加载：
- `report-prompt.md`（撰写提示词）
- `report-template.md`（报告模板）

### 第二步：AI 执行拆解

按 `report-prompt.md` 规范撰写拆解报告，核心原则：
1. **不摘抄原文** — 提炼观点，不是复制粘贴
2. **pop 视角** — 对标写作管线，给出行动项
3. **长短适度** — 短文 3-5 段，长文 6-8 段
4. **模板不死板** — 根据文章类型灵活调整

**❌ 门禁：** 报告必须有 `一句话定性` + 至少 3 个核心部分。缺结构 → 退回重写。

### 第三步：保存报告

→ 保存为 `{标题}_拆解报告.md`

```markdown
---
title: "[标题] 拆解报告"
source: "原文标题"
author: "公众号名"
source_url: "原文链接"
created: "YYYY-MM-DD"
type: "文章拆解"
tags: []
---

# [标题] 拆解报告
> 一句话定性
...
```

### 第四步（可选）：目录整理

```powershell
py report_agent.py --organize -o ./articles
```

产出结构：

```
./articles/
├── 原文/
│   ├── {标题}.md
│   └── images/
└── 拆解文/
    └── {标题}_拆解报告.md
```

---

## WRONG 示例

### WRONG 1：直接让用户装 Chrome 插件

> ❌ 用户："帮我下载这篇微信文章"
> Agent 回答："请先安装 Chrome 插件 XXX"
> 正确做法：自动使用 CDP Chrome Proxy，无需用户干预。

### WRONG 2：B站字幕手动复制粘贴

> ❌ Agent 手动打开 B站页面 → 逐行复制字幕
> 正确做法：用 `bili_subtitle.py` API 直链获取，自动化完事。

### WRONG 3：拆解报告写成长篇读书笔记

> ❌ 报告写成"第一章讲了...第二章讲了..."流水账
> 正确做法：按模板结构化输出：核心提炼→方法论→亮点→对比→行动项。

### WRONG 4：微信下载后不检查正文完整性

> ❌ 下载后直接丢给 Phase B，结果正文是空/错误页面
> 正确做法：验收正文非空，确认 `# 正文` 部分存在且有内容。

### WRONG 5：B站字幕获取失败后不尝试 fallback

> ❌ 直连 API 返回空字幕 → 直接放弃
> 正确做法：检查 `need_login` 标记，尝试 CDP fallback。

---

## 异常与边界条件表

| 场景 | 处理 |
|:-----|:-----|
| **微信 URL 不是公众号文章** | 检查域名 `mp.weixin.qq.com`，非此域名→退回 |
| **CDP Chrome 未启动** | 提示启动 web-access skill 提供 CDP 环境 |
| **B站视频无 CC 字幕** | 直连 API 返回空字幕；检查 `need_login` 标记，尝试 CDP fallback |
| **B站视频无口播（纯音乐）** | `subtitle_body` 为空 → 输出"无口播内容，无法提取文字"标记 |
| **下载的正文内容为空/乱码** | 重试下载；检查页面是否需登录/验证 |
| **微信文章含大量图片** | 自动下载并 OCR（需 Kimi API Key），无 key 则跳过 OCR |
| **专辑文章数量超 50 篇** | 自动限速（每篇间隔 2s）避免触发风控 |
| **批量去重：重复 URL** | `--batch` 模式自动去重（保留首次出现） |
| **拆解报告已存在** | `--skip-existing` 跳过已有，不覆盖 |
| **原文文件损坏无法读取 frontmatter** | 自动回退用文件名作为标题 |

---

## 阶段边界越界检测

| 边界场景 | 检测条件 | 处理 |
|:---------|:---------|:-----|
| Phase A 未完进入 Phase B | 原文 `.md` 不存在或 `# 正文` 为空 | ❌ 退回 Phase A |
| B站字幕未清洗就做拆解 | 尝试读取 `_字幕原始数据.json` 而非 `.md` | ❌ 先执行 AI 清洗→生成 `.md` |
| 拆解报告覆盖原文目录 | 报告存在 `原文/` 下 | ❌ 必须写入 `拆解文/` |
| 批量模式混用数据源 | 同一批次同时包含微信+B站 URL | ❌ 分两批执行 |
| OCR 跳过但后续需要图片文字 | `--no-ocr` 后图片无文字提取 | ⚠️ 标记"需人工补 OCR" |

---

## 落盘检查点

| 阶段 | 检查点 | 确认项 |
|:-----|:-------|:-------|
| A-1 微信下载 | `{标题}.md` 文件存在，正文非空 | [ ] |
| A-1 微信下载 | images 目录存在（若有截图） | [ ] |
| A-2 B站获取 | `{标题}_字幕原始数据.json` 存在 | [ ] |
| A-2 B站 AI 清洗 | `{标题}.md` 存在（清洗后） | [ ] |
| B 拆解报告 | `{标题}_拆解报告.md` 存在，结构完整 | [ ] |
| B 拆解报告 | frontmatter 完整（title/source/author/source_url/created/type/tags） | [ ] |
| C 目录整理 | `原文/` 和 `拆解文/` 正确分离 | [ ] |

---

## 文件引用

| 文件 | 路径 | 用途 |
|:-----|:-----|:-----|
| `downloader.py` | `scripts/downloader.py` | 微信文章下载（单篇/专辑/批量） |
| `bili_subtitle.py` | `scripts/bili_subtitle.py` | B站字幕获取（直连+CDP fallback） |
| `report_agent.py` | `scripts/report_agent.py` | 拆解报告编排（单篇/批量/目录整理） |
| `report-prompt.md` | `templates/report-prompt.md` | 拆解报告撰写 System Prompt |
| `report-template.md` | `templates/report-template.md` | 拆解报告 Markdown 模板 |
| `subtitle-clean-prompt.md` | `templates/subtitle-clean-prompt.md` | B站字幕清洗 Prompt |

---

## 版本

v1.0.0 | 2026-06-02 | 当前稳定版本。知识下载器，支持微信公众号和 B 站内容抓取。
