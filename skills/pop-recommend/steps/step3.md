# Step 3 · HTML渲染

> 消费 review.json → 读取 HTML 模板 → 注入数据 → 生成9页式推书卡

---

## 输入

1. 读取 `工作稿/review.json`
2. 读取 `templates/recommend-card.tpl.html`（HTML 模板文件——**必须读取，内含完整 CSS + 9 个渲染函数 + 4 处 SVG 装饰**）

---

## 渲染流程

1. 将 review.json 转为 JS 变量内容：`window.__BOOK_DATA__ = {...};`
2. 读取模板文件 `templates/recommend-card.tpl.html` 的全部内容
3. 替换占位符：
   - `{{TITLE}}` → 书名
   - `{{REVIEW_DATA}}` → 第1步的 JS 变量内容
4. 落盘到项目根目录：`{书名}-读者推书-v1.html`

---

## 模板文件说明

`templates/recommend-card.tpl.html` 是完整可工作的 HTML 骨架，包含：
- 完整 CSS（5 主题色 + 9 种页面设计语言的样式 + 品牌印记样式）
- 4 处 inline SVG 装饰图标（封面翻书图标、卖点页靶标、仪表盘折线图、封底五星评级）
- 9 个渲染函数（P1-P9，对应 9 种页面类型）
- `{{REVIEW_DATA}}` + `{{TITLE}}` 两个注入点
- review.js fallback 加载逻辑

**不要修改模板中的任何 CSS 类名、SVG 代码块或渲染函数。** 只做两个占位符替换。

---

## 产出

`{书名}-读者推书-v1.html` — 自包含文件，双击浏览器直接打开。

---

## 完成

HTML 落盘后直接打开验证。链式管线结束。
