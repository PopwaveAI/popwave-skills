# Shared HTML Design Core

> 所有产出 HTML 的 skill **必须遵守此规范**。
> 这是视觉质量的底线，不是上限。

---

## 一、CSS 变量体系

所有 HTML 必须使用以下命名约定的 CSS 变量：

```css
:root {
  /* ── 背景层 ── */
  --bg: #f1f5f9;         /* 页面背景 */
  --card: #ffffff;       /* 卡片背景 */
  --surface: #f8fafc;    /* 浅表面（次级卡片） */

  /* ── 颜色层 ── */
  --primary: #4f46e5;    /* 主色 — 靛蓝 600 */
  --primary-light: #eef2ff; /* 主色浅色 */
  --accent: #c9a84c;     /* 强调色 */
  --red: #ef4444;        /* 危险 */
  --amber: #f59e0b;      /* 警告 */
  --green: #10b981;      /* 成功 */
  --blue: #3b82f6;       /* 信息 */

  /* ── 文字层 ── */
  --text: #0f172a;       /* 主文字 */
  --text-secondary: #64748b; /* 次要文字 */
  --text-dim: #94a3b8;   /* 辅助文字 */

  /* ── 边界层 ── */
  --border: #e2e8f0;     /* 边框 */
  --divider: #f1f5f9;    /* 分割线 */

  /* ── 间距层 — 标准 4px 模数 ── */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;

  /* ── 字体层 ── */
  --font-sans: "Inter", -apple-system, BlinkMacSystemFont, "Noto Sans SC", sans-serif;
  --font-mono: "JetBrains Mono", "SF Mono", monospace;

  /* ── 布局层 ── */
  --radius: 10px;        /* 统一圆角 */
  --radius-sm: 6px;
  --shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.05), 0 2px 4px rgba(0,0,0,0.04);
  --nav-width: 240px;    /* 左侧导航宽度（如适用） */
}
```

### 深色模式（可选）

```css
[data-theme="dark"] {
  --bg: #0f172a;
  --card: #1e293b;
  --surface: #1a2332;
  --text: #f1f5f9;
  --text-secondary: #94a3b8;
  --text-dim: #64748b;
  --border: #334155;
  --divider: #1e293b;
}
```

### 覆盖规则

如需调整主色（不同产品场景），**只改 `--primary` 和 `--primary-light`**：
- 企业工具 → `#4f46e5` / `#eef2ff`（靛蓝）
- 医疗 → `#0891b2` / `#ecfeff`（青色）
- 金融 → `#059669` / `#ecfdf5`（翠绿）
- 社交 → `#ec4899` / `#fdf2f8`（粉红）
- 通用兜底 → 使用默认靛蓝

---

## 二、间距体系

间距只取标准尺度的倍数，不取任意值：

```
4px → 8px → 12px → 16px → 24px → 32px → 48px → 64px → 96px
```

### 应用规则

| 场景 | 间距 | 说明 |
|:----|:-----|:-----|
| 卡片内间距 | 20-24px | 内容不贴边 |
| 卡片间距 | 16-24px | 网格布局中卡片之间的 gap |
| 段落间距 | 16-24px | 段落之间的间隔 |
| 按钮内间距 | 10px 20px / 12px 24px | 垂直 / 水平 |
| 区块间距 | 48-80px | section 之间的分隔 |
| 页面边距 | 24-48px | 内容区距视口边缘 |
| 留白 | **宁可多不可少** | 留白是高级感的来源 |

---

## 三、字体层级

```css
h1 { font-size: 28-36px; font-weight: 600; line-height: 1.25; letter-spacing: -0.02em; }
h2 { font-size: 20-24px; font-weight: 600; line-height: 1.3; }
h3 { font-size: 16-18px; font-weight: 600; line-height: 1.4; }
h4 { font-size: 14-16px; font-weight: 500; line-height: 1.5; }
p  { font-size: 14px; font-weight: 400; line-height: 1.6; }
.small { font-size: 12-13px; color: var(--text-secondary); }
.label { font-size: 11-12px; font-weight: 500; letter-spacing: 0.05em; text-transform: uppercase; color: var(--text-dim); }
.mono { font-family: var(--font-mono); font-size: 13px; }
```

### 禁用规则
- font-weight > 700（除非极短的展示标题）
- 页面内超过 3 种字体权重
- 正文用纯黑 `#000` 或纯白 `#fff`（降级为 `#0f172a` / `#f8fafc`）

---

## 四、颜色使用规则

| 原则 | 说明 |
|:----|:-----|
| 主色 1 个 | 占 70% 面积（背景/卡片） |
| 辅色 1-2 个 | 占 25%（边框/次要表面） |
| 强调色 1 个 | 占 5%（唯一吸引眼球的地方） |
| 禁用 | 彩虹色标签、超过 4 种不相关颜色 |
| 状态色 | 红/黄/绿仅用于状态标记，不用于装饰 |

---

## 五、背景设计规范

当页面需要背景时，遵循以下层级（优先使用 CSS 纯方案，无需外部资源）：

### 5.1 通用背景（默认）

```css
/* 纯色背景 — 默认。干净、专业、安全 */
body { background: var(--bg); }
```

### 5.2 渐变背景

```css
/* 浅色渐变 — 适合仪表盘/数据页面 */
body { background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); }

/* 深色渐变 — 适合沉浸式/展示型页面 */
body { background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%); }
```

### 5.3 网格纹理

```css
/* 极淡网格 — 适合数据密集场景 */
body::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
  pointer-events: none;
  z-index: -1;
}
```

### 5.4 光影氛围

