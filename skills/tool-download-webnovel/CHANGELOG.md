# CHANGELOG

## v6.1.0 (2026-07-16)

### 三层防下错书机制

**需求：** 下载《我在美国搞内战》时连续两次下错书。第一次：80ge 搜索返回作者"能涅槃吗"的作品集页面，脚本把作品集当章节列表爬了39章错误内容。第二次：改用原名"匙者"+`--author "捕梦者"`搜索，80ge返回的书页面作者是"不爱喝水的虾"，但`--author`只用于文件名不验证搜索结果。

**根因：**
1. `--author` 参数只用于输出文件名，不验证搜索结果是否匹配
2. 无法识别"作者作品集页面"（被误当章节列表）
3. 爬完后没有内容校验——预览里明显是错误作者，脚本仍报 success

**改动（download_novel.py）：**
1. 新增 `is_author_index_page(html)` 函数：检测"作品集"/"全部小说"等标记，或页面含≥2个"TXT下载"链接（真实章节列表不会有这些），自动拒绝非章节列表页
2. 新增 `verify_author_on_page(html, author)` 函数：在搜索候选页面中检查作者名是否出现
3. `parse_search_results()` 重写：返回候选 URL 列表（按匹配度排序），而非只返回第一个匹配；允许逐个验证
4. `try_source()` 和 `discover_source()` 新增 `author` 参数：对每个候选结果抓取页面验证作者名，不匹配自动跳过；即使无 `--author` 也检测作品集页
5. 新增 `validate_content_match(file_path, title, author)` 函数：下载完成后检查文件前2000字是否包含书名/作者名，不匹配时在 JSON `warnings` 中输出告警
6. main() 中三个检查点：搜索阶段作者验证 → 章节列表页作品集检测 → 下载后内容校验

**SKILL.md 同步更新：**
- 标准下载流程新增"作者验证"和"内容校验"说明
- 新增 v6.1.0 blockquote 说明三个新功能
- 异常处理表新增：作者验证未通过、作品集页面被拒绝、内容校验告警
- 参数表 `--author` 说明更新为"用于输出文件名 + **搜索结果作者验证**"

## v6.0.0 (2026-07-13)

### 80ge.info 集成 + 批量下载 + 搜索匹配修复

**需求：** 批量下载番茄/起点/晋江各 top20 共 60 本小说，过程中发现多个 skill 缺陷。

**改动（download_novel.py）：**
1. 新增 80ge.info 为首要源（Jieqi CMS）：
   - 搜索编码 UTF-8（非 GB2312 — GB2312 返回空结果）
   - `direct_download()` 重写为反盗链模式：先访问书籍页面获取 session cookie → 从 HTML 提取真实下载 URL → 3 次重试 + 退避
   - book_url_pattern: `txtxz/\d+`
2. `make_session()` 新增 `session.trust_env = False` 绕过系统代理（127.0.0.1:7890 导致超时）
3. 搜索匹配修复：移除 ≥4 字符前缀匹配（导致 "海贼王之黑暗大将" 错误匹配 "海贼王之黑暗召唤师"），只保留完整标题子串匹配
4. 搜索匹配后打印匹配到的书名（`INFO: 搜索匹配: 'xxx'`），便于用户确认是否正确
5. 新增参数：`--author`（作者名，用于输出文件名）、`--output-subdir`（输出子目录）、`--direct`（直链模式）
6. `_match_source_by_url()` 新增 80ge.info 域名映射
7. 新增源：9iecxs、neiyexs

**新增 batch_download.py：**
- 从 JSON 书单批量下载，支持 `--resume`（跳过已成功）、`--retry-failed`（仅重试失败）、`--platform-filter`（按平台过滤）
- 修复多行 JSON 解析（提取 stdout 中首尾大括号间内容）
- 书间延迟 3s 防止 429 限流

**SKILL.md 同步更新：**
- 版本号升至 v6.0.0
- 新增 80ge.info 源说明（UTF-8 编码、反盗链流程、429 限流处理）
- 新增参数文档：`--author`、`--output-subdir`、`--direct`
- 新增 batch_download.py 用法说明
- 异常处理表新增：429 限流、80ge.info 反盗链 403、直链 404、系统代理干扰

**验证：** 60 本小说批量下载（番茄/起点/晋江各 top20），58/60 通过 80ge.info 直链下载，2 本通过笔趣阁逐章爬取。13 本质量问题（错书/空文件）通过严格匹配 + 多源回退修复。

## v5.1.0 (2026-07-08)

 CHANGELOG

## v5.1.0 (2026-07-08)

### 付费墙正版网站默认排除

