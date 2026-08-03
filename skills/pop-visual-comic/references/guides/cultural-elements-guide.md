# 漫画文化元素设计指南

> 从 `pop-visual-cover/references/novel-visual-design.md` §八 提取，改造成漫画场景使用规范。封面是"一张图0.3秒抓住读者"，漫画是"连续翻页讲好故事"——文化元素的使用位置、频率和功能完全不同。

## 设计哲学

**文化元素是漫画的"逼格放大器"——将漫画从"插画集合"升级为有文化底蕴的视觉作品。** 不是每页都加，只在该加的时候加，服务于叙事和氛围。

**与封面的核心差异**：

| 维度 | 封面（novel-visual） | 漫画（comic） |
|:-----|:--------------------|:-------------|
| 使用频率 | 一张封面最多2-3种 | 按页面类型按需使用，整章可0-3次 |
| 核心位置 | 书名旁/画面留白区/边栏 | 章节标题页/章末钩子页/场景转场 |
| 功能 | 营销钩子·逼格锚点 | 叙事装饰·氛围强化·章节仪式感 |
| 文字叠加 | 提示词直出（Seedream渲染） | HTML 层实现（CSS精确控制）+ 提示词层（道具铭文） |

**两层实现**：
- **HTML 层**（主）：定场诗、印章、版式线——CSS 精确控制位置和样式，不依赖 AI 渲染
- **提示词层**（辅）：道具铭文、背景纹理——在 Seedream 提示词中描述，画面层直出

## 文化元素速查表

| 元素 | 漫画使用位置 | 实现层 | 适合赛道 | 效果 |
|:-----|:-----------|:-------|:---------|:-----|
| **定场诗** | 章节标题页（竖排古体诗作为章首视觉锚点） | HTML 层 | 修仙/玄幻/古言/权谋 | ★★★★★ |
| **朱砂印章** | 章末钩子页落款 / 特殊页装饰 | HTML 层 | 全赛道通用 | ★★★★☆ |
| **古籍版式线** | 章节标题页边框 / 场景转场装饰 | HTML 层 | 修仙/古言/历史 | ★★★☆☆ |
| **小篆题字** | 道具铭文（法宝刻字）/ 章节装饰文字 | 提示词层 | 修仙/玄幻/历史 | ★★★★☆ |
| **题跋落款** | 章末页（作者名+章节感言） | HTML 层 | 修仙/玄幻/文艺向 | ★★★☆☆ |

> **使用纪律**：一章最多使用 2-3 种文化元素，过多会杂乱。文化元素服务于叙事氛围，不能为了"有文化"而硬加。

## 一、定场诗设计

### 1.1 核心原则

定场诗是漫画章节的"文学签名"——用 2-4 句古体诗浓缩本章核心意境，放在章节标题页，为读者建立"这本书有文化底子"的第一印象。

### 1.2 创作公式

```
[核心意象A] + [核心意象B] + [因果/转折] + [情感升华]
```

**创作要求**：
1. 2-4 句，每句 5-7 字（五言/七言），总计不超过 28 字
2. 必须包含本章的核心意象（道具/场景/情感），不能是通用诗句
3. 押韵但不强求平仄，重意境不重格律
4. 读者扫一眼能感受到"这一章有底蕴"

### 1.3 各赛道示例

| 赛道 | 定场诗 | 意象来源 |
|:-----|:-------|:---------|
| 家族修仙 | "鉴中千秋血，镜外万骨枯。六代薪传火，一鉴照仙途。" | 古镜+家族传承+血与仙途 |
| 诡异悬疑 | "表盘藏生死，裂痕窥幽冥。死亡非终局，时针转乾坤。" | 手表+死亡循环+模拟器 |
| 暗黑修仙 | "深渊无底处，诸神亦为尘。一人执剑起，万界颤乾坤。" | 深渊+诸神+主角逆袭 |
| 古言权谋 | "朱墙掩枯骨，金殿藏孤魂。棋落天下动，一笑定乾坤。" | 宫殿+权谋+棋局 |

### 1.4 HTML 实现（章节标题页）

定场诗通过 HTML CSS 叠加在章节标题页，不依赖 Seedream 渲染：

```css
.chapter-poem {
  text-align: center;
  padding: 16px 20px 24px;
  color: #c4b998;
  font-size: 14px;
  line-height: 2.2;
  letter-spacing: 3px;
  font-family: "Noto Serif SC", "STSong", serif;
  opacity: 0.85;
  writing-mode: vertical-rl;  /* 竖排（可选，竖排更有古韵） */
  text-orientation: upright;
}
```

