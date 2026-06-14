# PopWave SEO Content Pipeline — Workflow Documentation

> 一个关键词进来，一篇可直接发布的 SEO 文章出去。
> 不是「写文章」，而是一条 7 阶段、双轮审核的自动化内容生产线。

---

## 目录结构

```
SEO/
├── pipeline/                        # 所有 Python 脚本
│   ├── google_serp_scraper.py       # Playwright SERP 抓取
│   ├── serp_analyzer.py             # SERP 竞品结构分析
│   ├── serp_bridge.py               # 独立分析桥接
│   ├── seo_pipeline.py              # 主流水线（编排）
│   ├── generate_100_articles.py     # 竞品关键词去重生成选题
│   ├── beacons_keyword_analysis.py  # Beacons 关键词分类
│   ├── popwave_keyword_extraction.py # Beacons → PopWave 提取
│   ├── check_urls.py                # 批量 URL 检测
│   ├── 抓取SERP.command             # Mac 快捷抓取
│   └── 抓取SERP.bat                 # Windows 快捷抓取
│
├── data/                            # 数据存储
│   ├── keywords/                    # 竞品关键词 CSV
│   │   ├── 100篇内容选题计划.csv
│   │   ├── 10web_keywords_fixed.csv
│   │   ├── durable_keywords_fixed.csv
│   │   ├── wix_keywords_fixed.csv
│   │   ├── tubebuddy_keywords_fixed.csv
│   │   ├── viewstats_keywords_fixed.csv
│   │   └── 竞品功能词机会清单.csv
│   ├── ai_marketing_serp_results.json
│   ├── how_to_start_a_youtube_channel_serp_results.json
│   ├── wikihow_analysis.json
│   ├── youtube_channel_google_serp_results.md
│   └── youtube_channel_serp_analysis.md
│
├── articles/                        # 内容产出
│   ├── outputs/                     # 最终 HTML 文章
│   │   ├── article_ai_website_builder.html
│   │   ├── article_demo.html
│   │   └── article_how_to_start_a_blog.html
│   ├── drafts/                      # Markdown 草稿 & 大纲
│   │   ├── article_how_to_start_a_blog_draft_v1.md
│   │   ├── AI-Website-Builder-DRAFT-v1.md
│   │   ├── AI-Website-Builder-RESEARCH-DRIVEN.md
│   │   └── AI-Website-Builder-完整大纲.md
│   └── 页面设计/                     # 各页面类型设计规范
│       ├── ai-portfolio.md
│       ├── ai-resume.md
│       ├── ai-website-builder.md
│       └── link-in-bio.md
│
├── docs/                            # 文档
│   ├── SEOSKILL.md                  # 核心 SOP（宪法）
│   ├── WORKFLOW.md                  # 本文档
│   ├── Cursor-SSH-断线修复方案.md
│   ├── 安装说明.md
│   ├── 关键词策略_最终清单.md
│   ├── 域名架构规范.md
│   ├── 网站架构规划.md
│   └── 网页验收报告.md
│
├── brand/                           # 品牌设计
│   ├── popwave_palette_comparison_mint_emphasis_scales_unchanged.html
│   └── investor_demo.html
│
├── auto-browser/                    # 自动化浏览器代理（外部项目）
└── skills/                          # Claude Skills 集合（外部依赖）
```

---

## 整体架构

```
[关键词]
    |
    v
Step 1: 关键词调研 + 搜索意图识别       (docs/SEOSKILL.md Step 0-2)
    |
    v
Step 2: Google SERP 实时抓取            (pipeline/google_serp_scraper.py)
    |     提取 Top 10 结果 + PAA 问题 -> data/
    v
Step 3: 竞品结构分析                     (pipeline/serp_analyzer.py / serp_bridge.py)
    |     内容类型分布、主导框架判断、内容缺口识别
    v
Step 4: 竞品内容深读                     (WebFetch 抓取 Top 5 竞品全文)
    |     提取 H2/H3 结构、证据密度、缺失维度
    v
Step 5: 生成文章 Outline                 (AI 按框架生成大纲)
    |
    v
Step 6: Draft v1 完整可发布草稿          (AI 写完整正文) -> articles/drafts/
    |
    v
Step 7: Critique Round 1                (事实/逻辑/合规安全门禁)
    |     问题分类: critical_bug / factual_risk / logic_break
    |     任何重大问题不修复 = 禁止进入下一轮
    v
Step 8: Revision Round 1                (修复全部问题)
    |
    v
Step 9: Critique Round 2                (7 维度质量评分)
    |     Structure / Readability / Practicality / Depth /
    |     Credibility / SEO Fitness / Editorial Maturity
    |     通过条件: 无维度 < 7.0, 均值 >= 8.3, SEO+结构 >= 8.0
    v
Step 10: Final Revision + SEO Pack      (终稿 + 元数据 + 发布包)
    |     输出: 正文 / Meta title / Meta description /
    |     URL slug / FAQ / ALT建议 / 内链外链 / 来源标注
    v
Step 11: HTML 可视化                    (品牌色系适配 + 图文可视化)
    |     纯 CSS 图表: 统计卡片 / 流程图 / 柱状图 /
    |     时间轴 / 卡片矩阵 / Pro-Con 色块
    |     适配 PopWave Sky Bubble 品牌色板
    v
[可发布文章 + SEO Review 面板] -> articles/outputs/
```

---

## 核心 SOP: docs/SEOSKILL.md

`docs/SEOSKILL.md` 是整个系统的「宪法」。它定义了:

