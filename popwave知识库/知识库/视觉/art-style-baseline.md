---
id: art-style-baseline
lib: 知识库
cat: 视觉
version: 1.0.0
tags: [视觉]
---
# 画风基准库（Art Style Baseline）

> Step 0 定画风的唯一来源。**工程化复现铁律：画风不是从零发明的，是从成熟漫画/成熟作品提取、且经 Seedream 实测可复现的基准。**
> 每个基准 = 完整锁定画风串 + 验证图 + 题材适配方法。**选画风 = 按小说赛道从本库选一个基准，换题材只换配色，不换画风底盘。**
>
> **v7.2.0 核心变化（画风随赛道动态选）**：画风库从"唯一基准元尊V1"升级为"**多画风基准池**"。**画风不再定死，而是跟随小说风格类型选择**——仙侠/玄幻史诗用厚涂玄幻，赛博朋克用赛博画风，都市/异能用韩漫厚涂。赛博朋克类小说绝不能用元尊V1的书法墨线底盘。每个赛道绑定一个已验证基准，见 §一 赛道→画风映射表。

## 一、入库标准（可复现性门禁）

一个画风要入库，必须同时满足：

| 门禁 | 标准 | 不通过则 |
|:-----|:-----|:---------|
| **来源** | 从成熟漫画/成熟作品提取，非凭空发明 | 不入库 |
| **可复现基准** | 有 1 张 Seedream 实测通过的代表作作为验证图 | 不入库 |
| **画风串锁定** | 完整画风串（≥300字符）已锁定，记录生成参数 | 不入库 |
| **配色独立** | 画风底盘与配色解耦，换配色不影响画风本体 | 不入库 |

> **当前入库画风：`元尊V1` + `厚涂玄幻史诗` + `赛博霓虹冷光` + `韩漫半写实厚涂` + `水墨国风写意` + `日系高精赛璐璐` 六个基准。** 新画风必须实测通过后追加，禁止跳过实测直接入库。
> **画风差异度原则（老板定调）**：库内画风格局刻意拉开差异——墨线赛璐璐 / 无线稿厚涂 / 水墨写意 / 韩漫半写实 / 赛博霓虹冷光 / 日系高精赛璐璐，六套质感互为对角，杜绝"看似多套实则一套"。2026-08-03 立绘实测发现：元尊V1/厚涂B/厚涂C 三套画风串因共用角色+配色+模板，相似度极高归并为一套立绘基准（见 §三-b）。**画风差异必须靠画风底盘本身拉开，不能只改配色或换皮。**
> **定妆照必须与本库画风同源**：角色定妆照的画风 = 所选基准的画风底盘，禁止用无关风格串生成定妆照（否则参考图污染全书画风）。见 §三-b 定妆照PE区。

### 赛道 → 画风基准映射表（Step 0 定画风唯一依据）

> 选画风 = 查这张表，按小说赛道选基准。**表内没有的赛道 = 新增画风基准，走 §三 入库流程实测后追加，禁止硬套表内基准。**

| 小说赛道 | 画风基准 | 画风底盘特征 | 验证图 |
|:---------|:---------|:-------------|:------|
| **仙侠/玄幻/史诗** | **厚涂玄幻史诗**（§二-B） | 无线稿厚涂+冷暖大对撞+体积光/粒子/发光 | `R1-*_强化光影炫丽.jpg` |
| **国漫玄幻/古风** | **元尊V1**（§二） | 书法墨线赛璐璐+高饱和+对角分区 | `整页_复现_v1_非对称分格.jpg` |
| **古风/仙侠意境/水墨** | **水墨国风写意**（§二-E） | 墨色渲染+大留白+宣纸质感+淡彩 | `新画风-水墨国风写意.jpg` |
| **赛博朋克/都市异能** | **赛博霓虹冷光**（§二-C） | 青/品红霓虹+深黑底+冷光+高反差 | `新画风-赛博霓虹冷光.jpg` |
| **都市/悬疑/诡异** | **韩漫半写实厚涂**（§二-D） | 干净现代半写实+柔和光影+电影感 | `新画风-韩漫半写实厚涂.jpg` |
| **热血/战斗** | **韩漫半写实厚涂**（§二-D） | 同都市行，干净利落适合战斗 | `新画风-韩漫半写实厚涂.jpg` |
| **言情/甜宠/日常** | **日系高精赛璐璐**（§二-F） | 圆润透亮+渐变高光+明亮通透 | `新画风-日系高精赛璐璐.jpg` |

