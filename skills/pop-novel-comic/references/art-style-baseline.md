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

> **当前入库画风：`元尊V1` + `厚涂玄幻史诗` 两个基准。** 新画风必须实测通过后追加，禁止跳过实测直接入库。
> **定妆照必须与本库画风同源**：角色定妆照的画风 = 所选基准的画风底盘，禁止用无关风格串生成定妆照（否则参考图污染全书画风）。见 §三-b 定妆照PE区。

### 赛道 → 画风基准映射表（Step 0 定画风唯一依据）

> 选画风 = 查这张表，按小说赛道选基准。**表内没有的赛道 = 新增画风基准，走 §三 入库流程实测后追加，禁止硬套表内基准。**

| 小说赛道 | 画风基准 | 画风底盘特征 | 验证图 |
|:---------|:---------|:-------------|:------|
| **仙侠/玄幻/史诗** | **厚涂玄幻史诗**（§二-B） | 无线稿厚涂+冷暖大对撞+体积光/粒子/发光 | `R1-*_强化光影炫丽.jpg` |
| **国漫玄幻/古风** | **元尊V1**（§二） | 书法墨线赛璐璐+高饱和+对角分区 | `整页_复现_v1_非对称分格.jpg` |
| **赛博朋克/都市异能** | 韩漫暗黑厚涂（待入库） | 厚涂冷色+电影感+无线稿 | 需实测 |
| **都市/悬疑/诡异** | 韩漫暗黑厚涂（待入库） | 同赛博行 | 需实测 |
| **热血/战斗** | 日系热血/韩漫厚涂（待入库） | 需实测 | 需实测 |
| **言情/甜宠/古言** | 少女水彩/日系赛璐璐（待入库） | 需实测 | 需实测 |

> **列"待入库"的画风 = 未实测，禁止直接使用**。当遇到表内为"待入库"的赛道时，先走 §三 入库流程实测通过，再回填此表并入库。

---

## 定妆照画风同源铁律（新增）

> **立绘 OC 图决定成品漫画质量（老板定调），立绘画风必须与页面画风同源。**
> - 立绘是图生图链条的**参考真相源**：立绘画风 = 全书画风，立绘精度 = 全书质量上限。
> - **立绘画风 = 所选画风基准的底盘**（§二 或 §二-B 的锁定画风串），禁止用无关画风生成后再迁移。
> - 赛博朋克小说 → 立绘用赛博画风；仙侠 → 立绘用厚涂玄幻画风。**画风跟小说类型走，不锁定单一基准。**
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
- **尺寸**：`1728x2304`
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
- **尺寸**：`1728x2304`
- **参数**：纯文生图，无参考图

### 2B.4 题材适配（换题材只换配色）

| 题材 | 替代配色指令（替换 `{题材配色}`） | 示例已验证 |
|:-----|:---------------------------------|:-----------|
| **仙侠渡劫/飞升** | `imperial gold and cinnabar-red for the tribulation Dao-aura and ascension authority, vivid violet and electric azure for the thunder tribulation and immortal arts, cold deep teal-blue and starry cosmic nebula for the boundless void, pale moon-white and pure silver for the moment of enlightenment` | 厚涂玄幻R1 |
| **新增题材** | 从原文提取 3-4 组"对角色彩"填入此格式 | 需实测确认 |

### 2B.5 与画风硬边界的关系

> 本基准的"无线稿厚涂"在**单格独立生图（YZ-8 名场面/封面）时纯度最高**（R1 验证 4.5-5.0）。多格直出时同样受 §2.5 硬边界约束（纯度会降），但厚涂在多格下的表现比赛璐璐更稳（B 半厚涂为常规叙事页设计）。**常规叙事页建议用 B 半厚涂，名场面/封面用 C 强化光影。**

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

> **铁律：定妆照画风 = 所选画风基准（§二 元尊V1 或 §二-B 厚涂玄幻史诗）的底盘。** 定妆照是图生图的参考真相源，选错画风会污染所有下游页面。定妆照 PE 必须实测通过（`guides/pe-test-sop.md` §4.4）后入库。
> **立绘 OC 图决定成品漫画质量（老板定调）**：立绘画风必须与页面画风同源，且用高精度模板（见 oc-design-guide.md §高精度立绘升级）。

