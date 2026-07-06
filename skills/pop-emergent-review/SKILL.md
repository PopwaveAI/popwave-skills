---
name: pop-emergent-review
description: 当用户说'审稿/review/更新current-state/涌现式review/ledger'时启用。审稿、检查爽不爽/AI味/种子兑现/燃料入戏/正文漂移，把设定/人物/剧情线/燃料/伏笔压缩成下一次 write 必读的 current-state.md；不直接重写正文。
---

# Pop Emergent Review

审稿 + ledger。核心产物不是长评，而是新版 `涌现/current-state.md`——把"长出来的东西"变成下一次 write 必须消费的入口。

## 红线

1. 读取 skill 文件用 `Get-Content -Encoding UTF8 -Raw`，禁用 Read 工具。
2. 创建必须双文件：SKILL.md + skill.json。
3. 版本三处一致：SKILL.md + skill.json + CHANGELOG.md。
4. 不直接重写正文。
5. review 核心产物是更新 current-state，不是长评。
6. current-state 更新必先归档旧版到 `压缩归档/current-state-{YYYYMMDD}-{章位}.md`，再覆盖（见 PRD §4.4）。
7. review-沉淀.md 必追加不删改历史（append-only）。

## 速查表

| 文件 | 读取时机 |
| --- | --- |
| steps/step-1-audit.md | 执行审稿 6 步 SOP 时加载 |
| steps/step-2-commit.md | 沉淀分流与落盘 current-state/归档/沉淀时加载 |
| templates/current-state.tpl.md | step-2 落盘新版 current-state 前读 |
| ../pop-emergent/references/v3.5-pipeline-prd.md | 对齐骨架/owner/命名/历史层规则时读 |

骨架/owner/命名/execution.mode/回复格式统一引用 PRD §4：`../pop-emergent/references/v3.5-pipeline-prd.md`。

## execution.mode

引用 PRD §4.5，不在此重复三档表。本 skill 的 formal 必读输入：已读待审正文、`涌现/current-state.md`、`涌现/soul.md`。

## 强弱加载保障

- 强加载：红线、速查表、PRD §4 契约引用（每轮必读）。
- 弱加载：step-1/step-2/templates 按场景按需加载；关键约束已在红线自包含。

## 回复格式

采用 PRD §4.7 统一格式（本次采用 skill / execution.mode / 专属产出摘要 / 下一步）。专属摘要含：总判断、最影响阅读的 3 个问题、current-state 更新与归档状态、待确认修改。

## 版本

v3.5.0 | 2026-07-06 | 四层架构对齐 + 历史层职责分离 → CHANGELOG.md
