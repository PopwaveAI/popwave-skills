# 组件库参考 — HTML 结构

> 所有 HTML 页面的组件从此清单按需组装。
> 遵守统一的 CSS class 命名，确保各 skill 输出的一致性。

---

## 1. 指标卡片 (Metric Card)

```html
<div class="metric">
  <div class="metric-value">12,847</div>
  <div class="metric-label">总用户数</div>
  <div class="metric-trend up">+12.5% <span>较上月</span></div>
</div>
```

```css
.metric {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 24px;
}
.metric-value {
  font-size: 32px; font-weight: 600; line-height: 1.1;
  color: var(--text); letter-spacing: -0.02em;
}
.metric-label {
  font-size: 13px; color: var(--text-secondary); margin-top: 4px;
}
.metric-trend {
  font-size: 12px; margin-top: 8px;
}
.metric-trend.up { color: var(--green); }
.metric-trend.down { color: var(--red); }
```

---

## 2. 内容卡片 (Content Card)

```html
<div class="card">
  <div class="card-header">
    <h3>卡片标题</h3>
    <button class="btn-sm">操作</button>
  </div>
  <div class="card-body">
    <p>卡片主要内容区域</p>
  </div>
</div>
```

### 变体

| Class | 用法 |
|:------|:-----|
| `.card` | 标准卡片，白色背景 + 边框 + 圆角 |
| `.card-flat` | 无边框卡片，仅 hover 高亮 |
| `.card-highlight` | 左边框用 `--primary` 颜色强调 |
| `.card-glass` | 毛玻璃效果（半透明 + backdrop-filter） |
| `.card-plain` | 极简卡片，无边框无阴影 |

---

## 3. 数据表格 (Data Table)

```html
<div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>名称</th>
        <th>类别</th>
        <th>状态</th>
        <th>评分</th>
        <th>操作</th>
      </tr>
    </thead>
    <tbody>
      <tr onclick="goDetail(1)">
        <td class="cell-name">项目名称</td>
        <td><span class="tag tag-blue">科技</span></td>
        <td><span class="tag tag-green">活跃</span></td>
        <td>4.8</td>
        <td><button class="btn-text">查看</button></td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.table-wrap {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}
table { width: 100%; border-collapse: collapse; }
th {
  text-align: left; padding: 12px 16px;
  font-size: 12px; font-weight: 500; color: var(--text-secondary);
  background: var(--surface); border-bottom: 1px solid var(--border);
  text-transform: uppercase; letter-spacing: 0.05em;
}
td {
  padding: 12px 16px; font-size: 14px;
  border-bottom: 1px solid var(--divider);
}
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--primary-light); }
```

---

## 4. 状态标签 (Tag)

```html
<span class="tag tag-green">已通过</span>
<span class="tag tag-amber">待审核</span>
<span class="tag tag-red">已拒绝</span>
<span class="tag tag-blue">进行中</span>
<span class="tag tag-gray">草稿</span>
```

```css
.tag {
  display: inline-block; padding: 2px 10px;
  font-size: 12px; font-weight: 500; line-height: 1.5;
  border-radius: 999px; white-space: nowrap;
}
.tag-green { background: #dcfce7; color: #166534; }
.tag-amber { background: #fef3c7; color: #92400e; }
.tag-red { background: #fee2e2; color: #991b1b; }
.tag-blue { background: #dbeafe; color: #1e40af; }
.tag-gray { background: #f1f5f9; color: #475569; }
```

---

## 5. 评分条 (Progress Bar)

```html
<div class="progress-bar">
  <div class="progress-fill" style="width: 75%;"></div>
</div>
```

```css
.progress-bar {
  height: 8px; background: var(--border); border-radius: 999px; overflow: hidden;
}
.progress-fill {
  height: 100%; background: var(--primary); border-radius: 999px;
  transition: width 0.4s ease;
}
.progress-fill.green { background: var(--green); }
.progress-fill.amber { background: var(--amber); }
.progress-fill.red { background: var(--red); }
```

---

## 6. 筛选栏 (Filters)

