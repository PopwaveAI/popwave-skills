# CHANGELOG

## v1.3.0 (2026-08-13)

### 元数据同步

- skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步至 v1.3.0。

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

---

> 历史版本条目已归档：`_archive/changelog-history/pop-recommend/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
