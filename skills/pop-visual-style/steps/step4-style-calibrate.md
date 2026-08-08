# Step 4: 画风定标（Pipeline 语境下必做）

> 画风是"只能靠视觉验证"的抽象资产。本步用**小说次要视觉锚点 + 固定模板**渲染定标图，只验证一件事：**画风 DNA 是否被准确执行**。用户认可后**冻结为基线资产**。未认可不冻结、不放行下游。
>
> **v1.9.0 关键回归（画风定标素材 = 小说次要视觉锚点）**：老板定调——画风定标**不用主要人物形象当测试素材**（画风可能满意、但形象不满意，且本 skill 不是为设计人物而生）；但也**不用与小说无关的中性材料**（ahament 代入感会弱很多）。**画风定标默认用【和小说相关但无关紧要的次要元素**——某个战斗场景/地点、路人/NPC/龙套。这类元素：和小说强相关 → 保留代入感；无关紧要 → 不承担角色形象验收。**主角/主要角色归 `pop-visual-art-bible`/`oc` 环节，用已冻结画风去渲染承担。**

## 何时用（按 intent 档位分支）

- 本 skill 独立纯文生图：**跳过本步**（Step 1→2→3 直接出图）。
- **Pipeline 语境下（Phase 1 定画风）**，按 `视觉项目总控.html` 的 `intent` 档位分支：
  - `comic`/`full` → **完整定标（必做）**：走完整门禁 + 稳定复现验证（见下文 Step 4/5），进入 character（Phase 2）前先定标。
  - `cover`/`oc` → **agent 自检分支**：出定标图后 agent 自查辨识度/配色/光影/无文字即可，**不设强制用户门禁、不强制稳定复现**；达标即标记 `✅ 已认可` 供下游作画风参考。
- > Pipeline 未建总控（独立模式）时，按用户当次意图判定：明确做漫画/连载 → 完整档；做封面/OC → 自检分支。

## 核心原则

### 素材关联（用小说次要元素，保留代入感）
画风定标的测试素材**从小说提取次要视觉锚点**——某个战斗场景/地点（`--scene`）、路人/NPC/龙套（`--side`）。这类元素**和小说强相关**（画出来的画面有 project 代入感 ahament），又**无关紧要**（画风满意但形象不满的问题不会出现，因为不是要打磨的角色）。**禁止用主角/主要角色**——形象是否满意归角色设计环节，画风 skill 不负责。

### 变量隔离（素材固定，只验画风）
画风定标的唯一变量是**画风**。测试素材**一次确定、固定使用**（用 `--scene`/`--side` 注入后不换），构图固定、光照固定，才能判断"画风 DNA 是否被准确执行"。**素材固定后禁止中途换素材**——那会把"画风问题"和"素材适配度问题"混为一谈。角色形象是否满意不是本 skill 的职责。

### 稳定复现（工作流主线）
定标不只验证"这一张对不对"，还要验证"**能不能稳定复现**"。用**固定 seed + 同一提示词**复现，确认画风结果稳定，而非单次运气。**只有稳定复现的画风才冻结为基线。**

## 1. 测试素材（小说次要视觉锚点，变量隔离）

> **画风定标默认用【小说次要视觉锚点】**（和小说相关但无关紧要的元素），只验画风本身是否被执行。**禁止用主角/主要角色做测试素材**——画风可能满意但形象不满意，而形象是否满意归 `pop-visual-art-bible`/`oc` 环节，用已冻结的画风去渲染承担。

**从小说提取次要视觉锚点（两类，任选其一或组合）**：

- **场景类**（`--scene`，英文）：某个战斗场景/地点/环境片段，能体现画风光影与氛围。示例：
```
abandoned ancient temple courtyard, cracked stone floor, a single candle-lit altar, drifting dust motes in a beam of light, a torn banner stirring in the wind, no people, no text
```
- **人物类**（`--side`，英文）：路人/NPC/龙套，非主角、不需一致性、纯文生图。示例：
```
an old street vendor in worn robes, weathered face, standing by a wooden stall under a faded awning, neutral expression, no text
```

