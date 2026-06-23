# CHANGELOG

## v4.0.0 (2026-06-23)

### 核心升级：从"等用户提供链接" → "主动搜索发现来源"

**搜索能力（新增）：**
- 新增 `steps/step-1-search.md` — 4 级搜索策略：GitHub > 80txt > xiabook > 通用搜索
- 新增 `references/sources.md` — 已知免费下载源参考手册（URL 模式、搜索方式、优先级）
- 当用户只给书名时，自动多源搜索发现可下载 TXT/ZIP 链接

**脚本升级：**
- `scripts/download_text.py` 增加 `--extract-from-page` 参数 → 可提取网页可见文本
- `scripts/download_text.py` 增加 `--force` 参数 → 强制输出（跳过校验警告）
- 改进 HTTP 请求头模拟浏览器，减少被拦截
- 增加更多 BAD_TEXT_MARKERS（页面不存在、下载链接失效等）
- 增加更多编码支持（shift_jis）
- 超时从 30s 提升到 60s
- 50MB 文件大小上限警告

**流程重构：**
- 3 步流程：搜索 → 下载 → 校验（替代原来的 确认→下载→校验）
- 移除过时的 `steps/step-1-source.md`（已被搜索 step 替代）
- SKILL.md 重写为搜索优先架构
- skill.json 新增激活命令：下载小说、搜索下载TXT

### v3.0.1 (2026-06-22)

- Re-emphasized direct-link download as the primary workflow.
- Clarified that acceptable sources are authorized TXT/ZIP direct links or local files.
- Preserved boundaries against prioritizing infringing repost sites, bypassing access controls, and protected-site chapter crawling.

### v3.0.0 (2026-06-22)

- Reframed skill from "search direct links" to authorized source download/import.
- Added `scripts/download_text.py` for URL/local file import, ZIP extraction, UTF-8 normalization, HTML/error-page detection, and size validation.
- Replaced `steps/step-1-search.md` with `steps/step-1-source.md` to enforce source/permission checks.
- Updated SKILL.md and skill.json to forbid piracy-oriented search, login/paywall bypass, protected-site crawling, and full-text pasteback.

### v2.0.1 (2026-06-14)

- v5 structural refactoring: added CHANGELOG.md, steps/ directory, drop-point check table, steps references in SKILL.md, pipeline field in skill.json.

### v2.0.0 (2026-06-13)

- Initial release. SOP with lookup table, red lines, WRONG examples, error handling.
