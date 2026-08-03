# 推书卡9页布局指南 — v2.0 独立设计语言版

> 9种排版范式，每页独立视觉人格。主题色仅控制色板，不改变排版。

---

## 页面规格

- 尺寸：720 × 960 px
- 主题色：5种（literary-red / ink-blue / warm-paper / dark-modern / diary-orange）
- 每个 `page.type` 映射唯一 CSS class + 唯一 JS 渲染函数

---

## 9种设计语言

| type | 设计范式 | CSS class | 核心特征 |
|:--|:--|:--|:--|
| cover | **Cinematic Poster** 电影海报 | `page-cover` | 暗色渐变底+超大衬线书名+金线引言+底部版权标签 |
| hook | **Swiss Grid** 瑞士极简 | `page-swiss` | 纯白底+左侧6px黑边+2×2十字分割+01-04数字标注+全sans-serif |
| synopsis | **Magazine Editorial** 杂志页 | `page-magazine` | 左180px深色边栏（竖排眉标+巨大页码）+右内容区+时间线圆点 |
| characters | **Profile Spread** 人物特写 | `page-profiles` | 上眉线+2×2人物卡+名字下划线+身份标注+驱动力正文 |
| chemistry | **Infographic** 信息图 | `page-infographic` | 居中标题+A×B公式框+2解释卡+边框 |
| structure | **Horizontal Timeline** 时间线 | `page-timeline` | 横向黑线+圆点节点+下方标注+底部路线框 |
| selling_points | **Feature Showcase** 黑底展示 | `page-showcase` | 全黑底+金字标题+1px分割线网格+01-04编号+白字卡片 |
| risks | **Dashboard** 仪表盘 | `page-dashboard` | 左6维条形图+右红框警告列表+红标签 |
| verdict | **Back Cover** 封底 | `page-backcover` | 深色渐变底+居中评分大数字+推荐/不推荐双栏+底部引言 |

---

## 主题选择规则

| 主题 | 适用 | 主色 |
|:--|:--|:--|
| literary-red | 文学/言情（默认） | 金棕 gold |
| ink-blue | 仙侠/玄幻 | 海蓝 blue |
| warm-paper | 都市/现实 | 赤红 red |
| dark-modern | 悬疑/科幻 | 霓虹橙 |
| diary-orange | 青春/校园 | 深橙 orange |

---

## 数据契约（review.js）

```js
window.__BOOK_DATA__ = {
  theme: "literary-red",  // 主题名
  pages: [{
    page_no: 1,
    type: "cover",        // 决定渲染函数
    eyebrow: "一本书值不值得看？",
    title: "书名",
    highlight: "核心字",   // 在title中高亮
    subtitle: "作者 · 题材",
    blocks: [{ kind: "...", ... }],
    footer: "页脚标签"
  }]
}
```
