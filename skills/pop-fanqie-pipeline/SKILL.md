# pop-fanqie-pipeline · 番茄管线总控

> 项目初始化 + 用户意图深问 + 子agent并发推进 + 状态追踪 + 阶段路由。
> v2.0.0：Phase 0全量重构——从"问一本参考书"改为"深问赛道方向+标签+参考书群"，然后子agent并发推进。
> 每次对话开始，agent读project-state.md就知道"我在哪、该进哪个phase"。

---

## 做什么

输入：项目名（用户给）或当前项目目录
输出：标准化目录结构 + `project-state.md`（持续更新的管线地图）

**定位**：pipeline不写正文、不创意、不审核——它只负责"把agent指向正确的phase和skill"。所有下游skill（seed/plot/write/review/dna-style/download/research）由pipeline按phase调度，不自行启动。

---

## SOP骨架

| 步骤 | 做什么 | 产出 | 详细方法 |
|------|--------|------|---------|
| Step 1 | 初始化项目目录 + project-state.md | 目录就绪 + state=init | steps/step1.md |
| Step 2 | 读project-state.md → 按phase路由到对应phase执行 | 进入对应phase | steps/step2.md |

---

## Phase 路由规则

### Phase 0: 用户意图深问 + 子agent并发前置准备

```
触发条件：state.phase in [init, phase0]
```

**目标**：在创意发散之前把战场准备好——赛道方向、参考书群、标签/元素、力量体系参考全部就位。不做比做多更危险。

#### Phase 0: Stage 1 · 用户意图深问

pipeline 不是简单问"你要写什么"，而是像编辑一样深入摸底。四层递进：

**第1问：赛道方向（必须回答）**

> "你想写什么类型/题材？都市异能 / 玄幻修仙 / 无限流 / 历史架空 / 西幻 / 灵异悬疑 / 其他？说个模糊的感觉也行。"

锚定一个方向后，追问：
- 有没有已经想好的梗或画面？（有 → 记录，跳过市场调研的扫榜定方向步骤）
- 完全没有 → "没关系，后面我会帮你从排行榜找灵感"

**第2问：标签/元素（可不回答，跳过不阻塞）**

> "想往哪个方向做？比如——爽文向：打脸/升级/越级碾压。烧脑向：智斗/规则博弈/信息差。生活向：种田/经营/日常。完全没偏好就跳过。"

**第3问：参考书群（可不回答，跳过不阻塞）**

> "有没有2-3本你觉得写得好的书？不一定是同赛道，只要觉得笔触、节奏、设定有参考价值。"
>
> 如果有 → 追每本书想学什么（笔触？力量体系？角色塑造？节奏？）
> 如果没 → "我先帮你搜同赛道top作品，做完调研再问你要不要参考"

**第4问：现有设定（可不回答，跳过不阻塞）**

> "你心里有没有已经想好的力量体系/世界规则/主角身份设定？有的话先记下来，后面plot直接继承不重设计。"

**深问完成后**，落盘 `写作参考/用户意图.md`：

```markdown
# 用户意图（项目：{项目名}）

> pipeline Phase 0 Stage 1 · {timestamp}

## 赛道
- 方向：{用户回答}
- 已有梗/画面：{有/无，有则记录}

## 标签/元素
- 倾向：{回答 or "未指定"}
- 偏好：{回答 or "未指定"}

## 参考书群
| 书名 | 想学什么 | 用途 |
|:--|:--|:--|
| {书名1} | 笔触+节奏 | 文风DNA |
| {书名2} | 力量体系结构 | decon-lite |
| ... | ... | ... |

## 现有设定
- {有/无，有则记录}
```

#### Phase 0: Stage 2 · 子agent并发推进

> **Stage 1 用户意图落盘后，所有可以并发的前置准备任务同时派发。**
> 子agent描述原则：告诉它读哪个SKILL.md → 给参数 → 让它自己执行SOP。不塞文件内容。

