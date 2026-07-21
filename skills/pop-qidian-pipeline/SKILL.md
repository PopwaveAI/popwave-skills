# pop-qidian-pipeline · 起点管线总控

> v1.1.0：全链路联调完成，版本快照表更新对齐所有已升级skill（research v4.0.0 / seed v8.1.0 / world v2.0.0 / plot v4.0.0 / write v3.0.0 / review v3.0.0 / character v1.0.0）。Phase路由微调+Skill调度表标注版本号。Phase 0→6路由+project-state.md状态追踪+三层骨架依赖链（骨架→主角→血肉→写作→审核）。基于番茄pipeline v3.2.0适配起点架构（三层骨架前移到seed+流派write分离）。
> 每次对话开始，agent读project-state.md就知道"我在哪、该进哪个phase"。人读project-state.html看进度。

---

## 做什么

输入：项目名（用户给）或当前项目目录
输出：标准化目录结构 + `project-state.md`（agent读）+ `project-state.html`（人看）

**定位**：pipeline不写正文、不创意、不审核——它只负责"把agent指向正确的phase和skill"。所有下游skill（seed/world/character/plot/write/review/research/dna-style）由pipeline按phase调度，不自行启动。

**与pop-qidian v4.0.1的关系**：pop-qidian保留为初始化审计入口（项目创建时一次性调用），pop-qidian-pipeline是每轮对话的总控（每次对话先读state再路由）。

---

## 项目空间结构

```
{项目名}/
├── project-state.html
├── project-state.md
├── README.md
├── 素材/                           # Phase 0产出
│   ├── 用户意图.md
│   ├── 赛道调研.md
│   ├── 市场校准.md
│   ├── decon-lite-{书名}.md
│   ├── 文风锚定.md
│   └── downloads/
│       └── {书名}.txt
├── 设计/                           # Phase 1-3.5产出
│   ├── 创意.md                     # Phase 1 seed产出
│   ├── 骨架.md                     # Phase 1 seed产出（力量体系+动力引擎）
│   ├── 主角设计.md                 # Phase 2 seed产出（主角+金手指+爽感矛盾）
│   ├── 全书设定/                   # Phase 3 world产出
│   │   ├── 力量体系.md
│   │   ├── 地图.md
│   │   ├── 势力.md
│   │   ├── 危机.md
│   │   ├── 各卷切片.md
│   │   └── 全书配角.md
│   ├── 角色库/                     # Phase 3.5 character产出
│   │   └── 角色库.md
│   └── 第一卷剧情/                 # Phase 4 plot产出
│       ├── 剧情白描.md
│       └── 章锚点表.md
├── 正文/                           # Phase 5产出
│   └── chXXX.txt
└── 审核/                           # Phase 6产出
    └── review-chXXX.md
```

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

**目标**：在创意发散之前把战场准备好——赛道方向、参考书群、力量体系参考全部就位。

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
| **decon-lite拆书** | 用户给了力量体系参考书+下载完成 | `你扮演 pop-qidian-research v4.0.0 decon-lite档位，读取 skills/pop-qidian-research/SKILL.md 了解decon-lite SOP（v4.0.0九表拆解）。参考书：{书名}，txt路径：素材/downloads/{书名}.txt。拆九表→落盘素材/decon-lite-{书名}.md。返回：落盘路径+九表摘要。` |
| **赛道定位调研** | 必有（所有项目） | `你扮演 pop-qidian-research v4.0.0 赛道定位调研档位，读取 skills/pop-qidian-research/SKILL.md。赛道：{用户方向}。做4轮搜索→产出素材/赛道调研.md。返回：落盘路径+借鉴点/避雷点/爽点类型清单摘要。` |

**并发规则**：
- 下载依赖：先等下载子agent返回 → 再同时派发笔触DNA + decon-lite
- 赛道定位调研：和其他任务完全独立，第一优先级启动
- 全部子agent返回后 → 更新project-state.md + project-state.html → `phase=phase1`

---

### Phase 1: Seed 骨架层+创意+首章

```
触发条件：state.phase = phase1
前置底牌：用户意图已落盘 + 赛道调研已落盘（如有）
```

**执行流程**：
1. 调pop-qidian-seed v8.1.0，执行Phase 0七维底牌+Phase 1骨架层（1d力量体系设计+1e动力引擎设计+1f骨架自洽）→1g双轨发散→1h故事纲领→1i黄金首章
2. Seed产出落盘后（`设计/骨架.md` + `设计/创意.md` + `正文/ch001.txt`），更新project-state.md + html
3. 骨架就绪状态检查：力量体系✅ + 动力引擎✅ + 骨架自洽✅ → `phase=phase2`

**关键依赖**：骨架.md必须在创意发散前定稿。骨架自洽检查（1f）不通过不进Phase 2。

### Phase 2: Seed 主角层

```
触发条件：state.phase = phase2
前置检查：设计/骨架.md 存在 + 骨架自洽通过
```

