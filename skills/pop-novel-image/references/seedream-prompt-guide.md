# Seedream 提示词指南

> 本文件是pop-novel-image skill的提示词结构参考，也是cover/oc/comic skill的共享提示词知识源。
> 基于火山引擎方舟平台Seedream 5.0 Pro实测验证（Phase 0-7）。

## 一、6段式提示词结构（默认·纯文生图最优）

> Phase 0验证：结构A（画风优先）为最优解。Phase 6验证：6段式显著提升审美品质，新海诚风格达到Pinterest级A档。

```
[质量触发词] + Art style: [dna] [constraint] + [构图策略] + [光影叙事] + [场景] + [人物≤100字]
```

### 各段说明

| 段 | 内容 | 来源 | 字数控制 |
|:---|:-----|:-----|:---------|
| 1 质量触发词 | `IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed` | 固定 | 固定 |
| 2 画风DNA | `Art style: [dna字段] [constraint字段]` | style-dna-library.json | dna≤800字符 |
| 3 构图策略 | CT1/CT2英文描述 | lighting-composition-templates.md | 固定 |
| 4 光影叙事 | LT1/LT2/LT3英文描述 | lighting-composition-templates.md | 固定 |
| 5 场景 | 画面场景描述（环境/氛围/道具） | 用户输入 | 弹性 |
| 6 人物 | 人物描述（外貌/服饰/姿态/表情） | 用户输入 | ≤100字 |

### 关键原则

1. **画风前置**：画风DNA放第2段（高权重位），不放开头也不放末尾。Seedream注意力权重分配机制——前置信息执行力更强
2. **质量触发词固定**：`IMG_2094.CR2`稳定提升材质和光影35-50%（Phase 3验证）
3. **人物极简**：人物描述≤100字，释放画风表达空间（Phase 3验证）
4. **英文提示词**：Seedream对英文理解精度更高，≤600词
5. **自然语言**：用自然语言连贯描述，不堆叠关键词

### 组装示例

```
IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed.

Art style: Art style from Makoto Shinkai films, ultra-detailed background painting with photorealistic cloud and sky rendering. Vibrant high-saturation palette with signature deep blues, golden hour oranges and emerald greens. Lens flare and backlight halation as recurring motifs. Crystalline light effects, volumetric god rays through clouds. Clean sharp character linework contrasting with painterly environments. 7 head proportion, large expressive eyes with detailed iris reflections. Nostalgic longing, serene melancholy, nature as emotional mirror. Must maintain ultra-detailed background painting. No flat coloring. No rough sketch style. No chibi proportions. Keep photorealistic cloud rendering. No text overlay.

Composition: Vast environment dominates the frame, character is small in the lower third as a scale reference. Negative space above with atmospheric texture and depth. Character faces away from viewer, looking toward the distant horizon. Extreme wide shot, environment as primary subject, figure as narrative anchor.

Lighting: Subtractive lighting, 80% of image in deep atmospheric shadow. Only key features selectively illuminated. Edge rim lighting on silhouette. Darkness as active narrative presence, not absence. Multi-layer fog and atmospheric haze creating depth. Cold dominant palette with single warm focal point ≤10% of frame.

Scene: A lone figure stands on a cliff edge overlooking a vast sea of clouds at sunset. Ancient ruins emerge from the mist below. Flocks of birds circle in the golden distance.

Character: Young man in dark travel-worn cloak, windswept black hair, seen from behind, shoulders relaxed.
```

## 二、V3结构化公式（复杂场景备选）

> 适用于画面包含文字、多人物、多层景深、复杂配色的场景。cover/oc skill在纯文生图模式使用。

```
整体氛围框架（画面是绝对主体）+ 画面内容（远景→前景按层次）+ 文字（最后描述，融入画面）+ 风格
```

**关键规则**：
1. 先整体氛围：一句话定调画面主体性和色彩权重
2. 画面内容按空间层次：从远到近逐层描述
3. 文字最后描述：融入画面层次，不独占空间
4. 配色用"成数"不用百分比："玄黑七成"而非"70%"
5. 指定单一主光源
6. 风格词放末尾（注意：V3中风格在末尾，但6段式中画风在第2段——两者适用场景不同）

## 三、高精度4块结构（商业级备选）

> 适用于需要最高质量输出的场景。新增镜头语言、渲染要求、硬约束。