> **表内每个基准均已 Seedream 实测通过**（验证图见 §二 各小节）。**新增赛道 = 新增画风基准，走 §三 入库流程实测后追加，禁止硬套表内基准。**

---

## 定妆照画风同源铁律（新增）

> **立绘 OC 图决定成品漫画质量（老板定调），立绘画风必须与页面画风同源。**
> **老板确认（2026-08-03）：立绘 OC 画风 = 漫画画风 = 整个项目的基底画风。二者统一，不分离。**
> - 立绘是图生图链条的**参考真相源**：立绘画风 = 全书画风，立绘精度 = 全书质量上限。
> - **立绘画风 = 所选画风基准的底盘**（§二 至 §二-F 的锁定画风串），禁止用无关画风生成后再迁移。
> - **人物 OC 画风与漫画页画风必须一致**：选赛博 → 立绘和漫画页都用赛博画风（含赛博人物规格）；选仙侠 → 都用厚涂玄幻。OC 是漫画每一格的参考图，OC 画风错 = 全书画风错。
> - **立绘跟随所选赛道画风基准，画风跟小说类型走，不锁定单一基准。** 每套基准对应一套立绘画风（如赛博基准对应 §2C.5 赛博人物规格）。
> - 立绘质量用**高精度模板**（见 oc-design-guide.md §高精度立绘升级），材质/光源/硬约束逐项锁定，作为全书质量上限。

---

## 二、入库基准一：元尊V1（元尊式国漫玄幻·书法墨线厚涂）

> **基准一（国漫玄幻/古风赛道）。** 从《元尊》漫画第一章复现打磨而来，`整页_复现_v1_非对称分格.jpg` 为验证图。
> 适用赛道：**国漫玄幻/古风**。换题材只换配色，不换这个画风底盘。**注意：本基准不含无线稿厚涂，需要"无线稿炫丽"时改用 §二-B 厚涂玄幻史诗。**

### 2.1 画风特征拆解（为什么它"贵"）

| 维度 | 特征 | 说明 |
|:-----|:-----|:-----|
| **底色** | 赛璐璐平涂 + 部分喷枪渐变 | 干净利落的色块，带选择性渐变，不平滑到底 |
| **线稿** | 书法墨线（粗细顿挫） | 粗-细-粗的毛笔笔触，有飞白感，非均匀数字线 |
| **饱和** | 高饱和强对比 | 色块之间对比强烈，不灰 |
| **色彩分区** | 对角色彩分区贯穿全页 | 冷色（蓝/靛/紫）与暖色（金/红/紫红）对角对撞 |
| **光影** | 戏剧光 + 体积光 | 光柱/光晕增强氛围，非平光 |

### 2.2 锁定画风串（Seedream 执行串，直接复制）

> 这是**画风底盘**，已锁定。**换题材时只改"色彩分区"那句的配色，其余全部不动。**

```
Chinese fantasy manhua style, cel-shading with clean crisp painterly flats and selective airbrush gradients. Bold expressive black ink line work with varying confident stroke weight (thick-then-thin brush strokes, calligraphic flair), distinct manga inking. High saturation strong contrast. Distinct color-zoned palette: [题材配色，见2.4]. Strong diagonal color opposition across the page. Dramatic lighting with volumetric god rays. No flat cell-shading agar. No rough sketch. No chibi proportions. No modern clothing. No text overlay.
```

### 2.3 验证图与生成参数

- **验证图**：`workspace/元尊/复现测试/整页_复现_v1_非对称分格.jpg`
- **模型**：`doubao-seedream-5-0-pro-260628`
- **尺寸**：`1125x1500`
- **参数**：纯文生图，无参考图（Seedream 靠文字描述即可锁定画风）

### 2.4 题材适配（换题材只换配色）

> 换小说题材时，**只替换画风串中 `[题材配色]` 占位**，画风底盘（赛璐璐+书法墨线+高饱和+对角分区）全程不变。

| 题材 | 替代配色指令（直接替换 `[题材配色]`） | 示例已验证 |
|:-----|:-------------------------------------|:-----------|
| **玄幻/修仙** | `ice-blue and sky-blue for water/energy, deep purple-red for raging power, imperial gold and cinnabar-red for authority, deep indigo and moon-white for the suffering in-between` | 元尊V1 |
| **永夜/末世** | `cold deep indigo-blue and ash-black for the eternal night wilderness, warm crimson-red and ember-orange for the fire-stones' and fire-spring's life-giving light, pale moon-white and soft gold for the fragile warmth of home, ethereal silver-white for the awakening power` | 夜无疆测试 |
| **新增题材** | 从原文提取 3-4 组"对角色彩"（如 冷/暖/线索色），填入此格式 | 需实测确认 |

