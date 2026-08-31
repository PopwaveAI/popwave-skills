# CHANGELOG — short-body-generator

## v2.1.0 | 2026-08-31

### 去AI味 + 文档瘦身
- SKILL.md 版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 同步 skill.json（version）

---

## v2.0.0 — 2026-08-24

### steps 四件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1-style-select / step2-generate-segment / step3-pay-hook / step4-deai-check 四件全合入 SKILL.md 对应节（5A-5F）
- **执行模式明确**：主agent直执——连续创作链（逐段生成+逐段用户确认+文风全程锚定），无自然子agent适配点
- **内容精炼**：7类AI痕迹"症状/识别/修改方向"三列压为两列；平台推荐表/生成模式表/自检清单并入5A/5B/5D（原骨架与step重复处合一）；红线8条收敛为5条（文风确认+参考优先合并、逐段自检+去AI必走合并、改段规则三条合并，业务约束全保留）
- **死链清理**：速查表原引 `references/structure-guide.md`、`references/golden-three.md`，两文件实际不存在，引用删除
- references/（writing-styles.md / character-card.md / platform-rules.md）保持外部文件不变
- skill.json version 1.1.0→2.0.0

---

## v1.1.0 | 2026-08-13
### skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
- skill.json：description 改为面向用户介绍、tags 改为可调用专家标签
- 版本号同步至 v1.1.0

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
