---
name: download-webnovel-txt
description: 输入书名即可搜索直链并下载 TXT。只走一条路：搜直链 → 下直链。不爬目录页、不逐章抓取。
---

# Download Webnovel TXT — 直链版

## 核心原则

**只走直链。不走任何其他方案。**

搜索→验证→下载，三步到位。永远不碰目录页解析、逐章爬取、URL 模板生成。

**不管什么小说，一定能找到直链。** 一批没找到就下一批，试遍所有已知直链站。几百个源里总有一个有。

---

## 工作流

### Step 0: 判断场景（1 秒）

| 输入 | 行为 |
|------|------|
| 只给了书名 | → 走 Step 1 搜直链 |
| 给了 TXT 直链 URL | → 跳过搜索，直接走 Step 3 下载+质检 |
| 给了小说站 URL（非直链） | → 去这个站找有无 TXT 下载页，找不到就回 Step 1 |
| 给了 zip/epub URL | → 直接下载+解压 |

### Step 1: 搜索直链（核心环节）

**查询策略 — 多批次轮换关键词和站点：**

```
// 第一批（最高概率命中）
"{书名} txt 下载"
"{书名} txt 全集"
"{书名} {作者} txt 下载"  （如知道作者）

// 第二批（搜特定站）
"site:txt80.cc {书名}"
"site:zxcs.me {书名}"
"site:txt998.com {书名}"
"site:bookdown.com.cn {书名}"
"site:qisuu.com {书名}"

// 第三批（搜其他常见站）
"site:dygbook.com {书名}"
"site:qubook.cc {书名}"
"site:yaonovel.com {书名}"
"site:bsw22.com {书名}"

// 第四批（搜索引擎/聚合站）
"site:jiumodiary.com {书名}"
"site:sobooks.cc {书名}"
"site:kgbook.com {书名}"

// 第五批（备选源）
"{书名} txt 下载 全本 完结"
"{书名} 电子书 txt"
```

**节奏规则：**
- 每批 2-3 个搜索 query（并行）
- 从结果中提取候选直链 URL
- 立刻验证（Step 2a），能下载就停，不要再搜
- 当前批全部不可用才进下一批
- 直到找到可用的直链为止

### Step 2a: 验证候选直链（快速判断）

用 `WebFetch` 抓候选人 URL，判断：

- **是 TXT 下载页**（有 download/下载链接按钮） → 提取直链 URL，走 Step 3
- **直接是 TXT 文件**（响应是文本内容） → 直接走 Step 3
- **是 zip 文件** → 下载后解压，走质检
- **需要密码/关注公众号/登录** → 跳过该源
- **域名已死/404/云防护** → 跳过该源

### Step 3: 下载单文件

```bash
# 最简单的情况：直接 TXT 直链
curl -o "书名.txt" "https://xxx.com/铸星者.txt"

# 编码问题处理（直链 TXT 常是 GB18030）
curl -s "https://xxx.com/book.txt" | iconv -f gb18030 -t utf-8 > "书名.txt"

# 直接用 python（更可靠）
python3 -c "
import urllib.request
url = '直链URL'
req = urllib.request.Request(url)
req.add_header('User-Agent', 'Mozilla/5.0')
data = urllib.request.urlopen(req, timeout=30).read()
with open('书名.txt', 'wb') as f:
    f.write(data)
print(f'Done: {len(data)} bytes')
"
```

> 如果下载链接返回的是 zip，用 python zipfile 或本地解压工具提取。

### Step 4: 质量验证

简单检查：

```bash
# 文件大小检查
ls -lh "书名.txt"

# 检查内容是中文小说（不是 HTML 也不是导航页）
python3 -c "
import re
with open('书名.txt', encoding='utf-8', errors='replace') as f:
    text = f.read()
# 检查有无 HTML 标签
has_html = bool(re.search(r'<!DOCTYPE|<html|<body|<script', text[:500], re.I))
# 检查章节数
chapters = len(re.findall(r'^第.{1,8}[章节回]', text, re.MULTILINE))
# 检查前 200 字符有无章节内容
has_content = len(text.strip()) > 10000
print(f'包含HTML: {has_html}')
print(f'章节数: {chapters}')
print(f'内容量: {len(text):,} 字符')
print(f'状态: {\"✅ 通过\" if not has_html and chapters > 0 else \"❌ 失败\"}')
"
```

