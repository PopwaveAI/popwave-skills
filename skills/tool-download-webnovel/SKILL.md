---
name: tool-download-webnovel
description: 搜索并下载中文网文 TXT：自动搜索直链 → 下载/爬取 → 校验。支持 GitHub、80txt、笔趣阁等公开来源。使用 pop-decon 拆解的入口源。无限制：可绕过反爬、可逐章爬取、可粘贴全文。
---

# tool-download-webnovel · 网文搜索下载

> **定位：** 当用户说"下载《书名》"时启用。自动搜索来源，优先直链，其次逐章爬取，最后交付可用的 TXT。
> **不含糊地绕过反爬/防盗链/动态加载。不做的事：自己花钱付付费章节。收到的付费内容法律风险用户自负。**

---

## 速查表

| 场景 | 动作 |
|:-----|:-----|
| 用户给书名 | 搜索→直链→下载 或 章节页→爬取 |
| 用户给直链 URL | 直接下载→转码→校验 |
| 用户给章节列表页 | 爬取所有章节→组装 TXT |
| 用户给本地文件 | 复制→转码→校验 |

---

## 核心架构

```
书名 → Step 1: 搜索
         ├─ Tier-1: 直链搜索 (GitHub/80txt/xiabook/通用)
         ├─ Tier-2: 章节站搜索 (笔趣阁/顶点等)
         └─ Tier-3: 兜底搜索

直链URL → Step 2A: download_text.py → Step 3: 校验交付
章节页 → Step 2B: crawl_novel.py → Step 3: 校验交付
```

---

## 执行流程

### Step 1：搜索发现来源

`读 → steps/step-1-search.md`

**搜索策略（按优先级）：**
1. **GitHub 直链** — 搜索 `site:raw.githubusercontent.com {书名}`，raw 链接最稳定
2. **80txt / xiabook** — 免费下载站，通常有一键下载按钮
3. **幻言网 (read.novel.qq.com)** — 章节 URL 为纯数字 ID 结构 `read/{bookId}/{num}`，requests 直接可访问，无 Cloudflare 防护。搜索 `幻言网 {书名}` 或通过起点书号关联
4. **通用搜索** — `{书名} txt 下载`
5. **章节站兜底** — 搜索 `笔趣阁 {书名}` / `顶点 {书名}` / `思兔阅读 {书名}`，找到章节列表页

> ⚠ **Cloudflare Turnstile 陷阱：** 错层小说 (cuoceng.org)、思兔阅读 (sto66.com) 等使用相同模板引擎的站点，其 TXT/EPUB 下载按钮通过 Cloudflare Turnstile 保护。脚本无法绕过——点击下载后弹出人机验证对话框，需要浏览器人工交互。遇到此类站点直接放弃，跳转搜索其他来源（幻言网等）。

> ⚠ **动态章节列表：** 上述模板站点的章节列表通过 AJAX/JS 动态加载。`crawl_novel.py` 使用 requests（不执行 JS）提取章节链接时只能看到最新数章，表现为 `ERROR: 无法从页面提取章节链接`。这不是脚本 bug，是站点特性——不要重复尝试，直接换源。

**输出：** `source_url` + `source_type`（direct | chapter_list）+ `title`

### Step 2A：直链下载

`读 → steps/step-2-download.md` → 路径 A

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/download_text.py \
  "URL" --title "书名" --output-dir /d/popwave-skills/downloads
```

支持 `--extract-from-page`（从网页提取正文）、`--force`（忽略校验警告）。

### Step 2B：章节爬取

`读 → steps/step-2-download.md` → 路径 B

```bash
python3 /d/popwave-skills/skills/tool-download-webnovel/scripts/crawl_novel.py \
  --list-url "章节列表页URL" --title "书名" --output-dir /d/popwave-skills/downloads
