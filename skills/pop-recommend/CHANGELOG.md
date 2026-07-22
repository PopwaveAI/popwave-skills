# CHANGELOG

## v1.2.0 (2026-07-22)

### 按Popwave Skill设计规范重写SKILL.md结构

**改动**：
- SKILL.md从254行压缩到46行（≤100行），frontmatter加触发条件式description
- 红线从4条改为5条（新增读取协议红线），保留全部业务红线
- 速查表从产出路径+9页设计语言+文件结构改为全文件目录引导（含steps/references/templates）
- 新增强弱加载保障声明
- 版本历史只留最新一条，其余在CHANGELOG.md
- SOP骨架每step压缩到1-2行
- skill.json版本1.1.0→1.2.0，description改为触发条件式

**保留不动**：三阶段价值扫描方法论/9页设计语言/step2.md/step3.md——业务方法论不做改动

## v1.1.0 — 2026-07-20

### 重构：串联SOP链式加载架构
- **SKILL.md 内化 Step 1 完整方法论**：解决 Pop 平台仅注入 SKILL.md 导致 step 文件缺失的加载问题
- **steps/ 从 step2 开始**：step1.md 删除，方法论并入 SKILL.md
- **链式加载钩子**：SKILL.md 末尾 → "读取 steps/step2.md" ； step2.md 末尾 → "读取 steps/step3.md" ； step3.md 末尾 → "链式管线结束"
- **红线第4条更新**：Step 文件链式加载替代"HTML模板数据分离"（已改为内联方案）

### 架构原理
串联式 SOP skill 的加载保障：SKILL.md(Step1内化→自执行) → steps/step2.md(按需读取) → steps/step3.md(按需读取)。每步只依赖一个文件加载，无跨文件跳转风险

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
