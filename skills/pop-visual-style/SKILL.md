---
name: pop-visual-style
description: "当用户说'画一张图/生成图片/文生图'或需要纯文生图时启用。管理37种画风DNA库（含IP命名试点）+3光照模板+6段式提示词结构，调用Seedream API生成图片。作为art-bible/cover/oc/comic skill的共享画风层。"
---

# pop-visual-style

> 通用文生图引擎 + 画风DNA库。纯文生图，一键出图。v1.12.0

## 做什么

输入：画面描述（自然语言）+ 画风选择（从37种DNA库选或自定义）。
输出：生成图片 + 提示词记录。

核心价值：**画风库是营销专家skill群的公共资产**。本skill既独立执行纯文生图任务，又作为art-bible/cover/oc/comic的画风层引用源。

**画风×内容解耦铁律（v1.10.0 核心）**：DNA库每条画风分两层——`dna` 是**中性技法层**（怎么画：线稿/上色/光影/比例/特征，可跨题材复用），`content_theme` 是**可交换题材层**（画什么：该画风原生题材的内容元素）。生成时**画风段只用 `dna`+`constraint`（纯技法）**，内容由 `content_theme`（默认）或用户场景描述（覆盖）决定。不同画风耦合方式各异（如黑执事耦合维多利亚哥特、赛博边缘行者耦合高科技城市、蒸汽朋克黄铜耦合齿轮机械），逐条审计剥离，禁止一律只揪 `xianxia` 一种。

**与art-bible/cover/oc/comic的边界**：

| 本skill做 | 本skill不做（交给专用skill） |
|:---------|:---------------------------|
| 画风DNA库管理（37种+扩展） | 美术设定集（画风/人物/场景/符号五篇合一）→ art-bible |
| 提示词结构知识（6段式/V3/高精度4块） | 封面设计（视觉钩子+文字融入+构图骨架）→ cover |
| 光照-画风兼容性矩阵 | 立绘设计（六层文字+角色调研+系列冻结）→ oc |
| 构图模板（CT1/CT2） | 漫画生成（分镜+定妆图+跨章一致性）→ comic |
| 纯文生图执行 | 参考图策略（参考点放权）→ cover/oc |
| 质量触发词+画风前置优化 | 文化元素设计（定场诗/印章）→ cover/oc |

## 模型说明

| 生成内容 | 工具/方式 | 说明 |
|:-----|:---------|:-----|
| 静态图片（Seedream 5.0 Pro） | `image_generate` 工具 | 文生图/图生图/多图输入，无 API Key |
| 动态视频（Seedance 1.0 Pro） | `generate.py video` | 需显式设置 `ARK_API_KEY` 环境变量，不内置 key |

Seedream 5.0 Pro 画面不再泛白，简洁精确优于堆砌。支持文生图、图生图、多图输入。文字用双引号包裹。

## 怎么运作

### Step 1: 画风选择 → `steps/step1-style-select.md`

- 读取 `references/style-dna-library.json` 获取37种画风
- 按赛道/关键词筛选推荐1-3种画风
- 用户选择或自定义
- **Pinterest 参考图搜索（单张锚定）**：选定画风后搜 1 张最符合画风的参考图，落盘 `素材/ref-cache/`，路径记决策.md（一次搜索、全程复用）
- 自动加载该画风的 `recommended_lighting` 和 `recommended_composition`
- **画风-光照兼容性检查**：若画风推荐LT2柔光通透，禁止使用LT1减法照明

### Step 2: 提示词组装 → `steps/step2-prompt-build.md`

- 读取 `../pop-visual-shared/references/seedream-prompt-guide.md` 获取提示词结构
- **6段式结构**（纯文生图默认）：`[质量触发词] + Art style: [dna] [constraint] + [构图策略] + [光影叙事] + [场景] + [人物≤100字]`
- 画风DNA从库中取 `dna` + `constraint` 字段，放提示词前段（高权重位）——**只取技法层，禁止把内容元素混入画风段**
- **内容层接入**：画风段之后，第5段「场景」用 `content_theme` 兜底；若用户给出的画面题材与画风原生题材不同（跨题材复用），用**用户场景描述覆盖** `content_theme`，技法层不变
- 构图从 `references/lighting-composition-templates.md` 取 CT1/CT2 模板
- 光照从同文件取 LT1/LT2/LT3 模板，按兼容性矩阵选择
- 中文提示词 ≤400字，英文 ≤600词

