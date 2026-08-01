# Seedream / Seedance 提示词指南

> 本文件整合火山引擎方舟平台 Seedream（图片生成）和 Seedance（视频生成）的官方提示词指南，作为 Step 2 翻译环节的参考依据。
>
> Seedream 部分基于官方文档（doc 1829186）整理，覆盖 5.0 lite / 4.5 / 4.0 三个版本。

## 一、Seedream 提示词指南（图片生成）

适用版本：Seedream 5.0 Pro、5.0 lite

### 1.1 通用规则

1. **用自然语言清晰描述画面**

   用**简洁连贯**的自然语言写明 **主体 + 行为 + 环境**，若对画面美学有要求，可用自然语言或短语补充 **风格**、**色彩**、**光影**、**构图** 等美学元素。

   - ✅ 示例：一个穿着华丽服装的女孩，撑着遮阳伞走在林荫道上，莫奈油画风格。
   - ❌ 避免：一个女孩，撑伞，林荫街道，油画般的细腻笔触。

2. **明确应用场景和用途**

   当有明确的应用场景时，推荐在文本提示中写明图像用途和类型。

   - ✅ 示例：设计一张网文小说封面，主体是一个黑衣剑客站在悬崖上
   - ❌ 避免：一张抽象图片，剑客，悬崖

3. **提升风格渲染效果**

   如果有明确的风格需求，使用精准的 **风格词** 或提供 **参考图像**，能获得更理想的效果。

4. **提高文本渲染准确度**

   建议将要生成的 **文字内容** 放在 **双引号** 中。

   - ✅ 海报标题为 "深渊主宰"
   - ❌ 海报标题为深渊主宰

5. **明确图片编辑目标和保持不变的部分**

   使用 **简洁明确的指令**，说明需要修改或参考的对象及具体操作，避免使用指代模糊的代词；如果希望除了修改的内容都保持不变，则可以在 prompt 中强调。

   - ✅ 让图中最高的那只熊猫穿上粉色的京剧服饰并戴上头饰，并保持动作不变。
   - ❌ 让它穿上粉色衣服。

### 1.2 关键特性

> Seedream 5.0 Pro、5.0 lite 对文本提示的理解能力更强，能够在较少描述的情况下生成符合预期的画面，且**画面不再泛白**，因此在使用该模型时采用**简洁精确的提示通常优于重复堆叠华丽复杂的词汇**。

中文提示词 ≤300 字，英文 ≤600 词。

### 1.3 提示词公式

#### 基础公式（简单场景）

```
[主体描述] + [行为/姿态] + [环境/场景] + [光影] + [色彩] + [构图] + [风格]
```

#### 结构化公式（复杂封面/商业级，5.0 Pro 实测验证）

```
构图骨架（类型+空间关系）+ 配色比例（色名+成数）+ 光源设计（单一主光源）+ 画面内容（按空间层次）+ 风格
```

> **何时用结构化公式**：画面包含书名文字、多人物、多层景深、复杂配色时。结构化公式通过显式编码构图骨架、配色比例、光源设计，使纯文生图达到接近参考图生图的质量（A 级商业封面，4.2/5）。

**结构化公式关键规则**：
1. 构图骨架：命名类型（L型/对角线/分层/中心放射）+ 空间关系（远景/中景/近景）
2. 配色用"成数"：写"玄黑六成"而非"玄黑占60%"——模型理解成数但不理解百分比
3. 光源设计：指定"为画面唯一主光源"，避免多光源混乱
4. 群像处理：用阵型+光照统一（如"倒三角站位，背光剪影"），避免个体崩坏
5. 字体锚点：书名用双引号 + "占画面高度X成"给尺寸锚点 + 材质质感

**结构化公式示例**：
> 设计一张修仙小说封面，竖版构图。左侧竖排书名 "玄鉴仙族" 四字占画面高度七成，鎏金毛笔书法体，笔画飞白明显，金石碑刻龟裂质感。右侧上方族长侧脸半身像，玄色暗金纹路长袍，面容冷峻。身后破碎古镜悬浮，青绿光呈放射状爆发，为画面唯一主光源。中景三名修士倒三角站位，背光剪影，执剑施法。远景暗紫雷云与崩塌仙山。底部废墟剪影压边。配色比例：玄黑六成为底，青绿两成半为灵力光效，鎏金一成为文字纹饰，朱砂红点缀。暗黑奇幻国风厚涂风格。

