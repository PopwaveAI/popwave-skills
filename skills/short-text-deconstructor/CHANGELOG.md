# CHANGELOG — short-text-deconstructor

## v2.1.0 | 2026-08-31

### 去AI味 + 文档瘦身
- SKILL.md 版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 同步 skill.json（version）

---
## v2.0.0 — 2026-08-24

### steps 七件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step0-choose-depth / step1-structure / step2-character / step3-opening / step4-style / step5-evaluation / step6-impact 七件全合入 SKILL.md 对应 SOP 节
- **执行模式明确**：例文读取+各模块分析是只读工作，可派子agent执行——按方案B临时落盘报告回元数据，主agent校验归位；Step 0 拆解深度选择需用户交互确认，主agent直执
- **内容精炼**：既有"四种拆解深度"表与 step0 执行路由表合并为单表（选项/输出模块/执行步骤/适用场景）；既有"对后续Steps的影响"表并入 step6 的"应用方式"列合并为一张三列表；Step 1-5 各模块执行要点（平台判断依据/6模板+4套路/主角三公式/黄金三句表/文风画像六特征抽取法/评价定位）全内联；速查表清 7 行 steps 引用并补 golden-three.md 行
- skill.json version 1.1.0→2.0.0

---

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
