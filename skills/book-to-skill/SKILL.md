---
name: book-to-skill
description: "当用户说'把这本书转成skill/把文档做成skill/提取这本书的框架/学这本书/把这个文件夹做成知识库/合并资料为skill'时启用。将书籍和文档（PDF/EPUB/DOCX/HTML/Markdown/纯文本/RTF/MOBI/AZW）转化为结构化 Agent Skill，提取框架、心智模型、原则、技法和反模式。"
version: 1.0.0
pipeline:
  upstream: []
  downstream: []
---

# Book-to-Skill Converter

> 将书面知识转化为可执行的 Agent Skill —— 提取结构，而非产出摘要。

---

## 速查表：四种模式怎么选

| 用户说什么 | 走什么模式 | 执行步骤 | 产出 |
|:-----------|:-----------|:---------|:-----|
| "把这本书转成skill"（无特殊指令） | **模式 1：完整转换**（默认） | Step 0 → Step 10 全流程 | 完整 Skill（SKILL.md + chapters/ + glossary.md + patterns.md + cheatsheet.md） |
| "先分析" / "只提取看看" / "我先看看" | **模式 2：仅分析** | Step 0 → Step 3，产出分析报告后停止 | 分析报告（框架、原则、技法清单） |
| "从上次分析结果生成skill" | **模式 3：从分析结果生成** | 跳过 Step 0-3，用已有分析作为输入直接执行 Step 4-9 | 从已有分析生成 Skill 文件 |
| "往这个skill里加点新资料" / "把新文档合并到已有skill" | **模式 4：更新/合并** | Step 0-2 → 直接跳至 Update/Fold-in 工作流 | 更新后的已有 Skill（新增/修订章节 + 合并索引/术语表） |

---

## ❌ 质量红线

| # | 规则 | 说明 |
|:-:|:-----|:------|
| ❌1 | **提取结构，不写摘要** | 捕获命名框架、精确表述、反模式。写摘要 → 退回重写 |
| ❌2 | **保留作者精确性** | 保留原始命名，不一概而论。"5个为什么" ≠ "多问几次为什么" |
| ❌3 | **密度优先于完整** | 1000 token 提炼 > 10000 token 原文。超过 Token 预算 → 砍冗余 |
| ❌4 | **实践者语气** | "当 Y 时用 X"，不写"本书解释 X"。发现第三人称描述 → 改 |
| ❌5 | **SKILL.md 前置核心** | 最重要内容放最前，压缩保留 ~4000 token |
| ❌6 | **章节按需加载** | 不计入 Skill 预算，问到时才读。一次性全加载 → 退回 |
| ❌7 | **绝不复制原书文本** | 始终合成、提炼、提取信号。大段引用 → 退回 |
| ❌8 | **主题索引是命脉** | Agent 靠它导航到正确章节。无索引或索引不全 → 退回补充 |
| ❌9 | **大书必须 REPL 式访问** | >50K tokens 的书必须用 grep/sed 按需拉取，不可 Read 全量加载 |

---

# 模式 1：完整转换（默认）

> 用户提供文档路径，无特殊指令。执行全流程。

## 第一步：范围检查与输入验证（Step 0 → Step 1）

1. 无参数 → 停止，提示用法：`book-to-skill <路径> [skill名称]`
2. 识别输入路径和可选的 Skill 名称
   - 最后一个参数若不是文件/文件夹/glob，且看起来像 slug（小写连字符）→ 视为 `SKILL_NAME`
   - 其余参数视为 `INPUT_PATHS`
   - 若输入路径是已有 Skill 目录（含 SKILL.md + chapters/）→ 标记为模式 4
3. 验证至少有一个支持的文件（`.pdf` / `.epub` / `.docx` / `.txt` / `.md` / `.rst` / `.adoc` / `.html` / `.rtf` / `.mobi` / `.azw` / `.azw3`）
4. 对目录和 glob 展开匹配

❌ 门禁：无支持文件 → 退回，告知用户"未找到支持的文档格式"，列出支持格式清单。

## 第二步：识别内容类型 + 提取文本（Step 1.5 → Step 2）

询问用户内容类型：