**执行流程**：
1. 调pop-qidian-seed v8.1.0 继续执行Phase 2主角层（2a主角设计+2b金手指设计+2c爽感矛盾设计）
2. 产出`设计/主角设计.md`，更新project-state.md + html
3. 主角就绪状态检查：主角设计✅ + 金手指设计✅ + 爽感矛盾✅ → `phase=phase3`

### Phase 3: World（世界构筑→全书设定/）

```
触发条件：state.phase = phase3
前置检查：设计/骨架.md + 设计/主角设计.md + 正文/ch001.txt 存在
```

**执行流程**：
1. 调pop-qidian-world v2.0.0，消费骨架.md（第一优先）+主角设计.md，产出`设计/全书设定/`（多文件：力量体系.md+地图.md+势力.md+危机.md+各卷切片.md+全书配角.md）
2. world禁止自行发明力量体系和动力引擎，必须消费骨架.md
3. 更新state：`phase=phase3.5`

### Phase 3.5: Character（角色库建设）

```
触发条件：state.phase = phase3.5
前置检查：设计/全书设定/ 存在
```

**执行流程**：
1. 调pop-qidian-character v1.0.0，消费骨架.md（众生攀登方式分层）+全书设定/势力.md，产出`设计/角色库/角色库.md`
2. 每个角色标注攀登方式类型+等级坐标
3. 更新state.md + state.html：`phase=phase4`

### Phase 4: Plot（叙事流剧情白描）

```
触发条件：state.phase = phase4
前置检查：设计/全书设定/ + 设计/角色库/角色库.md 存在
```

**执行流程**：
1. 调pop-qidian-plot v4.0.0，消费骨架.md+主角设计.md+全书设定+角色库，产出`设计/第一卷剧情/剧情白描.md`（含四层结构+困难三层面：每幕出场角色清单）+ `章锚点表.md`
2. 更新state.md + state.html：`phase=phase5`，`current_chapter=ch002`

> **注**：起点架构中plot在character之后（与番茄pipeline的plot→character顺序不同），因为character需要骨架.md的众生攀登方式分层作为输入，而plot需要角色库作为输入。world→character→plot是血肉层的依赖链。

### Phase 5: Write（正文渲染 ch002+）

```
触发条件：state.phase = phase5
前置检查：设计/第一卷剧情/剧情白描.md + 设计/角色库/角色库.md + current_chapter 存在
```

**执行流程**：
1. **必须用子agent调write**——主agent只做路由，不直接执行write
2. 流派write选择：
   - 用户声明D&D数据面板流 → 调pop-qidian-write-dndlike v1.0.1
   - 用户声明海贼王世界冒险流 → 调pop-qidian-write-onepiece v1.0.1
   - 未声明流派 → 调pop-qidian-write v3.0.0（兜底模板）
3. 子agent指令模板：`你扮演 {write-skill-name}，读取 skills/{write-skill-name}/SKILL.md 了解完整SOP。项目目录：{projectDir}。当前章节：{current_chapter}。按SOP执行：加载输入→选章型→写正文→字数自检→落盘。注意：必须加载设计/角色库/角色库.md和设计/主角设计.md（爽感矛盾公式），战斗/升级场景必须使用DNA面板格式。`
4. 子agent产出`正文/chXXX.txt`
5. 更新state：`phase=phase6`

### Phase 6: Review（审核+沉淀）

```
触发条件：state.phase = phase6
前置检查：正文/chXXX.txt 存在
```

**执行流程**：
1. 调pop-qidian-review v3.0.0，产出`审核/review-chXXX.md`（四维审核+骨架维度检查）
2. 通过 → `phase=phase5`，`current_chapter=chNNN+1`
3. 打回 → `phase=phase5`（重写本章）

---

## project-state.md 模板

