---
name: pop-visual-style
description: "当用户说'画一张图/生成图片/文生图'或需要纯文生图时启用。管理37种画风DNA库（含IP命名试点）+3光照模板+6段式提示词结构，调用Seedream API生成图片。作为cover/oc/comic skill的共享画风层。"
---

# pop-visual-style

> 通用文生图引擎 + 画风DNA库。纯文生图，一键出图。v1.6.0

## 做什么

输入：画面描述（自然语言）+ 画风选择（从37种DNA库选或自定义）。
输出：生成图片 + 提示词记录。

核心价值：**画风库是营销专家skill群的公共资产**。本skill既独立执行纯文生图任务，又作为cover/oc/comic的画风层引用源。

**与cover/oc/comic的边界**：

| 本skill做 | 本skill不做（交给专用skill） |
|:---------|:---------------------------|
| 画风DNA库管理（37种+扩展） | 封面设计（视觉钩子+文字融入+构图骨架）→ cover |
| 提示词结构知识（6段式/V3/高精度4块） | 立绘设计（六层文字+角色调研+系列冻结）→ oc |
| 光照-画风兼容性矩阵 | 漫画生成（分镜+定妆图+跨章一致性）→ comic |
| 构图模板（CT1/CT2） | 参考图策略（参考点放权）→ cover/oc |
| 纯文生图执行 | Pinterest搜索 → cover/oc |
| 质量触发词+画风前置优化 | 文化元素设计（定场诗/印章）→ cover/oc |

## 模型说明

| 模型 | 用途 | API 端点 | 默认 |
|:-----|:-----|:---------|:----:|
| Seedream 5.0 Pro | 静态图片 | `POST /api/v3/images/generations` | ✅ |
| Seedance 1.0 Pro | 动态视频 | `POST /api/v3/contents/generations/tasks` | ❌ |

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
- 画风DNA从库中取 `dna` + `constraint` 字段，放提示词前段（高权重位）
- 构图从 `references/lighting-composition-templates.md` 取 CT1/CT2 模板
- 光照从同文件取 LT1/LT2/LT3 模板，按兼容性矩阵选择
- 中文提示词 ≤400字，英文 ≤600词

### Step 3: 执行生成 → `steps/step3-generate.md`

- 确定参数（模型/尺寸/输出路径）
- 执行 `../pop-visual-shared/scripts/generate.py`
- 保存图片 + 回写提示词记录

### Step 4: 画风定标 → `steps/step4-style-calibrate.md`（Pipeline 语境下必做）

- **画风×项目角色联合测试**：画风定标默认用**项目主角**当测试素材（`--character` + `--character-image` 图生图保证角色一致），验证"画风能否撑起本项目角色"，而非用中性素材测"画风通用底色"（v1.4.1 升级）
- 走固定脚本 `../pop-visual-shared/scripts/batch_test.py` **并发批量**（固定 6 段式模板 + 默认 8 线程 + 自动 PE 日志），一次出多张变体；变量隔离，唯一变量是画风
- 让画风第一次被眼睛看到，验证 DNA 是否被 Seedream 准确执行
- **🚪 门禁：画风定标验收**（辨识度/配色/光影/无文字）
- **稳定复现验证（核心）**：同 seed + 同脚本重跑对比，确认画风稳定而非单次运气
- 用户认可 → **冻结画风三字段为基线资产**（`素材/风格/画风决策.md` 标 `✅ 已认可`，记录 seed + 参考图路径）
- 未认可 / 未稳定复现 → 回炉微调 DNA 片段（只改变体一个子维度），不冻结、不放行下游
- 独立纯文生图时**跳过本步**（Step 1→2→3 直接出图）

## ❌ 铁律

| # | 铁律 | 违反后果 |
|:-:|:-----|:---------|
| ❌1 | **画风必须从DNA库取** — 禁止凭记忆编画风描述，必须从style-dna-library.json取dna+constraint字段 | 画风辨识度不足，风格漂移 |
| ❌2 | **画风前置** — 画风DNA放提示词前段（第2段），不放开头也不放末尾。Phase 0验证：画风前置符合Seedream注意力权重分配机制 | 画风执行力弱，被场景描述覆盖 |
| ❌3 | **光照兼容性检查** — 选定画风后必须检查recommended_lighting，柔美风格禁用LT1减法照明 | 水彩/柔美风格被暗色吞噬（LT1误用教训） |
| ❌4 | **提示词记录必须落盘** — 画风选择、提示词、参数写入项目文件 | 无法迭代优化 |
| ❌5 | **定标图必须用固定测试素材** — 画风定标时禁止换素材，唯一变量是画风 | 无法判断是画风问题还是素材问题，画风验证失效 |
| ❌6 | **未认可不冻结、不放行下游** — 画风定标图未获用户认可，不得进入基线、不得被下游消费 | 画风问题带病进入角色设计/封面/漫画，返工成本后置 |
| ❌7 | **必须验证稳定复现** — 画风定标必须用同 seed + 同提示词复现对比，未稳定复现不冻结；冻结时记录 seed + 参考图路径 | 画风依赖单次运气，下游无法复现，画风漂移 |
| ❌8 | **参考图是"图资产"单张锚定** — 主路径是整图复用（image 参数），不靠精确分离公式提炼文字；一次搜索、全程复用，禁止重复搜索 | 重复付费 + 文字提炼还原不了参考图，风格失真 |
| ❌9 | **画风定标走固定脚本 `batch_test.py`** — 定标必须用 `../pop-visual-shared/scripts/batch_test.py`（固定素材+固定6段式模板+并发批量+自动PE日志），禁止现场手写提示词、单张串行 | 每次测试变量不隔离、不稳定、慢 |

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
| 画风定标（Pipeline 必做） | `steps/step4-style-calibrate.md` | Step 4 |
| 固定画风测试脚本（并发批量） | `../pop-visual-shared/scripts/batch_test.py` | Step 4 |
| 生成图片 | `../pop-visual-shared/scripts/generate.py` | Step 3 |

> **环境**：Python 3.8+ + requests。API Key 内置在脚本中。

## 跨skill引用协议

cover/oc/comic skill引用本skill画风层时：

1. **画风描述**：从 `references/style-dna-library.json` 取 `dna` + `constraint` 字段
2. **光照兼容性**：取 `recommended_lighting` 字段，作为光源设计参考
3. **构图参考**：取 `recommended_composition` 字段，作为构图设计参考（不替代各skill自己的构图体系）
4. **提示词组装**：各skill用自己的结构层（V3/4块/三字段），画风段从DNA库取
5. **画风前置原则**：纯文生图场景，画风DNA放提示词前段；图生图场景按参考点策略处理
6. **画风基线资产**：Pipeline 语境下，画风经定标认可后冻结为基线（`素材/风格/画风决策.md` 标 `✅ 已认可`），下游只消费冻结的画风三字段 + 定标图，禁止各自发明新画风
7. **稳定复现**：下游复现画风时用**冻结的 seed** + 参考图（image 参数），保证画风稳定复现不漂移。seed 和参考图路径从 `画风决策.md` 读取
