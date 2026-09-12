# pop-visual-style

> 本技能提供通用文生图能力与画风DNA库。只做纯文生图，单次操作即可生成图片。当前版本为 v2.2.0，完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

## 职责范围

输入：画面描述（自然语言），以及画风选择（从 37 种 DNA 库中选择，或自定义）。
输出：生成的图片，以及提示词记录。

核心价值：画风库是营销专家 skill 群的公共资产，既支持独立执行纯文生图，又作为 art-bible、cover、oc、comic 的画风层引用源。

**画风与内容解耦铁律（v1.10.0 核心）**：DNA 库中每条画风分两层：`dna` 是**中性技法层**，说明怎么画（线稿、上色、光影、比例、特征），可跨题材复用；`content_theme` 是**可交换题材层**，说明画什么（原生题材的内容元素）。生成时**画风段只使用 `dna` 与 `constraint`（纯技法）**，内容由 `content_theme`（默认）或用户场景描述（覆盖）决定（铁律❌10）。耦合示例：黑执事与维多利亚哥特、赛博边缘行者与高科技城市、蒸汽朋克与齿轮机械。

**与art-bible/cover/oc/comic的边界**：

| 本 skill 负责 | 本 skill 不负责，交由专用 skill 承担 |
|:---------|:---------------------------|
| 画风DNA库管理（37种及扩展） | 美术设定集（画风、人物、场景、符号五篇合一），交由 art-bible |
| 提示词结构知识（6段式、V3、高精度4块） | 封面设计（视觉钩子、文字融入、构图骨架），交由 cover |
| 光照与画风兼容性矩阵 | 立绘设计（六层文字、角色调研、系列冻结），交由 oc |
| 构图模板（CT1、CT2） | 漫画生成（分镜、定妆图、跨章一致性），交由 comic |
| 纯文生图执行 | 参考图策略（参考点放权），交由 cover、oc |
| 质量触发词与画风前置优化 | 文化元素设计（定场诗、印章），交由 cover、oc |

## 模型说明

| 生成内容 | 工具/方式 | 说明 |
|:-----|:---------|:-----|
| 静态图片（Seedream 5.0 Pro） | `image_generate` 工具 | 文生图/图生图/多图输入，无 API Key |
| 动态视频（Seedance 1.0 Pro） | `generate.py video` | 需显式设置 `ARK_API_KEY` 环境变量，不内置 key |

Seedream 5.0 Pro 画面不再泛白，简洁精确优于堆砌；文字用双引号包裹。

## 执行模式

**主 agent 直接执行**：画风选择与定标验收是需要用户多轮交互的检查点（选择画风、确认图片、冻结签核），提示词组装与生成通过调用 `image_generate` 工具完成，批量定标通过固定脚本 `batch_test.py` 执行，没有适合派给子 agent 的环节。

## 怎么运作（规程全文内联）

### Step 1: 画风选择

1. **读取 DNA 库**：`references/文风DNA-library.json`，获取37种画风（含IP命名试点「双城之战」）。
2. **筛选推荐**：按赛道匹配 `suggested_genres` 字段，按关键词匹配 `keywords` 字段，按类别（二次元17、国漫6、韩漫3、插画概念10）推荐1-3种画风，并附推荐理由（视觉特征、代表作、适合赛道）。
3. **用户选择**：从候选池中选择画风，或描述自定义风格。**自定义画风处理**：按 DNA 库格式组装 `dna`（英文画风描述≤800字符）与 `constraint`（风格保真约束）；生成后验证辨识度，未达标则调整 `dna` 描述。
4. **Pinterest 参考图搜索（单张固定）**：搜索有成本（Bright Data 付费），**一次搜索，全程复用**。选定画风后搜索 1 张最符合画风的参考图，作为全书风格准绳：
   ```powershell
   python ../pop-visual-shared/scripts/pinterest_search.py "画风关键词" --limit 5 --max-results 5 --download --output-dir "素材/ref-cache/"
   ```
   - 关键词：画风名、赛道与主要特征（如"暗黑修仙厚涂 玄幻 封面"）
   - 从结果中选择 **1 张最符合画风**的参考图（单张固定），删除其余候选，避免多图带来的不确定性
   - 参考图路径记入 `素材/风格/画风决策.md` 的 `参考图` 字段，作为基线索引
   - 参考图是"图资产"，主路径整图复用（image 参数）；精确分离公式仅作风格迁移到新内容时的辅助（铁律❌8）
