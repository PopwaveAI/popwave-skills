---
name: cnovel-research
description: 网文作者社区用户调研专用技能。整合 AnySearch 搜索引擎 + 各平台 API + 绕过策略，覆盖龙空/晋江/阅文/贴吧/知乎/豆瓣/微博/B站/小红书/抖音/微信公众号/视频号等 12+ 平台。对高可采集平台全自动出报告；对低可采集平台提供标准人工兜底流程。
version: 1.1.0
---

# 网文作者社区用户调研技能

## 概述

基于 2026-05 对 8 个网文作者社区的全量调研实战经验沉淀。整合了 AnySearch 通用搜索引擎 + 各平台专用 API/爬虫工具 + 平台反爬策略 + 高效关键词库。

本技能用于：当需要调研「网文作者对 XXX 的态度」「XXX 工具在网文圈的讨论」「网文行业 YYY 趋势」等话题时，自动选择最优采集路径。

## 能力范围

| 平台 | 自动化 | 最佳路径 | 自动化拿得到正文吗 | 正文拿不到怎么办 |
|:---|:---:|:---|:---:|:---|
| **龙空 lkong.com** | ✅ 高 | AnySearch site: 搜索 + extract | ⚠️ 部分 | 用户粘贴 |
| **晋江碧水 bbs.jjwxc.net** | ✅ 高 | HTTP 直接抓取列表页 | ✅ 可 | — |
| **贴吧 tieba.baidu.com** | ✅ 高 | `aiotieba` protobuf API | ✅ 可 | — |
| **知乎 zhihu.com** | ✅ 中 | AnySearch site: 搜索 + WebFetch | ✅ 可 | — |
| **B站 bilibili.com** | ✅ 高 | B站搜索 API + 评论 API | ✅ 可 | — |
| **微博 weibo.com** | ✅ 高 | `crawl4weibo` 库 | ✅ 可 | — |
| **豆瓣 douban.com** | ⚠️ 低 | AnySearch site: 搜索列表页 | ❌ 403 | **人工粘贴** |
| **阅文 write.qq.com** | ⚠️ 低 | 问答搜索 API（免登录） | ❌ 需登录 | **人工粘贴** |
| **小红书 xiaohongshu.com** | ⚠️ 低 | AnySearch site: 搜索 | ❌ 需 Cookie | **人工粘贴** |
| **抖音 douyin.com** | ❌ 极低 | 不推荐自动化 | ❌ | **人工粘贴或跳过** |
| **微信公众号 mp.weixin.qq.com** | ⚠️ 低 | AnySearch site: 搜索 | ❌ 需账号 | **人工粘贴（推荐搜狗微信搜索辅助定位）** |
| **微信视频号 channels.weixin.qq.com** | ❌ 不可 | 无 | ❌ | **人工粘贴或跳过** |

### 怎么读这张表

- **自动化 ✅ 且正文 ✅**（6 个平台）：全自动跑，AI 可以独立完成采集+报告
- **自动化 ✅ 但正文 ⚠️**（1 个平台，龙空）：能搜到，但 extract 不稳定，需要用户配合贴内容
- **只有列表、没正文**（4 个平台：豆瓣/阅文/小红书/公众号）：必须先让用户手动粘贴，AI 才能出报告
- **完全不可自动化**（2 个平台：抖音/视频号）：跳过，或让用户手动搜索+粘贴

---

## 工具选择决策树

```
用户发起调研请求
├─ 是多平台扫描吗？
│   ├─ 是 → 用 AnySearch batch_search + site: 同时扫 3-5 个平台
│   └─ 否 → 查「能力范围」表
│
├─ 目标平台正文拿得到吗？
│   ├─ ✅ → 优先用平台专用工具（aiotieba / crawl4weibo / B站API）
│   ├─ ⚠️ → AnySearch site: 扫标题 + 交互动作让用户粘贴正文
│   └─ ❌ → 查「人工兜底方案」表，指导用户操作
│
├─ 需要帖子/视频详情内容（非仅标题）？
│   ├─ 是 + B站 → B站评论 API (免登录)
│   ├─ 是 + 贴吧 → aiotieba get_posts (需源码打 HTTP 补丁)
│   ├─ 是 + 龙空 → AnySearch extract (部分可提取)
│   ├─ 是 + 微博 → crawl4weibo 含评论模式
│   └─ 是 + 豆瓣/阅文/小红书/公众号 → 走「人工兜底方案」
│
└─ 被反爬拦截了？
    ├─ 换个 User-Agent
    ├─ 换 HTTP→HTTPS 或反过来
    ├─ 加 Referer/Origin
    └─ 还不通 → 查「能力范围」表：正文拿不到 → 启动「人工兜底方案」
```

---

## 各平台专用工具清单

### 1. AnySearch (通用搜索引擎 + 站点提取)

**安装**：见 AnySearch Skill 文档
**调用方式**：
```bash
python tools/anysearch/scripts/anysearch_cli.py search "<query>" --max_results 20
python tools/anysearch/scripts/anysearch_cli.py batch_search --query "site:xxx.com AI写作" --query "site:yyy.com 网文AI"
python tools/anysearch/scripts/anysearch_cli.py extract "https://example.com/article"
```

