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
3. **通用搜索** — `{书名} txt 下载`
4. **章节站兜底** — 搜索 `笔趣阁 {书名}` / `顶点 {书名}`，找到章节列表页

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
| 反爬触发 | 加大 `--delay` 重试；换 User-Agent；换来源站 |
| 爬取部分失败（≤30%） | 接受部分结果，说明缺失章节数 |
| 爬取全部失败 | 告知用户，换推荐搜索词 |
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

## 版本

v4.1.0 | 2026-06-23 | 解除全部限制：可绕过反爬、可逐章爬取、可粘贴全文 → [CHANGELOG.md](CHANGELOG.md)
