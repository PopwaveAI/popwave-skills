# 画风基准库（Art Style Baseline）

> Step 0 定画风的唯一来源。**工程化复现铁律：画风不是从零发明的，是从成熟漫画提取、且经 Seedream 实测可复现的基准。**
> 每个基准 = 完整锁定画风串 + 验证图 + 题材适配方法。**选画风 = 从本库选一个基准，换题材只换配色，不换画风底盘。**

## 一、入库标准（可复现性门禁）

一个画风要入库，必须同时满足：

| 门禁 | 标准 | 不通过则 |
|:-----|:-----|:---------|
| **来源** | 从成熟漫画/成熟作品提取，非凭空发明 | 不入库 |
| **可复现基准** | 有 1 张 Seedream 实测通过的代表作作为验证图 | 不入库 |
| **画风串锁定** | 完整画风串（≥300字符）已锁定，记录生成参数 | 不入库 |
| **配色独立** | 画风底盘与配色解耦，换配色不影响画风本体 | 不入库 |

> **当前入库画风：仅 `元尊V1` 一个。** 新画风必须实测通过后追加，禁止跳过实测直接入库。
> **定妆照必须与本库画风同源**：角色定妆照的画风 = 元尊V1底盘，禁止用独立/老龄风格串生成定妆照（否则参考图污染全书画风）。见 §三-b 定妆照PE区。

---

## 二、入库基准：元尊V1（元尊式国漫玄幻·书法墨线厚涂）

> **唯一入库基准。** 从《元尊》漫画第一章复现打磨而来，`整页_复现_v1_非对称分格.jpg` 为验证图。
> 老板定调：**画风以元尊V1为准，换题材只换配色，不换这个画风底盘。**

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

> **铁律：定妆照画风 = 元尊V1底盘。** 定妆照是图生图的参考真相源，选错画风会污染所有下游页面。定妆照 PE 必须实测通过（`guides/pe-test-sop.md` §4.4）后入库。

### 定妆照画风串（元尊V1 + 题材配色）

> 定妆照只把元尊V1画风串的 `[题材配色]` 换成题材配色，其余（赛璐璐+书法墨线+高饱和+对角分区）不变。换配色不换画风底盘。
> **R3 实测校准（重要）**：为避免 Seedream 把定妆照推向水墨写意，定妆照画风串用"软边赛璐璐+线稿主导+单阴影"版本，并在负面约束排掉 `No airbrush / No heavy painterly blending / No dry-brush / No ink-wash flying white`。

```
Chinese fantasy manga manhua style, soft cel-shading with flat color blocks and a single shadow layer with highlight points. Line-art dominant with strong clean outlines, bold confident manga inking with thick outer lines and thin inner structure lines. Medium-high saturation vivid character colors. Distinct color-zoned palette: [题材配色]. Strong diagonal color opposition across the page. Dramatic lighting with volumetric god rays. No airbrush. No heavy painterly blending. No dry-brush. No ink-wash flying white. No rough sketch. No chibi proportions. No modern clothing. No text overlay.
```

### 入库定妆照记录

| 角色 | 版本 | 画风串 | 验证图 | 轮次ID | 参数 |
|:-----|:-----|:-------|:-------|:-------|:-----|
| 秦铭 | v4 | 元尊V1软边赛璐璐 + 夜无疆配色 | `char-秦铭-v4-front.png` | R3-定妆 | 1728x2304 |
| 陆泽 | v4 | 元尊V1软边赛璐璐 + 夜无疆配色 | `char-陆泽-v4-front.png` | R3-定妆 | 1728x2304 |

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