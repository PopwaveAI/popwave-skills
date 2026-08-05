# Step 4: 画风定标（Pipeline 语境下必做）

> 画风是"只能靠视觉验证"的抽象资产。本步用**画风×项目角色 + 固定模板**渲染定标图，验证两件事：① 画风 DNA 是否被准确执行；② 画风能否撑起**本项目的角色**（画风×角色适配度）。用户认可后**冻结为基线资产**。未认可不冻结、不放行下游。
>
> **v1.4.1 关键升级（画风×项目角色联合测试）**：老板实测发现固定中性素材测不出"画风能否撑起项目角色"（玄鉴仙族用中性"现代青年+木屋"测画风，测不出"黑金甲衣+金瞳"主角的适配度）。**画风定标默认用项目主角当测试素材，而非中性素材。** 用 `--character` + `--character-image` 传项目角色（图生图保证角色一致）。

## 何时用（按 intent 档位分支）

- 本 skill 独立纯文生图：**跳过本步**（Step 1→2→3 直接出图）。
- **Pipeline 语境下（Phase 1 定画风）**，按 `视觉项目总控.html` 的 `intent` 档位分支：
  - `comic`/`full` → **完整定标（必做）**：走完整门禁 + 稳定复现验证（见下文 Step 4/5），进入 character（Phase 2）前先定标。
  - `cover`/`oc` → **agent 自检分支**：出定标图后 agent 自查辨识度/配色/光影/无文字即可，**不设强制用户门禁、不强制稳定复现**；达标即标记 `✅ 已认可` 供下游作画风参考。
- > Pipeline 未建总控（独立模式）时，按用户当次意图判定：明确做漫画/连载 → 完整档；做封面/OC → 自检分支。

## 核心原则

### 变量隔离（画风×项目角色）
画风定标的唯一变量是**画风**。测试角色固定（用本项目主角）、构图固定、光照固定，才能判断"画风 DNA 是否被准确执行" + "画风能否撑起这个角色"。**禁止换角色、禁止换素材。**

### 稳定复现（工作流主线）
定标不只验证"这一张对不对"，还要验证"**能不能稳定复现**"。用**固定 seed + 同一提示词**复现，确认画风结果稳定，而非单次运气。**只有稳定复现的画风才冻结为基线。**

## 1. 测试素材（画风×项目角色，默认用项目主角）

> **画风定标默认用项目主角做测试素材**（验证画风×角色适配度）。若项目尚未定角色（Phase 0 未产出），回退到脚本内置标准测试角色（仅排查画风本身是否被执行）。

**项目主角**（从 Phase 0 角色档案/定妆图取，英文描述人物段）：
```
[项目主角的英文描述，如：Li Zhouwei, an imperial warlord in black-gold ornate armor with purple-feathered mantle, golden pupils, holding a long halberd, imposing regal bearing]
```

**标准测试角色**（回退，英文，中性人设，可体现画风）：
```
a young adult standing half-body portrait, neutral calm expression, simple dark hair, plain white inner shirt under a muted earthy jacket, natural skin texture, facing camera, no accessories, no text
```

**标准场景**（英文，简单中性，可体现画风光影）：
```
a simple quiet interior, warm wooden room, soft window light from the left, a wooden table and a potted plant, calm atmosphere, no people, no text
```

> 项目主角素材已内置判断逻辑：传 `--character` 即用项目角色，否则回退标准角色。**默认用项目角色，禁止用中性素材测画风适配度。**

## 2. 组装定标提示词（走固定 SOP，不每次全新设计）

> **画风定标必须走固定脚本 `../pop-visual-shared/scripts/batch_test.py`**（固定测试素材 + 固定 6 段式模板 + 并发批量 + 自动 PE 日志）。禁止现场手写提示词、手动单张生成——那是"每次全新设计"，不稳定又慢。

### 2.1 测试素材（脚本内置，勿改）

**标准测试角色**（英文，中性人设，可体现画风）：
```
a young adult standing half-body portrait, neutral calm expression, simple dark hair, plain white inner shirt under a muted earthy jacket, natural skin texture, facing camera, no accessories, no text
```

