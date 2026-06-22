# Skill 审计清单

> 用途：Mode B（改造存量 skill）和 Mode D（会话审计）的通用检查清单。
> 执行：改造前先跑此清单，逐项打勾。

## 1. 版本一致性

| # | 检查项 | 判定 |
|:-:|:-------|:-----|
| 1 | SKILL.md frontmatter `version` == SKILL.md 标题中的版本号 | [ ] |
| 2 | SKILL.md 页脚版本 == frontmatter 版本 | [ ] |
| 3 | skill.json `version` == SKILL.md 版本 | [ ] |
| 4 | CHANGELOG 最新条目版本 == 当前版本 | [ ] |

> 不一致 = 🔴 阻塞。统一后再改。

## 2. 文件索引完整性

| # | 检查项 | 判定 |
|:-:|:-------|:-----|
| 1 | `steps/` 下所有 .md 文件都在速查表中列出 | [ ] |
| 2 | `templates/` 下所有文件都在速查表中列出 | [ ] |
| 3 | `references/` 下所有文件都在速查表中列出 | [ ] |
| 4 | 速查表中列出的文件在磁盘上确实存在 | [ ] |

> 缺失或孤儿文件 = 🟡 阻塞。补索引或删死文件。

## 3. 速查表格式

| # | 检查项 | 判定 |
|:-:|:-------|:-----|
| 1 | 分层引导：`### steps/` + `### templates/` + `### references/` + `### 外部依赖` | [ ] |
| 2 | 每行含：什么时候 | 读什么文件 | 产出 | 门禁（step 行） | [ ] |
| 3 | Step 行有门禁列，templates/references 行标 `—` 或不设门禁列 | [ ] |
| 4 | 不冗余：速查表和文件索引不重复列同一信息 | [ ] |

## 4. 路径有效性

| # | 检查项 | 判定 |
|:-:|:-------|:-----|
| 1 | 无 `00-总控/` 路径（已废弃，应为 `状态/`） | [ ] |
| 2 | 无 `设计/卷/volume-XX.md`（已废弃，应为 `剧情设计/卷/卷{N}-卷纲.md`） | [ ] |
| 3 | 无 `设计/幕/act-XX.yaml`（已废弃，应为 `剧情设计/幕/vol-XX/act-YY.md`） | [ ] |
| 4 | 无 `写作资产/设计包/`（已废弃，应为 `章节设计包/`） | [ ] |
| 5 | 无 `chekhov-tracker.md` 独立引用（已并入 act-YY.md） | [ ] |
| 6 | entity-snapshot 路径为 `状态/entity-snapshot.yaml` | [ ] |

## 5. 幽灵引用

| # | 检查项 | 判定 |
|:-:|:-------|:-----|
| 1 | 无 `层架构.md` 引用（已废弃，creative 不再产出） | [ ] |
| 2 | 无 `first-chapter-init.md` 引用（已删除，entity-snapshot 归属 chapter） | [ ] |
| 3 | plot v7.6+ 的 Canvas 引用格式为 markdown 表格（非 yaml `chapters[N].canvas`） | [ ] |

## 6. entity-snapshot 所有权

| # | 检查项 | 判定 |
|:-:|:-------|:-----|
| 1 | entity-snapshot 由 chapter 创建（CH1）和更新（每章设计后） | [ ] |
| 2 | prose 不创建 entity-snapshot，只读取 | [ ] |
| 3 | expert-writer 模板标注 `[chapter 设计后更新，prose 读取]` | [ ] |

## 7. SKILL.md 行数

| # | 检查项 | 判定 |
|:-:|:-------|:-----|
| 1 | 路由型 skill ≤ 120 行 | [ ] |
| 2 | 产文件型 skill ≤ 150 行 | [ ] |
| 3 | 版本历史仅 1 行（页脚），详细版在 CHANGELOG | [ ] |
| 4 | WRONG 示例 ≤ 5 条（取最致命的） | [ ] |
