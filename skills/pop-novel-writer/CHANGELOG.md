# CHANGELOG — pop-novel-writer

## v11.2.0 — 2026-06-05

### 移除黄金三章模式

**变更**：
- 删除 `steps/step-golden-triple.md`
- SKILL.md 移除黄金三章模式章节、❌7红线、WRONG3错误示例
- 所有章节统一走 5 步管线，不区分 CH1–CH3 与后续章节
- skill.json 更新 tags 和 description
- expert-writer 同步更新 writer 描述和引导模板

## v11.0.0 — 2026-06-05

### 管线重构为 5 步驱动（3 次 LLM 调用）

**核心变更**：
- **管线从 3 步扩展为 5 步**：Director(LLM) → 上下文搜集(零LLM) → 骨架Agent(LLM) → 渲染(LLM) → 状态更新(零LLM)
- **Director 精简**：不读文风DNA、不选锚定章、不出决策日志，只出设计说明+信息释放策略
- **新增 Step 2 上下文搜集**：按 Director 指示从文件系统搜集 L1 设定 + entity-state + global-summary
- **骨架 Agent 独立为 Step 3**：按事实骨架模板产出事件链+设定包+密度标记，含骨架层 QC
- **渲染 Step 4 输入精简为 7 项**：骨架+世界快照+设计说明+文风DNA+红线+全局摘要+上一章结尾
- **新增 Step 5 状态更新**：渲染器输出状态更新块 → 零LLM追加到 global-summary.md + entity-state.yaml
- **文风锚定包系统简化**：去掉 Layer 2（叙事策略指令）和锚定章注入，渲染器直接消费 DNA

**删除**：
- ❌ ESM before 的 DNA→叙事策略指令生成层
- ❌ 锚定章片段注入渲染器
- ❌ Pass1-chapter-planner.md（骨架 Agent 独立模板）
- ❌ SQLite/DB 引用（未运维，改为文件）
- ❌ Director 读文风DNA

**新增模板**：
- `templates/事实骨架模板.md` — 骨架标准化产出格式
- `templates/entity-state-schema.md` — 世界快照模板
- `templates/everything-bundle-schema.md` — 渲染器输入包参考

**Prompt 模板升级**：
- Director-prompt.md v5.0：精简版，不含DNA和锚定章
- Pass2-renderer.md v5.0：7项输入 + 三层框架消费 + 状态更新块输出

**兼容性**：
- entity-state.yaml 不存在 → Step 2 跳过
- 旧版 act-XX.yaml 无 info_release → Director 不输出信息释放策略
- 旧管线不依赖删除的 Pass1 文件

- **版本号 10.0.0 → 11.0.0**

## v10.0.0 — 2026-06-05

### 三层框架全面升级（纯事实骨架/叙事策略指令/文风DNA）

**核心架构变革**：
- **三层框架定义**：Layer 1（纯事实骨架：事件链+设定包+密度标记）/ Layer 2（叙事策略指令：ESM before 从DNA动态生成）/ Layer 3（文风DNA：5条叙事哲学原则+应用规则）
- **骨架Agent升级为 Layer 1 产出**：消费 act-XX.yaml info_release → 按 source_doc 从 L1 提取具体内容 → 按 release_method 嵌入骨架
- **ESM before 新增 Layer 2 生成逻辑**：从5条DNA原则动态生成5条叙事策略指令（信息释放/叙事者姿态/情感表达/对话策略/张力控制）
- **ESM 注入包从13项扩展为15项**：新增第13项（info_release实体内容）+ 第14项（叙事策略指令）
- **写前必读清单追加**：info_release确认 + 叙事策略指令确认
- **渲染新增"三层框架消费指南"**：消费优先级规则 + 三层冲突解决规则

**文风锚定包系统 v3.0**：
- **文风锚定包模板.md 从参数式升级为DNA式**：删除原7项复选框+5项技法偏好 → 5条叙事哲学DNA（信念陈述+证据链+跨章验证+应用规则）
- **锚定章片段新增"叙事哲学印证"字段**：绑定实例与DNA原则
- **所有 style 文件升级至 v3.0 格式**：abyss / default / tomato / zhetian / tunshi / shengwang / yazhou / zerg / guichui / nvpin 共10个文件

**Prompt 模板升级**：
- **Director-prompt.md v4.0**：新增"信息释放策略"区块 + 前置检查新增 info_release + 文风DNA读取
- **Pass1-chapter-planner.md v4.0**：新增 Step 2-a info_release 消费逻辑 + 骨架格式改为事件链+设定包+密度标记
- **Pass2-renderer.md v4.0**：15项输入 + 三层框架消费指南 + 写后自评第④问 + AC-6信息释放合规检查