| 任务 | 触发条件 | 子agent指令 |
|:--|:--|:--|
| **下载参考书** | 用户给了参考书+无本地文件 | `你扮演 tool-download-webnovel v7.0.0，读取 skills/tool-download-webnovel/SKILL.md。下载{书名}到downloads/。返回：落盘路径+文件大小。` |
| **笔触DNA提取** | 下载完成/已有本地文件 | `你扮演 pop-dna-style v1.1.0，读取 skills/pop-dna-style/SKILL.md。参考书：{书名}，txt路径：downloads/{书名}.txt。提取笔触DNA→落盘涌现/文风锚定.md。注意：判断参考书类型执行类型权重采样。返回：落盘路径+采样章数+覆盖场景类型。` |
| **decon-lite拆书** | 用户给了力量体系参考书+下载完成 | `你扮演 pop-research decon-lite档位，读取 skills/pop-research/SKILL.md 了解decon-lite SOP。参考书：{书名}，txt路径：downloads/{书名}.txt。拆两表（力量体系结构+剧情节奏）→落盘写作参考/decon-lite-{书名}.md。返回：落盘路径+两表各字段摘要。` |
| **赛道定位调研** | 必有（所有项目） | `你扮演 pop-research 赛道定位调研档位，读取 skills/pop-research/SKILL.md 了解赛道定位调研SOP。赛道：{用户方向}。做4轮搜索→产出写作参考/赛道调研.md。返回：落盘路径+借鉴点/避雷点/细分格局摘要。` |

**并发规则**：
- 下载依赖（如果参考书无本地文件）：先等下载子agent返回 → 再同时派发笔触DNA + decon-lite
- 赛道定位调研：和其他任务完全独立，第一优先级启动
- 用户没给参考书 → 跳过下载+DNA+decon-lite，只跑赛道定位调研
- 全部子agent返回后 → 更新project-state.md → `phase=phase1` → 进入Phase 1 seed

**超时处理**：子agent 180秒无响应→标注"超时跳过"，不阻塞后续流程。

#### project-state.md 更新（Phase 0完成）

```markdown
phase: phase1
# ↑ 已从 phase0 更新

## 底牌就绪状态
- 用户意图：写作参考/用户意图.md ✅
- 赛道调研：写作参考/赛道调研.md {✅/❌}
- 参考书下载：{done/skipped}
- 笔触DNA：涌现/文风锚定.md {✅/❌}
- decon-lite：写作参考/decon-lite-{书名}.md {✅/❌}
```

---

### Phase 1: Seed（创意+首章）

```
触发条件：state.phase = phase1
前置底牌：用户意图已落盘 + 赛道调研已落盘（如有）
```

**执行流程**：
1. 调pop-fanqie-seed，按最新SOP执行：跳过五维摸底（已在Phase 0完成）→ 直接进1c市场调研（如有子agent产出则消费落盘文件）→ 1d双轨发散 → 1e用户选 → Step 2结构化打磨 → Step 3黄金首章
2. Seed产出落盘后，更新project-state.md：`phase=phase2`

### Phase 2: Plot（世界构筑+剧情白描）

```
触发条件：state.phase = phase2
前置检查：0-立项/创意.md + 2-正文/ch001.md 存在
```

**执行流程**：
1. 调pop-fanqie-plot，按最新SOP执行（加载三件底牌→三源合流→叙事流剧情白描→落盘）
2. 产出落盘后更新project-state.md：`phase=phase3`，`current_chapter=ch002`

### Phase 3: Write（正文渲染 ch002+）

```
触发条件：state.phase = phase3
前置检查：剧情白描 + 章锚点表 + current-state 存在
```

**执行流程**：
1. 调pop-fanqie-write，按最新SOP执行（DNA按需加载→选章型→写正文→落盘）
2. 更新project-state.md：`phase=phase4`，`current_chapter=chNNN`

### Phase 4: Review（审核+沉淀）

