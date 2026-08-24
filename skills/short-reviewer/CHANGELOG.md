# CHANGELOG — short-reviewer
## v2.0.0 — 2026-08-24

### steps 三件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1-load / step2-diagnose / step3-report 三件全合入 SKILL.md 对应 SOP 节
- **执行模式明确**：正文通读+9维诊断是典型只读审查工作，可派子agent（审查官）执行——按方案B临时落盘报告回元数据，主agent校验归位；需用户交互的评审范围确认/流转确认主agent直执
- **内容精炼**：9维评分框架表与 step2 分维检查点合并为单表（维度/对标/诊断检查点）；step2 对标模式（仿写场景差距列+🔴门禁+差距汇总表）与诊断流程（7.0+通过线+问题必配建议）全内联；step3 报告结构六件套全内联；SOP 骨架表改逐步节；速查表清 3 行 steps 引用
- skill.json version 1.1.0→2.0.0

---

## v1.1.0 | 2026-08-13
### skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
- skill.json：description 改为面向用户介绍、tags 改为可调用专家标签
- 版本号同步至 v1.1.0

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
