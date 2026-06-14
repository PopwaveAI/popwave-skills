# Phase 4 -- 生成交互 Demo

> 用户确认 PRD 后说"生成 Demo"触发。

---

## Step 4.1：数据准备

| 层次 | 来源 |
|------|------|
| 业务数据 | 网络搜索行业案例、基准数据、竞品 |
| 角色模板 | references/kol_templates.json (12 个预置角色) |
| 平台基准 | references/platform_benchmarks.json |

Demo 使用真实名称。如果产品领域不涉及 KOL，替换为对应领域的真实案例对象。

---

## Step 4.2：构建 Demo 结构

参照 `references/demo_framework.md`，根据第 6 章的页面设计生成：

| 页面 | 来源 |
|------|------|
| 工作台 Dashboard | 第 6 章线稿 -> Dashboard 页 |
| 列表页 | 第 6 章线稿 -> List 页 |
| 详情页 (每对象独立) | 第 6 章线稿 -> Detail 页，4 Tab：评估/风险/案例/数据 |
| 看板页 | 第 3 章流程 + 第 6 章线稿 -> Kanban 页 |
| 评估/对比中心 | 第 6 章线稿 -> Compare 页 |

---

## Step 4.3：技术交付

- 单文件 HTML，数据 JS 内嵌
- 左侧固定导航 + 右侧内容区
- 详情 Tab 切换，showPage()/goDetail() 驱动（必须空值保护）
- 最终用 Python 内联 Chart.js -> Standalone 版本

---

## 门禁

| 门禁 |
|:------|
| 未搜索真实数据就编造示例数据 -> 退回，必须搜索获取真实信息 |
| 交付物不是单文件 HTML -> 退回合并为单文件 |
| 缺空值保护 -> 退回补充 |
| 用户未确认 PRD 前不生成 Demo -> 退回 Phase 2 |
