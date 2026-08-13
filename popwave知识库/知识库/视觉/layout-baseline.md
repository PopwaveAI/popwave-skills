---
id: layout-baseline
lib: 知识库
cat: 视觉
version: 1.0.0
tags: [视觉]
---
# 排版基准库（Layout Baseline）

> Step 2 分页设计的唯一来源。**工程化复现铁律：排版不是从零发明的，是从元尊真实页面逐页拆解、且经 Seedream 实测可复现的分页结构。**
> 每个模板 = 真实页面的几何复刻 + 锁定分格指令 + 叙事功能。**选排版 = 从本库选一个已验证结构，换题材里填空内容。**

## 一、入库标准（可复现性门禁）

| 门禁 | 标准 | 不通过则 |
|:-----|:-----|:---------|
| **来源** | 从成熟漫画真实页面逐页拆解，非凭空发明 | 不入库 |
| **可复现基准** | Seedream 实测通过（结构复现≥90%） | 不入库 |
| **分格指令锁定** | 精确的百分比分格指令已锁定 | 不入库 |
| **位置精度** | 复杂结构（内嵌/叠压/三列）位置精度达标 | 不入库 |

> **当前排版库：元尊 YZ-1~13 十三个已验证结构。** 已丢掉从零发明的12种基础花样（可复现性不保证）。

---

> **分格线统一规范（铁律）**：全模板分格线统一为**细黑线**（`thin black gutter`），颜色锁死 `black`，禁止混用 `Thick`/`white` 或其他颜色。所有模板指令中的分格线措辞一律为 `thin black gutters`（或 `thin black gutter`），如遇 `Thick` 或未锁色，一律改为细黑线。
>
> **⚠️ 唯一例外 YZ-5**：`YZ-5 全幅+内嵌·宏观微观页` 的前景叠压格用白色粗框浮于背景上，刻意制造 Z 轴层次（见第十七行"关键发现"第2条），**属于前景面板的叠压边界，不是普通格间分格线**，允许保留。除 YZ-5 前景叠压外，其余所有模板的格间分格线一律细黑线。

## 二、元尊真实分页的三大规律（先读这个）

1. **非对称是默认，对称是例外**。元尊几乎没有均分网格，全是"一大格主导 + 若干小格"的非对称结构，视觉重心永远落在情绪爆发格。
2. **格数随情绪密度变化**。建立页 2-3 格、推进页 4-6 格、高潮页 1-2 格（或全幅）。一页内格数递减 = 心理压迫加剧。
3. **色彩分区 + 破框出血是叙事语法**。大到整页（左冷右暖），小到单格（破框让情绪溢出框外），色彩与边框都是"情绪的分界线"。

---

## 三、13种已验证分页模板

### YZ-1：左大右双·危机对仗页 ★★★★☆

> 危机/受难时刻，大格承载动作，两小格收束情绪。

```
┌─────────────────────┐
│                     │
│  格1 大竖格(60%)     │   ← 主导动作/力量爆发
│  主角背影+能量漩涡    │
│  ┌────────┬────────┐ │
│  │ 格2 小 │ 格3 小 │ │  ← 双小格：受害/反应特写
│  └────────┴────────┘ │
└─────────────────────┘
```

**分格指令（锁定）**：
```
A vertical webtoon comic page with one large vertical panel on the left (60% height) and two smaller panels side by side at the bottom (40% height). Thin black gutters between all panels.
```

**叙事功能**：大格承载"发生了什么"，两小格承载"谁在承受/反应"。用于危机爆发、力量觉醒、灾难降临。
**节奏**：大格慢（沉浸）→ 双小格快（情绪点）→ 压迫感收束。

---

### YZ-2：上横下三·对话揭示页 ★★★★☆

> 上通栏全景建立 + 下左窄条对话 + 下右大格揭示。

```
┌─────────────────────┐
│  格1 上通栏横格(45%)  │  ← 全景建立/世界观
│  宫殿/场景全景        │
├──────┬──────────────┤
│ 格2  │  格3 大格      │  ← 窄条=对话/停顿，大格=揭示/高潮
│ 窄竖条│  关键道具特写   │
│ 25%  │  75%         │
└──────┴──────────────┘
```

**分格指令（锁定）**：
```
A vertical webtoon comic page with a wide horizontal panel at the top (full width, 45% height) and a bottom section split into two panels: a tall narrow vertical panel on the left (25% width) and a large panel on the right (75% width). Thin black gutters between all panels.
```

