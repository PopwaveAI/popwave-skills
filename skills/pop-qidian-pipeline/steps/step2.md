# step2 · 读state路由 + 完成后更新

> 本文件是 pop-qidian-pipeline 第二步执行指令。每次对话开始时执行。

## 目标

读 project-state.md → 判断当前 phase → 路由到对应 skill → 完成后更新 state.md + state.html

## 执行

### 1. 读 project-state.md

```powershell
Get-Content -Encoding UTF8 -Raw project-state.md
```

### 2. 按 phase 路由

对照 SKILL.md 速查表"启动时判断"，根据 phase 值路由到对应 Phase 流程。

### 3. Phase 完成后更新 state

每个 Phase 完成后：
1. 更新 project-state.md 的 phase 值 + 就绪状态 + 最近产出
2. 生成 project-state.html（如有脚本）
3. 告知用户下一步操作

### 4. 路由规则要点

- Phase 0 → Phase 1：底牌就绪（用户意图+赛道调研）
- Phase 1 → Phase 2：骨架就绪（力量体系+动力引擎+骨架自洽）
- Phase 2 → Phase 3：主角就绪（主角设计+金手指+爽感矛盾）
- Phase 3 → Phase 3.5：全书设定就绪
- Phase 3.5 → Phase 4：角色库就绪
- Phase 4 → Phase 5：剧情白描+章锚点表就绪
- Phase 5 → Phase 6：正文产出
- Phase 6 → Phase 5（通过→下一章 / 打回→重写本章）

## 质量门

- 每次路由前必读 project-state.md
- 每次Phase完成后必更新 project-state.md
- 三层骨架依赖链不可跳过
