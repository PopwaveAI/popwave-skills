---
name: tool-download-webnovel
description: 网文搜索下载。当用户说'下载小说''搜索网文'时启用。输入书名+作者→输出TXT文件。三阶段SOP：脚本搜索→web搜索兜底→验证交付。
---
# tool-download-webnovel
> 网文搜索下载TXT v7.1.0。三阶段SOP：脚本搜索→web搜索兜底→验证交付。

## 做什么
| 输入 | 输出 | 下游 |
|------|------|------|
| 书名+作者(可选) | TXT文件+JSON状态 | pop-decon(拆书管线第一步) |

默认排除付费墙正版网站（起点/晋江/纵横等）。

## 怎么操作（SOP骨架）
> execution.mode: 顺序执行Phase 1→2→3，Phase 1失败后强制进入Phase 2。
> 强加载：红线+速查表（每轮必读）；弱加载：scripts按需调用。

### Phase 1: 脚本自动搜索
- 执行 `python3 scripts/download_novel.py "书名" --author "作者" --output-dir downloads`
- status=success → 检查preview/warnings → 交付；status=error → **进入Phase 2**

### Phase 2: Agent Web搜索（Phase 1失败后强制）
- 至少尝试3组关键词：`{书名} {作者} 笔趣阁` / `{书名} txt 下载` / `{书名别名}`
- 找到章节列表页或直链后用 `--source-url` 传入脚本重新下载

### Phase 3: 验证与交付
- 检查JSON：status=success + chapters_failed=0 + warnings=[] → 交付
- chapters_failed>0 → `--resume` 补爬；warnings含内容校验 → 检查preview正文

## 红线
1. **读取协议**：强加载=红线+速查表（每轮必读）；弱加载=scripts按需调用。Phase 1失败后必须加载Phase 2指令。
2. **Phase 1失败后直接放弃** — 必须执行Phase 2 web搜索，至少尝试3组关键词
3. **搜索/使用付费墙正版站** — 起点/晋江/纵横等，`--source-url`传入会被自动拦截
4. **下载后不检查preview和warnings** — 确认内容正确再交付

## 速查表
| 文件 | 读取时机 | 核心内容 |
|------|----------|----------|
| SKILL.md | 每轮必读 | 红线+SOP骨架+速查表 |
| scripts/download_novel.py | 执行下载时 | 统一入口：搜索→验证→爬取→校验→交付 |
| scripts/batch_download.py | 批量下载时 | 从JSON书单批量下载，支持--resume/--retry-failed |
| scripts/crawl_novel.py | 章节站爬取时 | 逐章爬取引擎（自动检测章节链接+正文） |
| scripts/download_text.py | 直链下载时 | URL/本地文件导入+ZIP解压+UTF-8规范化 |

## 参数速查
| 参数 | 默认 | 说明 |
|------|------|------|
| --author | None | 作者名（文件名+搜索验证） |
| --source-url | None | 跳过搜索直接用此URL |
| --direct | off | 源URL为直链TXT/ZIP |
| --reverse | off | 反转章节顺序 |
| --resume | off | 断点续爬 |
| --limit N | 0 | 只爬前N章（测试用） |
| --content-selector | auto | 手动指定正文CSS选择器 |
| --include-paywall | off | 允许付费墙网站（默认排除） |

## 版本
v7.1.0 | 2026-07-22 | SKILL.md按设计规范重写：frontmatter补触发条件、红线重构为4条(首条读取协议)、速查表改为文件目录引导、版本历史移至CHANGELOG。