> **字体层级**：书名（毛笔书法体，最大）> 定场诗（宋体/楷体，中等）> 副标题（楷体，小）> 印章（篆刻体，小但醒目·红色）。

### 1.5 使用位置

| 位置 | 说明 | 频率 |
|:-----|:-----|:-----|
| **章节标题页** | 章节标题下方，竖排或横排定场诗 | 每章可选 |
| 章末钩子页 | 不加——钩子页要留悬念，加诗会泄气 | ❌ 禁止 |
| 大单页 | 不加——名场面画面自说，文字会干扰 | ❌ 禁止 |

> 定场诗只在章节标题页使用。它建立的是"开卷仪式感"，不是每页都有的装饰。

## 二、朱砂印章设计

### 2.1 核心原则

印章是漫画的"文化落款"——用朱砂红色形成视觉锚点，在章末钩子页或特殊页提供仪式感。

### 2.2 印章类型

| 印章类型 | 形态 | 内容 | 漫画位置 |
|:---------|:-----|:-----|:---------|
| **章末印** | 方形，2-3cm | 章节序号或章节关键词 | 章末钩子页右下角 |
| 闲章 | 圆形/椭圆形 | 定场诗中关键词/成语 | 章节标题页留白处 |
| 引首章 | 长方形 | 开卷/鉴赏类词 | 章节标题页开头处 |

### 2.3 HTML 实现

```css
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
  /* 模拟篆刻阴文效果 */
  text-shadow: 0 0 1px #b8332e;
  border: 2px solid #9a2b26;
}
.chapter-seal.bottom-right {
  bottom: 8%;
  right: 8%;
}
```

### 2.4 使用位置

| 位置 | 印章类型 | 说明 |
|:-----|:---------|:-----|
| **章末钩子页右下角** | 章末印 | 章末仪式感，如"终"字印或章节关键词 |
| **章节标题页** | 闲章 | 定场诗旁的点缀，朱砂红与宋体诗形成色彩对比 |
| 大单页 | ❌ 不加 | 名场面画面自说，印章会干扰 |

> **红点锚定**：印章的朱砂红是整页中重要的红色锚点。如果画面本身已有大量红色（血腥场景），印章应降低不透明度或省略。

## 三、古籍版式线

### 3.1 核心原则

用古籍印刷的版式元素做章节标题页边框/装饰，增加"典籍感"。适合修仙/古言/历史赛道。

### 3.2 版式元素

| 元素 | 形态 | 漫画用途 |
|:-----|:-----|:---------|
| **版框线** | 双线/单线矩形框 | 章节标题页边框装饰 |
| **鱼尾** | ♣形装饰符号 | 版框中线两端 |
| **界栏线** | 竖向分隔线 | 定场诗竖排分隔 |

### 3.3 HTML 实现

```css
.chapter-title-frame {
  border: 2px double #8a7a5c;
  border-radius: 0;
  padding: 32px 24px;
  position: relative;
}
/* 鱼尾装饰 */
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
```

### 3.4 使用位置

仅在章节标题页使用。其他页面不加版式线——连续翻页阅读中，版式线反复出现会变成视觉噪音。

## 四、小篆题字（提示词层）

### 4.1 核心原则

小篆用于"需要古老感但不影响可读性"的场景。读者不需要读懂小篆内容，只需要感受到"这字很古"。在漫画中主要用于道具铭文。

### 4.2 使用场景

| 场景 | 提示词写法 | 说明 |
|:-----|:-----------|:-----|
| **道具铭文** | `ancient seal script characters carved on the mirror surface, glowing faintly` | 古镜/法宝/玉简上的刻字 |
| **背景纹理** | `background decorated with faint ancient seal script patterns` | 画面背景的古文字装饰 |
| **门楣刻字** | `ancient seal script characters on the stone gate lintel` | 场景建立页的门楣/匾额 |

### 4.3 提示词写法要点

- 写"ancient seal script"而非"小篆"——英文提示词对古文字的描述更精确
- 不需要模型真的写出正确的小篆，只需要"看起来像古文字"的视觉效果
- 配合材质色描述：`glowing golden` / `faded bronze` / `cinnabar red`

### 4.4 与 HTML 层的分工

| 元素 | 实现层 | 原因 |
|:-----|:-------|:-----|
| 道具铭文 | 提示词层 | 铭文在画面中，必须由 Seedream 直出 |
| 章节装饰文字 | HTML 层 | 装饰文字在叠加层，CSS 精确控制 |
| 背景纹理 | 提示词层 | 纹理在画面中，由 Seedream 直出 |

## 五、题跋落款

### 5.1 核心原则

