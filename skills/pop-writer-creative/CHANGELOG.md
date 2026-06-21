# CHANGELOG — pop-writer-creative

## v3.5.0 — 2026-06-20

### 职责收窄 + 文件清理

- **砍掉素材采集**（W0/W0.5/W1/W2）、**素材储备池**、**样品试读**、**Phase Delta**、**主角设计/参考书策略**
- **删除 22 个遗产文件**：14 step（含 PE 并行版）、6 reference、2 template
- **step-r.md → 重构**：128 行 → 30 行，废除 A/B/C 三分支，只做输入粒度→搜索宽度路由
- **SKILL.md**：691 行 → 55 行，三板块（速查表/WRONG/红线）合并为 4 条红线
- **保留**：step-prd.md（v4 PRD 推导引擎）、step-r.md（路由）、layer-architecture-guide.md、prd-pitfalls.md

### creative 的新职责

用户给模糊想法 → agent 搜索生成选项 → 用户选 → 产出 PRD.md → 交付 world。只做这一件事。

### PRD 推导升级为 agent 研究提案模式

- **step-prd.md → v4「agent 研究提案，用户选择」**：用户给模糊想法 → agent 联网搜索 + 公共数据库 → 生成 2-3 个故事概念选项 → 用户选择 → 锁定推导
- **链路大幅缩短**：用户只需回答 ≤3 个关键问题。agent 负责研究、提案、推导
- **废除 A/B/C 三分支**：无论用户是清晰想法、碎片灵感还是一张白纸，统一走 agent 研究提案模式。区别只在搜索面的宽窄
- **新增故事概念选项格式**：每个选项含 一句话定位 / 世界观结构 / 核心冲突模式 / 金手指方向 / 对标参考
- **搜索定位从「辅助」变为「驱动」**：不是补充背景知识——搜索结果直接生成选项

### 相关文件更新

- `steps/step-prd.md` — 完全重写为 v4（8 步 agent 研究提案流程）
- `SKILL.md` — 版本 3.4.0，路由图简化，废除三分支表
- `skill.json` — 版本 3.4.0，描述更新

## v3.3.0 — 2026-06-20

### 爽点引擎 + 故事引擎合入 PRD

- PRD 成为唯一立项宪法。无独立爽点引擎.md 或故事引擎.md
- 爽点 Q&A 内化为 PRD 推导 Step 1；宪法约束通过核心承诺防崩 + DNA 实现
- step-prd.md 升级为 v3「对话推导指南」（10 步流程）
- 全书色彩采用「基因推演」逻辑

## v3.2.0 — 2026-06-20

### PRD 升级为 v2「创作宪法」

- 从 7 维产品需求文档升级为 9 维创作宪法
- 新增「篇幅规划」「全书色彩」维度
- 「加工哲学」升级为「加工矩阵」（5 维决策表）
- 「核心承诺」强制回引爽点引擎 + 防崩机制

## v3.0.0 — 2026-06-18

### 新增 Phase 爽点引擎（已合入 v3.3.0）

- 在 Phase R 之后、PRD 之前，通过 Q&A 确定本书 2-3 个主元爽点
- 元爽点 = 爽的基本粒子（信息差/阶级革命/绝境反杀/身份跃迁/世界观震撼/智斗博弈/情感羁绊）
- 解决「方向正确的废话」——让 PRD 从「是什么」变成「怎么让读者停不下来」

## v2.1.0 — 2026-06-18

### Phase Delta 重构
- creative 触发 + reservoir 执行的双长架构
- creative 仅负责最终判定（D1/D2/D3）

## v2.0.1 — 2026-06-17

### 修复 Phase Delta 前置检查

### 核心重构：路由机制 + 双产出模型 + 独立调起

