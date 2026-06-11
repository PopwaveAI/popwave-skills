## v8.1.0 | 2026-06-11

- **T2 模板消费引注更新**：act-XX-地图→volume-XX、info-release→act#info_release_plan、constitution→volume-XX引注
- **T7 文风DNA产出路径更新**：styles/ → 写作资产/文风DNA/

## v8.0.0 | 2026-06-08

- **采样策略升级为全读**：默认前100章改为全量逐章精读（覆盖率从24%升至100%），确保设定/角色/节奏信息无遗漏
- **T3 升级为角色系统设计**：从金手指天赋扩展为完整角色维度，含主角驱动力/关键决策节点/成长弧线/读者情感绑定/配角生态/反派分层体系/关系网/可复用规则
- **T5 合并为叙事技法综合**：原T6（叙事设计）+ T8（战斗高潮）+ T9（特殊魅力）三合一，五节覆盖开篇/节奏/悬念/战斗高潮/特殊魅力
- **T6 改为赛道触发型**：原T7（数据流写法）调整为仅系统/面板类赛道执行，其余赛道跳过
- **T7 文风DNA**：原T10改编号，内容不变
- **模板总数**：10 → 7（删除旧T3金手指、T8战斗、T9魅力；保留T1/T2/T4；升级T3；合并T5；重排T6/T7）

## v6.3.0 | 2026-06-07

- **T4 剧情全貌模板重写**：引入双主线结构（M1世界压力源+M2主角成长），支线标注衍生关系，Act边界由M1+M2双轴密度共同决定
- **新增**：逐章情节线分布表（CH×6列）强制产出、Plotline关系图（ASCII）强制产出、按plotline分列的契诃夫枪链跟踪+跨度标记
- **沉淀**：来自深渊主宰前50章反拆实战的SOP

# CHANGELOG — pop-novel-deconstructor

## v5.0.0 — 2026-06-05

### 新增 Step 3-b：叙事哲学DNA提取（三层框架 v3.0）

- **新增 Step 3-b 提取叙事哲学DNA**：在锚定章片段提取之后，按 v3.0 模板产出 5 条叙事哲学原则
  - 5 个维度：信息释放哲学、叙事者姿态哲学、情感表达哲学、对话策略哲学、张力-释放哲学
  - 每条原则含：信念陈述 + 证据链（引用锚定章）+ 跨章验证 + 应用规则
  - 格式参考 `skills/pop-novel-writer/styles/文风锚定包模板.md`（v3.0）
- **新增产出物路径**：`01-写作资产/文风锚定包.md`（Layer 1 锚定章片段 + Layer 3 叙事哲学DNA）
- **新增 WRONG 4**：只产锚定章不产DNA的错误示例
- **新增质量红线 ❌9**：DNA提取完整性检查
- **改造依据**：writer v10.0 消费侧要求 v3.0 DNA 格式的 `01-写作资产/文风锚定包.md`
- **版本号 4.9.1 → 5.0.0**

## v4.9.1 — 2026-06-04

### darwin-skill 评估驱动优化：边界条件表

- **新增「异常与边界条件」表**：10 种异常场景预定义 fallback，借鉴 bootstrap 的优化模式
  - 正文文件不存在 → 不退回到编造内容
  - 参考书字数太少 → 缩减拆解范围
  - 同人题材无原著知识 → 必须先搜索
  - 所有规则都是 P2 → 回退到模式A
  - 锚定章无 P0 片段 → 降标到 P1
  - WebSearch 不可用 → 降级可用平台
  - fragment-pipeline 失败 → 不阻塞锚定章
  - 拆解中发现书质量差 → 输出不推荐报告
  - 用户要求拆自身作品 → 按场景判断
  - 多模式产出路径冲突 → 文件名加模式标识
- **改造依据**：darwin-skill 评估改进建议 P0

## v4.9.0 — 2026-06-04

### 按 pop-skill-create 模式重新改造（前次未保存）

- **精简 frontmatter**：26 行 → 3 行，元数据迁移至 skill.json
- **description 改为触发条件式**
- **新增 8 条 ❌ 质量红线（带 [ ] 勾选框）**
- **流程拍平为 3 步**：拆前思考 → 执行拆解 → 提取锚定章
- **新增 3 个 WRONG 错误示例**：只停复述剧情、特征≈复述、不搜资料
- **质量门禁令化**：P0/P1/P2 → ❌5
- **输出路径更新**：01-写作资产/ → 素材库/

## v4.8.1 (2026-06-03)
- **name/directory 字段对齐**：`name: book-deconstructor`→`pop-novel-deconstructor`，`directory: skill-book-deconstructor`→`pop-novel-deconstructor`
- **内部旧 skill 名修复**：`emergent-writer`→`pop-novel-writer`、`project-bootstrap`→`pop-novel-bootstrap`
- **死路径修复**：`_工具配置/novel-agent-pro/skills/...`→`skills/pop-novel-deconstructor/fragment-pipeline/`
- **书数据污染清理**：`novel-agent-pro 内部拆书引擎`引用指向 `_archive`

## v4.8.0 (2026-06-03)
- 从 novel-agent-pro/skills/skill-book-deconstructor 独立提升
- 修复路径引用（_工具配置/novel-agent-pro/ → skills/pop-novel-deconstructor/）
