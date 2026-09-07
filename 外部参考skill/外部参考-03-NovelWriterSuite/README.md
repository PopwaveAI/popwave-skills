# Novel Suite

> 中文长篇小说创作的 Claude Code skill 套件 —— **一本小说 = 一个 Obsidian vault = 一个 git repo**。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-7C3AED)](https://docs.anthropic.com/claude/docs/claude-code)
[![Status](https://img.shields.io/badge/Status-v0.1.0-blue)](CHANGELOG.md)

---

## 是什么

把"写长篇小说"这件事拆成 10 个互相协作的 Claude Code skill：从创意构思 → 世界观 → 角色 → 卷纲 → 文风学习 → 章节写作循环 → 长期记忆 → 校稿。

所有产物是纯 markdown（带 YAML frontmatter），可直接拖进 Obsidian 当 vault，也可以 git 版本化。

## 套件包含的 skill

| Skill | 触发短语 | 用途 |
|---|---|---|
| `novel-init` | "开始写小说" / "新建小说项目" | 项目脚手架 |
| `novel-brainstorm` | "讨论世界观" / "想剧情" | 对话式创意构思 |
| `novel-worldbuilding` | "构建世界观" / "加地点" | 世界观资产管理 |
| `novel-characters` | "加角色" / "角色关系" | 角色卡 + 关系图 |
| `novel-plot` | "卷纲" / "伏笔" / "时间线" | 情节结构 + 伏笔账 |
| `novel-style-engine` | "学这个文风" / "提取写法" | 文风学习与编译 |
| `novel-memory` | (自动触发) | 长期记忆管理 |
| `novel-chapter` | "写第 X 章" / "继续写" | 章节写作循环 |
| `novel-review` | "校稿" / "审一遍" | 37 维质量审查 |
| `novel-adapt` | "转剧本" / "做分镜" | 格式转换（v0.2 规划）|

## 安装

### Claude Code（推荐）

```bash
# 方式 1: 从 marketplace 安装（需要项目托管在公开 GitHub 仓库）
/plugin marketplace add alonegg/novel-suite
/plugin install novel-suite@novel-suite

# 方式 2: 直接 clone 到 skills 目录
git clone https://github.com/alonegg/novel-suite.git ~/.claude/skills/novel-suite
```

重启 Claude Code 后，说"我想写一本小说"即可触发 `novel-init`。

### 其他 SKILL.md 兼容工具

适配 Cursor / Windsurf / Codex / Gemini CLI / OpenCode 等支持 [Agent Skills](https://agentskills.io) 标准的工具：

```bash
git clone https://github.com/alonegg/novel-suite.git
cp -r novel-suite/skills/* <your-skills-dir>/
```

具体 skills 目录位置请查阅对应工具的文档。

## 快速开始

```
你：我想写一本小说
→ 触发 novel-init，问几个基本字段（书名/题材/视角/基调），搭建 vault 目录

你：开始 brainstorm
→ 触发 novel-brainstorm，对话式收敛一句话简介、核心矛盾、30 章承诺

你：加一个主角
→ 触发 novel-characters，建角色卡

你：构建世界观
→ 触发 novel-worldbuilding，建地点 / 体系

你：做卷纲
→ 触发 novel-plot，设计故事弧 + 卷级章节大纲

你：学这个文风（粘贴样本）
→ 触发 novel-style-engine，抽取写法特征 + 编译

你：写第 1 章
→ 触发 novel-chapter，9 步循环（章纲 → 用户确认 → 写作 → 自检 → 修复 → 记忆更新 → 检查点 → 用户审阅）

你：校稿第 1 章
→ 触发 novel-review，37 维质量审查
```

## Vault 结构

```
{书名}/
├── story.md              # 故事圣经（顶层 frontmatter + 30 章承诺）
├── status.md             # 当前状态（唯一真相源）
├── style/                # 写法档案
│   ├── samples/          # 用户投喂的样本
│   ├── features.md       # 抽取出的写法特征（可编辑权重）
│   ├── anti-ai.md        # 反 AI 规则
│   └── compiled/         # 编译后的 prompt block
├── characters/           # 每个角色一个文件
├── worldbuilding/        # 地点 + 体系
├── plot/                 # 故事弧 + 时间线 + 伏笔账
├── chapters/             # 各章 markdown（章纲 + hook 账 + 正文）
├── deliverables/         # 合稿 / 剧本 / 分镜
└── .memory/              # 长期记忆（8 个 bank）
```

## 关键差异化能力

1. **写法引擎**（差异化核心）
   - 投喂样本 → 客观统计 + LLM 主观抽取
   - 5 任务模板 × 3 强度档 × 6 prompt 层
   - 同规则在 chapter / polish / rewrite / fix-ai 任务下用不同措辞编译

2. **37 维校稿**
   - 4 维统计学（段落变异系数 / 套话密度 / 公式化转折 / 列表化结构）—— Python 脚本
   - 33 维 LLM 评估（OOC / 时间线 / 设定冲突 / 战力崩坏 / 流水账 ...）
   - 伏笔账核对：CJK 2-gram 关键词回声 + 揭1埋1硬底线（番茄文章 10）

3. **长期记忆**
   - 8 bank 分类（chapter-briefs / scene-cards / entity-state / relationship-state / continuity-facts / decision-log / revision-notes / tool-observations）
   - 写新章前自动 load + token 预算控制
   - 写完后自动 update + 实体追踪 + 关系演变

4. **强制确认门**
   - 章纲未确认不允许写作（避免 LLM 自作主张写跑偏）
   - 用户审阅意见自动累积到 `.memory/revision-notes.md`，作为下章写作的"经验进化"输入

5. **检查点机制**
   - 每完成一章自动快照
   - 不满意可一键 rollback 到任意检查点

## 文档

- [docs/DESIGN.md](docs/DESIGN.md) —— 完整设计图（v2.1, 600+ 行，含 9 skill 的详细 spec）
- [docs/AUDIT.md](docs/AUDIT.md) —— 5 候选开源项目的代码级审计依据
- [CHANGELOG.md](CHANGELOG.md) —— 版本变更日志

## 设计致谢

本项目独立实现，借鉴以下开源项目的设计与算法：

- [story-skills](https://github.com/danjdewhurst/story-skills) (MIT) —— vault 骨架结构
- [novel-writer](https://github.com/AI-Practical-Lab/novel-writer) —— 中文网文领域规则、检查点设计
- [inkos](https://github.com/Narcooo/inkos) (AGPL-3.0) —— ai-tells 算法、post-write 硬规则、hook-ledger 算法
- [AI-Novel-Writing-Assistant](https://github.com/ExplosiveCoderflome/AI-Novel-Writing-Assistant) (AGPL-3.0) —— 写法引擎概念架构
- [NovelClaw](https://github.com/iLearn-Lab/NovelClaw) (MIT) —— 16 bank 记忆分类法

详细审计与借鉴对照表见 [docs/AUDIT.md](docs/AUDIT.md)。

## License

[MIT](LICENSE)

## 贡献

欢迎 issue / PR。当前在 dogfood 阶段，准备根据实际写作反馈迭代到 v0.2。

> Made with care for 中文长篇小说作者.
