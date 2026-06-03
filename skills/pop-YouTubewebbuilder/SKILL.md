---
name: pop-YouTubewebbuilder
description: 创作者个人网站生成器。透过内容读懂创作者 → 人物优先设计 → agent 自主创作个人品牌页。输出 .md + .html 文件。
version: 4.1.0
---

> **⚠️ Windows PowerShell 警告：所有 `&&` 必须替换为 `;`**
>
> 本 skill 运行在 **Windows PowerShell** 环境中。PowerShell **不支持** `&&` 命令链。
> 执行任何命令时，必须将 `&&` 替换为 `;`。
>
> | ❌ 错误写法（bash 语法） | ✅ 正确写法（PowerShell） |
> |:------------------------|:--------------------------|
> | `cd xxx && python run.py` | `cd xxx; python run.py` |
> | `command1 && command2` | `command1; command2` |
>
> 如果出现 GBK 编码错误，在所有命令前加 `$env:PYTHONIOENCODING='utf-8'`。

# pop-creator-site · 创作者个人网站

> **定位：每一位创作者的个人品牌页面。**
>
> 核心管线：**提供创作者内容入口 → 读懂这个人 → 设计表达这个人 → 生成个人网站**。
>
> ⚠️ v4.1 变更：从「数据驱动设计」转向「人物驱动设计」。YouTube 数据降级为辅助参考。新增铁律 #6（数据驱动 HTML）。所有脚本已移除 emoji 以兼容 Windows GBK 终端。输出文件自动按频道 handle 命名（避免 data.json 被覆盖）。

---

## 管线概览

```
Step 1 ─ 提供创作者内容入口（频道链接 / 频道 ID）
Step 2 ─ 自动获取内容（python scripts/run.py → data.json + analysis_ready.json）
Step 3 ─ 人物速写 + 内容分析 → 产出 {创作者}_设计PRD.md（给用户确认）
Step 4 ─ Agent 基于 PRD 创作自包含单文件 HTML
Step 4.5 ─ 独立审查子 Agent 冷眼审查（零 Emoji + 质量门禁）
Step 5 ─ 视觉质检（可选，Kimi K2.5）
```

**铁律：PRD 未经用户确认，不得进入 HTML 创作。审查未通过不得交付。**

---

## 设计原则（速览）

本文档仅列核心原则标题。**每个原则的完整解说、10 个常规设计方向、5 个极端风格、PRD 模板完整版、创作步骤详述请参考 `DESIGN_GUIDE.md`。**

| # | 原则 | 一句话 |
|:-|:-----|:------|
| 一 | 人物优先 | 先读懂这个人，再看数据。页面最终要像这个人，不是像她的数据报表。 |
| 二 | 人格驱动 | 识别她的 personality signature，用视觉语言放大它。禁止套模板。 |
| 三 | 视觉表现力 = 人格翻译器 | 信息层级是骨架，视觉张力是灵魂。层级固定：Hero→Stats→About→Videos→Footer。 |
| 四 | 色彩即情绪 | 色彩传递创作者的情绪信号，不是配色公式。对比度 ≥ 4.5:1。 |
| 五 | 艺术多样性 | **每个创作者值得一种独特的视觉语言。** 详见 `DESIGN_GUIDE.md` 的 10 个常规方向 + 5 个极端风格。严禁连续两次使用同一方向。 |
| 六 | 响应式 | mobile-first。三档：≥1024px / 768-1023px / <768px。 |
| 七 | 技术纯洁性 | 自包含单文件 HTML，CSS/JS 全内联，零外部依赖，零 Emoji。 |
| 八 | 视觉缺口 | 头像/banner/场景图缺失时，走决策树（优先用缩略图 → GenerateImage → CSS 质感设计），禁止 emoji/占位符。 |
| 九 | 工匠精神 | 每个像素都可以更好。见 `DESIGN_GUIDE.md` 的充实度参考表。 |

---

## 网站设计 PRD 模板（结构概要）

文件命名：`{创作者}_设计PRD.md`

完整版含示例见 `DESIGN_GUIDE.md`。这里的提纲不可省略：

1. **创作者深度理解** — 人物速写叙事（禁止数据罗列）
2. **内容信号 → 设计策略映射** — 至少 3 个信号，每个用「证据→设计映射→具体措施」格式
3. **视觉语言系统** — 色彩方案（含对比度验证）+ 字体系统 + 整体质感
4. **体验架构** — 体验序列 + 每个 Section 的设计笔记
5. **设计决策依据 & 风险评估** — 设计哲学 + 关键决策溯源 + 风险备选

---

## 创作步骤

### 第 1 步：人物速写 + 内容分析
- **1a. 人物速写（必先做）**：浏览所有视频标题，感受语气，写 100-200 字人物画像。这是北极星。
- **1b. 深度内容分析**：读取 `data.json` + `analysis_ready.json`，分析内容赛道/播放量分布/语言/内容系列等。

### 第 2 步：产出 PRD
按 PRD 模板撰写 → **给用户确认** → 确认后方可进入 Step 4。