```html
<div class="filters">
  <div class="filter-group">
    <label>平台</label>
    <select><option>全部</option><option>B站</option><option>抖音</option></select>
  </div>
  <div class="filter-group">
    <label>状态</label>
    <select><option>全部</option><option>活跃</option><option>待审核</option></select>
  </div>
  <div class="filter-search">
    <input type="search" placeholder="搜索名称..." oninput="filterList(this.value)">
  </div>
  <button class="btn" onclick="resetFilters()">重置</button>
</div>
```

```css
.filters {
  display: flex; gap: 16px; align-items: flex-end; flex-wrap: wrap;
  padding: 16px 0; margin-bottom: 16px;
}
.filter-group { display: flex; flex-direction: column; gap: 4px; }
.filter-group label { font-size: 12px; color: var(--text-secondary); font-weight: 500; }
.filter-group select, .filter-search input {
  height: 36px; padding: 0 12px; border: 1px solid var(--border); border-radius: var(--radius-sm);
  background: var(--card); color: var(--text); font-size: 14px;
}
.filter-search input { width: 200px; }
```

---

## 7. Tab 切换 (Tabs)

```html
<div class="tabs" data-tabs="detail-tabs">
  <button class="tab active" onclick="switchTab('detail-tabs', 'overview')">概览</button>
  <button class="tab" onclick="switchTab('detail-tabs', 'risk')">风险</button>
  <button class="tab" onclick="switchTab('detail-tabs', 'history')">历史</button>
</div>
<div id="tab-detail-tabs-overview" class="tab-content active">概览内容</div>
<div id="tab-detail-tabs-risk" class="tab-content">风险内容</div>
<div id="tab-detail-tabs-history" class="tab-content">历史内容</div>
```

```javascript
function switchTab(group, name) {
  document.querySelectorAll(`[data-tabs="${group}"] .tab`).forEach(t => t.classList.remove('active'));
  document.querySelectorAll(`[id^="tab-${group}-"]`).forEach(c => c.classList.remove('active'));
  document.querySelector(`[data-tabs="${group}"] .tab[onclick*="'${name}'"]`).classList.add('active');
  document.getElementById(`tab-${group}-${name}`).classList.add('active');
}
```

```css
.tabs { display: flex; gap: 0; border-bottom: 1px solid var(--border); margin-bottom: 20px; }
.tab {
  padding: 10px 20px; font-size: 14px; font-weight: 500; color: var(--text-secondary);
  border: none; background: none; cursor: pointer; border-bottom: 2px solid transparent;
}
.tab.active { color: var(--primary); border-bottom-color: var(--primary); }
.tab:hover { color: var(--text); }
.tab-content { display: none; }
.tab-content.active { display: block; }
```

---

## 8. 弹窗 (Modal)

```html
<div class="modal-overlay" id="modal-overlay" onclick="closeModal()">
  <div class="modal-content" onclick="event.stopPropagation()">
    <div class="modal-header">
      <h3>弹窗标题</h3>
      <button class="modal-close" onclick="closeModal()">&times;</button>
    </div>
    <div class="modal-body">
      <!-- 弹窗内容 -->
    </div>
    <div class="modal-footer">
      <button class="btn" onclick="closeModal()">取消</button>
      <button class="btn btn-primary" onclick="confirmAction()">确认</button>
    </div>
  </div>
</div>
```

```css
.modal-overlay {
  position: fixed; inset: 0; z-index: 1000;
  background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: opacity 0.2s;
}
.modal-overlay.open { opacity: 1; pointer-events: auto; }
.modal-content {
  background: var(--card); border-radius: var(--radius);
  width: 90%; max-width: 520px; max-height: 80vh; overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
.modal-header, .modal-footer {
  padding: 16px 24px; display: flex; align-items: center;
  justify-content: space-between;
}
.modal-body { padding: 0 24px 20px; }
.modal-header { border-bottom: 1px solid var(--border); }
.modal-footer { border-top: 1px solid var(--border); justify-content: flex-end; gap: 12px; }
.modal-close { width: 32px; height: 32px; border: none; background: none; font-size: 24px; cursor: pointer; color: var(--text-secondary); border-radius: 6px; }
.modal-close:hover { background: var(--surface); }
```