**配色提取规则**：从小说世界观提取 3-4 组对角色彩，每组 = 情绪/场景 + 色系。例：冷（永夜/绝望）+ 暖（火/生机）+ 线索色（觉醒银光）。

---

## 二-B、入库基准二：厚涂玄幻史诗（仙侠/玄幻/史诗赛道）

> **基准二（仙侠/玄幻/史诗赛道）。** 从老板上传的"东方玄幻史诗厚涂风"实测打磨而来（2026-08-03 R1 四变体散布，详见 `pe-log-2026-08-03.md`）。
> 适用赛道：**仙侠/玄幻/史诗**。最适合"渡劫飞升/道法相/璀璨炫丽"的戏剧性名场面。**与元尊V1的区别：无线稿厚涂（非书法墨线）**，炫丽度更高。

### 2B.1 画风特征拆解（为什么它"炫丽"）

| 维度 | 特征 | 说明 |
|:-----|:-----|:-----|
| **底色** | 无线稿厚涂/半厚涂 | 形式靠色彩对比+光影交界定义，无勾线；半厚涂最稳（纯厚涂时 Seedream 会偏薄涂平滑渐变） |
| **线稿** | 无（lineless） | 轮廓由色彩与明暗界定，非物理线条 |
| **饱和** | 焦点高饱和双高峰 | 暖色（金/橙/朱红）饱和峰值 + 冷色（青/蓝/紫）次峰值，刻意设计 |
| **色彩分区** | 强冷暖大对撞 | 中心暖（能量核）+ 外围冷（宇宙虚空），包围式/辐射式对撞 |
| **光影** | 体积光+粒子+发光三重叠加 | 边缘光+自发光+体积光+粒子+镜头光晕，是"炫丽"的核心 |

### 2B.2 锁定画风串（Seedream 执行串，直接复制）

> **推荐用 B 变体（半厚涂）作为常规叙事页基准，C 变体（强化光影）作为名场面/封面高纯度基准。** 换题材时只改"色彩分区"那句的配色，其余不动。

**常规叙事页基准（B 半厚涂，最稳）**：
```
Chinese xianxia fantasy epic digital painting, luminous semi-thick-paint rendering with subtle implied line structure, forms defined mostly by color contrast with faint structural hints at edges. Bold painterly brushstrokes, rich impasto texture. High saturation vivid colors concentrated in the light core (gold/orange/crimson) attenuating to deep cold shadows (teal/blue/black). Strong warm-cold color opposition across the whole image. Multiple light sources: rim light outlining the subject, self-luminous energy, volumetric god rays, drifting glowing particles and star fields. Sacred transcendent cosmic atmosphere, scale of eons. Distinct color-zoned palette: {题材配色}. No flat cel-shading. No cartoon. No anime flat coloring. No visible outline lineart. No text overlay.
```

**名场面/封面高纯度基准（C 强化光影，最炫丽）**：
```
Chinese xianxia fantasy epic digital painting, luminous thick-paint volumetric rendering with no visible line art, forms defined purely by color contrast and light-shadow transitions instead of outlines. Bold painterly brushstrokes, rich impasto texture. High saturation vivid colors concentrated in the light core (gold/orange/crimson) attenuating to deep cold shadows (teal/blue/black). Strong warm-cold color opposition across the whole image. Multiple dramatic light sources: strong rim light, self-luminous energy core, volumetric god rays, heavy drifting glowing particles, star fields, lens flare, bokeh. Sacred transcendent cosmic atmosphere, scale of eons. Distinct color-zoned palette: {题材配色}. No flat cel-shading. No cartoon. No anime flat coloring. No visible outline lineart. No text overlay.
```

> **质量标记**（与元尊V1相反，用写实概念艺术词）：`High quality cinematic Chinese xianxia fantasy concept art, highly detailed, masterpiece, best quality, volumetric rendering.`
> **负面约束**：禁平涂/赛璐璐/卡通，不禁厚涂（`No flat cel-shading. No cartoon. No anime flat coloring. No visible outline lineart.`）

### 2B.3 验证图与生成参数