**叙事功能**：上格建立场景，下左窄条承载对话/独白（视觉信息少，节奏慢），下右大格承载视觉冲击（道具/揭示/情绪爆发）。**窄条对大格 = 对话的"静"对画面的"动"。**
**节奏**：上慢（全景）→ 左下更慢（对话停顿）→ 右下急（大格冲击）。

---

### YZ-3：左列右幅·蒙太奇冲击页 ★★★★★

> T型动线，左侧信息积累，右侧情绪爆发。含内嵌子格（画中画）。

```
┌──────────────────┬──────────────┐
│  格1 场景(60%)    │              │
│  云端宫殿/全景     │              │
├──────────────────┤  格4 全幅    │
│  格2 人物(20%)    │  情绪特写     │
├──────────────────┤  (100%高)    │
│  格3 道具(20%)    │  ┌──────┐    │
│  卷轴/线索        │  │ 格5  │    │  ← 内嵌子格
│                  │  │小道具│    │     (画中画)
└──────────────────┴──┴──────┴────┘
```

**分格指令（锁定）**：
```
A vertical webtoon comic page with a left column of 3 stacked panels (60% width) and a large full-height panel on the right (40% width). Left column: top panel 60% height, middle panel 20% height, bottom panel 20% height. Right panel occupies the full page height. Inside the right panel, a small inset panel in the upper-left corner (15% of the right panel). Thin black gutters.
```

**叙事功能**：左侧三格逐步累积信息（场景→人物→线索），右侧全幅格集中爆发情绪（大特写/关键画面）。**"量变→质变"的视觉隐喻**。内嵌子格将"线索源头"与"情绪载体"并置，建立因果。
**节奏**：左慢（纵向积累）→ 右急（横向截断+全幅冲击）。T型动线。

---

### YZ-4：右大左双·情绪递进页 ★★★★☆

> 左右两竖格，一宽一窄，一问一答。

```
┌──────────────┬──────────┐
│              │          │
│  格1 大竖格(60%)│ 格2 窄竖格│
│  场景/揭示      │ (40%)    │
│  篡夺者/暗面    │ 主角震惊   │
│              │ 特写      │
│              │          │
└──────────────┴──────────┘
```

**分格指令（锁定）**：
```
A vertical webtoon comic page divided into two tall vertical panels side by side: a wide panel on the left (60% width) and a narrow panel on the right (40% width). Both panels span the full page height. Thin black gutter between them.
```

**叙事功能**：左宽格承载"真相/事件"（大画面），右窄格承载"主角反应"（特写）。**"发生的事"对"承受的人"**。窄格天然压迫感，强化主角震惊。
**节奏**：一宽一窄，一问一答，视觉对仗。

---

### YZ-5：全幅+内嵌·宏观微观页 ★★★★★

> 大背景全幅 + 前景叠压两格，压缩时间空间。

```
┌─────────────────────┐
│  格1 大背景全幅(65%)  │  ← 宏观场景/战争/全景
│  攻城战/火烧城        │
│  ┌─────────┐         │
│  │ 格2 主角 │  ┌─────┐│
│  │ 中景方格 │  │格3  ││  ← 前景叠压
│  └─────────┘  │情绪  ││
│               │冲击  ││
│               └─────┘│
└─────────────────────┘
```

**分格指令（锁定）**：
```
A vertical webtoon comic page with a large full-page background panel of a grand scene (65% height). Two smaller foreground panels overlap on top of the background: a medium square panel in the lower-left and a small panel in the lower-right. The foreground panels have distinct borders to separate them from the background. Thick framing.
```

**叙事功能**：大背景格承载宏观语境（战争/历史/全景），前景叠压格承载主角的追问与情绪反应。**"大历史"对"个人命运"**。空间压缩但时间连续。
**节奏**：背景大格慢（沉浸）→ 前景小格快（个人反应）。

---

### YZ-6：三列纵向分区·设定揭示页 ★★★★☆

> 6格3区，左中右三列物理性分区，色彩/情绪逐列过渡。

```
┌──────┬──────────┬──────────┐
│ 格1  │  格4 竖长  │          │
│ 小竖  │  夜空龙纹  │  格6 全高 │
│ 头像  ├──────────┤  水墨竖条 │
│ 格2  │  格5 竖短  │  (阴谋/   │
│ 大圣光│  蛟蟒圆盘  │   反转)   │
│ 场景  │          │          │
│ 格3  │          │          │
│ 横条  │          │          │
└──────┴──────────┴──────────┘
```

