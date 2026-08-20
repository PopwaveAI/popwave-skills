# CHANGELOG

## v7.3.0 | 2026-08-13

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v7.3.0。

## v7.2.0 (2026-07-31)

### 内容污染检测 + 质量门禁强化 + 新增直链源

**需求：** 下载《玄鉴仙族》时，80ge 直链源的 TXT 文件末尾拼接了十几本其他小说内容，脚本零感知直接交付。根因是直链下载后零内容校验 + 验证只看前2000字 + 逐章爬取无防盗拦截。

**改动（download_novel.py）：**

1. **新增 `FOREIGN_CONTENT_MARKERS` 常量 + `scan_for_contamination()` 函数** — 全文件扫描其他小说内容（角色名/设定标记），返回污染位置和样本
2. **新增 `truncate_contamination()` 函数** — 尾部污染自动截断（最后10%区域内的污染集群），超过15%阈值不截断防误删
3. **`direct_download()` 增加下载后污染扫描** — 直链下载→解码→扫描污染→自动截断尾部→写入文件
4. **新增 `ANTILEECH_MARKERS` 常量** — 防盗占位符标记列表（"正在手打中"等6个）
5. **`fetch_chapter_content()` 增加逐章防盗检测** — 章节内容为占位符且<200字时返回 `[ANTILEECH:marker]` 标记
6. **`crawl_chapters()` 新增 `truncated` 返回值** — 统计被防盗截断的章节数，进度日志含截断计数
7. **`validate_content_match()` 改为全文件扫描** — 书名/作者检查范围从2000字扩大到5000字；新增尾部5%污染检查
8. **新增 `validate_chapter_continuity()` 函数** — 扫描"第N章"编号连续性，报告缺失/重复章节
9. **`verify_output()` 集成三项新检查** — 污染扫描 + 章节连续性 + 全文读取（一次读取做所有检查）
10. **`_print_result()` 三级质量状态** — `success`/`success_with_warnings`/`poor_quality`，JSON 新增 `chapters_truncated`/`chapters_missing`/`contamination_found`/`chapter_range` 字段
11. **新增 3 个直链源**：知轩藏书(zxcs.click)、下书网(xiashuyun.com)、奇书网(qisuwang.com)

**实测验证：** 80ge源《玄鉴仙族》6.6M文件，检测到7处污染（5处在96-100%尾部，1处在67%章内注入），自动截断尾部251KB（3.8%），章内注入保留并标记warning。章节连续性检测到37章缺失+8章重复。

## v7.1.0 (2026-07-22)

### SKILL.md按设计规范重写

- frontmatter补触发条件（'下载小说''搜索网文'时启用）
- 红线重构为4条（首条为读取协议/强弱加载规则）
- 速查表从合格/不合格对照表改为文件目录引导（文件+读取时机+核心内容）
- 版本历史只留最新一条，其余移至CHANGELOG
- 新增强弱加载保障声明（SOP骨架区块）
- 业务方法论不变，只改结构/格式/规范
- skill.json版本号7.0.0→7.1.0

---

> 历史版本条目已归档：`_archive/changelog-history/tool-download-webnovel/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
