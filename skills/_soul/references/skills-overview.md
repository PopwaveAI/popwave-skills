# 14 个 Skill 能力图谱

> 导航：`_shared/INDEX.md` → 本文档
> 用途：快速了解每个 skill 能做什么、有什么知识资产、跟其他 skill 的关系

---

## 🖊️ 内容创作类

### pop-novel-agent-pro

- **定位**：全链路网文创作系统。覆盖"拆书→开书→剧情架构→正文写作→QC质检→发布"完整管线
- **核心管线**：emergent-writer v9.3（6阶段）、qa-payoff v0.4、plot-architecture v2.7、project-bootstrap v2.8
- **技术栈**：glue Python 层（零 LLM 前置检查）+ spec-bridge + ESMsqlite/YAML 双模式
- **核心知识资产**：
  - `学习资料/` — 知乎10篇、外部干货9份、爽点设计库18份、拆书报告
  - `项目复盘/` — 7 份复盘沉淀、8 份问题跟踪、实验对比、架构迭代、设计决策
  - `skills/_shared/` — template-pools（7场景模板）、universal-knowledge
- **协作关系**：产出 MD/YAML → pop-html-anything 渲染 HTML；产出设定 → pop-novel-game 做文游

### pop-html-anything

- **定位**：**唯一 HTML 渲染引擎**。接收上游结构化数据，产出单文件 HTML
- **核心能力**：8 种骨架模板、Seedream 内嵌生图、三层叠图 Hero、长文阅读器
- **设计系统**：`_design/DESIGN_CORE.md` + components + responsive
- **硬规则**：角色必须有肖像、场景必须有插图（配图硬性触发）
- **协作关系**：消费 pop-novel-agent-pro/reader-making 的结构化数据
- **边界**：novel-agent-pro 内部另有 python html-renderer 作为专用渲染层，不冲突

### pop-book-promo

- **定位**：小说营销物料生成器。PRD 先行 → 设计哲学驱动 → 生图 + 定制 HTML
- **核心模式**：4 种视觉方向（水墨/光影/极简/绮丽）
- **模式 B（旧模板管线）**：⚠️ **Deprecated** — 向后兼容，新项目推荐走模式 A（PRD 先行）
- **边界**：模式 A 产出的是营销落地页（品牌调性优先），与 pop-html-anything 的通用渲染能力互补，不冲突

### pop-novel-game

- **定位**：小说设定 → AI 互动文字游戏（HTML 单文件，零外部依赖）
- **核心流程**：资料解析 → 文游设计 → 产出生成
- **踩坑记录**：5 个实战陷阱（反引号转义/流式兼容/loading锁/超时重试/localStorage恢复）
- **方法论文档**：`方法/资料解析协议.md`、`方法/文游设计协议.md`

### pop-reader-making

- **定位**：长篇小说拆解为结构化参考文件（人类可读的 MD + 机器可消费的 YAML）
- **核心产出**：叙事笔记、章节标注、实体共现、角色/名场面 image_prompt
- **协作关系**：产出 → pop-html-anything 直接消费渲染

### pop-YouTubewebbuilder

- **定位**：YouTube 创作者个人品牌网站生成器
- **核心流程**：YouTube 内容抓取 → 人物画像 → 设计 PRD → 单文件 HTML
- **知识资产**：`DESIGN_GUIDE.md`（15 种视觉方向）、`DATA_CONTRACT.md`
- **铁律**：零 Emoji

---

## 🔍 调研与采集类

### cnovel-research

- **定位**：网文作者社区调研，12+ 平台覆盖
- **核心能力**：AnySearch 引擎 + 各平台 API + 绕过策略 + 人工兜底
- **知识资产**：6 个踩坑记录、调研关键词库、工具选择决策树
- **报告模板**：输出报告标准格式

### book-opinion-tracker

- **定位**：网文舆情追踪。输入书名扫8平台舆情，输出标准化舆情报告
- **核心能力**：依赖 cnovel-research 的平台采集能力，标准化报告模板
- **来源**：原位于 `pop-novel-agent-pro` 内部，v1.8.0 提升为顶层独立 skill
- **协作**：为 book-promo / novel-agent-pro 提供舆情数据

### knowledge-downloader

- **定位**：微信公众号 + B 站内容下载 → 统一结构化拆解报告
- **核心流程**：CDP 下载微信 / API 获取 B 站字幕 → 通用拆解管线
- **模板**：`templates/report-template.md`、`report-prompt.md`

### download-webnovel-txt

- **定位**：输入书名搜索下载网文 TXT
- **核心能力**：5 步工作流 + 6 个目标站点知识库
- **踩坑记录**：7 个常见坑（反爬/VIP/编码/分页/源漂移/别名/连载中）

### web-access

- **定位**：**所有联网操作的唯一入口**
- **核心能力**：WebSearch/WebFetch/curl/Chrome CDP/Jina 预处理
- **方法论**：像人一样浏览、一手来源优先、子 Agent 并行调研
- **站点经验**：`references/site-patterns/{domain}.md` 结构
- ⚠️ **协作边界**：应优先调用此 skill 做联网操作，而非在各自 skill 内自行实现

---

## 🛠️ 基础设施类

### pop-seo-anything

- **定位**：英文 SEO 博客全自动生产管线
- **核心管线**：7 阶段 + 双轮 critique/revision + Publish Gate 10 项检查
- **质量体系**：Unified Scorecard 7 维度评分

### feishu-docs

- **定位**：飞书云文档 API 自动化（文档/评论/多维表格/权限/Markdown导入）
- **核心知识**：Token 架构、Block Type 映射表、错误码参考表（10 个常见码）
- **协作关系**：prd-builder 依赖此 skill

### prd-builder

- **定位**：产品想法 → 结构化 PRD → 飞书同步 → 交互 Demo
- **核心流程**：4 阶段管线（澄清→生成+同步→反馈→Demo）
- **引用**：`references/prd_structure.md`、`demo_framework.md`、`kol_templates.json`
- **依赖**：feishu-docs

### pop-skill-create

- **定位**：**元 skill**。定义 Skill 的编写规范和抽象原则
- **核心产出**：六大抽象原则、场景分类规范、12 项编写检查清单
- **示范案例**：以 cnovel-research 为范例文档

---

## 协作边界清单

| 协作点 | 应该由谁做 | 不应由谁做 |
|:-------|:----------|:----------|
| **联网操作** | web-access | 各 skill 自实现 curl/fetch |
| **HTML 渲染** | pop-html-anything | pop-book-promo（已有重叠） |
| **飞书操作** | feishu-docs | 各 skill 自调飞书 API |
| **SEO 文章** | pop-seo-anything | — |
| **网文下载** | download-webnovel-txt | — |
| **公众号采集** | knowledge-downloader | — |

---

*本文档随 skill 新增/更新同步维护。最后更新：2026-06-02*
