---
name: popwave-browser-extension
display_name: "Popwave 知识获取器 — 浏览器插件"
category: product-design
status: draft
tags: ["浏览器插件", "Chrome Extension", "内容采集", "B站字幕", "微信文章", "知识获取"]
created: "2026-05-28"
---

# Popwave 知识获取器 — 浏览器插件设计方案

## 概述

将 `_knowledge-downloader` 的 CLI 能力封装为**浏览器插件**，让用户在浏览网页时一键收集高价值内容，自动走清洗 + 拆解管线。插件是客户端，`knowledge-downloader` 是后端。

## 核心理念

> **浏览器里看到什么有价值的内容，点一下 Popwave 就「收」进来了。**

```
用户浏览网页时（微信/B站/任意页面）
     │ 点击 Popwave 插件图标
     ▼
插件抓取当前页面结构化数据
     │ 发送到本地 HTTP API
     ▼
knowledge-downloader 后端
     │ 内容识别 → 清洗 → 拆解报告
     ▼
原文/ + 拆解文/
```

## 能力矩阵

| 页面类型 | 插件抓取方式 | 后端处理 | 优先级 |
|---------|------------|---------|--------|
| **B 站视频页** | `window.__INITIAL_STATE__.videoSubtitle.list` → subtitle_url | fetch 字幕正文 + AI 清洗 + 拆解报告 | **P0（已验证可通）** |
| **微信公众号文章** | 读取 DOM（`#activity_name`, `#js_content`） | 已有 `downloader.py` 可复用 | P1（等于 CLI 包装） |
| **任意网页** | `document.title` + `meta[description]` + `body.innerText` | 降级处理：纯文本摘要 + 基础拆分 | P2 |

## 技术架构

```
┌─────────────────────────────────────────────────┐
│                 浏览器插件（Chrome Extension）      │
│                                                   │
│  manifest.json  ← 权限声明（activeTab, storage）    │
│  popup.html/js  ← 点击图标后的弹窗界面              │
│  content.js     ← 注入当前页面，提取结构化数据       │
│  background.js  ← 连接本地 API，管理队列             │
└──────────────┬──────────────────────────────────┘
               │ HTTP POST (JSON)
               ▼
┌─────────────────────────────────────────────────┐
│             本地 HTTP 服务（localhost:3457）       │
│                                                   │
│  接收插件提报的页面数据                              │
│  按类型路由到对应处理器：                              │
│    - B站字幕  → bili_subtitle 流程                  │
│    微信文章  → downloader-style 处理               │
│    通用网页  → 降级处理                              │
│  输出到 原文/ + 拆解文/                             │
└─────────────────────────────────────────────────┘
```

## 与现有基础设施的复用关系

| 现有设施 | 插件方案复用方式 |
|---------|---------------|
| `_knowledge-downloader/scripts/report_agent.py` | 无改动，直接调用 |
| `_knowledge-downloader/templates/report-prompt.md` | 无改动 |
| `_knowledge-downloader/templates/report-template.md` | 无改动 |
| `_knowledge-downloader/templates/subtitle-clean-prompt.md` | 无改动 |
| CDP Proxy | **不再需要**（插件天然在已登录浏览器里运行） |
| `downloader.py`（微信 CDP 下载） | 仅处理非手动浏览的场景（专辑批量） |

**核心价值：** Phase B 拆解管线 100% 复用，零改造。插件只承担「把数据捞出来递过去」这一件事。

## 为什么插件比 CDP 好

| 维度 | CDP 方案 | 插件方案 |
|------|---------|---------|
| **登录态** | 依赖专门的 Chrome 实例 | **用户日常用的浏览器，天然已登录** |
| **B站字幕** | 开新 Tab 拿到的可能跟当前看的不同 | **用户正在看什么就拿什么** |
| **微信文章** | 需要 CDP + Chrome 双端口 | **直接在文章页点一下就行** |
| **操作路径** | 复制链接 → 切窗口 → 敲命令 | **点一下图标，不用离开当前页** |
| **用户门槛** | 需要了解 CLI | 零门槛 |
| **扩展性** | 每增加一个数据源都要写 CDP 逻辑 | 插件可适配任意页面（content.js 通用） |

## 实施路径

### Phase 1：B站字幕获取 MVP（~半天）

1. 搭建插件骨架（manifest.json + popup + content.js）
2. content.js 读取 `window.__INITIAL_STATE__` 提取字幕 URL
3. 点击弹窗 → 数据以 JSON 形式保存到 `原文/` 目录
4. 手动触发 report_agent.py 走拆解管线

### Phase 2：本地 HTTP 服务（1-2 天）

1. 新增 `scripts/local_server.py`，启动 `localhost:3457`
2. 插件端 POST 数据到本地服务
3. 服务端自动路由到对应处理器
4. 完成后台自动触发 Phase B 拆解

### Phase 3：通用化 + 产品化（未来）

1. 支持微信公众号文章（直接读 DOM）
2. 支持任意网页降级采集
3. 支持采集队列管理（批量确认 → 批量处理）
4. 计划：打包上架 Chrome Web Store

## 文件结构

```
_knowledge-downloader/
├── extension/                    ← 浏览器插件目录
│   ├── manifest.json             ← 插件声明
│   ├── popup.html                ← 弹出窗口 UI
│   ├── popup.js                  ← 弹出窗口逻辑
│   ├── content.js                ← 页面注入脚本
│   └── background.js             ← 后台服务连接
├── scripts/
│   ├── local_server.py           ← 本地 HTTP 服务（新增）
│   ├── downloader.py             ← 已有
│   ├── bili_subtitle.py          ← 已有
│   └── report_agent.py           ← 已有
├── templates/
│   ├── report-template.md        ← 已有
│   ├── report-prompt.md          ← 已有
│   └── subtitle-clean-prompt.md  ← 已有
└── SKILL.md
```

## 关联项目参考

- `e:\AI小说\Ai 网文agent外部资料学习\chrome-extension\Wawa Prompt Interceptor` — 同类型的浏览器数据提取插件，可复用其 manifest.json 骨架和 content.js 注入模式
- `_knowledge-downloader` — 后端管线，插件的数据消费方

## 一句话总结

> 把 CLI 能力装进浏览器，让内容采集从「复制链接→敲命令」变成「看到好内容，点一下 Popwave」，后端管线 100% 复用。
