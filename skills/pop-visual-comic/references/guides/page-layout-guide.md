# 页面排版+文字叠加指南

> Step 2 生成 HTML 的参考。画面是 AI 画的（Seedream 直出完整漫画页），文字是 HTML 叠的（旁白条/对白气泡）。各司其职。

## 设计哲学

**v4.0 核心**：生成单位从"格"升级为"页"。Seedream 在单张图内直出完整漫画页（含分格线、多格内容、镜头语言），HTML **不做格子布局**，只负责：
1. 长条滚动展示（所有漫画页从上到下竖向排列）
2. 文字叠加（旁白条/对白气泡）

**v4.3.2**：从翻页阅读器改回长条滚动——纯 HTML+CSS，零 JS 交互，稳定无 bug。

## 页面配置 JSON 规范

`页面配置.json` 是 Step 2 生成 HTML 的输入配置：

```json
{
  "title": "{章节标题}",
  "subtitle": "第{N}章 · {章节名}",
  "poem": "鉴中千秋血，镜外万骨枯。",
  "seal": {
    "text": "终",
    "position": "bottom-right"
  },
  "pages_dir": "output",
  "output_html": "index.html",
  "slogan": "popwave.cn 让创意一键落地",
  "pages": [
    {
      "file": "page1.png",
      "captions": [
        {"type": "narration", "text": "旁白文字", "position": "bottom"}
      ]
    },
    {
      "file": "page2.png",
      "captions": [
        {"type": "narration", "text": "旁白文字", "position": "bottom"},
        {"type": "dialogue", "text": "对白文字", "position": "top-right"}
      ]
    },
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
| `poem` | string | 否 | 定场诗内容（≤28字），仅标题区渲染。详见 `cultural-elements-guide.md` |
| `seal` | object | 否 | 朱砂印章配置。详见 `cultural-elements-guide.md` |
| `seal.text` | string | 否 | 印章文字（1-2字），如"终""卷"等 |
| `seal.position` | string | 否 | 印章位置（`bottom-right` / `top-right`），默认 `bottom-right` |
| `pages_dir` | string | 是 | 页面图片目录（相对路径，通常为 `output`） |
| `output_html` | string | 是 | 输出 HTML 文件名（通常为 `index.html`） |
| `footer` | string | 否 | 页脚信息（默认 `未完待续 · popwave.cn 让创意一键落地`），钩子+品牌合并为单行 |
| `slogan` | string | 否 | 品牌 slogan（默认 `popwave.cn 让创意一键落地`），渲染在标题区第三行 |
| `pages` | array | 是 | 页面数组，按阅读顺序排列 |
| `pages[].file` | string | 是 | 页面图片文件名（如 `page1.png`） |
| `pages[].captions` | array | 否 | 文字叠加数组 |
| `captions[].type` | string | 是 | `narration`（旁白条）/ `dialogue`（对白气泡） |
| `captions[].text` | string | 是 | 文字内容（直接使用小说原文，旁白≤80字/条，对白≤15字/条） |
| `captions[].position` | string | 是 | 定位（见下方位置规范） |

### 位置规范

| position 值 | 适用类型 | 定位说明 |
|:-----------|:---------|:---------|
| `bottom` | narration | 底部全宽渐变遮罩条 |
| `top` | narration | 顶部全宽渐变遮罩条 |
| `side-top` | narration | 顶部侧边窄条（左上，避开人脸/对白） |
| `side-bottom` | narration | 底部侧边窄条（左下，避开人脸/对白） |
| `top-left` | dialogue | 左上角气泡 |
| `top-right` | dialogue | 右上角气泡 |
| `bottom-left` | dialogue | 左下角气泡 |
| `bottom-right` | dialogue | 右下角气泡 |
| `center` | dialogue | 居中气泡（少用） |

> **铁律（v7.20.0）**：旁白条类名**只用 `top` / `bottom` / `side-top` / `side-bottom`**，CSS 必须为这四个类定义定位规则。**禁用 `top-left` / `top-right` 作为旁白条类名**（这两个类只给对白气泡用）——旁白条若用无定位规则的类名，会因缺少 `top` 锚点而错位落到页面底部之外（第4章 P1/P6 实测踩坑）。

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
  left: 0; right: 0; bottom: 0;
  padding: 40px 20px 16px;
  background: linear-gradient(0deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.5) 60%, transparent 100%);
  color: #f5f0e8;
  font-size: 15px; line-height: 1.9;
  text-shadow: 0 1px 3px rgba(0,0,0,0.9), 0 0 8px rgba(0,0,0,0.6);
}
.caption-narration.top {
  top: 0; bottom: auto;
  padding: 16px 20px 40px;
  background: linear-gradient(180deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.5) 60%, transparent 100%);
}
```

