---
name: tool-download-webnovel
description: 搜索并下载中文网文 TXT。三阶段 SOP：脚本自动搜索 → agent web 搜索兜底 → 验证交付。默认排除付费墙正版网站。拆书管线第一步：用户说"拆书"但无源文件时，先执行本 skill 下载。
---

# tool-download-webnovel · 网文搜索下载

> **定位：** 用户说"下载《书名》"时启用。三阶段 SOP，从搜索到交付一条龙。

---

## SOP: 三阶段下载流程

### Phase 1: 脚本自动搜索

```bash
python3 .../download_novel.py "书名" --author "作者" --output-dir .../downloads
```

脚本自动完成：搜索内置源 → 作者验证 → 作品集页检测 → 测单章确定选择器 → 10 线程并发爬取 → 导航噪音过滤 → 付费墙检测 → 内容校验 → 输出 JSON。

- `status=success` → 检查 preview 和 warnings → 交付
- `status=error` → **不要放弃，进入 Phase 2**

### Phase 2: Agent Web 搜索（Phase 1 失败后强制执行）

> **红线：禁止在 Phase 1 失败后直接告知用户"找不到"。必须执行 Phase 2。**

内置源覆盖有限，大量书需通过 web 搜索找到外部免费源。按以下策略逐条尝试：

**搜索关键词（按优先级）：**
1. `{书名} {作者} 笔趣阁` — 找笔趣阁系镜像站
2. `{书名} txt 下载` — 找直链下载站
3. `{书名} {作者} 最新章节 免费阅读` — 找章节列表站
4. `{书名别名}` — 用原名/笔名/别名（网文常改名，如起点名→笔趣阁名）

**判断搜索结果：**
- ✅ **章节列表页**：URL 含 `/shu/` `/book/` `/txt/` 等，页面列出大量章节链接 → 用 `--source-url`
- ✅ **直链下载**：URL 以 `.txt`/`.zip` 结尾 → 用 `--source-url --direct`
- ❌ **付费墙站**：起点/晋江/纵横等（脚本自动拦截，无需手动排除）
- ❌ **目录索引页**：列出章节但链接指向 `qidian.com` 等 → 跳过，换源
- ❌ **APP 下载页**：要求下载 APP 才能阅读 → 跳过

**找到 URL 后执行：**
```bash
# 先测 3 章确认能抓到内容
python3 .../download_novel.py "书名" --author "作者" --source-url "URL" --limit 3

# 确认无误后全量下载
python3 .../download_novel.py "书名" --author "作者" --source-url "URL" --workers 10
```

**常见调整：**
- 章节倒序（最新章在前）→ 加 `--reverse`
- 正文有导航噪音 → 脚本自动过滤；仍残留则用 `--content-selector` 精确指定
- 内容选择器未自动检测到 → 手动指定 `--content-selector "div#content"`
- 笔趣阁站改名（如《我在美国搞内战》→《我在美国拼高达》）→ 内容校验会告警，但预览正文正确即可

### Phase 3: 验证与交付

检查 JSON 输出：
- `status=success` + `chapters_failed=0` + `warnings=[]` → 交付文件路径
- `chapters_failed > 0` → `--resume` 补爬失败章节
- `warnings` 含"内容校验" → 检查 `preview` 正文是否正确（笔趣阁改名不一定是下错书）
- `preview` 内容明显不对 → 删除文件，换源或换书名重试

---

## 红线

1. **禁止在 Phase 1 脚本搜索失败后直接放弃** — 必须执行 Phase 2 web 搜索，至少尝试 3 组关键词
2. **禁止搜索/使用付费墙正版站** — 起点/晋江/纵横等，`--source-url` 传入会被自动拦截
3. **下载后必须检查 preview 和 warnings** — 确认内容正确再交付

---

## 参数速查