- **验证图**：`workspace/厚涂玄幻画风测试/R1-C_强化光影炫丽.jpg`（5.0）与 `R1-B_半厚涂加结构线.jpg`（4.95）
- **模型**：`doubao-seedream-5-0-pro-260628`
- **尺寸**：`1125x1500`
- **参数**：纯文生图，无参考图

### 2B.4 题材适配（换题材只换配色）

| 题材 | 替代配色指令（替换 `{题材配色}`） | 示例已验证 |
|:-----|:---------------------------------|:-----------|
| **仙侠渡劫/飞升** | `imperial gold and cinnabar-red for the tribulation Dao-aura and ascension authority, vivid violet and electric azure for the thunder tribulation and immortal arts, cold deep teal-blue and starry cosmic nebula for the boundless void, pale moon-white and pure silver for the moment of enlightenment` | 厚涂玄幻R1 |
| **新增题材** | 从原文提取 3-4 组"对角色彩"填入此格式 | 需实测确认 |

### 2B.5 与画风硬边界的关系

> 本基准的"无线稿厚涂"在**单格独立生图（YZ-8 名场面/封面）时纯度最高**（R1 验证 4.5-5.0）。多格直出时同样受 §2.5 硬边界约束（纯度会降），但厚涂在多格下的表现比赛璐璐更稳（B 半厚涂为常规叙事页设计）。**常规叙事页建议用 B 半厚涂，名场面/封面用 C 强化光影。**

---

## 二-C、入库基准三：赛博霓虹冷光（赛博朋克/都市异能赛道）

> **基准三（赛博朋克/都市异能赛道）。** 2026-08-03 画风库扩充实测（详见 `workspace/画风库扩充测试/pe-log-2026-08-03.md`）。
> 适用赛道：**赛博朋克/都市异能**。冷光系底盘，与库内暖色系厚涂（§二-B）形成明显对角。**与元尊V1/厚涂玄幻的区别：冷光主导 + 霓虹 + 深黑底，无暖色体积光。**
> **⚠️ 铁律：赛博画风必须"人物也赛博化"，不能只背景赛博。** R1 实测失败——用仙侠角色载体（道袍+亚麻发）时，人物呈现写实仙侠、仅背景赛博，两层割裂，不合格。R2 修正：**人物本体 = 科技服+霓虹边缘+机械义体/发光瞳+半写实动漫渲染**，人物与背景共用同一套霓虹色系，融为一体。**选赛博画风时，角色规格必须同步替换为赛博人物（科技服/义体/未来感），禁止用古风/仙侠角色载体。**

### 2C.1 画风特征拆解（为什么它"冷"）

| 维度 | 特征 | 说明 |
|:-----|:-----|:-----|
| **底色** | 深黑底 + 霓虹亮面 | 近纯黑阴影（保留微弱蓝紫倾向），霓虹高光高饱和，两级化 |
| **线稿** | 无硬边线稿 | 靠明暗分区 + 逆光勾勒轮廓，非物理线条 |
| **饱和** | 双色系统高饱和 | 青（cyan）主导科技感 + 品红（magenta）注入危险张力，冷暖对抗 |
| **人物赛博化** | 科技服 + 霓虹边缘 + 义体/发光瞳 | 人物本体即赛博，不靠背景补赛博感（R2 修正） |
| **色彩分区** | 霓虹框式包围 | 霓虹光源分布于画面两侧/背景，将视觉焦点压向中央人物 |
| **光影** | 冷光 + 逆光 + 雾气 | 青/品红霓虹 + 大量雾气散射光晕 + 湿地面反射，高反差 |

### 2C.2 锁定画风串（Seedream 执行串，直接复制）

> **画风底盘已锁定。换题材时只改配色/场景，画风本体不动。人物必须走赛博角色规格（见 §2C.5），不能套用古风/仙侠载体。**

```
Cyberpunk neon-noir digital illustration, full illustration style where BOTH the character and the environment are saturated in electric neon glow, stylized anime-adjacent rendering with bold clean shapes and graphic silhouette, NOT realistic photography. Electric cyan, magenta and violet neon light cutting through deep near-black shadows. The character wears futuristic techwear with glowing neon trim lines, cybernetic implants and holographic accents, neon edge-light on every contour. Wet reflective surfaces, volumetric fog, holographic light streaks, high-contrast cold lighting. [题材配色]. No photography. No realistic face. No photoreal skin. No medieval fantasy. No kimono. No martial-arts robe. No warm pastoral palette. No cel-shading. No ink-wash. No chibi proportions. No text overlay.
```

