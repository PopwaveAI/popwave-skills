# 页面排版+文字叠加指南

> v4.0 参考文件。画面是 AI 画的（Seedream 直出完整漫画页），文字是 HTML 叠的（旁白条/对白气泡）。各司其职。

## 设计哲学

**v4.0 核心变化**：生成单位从"格"升级为"页"。Seedream 在单张图内直出完整漫画页（含分格线、多格内容、镜头语言），HTML **不再做格子布局**，只负责：
1. 页面图片全宽展示（移动端优先）
2. 文字叠加（旁白条/对白气泡）
3. 页面间隔符（scene-break）

| v3.x（格级） | v4.0（页级） |
|:-------------|:------------|
| HTML 做格子布局（7种布局类） | 画面已有分格线，HTML 不做格子布局 |
| 每格一张图，HTML 排列组合 | 每页一张图（含多格），HTML 全宽展示 |
| CSS 负责格子大小/间距/特效 | CSS 只负责文字叠加+页面间距 |
| 布局漂移风险（50%帧被擅自改布局） | 无布局漂移风险（画面是AI直出的） |

## 页面配置 JSON 规范

`页面配置.json` 是 Step 2b 生成 HTML 的输入配置：

```json
{
  "title": "{章节标题}",
  "subtitle": "第{N}章 · {章节名}",
  "poem": "鉴中千秋血，镜外万骨枯。六代薪传火，一鉴照仙途。",
  "seal": {
    "text": "终",
    "position": "bottom-right"
  },
  "pages_dir": "output",
  "output_html": "index.html",
  "footer": "popwave",
  "pages": [
    {
      "file": "page1.png",
      "captions": [
        {"type": "narration", "text": "旁白文字", "position": "bottom"}
      ]
    },
    {"separator": true},
    {
      "file": "page2.png",
      "captions": [
        {"type": "narration", "text": "旁白文字", "position": "bottom"},
        {"type": "dialogue", "text": "对白文字", "position": "top-right"}
      ]
    },
    {"separator": true},
    {
      "file": "page3.png",
      "captions": []
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `title` | string | 是 | 章节标题 |
| `subtitle` | string | 是 | 章节副标题（第N章 · 章节名） |
| `poem` | string | 否 | 定场诗内容（≤28字），仅章节标题页渲染。详见 `cultural-elements-guide.md` |
| `seal` | object | 否 | 朱砂印章配置。详见 `cultural-elements-guide.md` |
| `seal.text` | string | 否 | 印章文字（1-2字），如"终""卷"等 |
| `seal.position` | string | 否 | 印章位置（`bottom-right` / `top-right`），默认 `bottom-right` |
| `pages_dir` | string | 是 | 页面图片目录（相对路径，通常为 `output`） |
| `output_html` | string | 是 | 输出 HTML 文件名（通常为 `index.html`） |
| `footer` | string | 否 | 页脚品牌信息（默认 `popwave`） |
| `pages` | array | 是 | 页面数组，按阅读顺序排列 |
| `pages[].file` | string | 是 | 页面图片文件名（如 `page1.png`） |
| `pages[].separator` | boolean | - | 若为 `true`，此元素是页面间隔符（不渲染图片） |
| `pages[].captions` | array | 否 | 文字叠加数组 |
| `captions[].type` | string | 是 | `narration`（旁白条）/ `dialogue`（对白气泡） |
| `captions[].text` | string | 是 | 文字内容（直接使用小说原文，≤15字/条） |
| `captions[].position` | string | 是 | 定位（见下方位置规范） |

### 位置规范

| position 值 | 适用类型 | 定位说明 |
|:-----------|:---------|:---------|
| `bottom` | narration | 底部全宽渐变遮罩条 |
| `top` | narration | 顶部全宽渐变遮罩条 |
| `top-left` | dialogue | 左上角气泡 |
| `top-right` | dialogue | 右上角气泡 |
| `bottom-left` | dialogue | 左下角气泡 |
| `bottom-right` | dialogue | 右下角气泡 |
| `center` | dialogue | 居中气泡（少用） |

## 文字叠加类型

### 旁白条（narration）

**用途**：旁白叙述、内心独白、环境描写、世界观交代。直接使用小说原文，不二次改写。

**视觉规范**：
- 全宽渐变遮罩（底部或顶部）
- 黑色半透明背景 + 白色文字
- text-shadow 双层确保暗/亮画面均可读
- 字号 14-16px，行高 1.8-2.0
- 单条旁白不超过 3 行（约 80 字）

```css
.caption-narration {
  position: absolute;
  left: 0;
  right: 0;
  padding: 40px 20px 16px;
  background: linear-gradient(0deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.5) 60%, transparent 100%);
  color: #f5f0e8;
  font-size: 15px;
  line-height: 1.9;
  text-shadow: 0 1px 3px rgba(0,0,0,0.9), 0 0 8px rgba(0,0,0,0.6);
}
.caption-narration.top {
  top: 0;
  bottom: auto;
  padding: 16px 20px 40px;
  background: linear-gradient(180deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.5) 60%, transparent 100%);
}
```

### 对白气泡（dialogue）

**用途**：角色台词。圆角白色半透明气泡。

**视觉规范**：
- 最大宽度 45%（不遮挡画面主体）
- 白色半透明背景（rgba(255,255,255,0.92)）
- 圆角 12px
- 深色文字（#1a1a1a）
- 字号 14px，行高 1.6

```css
.caption-dialogue {
  position: absolute;
  max-width: 45%;
  padding: 10px 14px;
  background: rgba(255,255,255,0.92);
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  color: #1a1a1a;
  box-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.caption-dialogue.top-left { top: 12%; left: 5%; }
.caption-dialogue.top-right { top: 12%; right: 5%; }
.caption-dialogue.bottom-left { bottom: 18%; left: 5%; }
.caption-dialogue.bottom-right { bottom: 18%; right: 5%; }
.caption-dialogue.center { top: 40%; left: 50%; transform: translateX(-50%); }
```

### 大单页文字处理

**大单页通常不加文字**——名场面画面自说，文字会干扰视觉冲击。

| 页面类型 | 文字叠加策略 |
|:---------|:------------|
| 大单页（名场面） | captions 留空，除非导演卡明确标注旁白文字 |
| 多格页 | 按导演卡页面设计表的旁白文字配置 |
| 双格页 | 按导演卡页面设计表的旁白文字配置 |

> 如果导演卡标注"无（画面自说）"，`captions` 留空数组 `[]`。

## HTML 结构规范

### 完整 HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{章节标题}</title>
  <style>
    /* === 全局 === */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #0d0d0d;
      font-family: "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
      color: #f5f0e8;
    }
    /* === 漫画容器 === */
    .comic-container {
      max-width: 820px;
      margin: 0 auto;
      padding: 20px 0;
    }
    /* === 章节标题 === */
    .chapter-title {
      text-align: center;
      padding: 40px 20px;
    }
    .chapter-title h1 {
      font-size: 22px;
      font-weight: 700;
      margin-bottom: 8px;
      letter-spacing: 2px;
    }
    .chapter-title p {
      font-size: 13px;
      opacity: 0.6;
      letter-spacing: 1px;
    }
    /* === 页面 === */
    .comic-page {
      width: 100%;
      position: relative;
      overflow: hidden;
      border-radius: 4px;
      margin-bottom: 0;
    }
    .comic-page img {
      width: 100%;
      height: auto;
      display: block;
    }
    /* === 旁白条 === */
    .caption-narration {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      padding: 40px 20px 16px;
      background: linear-gradient(0deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.5) 60%, transparent 100%);
      color: #f5f0e8;
      font-size: 15px;
      line-height: 1.9;
      text-shadow: 0 1px 3px rgba(0,0,0,0.9), 0 0 8px rgba(0,0,0,0.6);
    }
    .caption-narration.top {
      top: 0;
      bottom: auto;
      padding: 16px 20px 40px;
      background: linear-gradient(180deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.5) 60%, transparent 100%);
    }
    /* === 对白气泡 === */
    .caption-dialogue {
      position: absolute;
      max-width: 45%;
      padding: 10px 14px;
      background: rgba(255,255,255,0.92);
      border-radius: 12px;
      font-size: 14px;
      line-height: 1.6;
      color: #1a1a1a;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .caption-dialogue.top-left { top: 12%; left: 5%; }
    .caption-dialogue.top-right { top: 12%; right: 5%; }
    .caption-dialogue.bottom-left { bottom: 18%; left: 5%; }
    .caption-dialogue.bottom-right { bottom: 18%; right: 5%; }
    .caption-dialogue.center { top: 40%; left: 50%; transform: translateX(-50%); }
    /* === 页面间隔符 === */
    .scene-break {
      text-align: center;
      padding: 24px 0;
      color: #555;
      font-size: 14px;
      letter-spacing: 8px;
    }
    /* === 页脚 === */
    .comic-footer {
      text-align: center;
      padding: 30px 20px 20px;
      color: #444;
      font-size: 12px;
      letter-spacing: 2px;
    }
  </style>
</head>
<body>
  <div class="comic-container">
    <div class="chapter-title">
      <h1>{章节标题}</h1>
      <p>第{N}章 · {章节名}</p>
    </div>

    <!-- 逐页渲染 -->
    <div class="comic-page">
      <img src="output/page1.png" alt="P1">
      <div class="caption-narration">西蜀在大西塬吃亏。</div>
    </div>

    <div class="scene-break">◇ ◇ ◇</div>

    <div class="comic-page">
      <img src="output/page2.png" alt="P2">
      <div class="caption-narration">迟早要攻蜀。</div>
      <div class="caption-dialogue top-right">伐蜀只是顺便。</div>
    </div>

    <div class="scene-break">◇ ◇ ◇</div>

    <div class="comic-page">
      <img src="output/page3.png" alt="P3">
      <!-- 大单页，无文字叠加 -->
    </div>

    <div class="scene-break">◇ ◇ ◇</div>

    <div class="comic-page">
      <img src="output/page4.png" alt="P4">
      <div class="caption-narration">擒主焚庙可矣。</div>
    </div>

    <div class="comic-footer">popwave</div>
  </div>
</body>
</html>
```

## 移动端适配

**移动端优先设计**——漫画的主要消费场景是手机竖向滑动阅读。

| 维度 | 规范 | 说明 |
|:-----|:-----|:-----|
| 容器宽度 | `max-width: 820px` | 桌面端居中限宽，手机端全宽 |
| 图片展示 | `width: 100%; height: auto` | 图片自适应容器宽度 |
| 文字定位 | 绝对定位 + 百分比 | 适配不同屏幕尺寸 |
| 字号 | 14-15px | 手机端可读，不过大 |
| 间距 | scene-break 24px | 页面间呼吸感 |
| 背景色 | `#0d0d0d` | 深色背景突出画面 |

### 响应式微调

```css
@media (max-width: 480px) {
  .caption-narration { font-size: 14px; padding: 32px 16px 12px; }
  .caption-dialogue { font-size: 13px; max-width: 50%; }
  .chapter-title h1 { font-size: 18px; }
}
```

## 避让规则

文字叠加不得遮挡画面关键信息：

| 规则 | 说明 |
|:-----|:-----|
| 避让人物面部 | 对白气泡不得覆盖角色脸部区域 |
| 避让动作焦点 | 旁白条放在底部/顶部，不覆盖画面中心动作 |
| 大单页慎用文字 | 名场面画面自说，除非导演卡明确标注旁白 |
| 旁白条 ≤3 行 | 超过 3 行用导演卡拆分为多页或精简旁白 |
| 对白气泡 ≤15 字 | 超长对白拆分为多个气泡或精简 |

## 页面间隔符

页面之间用 `scene-break` 分隔，视觉上是一行 `◇ ◇ ◇`：

```html
<div class="scene-break">◇ ◇ ◇</div>
```

- 每页之间都插入间隔符（对应 `页面配置.json` 中的 `{"separator": true}`）
- 间隔符提供页面间的呼吸感，让读者感知"翻页"
- 视觉风格：深灰色小字，居中，字间距大

## 与 v3.x layout-pool.md 的差异

| 维度 | v3.x layout-pool.md | v4.0 page-layout-guide.md |
|:-----|:--------------------|:--------------------------|
| 核心职责 | 格子布局（7种布局类） | 文字叠加（旁白条/对白气泡） |
| HTML 复杂度 | 高（flex/aspect-ratio/定位/clip-path） | 低（全宽图片+绝对定位文字） |
| 布局类 | layout-splash/split/fullwide/overlay/narrow/fullbleed/climax | 无（画面是AI直出的） |
| 布局漂移风险 | 高（50%帧布局被擅自更改） | 无（无格子布局） |
| 移动端适配 | 需要为每种布局单独适配 | 天然适配（全宽图片+百分比定位） |
| CSS 效果类 | speed-lines/tilt/flashback/sepia/noir/dream/impact | 无（特效在提示词层直出） |

## 文化元素叠加（可选）

> 详见 `references/cultural-elements-guide.md`。仅修仙/玄幻/古言/权谋等古风赛道适用。

当 `页面配置.json` 包含 `poem` 或 `seal` 字段时，HTML 模板自动渲染文化元素：

### 章节标题页文化元素

| 元素 | 触发条件 | 渲染位置 |
|:-----|:---------|:---------|
| 定场诗 | `poem` 字段存在 | 章节标题下方，宋体/楷体竖排或横排 |
| 古籍版式线 | `poem` 字段存在 | 章节标题区域双线边框+鱼尾装饰 |
| 引首章 | `poem` 字段存在 | 章节标题上方，朱砂红小印 |

### 章末钩子页文化元素

| 元素 | 触发条件 | 渲染位置 |
|:-----|:---------|:---------|
| 章末印 | `seal` 字段存在 | 最后一个 `.comic-page` 右下角，朱砂红方形印 |

### HTML 模板扩展

在基础 HTML 模板的 `<style>` 中追加文化元素 CSS：

```css
/* === 文化元素（定场诗+印章+版式线） === */
.chapter-title-frame {
  border: 2px double #8a7a5c;
  padding: 32px 24px;
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}
.chapter-title-frame::before,
.chapter-title-frame::after {
  content: "♣";
  position: absolute;
  color: #8a7a5c;
  font-size: 14px;
  left: 50%;
  transform: translateX(-50%);
}
.chapter-title-frame::before { top: -8px; }
.chapter-title-frame::after { bottom: -8px; }
.chapter-poem {
  color: #c4b998;
  font-size: 14px;
  line-height: 2.2;
  letter-spacing: 3px;
  font-family: "Noto Serif SC", "STSong", serif;
  opacity: 0.85;
  margin-top: 16px;
}
.chapter-seal {
  position: absolute;
  width: 48px;
  height: 48px;
  background: #b8332e;
  color: #f5f0e8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "STSong", "SimSun", serif;
  font-size: 18px;
  font-weight: bold;
  border-radius: 2px;
  opacity: 0.9;
  box-shadow: 0 1px 3px rgba(0,0,0,0.4);
  border: 2px solid #9a2b26;
}
.chapter-seal.bottom-right { bottom: 8%; right: 8%; }
.chapter-seal.top-right { top: 8%; right: 8%; }
```

### 渲染逻辑

```html
<!-- 章节标题页（有 poem 时渲染版式线+定场诗） -->
<div class="chapter-title">
  <div class="chapter-title-frame">
    <h1>{章节标题}</h1>
    <p>第{N}章 · {章节名}</p>
    {if poem}<div class="chapter-poem">{poem}</div>{/if}
  </div>
</div>

<!-- 章末钩子页（有 seal 时渲染印章） -->
<div class="comic-page">
  <img src="output/pageN.png" alt="P{N}">
  {if seal}<div class="chapter-seal {seal.position}">{seal.text}</div>{/if}
</div>
```

> **无文化元素的章节**：`poem` 和 `seal` 字段省略，HTML 模板不渲染对应元素，退回标准章节标题样式。
