# CHANGELOG — pop-novel-bootstrap

## v3.0.0 — 2026-06-05

### 完整重构：Bootstrap 优化（5 Phase 执行计划）

**Phase 1 — Phase 0 重写 + Reader Profile 直出**
- 删除"灵魂三问"（为什么要我写/读者为什么非看不可/核心情绪），改为**故事引擎设计**
- Phase 0 改为 agent 接住用户想象 → 追问 2-3 轮 → 产出结构化 `story-engine.yaml`
- 替代旧 PRD.md（无人消费的死文档）
- reader_profile 直接在 Phase 0 嵌入 project.yaml，Phase 4 降级为校对确认
- 三条红线更新（❌1/❌3/❌8），前 9 条压缩为前 8 条

**Phase 2 — L1 分类重设计 + Phase 1 全量重写**
- 旧六件套（底层逻辑/表层规则/种族/金手指/势力/物品）→ 新六件套
  - 01-世界蓝图 / 02-力量体系 / 03-历史与驱动力 / 04-物种与天赋 / 05-势力格局 / 06-资源与物品
- 验证：三本差异小说（遮天/吞噬星空/深渊主宰）均通过新分类
- 每篇加 schema + before/after 示例（来自真实小说）
- 金手指改为 `[主角]` 标签化，不设独立维度
- Phase 1.5 从自问模式改为 7 项 checklist 模式
- Phase 1.3 从污染式 `【关联：XX】` 标注改为独立 `_交叉引用记录.md`
- 删除 phase-1.2.ref.md（标准已合并到 phase-1.ref.md）

**Phase 3 — 边界清理**
- 删除 Phase 2（L2 卷级展开），交给 plot skill
- 删除 Phase 6（硬检查），交给 plot skill（数值膨胀保留到 Phase 5）
- 相位流：0→0.3→0.4→0.5→1→1.2→1.3→1.5→3→4→5

**Phase 4 — 剩余 Phase 模板化 + 量化重写**
- Phase 0.3: 差异化三列表加模板 + 示例（遮天 vs 凡人）
- Phase 0.4: 金手指加 before/after 示例 + 标签化说明
- Phase 0.5: 量化从数字游戏改为质量导向三层检查（L1定位/L2结构/L3融入）
- Phase 3: constitution.yaml 深度模板（cant_do/must_do 带 example+reason）
- Phase 5: 3 个 yaml 文件加完整字段模板

**Phase 5 — Reverse 对齐 + 清理**
- 事件日志 L1 候选字段对齐新六件套分类
- 删除无关文件 references/PRD-文件读取现状与根因分析.md

**版本号 2.9.3 → 3.0.0**

## v2.9.2 — 2026-06-04

### 按 pop-skill-create 模式重新改造（前次未保存）

- **精简 frontmatter**：19 行 → 3 行，元数据迁移至 skill.json
- **description 改为触发条件式**
- **新增 ❌ 质量红线**：forward 9 条 + reverse 3 条（带 [ ] 勾选框）
- **流程拍平为 3 步**：两条决策路径 × 3 步
- **新增 3 个 WRONG 错误示例**：灵魂层未对齐、续写跳过阅读、跨域素材跳过
- **旧目录路径更新**：skill.json produces 中配置

## v2.9.1 — 2026-06-03

- **merge continuation skill**：pop-novel-continuation 合并入 bootstrap，新增 reverse 模式
- **新增 7 个相位文件**：phase-r1~r6
- **SKILL.md 新增模式选择**：forward（正向新书）/ reverse（逆向续写）
- **master 路由更新**：续写任务指向 `pop-novel-bootstrap (reverse mode)`

## v2.9.0 — 2026-06-03

- **phase 文件名规范化**：6 个文件重命名
- **全量 phase 重写**：13 个文件新增三段式框架
- **name/directory 字段对齐**：`project-bootstrap` → `pop-novel-bootstrap`
- **内部旧引用修复**：`novel-deconstructor` → `pop-novel-deconstructor`

## v2.8.0 — 2026-06-03

- Phase 0.5 强制执行+量化标准；新增 Phase 1.2/1.3
- 从 novel-agent-pro/skills/skill-project-bootstrap 独立提升
