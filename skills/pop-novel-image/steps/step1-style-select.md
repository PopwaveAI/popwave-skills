# Step 1: 画风选择

> 读取DNA库 → 赛道/关键词筛选 → 推荐1-3种 → 用户选择 → 加载光照构图推荐

## 1. 读取画风DNA库

读取 `references/style-dna-library.json`，获取36种画风。

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

## 4. 加载光照构图推荐

取选定画风的：
- `recommended_lighting` → 光照模板（LT1/LT2/LT3）
- `recommended_composition` → 构图模板（CT1/CT2）

**兼容性检查**（铁律❌3）：
- 查 `references/lighting-composition-templates.md` 兼容性矩阵
- 柔美风格（凡妮塔斯/少女水彩/吉卜力等）→ 必须用LT2，禁止LT1
- 平面风格（浮世绘/水墨/版画）→ 必须用LT3
- 暗黑风格 → 用LT1

## 5. 输出

记录到项目文件（`素材/画风选择记录.md`）：
- 选定画风名+类别+keywords
- dna + constraint
- recommended_lighting + recommended_composition
- 兼容性检查结果

## 下一步

→ 进入 `step2-prompt-build.md`，用选定的画风DNA组装6段式提示词
