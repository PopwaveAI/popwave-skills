# CHANGELOG — pop-novel-bootstrap

## v2.9.3 — 2026-06-04

### darwin-skill 评估驱动优化：边界条件表

- **新增「异常与边界条件」表**：10 种异常场景预定义 fallback，借鉴 darwin-skill 的异常处理范式
  - 正文文件找不到（reverse）→ 暂停管线，不编造数据
  - WebSearch 不可用 → 降级本地知识库
  - 对标书未提供 → 通用节奏模板代替
  - L1 与 L0 冲突 → 输出冲突说明返回用户决策
  - 世界断裂 → 暂停，用户决定修复方向
  - 中途改平台 → 退回重建画像
  - reverse 正文 < 10 章 → 全部细读
  - phase 文件缺失 → 手动推导
  - 子 agent 启动失败 → master 手动执行+红线自检
- **改造依据**：darwin-skill 评估改进建议 P0

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