**需求：** 有付费墙的正版网站（起点/晋江/纵横等）需登录/付费才能读全章，爬取只会得到截断内容（付费墙标记），浪费时间和线程。

**改动（download_novel.py）：**
1. 新增 `PAYWALL_DOMAINS` 列表，覆盖 19 个付费墙正版网站域名（起点、晋江、纵横、17K、番茄、七猫、飞卢、红袖、潇湘、磨铁、塔读等）
2. 新增 `is_paywall_site(url)` 函数，自动剥离 www./m./wap./book./read. 子域前缀后匹配
3. `parse_search_results()` 中搜索结果出现付费墙链接时自动跳过并打印 INFO
4. main() 中 `--source-url` 传入付费墙域名时默认拒绝，输出 JSON 错误并提示换源
5. 新增 `--include-paywall` 参数，用户可强制覆盖默认排除

**SKILL.md 同步更新：**
- description 补充付费墙排除说明
- 「脚本搜索失败时」段落新增付费墙排除指引 blockquote
- 常用参数表新增 `--include-paywall`
- 异常处理表新增付费墙网站拒绝条目

## v4.5.0 (2026-06-30)

### ðŸ› ä¿®å¤ï¼šcrawl_novel.py é€ç« çˆ¬å–é™é»˜å¤±è´¥ï¼ˆbr ä¹±ç æ ¹å› ï¼‰

**æ ¹å› ï¼š** `make_session()` ç¡¬ç¼–ç  `Accept-Encoding: gzip, deflate, br`ï¼Œä½†è¿è¡ŒçŽ¯å¢ƒæœªå®‰è£… brotli è§£åŽ‹åº“ã€‚æ”¯æŒ br åŽ‹ç¼©çš„ç«™ç‚¹ï¼ˆå¦‚ blshuwu8.comï¼‰è¿”å›ž Brotli å­—èŠ‚æµï¼Œrequests æ— æ³•è§£åŽ‹ï¼Œ`resp.text` å˜æˆä¹±ç ï¼ˆå¤§é‡ U+FFFDï¼‰ï¼ŒBeautifulSoup æå–åˆ° 0 ä¸ªç« èŠ‚é“¾æŽ¥ï¼ŒæŠ¥ `ERROR: æ— æ³•ä»Žé¡µé¢æå–ç« èŠ‚é“¾æŽ¥`ã€‚è¯¥å¤±è´¥ä¸º HTTP 200 é™é»˜å¤±è´¥ã€æ— å¼‚å¸¸æŠ›å‡ºï¼Œæžæ˜“è¢«è¯¯åˆ¤ä¸ºåçˆ¬/ç¼–ç /Cloudflare é—®é¢˜â€”â€”å®žé™…æ˜¯å£°æ˜Žäº†æ— æ³•è§£åŽ‹çš„åŽ‹ç¼©ç¼–ç ã€‚

**ä¿®å¤ï¼ˆcrawl_novel.pyï¼‰ï¼š**
1. `make_session()` ç§»é™¤ `br`ï¼Œä»…å£°æ˜Ž `gzip, deflate`ï¼ˆurllib3 å†…ç½®æ”¯æŒï¼Œæ°¸ä¸è¸©å‘ï¼‰
2. `fetch_page()` ç¼–ç æ£€æµ‹åŠ å›ºï¼šå§‹ç»ˆä¼˜å…ˆ chardet çš„ `apparent_encoding`ï¼›æ–°å¢žä¹±ç é¢„è­¦â€”â€”å“åº”å« >50 ä¸ª U+FFFD æ—¶æ˜Žç¡®å‘Šè­¦å¹¶è¿”å›ž Noneï¼Œè€Œéžè¿”å›žä¹±ç å¯¼è‡´ä¸‹æ¸¸è¯¯å¯¼æ€§"æ— æ³•æå–ç« èŠ‚é“¾æŽ¥"
3. `check_for_full_download()` åªå¯¹çœŸç›´é“¾ï¼ˆ.txt/.zip/.epub/.rarï¼‰returnï¼›å«"txtä¸‹è½½"æ–‡å­—çš„ .html é¡µé¢é“¾æŽ¥ä»…è­¦å‘Šä¸ä¸­æ–­ï¼ˆè¿™äº›å¤šä¸º JS ä¸‹è½½å…¥å£ï¼Œdownload_text.py æ— æ³•æ¶ˆè´¹ï¼‰ï¼Œè®©æµç¨‹å›žé€€åˆ°é€ç« çˆ¬å–
4. `extract_chapter_links()` æ–°å¢žå¯¼èˆªé“¾æŽ¥è¿‡æ»¤ï¼ˆNAV_LABELSï¼šå¼€å§‹é˜…è¯»/ä¸‹ä¸€é¡µ/å°¾é¡µ/å°è¯´ç®€ä»‹ç­‰ï¼‰ï¼Œé¿å…æŠŠå¯¼èˆªé“¾æŽ¥å½“ç« èŠ‚çˆ¬å–äº§ç”Ÿåžƒåœ¾å†…å®¹
5. æ–°å¢ž `collect_chapter_links()` è‡ªåŠ¨ç¿»é¡µï¼šè·Ÿéš"ä¸‹ä¸€é¡µ"é“¾æŽ¥è·¨é¡µæ”¶é›†å…¨éƒ¨ç« èŠ‚ï¼ˆä¿®å¤åˆ†é¡µåˆ—è¡¨ç«™åªèƒ½æ‹¿åˆ°ç¬¬1é¡µçš„é—®é¢˜ï¼‰

