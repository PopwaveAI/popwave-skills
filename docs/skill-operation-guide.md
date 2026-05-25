# Skill 新增与修改操作手册

本文面向不熟悉代码开发的 Skill 作者，说明如何在 Popwave Skills 仓库中新增或修改一个 Skill。

仓库地址：https://github.com/PopwaveAI/popwave-skills

你不需要理解完整的程序构建流程，但需要能完成以下几件事：

- 打开仓库文件。
- 编辑 Markdown 文档。
- 按步骤填写 `skill.json`。
- 使用本地命令完成检查。
- 提交 PR 等待合并发布。

## 一、先了解 Skill 是什么

一个 Skill 是一组放在同一个文件夹里的说明和配置，用来告诉泡泡应用：

- 这个 Skill 叫什么。
- 什么时候应该使用它。
- 它能读取或修改哪些内容。
- 它应该按照什么流程完成任务。
- 用户或模型需要参考哪些资料。

每个 Skill 都放在：

```text
skills/<skill-id>/
```

例如：

```text
skills/example-writing/
```

## 二、一个 Skill 文件夹里通常有什么

```text
skills/<skill-id>/
  skill.json
  SKILL.md
  CHANGELOG.md
  README.md
  references/
  examples/
  scripts/
```

常用文件说明：

| 文件或文件夹 | 用途 | 是否必须 |
| --- | --- | --- |
| `skill.json` | 给应用读取的配置文件，包括名称、版本、权限等 | 必须 |
| `SKILL.md` | 给模型读取的核心说明，描述何时使用、怎么执行、输出什么 | 必须 |
| `CHANGELOG.md` | 记录每个版本改了什么 | 必须 |
| `README.md` | 给人看的说明，比如这个 Skill 的用途和维护注意事项 | 建议填写 |
| `references/` | 放较长的背景资料、规则、参考文档 | 可选 |
| `examples/` | 放示例输入、示例输出 | 可选 |
| `scripts/` | 放脚本工具，通常由技术同事维护 | 可选 |

## 三、新增 Skill

### 1. 确定 Skill ID

Skill ID 是文件夹名，也会出现在配置里。建议使用英文小写、数字和连字符。

推荐：

```text
novel-outline
brand-review
meeting-summary
```

不推荐：

```text
小说大纲
Brand Review!
meeting summary
```

### 2. 创建 Skill 文件夹

如果你会使用命令行，可以在仓库根目录运行：

```bash
npm run skills:new -- novel-outline
```

其中 `novel-outline` 换成你的 Skill ID。

运行后会自动创建：

```text
skills/novel-outline/
  skill.json
  SKILL.md
  CHANGELOG.md
  README.md
```

如果你不会使用命令行，可以复制已有的 `skills/example-writing/` 文件夹，粘贴后改名为新的 Skill ID。复制后一定要修改里面的 `skill.json` 和文档内容，不能保留示例 Skill 的说明。

### 3. 修改 `skill.json`

打开：

```text
skills/<skill-id>/skill.json
```

重点填写这些字段：

```json
{
  "id": "novel-outline",
  "version": "0.1.0",
  "displayName": "小说大纲助手",
  "description": "帮助用户根据题材、人物和世界观生成结构清晰的小说大纲。",
  "entry": "SKILL.md",
  "activation": {
    "slashCommands": ["novel-outline"],
    "default": false
  },
  "permissions": {
    "readProjectFiles": true,
    "writeProjectFiles": true,
    "network": false,
    "shell": false
  },
  "loadPolicy": {
    "includeReferences": "on-demand",
    "maxPromptChars": 50000
  }
}
```

填写建议：

| 字段 | 怎么填 |
| --- | --- |
| `id` | 必须和文件夹名一致 |
| `version` | 新 Skill 通常从 `0.1.0` 开始 |
| `displayName` | 给用户看的名称，可以用中文 |
| `description` | 一句话说明这个 Skill 能帮用户完成什么 |
| `slashCommands` | 通常和 `id` 一致 |
| `readProjectFiles` | 是否需要读取项目文件 |
| `writeProjectFiles` | 是否需要修改或生成项目文件 |
| `network` | 是否需要联网 |
| `shell` | 是否需要执行命令 |
| `includeReferences` | 推荐保持 `on-demand`，需要时再读取参考资料 |
| `maxPromptChars` | 一般保持默认值即可 |

权限填写原则：

