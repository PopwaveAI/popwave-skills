---
name: tool-book-to-skill
description: "当用户说'把这本书转成skill/把文档做成skill/提取这本书的框架/学这本书/把这个文件夹做成知识库/合并资料为skill'时启用。将书籍和文档（PDF/EPUB/DOCX/HTML/Markdown/纯文本/RTF/MOBI/AZW）转化为结构化 Agent Skill，提取框架、心智模型、原则、技法。"
version: 1.1.0
pipeline:
  upstream: []
  downstream: []
---
# Book-to-Skill Converter v1.1.0

> 将书面知识转化为可执行的 Agent Skill —— 提取结构，而非产出摘要。

## 模式选择

详见 [steps/00-mode-selection.md](steps/00-mode-selection.md)

| 用户说什么 | 模式 | 步骤 | 产出 |
|:-----------|:-----|:-----|:-----|
| "转成skill"（默认） | 模式 1：完整转换 | Step 0→10 | 完整 Skill |
| "先分析看看" | 模式 2：仅分析 | Step 0→3 | 分析报告 |
| "从分析结果生成" | 模式 3：从分析生成 | Step 4→9 | Skill 文件 |
| "合并到已有skill" | 模式 4：更新/合并 | Update/Fold-in | 更新后 Skill |

## 红线

| # | 红线 | 说明 |
|:-:|:-----|:------|
| 1 | 提取结构，不写摘要 | 捕获命名框架、精确表述、反模式。写摘要 → 退回重写 |
| 2 | 保留作者精确性 | 保留原始命名。`5个为什么` ≠ `多问几次为什么` |
| 3 | 密度优先 | 1000 token 提炼 > 10000 token 原文。超预算 → 砍冗余 |
| 4 | 实践者语气 | `当 Y 时用 X`，不写`本书解释 X` |
| 5 | SKILL.md 前置核心 | 最重要内容放最前，核心 ~4000 token |
| 6 | 章节按需加载 | 不计入 Skill 预算，问到时才读 |
| 7 | 绝不复制原书文本 | 始终合成、提炼、提取信号。大段引用 → 退回 |
| 8 | 主题索引是命脉 | Agent 靠它导航。无索引或不全 → 退回补充 |
| 9 | 大书 REPL 式访问 | >50K tokens 必须 grep/sed 按需拉取，不可 Read 全量 |

## Drop Check

| # | 检查项 | 触发条件 | 动作 |
|:-:|:-------|:---------|:-----|
| D1 | 无支持格式文件 | Step 1 验证无匹配 | 退回，列出支持格式清单 |
| D2 | 提取前未问类型 | Step 2 跳过询问 | 退回重选 BOOK_TYPE |
| D3 | 成本预估跳过 | Step 2.5 未展示 | 退回，展示预估后等确认 |
| D4 | cheatsheet = glossary 缩写 | Step 8 产出审查 | 退回重写 cheatsheet |

## 核心流程

> 模式 1（完整转换）按以下顺序执行 Step 文件。

| Step | 文件 | 说明 |
|:-----|:-----|:-----|
| 0-1 | [steps/01-input-validation.md](steps/01-input-validation.md) | 范围检查与输入验证 |
| 1.5-2 | [steps/02-content-extraction.md](steps/02-content-extraction.md) | 识别内容类型 + 提取文本 |
| 2.5-2.6 | [steps/03-cost-estimation.md](steps/03-cost-estimation.md) | 成本预估 + 大书处理 |
| 3-4 | [steps/04-analysis.md](steps/04-analysis.md) | 分析结构 + 询问用途 |
| 5-7 | [steps/05-chapters.md](steps/05-chapters.md) | 创建目录结构 + 生成章节摘要 |
| 8 | [steps/06-aux-files.md](steps/06-aux-files.md) | 生成辅助文件（glossary/patterns/cheatsheet） |
| 9 | [steps/07-main-skill.md](steps/07-main-skill.md) | 生成主 SKILL.md |
| 10 | [steps/08-cleanup.md](steps/08-cleanup.md) | 清理与报告；模式 4 合并工作流 |

## WRONG 示例

| # | 错误 | 正确 |
|:-:|:-----|:-----|
| W1 | 大书 `Read(full_text.txt)` 全量加载 80K tokens | 大书用 grep/sed 按需拉取章节切片 |
| W2 | cheatsheet 写成 glossary 缩写版 | cheatsheet 是决策辅助：`当 X 时 → 用 Y，因为 Z` |
| W3 | SKILL.md 无主题索引 | 必须含 `**术语** → ch<N>` 主题索引供 Agent 导航 |
| W4 | 复制原书大段原文作为章节摘要 | 始终合成提炼，用自己的话写 Core Idea |

## 异常与边界条件

| 场景 | 触发条件 | 处理 |
|:-----|:---------|:-----|
| 无支持格式文件 | Step 1 无匹配格式 | 报错，列出支持格式清单 |
| 提取器未安装 | extract.py 缺依赖 | `--install-missing ask`；拒绝→降级内置提取器 |
| 大书无 "Chapter N" 标题 | 无法自动分段 | 手动指定章节范围 |
| 用户提供空目录 | glob 展开匹配 0 文件 | 提示无支持文档，建议重新指定 |
| 成本预估用户拒绝 | 展示成本后放弃 | 停止管线，清理临时文件 |
| 已有 Skill 目录冲突 | 目标路径已存在 | 提示：覆盖/重命名/合并（模式 4） |
| 提取文本质量过低 | 大量乱码/空行 | 告知用户，询问是否继续 |
| 章节自动检测失败 | 无法识别章节边界 | 按比例切分，标注"自动切分" |
| 合并领域不匹配 | 模式 4 主题差异大 | 建议创建新 Skill；坚持合并则标注 |
| 文件超出 Token 预算 | 超各自最大限制 | 砍冗余：示例→次要框架→次要术语 |

## 支持的格式

| 格式 | 推荐工具 | 安装 |
|------|----------|------|
| PDF(文字类) | pdftotext | `poppler-utils` |
| PDF(技术类) | docling | `pip install docling` |
| EPUB | ebooklib+bs4 | `pip install ebooklib beautifulsoup4` |
| DOCX | python-docx | `pip install python-docx` |
| HTML | beautifulsoup4 | `pip install beautifulsoup4` |
| RTF | striprtf | `pip install striprtf` |
| MOBI/AZW | Calibre | calibre-ebook.com |
| TXT/MD/RST/AsciiDoc | 内置 | — |

## 脚本

| 脚本 | 用途 |
|------|------|
| `scripts/extract.py` | 主提取入口，支持所有格式 |
| `scripts/extract.py --check` | 检查各格式提取器安装状态 |
| `scripts/discovery_tax.py` | 测量 Discovery Loop 与 Skill 方式的 token 差异 |
| `scripts/validate_skill.py` | 验证生成的 Skill 结构完整性 |

## Gotchas

- **大书（>50K tokens）必须 REPL 式访问**：不要 `Read(full_text.txt)` 全量加载，用 grep/sed 按需拉取章节切片
- **章节自动检测需要 "Chapter N" 格式标题**：纯标题（无编号）或用罗马数字的书无法自动分段，需要手动处理
- **询问内容类型必须在提取前**：选错 `BOOK_TYPE` 会导致技术书的表格/代码丢失或文字书浪费 Docling 时间
- **成本预估必须在生成前展示**：不要跳过 Step 2.5，让用户有知情权
- **cheatsheet 不是 glossary 的缩写版**：cheatsheet 是决策辅助，glossary 是术语索引，两者职能完全不同