```
触发条件：state.phase = phase4
前置检查：chNNN正文存在
```

**执行流程**：
1. 调pop-fanqie-review，按SOP执行
2. 通过 → `phase=phase3`，`current_chapter=chNNN+1`（回到write写下一章）
3. 打回 → `phase=phase3`（回到write重写本章）

---

## project-state.md 模板

```markdown
# 项目：{项目名}

> 管线：番茄skill群 | 创建：{timestamp} | 更新：{timestamp}

## 当前阶段
phase: {init | phase0 | phase1 | phase2 | phase3 | phase4}
current_chapter: {ch000 | ch001 | ch002 | ...}

## 阶段完成情况
- [ ] Phase 0: 用户意图 + 并发前置准备
- [ ] Phase 1: Seed → 创意.md + ch001
- [ ] Phase 2: Plot → 世界构筑 + 剧情白描 + 章锚点表
- [ ] Phase 3: Write → 逐章渲染 (当前: chNNN)
- [ ] Phase 4: Review → 审核-chNNN.md

## 底牌就绪
- 用户意图：写作参考/用户意图.md {✅/❌}
- 赛道调研：写作参考/赛道调研.md {✅/❌}
- 参考书下载：{done/skipped}
- 笔触DNA：涌现/文风锚定.md {✅/❌}
- decon-lite：{路径} {✅/❌}

## 创意摘要
- 书名(暂)：{seed产出}
- 一句话：{seed产出}

## 最近产出
| 阶段 | 产出文件 | 落盘时间 |
|------|---------|---------|
| ... | ... | ... |
```

---

## 红线

1. **project-state.md是唯一状态源**——所有phase切换、进度追踪以它为准
2. **Phase 0必须先深问再并发**——不完成Stage 1用户意图深问，不进入Stage 2（但Stage 1的2-4问可不回答跳过）
3. **pipeline只做路由不干活**——不写正文、不创意、不审核、不提取DNA，只把agent指向正确的skill
4. **每phase完成后必须更新project-state.md**
5. **agent每次对话第一件事是读project-state.md**

---

## 速查表

### 启动时判断

| project-state.md 存在？ | phase 值 | 执行 |
|------------------------|---------|------|
| 不存在 | — | Step 1 初始化 → 进 Phase 0 Stage 1 |
| 存在 | init / phase0 | Phase 0 Stage 1 深问（如已完成则 Stage 2） |
| 存在 | phase1 | Phase 1 Seed |
| 存在 | phase2 | Phase 2 Plot |
| 存在 | phase3 | Phase 3 Write (current_chapter) |
| 存在 | phase4 | Phase 4 Review |

### Skill调度表

| 阶段 | 调用Skill | 前置 |
|-------|----------|---------|
| Phase 0 Stage 2 | tool-download-webnovel | 用户给了书名+无本地 |
| Phase 0 Stage 2 | pop-dna-style | 参考书已下载 |
| Phase 0 Stage 2 | pop-research（decon-lite） | 用户给了力量体系参考书+已下载 |
| Phase 0 Stage 2 | pop-research（赛道定位调研） | 赛道方向已知 |
| Phase 1 | pop-fanqie-seed | Phase 0 底牌就绪 |
| Phase 2 | pop-fanqie-plot | 创意.md + ch001 存在 |
| Phase 3 | pop-fanqie-write | 剧情白描 + 章锚点表 存在 |
| Phase 4 | pop-fanqie-review | chNNN正文存在 |

---

## 版本

v2.0.0 | 2026-07-20 | Phase 0全量重构：从"问一本参考书"改为"用户意图深问(赛道+标签+参考书群+现有设定)→子agent并发推进(下载/DNA/decon-lite/赛道定位调研)→seed"。项目state模板扩展底牌就绪表。去参考书闸门(seed已内置) → CHANGELOG.md
v1.0.0 | 2026-07-20 | 新建skill。项目初始化+project-state.md状态追踪 → CHANGELOG.md