- 不需要联网，就把 `network` 设为 `false`。
- 不需要执行命令，就把 `shell` 设为 `false`。
- 只读资料、不写文件时，可以把 `writeProjectFiles` 设为 `false`。
- 不确定时，先选择更少的权限，再请技术同事确认。

### 4. 编写 `SKILL.md`

打开：

```text
skills/<skill-id>/SKILL.md
```

建议使用下面的结构：

```markdown
---
name: novel-outline
description: 当用户需要创作小说大纲、章节规划或故事结构时使用。
---

# 小说大纲助手

## 目标

帮助用户把零散想法整理成可继续写作的小说大纲。

## 什么时候使用

- 用户要求生成小说大纲。
- 用户要求整理人物、世界观、冲突线。
- 用户要求把故事想法扩展成章节规划。

## 输入要求

优先使用用户提供的题材、主角、背景、篇幅、风格和限制条件。

如果关键信息缺失，可以先给出一个合理假设，并在输出中标明。

## 工作流程

1. 先确认用户真正要的是大纲、章节规划、人物设定还是世界观整理。
2. 提取已有信息，不要编造与用户设定冲突的内容。
3. 按“核心卖点、主线冲突、人物弧光、章节结构、后续建议”组织输出。
4. 输出应具体、可继续创作，避免空泛评价。

## 输出格式

使用 Markdown 输出，包含：

- 故事一句话概括
- 主要人物
- 主线冲突
- 分章节大纲
- 可继续补充的问题

## 质量标准

- 逻辑清楚。
- 不覆盖用户已有设定。
- 不使用空泛套话。
- 每个章节都要有明确推进作用。
```

写作要点：

- 写“什么时候使用”，不要只写“这是一个好用的工具”。
- 写“具体怎么做”，不要只写“帮助用户完成任务”。
- 写“输出格式”，让结果稳定。
- 写“质量标准”，告诉模型什么算好。
- 如果有禁止事项，也要明确写出来。

### 5. 编写 `README.md`

打开：

```text
skills/<skill-id>/README.md
```

这是给维护者看的说明。可以简单写：

```markdown
# 小说大纲助手

用于帮助用户生成小说大纲、章节规划、人物关系和故事主线。

## 适用场景

- 用户已有一个故事想法，需要扩展成大纲。
- 用户需要把人物、冲突和章节整理清楚。

## 维护说明

- 修改核心流程时，需要同步更新 `SKILL.md`。
- 增加参考资料时，建议放入 `references/`。
```

### 6. 更新 `CHANGELOG.md`

打开：

```text
skills/<skill-id>/CHANGELOG.md
```

新 Skill 可以写：

```markdown
# Changelog

## 0.1.0 - 2026-05-25

- 新增小说大纲助手 Skill。
```

日期请填写实际修改日期。

### 7. 检查 Skill 是否能通过校验

如果你会使用命令行，在仓库根目录运行：

```bash
npm install
npm run build
```

如果命令运行成功，说明基本格式没有问题。

如果你不会使用命令行，请在提交 PR 前请技术同事帮你运行这两条命令。

## 四、修改已有 Skill

### 1. 找到要修改的 Skill

所有 Skill 都在：

```text
skills/
```

例如要修改中文网文调研 Skill，就打开：

```text
skills/cnovel-research/
```

### 2. 判断这次修改属于哪一种

常见修改类型：

| 修改类型 | 例子 | 需要改哪些文件 |
| --- | --- | --- |
| 改说明文字 | 优化表达、补充注意事项 | `SKILL.md`、`CHANGELOG.md` |
| 改输出格式 | 增加一个输出小节、调整表格字段 | `SKILL.md`、`CHANGELOG.md`、可能需要改 `README.md` |
| 增加参考资料 | 新增行业资料、规则说明、案例 | `references/`、`SKILL.md`、`CHANGELOG.md` |
| 增加能力 | 从“只生成大纲”变成“也能生成章节细纲” | `SKILL.md`、`skill.json`、`CHANGELOG.md` |
| 修改权限 | 新增联网、执行脚本、写文件能力 | `skill.json`、`SKILL.md`、`CHANGELOG.md` |

### 3. 修改对应文件

优先修改最少的内容。不要在一次修改里同时做很多无关调整。

推荐做法：

- 只解决这次明确的问题。
- 保留原有结构。
- 不删除还在使用的说明。
- 如果不确定某段是否可以删，先加备注或请同事确认。

