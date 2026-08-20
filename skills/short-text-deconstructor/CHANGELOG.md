# CHANGELOG — short-text-deconstructor
## v1.1.0 | 2026-08-13
### skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
- skill.json：description 改为面向用户介绍、tags 改为可调用专家标签
- 版本号同步至 v1.1.0

## v1.0.0 | 2026-08-04
### 新建 skill：拆文分析器（Popwave规范改造）
- 初始版本。按Popwave Skill设计规范完整重构
- SKILL.md 压缩至约90行，含YAML frontmatter、SOP骨架表（7步）、4种拆解深度、红线、速查表、版本
- 拆分执行步骤至 steps/：step0-choose-depth、step1-structure、step2-character、step3-opening、step4-style、step5-evaluation、step6-impact
- 创建 templates/deconstruct-report.tpl.md：拆解报告模板，含结构/角色/开篇/文风/评价/影响
- 4种拆解深度选项，按需跳过无关步骤
- 拆解结论标注对后续6个Steps的影响信号
- 补全 skill.json：tags=["短篇创作","拆文分析"]、author="popwave"、license="UNLICENSED"