### 2C.3 验证图与生成参数

- **验证图**：`workspace/画风库扩充测试/新画风-赛博霓虹冷光-R2.jpg`（R2，人物已赛博化，合格）
- **模型**：`doubao-seedream-5-0-pro-260628` / **尺寸**：`1125x1500` / **参数**：纯文生图

### 2C.4 题材适配（换题材只换配色）

| 题材 | 替代配色指令（替换 `[题材配色]`） | 示例已验证 |
|:-----|:---------------------------------|:-----------|
| **赛博朋克/都市异能** | `electric cyan and magenta for the neon city, violet for the digital void, deep black-blue for the polluted sky` | 扩充测试 |
| **新增题材** | 从原文提取 3-4 组"对角色彩"填入 | 需实测确认 |

### 2C.5 赛博角色规格模板（R2 实测可用，选赛博画风必须套用）

> **R2 修复的根因：人物必须本体赛博化，不能只背景赛博。** 选赛博画风时，角色规格必须用此模板（科技服+霓虹边缘+义体/发光瞳+半写实动漫渲染），禁止套用古风/仙侠载体。人物 7 维度如下：

```
A 20-year-old male cyberpunk [street-samurai / hacker / mercenary] with a lean athletic build. Short choppy [hair color] hair with electric [cyan/magenta]-streaked undercut, sharp intense eyes with a faint glowing [color] iris implant, sharp jawline, pale skin with subtle cybernetic circuit lines on the temples. Wearing a fitted high-collar techwear jacket in dark charcoal with glowing neon trim, a tactical harness with glowing [color] accents, fingerless gloves, metallic choker, and a worn cybernetic arm joint visible at the wrist. Expression: calm, guarded, street-smart edge.
```

> **配套硬约束**：`No realistic photographic rendering. No photoreal skin. No kimono. No martial-arts robe.`（人物本体动漫化，禁写实人像，禁古风服饰）

---

## 二-D、入库基准四：韩漫半写实厚涂（都市/悬疑/热血赛道）

> **基准四（都市/悬疑/诡异/热血/战斗赛道）。** 2026-08-03 画风库扩充实测。
> 适用赛道：**都市/悬疑/诡异/热血/战斗**。干净现代半写实，是"美强惨"人设 + 商业级完成的默认底盘。**与厚涂玄幻（§二-B）的区别：更干净更现代、光影柔和、非炫丽粒子。**

### 2D.1 画风特征拆解（为什么它"干净"）

| 维度 | 特征 | 说明 |
|:-----|:-----|:-----|
| **底色** | 无线稿半写实厚涂 | 色块过渡柔和，边缘虚实结合，无硬勾线 |
| **线稿** | 隐线（极细暗示线） | 面部/衣褶转折处保留极细高精度线，其余靠块面 |
| **饱和** | 低饱和高级灰调 | 现代"电影感"审美，暖金发+冷灰背景形成冷暖对比 |
| **色彩分区** | 单点光源分区 | 焦点锐利、次焦朦胧、背景虚化，三级信息层级 |
| **光影** | 戏剧性照明 + 边缘光 | 舞台光 + 明确明暗交界线 + 边缘光分离人物 |

### 2D.2 锁定画风串（Seedream 执行串，直接复制）

```
Korean manhwa webtoon style, semi-realistic rendering with clean refined line-work and smooth polished shading, modern fashion-forward aesthetic. Soft cinematic lighting with gentle gradients and natural skin tones, subtle atmospheric depth. Deep elegant color saturation with a modern urban palette of cool slate-blue and warm amber highlights. Crisp high-quality production value, refined character design. [题材配色]. No cel-shading. No anime flat coloring. No ink-wash. No 3D render look. No chibi proportions. No text overlay.
```

### 2D.3 验证图与生成参数

- **验证图**：`workspace/画风库扩充测试/新画风-韩漫半写实厚涂.jpg`（技术完成度与市场适配度双满分）
- **模型**：`doubao-seedream-5-0-pro-260628` / **尺寸**：`1125x1500` / **参数**：纯文生图

### 2D.4 题材适配（换题材只换配色）