```
LOCKED COMPOSITION（锁定构图）
  镜头规格 + 角色定位 + 角色外观 + 角色动作 + 背景层次

ENVIRONMENT AND LIGHTING（环境与光影）
  色彩方案 + 光源设计 + 渲染要求

EXACT TYPOGRAPHY AND PLACEMENT（精确文字排版）
  每个文字元素独立描述

HARD CONSTRAINTS（硬约束）
  负面约束清单
```

> 高精度模板的HARD CONSTRAINTS是核心增量——V3公式没有负面约束，模型常出现多指、残肢、文字乱码。硬约束以"禁止"列表形式堵住缺陷。
> 
> cover/oc skill在需要精确文字渲染时使用此结构。本skill纯文生图默认用6段式。

## 四、画风DNA库引用

### 从style-dna-library.json取字段

```json
{
  "凡妮塔斯": {
    "dna": "Art style by Jun Mochizuki...",     // → 第2段
    "constraint": "Must maintain watercolor...", // → 第2段
    "recommended_lighting": "LT2_soft_luminous", // → 第4段
    "recommended_composition": "CT2_silhouette_back" // → 第3段
  }
}
```

### 画风选择逻辑

1. 按赛道筛选：`suggested_genres` 字段匹配用户赛道
2. 按关键词筛选：`keywords` 字段匹配用户描述
3. 取推荐光照和构图：`recommended_lighting` + `recommended_composition`
4. 兼容性检查：查 `lighting-composition-templates.md` 兼容性矩阵

### 跨skill引用协议

cover/oc/comic skill从DNA库取画风时：
- `dna` + `constraint` → 提示词的画风段
- `recommended_lighting` → 光照兼容性参考（不替代各skill自己的光源设计）
- `recommended_composition` → 构图参考（不替代各skill自己的构图体系）
- **画风前置原则**：纯文生图场景画风放前段；图生图按参考点策略

## 五、Seedream通用规则

1. **用自然语言清晰描述画面**：简洁连贯地写明主体+行为+环境+风格
2. **明确应用场景**：在提示中写明图像用途（如"设计一张小说封面"）
3. **文字用双引号包裹**：`"深渊主宰"` 而非 `深渊主宰`
4. **简洁精确优于堆砌**：5.0 Pro画面不再泛白，少描述也能生成符合预期的画面

## 六、图生图能力

### 参考图生图

上传图像作为参考，提示词明确两部分：指明参考对象 + 描述生成画面。

| 参考类型 | 写法 | 应用场景 |
|:---------|:-----|:---------|
| 参考人物形象 | "参考图中的人物形象，生成[新场景]" | 角色换场景 |
| 参考风格 | "参考图标的[风格描述]，设计[新内容]" | 统一视觉风格 |
| 参考款式 | "生成[新内容]，款式与图中[对象]一致" | 同款不同色 |

### 精确分离公式

控制参考图影响范围（只吸收画风不影响构图，或反之）：

```
仅参考此图的[具体要素列表]，不参考[具体排除要素列表]。
以下画面内容完全由本段描述决定：[详细画面描述]
```

### 多图输入

Seedream支持多张参考图，完成替换、组合、迁移等复合编辑。

### 技术注意

`image`参数必须使用data URI格式：`data:image/png;base64,<base64数据>`

## 七、多图输出

通过"一系列""一套""组图"等提示词触发，或用具体数字表明图片数量。

## 八、尺寸参数

| 比例 | 像素值 | 用途 |
|:-----|:-------|:-----|
| 1:1 | 1500x1500 | 方形 |
| 3:4 | 1125x1500 | 竖版 |
| 4:3 | 1500x1125 | 横版 |
| 16:9 | 1500x844 | 宽屏 |
| 9:16 | 844x1500 | 竖版海报 |
| 21:9 | 1500x644 | 超宽 |

> 所有图像输出控制在1500x1500以内。

## 九、避坑清单

| 问题 | 原因 | 解决 |
|:-----|:-----|:-----|
| 画风辨识度不足 | 画风描述放末尾被场景覆盖 | 画风前置到第2段 |
| 水彩/柔美风格崩溃 | 使用了LT1减法照明 | 换LT2柔光通透 |
| 画面泛白发灰 | 旧版模型/堆砌华丽词汇 | 用5.0 Pro，简洁精确 |
| 人物变形 | 缺少稳定性约束 | 添加"五官清晰、人体结构正常" |
| 风格不对 | 风格词模糊 | 从DNA库取具体dna+constraint |
| 文字渲染失败 | 文字未用引号 | 用双引号包裹 |
| 画面缺失元素 | 提示词过长信息分散 | 控制字数，聚焦核心 |
