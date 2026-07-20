# CHANGELOG

## v1.0.0 (2026-07-20)

### 新建pop-fanqie-pipeline skill

**根因**：R41全链路测试+7-20项目a实际运行诊断发现管线三大结构性缺口：
1. 没有"我在哪"的文件——agent启动时没有任何落盘文件告诉它当前在管线的哪个阶段
2. skill之间盲调度——每个skill只知道自己的SOP，不知道何时该调下游
3. 参考书是"用户提了才触发"的可选项——seed 1a不问参考书，用户不提就永远跳过

**设计**：
- SKILL.md：项目初始化+project-state.md模板+5个phase路由规则+红线5条+速查表
- step1.md：初始化。创建标准目录结构（8个子目录）+ 落盘project-state.md（phase=init）
- step2.md：路由。读project-state.md → 按phase值分流到5个phase执行，每个phase完成后更新state
- skill.json：v1.0.0

**Phase 0参考书闸门**（最关键的改动）：
- 进入Phase 1 Seed前，必须先通过Phase 0参考书摸底
- 三条路径：用户给书名→download+dna-style / 用户没想好→research推荐→download+dna-style / 用户明确拒绝→标注风险
- 不完成参考书摸底，不进入Phase 1

**项目目录结构**：
```
项目/
├── project-state.md        ← 管线状态追踪
├── 0-立项/
├── 1-骨架/
├── 2-正文/
├── 审核/
├── 涌现/
├── downloads/
└── 写作参考/知识沉淀/
```