章末页的小字落款，类似古籍题跋——作者名+章节感言或下章预告。

### 5.2 HTML 实现

```css
.chapter-colophon {
  text-align: right;
  padding: 12px 20px;
  color: #665;
  font-size: 12px;
  font-family: "STKaiti", "KaiTi", serif;
  line-height: 1.8;
  opacity: 0.7;
}
```

### 5.3 使用位置

仅在章末页 footer 区域使用，与品牌信息（popwave）并列。不是每章都加——有特别想说的章节才加。

## 六、赛道适配建议

| 赛道 | 推荐元素组合 | 不推荐 | 说明 |
|:-----|:-------------|:-------|:-----|
| 修仙/玄幻 | 定场诗 + 印章 + 版式线 | 竹简 | 标准组合，最有古韵 |
| 古言权谋 | 定场诗(隶书) + 印章 + 版式线 | 小篆 | 隶书比小篆更适配权谋气质 |
| 悬疑诡异 | 定场诗(行草) + 印章 | 版式线 | 版式线太正式，行草诗更符合诡异感 |
| 都市异能 | 印章(变体) + 落款 | 定场诗/小篆 | 古元素违和，仅用印章变体点缀 |
| 末世生存 | 落款(手写体) | 定场诗/印章 | 全部古元素违和 |
| 言情甜宠 | 印章(小清新变体) + 落款 | 定场诗 | 印章用粉色/浅色变体 |

## 七、章节标题页设计模板

章节标题页是文化元素的核心载体。以下是标准模板（HTML 层实现）：

```html
<div class="chapter-title-page">
  <div class="chapter-title-frame">
    <div class="chapter-seal intro-seal">卷</div>
    <h1 class="chapter-title">{章节标题}</h1>
    <p class="chapter-subtitle">第{N}章 · {章节名}</p>
    <div class="chapter-poem">
      {定场诗第一句}<br>
      {定场诗第二句}<br>
      {定场诗第三句}<br>
      {定场诗第四句}
    </div>
  </div>
</div>
```

```css
.chapter-title-page {
  text-align: center;
  padding: 60px 24px 40px;
}
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
.chapter-title {
  font-size: 24px;
  font-weight: 700;
  color: #f5f0e8;
  margin-bottom: 8px;
  letter-spacing: 4px;
  font-family: "Noto Serif SC", "STSong", serif;
}
.chapter-subtitle {
  font-size: 13px;
  color: #887;
  letter-spacing: 2px;
  margin-bottom: 20px;
}
.chapter-poem {
  color: #c4b998;
  font-size: 14px;
  line-height: 2.2;
  letter-spacing: 3px;
  font-family: "Noto Serif SC", "STSong", serif;
  opacity: 0.85;
}
.chapter-seal.intro-seal {
  position: static;
  display: inline-block;
  margin-bottom: 16px;
  width: 36px;
  height: 36px;
  font-size: 14px;
}
```

## 八、页面配置 JSON 扩展

在 `页面配置.json` 中，章节标题页和章末钩子页可携带文化元素配置：

```json
{
  "title": "{章节标题}",
  "subtitle": "第{N}章 · {章节名}",
  "poem": "鉴中千秋血，镜外万骨枯。六代薪传火，一鉴照仙途。",
  "seal": {
    "text": "终",
    "position": "bottom-right"
  },
  "pages": [...]
}
```

| 字段 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| `poem` | string | 否 | 定场诗内容（≤28字），仅章节标题页使用 |
| `seal` | object | 否 | 印章配置 |
| `seal.text` | string | 是 | 印章文字（1-2字） |
| `seal.position` | string | 是 | 印章位置（`bottom-right` / `top-right`） |

> 无文化元素的章节，`poem` 和 `seal` 字段省略即可。HTML 模板检测到字段存在才渲染对应元素。

## 九、使用决策树

```
本章赛道是否适合文化元素？
├─ 否（都市/末世/科幻等） → 不使用，结束
└─ 是（修仙/玄幻/古言/权谋等）
    └─ 章节标题页是否需要定场诗？
        ├─ 是 → 创作定场诗（创作公式+意象要求）→ HTML 层实现
        └─ 否 → 跳过
    └─ 章末钩子页是否需要印章？
        ├─ 是 → 选择印章类型+文字 → HTML 层实现
        └─ 否 → 跳过
    └─ 本章是否有道具铭文场景？
        ├─ 是 → 在 Seedream 提示词中描述 ancient seal script → 提示词层实现
        └─ 否 → 跳过
```

> **核心原则**：文化元素是锦上添花，不是必须项。如果章节内容本身不支撑（如现代都市章），不加比硬加更好。