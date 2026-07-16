---
name: tool-download-webnovel
description: 搜索并下载中文网文 TXT：自动搜索直链 → 下载/爬取 → 校验。支持 80ge.info、GitHub、笔趣阁等公开来源。默认排除付费墙正版网站（起点/晋江/纵横等）。拆书管线第一步：用户说"拆书"但无源文件时，先执行本 skill 下载。无限制：可绕过反爬、可逐章爬取、可粘贴全文、可批量下载。
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

### 批量下载（从 JSON 书单）

```bash
python3 .../batch_download.py book_list.json --output-base "D:\\workspace\\参考小说txt" --script-dir "..."
```

支持 `--resume`（跳过已成功）、`--retry-failed`（仅重试失败）、`--platform-filter`（按平台过滤）。

### 已知 URL（跳过搜索）

```bash
# 章节列表页 URL
python3 .../download_novel.py "书名" --source-url "http://www.boquku.com/book/123/"

# 直链 TXT/ZIP（80ge.info 直链会自动处理反盗链）
python3 .../download_novel.py "书名" --source-url "https://example.com/book.txt" --direct
```

### 常用参数

| 参数 | 默认 | 说明 |
|:-----|:-----|:-----|
| `--author NAME` | None | 作者名（用于输出文件名 + 匹配验证） |
| `--output-subdir DIR` | None | 输出子目录（如 `番茄top20`） |
| `--workers N` | 10 | 并发线程数（无反爬站推荐 16） |
| `--resume` | off | 断点续爬，跳过已下载章节 |
| `--limit N` | 0 | 只爬前 N 章（测试用） |
| `--direct` | off | 源 URL 为直链 TXT/ZIP |
| `--chapter-selector` | auto | 手动指定章节列表 CSS 选择器 |
| `--content-selector` | auto | 手动指定正文 CSS 选择器 |
| `--include-paywall` | off | 允许爬取付费墙正版网站（默认排除） |

### 脚本搜索失败时

脚本内置源的搜索功能可能失效（站点改版/下线）。此时 agent 用 popwave-search 搜索 `{书名} txt 下载` / `{书名} 笔趣阁`，找到章节列表页 URL 后用 `--source-url` 传入。脚本会自动按域名匹配已知选择器配置。

> **付费墙正版网站默认排除：** 起点(qidian.com)、晋江(jjwxc.net)、纵横(zongheng.com)、17K(17k.com)、番茄(fanqienovel.com)、七猫(qimao.com)、飞卢(faloo.com) 等正版站点需登录/付费才能读全章，爬取只会得到截断内容。搜索时**禁止**选这些站作为来源；`--source-url` 传入这些域名会被脚本自动拒绝。确需爬免费试读章节时加 `--include-paywall`。

---

## 已知源

| 源 | 搜索 | 说明 |
|:---|:-----|:-----|
| **80ge.info** | ✓ | Jieqi CMS，搜索编码 UTF-8（非 GB2312）。直链需反盗链：先访问书籍页面获取 cookie → 从 HTML 提取真实下载 URL → 重试 3 次。批量下载需 3-5s 间隔防 429 限流 |
| miaobige | ✓ | 秒笔阁，通用爬取 |
| boquku | ✗ | 博趣库，搜索已关闭，需 `--source-url` |
| ishubao | ✗ | 需 `--source-url` |
| 9iecxs | ✗ | 需 `--source-url` |
| neiyexs | ✗ | 需 `--source-url` |

---

## 输出格式（JSON）

```json
{
  "status": "success",
  "output": "D:\\\\popwave-skills\\\\downloads\\\\书名.txt",
  "size_mb": 10.67,
  "chapters_crawled": 1030,
  "chapters_failed": 0,
  "source": "80ge",
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
| 反爬触发（429/503） | `--workers 1 --delay 2.5` 降速重试；80ge.info 批量下载间隔 ≥3s |
| 80ge.info 反盗链 403 | 脚本自动访问书籍页面获取 cookie，无需手动处理 |
| 80ge.info 直链 404 | URL 编码问题，尝试章节爬取模式（`txtml_{book_id}.html`） |
| 爬取中断 | `--resume` 断点续爬 |
| 付费墙检测告警 | 换源重下 |
| `--source-url` 指向付费墙正版网站 | 默认拒绝，换免费源；或加 `--include-paywall` |
| 文件 > 50MB | 拒绝 |
| 系统代理干扰（127.0.0.1:7890） | 脚本已内置 `session.trust_env = False` 自动绕过 |

---

## 文件职责

| 文件 | 用途 |
|:-----|:-----|
| `scripts/download_novel.py` | **统一入口**：搜索→爬取→验证→交付。支持 `--direct` 直链模式、`--author`/`--output-subdir` 参数、80ge.info 反盗链 |
| `scripts/batch_download.py` | **批量下载**：从 JSON 书单批量下载，支持 `--resume`/`--retry-failed`/`--platform-filter` |
| `scripts/crawl_novel.py` | 逐章爬取（保留兼容） |
| `scripts/download_text.py` | 直链下载/本地导入（保留兼容） |

---

## 版本

v6.0.0 | 2026-07-13 | 新增 80ge.info 为首要源（UTF-8 搜索 + 反盗链直链下载）；新增 `--author`/`--output-subdir`/`--direct` 参数；新增 `batch_download.py` 批量下载脚本；搜索匹配改为严格模式（完整标题或≥4字符前缀匹配，替代旧的2字符宽松匹配）；`make_session()` 添加 `trust_env=False` 绕过系统代理；`direct_download()` 重写为反盗链模式（先访问书籍页面获取 cookie → 提取真实 URL → 3 次重试）；`batch_download.py` 修复多行 JSON 解析
v5.1.0 | 2026-07-08 | 新增付费墙正版网站默认排除（起点/晋江/纵横等19个域名），搜索结果自动过滤付费墙链接，`--source-url` 传入付费墙域名时拒绝并提示换源，新增 `--include-paywall` 参数可强制覆盖
v5.0.0 | 2026-07-06 | 重构：统一入口 download_novel.py 吃下全链路（搜索+测源+并发爬取+付费墙检测+交付），删除 step-1/2/3 + sources.md，SKILL.md 从 230 行砍至极简
v4.6.0 | 2026-07-06 | crawl_novel.py 新增 ThreadPoolExecutor 并发 + 断点续爬
v4.5.0 | 2026-06-30 | 修复 crawl_novel.py br 压码致静默失败
v4.4.0 | 2026-06-24 | Step 3 新增付费墙检测
