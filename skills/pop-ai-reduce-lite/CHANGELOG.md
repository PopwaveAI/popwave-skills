# CHANGELOG — pop-ai-reduce-lite

## v4.0.0 | 2026-09-02

### 整包替换为 @user_741dc82b/libai（李白.Skill:润色专家 v2.0）

> **根因**：对比评测后老板拍板——第三方李白.Skill 的检测（实测 AI 含量%+7维诊断）+改写（四步排雷+破式五层）能力全面强于自研 lite 的表层规则降噪。与其在自研浅层上补检测短板，不如整包采用成熟引擎。但维持"非 snow 默认流程"定位不动。

**改动**：
- **实现整包替换**：pop-ai-reduce-lite 目录清空旧实现，铺入 libai 全部内容（SKILL.md / README / QUICKSTART / faq / resources 规则库 / scripts Python 检测改写引擎）
- **去掉两级闸门**：删除原「表层降噪→表层后询问→路由 pop-ai-reduce 深度18技法」链路，改为李白一次到位（A 专业报告 / B 轻量 / C 仅诊断 三模式交付）
- **skill.json 重写**：id 与中文触发词（降AI/去AI味/降朱雀/润色）保留；version 3.0.0→4.0.0
- **SKILL.md frontmatter**：name 由 libai-skill 改为 pop-ai-reduce-lite，triggers 保留李白全集并补「降朱雀」；正文保留李白原版流程不变
- **脚本运行时**：由 Node(.mjs) 切换为李白的 Python(detect.py/rewrite.py) 引擎；依赖 Python ≥3.8（本机 3.10 可用）
- **旧实现已备份**：`temp/backup_pop-ai-reduce-lite_20260902_170039/`（project-source + runtime-copy 双份）

---

## v3.1.0 | 2026-08-31

### 去AI味
- 「交互闭环」改为「在同一流程内完成」，去空洞名词
- 同步 skill.json（version）

---

## v3.0.0 | 2026-08-24

### steps 单件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层）。参考 write/pipeline 改造模式合入主文档。

**改动**：
- **steps/ 目录删除**：pipeline-execute.md 全文合入 SKILL.md「四步执行管线」节（Step 1-4 执行细节+词表+示例全保留）
- **执行模式明确**：主agent直执——单章4步改写+脚本验证+表层后询问用户是同一交互闭环，无自然子agent适配点
- **内容精炼**：字数保留率回查规则收敛进红线❌5（补上step文件中"重点查Step 1/Step 4过度删除"的指向）；速查表三条全部并入「输出与验证」节正文（去独立表）；加载门禁节随链式加载架构废除删除；表层后询问模板压缩（提醒两点+选项保留）
- skill.json version 2.4.0→3.0.0

---

> 历史版本条目已归档：`temp/backup_pop-ai-reduce-lite_20260902_170039/project-source/CHANGELOG.md`