---

## 9. 详情页头部 (Detail Header)

```html
<div class="detail-header">
  <div class="detail-avatar">
    <img src="..." alt="avatar">
  </div>
  <div class="detail-info">
    <h2>名称</h2>
    <div class="detail-meta">
      <span class="tag tag-green">活跃</span>
      <span class="detail-stat"><strong>4.8</strong> 综合评分</span>
      <span class="detail-stat"><strong>128</strong> 合作案例</span>
    </div>
  </div>
  <div class="detail-actions">
    <button class="btn">操作</button>
  </div>
</div>
```

---

## 10. 空状态 (Empty State)

```html
<div class="empty-state">
  <div class="empty-icon">
    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
    </svg>
  </div>
  <h3>暂无数据</h3>
  <p>当前筛选条件下没有找到结果</p>
  <button class="btn" onclick="resetFilters()">重置筛选</button>
</div>
```

```css
.empty-state {
  text-align: center; padding: 60px 20px; color: var(--text-secondary);
}
.empty-icon { opacity: 0.3; margin-bottom: 16px; }
.empty-state h3 { color: var(--text); margin-bottom: 8px; }
.empty-state p { font-size: 14px; margin-bottom: 20px; }
```

---

## 11. 加载状态 (Skeleton)

```html
<div class="skeleton-list">
  <div class="skeleton-row">
    <div class="skeleton skeleton-circle"></div>
    <div class="skeleton skeleton-line w-60"></div>
    <div class="skeleton skeleton-line w-30"></div>
  </div>
  <div class="skeleton-row">
    <div class="skeleton skeleton-circle"></div>
    <div class="skeleton skeleton-line w-50"></div>
    <div class="skeleton skeleton-line w-40"></div>
  </div>
</div>
```

```css
@keyframes pulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
.skeleton { background: var(--border); border-radius: var(--radius-sm); animation: pulse 1.5s ease-in-out infinite; }
.skeleton-line { height: 14px; }
.skeleton-circle { width: 40px; height: 40px; border-radius: 50%; }
.skeleton-row { display: flex; gap: 12px; align-items: center; padding: 12px 0; }
.w-30 { width: 30%; } .w-40 { width: 40%; } .w-50 { width: 50%; } .w-60 { width: 60%; }
```

---

## 12. 按钮 (Buttons)

```html
<button class="btn">默认</button>
<button class="btn btn-primary">主要</button>
<button class="btn btn-ghost">幽灵</button>
<button class="btn btn-text">文字</button>
<button class="btn btn-sm">小按钮</button>
<button class="btn btn-primary" disabled>禁用</button>
```

```css
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  height: 36px; padding: 0 16px; border: 1px solid var(--border);
  border-radius: var(--radius-sm); background: var(--card);
  color: var(--text); font-size: 14px; font-weight: 500;
  cursor: pointer; transition: all 0.15s;
}
.btn:hover { border-color: var(--primary); color: var(--primary); }
.btn-primary { background: var(--primary); color: white; border-color: var(--primary); }
.btn-primary:hover { opacity: 0.9; }
.btn-ghost { border-color: transparent; background: transparent; }
.btn-ghost:hover { background: var(--surface); }
.btn-text { border: none; background: none; color: var(--primary); padding: 0; height: auto; }
.btn-text:hover { text-decoration: underline; }
.btn-sm { height: 28px; padding: 0 12px; font-size: 12px; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
```

---

## 13. 内容互联 (Content Interconnect)

> 适用于"列表卡片 → 详情正文"双向跳转的场景，如拆书角色卡片点击跳转到章内对应位置。

### 数据结构（单一数据源）

```javascript
const NODES = [
  {
    id: 'char-1',
    title: '陈昂',
    badge: '主角 · 卷1',
    image: 'data:image/png;base64,...',
    chapter: 0,          // 关联章节索引
    anchor: '陈昂服下NZT',  // 在原文中定位的关键短语
    excerpt: '陈昂服下NZT，大脑超频。进入笑傲世界...',
    meta: 'NZT · 大脑开发',
  },
  // ...
];
```

