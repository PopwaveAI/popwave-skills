---
name: zhixia-content-studio
description: "当用户说'知夏文案/网文营销号/学习资料并生成HTML/小红书标题SEO/最新模板直出'时启用。完成外部检索、内容策划、文案SEO、HTML组图和可选资产沉淀。"
---

# zhixia-content-studio

> “知夏陪你写网文”的一体化内容工作室：研究 → 策划 → 文案/SEO → HTML → 可选沉淀。

## ❌ 核心红线

1. **禁止跳读执行文件**：进入任一步前完整加载对应 `steps/step-*.md`；文件疑似截断时重新读取。
2. **禁止无路由开工**：先按输入类型选择搜索强度和后续路径，不对完整文案重新做全量检索。
3. **禁止越过确认闸门**：默认在策划后、HTML前等用户确认；仅用户明确“直出/不用确认”时跳过等待。
4. **禁止脱离模板重写HTML**：必须从 `templates/html/` 复制填充；新版本不得覆盖历史终稿。
5. **禁止伪造热度与事实**：无来源的“爆款/全网热门/平台推流”只作线索，不写成结论。
6. **禁止视觉先于内容**：封面、第二页和分页文案确认后，才能进入完整HTML生产。
7. **禁止版本漂移**：改造Skill时同步更新 `SKILL.md`、`skill.json`、`CHANGELOG.md` 的版本。

## 强弱加载保障

- 强保障：本文件负责路由和红线，必须保持简短可见。
- 弱保障：`steps/`、`references/`、`templates/` 按任务加载；未加载对应Step不得产出该阶段文件。

## 输入路由

| 输入 | Step 1策略 | 后续 |
|---|---|---|
| 只有选题 | 标准外搜 + 内部知识 | 1→2→确认→3→确认→4→可选5 |
| DOCX/截图/参考帖 | 用户资料优先 + 快速补缺 | 1→2→确认→3→确认→4→可选5 |
| 完整文案 | 事实与SEO快速核验 | 1→3→确认→4→可选5 |
| 只改HTML | 跳过内容搜索 | 4 |
| 系统选题研究 | 深度外搜 + 证据包 | 1→2→确认后分批生产 |

## 全文件速查

| 操作 | 必须加载 | 产出 | 门禁 |
|---|---|---|---|
| 检索研究 | `steps/step-1-research.md` + `references/research-sop.md` | 研究包 | ⛔ 来源分级后进入Step 2 |
| 内容策划 | `steps/step-2-content-plan.md` + `references/task-routing.md` + `references/soul.md` | 策划卡 | ⛔ 用户确认A |
| 文案与SEO | `steps/step-3-copy-seo.md` + `references/seo-sop.md` + 对应 `templates/copy/` | 封面、分页、发布稿 | ⛔ 用户确认B |
| HTML组图 | `steps/step-4-html.md` + `references/html-template-guide.md` + `references/visual-qa.md` | 新版本HTML | ⛔ 结构与视觉验收 |
| 资产沉淀 | `steps/step-5-ingest.md` + `references/knowledge/index.md` | 可复用规则/索引 | ⛔ 只沉淀已核对资产 |
| 主题素材 | `references/knowledge/{cp,bazong,foreshadowing,dialogue,facial-expression,worldbuilding-naming}.md` | 主题知识 | 只读当前主题 |
| 来源核对 | `references/knowledge/source-extracts.md` | 来源证据 | 不直接复制发布 |
| 文案模板 | `templates/copy/{list-post,deep-case-post,tutorial-post,concept-post,publish-caption}.md` | 对应稿件 | 按任务选择一个 |
| HTML模板 | `templates/html/{list-9page,deep-case-9page}.html` | 1080×1920组图 | 不从空白CSS开始 |
| 辅助搜索 | `scripts/build_search_matrix.py` / `scripts/search_knowledge.py` | 查询矩阵/内部结果 | 结果仍需判断 |

## 执行规则

按路由加载第一个Step；每个Step末尾给出下一步加载条件。默认互动模式执行两个确认闸门；用户明确直出时内部完成确认材料但不暂停。正式沉淀是可选步骤，不因“完成HTML”自动污染知识库。

## 版本

v2.0.0 | 2026-07-06 | 从资料库重构为分层内容工作室 → [CHANGELOG.md](CHANGELOG.md)
