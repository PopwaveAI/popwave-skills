---
name: novel-style-engine
description: 写法引擎 —— 从用户投喂的样本中抽取文风特征，编译成可注入 prompt 的写作约束。整合 AI-NWA 写法引擎 6 层结构 + 3 强度档 + 5 任务模板。当用户说"学这个文风"、"提取写法"、"投喂样本"、"我想要 XX 风格"、"看这个的味道"、"反 AI 化"、"编译写法" 等时触发。是本套件相对其他 AI 写作工具的核心差异化模块。
---

# Novel Style Engine —— 写法引擎

## 功能

把"我想写得像 XXX"转化成可执行的写作约束。完整流程：

```
样本投喂 → 客观统计 + 主观抽取 → 特征池 → 编译 → 5 个 prompt block → 注入到 writer
```

完成后写法约束自动在 `novel-chapter` 写作时注入。

## 数据模型

整套写法资产保存在 `style/` 目录：

```
style/
├── _index.md           # 档案注册表
├── samples/            # 用户投喂的样本（手放或粘贴）
│   ├── ref-001-{slug}.md
│   └── ...
├── features.md         # 抽取出的特征池（核心数据）
├── anti-ai.md          # 反 AI 规则（forbidden/risk/encourage）
└── compiled/           # 编译后的 prompt block
    ├── global-context.md
    ├── style-rules.md
    ├── anti-ai.md
    ├── output-format.md
    └── self-check.md
```

## 工作流

### A. 投喂样本

用户可以：
- **直接粘贴**：在对话中粘贴 1-5 段文本，本 skill 把它存到 `style/samples/ref-NNN-{slug}.md`
- **放文件**：用户手动放文件到 `style/samples/`，跟 skill 说"我放了 3 个样本"

每个样本文件用 frontmatter 标注来源：

```markdown
---
source: "诡秘之主 第 1 章"
author: "爱潜水的乌贼"
genre: 玄幻
sample-id: ref-001
notes: "我想学的就是开头这段的悬疑感"
---

{样本文本}
```

**建议**：每本书 3-5 个样本足够。太多会让特征"平均化"——失去个性。

### B. 特征抽取（extract）

调用：

```bash
python3 novel-suite/skills/novel-style-engine/scripts/extract_style.py --samples style/samples/ --out style/features.objective.json
```

脚本输出 **客观统计**（JSON）：
- 平均句长（汉字）
- 句长标准差
- 平均段长（句数）
- 段长标准差
- 标点频率（句号 / 逗号 / 分号 / 破折号 / 引号 / 感叹号 / 问号 / 省略号）
- 词频 top 30
- 对话占比（引号字数 / 总字数）

然后 **本 skill 调 LLM** 抽取 **主观特征**（让 LLM 看样本文本，输出结构化分析）：

LLM prompt（在本 skill 内自动调用，无需用户介入）：

```
我会给你 {N} 段样本文本。请提取这些样本共同的写法特征。

每条特征用以下结构：
- enabled: true
- weight: <0.0-1.0>
- category: <narrative / character-voice / language / rhythm>
- rule: "<一句话规则，如'用动作和神态表现情绪，不用形容词直述'>"
- example-good: "<样本中的正面例证>"
- example-bad: "<反例，可虚构>"

要求：
- 提取 8-15 条特征
- 每个 category 至少 2 条
- weight 是这条特征在样本中的稳定程度（出现频率高 + 一致 = 高 weight）
- 不要泛泛而谈"语言生动"——要具体说"用什么方法做到生动"

输出 markdown，可直接拼接到 style/features.md
```

把客观统计 + 主观特征合并写入 `style/features.md`：

```markdown
---
type: style-features
sources:
  - ref-001-诡秘之主第1章
  - ref-002-诡秘之主第3章
last-extracted: 2026-05-20
---

## 客观特征

- avg-sentence-length: 14
- sentence-std: 8.2 (长短交替)
- avg-paragraph-length: 2.3 句
- paragraph-std: 1.1
- punctuation-density:
    period: 0.06
    comma: 0.12
    em-dash: 0.00       # 样本基本不用破折号
    quote: 0.08
    exclaim: 0.01
    question: 0.02
- dialogue-narrative-ratio: 0.22
- top-words: ["他", "的", "是", "了", "一", ...]

## 主观特征（特征池）

### narrative
- enabled: true
  weight: 0.85
  rule: "用动作和神态表现情绪，不用形容词直述"
  example-good: "他握紧拳头，指节发白"
  example-bad: "他很愤怒"
- enabled: true
  weight: 0.70
  rule: "环境描写优先建立现场感，再展开人物动作"

### character-voice
- enabled: true
  weight: 0.75
  rule: "主角内心 OS 多，常用反问"
  example-good: "这就是所谓的命运？"
- ...

### language
- ...

### rhythm
- ...
```

### C. 反 AI 规则（anti-ai）

`style/anti-ai.md` 包含三段（forbidden / risk / encourage），从 `references/anti-ai-rules.md` 拷贝默认值，用户可在样本抽取后调整。

```markdown
---
type: anti-ai-rules
---

## forbidden（绝对禁止）

- pattern: "不是.+而是"
  description: "AI 特征句式"
  weight: 1.0

- pattern: "——"
  description: "破折号在网文中是 AI 痕迹"
  weight: 1.0

- pattern: "值得注意的是|核心在于|关键在于"
  description: "学术报告腔"
  weight: 1.0

## risk（频次监控）

- pattern: "突然|忽然|猛然"
  max-per-3000: 1
  description: "AI 常用突兀转折词"

- pattern: "似乎|可能|或许|大概"
  max-density-per-1000: 3
  description: "套话密度过高语气模糊"

## encourage（鼓励出现）

- description: "感官描写（视/听/嗅/触/味）每场景至少 2 类"
  weight: 0.7

- description: "用具体细节而非抽象总结"
  weight: 0.8
```

