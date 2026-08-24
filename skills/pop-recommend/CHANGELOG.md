# CHANGELOG — pop-recommend

## v2.0.0 (2026-08-24)

### steps 两件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step2 / step3 两件全合入 SKILL.md 对应节
- **执行模式明确**：Step1 三阶段价值扫描可派子agent（只读扫描类工作天然适配——子agent读原文扫描+提取锚点+打分回报，主agent落盘5个JSON）；Step2 评审合成与 Step3 HTML渲染主agent直执
- **内容精炼**：step2 的11条合成逻辑整理为单表（spoiler三级控制/模糊化规则/evidence_ids绑定/6维评分与推荐结论算法全保留）；review.json完整schema压缩为合成规则表内字段标注；step3 渲染流程内联；红线5从"step文件链式加载"改为"管线顺序强制"（业务意图不变：禁止跳步）
- skill.json version 1.3.0→2.0.0

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