### 1.4 文生图技巧

采用清晰明确的自然语言描述画面内容，对于细节比较丰富的图像，可通过详细的文本描述精准控制画面细节。

Seedream 可将知识与推理结果转化为高密度图像内容（如公式、图表、教学插图），生成时应明确使用**专业术语**，确保知识点表达准确。

**人物外形精细化**：用自然语言精细刻画人物细节。
- "一个脸型微胖的年轻女人，三白眼，眼角边有一颗痣，皮肤粗糙"
- "一个发型凌乱的男人，穿着破旧的长衫"

**画面氛围控制**：用视频类型或自然语言形容氛围。
- "油画般的电影场景" / "有质感的老电影，复古氛围" / "略显古早的80年代电视剧"
- 正向氛围："温馨""治愈""史诗感"
- 负向氛围："压抑""诡异""破败"

### 1.5 图生图能力（重要）

Seedream 支持结合文本与图片完成图像编辑和参考生成任务，并可通过**箭头**、**线框**、**涂鸦等视觉信号**控制画面区域，实现可控生成。

#### 1.5.1 图像编辑（增删替换改）

| 操作 | 写法 | 示例 |
|:-----|:-----|:-----|
| 增加 | 给图中[对象]增加[元素] | 给图中女生增加相同款式的银色耳线和项链 |
| 删除 | 去掉[对象]的[元素] | 去掉女生的帽子 |
| 替换 | 把[对象]换成[新元素]，保持[不变项] | 把最大的面包人换成牛角包形象，保持动作和表情不变 |
| 修改 | 让图中[对象]变成[新状态] | 让图中三个机器人变成透明水晶材质，颜色从左到右分别变成红黄绿 |

当画面内容复杂难以用文本准确描述编辑对象时，可采用**涂鸦**、**线框**等方式指明编辑对象和位置。

#### 1.5.2 参考图生图

当有明确需保持的特征（角色形象、视觉风格、产品设计）时，可上传图像作为参考。提示词需明确两部分：

1. **指明参考对象**：清晰描述希望从参考图中提取并保留的元素
2. **描述生成画面**：具体说明希望生成的画面内容、场景等细节

| 参考类型 | 提示词写法 | 网文应用场景 |
|:---------|:-----------|:-------------|
| 参考人物形象 | "参考图中的人物形象，生成[新场景]" | 用角色参考图生成不同场景封面 |
| 参考风格 | "参考图标的[风格描述]，设计[新内容]" | 统一整套视觉物料风格 |
| 参考虚拟实体形象 | "图中的形象变成[新材质/形态]" | 角色手办化、Q版化 |
| 参考款式 | "生成[新内容]，款式与图中[对象]一致" | 同款不同色的角色服装 |

##### 精确分离公式（实测验证）

当需要精确控制参考图的影响范围（只吸收画风不影响构图，或构图互换）时，用以下公式：

```
仅参考此图的[具体画风/构图要素列表]，不参考[具体排除要素列表]。
以下画面内容完全由本段描述决定：[详细画面描述]
```

**关键原则**：
1. 画风要素拆解到**笔触技法、色彩系统、明暗方式**层面（不写"参考风格"这种模糊词）
2. 构图要素拆解到**人物数量、位置关系、空间布局**层面（不写"参考构图"这种模糊词）
3. 明确声明"以下画面内容由描述决定，与参考图无关"

**模式一：只吸收画风（高度可靠，实测吸收率 75-90%）**

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

**反向强化技巧**（当参考图影响过强、目标画风被覆盖时）：
1. 将目标画风描述提到提示词最前面（增加权重）
2. 用量化词："占比不低于40%""大面积"
3. 用禁止词："完全不使用[参考图的色彩]""禁止[参考图的技法]"
4. 用具体色名替代笼统描述："朱砂红"而非"红色"

> **技术注意**：`image` 参数必须使用 data URI 格式 `data:image/png;base64,<base64数据>`，不能传裸 base64。

#### 1.5.3 设计草图生成

当需要根据设计草图（如平面图、线稿图、手绘原型）生成高保真效果图时：
1. 提供清晰的原始图片，若图中有文字说明，则在提示中注明"遵循图中文字内容进行生成"
2. 明确主体与要求（如高保真 UI 界面、现代简约风格客厅实景图）
3. 明确指出需与参考图保持一致的关键要求（如家具位置与参考图一致、按照原型图的布局）

