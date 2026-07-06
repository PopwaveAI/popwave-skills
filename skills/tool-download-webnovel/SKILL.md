---
name: tool-download-webnovel
description: 搜索并下载中文网文 TXT：自动搜索直链 → 下载/爬取 → 校验。支持 GitHub、80txt、笔趣阁等公开来源。拆书管线第一步：用户说"拆书"但无源文件时，先执行本 skill 下载。无限制：可绕过反爬、可逐章爬取、可粘贴全文。
---

# tool-download-webnovel · 网文搜索下载

> **定位：** 当用户说"下载《书名》"时启用。一条命令完成搜索→爬取→验证→交付。

---

## 用法

### 标准下载（自动搜索 + 并发爬取 + 验证）

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/download_novel.py "书名" \
  --output-dir /d/popwave-skills/downloads
```

脚本自动完成：搜索已知源 → 测单章确定选择器 → 10 线程并发爬取 → 付费墙检测 → 输出 JSON 结果。

### 已知 URL（跳过搜索）

```bash
# 章节列表页 URL
python3 .../download_novel.py "书名" --source-url "http://www.boquku.com/book/123/"

# 直链 TXT/ZIP
python3 .../download_novel.py "书名" --source-url "https://example.com/book.txt" --direct
```

### 常用参数

| 参数 | 默认 | 说明 |
|:-----|:-----|:-----|
| `--workers N` | 10 | 并发线程数（无反爬站推荐 16） |
| `--resume` | off | 断点续爬，跳过已下载章节 |
| `--limit N` | 0 | 只爬前 N 章（测试用） |
| `--chapter-selector` | auto | 手动指定章节列表 CSS 选择器 |
| `--content-selector` | auto | 手动指定正文 CSS 选择器 |

### 脚本搜索失败时

脚本内置源的搜索功能可能失效（站点改版/下线）。此时 agent 用 popwave-search 搜索 `{书名} txt 下载` / `{书名} 笔趣阁`，找到章节列表页 URL 后用 `--source-url` 传入。脚本会自动按域名匹配已知选择器配置。

---

## 输出格式（JSON）

```json
{
  "status": "success",
  "output": "D:\\popwave-skills\\downloads\\书名.txt",
  "size_mb": 10.67,
  "chapters_crawled": 1030,
  "chapters_failed": 0,
  "source": "boquku",
  "elapsed_seconds": 75.7,
  "paywall_warnings": 0,
  "warnings": [],
  "preview": "第一章..."
}
```

status=error 时读 `reason` 和 `suggestion`。

---

## 异常处理

| 情况 | 动作 |
|:-----|:-----|
| 脚本自动搜索全部失败 | agent 用 popwave-search 找 URL，`--source-url` 传入 |
| Cloudflare Turnstile 验证 | 无法绕过，换源 |
| CDN 直链 522/403 | **禁止重试**，换章节站爬取 |
| 反爬触发（429/503） | `--workers 1 --delay 2.5` 降速重试 |
| 爬取中断 | `--resume` 断点续爬 |
| 付费墙检测告警 | 换源重下 |
| 文件 > 50MB | 拒绝 |

---

## 文件职责

| 文件 | 用途 |
|:-----|:-----|
| `scripts/download_novel.py` | **统一入口**：搜索→爬取→验证→交付 |
| `scripts/crawl_novel.py` | 逐章爬取（download_novel.py 内部逻辑的独立版本，保留兼容） |
| `scripts/download_text.py` | 直链下载/本地导入（保留兼容） |

---

## 版本

v5.0.0 | 2026-07-06 | 重构：统一入口 download_novel.py 吃下全链路（搜索+测源+并发爬取+付费墙检测+交付），删除 step-1/2/3 + sources.md，SKILL.md 从 230 行砍至极简
v4.6.0 | 2026-07-06 | crawl_novel.py 新增 ThreadPoolExecutor 并发 + 断点续爬
v4.5.0 | 2026-06-30 | 修复 crawl_novel.py br 压码致静默失败
v4.4.0 | 2026-06-24 | Step 3 新增付费墙检测