| 题材 | 替代配色指令（替换 `[题材配色]`） | 示例已验证 |
|:-----|:---------------------------------|:-----------|
| **都市/悬疑/异能** | `cool slate-blue and charcoal for the urban night, warm amber for the supernatural glow, muted steel-gray for the mundane world` | 扩充测试 |
| **热血/战斗** | `crimson and ember-orange for the fighting spirit, electric blue for the energy clash, deep charcoal for the arena` | 需实测确认 |
| **新增题材** | 从原文提取 3-4 组"对角色彩"填入 | 需实测确认 |

---

## 二-E、入库基准五：水墨国风写意（古风/仙侠意境赛道）

> **基准五（古风/仙侠意境/水墨赛道）。** 2026-08-03 画风库扩充实测。
> 适用赛道：**古风/仙侠意境/水墨**。墨色渲染 + 大留白 + 宣纸质感，是库内最"高级国风"的底盘。**与元尊V1（§二 书法墨线赛璐璐）的区别：水墨写意 vs 赛璐璐，前者重意境留白，后者重色块对比。**

### 2E.1 画风特征拆解（为什么它"意境"）

| 维度 | 特征 | 说明 |
|:-----|:-----|:-----|
| **底色** | 水墨渲染 + 宣纸质感 | 墨色浓淡五色（五色墨）+ 湿墨晕染 + 宣纸纤维纹理 |
| **线稿** | 写意书法线 | 竹叶/衣褶用粗细顿挫笔触，飞白（feibai）质感 |
| **饱和** | 低饱和淡彩 | 墨色为主 + 朱砂红/淡金点缀，克制不堆叠 |
| **色彩分区** | 大留白 + 计白当黑 | 约60%留白，人物从虚空中浮现，营造疏离敬畏感 |
| **光影** | 水墨晕染 + 大气透视 | 雾霭渲染 + 远山淡墨，非现实光影 |

### 2E.2 锁定画风串（Seedream 执行串，直接复制）

```
Chinese ink-wash painting (shuimo guofeng) style, expressive freehand brushwork with bold flowing ink strokes and soft ink diffusion, generous negative space (liubai), figures drawn in elegant calligraphic ink lines with sparse translucent color washes. Muted refined palette with sparse cinnabar-red and pale gold accents on rice-paper white. Visible rice paper texture and subtle ink bleed. Wispy breathable composition, poetic atmospheric mood. [题材配色]. No cel-shading. No thick-paint. No realistic rendering. No glossy anime look. No heavy color saturation. No chibi proportions. No text overlay.
```

### 2E.3 验证图与生成参数

- **验证图**：`workspace/画风库扩充测试/新画风-水墨国风写意.jpg`（风格对齐 ★★★★☆，意境高级）
- **模型**：`doubao-seedream-5-0-pro-260628` / **尺寸**：`1125x1500` / **参数**：纯文生图

### 2E.4 题材适配（换题材只换配色）

| 题材 | 替代配色指令（替换 `[题材配色]`） | 示例已验证 |
|:-----|:---------------------------------|:-----------|
| **古风/仙侠意境** | `sparse cinnabar-red and pale gold for the immortal aura, ink-black and ash-gray for the mountain, pale moon-white for the void` | 扩充测试 |
| **新增题材** | 从原文提取 3-4 组"对角色彩"填入 | 需实测确认 |

---

## 二-F、入库基准六：日系高精赛璐璐（言情/甜宠/日常赛道）

> **基准六（言情/甜宠/日常赛道）。** 2026-08-03 画风库扩充实测。
> 适用赛道：**言情/甜宠/日常**。圆润透亮 + 渐变高光 + 明亮通透，是"美型但通透"的二次元底盘。**与元尊V1（§二 书法墨线赛璐璐）的区别：日系高精赛璐璐更圆润透亮、渐变高光，非书法墨线。**

### 2F.1 画风特征拆解（为什么它"透亮"）

| 维度 | 特征 | 说明 |
|:-----|:-----|:-----|
| **底色** | 高精赛璐璐 + 渐变 | 色块清晰 + 平滑渐变 + 半透明叠加，保留"果冻质感" |
| **线稿** | 精细柔边线稿 | 轮廓锐利 + 内部柔边，非墨线顿挫 |
| **饱和** | 明亮通透 + 冷暖微差 | 单色系主导 + 冷暖微差，克制高级 |
| **色彩分区** | 色彩分区 + 大气透视 | 背景山体蓝灰渐变，前景人物清晰 |
| **光影** | 渐变高光系统 | 主高光 + 边缘光 + 透射高光 + 材质高光，圆润体感 |