### Step 3: 执行生成 → `steps/step3-generate.md`

- 确定参数（模型/尺寸/输出路径）
- 执行 `../pop-visual-shared/scripts/generate.py`
- 保存图片 + 回写提示词记录

### Step 4: 画风定标（按 intent 档位分支）→ `steps/step4-style-calibrate.md`

- **小说次要视觉锚点素材**：画风定标默认用**和小说相关但无关紧要的次要元素**测画风——某个战斗场景/地点（`--scene`）、路人/NPC/龙套（`--side`）。和小说强相关 → 保留 project 代入感 ahament；无关紧要 → 不承担角色形象验收（v1.9.0 回归，**禁止用主角测画风**——画风可能满意但形象不满意，画风 skill 只验画风，人物形象归 `pop-visual-art-bible`/`oc` 环节用已冻结画风去渲染；不传则兜底用脚本内置中性素材）
- 走固定脚本 `../pop-visual-shared/scripts/batch_test.py` **并发批量**（固定 6 段式模板 + 默认 8 线程 + 自动 PE 日志），一次出多张变体；变量隔离，唯一变量是画风
- 让画风第一次被眼睛看到，验证 DNA 是否被 Seedream 准确执行
- **档位分支（按 intent）**：
  - `comic`/`full` → **完整定标（必做）**：🚪 **画风定标验收门禁**（辨识度/配色/光影/无文字）+ **稳定复现验证**（同 seed 复现对比），用户认可 → **冻结画风三字段为基线资产**（`素材/风格/画风决策.md` 标 `✅ 已认可`，记录 seed + 参考图路径）
  - `cover`/`oc` → **降为 agent 自检分支**：agent 自查辨识度/配色/光影/无文字即可，**不设强制用户门禁**；定标图可单张，达标即标记 `✅ 已认可` 供下游作画风参考，**不强制稳定复现验证**
  - 独立纯文生图时 → **跳过本步**（Step 1→2→3 直接出图）
- 未认可 / 未稳定复现 → 回炉微调 DNA 片段（只改变体一个子维度），不冻结、不放行下游

## ❌ 铁律

| # | 铁律 | 违反后果 |
|:-:|:-----|:---------|
| ❌1 | **画风必须从DNA库取** — 禁止凭记忆编画风描述，必须从style-dna-library.json取dna+constraint字段 | 画风辨识度不足，风格漂移 |
| ❌2 | **画风前置** — 画风DNA放提示词前段（第2段），不放开头也不放末尾。Phase 0验证：画风前置符合Seedream注意力权重分配机制 | 画风执行力弱，被场景描述覆盖 |
| ❌3 | **光照兼容性检查** — 选定画风后必须检查recommended_lighting，柔美风格禁用LT1减法照明 | 水彩/柔美风格被暗色吞噬（LT1误用教训） |
| ❌4 | **提示词记录必须落盘** — 画风选择、提示词、参数写入项目文件 | 无法迭代优化 |
| ❌5 | **定标图必须用小说次要视觉锚点（变量隔离）** — 画风定标默认用**和小说相关但无关紧要的次要元素**测画风（`--scene` 场景/`--side` 路人），素材一次确定、固定使用，唯一变量是画风；**禁止用主角/主要角色测画风**（画风可能满意但形象不满意，画风 skill 只验画风，人物形象归 art-bible/oc 环节） | 用主角 → 混入角色形象变量，分不清是画风问题还是形象问题；用与小说无关的中性素材 → ahament 代入感弱 |
| ❌6 | **未认可不冻结、不放行下游** — 画风定标图未获用户认可，不得进入基线、不得被下游消费 | 画风问题带病进入角色设计/封面/漫画，返工成本后置 |
| ❌7 | **必须验证稳定复现** — 画风定标必须用同 seed + 同提示词复现对比，未稳定复现不冻结；冻结时记录 seed + 参考图路径 | 画风依赖单次运气，下游无法复现，画风漂移 |
| ❌8 | **参考图是"图资产"单张锚定** — 主路径是整图复用（image 参数），不靠精确分离公式提炼文字；一次搜索、全程复用，禁止重复搜索 | 重复付费 + 文字提炼还原不了参考图，风格失真 |
| ❌9 | **画风定标走固定脚本 `batch_test.py`** — 定标必须用 `../pop-visual-shared/scripts/batch_test.py`（固定素材+固定6段式模板+并发批量+自动PE日志），禁止现场手写提示词、单张串行 | 每次测试变量不隔离、不稳定、慢 |
| ❌10 | **画风与内容解耦 — DNA 必须是纯技法层** — `dna` 只描述怎么画（线稿/上色/光影/比例/特征），**禁止嵌入题材内容词**（世界观/服装/建筑/道具/招数斗气等）；内容走 `content_theme`（默认）或用户场景覆盖。不同画风耦合方式各异，逐条剥离，禁止一律只揪 `xianxia` | 画风污染实际内容（如国漫玄幻厚涂把现代都市场景拉回古代仙侠），跨题材复用失效 |

