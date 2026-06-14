# CHANGELOG — expert-writer

## v3.1.1 (2026-06-14)

- **v5 结构重构**：SKILL.md 瘦身至 ≤120 行（从 176 行缩减），Think/Execute/Reflect 核心内容拆分至 `steps/step-1-think.md`、`steps/step-2-execute.md`、`steps/step-3-reflect.md`
- **红线表格化**：从列表格式转为 `| # | 红线 |` 表格格式，7 条核心红线
- **核心流程指针化**：SKILL.md 中只保留 3 步指针表，指向 steps/ 文件
- **身份声明迁移**：pop 身份声明协议（每次新任务输出格式）从 SKILL.md 移至 `_shared/pop/IDENTITY.md`
- **pipeline 字段**：skill.json 新增 `pipeline.upstream`（空数组，元 skill 无上游）和 `pipeline.downstream`（15 个子 skill 完整列表）

## v3.1.0 (2026-06-11)

- **constitution.yaml 移除**：全链路删除，act-XX.yaml Canvas 字段（chekhov_set/combat.scale/payoff/plotlines_active）已全覆盖约束
- **路径重构**：03-正文→正文、03-写作资产→写作资产/设计包、L3-角色层→状态/角色、幕按卷分组(vol-XX/)
- **Reflect L2 一致性对象变更**：entity-snapshot ↔ constitution → entity-snapshot ↔ 角色卡
- **pipeline-check**：去 constitution/act-XX-人物检查，新增状态/角色/目录检查
- **ROUTE-AUGMENT**：constitution_ok → state_ok，constitution 路径删除

## v3.0.0 (2026-06-10)

- **SKILL.md 瘦身：21K → 9K**（-57%），每次 Paopao 注入节省 12K 上下文窗口
- **5 个 references/ 文件提取**：reflection(L1-L4 审视) / dynamic-fusion(动态融合) / completion-guide(完成后引导) / pipeline-check(管道校验) / typical-paths(典型路径)
- **加载协议统一**：所有 reference 文件用 `Get-Content -Encoding UTF8 -Raw` 加载，同行标注"不用 Read 工具"
- **SKILL.md 保留骨架**：纪律/身份声明/Skill清单/路由表/工作流三步/修改路由 — 所有核心指令一律保留
- **references/reflection.md 合并**：原有 68 行 + SKILL.md L1-L4 审视清单 → 完整四层审视
- **新增 references/**：completion-guide.md, dynamic-fusion.md, pipeline-check.md, typical-paths.md

## v2.6.0 (2026-06-10)

- **动态融合检查（Think 第二步·A）**：追加核心设定后禁止打补丁。逐文件重新审视 L1 六件套每个字段，决定被新设定深度改写/不变/新建子段
- **大环节转换自检（§3.1.6 ⑥）**：bookstrap→plot→chapter-design→prose-render 切换前，agent 用 Get-Content 读取上一环节全部产出文件，回答三个语义级问题：深度是否足够、追加设定是否充分融合、是否有数据断点
- **明确禁令**：禁止"在末尾追加段落"、"只改一个文件"、"跳过逐字段检查"等打补丁行为
- **输出融合声明**：动态融合完成后输出每文件的受影响字段数

## v2.5.0 (2026-06-10)

- **路由前强制加载协议**：路由到任何子 skill 前无条件加载 4 项（子 skill SKILL.md + 全部文档文件 + 项目 YAML + 文风DNA）
- **去掉条件判断**：v2.3 "任务类型切换检查" 要求 agent 判断 intent 是否变化 → agent 判断失误极高（"都是写正文"→跳过）。v2.5 改为无条件加载，不依赖 agent 自觉
- **写为路由前置条件**：不加载 = 路由失败，agent 会被卡住，必须补加载才能继续
- **明确禁令**：禁止以"之前读过"、"我记住了"、"不需要"为理由跳过加载
- **"继续前进"路线更新**：执行路径第一条改为"先强制加载，再读进度判定路由"
- **Reflect 文件加载检查同步更新**

## v2.4.0 (2026-06-10)

- **读文件方式重构**：禁止使用 Read 工具读取子 skill 文档文件和 YAML 文件
- **全量改用 exec + Get-Content -Encoding UTF8 -Raw** — 彻底解决 Read 截断 bug
- **覆盖范围扩展**：SKILL.md、steps/*.md、phases/*.md、templates/*.md、references/*.md、README.md、*.yaml、*.yml
- **§0.8 重写**：从"Read+检查行号+offset续读"改为"优先 exec 完整加载"+"仅 >25K 文件回退 Read+offset"
- **§0.9 重写**：路由前文件完整性验证适配新方法
- **Think §3.1.6 ③ 更新**：管道前置校验升级为全量 Get-Content 验证
- **Reflect 检查更新**：行号追溯检查替换为 Get-Content 加载完整性检查
- **证据**：6-10项目测试 42 次 run 全部命中 Read 截断，最大仅返回 2,416 字符
- **exec stdout 上限**：~30,000 字符，所有 SKILL.md（最大 17K）和 YAML 文件均可完整读取

## v1.0.0 (2026-06-04)

- **首次发布**：V1 写作专家元 Skill
- **两步判断规则**：范围判断（创作/非创作）→ 意图路由（新建/继续/修改/质检/调研），Agent 一条链决策
- **修改路由（三层联动）**：
  - 定位修改层（bootstrap / plot / writer / opening-arc / qa）
  - 评估连锁影响（5 种修改类型 × 需联动层映射表）
  - 执行修改（最小影响原则，从上层到下层逐层更新）
- **完成后引导**：基于项目文件状态（非记忆）的跨轮引导。每轮产出后先问修改 + 建议下一步
- **10 个推荐 Skill + 4 个延伸 Skill**：覆盖完整网文创作管线
- **输出规范**：中文写作、不暴露内部 Skill 名称、必须追引导、非创作请求不强行关联

> 配套 PRD：`06_专家模式PRD_v1.md` | 架构文档：[06_专家模式PRD_v1 — 飞书](https://www.feishu.cn/docx/ImVQdtzSloSsbdxJsMAcwHCIn6c)