### 4. 更新版本号

打开：

```text
skills/<skill-id>/skill.json
```

找到：

```json
"version": "0.1.0"
```

按下面规则更新：

| 修改程度 | 版本变化 | 例子 |
| --- | --- | --- |
| 小修小补 | `0.1.0` -> `0.1.1` | 改错别字、优化提示词、补充例子 |
| 增加兼容能力 | `0.1.0` -> `0.2.0` | 新增一种输出形式，但不影响旧用法 |
| 重大变化 | `0.1.0` -> `1.0.0` | 改变输入要求、输出结构、权限或文件布局 |
| 内部测试版 | `0.2.0-beta.1` | 还不想正式发布，只给内部验证 |

简单判断方法：

- 用户几乎感知不到，只是更准确：改最后一位。
- 用户会看到新能力，但旧用法还能继续用：改中间一位。
- 用户原来的使用方式可能会失效：改第一位。

### 5. 更新 `CHANGELOG.md`

每次修改都要记录。格式示例：

```markdown
## 0.1.1 - 2026-05-25

- 优化章节大纲输出要求，要求每章必须包含冲突推进。
- 补充人物弧光的写作注意事项。
```

注意：

- 版本号要和 `skill.json` 里的 `version` 一致。
- 日期写实际修改日期。
- 用用户能看懂的话描述变化。

### 6. 检查修改是否通过

在仓库根目录运行：

```bash
npm run build
```

如果没有报错，可以提交 PR。

如果报错，常见原因包括：

- `skill.json` 不是合法 JSON，例如少了逗号或多了逗号。
- `version` 格式不对，例如写成了 `v1.0`。
- `description` 太短。
- `id` 和文件夹名不一致。

## 五、提交 PR 前检查清单

提交前请逐项确认：

- [ ] Skill 文件夹放在 `skills/<skill-id>/` 下。
- [ ] `skill.json` 里的 `id` 和文件夹名一致。
- [ ] `skill.json` 里的 `version` 已更新。
- [ ] `SKILL.md` 写清楚了使用场景、工作流程和输出格式。
- [ ] `CHANGELOG.md` 已记录本次版本变化。
- [ ] 没有把账号、密码、Token、Access Key 等敏感信息写进仓库。
- [ ] 如果新增联网或执行命令能力，已经在 `skill.json` 中声明，并请技术同事确认。
- [ ] 已运行或请人运行 `npm run build`。

## 六、发布后会发生什么

PR 合并后，GitHub Actions 会自动：

1. 校验所有 Skill。
2. 构建 Skill 压缩包。
3. 生成 `dist/registry.json`。
4. 把 `dist/` 发布到国内对象存储和 CDN。

泡泡用户刷新 Skills 后，就可以安装新版本。项目会在：

```text
.paopao/skills/config.json
```

中记录并锁定已安装的版本。

## 七、常见问题

### 我不会使用命令行怎么办？

可以只负责编辑 `SKILL.md`、`README.md`、`CHANGELOG.md` 和 `skill.json`。提交前请技术同事帮你运行：

```bash
npm run build
```

### `skill.json` 很容易写错怎么办？

建议从已有 Skill 复制一份，再只修改必要字段。修改 JSON 时注意：

- 英文双引号不能省略。
- 每一项之间通常需要英文逗号。
- 最后一项后面不要加逗号。
- `true` 和 `false` 不要加引号。

### 什么内容应该放进 `references/`？

适合放入 `references/` 的内容包括：

- 长篇背景资料。
- 固定规则。
- 行业术语说明。
- 示例报告。
- 可复用的评价标准。

不要把太长的资料全部塞进 `SKILL.md`。`SKILL.md` 应该写核心流程，详细资料放在 `references/` 中按需读取。

### 什么时候需要找技术同事？

以下情况建议找技术同事确认：

- 需要联网。
- 需要执行脚本或命令。
- 需要读取或写入大量项目文件。
- 需要新增 `scripts/` 工具。
- 修改可能影响已有用户的使用方式。

## 八、推荐的 PR 描述模板

```markdown
## 本次修改

- 新增/修改了哪个 Skill：
- 主要变化：
- 版本号：

## 验证方式

- [ ] 已运行 `npm run build`
- [ ] 已人工检查 `SKILL.md`
- [ ] 已确认没有敏感信息
```