## 速查表

| 我要 | 读什么 | 什么时候 |
|:-----|:------|:---------|
| 画风DNA库（37种） | `references/style-dna-library.json` | Step 1 |
| 提示词结构+写法 | `../pop-visual-shared/references/seedream-prompt-guide.md` | Step 2 |
| 构图模板+光照模板+兼容性矩阵 | `references/lighting-composition-templates.md` | Step 2 |
| 画风选择流程 | `steps/step1-style-select.md` | Step 1 |
| Pinterest 参考图搜索 | `../pop-visual-shared/scripts/pinterest_search.py` | Step 1 |
| 提示词组装流程 | `steps/step2-prompt-build.md` | Step 2 |
| 生成执行 | `steps/step3-generate.md` | Step 3 |
| 画风定标（按 intent 档位分支） | `steps/step4-style-calibrate.md` | Step 4 |
| 固定画风测试脚本（并发批量） | `../pop-visual-shared/scripts/batch_test.py` | Step 4 |
| 生成图片 | `../pop-visual-shared/scripts/generate.py` | Step 3 |

> **环境**：Python 3.8+ + requests。生图统一走 `image_generate` 工具（不直连 API、无内置 API Key）。

## 跨skill引用协议

art-bible/cover/oc/comic skill引用本skill画风层时：

1. **画风描述**：从 `references/style-dna-library.json` 取 `dna` + `constraint` 字段（**纯技法层**）；取 `content_theme` 作为该画风原生题材的默认内容（跨题材时用各skill的场景描述覆盖）
2. **光照兼容性**：取 `recommended_lighting` 字段，作为光源设计参考
3. **构图参考**：取 `recommended_composition` 字段，作为构图设计参考（不替代各skill自己的构图体系）
4. **提示词组装**：各skill用自己的结构层（V3/4块/三字段），画风段从DNA库取 `dna`+`constraint`（纯技法），内容层独立于画风段，禁止把题材内容混入画风段
5. **画风前置原则**：纯文生图场景，画风DNA放提示词前段；图生图场景按参考点策略处理
6. **画风基线资产**：Pipeline 语境下，画风经定标认可后冻结为基线（`素材/风格/画风决策.md` 标 `✅ 已认可`），下游（art-bible/oc/cover/comic）只消费冻结的画风三字段 + 定标图，禁止各自发明新画风。**按 intent 档位**：`comic`/`full` 必须完整定标门禁+稳定复现；`cover`/`oc` 走 agent 自检分支，定标图达标即标记认可，供下游作画风参考
7. **稳定复现**：下游复现画风时用**冻结的 seed** + 参考图（image 参数），保证画风稳定复现不漂移。seed 和参考图路径从 `画风决策.md` 读取
8. **art-bible 是第一消费方**：L1 基建语境下，画风基线首先被 `pop-visual-art-bible` 消费（画风篇引用 + 定全宇宙色彩基调），再由美术设定集下发给 oc/cover/comic，禁止派生层绕过美术设定集直接读画风决策
