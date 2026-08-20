# Seedream / Seedance 提示词指南（共享权威源）

> 本文件是 **pop-visual-shared 的共享提示词知识源**，被 cover / oc / style / comic 等所有视觉 skill 复用。
> 由 `pop-visual-style` 的"6段式"（Phase 6 验证）与 `pop-visual-oc` 的完整版（V3 结构化公式 + 高精度 4 块模板 + Seedance）合并而成，消除多份副本分化。
> 提示词结构有两条主线：**纯文生图默认走 6 段式；复杂/商业级走 V3 或高精度 4 块**。由各 skill 按场景选用。

---

## 一、6 段式提示词结构（默认 · 纯文生图最优）

> Phase 0 验证：结构 A（画风优先）为最优解。Phase 6 验证：6 段式显著提升审美品质。

```
[质量触发词] + Art style: [dna] [constraint] + [构图策略] + [光影叙事] + [场景] + [人物≤100字]
```

### 各段说明

| 段 | 内容 | 来源 | 字数控制 |
|:---|:-----|:-----|:---------|
| 1 质量触发词 | `IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed` | 固定 | 固定 |
| 2 画风DNA | `Art style: [dna字段] [constraint字段]` | 文风DNA-library.json | dna≤800字符 |
| 3 构图策略 | CT1/CT2 英文描述 | lighting-composition-templates.md | 固定 |
| 4 光影叙事 | LT1/LT2/LT3 英文描述 | lighting-composition-templates.md | 固定 |
| 5 场景 | 画面场景描述（环境/氛围/道具） | 用户输入 | 弹性 |
| 6 人物 | 人物描述（外貌/服饰/姿态/表情） | 用户输入 | ≤100字 |

### 关键原则

1. **画风前置**：画风DNA放第2段（高权重位），不放开头也不放末尾。Seedream 注意力权重分配——前置信息执行力更强
2. **质量触发词固定**：`IMG_2094.CR2` 稳定提升材质和光影 35-50%（Phase 3 验证）
3. **人物极简**：人物描述≤100字，释放画风表达空间
4. **英文提示词**：Seedream 对英文理解精度更高，≤600词
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

---

## 二、V3 结构化公式（复杂场景备选）

> 适用于画面包含文字、多人物、多层景深、复杂配色的场景。cover/oc 在纯文生图模式使用。

```
整体氛围框架（画面是绝对主体）+ 画面内容（远景→前景按层次）+ 文字（最后描述，融入画面）+ 风格
```

**关键规则**：
1. 先整体氛围：一句话定调画面主体性和色彩权重
2. 画面内容按空间层次：从远到近逐层描述
3. 文字最后描述：融入画面层次，不独占空间
4. 配色用"成数"不用百分比："玄黑七成"而非"70%"
5. 指定单一主光源
6. 风格词放末尾（注意：V3 中风格在末尾，但 6 段式中画风在第 2 段——适用场景不同）

---

## 三、高精度 4 块结构（商业级备选）

> 适用于需要最高质量输出的场景（商业级封面、角色立绘加强版、漫画关键帧）。新增镜头语言、渲染要求、硬约束。比 V3 更严谨。

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

### 何时使用

| 场景 | 用 V3 结构化公式 | 用高精度模板 |
|:-----|:----------------:|:------------:|
| 纯文生图封面（无参考图） | ✅ | ✅（质量更高） |
| 图生图封面（有参考图） | ✅ | ❌（参考图已提供结构） |
| 角色立绘（含文字） | ✅ | ✅（文字渲染更精确） |
| 漫画定妆图 | ✅ | ✅（定妆图是跨章基准，值得高精度） |
| 漫画普通分镜帧 | ✅ | ❌（速度优先） |
| 漫画关键帧（高潮/变身/名场面） | ✅ | ✅（值得高精度） |
| 需要精确文字渲染 | ❌ | ✅ |

### 关键规则

- **块1 锁定构图**：镜头规格用具体焦段（"24mm广角"比"广角"精确）；角色外观写皮肤质感和毛孔级细节；服装从外到内逐层写；每只手写具体动作；背景按远→中→近标注虚实
- **块2 环境光影**：光源指定"唯一主光源"；渲染要求列材质清单（fabric weave/leather texture/hair strands/steam particles）；风格参考用标杆作品（"similar to Dark Souls art direction"比"dark fantasy"精确）；特效写粒子级描述
- **块3 精确文字**：每个文字元素用双引号包裹；字体写材质（"weathered metallic serif with gold gradient"）；位置用画面方位词；文字与画面有物理交互
- **块4 硬约束**：负面清单堵住多指/残肢/文字乱码等缺陷，是核心增量。示例：`Exactly one principal character. No duplicated limbs. No flat cel-shaded anime. No text overlay.`

**语言选择**：英文（推荐，≤600词）；中文（纯中文赛道可用，≤400字，材质渲染术语建议混用英文）。

---

## 四、画风 DNA 库引用

