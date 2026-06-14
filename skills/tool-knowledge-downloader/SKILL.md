---
name: tool-knowledge-downloader
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
description: 当用户说"下载这篇微信文章""抓取B站字幕""把这个视频转成文章""保存这篇公众号""批量下载专辑""提取视频文字"时启用。统一的知识内容获取工具，支持微信公众号文章（CDP 操控 Chrome 下载）和 B 站视频（API 获取字幕）。下载后自动进入 Phase B 拆解阶段，按标准模板产出结构化拆解报告。依赖 tool-web-access skill 进行微信下载。
---

# 知识获取器 v1.0.1

> **定位：** 从微信/公众号文章 + B站视频中提取原始内容，然后拆解为结构化报告。
> **核心管线：** 输入 URL → Phase A 下载 → Phase B 拆解报告。

---

## 红线

| # | 禁止行为 |
|:-:|:---------|
| R1 | 微信下载后不检查正文完整性 |
| R2 | B站字幕获取失败后不尝试 CDP fallback |
| R3 | 拆解报告写成流水账（"第一章讲了..."） |
| R4 | 拆解报告摘抄原文而不提炼观点 |
| R5 | Phase A 未完成就进入 Phase B |
| R6 | B站字幕未清洗就做拆解 |

## 掉头检查

| # | 条件 | 动作 |
|:-:|:-----|:-----|
| D1 | 微信 URL 不是 `mp.weixin.qq.com` | 退回，提示用户提供微信文章 URL |
| D2 | 微信下载正文为空 | 重试或标记失败 |
| D3 | B站无法提取 BV 号 | 退回，要求提供标准 B站视频链接 |
| D4 | B站 `subtitle_body` 为空 | 标记"无字幕视频" |
| D5 | 拆解报告缺 `一句话定性` | 退回重写 |
| D6 | 批量模式混用微信+B站 URL | 分两批执行 |

---

## 执行步骤

| 阶段 | 文件 | 职责 | 产出 |
|:-----|:-----|:-----|:-----|
| Phase A-1 | `steps/step-a1-wechat.md` | 微信文章下载 | `{标题}.md` |
| Phase A-2 | `steps/step-a2-bilibili.md` | B站字幕获取 | `{标题}_字幕原始数据.json` |
| Phase B | `steps/step-b-report.md` | 拆解报告生成 | `{标题}_拆解报告.md` |
| Phase C | `steps/step-c-organize.md` | 目录整理（可选） | `原文/` + `拆解文/` 结构 |

---

## 速查表

| 操作 | 入口 | 产出 | 耗时 |
|:----|:-----|:-----|:-----|
| 单篇微信文章下载 | `py scripts/downloader.py <URL>` | `{标题}.md` | ~30s/篇 |
| 专辑/合集下载 | `py scripts/downloader.py <URL> --album` | N x `{标题}.md` | ~30s x N |
| B站单集字幕获取 | `py scripts/bili_subtitle.py <BV号/URL>` | `{标题}_字幕原始数据.json` | ~10s/集 |
| 生成拆解报告 | AI 读取原文 + 模板 | `{标题}_拆解报告.md` | ~2min/篇 |
| 目录整理 | `py scripts/report_agent.py --organize` | `原文/` + `拆解文/` | ~1s |

---

## 管线总览

```
用户提供 URL
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Phase A: 下载                                   │
│  ├── 微信数据源: scripts/downloader.py（CDP）     │
│  └── B站数据源: scripts/bili_subtitle.py（API）   │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Phase B: 拆解报告                               │
│  ├── 读取原文 .md（微信）或字幕 JSON（B站）       │
│  ├── 加载 templates/report-prompt.md              │
│  └── 产出 {标题}_拆解报告.md                      │
└─────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────┐
│  Phase C（可选）: 目录整理                       │
└─────────────────────────────────────────────────┘
```

---

## 文件引用

| 文件 | 路径 | 用途 |
|:-----|:-----|:-----|
| `downloader.py` | `scripts/downloader.py` | 微信文章下载 |
| `bili_subtitle.py` | `scripts/bili_subtitle.py` | B站字幕获取 |
| `report_agent.py` | `scripts/report_agent.py` | 拆解报告编排 |
| `report-prompt.md` | `templates/report-prompt.md` | 拆解报告 System Prompt |
| `report-template.md` | `templates/report-template.md` | 拆解报告 Markdown 模板 |
| `subtitle-clean-prompt.md` | `templates/subtitle-clean-prompt.md` | B站字幕清洗 Prompt |

---

## 异常与边界条件

| 场景 | 处理 |
|:-----|:-----|
| **微信 URL 不是公众号文章** | 检查域名 `mp.weixin.qq.com` |
| **CDP Chrome 未启动** | 提示启动 tool-web-access skill |
| **B站视频无 CC 字幕** | 检查 `need_login` 标记，尝试 CDP fallback |
| **B站视频无口播（纯音乐）** | 输出"无口播内容"标记 |
| **下载的正文内容为空/乱码** | 重试下载 |
| **微信文章含大量图片** | 自动下载并 OCR（需 Kimi API Key） |
| **专辑文章数量超 50 篇** | 每篇间隔 2s 避免风控 |

---

> v1.0.1 | Tier D v5 重构
