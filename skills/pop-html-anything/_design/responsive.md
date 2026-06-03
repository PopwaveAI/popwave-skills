# 响应式规范

> 所有 HTML 页面必须支持三个断点。
> mobile-first 开发，先在小屏把核心信息排好，再向大屏扩展。

---

## 断点

```
手机:  <768px
平板:  768px ~ 1023px
桌面:  ≥1024px
```

## 通用模板

```css
/* 桌面优先（默认样式） */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}

/* 平板 */
@media (max-width: 1023px) {
  .container { padding: 0 24px; }
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
}

/* 手机 */
@media (max-width: 767px) {
  .container { padding: 0 16px; }
  .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
  .filters { flex-direction: column; }
  .filter-search input { width: 100%; }
  table { font-size: 13px; }
  th, td { padding: 10px 12px; }
  h1 { font-size: 24px; }
}
```

## 各布局类型的响应式策略

### 导航型布局（后台/仪表盘）

| 断点 | 导航 | 内容区 | 调整 |
|:----|:-----|:-------|:-----|
| ≥1024px | 左侧固定 240px | 剩余宽度 | 完整布局 |
| 768-1023px | 折叠为汉堡菜单 | 全宽 | 导航图标 + 悬浮展开 |
| <768px | 底部 Tab 或隐藏 | 全宽 | 导航折叠，全屏内容 |

### 流式布局（展示/画廊/品牌页）

| 断点 | 网格 | 间距 | 字号 |
|:----|:-----|:-----|:-----|
| ≥1024px | 3-4 列 | 24px | 正常 |
| 768-1023px | 2 列 | 16px | 略缩 |
| <768px | 1 列 | 12px | 小 |

### 沉浸式布局（图谱/百科）

| 断点 | 布局 | 调整 |
|:----|:-----|:-----|
| ≥1024px | 左侧索引 + 右侧详情/图谱 | 完整双栏 |
| 768-1023px | 索引可折叠 | 图谱全宽 + 浮动详情 |
| <768px | 单栏堆叠 | 图谱全宽 + 详情全宽底部 |

## 通用响应式工具类

```css
/* 响应式网格 */
.grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }

@media (max-width: 1023px) {
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 767px) {
  .grid-2, .grid-3, .grid-4 { grid-template-columns: 1fr; }
}

/* 响应式隐藏 */
.hide-mobile { display: block; }
.show-mobile { display: none; }
@media (max-width: 767px) {
  .hide-mobile { display: none; }
  .show-mobile { display: block; }
}
```

## 检查清单

```
[ ] 桌面 ≥1024px — 完整布局，多列网格
[ ] 平板 768-1023px — 网格减列，保持可读
[ ] 手机 <768px — 单列布局，touch-friendly
[ ] 没有横向滚动（overflow-x 仅限表格容器）
[ ] 触控元素大小 ≥44px
[ ] 字体在手机上可读（最小 14px）
```
