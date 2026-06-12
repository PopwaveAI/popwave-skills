# Skill 设计规范 PRD

## 文档信息
- **来源**: 微信公众号文章《写好 Skill 的 7 条硬规则》
- **原文链接**: https://mp.weixin.qq.com/s/PR5GfjpiJsFXAq3aTmvlFw
- **作者**: 森哥
- **沉淀日期**: 2026-06-10
- **适用对象**: popwave-skills 项目所有 Skill 设计者

---

## 一、核心定位

**Skill 不是提示词，而是给 Agent 用的可复用操作手册。**

Skill 的价值不在于覆盖广度，而在于**减少 Agent 在特定场景下的翻车概率**。

---

## 二、7 条硬规则

### 规则 1：Description 必须写触发场景

**核心原则**: Description 的第一句必须是"用户会怎么问"，而不是"这个 Skill 是做什么的"。

**格式模板**:
```
description: Use when the user asks to <意图1>, <意图2>, or <意图3>. <一句话说明这个 Skill 会怎么做>.
```

**中文模板**:
```
description: 当用户要求<意图1>、<意图2>或<意图3>时使用。<一句话说明这个 Skill 会怎么做>。
```

**测试方法**:
把 Skill 正文全部删掉，只保留 name 和 description。问自己：如果用户说「帮我看看这个 PR 能不能合」，模型能不能准确想到要加载它？

**反例**:
```
❌ description: 这是一个用于代码审查的 Skill，帮助开发者检查代码质量。
```

**正例**:
```
✅ description: 当用户要求检查 PR、排查 CI 失败、审查代码改动能否合并时使用。按 diff→测试→风险→结论的顺序完成审查。
```

---

### 规则 2：只写模型不知道的东西

**核心原则**: Skill 的价值密度取决于 Gotchas 的密度。

**不应该写的内容**:
- Git 基础命令
- Python 基础语法
- 通用 REST API 概念
- 「认真检查」「确保质量」这种空话
- 模型训练语料里已经大量存在的常识

**应该写的内容**:
- 本项目特有的命令
- 本团队特有的流程
- 官方文档没有写但经常踩坑的边界条件
- 工具返回值容易误判的地方
- 看似合理但实际上会失败的做法
- 必须按顺序执行的检查项
- 已经翻车过一次的经验

**判断标准**:
> 如果这段内容换到任何项目都成立，它大概率不该写进 Skill。

**反例**:
```markdown
## How to use Git
1. Use git status to inspect current changes.
2. Use git diff to see modifications.
3. Use git add to stage files.
4. Use git commit to commit changes.
```

**正例**:
```markdown
## Project-specific Git Gotchas
- This repo uses generated files under `src/generated/`; do not manually edit them.
- Always run `pnpm codegen` after changing GraphQL schema files.
- Do not squash commits on release branches; release automation depends on commit boundaries.
- The `main` branch is protected. Use `gh pr create` instead of pushing directly.
```

---

### 规则 3：把 SKILL.md 写成导航页，不要写成百科全书

**核心原则**: SKILL.md 不应该塞满所有细节，它更像地图。

**推荐目录结构**:
```
my-skill/
├── SKILL.md                    # 导航页
├── references/
│   ├── api-gotchas.md          # 重型参考资料
│   ├── release-checklist.md
│   └── troubleshooting.md
├── scripts/
│   ├── check_status.py         # 重复动作脚本
│   └── validate_output.py
├── templates/
│   └── report-template.md      # 固定格式模板
└── assets/
    └── example-config.yaml     # 示例配置
```

**SKILL.md 应该告诉 Agent**:
- 这个 Skill 什么时候用
- 先做什么，后做什么
- 哪些坑必须避开
- 需要更详细信息时去哪个文件
- 哪些动作必须用脚本，而不是靠模型手写
- 做完后怎么验收

**渐进暴露原则**:
不要一上来就让模型背完整税法、完整 API 文档、完整故障手册。先给它目录。它需要哪一页，再让它翻哪一页。

