# step-2 落盘燃料 + 机制文档

> 本文件是 pop-qidian-research 第二步执行指令。进入前 step-1 草稿已通过质量门。

## 目标

把 step-1 草稿正式落盘为两个库层文件，均带元数据。这是 content-mechanics.md 从"分流建议"升级为正式落盘的核心修复（owner=research，PRD §4.2）。

## 落盘清单

| 文件 | 模板 | owner | read_policy | primary_consumer |
|:-----|:-----|:------|:------------|:-----------------|
| `涌现/research-写作燃料.md` | `templates/fuel-doc.tpl.md` | research | full-if-targeted | review |
| `涌现/content-mechanics.md` | `templates/mechanics-doc.tpl.md` | research | full-if-targeted | review |

owner / read_policy / primary_consumer 见 PRD §4.2，命名见 PRD §4.3。

## 执行

### 1. 读取模板

```powershell
Get-Content -Encoding UTF8 -Raw templates/fuel-doc.tpl.md
Get-Content -Encoding UTF8 -Raw templates/mechanics-doc.tpl.md
```

### 2. 落盘 research-写作燃料.md

写入 `涌现/research-写作燃料.md`。文件名唯一，禁用 `燃料库.md` 别名（PRD §4.3）。开头元数据块必填：`doc_type: research` / `read_policy: full-if-targeted` / `primary_consumer: review` / `last_updated`。填充章节：

- 资料覆盖声明（已读 / 用户描述 / 模型推断 / 禁止外推）
- 本书涌现燃料表（燃料 / 来源 / 可触发事件 / 主角操作点 / 可外显爽点 / 风险）
- 外部燃料表（燃料 / 已读范围 / 短复述 / 本项目转译 / 不照搬）
- 可筛入 current-state 的近期燃料 / 中期保留燃料 / 禁用燃料
- Content Mechanics 分流建议表（指向 content-mechanics.md）

### 3. 落盘 content-mechanics.md

写入 `涌现/content-mechanics.md`。开头元数据块必填：`doc_type: mechanics` / `read_policy: full-if-targeted` / `primary_consumer: review` / `last_updated`。填充章节：

- 机制分流表（机制名称 / 来源 / 能否迁移 / 正确路由 / 禁止误用）
- 机制明细

**核心修复**：不能直接迁移的机制必须在此正式落盘，不再只停留在燃料文档的"分流建议"里。trial 模式不落盘。

### 4. 回复

采用 PRD §4.7 统一回复格式：

```markdown
本次采用 skill：pop-qidian-research
execution.mode：{formal|draft|trial}

{燃料条数、主燃料摘要、content-mechanics 落盘条数}

下一步：建议执行 pop-qidian-review 初始化/更新 current-state，把近期燃料筛入。
```

## 质量门

- 两个文件均已落盘，元数据块完整（trial 除外）。
- content-mechanics.md 非空（有不能迁移的机制即落盘，draft/formal）。
- 燃料文档无 `燃料库.md` 别名引用。
- 内容机制未伪装成文风特征交给 soul/write。
- 不写正文、不排章纲。
