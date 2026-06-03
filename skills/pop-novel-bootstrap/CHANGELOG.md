# CHANGELOG — pop-novel-bootstrap

## v2.9.2 (2026-06-03)
- **merge continuation skill**：pop-novel-continuation 合并入 bootstrap，新增 reverse 模式
- **新增 7 个相位文件**：phase-r1~r6（共 6 执行 + 1 参考）
  - r1：逆向工程逐章事件日志（含独立 ref 模板）
  - r2：L0 产品层提取（复用 phase-0.ref.md）
  - r3：L1 元设定层提取（复用 phase-1.ref.md）
  - r4：宪法提取（复用 phase-3.ref.md）
  - r5：卷大纲确认
  - r6：交接验证
- **SKILL.md 新增模式选择**：forward（正向新书）/ reverse（逆向续写），相位索引表分列
- **master 路由更新**：续写任务指向 `pop-novel-bootstrap (reverse mode)`

## v2.9.1 (2026-06-03)
- **phase 文件名规范化**：`phase-03`→`phase-0.3`、`phase-04`→`phase-0.4`、`phase-05`→`phase-0.5`、`phase-12`→`phase-1.2`、`phase-13`→`phase-1.3`、`phase-15`→`phase-1.5`（共6个）
- **全量 phase 重写**：13个文件全部新增「存在意义」「没有它的后果」「必须回答的问题」三段式框架，执行步骤围绕问题组织而非机械罗列
  - Phase 0：灵魂三问+PRD+压力测试，每项通过条件明确
  - Phase 0.3：新增强制 WebSearch 规则和禁止 LLM 内部知识约束
  - Phase 0.4：金手指设计围绕「为什么是他」「凭什么脱颖而出」「和常规体系的区别」5个必答问题重构
  - Phase 0.5：新增量化自查表（覆盖领域/种子数/转化率/字数）
  - Phase 1：六篇 L1 文件统一围绕「核心矛盾」展开，每个文件有专属的必答问题
  - Phase 1.2：深度展开节点明确为「定义+表现形式+剧情影响+画面锚点」四要素
  - Phase 1.3：14对关联矩阵逐对检查+交叉引用标准格式
  - Phase 1.5：新增「信息暴露检查」和「写死自己检查」
  - Phase 2：新增「驱动角色行动」问题——不是作者让主角做，是主角想做什么
  - Phase 3：新增 constitution.yaml 产出（不可违背创作原则）
  - Phase 4：新增「弃书阈值」作为核心问题
  - Phase 5：从经典体系中提炼断级差/标志性节点/代价递进/跨级战四条原则
  - Phase 6：Boss 和数值体系的超越性检查各有独立必答问题
- **参考书污染清理**：phase-0.3 新增禁止 LLM 内部知识规则，要求 WebSearch
- **模板文件评审**：识别出 chapter-state-template.yaml 是真模板保留，project-proposal-template.md 假模板待删除
- **name/directory 字段对齐**：`name: project-bootstrap`→`pop-novel-bootstrap`，`directory: skill-project-bootstrap`→`pop-novel-bootstrap`
- **内部旧引用修复**：`novel-deconstructor`→`pop-novel-deconstructor`

## v2.9.0 (2026-06-03)
- Phase 0.5 强制执行+量化标准；新增 Phase 1.2 L1深度展开；新增 Phase 1.3 L1交叉关联矩阵
- 从 novel-agent-pro/skills/skill-project-bootstrap 独立提升
