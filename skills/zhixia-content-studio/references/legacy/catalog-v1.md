# 知夏资源目录

本文件只负责告诉Agent“每个文件是什么、什么时候读”。不要一次性加载全部资料。

## 账号层

| 文件 | 用途 |
|---|---|
| `../SOUL.md` | 账号人设、口吻、价值观、禁用表达、固定结束语；任何对外内容必读 |

## 工作流层

| 文件 | 用途 |
|---|---|
| `workflows/research-search.md` | 外部搜索策略、搜索矩阵、来源分级、交叉验证和研究包格式 |
| `copy-templates/task-router.md` | 按清单、深写、教程、概念、发布配文选择文字排版结构 |
| `seo-keyword-playbook.md` | 核心词、长尾词、标题/正文/评论/标签分配 |
| `visual-playbook.md` | 视觉验收、封面重心、密度选择、版本留档 |
| `content-playbook.md` | 旧版综合手册，仅供历史兼容，不作为新任务第一入口 |

工作流辅助脚本：

- `../scripts/build_search_matrix.py`：为外部搜索生成概念、写法、痛点、平台、反例与事实核验查询。
- `../scripts/search_library.py`：搜索内部主题文库。

## HTML模板层

| 文件 | 用途 |
|---|---|
| `../templates/html/README.md` | 模板选择、槽位说明、认可终稿来源 |
| `../templates/html/list-9page.html` | 数量清单、短素材库 |
| `../templates/html/deep-case-9page.html` | 一页一组的人设、写法、完整案例 |

## 主题知识层

| 主题 | 文件 | 典型关键词 |
|---|---|---|
| 总索引 | `library-index.md` | 不确定该读哪个主题时 |
| CP与关系 | `cp-setting-library.md` | CP、人设、宿敌、双强、校园纯爱、名场面 |
| 霸总豪门 | `bazong-writing-library.md` | 总裁、豪门、联姻、黑卡、宴会、商战 |
| 伏笔 | `foreshadowing-library.md` | 伏笔、埋梗、回收、身份反转、叙述诡计 |
| 对话 | `dialogue-writing-library.md` | XX说、提示语、潜台词、声线、对话节奏 |
| 眉眼神态 | `facial-expression-library.md` | 眼神、视线、眉毛、睫毛、微表情 |
| 地名世界观 | `worldbuilding-naming-library.md` | 虚拟城市、学校、古风州郡、仙侠秘境 |
| 来源摘录 | `source-extracts.md` | 核对参考图片与历史来源 |

## 按任务读取

### 用户提供资料并要求“学习、分析、入库、生成HTML”

必读：`SOUL.md`、本目录、`workflows/research-search.md`、对应主题知识、`copy-templates/task-router.md`、SEO手册、HTML模板说明。外部检索只补缺与核验，不覆盖用户材料。

### 用户只给选题，需要从零完成内容

必读：`workflows/research-search.md`，执行标准检索；再读对应主题知识、文案模板、SEO和HTML模板。

### 用户已经给出完整文案

使用快速检索，只核验事实、补SEO和发现明显缺口。不要为了调用文库重新拼一篇。

### 用户只要写作素材

必读：本目录、对应主题知识。无需读取HTML模板。

### 用户只要小红书标题/正文/tag

必读：`SOUL.md`、文案任务模板、SEO手册。无需读取HTML模板和全部主题库。

### 用户只要求改HTML排版

必读：HTML模板说明、视觉验收规则、当前HTML。跳过外部检索；文案无变化时不读取全部主题库。

### 用户要求重新入库

必读：来源摘录、对应主题知识、`SKILL.md` Step 5。确认终稿后再正式写入。