### 正向：卡片 → 正文跳转 + 高亮

```javascript
function jumpToAnchor(node) {
  showPage('reader');
  setTimeout(() => {
    if (node.chapter !== curCh) showCh(node.chapter);
    setTimeout(() => highlightInChapter(node.anchor), 220);
  }, 80);
}

function highlightInChapter(anchor) {
  const ps = document.querySelectorAll('.chapter-body p');
  for (const p of ps) {
    if (p.textContent.includes(anchor)) {
      const safe = anchor.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      p.innerHTML = p.innerHTML.replace(
        new RegExp(safe),
        `<mark class="flash">${anchor}</mark>`
      );
      p.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(() => {
        const m = p.querySelector('mark.flash');
        if (m) m.replaceWith(document.createTextNode(m.textContent));
      }, 2600);
      return;
    }
  }
}
```

```css
mark.flash {
  background: rgba(184,146,74,.25);
  animation: flash 2.4s ease-out;
}
@keyframes flash {
  0%   { background: rgba(184,146,74,.6); box-shadow: 0 0 0 6px rgba(184,146,74,.5); }
  100% { background: transparent;        box-shadow: 0 0 0 3px transparent; }
}
```

### 反向：正文渲染时插入标记图标

```javascript
function markNodesInChapter(chapterIdx) {
  const matched = NODES.filter(n => n.chapter === chapterIdx);
  matched.forEach(node => {
    const ps = document.querySelectorAll('.chapter-body p');
    for (const p of ps) {
      if (p.dataset.marked) continue;
      if (!p.textContent.includes(node.anchor)) continue;
      const safe = node.anchor.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      p.innerHTML = p.innerHTML.replace(
        new RegExp(safe),
        `<span class="node-mark">$&<button class="node-icon" data-id="${node.id}">&#9670;</button></span>`
      );
      p.dataset.marked = '1';
      break;
    }
  });
}
```

### hover 浮窗预览

```javascript
function showPreview(iconEl) {
  const node = NODES.find(n => n.id === iconEl.dataset.id);
  if (!node) return;
  const existing = document.querySelector('.preview-tip');
  if (existing) existing.remove();

  const tip = document.createElement('div');
  tip.className = 'preview-tip';
  tip.innerHTML = `
    <div class="preview-img" style="background-image:url('${node.image}')"></div>
    <div class="preview-cap"><strong>${node.title}</strong><span>${node.meta}</span></div>
  `;
  document.body.appendChild(tip);

  const r = iconEl.getBoundingClientRect();
  const W = 320, H = 240;
  let left = r.right + 12, top = r.top - 10;
  if (left + W > innerWidth - 12) left = r.left - W - 12;
  if (left < 12) left = 12;
  if (top + H > innerHeight - 12) top = innerHeight - H - 12;
  if (top < 60) top = 60;
  tip.style.cssText = `left:${left}px;top:${top}px`;
}
function hidePreview() {
  document.querySelector('.preview-tip')?.remove();
}
```

### hover 浮窗 CSS

```css
.preview-tip {
  position: fixed; z-index: 9999;
  width: 320px; border-radius: 12px; overflow: hidden;
  background: var(--card); border: 1px solid var(--border);
  box-shadow: 0 8px 32px rgba(0,0,0,.18);
  pointer-events: none; animation: fadeIn .15s ease;
}
.preview-img {
  height: 160px; background-size: cover; background-position: center;
}
.preview-cap {
  padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;
}
.preview-cap strong { font-size: 13px; color: var(--text); }
.preview-cap span { font-size: 11px; color: var(--text-secondary); }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### 内容互联的收益

只需要在 `NODES` 数组里加一条数据，自动获得：
- 卡片展示（在列表/索引页）
- 卡片点击 → 跳转正文 + 高亮
- 正文 → 标记图标 + hover 浮窗预览 + 点击跳回详情

**新增/修改一个节点不需要改任何渲染逻辑。**

---

> **使用原则：** 按需取用，不堆砌组件。
> 一个页面如果同时出现 7 种以上不同类型的组件，说明信息架构需要整理。
> 相反，2-3 种组件用好了，页面就足够充实。