#### 1.5.4 多图输入

Seedream 支持同时输入多张图像，完成**替换**、**组合**、**迁移**等复合编辑操作。提示词中需清楚指明不同图像需要编辑/参考的对象及操作：

| 操作 | 提示词写法 | 网文应用场景 |
|:-----|:-----------|:-------------|
| 替换 | 将图一的主体替换为图二的主体 | 角色换脸、场景换人 |
| 组合 | 让图一人物穿上图二的服装 | 角色换装 |
| 迁移 | 参考图二的风格，对图一进行风格转换 | 封面风格统一化 |

### 1.6 多图输出（组图生成）

Seedream 支持生成角色连贯、风格统一的图像序列，适用于分镜、漫画创作，以及需要统一视觉风格的成套设计场景。

通过"一系列""一套""组图"等提示词触发，或采用具体数字表明图片数量。

网文应用场景：
- 一套角色表情包（"生成一套角色的6个表情包"）
- 分镜封面组图（"生成四张图，分别对应角色的四个标志性行为"）
- 多角色组图（"生成三个角色的全身图，风格统一"）

### 1.7 尺寸参数

| 比例 | 宽高像素值（≤1500） | 用途 |
|:-----|:---------------------|:-----|
| 1:1 | 1500x1500 | 头像/方形 |
| 3:4 | 1125x1500 | 竖版封面 |
| 4:3 | 1500x1125 | 横版封面 |
| 16:9 | 1500x844 | 宽屏banner |
| 9:16 | 844x1500 | 竖版海报/手机壁纸 |
| 21:9 | 1500x644 | 超宽banner |

也可使用分辨率档位：`1K` / `2K` / `4K`（需在 prompt 中用自然语言描述宽高比）。

### 1.8 网文封面提示词模板

**修仙/玄幻封面**：
```
一个[外貌特征]的[角色身份]，[姿态动作]，[场景环境]。[光影描述]，[色彩方案]，[构图说明]。[风格词]风格，竖版构图，上方留白。
```

**都市/异能封面**：
```
一个[外貌特征]的[角色身份]站在[城市场景]，[姿态动作]，[氛围描述]。[光影方向]，[色彩方案]，[构图说明]。[风格词]风格，竖版构图。
```

**言情/古言封面**：
```
[角色性别]身穿[服饰描述]，[姿态动作]，[场景环境]。[光影氛围]，[色彩方案]，[情绪基调]。[风格词]风格，竖版构图，上方留白预留书名。
```

### 1.10 高精度提示词模板（商业级）

> 基于实测验证的工程图纸级写法。适用于商业级封面、漫画关键帧等需要最高质量输出的场景。比 V3 结构化公式更严谨，新增镜头语言、渲染要求、硬约束三个维度。

#### 何时使用

| 场景 | 用 V3 结构化公式 | 用高精度模板 |
|:-----|:----------------:|:------------:|
| 纯文生图封面（无参考图） | ✅ | ✅（质量更高） |
| 图生图封面（有参考图） | ✅ | ❌（参考图已提供结构） |
| 漫画定妆图 | ✅ | ✅（定妆图是跨章基准，值得高精度） |
| 漫画普通分镜帧 | ✅ | ❌（速度优先） |
| 漫画关键帧（高潮/变身/名场面） | ✅ | ✅（值得高精度） |
| 需要精确文字渲染 | ❌ | ✅ |

#### 4 块结构

高精度模板由 4 个命名块组成，每块有明确的职责边界：

**块1：LOCKED COMPOSITION（锁定构图）**

编码画面的空间结构，包括镜头、角色位置、详细外观、背景层次。

```
LOCKED COMPOSITION:

[镜头规格]：焦段（24mm广角/35mm/50mm）+ 机位（平视/仰角/俯角）+ 位置描述
[角色定位]：角色在画面中的位置 + 占比 + 朝向
[角色外观]：年龄+种族+发型发色+眼瞳色+面部特征+皮肤质感+表情+服装（从外到内每层）+配饰+手持道具
[角色动作]：每只手的具体动作 + 身体姿态
[背景层次]：远景元素+位置+虚实 → 中景元素+位置 → 前景元素
```

