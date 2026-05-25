---
name: download-webnovel-txt
description: 输入书名即可自动搜索、下载网文并保存为干净 TXT。支持公开页面、用户提供的URL、登录态、本地HTML导出、目录页。无需用户指定来源。
---

# Download Webnovel TXT (Trae Edition)

## 概述

用户只需提供书名（可选作者），系统自动完成：搜索源 → 选最佳源 → 下载全部章节 → 质量验证 → 交付干净 TXT。

**LLM 负责**：用 WebSearch 搜源、WebFetch 探测、决策选哪个源、生成章节 URL 列表。
**脚本负责**：批量下载章节、编码处理、TXT 清洗、质量报告。

## 工作流

### Step 1: 搜索源

用 `WebSearch` 搜 3-4 个 query：

```
"{书名} txt 下载 全本"
"{书名} 小说 目录"
"{书名} {作者}"  (如果知道作者)
"site:69shuba.com {书名}"
```

从搜索结果中提取候选 URL，优先级：
- ixdzs8.com/read/ → 92 分
- 69shuba.com/book/ → 90 分
- zxcs.info → 85 分（如果是zip）
- 其他小说站 → 70-80 分

### Step 2: 探测最佳源

对 Top 3 候选用 `WebFetch` 抓首页，判断：
- 是 **目录页(TOC)**？提取总章数
- 是 **全本 TXT 下载页**？直接拿到下载链接
- 是 **单章页**？找目录入口
- 挂了/要登录/云防护？跳过

### Step 3: 生成章节 URL 列表

- **TOC 型源**：用脚本自动提取 `--extract-chapter-links-auto-from`
- **连续编号型**：手动生成 URL 模板 `https://xxx/book/N/p{M}.html`
- **直链 TXT/ZIP**：直接 `--download-file-from` 或 `--extract-zip`

### Step 4: 批量下载

```bash
python3 scripts/download_novel.py \
  --urls-file chapter_urls.txt \
  --output "书名.txt" \
  --title "书名" \
  --delay 0.6 --delay-jitter 0.3 \
  --retries 3 --timeout 30 \
  --flush-each \
  --failure-output failed.txt \
  --stop-after-consecutive-failures 30 \
  --dedupe-adjacent-lines
```

### Step 5: 质量验证

```bash
python3 scripts/download_novel.py \
  --quality-report "书名.txt" \
  --expected-sections N \
  --require-chapter-number-sequence \
  --required-term "主角名|关键地名" \
  --output quality.json
```

验收标准：
- `acceptance_status: pass`
- 所有 suspicious_counts 为 0 或有合理解释
- 首/中/尾章节抽样不是导航/占位/乱码

## 关键选项速查

| 选项 | 用途 |
|---|---|
| `--auto-title` | 全自动（需外网） |
| `--urls-file urls.txt` | 批量下载 |
| `--extract-chapter-links-auto-from URL` | 从目录页自动抽链 |
| `--generate-url-template` | 连续编号 URL |
| `--download-file-from URL` | 下载页直链 |
| `--extract-epub / --extract-zip` | EPUB/ZIP 提取 |
| `--merge-txt` | 多源合并 |
| `--quality-report` | 生成质量报告 |
| `--delay 0.6 --delay-jitter 0.3` | 反限速 |
| `--stop-after-consecutive-failures N` | 断连保护 |
| `--failure-output` | 失败日志 |
| `--require-chapter-number-sequence` | 序列完整性 |
| `--required-term` | 源漂移检测 |

## 网文站点知识库

| 站点 | URL 模式 | TOC | 特点 |
|---|---|---|---|
| 69书吧 | `69shuba.com/book/ID` | 需拿目录页 | 更新最快, 反爬严 |
| 爱下电子书 | `ixdzs8.com/read/ID` | `/read/ID/` | 连续 p{N}.html |
| 飞速中文 | `feisxs.com/book-ID` | 有全本目录 | 直链较多 |
| YBSWA | `ybswa.com` | TOC 页 | 需 selector |
| 文学城读书 | `wxc` 系列 | 目录页 | 稳定但容器特殊 |

## 常见坑

- **69书吧反爬**：Cloudflare 验证 → 换源
- **VIP 章节**：晋江等需要登录态，公开章节能拿多少拿多少
- **编码问题**：直链 TXT 常是 GB18030，用 `--input-encoding gb18030`
- **章内分页**：单章被拆 `_2.html` `_3.html`，用 `--page-link-regex`
- **源漂移**：镜像站 VIP 后用别的书填充 → `--required-term` 检测
- **书名别名**：搜索时注意 "幽冥仙途" vs "幽明仙途"
- **连载中**：标注 "当前已发布章节"，不要写"完结"

## 典型对话

用户："下载玄鉴仙族"

LLM:
1. WebSearch "玄鉴仙族 txt 下载 全本"
2. WebFetch ixdzs8.com/read/508570/ → 确认 1132 章, 季越人, 连载中
3. 生成 1132 个 URL: ixdzs8.com/read/508570/p1..p1132.html
4. 跑脚本下载
5. 跑质量报告 → complete 1132/1132 pass
6. 交付: "玄鉴仙族.txt, 1132章, 连载中(截至2025-04), 零噪声"