```css
/* 径向光晕 — 适合 Hero 区域或深色页面 */
body::after {
  content: '';
  position: fixed;
  top: -20%; left: -10%;
  width: 60%; height: 60%;
  background: radial-gradient(circle at 30% 40%, rgba(79,70,229,0.08), transparent 60%);
  pointer-events: none;
  z-index: -1;
}
```

### 选择指南

| 页面类型 | 推荐背景方案 |
|:---------|:------------|
| 数据仪表盘 / 列表页 | 纯色或极淡网格 |
| 详情页 / 内容页 | 纯色 |
| Hero / 品牌展示 | 渐变或光影氛围 |
| 沉浸式 / 知识图谱 | 深色渐变 + 光影 |
| 营销 / 画廊 | 浅色渐变 + 光影 |

---

## 六、卡片设计

```css
/* 标准卡片 */
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 24px;
}

/* 悬浮效果 */
.card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--primary);
}
```

### 卡片变体

| 变体 | 用法 | 样式 |
|:----|:-----|:-----|
| `.card` | 默认 | 白底 + 边框 + 圆角 |
| `.card-flat` | 密集列表 | 无边框，仅 row hover 高亮 |
| `.card-highlight` | 关键指标 | 左边框强调色 + 数字放大 |
| `.card-glass` | 沉浸式深色 | 半透明背景 + 毛玻璃 |
| `.card-plain` | 内嵌 | 无边框、无阴影、极淡背景 |

---

## 七、组件

所有 HTML 页面的组件从以下清单中按需组装：

| 组件 | CSS 名称 | 用途 | 参考 DEMO |
|:----|:---------|:-----|:----------|
| 指标卡片 | `.metric` / `.metric-value` / `.metric-label` | 数据概览 | 大数字 + 标签 + 趋势 |
| 内容卡片 | `.card` / `.card-header` / `.card-body` | 通用容器 | 标题 + 内容 + 操作 |
| 数据表格 | `table` / `thead` / `tbody` / `th` / `td` | 列表数据 | 表头固定 + 行 hover |
| 状态标签 | `.tag` + `.tag-green/.tag-amber/.tag-red/.tag-blue` | 状态标记 | 彩色圆角小标签 |
| 评分条 | `.progress-bar` / `.progress-fill` | 图示占比 | 百分比条 |
| 筛选栏 | `.filters` / `select` / `input[type=search]` | 数据过滤 | 下拉 + 搜索 + 按钮 |
| Tab 切换 | `.tabs` / `.tab` / `.tab-content` + JS | 多视图 | 点 Tab 切换内容区 |
| 看板列 | `.kanban` / `.kanban-col` / `.kcard` | 流程管理 | 多列拖拽卡片 |
| 弹窗/抽屉 | `.modal` / `.modal-overlay` / `.modal-content` | 详情/编辑 | 遮罩 + 居中面板 |
| 详情页 | `.detail-header` / `.detail-tabs` / `.detail-content` | 对象详情 | 头部 + Tab 切换 |
| 空状态 | `.empty-state` | 无数据提示 | 图标 + 文字 + 操作按钮 |
| 加载状态 | `.skeleton` | 数据加载中 | 脉冲动画占位块 |

> 每种组件的完整 HTML 结构参考见 `components.md`

---

## 八、页面布局骨架

### 8.1 导航型布局（数据系统/后台）

```
┌──────────────┬─────────────────────────────────────┐
│              │  <header> 顶部栏（搜索/面包屑/操作）   │
│  <nav>       ├─────────────────────────────────────┤
│  左侧固定    │  <main>                              │
│  导航        │  ├── <section.page#page-dashboard>   │
│  (240px)     │  ├── <section.page#page-list>        │
│              │  ├── <section.page#page-detail>      │
│              │  └── ...                             │
└──────────────┴─────────────────────────────────────┘
```

### 8.2 流式布局（展示/内容/画廊）

```
┌────────────────────────────────────────────────────┐
│  <header> / <nav>                                   │
├────────────────────────────────────────────────────┤
│  <section.hero> — 大标题 + 副标题 + CTA              │
│  <section.stats> — 关键数字                          │
│  <section.about> — 介绍文字                          │
│  <section.content> — 卡片网格/列表                    │
│  <section.cta> — 号召行动                             │
│  <footer> — 版权 + 链接                              │
└────────────────────────────────────────────────────┘
```

### 8.3 沉浸式布局（图谱/百科/档案）

```
┌────────────────────────────────────────────────────┐
│  全屏 Canvas/SVG 交互区域                            │
│  ┌── 侧边信息面板（浮动） ──┐                        │
│  │  标题 / 描述 / 详情      │                        │
│  └─────────────────────────┘                        │
│  底部控制栏（缩放/主题/图例）                          │
└────────────────────────────────────────────────────┘
```

---

## 九、质量门禁清单

每页 HTML 交付前必须逐条检查：

```
[ ] CSS 变量命名遵循 DESIGN_CORE 规范
[ ] 使用 --primary / --card / --text 等标准变量名
[ ] 间距使用 4px 模数（4/8/12/16/24/32/48/64/96）
[ ] 颜色不超过 4 种（不含黑白灰）
[ ] 强调色只在一处使用
[ ] 字体层级清晰：h1/h2/h3/正文/辅助
[ ] 正文不用纯黑 #000 或纯白 #fff
[ ] 卡片间距统一
[ ] hover 状态精致但不浮夸
[ ] 留白 > 内容区域
[ ] 没有元素重叠或溢出
[ ] 看起来像专业产品，不像拼凑品
[ ] 双击 HTML 可直接在浏览器打开
[ ] 零 emoji（所有视觉标识用 CSS/SVG 实现）
```

---

> 设计核心是底线，不是天花板。
> 视觉上限由场景模板（templates/）和 LLM 的创意决定，但底线由这套规范保证。
> 遵守 DESIGN_CORE 的 HTML，至少值 75 分。
