# Demo HTML 框架模板

## 核心结构

```
单文件 HTML
├── <style> 全部 CSS 内联
├── <nav> 左侧固定导航 (240px)
│   ├── 工作台
│   ├── 资源/对象列表
│   └── 合作管理 / 评估中心
├── <main>
│   ├── <header> 顶部栏 (搜索 + 面包屑)
│   └── <section.page> × N 个页面
├── <script src="Chart.js CDN">
└── <script> 全部数据和逻辑
```

## CSS 变量体系

```css
:root{
  --bg:#f1f5f9; --card:#fff; --t:#0f172a; --s:#64748b;
  --p:#4f46e5; --pl:#eef2ff; --b:#e2e8f0; --r:10px;
  --red:#ef4444; --amber:#f59e0b; --green:#10b981; --nav:240px
}
```

## 核心组件

| 组件 | CSS class | 用途 |
|------|-----------|------|
| 指标卡片 | .metric + .v + .l | 数据概览 |
| 内容卡片 | .c + .c-h | 通用容器 |
| 数据表格 | table / th / td | 列表和对比 |
| 标签 | .tag + .tg/.ty/.tb/.tr | 状态标记 |
| 评分条 | .sb + .sb-bar + .sb-fill | 可视化评分 |
| 看板列 | .kanban + .kanban-col + .kcard | 流程看板 |
| 风险提示 | .alert + .red/.amber/.green | 风险事件 |
| Tab 切换 | .tabs + .tab + .tab-content | 详情页切换 |
| 筛选栏 | .fbar + select + input | 列表筛选 |

## 页面切换机制

```javascript
function showPage(name){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n=>n.classList.remove('active'));
  var pg=document.getElementById('page-'+name);
  if(pg)pg.classList.add('active');
  var navEl=document.querySelector('[data-page="'+name+'"]');
  if(navEl)navEl.classList.add('active');
}

function goDetail(id){
  showPage('detail');
  renderDetail(id);
}
```

> 关键：showPage 中 querySelector 和 getElementById 都必须空值保护，防止详情页跳转时因 nav 中无对应菜单而报错。

## 图表

使用 Chart.js v4.4.0 CDN：
- 饼图/环形图 (doughnut)：平台/类别分布
- 柱状图 (bar)：粉丝量级分布、CPM 对比
- 折线图 (line)：月度趋势
- 雷达图 (radar)：多维度评估
- 所有 chart 变量存 window.charts 对象便于销毁重建

## 最终处理

生成 standalone 版本：
```python
# 1. 下载 Chart.js
# 2. 替换 <script src="CDN"> 为 <script>chartJsContent</script>
# 3. 输出 *_Standalone.html
```

## 5 个页面模板

### 1. 工作台 Dashboard (page-dashboard)
- 4 个指标卡片
- 左侧：待办事项列表 + 右侧：风险预警
- 图表区：饼图 + 趋势折线图
- 底部：最近入库列表（可点击进详情）

### 2. 列表页 (page-list)
- 筛选栏：平台/类别/风险/评分 + 搜索框
- 列表表头 + 数据行，每行可点击进详情

### 3. 详情页 (page-detail)
- 顶部：头像、名称、评分、标签、风险等级
- 4 个 Tab：
  - 评估概览：雷达图 + 各维度得分
  - 风险评估：风险事件时间线（三级颜色）
  - 合作/历史案例：每案例一个卡片
  - 数据详情：12+ 指标表格

### 4. 看板页 (page-kanban)
- 多阶段看板列（根据 PRD 流程调整阶段名）
- 每个卡片：对象名 + 关联需求 + 金额 + 负责人 + 截止日

### 5. 评估中心 (page-eval)
- 2-3 人雷达图对比
- 指标逐项 PK 表（高亮最优值）