### 对白气泡（dialogue）

**用途**：角色台词。圆角白色气泡。

**视觉规范**：
- 最大宽度 45%（不遮挡画面主体）
- **接近实色白底（rgba(255,255,255,0.97)）**——浅色/高亮画面上气泡仍清晰成型，不融进背景
- **深色文字 + 白色描边**（color #1a1a1a + text-shadow 白边）——深字带白描边，在亮画面上与画面分隔，醒目
- 圆角 12px
- 字号 14px，行高 1.6

```css
.caption-dialogue {
  position: absolute;
  max-width: 45%;
  padding: 10px 14px;
  background: rgba(255,255,255,0.97);   /* 接近实色白底，浅色画面不融背景 */
  border-radius: 12px;
  font-size: 14px; line-height: 1.6;
  color: #1a1a1a;
  text-shadow: 0 0 2px rgba(255,255,255,0.9), 0 1px 3px rgba(0,0,0,0.25);  /* 白描边+轻投影 */
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

## 信息页渲染（半文半图，v7.18.0）

> 信息页 = 一半漫画图 + 一半文字块，**图文同页不可分离**（禁止纯文字无图的信息卡）。上漫画下文字，文字承载浓密世界观/背景，画面提供视觉锚点。信息页设计与穿插节奏由导演卡 `step1-director-card.md` §3.1c 规划。

### 页面配置 JSON 结构

信息页在 `pages` 数组中用 `"type": "info"` 标记，独占一页：

```json
{
  "file": "info_page1.png",
  "type": "info",
  "info": {
    "heading": "是谁·是谁的夜",
    "title": "他继承的，不止是身体",
    "body": [
      "克莱恩·莫雷蒂——鲁恩王国阿霍瓦郡廷根市人，霍伊大学历史系刚毕业。",
      "父亲是皇家陆军上士，牺牲在南大陆；母亲是黑夜女神信徒，也已离世。",
      "他有一个哥哥班森、一个妹妹梅丽莎，一家人挤在出租公寓里，家境拮据。"
    ]
  }
}
```

### HTML 渲染结构

```html
<div class="info-page">
  <div class="info-art">
    <img src="output/info_page1.png" alt="设定配图">
  </div>
  <div class="info-text">
    <div class="info-heading">是谁·是谁的夜</div>
    <div class="info-title">他继承的，不止是身体</div>
    <div class="info-body">
      <p>克莱恩·莫雷蒂——鲁恩王国阿霍瓦郡廷根市人……</p>
      <p>……</p>
    </div>
  </div>