### 2F.2 锁定画风串（Seedream 执行串，直接复制）

```
Premium Japanese anime illustration style, clean crisp cel-shading with smooth gradient shading and glossy highlights, delicate refined line-art with soft edges, bright airy color palette. Expressive large eyes, soft appealing character design, polished high-quality production with gentle soft lighting and clean backgrounds. [题材配色]. No thick-paint. No realistic rendering. No watercolor. No ink-wash. No harsh shadows. No chibi proportions. No text overlay.
```

### 2F.3 验证图与生成参数

- **验证图**：`workspace/画风库扩充测试/新画风-日系高精赛璐璐.jpg`（色彩和谐 ★★★★★，技术展示 ★★★★★）
- **模型**：`doubao-seedream-5-0-pro-260628` / **尺寸**：`1125x1500` / **参数**：纯文生图

### 2F.4 题材适配（换题材只换配色）

| 题材 | 替代配色指令（替换 `[题材配色]`） | 示例已验证 |
|:-----|:---------------------------------|:-----------|
| **言情/甜宠/日常** | `soft rose-pink and cream for the romance, pale sky-blue and pearl-white for the daily warmth, gentle gold for the happy moments` | 扩充测试 |
| **新增题材** | 从原文提取 3-4 组"对角色彩"填入 | 需实测确认 |

---

## 2.5 画风硬边界铁律（2026-08-03 夜无疆×元尊，R4-R10 实测，详见 pe-log-2026-08-03.md）

> **决定生产路线的硬边界**：**画风纯度与结构化排版在 Seedream 上互斥**——单格独立生图能达到 65-70% 赛璐璐纯度，但一旦进入多格直出，纯度必然掉到 20-40%（Seedream 为格间连贯与叙事流，总是优先环境光遮蔽/体积光/大气透视，牺牲画风纯度）。**二者只能取其一。**

**生产路线定型（严格执行）**：
- **常规叙事页 = 直出多格，接受"半赛璐璐"**（画风纯度 20-40%，但保留完整排版结构/色彩分区/跨格叙事流）。这是连载的默认形态。
- **S级名场面/章末钩子页 = 单格独立生图**（YZ-8 全幅单格，可达 65-70% 纯度）。单格没有多格连贯压力，画风纯度最高。

**已确认有效的画风改进点**（直出多格下，按有效性排序）：
1. **质量标记禁用写实词**：`IMG_*.CR2 / 8K ultra HD / cinematic quality / masterpiece` 会显著推高厚涂倾向。改用 `High quality anime comic illustration, highly detailed, professional manga art, clean lineart, crisp colors.`
2. **去掉 `Dramatic lighting with volumetric god rays`**：该语言激活场景厚涂。改用 `Flat cel-shaded rendering with hard color edges, minimal gradient, crisp clean panels.`
3. **硬cel-shading约束**：`2D anime cel-shading, flat colors with hard-edged single shadow layer, crisp two-tone shading (base + shadow + highlight). Clean bold lineart.`
4. **负面压氛围词**：`No painterly. No soft gradient. No atmospheric haze. No volumetric light. No thick paint. No airbrush. No dry-brush. No ink-wash flying white.`
5. **mood 文案收敛**：末尾氛围堆叠词（claustrophobic/oppressive/sacred/vast sacred light）会推厚涂，改为克制情节拍点。

> **重要**：以上改进点仅在**单格独立生图**时有效（R10 验证：回灌到直出多格反而更低，因为去掉氛围词后 Seedream 用更写实的雪山体积补足）。**直出多格时不要过度压画风，接受半赛璐璐即可**，重点保住排版结构与叙事流。

---

## 三、如何新增画风基准（入库流程）

> 探索新画风时，先走一次"实测复现"验证，通过后才入库。禁止直接写进基准库。

1. 提取目标画风的特征拆解（底色/线稿/饱和/分区/光影 五维）
2. 组装候选画风串
3. 用目标作品的代表性场景 Seedream 实测（≥1 张）
4. 对照验证图评估：是否达到"元尊V1同等级质感"
5. **通过则该画风入库为第2个基准**；不通过则调整或放弃
6. 入库时锁定：画风串 + 验证图 + 题材适配表

---

## 三-b、角色定妆照 PE 区（入库）