关键规则：
1. 镜头规格用具体焦段——"24mm广角"比"广角镜头"更精确
2. 角色外观写皮肤质感和毛孔级别细节——"fair skin, subtle skin texture, realistic pores"
3. 服装从外到内逐层写——coat → shirt → belt → trousers → boots
4. 每只手都要写具体动作——"left hand rests on the cutlass hilt; right hand raised, palm upward"
5. 背景按远→中→近层次，标注虚实——"slightly out of focus" / "sharp focus"

**块2：ENVIRONMENT AND LIGHTING（环境与光影）**

编码色彩、光源、渲染要求。

```
ENVIRONMENT AND LIGHTING:

[色彩方案]：主色+辅色+点缀色，用具体色名（navy blue/charcoal black/ocean gray）
[光源设计]：方向+类型+色温+强度（"warm golden rim light from behind-left"）
[渲染要求]：材质质感列表（fabric weave/leather texture/hair strands/steam particles）+ 风格参考 + 画质标准
```

关键规则：
1. 光源指定"唯一主光源"——避免多光源混乱
2. 渲染要求列材质清单——每个可见材质都要写质感描述
3. 风格参考用标杆作品——"similar to Dark Souls art direction"比"dark fantasy"更精确
4. 蒸汽/火焰/能量等特效要写粒子级描述——"individual particles visible, glowing faintly blue-white"

**块3：EXACT TYPOGRAPHY AND PLACEMENT（精确文字排版）**

每个文字元素独立描述，包含内容、字体、材质、位置、尺寸。

```
EXACT TYPOGRAPHY AND PLACEMENT:

[文字元素1]：位置（top-center/upper-right/lower-left）+ 精确内容（双引号包裹）+ 字体类型 + 材质质感 + 尺寸关系 + 与画面的交互
[文字元素2]：同上格式
[印章/符号]：位置 + 形态 + 内容 + 材质质感
```

关键规则：
1. 每个文字元素必须用双引号包裹精确内容
2. 字体写材质——"weathered metallic serif with gold gradient and dark shadow"比"金属字体"更精确
3. 位置用画面方位词——"top-center" / "lower-right corner" / "upper-left area"
4. 文字与画面要有物理交互——"placed in the gap between storm clouds" / "bottom strokes partially obscured by foreground debris"
5. 竖排文字明确方向——"written vertically from top to bottom"

**块4：HARD CONSTRAINTS（硬约束）**

负面约束清单，防止 AI 生成常见缺陷。

```
HARD CONSTRAINTS:

Exactly one principal character.
No additional people or background figures.
No duplicated limbs.
No detached or fused anatomy.
Exactly five fingers on each visible hand.
Do not crop the character's head, hair, or raised hand.
Do not obscure the character's face.
No chibi proportions.
No flat cel-shaded anime.
No comic panels or speech bubbles.
No watermark or unrelated logos.
No misspelled typography.
All displayed text must be perfectly spelled and cleanly placed exactly as specified.
```

> **HARD CONSTRAINTS 是高精度模板的核心增量**。V3 公式没有负面约束机制，模型常出现多指、残肢、文字乱码等问题。硬约束以"禁止"列表形式直接堵住这些缺陷。

#### 语言选择

- **英文**（推荐）：Seedream 对英文提示词的理解精度更高，尤其材质、光影、镜头术语。≤600 词
- **中文**：可用于纯中文赛道（修仙/古言），但材质和渲染术语建议混用英文。≤400 字

#### 完整示例（封面图）

