---
name: pop-visual-cover
description: "当用户说'网文封面/小说封面/场景图/视觉设计'或提供小说原文时启用。支持两种起点：①用户意图→Pinterest搜参考→选图+对齐参考点→设计方案；②小说原文→原文解构→上下文补全→叙事瞬间选取→理解确认→设计方案。调用 Seedream/Seedance API 生成图片/视频。"
---

# pop-visual-cover

> 网文封面与场景视觉资产生成器。两种起点，同一个终点。v1.8.0

## 做什么

输入：小说项目文件 + 视觉需求（封面/场景图/素材）+ 可选参考图或原文。
输出：生成图片/视频 + 设计方案文档 + 提示词记录。

核心价值：帮用户把模糊画面变成可执行的参考图和参考点，再翻译为模型提示词。**两个用户对齐门禁**确保方向不跑偏。

**三段流程**：
1. 用户意图 →（意图分析+Pinterest 搜索 / 原文理解管线）→ **门禁A：选图+对齐参考点 或 理解确认**
2. 参考图+参考点 →（设计画面差异）→ **门禁B：方案对齐**
3. 确认方案 →（参考点驱动提示词策略）→ API 生成

## 模型说明

| 生成内容 | 工具/方式 | 说明 |
|:-----|:---------|:-----|
| 静态图片（Seedream 5.0 Pro） | `image_generate` 工具 | 文生图/图生图/多图输入，无 API Key |
| 动态视频（Seedance 1.0 Pro） | `generate.py video` | 需显式设置 `ARK_API_KEY` 环境变量，不内置 key |

Seedream 5.0 Pro 画面不再泛白，简洁精确优于堆砌。支持文生图、图生图、多图输入。文字用双引号包裹。

## 怎么运作

### Step 0: 意图分析 + 搜图 + 选图对齐 → `steps/step0-research.md`
### Step 0-Scene: 原文理解管线（场景图模式）→ `steps/step0-scene-understand.md`

- **优先读取 `素材/视觉资产/` 下的资产文件**（pop-visual-asset 产出）：场景资产表→帧解构、角色档案→角色规格、视觉符号库→环境材质、IP视觉DNA→IP背景
- **角色本体身份以 `pop-visual-art-bible` 产出的「美术设定集·人物篇」为唯一真源**：封面只要出现角色，就读取 `素材/美术设定集.md` 的人物篇作为角色本体（剪影/色彩/细节/记忆锚点/冻结提示词），本模式只负责把角色放进封面构图，**禁止重建角色身份**。美术设定集缺失时提示先跑 `pop-visual-art-bible`。
- **档位说明（cover 意图 = 轻量基建）**：Pipeline 语境下 cover 只需基建到美术设定集即可派生，**不强制双角度定妆**；如需角色参考图，用 art-bible 产出的**单张**定妆图作图生图参考即可。
- 资产缺失时回退到原流程（原文解构/WebSearch）

- 提取视觉意图（赛道+气质关键词+目标读者画像+视觉类型+书名）
- **视觉模式判定**：封面图 / 普通素材 / 场景图
- Pinterest 3维度搜索（风格/角色/IP，每维度2-3个英文表达并行，合计6张）
- **🚪 门禁A**：用户选参考图+对齐参考点（全面参考/色系/构图/画风/光影/字体/组合）
- **场景图模式**：原文解构→上下文补全→叙事瞬间选取→门禁A（理解确认，非选图）

### Step 1: 设计方案 → `steps/step1-design.md`

- 基于参考图+参考点，设计需要改动的部分
- 参考点决定描述范围（全面参考=只写差异；色系=不写配色）
- 形成人可读设计方案（全部人话，非技术prompt）
- **🚪 门禁B**：用户确认设计方案

### Step 2: 生成资产 → `steps/step2-generate.md`

