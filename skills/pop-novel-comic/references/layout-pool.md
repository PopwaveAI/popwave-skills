# 排版池

> v3.0.0 新增。CH001 测试验证的 7 种 HTML 排版布局。5 种已验证可直接用于生产（layout-splash / layout-split / layout-fullwide / layout-narrow / layout-climax），2 种标注为进阶布局需谨慎使用（layout-overlay / layout-fullbleed）。

## 核心原则

**HTML 排版是主要产出格式。** 通过本地 HTTP 服务器预览，图片使用外部路径引用（非 base64 内联），保持 HTML 文件轻量、可编辑。

**布局从叙事需求推导，不从模板出发。** 每种布局对应特定的叙事功能和情感强度，选择时必须能回答"为什么用这个布局"。详细推导链见 `storyboard-guide.md` 页面布局系统章节。

**Pillow 拼图作为备选。** 当 HTML 排版环境不可用（无浏览器/无本地服务器）时，回退到 `scripts/assemble_comic.py` 纯 Pillow 拼图，输出 JPEG 长图。

## CSS 层职责铁律

> **v3.1.0 新增**。从玄鉴仙族ch1491和深渊主宰ch016测试中总结。CSS 后叠加的 SVG 特效（速度线、粒子、发光）与 AI 生成的画面脱节，视觉效果为负。特效必须在生图提示词中直接生成。

**CSS 层仅负责三项功能，不处理特效：**

| # | CSS 职责 | 说明 | 禁止事项 |
|:-:|:---------|:-----|:---------|
| 1 | 格子布局 | flex/aspect-ratio/定位控制画框大小和排列 | 禁止用 CSS 创建非矩形画框特效（如 SVG 速度线突破画框） |
| 2 | 文字排版 | 旁白渐变遮罩、对白气泡、字号行高、text-shadow | 禁止用 CSS 叠加拟声字/特效文字（如 SVG 拟声字叠加） |
| 3 | 场景过渡 | scene-break 分隔符、帧间距、出血布局边距 | 禁止用 CSS 创建粒子/光效/动态背景 |

**所有视觉特效必须在生图提示词中直接生成：**

| 特效类型 | 错误做法（CSS 叠加） | 正确做法（提示词内化） |
|:---------|:-------------------|:-------------------|
| 速度线 | SVG 线条叠加在画面上 | 提示词中写 "speed lines radiating from impact point" |
| 冲击波 | CSS 径向渐变 + 模糊 | 提示词中写 "shockwave ripple distorting the air" |
| 发光效果 | CSS box-shadow / filter | 提示词中写 "glowing energy emanating from..." |
| 粒子特效 | CSS particle animation | 提示词中写 "floating embers/particles in the air" |
| 拟声字 | SVG/CSS 文字叠加 | HTML 文字层仅放旁白和对白，拟声字在画面中生成 |

> **核心原则**：画面是 AI 画的，排版是 CSS 做的。两者各司其职，不交叉。CSS 叠加的特效永远无法与 AI 生成的画面完美融合——色调、透视、光影都不匹配。

**所有图片必须使用 `object-fit: cover`**，确保图片填满画框不留黑边：

