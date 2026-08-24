# CHANGELOG

## v2.0.0 | 2026-08-24

### steps 两件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：step1-collect / step2-adapt 两件全部合入 SKILL.md 对应节——Step 1（前置门禁+X确认+强度选择+冲突拍板+落盘）、Step 2（DNA替换矩阵+DNA替换三问+剧情类比切换策略+X体验层+直写PRD+改编继承表模板+落盘验收）
- **执行模式明确**：主agent直执——强度选择/冲突拍板必须用户交互；改编计划是全管线改编指令源，X耦合度与验收密度高，不派子agent
- **内容精炼**：强度三档表并入"适合场景"列（原SKILL与step1两表合一）；DNA替换矩阵/继承表模板/验收口径全保留；SOP指针与速查表steps行删除
- **修复死链**：原速查表引用 `templates/素材/改编计划.tpl.md` 实际不存在，改编计划格式已内联Step 2
- skill.json version 1.0.0→2.0.0

---

## v1.0.0 | 2026-08-16

- **取代 test-seed v14.0.0**：从「仿写·硬对齐」升级为「改编·DNA替换」
- 新增：改编强度A/B/C选择门禁、`素材/改编计划.md`（X DNA替换矩阵+剧情类比切换策略+X体验层）、改编继承表
- 保留：六要素立项PRD、包配方质量锚、偏离声明机制
- skill.json version 14.0.0→1.0.0（新skill，test-seed并入删除）
