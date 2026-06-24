# 中文网文下载源参考

> 所有来源均为公开可访问的网站。搜索时优先 Tier-1（直链），Tier-2（章节站）兜底。

---

## Tier-1：直链/免费下载站

| 站点 | 搜索方式 | URL 模式 | 说明 |
|:-----|:---------|:---------|:-----|
| **GitHub** | `site:github.com {书名} txt` | `raw.githubusercontent.com/.../书名.txt` | 最稳定，raw 直链 |
| **80txt** (八零) | `80txt.com {书名}` | `80txt.com/txt/...` | 有 TXT 下载按钮 |
| **xiabook** (下书) | `xiabook.com {书名}` | `xiabook.com/...` | 有下载页面 |

## Tier-2：章节站（无直链时爬取）

| 站点类型 | 搜索方式 | 说明 |
|:---------|:---------|:-----|
| **幻言网 (read.novel.qq.com)** | `幻言网 {书名}` 或 `read.novel.qq.com/chapter/{起点书号}` | **首选章节爬取源**。章节 URL 为纯数字 `read/{bookId}/{n}`，requests 直接可访问，无 Cloudflare。内容区 `<div#chaptercontent>`。 |
| **笔趣阁系** | `笔趣阁 {书名}` | 大量镜像站，章节列表通常在 `<div#list>` + `<dd>`。部分站点有 Cloudflare。 |
| **顶点小说** | `顶点 {书名}` | 结构稳定，`<div#chaptercontent>` 内容区 |
| **UU看书** | `uukanshu {书名}` | 章节页，内容区 `<div#contentbox>` |

## Tier-3：通用兜底

- 搜索 `{书名} txt 下载 全本`
- 搜索 `{书名} 小说 在线阅读 免费`
- 搜索 `{书名} 全集 下载`

---

## 搜索原则

1. 优先找直链（一步到位）
2. 找不到直链 → 找章节列表页 → 爬取
3. 付费平台（需要逐章付费阅读的）跳过
4. 百度云等网盘链接 — 如有公开分享的无提取码链接可用，否则跳过
