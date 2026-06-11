---
name: book-to-skill
description: "将书籍和文档（PDF/EPUB/DOCX/HTML/Markdown/纯文本/RTF/MOBI/AZW）转化为结构化Agent Skill，提取框架、心智模型、原则、技法和反模式。当用户想学习一本技术书、把文档文件夹变成知识库、或将资料集合转为可复用Skill时触发。"
version: 1.0.0
pipeline:
  upstream: []
  downstream: []
---

# Book-to-Skill Converter

> 将书面知识转化为可执行的 Agent Skill —— 提取结构，而非产出摘要。

## 触发场景

- 用户提供一本书/文档/文件夹，想将其变成 Skill 随时查阅
- 用户说"把这本书转成 skill"、"把这个文档夹做成知识库"
- 用户想将多份资料合并为一个统一的 Skill

## 核心哲学

书籍包含结晶的专家知识：框架、原则、技法。本 Skill 将这些知识提取为 Agent 可反复利用的格式。

**六条设计原则：**

| # | 原则 | 含义 |
|---|------|------|
| 1 | 提取结构，不写摘要 | Skill 不是读书报告，是命名框架 + 可执行原则 + 技法 + 反模式 |
| 2 | 保留作者的精确性 | "5 Whys" ≠ "多问几次为什么" —— 保留原始命名 |
| 3 | 密度优先于完整 | 1000 token 的提炼 > 10000 token 的原文节选 |
| 4 | 实践者语气 | 写"当 Y 情况时用 X"，不写"本书解释了 X" |
| 5 | SKILL.md 前置核心 | 压缩保留前 4000 token，最重要的内容放最前 |
| 6 | 章节文件按需加载 | 章节不计入 Skill 预算，仅在提问时加载 |

---

## 四种运行模式

根据用户意图路由：

### 模式 1：完整转换（默认）
**触发：** 用户提供文档路径，无特殊指令
**流程：** 执行 Step 0–10 全流程
**输出：** 完整 Skill（SKILL.md + chapters/ + glossary.md + patterns.md + cheatsheet.md）

### 模式 2：仅分析
**触发：** 用户说"先分析"、"只提取"、"我先看看再生成"
**流程：** 执行 Step 0–3，产出结构化提取报告后停止
**输出：** 分析报告（框架、原则、技法清单）

### 模式 3：从分析结果生成
**触发：** 用户已有分析笔记或之前运行过仅分析
**流程：** 跳过 Step 0–3，用已有分析作为输入，执行 Step 4–9
**输出：** 从已有分析生成 Skill 文件

### 模式 4：更新 / 合并（已有 Skill）
**触发：** 用户提供新资料路径 + 指向已有 Skill 目录
**流程：** Step 0–2 → 直接跳至 Update/Fold-in 工作流
**输出：** 更新后的已有 Skill（新增/修订章节 + 合并索引/术语表）

---

## 完整转换工作流（模式 1）

### Step 0 — 范围检查
无参数时停止，提示用法：`book-to-skill <路径> [skill名称]`

- 识别输入路径和可选的 Skill 名称
- 最后一个参数若不是文件/文件夹/glob，且看起来像 slug（小写连字符），视为 `SKILL_NAME`
- 其余参数视为 `INPUT_PATHS`
- 若输入路径是已有 Skill 目录（含 SKILL.md + chapters/），标记为模式 4

### Step 1 — 验证输入
验证至少有一个支持的文件（`.pdf` / `.epub` / `.docx` / `.txt` / `.md` / `.rst` / `.adoc` / `.html` / `.rtf` / `.mobi` / `.azw` / `.azw3`）。对目录和 glob 展开匹配。无支持文件则报错退出。

### Step 1.5 — 识别内容类型
询问用户：
> 这些资料是什么类型？
> 1. **技术类** — 含代码块、表格、公式（编程书/论文/架构指南）
> 2. **文字类** — 主要是散文，表格/代码很少（管理/效率/叙事非虚构）
> 3. **不确定** — 我用快速方法，质量有限时提醒你