**适用场景**：
- 多平台并行扫描（batch_search 一次覆盖 5 个平台）
- 补充被反爬的平台（豆瓣、小红书、阅文）的列表页数据
- 提取 B站专栏等可提取页面的全文

**注意**：`extract` 对需要 Cookie 的平台（豆瓣、阅文）返回空或 403。

### 2. aiotieba (贴吧专用，免登录)

**安装**：`pip install aiotieba --break-system-packages`
**关键补丁**：必须将 `get_posts/_api.py` 中 `scheme="https"` 改为 `scheme="http"`
**调用方式**：
```python
import aiotieba
async with aiotieba.Client() as client:
    threads = await client.get_threads("小说", pn=1, rn=50)  # 帖子列表
    posts = await client.get_posts(tid, pn=1, rn=30)  # 回复
```

### 3. crawl4weibo (微博专用)

**安装**：`pip install crawl4weibo --break-system-packages`
**特性**：自动获取 Cookie，无需手动配置
**调用方式**：
```python
from crawl4weibo import WeiboClient
client = WeiboClient()
result = client.search_posts("AI写小说", page=1)
posts, has_more = result
```

### 4. B站 API (免登录)

**搜索视频**：
```
GET https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword=<关键词>&page=<页码>
```
**获取评论**：
```
GET https://api.bilibili.com/x/v2/reply/main?oid=<aid>&type=1&mode=3&next=<页码>
```
**补全播放数据**：
```
GET https://api.bilibili.com/x/web-interface/view?bvid=<bvid>
```

### 5. 晋江碧水 (免登录)

直接 HTTP 抓取：
```
https://bbs.jjwxc.net/board.php?board=17&page=<页码>
```
筛选规则：提取表格 `<table class="olt">` 中的帖子列表，按标题关键词过滤。

---

## AI写作调研关键词库

### 一级关键词（高信噪比，直接命中 AI 写作讨论）
```
AI写小说, AI写作, 网文AI, AI辅助写作, AI润色, DeepSeek写作,
AI生成小说, AI网文, ChatGPT写小说, 豆包写作, AI小说,
番茄AI, 起点AI, 鉴AI, 去AI味, AI文
```

### 二级关键词（扩展覆盖，可能包含非写作 AI 内容）
```
AI工具, AI大模型, 人工智能写作, 智能写作, AIGC, LLM, 
prompt, 提示词, 大模型写作, deepseek, kimi, claude,
星月写作, 笔灵AI, 蛙蛙写作, 风月AI
```

### 平台专属补充关键词
| 平台 | 补充关键词 | 原因 |
|:---|:---|:---|
| 晋江 | 文心智能体, AI小美, 盗文, 被鉴AI, 朱雀 | 文心盗文是晋江独特痛点 |
| 豆瓣 | 抄袭, 拼尸块, 喂AI, 马甲 | 豆瓣偏文学伦理讨论 |
| 贴吧 | 验证期, 零流量, 签约, 卖身契 | 番茄实战讨论多 |
| B站 | 打假, 避雷, 纪录片, 翻车 | B站负面向内容流量高 |
| 微博 | 月入过万, 暴富, 割韭菜, 卖课 | 微博暴富叙事浓 |

---

## 踩过的坑和解决方案

### 坑 1：贴吧 get_posts 超时
**原因**：aiotieba 默认走 HTTPS，在此服务器上 HTTPS 极慢
**解决**：改源码 `/usr/local/lib/python3.10/dist-packages/aiotieba/api/get_posts/_api.py`，`scheme="https"` → `scheme="http"`

### 坑 2：豆瓣小组详情页 403
**原因**：豆瓣反爬 + 需要登录态
**解决**：用 AnySearch `site:douban.com/group` 搜列表页标题 + 摘要；详情内容需用户手动保存

### 坑 3：阅文 write.qq.com 搜索 API 返回有限
**原因**：阅文 API 免登录可搜标题，但详情页需认证
**解决**：用搜索 API 拿到帖子列表（标题+回复数），配合 AnySearch site 搜索补全

### 坑 4：小红书 extract 返回空
**原因**：小红书需 Cookie + 动态渲染
**解决**：用 AnySearch site 搜索拿到笔记标题和部分摘要；正文仍需用户手动

### 坑 5：抖音搜索返回 code 2483 需登录
**原因**：抖音搜索 API 严格限流 + 需 Cookie
**解决**：放弃。如需抖音数据，建议用户手动搜索后粘贴

### 坑 6：B站搜索 API 有时返回空
**原因**：频率限制
**解决**：加 0.3-1s 延迟；换个 User-Agent；分批次请求

---

## 人工兜底方案：当自动化拿不到正文时

**适用于**：豆瓣、阅文、小红书、微信公众号、抖音、视频号等需要登录态或 Cookie 的平台。

### 标准操作流程

代理（AI）执行：