- **新增 Phase R 路由诊断**：按用户启动状态走三分支。A: PRD先行（清晰想法）→ 定向采集；B: 广度采集 → PRD浮现（碎片灵感）；C: 方向碰撞 → PRD提炼（空白）
- **新增 Phase Delta 独立调起**：项目中后期注入新元素（热点/IP/新灵感）时执行轻量级注入诊断。三步：PRD契合度评估 → 宪法冲突检测 → 素材储备池追加。不重跑全流程
- **新增双产出模型**：产出物从单一「故事引擎」拆为「故事引擎.md（宪法约束）+ 素材储备池.md（剧情种子）」两件套。素材储备池按主线索材/支线索材/背景素材/剩余焊接点四类归档，供 plot 消费
- **PRD 独立为前置/中置阶段**：PRD 从故事引擎的隐藏部分提前为独立产出（PRD.md），A分支在素材前、B分支在素材后、C分支在方向选定后
- **故事引擎模板新增「〇、基本法」章节**：对接 PRD.md，作为引擎的宪法基线

### 新增文件

- `steps/step-r.md` — 路由诊断（三分支决策矩阵 + 追问策略 + 调用模式识别）
- `steps/step-prd.md` — PRD 撰写指导（三种模式 + 微调模式）
- `steps/step-delta.md` — 新元素注入流程（PRD契合度 + 宪法冲突 + D1/D2/D3 三等级）（★ NEW）
- `templates/materials-pool.tpl.md` — 素材储备池模板（四类分类 + PRD反审记录 + Delta 注入段落）

### 更新文件

- `SKILL.md` — 完整重写：路由总图（含模式2独立调起）+ 三分支流程 + Phase Delta + 双产出模型 + 新增红线 x4 + Delta 红线 x5
- `steps/step-r.md` — 新增调用模式识别（Delta vs 管线入口）+ 三分支诊断
- `steps/step-w0.md` — 分支感知：PRD筛选检索 vs 广度检索
- `steps/step-w1.md` — 拆分 Part A 跨域素材采集 + Part B 拆书融合，均分支感知
- `steps/step-prd.md` — 新增模式 D（Phase Delta PRD 微调）
- `templates/story-engine.tpl.md` — 新增「〇、基本法」章节对接 PRD.md
- `skill.json` — v2.0.0 版本 + 描述更新 + downstream 新增 pop-writer-plot + 新增 activation 关键词

### 新增红线

| # | 红线 |
|:-:|:-----|
| ❌1 | Phase R 不可跳过 |
| ❌3 | PRD 不可跳过 |
| ❌4 | 素材储备池不可跳过 |
| ❌12 | 素材储备池不分类直接堆 |
| ❌D1 | Delta：不读项目已有产出就评估 |
| ❌D2 | Delta：不擅自修订宪法 |
| ❌D3 | Delta：冲突时不沉默吞入 |
| ❌D4 | Delta：注入不写储备池 |
| ❌D5 | Delta：重复注入同一元素 |

### 重新编号

红线从 10 条扩展为 12 条（原 ❌1-10 保留，❌2/W0 保留，新增 ❌1/R ❌3/PRD ❌4/池 ❌12/分类）+ Delta 5 条（❌D1-D5）

## v1.4.1 — 2026-06-14

- v5 structural refactoring: added WRONG examples table (3 entries), templates/ directory with story-engine.tpl.md, step files for W0/W1/Phase0/0.3/0.4/0.5, steps references in SKILL.md, pipeline field in skill.json.

## v1.4.0 — 2026-06-12

### 数据采集层回流 + 前置
- Phase W0（跨域素材聚合）和 Phase W1（拆书融合）从 06-pop-novel-world 移回 creative
- **关键变化：W0/W1 放在 Phase 0 元素融合之前** — 先采集燃料，再碰撞创意
- 核心哲学：没有足够的跨域素材和拆书数据，碰撞不出好方向。后面一切都是空谈
- W0 始终强制（HARD GATE），W1 有对标书时强制
- 交接包扩充：跨域素材蒸馏.md + 拆书融合摘要.md 纳入移交 world 的文件
- 质量红线新增 ❌0：跨域素材不得跳过

