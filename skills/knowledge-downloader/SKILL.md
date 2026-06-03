---
name: knowledge-downloader
display_name: "知识获取器 — 微信文章 + B站视频"
category: content-acquisition
scenario: analyze
mode: batch
recommended: 8
tags: ["微信", "公众号", "B站", "视频字幕", "文章下载", "OCR", "内容拆解", "价值提炼"]
fidelity: production
description: 统一的知识内容获取工具。支持两大数据源：微信公众号文章（CDP 操控 Chrome 下载）和 B 站视频（API 获取字幕）。下载后自动进入 Phase B 拆解阶段，按标准模板产出结构化拆解报告。依赖 web-access skill 进行微信下载。
version: 1.0.0
novel_agent_version: v3.3

orchestration:
  preflight:
    - check Chrome remote-debugging enabled (微信数据源)
    - check web-access skill available (微信数据源)
    - check Kimi API key configured (可选)
  dependencies:
    - web-access (微信数据源)
  subagent_required: false

produces:
  - 微信公众号文章原文 Markdown（微信数据源）
  - B站视频字幕清洗文章 Markdown（B站数据源）
  - 文章配图 / 视频封面（可选）
  - 结构化拆解报告（通用 Phase B）
  - 拆解报告模板（templates/report-template.md）
  - 标准化撰写 Prompt（templates/report-prompt.md）
  - B站字幕清洗 Prompt（templates/subtitle-clean-prompt.md）
---

<POP-CALL>
每次收到用户需求，**必须在开头声明 pop 介入**：
```
🖋️ **pop 收到老板指示**

任务理解：[一句话复述用户需求]
执行路线：knowledge-downloader v1.0.0 | 双数据源（微信/B站）→ 统一拆解管线
```
</POP-CALL>

# 🧠 知识获取器 v1.0

统一获取微信公众号文章和 B 站视频内容，自动产出结构化拆解报告。
**不摘抄原文，每篇都提炼价值。**

---

## 🎯 能做什么

| 能力 | 数据源 | 说明 |
|------|--------|------|
| **📄 微信单篇 + 拆解** | 微信 | 输入文章链接 → 原文 MD + 拆解报告 |
| **📚 微信专辑 + 拆解** | 微信 | 专辑链接 → 全部文章一次搞定 |
| **📋 微信 URL 批处理** | 微信 | 从文本文件读取 URL，自动去重 |
| **🎬 B站单集 + 清洗** | B站 | 输入视频链接/BV号 → 字幕提取 + 清洗为文章 |
| **📋 B站批量获取** | B站 | 文本文件读取多个视频链接 |
| **🖼️ 配图下载** | 微信 | 微信懒加载图片自动抓取 |
| **🔍 截图变文字** | 微信 | Kimi OCR 把截图内容读出来 |
| **🤖 通用 Phase B** | 通用 | 下载后按模板自动产出拆解报告（微信/B站统一） |
| **📂 自动目录整理** | 通用 | `--organize` 一键整理为 `原文/` 和 `拆解文/` |

---

## 🔄 双数据源 + 统一拆解管线

```
用户输入
   ├── 微信链接 ─────────────────────┐
   │                                 ▼
   │              Phase A（微信数据源）        Phase B（通用）
   │         CDP + Chrome 操控         │
   │         提取 DOM → 正文 + 配图      │
   │                                  │
   ├── B站链接 ─────────────────────┐  ├── report_agent.py 加载原文
   │                                 ▼  ├── report-template.md 定结构
   │              Phase A（B站数据源）      ├── report-prompt.md 定视角
   │         HTTP API → 字幕 JSON      │  └── AI 撰写拆解报告
   │         组装上下文包 → AI 清洗为文章   │
   │                                  ▼
   └── 输出目录/
       ├── 原文/xxx.md               ← 📄 清洗/下载后的原文
       └── 拆解文/xxx_拆解报告.md     ← 🧠 结构化拆解报告
```

### 核心理念

| 原则 | 说明 |
|------|------|
| **脚本只做数据获取** | 脚本承担 API 调用、DOM 提取、数据组装，不做语义理解 |
| **语义工作全交 AI** | 清洗字幕、写拆解报告、价值提炼——全部由 AI 完成 |
| **Phase B 完全通用** | 无论数据源是微信还是 B 站，拆解报告走同一套模板和 Prompt |
| **输出格式兼容** | 两路 Phase A 都产出标准 frontmatter + Markdown 正文 |

---

## 📂 目录结构

```
_knowledge-downloader/
├── SKILL.md                          ← 本技能文件
├── templates/
│   ├── report-template.md            ← 拆解报告结构模板（通用）
│   ├── report-prompt.md              ← 拆解报告撰写 Prompt（通用）
│   └── subtitle-clean-prompt.md      ← B站字幕清洗 Prompt（B站专用）
└── scripts/
    ├── downloader.py                 ← Phase A: 微信下载（CDP + Chrome）
    ├── bili_subtitle.py              ← Phase A: B站字幕获取（HTTP API）
    │                                    脚本只做 API 调用，清洗走大模型
    └── report_agent.py               ← Phase B: 拆解报告生成（通用）
                                          支持单篇/批量/断点续跑/目录整理
```