1. **用 AnySearch site: 搜索扫标题** — 找出该平台有哪些 AI 相关的帖子/笔记，拿到标题、链接、互动数（评论数/点赞数）。这一步不需要人工参与。
2. **选出 10-30 篇需要深度阅读的内容** — 优先选高互动、标题里直接命中的。把链接列出来。
3. **告诉用户需要人工操作** — 用以下话术：

> 自动抓取被拦了（需要登录态/Cookie），但我已经用搜索引擎找到了 [X] 个相关帖子。你可以帮我打开下面的链接，各 Command+S（或 Ctrl+S）保存页面，或者直接复制粘贴帖子正文给我。发完了告诉我。

4. **用户发来粘贴内容后** — 跟自动化采集到的数据一样处理：提取引用、分类人群、输出报告。

### 各平台人工操作指南

| 平台 | 如何打开 | 如何保存 | 注意 |
|:---|:---|:---|:---|
| **豆瓣小组** | 浏览器打开帖子链接 | `Ctrl+S` / `Cmd+S` 保存完整 HTML，或直接复制页面文字粘贴 | 需要已登录豆瓣账号 |
| **阅文 write.qq.com** | 浏览器打开帖子链接 | 同上 | 需要已登录阅文/起点账号 |
| **小红书** | 手机 App 内打开更好 | 截图 + 复制文字，或 PC 端 `Cmd+S` | PC 端经常弹验证码，手机端更稳定 |
| **微信公众号** | 微信内打开文章 | 复制全文粘贴。或用搜狗微信搜索 (weixin.sogou.com) 定位文章后浏览器打开 | 搜狗微信搜索是定位公众号文章的最佳免费工具 |
| **抖音** | 手机 App | 看视频内容 + 复制评论区文字 | 抖音评论区复制有限，可截图让 AI 读取 |
| **微信视频号** | 微信内 | 只能手动浏览 + 口述总结给 AI | 视频号无公开链接 |

### 给自动化工具的提示：如何在搜狗微信搜索上定位公众号内容

```bash
# 搜狗微信搜索（免费、免登录）
python tools/anysearch/scripts/anysearch_cli.py search "site:mp.weixin.qq.com AI写作 网文" --max_results 10
# 或直接：
# https://weixin.sogou.com/weixin?type=2&query=AI写作+网文
```

注意：搜狗只能搜到近期公众号文章，更老的内容可能不索引。如果搜不到，说明该话题在公众号上讨论较少，跳过即可。

### 实操案例参考

本次调研中：
- **豆瓣**：先用 AnySearch 扫了 6 个写作小组的列表页标题，筛出 30+ 篇 AI 相关帖子。然后用户手动打开每篇、复制粘贴全部正文（含回复），AI 接收后出报告。
- **阅文**：用 write.qq.com 的问答搜索 API 扫到 41 篇 AI 相关帖子的标题+回复数。详情页全部由用户手动打开粘贴。
- **小红书/抖音/视频号**：因投入产出比放弃。

---

## 调研工作流模板

### 场景 A：全平台快速扫描（2-3小时）

1. **AnySearch batch_search** 扫全部 8 个平台 `site:`，每个平台 10 条结果
2. 用平台专用工具深入 Top 3 平台（按内容量和相关性选）
3. 整理关键引用 + 出简报

### 场景 B：单平台深度调研（4-6小时）

1. 查「能力范围」表确定最优路径
2. 如果是高可采集平台 → 用专用工具全量爬取（翻 5-10 页）
3. 对热帖/高评论内容 → 爬评论
4. 人工挑选高质量引用 + 出报告

### 场景 D：人工兜底模式（适用于低可采集平台）

1. **AI 先用 AnySearch site: 扫标题** — 输出帖子/笔记列表（含标题、链接、互动数）
2. **AI 挑 10-30 篇高价值内容** — 把链接发给用户
3. **用户手动打开 → 复制粘贴** — 每条帖子包含正文+回复
4. **AI 接收 → 像自动化数据一样处理** — 提取引用、分类人群、输出报告

### 场景 E：竞品工具调研

重点关注平台的"用什么AI写文"类讨论：
- 知乎 > "写小说，哪个Ai好用?"
- B站 > 工具对比/横评类视频评论
- 微博 > "AI工具清单"类博文
- 豆瓣 > 工具测评类帖子

---

## 输出报告模板

```markdown
# <平台名> <调研主题> 调研报告

> **数据来源**：<平台名> — <搜索词/版块>
> **采集方式**：<工具名>
> **数据规模**：<X> 个帖子/视频，<Y> 条回复/评论
> **采集时间**：<日期>

## 一、采集概况
## 二、用户真实态度（分层：激烈反对→沉默实用→实战派→营销号）
## 三、使用的工具/方法
## 四、痛点拆解（可解决/不可解决/需规避）
## 五、产品机会
## 六、产品/营销/风险三维建议
```

---

> 版本：1.1.0 | 基于 2026-05 全平台调研实战沉淀 | v1.1 新增：覆盖微信公众号/视频号 + 人工兜底方案完整流程
