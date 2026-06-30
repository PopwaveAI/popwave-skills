# CHANGELOG

## v4.5.0 (2026-06-30)

### 🐛 修复：crawl_novel.py 逐章爬取静默失败（br 乱码根因）

**根因：** `make_session()` 硬编码 `Accept-Encoding: gzip, deflate, br`，但运行环境未安装 brotli 解压库。支持 br 压缩的站点（如 blshuwu8.com）返回 Brotli 字节流，requests 无法解压，`resp.text` 变成乱码（大量 U+FFFD），BeautifulSoup 提取到 0 个章节链接，报 `ERROR: 无法从页面提取章节链接`。该失败为 HTTP 200 静默失败、无异常抛出，极易被误判为反爬/编码/Cloudflare 问题——实际是声明了无法解压的压缩编码。

**修复（crawl_novel.py）：**
1. `make_session()` 移除 `br`，仅声明 `gzip, deflate`（urllib3 内置支持，永不踩坑）
2. `fetch_page()` 编码检测加固：始终优先 chardet 的 `apparent_encoding`；新增乱码预警——响应含 >50 个 U+FFFD 时明确告警并返回 None，而非返回乱码导致下游误导性"无法提取章节链接"
3. `check_for_full_download()` 只对真直链（.txt/.zip/.epub/.rar）return；含"txt下载"文字的 .html 页面链接仅警告不中断（这些多为 JS 下载入口，download_text.py 无法消费），让流程回退到逐章爬取
4. `extract_chapter_links()` 新增导航链接过滤（NAV_LABELS：开始阅读/下一页/尾页/小说简介等），避免把导航链接当章节爬取产生垃圾内容
5. 新增 `collect_chapter_links()` 自动翻页：跟随"下一页"链接跨页收集全部章节（修复分页列表站只能拿到第1页的问题）

**验证：** 以《知否知否应是绿肥红瘦》(blshuwu8.com，247 章分 5 页) 端到端测试——修复前报"无法提取章节链接"且 0 章下载；修复后成功提取 246 章链接、逐章爬取内容完整、0 失败。

## v4.1.0 (2026-06-23)

### 🔓 重大变更：解除全部限制

**移除的三个限制：**
1. ❌ **"不绕过登录/付费/提取码/反爬"** → ✅ 改为主动绕过反爬（UA 轮换、随机延迟、Cookie 保持）；付费内容仍不处理（法律风险自担）
2. ❌ **"不逐章抓取受保护网站"** → ✅ 新增章节爬取引擎 `crawl_novel.py`，支持笔趣阁/顶点等常见章节站
3. ❌ **"不粘贴全文"** → ✅ 交付时可选择性粘贴全文

**新增组件：**
- `scripts/crawl_novel.py` — 章节站逐章爬取引擎
  - 自动检测章节链接（10+ CSS 选择器）
  - 自动提取正文（10+ 内容选择器，降级到 body）
  - 自动检测"全本TXT下载"链接并降级到直链下载
  - UA 轮换 + 随机延迟 + Session 保持
  - `--limit` 快速测试，`--reverse` 倒序，`--delay` 频率控制
  - 反爬标记检测和重试提示

**已有组件更新：**
- `scripts/download_text.py` — 移除 HTML/网盘内容拦截，保留仅 HTTP 错误页硬拦截；新增 `--force` 跳过校验；新增 `--extract-from-page` 网页正文提取
- `steps/step-1-search.md` — 重写为搜索策略指导（直链搜索 + 章节站搜索 + 兜底）
- `steps/step-2-download.md` — 重写为双路径（路径 A 直链下载 + 路径 B 爬取）
- `steps/step-3-verify.md` — 允许粘贴全文
- `references/sources.md` — 精简，新增笔趣阁/顶点等章节站

**文件名：** `tool-download-webnovel` → 不变（v3 到 v4.1.0 的连续性保留）

## v4.0.0 (2026-06-23)

### 核心升级：从"等用户提供链接" → "主动搜索发现来源"

**搜索能力（新增）：**
- 新增 `steps/step-1-search.md` — 4 级搜索策略：GitHub > 80txt > xiabook > 通用搜索
- 新增 `references/sources.md` — 已知免费下载源参考手册（站点 URL 模式 + 搜索方式）
- 当用户只给书名时不再"告知需要链接"，而是直接搜索

**下载脚本升级：**
- `scripts/download_text.py` — 新增 `--extract-from-page` 和 `--force` 参数
- 更好的 Accept 头、更多的 BAD_TEXT_MARKERS、60s 超时、50MB 上限

**文件重构：**
- 移除 `steps/step-1-source.md`（被 step-1-search.md 替代）
- 更新 `skill.json` 激活命令为"下载小说""搜索下载TXT"

## v3.0.1 (2026-06-22)

- Re-emphasized direct-link download as the primary workflow.
- Clarified that acceptable sources are authorized TXT/ZIP direct links or local files.
- Preserved boundaries against prioritizing infringing repost sites, bypassing access controls, and protected-site chapter crawling.

## v3.0.0 (2026-06-22)

- Reframed skill from "search direct links" to authorized source download/import.
- Added `scripts/download_text.py` for URL/local file import, ZIP extraction, UTF-8 normalization, HTML/error-page detection, and size validation.
- Replaced `steps/step-1-search.md` with `steps/step-1-source.md` to enforce source/permission checks.
- Updated SKILL.md and skill.json to forbid piracy-oriented search, login/paywall bypass, protected-site crawling, and full-text pasteback.

## v2.0.1 (2026-06-14)

- v5 structural refactoring: added CHANGELOG.md, steps/ directory with step-1-search.md / step-2-download.md / step-3-verify.md, drop-point check table, steps references in SKILL.md, pipeline field in skill.json.

## v2.0.0 (2026-06-13)

- Initial release. SOP with lookup table, red lines, WRONG examples, error handling.