</div>
```

### 视觉规范

```css
.info-page { position:relative; margin-bottom:4px; }
.info-art { width:100%; }
.info-art img { display:block; width:100%; height:auto; }
.info-text {
  padding: 24px 22px 30px;
  background: linear-gradient(180deg, #151312 0%, #1a1714 100%);
  border-top: 1px solid #3a342c;
}
.info-heading { font-size:12px; letter-spacing:3px; color:#8a7a5c; margin-bottom:8px; }
.info-title { font-size:20px; font-weight:700; color:#c4b998; letter-spacing:2px; margin-bottom:14px; }
.info-body p { font-size:15px; line-height:2.0; color:#e8e2d6; margin-bottom:10px; text-align:justify; }
```

**要点**：上半图片 `info-art` 只放画面（提示词已含负面约束无文字），下半文字块 `info-text` 承载 2-4 条分条信息（每条≤80字）。文字块不透明衬底，保证长文可读，不与漫画图叠压。

### 信息页 JSON 字段说明

| 字段 | 类型 | 说明 |
|:-----|:-----|:-----|
| `pages[].type` | string | `"info"` 标记为信息页；省略则按普通漫画页渲染 |
| `pages[].info.heading` | string | 信息页小标（栏目名，如"人物·夜之国"） |
| `pages[].info.title` | string | 信息页大标题（一句话点题） |
| `pages[].info.body` | array | 分条文字，每条 ≤80 字，2-4 条 |

> **铁律**：信息页必须有图（`info-art` 不可为空）。信息页前后必须各有漫画页，禁止连续 2 个信息页。信息页占全章页数 ≤30%。

## 避让规则

文字叠加不得遮挡画面关键信息，尤其**角色脸部**：

| 规则 | 说明 |
|:-----|:-----|
| 避让人物面部 | 对白/旁白不得覆盖角色脸部区域 |
| 旁白条只占边缘 | 顶部/底部旁白条高度 ≤6%，只放 `top`/`bottom`/`side-top`/`side-bottom` 四类，不覆盖画面中心动作 |
| 对白气泡放角落 | 只放四角，max-width 45%，不压脸 |
| 禁用无规则类名 | 旁白条禁用 `top-left`/`top-right`（那是对白类），否则错位落底部之外 |
| 大单页慎用文字 | 名场面画面自说，除非导演卡明确标注旁白 |
| 旁白条 ≤3 行 | 超过 3 行用导演卡拆分为多页或精简旁白 |
| 对白气泡 ≤15 字 | 超长对白拆分为多个气泡或精简 |

> **文字安全区（v7.20.0）**：导演卡设计页面时，为每页预留**顶部 6% + 底部 6% 文字安全带**。角色脸部/关键动作放在画面中部，旁白条只放在安全带内——从源头避免"文字压脸"。若某页角色脸必须贴近上/下边缘，则该页旁白改用 `side-top`/`side-bottom` 窄条或干脆不放该位置。

## 完整 HTML 模板（长条滚动）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{章节标题}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #0d0d0d;
      font-family: "Noto Sans CJK SC", "Microsoft YaHei", sans-serif;
      color: #f5f0e8;
    }
    .container {
      max-width: 820px;
      margin: 0 auto;
    }
    .title-banner {
      text-align: center;
      padding: 48px 24px 36px;
      background: #0d0d0d;
    }
    .title-banner h1 {
      font-size: 24px; font-weight: 700;
      letter-spacing: 3px;
      color: #c4b998;
      margin-bottom: 8px;
    }
    .title-banner .subtitle {
      font-size: 13px; opacity: 0.4;
      letter-spacing: 2px;
    }
    .title-banner .brand-line {
      margin-top: 14px;
      font-size: 11px; opacity: 0.35;
      letter-spacing: 2px;
      color: #c4b998;
    }
    .page {
      position: relative;
      margin-bottom: 4px;
    }
    .page img {
      display: block;
      width: 100%;
    }
    .caption-narration {
      position: absolute;
      left: 0; right: 0;
      padding: 22px 20px 12px;
      background: linear-gradient(0deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.45) 45%, transparent 100%);
      font-size: 15px; line-height: 1.9;
      text-shadow: 0 1px 3px rgba(0,0,0,0.9), 0 0 8px rgba(0,0,0,0.6);
    }
    .caption-narration.top {
      top: 0; bottom: auto;
      padding: 12px 20px 22px;
      background: linear-gradient(180deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.45) 45%, transparent 100%);
    }
    .caption-narration.bottom { bottom: 0; }
    .caption-narration.side-top {
      top: 0; bottom: auto; left: 0; right: auto;
      max-width: 72%;
      padding: 12px 20px 22px;
      background: linear-gradient(180deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.45) 45%, transparent 100%);
      border-radius: 0 0 10px 0;
    }
    .caption-narration.side-bottom {
      bottom: 0; left: 0; right: auto;
      max-width: 72%;
      padding: 22px 20px 12px;
      background: linear-gradient(0deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.45) 45%, transparent 100%);
      border-radius: 0 10px 0 0;
    }
    .caption-dialogue {
      position: absolute;
      max-width: 45%;
      padding: 10px 14px;
      background: rgba(255,255,255,0.92);
      border-radius: 12px;
      font-size: 14px; line-height: 1.6;
      color: #1a1a1a;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .caption-dialogue.top-left { top: 12%; left: 5%; }
    .caption-dialogue.top-right { top: 12%; right: 5%; }
    .caption-dialogue.bottom-left { bottom: 18%; left: 5%; }
    .caption-dialogue.bottom-right { bottom: 18%; right: 5%; }
    .caption-dialogue.center { top: 40%; left: 50%; transform: translateX(-50%); }
    .footer-banner {
      text-align: center;
      padding: 40px 24px;
      font-size: 12px; color: #444;
      letter-spacing: 3px;
    }
    @media (max-width: 480px) {
      .caption-narration { font-size: 14px; padding: 32px 16px 12px; }
      .caption-dialogue { font-size: 13px; max-width: 50%; }
      .title-banner h1 { font-size: 18px; }
    }
  </style>
</head>
<body>
  <div class="container">

    <div class="title-banner">
      <h1>{章节标题}</h1>
      <div class="subtitle">第{N}章 · {章节名}</div>
      <div class="brand-line">{slogan}</div>
    </div>

    <div class="page">
      <img src="output/page1.png" alt="P1">
      <div class="caption-narration bottom">{旁白文字}</div>
    </div>

    <div class="page">
      <img src="output/page2.png" alt="P2">
      <div class="caption-narration top">{旁白文字}</div>
      <div class="caption-narration bottom">{旁白文字}</div>
    </div>

    <div class="page">
      <img src="output/page3.png" alt="P3">
      <!-- 大单页，无文字叠加 -->
    </div>

    <div class="page">
      <img src="output/page4.png" alt="P4">
      <div class="caption-dialogue top-right">{对白文字}</div>
      <div class="caption-narration bottom">{旁白文字}</div>
    </div>

    <div class="footer-banner">{footer}</div>

  </div>
</body>
</html>
```

> **直接复制模板，替换 `{章节标题}`/`{章节名}`/`pageN.png`/`{旁白文字}`/`{对白文字}`/`{slogan}`/`{footer}` 等占位符即可。** 纯 HTML+CSS，无 JavaScript，向下滚动浏览。

## 品牌水印（v7.6.0）

> 2026-08-04 定稿：品牌署名走 HTML 工程化方案（历史已踩坑——提示词融水印不稳定，见 CHANGELOG）。品牌水印**不逐页压**，避免破坏画面冲击力。

### 品牌结构（开头三行 + 结尾单行）

**开头标题区三行**（小说名 / 第X章·章名 / slogan）：

```html
<div class="title-banner">
  <h1>{章节标题}</h1>
  <div class="subtitle">第{N}章 · {章节名}</div>
  <div class="brand-line">{slogan}</div>
</div>
```

**结尾页脚单行**（未完待续 + slogan，不占两行——老板反馈页脚两行过挤）：

```html
<div class="footer-banner">{footer}</div>
```

### 默认文案

- **slogan**：`popwave.cn 让创意一键落地`（老板定稿，标题区第三行）
- **footer**：`未完待续 · popwave.cn 让创意一键落地`（页脚单行）
- 通过 `slogan` / `footer` 字段自定义

### 文案要点

- 不用 `powered by`（太像开源软件署名/技术声明）
- slogan 点出"让创意一键落地"的 AI 自动代劳卖点，品牌 `popwave.cn` 前置
- 结尾 `未完待续` 是追读钩子，与 slogan 合并单行，避免两行过挤

### 设计原则

- **不逐页压角标**：长条滚动漫画是沉浸阅读，每页压水印会破坏画面冲击力（历史踩坑：提示词融水印 → 不稳定，改走 HTML）
- **不抢剧情**：品牌只放标题区与页脚，不在画面区，不遮挡关键画面
- **低调克制**：低透明度 + 与暗色背景融合，不喧宾夺主

## 文化元素叠加（可选）

> 详见 `cultural-elements-guide.md`。仅修仙/玄幻/古言/权谋等古风赛道适用。

当 `页面配置.json` 包含 `poem` 或 `seal` 字段时，HTML 模板自动渲染文化元素：

### 文化元素 CSS

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
<!-- 标题区（有 poem 时渲染版式线+定场诗） -->
<div class="title-banner">
  <div class="chapter-title-frame">
    <h1>{章节标题}</h1>
    <p>第{N}章 · {章节名}</p>
    {if poem}<div class="chapter-poem">{poem}</div>{/if}
  </div>
</div>

<!-- 章末页（有 seal 时渲染印章） -->
<div class="page">
  <img src="output/pageN.png" alt="P{N}">
  {if seal}<div class="chapter-seal {seal.position}">{seal.text}</div>{/if}
</div>
```

> **无文化元素的章节**：`poem` 和 `seal` 字段省略，退回标准标题样式。