### world 联动
- world v1.2.0: 移除 W0/W1，简化管线为 Phase 1-6（L1→稳定性→角色→数值→起点→宪法）
- world 从 creative 接收已完成的数据产物，不再自己做采集

---

## v1.3.0 — 2026-06-12

### 剥离数据采集层 → world
- Phase 0.6（跨域素材）和 Phase 0.7（拆书融合）移至 06-pop-novel-world 的 Phase W0/W1
- creative 在样品签字后使命完成——不负责采集 world 用的数据
- 交接包精简为：故事引擎.md + 样品签字 + 主角设计笔记 + 参考书策略
- world 的新增红线：跨域素材始终强制，拆书融合有对标书时强制

---

## v1.2.0 — 2026-06-12

### Phase 0：方向 sketch 轻量化 + yaml 退场
- 方向产出从"三层 heavy brief"改为"轻量 sketch（碰撞+钩子+第一画面+基调，~150字）"
- 用户选完方向后才深化为完整的故事引擎.md（不浪费时间深挖没选的方向）
- **story-engine.yaml 退场** — 全部产出改为 .md 格式，叙事优先、人可读
- 红线 ❌7 从"卖点验证可复述"改为"故事引擎可被十分钟读完"
- 交接包更新：`故事引擎.md` 替代 `story-engine.yaml`

### Phase 0.3：参考书甄别 → 参考书策略
- 定位从"自己做拆书"改为"deconstructor 的策略层"
- 新流程：从碰撞点推导验证需求 → 形成观察清单（映射到 deconstructor T维度）→ 触发 deconstructor Lv1 → 差异化决策 → 反哺宪法
- 产出从 `_参考书分析/{书名}.md` 改为 `观察清单+差异化.md`

### Phase 0.4：金手指设计 → 主角设计
- 金手指降为主角的子维度，不再独立 Phase
- 新增"唯一性"作为第四维（必填）——替代原来的"能力/金手指"
- 唯一性四级评估从"能力评估"改为"主角资格检验"：L1核心差异 / L2约束 / L3不可替代性 / L4叙事驱动
- 任何题材都必走唯一性四级评估。"金手指"只是修真/系统类下唯一性的载体之一

### 其他
- 红线 ❌1: story-engine.yaml v3 → 故事引擎.md
- 红线 ❌5: 金手指四级评估 → 主角四维完整（唯一性必填）
- 下游 world 同步更新所有 yaml→md 引用

---

## v1.1.0 — 2026-06-12

### Phase 0 重构：追问 → 元素融合 SOP
- 从"接住+追问 2-3 轮"改为"碎片分析+元素联想+碰撞评级+方向 brief 生成"
- 新增元素融合 5 步 SOP（解吸→拆规则→找碰撞点→落主角→方向 brief）
- 新增方向 brief 模板（宏观/卖点/微观三层咬合）
- 新增碰撞强度评级（★☆☆弱碰撞 ★★☆中等 ★★★强碰撞）
- story-engine v3 新增 `fusion_method` / `colliding_elements` / `collision_point` 字段
- 用户交互从"被审问"变为"在 2-3 个完整提案中选择"

---

## v1.0.0 — 2026-06-12

### 初始分叉
- 从 pop-novel-bookstrap v4.1.0 分叉
- 剥离 L1 设定层（Phase 1-1.5）→ 移入 06-pop-novel-world
- 剥离数值体系（Phase 3-5）→ 移入 06-pop-novel-world
- 剥离起点/终点快照（Phase 6-7）→ 移入 06-pop-novel-world
- 新增 Phase 0.5 样品试读（核心闸门）
- story-engine 升级至 v3（constitutional_bounds + selling_point_validation）
- 管线位置变更：deconstructor → creative → world