**分格指令（锁定）**：
```
A vertical webtoon comic page divided into 3 vertical columns (30% / 40% / 30% width). Left column: a small vertical panel at top, a large panel in the middle, a horizontal strip at bottom. Middle column: a tall vertical panel at top, a shorter vertical panel below. Right column: one tall full-height vertical panel. Thin black gutters between all panels.
```

**叙事功能**：三列物理性分区 = 三阶段情绪（左=祥瑞/事件，中=对比/设定，右=阴谋/反转）。**色彩逐列过渡**（金→蓝→水墨黑白）强化"光明→揭秘→阴谋"曲线。右列全高水墨条带是"隔离黑暗真相"的物理边界。
**节奏**：三列并进，左中右 = 背景→对比→反转。设定揭示页专用。

---

### YZ-7：封面+四格·话首双功能页 ★★★★☆

> 左封面（角色特写+标题）+ 右四格叙事。

```
┌──────────────┬──────────────────┐
│  左封面区(45%)│ 格1 全宽横格(25%)   │
│  角色特写     ├──────────────────┤
│  标题+话名    │ 格2 全宽横格(25%)   │
│  纵向贯穿     ├─────────┬────────┤
│              │ 格3 左半 │ 格4 右半│
│              │ 窄纵格   │ 窄纵格  │
└──────────────┴─────────┴────────┘
```

**分格指令（锁定）**：
```
A vertical webtoon comic page with a left column (45% width) showing a full-height character portrait, and a right section (55% width) with 4 panels: two full-width horizontal panels on top (each 25% height), and two smaller vertical panels side by side at the bottom (each 50% width). Thin black gutters.
```

**叙事功能**：话首/关键页专用。左封面区承担"角色名片+章节标识"，右四格承担叙事推进。**"2+2阶梯式"**：上两格全宽（铺垫）→ 下两格分裂（爆发/揭示）。
**节奏**：左静（肖像）→ 右动（叙事）；上缓（铺垫）→ 下急（爆发）。

---

### YZ-8：全幅单格·名场面/章末钩子页 ★★★★★

```
┌─────────────────────┐
│                     │
│  全幅单格            │
│  无边框·无虚线        │
│  主角特写/名场面      │
│  + 情绪冲击          │
│                     │
└─────────────────────┘
```

**分格指令（锁定）**：
```
A single full-page webtoon panel, no gutters, no borders, full bleed.
```

**叙事功能**：S级名场面/章末钩子/情绪顶点。全幅无框 = 情绪溢出页面的边界。
**节奏**：完全静止，但画面内部张力极强。

---

### YZ-9：斜切格·心境崩坏页 ★★★★★

> 对角线不对等切分，用于心境崩坏/记忆碎片/现实扭曲/突发危机。

```
┌──────────────────╲
│                  ╲
│  格1 大三角(70%)   ╲ ← 上右大三角：崩坏主画面
│                  ╲
│  对角线缝         ╲
│──────────────────╲
│  格2 小三角(30%)  ╲
└──────────────────╲
```

**分格指令（锁定）**：
```
A vertical manga comic page divided diagonally into two unequal triangular panels by a thin diagonal black gutter running from the bottom-left corner to the top-right corner. The large triangular panel on the upper-left side occupies about 70% of the page, the small triangular panel on the lower-right side occupies about 30%.
```

**叙事功能**：对角线 = 失衡/崩塌的物理隐喻。大三角承载崩坏主画面（人物崩溃/世界扭曲），小三角承载"碎片/闪回/残余意志"。用于心境崩坏、记忆碎片、现实扭曲、突发危机。
**节奏**：斜切本身制造失衡，大三角慢（沉浸崩坏）→ 小三角快（碎片闪回）。
**工具级限制**：Seedream 对斜线会自然加粗（实测 8-12px），无法做到竖/横线的 2-3px 细线。斜切类模板的粗线是固有特征，可接受。

---

### YZ-10：蓄力爆发页（抑扬） ★★★★☆

> 上段压缩蓄力 + 下段全幅爆发，"抑→扬"一气呵成。三蓄力格有**平铺**与**交错斜切**两种子变体。

