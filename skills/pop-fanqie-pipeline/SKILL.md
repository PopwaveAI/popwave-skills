# pop-fanqie-pipeline · 番茄管线总控

> v3.0.0：项目空间重构（四文件夹：素材/设计/正文/审核）+ project-state.html可视化。Phase 0→5的进度、底牌状态、产出文件、下一步操作可视化查看。
> v2.1.0：Phase 2拆分为Phase 2(World)+Phase 3(Plot)，设定设计与叙事创作分离。
> 每次对话开始，agent读project-state.md就知道"我在哪、该进哪个phase"。人读project-state.html看进度。

---

## 做什么

输入：项目名（用户给）或当前项目目录
输出：标准化目录结构 + `project-state.md`（agent读）+ `project-state.html`（人看）

**定位**：pipeline不写正文、不创意、不审核——它只负责"把agent指向正确的phase和skill"。所有下游skill（seed/plot/write/review/dna-style/download/research）由pipeline按phase调度，不自行启动。

---

## 项目空间结构（v3.0.0重构）

```
{项目名}/
├── project-state.html     # 可视化状态（人看，每次更新state时同步生成）
├── project-state.md       # 机器状态（agent读，唯一状态源）
├── README.md
├── 素材/                   # Phase 0产出（调研+DNA+拆书+原书）
│   ├── 用户意图.md
│   ├── 赛道调研.md
│   ├── 市场校准.md
│   ├── decon-lite-{书名}.md
│   ├── 文风锚定.md
│   └── downloads/
│       └── {书名}.txt
├── 设计/                   # Phase 1-3产出（创意+骨架+剧情白描）
│   ├── 创意.md
│   ├── 骨架.md
│   └── 剧情白描.md
├── 正文/                   # Phase 4产出（逐章渲染）
│   └── chXXX.txt
└── 审核/                   # Phase 5产出（审核记录）
    └── review-chXXX.md
```