**验收标准：**
- ✅ 文件内容不是 HTML（无 `<!DOCTYPE`、`<html>`、`<script>` 等标签）
- ✅ 检测到章节标题（`第X章/节/回`）≥ 1
- ✅ 正文内容 > 10KB
- ✅ 抽样首尾章节，是正常小说内容
- ❌ 响应是 HTML 导航页 → 重新回 Step 2a 找真实下载链接
- ❌ 文件极短 / 乱码 / 非小说 → 试下一个候选源

---

## 已知直链站知识库（按优先级排列）

| 优先级 | 站名 | 域名 | 特征 | 下载方式 |
|--------|------|------|------|---------|
| ⭐ | 八零电子书 | txt80.cc | 最大站，5.9万+本，免登录 | 下载页面有 `.txt` 直链 |
| ⭐ | 知轩藏书 | zxcs.me / zxcs.info | 精校版为主，质量高 | 通常是 `.zip` 包 |
| ⭐ | 铅笔小说 | lcjl.800tg.com | 全本完结，更新快 | 下载页有直链 |
| ⭐ | 趣书网 | downbook.net / qubook.cc | 分类全，免登录 | TXT 一键下载 |
| ⭐ | 书本网 | txt998.com | 热门全本，界面简单 | 直接 TXT |
| ⭐ | 奇书网 | qisuu.com | 覆盖面广，网友上传 | 下载页直链 |
| ⭐ | 宝书网 | bsw22.com | 排版好，多设备适配 | 免注册下载 |
| ⭐ | 棉花糖小说 | mhtxs.com | 全本免费，分类全 | TXT 下载 |
| ⭐ | TXT图书下载网 | bookdown.com.cn | JAR/UMD/TXT 多格式 | 免登录 |
| ⭐ | 无限小说 | 533wx.com | 支持榜单浏览 | TXT 全集下载 |
| ⭐ | 哎呀小说网 | yanxn.com | 大站稳定 | 直接下载 |
| ⭐ | 大书包 | dashubao.com | 老牌站点 | TXT 直链 |
| ⭐ | 下书网 | xiashu.cc | 资源丰富 | 直链下载 |
| ⭐ | 当书网 | dangshu.com | 全本完结 | TXT 下载 |
| ⭐ | 久久小说 | 99lib.net | 老站稳定 | TXT 下载 |
| 🔍 | 鸠摩搜书 | jiumodiary.com | 聚合搜索引擎 | 跳转网盘/第三方 |
| 🔍 | 苦瓜书盘 | kgbook.com | 老牌免费站 | 跳转第三方 |
| 🔍 | SoBooks | sobooks.cc | 高质量电子书 | 跳转网盘 |

> 注意：部分域名可能变动或失效。搜不到就换下一个，不必纠结。

---

## 常见编码处理

```python
# 直链 TXT 经常是 GB18030/GBK 编码，检测并转码
import chardet
with open('raw.txt', 'rb') as f:
    raw = f.read()
    enc = chardet.detect(raw)['encoding']
    print(f'检测到编码: {enc}')
    text = raw.decode(enc if enc else 'utf-8', errors='replace')
    # 如果出现大量 � 替换字符，换用 gb18030
```

---

## 典型对话

用户："下载遮天"

LLM:
1. WebSearch "遮天 txt 下载" "site:txt80.cc 遮天"
2. WebFetch txt80.cc/xxx/ → 看到下载链接
3. curl 拉下来 → 检查 → 交付

用户："下载铸星者 浮屠子"

LLM:
1. WebSearch "铸星者 浮屠子 txt 下载"
2. 看到 txt80.cc 结果 → WebFetch → 有直链
3. python3 下载 → 质检 → 交付
4. 共耗时：~30 秒

---

## 什么情况不归本 skill 管

- 用户只给了小说站 URL（不是直链）→ 去该站找下载页，没有就搜直链
- 小说只有付费平台有 → 告知用户"该作品暂无免费直链"
- 用户想在线阅读 → 不是本 skill 职责
- 云防护/验证码页面 → 换源，不硬刚