### D. 编译（compile）

调用：

```bash
python3 novel-suite/skills/novel-style-engine/scripts/compile_style.py --vault {vault} --task chapter
```

参数说明：
- `--task`：任务类型，决定编译策略（详见 references/compiler-spec.md）：
  - `chapter` / `continue` / `polish` / `rewrite` / `fix-ai`

脚本读取 `style/features.md` + `style/anti-ai.md` + `story.md`，输出 5 个 prompt block 到 `style/compiled/`：

| 文件 | 内容 |
|---|---|
| `global-context.md` | story 圣经摘要 + 当前任务上下文（Layer 1） |
| `style-rules.md` | 主写法规则（Layer 2，4 sub-categories）|
| `anti-ai.md` | 反 AI 约束（Layer 4，三段）|
| `output-format.md` | 输出格式要求（Layer 5） |
| `self-check.md` | 自检指令（Layer 6） |

**Layer 3 角色表达校正层** 是动态的：由 `novel-chapter` 在写作时按本章 POV 角色读对应 character.md，不预编译。

### E. 编译策略：3 强度档

`compile_style.py` 按 feature weight 选择措辞：

| 权重区间 | 档位 | 措辞 |
|---|---|---|
| 0.85 - 1.00 | 高强度 | "必须 / 禁止 / 不得 / 只能" |
| 0.65 - 0.84 | 中强度 | "优先 / 注意避免 / 警惕" |
| 0.30 - 0.64 | 低强度 | "尽量 / 倾向 / 可适当" |
| < 0.30 | 不编译 | （太弱，不输出）|

示例同一条规则在不同档位下的编译结果（"禁止解释心理"）：

- 高强度：`禁止直接解释人物心理，不得使用"他感到"、"他意识到"等表达`
- 中强度：`尽量不要直接解释人物心理，优先通过动作和对话体现情绪`
- 低强度：`心理描写倾向于行为化，可适当保留少量直接陈述`

### F. 编译策略：5 任务模板

不同任务用不同 prompt 装配：

| 任务（--task） | 写法规则 | 反 AI | 自检 | 额外约束 |
|---|---|---|---|---|
| chapter（默认） | 高强度 | 强 | 开 | 字数 word-target |
| continue（续写） | 高强度 | 强 | 开 | "保持前文气质，禁止突然升华" |
| polish（润色） | 中强度 | 中 | 开 | "不增剧情，不改人物关系" |
| rewrite（改写） | 高强度 | 高 | 开 | "保留事实，替换表达" |
| fix-ai（AI 味修正） | 仅反 AI 强 | 高 | 关 | "只修违规点，附违规报告" |

### G. 多层绑定（v0.2）

写法可以绑定到不同层级：

```yaml
# 在 story.md 顶层
style-binding:
  - target: novel              # 全书
    profile: features.md       # 全书写法
  - target: arc:arc-1           # 卷一
    profile: features-arc1.md  # 卷一特殊写法
  - target: chapter:ch-008      # 单章
    profile: features-ch8.md   # 特殊章节
  - target: pov:sera-voss       # 某 POV
    profile: features-sera.md  # sera 视角的写法（如内心戏更多）
```

**合并规则**（越具体越优先）：
- 任务级 > 角色视角级 > 章级 > 卷级 > 全书级
- 同字段冲突取高优先级
- forbidden 三态 union（任何层级 forbidden 即 forbidden）

v0.1 暂只支持全书级（single binding），v0.2 加多层。

## 显式管理操作

### "看一下当前文风"

读 `style/features.md` 和 `style/compiled/`，把启用的特征列出来给用户：

```
📚 当前写法档案（来自 2 个样本）

启用的特征（按权重排序）：

[narrative]
✓ 0.85 用动作和神态表现情绪，不用形容词直述
✓ 0.70 环境描写优先建立现场感

[character-voice]
✓ 0.75 主角内心 OS 多，常用反问

[language]
✓ 0.80 段落控制在 3 句话以内

[rhythm]
✓ 0.65 长短句交替

[anti-ai forbidden]
✗ 不是.+而是 句式
✗ 破折号 ——
✗ 学术报告腔 (值得注意的是 等)

下次写作会注入以上约束。
```

### "停用某条特征"

修改 `style/features.md` 把对应 `enabled: true` 改为 `false`，然后重新编译。

### "调权重"

修改 `style/features.md` 的 weight 值，然后重新编译。

### "添加新样本"

把新样本扔进 `style/samples/`，重跑 extract → compile。

### "重置写法"

清空 `style/features.md`（保留 frontmatter），重做 extract。

## 与其他 skill 的边界

- **不写正文**：那是 `novel-chapter`
- **不改角色 voice**：voice 是 `novel-characters` 的事；写法引擎管全书共通的"叙事方式"
- **不评判用户的样本好不好**

## 输出

每次跑完 compile 后给用户：

```
✅ 写法已编译。
- 启用特征：12 条
- 反 AI 规则：3 forbidden + 5 risk + 4 encourage
- 输出文件：style/compiled/{5 files}

下次写章节时会自动注入。
```
