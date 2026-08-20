# 视觉项目总控.html 更新协议（单源）

> 本文件是 `视觉项目总控.html` 所有 SearchReplace 更新操作的唯一规范。step0 初始化、step1 导入重建、路由循环的 phase 完成更新都读本文件，禁止在其他文件复述字段表（防多源漂移）。
> 加载时机：**phase 完成后更新 html 时**（路由循环第 3 步）；step0/step1 落地时。

视觉项目总控.html 是唯一状态文件。agent 直接用 SearchReplace 更新 `<!--STATE:xxx -->` 标记字段和 phase circle 的 CSS class。**只更新本次操作涉及的字段，不全量替换。**

---

## 1. 通用更新（每次 phase 完成必更）

| 操作 | SearchReplace 示例 |
|:--|:--|
| 更新 phase | `<!--STATE:phase -->init<!--/STATE:phase -->` → `<!--STATE:phase -->phase1<!--/STATE:phase -->` |
| 更新时间戳 | `<!--STATE:updated_at -->--<!--/STATE:updated_at -->` → `<!--STATE:updated_at -->{当前时间}<!--/STATE:updated_at -->` |
| 更新 next_step | `<!--STATE:next_step -->旧值<!--/STATE:next_step -->` → `<!--STATE:next_step -->{下一步}<!--/STATE:next_step -->` |

## 2. Phase circle（标记完成+当前阶段）

把已完成 phase 的 circle 从 `pending` 改 `done`，新阶段的 circle 从 `pending` 改 `current`：

| 操作 | SearchReplace 示例 |
|:--|:--|
| 标记完成 | `class="phase-circle pending" id="ph-0"` → `class="phase-circle done" id="ph-0"` |
| 同上连线 | `class="phase-line" id="ln-0"` → `class="phase-line done" id="ln-0"` |
| 标记当前 | `class="phase-circle pending" id="ph-1"` → `class="phase-circle current" id="ph-1"` |
| label 活跃 | `<div class="phase-label" id="lb-1">` → `<div class="phase-label active" id="lb-1">` |

**Phase ID 对照表**：

| Phase | circle id | line id | label id |
|:--|:--|:--|:--|
| 0 | ph-0 | ln-0 | lb-0 |
| 1 | ph-1 | ln-1 | lb-1 |
| 2 | ph-2 | ln-2 | lb-2 |
| 3 | ph-3 | ln-3 | lb-3 |
| 4 | ph-4 | ln-4 | lb-4 |
| 5 | ph-5 | ln-5 | lb-5 |
| 6 | ph-6 | — | lb-6 |

## 3. 就绪 badge（按 phase 产出更新）

| Phase 完成 | 更新 badge |
|:--|:--|
| Phase 0 | `base_0`(资产提取)→✅ |
| Phase 1 | `base_1`(画风基准)→✅ |
| Phase 2 | `base_2`(美术设定集)→✅ |
| Phase 3 | `deriv_0`(封面图)→✅ |
| Phase 4 | `deriv_1`(人物OC)→✅ |
| Phase 5 | `deriv_2`(场景图)→✅ |
| Phase 6 | `deriv_3`(漫画)→✅ |

badge 示例：`<!--STATE:base_0 -->❌<!--/STATE:base_0 -->` → `<!--STATE:base_0 -->✅<!--/STATE:base_0 -->`

## 4. 创意摘要

- Phase 1 完成后：`book_name`、`genre`、`style_base`
- Phase 2 完成后：`core_char`（核心角色名）

## 5. 最近产出追加（每次 phase 完成都追加）

- old: `<!--STATE:outputs_start-->`
- new: `<!--STATE:outputs_start-->\n        <tr><td>{Phase名}</td><td class="file-path">{产出文件路径}</td><td>{时间}</td></tr>`