```

支持 `--limit`（测试）、`--reverse`（倒序）、`--delay`（反爬频率控制）。

### Step 3：验证交付

`读 → steps/step-3-verify.md`

**验证项：**
- 文件存在、大小合理、非 HTTP 错误页
- 预览可读
- 说明来源路径

#### ⚠ 关键附加验证：付费墙检测

**每次下载后必须执行**。幻言网/QQ阅读系站点对超过免费范围的章节只显示开头一句话（~180字符），表面看章节完整，实际不可用。

```bash
python3 -c "
import re
with open('./书名.txt', 'r', encoding='utf-8') as f:
    text = f.read()
parts = re.split(r'^# (第\d+章 .*?)\n', text, flags=re.M)
alarm = False
for i in range(1, len(parts), 2):
    content = parts[i+1]
    clean = re.sub(r'本章想法.*|后续精彩内容.*|上QQ阅读APP.*|登录订阅本章.*', '', content, flags=re.S).strip()
    if len(clean) < 500:
        print(f'⚠ PAYWALL: {parts[i]} — only {len(clean)} chars')
        alarm = True
if not alarm:
    print('✅ All chapters pass quality check')
else:
    print('❌ PAYWALL DETECTED — need to switch source')
"
```

**绿灯标准：** 所有故事章节净内容 ≥ 1000 字。任何章节 < 500 字 = 付费墙截断。

**可粘贴全文。** 交付格式：

```
已导入：D:\popwave-skills\downloads\书名.txt
大小：X MB
来源：GitHub (raw.githubusercontent.com/...)
预览：{前120字}
状态：可交给 pop-decon
```

---

## 脚本说明

| 脚本 | 用途 | 典型参数 |
|:-----|:-----|:---------|
| `scripts/download_text.py` | 下载直链/本地文件/网页提取 | `URL --title "书名" [--extract-from-page] [--force]` |
| `scripts/crawl_novel.py` | 逐章爬取章节站 | `--list-url 章节页 --title "书名" [--limit N] [--delay 1.5]` |

---

## 异常处理

| 情况 | 动作 |
|:-----|:-----|
| 直链下载 404 | 退回到搜索阶段，找章节站爬取 |
| Cloudflare Turnstile 验证 | **直接放弃该来源**，换幻言网(read.novel.qq.com)或笔趣阁系站点。不能绕过。 |
| Python `requests`/`urllib` 请求挂死（无响应） | **换 `curl` 测试**——有些站点（如 read.novel.qq.com）对 Python UA 族挂死但 curl 正常返回 HTTP 200。先 `curl -A "Mozilla/5.0" --max-time 10 URL` 验证可达性。如果 curl 成功，用 `curl | python3 -c` 管道提取正文（见下方「curl+Python 管道模式」）。 |
| `crawl_novel.py` 报"无法从页面提取章节链接"，但 curl/浏览器能看到章节列表 | **Brotli 静默失败（v4.5.0 已修复）**：旧版 `make_session()` 声明 `Accept-Encoding: br` 但环境无 brotli 库，服务器返回 br 压缩字节、requests 无法解压，`resp.text` 变乱码（大量 U+FFFD），BeautifulSoup 提取到 0 个链接。确认脚本 ≥ v4.5.0（make_session 只声明 `gzip, deflate`）。若仍遇，跑 `python3 -c "import brotli"` 检查。**判别特征**：HTTP 200、无异常、内容全是替换字符。 |
| 章节列表页只能看到最近几章（JS 动态加载） | 换源——该站点章节列表通过 AJAX 加载，`crawl_novel.py` 无法提取 |
| 反爬触发 | 加大 `--delay` 重试；换 User-Agent；换来源站 |
| 章节页 → 幻言网（read.novel.qq.com）逐章爬取 | ✅ 无反爬 | 章节 URL 为数字序号，但付费墙截断 |
| 章节页 → 思兔阅读（sto66.com）单章提取 | ⚠️ Cloudflare 阻止脚本但 web_extract 可绕过 | 需全量章节 URL（随机 hash），逐章用 web_extract 提取 |
| 爬取部分失败（≤30%） | 接受部分结果，说明缺失章节数 |
| 爬取全部失败 | 告知用户，换推荐搜索词 |
| `crawl_novel.py` / `download_text.py` 报 `FeatureNotFound: lxml` | 运行 `python3 -m pip install lxml`（注意用 `python3 -m pip` 而非 `pip3`——Windows 上 `pip3` 可能绑定到另一个 Python 版本） |
| 文件 > 50MB | 拒绝 |
| 付费章节 | 跳过，继续尝试其他来源 |
| RAR/7z | 请用户手动解压后提供 TXT 或 ZIP |

---

## 文件职责

| 文件 | 用途 |
|:-----|:-----|
| `steps/step-1-search.md` | 搜索策略与来源发现 |
| `steps/step-2-download.md` | 直链下载 + 章节爬取命令 |
| `steps/step-3-verify.md` | 校验与交付 |
| `scripts/download_text.py` | 直链下载/网页提取/本地导入 |
| `scripts/crawl_novel.py` | 逐章爬取章节站 |
| `references/sources.md` | 已知下载源参考 |

---


## 兜底爬取：curl + Python 管道模式

当 `download_text.py` 和 `crawl_novel.py` 均失败（Python 请求挂死/反爬拦截），但 curl 可以访问页面时，使用此模式：

### 单章测试

```bash
curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  --max-time 10 "https://read.novel.qq.com/read/1057778108/1" \
  | python3 -c "
