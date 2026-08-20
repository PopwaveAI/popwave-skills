# Step 2: 提示词组装

> 读取画风DNA → 6段式组装 → 字数检查 → 自检

## 1. 读取输入

从Step 1的输出获取：
- 画风 `dna` + `constraint`（**纯技法层**）
- `content_theme`（该画风原生题材的默认内容层）
- `recommended_lighting` + `recommended_composition`
- 用户的画面描述（场景+人物）

> **画风×内容解耦（铁律❌10）**：`dna` 只描述怎么画，把题材内容词（世界观/服装/建筑/道具）留到 `content_theme` 或用户场景。画风段禁止混入内容元素。

## 2. 6段式组装

读取 `../pop-visual-shared/references/seedream-prompt-guide.md` §一，按6段式结构组装：

```
[质量触发词] + Art style: [dna] [constraint] + [构图策略] + [光影叙事] + [场景] + [人物≤100字]
```

### 各段取值

| 段 | 取值来源 |
|:---|:---------|
| 1 质量触发词 | 固定：`IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed` |
| 2 画风DNA | Step 1选定的 `dna` + `constraint`（**纯技法层，禁止混入内容**） |
| 3 构图策略 | `references/lighting-composition-templates.md` 中CT1/CT2的英文描述 |
| 4 光影叙事 | 同文件中LT1/LT2/LT3的英文描述 |
| 5 场景 | **内容层接入**：用户场景描述优先；若用户未给具体题材或跨题材复用，用 `content_theme` 兜底 |
| 6 人物 | 用户输入的人物描述，≤100字 |

### 内容层接入规则（跨题材复用）

- **用户给了具体场景题材** → 用用户场景描述，`content_theme` 仅作参考，不覆盖用户
- **用户要跨题材复用画风**（如用「国漫玄幻厚涂」画现代都市）→ 场景段用用户提供的现代场景，**技法层不变**，禁止让 `content_theme` 的仙侠元素污染
- **用户没给题材 / 就想要画风原生题材** → 用 `content_theme` 作为场景段兜底

### 画风前置原则（铁律❌2）

画风DNA必须在第2段（紧跟质量触发词后），不放开头也不放末尾。
Phase 0验证：画风前置符合Seedream注意力权重分配机制，风格执行力最强。

## 3. 字数检查

- 英文提示词 ≤600词
- 人物描述 ≤100字
- dna字段 ≤800字符（DNA库已保证）

## 4. 自检

- [ ] 画风DNA从DNA库取（铁律❌1）
- [ ] 画风在第2段（铁律❌2）
- [ ] 光照与画风兼容（铁律❌3）
- [ ] **画风段只含技法，无题材内容词（铁律❌10）**——检查 `dna` 段是否误带世界观/服装/建筑/招数等；内容都在 `content_theme` 或用户场景
- [ ] 人物描述≤100字
- [ ] 总词数≤600
- [ ] 用自然语言连贯描述，非关键词堆叠

## 5. 备选结构

若用户需要文字渲染（书名/角色名等），切换到：
- **V3结构化公式**：见 `../pop-visual-shared/references/seedream-prompt-guide.md` §二
- **高精度4块结构**：见同文件 §三（商业级，含HARD CONSTRAINTS）

> 纯文生图默认用6段式。V3和高精度4块供cover/oc skill跨场景使用。

## 下一步

→ 进入 `step3-generate.md`，确定参数并执行生成