5. **加载光照构图推荐**：取选定画风的 `recommended_lighting`（LT1/LT2/LT3）、`recommended_composition`（CT1/CT2）、`content_theme`（**该画风原生题材的默认内容层**，供 Step 2 场景段兜底；跨题材时由用户场景覆盖）。
6. **兼容性检查**（铁律❌3，查 `references/lighting-composition-templates.md` 兼容性矩阵）：柔美风格（少女水彩、轻小说、日系赛璐珞等）必须用LT2，禁止用LT1；平面风格（扁平矢量、波普、极简线条）必须用LT3；暗黑风格用LT1。
7. **输出记录**到 `素材/画风选择记录.md`：选定画风名、类别、`keywords`、`dna` 与 `constraint`（**纯技法层，禁止混入内容**）、`content_theme`、`recommended_lighting` 与 `recommended_composition`、兼容性检查结果。

### Step 2: 提示词组装

读取 `../pop-visual-shared/references/seedream-prompt-guide.md` §一，按6段式结构组装：

```
[质量触发词] + Art style: [dna] [constraint] + [构图策略] + [光影叙事] + [场景] + [人物≤100字]
```

| 段 | 取值来源 |
|:---|:---------|
| 1 质量触发词 | 固定：`IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed` |
| 2 画风DNA | Step 1 选定的 `dna` 与 `constraint`（**纯技法层，禁止混入内容**；必须放在第2段紧跟质量触发词，因画风前置符合 Seedream 注意力权重机制，执行力最强，铁律❌2） |
| 3 构图策略 | `references/lighting-composition-templates.md` 中CT1/CT2的英文描述 |
| 4 光影叙事 | 同文件中LT1/LT2/LT3的英文描述（按兼容性选择） |
| 5 场景 | **内容层接入**：用户场景描述优先；跨题材复用时用户场景覆盖；无题材或要画风原生题材时用 `content_theme` 兜底 |
| 6 人物 | 用户输入的人物描述，≤100字 |

**内容层接入规则（铁律❌10）**：用户给出具体场景时，使用用户场景描述（`content_theme` 仅供参考，不覆盖）；跨题材复用画风时（如用「国漫玄幻厚涂」画现代都市），场景段使用用户场景，**技法层不变**，禁止 `content_theme` 的题材元素污染画面；用户未给出题材时，用 `content_theme` 兜底。

**字数检查**：英文提示词≤600词，人物描述≤100字，`dna` 字段≤800字符（DNA 库已保证）；须用自然语言连贯描述，不得堆叠关键词。

**自检**：画风DNA从DNA库取（❌1）；画风在第2段（❌2）；光照与画风兼容（❌3）；**画风段只含技法、不含题材内容词（❌10）**，检查 `dna` 段是否误带世界观、服装、建筑、招数等；人物≤100字；总词数≤600。

**备选结构**（需要文字渲染，如书名、角色名等时切换）：**V3结构化公式**见 `seedream-prompt-guide.md` §二；**高精度4块结构**见同文件 §三（商业级，含 HARD CONSTRAINTS）。纯文生图默认使用6段式，备选结构供 cover、oc skill 跨场景使用。

### Step 3: 执行生成

1. **确定参数**：尺寸按画幅选择；watermark=`false`。尺寸速查：

