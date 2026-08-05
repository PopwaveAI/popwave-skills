# CHANGELOG — short-reviewer
## v1.0.0 | 2026-08-04
### 新建 skill：短篇评审器（Popwave规范改造）
- 初始版本。按Popwave Skill设计规范完整重构
- SKILL.md 压缩至约75行，含YAML frontmatter、SOP骨架表、9维框架、等级表、红线、速查表、版本
- 拆分执行步骤至 steps/：step1-load（加载范围确认）、step2-diagnose（9维逐项诊断）、step3-report（报告输出）
- 创建 templates/review-report.tpl.md：评审报告模板，含总览/亮点/不足/分维诊断/AI味儿/总结
- 核心原则：只诊断不修改
- AI味儿不纳入评分，仅作参考
- 每维诊断必须对标具体前置卡片数据
- 补全 skill.json：tags=["短篇创作","质量评审"]、author="popwave"、license="UNLICENSED"
