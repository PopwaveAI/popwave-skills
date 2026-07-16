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

脚本自动完成：搜索已知源 → **作者验证** → 测单章确定选择器 → 10 线程并发爬取 → 付费墙检测 → **内容校验** → 输出 JSON 结果。

> **作者验证（v6.1.0 新增）：** 提供 `--author` 时，脚本会对每个搜索候选结果抓取页面并验证作者名是否出现。不匹配的候选自动跳过，避免下错书。

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
| `--author NAME` | None | 作者名（用于输出文件名 + **搜索结果作者验证**） |
| `--output-subdir DIR` | None | 输出子目录（如 `番茄top20`） |
| `--workers N` | 10 | 并发线程数（无反爬站推荐 16） |
| `--resume` | off | 断点续爬，跳过已下载章节 |
| `--limit N` | 0 | 只爬前 N 章（测试用） |
| `--direct` | off | 源 URL 为直链 TXT/ZIP |
| `--chapter-selector` | auto | 手动指定章节列表 CSS 选择器 |
| `--content-selector` | auto | 手动指定正文 CSS 选择器 |
| `--include-paywall` | off | 允许爬取付费墙正版网站（默认排除） |
| `--reverse` | off | 反转章节顺序（部分站最新章在前） |

### 脚本搜索失败时

脚本内置源的搜索功能可能失效（站点改版/下线）。此时 agent 用 popwave-search 搜索 `{书名} txt 下载` / `{书名} 笔趣阁`，找到章节列表页 URL 后用 `--source-url` 传入。脚本会自动按域名匹配已知选择器配置。

> **付费墙正版网站默认排除：** 起点(qidian.com)、晋江(jjwxc.net)、纵横(zongheng.com)、17K(17k.com)、番茄(fanqienovel.com)、七猫(qimao.com)、飞卢(faloo.com) 等正版站点需登录/付费才能读全章，爬取只会得到截断内容。搜索时**禁止**选这些站作为来源；`--source-url` 传入这些域名会被脚本自动拒绝。确需爬免费试读章节时加 `--include-paywall`。

> **作者作品集页面自动检测（v6.1.0 新增）：** 部分站的搜索结果会返回作者作品集页面（如"XX作品集"），而非具体书籍的章节列表。脚本会自动检测此类页面（检查"作品集"标记或多个"TXT下载"链接）并拒绝，避免把作品集里的其他书当章节爬取。

---

## 已知源

| 源 | 搜索 | 说明 |
|:---|:-----|:-----|
| **80ge.info** | ✓ | Jieqi CMS，搜索编码 UTF-8（非 GB2312）。直链需反盗链：先访问书籍页面获取 cookie → 从 HTML 提取真实下载 URL → 重试 3 次。批量下载需 3-5s 间隔防 429 限流 |
| miaobige | ✓ | 秒笔阁，通用爬取 |
| biquge365 | ✗ | 新笔趣阁，需 `--source-url`。正文选择器 `div.txt`，章节列表通常倒序需 `--reverse` |
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

> **内容校验告警（v6.1.0 新增）：** 下载完成后，脚本会检查文件前 2000 字中是否包含用户指定的书名和作者名。如果不匹配，JSON 的 `warnings` 字段会输出 `"内容校验: 文件中未找到作者 'XX'，可能下错了书"`。**注意：** 笔趣阁系站点常改名防搜索（如《我在美国搞内战》改为《我在美国拼高达》），内容校验告警不一定代表下错书，应结合预览内容判断。agent 看到此 warning 时应先检查预览正文是否正确，而非直接删除。

---

## 异常处理

| 情况 | 动作 |
|:-----|:-----|
| 脚本自动搜索全部失败 | agent 用 popwave-search 找 URL，`--source-url` 传入 |
| 作者验证未通过 | 换源或换书名（原名/别名）重试 |
| 作者作品集页面被拒绝 | 搜索具体书籍页 URL，而非作者页 |
| 内容校验告警 | 先检查预览正文是否正确（笔趣阁站可能改名），确认下错书再删除重下 |
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
| `scripts/download_novel.py` | **统一入口**：搜索→作者验证→爬取→验证→内容校验→交付。支持 `--direct` 直链模式、`--author`/`--output-subdir` 参数、80ge.info 反盗链、作者作品集页检测 |
| `scripts/batch_download.py` | **批量下载**：从 JSON 书单批量下载，支持 `--resume`/`--retry-failed`/`--platform-filter` |
| `scripts/crawl_novel.py` | 逐章爬取（保留兼容） |
| `scripts/download_text.py` | 直链下载/本地导入（保留兼容） |

---

## 版本

v6.2.0 | 2026-07-16 | 新增 `--reverse` 参数（笔趣阁站章节通常倒序）；新增 `CONTENT_NOISE_PATTERNS` 导航噪音过滤（自动清除"首页/章节报错/存书签/关灯/一秒记住"等笔趣阁导航文字）；`div.txt` 加入 fallback 选择器列表；新增 biquge365 已知源；内容校验告警逻辑优化（笔趣阁站改名不误判）
v6.1.0 | 2026-07-16 | 新增三层防下错书机制：①作者验证（`--author` 提供时抓取候选页面验证作者名，不匹配自动跳过）；②作者作品集页面检测（检测"作品集"标记/多个"TXT下载"链接，自动拒绝非章节列表页）；③内容校验（下载后检查文件前2000字是否包含书名/作者名，不匹配输出告警）。搜索结果改为返回候选列表（按匹配度排序），支持逐个验证
v6.0.0 | 2026-07-13 | 新增 80ge.info 为首要源（UTF-8 搜索 + 反盗链直链下载）；新增 `--author`/`--output-subdir`/`--direct` 参数；新增 `batch_download.py` 批量下载脚本；搜索匹配改为严格模式；`make_session()` 添加 `trust_env=False` 绕过系统代理；`direct_download()` 重写为反盗链模式
v5.1.0 | 2026-07-08 | 新增付费墙正版网站默认排除（起点/晋江/纵横等19个域名），搜索结果自动过滤付费墙链接，`--source-url` 传入付费墙域名时拒绝并提示换源，新增 `--include-paywall` 参数可强制覆盖
v5.0.0 | 2026-07-06 | 重构：统一入口 download_novel.py 吃下全链路，删除 step-1/2/3 + sources.md