### 定妆照画风串（所选基准 + 题材配色）

> 定妆照只把所选基准画风串的 `[题材配色]` 换成题材配色，其余（画风底盘）不变。换配色不换画风底盘。
> **选元尊V1**（国漫玄幻/古风赛道）时用**元尊V1定妆照画风串**（软边赛璐璐+线稿主导+单阴影）：
> **选厚涂玄幻史诗**（仙侠/玄幻/史诗赛道）时用**厚涂玄幻定妆照画风串**（无线稿半厚涂+体积光+发光），见 §二-B 2B.2 的"常规叙事页基准"。

**元尊V1 定妆照画风串**（国漫玄幻/古风赛道）：
```
Chinese fantasy manga manhua style, soft cel-shading with flat color blocks and a single shadow layer with highlight points. Line-art dominant with strong clean outlines, bold confident manga inking with thick outer lines and thin inner structure lines. Medium-high saturation vivid character colors. Distinct color-zoned palette: [题材配色]. Strong diagonal color opposition across the page. Dramatic lighting with volumetric god rays. No airbrush. No heavy painterly blending. No dry-brush. No ink-wash flying white. No rough sketch. No chibi proportions. No modern clothing. No text overlay.
```

**厚涂玄幻史诗 定妆照画风串**（仙侠/玄幻/史诗赛道）：
```
Chinese xianxia fantasy epic digital painting, luminous semi-thick-paint rendering with subtle implied line structure, forms defined mostly by color contrast with faint structural hints at edges. Bold painterly brushstrokes, rich impasto texture. High saturation vivid colors concentrated in the light core (gold/orange/crimson) attenuating to deep cold shadows (teal/blue/black). Strong warm-cold color opposition across the whole image. Multiple light sources: rim light outlining the subject, self-luminous energy, volumetric god rays, drifting glowing particles and star fields. Sacred transcendent cosmic atmosphere, scale of eons. Distinct color-zoned palette: [题材配色]. No flat cel-shading. No cartoon. No anime flat coloring. No visible outline lineart. No text overlay.
```

> **R3 实测校准（元尊V1）**：为避免 Seedream 把定妆照推向水墨写意，元尊V1定妆照画风串用"软边赛璐璐+线稿主导+单阴影"版本，并在负面约束排掉 `No airbrush / No heavy painterly blending / No dry-brush / No ink-wash flying white`。
> **厚涂玄幻定妆照**：R1 验证 B 半厚涂最稳（画风纯度与角色可读性平衡），正面/侧面立绘均用此串，保证双角度画风统一。

### 入库定妆照记录

| 角色 | 版本 | 画风基准 | 画风串 | 验证图 | 轮次ID | 参数 |
|:-----|:-----|:---------|:-------|:-------|:-------|:-----|
| 秦铭 | v4 | 元尊V1 | 元尊V1软边赛璐璐 + 夜无疆配色 | `char-秦铭-v4-front.png` | R3-定妆 | 1728x2304 |
| 陆泽 | v4 | 元尊V1 | 元尊V1软边赛璐璐 + 夜无疆配色 | `char-陆泽-v4-front.png` | R3-定妆 | 1728x2304 |

> 夜无疆配色：`cold deep indigo-blue and ash-black for the eternal night wilderness, warm crimson-red and ember-orange for the fire-stones' and fire-spring's life-giving light, pale moon-white and soft gold for the fragile warmth of home, ethereal silver-white for the awakening power`

---

## 四、速查

| 我要 | 读什么 |
|:-----|:------|
| 定画风（默认） | 本文件 §2，选元尊V1，换题材配色 |
| 换题材配色 | 本文件 §2.4 题材适配表 |
| 新增画风 | 本文件 §三 入库流程 |
| **画风硬边界/生产路线（常规页直出半赛璐璐，名场面单格高纯度）** | 本文件 §2.5 画风硬边界铁律 |
| 画风如何进提示词 | director-card-template → 6段式PE第2段 |