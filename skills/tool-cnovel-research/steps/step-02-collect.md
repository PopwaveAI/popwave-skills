# Step 2: 工具选择 + 数据采集

## 输入
第一步产出的调研计划。

## 执行
按决策树选择采集工具。

### 工具选择决策树
```
用户发起调研请求
├─ 是多平台扫描吗？
│   ├─ 是 → 用 AnySearch batch_search + site: 同时扫 3-5 个平台
│   └─ 否 → 查"平台能力矩阵"表
│
├─ 目标平台正文拿得到吗？
│   ├─ ✅ → 优先用平台专用工具（aiotieba / crawl4weibo / B站API）
│   ├─ ⚠️ → AnySearch site: 扫标题 + 交互动作让用户粘贴正文
│   └─ ❌ → 查"人工兜底方案"，指导用户操作
│
├─ 需要帖子/视频详情内容（非仅标题）？
│   ├─ 是 + B站 → B站评论 API（免登录）
│   ├─ 是 + 贴吧 → aiotieba get_posts（需 HTTP 补丁）
│   ├─ 是 + 龙空 → AnySearch extract（部分可提取）
│   ├─ 是 + 微博 → crawl4weibo 含评论模式
│   └─ 是 + 豆瓣/阅文/小红书/公众号 → 走人工兜底
│
└─ 被反爬拦截了？
    ├─ 换个 User-Agent
    ├─ 换 HTTP→HTTPS 或反过来
    ├─ 加 Referer/Origin
    └─ 还不通 → 正文拿不到 → 启动人工兜底
```

### 各平台专用工具调用

```bash
# AnySearch 通用
python scripts/anysearch/scripts/anysearch_cli.py search "<query>" --max_results 20
python scripts/anysearch/scripts/anysearch_cli.py batch_search --query "site:xxx.com AI写作" --query "site:yyy.com 网文AI"
python scripts/anysearch/scripts/anysearch_cli.py extract "https://example.com/article"

# B站 API
GET https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=<关键词>&page=<页码>
GET https://api.bilibili.com/x/v2/reply/main?oid=<aid>&type=1&mode=3&next=<页码>

# 晋江碧水
https://bbs.jjwxc.net/board.php?board=17&page=<页码>
（提取表格 <table class="olt"> 中帖子）
```

### Python 调用
```python
# aiotieba（贴吧）
import aiotieba
async with aiotieba.Client() as client:
    threads = await client.get_threads("小说", pn=1, rn=50)
    posts = await client.get_posts(tid, pn=1, rn=30)

# crawl4weibo（微博）
from crawl4weibo import WeiboClient
client = WeiboClient()
result = client.search_posts("AI写小说", page=1)
```

## 门禁
- [ ] 每个平台采集结果 >= 10 条内容（或全量）
- [ ] 低可采集平台已向用户发出人工粘贴请求

## 产出
各平台原始数据（结构化 JSON / 文本 / 用户粘贴内容）。

## 人工兜底方案

适用于：豆瓣、阅文、小红书、微信公众号、抖音、视频号（需要登录态/Cookie 的平台）。

1. **AI 用 AnySearch site: 搜索扫标题** — 找出该平台有哪些相关帖子/笔记
2. **AI 选出 10-30 篇高价值内容** — 优先选高互动、标题直接命中的
3. **AI 告知用户需要人工操作**
4. **用户发来内容后** — 跟自动化采集数据一样处理
