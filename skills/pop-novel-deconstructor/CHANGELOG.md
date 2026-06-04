# CHANGELOG — pop-novel-deconstructor

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