| 比例 | 像素 | 用途 |
|:-----|:-----|:-----|
| 3:4 | 1125x1500 | 竖版（默认） |
| 4:3 | 1500x1125 | 横版 |
| 1:1 | 1500x1500 | 方形 |
| 16:9 | 1500x844 | 宽屏 |
| 9:16 | 844x1500 | 竖版海报 |

> **铁律：所有出图总像素 ≤ 236 万（Seedream 5.0 Pro 计费临界，超限报价翻倍）。** 上表全部安全（最大 1500x1500=225 万）。用 `image_generate` 工具生成时按此尺寸传参，超限需人工拦截。

> **⚠️ 画风定标图禁止加品牌水印**：定标图是下游图生图 `ref_image` 的生产参考，加 `popwave.cn` 会被 Seedream 当作画面内容带入下游成品，造成层层污染；水印只在对外展示的产出（OC 立绘、封面、漫画页）完成之后叠加。

2. **执行生成**（统一走 `image_generate` 工具，不直连 API、无内置 API Key）：
   ```text
   image_generate(prompt='提示词内容', size='1125x1500', output='测试/画风定标/{画风}-v1.png')

   # 图生图模式（有参考图时）
   image_generate(prompt='提示词内容', size='1125x1500', ref_image='测试/画风定标/参考图.png', output='测试/画风定标/{画风}-v1.png')
   ```
   画风定标/批量测试：走固定脚本 `batch_test.py`（导出 `generation_tasks.json`），再由 `image_generate` 工具逐条生成（见 Step 4）。

3. **输出目录**（三态写入规则见 `../pop-visual-pipeline/references/落盘规范.md`）：定标候选统一输出到 `测试/画风定标/`（目录不存在则创建）；**认可冻结后**复制到 `素材/风格/`（基建真源），并在 `画风决策.md` 记录冻结路径；`测试/` 内不标 final，冻结到 `素材/风格/` 才算定稿（`测试/画风定标/` 属可清理态）。

4. **回写提示词记录**（追加到项目文件）：模型、画风、光照模板、构图模板、完整提示词、尺寸、输出路径、状态✅。

5. **迭代**：用户不满意时诊断问题（画风辨识度不足则强化 `dna` 描述；光照不兼容则更换模板；人物变形则增加约束），调整对应维度后重新生成（文件名递增为 v2、v3……），并更新记录。

### Step 4: 画风定标（Pipeline 语境下必做；独立纯文生图跳过本步，Step 1 至 Step 3 直接出图）

画风是"只能靠视觉验证"的抽象资产。本步用**小说次要视觉锚点与固定模板**渲染定标图，只验证一件事：**画风 DNA 是否被准确执行**。用户认可后**冻结为基线资产**；未认可则不冻结，也不放行到下游。

**核心原则**：
- **素材关联**：测试素材**从小说中提取次要视觉锚点**，包括战斗场景或地点（`--scene`）、路人、NPC 或龙套（`--side`）；素材与小说强相关，保留代入感，但无关紧要，不承担形象验收。**禁止使用主角或主要角色**，其形象由 `pop-visual-art-bible` 与 `oc` 环节承担（铁律❌5）。
- **变量隔离**：画风定标的唯一变量是**画风**。测试素材**一次确定，固定使用**（传入后不再更换），构图固定，光照固定；**素材固定后禁止中途更换**，否则会把"画风问题"和"素材适配度问题"混为一谈。
- **稳定复现（工作流主线）**：不只验证"这一张对不对"，还要验证"**能不能稳定复现**"：固定 seed 与同一提示词做复现对比，确认画风结果稳定，而非出于单次运气。**只有稳定复现的画风才冻结为基线。**

**何时用（按 intent 档位分支）**：Pipeline 语境下读项目根 `状态.md` 的 `intent` 字段；未建 状态.md（独立模式）按用户当次意图判定：