```
┌─────────────────────┐
│ 格1 蓄力(15%)         │
├─────────────────────┤
│ 格2 蓄力(15%)         │
├─────────────────────┤
│ 格3 蓄力(15%)         │
├─────────────────────┤
│                     │
│ 格4 全宽大格(55%)     │ ← 爆发/释放
│                     │
└─────────────────────┘
```

**分格指令（锁定 · 基础平铺版）**：
```
A vertical manga comic page with a top section of three small compressed horizontal panels stacked tightly (each about 15% height, total 45%) and one large full-width horizontal panel at the bottom (55% height). Thin black gutters between all panels.
```

**分格指令（锁定 · 交错斜切 V3-A · 之字形 · 推荐）**：
```
A vertical manga comic page with a top section divided into three interlocking slanted panels by a zigzag of two intersecting diagonal thin black gutters, the three slanted parallelogram panels tilting in alternating directions and interlocking like a woven weave, and one large full-width horizontal panel at the bottom (about 50% height). Thin black gutters.
```

**分格指令（锁定 · 交错斜切 V3-B · 交叉汇聚 · 备选）**：
```
A vertical manga comic page with a top section divided by two diagonal thin black gutters crossing each other in an X shape, creating three slanted panels that funnel toward a central focus point, and one large full-width horizontal panel at the bottom (about 50% height). Thin black gutters.
```

**叙事功能**：上三小格逐步蓄力（铺垫/累积/提升），下全宽大格一次性爆发。"量变→质变"纵向节奏。**基础平铺版三格可用镜距逼近（远→中→特写）+ 能量聚焦（微光→旋涡→压缩）破重复**；交错斜切版用斜向织感强化"凝聚/不稳定"。
**节奏**：上慢（蓄力）→ 下急（爆发）。交错斜切版蓄力张力更强。
**工具级限制**：之字形（V3-A）斜线侥幸最细（2-3px）；X 形交叉（V3-B）斜线偏粗（15-20px）。

---

### YZ-11：破框贯穿页·动作溢出页 ★★★★☆

> 中心主格 + 主角动作破框出血，情绪溢出画格边界。

```
┌─────────────────────┐
│  主格(80%)           │
│  ┌───────────────╮   │
│  │ 主角出手        │   │
│  │ 拳/兵刃撞破上缘  │ ← 破框出血
│  ────────────────╯   │
│  出血余白(20%)        │
└─────────────────────┘
```

**分格指令（锁定）**：
```
A vertical manga comic page with one large central panel occupying about 80% of the page, framed by a thin bold black border, and the remaining 20% as empty dark margin around it. The main action character breaks out of the panel, fist and body shattering through the top edge of the frame, bursting outward beyond the border into the margin.
```

**叙事功能**：破框 = 力量/情绪溢出画格边界。主格承载动作主体，角色肢体冲破边框制造"冲出画面"的冲击力。用于动作爆发、情绪顶点、力量不受控。
**节奏**：主格慢（沉浸动作）→ 破框瞬间爆发。**核心叙事语法是"破框出血"，即使主格占比略低（60-70%）也成立**。

---

### YZ-12：对称文戏页·对立对谈页 ★★★★☆

> 左右完全对称两竖格，一左一右，对峙/对谈/对立。

```
┌─────────────────────┐
│         │           │
│         │           │
│ 格1 左   │ 格2 右     │
│ 50%     │ 50%       │
│ 主体A    │ 主体B      │
│         │           │
│         │           │
└─────────┴───────────┘
```

**分格指令（锁定）**：
```
A vertical manga comic page divided symmetrically into two equal full-height vertical panels side by side (each 50% width), separated by a thin vertical black gutter.
```

**叙事功能**：完全对称 = 势均力敌的对立/对谈。左格主体A、右格主体B，视觉天平均衡。**对称是例外，一旦出现即强调"对峙"**。用于正面对峙、谈判对谈、立场对立。
**节奏**：一左一右，二问一答，视觉对仗。
**工具级限制**：竖直格线 Seedream 可精确控制细度（2-3px），犀利。

---

### YZ-13：章末留白页·余韵钩子页 ★★★★★

> 上部大面积黑暗留白 + 下部一帧孤单意象，余韵/钩子。

```
┌─────────────────────┐
│                     │
│  大面积留白(65%)      │ ← 空、静、余韵
│  零散星光/尘埃        │
│                     │
├─────────────────────┤
│  底部单格(35%)        │ ← 孤单意象/钩子
│  远影/独物           │
└─────────────────────┘
```