| 参数 | 默认 | 说明 |
|:-----|:-----|:-----|
| `--author NAME` | None | 作者名（输出文件名 + 搜索结果作者验证） |
| `--output-subdir DIR` | None | 输出子目录（如 `番茄top20`） |
| `--workers N` | 10 | 并发线程数 |
| `--source-url URL` | None | 跳过搜索，直接用此 URL |
| `--direct` | off | 源 URL 为直链 TXT/ZIP |
| `--reverse` | off | 反转章节顺序（笔趣阁站最新章在前） |
| `--resume` | off | 断点续爬 |
| `--limit N` | 0 | 只爬前 N 章（测试用） |
| `--chapter-selector` | auto | 手动指定章节列表 CSS 选择器 |
| `--content-selector` | auto | 手动指定正文 CSS 选择器 |
| `--include-paywall` | off | 允许爬取付费墙正版网站（默认排除） |

---

## 已知源

| 源 | 搜索 | 说明 |
|:---|:-----|:-----|
| **xbiquge.la** | ✓ | 新笔趣阁（重定向到 xbiqugu.la），Jieqi CMS，章节爬取首选源 |
| **80ge.info** | ✓ | TXT 下载站（适合 `--direct` 直链模式，不适合章节爬取）。UTF-8 搜索，反盗链自动处理 |
| miaobige | ✓ | 秒笔阁 |
| biquge365 | ✗ | 需 `--source-url`。正文 `div.txt`，通常需 `--reverse` |
| boquku | ✗ | 需 `--source-url` |
| ishubao | ✗ | 需 `--source-url` |
| 9iecxs | ✗ | 需 `--source-url` |
| neiyexs | ✗ | 需 `--source-url` |

> **源不够用时：** 内置源只有 3 个支持搜索，覆盖有限。Phase 2 的 web 搜索是核心兜底机制——通过搜索引擎可以找到大量临时镜像站，用 `--source-url` 传入即可。脚本会自动匹配已知域名的选择器配置，未知域名则自动尝试 fallback 选择器。

---

## 异常处理

| 情况 | 动作 |
|:-----|:-----|
| 脚本搜索全部失败 | **执行 Phase 2 web 搜索**（非可选） |
| Phase 2 搜索也找不到 | 换书名（原名/别名/笔名）重试；仍无果则告知用户并建议正版阅读 |
| 作者验证未通过 | 换源或换书名重试 |
| 作者作品集页面被拒绝 | 搜索具体书籍页 URL，而非作者页 |
| 内容校验告警 | 先检查 preview 正文（笔趣阁可能改名），确认下错再删除 |
| 章节倒序 | 加 `--reverse` |
| 正文有导航噪音 | 脚本自动过滤；残留则 `--content-selector` 精确指定 |
| 选择器未自动检测到 | 手动指定 `--content-selector`；或先 `--limit 1` 检查页面结构 |
| Cloudflare 验证 | 无法绕过，换源 |
| 反爬触发（429/503） | `--workers 1 --delay 2.5` 降速 |
| 爬取中断 | `--resume` 断点续爬 |
| 付费墙网站 | 默认拒绝；加 `--include-paywall` 强制 |
| 系统代理干扰 | 脚本已内置 `trust_env=False` 绕过 |

---

## 输出格式（JSON）

```json
{"status":"success","output":"...","size_mb":4.18,"chapters_crawled":382,
 "chapters_failed":0,"source":"biquge365","warnings":[],"preview":"第一章..."}
```

`status=error` 时读 `reason` 和 `suggestion`。

---

## 文件职责

| 文件 | 用途 |
|:-----|:-----|
| `scripts/download_novel.py` | 统一入口：搜索→验证→爬取→校验→交付 |
| `scripts/batch_download.py` | 批量下载：从 JSON 书单，支持 `--resume`/`--retry-failed` |

---

## 版本

v7.0.0 | 2026-07-16 | SKILL.md 重构为三阶段 SOP（脚本搜索→agent web搜索兜底→验证交付）；强制 Phase 2 web 搜索红线；新增 xbiquge.la 可搜索源；已知源说明优化（强调 Phase 2 兜底机制）
v6.2.0 | 2026-07-16 | `--reverse` 参数；导航噪音过滤；biquge365 源；内容校验告警优化
v6.1.0 | 2026-07-16 | 三层防下错书：作者验证+作品集页检测+内容校验
v6.0.0 | 2026-07-13 | 80ge.info 首要源；`--author`/`--output-subdir`/`--direct`；批量下载
v5.1.0 | 2026-07-08 | 付费墙正版网站默认排除
v5.0.0 | 2026-07-06 | 统一入口重构
