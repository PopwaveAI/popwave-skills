# step2 · 路由循环（主agent执行指南）

> 本文件是 pop-visual-pipeline 第三步执行指令。每次对话开始（路由时）执行。

## 目标

读视觉项目总控.html → 判断当前 phase → 路由到对应子 skill → 完成后 SearchReplace 更新 html。

## 执行

### 1. 读视觉项目总控.html

每次对话第一件事，用 Read 读取项目根目录的 `视觉项目总控.html`。

从 `<!--STATE:xxx -->` 标记提取：
- `phase`：当前阶段
- `intent`：本次目标（cover/oc/comic/full/asset-only）
- `next_step`：下一步动作
- `mode`：fresh/import/resume

> **先读 intent 再路由**：intent 决定基建档位和派生层去向。intent 为空时先走意图闸口（见 §2.5）。

### 2. 按 phase + intent 路由

对照 SKILL.md Phase 路由表，路由到对应子 skill：

| phase | 调度 skill | 产出 |
|:------|:-----------|:-----|
| `init` | `pop-visual-asset` | `素材/视觉资产/` |
| `phase1` | `pop-visual-style` | `素材/风格/画风决策.md` |
| `phase2` | `pop-visual-character` | `素材/视觉资产/[角色名]视觉身份卡.md` |
| `phase3` | `pop-visual-cover` | `素材/视觉/封面-{书}-v1.png` |
| `phase4` | `pop-visual-oc` | `素材/视觉/OC-{角色}-v1.png` |
| `phase5` | `pop-visual-cover`(场景) | `素材/视觉/场景-{名}-v1.png` |
| `phase6` | `pop-visual-comic` | `漫画/` |

**基建就绪门禁**：进入派生层（phase3-6）前，必须验证 `素材/视觉资产/[角色名]视觉身份卡.md` 存在。缺失 = 报错中止，提示先跑基建。

**派生层触发规则（按 intent 档位）**：phase3-6 不是线性顺序，**由 intent 决定去哪里**，不是默认推漫画：

| intent | 派生层去向 | 基建档位 |
|:-------|:----------|:---------|
| `cover` | phase3（封面）或 phase5（场景图） | 轻量（可跳过 comic 双角度定妆） |
| `oc` | phase4（人物OC） | 轻量~中（可跳过双角度定妆） |
| `comic` | phase6（漫画） | 完整 |
| `full` | 按需 loop 3-6 | 完整 |
| `asset-only` | 停在 phase0，不进派生层 | 最轻 |

> **建档层面**：`cover`/`oc` 意图时，基建只需到"身份卡"（phase2）即可派生，**不强制跑 phase2 的双角度定妆**（那是 comic 完整档才需要）。`comic` 意图才走完整基建（深度资产+画风定标+身份卡+双角度定妆）。

### 3. 子 skill 执行方式

- **基建层（phase0-2）**：主 agent 直接执行，读子 skill 的 SKILL.md + step 文件，按 SOP 操作
- **派生层（phase3-6）**：主 agent 直接执行或派发子 agent，读子 skill 的 SKILL.md + step 文件

> 子 skill 指令必须显式包含"读取 SKILL.md + step 文件"，禁止依赖 agent 记忆"扮演"skill 功能。

### 4. Phase 完成后更新 总控.html

用 SearchReplace 更新 STATE 字段（只更新本 phase 涉及的）：

#### 4a. 通用更新

| 操作 | SearchReplace 示例 |
|:-----|:--------------------|
| 更新 phase | old: `<!--STATE:phase -->init<!--/STATE:phase -->` → new: `<!--STATE:phase -->phase1<!--/STATE:phase -->` |
| 更新时间戳 | old: `<!--STATE:updated_at -->--<!--/STATE:updated_at -->` → new: `<!--STATE:updated_at -->{当前时间}<!--/STATE:updated_at -->` |
| 更新 next_step | old: `<!--STATE:next_step -->Phase 0: ...<!--/STATE:next_step -->` → new: `<!--STATE:next_step -->{下一步}<!--/STATE:next_step -->` |

#### 4b. Phase circle 更新

| Phase | circle id | line id | label id |
|:------|:----------|:--------|:---------|
| 0 | ph-0 | ln-0 | lb-0 |
| 1 | ph-1 | ln-1 | lb-1 |
| 2 | ph-2 | ln-2 | lb-2 |
| 3 | ph-3 | ln-3 | lb-3 |
| 4 | ph-4 | ln-4 | lb-4 |
| 5 | ph-5 | ln-5 | lb-5 |
| 6 | ph-6 | — | lb-6 |

- 完成: `class="phase-circle pending" id="ph-X"` → `class="phase-circle done" id="ph-X"`
- 连线: `class="phase-line" id="ln-X"` → `class="phase-line done" id="ln-X"`
- 当前: `class="phase-circle pending" id="ph-Y"` → `class="phase-circle current" id="ph-Y"`
- label 活跃: `<div class="phase-label" id="lb-Y">` → `<div class="phase-label active" id="lb-Y">`

#### 4c. 就绪状态更新

| Phase 完成 | 更新 badge |
|:-----------|:-----------|
| Phase 0 | `base_0`(资产提取)→✅ |
| Phase 1 | `base_1`(画风基准)→✅ |
| Phase 2 | `base_2`(人物身份卡)→✅ |
| Phase 3 | `deriv_0`(封面图)→✅ |
| Phase 4 | `deriv_1`(人物OC)→✅ |
| Phase 5 | `deriv_2`(场景图)→✅ |
| Phase 6 | `deriv_3`(漫画)→✅ |

badge 示例: old: `<!--STATE:base_0 -->❌<!--/STATE:base_0 -->` → new: `<!--STATE:base_0 -->✅<!--/STATE:base_0 -->`

#### 4d. 创意摘要更新

- Phase 1 完成后: `book_name`、`genre`、`style_base`
- Phase 2 完成后: `core_char`（核心角色名）

#### 4e. 最近产出追加

在 `<!--STATE:outputs_start-->` 和 `<!--STATE:outputs_end-->` 之间追加一行：

SearchReplace:
- old: `<!--STATE:outputs_start-->`
- new: `<!--STATE:outputs_start-->\n        <tr><td>{Phase名}</td><td class="file-path">{产出文件路径}</td><td>{时间}</td></tr>`

### 5. 继续下一次路由

完成更新后，回到第 1 步重新读总控，判断是否还有下一步：
- **基建层（phase0-2）**：按顺序推进，直到达到 intent 档位所需深度
  - `cover`/`oc`：到 phase2（身份卡）即基建完成，可派生
  - `comic`/`full`：到 phase2 且双角度定妆完成（基建完整）才派生
- **派生层（phase3-6）**：按 intent 路由，完成后回读总控判断是否还有派生目标（`full` 档才 loop）

> **不默认推漫画**：intent 是 `cover`/`oc` 时，基建完成后直接进对应派生，不自动进 phase6 漫画。用户中途改意图 → 更新 intent 字段后按新档位路由。

## 红线

- 每次对话第一件事必须读总控，禁止跳过直接干活
- 基建就绪门禁强制，派生层前必须验证身份卡存在
- pipeline 只做路由不干活，产出由下游 skill 生成