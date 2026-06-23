# Step 2：下载并转码（直链 / 爬取双路径）

> **读什么：** Step 1 输出的 `source_url`、`source_type`、`title`。  
> **产出什么：** UTF-8 TXT 文件路径。

---

## 路径 A：直链下载（source_type = "direct"）

### 通用命令

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/download_text.py \
  "URL" --title "书名" \
  --output-dir /d/popwave-skills/downloads
```

短篇/样章降低阈值：
```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/download_text.py \
  "URL" --title "书名" \
  --output-dir /d/popwave-skills/downloads \
  --min-bytes 2048
```

强制保存（忽略小文件/内容警告）：
```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/download_text.py \
  "URL" --title "书名" \
  --output-dir /d/popwave-skills/downloads \
  --force
```

### 从页面提取文本（不是直接 TXT 下载链接时）

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/download_text.py \
  "URL" --title "书名" \
  --output-dir /d/popwave-skills/downloads \
  --extract-from-page
```

> `--extract-from-page` 会用 requests+BeautifulSoup 提取页面的可见文本，去掉导航/脚注等无关内容。

---

## 路径 B：逐章爬取（source_type = "chapter_list"）

当只有章节列表页（笔趣阁、顶点等）但没有直链时，用爬虫脚本自动抓取全文。

### 基本爬取

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/crawl_novel.py \
  --list-url "章节列表页URL" \
  --title "书名" \
  --output-dir /d/popwave-skills/downloads
```

### 快速测试（只爬前 5 章看效果）

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/crawl_novel.py \
  --list-url "章节列表页URL" \
  --title "书名" \
  --limit 5
```

### 如果章节顺序反了（网站最新的在前）

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/crawl_novel.py \
  --list-url "..." --title "书名" \
  --reverse
```

### 自定义内容选择器（脚本自动检测失败时）

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/crawl_novel.py \
  --list-url "..." --title "书名" \
  --chapter-selector "a.chapter" \
  --content-selector "div#chaptercontent"
```

### 降低请求频率（反爬严格站）

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/crawl_novel.py \
  --list-url "..." --title "书名" \
  --delay 2.5
```

### 自动降级：脚本发现"全本TXT下载"链接时

crawl_novel.py 会自动检测页面上的全本下载链接。如果找到：
- 输出 `FULL_DOWNLOAD=URL`
- 退出码 0
- 此时应该把 URL 传给 download_text.py 重新走**路径 A**

---

## 门禁

| 场景 | 动作 |
|:-----|:-----|
| 直链下载成功 | 进入 Step 3 验证 |
| 直链 404/失败 | 回退到 Tier-2，找章节列表页用路径 B |
| 爬取成功（部分章节失败可接受） | 进入 Step 3 验证 |
| 爬取全部失败 | 说明原因；建议换来源 |
| 爬取中触发反爬 | 加大 `--delay` 重新尝试 |
| 文件 > 50MB | 拒绝下载 |

---

## 脚本输出格式

```
output=D:\popwave-skills\downloads\书名.txt
encoding=utf-8
bytes=1234567
preview=第一章...
chapters_crawled=352
chapters_failed=3
```
