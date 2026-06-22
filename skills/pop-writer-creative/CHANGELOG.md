# CHANGELOG — pop-writer-creative

## v4.4.0 (2026-06-22)

### 对齐 pop-shared-skill-create v5.0 标准 + trope-library 集成

**SKILL.md 重写**：
- 新增读取协议作为 ❌1 红线（禁止 Read 工具，用 skill_view 或 Get-Content -Encoding UTF8 -Raw）
- 新增速查表（完整目录引导）— steps/ 2文件 + references/ 2文件 + 外部依赖 3文件
- 版本历史从 SKILL.md 头部移至本文件（原 20 行版本注释 → 1 行版本戳）
- 红线 3 和 7 合并为一条（原 7 条 → 7 条，但去掉了重复的 L1 施工细节红线）
- 新增 trope-library 查询引导（Step 2 前查询套路库/00-总索引 + 元爽点-变体映射表）

**新增 CHANGELOG.md**：承接 v3.5.0→v4.3.0 的历史版本记录

**删除 `references/管线接口格式.md`**：管线 PRD 文档格式约定不属于 creative skill 职责，属于 pop-shared-skill-create 或 PRD 自身

**step-r.md**：新增读取协议头部

**step-prd.md**：
- 新增读取协议头部
- Step 2 新增 trope-library 查询步骤（查询套路库/00-总索引 + 元爽点-变体映射表，按调用匹配SOP 三维查询）
- 修复第 518 行废弃路径引用（`创意种子/层架构.md` → 删除）

**新增 `references/搜索SOP.md`**：联网搜索操作标准 — 关键词提取规则（从特征参数表提取）、三路搜索路径（A≥5本/B≥3个/C≥3种）、搜索结果沉淀格式、迭代搜索策略（最大2轮）、质量自检清单。step-prd.md §2.1 从内联描述改为引用 SOP。

**references/ vs templates/ 目录分离**：模板文件（`prd-模板-空白.md`、`prd-模板-魔门.md`）从 references/ 移到 templates/。references/ 只保留 SOP/规范类文件（`搜索SOP.md`）。

**新增 `templates/故事概念选项-模板.md`**：故事概念选项的质量标准+吸引力设计+差异化矩阵。解决"给出来的故事太low，这个阶段就劝退用户"的问题。包含：好vs Low对照表、选项差异化矩阵（强制≥2维度不同）、增强版选项格式模板（一句话钩子+吃人规则+金手指代价设计）、吸引力设计技巧（5种钩子公式+代价戏剧性分级）、质量自检清单。step-prd.md §2.2 从内联格式改为引用模板。

**step-prd.md 拆分**：7类爽点追问链+元模板（97行）下沉到 `references/爽点追问链.md`，step-prd.md 从 376→306 行。剩余内容为 9 个 Step 的执行流程，保持连贯性不再拆分。

**step-prd.md 按 Step 3 用户断点拆为两个文件**：
- `steps/step-prd-research.md`（Step 1-2）— 研究+生成选项，产出故事概念选项，以用户断点结束
- `steps/step-prd-derive.md`（Step 3-9）— 锁定概念后推导 PRD 全部内容
- 拆分理由：Step 3 用户选择是天然分水岭，前面是 agent 主导的研究阶段，后面是基于用户选择的推导阶段，彼此独立。拆分后 agent 走完 research 自然暂停等用户，不需要在长文件里记住"到 Step 3 停下来"

**skill.json**：修正 description（v4.2.0→v4.4.0，PRD.md→全书立项PRD.md），新增 references 字段

---

## v4.3.0 (2026-06-20)

- PRD 产出文件名统一为 `全书立项PRD.md`，不再放在 `创意种子/` 子目录
- reference 从 5 个精简为 2 个（`prd-模板-空白.md` + `prd-模板-魔门.md`），删除与 PRD 推导无关的 pitfalls/layer-architecture/缺口分析
- 红线 3+7 修正——PRD 可写核心创意命名，不可写 L1 施工细节
- 管线 PRD 同步更新（creative v4.2.0→v4.3.0，文件级接口表格式，四环节分组）

## v4.1.0

- PRD 宪法结构最终定型——本书剧情简述(~200字梗概) → 篇幅规划 → 爽点锚点(含L1-L4特征参数) → 核心卖点(≥5条) → 美学基因推导链 → 世界宪法 → 核心承诺+防崩阈值 → DNA+边界 → 加工矩阵(可选) → 跨域素材指引 → 用户画像

## v4.0.0

- PRD 移除加工矩阵/层架构/材料选择，改为宪法层结构

## v3.6.0

- Phase 2 自问链 + 场景判定 R/M/O + 元模板——消除「分类代替分析」

## v3.5.0

- 职责收窄——只做 PRD 推导。素材采集/注入/样品试读/Phase Delta 全部移除