> **铁律：立绘画风 = 漫画画风 = 所选赛道画风基准的底盘（老板确认 2026-08-03）。** 立绘 OC 图是图生图链条的参考真相源，选错画风会污染所有下游页面。定妆照 PE 必须实测通过（`guides/pe-test-sop.md` §4.4）后入库。
> **立绘 OC 图决定成品漫画质量（老板定调）**：立绘用高精度模板（见 oc-design-guide.md §高精度立绘升级），保证角色识别准确。
> **立绘跟随所选赛道画风基准，不锁单一基准**：选赛博 → 立绘用 §2C 赛博画风 + §2C.5 赛博人物规格；选仙侠 → 立绘用厚涂玄幻；选水墨 → 立绘用水墨画风。**"画风差异由页面场景承担"不适用于本基准——立绘本身就是所选画风的执行，必须与页面同源。**
> **R1 实测校准（2026-08-03）**：元尊V1/厚涂B/厚涂C 三套画风串在"同一仙侠角色+同一配色+同一4块模板"下生成立绘，相似度极高，归并为一套（即非"换皮"式的假装差异）。**这提醒：立绘差异必须靠"画风底盘 + 角色载体"双维度拉开，不能只改配色或模板。** 仙侠项目以厚涂C为底（光影/服装细节/汉服正确度最强）融合元尊V1线条清晰度，作为仙侠立绘基准。

### 立绘画风串（仙侠项目示例，其他赛道用对应基准画风串）

> **以仙侠赛道为例。** 换赛道时，立绘画风串 = 该赛道基准的锁定画风串（§二 至 §二-F），角色规格 = 该赛道的人物载体（如赛博用 §2C.5）。换题材只换 `[题材配色]`，画风底盘不变。

```
Chinese xianxia fantasy epic digital painting, luminous semi-thick-paint rendering with subtle implied line structure and clean confident line work, forms defined mostly by color contrast with defined facial features. Bold painterly brushstrokes, rich impasto texture. High saturation vivid colors concentrated in the light core (gold/orange/crimson) attenuating to deep cold shadows (teal/blue/black). Strong warm-cold color opposition across the whole image. Multiple light sources: rim light outlining the subject, self-luminous energy, volumetric god rays, drifting glowing particles and star fields. Clearly defined eastern hanfu with correct cross-collar (right over left) construction. Distinct color-zoned palette: [题材配色]. No flat cel-shading. No overly smooth plastic skin. No chibi proportions. No text overlay.
```

> **R1 实测校准（2026-08-03 立绘画风测试）**：三套画风串（元尊V1/厚涂B/厚涂C）实测正面对比，因共用角色+配色+4块模板，相似度极高，判定归并为一套。以厚涂C为底（光影最炫、金绣纹+破损细节最足、汉服右衽正确，综合 8.95/10），融合元尊V1线条清晰度（解决皮肤偏塑料问题）。**立绘画风统一，画风差异由页面场景承担。**

### 入库定妆照记录

| 角色 | 版本 | 画风基准 | 画风串 | 验证图 | 轮次ID | 参数 |
|:-----|:-----|:---------|:-------|:-------|:-------|:-----|
| 秦铭 | v4 | 仙侠玄幻国漫立绘 | 统一立绘串 + 夜无疆配色 | `char-秦铭-v4-front.png` | R3-定妆 | 1125x1500 |
| 陆泽 | v4 | 仙侠玄幻国漫立绘 | 统一立绘串 + 夜无疆配色 | `char-陆泽-v4-front.png` | R3-定妆 | 1125x1500 |

> 夜无疆配色：`cold deep indigo-blue and ash-black for the eternal night wilderness, warm crimson-red and ember-orange for the fire-stones' and fire-spring's life-giving light, pale moon-white and soft gold for the fragile warmth of home, ethereal silver-white for the awakening power`

---

## 四、速查

| 我要 | 读什么 |
|:-----|:------|
| 定画风（默认） | 本文件 §一 赛道→画风映射表，按小说赛道选基准 |
| 换题材配色 | 本文件 §2.4 / §2B.4 / §2C.4 / §2D.4 / §2E.4 / §2F.4 各基准题材适配表 |
| 新增画风 | 本文件 §三 入库流程 |
| **画风硬边界/生产路线（常规页直出半赛璐璐，名场面单格高纯度）** | 本文件 §2.5 画风硬边界铁律 |
| 立绘定妆照画风 | 本文件 §三-b + 立绘跟随所选赛道画风基准（OC=漫画=项目基底） |
| 画风如何进提示词 | director-card-template → 6段式PE第2段 |