---

### 规则 4：脚本负责重复劳动，文字负责判断经验

**核心原则**: 脚本做确定性执行，Skill 正文解释什么时候跑、怎么看结果、什么情况必须停。

**分工标准**:

| 类型 | 处理方式 |
|------|----------|
| 每次都一样的动作 | 写脚本 |
| 需要判断上下文的经验 | 写说明 |
| 需要固定格式的输出 | 写模板 |
| 需要大量背景细节 | 放 reference |

**反例**:
```markdown
请检查 HTML 是否存在横向溢出、坏图、本地图片路径、Markdown 表格泄漏，并生成 QA 报告。
```

**正例**:
```markdown
Run the runtime QA script before sending preview:
```bash
node scripts/wechat-html-runtime-qa.mjs article.html /tmp/qa-output
```

Interpretation rules:
- `high` issues must be fixed before delivery.
- `localSrc` is acceptable for local preview only; before publishing, upload images to CDN.
- `pipeLeakLines` means the Markdown table was not converted; fix the source Markdown and regenerate HTML.
```

**判断标准**:
不要让模型每次手写 80 行 Python 去检查同一件事。那不是智能，那是浪费。

---

### 规则 5：明确禁止动作，比泛泛鼓励更有用

**核心原则**: Agent 需要的是边界，不是道德教育。

**反例**:
```markdown
Be careful when modifying production data.
```

**正例**:
```markdown
## High-risk actions — do not do without explicit user approval
1. Do not run `git reset --hard` unless the user explicitly approves destructive changes.
2. Do not delete production records directly. Export matching IDs first and ask for confirmation.
3. Do not publish the article draft unless the user says "推" / "发布" / "发出去".
4. Do not edit generated files under `src/generated/`; update the schema and run codegen.
```

**适合写进 Skill 的禁止项**:
- 不可逆操作
- 付费操作
- 发布/推送/群发
- 会影响生产环境的数据修改
- 用户曾经明确打回过的风格
- 看似省事但历史上翻车过的捷径

**原则**: 不要只说「不要」。要告诉 Agent 应该怎么做。

---

### 规则 6：给 Eval，不要靠感觉判断写得好不好

**核心原则**: Skill 写完不是结束，真正的问题是它在真实任务里会不会被正确加载？加载后能不能把事做对？

**Eval 分类**:

1. **Routing Evals** (路由测试):
```markdown
## Routing evals
- 用户请求：帮我看看这个 PR 能不能合
  - Expected skill: pr-review
  - Should load: yes
- 用户请求：CI 又挂了，查一下
  - Expected skill: pr-review
  - Should load: yes
- 用户请求：写一篇公众号文章
  - Expected skill: pr-review
  - Should load: no
```

2. **Task Evals** (端到端测试):
```markdown
## Task evals
### Case 1: CI failure diagnosis
Input: user says "CI failed on PR #123, find the reason"
Expected behavior:
- Inspect PR checks first
- Identify failing job
- Read logs before suggesting fixes
- Do not rerun all tests blindly
- Output root cause + next action
```

**Eval 必须覆盖的三类问题**:
1. 该加载时能加载
2. 不该加载时别加载
3. 加载后能做对

**重要提醒**: 改 description 后必须重跑路由 Eval。

---

### 规则 7：把失败变成 Gotcha 飞轮

**核心原则**: Skill 不可能一次写完。正确维护方式不是定期开大会重构，而是把每次失败沉淀成 Gotcha。

**Gotcha 格式**:
```markdown
## Gotchas
- `web_extract` may fail on dynamic pages. If extraction returns empty content, use browser navigation and `document.body.innerText`.
- SVG `<text>` does not auto-wrap. For long Chinese bullet text, manually split into `<tspan>` lines.
- WeChat article converter treats `---` as the start of the footer section. Do not use `---` as a body separator.
```