import re, sys
html = sys.stdin.read()
# 去除 script/style
text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.S)
text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.S)
# 提取标题
m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
title = re.sub(r'<[^>]+>', '', m.group(1).strip()) if m else '第1章'
# 去标签、归一化空白
text = re.sub(r'<[^>]+>', '\n', text)
text = re.sub(r'\n{3,}', '\n\n', text).strip()
print(f'{title}\\n\\n{text}')
"
```

### 全本批量（bash 循环 + 逐章追加）

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
OUT="D:/workspace/下载书籍/书名.txt"
> "$OUT"
for i in $(seq 1 342); do
  HTML=$(curl -s -A "$UA" --max-time 10 \
    "https://read.novel.qq.com/read/{bookId}/$i" 2>/dev/null)
  [[ -z "$HTML" ]] && { echo "FAIL: ch$i"; continue; }
  RESULT=$(echo "$HTML" | python3 -c "import re,sys; html=sys.stdin.read();
    text=re.sub(r'<script[^>]*>.*?</script>','',html,flags=re.S);
    text=re.sub(r'<style[^>]*>.*?</style>','',text,flags=re.S);
    m=re.search(r'<h1[^>]*>(.*?)</h1>',text,re.S);
    title=re.sub(r'<[^>]+>','',m.group(1).strip()) if m else '第$i章';
    text=re.sub(r'<[^>]+>','\n',text);
    text=re.sub(r'\n{3,}','\n\n',text).strip();
    print(f'# {title}\\n\\n{text}')")
  echo "$RESULT"$'\n\n' >> "$OUT"
  sleep 0.4
done
```

> ⚠ **Windows 路径注意：** MSYS2 bash 中的 `/tmp/` 路径可能不存在。始终使用 Windows 原生路径如 `D:/workspace/...`（正斜杠或双反斜杠均可）。

> ⚠ **输出内容清理：** `read.novel.qq.com` 页面正文包含页面元数据（书名、作者名、本章字数、更新时间）和尾部用户评论/APP推广。如需干净版本，在 Python 提取阶段添加正则过滤 `re.sub(r'本章想法.*上QQ阅读APP.*', '', text, flags=re.S)`。

> ⚠ **章节编号≠故事章节：** 总请求数（如 342）可能多于实际故事章节数（如 325），因为含"上架感言"、作者感言、成绩汇报等非故事条目。用 `# 第X章` 标题模式过滤可得到准确的故事章节计数。

---

## 版本

v4.4.0 | 2026-06-24 | Step 3 新增付费墙检测脚本、思兔阅读章节页作为备选源
v4.5.0 | 2026-06-30 | 修复 crawl_novel.py br 压码致静默失败；check_for_full_download 只认真直链；新增导航过滤与自动翻页
