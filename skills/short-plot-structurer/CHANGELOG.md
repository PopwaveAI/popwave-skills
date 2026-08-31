# CHANGELOG — short-plot-structurer

## v2.1.0 | 2026-08-31

### 去AI味 + 文档瘦身
- SKILL.md 版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 同步 skill.json（version）

---

## v2.0.0 — 2026-08-24

### steps 4件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1-select-template / step2-arc-design / step3-character-design / step4-output-card 四件全合入 SKILL.md 对应节
- **执行模式明确**：主agent直执——连续创作链（脑洞→导语→结构）的交互确认环节（模板选定/弧线确认/角色清单逐关与用户确认），无自然子agent适配点
- **内容精炼**：原「4种结构模板」概要表与 Step 1 平台匹配表+结构框架合并去重；剧情动作差异化三规则与角色密度合并检查全内联；骨架卡片/流转上下文格式由代码块压为要点行；完整性自检表保留；5条红线全保留
- skill.json version 1.1.0→2.0.0

---

## v1.1.0 | 2026-08-13
### skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
- skill.json：description 改为面向用户介绍、tags 改为可调用专家标签
- 版本号同步至 v1.1.0

## v1.0.0 | 2026-08-04
### 新建 skill：短篇剧情结构器
- 初始版本。4种结构模板（知乎反转体/番茄单元剧体/经典三幕式/情绪爆发体）
- Step 1 平台×题材×卖点自动推荐结构模板
- Step 2 剧情弧线设计，按免费/付费分段+情绪走向+钩子嵌入
- Step 3 角色设计（≤5人），主角四维+配角功能分类，角色服务于剧情
- Step 4 输出骨架卡片+流转上下文
- 按Popwave Skill设计规范重构：SKILL.md压缩至50行，执行细节拆分至steps/
- 5条红线，角色上限+功能合并为核心约束
- 模板 `skeleton-card.tpl.md` 含6个区块+弧线循环表+流转上下文
