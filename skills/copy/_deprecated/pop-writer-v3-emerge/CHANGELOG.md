# CHANGELOG

## v2.1.0 — 2026-06-26

### 设定库按需读取 + 路径修正

- **step-1 新增设定库读取**：信息获取步骤新增"1.5 读设定库索引"——检查 `写作资产/设定库/_index.yaml` 是否存在，存在则按 chapter_plan 判断是否需要读力量体系/社会结构/世界宪法/角色档案/卷纲路标
- **step-1 读什么表格更新**：第3项 `种子文档.md` → `种子/`文件夹；第6项 creative `生态调研SOP.md` → v3-seed `种子搜索法SOP.md`（creative已废弃）；新增第7项 设定库索引
- **step-1 info_acquired 新增字段**：setting_lib_read + setting_files_read
- **step-1 产出自检新增**：设定库索引已检查
- **消费方更新**：header 消费项新增 `写作资产/设定库（如有）`

## v2.0.0 — 2026-06-26

### 架构变更：3子agent拆为3独立skill，emerge降为纯调度器

- **emerge降为调度器**：3子agent（创作/修订/质检）从emerge内嵌step拆为3个独立skill（pop-writer-v3-create/revise/qa），emerge降为纯调度器。context隔离从纪律约束变为架构边界（红线❌7改写为"子skill调度context隔离"）
- **Step 2/3/4改为dispatch契约**：step-2-create.md→step-2-dispatch-create.md（调度create子skill）；step-3-revise.md→step-3-dispatch-revise.md（调度revise子skill）；step-4-qa.md→step-4-dispatch-qa.md（调度qa子skill）。每个dispatch step含：输入context组装→调用子skill→输出收集→门禁
- **行为准则贯穿**：create子skill新增行为一致性检查（红线❌2）；revise子skill人设丰富新增行为准则对齐（2.3）；qa子skill新增行为一致性终验维度
- **素材库替代知识库**：所有 `写作资产/知识库/` 路径改为 `素材库/知识沉淀/`；红线❌6从"读 `写作资产/知识库/索引.md`"改为"读 `素材库/索引.md`"
- **搜索深度标准**：emerge step-1新增"4e. 搜索深度标准"（每篇≥500字+具体案例/流程/数据+多轮搜索策略）；信息获取强制化SOP新增"5.4 搜索深度标准"+"5.5 知识沉淀文件字数门禁"
- **无需求门槛提高**：needs:[]需逐类说明理由no_need_reasons（4项未全部填写=退回补填）；连续3章needs:[]→标记信息获取退化预警

### 红线变更

- ❌1 文风DNA缺失：从"修订子agent"→"revise子skill"（措辞更新）
- ❌2 质检不通过：新增"行为一致性终验❌"作为不通过条件之一
- ❌6 信息获取必须读索引：路径从 `写作资产/知识库/索引.md` → `素材库/索引.md`
- ❌7 context隔离：从"3子agent context隔离"→"子skill调度context隔离"（架构边界化）

### 文件变更

| 操作 | 文件 | 说明 |
|:-----|:-----|:-----|
| 删除 | steps/step-2-create.md | 迁移到pop-writer-v3-create/steps/step-1-create.md |
| 删除 | steps/step-3-revise.md | 迁移到pop-writer-v3-revise/steps/step-1-revise.md |
| 删除 | steps/step-4-qa.md | 迁移到pop-writer-v3-qa/steps/step-1-qa.md |
| 新建 | steps/step-2-dispatch-create.md | 调度create子skill的dispatch契约 |
| 新建 | steps/step-3-dispatch-revise.md | 调度revise子skill的dispatch契约 |
| 新建 | steps/step-4-dispatch-qa.md | 调度qa子skill的dispatch契约 |
| 删除 | references/创作指南.md | 迁移到pop-writer-v3-create/references/创作指南.md（+行为一致性检查章节） |
| 删除 | references/修订指南.md | 迁移到pop-writer-v3-revise/references/修订指南.md（+行为准则对齐） |
| 删除 | templates/创作-模板.md | 迁移到pop-writer-v3-create/templates/创作-模板.md（+行为准则确认项） |
| 删除 | templates/修订checklist-模板.md | 迁移到pop-writer-v3-revise/templates/修订checklist-模板.md（+2.3行为准则对齐） |
| 删除 | templates/质检报告-模板.md | 迁移到pop-writer-v3-qa/templates/质检报告-模板.md（+行为一致性终验） |
| 改写 | steps/step-1-info-forced.md | 素材库路径+搜索深度标准+无需求门槛 |
| 改写 | references/信息获取强制化SOP.md | 素材库路径+搜索深度标准+字数门禁 |
| 改写 | templates/信息获取记录-模板.md | 素材库路径+no_need_reasons |
| 改写 | references/活种子生长触发规则.md | 新增行为准则演化生长场景+细化行为准则边界 |

## v1.2.0 — 2026-06-26

### 架构重构