- 选 1 → `BOOK_TYPE=technical`（用 Docling，~1.5s/页）
- 选 2 或 3 → `BOOK_TYPE=text`（用最快提取器）

### Step 2 — 提取文本
运行提取脚本：

```bash
python scripts/extract.py <INPUT_PATHS> --mode <BOOK_TYPE> --install-missing ask
```

产出：
- `<tempdir>/book_skill_work/full_text.txt` — 合并提取文本
- `<tempdir>/book_skill_work/metadata.json` — 统计数据

**预检环境：** `python scripts/extract.py --check` 打印各格式提取器安装状态。

### Step 2.5 — 成本预估
读取 metadata.json，在生成前展示预估：

```
📖 检测到 <N> 个源文件
📄 合并页数: ~<N> | 词数: ~<N> | Token: ~<N>K

💰 预估成本:
   输入: ~<N>K tokens  |  输出: ~<N>K tokens  |  总计: ~<N>K tokens
   Sonnet 4.5: ~$<X>  |  Haiku 4.5: ~$<X>
   ⏱ 预计耗时: ~<N> 分钟

📁 将生成: SKILL.md + 章节文件 + glossary + patterns + cheatsheet
```

等待用户确认后继续。

### Step 2.6 — 大书 REPL 式访问（> 50K tokens）
将 `full_text.txt` 视为可查询语料库，不要一次性全读：

```bash
wc -w full_text.txt                           # 大小检查
grep -n "^\s*(Chapter|CHAPTER)\s+[0-9]+" ...  # 找章节偏移
sed -n '<start>,<end>p' full_text.txt         # 只拉需要的章节
grep -c -i "关键词" full_text.txt             # 验证框架是否提到
```

50K tokens 以下直接 Read 即可。

### Step 3 — 分析结构
读取 full_text.txt 前 8000 字符，识别：书名/作者、章节结构、核心主题。

如果是**仅分析模式**，产出提取报告（框架、原则、技法、反模式、建议 Skill 名、章节目录表）后停止。

### Step 4 — 询问用途（仅完整转换）
> "这个 Skill 主要帮你做什么？"
> 1. 工作时应用作者的框架
> 2. 用作者的心智模型思考
> 3. 查阅具体章节和概念
> 4. 以上全部

- 只选 3 → `DEPTH=reference`（精简快查）
- 含 1/2/4 → `DEPTH=study`（深度，含实例和推理）

### Step 5 — 确定 Skill 名称与目标路径
- 有 `SKILL_NAME` 则直接用
- 否则提议两种命名格式：`{作者}-{核心概念}` 或 `{书名-slug}`
- 目标路径默认 `~/.claude/skills/`，已存在则提示覆盖/重命名/合并

### Step 6 — 创建目录结构
```bash
mkdir -p <skills_home>/<skill_name>/chapters
```

### Step 7 — 生成章节摘要

**Token 预算矩阵：**

| BOOK_TYPE \ DEPTH | reference | study |
|---|---|---|
| text | 800–1200 | 1000–1800 |
| technical | 1200–1800 | 2000–3000 |

**章节文件模板：**
```markdown
# Chapter N: <完整标题>

## Core Idea
<1-2 句：本章最重要的一个洞见>

## Frameworks Introduced
- **<框架名>**: <精确表述>
  - 何时用: <场景>
  - 怎么做: <步骤或标准>

## Key Concepts
- **<术语>**: <一句话精确定义>
(本章最重要的 5-10 个术语)

## Mental Models
<2-4 个思维工具，写成"遇到 X 时用 Y"或"把 X 理解为 Y">

## Anti-patterns
- **<要避免的>**: <为什么失败>

## Code Examples *(仅 technical)*
```<language>
<本章最具启发性的代码片段>
```
- **说明**: <一句话>

## Reference Tables *(仅 technical)*
<!-- 还原本章的比较矩阵、参数表、决策表 -->

## Worked Example *(仅 DEPTH=study)*
<!-- 还原作者演示的一个具体实例 -->

## Key Takeaways
1. <可执行的洞察>
...

## Connects To
- **Ch N**: <为什么相关>
```

### Step 8 — 生成辅助文件

