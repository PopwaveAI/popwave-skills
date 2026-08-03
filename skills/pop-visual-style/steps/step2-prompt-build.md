# Step 2: 提示词组装

> 读取画风DNA → 6段式组装 → 字数检查 → 自检

## 1. 读取输入

从Step 1的输出获取：
- 画风 `dna` + `constraint`
- `recommended_lighting` + `recommended_composition`
- 用户的画面描述（场景+人物）

## 2. 6段式组装

读取 `../pop-visual-shared/references/seedream-prompt-guide.md` §一，按6段式结构组装：

```
[质量触发词] + Art style: [dna] [constraint] + [构图策略] + [光影叙事] + [场景] + [人物≤100字]
```

### 各段取值

| 段 | 取值来源 |
|:---|:---------|
| 1 质量触发词 | 固定：`IMG_2094.CR2, 8K ultra HD, cinematic quality, masterpiece, best quality, highly detailed` |
| 2 画风DNA | Step 1选定的 `dna` + `constraint` |
| 3 构图策略 | `references/lighting-composition-templates.md` 中CT1/CT2的英文描述 |
| 4 光影叙事 | 同文件中LT1/LT2/LT3的英文描述 |
| 5 场景 | 用户输入的画面场景描述 |
| 6 人物 | 用户输入的人物描述，≤100字 |

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
