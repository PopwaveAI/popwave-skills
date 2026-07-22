# step2 · 读项目总控路由 + 完成后更新

> 本文件是 pop-qidian-pipeline 第二步执行指令。每次对话开始时执行。

## 目标

读 项目总控.html → 判断当前 phase → 路由到对应 skill → 完成后用SearchReplace更新html

**v1.2.0核心变化**：不再有project-state.md。项目总控.html是唯一状态文件。agent直接用SearchReplace更新html中的`<!--STATE:xxx -->`标记字段和phase circle的CSS class。

## 执行

### 1. 读 项目总控.html

用Read工具读取项目根目录的 `项目总控.html`。

从HTML注释标记中提取当前状态：
- phase值：找 `<!--STATE:phase -->xxx<!--/STATE:phase -->`
- chapter值：找 `<!--STATE:chapter -->xxx<!--/STATE:chapter -->`
- next_step：找 `<!--STATE:next_step -->xxx<!--/STATE:next_step -->`

### 2. 按 phase 路由

对照 SKILL.md 速查表"启动时判断"，根据 phase 值路由到对应 Phase 流程。

### 3. Phase 完成后更新 项目总控.html

每个Phase完成后，用SearchReplace更新以下字段（不是全部，只更新本phase涉及的）：

#### 3a. 通用更新（每次phase完成都必须更新）

| 操作 | SearchReplace示例 |
|:--|:--|
| 更新phase | old: `<!--STATE:phase -->phase0<!--/STATE:phase -->` → new: `<!--STATE:phase -->phase1<!--/STATE:phase -->` |
| 更新timestamp | old: `<!--STATE:updated_at -->2026-07-22 14:00<!--/STATE:updated_at -->` → new: `<!--STATE:updated_at -->{当前时间}<!--/STATE:updated_at -->` |
| 更新next_step | old: `<!--STATE:next_step -->Phase 0: ...<!--/STATE:next_step -->` → new: `<!--STATE:next_step -->{下一步}<!--/STATE:next_step -->` |

#### 3b. Phase circle更新（标记完成+当前阶段）

把已完成的phase circle从`pending`改为`done`，把新阶段的circle从`pending`改为`current`：

| 操作 | SearchReplace示例 |
|:--|:--|
| 标记完成 | old: `class="phase-circle pending" id="ph-0"` → new: `class="phase-circle done" id="ph-0"` |
| 同上连线 | old: `class="phase-line" id="ln-0"` → new: `class="phase-line done" id="ln-0"` |
| 标记当前 | old: `class="phase-circle pending" id="ph-1"` → new: `class="phase-circle current" id="ph-1"` |
| 标记label活跃 | old: `<div class="phase-label" id="lb-1">` → new: `<div class="phase-label active" id="lb-1">` |

**Phase ID对照表**：

| Phase | circle id | line id | label id |
|:--|:--|:--|:--|
| Phase 0 | ph-0 | ln-0 | lb-0 |
| Phase 1 | ph-1 | ln-1 | lb-1 |
| Phase 2 | ph-2 | ln-2 | lb-2 |
| Phase 3 | ph-3 | ln-3 | lb-3 |
| Phase 3.5 | ph-3_5 | ln-3_5 | lb-3_5 |
| Phase 4 | ph-4 | ln-4 | lb-4 |
| Phase 5 | ph-5 | ln-5 | lb-5 |
| Phase 6 | ph-6 | — | lb-6 |

#### 3c. 就绪状态更新（按phase产出更新对应badge）

| Phase完成 | 需要更新的badge |
|:--|:--|
| Phase 0 | deck_0(用户意图)→✅, deck_1(赛道调研)→✅, deck_2(参考书)→✅或跳过, deck_3(笔触DNA)→✅或跳过, deck_4(decon-lite)→✅或跳过 |
| Phase 1 | skel_0(力量体系)→✅, skel_1(动力引擎)→✅, skel_2(骨架自洽)→✅ |
| Phase 2 | prot_0(主角设计)→✅, prot_1(金手指)→✅, prot_2(爽感矛盾)→✅ |
| Phase 3 | flesh_0(地图)→✅, flesh_1(势力)→✅ |
| Phase 3.5 | flesh_2(角色库)→✅ |
| Phase 4 | flesh_3(剧情白描)→✅, chapter→ch002 |

**badge SearchReplace示例**：
- old: `<!--STATE:skel_0 -->❌<!--/STATE:skel_0 -->` → new: `<!--STATE:skel_0 -->✅<!--/STATE:skel_0 -->`

#### 3d. 创意摘要更新（Phase 1完成后）

Phase 1 seed产出后，更新书名和一句话简介：
- old: `<!--STATE:book_name -->待seed产出<!--/STATE:book_name -->` → new: `<!--STATE:book_name -->{实际书名}<!--/STATE:book_name -->`
- old: `<!--STATE:one_line -->待seed产出<!--/STATE:one_line -->` → new: `<!--STATE:one_line -->{实际一句话}<!--/STATE:one_line -->`

#### 3e. 最近产出追加（每次phase完成都追加一行）

在`<!--STATE:outputs_start-->`和`<!--STATE:outputs_end-->`之间追加新行：

SearchReplace:
- old: `<!--STATE:outputs_start-->`
- new: `<!--STATE:outputs_start-->\n        <tr><td>{Phase名}</td><td class="file-path">{产出文件路径}</td><td>{时间}</td></tr>`

#### 3f. write_skill更新（Phase 5开始时）

- old: `<!--STATE:write_skill -->待Phase 5指定<!--/STATE:write_skill -->` → new: `<!--STATE:write_skill -->{pop-qidian-write / pop-qidian-write-dndlike / pop-qidian-write-onepiece}<!--/STATE:write_skill -->`

### 4. 路由规则要点

- Phase 0 → Phase 1：底牌就绪（用户意图+赛道调研）
- Phase 1 → Phase 2：骨架就绪（力量体系+动力引擎+骨架自洽）
- Phase 2 → Phase 3：主角就绪（主角设计+金手指+爽感矛盾）
- Phase 3 → Phase 3.5：全书设定就绪
- Phase 3.5 → Phase 4：角色库就绪
- Phase 4 → Phase 5：剧情白描+章锚点表就绪
- Phase 5 → Phase 6：正文产出
- Phase 6 → Phase 5（通过→下一章 / 打回→重写本章）

**Phase 6→Phase 5循环时**：只更新chapter值和next_step，不修改phase circle（Phase 5和6已在循环中交替）。

## 质量门

- 每次路由前必读 项目总控.html
- 每次Phase完成后必更新 项目总控.html（至少更新phase+timestamp+next_step+circle）
- 三层骨架依赖链不可跳过