```markdown
# 项目：{项目名}

> 管线：起点skill群 | 创建：{timestamp} | 更新：{timestamp}

## 当前阶段
phase: {init | phase0 | phase1 | phase2 | phase3 | phase3.5 | phase4 | phase5 | phase6}
current_chapter: {ch000 | ch001 | ch002 | ...}
current_write_skill: {pop-qidian-write | pop-qidian-write-dndlike | pop-qidian-write-onepiece}

## 阶段完成情况
- [ ] Phase 0: 用户意图 + 并发前置准备
- [ ] Phase 1: Seed骨架层 → 设计/骨架.md + 设计/创意.md + 正文/ch001.txt
- [ ] Phase 2: Seed主角层 → 设计/主角设计.md
- [ ] Phase 3: World → 设计/全书设定/（多文件）
- [ ] Phase 3.5: Character → 设计/角色库/角色库.md
- [ ] Phase 4: Plot → 设计/第一卷剧情/剧情白描.md + 章锚点表.md
- [ ] Phase 5: Write → 正文/chXXX.txt (当前: chNNN)
- [ ] Phase 6: Review → 审核/review-chXXX.md

## 骨架就绪状态（Phase 1产出）
- 力量体系（坐标系）：{✅/❌}
- 动力引擎（众生攀登系统）：{✅/❌}
- 骨架自洽检查：{✅/❌}

## 主角就绪状态（Phase 2产出）
- 主角设计：{✅/❌}
- 金手指设计（含限制+代价）：{✅/❌}
- 爽感矛盾设计（公式化）：{✅/❌}

## 血肉就绪状态（Phase 3-4产出）
- 地图：{✅/❌}
- 势力：{✅/❌}
- 角色库：{✅/❌}
- 剧情白描：{✅/❌}

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

## 红线

1. **project-state.md是唯一状态源**——所有phase切换、进度追踪以它为准。project-state.html是可视化镜像，不作为状态源
2. **每次更新state.md必须同步生成state.html**——保持人读和机器读一致
3. **Phase 0必须先深问再并发**——不完成Stage 1用户意图深问，不进入Stage 2
4. **pipeline只做路由不干活**——不写正文、不创意、不审核、不提取DNA
5. **Phase 5必须用子agent调write**——主agent只做路由，不直接执行write。主agent执行write会导致skill读取不全+正文质量退化+字数越来越短
6. **每phase完成后必须更新project-state.md + project-state.html**
7. **三层骨架依赖链不可跳过**——骨架没就绪不进主角层，主角没就绪不进血肉层，血肉没就绪不写作
8. **Phase 3.5 Character必须执行**——world完成后必须经过character建角色库，plot和write才能消费角色库
9. **agent每次对话第一件事是读project-state.md**

---

## 速查表

### 启动时判断

| project-state.md 存在？ | phase 值 | 执行 |
|------------------------|---------|------|
| 不存在 | — | Step 1 初始化 → 进 Phase 0 Stage 1 |
| 存在 | init / phase0 | Phase 0 Stage 1 深问 |
| 存在 | phase1 | Phase 1 Seed骨架层+创意+首章 |
| 存在 | phase2 | Phase 2 Seed主角层 |
| 存在 | phase3 | Phase 3 World |
| 存在 | phase3.5 | Phase 3.5 Character |
| 存在 | phase4 | Phase 4 Plot |
| 存在 | phase5 | Phase 5 Write |
| 存在 | phase6 | Phase 6 Review |

### Skill调度表

| 阶段 | 调用Skill | 版本 | 前置 | 产出路径 |
|-------|----------|------|------|---------|
| Phase 0 Stage 2 | tool-download-webnovel | v7.0.0 | 用户给了书名 | 素材/downloads/ |
| Phase 0 Stage 2 | pop-dna-style | v1.1.0 | 参考书已下载 | 素材/文风锚定.md |
| Phase 0 Stage 2 | pop-qidian-research（decon-lite） | v4.0.0 | 力量体系参考书+已下载 | 素材/decon-lite-{书名}.md |
| Phase 0 Stage 2 | pop-qidian-research（赛道定位调研） | v4.0.0 | 赛道方向已知 | 素材/赛道调研.md |
| Phase 1 | pop-qidian-seed | v8.1.0 | Phase 0 底牌就绪 | 设计/骨架.md + 设计/创意.md + 正文/ch001.txt |
| Phase 2 | pop-qidian-seed | v8.1.0 | 设计/骨架.md | 设计/主角设计.md |
| Phase 3 | pop-qidian-world | v2.0.0 | 设计/骨架.md + 设计/主角设计.md | 设计/全书设定/（多文件） |
| Phase 3.5 | pop-qidian-character | v1.0.0 | 设计/全书设定/ + 设计/骨架.md | 设计/角色库/角色库.md |
| Phase 4 | pop-qidian-plot | v4.0.0 | 设计/全书设定/ + 设计/角色库/ + 设计/骨架.md + 设计/主角设计.md | 设计/第一卷剧情/剧情白描.md + 章锚点表.md |
| Phase 5 | pop-qidian-write (**子agent**) | v3.0.0 | 设计/第一卷剧情/ + 设计/角色库/ + 设计/主角设计.md | 正文/chXXX.txt |
| Phase 5 | pop-qidian-write-dndlike (**子agent**) | v1.0.1 | 同上+用户声明D&D流 | 正文/chXXX.txt |
| Phase 5 | pop-qidian-write-onepiece (**子agent**) | v1.0.1 | 同上+用户声明海贼王流 | 正文/chXXX.txt |
| Phase 6 | pop-qidian-review | v3.0.0 | 正文/chXXX.txt | 审核/review-chXXX.md |

---

## 版本

v1.1.0 | 2026-07-21 | 全链路联调完成。版本快照表对齐所有已升级skill（research v4.0.0 / seed v8.1.0 / world v2.0.0 / plot v4.0.0 / write v3.0.0 / review v3.0.0 / character v1.0.0 / write-dndlike v1.0.1 / write-onepiece v1.0.1）。Phase路由微调+Skill调度表标注版本号。 → CHANGELOG.md

v1.0.0 | 2026-07-21 | 新建skill。Phase 0→6路由+project-state.md状态追踪+三层骨架依赖链（骨架→主角→血肉→写作→审核）。基于番茄pipeline v3.2.0适配起点架构（三层骨架前移到seed+流派write分离+character在plot之前）。 → CHANGELOG.md