**兼容性**：
- info_release 字段可选 → 旧版 act-XX.yaml 无此字段时骨架 Agent 按原逻辑工作
- 文风锚定包兼容 v2.0（参数式）→ ESM before 检测后走旧逻辑生成近似指令
- Pass2 输入项扩展不破坏旧项编号映射

**测试验证**：
- 三轮验证（CH1×3DNA + CH2×3DNA + CH3×3DNA + CH2v2×3DNA = 12篇并行产出）
- v2 差异从"同故事不同语气"升级为"同事实不同叙事者结构决策"
- 复盘PRD沉淀：三层框架定义+数据证据+落地建议

- **版本号 9.7.1 → 10.0.0**

## v9.7.1 — 2026-06-04

### 新增异常与边界条件表
- **SKILL.md 新增 `## 异常与边界条件` 表格**：覆盖 10 个异常场景（act 缺失、spec 未审批、设定文件缺失、QC 模板缺失、文风锚定包缺失、实体不足、自评重大缺陷、用户中途改风格、summary 损坏、段落字数不足）
- **新增"绝不静默编造内容"核心原则**：所有兜底行为必须输出可追溯标记
- **版本号 9.7.0 → 9.7.1**

### 删除 template-pools（场景模板）
- **删除 8 个场景模板文件**：通用场景结构约束移除，交由 styles/ 和管线自然决定
- **ESM before 从 14 项压缩为 13 项**：删除第 11 项（场景模板）

## v9.7.0 — 2026-06-04

### 新增 5 种文风参考，覆盖新赛道
- **shengwang（圣王）**：梦入神机·狂暴升级流·设定密集型
- **yazhou（海贼法典）**：同人/二次元·穿越吐槽·日漫分镜感
- **zerg（虫族帝国）**：异兽流·游戏系统·基地种田
- **guichui（鬼吹灯）**：悬疑盗墓·知识科普·层进氛围
- **nvpin（女频古言）**：细腻日常·微表情对话·慢热情感
- **SKILL.md 风格清单同步更新**：从 5 种扩展至 10 种
- **版本号 9.6.0 → 9.7.0**

## v9.6.0 — 2026-06-04

### 文风锚定包 — 锚定章 + 风格合并为单次注入
- **删除 style-dna-template.md**：第1层（微观质感）不再单独定义，由锚定章片段直接提供实例
- **创建文风锚定包模板**：`styles/文风锚定包模板.md` 合并锚定章片段 + 叙事策略 + 技法偏好 + 红线清单
- **所有 style 文件按新格式重写**：default/tomato/tunshi/zhetian/abyss 去掉第 1 层，改为"锚定章参考模式 + 抽象规则"结构
- **ESM before 从 17 项压缩为 14 项**：原第 10 项（锚定章）+ 第 16 项（style）合并为第 10 项（文风锚定包）
- **读取优先级**：`01-写作资产/文风锚定包.md`（项目级）→ `styles/{writing_style}.md`（内部）→ `styles/default.md`（兜底）
- **styles/ 目录定位改变**：从"用户可选的5种风格"变为"bootstrap 提取时的内部参考样本"
- **版本号 9.5.1 → 9.6.0**

## v9.5.1 — 2026-06-04

### 按 pop-skill-create 改造模式改造

- **精简 frontmatter**：38 行 → 3 行，元数据迁移至 skill.json
- **description 改为触发条件式**
- **新增 10 条 ❌ 质量红线（带 [ ] 勾选框）**，提至第一屏
- **流程拍平为 3 步**：Director → 骨架+ESM → 渲染+QC → 状态更新（原 6 Phase 嵌套）
- **新增 3 个 WRONG 错误示例**：靠"我记得"写正文、无决策日志、黄金三章当普通章
- **删除重复内容**：锚定章系统（deconstructor 已有）、经验日志详情、重复 ESM 表
- **整合 HARD-GATE + 写前必读清单**：原两处分散规则合并为一次性清单
- **输出路径更新**：01-事实骨架/ → 骨架/，03-正文/ → 正文/，02-章纲/ → 配置/
- **新增 CHANGELOG.md**

## v9.5.0 — 2026-06-03

- 风格注入系统：styles/ 目录提供可插拔文风配置
- ESM before 升级 15 项输入包（+style-bundle）
- 新增 tomato 文风

## v9.4.0 — 2026-06-03

- 黄金三章模式合并入正文引擎（原 pop-novel-opening-arc）

## v9.3.0 — 2026-05-25

- 六阶段管线重构
- Director 升级 + ESM before 14 项 + Pass 2 写后自评 + QC 三层介入

## v9.0.0 — 2026-05-24

- ESM v2.0 SQLite 全书数据中台
- Pass 1/Pass 2 分离

## v8.0.0 — 2026-05-21

- 导演 Agent 回归
- K1-K4 知识注入体系
- 经验日志机制
