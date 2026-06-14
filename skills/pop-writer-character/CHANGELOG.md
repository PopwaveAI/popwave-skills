# CHANGELOG — 04-pop-novel-character-schema

## v2.0.1 (2026-06-14)

### v5 结构重构：精简 SKILL.md + 目录规范化 + pipeline 对齐

- **SKILL.md 精简至 ≤150 行**：移除方法论内容（维度递增体系、每级设计目的 & 叙事能力）至 `references/level-selection-methodology.md`
- **目录重命名**：删除重复的 `schema/` 目录（内容已存在于 `references/`），模板路径统一为 `references/`
- **steps/ 规范化**：step-2-fill-core.md → step-2-write-card.md，step-3-validate.md → step-3-verify.md；各 step 文件包含来自 SKILL.md 的真实内容
- **新增落盘检查点**：`## 落盘检查点` 表，定义 5 项产出校验标准
- **skill.json 更新**：新增 `pipeline` 字段，版本升至 v2.0.1
- **版本号对齐**：SKILL.md 版本行更新为 v2.0.1 → CHANGELOG.md

---

## v2.0.0 (2026-06-11)

### 重大重构：重新编号 + 维度对齐 + 设计目的 & 能力

- **编号纠正**：按认知常识重新编号
  - 旧 Lv4（一次性）→ 新 Lv1（路人/一次性）
  - 旧 Lv3（功能角色）→ 新 Lv2（功能角色）
  - 旧 Lv2（重要配角）→ 新 Lv3（重要配角）
  - 旧 Lv1（主角/核心对立）→ 新 Lv4（主角/核心对立）
- **维度对齐**：每级 = 上一级全部维度 + 本级新增，严格做加法
  - 新增「维度矩阵一览」表，一表看全四级继承关系
- **每级新增「设计目的」+「叙事能力」**：Lv1~Lv4 每级角色卡必须声明设计的意图和能力边界
- **SKILL.md**：符合 pop-skill-create 规范（质量红线第一屏、WRONG 错误示例、异常边界条件表）
- **schema 模板文件名同步更新**：`Lv1-one-shot.md` / `Lv2-functional.md` / `Lv3-important.md` / `Lv4-core.md`
- **各模板新增升级标注**：每个维度标注 `← LvN 升级` / `← 新增` / `← LvN 继承`，溯源清晰

---

## v1.0.0 (2026-06-10)

- **首次发布**：角色卡分级标准定义
- **Lv1 主角模板**：6 维全量（身份/心理/驱力/能力/演化/网络）
- **Lv2 重要配角模板**：4 维（身份/心理·驱力/叙事功能/弧线）
- **Lv3 功能角色模板**：3 维（身份/标签/驱动·功能）
- **Lv4 一次性角色模板**：1 维（一句话摘要）
- **references/character-arc.md**：弧线设计指南
- **跨赛道复用**：模板使用通用写作术语，不绑定特定题材
- **定位**：轻量标准定义 Skill，对标 03-pop-dna
