# CHANGELOG — pop-html-anything

> 版本规则：主版本.次版本.修订号
> 每次调优产生一个新版本号

---

## v2.5.0 (2026-06-14)

**根因**: SKILL.md 膨胀至 592 行，所有 SOP 流程、设计方法论、异常处理全部挤在一个文件中，维护困难
**类型**: architecture
**改动**: Tier C v5 结构重构：
- 新建 `steps/` 目录，8 个 SOP 步骤文件（phase-0 到 step-06）拆分自主流程
- `_design/` → `references/design/`，`_tooling/` → `references/tooling/`
- 新建 `references/` 补充文件：output-spec / input-spec / templates / responsibility / wrong-examples / errors
- SKILL.md 从 592 行瘦身至 137 行，红线改为 `| # | 红线 |` 表格，新增 Drop Check 前置闸门
- `skill.json` 新增 `pipeline` 字段（role: render），版本升至 2.5.0，依赖路径更新
**效果**: 结构清晰，逻辑分离，SKILL.md 只做索引和红线声明，具体执行指向 steps/

---

## v2.4.0 (2026-05-31)

**根因**: 配图规划是"思考决定"模式 → LLM 在 Phase 0 认为"不需要"跳过配图
**类型**: prompt
**改动**: Step 4.5 执行步骤改为从 YAML 读取上游预写 image_prompt 直接生图，不再自行构思 prompt
**效果**: 角色肖像和名场面配图使用 pop-reader-making 拆书时产出的预写 prompt，质量更高

---

## v2.3.0 (2026-05-31)

**根因**: 配图规划写的是"思考决定"→ LLM 自我说服后跳过配图，3 卷 HTML 无配图
**类型**: architecture
**改动**: Phase 0.2.5 从"思考决定"改为"硬性触发规则"——有角色必须配肖像、有场景必须配插图、有 Hero 必须配背景；Step 4.5 新增 5 条铁律（数量达标/脚本生图/就地处理/必须嵌入/规划锁死）；质量门禁新增 6 条红色铁律检查
**效果**: LLM 不再有"我觉得不需要"的选项，配图从可选变强制

---

## v2.2.0 (2026-05-31)

**根因**: 输出 HTML 设计过于简单，缺少专业排版技巧和交互功能
**类型**: knowledge
**改动**: 融合《单文件HTML工程化改造方法论》实战经验——配色温度三步法（定温度→选点缀→收饱和）、三层叠图 Hero CSS 模板、长文阅读器骨架 D、内容互联组件模式、反模式质量门禁
**效果**: HTML 输出具备专业前端工程水准

---

## v2.1.0 (2026-05-31)

**根因**: 开发过程中改成了内部 `_design/` 目录，但 Skill 仍引用旧 shared-html-design 路径；上游给素材后 LLM 没有固定脚本调用生图
**类型**: architecture
**改动**: shared-html-design 合并入本 skill 的 `_design/` 目录；新增 `scripts/generate_image.py`（从 pop-book-promo 剥离核心生图能力）；Step 4.5 改为"执行阶段"不再讨论"要不要配"
**效果**: 资源完全自包含；LLM 可直接调 `python3 scripts/generate_image.py` 生图

---

## v2.0.0 (2026-05-31)

**根因**: 旧版是哲学驱动，每个模板各自为政，视觉质量不稳定；shared-html-design 是独立 skill 但引用关系混乱
**类型**: architecture
**改动**: 彻底重构——从"每页艺术品"改为"稳定的好看"；新增 Phase 0 设计简报前置；新增 `_design/DESIGN_CORE.md` / `components.md` / `responsive.md` 设计系统；确立唯一 HTML 渲染引擎定位
**效果**: 统一视觉体系，保底 75 分

---

## v0.2.0 (2026-05-30)

初始版本。仅有设计哲学（5 种视觉方向），无设计系统管线。