**路径映射（旧→新）**：
| 旧路径 | 新路径 | 说明 |
|:--|:--|:--|
| 0-立项/创意.md | 设计/创意.md | 创意归设计 |
| 1-骨架/骨架.md | 设计/骨架.md | 骨架归设计 |
| 1-骨架/剧情白描.md | 设计/剧情白描.md | 剧情白描归设计 |
| 2-正文/chXXX.txt | 正文/chXXX.txt | 只改文件夹名 |
| 写作参考/用户意图.md | 素材/用户意图.md | 调研归素材 |
| 写作参考/赛道调研.md | 素材/赛道调研.md | 调研归素材 |
| 写作参考/市场校准.md | 素材/市场校准.md | 调研归素材 |
| 写作参考/decon-lite-*.md | 素材/decon-lite-*.md | 拆书归素材 |
| 涌现/文风锚定.md | 素材/文风锚定.md | DNA归素材 |
| downloads/*.txt | 素材/downloads/*.txt | 原书归素材子目录 |

---

## SOP骨架

| 步骤 | 做什么 | 产出 | 详细方法 |
|------|--------|------|---------|
| Step 1 | 初始化项目目录 + project-state.md + project-state.html | 目录就绪 + state=init | steps/step1.md |
| Step 2 | 读project-state.md → 按phase路由 → 完成后更新state.md+state.html | 进入对应phase | steps/step2.md |

---

## Phase 路由规则

### Phase 0: 用户意图深问 + 子agent并发前置准备

```
触发条件：state.phase in [init, phase0]
```

**目标**：在创意发散之前把战场准备好——赛道方向、参考书群、标签/元素、力量体系参考全部就位。

#### Phase 0: Stage 1 · 用户意图深问

pipeline 不是简单问"你要写什么"，而是像编辑一样深入摸底。四层递进：

**第1问：赛道方向（必须回答）**
> "你想写什么类型/题材？都市异能 / 玄幻修仙 / 无限流 / 历史架空 / 西幻 / 灵异悬疑 / 其他？说个模糊的感觉也行。"

**第2问：标签/元素（可不回答，跳过不阻塞）**
> "想往哪个方向做？爽文向：打脸/升级/越级碾压。烧脑向：智斗/规则博弈/信息差。生活向：种田/经营/日常。"

**第3问：参考书群（可不回答，跳过不阻塞）**
> "有没有2-3本你觉得写得好的书？不一定是同赛道，只要觉得笔触、节奏、设定有参考价值。"

**第4问：现有设定（可不回答，跳过不阻塞）**
> "你心里有没有已经想好的力量体系/世界规则/主角身份设定？"

**深问完成后**，落盘 `素材/用户意图.md`。

#### Phase 0: Stage 2 · 子agent并发推进

| 任务 | 触发条件 | 子agent指令 |
|:--|:--|:--|
| **下载参考书** | 用户给了参考书+无本地文件 | `你扮演 tool-download-webnovel v7.0.0，读取 skills/tool-download-webnovel/SKILL.md。下载{书名}到素材/downloads/。返回：落盘路径+文件大小。` |
| **笔触DNA提取** | 下载完成/已有本地文件 | `你扮演 pop-dna-style v1.1.0，读取 skills/pop-dna-style/SKILL.md。参考书：{书名}，txt路径：素材/downloads/{书名}.txt。提取笔触DNA→落盘素材/文风锚定.md。返回：落盘路径+采样章数+覆盖场景类型。` |
| **decon-lite拆书** | 用户给了力量体系参考书+下载完成 | `你扮演 pop-research decon-lite档位，读取 skills/pop-research/SKILL.md 了解decon-lite SOP（v2.1.0八表拆解）。参考书：{书名}，txt路径：素材/downloads/{书名}.txt。拆八表→落盘素材/decon-lite-{书名}.md。返回：落盘路径+八表摘要。` |
| **赛道定位调研** | 必有（所有项目） | `你扮演 pop-research 赛道定位调研档位，读取 skills/pop-research/SKILL.md。赛道：{用户方向}。做4轮搜索→产出素材/赛道调研.md。返回：落盘路径+借鉴点/避雷点/爽点类型清单摘要。` |

**并发规则**：
- 下载依赖：先等下载子agent返回 → 再同时派发笔触DNA + decon-lite
- 赛道定位调研：和其他任务完全独立，第一优先级启动
- 全部子agent返回后 → 更新project-state.md + project-state.html → `phase=phase1`

#### project-state.md 更新（Phase 0完成）

```markdown
phase: phase1

## 底牌就绪状态
- 用户意图：素材/用户意图.md ✅
- 赛道调研：素材/赛道调研.md {✅/❌}
- 参考书下载：{done/skipped}
- 笔触DNA：素材/文风锚定.md {✅/❌}
- decon-lite：素材/decon-lite-{书名}.md {✅/❌}
```

---

### Phase 1: Seed（创意+首章）

```
触发条件：state.phase = phase1
前置底牌：用户意图已落盘 + 赛道调研已落盘（如有）
```

**执行流程**：
1. 调pop-fanqie-seed，按最新SOP执行
2. Seed产出落盘后（`设计/创意.md` + `正文/ch001.txt`），更新project-state.md + html：`phase=phase2`

### Phase 2: World（世界构筑→骨架.md）

```
触发条件：state.phase = phase2
前置检查：设计/创意.md + 正文/ch001.txt 存在
```

**执行流程**：
1. 调pop-fanqie-world，产出`设计/骨架.md`
2. 更新state：`phase=phase3`

### Phase 3: Plot（叙事流剧情白描）

```
触发条件：state.phase = phase3
前置检查：设计/骨架.md 存在
```

**执行流程**：
1. 调pop-fanqie-plot，产出`设计/剧情白描.md`
2. 更新state：`phase=phase4`，`current_chapter=ch002`

### Phase 4: Write（正文渲染 ch002+）

```
触发条件：state.phase = phase4
前置检查：设计/剧情白描.md + current_chapter 存在
```

**执行流程**：
1. 调pop-fanqie-write，写`正文/chXXX.txt`
2. 更新state：`phase=phase5`

### Phase 5: Review（审核+沉淀）

```
触发条件：state.phase = phase5
前置检查：正文/chXXX.txt 存在
```

**执行流程**：
1. 调pop-fanqie-review，产出`审核/review-chXXX.md`
2. 通过 → `phase=phase4`，`current_chapter=chNNN+1`
3. 打回 → `phase=phase4`（重写本章）

---

## project-state.md 模板

```markdown
# 项目：{项目名}

> 管线：番茄skill群 | 创建：{timestamp} | 更新：{timestamp}

## 当前阶段
phase: {init | phase0 | phase1 | phase2 | phase3 | phase4 | phase5}
current_chapter: {ch000 | ch001 | ch002 | ...}

## 阶段完成情况
- [ ] Phase 0: 用户意图 + 并发前置准备
- [ ] Phase 1: Seed → 设计/创意.md + 正文/ch001.txt
- [ ] Phase 2: World → 设计/骨架.md
- [ ] Phase 3: Plot → 设计/剧情白描.md
- [ ] Phase 4: Write → 正文/chXXX.txt (当前: chNNN)
- [ ] Phase 5: Review → 审核/review-chXXX.md

## 底牌就绪
- 用户意图：素材/用户意图.md {✅/❌}
- 赛道调研：素材/赛道调研.md {✅/❌}
- 参考书下载：{done/skipped}
- 笔触DNA：素材/文风锚定.md {✅/❌}
- decon-lite：素材/decon-lite-{书名}.md {✅/❌}

## 创意摘要
- 书名(暂)：{seed产出}
- 一句话：{seed产出}

## 最近产出
| 阶段 | 产出文件 | 落盘时间 |
|------|---------|---------|
| ... | ... | ... |
```

---

## project-state.html 可视化（v3.0.0新增）

> 每次更新project-state.md时，同步生成project-state.html。人用浏览器打开即可查看项目进度。

**HTML内容板块**：
1. **顶部**：项目名 + 管线名 + 创建/更新时间
2. **Phase进度条**：Phase 0→5的可视化进度条（✅完成/🔄进行中/⬜未开始）
3. **底牌就绪卡片**：5张底牌的就绪状态（✅/❌/skipped）
4. **创意摘要卡片**：书名 + 一句话 + 主角
5. **最近产出表格**：阶段 + 文件名 + 落盘时间
6. **下一步操作**：当前phase该做什么 + 前置检查

**HTML生成规则**：
- 自包含单文件：内联CSS+JS，不依赖外部资源
- 从project-state.md解析字段填充HTML
- 模板文件：`skills/pop-fanqie-pipeline/templates/project-state.html.tpl`
- 生成方式：pipeline读取project-state.md → 解析字段 → 替换模板占位符 → 落盘project-state.html

**模板占位符**：
| 占位符 | 替换内容 | 来源 |
|:--|:--|:--|
| `{{PROJECT_NAME}}` | 项目名 | project-state.md 第1行 |
| `{{CREATED_AT}}` | 创建时间 | project-state.md |
| `{{UPDATED_AT}}` | 更新时间 | project-state.md |
| `{{PHASE}}` | 当前phase | phase字段 |
| `{{CURRENT_CHAPTER}}` | 当前章节 | current_chapter字段 |
| `{{PHASE_CHECKLIST}}` | Phase完成情况HTML | 阶段完成情况 |
| `{{DECK_CARDS}}` | 底牌就绪HTML | 底牌就绪区块 |
| `{{CREATIVE_SUMMARY}}` | 创意摘要HTML | 创意摘要区块 |
| `{{RECENT_OUTPUTS}}` | 最近产出表格HTML | 最近产出表 |
| `{{NEXT_STEP}}` | 下一步操作HTML | 当前phase路由 |

---

## 红线

1. **project-state.md是唯一状态源**——所有phase切换、进度追踪以它为准。project-state.html是可视化镜像，不作为状态源
2. **每次更新state.md必须同步生成state.html**——保持人读和机器读一致
3. **Phase 0必须先深问再并发**——不完成Stage 1用户意图深问，不进入Stage 2
4. **pipeline只做路由不干活**——不写正文、不创意、不审核、不提取DNA
5. **每phase完成后必须更新project-state.md + project-state.html**
6. **agent每次对话第一件事是读project-state.md**

---

## 速查表

### 启动时判断

| project-state.md 存在？ | phase 值 | 执行 |
|------------------------|---------|------|
| 不存在 | — | Step 1 初始化 → 进 Phase 0 Stage 1 |
| 存在 | init / phase0 | Phase 0 Stage 1 深问 |
| 存在 | phase1 | Phase 1 Seed |
| 存在 | phase2 | Phase 2 World |
| 存在 | phase3 | Phase 3 Plot |
| 存在 | phase4 | Phase 4 Write |
| 存在 | phase5 | Phase 5 Review |

### Skill调度表

| 阶段 | 调用Skill | 前置 | 产出路径 |
|-------|----------|---------|---------|
| Phase 0 Stage 2 | tool-download-webnovel | 用户给了书名 | 素材/downloads/ |
| Phase 0 Stage 2 | pop-dna-style | 参考书已下载 | 素材/文风锚定.md |
| Phase 0 Stage 2 | pop-research（decon-lite） | 力量体系参考书+已下载 | 素材/decon-lite-{书名}.md |
| Phase 0 Stage 2 | pop-research（赛道定位调研） | 赛道方向已知 | 素材/赛道调研.md |
| Phase 1 | pop-fanqie-seed | Phase 0 底牌就绪 | 设计/创意.md + 正文/ch001.txt |
| Phase 2 | pop-fanqie-world | 设计/创意.md + 正文/ch001.txt | 设计/骨架.md |
| Phase 3 | pop-fanqie-plot | 设计/骨架.md | 设计/剧情白描.md |
| Phase 4 | pop-fanqie-write | 设计/剧情白描.md | 正文/chXXX.txt |
| Phase 5 | pop-fanqie-review | 正文/chXXX.txt | 审核/review-chXXX.md |

---

## 版本

v3.0.0 | 2026-07-21 | 项目空间重构：四文件夹（素材/设计/正文/审核）+ project-state.html可视化。所有路径引用统一更新。 → CHANGELOG.md
v2.1.0 | 2026-07-21 | Phase 2拆为Phase 2(World)+Phase 3(Plot)，设定设计与叙事创作分离。 → CHANGELOG.md
v2.0.0 | 2026-07-20 | Phase 0全量重构。 → CHANGELOG.md
v1.0.0 | 2026-07-20 | 新建skill。 → CHANGELOG.md