| intent 档位 | 定标方式 |
|:------------|:---------|
| `comic`/`full` | **完整定标（必做）**：完整检查与稳定复现验证（见下文 3），进入 character（Phase 2）前先定标 |
| `cover`/`oc` | **agent 自检分支**：出定标图后 agent 自查辨识度、配色、光影、无文字即可，**不设强制用户确认，不强制稳定复现**；定标图可单张，达标即标记 `✅ 已认可` 供下游作画风参考 |
| 独立纯文生图 | 跳过本步 |

**1. 测试素材（小说次要视觉锚点）**，两类任选其一或组合（英文）：
- **场景类**（`--scene`）：战斗场景、地点或环境片段，能体现画风光影与氛围。示例：`abandoned ancient temple courtyard, cracked stone floor, a single candle-lit altar, drifting dust motes in a beam of light, a torn banner stirring in the wind, no people, no text`
- **人物类**（`--side`）：路人、NPC 或龙套，非主角，不要求一致性，纯文生图。示例：`an old street vendor in worn robes, weathered face, standing by a wooden stall under a faded awning, neutral expression, no text`
- 小说暂无可提取的合适次要元素（如排期未定）时，可兜底使用脚本内置的中性素材（不传 `--scene` 与 `--side`）。**禁止传 `--character` 或 `--character-image` 引入主角、主要角色**。

**2. 批量导出定标任务**（一次出多张变体；必须使用固定脚本，禁止现场手写提示词、单张串行，后者等于"每次全新设计"，既不稳定又慢）：
```powershell
# 从 DNA 库按画风名批量测（传入小说次要素材：战斗场景 + 路人）→ 导出 generation_tasks.json
python ../pop-visual-shared/scripts/batch_test.py --style-names "暗黑悬疑高对比,赛博边缘行者" --scene "<上文场景类示例>" --side "<上文人物类示例>" --out-dir 测试/画风定标 --seed 20260803

# 只用场景类（无路人）测画风
python ../pop-visual-shared/scripts/batch_test.py --style-names "暗黑悬疑高对比" --scene "moonlit bamboo grove, swirling mist, a lone stone lantern glowing faintly, wind-blown leaves, no people, no text" --out-dir 测试/画风定标 --seed 20260803

# 精调变体（定制 variant 的 dna/constraint/lighting，脚本注入的 scene/side 会覆盖变体同名段）→ 用于"只改一个子维度"的返工迭代
python ../pop-visual-shared/scripts/batch_test.py --config _过程/脚本任务/定标变体.json --scene "..." --side "..." --out-dir 测试/画风定标 --seed 20260803
```
- **`--style-names`**：从 DNA 库按画风名批量测（推荐），脚本自动取 `dna`、`constraint`、`recommended_composition`、`recommended_lighting`（默认 8 线程并发批量与自动 PE 日志）；画风 DNA 放在第 2 段，由脚本固定模板保证（铁律❌2）
- **`--config 变体.json`**：精调变体，每个变体可单独修改 `dna`、`constraint`、`lighting`
- **`--seed`**：固定随机种子保证复现（下游图生图用同 seed 不漂移）
- **输出**：`generation_tasks.json`（每个变体一个任务，含 prompt、size、ref_images、output_path）与 `pe-log.json`（含测试素材、模板、每个变体完整 prompt，可复现）
- **生成**：读 `generation_tasks.json`，对每条任务用 `image_generate` 工具生成（有 ref_images 时传参考图），输出到各任务 output_path，即 `{out-dir}/seed-{seed}/{画风名}.png`
- 从结果中选择达标变体作为候选定标图；**不达标返工时只改该变体 JSON 的一个子维度，重新执行同一脚本，不重写调用**

**3. 🚪 检查：画风定标验收与稳定复现验证**（comic/full 完整档必做）：
- **画风定标验收**（向用户呈现定标图逐项验收）：