```css
/* 通用规则：所有布局的图片都必须填满画框 */
.frame img, .layout-splash img, .layout-split img, .layout-fullwide img,
.layout-overlay img, .layout-narrow img, .layout-fullbleed img, .layout-climax img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

> 从深渊主宰ch016测试中总结：narrow 布局缺少 `object-fit: cover` 导致图片下方出现 341px 黑边。所有布局的图片样式必须包含此属性。

## 布局总览

| # | 布局类 | CSS 关键词 | 画幅 | 叙事功能 | 验证状态 |
|:-:|:-------|:-----------|:-----|:---------|:---------|
| 1 | layout-splash | 竖幅3:4 + 标题叠加 + 底部遮罩 | 3:4 竖幅 | 章节开场/场景建立 | 已验证 |
| 2 | layout-split | flex 50/50 + 中线分隔 | 双格 | 对比/并进/反应 | 已验证 |
| 3 | layout-fullwide | 4:3 横幅 + 底部遮罩 | 4:3 横幅 | 情感舒缓/环境交代 | 已验证 |
| 4 | layout-overlay | 主图全幅 + 右下inset 35% | 主图+小图 | 戏剧转折/因果对照 | 进阶 |
| 5 | layout-narrow | flex 30/70 + 左文字右竖图 | 3:7 分割 | 旁白密集/静态段落 | 已验证 |
| 6 | layout-fullbleed | 100vw 突破容器 + 16:9 | 16:9 横幅 | 战斗/冲击/沉浸 | 进阶 |
| 7 | layout-climax | 竖幅3:4 + 85vh + 居中遮罩 | 3:4 竖幅 | 情感高潮/章末收尾 | 已验证 |

---

## 1. 全幅 Splash（layout-splash）

> 竖幅 3:4 全屏画面 + 标题文字叠加 + 底部旁白渐变遮罩。用于章节开场、新场景建立、时间跳跃后的"落地帧"。

### CSS 实现要点

```css
.layout-splash {
  position: relative;
  width: 100%;
  aspect-ratio: 3 / 4;
  overflow: hidden;
}
.layout-splash img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
/* 标题叠加层 */
.layout-splash .splash-title {
  position: absolute;
  top: 8%;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 0.15em;
  color: #fff;
  text-shadow: 0 2px 8px rgba(0,0,0,0.9), 0 0 20px rgba(0,0,0,0.5);
}
/* 底部旁白渐变遮罩 */
.layout-splash .caption-layer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 20px 20px;
  background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
}
```

### 适用场景

- 章节第一帧（建立场景/氛围/时代）
- 时间跳跃后的"落地"帧
- 新地点首次出现的全景建立

### 叙事功能

给读者一个"我在哪"的空间锚点。3:4 竖幅最大化画面信息密度，标题叠加提供章节定位，底部遮罩承载开场旁白。

### 避让规则

- 标题文字叠加区（顶部 8-15%）的画面内容应为天空/远景/墙面等留白区域，避免遮挡人物面部
- 生成图片时提示词需包含"画面上方留白"的构图指令

---

## 2. 垂直分格（layout-split）

> 左右 50/50 分割，中间细线分隔。替代失败的斜切分格方案。用于对比、并进叙事、反应镜头。

### CSS 实现要点

```css
.layout-split {
  display: flex;
  width: 100%;
  gap: 0;
}
.layout-split .split-cell {
  flex: 1;
  position: relative;
  overflow: hidden;
}
.layout-split .split-cell:first-child {
  border-right: 1px solid rgba(255,255,255,0.15);
}
.layout-split .split-cell img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
/* 每格独立的底部遮罩 */
.layout-split .caption-layer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 30px 12px 10px;
  background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
}
```

### 适用场景

- 角色 A 的动作 vs 角色 B 的反应（因果对照）
- 同一时刻两个地点的并进叙事
- 两个情绪对比帧（压抑 vs 释然）
- 替代斜切分格的安全方案

### 叙事功能

将两个有因果或对比关系的帧并置，读者眼睛左右扫描即可建立关联。比上下排列更紧凑，比斜切分格更安全。

### 避让规则

- 两格画面各自独立，不涉及 clip-path 裁切，无需特殊留白指令
- 每格旁白独立叠加，单格旁白不超过 2 行（约 50 字）

---

## 3. 全幅横版（layout-fullwide）

> 4:3 横幅 + 底部旁白遮罩。用于情感舒缓段落、环境交代、角色日常。

### CSS 实现要点

```css
.layout-fullwide {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  overflow: hidden;
}
.layout-fullwide img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.layout-fullwide .caption-layer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 20px 18px;
  background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
}
```

### 适用场景

- 情感舒缓段落（雨后/和解/日常）
- 环境交代（集市/街道/室内全景）
- 角色行走/移动的过渡帧
- 叙事节奏的"呼吸"帧

### 叙事功能

4:3 横幅比 3:4 竖幅更"安静"，视觉重心偏低，适合承载不需要冲击力的信息帧。底部遮罩承载旁白，画面主体不被文字干扰。

### 避让规则

- 底部遮罩区约占画面下方 25%，生成图片时提示词包含"画面下方留白"的构图指令
- 旁白不超过 3 行（约 80 字）

---

## 4. 叠加嵌套（layout-overlay）

> 主图全幅 + 右下角 inset 小图（35% 宽度）。用于戏剧转折、因果对照、时间跳跃。

> **进阶布局**：需确保主图右下角区域内容简单（不遮挡关键信息），inset 小图有独立边框区分。

### CSS 实现要点

```css
.layout-overlay {
  position: relative;
  width: 100%;
  aspect-ratio: 3 / 4;
  overflow: hidden;
}
.layout-overlay .main-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
/* 右下角 inset 小图 */
.layout-overlay .inset-img {
  position: absolute;
  bottom: 12%;
  right: 5%;
  width: 35%;
  aspect-ratio: 3 / 4;
  border: 3px solid #fff;
  box-shadow: 0 4px 20px rgba(0,0,0,0.6);
  overflow: hidden;
  z-index: 2;
}
.layout-overlay .inset-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
/* 底部遮罩（主图旁白） */
.layout-overlay .caption-layer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 20px 18px;
  background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
  z-index: 1;
}
```

### 适用场景

- 戏剧转折：主图展示"现在"，inset 展示"原因/过去"
- 因果对照：主图展示"结果"，inset 展示"触发事件"
- 时间跳跃：主图展示当前时间线，inset 展示闪回画面
- 角色内心冲突：主图展示外部表现，inset 展示内心画面

### 叙事功能

在单帧内建立两个信息层的对照关系。inset 小图通过白色边框和阴影与主图视觉分离，读者先看主图再发现 inset，制造"发现感"。

### 避让规则

- 主图右下角（inset 覆盖区域）不得有关键人物面部或重要视觉信息
- 生成主图时提示词包含"画面右下角留白/简单背景"的构图指令
- inset 小图必须有明显边框区分（3px 白边 + 阴影），避免与主图画面混淆
- 底部旁白遮罩的 z-index 低于 inset，确保不遮挡 inset 内容

---

## 5. 侧边文字 + 竖图（layout-narrow）

> flex 30/70 分割，左侧纯文字旁白 + 右侧竖图。用于旁白密集段落、静态场景、世界观交代。

### CSS 实现要点

```css
.layout-narrow {
  display: flex;
  width: 100%;
  gap: 0;
}
.layout-narrow .text-panel {
  flex: 0 0 30%;
  background: #1a1a1a;
  padding: 24px 16px;
  display: flex;
  align-items: center;
}
.layout-narrow .text-panel .narration {
  color: #e0e0e0;
  font-size: 15px;
  line-height: 1.9;
  text-shadow: 0 1px 3px rgba(0,0,0,0.8);
}
.layout-narrow .image-panel {
  flex: 0 0 70%;
  position: relative;
  overflow: hidden;
  aspect-ratio: 3 / 4;
}
.layout-narrow .image-panel img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
/* 右侧竖图底部遮罩（可选，画面内旁白时用） */
.layout-narrow .image-panel .caption-layer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 30px 14px 12px;
  background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
}
```

### 适用场景

- 旁白密集段落（原文有大段叙述性文字需要保留）
- 静态场景（画面张力不足，用文字弥补）
- 世界观交代（设定信息通过旁白传递，画面提供氛围）
- 角色内心独白（文字承载心理，画面承载表情）

### 叙事功能

左侧 30% 文字面板承载大量旁白（可达 150-200 字），右侧 70% 竖图提供视觉氛围。文字面板深色背景确保可读性，与画面形成"阅读+观看"的双通道体验。

### 避让规则

- 文字面板独立于画面，不受 clip-path 影响
- 右侧竖图如有底部遮罩旁白，单行不超过 2 行（约 50 字）
- 左侧文字面板背景色 #1a1a1a 与整体漫画页面背景协调

---

## 6. 全幅出血（layout-fullbleed）

> 100vw 突破容器边界，16:9 横幅。用于战斗/冲击场景，打破边界制造沉浸感。

> **进阶布局**：出血效果在本地 HTTP 服务器预览时表现最佳。导出为静态图片时出血效果会丢失，仅保留 16:9 横幅。

### CSS 实现要点

```css
/* 容器需要允许溢出 */
.comic-page {
  overflow-x: hidden; /* 允许出血帧横向突破，但页面不出现横向滚动条 */
}
.layout-fullbleed {
  position: relative;
  width: 100vw;
  margin-left: calc(50% - 50vw); /* 突破父容器边界 */
  aspect-ratio: 16 / 9;
  overflow: hidden;
}
.layout-fullbleed img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.layout-fullbleed .caption-layer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 40px 20px 18px;
  background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
}
```

### 适用场景

- 战斗场景的冲击瞬间
- 大规模破坏/爆炸/能量释放
- 角色全力爆发的定格帧
- 需要打破漫画格子边界的"破格"时刻

### 叙事功能

出血布局打破漫画的"格子"边界，画面延伸到视口边缘，制造无边界沉浸感。16:9 宽幅适合横向展开的战斗/冲击场景，强化"事件规模超出画框"的感受。

### 避让规则

- 出血帧前后建议用 scene-break 分隔，视觉上明确"这是一格特殊帧"
- 底部遮罩旁白不超过 2 行（约 50 字），避免遮挡冲击画面
- 生成图片时使用 16:9 横幅构图，提示词包含"wide cinematic shot"

---

## 7. 大格收尾（layout-climax）

> 竖幅 3:4 最大画幅 85vh + 居中文字渐变遮罩。用于情感高潮、章末收尾、名场面定格。

### CSS 实现要点

```css
.layout-climax {
  position: relative;
  width: 100%;
  max-height: 85vh;
  aspect-ratio: 3 / 4;
  overflow: hidden;
  margin: 0 auto;
}
.layout-climax img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
/* 居中文字渐变遮罩（从上下两端向中间渐变） */
.layout-climax .caption-layer {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: linear-gradient(180deg,
    rgba(0,0,0,0.6) 0%,
    transparent 25%,
    transparent 60%,
    rgba(0,0,0,0.85) 100%);
}
.layout-climax .caption-layer .climax-text {
  position: absolute;
  bottom: 12%;
  left: 0;
  right: 0;
  text-align: center;
  padding: 0 24px;
  color: #fff;
  font-size: 16px;
  line-height: 2.0;
  text-shadow: 0 2px 8px rgba(0,0,0,0.9), 0 0 16px rgba(0,0,0,0.6);
}
```

### 适用场景

- 情感高潮定格（角色觉醒/重逢/诀别）
- 章末最后一帧（名场面 + 钩子文字）
- 全章最强视觉冲击帧
- S 级信息的最终呈现帧

### 叙事功能

85vh 最大画幅给最强情感帧最大视觉空间。居中文字渐变遮罩从顶部和底部向中间渐变，确保文字区可读的同时最大化画面展示面积。用于章末时配合钩子文字制造"未完待续"的悬念感。

### 避让规则

- 文字叠加区（底部 12-25%）的画面内容应为环境/地面/暗部区域
- 生成图片时提示词包含"画面下方留暗/留白"的构图指令
- 收尾帧旁白不超过 3 行（约 80 字），最后一句建议是钩子句

---

## 排版避让铁律

> 从 CH001 测试 F2/F3 斜切分格失败中总结。这些规则适用于所有涉及 clip-path 裁切和非标准裁切的布局。

| # | 铁律 | 违反后果 |
|:-:|:-----|:---------|
| 1 | **clip-path 斜切线只能穿过画面空白区**（墙壁/地面/天空），绝不能穿过人物和文字 | 人物被裁切残缺，文字被切割不可读 |
| 2 | **使用斜切布局时，生成图片的提示词必须包含留白构图指令**（如"画面左侧留白""右侧为简单背景"） | 斜切线穿过人物或复杂背景，画面破碎 |
| 3 | **旁白文字不能放在被 clip-path 裁切的区域内** | 文字被裁切，信息丢失 |
| 4 | **斜切无叙事必要性时不使用，垂直分格（layout-split）是更安全的替代方案** | 为花样而花样，画面混乱读者出戏 |

> **核心教训**：CH001 测试中 F2/F3 帧使用 clip-path 斜切分格，斜切线穿过了人物身体和旁白文字区域，导致画面残缺、文字不可读。垂直分格（layout-split）用 50/50 flex 分割 + 细线分隔，完全不涉及裁切，是更安全可靠的并置方案。

---

## 原文旁白嵌入规范

> v3.0.0 新增。旁白文字直接嵌入 HTML 排版，不再依赖 Pillow 拼图叠加。

### 渐变遮罩规范

所有底部旁白遮罩统一使用以下渐变：

```css
background: linear-gradient(0deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
```

- 遮罩从底部 85% 不透明度向上渐变到 0% 透明，过渡区占画面下方约 25-30%
- 确保文字区域背景足够暗（0.85 不透明度），同时画面主体不被过度遮挡

### 文字样式规范

```css
.caption-text {
  color: #fff;
  font-size: 15px;          /* 14-16px 范围 */
  line-height: 1.9;         /* 1.8-2.0 范围 */
  /* 双层 text-shadow 确保暗/亮画面均可读 */
  text-shadow:
    0 1px 4px rgba(0,0,0,0.9),    /* 第一层：近距浓阴影 */
    0 0 12px rgba(0,0,0,0.6);     /* 第二层：远距扩散阴影 */
}
```

- **字号 14-16px**：移动端可读，桌面端不拥挤
- **行高 1.8-2.0**：中文排版透气感，避免文字堆叠
- **text-shadow 至少 2 层**：第一层近距浓阴影保证暗色画面对比度，第二层远距扩散保证亮色画面对比度

### 旁白内容规范

| 规则 | 说明 |
|:-----|:-----|
| **直接使用小说原文** | 旁白内容直接从原文摘取，不二次改写、不概括、不扩写 |
| **单帧不超过 3 行** | 约 80 字以内。超长旁白改用 layout-narrow 侧边文字布局 |
| **超长旁白处理** | 超过 3 行的旁白段，使用 layout-narrow 左侧文字面板承载（可达 150-200 字） |
| **旁白与画面对应** | 每帧旁白对应原文中该帧所呈现的段落，不跨段拼接 |

### 旁白布局选择决策

```
旁白字数 ≤ 80 字（3行内）？
├─ 是 → 底部渐变遮罩（layout-splash/fullwide/fullbleed/climax/overlay）
└─ 否 → 侧边文字面板（layout-narrow）
```

---

## 画风适配规则

> 不同叙事场景需要不同强度的画面呈现。布局选择应匹配场景的戏剧性强度。

| 场景类型 | 戏剧性强度 | 推荐布局 | 理由 |
|:---------|:----------|:---------|:-----|
| 高戏剧性（觉醒/变身/决战） | 极高 | layout-splash / layout-climax | 大格全幅发挥厚涂光影优势，给最强情感最大画幅 |
| 战斗/冲击（爆炸/突袭/破坏） | 高 | layout-fullbleed | 出血打破边界，16:9 宽幅展开冲击场面，沉浸感最强 |
| 戏剧转折（反转/揭示/对照） | 中高 | layout-overlay | 主图+inset 双层对照，在单帧内建立因果/时间对照 |
| 情感舒缓（日常/和解/过渡） | 中低 | layout-fullwide | 4:3 横幅安静沉稳，底部遮罩承载舒缓旁白 |
| 静态/旁白密集（独白/设定/回忆） | 低 | layout-narrow | 文字面板弥补画面张力不足，竖图提供氛围 |
| 对比/并进（双视角/反应） | 中 | layout-split | 50/50 并置建立关联，安全可靠 |
| 情感高潮/章末（名场面/钩子） | 极高 | layout-climax | 85vh 最大画幅 + 居中遮罩，章末最强定格 |

### 布局节奏建议

一章漫画的布局节奏应遵循"慢→快→慢"的节奏弧：

```
开场（splash/fullwide）→ 发展（split/narrow/overlay 交替）→ 高潮（fullbleed/climax）→ 收尾（climax）
```

- **不要连续使用 3 个相同布局** — 读者视觉疲劳
- **每章至少 1 个 splash 或 climax** — 视觉锚点
- **章末最后一帧建议用 climax** — 最大画幅给最强情感/钩子
- **fullbleed 每章不超过 1-2 次** — 出血帧是"破格"时刻，过多则失去冲击力

---

## HTML 排版技术规范

### 图片引用方式

**使用外部图片路径引用，不使用 base64 内联。** 通过本地 HTTP 服务器预览。

```html
<!-- 正确：外部路径引用 -->
<img src="output/frame1.png" alt="">

<!-- 错误：base64 内联（v2.11.0 已废弃的问题方案） -->
<img src="data:image/png;base64,iVBORw0KGgo..." alt="">
```

### 本地 HTTP 服务器预览

```powershell
# 在章节目录下启动本地 HTTP 服务器
cd "{漫画项目}/第{N}章"
python -m http.server 8000

# 浏览器打开
# http://localhost:8000/index.html
```

> 本地 HTTP 服务器解决了 v1.2.0 中 popwave webview 安全策略禁止加载外部资源的问题。通过 HTTP 协议加载图片，浏览器/webview 正常渲染。

### HTML 页面结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{漫画标题} - 第{N}章</title>
  <style>
    /* 全局样式 */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #0d0d0d;
      font-family: "Noto Sans SC", "Microsoft YaHei", sans-serif;
      max-width: 900px;
      margin: 0 auto;
      overflow-x: hidden;
    }
    .comic-page { width: 100%; }
    .frame { margin-bottom: 4px; }
    .scene-break {
      text-align: center;
      padding: 20px 0;
      color: #555;
      letter-spacing: 1em;
    }
    /* 各布局类样式见上方各布局章节 */
  </style>
</head>
<body>
  <div class="comic-page">
    <!-- 帧序列 -->
    <div class="frame layout-splash">
      <img src="output/frame1.png" alt="">
      <div class="splash-title">第一章 · 绯红</div>
      <div class="caption-layer">
        <div class="caption-text">没有食物了。</div>
      </div>
    </div>

    <div class="scene-break">◇ ◇ ◇</div>

    <!-- 更多帧... -->

    <div class="frame layout-climax">
      <img src="output/frame8.png" alt="">
      <div class="caption-layer">
        <div class="climax-text">脚步声，越来越近……</div>
      </div>
    </div>
  </div>
</body>
</html>
```

### 布局类映射表（HTML）

> Step 2 拼图配置中的 `layout` 值对应 HTML 布局类（由 Step 1 分格设计表确定，**继承不重新选择**）。

| 分格设计表布局类 | HTML layout 值 | Pillow layout 值（备选） | 说明 |
|:----------------|:--------------|:----------------------|:-----|
| panel-splash | layout-splash | scene | 竖幅3:4全屏+标题+底部遮罩 |
| panel-split | layout-split | half×2 | 左右50/50分割 |
| panel-fullwide | layout-fullwide | full | 4:3横幅+底部遮罩 |
| panel-overlay | layout-overlay | — | 主图全幅+右下inset 35% |
| panel-narrow | layout-narrow | — | flex 30/70 左文字右竖图 |
| panel-fullbleed | layout-fullbleed | impact | 100vw出血+16:9横幅 |
| panel-climax | layout-climax | hook | 竖幅3:4+85vh+居中遮罩 |

> Pillow 备选方案不支持 layout-overlay 和 layout-narrow（需文字面板/嵌套图），这两种布局仅限 HTML 排版。遇到这两种布局且必须用 Pillow 时，回退为 layout-fullwide。

### scene-break（场景分隔）

在帧之间插入场景分隔符，对应导演卡页面设计表的页面边界：

```html
<div class="scene-break">◇ ◇ ◇</div>
```
