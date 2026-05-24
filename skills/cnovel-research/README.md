# cnovel-research

中国网文作者社区用户调研工具包 —— 基于 2026-05 对 **8 个平台、1,043+ 条内容、14,316+ 条互动**的全量调研实战沉淀。

## 📁 目录结构

```
cnovel-research/
├── README.md                    ← 你在这里
├── SKILL.md                     ← 核心技能文件（调研方法论 + 工具选择决策树）
├── reports/                     ← 9 份完整调研报告
│   ├── 00_跨平台总报告.md       ← 最推荐先读这个
│   ├── 01_龙空.md
│   ├── 02_晋江碧水.md
│   ├── 03_阅文作家社区.md
│   ├── 04_贴吧.md
│   ├── 05_知乎.md
│   ├── 06_豆瓣.md
│   ├── 07_微博.md
│   └── 08_B站.md
└── tools/                       ← 爬虫脚本 + AnySearch 搜索引擎
    ├── anysearch/               ← AnySearch Skill（通用搜索引擎）
    ├── bilibili_scanner.py      ← B站视频 + 评论爬虫
    ├── tieba_final.py           ← 贴吧 aiotieba 全量扫描器
    └── weibo_scanner.py         ← 微博 crawl4weibo 全量扫描器
```

## 🚀 快速开始

### 1. 先读 SKILL.md

核心资产。包含：
- **11 个平台**的可采集性矩阵（哪个能爬、怎么爬、正文拿不到怎么办）
- **工具选择决策树**（什么时候用 AnySearch，什么时候用专用工具，什么时候让人工兜底）
- **人工兜底方案**（豆瓣/阅文/小红书/公众号/抖音/视频号的标准操作流程）
- **AI 写作调研关键词库**（按平台分级的搜索词）
- **踩过的 6 个坑**和解决方案

### 2. 想看结论 → 读跨平台总报告

`reports/00_跨平台总报告.md` 整合了全部 8 个平台的发现，分为 7 个部分：
1. 网文作者对 AI 的态度光谱（5 档人群 × 8 平台交叉表）
2. "AI 写得不行"的 6 种抱怨完整拆解（哪些产品能解决、哪些不能）
3. 8 个平台的态度差异全景
4. 产品战略（P0/P1 功能清单）
5. 营销战略（目标用户分群 × 各平台话术矩阵）
6. 7 大雷区和预设应对
7. 总结和机会判断

### 3. 想看某个平台 → 读对应的分平台报告

例如 `reports/06_豆瓣.md` 覆盖了豆瓣 6 个写作小组的 30+ 个 AI 帖子和 500+ 回复。

### 4. 想重新跑数据

```bash
# 贴吧（需先给 aiotieba 打 HTTP 补丁，见 SKILL.md）
python tools/tieba_final.py

# 微博（自动获取 Cookie）
python tools/weibo_scanner.py

# B站（免登录）
python tools/bilibili_scanner.py

# 通用搜索（免 API Key 也可用，但限制频率）
python tools/anysearch/scripts/anysearch_cli.py search "AI写小说 site:tieba.baidu.com"
```

## 📊 本次调研数据基础

| 平台 | 内容量 | 互动量 | 核心用户 |
|:---|:--:|:--:|:---|
| 龙空 | 74 帖 | 923 回复 | 男频老作者 |
| 晋江碧水 | 199 帖 | 396 回复 | 女频签约作者 |
| 阅文作家社区 | 41 帖 | 108 回复 | 起点/阅文签约作家 |
| 贴吧（7 吧） | 106 帖 | 1,363 回复 | 番茄等免费站底层作者 |
| 知乎（9 问） | 9 问 | 2,000+ 回答 | 方法论分享者/签约作者 |
| 豆瓣（6 组） | 30+ 帖 | 500+ 回复 | 女频/文学向/同人作者 |
| 微博 | 386 条 | 7,399 评论 | KOL/卖课号/普通用户 |
| B站 | 198 视频 | 1,627 评论 | UP主/KOL/吃瓜群众 |
| **合计** | **1,043+** | **14,316+** | |

## ⚙️ 环境准备

```bash
# Python 依赖
pip install aiotieba crawl4weibo requests beautifulsoup4 --break-system-packages

# aiotieba 需要源码补丁：修改 get_posts/_api.py 中 scheme="https" → scheme="http"
# 路径通常在 /usr/local/lib/python3.10/dist-packages/aiotieba/api/get_posts/_api.py

# AnySearch（可选，搜索增强）
# 见 tools/anysearch/README.md
# 免 API Key 也可用，但有频率限制
```

## 📝 贡献指南

### 新调研场景

当对某个平台/话题做了新调研后：

1. **更新 `SKILL.md`** 中的"能力范围"表和"踩坑"清单
2. **新增报告**到 `reports/` 目录
3. **新增脚本**到 `tools/` 目录
4. **更新本 README** 的数据表

### 报告格式约定

- 所有引用必须是用户原帖/评论原文（"零转述零二手资料"）
- 分析要落到三件事：产品/营销/风险
- 态度不要简单分"支持/反对"，要按人群和平台分层

## 📄 License

CC BY-NC 4.0 — 用于非商业用途请保留署名

---

> 调研时间：2026-05-15 ~ 2026-05-18
> 调研工具：aiotieba / crawl4weibo / B站 API / AnySearch / 晋江 HTTP / WebSearch / WebFetch