| 维度 | 验收判据 |
|:-----|:---------|
| 辨识度 | 0.3 秒能否认出"来自哪个画风体系"（厚涂玄幻、赛璐珞、水彩、暗黑高对比） |
| 配色成立 | 画风自带主色板在这个测试场景下是否成立、是否被场景吞掉 |
| 光影兼容 | 所选光照模板与该画风是否兼容（柔美风格禁 LT1，防柔美画风被暗色吞噬） |
| 无文字 | 无乱码、无伪文字、无加字 |

**未达标不冻结**：返工微调 DNA 片段（非重选风格），重新生成 v2、v3……直到达标。
- **稳定复现验证（核心）**：用**同一提示词与同一 seed** 重新执行一次固定脚本（`batch_test.py` 的输出目录按 `seed-{seed}` 分级，同 seed 重跑输出到同一目录，天然形成复现对比）：`python ../pop-visual-shared/scripts/batch_test.py --style-names "画风名" --out-dir 测试/画风定标 --seed 20260803`；判据为：同 seed 目录下辨识度、配色、光影是否**稳定一致**（允许构图微差，画风铁定）。**未稳定复现不冻结**：画风漂移说明提示词对 seed 敏感，只改该变体的一个子维度进行调整，直到稳定复现。

**4. 认可后冻结基线资产**：用户认可且稳定复现通过后，画风三字段**冻结为基线**：
- 写入 `素材/风格/画风决策.md`，并标注 `签核状态: ✅ 已认可`
- 记录：画风名、`dna`、`constraint`、`recommended_lighting`、`recommended_composition`、**参考图路径**、**定标 seed**、定标图路径
- **seed 必须记录**：下游用同 seed 复现保证稳定；参考图路径作为下游图生图 image 参数的来源

**5. 通知下游**：画风定标图已就绪，可供以下环节消费：

| 消费方 | 用途 |
|:-------|:-----|
| `pop-visual-art-bible` | 美术设定集画风篇的画风基准（首消费方，定全宇宙色彩基调） |
| `pop-visual-cover` / `pop-visual-oc` | 封面与 OC 的风格参考图（image 参数与同 seed） |
| `pop-visual-comic` | 漫画页的风格基准（同 seed 保证画风不漂移） |

> **铁律**：画风基线一旦冻结，下游只消费它（同 seed 复现），禁止各自发明新画风；画风改动必须回本 skill 重新定标。

> Pipeline 语境下完成后进入 Phase 2（`pop-visual-art-bible`）产出美术设定集（定妆深度按 intent 档位：`comic`/`full` 完整双角度，`cover`/`oc` 单张或跳过）。

## ❌ 铁律

