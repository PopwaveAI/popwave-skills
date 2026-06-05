# CHANGELOG — pop-novel-master

## v1.5.0 (2026-06-05)
- **全线同步 bootstrap v3.0 和 plot v3.1 的变更**：
  - SKILL.md bootstrap 描述从"灵魂对齐→数值体系"改为"故事引擎→L1新六件套→宪法→数值体系"
  - 决策点闸门表从"Phase 0 灵魂三问"改为"story-engine 确认"
  - Reflect L2 一致性检查从"L0 PRD/灵魂层"改为"story-engine.yaml 字段"
- **references/ 同步**：
  - think-开书设定.md：PRD/压力测试/灵魂层全部替换为 story-engine 概念
- **路由文件全线修复**：
  - POP-ROUTER.md：旧 skill 名全部替换（skill-project-bootstrap / skill-emergent-writer / skill-book-deconstructor 等→ pop-novel-*）；删除 spec-bridge 引用；删除 glue 编排脚本引用
  - POP-CALL.md：同上，路由表更新 + 场景示例更新（续写示例改为 reverse 模式）
- **版本提升**：v1.4.0 → v1.5.0

## v1.2.0 (2026-06-03)
- **续写路由更新**：pop-novel-continuation 已合并进 pop-novel-bootstrap 的 reverse 模式
- **技能群索引精简**：移除已删除的 continuation / opening-arc 条目
- **路由表更新**：续写任务指向 `pop-novel-bootstrap (reverse mode)`

## v1.1.0 (2026-06-03)
- **pop 身份声明加入**：新增 pop-identity-declaration.md 作为系统级强制规则
- **SKILL.md 重构为 Think→Execute→Reflect 三层工作流**：每次任务先加载审视框架想清楚，再路由，再反思产出
- **新增 references/ 目录**：5 个审视框架文件
  - `think-开书设定.md`：资深编辑视角，审视开书需求+bootstrap产出
  - `think-正文写作.md`：责编视角，审视写正文的前置条件+产出质量
  - `think-续写.md`：项目交接经理视角，审视续写状态+一致性
  - `think-审稿.md`：品控主编视角，审视质检报告+模式问题
  - `reflection.md`：通用反思检查框架，所有路由后执行
  - `pop-identity-declaration.md`：系统级身份声明
- **版本提升**：v1.0.1 → v1.1.0

## v1.0.1 (2026-06-03)
- ROLE.md 合并入 SKILL.md，删除 roles/ 目录
- _shared/ _archive/ 移入自有目录
- 书数据污染清理：SOUL.md 中的海贼法典/深渊主宰引用替换为通用表述
- project_config.py 中的灰骑士路径替换为通用路径

## v1.0.0 (2026-06-03)
- 初始创建：网文作者专家角色定义 + 路由表 + glue编排
- 归档旧 novel-agent-pro 单体存档