**标准场景**（英文，简单中性，可体现画风光影）：
```
a simple quiet interior, warm wooden room, soft window light from the left, a wooden table and a potted plant, calm atmosphere, no people, no text
```

> 测试素材是**变量隔离铁律**：画风定标的唯一变量是画风。**画风×项目角色联合测试时**，用 `--character` 传项目角色描述 + `--character-image` 传定妆图/OC图（图生图保证角色一致），替换标准角色。这批素材已内置于 `batch_test.py`，无需手动维护。

### 2.2 按画风批量取变体

- **从 DNA 库按画风名批量测**（推荐）：`--style-names "画风A,画风B"`，脚本自动取 `dna` + `constraint` + `recommended_composition` + `recommended_lighting`。
- **精调变体**：`--config 变体.json`，每个变体可单独改 `dna`/`constraint`/`lighting`（用于"只改一个子维度"的回炉迭代）。
- 画风 DNA 放第 2 段由脚本固定模板保证（铁律❌2）；构图/光照取自该画风 `recommended_*`（兼容性检查铁律❌3）。

## 3. 批量导出定标任务（一次出多张变体）

> 走固定脚本 `batch_test.py` **导出任务清单**，再由 `image_generate` 工具逐条生成。一次出一批变体，脚本只负责组装+校验，不直连 API。

```powershell
# 画风×项目角色联合测试（推荐，验证画风能否撑起项目主角）→ 导出 generation_tasks.json
python ../pop-visual-shared/scripts/batch_test.py --style-names "国漫玄幻厚涂,暗黑悬疑高对比" --character "李周巍, 黑金玄纹甲衣, 紫羽王氅, 金瞳, 持长戟" --character-image "素材/李周巍OC-v1.png" --out-dir 素材/视觉 --seed 20260803

# 从 DNA 库按画风名批量测（无角色时用中性素材，仅排查画风本身）→ 导出 generation_tasks.json
python ../pop-visual-shared/scripts/batch_test.py --style-names "暗黑悬疑高对比,赛博边缘行者" --out-dir 素材/视觉 --seed 20260803

# 精调变体（定制 variant 的 dna/constraint/lighting）→ 导出 generation_tasks.json
python ../pop-visual-shared/scripts/batch_test.py --config 素材/视觉/定标变体.json --out-dir 素材/视觉 --seed 20260803
```

- `--seed` 固定随机种子，保证复现（下游图生图用同 seed 不漂移）。
- 输出：`generation_tasks.json`（每个变体一个任务，含 prompt/size/ref_images/output_path）+ `pe-log.json`（含固定素材/模板/每个变体完整 prompt，可复现）。
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
| `pop-visual-character` | 作为角色定妆图的画风基准（同款画风 + 同 seed 渲染） |
| `pop-visual-cover` / `pop-visual-oc` | 作为封面/OC 的风格参考图（image 参数 + 同 seed） |
| `pop-visual-comic` | 作为漫画页的风格基准（同 seed 保证画风不漂移） |

> **铁律**：画风基线一旦冻结，下游只消费它，禁止各自发明新画风。画风改动必须回到本 skill 重新定标。下游复现时用**冻结的 seed**，保证画风稳定复现。

## 下一步

→ 完成。Pipeline 语境下进入 Phase 2（`pop-visual-character`）设计人物身份卡（定妆深度按 intent 档位：`comic`/`full` 完整双角度，`cover`/`oc` 单张或跳过）。

## 红线

- 定标必须走固定脚本 `batch_test.py`（固定素材+固定模板+并发批量），禁止现场手写提示词、单张串行
- 定标图必须用固定测试素材（变量隔离），禁止换素材
- **必须验证稳定复现**（同 seed 复现对比），未稳定复现不冻结
- 未认可不冻结、不放行下游
- 画风基线冻结后下游只消费，禁止各自发明
- 冻结时必须记录 seed + 参考图路径，否则下游无法复现