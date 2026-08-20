# 项目总控.html 更新协议（单源）

> 本文件是 `项目总控.html` 所有 SearchReplace 更新操作的唯一规范。初始化创建（step1）、导入重建（step0）、Phase 完成更新（路由循环）都读本文件，禁止在其他文件复述字段表（防多源漂移）。
> 加载时机：**phase 完成后更新 html 时**（路由循环第 3 步）；step0 重建 / step1 初始化时。

项目总控.html 是唯一状态文件（无 project-state.md）。agent 直接用 SearchReplace 更新 `<!--STATE:xxx -->` 标记字段和 phase circle 的 CSS class。**只更新本次操作涉及的字段，不全量替换。**

---

## 1. 初始化创建字段（step1 首次落盘时）

读模板 `templates/项目总控.html` 写入项目根目录后，更新：

| 标记 | 替换值 |
|:--|:--|
| `<!--STATE:project_name -->未命名项目<!--/STATE:project_name -->` | `{用户给的项目名}` |
| `<!--STATE:created_at -->--<!--/STATE:created_at -->` | `{YYYY-MM-DD HH:mm}` |
| `<!--STATE:updated_at -->--<!--/STATE:updated_at -->` | `{YYYY-MM-DD HH:mm}` |
| `<!--STATE:genre -->待指定<!--/STATE:genre -->` | `{用户赛道方向}`（未指定则保留"待指定"） |

## 2. 导入重建字段（step0 落地Phase后）

| 标记 | 替换值 |
|:--|:--|
| `<!--STATE:mode -->fresh<!--/STATE:mode -->` | `{import/resume}` |
| `<!--STATE:phase -->init<!--/STATE:phase -->` | `{落地Phase}` |
| `<!--STATE:chapter -->ch000<!--/STATE:chapter -->` | `{current_chapter}` |
| project_name / updated_at | 同 §1 |

同时把已就绪 Phase 的 circle 改 `done`、落地 Phase 改 `current`、已有资产 badge 改 ✅（规则见 §3-§4）。

## 3. 循环更新字段（每次 Phase 完成后）

### 3a. 通用（每次必更）

| 操作 | SearchReplace 示例 |
|:--|:--|
| 更新 phase | `<!--STATE:phase -->phase0<!--/STATE:phase -->` → `<!--STATE:phase -->phase1<!--/STATE:phase -->` |
| 更新时间戳 | `<!--STATE:updated_at -->旧时间<!--/STATE:updated_at -->` → `<!--STATE:updated_at -->{当前时间}<!--/STATE:updated_at -->` |
| 更新 next_step | `<!--STATE:next_step -->旧值<!--/STATE:next_step -->` → `<!--STATE:next_step -->{下一步}<!--/STATE:next_step -->` |

### 3b. Phase circle（标记完成+当前阶段）

把已完成的 circle 从 `pending` 改 `done`，新阶段的 circle 从 `pending` 改 `current`：

| 操作 | SearchReplace 示例 |
|:--|:--|
| 标记完成 | `class="phase-circle pending" id="ph-0"` → `class="phase-circle done" id="ph-0"` |
| 同上连线 | `class="phase-line" id="ln-0"` → `class="phase-line done" id="ln-0"` |
| 标记当前 | `class="phase-circle pending" id="ph-1"` → `class="phase-circle current" id="ph-1"` |
| label 活跃 | `<div class="phase-label" id="lb-1">` → `<div class="phase-label active" id="lb-1">` |

**Phase ID 对照表**：

| Phase | circle id | line id | label id |
|:--|:--|:--|:--|
| Phase 0 | ph-0 | ln-0 | lb-0 |
| Phase 1 | ph-1 | ln-1 | lb-1 |
| Phase 3 | ph-3 | ln-3 | lb-3 |
| Phase 3.5 | ph-3_5 | ln-3_5 | lb-3_5 |
| Phase 4 | ph-4 | ln-4 | lb-4 |
| Phase 5 | ph-5 | ln-5 | lb-5 |
| Phase 6 | ph-6 | — | lb-6 |

> **Phase 6→5 写审循环**：只更新 chapter 值和 next_step，**不修改 phase circle**（Phase 5/6 已在循环中交替）。

### 3c. 就绪 badge（按 phase 产出更新）

| Phase 完成 | 需要更新的 badge |
|:--|:--|
| Phase 0 | deck_0(用户意图)→✅, deck_1(赛道调研)→✅, deck_2(参考书)→✅或跳过, deck_3(笔触DNA)→✅或跳过, deck_4(decon-lite)→✅或跳过 |
| Phase 1 | prd_0(立项PRD)→✅ |
| Phase 3 | skel_0(力量体系)→✅, skel_1(动力引擎)→✅, flesh_0(全书设定)→✅ |
| Phase 3→3.5 | flesh_1(DNA综合)→✅ |
| Phase 3.5 | prot_0(金手指)→✅, flesh_2(角色库)→✅ |
| Phase 4 | main_0(主线)→✅, flesh_3(卷纲)→✅, chapter→ch002 |

badge 示例：`<!--STATE:skel_0 -->❌<!--/STATE:skel_0 -->` → `<!--STATE:skel_0 -->✅<!--/STATE:skel_0 -->`

### 3d. 创意摘要（Phase 1 seed 产出后）

- `<!--STATE:book_name -->待seed产出<!--/STATE:book_name -->` → `{实际书名}`
- `<!--STATE:one_line -->待seed产出<!--/STATE:one_line -->` → `{实际一句话}`

### 3e. 最近产出追加（每次 phase 完成都追加）

- old: `<!--STATE:outputs_start-->`
- new: `<!--STATE:outputs_start-->\n        <tr><td>{Phase名}</td><td class="file-path">{产出文件路径}</td><td>{时间}</td></tr>`

### 3f. 流派记录（Phase 5 开始时）

- `<!--STATE:write_skill -->待Phase 5指定<!--/STATE:write_skill -->` → `pop-qidian-write（流派: {流派名}）`