> 这些资料是什么类型？
> 1. **技术类** — 含代码块、表格、公式（编程书/论文/架构指南）
> 2. **文字类** — 主要是散文，表格/代码很少（管理/效率/叙事非虚构）
> 3. **不确定** — 我用快速方法，质量有限时提醒你

- 选 1 → `BOOK_TYPE=technical`（用 Docling，~1.5s/页）
- 选 2 或 3 → `BOOK_TYPE=text`（用最快提取器）

运行提取脚本：

```bash
python scripts/extract.py <INPUT_PATHS> --mode <BOOK_TYPE> --install-missing ask
```

产出：
- `<tempdir>/book_skill_work/full_text.txt` — 合并提取文本
- `<tempdir>/book_skill_work/metadata.json` — 统计数据

**预检环境：** `python scripts/extract.py --check` 打印各格式提取器安装状态。

❌ 门禁：**必须在提取前询问内容类型。** 选错 `BOOK_TYPE` 会导致技术书的表格/代码丢失或文字书浪费 Docling 时间 → 退回重选。

## 第三步：成本预估 + 大书处理（Step 2.5 → Step 2.6）

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

**大书处理（>50K tokens）：** 将 `full_text.txt` 视为可查询语料库，不要一次性全读：

```bash
wc -w full_text.txt                           # 大小检查
grep -n "^\s*(Chapter|CHAPTER)\s+[0-9]+" ...  # 找章节偏移
sed -n '<start>,<end>p' full_text.txt         # 只拉需要的章节
grep -c -i "关键词" full_text.txt             # 验证框架是否提到
```

50K tokens 以下直接 Read 即可。

❌ 门禁：**成本预估必须在生成前展示。** 跳过 Step 2.5 → 退回，让用户有知情权。

## 第四步：分析结构 + 询问用途（Step 3 → Step 4）

读取 full_text.txt 前 8000 字符，识别：书名/作者、章节结构、核心主题。

询问用途：

> "这个 Skill 主要帮你做什么？"
> 1. 工作时应用作者的框架
> 2. 用作者的心智模型思考
> 3. 查阅具体章节和概念
> 4. 以上全部

- 只选 3 → `DEPTH=reference`（精简快查）
- 含 1/2/4 → `DEPTH=study`（深度，含实例和推理）

## 第五步：创建目录结构 + 生成章节摘要（Step 5 → Step 6 → Step 7）

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

❌ 门禁：章节摘要超过 Token 预算 → 砍冗余，确保密度优先。

## 第六步：生成辅助文件（Step 8）

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

❌ 门禁：cheatsheet 写成 glossary 的缩写版 → 退回重写。cheatsheet 是决策辅助，glossary 是术语索引，两者职能完全不同。

## 第七步：生成主 SKILL.md（Step 9）

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

## 第八步：清理与报告（Step 10）

---

# 模式 2：仅分析

> 用户说"先分析"、"只提取"、"我先看看再生成"时走此模式。

**流程：** 执行 Step 0-3，产出结构化提取报告后停止。
**输出：** 分析报告（框架、原则、技法清单）

---

# 模式 3：从分析结果生成

> 用户已有分析笔记或之前运行过仅分析。

**流程：** 跳过 Step 0-3，用已有分析作为输入，执行 Step 4-9。
**输出：** 从已有分析生成 Skill 文件。

---

# 模式 4：更新 / 合并（已有 Skill）

> 用户提供新资料路径 + 指向已有 Skill 目录。

**流程：** Step 0-2 → 直接跳至 Update/Fold-in 工作流。

**合并步骤：**
1. **读取已有结构** — 解析 SKILL.md 的章节索引、主题索引、元数据
2. **匹配内容** — 识别新内容是更新已有章节还是新增章节（从最大章节号后编号）
3. **生成/更新章节** — 按章节模板格式
4. **合并辅助文件** — glossary / patterns / cheatsheet 去重合并
5. **重新生成 SKILL.md** — 更新章节数、框架、索引
6. **清理** → Step 10

---

## ❌ 错误示例

### WRONG 1：大书全量 Read 加载

```
用户：把《Clean Architecture》转成skill
Agent：Read(full_text.txt) → 一次性加载 80K tokens 的内容
❌ 错误：大书（>50K tokens）必须 REPL 式访问，全量加载消耗大量 Token 且可能超时
✅ 正确：先用 grep -n "Chapter" 找章节偏移，按需 grep -i "关键词" 确认框架位置，sed 拉取指定章节切片
```

