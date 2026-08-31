# CHANGELOG — short-opening-designer

## v2.1.0 | 2026-08-31

### 去AI味 + 文档瘦身
- SKILL.md 版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 同步 skill.json（version）

---

## v2.0.0 — 2026-08-24

### steps 5件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1-sell-point / step2-choose-formula / step3-golden-three / step4-full-opener / step5-pay-hook 五件全合入 SKILL.md 对应节
- **执行模式明确**：主agent直执——连续创作链（脑洞→导语→结构）的交互确认环节（卖点主轴/黄金三句/导语逐关与用户确认），无自然子agent适配点
- **内容精炼**：6种导语公式压缩为单表（结构+平台适配）+平台优先序一行；付费钩子位置4平台压缩为一段文字+钩子类型表；开篇卡片/流转上下文/钩子策略三格式由代码块压为要点行；逐关门禁（主轴确认前不进Step2/三句确认前不进Step4/导语确定前不进Step5）与5条红线全保留
- skill.json version 1.1.0→2.0.0

---

## v1.1.0 | 2026-08-13
### skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
- skill.json：description 改为面向用户介绍、tags 改为可调用专家标签
- 版本号同步至 v1.1.0

## v1.0.0 | 2026-08-04
### 新建 skill：短篇开篇设计器
- 初始版本。6种导语公式（悬念前置/情绪爆发/对话开头/身份共鸣/反转/画面切入）
- Step 1 确定卖点主轴，2-3个候选标注优先级
- Step 2 平台×卖点自动匹配导语公式
- Step 3 三要素法生成2-3组黄金三句
- Step 4 补完整导语，100-200字约束+3大禁忌
- Step 5 4种付费钩子类型+平台差异化位置
- 按Popwave Skill设计规范重构：SKILL.md压缩至48行，执行细节拆分至steps/
- 5条红线，导语不是正文第一句
- 模板 `opening-card.tpl.md` 含6个区块+流转上下文