```
Create a finished, edge-to-edge, vertical 3:4 web novel cover poster. The final image must look like premium AAA dark fantasy pirate manga key art combined with cinematic promotional illustration.

LOCKED COMPOSITION:

Use a dramatic mid-angle camera with a 24mm wide lens, positioned slightly below eye level looking upward at the main character. The character stands in the center of the composition, positioned slightly to the right of center, occupying the upper two-thirds of the image.

The main character is a 17-year-old male pirate captain of Germanic descent. He has golden-blonde windswept hair, piercing ice-blue eyes, a handsome but weathered young face with fair skin, subtle skin texture, and a confident, slightly cold expression. He wears a dark navy captain's long coat with gold trim and brass buttons, left open and billowing in the sea wind, revealing a white shirt underneath with a loose collar. A leather belt with a cutlass sword hangs at his waist. His left hand rests on the cutlass hilt; his right hand is raised slightly, palm upward, with wisps of white steam curling upward from his fingers.

Behind him, a massive three-masted pirate ship with dark sails cuts through stormy ocean waves. The ship is positioned in the upper-left background, slightly out of focus. Dark storm clouds fill the sky behind the ship, with a break in the clouds allowing a single dramatic shaft of golden sunlight to strike the character from behind-left, creating strong rim lighting on his hair and coat.

The lower third shows churning dark ocean waves with white foam, steam rising from the water's surface near the character's feet.

ENVIRONMENT AND LIGHTING:

The color palette is dominated by deep navy blue, charcoal black, and ocean gray, with warm golden accents from the breaking sunlight and brass details. White steam provides the brightest highlights.

Use cinematic rim lighting from behind-left (warm golden), soft frontal fill on the character's face (cool blue-white from the stormy sky), and dramatic volumetric god rays through the cloud break. The steam should glow with a faint blue-white luminescence.

The rendering must combine: photorealistic materials, high-end stylized 3D character design, dark fantasy manga aesthetic, detailed fabric weave on the coat, realistic leather texture, individual wet hair strands, volumetric steam particles, churning ocean foam, 8K promotional artwork.

EXACT TYPOGRAPHY AND PLACEMENT:

At the top-center, place the exact large text "海贼法典" in a bold, weathered, metallic serif typeface with a slight gold gradient and dark shadow. Place it in the gap between the storm clouds.

Below the title, place the exact smaller text "惟求得中" in a clean, elegant serif font.

On the lower-left, place one large stylized kanji character "蒸" painted with expressive dry-brush sumi-e strokes in white with a faint blue glow.

HARD CONSTRAINTS:

Exactly one principal character. No additional people. No duplicated limbs. No detached or fused anatomy. Exactly five fingers on each visible hand. Do not crop the character's head or raised hand. Do not obscure the face. No chibi proportions. No flat cel-shaded anime. No watermark. All text perfectly spelled and placed exactly as specified.
```

> **与 V3 结构化公式的对比**：V3 用"成数"描述配色，高精度模板用具体色名+方向描述光源；V3 无负面约束，高精度模板用 HARD CONSTRAINTS 堵住常见缺陷；V3 字数 ≤400 字，高精度模板英文 ≤600 词，信息密度更高。

## 二、Seedance 1.0 Pro 提示词指南（视频生成）

### 2.1 通用规则

- 中文提示词 ≤500 字，英文 ≤1000 词
- 支持文生视频、图生视频（首帧/首尾帧）
- 动作描述要"碎"要"慢"

### 2.2 提示词公式

```
[主体] + [动作（慢、连贯）] + [场景] + [光影] + [镜头语言] + [风格] + [画质] + [稳定性约束]
```

### 2.3 核心技巧

**动作描述**：
- ✅ 推荐词：缓慢、轻柔、连贯、自然、流畅、不僵硬、轻轻抬手、脚步轻移
- ❌ 避坑词：跳舞、跑步、高速、复杂互动、大幅度扭曲

**镜头与运镜**：
- 景别：特写 / 近景 / 中景 / 全景
- 动效：缓慢推镜 / 平稳横移 / 环绕 / 稳定跟拍
- 强制指令：固定镜头、无抖动、丝滑流畅

**角色稳定约束**：
- 五官清晰、面部稳定、不扭曲、人体结构正常、比例自然、同一角色、服装一致、发型不变

**画质词**：
- 4K、超高清、细节丰富、无模糊、无重影、无闪烁

**多镜头叙事**（Seedance 1.0 Pro 独有）：
- 用"镜头切换"连接多个场景
- 每次切镜后可刻画新出现的人物/场景特征

### 2.4 视频封面提示词模板

```
一个[外貌特征]的[角色身份]，缓慢[动作]，[场景环境]。[光影描述]，[色彩方案]。[镜头语言：景别+运镜]，[风格词]风格，4K超高清，面部清晰不变形，人体结构正常，画面流畅稳定，无闪烁。
```

### 2.5 视频参数

| 参数 | 选项 | 默认 |
|:-----|:-----|:----:|
| ratio | 1:1 / 3:4 / 4:3 / 16:9 / 9:16 / 21:9 | 16:9 |
| duration | 4-10 秒 | 5 |
| resolution | 480p / 720p / 1080p | 1080p |
| camera_fixed | true / false | false |

