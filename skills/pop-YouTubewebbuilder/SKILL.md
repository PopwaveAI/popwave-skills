---
name: pop-YouTubewebbuilder
description: 当用户说"给我做个个人网站""生成 YouTuber 品牌页""创作者主页""帮我建一个频道页面""个人品牌网站"时启用。创作者个人网站生成器。透过内容读懂创作者 → 人物优先设计 → agent 自主创作个人品牌页。输出 .md + .html 文件。
version: 4.1.0
pipeline:
  upstream: []
  downstream: []
---

# pop-creator-site · 创作者个人网站 v4.1.0

> **定位：** 每一位创作者的个人品牌页面。核心管线：**提供创作者内容入口 → 读懂这个人 → 设计表达这个人 → 生成个人网站**。
>
> ⚠️ v4.1 变更：从"数据驱动设计"转向"人物驱动设计"。YouTube 数据降级为辅助参考。输出文件自动按频道 handle 命名。
>
> ⚠️ **Windows PowerShell 注意：** 所有命令用 `;` 替代 `&&`。GBK 错误时先设 `$env:PYTHONIOENCODING='utf-8'`。

---

## 速查表

| 操作 | 入口 | 产出 | 耗时 |
|:-----|:-----|:-----|:-----|
| 获取频道数据 | `python scripts/run.py --channel-url "https://www.youtube.com/@handle"` | `data.json` + `analysis_ready.json` | ~30s |
| 人物速写+PRD | AI 读取 data.json → 撰写 PRD | `{创作者}_设计PRD.md` | ~5min |
| HTML 创作 | AI 基于 PRD → 创作单文件 HTML | `{handle}_site.html` | ~10min |
| 独立审查 | AI 子 Agent 冷眼审查 | 审查报告 | ~2min |
| 视觉质检（可选） | `python scripts/qa.py` | 质检报告 | ~1min |

**核心铁律：** PRD 未经用户确认 → 不得进入 HTML 创作。审查未通过 → 不得交付。

---

## 管线总览

```
Step 1 ─ 提供创作者内容入口（频道链接/频道 ID）
    ↓
Step 2 ─ 自动获取内容（python scripts/run.py → data.json + analysis_ready.json）
    ↓
Step 3 ─ 人物速写 + 内容分析 → 产出 {创作者}_设计PRD.md
    ↓   ← ❌ 门禁：用户确认 PRD 后才能进入 Step 4
Step 4 ─ Agent 基于 PRD 创作自包含单文件 HTML
    ↓
Step 4.5 ─ 独立审查子 Agent 冷眼审查
    ↓   ← ❌ 门禁：审查未通过不得交付（最多2次重审）
Step 5 ─ 视觉质检（可选，Kimi K2.5）
    ↓
    ✅ 交付 {handle}_site.html
```

---

## Step 1：提供创作者入口 — SOP

### 第一步：确认输入

用户提供 YouTube 频道链接或频道 ID。

| 输入格式 | 示例 |
|:---------|:-----|
| 频道 URL | `https://www.youtube.com/@频道名` |
| 频道 handle | `@频道名` |

**❌ 门禁：** 必须是 YouTube 频道入口。非 YouTube 链接 → 退回要求提供频道 URL。

---

## Step 2：获取数据 — SOP

### 第一步：运行数据采集脚本

```powershell
# PowerShell 用户
cd 项目目录; $env:PYTHONIOENCODING='utf-8'; python scripts/run.py --channel-url "https://www.youtube.com/@handle"
```

**读什么：** 脚本自动从 YouTube API 抓取频道信息 + 前 12 个视频

### 第二步：验收产出

两个文件必须存在：

| 文件 | 内容 | 关键字段 |
|:-----|:-----|:---------|
| `data.json` | 频道信息+视频列表+统计数据 | `channel.title`, `channel.statistics`, `videos[].thumbnails.maxres` |
| `analysis_ready.json` | 频道分析摘要 | `channel_analysis.language`, `video_analysis.titles` |

**❌ 门禁：** `data.json` 缺失或为空 → 退回检查网络/API Key，重试。

---

## Step 3：产出 PRD — SOP

> **核心原则：人物优先设计。** 先读懂这个人，再看数据。页面最终要像这个人，不是像她的数据报表。

### 第一步：人物速写（必先做）

浏览所有视频标题，感受语气，写 100-200 字人物画像。这是北极星。

### 第二步：深度内容分析

**读什么：** `data.json` + `analysis_ready.json`