> 画风 DNA 统一沉淀到 `pop-visual-style/references/文风DNA-library.json`，含 36 种画风（二次元12 / 国漫5 / 韩漫3 / 插画概念16），每种含 `dna` + `constraint` + `recommended_lighting` + `recommended_composition` 四字段。构图/光影模板见 `pop-visual-style/references/lighting-composition-templates.md`（CT1/CT2 构图 + LT1/LT2/LT3 光影 + 兼容性矩阵）。

### 从 文风DNA-library.json 取字段

```json
{
  "赛博边缘行者": {
    "dna": "Art style from Cyberpunk Edgerunners by Studio Trigger...", // → 第2段
    "constraint": "Must maintain bold outlines and cel-shaded coloring...", // → 第2段
    "recommended_lighting": "LT1_subtractive", // → 第4段
    "recommended_composition": "CT2_silhouette_back" // → 第3段
  }
}
```

### 画风选择逻辑

1. 按赛道筛选：`suggested_genres` 字段匹配用户赛道
2. 按关键词筛选：`keywords` 字段匹配用户描述
3. 取推荐光照和构图：`recommended_lighting` + `recommended_composition`
4. 兼容性检查：查 `lighting-composition-templates.md` 兼容性矩阵

### 跨 skill 引用协议

cover/oc/comic 从 DNA 库取画风时：
- `dna` + `constraint` → 提示词的画风段
- `recommended_lighting` → 光照兼容性参考（不替代各 skill 自己的光源设计）
- `recommended_composition` → 构图参考（不替代各 skill 自己的构图体系）
- **画风前置原则**：纯文生图场景画风放前段；图生图按参考点策略

---

## 五、Seedream 通用规则

1. **用自然语言清晰描述画面**：简洁连贯地写明主体+行为+环境+风格
2. **明确应用场景**：在提示中写明图像用途（如"设计一张小说封面"）
3. **文字用双引号包裹**：`"深渊主宰"` 而非 `深渊主宰`
4. **简洁精确优于堆砌**：5.0 Pro 画面不再泛白，少描述也能生成符合预期的画面
5. **风格用精准词或参考图**：明确风格需求时，用精准风格词或提供参考图
6. **图生图编辑用明确指令**：说明修改/参考对象及具体操作，避免模糊代词

---

## 六、图生图能力

### 参考图生图

上传图像作为参考，提示词明确两部分：指明参考对象 + 描述生成画面。

| 参考类型 | 写法 | 应用场景 |
|:---------|:-----|:---------|
| 参考人物形象 | "参考图中的人物形象，生成[新场景]" | 角色换场景 |
| 参考风格 | "参考图标的[风格描述]，设计[新内容]" | 统一视觉风格 |
| 参考款式 | "生成[新内容]，款式与图中[对象]一致" | 同款不同色 |

### 画风参考：放开吸收（默认推荐，实测验证）

当用户参考点为"画风"时，默认使用放开吸收公式。核心是**正向吸收 + 最小排除**——不要堆"不参考"清单，否则等于没参考（实测吸收被抑制）。

```
参考这张图的[画风质感、色彩系统、光影氛围]：柔和数字插画笔触，painterly soft-focus质感，人物精致细腻的画风，[色彩倾向描述]，[光影氛围描述]。
仅排除图中具体场景内容和人物长相——场景里的物品、环境元素、人物五官长相不参考。
以下画面内容完全由本段描述决定：[目标画面详细描述]
```

**关键原则**：
1. 正向吸收：明确列出要吸收的要素——画风质感（笔触/渲染）+ 色彩系统（色调倾向/饱和度/明暗）+ 光影氛围（光源/氛围/空气感）+ 人物精致度
2. 最小排除：只排除两样——具体场景内容（场景物品/环境元素）和人物长相（五官/脸型）。姿态、服饰、构图、色彩都允许参考图自然传导
3. 吸收要素落到具体词（笔触技法/色彩倾向/光影语言/人物精致度），不写"参考风格"这种模糊词
4. 明确声明"以下画面内容由描述决定"，保证主体内容（书名/人物/构图）由提示词控制

> **实测结论**（R14 言情封面）：放开吸收后画风传递显著增强（柔和 painterly 笔触、通透光效、暖色调过渡、光斑粒子均明显从参考图传导），同时三人三角站位和人物动作仍由提示词精确控制。早期"精确分离公式"（排除人物/姿态/服饰/场景/构图/配色）画风吸收被抑制，用户反馈"等于没参考"。

### 精确分离公式（高级控制，仅在确需阻止特定元素泄漏时使用）

当必须精确控制参考图影响范围（例如只吸收构图、禁止任何色彩/画风传导，OC/角色一致性场景）时，才用精确分离：

```
仅参考此图的[具体要素列表]，不参考[具体排除要素列表]。
以下画面内容完全由本段描述决定：[详细画面描述]
```

**关键原则**：
1. 画风要素拆解到**笔触技法、色彩系统、明暗方式**层面（不写"参考风格"这种模糊词）
2. 构图要素拆解到**人物数量、位置关系、空间布局**层面（不写"参考构图"这种模糊词）
3. 明确声明"以下画面内容由描述决定，与参考图无关"

