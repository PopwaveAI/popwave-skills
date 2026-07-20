# CHANGELOG

## v1.0.0 — 2026-07-20

### 新建
- 基于 v1.5.3 工作稿的临时管线正式 skill 化
- **Step 1 三阶段价值扫描**：放弃逐章摘要，改为骨架扫描(15-20章)+锚点深读(10-15章)+阅感采样(5-8章)，100章只精读30-40章
- **spoiler 三级控制**：safe / mild / major，Step2 只消费 safe+mild
- **Step 2 评审生成**：合并 v1.5.3 的 public-review-input + review-draft 两个JSON为一个 review.json
- **Step 3 HTML渲染**：模板与数据分离，禁止内联JSON到 `<script>` 标签
- 5个产出模板：structure-map / anchor-pool / reading-metrics / review / recommend-card
- 1个参考文档：page-layout-guide（推书卡9页布局指南）

### 修复
- 砍掉 arc-summaries 的6个"待补充"字段（character_state_changes / relationship_changes / new_rules / setups / payoffs / pacing_observations）
- 砍掉 arc-summaries 的 turning_point 字段（剧透点不应作为推书核心字段）
- 禁止占位符输出（"故事内容"/"待补充"）
