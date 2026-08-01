---
name: pop-novel-image
description: "当用户说'画一张图/生成图片/文生图'或需要纯文生图时启用。管理36种画风DNA库+3光照模板+6段式提示词结构，调用Seedream API生成图片。作为cover/oc/comic skill的共享画风层。"
---

# pop-novel-image

> 通用文生图引擎 + 画风DNA库。纯文生图，一键出图。v1.0.0

## 做什么

输入：画面描述（自然语言）+ 画风选择（从36种DNA库选或自定义）。
输出：生成图片 + 提示词记录。

核心价值：**画风库是营销专家skill群的公共资产**。本skill既独立执行纯文生图任务，又作为cover/oc/comic的画风层引用源。

**与cover/oc/comic的边界**：

| 本skill做 | 本skill不做（交给专用skill） |
|:---------|:---------------------------|
| 画风DNA库管理（36种+扩展） | 封面设计（视觉钩子+文字融入+构图骨架）→ cover |
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

- 读取 `references/style-dna-library.json` 获取36种画风
- 按赛道/关键词筛选推荐1-3种画风
- 用户选择或自定义
- 自动加载该画风的 `recommended_lighting` 和 `recommended_composition`
- **画风-光照兼容性检查**：若画风推荐LT2柔光通透，禁止使用LT1减法照明

### Step 2: 提示词组装 → `steps/step2-prompt-build.md`

- 读取 `references/seedream-prompt-guide.md` 获取提示词结构
- **6段式结构**（纯文生图默认）：`[质量触发词] + Art style: [dna] [constraint] + [构图策略] + [光影叙事] + [场景] + [人物≤100字]`
- 画风DNA从库中取 `dna` + `constraint` 字段，放提示词前段（高权重位）
- 构图从 `references/lighting-composition-templates.md` 取 CT1/CT2 模板
- 光照从同文件取 LT1/LT2/LT3 模板，按兼容性矩阵选择
- 中文提示词 ≤400字，英文 ≤600词

### Step 3: 执行生成 → `steps/step3-generate.md`

- 确定参数（模型/尺寸/输出路径）
- 执行 `scripts/generate.py`
- 保存图片 + 回写提示词记录

## ❌ 铁律

| # | 铁律 | 违反后果 |
|:-:|:-----|:---------|
| ❌1 | **画风必须从DNA库取** — 禁止凭记忆编画风描述，必须从style-dna-library.json取dna+constraint字段 | 画风辨识度不足，风格漂移 |
| ❌2 | **画风前置** — 画风DNA放提示词前段（第2段），不放开头也不放末尾。Phase 0验证：画风前置符合Seedream注意力权重分配机制 | 画风执行力弱，被场景描述覆盖 |
| ❌3 | **光照兼容性检查** — 选定画风后必须检查recommended_lighting，柔美风格禁用LT1减法照明 | 水彩/柔美风格被暗色吞噬（凡妮塔斯D档失败教训） |
| ❌4 | **提示词记录必须落盘** — 画风选择、提示词、参数写入项目文件 | 无法迭代优化 |

## 速查表

| 我要 | 读什么 | 什么时候 |
|:-----|:------|:---------|
| 画风DNA库（36种） | `references/style-dna-library.json` | Step 1 |
| 提示词结构+写法 | `references/seedream-prompt-guide.md` | Step 2 |
| 构图模板+光照模板+兼容性矩阵 | `references/lighting-composition-templates.md` | Step 2 |
| 画风选择流程 | `steps/step1-style-select.md` | Step 1 |
| 提示词组装流程 | `steps/step2-prompt-build.md` | Step 2 |
| 生成执行 | `steps/step3-generate.md` | Step 3 |
| 生成图片 | `scripts/generate.py` | Step 3 |

> **环境**：Python 3.8+ + requests。API Key 内置在脚本中。

## 跨skill引用协议

cover/oc/comic skill引用本skill画风层时：

1. **画风描述**：从 `references/style-dna-library.json` 取 `dna` + `constraint` 字段
2. **光照兼容性**：取 `recommended_lighting` 字段，作为光源设计参考
3. **构图参考**：取 `recommended_composition` 字段，作为构图设计参考（不替代各skill自己的构图体系）
4. **提示词组装**：各skill用自己的结构层（V3/4块/三字段），画风段从DNA库取
5. **画风前置原则**：纯文生图场景，画风DNA放提示词前段；图生图场景按参考点策略处理