**模式一：只吸收画风（仅在确需完全隔离内容时使用）**
```
仅参考此图的[笔触技法A、笔触技法B]和色彩系统（[主色调描述]、[点缀色描述]），
不参考图中的人物形象、姿态动作、服饰道具、场景环境、构图布局。
以下画面内容完全由本段描述决定：[目标画面详细描述]
```

**模式二：构图互换（需强化控制）**
```
仅参考此图的构图布局：[人物数量+位置关系+空间层次的具体描述]，
不参考图中的人物服饰、色彩配色、场景环境、笔触风格。
以下画面的画风和色彩完全由本段描述决定：[目标画风+色彩详细描述]
```

> **选择指引**：封面/场景图等追求画风传导时，用"放开吸收"；角色一致性、需完全隔离画面主体时，才用"精确分离"。

> **技术注意**：`image` 参数必须使用 data URI 格式 `data:image/png;base64,<base64数据>`，不能传裸 base64。

### 多图输入

Seedream 支持多张参考图，完成替换、组合、迁移等复合编辑。提示词中需清楚指明不同图像需要编辑/参考的对象及操作。

| 操作 | 提示词写法 | 网文应用场景 |
|:-----|:-----------|:-------------|
| 替换 | 将图一的主体替换为图二的主体 | 角色换脸、场景换人 |
| 组合 | 让图一人物穿上图二的服装 | 人设图换装 |
| 迁移 | 参考图二的风格，对图一进行风格转换 | 封面风格统一化 |

---

## 七、多图输出

通过"一系列""一套""组图"等提示词触发，或用具体数字表明图片数量。适用于分镜、漫画创作、成套视觉设计。

---

## 八、尺寸参数

| 比例 | 像素值 | 用途 |
|:-----|:-------|:-----|
| 1:1 | 1500x1500 | 正方形 |
| 3:4 | 1125x1500 | 竖版封面 |
| 4:3 | 1500x1125 | 横版封面 |
| 16:9 | 1500x844 | 宽屏 banner |
| 9:16 | 844x1500 | 竖版海报/全身立绘 |
| 21:9 | 1500x644 | 超宽 banner |

> **铁律：所有出图总像素必须 ≤ 236 万（Seedream 5.0 Pro 计费临界，超 236 万像素报价从 0.3 元/张翻倍到 0.6 元/张）。** 上表全部在安全范围内（最大 1500x1500=225 万）。生图统一走 `image_generate` 工具，按上表传 `size`，用工具前人工核对总像素 ≤ 236 万。分辨率档位仅支持 `1K`（1024x1024=105 万）；`2K`/`4K` 均超上限，禁止使用。脚本 `generate.py`/`batch_test.py` 内置 `assert_size_safe` 校验，超限导出时直接报错中止。

---

## 九、Seedance 1.0 Pro 提示词指南（视频生成）

### 9.1 通用规则

- 中文提示词 ≤500 字，英文 ≤1000 词
- 支持文生视频、图生视频（首帧/首尾帧）
- 动作描述要"碎"要"慢"

### 9.2 提示词公式

```
[主体] + [动作（慢、连贯）] + [场景] + [光影] + [镜头语言] + [风格] + [画质] + [稳定性约束]
```

### 9.3 核心技巧

- **动作描述**：推荐"缓慢、轻柔、连贯、自然、流畅、不僵硬、轻轻抬手、脚步轻移"；避免"跳舞、跑步、高速、复杂互动、大幅度扭曲"
- **镜头与运镜**：景别（特写/近景/中景/全景）；动效（缓慢推镜/平稳横移/环绕/稳定跟拍）；强制指令（固定镜头、无抖动、丝滑流畅）
- **角色稳定约束**：五官清晰、面部稳定、不扭曲、人体结构正常、比例自然、同一角色、服装一致、发型不变
- **画质词**：4K、超高清、细节丰富、无模糊、无重影、无闪烁
- **多镜头叙事**（Seedance 1.0 Pro 独有）：用"镜头切换"连接多个场景，每次切镜后可刻画新出现的人物/场景特征

### 9.4 视频参数

| 参数 | 选项 | 默认 |
|:-----|:-----|:----:|
| ratio | 1:1 / 3:4 / 4:3 / 16:9 / 9:16 / 21:9 | 16:9 |
| duration | 4-10 秒 | 5 |
| resolution | 480p / 720p / 1080p | 1080p |
| camera_fixed | true / false | false |

---

## 十、避坑清单

| 问题 | 原因 | 解决 |
|:-----|:-----|:-----|
| 画风辨识度不足 | 画风描述放末尾被场景覆盖 | 画风前置到第2段 |
| 水彩/柔美风格崩溃 | 使用了LT1减法照明 | 换LT2柔光通透 |
| 画面泛白发灰 | 旧版模型/堆砌华丽词汇 | 用5.0 Pro，简洁精确 |
| 人物变形 | 缺少稳定性约束 | 添加"五官清晰、人体结构正常" |
| 风格不对 | 风格词模糊 | 从DNA库取具体dna+constraint |
| 文字渲染失败 | 文字未用引号 | 用双引号包裹 |
| 画面缺失元素 | 提示词过长信息分散 | 控制字数，聚焦核心 |