- 读取确认方案 + 参考点
- **参考点→提示词策略**：用户选了什么参考点，提示词就在那个维度**放弃控制权**
- 翻译为 Seedream/Seedance 提示词 → 执行 API → 保存图片 → 回写记录
- 降级机制：太像→收窄参考点；放权维度失控→降级为控制
- **品牌水印（必做）**：封面是**对外展示产出**，落地后用共享脚本叠加半透明 `popwave.cn`：`python skills/pop-visual-shared/scripts/watermark.py '<图路径>'`（幂等，二次运行输出"已含水印，跳过"）

### 迭代模式（快速路径）

**当用户要求修改已生成的图片时**，**跳过 Step 0 和 Step 1**，直接执行：

1. 读取 `_过程/提示词记录.md` 获取上一版设计方案+提示词记录
2. 识别用户要求的变更点
3. 直接进入 `steps/step2-generate.md`，在上一版提示词基础上修改对应维度
4. 执行 API 生成（文件名递增 v2, v3...）
5. 回写提示词记录

> 仅当用户明确要求"重新设计/换方向/换赛道"时，才回到完整三段流程。

## ❌ 铁律

| # | 铁律 | 违反后果 |
|:-:|:-----|:---------|
| ❌1 | **先搜图选图再出方案** — 必须先搜参考图、用户选图+对齐参考点，再设计方案 | 设计方向跑偏 |
| ❌2 | **两个门禁不可跳过** — 门禁A和门禁B必须等用户确认后才能继续 | 方向跑偏，浪费生成次数 |
| ❌3 | **参考点放权一致性** — 用户选了什么参考点，提示词就在那个维度放弃控制权（画风参考=放开吸收，只排除具体场景内容+人物长相，禁止堆"不参考"清单） | 提示词与参考图矛盾 |
| ❌4 | **设计方案必须落盘三态** — 选图记录、参考点、设计方案和提示词写入 `_过程/提示词记录.md`；候选图落 `测试/封面/`，确认后复制到 `成品/封面/`（加 `-final`） | 无法迭代优化 |
| ❌5 | **场景图必须经过理解管线** — 用户提供原文时，必须经过原文解构→上下文补全→叙事瞬间选取→门禁A | 理解偏差，精确地画错画面 |
| ❌6 | **对外产出必加品牌水印** — 封面/场景图落地后必须运行 `watermark.py` 叠加 `popwave.cn`（幂等，二次运行输出"已含水印，跳过"）；禁止跳过此步 | 发布图无溯源，品牌曝光丢失 |

## 速查表

| 我要 | 读什么 | 什么时候 |
|:-----|:------|:---------|
| 联网搜索+选图对齐 | `steps/step0-research.md` | Step 0 |
| 场景图理解管线 | `steps/step0-scene-understand.md` | 场景图模式（替代标准Step 0） |
| 设计方案 | `steps/step1-design.md` | Step 1 |
| 生成+提示词翻译 | `steps/step2-generate.md` | Step 2 |
| 设计封面图 | `references/mode-cover.md` | 封面图模式时 |
| 设计普通素材 | `references/mode-scene-art.md` | 普通素材模式时 |
| 设计场景图 | `references/mode-scene.md` | 场景图模式时 |
| 视觉钩子+构图骨架库 | `references/novel-visual-design.md` §二§三§四 | Step 1 |
| 文化元素（定场诗/印章） | `references/novel-visual-design.md` §八 | Step 1 |
| 提示词写法+控制公式 | `../pop-visual-shared/references/seedream-prompt-guide.md` | Step 2 |
| 画风DNA库（36种+光照兼容性） | `skills/pop-visual-style/references/文风DNA-library.json` | Step 2 |
| 光照-构图模板+兼容性矩阵 | `skills/pop-visual-style/references/lighting-composition-templates.md` | Step 2 |
| 生成图片 | `image_generate` 工具 | Step 2 |
| 叠加品牌水印（必做） | `../pop-visual-shared/scripts/watermark.py` | Step 2 落地后 |
| 搜 Pinterest | `../pop-visual-shared/scripts/pinterest_search.py` | Step 0 |
| 设计方案模板 | `templates/design-plan.tpl.md` | Step 1 |

> **环境**：Python 3.8+ + requests。API Key 内置在脚本中。Pinterest 下载三层 fallback（本地代理→Bright Data→优雅降级保留URL）。