- **默认输出**: 英文、可直接发布到 CMS
- **多轮强制评审**: 写文 -> 挑刺 -> 修改 -> 再挑刺 -> 终稿
- **反幻觉规则**: 不编造数据、不伪造来源、不伪装一手经验
- **Publish Gate**: 10 项检查全部通过才标记 publish-ready
- **GEO 适配**: FAQ Schema、引用标注、声明可验证性

---

## 脚本清单

### 核心流水线 (`pipeline/`)

| 文件 | 作用 | 输入 | 输出 |
|---|---|---|---|
| `google_serp_scraper.py` | Playwright 抓取 Google SERP | 关键词 | `data/{keyword}_serp_results.json` |
| `serp_analyzer.py` | SERP 竞品结构分析 | SERP JSON | `data/{keyword}_serp_analysis.json` |
| `serp_bridge.py` | 独立分析桥接（双数据源） | SERP JSON | 分析报告 + 框架建议 |
| `seo_pipeline.py` | 主流水线（编排抓取+分析） | 关键词 | SERP JSON + 分析 JSON + 简报 |

### 关键词研究工具 (`pipeline/`)

| 文件 | 作用 |
|---|---|
| `beacons_keyword_analysis.py` | Beacons 竞品关键词分类分析 |
| `popwave_keyword_extraction.py` | 从 Beacons 关键词池提取 PopWave 相关词 |
| `generate_100_articles.py` | 从多个竞品 CSV 合并去重生成 100 篇选题 |
| `check_urls.py` | 批量检测 URL 可达性 |

### 快捷工具 (`pipeline/`)

| 文件 | 作用 |
|---|---|
| `抓取SERP.command` | macOS 双击即可抓取 SERP |
| `抓取SERP.bat` | Windows 双击即可抓取 SERP |

---

## 数据层 (`data/keywords/`)

| 文件 | 来源 | 用途 |
|---|---|---|
| `10web_keywords_fixed.csv` | 10Web | 关键词调研参考 |
| `durable_keywords_fixed.csv` | Durable | 关键词调研参考 |
| `wix_keywords_fixed.csv` | Wix | 关键词调研参考 |
| `tubebuddy_keywords_fixed.csv` | TubeBuddy | 关键词调研参考 |
| `viewstats_keywords_fixed.csv` | Viewstats | 关键词调研参考 |
| `100篇内容选题计划.csv` | 合并去重后 | 100 篇文章选题库 |
| `竞品功能词机会清单.csv` | 竞品分析 | 功能词机会 |

---

## 内容资产

### 最终产出 (`articles/outputs/`)

| 文件 | 类型 | 字数 | 搜索量（主词） |
|---|---|---|---|
| `article_ai_website_builder.html` | Pillar Page 榜单 | ~13,000 | 22,200/mo |
| `article_demo.html` | Tutorial 教程 | ~2,800 | 890K/mo |
| `article_how_to_start_a_blog.html` | Tutorial 教程 | ~2,800 | 890K/mo |

### 草稿 & 素材 (`articles/drafts/`)

| 文件 | 说明 |
|---|---|
| `article_how_to_start_a_blog_draft_v1.md` | Blog 文章草稿 |
| `AI-Website-Builder-DRAFT-v1.md` | AI Website Builder 草稿 v1 |
| `AI-Website-Builder-RESEARCH-DRIVEN.md` | 研究驱动版（含引用） |
| `AI-Website-Builder-完整大纲.md` | 完整 H1/H2/H3 大纲 + 关键词部署 |

### 页面设计规范 (`articles/页面设计/`)

| 文件 | 页面类型 |
|---|---|
| `ai-website-builder.md` | AI 建站工具页 |
| `ai-portfolio.md` | AI 作品集页 |
| `ai-resume.md` | AI 简历页 |
| `link-in-bio.md` | Link-in-bio 页 |

---

## 品牌设计 (`brand/`)

| 文件 | 说明 |
|---|---|
| `popwave_palette_comparison_mint_emphasis_scales_unchanged.html` | PopWave 品牌色板（New 01 Sky Bubble） |
| `investor_demo.html` | 投资人演示页面 |

---

## 实际使用方式

当前工作流中，SERP 抓取（Playwright）需要在可访问 Google 的网络环境中运行。
在本地网络受限时，采用 **手动 + AI 协作模式**:

1. 用户给出关键词（如 `ai website builder`）
2. AI 通过 WebSearch + WebFetch 获取 SERP 结果和竞品全文
3. AI 按照 `docs/SEOSKILL.md` SOP 执行完整流程
4. AI 产出: 英文正文 + SEO Pack + HTML 可视化
5. HTML 适配 PopWave Sky Bubble 品牌色系
6. 最终文章保存到 `articles/outputs/`，数据分析保存到 `data/`

### 远程服务器模式（Playwright 可用时）

```bash
cd pipeline/

# 完整流水线
python3 seo_pipeline.py "your keyword" 20

# 单独抓取 SERP
python3 google_serp_scraper.py "your keyword" 20

# 分析已有 SERP 数据
python3 serp_bridge.py "your keyword"
```

---

## 后续可做的事

- [ ] 在可访问 Google 的服务器上部署批量跑词
- [ ] 把 `article_demo.html` 的 blog 文章也迁移到 PopWave 品牌色
- [ ] 建立内容库去重机制（Step 0 Backlog Check）
- [ ] 接入真实的 Google Search Console / Ahrefs 排名追踪
- [ ] 产出 JSON-LD Schema 自动生成
