---
id: lighting-composition-templates
lib: 知识库
cat: 视觉
version: 1.0.0
tags: [视觉]
---
# 光照与构图模板库

> 本文件定义3种光照模板（LT1/LT2/LT3）和2种构图模板（CT1/CT2），以及画风-光照-构图兼容性矩阵。数据源：`references/style-dna-library.json`。

## 构图模板

### CT1 尺度操控（Scale Contrast）

**英文描述**（直接拼入提示词）：
```
Composition: Vast environment dominates the frame, character is small in the lower third as a scale reference. Negative space above with atmospheric texture and depth. Character faces away from viewer, looking toward the distant horizon. Extreme wide shot, environment as primary subject, figure as narrative anchor.
```

**适合**：史诗/电影感风格，环境叙事为主的场景
**最佳画风**：新海诚电影风(A)、天野喜孝幻想(B+)、大友克洋硬核、暗黑奇幻油画、经典漫威美漫、好莱坞概念艺术、电影院线海报、超现实梦境、低多边形3D

### CT2 剪影悬念（Silhouette Suspense）

**英文描述**（直接拼入提示词）：
```
Composition: Character shown from behind in three-quarter back view, face partially obscured by shadow and hair. Tight cropping on upper body. Mystery through concealment. Single light source from front creating dramatic backlit silhouette. Rim lighting on shoulders and hair edges. Figure as viewing proxy, audience sees what character sees.
```

**适合**：神秘/氛围感风格，角色代入感强的场景
**最佳画风**：新海诚电影风(A)、哥特暗黑风、黑执事、暗黑悬疑高对比、美漫极简线稿、现代电影感美漫、扁平矢量插画、波普艺术、极简线条插画

> **Phase 6发现**：剪影悬念在缩略图辨识度上普遍优于尺度操控，更适合Pinterest传播。

## 光照模板

### LT1 减法照明（Subtractive Lighting）

**英文描述**（直接拼入提示词）：
```
Lighting: Subtractive lighting, 80% of image in deep atmospheric shadow. Only key features selectively illuminated. Edge rim lighting on silhouette. Darkness as active narrative presence, not absence. Multi-layer fog and atmospheric haze creating depth. Cold dominant palette with single warm focal point ≤10% of frame.
```

**适合**：暗黑/哥特/恐怖/赛博风格
**兼容画风**：新海诚电影风、哥特暗黑风、暗黑奇幻油画、赛博边缘行者、大友克洋硬核、废土末日、暗黑悬疑高对比、韩漫暗黑厚涂、黑执事、蒸汽朋克黄铜、经典漫威美漫、现代电影感美漫、美漫极简线稿、好莱坞概念艺术、电影院线海报、超现实梦境、低多边形3D

> **铁律**：LT1会吞噬水彩/柔美风格，此类风格应改用LT2柔光通透模板。

### LT2 柔光通透（Soft Luminous Lighting）

**英文描述**（直接拼入提示词）：
```
Lighting: Soft luminous lighting with gentle diffused glow. Light emanates from within the image, characters remain visible and readable. Warm ambient light with cool shadow undertones. Backlighting with ethereal halos, golden hour quality. Bokeh and light particles. No crushed blacks, shadows retain color information. Luminous shadows, preserving figure readability even in dark scenes.
```

**适合**：水彩/柔美/治愈/明亮风格
**兼容画风**：少女水彩言情、天野喜孝幻想、轻小说插画风、韩漫华丽言情、穆夏新艺术、日系赛璐珞、京都动画萌系、轻喜剧Q版、韩国Webtoon现代风、新国潮风、迪士尼皮克斯3D、90年代复古动漫、日系热血战斗、伪厚涂半厚涂、国漫玄幻厚涂

> **Phase 7验证**：成功拯救水彩风格(D→B)，轻小说插画风获A档。

### LT3 平光漫射（Flat Atmospheric Lighting）

**英文描述**（直接拼入提示词）：
```
Lighting: Flat even illumination with minimal directional lighting. Light distributed uniformly across the scene, no dramatic shadows. Atmospheric depth through color and mist rather than light/shadow contrast. Subtle ambient occlusion only. Medium-key lighting, neither high nor low contrast. Natural diffuse light like overcast sky or soft window light. Texture and line quality are primary visual carriers, not lighting drama.
```

**适合**：平面/矢量/图形风格
**兼容画风**：扁平矢量插画、波普艺术、极简线条插画

> **Phase 7验证**：保护平面画风线条与色块表达。

## 兼容性矩阵

### 三分法速查

| 光照系 | 光照模板 | 画风系 | 代表画风 |
|:-------|:---------|:-------|:---------|
| 暗黑电影系 | LT1 减法照明 | 暗黑/哥特/赛博 | 新海诚、哥特暗黑、赛博边缘行者、黑执事 |
| 柔美通透系 | LT2 柔光通透 | 水彩/治愈/明亮 | 少女水彩、轻小说、日系赛璐珞、京都动画 |
| 平面系 | LT3 平光漫射 | 平面/矢量/图形 | 扁平矢量(LT3)、波普(LT3)、极简线条(LT3) |

### 特殊画风专属配置

| 画风 | 光照 | 构图 | 说明 |
|:-----|:-----|:-----|:-----|
| 天野喜孝幻想 | LT1或LT2 | CT1 | LT1偏暗黑，LT2偏空灵 |
| 硬朗武侠历史 | LT1 | CT1 | 粗糙硬光配刻刀线条 |

## 使用方法

1. 从 `style-dna-library.json` 取画风的 `recommended_lighting` 和 `recommended_composition`
2. 从本文件取对应模板的英文描述
3. 将英文描述拼入6段式提示词的第4段（光影叙事）和第3段（构图策略）
4. 若画风在特殊系中，按特殊配置选择

## 跨skill引用

cover/oc/comic skill引用本文件时：
- **cover skill**：光源设计表仍由叙事驱动（道具自发光/逆光/顶光等），本文件的光照模板作为画风兼容性参考——选定画风后检查recommended_lighting，避免使用不兼容的光照
- **oc skill**：同cover，立绘的光源以角色表现为优先，但需检查画风兼容性
- **comic skill**：分镜帧的光照直接引用本文件模板，保证画风-光照兼容