---

## 📥 使用方式

### 微信数据源

```bash
cd E:\AI小说\_知识获取技能\scripts

# 单篇下载 + 自动拆解
py downloader.py "https://mp.weixin.qq.com/s/xxxxx" -o "输出目录" --no-ocr

# 专辑批量下载
py downloader.py "专辑链接" -o "输出目录" --album --no-ocr

# URL 批处理（自动去重）
py downloader.py --batch urls.txt -o "输出目录" --no-ocr
```

### B站数据源

```bash
# 单集获取（自动判断：直连→CDP fallback）
py bili_subtitle.py "https://www.bilibili.com/video/BVxxxxxx" -o "输出目录"

# 也支持纯 BV 号
py bili_subtitle.py "BV1GX4y1N7Vn" -o "输出目录"

# 只输出 JSON 到 stdout（配合管道使用）
py bili_subtitle.py "BVxxxxxx" --json-only

# 禁用 CDP fallback（仅直连）
py bili_subtitle.py "BVxxxxxx" --no-cdp

# 批量模式
py bili_subtitle.py --batch video_urls.txt -o "输出目录"
```

> **字幕获取路径：**
> 1. 尝试直连 API（部分视频有 CC 字幕，不需要登录）
> 2. 如果直连返回空且 `need_login_subtitle=true` → CDP fallback
> 3. CDP 通过已登录 Chrome 获取字幕 URL → Python 直连字幕正文（auth_key 鉴权）

### 通用 Phase B：拆解报告

```bash
# 批量生成拆解报告（微信/B站原文通用）
py report_agent.py --batch "输出目录/原文/" -o "输出目录/拆解文/" --skip-existing

# 单篇生成
py report_agent.py "输出目录/原文/标题.md" -o "输出目录/拆解文/"

# 目录整理
py report_agent.py --organize -o "输出目录"
```

---

## 🧠 Phase B 通用拆解报告模板

无论数据源是微信还是 B 站，拆解报告都走同一套标准：

```
一句话定性 → 核心内容提炼 → 关键观点/方法论表
→ 亮点深度分析 → 与 pop 的关联/对比 → 可复用思路
→ 总体评价 + 优先级
```

详见 `templates/report-template.md` 和 `templates/report-prompt.md`。

---

## ⚙️ 前置准备

### 微信数据源

1. Chrome 以调试模式启动（`--remote-debugging-port=9222`）
2. 启动 CDP Proxy：`node "E:\AI小说\_工具配置\web-access\scripts\check-deps.mjs"`
3. 安装依赖：`py -m pip install requests`

### B站数据源

无需额外准备。纯 HTTP API，不需要浏览器或 CDP。

---

## ❓ 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| CDP Proxy 连不上 | 服务未启动 | 运行 `check-deps.mjs` |
| 微信文章标题为空 | JS 选择器不匹配 | 文章结构特殊，需检查 |
| 微信图片 403 | 缺少 Referer | 已内置 |
| **B站视频无字幕** | UP主未开启 AI 字幕或 CC 字幕 | `bili_subtitle.py` 走 CDP fallback 尝试获取 AI 字幕；仍无则输出简介+标签导读 |
| **B站 CDP 拿不到字幕** | Chrome 未登录 B 站 | 在 Chrome 中打开 bilibili.com 登录 |
| **B站 AI 字幕内容不对** | CDP Tab 缓存问题 | 重新运行一次即可（CDP 开新 Tab 可能拿到不同缓存） |
| **B站字幕质量差** | AI 字幕准确率有限 | 交给大模型清洗时自动纠错，段落合并后整体可读 |
| **B站 API 频率限制** | 短时间请求过多 | 批量时已内置 1s 间隔 |
| B站 wbi 签名 | 部分 API 需要 | CDP fallback 跳过签名问题（直接用已登录浏览器请求） |
| 输出目录太乱 | 多篇混在一起 | `--organize` 整理 |
| 拆解报告质量不够 | 对标视角不足 | 重新触发 `report_agent.py` |

---

## 📝 更新日志

### v1.0.0（2026-05-28）

- **统一知识获取器诞生** — 合并微信文章下载 + B站视频字幕获取为同一技能
- **新增 B站数据源** — `scripts/bili_subtitle.py`，支持两级 fallback：直连 API → CDP
- **CDP fallback** — `need_login_subtitle=true` 时自动通过已登录 Chrome 获取 AI 字幕
- **字幕清洗走大模型** — 脚本只做 API 调用和组装，清洗 100% 由 AI 完成
- **新增 `subtitle-clean-prompt.md`** — B站字幕清洗专用 Prompt
- **Phase B 完全通用** — 微信和 B站的原文统一走 `report_agent.py` 拆解管线
- **`--no-cdp` 参数** — 允许显式禁用 CDP fallback
- **迁移自 wechat-article-downloader v2.1.0** — 保留全部微信下载能力

> wechat-article-downloader 目录保留作为向后兼容入口，推荐迁移到 _knowledge-downloader。
