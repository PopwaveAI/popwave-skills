# CHANGELOG — pop-writer-creative

## v6.2.0 (2026-06-25)

### P2优化：金手指行动引擎检查

- **SKILL.md**：新增红线❌5——金手指设计必须含≥1个行动驱动机制（任务/技能/经验/血量/战宠）
- 若金手指只有"观察/标注"功能→标注风险并提示用户

## v6.0.0 (2026-06-24)

### 大改：合并 reservoir → 种子展开法 → 深度调研前置 → 三调用模式

**核心理念**：海明威冰山原则——深度调研是水下的八分之七，PRD 是水面的八分之一。没收集够信息不该开 PRD。

**架构变更**：8 阶段管线 → 7 阶段管线（creative 吸收 reservoir）

**新增文件**：
- `references/种子展开法.md`（~300行）— 5阶段系统调研：种子识别→直接研究→切向扩展（5辐射路径）→深度域研究→交叉授粉。替代域研究SOP
- `references/深度域研究SOP.md` — 从 reservoir 采风SOP 移入，四层穿透(L1-L4)+域DNA档案
- `references/四层转化模型.md` — 从 reservoir 移入
- `references/安全门禁.md` — 从 reservoir 移入
- `references/权重矩阵.md` — 从 reservoir 移入
- `steps/step-reserve.md` — 全新，合并 reservoir 的 step-inject-collect + step-inject-archive
- `templates/剧情储备卡-模板.md` — 从 reservoir 移入
- `templates/设定储备卡-模板.md` — 从 reservoir 移入
- `templates/materials-pool.tpl.md` — 从 reservoir 移入

**重写文件**：
- `SKILL.md`：v5.0.0→v6.0.0，新增三调用模式（新书/素材注入/主动丰富），Phase R→1→2→3 四阶段
- `steps/step-prd-research.md` → `steps/step-research.md`：重命名+大改，Step 2 从浅层域研究升级为种子展开法全流程
- `steps/step-prd-derive.md`：Step 6 从"域研究委托"升级为"研究档案引用"，末尾交接 step-reserve.md
- `steps/step-r.md`：新增 Mode 2/3 路由
- `references/碰撞引擎.md`：更新四层转化对接引用
- `skill.json`：v5.0.0→v6.0.0
- `templates/prd-模板-空白.md`：第九块从"域研究委托"升级为"域DNA档案引用"

**删除文件**：
- `references/域研究SOP.md`（被种子展开法替代）
- `steps/step-prd-research.md`（重命名为 step-research.md）
- 整个 `pop-writer-reservoir/` 目录（能力已被 creative 吸收）

## v5.0.0 (2026-06-23)

### 大幅强化：域碰撞引擎 + 域研究SOP + PRD第九块升级

**核心问题**：v4.4.0 的"碰撞"实为参数匹配（A参数+B参数=拼凑），不是创意碰撞（A的DNA×B的DNA=新东西）。搜索是浅层三路关键词匹配，无"域"概念。对比武林半侠传（115条创意溯源、5参考域、4层融合结构）差距巨大。

**新增4个核心方法论文件**：
- `references/碰撞引擎.md`（254行）— 6步碰撞工作流（域识别→域DNA提取→焊接点发现→叙事语法判定→跨域联动设计→碰撞产出）+ 5种碰撞模式（颠覆性重构/概念跨界/三重融合/系统化重组/叙事语法嫁接）+ 5维质量评估（S/A/B/C分级）
- `references/域研究SOP.md`（151行）— 浅层域研究标准，替代三路搜索。域识别（R/M/O场景）→ 四维DNA浅层提取（叙事语法/核心机制/美学基因/经典元素）→ trope-library对接 → 域DNA摘要
- （reservoir侧）`references/四层转化模型.md`（224行）+ `references/采风SOP.md`（249行）

**step文件修改**：
- `step-prd-research.md`：Step 2.0新增立项库查询；Step 2.1从三路搜索升级为域研究（引用域研究SOP）；Step 2.2从参数匹配升级为域碰撞（引用碰撞引擎）；新增Phase 2a+域识别
- `step-prd-derive.md`：Step 6升级为"域研究委托+叙事语法声明"（给reservoir采风方向）；Step 8 PRD第九块从"跨域素材指引"升级为"域研究委托+叙事语法声明"；Step 9新增3项碰撞质量检查

**模板修改**：
- `templates/故事概念选项-模板.md`：新增"域碰撞设计"段（域清单/叙事语法声明/素材贡献表/跨域联动清单/原创空间）+ 2项质量检查（域碰撞设计/碰撞非缝合）
- `templates/prd-模板-空白.md`：第九块从"跨域素材指引"升级为"域研究委托+叙事语法声明"（3子节：叙事语法声明/域研究委托/碰撞方案摘要）

**SKILL.md + skill.json**：
- 版本 4.4.0→5.0.0；displayName "创意打磨"→"创意碰撞引擎"
- references表新增碰撞引擎.md和域研究SOP.md为⛔必读；搜索SOP.md标注deprecated
- 路由更新：域识别→域研究→碰撞合成→域研究委托

**旧SOP标注deprecated**：`references/搜索SOP.md` 标注 DEPRECATED，由域研究SOP替代

**设计源头**：武林半侠传创意溯源（115条/5域/4层融合结构）→ 提炼出"叙事语法=操作系统"核心洞察 → 产品化为域DNA四维模型+碰撞引擎+四层转化模型

---

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
