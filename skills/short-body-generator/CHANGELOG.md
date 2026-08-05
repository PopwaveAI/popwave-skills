# CHANGELOG — short-body-generator
## v1.0.0 | 2026-08-04
### 新建 skill：短篇正文生成器（Popwave规范改造）
- 初始版本。按Popwave Skill设计规范完整重构
- SKILL.md 压缩至约80行，含YAML frontmatter、SOP骨架表、红线、速查表、版本
- 拆分执行步骤至 steps/：step1-style-select、step2-generate-segment、step3-pay-hook、step4-deai-check
- 5A文风选择：5种平台文风自动匹配+用户参考文本最高优先
- 5B-5D逐段生成：逐段确认/一键全文双模式+每段自检5项
- 5E付费钩子控制：断点位置+类型+驱动力三级强度检查
- 5F去AI味儿：5类AI痕迹识别+逐段扫描+修改方向建议
- 补全 skill.json：tags=["短篇创作","正文生成"]、author="popwave"、license="UNLICENSED"
- 不需 templates/（正文是直接产出，无固定模板格式）
