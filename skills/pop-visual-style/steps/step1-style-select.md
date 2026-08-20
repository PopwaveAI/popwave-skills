# Step 1: 画风选择

> 读取DNA库 → 赛道/关键词筛选 → 推荐1-3种 → 用户选择 → 加载光照构图推荐

## 1. 读取画风DNA库

读取 `references/文风DNA-library.json`，获取37种画风（含IP命名试点「双城之战」）。

## 2. 筛选推荐

按用户需求筛选：

**按赛道**：匹配 `suggested_genres` 字段
**按关键词**：匹配 `keywords` 字段
**按类别**：二次元(17) / 国漫(6) / 韩漫(3) / 插画概念(10)

推荐1-3种画风，附推荐理由（视觉特征+代表作+适合赛道）。

## 3. 用户选择

用户可选池中画风，或描述自定义风格。

**自定义画风处理**：
- 按DNA库格式组装：`dna`（英文画风描述≤800字符）+ `constraint`（风格保真约束）
- 需在生成后验证辨识度，未达标则调整dna描述

## 4. Pinterest 参考图搜索（单张锚定）

> 搜索有成本（Bright Data 付费），**一次搜索、全程复用**。选定画风后搜 1 张最符合画风的参考图，作为全书风格准绳。参考图是"图资产"——靠整图作为 image 参数复用，不靠文字提炼。

**执行**：
```powershell
python ../pop-visual-shared/scripts/pinterest_search.py "画风关键词" --limit 5 --max-results 5 --download --output-dir "素材/ref-cache/"
```

- 关键词：画风名 + 赛道 + 主要特征（如"暗黑修仙厚涂 玄幻 封面"）
- 从结果中选 **1 张最符合画风**的参考图（单张锚定）
- 删掉其余候选，只保留 1 张，避免多图不确定性

**落盘**：参考图路径记入 `素材/风格/画风决策.md` 的 `参考图` 字段，作为基线索引。

> **铁律**：参考图是"图资产"，主路径是整图复用（image 参数），不靠精确分离公式提炼成文字。精确分离公式只在"需要把风格迁移到新内容"时作辅助。

## 5. 加载光照构图推荐

取选定画风的：
- `recommended_lighting` → 光照模板（LT1/LT2/LT3）
- `recommended_composition` → 构图模板（CT1/CT2）
- `content_theme` → **该画风原生题材的默认内容层**（供 Step 2 场景段兜底；跨题材时由用户场景覆盖）

**兼容性检查**（铁律❌3）：
- 查 `references/lighting-composition-templates.md` 兼容性矩阵
- 柔美风格（少女水彩/轻小说/日系赛璐珞等）→ 必须用LT2，禁止LT1
- 平面风格（扁平矢量/波普/极简线条）→ 必须用LT3
- 暗黑风格 → 用LT1

## 6. 输出

记录到项目文件（`素材/画风选择记录.md`）：
- 选定画风名+类别+keywords
- dna + constraint（**纯技法层，禁止混入内容**）
- content_theme（原生题材默认内容层）
- recommended_lighting + recommended_composition
- 兼容性检查结果

## 下一步

→ 进入 `step2-prompt-build.md`，用选定的画风DNA组装6段式提示词
