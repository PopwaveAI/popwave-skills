# CHANGELOG — expert-writer

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