- **调度+3子agent架构**：六步同会话线性 → 主会话调度Step 0-1和Step 5-6；Step 2/3/4为独立子agent（创作/修订/质检），通过expert-writer Execute层调度，context隔离（红线❌7）
- **文风从创作端拆出到修订层**：创作子agent专注故事涌现（场景流+压力源+钩子），不管文风/8020/AI观感词；修订子agent负责文风对齐/人设丰富/爽点验证/bug修复/AI观感词清理。解决v3.0创作端注意力分散导致字数坍塌53%的问题
- **信息获取强制化**：从"自主判断要不要查"改为"强制读索引→读/搜→写本地→更新索引"。每章必须读知识库索引（红线❌6），WebSearch结果写入知识库并更新索引。解决v3.0的ch12-23持续跳过16章信息获取的问题
- **质检子agent独立**：反思从主会话自审改为独立子agent质检，context隔离消除自我审视偏差。解决v3.0的27章全✅、0回退问题
- **种子六要素**：七要素→六要素（文风DNA移至项目资产，由pop-writer-v3-seed蒸馏产出，修订层直接加载）

### 红线变更

- ❌1 文风DNA缺失：从创作端硬阻塞 → 修订层硬阻塞终止
- ❌2 反思不通过：保持回退，改为质检子agent判定，回退Step 2(故事层)或Step 3(文风层)
- ❌3 活记忆唯一写入者：保持，从Step 4移到Step 5
- ❌4 种子生长版本号：保持，新增last_updated_ch更新
- ❌5 法则对照：保持
- **新增❌6**：信息获取必须读索引——索引.md未读取=退回补读
- **新增❌7**：3子agent context隔离——传入精简context，不传会话历史

### 步骤变更（6步→7步）

| v3.0步骤 | v3.1步骤 | 变更 |
|:---------|:---------|:-----|
| step-0 本章规划 | step-0 本章规划 | 微调（去文风DNA，六要素） |
| step-1 信息需求判断 | step-1 信息获取强制化 | 重写（强制读索引+知识库沉淀） |
| step-2 涌现写作 | step-2 创作子agent | 重写（context隔离，纯故事涌现） |
| （无） | step-3 修订子agent | 新建（文风对齐+人设+爽点+bug+AI词清理） |
| step-3 反思五问 | step-4 质检子agent | 重写（context隔离，五问+种子生长+爽点终验） |
| step-4 活记忆+种子 | step-5 记忆更新+方向 | 重写（主会话机械执行，不做判断） |
| step-5 方向+落盘 | step-6 落盘+总控 | 重写（落盘+项目总控+弧线触发） |

### references变更

| v3.0文件 | v3.1文件 | 变更 |
|:---------|:---------|:-----|
| 涌现写作指南.md | 创作指南.md | 重写（去文风DNA/8020/AI观感词） |
| 信息需求判断SOP.md | 信息获取强制化SOP.md | 重写（强制化+知识库+索引） |
| （无） | 修订指南.md | 新建（5项修订任务详解） |
| 网文爽感机制.md | 不变 | — |
| 活种子生长触发规则.md | 微调 | 七→六要素+last_updated_ch |

### templates变更

| v3.0文件 | v3.1文件 | 变更 |
|:---------|:---------|:-----|
| 信息需求判断记录-模板.md | 信息获取记录-模板.md | 重写（+知识库目录+索引格式） |
| 反思五问-模板.md | 质检报告-模板.md | 重写（+种子生长判断+爽点终验+回退目标） |
| （无） | 创作-模板.md | 新建（上下文确认+涌现结构+决策记录+门禁） |
| （无） | 修订checklist-模板.md | 新建（5项checklist+修订记录YAML） |

## v1.1.0 — 2026-06-26

### 新增

- **Step 0 本章规划**（先想再查再写）：读种子+上章正文+活记忆+方向提示+网文爽感机制 → 5个决策点（场景/线索/爽点/危机/钩子）+ 10条法则对照检查
- **网文爽感机制.md**：写作法则配置文件，10条法则（压力机制/即时奖励/危机链/高密度/主动决策/养成感/信息披露/80展示20内省/多线交叉/情绪闭环），可替换为其他领域法则
- **红线❌5**：本章规划必须对照网文爽感机制10条法则，law_check全部✅才能进Step 1
- step-1信息需求判断改造：从"直接基于种子判断"改为"基于本章规划判断"——先想清楚写什么，再判断缺什么信息
- 步骤从5步变6步：step-0本章规划→step-1信息需求→step-2写作→step-3反思→step-4记忆+种子→step-5方向

## v1.0.0 — 2026-06-26

### 新建

- 涌现写作环初始创建，v3管线第二阶段
- 五步循环：信息需求判断 → 涌现写作 → 反思五问 → 活记忆更新+种子生长 → 方向提示
- chapter+prose合并，消除章纲→正文的第三次信息损失
- 信息需求判断：agent自主判断4类检查，不是每章必须查
- 活种子生长：agent自主判断是否追加新要素，权限全给agent
- 反思五问：每个问题必须有具体正文引用作为证据，不通过=回退重写
- 文风DNA硬阻塞（继承v2 prose）
- 活记忆唯一写入者（对齐v2 prose是state-log唯一写入者）
- 3个references：信息需求判断SOP、涌现写作指南、活种子生长触发规则
- 2个templates：信息需求判断记录、反思五问