**好的 Gotcha 应该包含**:
- 触发场景
- 错误做法
- 为什么错
- 正确做法
- 必要时附验证命令

**维护原则**: append-mostly
- 出现一个真实失败
- 找到可复用原因
- 写成一条具体规则
- 加到 Gotchas / Pitfalls / Checklist
- 下次同类任务不再犯

**反例**:
```markdown
注意不要粗心，之前这里出过错。
```

**正例**:
```markdown
When generating SVG cards, do not assume text wraps automatically. SVG `<text>` renders a single line unless manually split with `<tspan>`. Run visual QA before sending.
```

---

## 三、Skill 模板

### 最小可用版本 (5 块)

```markdown
# Frontmatter
name: my-task-skill
description: Use when <真实用户触发语义>.

# My Task Skill

## When to Use
Use this skill when the user asks to:
- <触发场景1>
- <触发场景2>

Do not use it for:
- <排除场景1>
- <排除场景2>

## Workflow
1. <第一步>
2. <第二步>
3. <第三步>

## Gotchas
- <真实坑1>
- <真实坑2>

## Verification
- [ ] <验证项1>
- [ ] <验证项2>
```

---

## 四、Skill 分类指南

| 类别 | 说明 | 适合内容 |
|------|------|----------|
| 1. Library / API 参考 | 写内部库、SDK、CLI 的正确用法和坑 | 初始化方式、认证方式、常见错误、版本差异 |
| 2. 产品验证 | 告诉 Agent 怎么确认产物真的可用 | 验证流程、检查清单、验收标准 |
| 3. 数据获取和分析 | 把数据源、查询方式、字段含义写清楚 | 业务字段的真实含义、查询示例 |
| 4. 业务流程自动化 | 日报、工单、会议纪要、发布清单 | 流程步骤、审批节点、输出格式 |
| 5. 代码脚手架 | 新建模块、新建迁移、新建插件 | 模板和命令 |
| 6. 代码质量 / 审查 | 审查标准、项目禁忌、测试要求 | 审查清单、输出格式 |
| 7. CI/CD / 部署 | 部署顺序、回滚方式、环境差异 | 发布前检查、回滚命令 |
| 8. 应急预案 | 症状→排查命令→判断分支→报告格式 | 强调不要直接修，要先定位 |
| 9. 基础设施运维 | 成本排查、孤儿资源清理、权限检查 | 风险高，要把审批边界写清楚 |

---

## 五、写作前自查 6 问

1. **用户会用什么话触发这个 Skill？**
2. **没有这个 Skill，Agent 最容易在哪里犯错？**
3. **哪些知识是模型不知道、但你知道的？**
4. **哪些步骤是重复劳动，应该写成脚本？**
5. **哪些动作有风险，必须禁止或要求确认？**
6. **做完之后，怎么验证真的成功？**

**判断标准**:
- 如果第 2 个问题答不上来，这个 Skill 可能根本不需要写。
- 如果第 3 个问题答不上来，它大概率只是常识文档。
- 如果第 6 个问题答不上来，这个 Skill 很难闭环。

---

## 六、什么时候不要写 Skill

| 不要写的情况 | 原因 |
|--------------|------|
| 模型已经知道的常识 | 比如「如何使用 Git」「如何写 Python 函数」 |
| 变化快于维护速度的信息 | 比如某个网站今天的按钮位置、临时 API |
| 一次性任务 | 只做一次的东西，写在当前任务说明里就够了 |
| 系统 prompt 已经覆盖的规则 | 不要在每个 Skill 里重复系统层规则 |
| 范围过大的超级 Skill | 比如 `name: software-engineering` |

---

> **最终判断标准**: Skill 写得好不好，只看一件事——下一次 Agent 遇到同类任务，会不会因为它少犯一个错。

---

*来源：森哥《写好 Skill 的 7 条硬规则》+ Anthropic/Perplexity 实践经验，2026-06-10 沉淀*