> 若小说暂无可提取的合适次要元素（如排期未定），可兜底用脚本内置中性素材（`--scene`/`--side` 不传）。这批中性素材已内置于 `batch_test.py`。

## 2. 组装定标提示词（走固定 SOP，不每次全新设计）

> **画风定标必须走固定脚本 `../pop-visual-shared/scripts/batch_test.py`**（固定测试素材 + 固定 6 段式模板 + 并发批量 + 自动 PE 日志）。禁止现场手写提示词、手动单张生成——那是"每次全新设计"，不稳定又慢。

### 2.1 测试素材（小说次要视觉锚点，脚本注入）

**从小说提取次要视觉锚点**（场景类 `--scene` / 人物类 `--side`，英文），作为测试素材注入：

- **场景类**（某个战斗场景/地点/环境片段，体现画风光影氛围）：
```
abandoned ancient temple courtyard, cracked stone floor, a single candle-lit altar, drifting dust motes in a beam of light, a torn banner stirring in the wind, no people, no text
```
- **人物类**（路人/NPC/龙套，非主角、不需一致性、纯文生图）：
```
an old street vendor in worn robes, weathered face, standing by a wooden stall under a faded awning, neutral expression, no text
```

> 测试素材是**变量隔离铁律**：画风定标的唯一变量是画风。素材**一次确定、固定使用**（`--scene`/`--side` 注入后不换）。**禁止传 `--character`/`--character-image` 引入主角/主要角色**——画风定标不用主角，人物形象是否满意归角色设计环节。

### 2.2 按画风批量取变体

- **从 DNA 库按画风名批量测**（推荐）：`--style-names "画风A,画风B"`，脚本自动取 `dna` + `constraint` + `recommended_composition` + `recommended_lighting`。
- **精调变体**：`--config 变体.json`，每个变体可单独改 `dna`/`constraint`/`lighting`（用于"只改一个子维度"的回炉迭代）。
- 画风 DNA 放第 2 段由脚本固定模板保证（铁律❌2）；构图/光照取自该画风 `recommended_*`（兼容性检查铁律❌3）。

## 3. 批量导出定标任务（一次出多张变体）

> 走固定脚本 `batch_test.py` **导出任务清单**，再由 `image_generate` 工具逐条生成。一次出一批变体，脚本只负责组装+校验，不直连 API。

```powershell
# 从 DNA 库按画风名批量测（传入小说次要素材：战斗场景 + 路人）→ 导出 generation_tasks.json
python ../pop-visual-shared/scripts/batch_test.py --style-names "暗黑悬疑高对比,赛博边缘行者" --scene "abandoned ancient temple courtyard, cracked stone floor, a single candle-lit altar, drifting dust motes in a beam of light, a torn banner stirring in the wind, no people, no text" --side "an old street vendor in worn robes, weathered face, standing by a wooden stall under a faded awning, neutral expression, no text" --out-dir 素材/视觉 --seed 20260803

# 只用场景类（无路人）测画风
python ../pop-visual-shared/scripts/batch_test.py --style-names "暗黑悬疑高对比" --scene "moonlit bamboo grove, swirling mist, a lone stone lantern glowing faintly, wind-blown leaves, no people, no text" --out-dir 素材/视觉 --seed 20260803

# 精调变体（定制 variant 的 dna/constraint/lighting，脚本注入的 scene/side 会覆盖变体同名段）→ 导出 generation_tasks.json
python ../pop-visual-shared/scripts/batch_test.py --config 素材/视觉/定标变体.json --scene "..." --side "..." --out-dir 素材/视觉 --seed 20260803
```

- **测试素材 = 小说次要视觉锚点**（`--scene` 场景/`--side` 路人），和小说强相关、无关紧要；不传则兜底用脚本内置中性素材。
- **禁止传 `--character`/`--character-image`**：画风定标不用主角/主要角色（画风可能满意但形象不满意，形象归角色设计环节）。
- `--seed` 固定随机种子，保证复现（下游图生图用同 seed 不漂移）。
- 输出：`generation_tasks.json`（每个变体一个任务，含 prompt/size/ref_images/output_path）+ `pe-log.json`（含测试素材/模板/每个变体完整 prompt，可复现）。
- **生成**：读 `generation_tasks.json`，对每条任务用 `image_generate` 工具生成（有 ref_images 时传参考图），输出到各任务 output_path，即 `{out-dir}/seed-{seed}/{画风名}.png`。
- 从结果中选达标变体作为候选定标图；**不达标回炉只改该变体 JSON 的一个子维度，再跑同脚本，不重写调用。**