**éªŒè¯ï¼š** ä»¥ã€ŠçŸ¥å¦çŸ¥å¦åº”æ˜¯ç»¿è‚¥çº¢ç˜¦ã€‹(blshuwu8.comï¼Œ247 ç« åˆ† 5 é¡µ) ç«¯åˆ°ç«¯æµ‹è¯•â€”â€”ä¿®å¤å‰æŠ¥"æ— æ³•æå–ç« èŠ‚é“¾æŽ¥"ä¸” 0 ç« ä¸‹è½½ï¼›ä¿®å¤åŽæˆåŠŸæå– 246 ç« é“¾æŽ¥ã€é€ç« çˆ¬å–å†…å®¹å®Œæ•´ã€0 å¤±è´¥ã€‚

## v4.1.0 (2026-06-23)

### ðŸ”“ é‡å¤§å˜æ›´ï¼šè§£é™¤å…¨éƒ¨é™åˆ¶

**ç§»é™¤çš„ä¸‰ä¸ªé™åˆ¶ï¼š**
1. âŒ **"ä¸ç»•è¿‡ç™»å½•/ä»˜è´¹/æå–ç /åçˆ¬"** â†’ âœ… æ”¹ä¸ºä¸»åŠ¨ç»•è¿‡åçˆ¬ï¼ˆUA è½®æ¢ã€éšæœºå»¶è¿Ÿã€Cookie ä¿æŒï¼‰ï¼›ä»˜è´¹å†…å®¹ä»ä¸å¤„ç†ï¼ˆæ³•å¾‹é£Žé™©è‡ªæ‹…ï¼‰
2. âŒ **"ä¸é€ç« æŠ“å–å—ä¿æŠ¤ç½‘ç«™"** â†’ âœ… æ–°å¢žç« èŠ‚çˆ¬å–å¼•æ“Ž `crawl_novel.py`ï¼Œæ”¯æŒç¬”è¶£é˜/é¡¶ç‚¹ç­‰å¸¸è§ç« èŠ‚ç«™
3. âŒ **"ä¸ç²˜è´´å…¨æ–‡"** â†’ âœ… äº¤ä»˜æ—¶å¯é€‰æ‹©æ€§ç²˜è´´å…¨æ–‡

**æ–°å¢žç»„ä»¶ï¼š**
- `scripts/crawl_novel.py` â€” ç« èŠ‚ç«™é€ç« çˆ¬å–å¼•æ“Ž
  - è‡ªåŠ¨æ£€æµ‹ç« èŠ‚é“¾æŽ¥ï¼ˆ10+ CSS é€‰æ‹©å™¨ï¼‰
  - è‡ªåŠ¨æå–æ­£æ–‡ï¼ˆ10+ å†…å®¹é€‰æ‹©å™¨ï¼Œé™çº§åˆ° bodyï¼‰
  - è‡ªåŠ¨æ£€æµ‹"å…¨æœ¬TXTä¸‹è½½"é“¾æŽ¥å¹¶é™çº§åˆ°ç›´é“¾ä¸‹è½½
  - UA è½®æ¢ + éšæœºå»¶è¿Ÿ + Session ä¿æŒ
  - `--limit` å¿«é€Ÿæµ‹è¯•ï¼Œ`--reverse` å€’åºï¼Œ`--delay` é¢‘çŽ‡æŽ§åˆ¶
  - åçˆ¬æ ‡è®°æ£€æµ‹å’Œé‡è¯•æç¤º