#### glossary.md
- 所有重要术语，按字母排序
- 格式：`**术语** — 定义 (Ch N)`
- 最多 1500 tokens

#### patterns.md
- 所有技法、设计模式、算法
- 格式：`## 模式名\n**何时用**: ...\n**怎么做**: ...\n**权衡**: ...`
- 最多 2000 tokens

#### cheatsheet.md（最差异化的层）
**核心是捕获作者的判断力，不是关键词列表。** 优先级：
1. 决策规则 — "当 X，做 Y，因为 Z"
2. 决策树/流程图
3. 权衡矩阵 — 竞争选项在作者关心的维度上打分
4. 阈值与默认值 — 作者给出的具体数字
5. 信号与气味 — 快速识别法（"看到 X 就知道是 Y 问题"）

最多 1200 tokens。

### Step 9 — 生成主 SKILL.md

```markdown
---
name: <skill_name>
description: "来自《<书名>》<作者>的知识库。..."
allowed-tools: [Read, Grep]
argument-hint: [主题、框架名或章节号]
---

# <书名>
**作者**: <> | **页数**: ~<N> | **章节数**: <N> | **生成日期**: <YYYY-MM-DD>

## 如何使用
- 无参数 → 加载核心框架
- 带主题 → 查找并解释对应章节
- 带 ch<N> → 加载指定章节
- "有哪些章节？" → 显示章节目录

## 核心框架与心智模型
<!-- ~2000 tokens: 作者最重要的命名框架和原则 -->

## 章节目录
| # | 标题 | 关键框架 |
|---|------|----------|
...

## 主题索引
- **<术语>** → ch<N>

## 辅助文件
- [glossary.md] / [patterns.md] / [cheatsheet.md]

## 范围与限制
本 Skill 仅覆盖书籍内容。结合项目工具进行实际实现。
```

### Step 10 — 清理与报告

---

## 更新 / 合并工作流（模式 4）

对已有 Skill `$SKILLS_HOME/<skill_name>/` 进行合并：

1. **读取已有结构** — 解析 SKILL.md 的章节索引、主题索引、元数据
2. **匹配内容** — 识别新内容是更新已有章节还是新增章节（从最大章节号后编号）
3. **生成/更新章节** — 按 Step 7 格式
4. **合并辅助文件** — glossary / patterns / cheatsheet 去重合并
5. **重新生成 SKILL.md** — 更新章节数、框架、索引
6. **清理** → Step 10

---

## 质量红线

| # | 规则 | 说明 |
|---|------|------|
| 1 | 提取结构，不写摘要 | 捕获命名框架、精确表述、反模式 |
| 2 | 保留作者精确性 | 保留原始命名，不一概而论 |
| 3 | 密度优先于完整 | 1000 token 提炼 > 10000 token 原文 |
| 4 | 实践者语气 | "当 Y 时用 X"，不写"本书解释 X" |
| 5 | SKILL.md 前置核心 | 最重要内容放最前，压缩保留 ~4000 token |
| 6 | 章节按需加载 | 不计入 Skill 预算，问到时才读 |
| 7 | 绝不复制原书文本 | 始终合成、提炼、提取信号 |
| 8 | 主题索引是命脉 | Agent 靠它导航到正确章节 |

---

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
| `tools/discovery_tax.py` | 测量 Discovery Loop 与 Skill 方式的 token 差异 |
| `tools/validate_skill.py` | 验证生成的 Skill 结构完整性 |

## Gotchas

- **大书（>50K tokens）必须 REPL 式访问**：不要 `Read(full_text.txt)` 全量加载，用 grep/sed 按需拉取章节切片
- **章节自动检测需要 "Chapter N" 格式标题**：纯标题（无编号）或用罗马数字的书无法自动分段，需要手动处理
- **询问内容类型必须在提取前**：选错 `BOOK_TYPE` 会导致技术书的表格/代码丢失或文字书浪费 Docling 时间
- **成本预估必须在生成前展示**：不要跳过 Step 2.5，让用户有知情权
- **cheatsheet 不是 glossary 的缩写版**：cheatsheet 是决策辅助，glossary 是术语索引，两者职能完全不同