| 分析维度 | 关注点 |
|:---------|:-------|
| 内容赛道 | 视频主题/系列 |
| 播放量分布 | 哪个系列最受欢迎 |
| 语言 | chinese/english/bilingual |
| 内容系列 | 是否有系列化内容 |

### 第三步：撰写 PRD

**PRD 结构（不可省略）：**

1. **创作者深度理解** — 人物速写叙事（禁止数据罗列）
2. **内容信号→设计策略映射** — 至少 3 个信号，每个用"证据→设计映射→具体措施"格式
3. **视觉语言系统** — 色彩方案（含对比度验证 ≥4.5:1）+ 字体系统 + 整体质感
4. **体验架构** — 体验序列 + 每个 Section 的设计笔记
5. **设计决策依据 & 风险评估** — 设计哲学 + 关键决策溯源 + 风险备选

**产出文件：** `{创作者}_设计PRD.md`

**❌ 门禁（关键！）：PRD 产出后必须给用户确认。用户未确认 → 不得进入 Step 4。** 任何未经确认的 HTML 创作 → 退回。

---

## Step 4：创作 HTML — SOP

> **前提：** Step 3 PRD 已通过用户确认。

### 第一步：学习设计参考

读取 `DESIGN_GUIDE.md`（完整设计参考），确认视觉选型：
- 10 个常规设计方向 + 5 个极端风格
- 严禁连续两次使用同一方向

### 第二步：创作单文件 HTML

**铁律：**

| # | 规则 | 具体要求 |
|:-:|:-----|:---------|
| 1 | **零 Emoji** | HTML 可见内容禁止 Emoji Unicode。用 ISO 代码（JP/SG/ID）、纯文字、SVG 替代 |
| 2 | **人物驱动** | 从"读懂这个人"出发，不套模板 |
| 3 | **自包含单文件** | CSS/JS 全内联，零外部依赖，双击可打开 |
| 4 | **响应式** | mobile-first，三档：≥1024px / 768-1023px / <768px |
| 5 | **数据驱动 HTML** | 视频 ID/标题/播放量/时长等所有数据从 `data.json` 动态生成。禁止手动抄写 |
| 6 | **禁止内容** | Services/Testimonials/Blog/Case Studies/Team → 一律禁止 |
| 7 | **视觉缺口处理** | 缺头像/banner → 先用缩略图 → GenerateImage → CSS 质感，禁止 emoji/占位符 |

**Section 规范：**

| Section | 最低要求 |
|:--------|:---------|
| Hero | 至少 4-5 层视觉层次 |
| Stats | 必须有数字动画（requestAnimationFrame） |
| About | 至少 3 段正文 |
| Videos | 至少 6 个，缩略图用 `maxresdefault` |
| Footer | 版权+社交 SVG 图标+订阅 CTA |

---

## Step 4.5：独立审查 — SOP

### 第一步：启动子 Agent 冷眼审查

子 Agent 不参与写作，只负责挑刺。

### 第二步：质量门禁清单

| 检查项 | 标准 | 结果 |
|:-------|:-----|:-----|
| 零 Emoji | 遍历可见文本节点，无 Emoji Unicode | [ ] |
| 页面充实度 | ≥5 section + About ≥3 段 + Hero ≥4 层 | [ ] |
| 视觉方向一致性 | 与 PRD 一致 | [ ] |
| 工匠精神 | 数字动画 + 入场动画 + hover 反馈 | [ ] |
| 响应式 | 三档测试通过 | [ ] |
| 技术纯净 | 内联 CSS/JS、零依赖、maxresdefault | [ ] |

**❌ 门禁：** 审查未通过 → 最多 2 次重审。审查报告必须公开追加到回复中。

---

## Step 5：视觉质检（可选） — SOP

```powershell
python scripts/qa.py
```

使用 Kimi K2.5 进行视觉质量评估。

---

## WRONG 示例

### WRONG 1：不写 PRD 直接出 HTML

> ❌ 用户："给这个频道做个网站"
> Agent 直接写 HTML，跳过 PRD 确认环节
> ✅ 先产 PRD，给用户确认，确认后再创作 HTML

### WRONG 2：HTML 里硬编码频道数据

> ❌ HTML 里写死视频标题、播放量
> ✅ 从 `data.json` 动态读取并生成 HTML 卡片

### WRONG 3：用 Emoji 当装饰元素

> ❌ Section 标题用 "🔥 Popular Videos"
> ✅ 改为 "Popular Videos" 或 SVG 图标

### WRONG 4：使用占位符图片