| # | 铁律 | 违反后果 |
|:-:|:-----|:---------|
| ❌1 | **画风必须从DNA库取** — 禁止凭记忆编写画风描述，必须从文风DNA-library.json取dna与constraint字段 | 画风辨识度不足，风格漂移 |
| ❌2 | **画风前置** — 画风DNA放提示词前段（第2段），不放开头也不放末尾。Phase 0验证：画风前置符合Seedream注意力权重分配机制 | 画风执行力弱，被场景描述覆盖 |
| ❌3 | **光照兼容性检查** — 选定画风后必须检查recommended_lighting，柔美风格禁用LT1减法照明 | 水彩/柔美风格被暗色吞噬（LT1误用教训） |
| ❌4 | **提示词记录必须写入** — 画风选择、提示词、参数一并写入项目文件 | 无法迭代优化 |
| ❌5 | **定标图必须用小说次要视觉锚点（变量隔离）** — 用**和小说相关但无关紧要的次要元素**测画风（`--scene` 场景、`--side` 路人），素材一次确定，固定使用，唯一变量是画风；**禁止使用主角或主要角色**（形象验收归 art-bible、oc 环节） | 用主角则混入形象变量，分不清画风与形象问题；用无关中性素材则代入感弱 |
| ❌6 | **未认可不冻结、不放行下游** — 画风定标图未获用户认可，不得进入基线、不得被下游消费 | 画风问题带病进入角色设计/封面/漫画，返工成本后置 |
| ❌7 | **必须验证稳定复现** — 画风定标必须用同 seed 与同提示词复现对比，未稳定复现不冻结；冻结时记录 seed 与参考图路径 | 画风依赖单次运气，下游无法复现，画风漂移 |
| ❌8 | **参考图是"图资产"，单张固定** — 主路径是整图复用（image 参数），不靠精确分离公式提炼文字；一次搜索，全程复用，禁止重复搜索 | 重复付费，且文字提炼还原不了参考图，风格失真 |
| ❌9 | **画风定标走固定脚本 `batch_test.py`** — 定标必须用 `../pop-visual-shared/scripts/batch_test.py`（固定素材、固定6段式模板、并发批量、自动PE日志），禁止现场手写提示词、单张串行 | 每次测试变量不隔离、不稳定、慢 |
| ❌10 | **画风与内容解耦 — DNA 必须是纯技法层** — `dna` 只描述怎么画（线稿、上色、光影、比例、特征），**禁止嵌入题材内容词**（世界观、服装、建筑、道具、招数斗气等）；内容走 `content_theme`（默认）或用户场景覆盖。不同画风的耦合方式各异，须逐条剥离，禁止一律只揪 `修仙流` | 画风污染实际内容（如国漫玄幻厚涂把现代都市场景拉回古代仙侠），跨题材复用失效 |

## 速查表

| 需求 | 读取内容 | 使用时机 |
|:-----|:------|:---------|
| 画风DNA库（37种） | `references/文风DNA-library.json` | Step 1 |
| 提示词结构与写法 | `../pop-visual-shared/references/seedream-prompt-guide.md` | Step 2 |
| 构图模板、光照模板与兼容性矩阵 | `references/lighting-composition-templates.md` | Step 1 兼容性检查 / Step 2 |
| Pinterest 参考图搜索 | `../pop-visual-shared/scripts/pinterest_search.py` | Step 1 |
| 生成图片 | `image_generate` 工具 | Step 3 |
| 固定画风测试脚本（并发批量） | `../pop-visual-shared/scripts/batch_test.py` | Step 4 |

> **环境**：Python 3.8+ 及 requests。

## 跨skill引用协议

art-bible、cover、oc、comic 各 skill 引用本 skill 画风层时：

1. **画风描述**：从 `references/文风DNA-library.json` 取 `dna` 与 `constraint` 字段（**纯技法层**）；取 `content_theme` 作为该画风原生题材的默认内容（跨题材时由各 skill 的场景描述覆盖）
2. **光照兼容性**：取 `recommended_lighting` 字段，作为光源设计参考
3. **构图参考**：取 `recommended_composition` 字段，作为构图设计参考（不替代各skill自己的构图体系）
4. **提示词组装**：各 skill 使用自己的结构层（V3、4块、三字段），画风段从 DNA 库取 `dna` 与 `constraint`（纯技法），内容层独立于画风段，禁止把题材内容混入画风段
5. **画风前置原则**：纯文生图场景，画风DNA放提示词前段；图生图场景按参考点策略处理
6. **画风基线资产与稳定复现**：Pipeline 语境下定标认可后冻结（`素材/风格/画风决策.md` 标 `✅ 已认可`），下游只消费冻结的画风三字段、定标图、冻结 seed、参考图（均从 `画风决策.md` 读取），禁止各自发明新画风；**按 intent 分流**：`comic`/`full` 走完整定标检查与稳定复现，`cover`/`oc` 走 agent 自检分支
7. **art-bible 是第一消费方**：画风基线首先被 `pop-visual-art-bible` 消费（引用画风篇，定全宇宙色彩基调），再由美术设定集下发给 oc、cover、comic，禁止派生层绕过美术设定集直接读画风决策