### 第 4 步：创作 HTML
基于已确认的 PRD 创作。核心规范：
- Hero 至少 4-5 层视觉层次
- Stats 必须有数字动画（requestAnimationFrame）
- About 至少 3 段正文
- Videos 至少 6 个，缩略图用 `maxresdefault`
- Footer 含版权 + 社交 SVG 图标 + 订阅 CTA
- ❌ 禁止 Services/Testimonials/Blog/Case Studies/Team
- ❌ 禁止占位图、中英混用（除非频道双语）

### 第 4.5 步：独立审查
启动子 Agent 冷眼审查，对照质量门禁清单：
- 零 Emoji（遍历可见文本节点）
- 页面充实度 ≥ 5 section + About ≥ 3 段 + Hero ≥ 4 层
- 视觉方向与 PRD 一致
- 工匠精神（数字动画 + 入场动画 + hover 反馈）
- 响应式（3 档）
- 技术检查（内联 CSS/JS、零依赖、maxresdefault）

审查报告必须公开追加到回复中。最多 2 次重审。

---

## 快速开始

```bash
python scripts/run.py --channel-url "https://www.youtube.com/@频道名"
```

> **Windows PowerShell 用户注意：** 使用 `;` 代替 `&&` 分隔命令。
> ```powershell
> cd 项目目录; python scripts/run.py --channel-url "https://www.youtube.com/@handle"
> ```
>
> 如果遇到 GBK 编码错误，先设置 UTF-8：
> ```powershell
> $env:PYTHONIOENCODING='utf-8'; python scripts/run.py --channel-url "..."
> ```

然后三步走：
1. 读懂这个人，产出 PRD（`{创作者}_设计PRD.md`）
2. 给用户确认
3. 创作 HTML

---

## 数据字段参考

### data.json 结构

```
{
  "channel": {                          // 频道信息
    "title", "description", "customUrl", "publishedAt", "country",
    "thumbnails": { "default","medium","high": { url,width,height } },
    "bannerUrl",                        // 频道 Banner，可用作 Hero 背景
    "statistics": {                     // viewCount, subscriberCount, videoCount（格式化+raw*）
      "viewCount":"14.3亿","subscriberCount":"142.0万","videoCount":"1,931",
      "rawViewCount":1429890063,"rawSubscriberCount":1420000,"rawVideoCount":1931
    },
    "socialLinks": [{ "platform","url","label" }]
  },
  "videos": [                           // 最多 12 个
    { "id","title","description", "publishedAt",
      "thumbnails": { "default","medium","high","standard","maxres": { url,width,height } },
      "duration":"15:30",
      "statistics": { "viewCount":"53.4万","likeCount":"2.8万","commentCount":"270" },
      "timeAgo":"2天前",
      "url":"https://www.youtube.com/watch?v=..."
    }
  ],
  "fetchedAt": "ISO 时间戳",
  "totalVideos": 12
}
```

### analysis_ready.json 结构

```
{
  "channel_analysis": {
    "name", "language": "chinese|english|bilingual",
    "tags": ["manifestation","education",...],
    "subscriber_count","video_count","view_count"（原始 int）,
    "channel_description"（前 500 字）
  },
  "video_analysis": {
    "total_videos","titles":[...],"descriptions":[...]
  }
}
```

### 缩略图选择策略

- **频道头像**：`thumbnails.high` > `medium` > `default`
- **视频缩略图**：`thumbnails.maxres` > `high` > `medium` > `default`
- **Hero 背景**：`bannerUrl`（否则用频道 `high` 头像）

---

## 目录结构

```
pop-creator-site/
├── SKILL.md              ← 本文档（核心）
├── DESIGN_GUIDE.md       ← 完整设计参考（设计方向/PRD模板/步骤详述）
├── DATA_CONTRACT.md      ← 数据字段参考
├── config.json           ← API Key 配置
├── style-refs/           ← 视觉风格参考模板（双击即开）
├── scripts/
│   ├── run.py            ← 一键抓取 + 分析入口
│   ├── fetch_youtube.py  ← YouTube API 数据抓取
│   ├── analyze.py        ← 数据分析格式化
│   ├── qa.py             ← 视觉质检
│   ├── inject.py         ← (已废弃 v3)
│   └── build_page.py     ← (已废弃 v3)
└── templates/            ← (已废弃) 旧模板
```

---

## 铁律

1. **零 Emoji 政策** — HTML 可见内容中禁止出现任何 Emoji Unicode 字符。用 ISO 代码（JP/SG/ID）、纯文字、内联 SVG 替代。
2. **人物驱动设计，不套模板** — 每个页面从「读懂这个人」出发。
3. **先出 PRD，再出 HTML** — PRD 未经用户确认不得进入 HTML 创作。
4. **每次创作独立选型** — 禁止连续两次使用相同的视觉方向。
5. **单文件 HTML** — 零外部依赖，双击即可打开。
6. **数据驱动 HTML** — 视频 ID、标题、播放量、时长等所有数据必须从 `data.json` 中读取并动态生成 HTML 卡片。禁止手动抄写任何数据（包括视频 ID、播放量、标题），禁止在 HTML 中硬编码频道数据。