> ❌ 头像缺失时用 `placeholder.com` 或灰色方块
> ✅ 优先用缩略图 → GenerateImage 生成 → CSS 质感设计

### WRONG 5：连续两次用相同视觉方向

> ❌ 上一个频道用了"极简科技风"，这个也用同一风格
> ✅ 每个创作者选独特的视觉语言，禁止连续重复

### WRONG 6：审查不通过仍交付

> ❌ 审查报告指出 Emoji 问题，不修复直接交付
> ✅ 修复全部问题后再交付，最多 2 次重审

---

## 异常与边界条件表

| 场景 | 处理 |
|:-----|:-----|
| **YouTube API Key 缺失** | `data.json` 抓取失败，检查 `config.json` 中的 API Key |
| **频道没有公开视频** | 脚本返回空视频列表 → PRD 标注"无视频数据"，手动补充创作者信息 |
| **频道语言非中/英文** | `analysis_ready.json` 标注语言，设计时适配对应文字风格 |
| **创作者的 Banner 图缺失** | 视觉缺口处理：优先用频道高清晰度头像 → GenerateImage → CSS 质感设计 |
| **缩略图非 maxres 格式** | 降级链：maxres → high → medium → default |
| **用户提供非 YouTube 入口** | ❌ 退回，要求提供 YouTube 频道链接 |
| **GBK 编码错误（中文 Windows）** | 命令前加 `$env:PYTHONIOENCODING='utf-8';` |
| **脚本运行超时** | 检查网络连接，重试；API 限制时等待后重试 |
| **PRD 被用户拒绝** | 根据反馈修改 PRD，重新提交确认 |
| **HTML 审查 2 次仍未通过** | 输出最终审查报告，标记"需人工干预"，附上具体问题清单 |

---

## 阶段边界越界检测

| 边界场景 | 检测条件 | 处理 |
|:---------|:---------|:-----|
| Step 2 未完成进入 Step 3 | `data.json` 不存在或为空 | ❌ 退回 Step 2 |
| Step 3 PRD 未确认进入 Step 4 | 检查用户是否回复"确认"/"可以" | ❌ 退回要求用户确认 |
| Step 4 数据未动态生成 | HTML 中出现硬编码视频数据 | ❌ 退回重写为动态加载 |
| Step 4.5 未执行直接交付 | 审查报告不存在 | ❌ 退回 Step 4.5 |
| 审查报告有未修复问题 | critical_bug 列表非空 | ❌ 退回 Step 4.5 重审 |
| 视觉方向重复 | 检查上次使用的方向 | ⚠️ 更换方向后再创作 |

---

## 落盘检查点

| 检查点 | 确认项 | 确认 |
|:-------|:-------|:-----|
| Step 2 data.json | 文件存在且含完整频道+视频数据 | [ ] |
| Step 2 analysis_ready.json | 文件存在且含频道分析摘要 | [ ] |
| Step 3 PRD | `{创作者}_设计PRD.md` 存在，5部分完整 | [ ] |
| Step 3 PRD 确认 | 用户已回复确认 | [ ] |
| Step 4 HTML | 自包含单文件，CSS/JS 内联 | [ ] |
| Step 4 零 Emoji | 遍历可见文本无 Emoji | [ ] |
| Step 4.5 审查报告 | 审查报告生成，无 critical_bug | [ ] |
| Step 4.5 质量门禁 | 6项门禁全部通过 | [ ] |

---

## 设计原则（速览）

完整解说见 `DESIGN_GUIDE.md`。

| # | 原则 | 一句话 |
|:-:|:-----|:------|
| 一 | 人物优先 | 先读懂这个人，再看数据 |
| 二 | 人格驱动 | 识别 personality signature，用视觉语言放大 |
| 三 | 视觉表现力 | Hero→Stats→About→Videos→Footer 固定层级 |
| 四 | 色彩即情绪 | 对比度 ≥ 4.5:1 |
| 五 | 艺术多样性 | 每个创作者一种独特视觉语言，严禁连续两次同方向 |
| 六 | 响应式 | mobile-first，三档 |
| 七 | 技术纯洁性 | 自包含单文件 HTML，零外部依赖，零 Emoji |
| 八 | 视觉缺口 | 缺图走决策树，禁止 emoji/占位符 |
| 九 | 工匠精神 | 每个像素都可以更好 |

---

## 版本

v4.1.0 | 从「数据驱动设计」转向「人物驱动设计」。YouTube 数据降级为辅助参考。新增铁律 #6（数据驱动 HTML）。所有脚本已移除 emoji。