**分格指令（锁定）**：
```
A vertical manga comic page with a large dark empty negative space occupying the top (about 65% height, mostly blank with a few faint scattered dust motes or stars) and one small focused panel at the bottom (about 35% height) showing a lone distant figure, separated by a thin black gutter.
```

**叙事功能**：大面积留白 = 余韵/无力感/孤独。顶部空静营造"余音"，底部单帧承载"钩子/去向/孤单意象"。用于章末收束、情绪沉淀、悬念钩子。
**节奏**：上部极慢（留白呼吸）→ 底部单帧聚焦（钩子）。

---

### YZ-INFO：信息页·半文半图（图文同页） ★★★★★

> **信息页专用模板（v7.22.0）**：上半 50% = Seedream 单格大图（画风统一/漫画沉浸），下半 50% = HTML 文字块（文字层物理上由 HTML 承载，Seedream 不画可读文字）。**禁止纯 HTML 搭整页**——那会让信息页像网页插进漫画滚动流。图文同页不可分离。

```
┌─────────────────────┐
│                     │
│  上半 50%（Seedream） │  ← 单格全宽大图·全出血
│  与设定相关的象征画面  │     意象/场景/象征
│                     │
├─────────────────────┤
│                     │
│  下半 50%（HTML）     │  ← 文字块：2-4 条分条信息
│  分条信息1 …         │     每条 ≤80 字
│  分条信息2 …         │     直接摘原文/浓缩
│                     │
└─────────────────────┘
```

**上半 Seedream 分格指令（锁定）**：
```
A vertical webtoon comic page with only the upper half (50% height) occupied by a single full-width full-bleed comic art panel without any borders or gutters, the lower half left as empty plain blank space with no panels, no gutters, no borders, reserved purely as a clean background for text overlay.
```

**叙事功能**：上半画面提供视觉锚点（读者先"看到"再"读到"），下半文字承载浓密信息（世界观/背景/长原文）。**图文同页不可分离**——画面让读者不划走，文字讲清设定。
**节奏**：上半慢（画面沉浸）→ 下半中（信息消化）。穿插铁律：前后必须各有漫画页，禁止连续 2 个信息页，占页数 ≤30%。

> **注意**：YZ-INFO 只锁上半 Seedream 的指令。下半文字块由 HTML 后处理承载，**不进 Seedream**，不参与分格。上半画面必须是与设定相关的意象/场景/象征，非纯色块。

---

## 四、模板选择速查表

| 页类型 | 元尊模板 | 格数 | 叙事语法 |
|:-------|:---------|:-----|:---------|
| 危机/灾难页 | YZ-1 左大右双 | 3格 | 大格动作+双小格受难 |
| 对话/揭示页 | YZ-2 上横下三 | 3格 | 全景+窄条对话+大格冲击 |
| 蒙太奇冲击页 | YZ-3 左列右幅 | 4-5格 | 左积累+右爆发+T型动线 |
| 情绪递进页 | YZ-4 右大左双 | 2格 | 发生的事对承受的人 |
| 宏观微观页 | YZ-5 全幅+内嵌 | 3格 | 大历史对个人命运 |
| 设定揭示页 | YZ-6 三列分区 | 6格 | 三列=三阶段情绪过渡 |
| 话首双功能页 | YZ-7 封面+四格 | 5格 | 角色名片+叙事推进 |
| 名场面/钩子页 | YZ-8 全幅单格 | 1格 | 情绪溢出页面边界 |
| 心境崩坏页 | YZ-9 斜切格 | 2格 | 对角线失衡+崩坏主画面对碎片闪回 |
| 蓄力爆发页 | YZ-10 抑扬 | 4格 | 上三格蓄力+下全宽爆发（可斜切） |
| 动作溢出页 | YZ-11 破框贯穿 | 1格 | 拳/兵刃破框出血，情绪溢出画格 |
| 对立对谈页 | YZ-12 对称 | 2格 | 完全对称=势均力敌的对峙/对谈 |
| 章末余韵页 | YZ-13 留白 | 2区 | 上部大面积留白+底部单帧钩子 |
| 信息页·半文半图 | YZ-INFO | 图文1:1 | 上半Seedream单格大图锚点+下半HTML文字块 |

## 五、Seedream 复现实测结论