## 4. 🚪 门禁：画风定标验收 + 稳定复现验证

### 4.1 画风定标验收

向用户呈现定标图，逐项验收：

| 维度 | 验收判据 |
|:-----|:---------|
| 辨识度 | 0.3 秒能否认出"来自哪个画风体系"（厚涂玄幻/赛璐珞/水彩/暗黑高对比） |
| 配色成立 | 画风自带主色板在这个测试场景下是否成立、是否被场景吞掉 |
| 光影兼容 | 所选光照模板与该画风是否兼容（柔美风格禁 LT1，防柔美画风被暗色吞噬） |
| 无文字 | 无乱码、无伪文字、无加字 |

**未达标不冻结。** 回炉微调 DNA 片段（非重选风格），重新生成 v2、v3... 直到达标。

### 4.2 稳定复现验证（核心）

用**同一提示词 + 同一 seed** 再跑一次固定脚本，对比两张是否一致。`batch_test.py` 输出目录按 `seed-{seed}` 分级，同 seed 重跑即落在同目录，天然形成复现对比：

- 复现生成：`python ../pop-visual-shared/scripts/batch_test.py --style-names "画风名" --out-dir 素材/视觉 --seed 20260803`（同 seed 重跑）
- 对比判据：同一 seed 目录下，本次与上次的画风辨识度、配色、光影是否**稳定一致**（允许构图微差，但画风铁定）

**未稳定复现不冻结。** 若复现结果画风漂移，说明提示词对 seed 敏感，需调整 DNA 或提示词（只改变体一个子维度），直到稳定复现。

## 5. 认可 → 冻结画风基线资产

用户认可 + 稳定复现通过后，把画风三字段**冻结为基线资产**：

- 落盘 `素材/风格/画风决策.md` 并标注 `签核状态: ✅ 已认可`
- 记录：画风名 + `dna` + `constraint` + `recommended_lighting` + `recommended_composition` + **参考图路径** + **定标 seed** + 定标图路径
- **seed 必须记录** —— 下游复现画风时用同 seed，保证稳定
- 参考图路径记入决策.md，作为下游图生图 image 参数来源

## 6. 通知下游

告知用户画风定标图已就绪，可被以下消费：

| 消费方 | 用途 |
|:-------|:-----|
| `pop-visual-art-bible` | 作为美术设定集画风篇的画风基准（首消费方，定全宇宙色彩基调） |
| `pop-visual-cover` / `pop-visual-oc` | 作为封面/OC 的风格参考图（image 参数 + 同 seed） |
| `pop-visual-comic` | 作为漫画页的风格基准（同 seed 保证画风不漂移） |

> **铁律**：画风基线一旦冻结，下游只消费它，禁止各自发明新画风。画风改动必须回到本 skill 重新定标。下游复现时用**冻结的 seed**，保证画风稳定复现。

## 下一步

→ 完成。Pipeline 语境下进入 Phase 2（`pop-visual-art-bible`）产出美术设定集（定妆深度按 intent 档位：`comic`/`full` 完整双角度，`cover`/`oc` 单张或跳过）。

## 红线

- 定标必须走固定脚本 `batch_test.py`（固定素材+固定模板+并发批量），禁止现场手写提示词、单张串行
- 定标图必须用**小说次要视觉锚点**（`--scene` 场景/`--side` 路人），和小说强相关、无关紧要；不传兜底用中性素材
- **禁止用主角/主要角色测画风**——画风可能满意但形象不满意，画风 skill 只验画风，人物形象归 `pop-visual-art-bible`/`oc` 环节
- **必须验证稳定复现**（同 seed 复现对比），未稳定复现不冻结
- 未认可不冻结、不放行下游
- 画风基线冻结后下游只消费，禁止各自发明
- 冻结时必须记录 seed + 参考图路径，否则下游无法复现