## 三、实测验证的控制公式

| 公式 | 用途 | 写法 |
|:-----|:-----|:-----|
| **结构化提示词V3** | 纯文生图达到商业级质量 | `整体氛围框架（画面是绝对主体）+ 画面内容（远景→前景按层次）+ 文字（最后描述，融入画面）+ 风格` |
| 风格控制 | 精确指定画风 | `[风格名称] + [技法描述] + [质感描述] + [参考标杆]` |
| 字体控制 | 精确指定书名质感 | `[书名] + [字体类型] + [材质/质感] + [色彩层次]` |
| 定场诗创作 | 浓缩小说意境为古体诗 | `[核心意象A] + [核心意象B] + [因果/转折] + [情感升华]` |
| 参考图精确分离 | 控制画风/构图吸收 | `仅参考此图的[具体要素]，不参考[具体要素]。以下画面内容由描述决定` |

## 四、画风DNA库（引用 pop-novel-image）

> 画风DNA已统一沉淀到 `skills/pop-novel-image/references/style-dna-library.json`，含36种画风（二次元17/国漫6/韩漫3/插画概念10），每种画风包含 `dna` + `constraint` + `recommended_lighting` + `recommended_composition` 四字段。

### 引用方式

1. 读取 `skills/pop-novel-image/references/style-dna-library.json`
2. 按 `suggested_genres` 或 `keywords` 筛选适合赛道的画风
3. 取 `dna` 字段作为风格描述（替代旧的关键词式风格词）
4. 取 `constraint` 字段作为风格保真约束
5. 取 `recommended_lighting` 检查光照兼容性（见 `skills/pop-novel-image/references/lighting-composition-templates.md`）

### 赛道→画风速查（从36种中筛选）

| 赛道 | 推荐画风（DNA库名） | 备注 |
|:-----|:-------------------|:-----|
| 暗黑修仙/末日 | 暗黑奇幻油画、哥特暗黑风、废土末日 | LT1减法照明 |
| 传统仙侠/古言 | 国漫玄幻厚涂、国风水墨仙侠、工笔重彩感 | 水墨用LT3平光 |
| 言情/甜宠 | 少女水彩言情、日系赛璐珞、轻小说插画风 | LT2柔光通透 |
| 悬疑/诡异 | 暗黑悬疑高对比、伊藤潤二、黑执事 | LT1减法照明 |
| 热血/战斗 | 日系热血战斗、韩漫暗黑厚涂、赛博边缘行者 | LT1或LT2 |
| IP化/影视化 | 新海诚电影风、电影概念艺术 | 按氛围选光照 |

> 完整36种画风详见 `skills/pop-novel-image/references/style-dna-library.json`。纯文生图时建议画风前置（放提示词前段），图生图时按参考点策略处理。

## 五、视觉类型与画幅

| 类型 | 比例 | 用途 | 推荐尺寸 |
|:-----|:-----|:-----|:---------|
| 封面-竖版 | 3:4 | 起点/番茄封面 | 1125x1500 |
| 封面-横版 | 16:9 | 宣传 banner | 1500x844 |
| 方形头像 | 1:1 | 角色头像 | 1500x1500 |

> 所有图像输出控制在 1500×1500 以内。

## 六、避坑清单

| 问题 | 原因 | 解决 |
|:-----|:-----|:-----|
| 画面缺失元素 | 提示词过长导致信息分散 | 控制字数，聚焦核心元素 |
| 画面泛白发灰 | 旧版模型特性；堆叠过多华丽词汇 | 用 5.0 lite/4.5/4.0（不再泛白）；简洁精确优于堆砌 |
| 人物变形 | 缺少稳定性约束 | 添加"五官清晰、人体结构正常" |
| 风格不对 | 风格词模糊 | 使用具体风格词（如"国风暗黑插画"）或提供参考图 |
| 构图偏差 | 缺少构图指引 | 添加"竖版构图""视觉重心在下方" |
| 色彩偏差 | 色彩描述模糊 | 用具体色名（如"深蓝与墨黑"） |
| 文字渲染失败 | 文字未用引号 | 用双引号包裹文字内容 |
| 图生图编辑不准 | 指代模糊 | 准确指示编辑对象，强调保持不变的部分 |