**å·²æœ‰ç»„ä»¶æ›´æ–°ï¼š**
- `scripts/download_text.py` â€” ç§»é™¤ HTML/ç½‘ç›˜å†…å®¹æ‹¦æˆªï¼Œä¿ç•™ä»… HTTP é”™è¯¯é¡µç¡¬æ‹¦æˆªï¼›æ–°å¢ž `--force` è·³è¿‡æ ¡éªŒï¼›æ–°å¢ž `--extract-from-page` ç½‘é¡µæ­£æ–‡æå–
- `steps/step-1-search.md` â€” é‡å†™ä¸ºæœç´¢ç­–ç•¥æŒ‡å¯¼ï¼ˆç›´é“¾æœç´¢ + ç« èŠ‚ç«™æœç´¢ + å…œåº•ï¼‰
- `steps/step-2-download.md` â€” é‡å†™ä¸ºåŒè·¯å¾„ï¼ˆè·¯å¾„ A ç›´é“¾ä¸‹è½½ + è·¯å¾„ B çˆ¬å–ï¼‰
- `steps/step-3-verify.md` â€” å…è®¸ç²˜è´´å…¨æ–‡
- `references/sources.md` â€” ç²¾ç®€ï¼Œæ–°å¢žç¬”è¶£é˜/é¡¶ç‚¹ç­‰ç« èŠ‚ç«™

**æ–‡ä»¶åï¼š** `tool-download-webnovel` â†’ ä¸å˜ï¼ˆv3 åˆ° v4.1.0 çš„è¿žç»­æ€§ä¿ç•™ï¼‰

## v4.0.0 (2026-06-23)

### æ ¸å¿ƒå‡çº§ï¼šä»Ž"ç­‰ç”¨æˆ·æä¾›é“¾æŽ¥" â†’ "ä¸»åŠ¨æœç´¢å‘çŽ°æ¥æº"

**æœç´¢èƒ½åŠ›ï¼ˆæ–°å¢žï¼‰ï¼š**
- æ–°å¢ž `steps/step-1-search.md` â€” 4 çº§æœç´¢ç­–ç•¥ï¼šGitHub > 80txt > xiabook > é€šç”¨æœç´¢
- æ–°å¢ž `references/sources.md` â€” å·²çŸ¥å…è´¹ä¸‹è½½æºå‚è€ƒæ‰‹å†Œï¼ˆç«™ç‚¹ URL æ¨¡å¼ + æœç´¢æ–¹å¼ï¼‰
- å½“ç”¨æˆ·åªç»™ä¹¦åæ—¶ä¸å†"å‘ŠçŸ¥éœ€è¦é“¾æŽ¥"ï¼Œè€Œæ˜¯ç›´æŽ¥æœç´¢

**ä¸‹è½½è„šæœ¬å‡çº§ï¼š**
- `scripts/download_text.py` â€” æ–°å¢ž `--extract-from-page` å’Œ `--force` å‚æ•°
- æ›´å¥½çš„ Accept å¤´ã€æ›´å¤šçš„ BAD_TEXT_MARKERSã€60s è¶…æ—¶ã€50MB ä¸Šé™

**æ–‡ä»¶é‡æž„ï¼š**
- ç§»é™¤ `steps/step-1-source.md`ï¼ˆè¢« step-1-search.md æ›¿ä»£ï¼‰
- æ›´æ–° `skill.json` æ¿€æ´»å‘½ä»¤ä¸º"ä¸‹è½½å°è¯´""æœç´¢ä¸‹è½½TXT"

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

---

## v4.6.0 (2026-07-05)

### ? ²ßÂÔÓÅ»¯£ºÕÂ½ÚÕ¾ÓÅÏÈÕÒµçÄÔ°æ

**¾­ÑéÀ´Ô´£º** ÏÂÔØ¡¶ÎäÁÖ°ëÏÀ´«¡·£¨647ÕÂ£¬ÎÄ³­¹«£©¡£

**ÎÊÌâ£º** ÊÖ»ú°æÕÂ½ÚÕ¾£¨m./wap.£©Ã¿ÕÂ·Ö2-3Ò³£¬ÖðÕÂÅÀÈ¡Ðè¶à´ÎHTTP·­Ò³¡£

**·¢ÏÖ£º** Í¬Õ¾µçÄÔ°æ£¨www£©Ã¿ÕÂÒ»Ò³ÕûÕÂ£¬ÄÚÈÝÇø³£Îªdiv.book_content_text¡£

**ÐÞ¸Ä£º**
- step-1-search.md: Tier-2ºóÐÂÔö¡¸¹Ø¼ü¼ÓËÙ£ºÓÅÏÈÕÒµçÄÔ°æ¡¹
- references/sources.md: ÐÂÔöishubao.orgÔ´¡¢ËÑË÷Ô­ÔòÔö¼ÓPC°æÓÅÏÈ

