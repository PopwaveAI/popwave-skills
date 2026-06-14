---
name: tool-youtube-webbuilder
description: 当用户说"给我做个个人网站""生成 YouTuber 品牌页""创作者主页""帮我建一个频道页面""个人品牌网站"时启用。创作者个人网站生成器。透过内容读懂创作者 → 人物优先设计 → agent 自主创作个人品牌页。输出 .md + .html 文件。
version: 4.2.0
pipeline:
  upstream: []
  downstream: []
---

# pop-creator-site · 创作者个人网站 v4.2.0

> **定位：** 创作者个人品牌页。核心管线：**提供内容入口 → 读懂这个人 → 设计表达这个人 → 生成网站**。YouTube 数据为辅助，文件按 handle 命名。Windows：用 `;` 替代 `&&`，GBK 错误设 `$env:PYTHONIOENCODING='utf-8'`。

---

## 速查表

| 操作 | 入口 | 产出 | 耗时 |
|:-----|:-----|:-----|:-----|
| 获取频道数据 | `python scripts/run.py --channel-url` | `data.json` + `analysis_ready.json` | ~30s |
| 人物速写+PRD | AI 读取 data.json → 撰写 PRD | `{创作者}_设计PRD.md` | ~5min |
| HTML 创作 | AI 基于 PRD → 创作单文件 HTML | `{handle}_site.html` | ~10min |
| 独立审查 | AI 子 Agent 冷眼审查 | 审查报告 | ~2min |
| 视觉质检（可选） | `python scripts/qa.py` | 质检报告 | ~1min |

**核心铁律：** PRD 未经用户确认 → 不得进入 HTML 创作。审查未通过 → 不得交付。

---

## 管线总览

```
Step 1 ─ 提供创作者内容入口 → Step 2 ─ 自动获取内容（python scripts/run.py）
    → Step 3 ─ 人物速写 + 内容分析 → 产出 {创作者}_设计PRD.md
    ← ❌ 门禁：用户确认 PRD 后才能进入 Step 4
Step 4 ─ Agent 基于 PRD 创作自包含单文件 HTML
    → Step 4.5 ─ 独立审查子 Agent 冷眼审查
    ← ❌ 门禁：审查未通过不得交付（最多2次重审）
Step 5 ─ 视觉质检（可选，Kimi K2.5）→ ✅ 交付 {handle}_site.html
```

---

## 核心流程

详细 SOP 见对应步骤文件。配套参考：`DESIGN_GUIDE.md`（设计方向/PRD 模板）、`references/style-refs/`（视觉参考模板）

| Step | 文件 |
|:-----|:-----|
| 1 | `steps/step-1-channel-entry.md` |
| 2 | `steps/step-2-data-fetch.md` |
| 3 | `steps/step-3-prd.md` |
| 4 | `steps/step-4-html-creation.md` |
| 4.5 | `steps/step-4-5-independent-review.md` |
| 5 | `steps/step-5-visual-qa.md` |

---

## 红线

| # | 红线 |
|:-:|:-----|
| 1 | PRD 未经用户确认 → 不得进入 HTML 创作 |
| 2 | 审查未通过 → 不得交付（最多 2 次重审） |
| 3 | HTML 可见内容零 Emoji。用 ISO 代码、纯文字、SVG 替代 |
| 4 | 所有视频数据从 `data.json` 动态生成。禁止硬编码 |
| 5 | 自包含单文件 HTML，CSS/JS 全内联，零外部依赖 |
| 6 | 禁止连续两次使用相同视觉方向 |
| 7 | 禁止占位符图片。缺图走决策树：缩略图 → GenerateImage → CSS 质感 |

---

## Drop Check

交付前必须确认：

```
[ ] PRD 已获用户明确确认
[ ] 审查报告通过（6项质量门禁全部通过）
[ ] HTML 零 Emoji（遍历可见文本节点）
[ ] 视频数据动态生成，无硬编码
[ ] 页面自包含单文件，CSS/JS 全内联
[ ] 无 Services/Testimonials/Blog/Case Studies/Team section
```

任一项未通过 → 不可交付。

## WRONG 示例

| # | 违规 | 正确做法 |
|:-:|:-----|:---------|
| 1 | 不写 PRD 直接出 HTML | 先产 PRD → 用户确认 → 再创作 HTML |
| 2 | HTML 硬编码频道数据 | 从 `data.json` 动态读取并生成 HTML 卡片 |
| 3 | 用 Emoji 当装饰元素 | 改为纯文字或 SVG 图标 |
| 4 | 使用占位符图片 | 缩略图 → GenerateImage → CSS 质感设计 |

## 异常与边界条件表

| 场景 | 处理 |
|:-----|:-----|
| **YouTube API Key 缺失** | 检查 `config.json` 中的 API Key |
| **频道没有公开视频** | PRD 标注"无视频数据"，手动补充创作者信息 |
| **频道语言非中/英文** | `analysis_ready.json` 标注语言，设计时适配 |
| **Banner 图缺失** | 频道头像 → GenerateImage → CSS 质感设计 |
| **缩略图非 maxres 格式** | 降级链：maxres → high → medium → default |
| **GBK 编码错误** | 命令前加 `$env:PYTHONIOENCODING='utf-8';` |
| **PRD 被用户拒绝** | 根据反馈修改 PRD，重新提交确认 |

## 阶段边界越界检测

| 边界场景 | 检测条件 | 处理 |
|:---------|:---------|:-----|
| Step 2 未完成进入 Step 3 | `data.json` 不存在或为空 | ❌ 退回 Step 2 |
| PRD 未确认进入 Step 4 | 用户未回复"确认" | ❌ 退回要求用户确认 |
| HTML 数据未动态生成 | HTML 中出现硬编码视频数据 | ❌ 退回重写 |
| Step 4.5 未执行直接交付 | 审查报告不存在 | ❌ 退回 Step 4.5 |

## 落盘检查点

| 检查点 | 确认项 | 确认 |
|:-------|:-------|:-----|
| Step 2 | `data.json` + `analysis_ready.json` 存在且完整 | [ ] |
| Step 3 | PRD 存在，5部分完整 | [ ] |
| Step 3 确认 | 用户已回复确认 | [ ] |
| Step 4 | HTML 自包含单文件，CSS/JS 内联 | [ ] |
| Step 4 零 Emoji | 遍历可见文本无 Emoji | [ ] |
| Step 4.5 | 审查报告生成，无 critical_bug | [ ] |
| Step 4.5 门禁 | 6项门禁全部通过 | [ ] |

## 设计原则（速览）

完整解说见 `DESIGN_GUIDE.md`。

| # | 原则 |
|:-:|:-----|
| 一 | 人物优先：先读懂这个人，再看数据 |
| 二 | 人格驱动：识别 personality signature，用视觉语言放大 |
| 三 | 艺术多样性：每个创作者独特视觉语言，严禁连续两次同方向 |
| 四 | 色彩即情绪：对比度 ≥ 4.5:1 |
| 五 | 技术纯洁性：自包含单文件 HTML，零外部依赖，零 Emoji |
| 六 | 响应式：mobile-first，三档 |
| 七 | 工匠精神：每个像素都可以更好 |

## 版本

v4.2.0 | 2026-06-14 | Tier C v5 结构重构：qa-output/style-refs → references/，6步骤 SOP 提取到 steps/，SKILL.md 瘦身至 ≤150 行，新增红线表+Drop Check。
