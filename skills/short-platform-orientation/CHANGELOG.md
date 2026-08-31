# CHANGELOG — short-platform-orientation

## v2.1.0 | 2026-08-31

### 去AI味 + 文档瘦身
- SKILL.md 版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 同步 skill.json（version）

---

## v2.0.0 — 2026-08-24

### steps 三件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1-survey / step2-match / step3-output 三件全合入 SKILL.md 对应节（Step 1-3）
- **执行模式明确**：主agent直执——全程与作者问答交互（摸底→匹配→定位确认），无自然子agent适配点
- **内容精炼**：摸底跳过条件三情形压缩为要点；Step 2 八维度整理为单段要点列表（8维度对比表格式说明保留）；平台×性质冲突警告去重（原SKILL.md与step3重复表述合一）；速查表清 steps 引用
- **版本漂移修复**：SKILL.md 已于 v1.2.0 更新（项目总览改由主agent创建）但 skill.json 滞留 1.1.0 未同步，本次一并归位
- references/（platform-rules.md / genre-guide.md）与 templates/（platform-card.tpl.md）保持外部文件不变
- skill.json version 1.1.0→2.0.0

---

## v1.1.0 | 2026-08-13
### skill.json 的 description 改为面向用户介绍、tags 改为可调用专家标签、版本号同步
- skill.json：description 改为面向用户介绍、tags 改为可调用专家标签
- 版本号同步至 v1.1.0

## v1.0.0 | 2026-08-04
### 新建 skill：短篇平台定位器
- 初始版本。支持6大短篇平台（番茄/知乎/每天读点故事/豆瓣/小程序/七猫）
- Step 1 快速摸底3问，支持跳过条件
- Step 2 平台深度匹配，最多展开2个平台
- Step 3 输出定位卡片+流转上下文
- 按Popwave Skill设计规范重构：SKILL.md压缩至50行，执行细节拆分至steps/
- 4条红线，平台数据以references为准
