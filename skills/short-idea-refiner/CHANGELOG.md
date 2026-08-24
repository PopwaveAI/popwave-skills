# CHANGELOG — short-idea-refiner

## v2.0.0 — 2026-08-24

### steps 3件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1-gather-input / step2-refine-directions / step3-verify-output 三件全合入 SKILL.md 对应节
- **执行模式明确**：主agent直执——连续创作链（脑洞→导语→结构）的对话交互环节（路径判断/方向选择/检验补强全程与用户确认），无自然子agent适配点
- **内容精炼**：原「三条路径」节与 Step 1 路径表合并去重（A/B路径微观步骤全保留在 SOP 内联流程中）；Step 2 热点拉取三级来源/路径B方向菜单/Step 3 三项检验+脑洞卡片+流转上下文格式全内联；门禁（≥2项检验通过才进下一步）与4条红线全保留
- skill.json version 1.1.0→2.0.0

---

## v1.1.0 | 2026-08-13
### skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
- skill.json：description 改为面向用户介绍、tags 改为可调用专家标签
- 版本号同步至 v1.1.0

## v1.0.0 | 2026-08-04
### 新建 skill：短篇脑洞提炼器
- 初始版本。支持3条路径（A有模糊想法/B只有方向/C带例文）
- Step 1 收集输入+路径判断
- Step 2 热点拉取+提炼2-3个脑洞方向
- Step 3 3项检验+补强+输出脑洞卡片
- 按Popwave Skill设计规范重构：SKILL.md压缩至42行，执行细节拆分至steps/
- 4条红线，热点数据仅作参考
- 模板 `idea-card.tpl.md` 含7个区块+流转上下文