### WRONG 2：cheatsheet 写成 glossary 的缩写版

```
Agent 输出的 cheatsheet：
- Encapsulation — 封装，将数据和操作封装在一起 (Ch 4)
- Polymorphism — 多态，同一接口不同实现 (Ch 5)
❌ 错误：这就是 glossary 的复制，没有捕获作者的判断力
✅ 正确：cheatsheet 应该是决策辅助——
  "当需要隐藏实现细节时 → 用封装，因为降低耦合"
  "接口变化频率高于实现时 → 用多态，因为调用方不受实现变更影响"
```

### WRONG 3：SKILL.md 没有主题索引

```
Agent 输出了完整的 SKILL.md + 章节，但没有主题索引
用户问"这本书讲了依赖注入吗？"
Agent 只能逐一搜索章节目录
❌ 错误：无索引 = Agent 无法快速定位内容，每次都要扫描全文件
✅ 正确：SKILL.md 必须包含主题索引（**<术语>** → ch<N>），Agent 靠它导航
```

### WRONG 4：复制原书大段原文作为章节摘要

```
Agent 从原书直接复制了 3 段话（~500 tokens）作为章节摘要
❌ 错误：违反"绝不复制原书文本"红线，且浪费 Token 预算
✅ 正确：始终合成、提炼、提取信号 —— 用自己的话写 Core Idea（1-2 句）和 Key Concepts（5-10 个术语）
```

---

## 异常与边界条件

| 场景 | 触发条件 | 处理动作 |
|:-----|:---------|:---------|
| **无支持格式文件** | Step 1 验证输入时没有识别到 `.pdf/.epub/.docx/.txt/.md/.html/.rtf/.mobi/.azw` 中的任意一种 | 报错退出，列出支持的格式清单供用户参考。不自动创建空文件 |
| **提取器未安装** | Step 2 运行 `python scripts/extract.py` 时缺少依赖库 | 使用 `--install-missing ask` 参数提示安装。用户拒绝安装 → 降级为内置提取器（仅支持 txt/md），产出标注"缺少XX提取器，部分格式无法处理" |
| **大书 >50K tokens 且内容无"Chapter N"标题** | 书籍标题不使用"Chapter N"格式（如纯标题无编号或用罗马数字） | 无法自动分段，需要手动处理。告知用户"需要手动指定章节范围"，逐段读取前半部分确定章节边界 |
| **用户提供空目录** | Step 1 展开目录或 glob 后匹配到 0 个文件 | 提示用户"该目录下没有支持的文档格式"，建议重新指定路径或文件 |
| **成本预估用户拒绝继续** | Step 2.5 展示成本后用户表示太贵或放弃 | 停止管线，清理临时文件。不留下半成品文件 |
| **已有 Skill 目录命名冲突** | Step 5 目标路径 `~/.claude/skills/<name>` 已存在同名 Skill | 提示用户选择：覆盖 / 重命名 / 合并（走模式 4）。不静默覆盖 |
| **提取文本内容质量过低**（大量乱码/空行/OCR错字） | Step 2 提取后 `full_text.txt` 大量不可读内容 | 告知用户"文本提取质量较低，建议检查原文件是否为扫描件/图片PDF"，询问是否继续。继续 → 产出标注"提取质量低" |
| **章节自动检测失败** | Step 7 无法自动识别章节边界 | 使用按比例切分：将全文按页数/token 等分后生成章节摘要，产出标注"章节为自动切分，非原书结构" |
| **合并时新资料与已有 Skill 领域不匹配** | 模式 4 合并时新资料主题与已有 Skill 领域差异过大 | 提示用户"新资料主题与已有 Skill 领域差异较大"，建议创建新 Skill 而非合并。用户坚持合并 → 合并后标注"含跨域内容" |
| **生成文件超出 Token 预算** | SKILL.md / glossary / patterns / cheatsheet 超出各自最大 Token 限制 | 逐文件砍冗余。**砍的顺序**：示例文本 → 次要框架 → 次要术语 → 确保核心框架完整保留 |

**原则**：异常先告知用户，再按规则处理。绝不静默跳过或编造数据。

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