| 模板 | 结构复现 | 位置精度 | 结论 |
|:-----|:---------|:---------|:-----|
| **YZ-1 左大右双·危机页** | ✅ 左大竖格+下双小格全复现 | ★★★★☆ 下双格比例约6:4 | **可用**（本轮夜无疆P3验证） |
| **YZ-2 上横下三·对话页** | ✅ 上通栏横格+下左窄右大全复现 | ★★★★☆ 下栏常压成二格变体 | **可用**（结构稳定，下栏格数适配） |
| **YZ-3 左列右幅·T型** | ✅ 左3格+右全幅+内嵌子格全复现 | ★★★★☆ 子格偏左上 | **可用**，架构100%匹配 |
| **YZ-5 全幅+内嵌·叠压** | ✅ 大背景全幅+2前景格叠压全复现 | ★★★★★ 全幅背景无切割 | **完美可用** |
| **YZ-6 三列分区·设定揭示** | ✅ 左3-中2-右1三列全复现 | ★★★★★ 三列等宽精确 | **完美可用**（本轮夜无疆P8验证） |
| **YZ-8 全幅单格·名场面** | ✅ 全幅无框单格全复现 | ★★★★★ 无切割 | **完美可用**（本轮夜无疆P5验证） |
| **YZ-9 斜切格·心境崩坏** | ⚠️ 大三角60-65%/小三角35-40%，非严格70:30 | ★★★☆☆ 斜线减细有限（8-12px） | **可用**（斜切粗线=固有特征） |
| **YZ-10 蓄力爆发·抑扬** | ✅ 上三格+下全宽大格全复现 | ★★★★☆ 基础横缝细；V3-A之字形2-3px | **完美可用**（V3-A之字形推荐） |
| **YZ-11 破框贯穿·动作溢出** | ⚠️ 主格60-70%未达80%，余白偏多 | ★★★★☆ 上缘破框+拳臂冲出+碎片三层完整 | **可用**（破框语法优先，占比放宽） |
| **YZ-12 对称文戏·对立对谈** | ✅ 左右各48%均分、等高 | ★★★★★ 细竖缝精确 | **完美可用** |
| **YZ-13 章末留白·余韵钩子** | ✅ 上部65%/下部35% | ★★★★★ 负空间干净 | **完美可用** |

**关键发现**：
1. **三列分区（YZ-6）是 Seedream 最擅长的复杂结构**，三列等宽+各列格子数不同（3/2/1）都能精确复现，且三列色彩分区也成功隔离。
2. **全幅+前景叠压（YZ-5）执行完美**，前景格用白色粗边框清晰浮于背景之上，Z轴层次明确。
3. **内嵌子格（YZ-3）位置会偏左上**而非几何中心，但这是艺术化调整，不影响结构定义。
4. **非对称+大格主导是元尊质感的根源**，Seedream 完全能执行，回调用本模板库即可获得元尊级分页。
5. **本轮夜无疆×元尊实测（2026-08-03）**：YZ-1/2/6/8 结构复现均稳定（≥90%）。YZ-2 下栏若指定"下三格"，Seedream 常压成二格变体，建议按"上横+下二格"使用或明确格式；YZ-8 全幅单格用于名场面可靠。排版层与角色层（v4定妆图）已稳定，画风层见 `pe-log-2026-08-03.md` R4-R8。
6. **本轮深渊主宰×YZ-9~13 实测（2026-08-06）**：全模板分格线统一改细（thin gutter）。**竖直/水平格线 Seedream 可精确控细（2-3px），斜线/交叉线会自然加粗（YZ-9斜线8-12px、YZ-10 V3-B的X线15-20px）——斜切类模板的粗线是固有特征，可接受**。YZ-10 V3-A之字形交错是本轮亮点（斜线侥幸最细2-3px + 三格↘↗↘完美交错）。YZ-11 破框出血三层语言完整，主格占比略低不影响叙事语法。测试图见 `深渊主宰-漫画/第5章/output/yz_templates/T2-*.png`。

## 六、速查

| 我要 | 读什么 |
|:-----|:------|
| 选分页结构 | 本文件 §三 13种模板 + YZ-INFO |
| 判断页类型用哪个模板 | 本文件 §四 速查表 |
| 分格指令（锁定） | 各模板"分格指令"段，直接复制 |
| 排版如何进提示词 | director-card-template → 6段式PE第3段 |