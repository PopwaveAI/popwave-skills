# pop-qidian-pipeline · 起点管线总控

> v1.2.0：删除project-state.md，项目总控.html成为唯一状态文件。agent直接用SearchReplace更新html中的`<!--STATE:xxx -->`标记字段。初始化强制创建全部目录（含审核/）+自检。write DNA改为100%项目空间读取（删除skill内部dna/目录）。
> v1.1.0：全链路联调完成，版本快照表更新对齐所有已升级skill。Phase 0→6路由+三层骨架依赖链（骨架→主角→血肉→写作→审核）。基于番茄pipeline v3.2.0适配起点架构。
> 每次对话开始，agent读项目总控.html就知道"我在哪、该进哪个phase"。人读同一个html看进度。

---

## 做什么

输入：项目名（用户给）或当前项目目录
输出：标准化目录结构 + `项目总控.html`（agent读+人看，唯一状态文件）

**定位**：pipeline不写正文、不创意、不审核——它只负责"把agent指向正确的phase和skill"。所有下游skill（seed/world/character/plot/write/review/research/dna-style）由pipeline按phase调度，不自行启动。

**与pop-qidian v4.0.1的关系**：pop-qidian保留为初始化审计入口（项目创建时一次性调用），pop-qidian-pipeline是每轮对话的总控（每次对话先读state再路由）。

---

## 项目空间结构

```
{项目名}/
├── 项目总控.html                   # 唯一状态文件（agent读+人看）
├── README.md
├── 素材/                           # Phase 0产出
│   ├── 用户意图.md
│   ├── 赛道调研.md
│   ├── 市场校准.md
│   ├── decon-lite-{书名}.md
│   ├── 文风锚定.md                 # pop-dna-style提取的笔触DNA（write的唯一DNA源）
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
    ├── review-chXXX.md             # 单章审核报告
    └── 小说快照.md                  # 全书累计视图（每章review后更新）
```

---

## SOP骨架

| 步骤 | 做什么 | 产出 | 详细方法 |
|------|--------|------|---------|
| Step 1 | 初始化项目目录 + 项目总控.html | 目录就绪 + state=init | steps/step1.md |
| Step 2 | 读项目总控.html → 按phase路由 → 完成后SearchReplace更新html | 进入对应phase | steps/step2.md |

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
- 全部子agent返回后 → 更新项目总控.html → `phase=phase1`

---

### Phase 1: Seed 骨架层+创意+首章

```
触发条件：state.phase = phase1
前置底牌：用户意图已落盘 + 赛道调研已落盘（如有）
```

**执行流程**：
1. 调pop-qidian-seed v8.1.0，执行Phase 0七维底牌+Phase 1骨架层（1d力量体系设计+1e动力引擎设计+1f骨架自洽）→1g双轨发散→1h故事纲领→1i黄金首章
2. Seed产出落盘后（`设计/骨架.md` + `设计/创意.md` + `正文/ch001.txt`），更新项目总控.html
3. 骨架就绪状态检查：力量体系✅ + 动力引擎✅ + 骨架自洽✅ → `phase=phase2`

**关键依赖**：骨架.md必须在创意发散前定稿。骨架自洽检查（1f）不通过不进Phase 2。

### Phase 2: Seed 主角层

```
触发条件：state.phase = phase2
前置检查：设计/骨架.md 存在 + 骨架自洽通过
```

**执行流程**：
1. 调pop-qidian-seed v8.1.0 继续执行Phase 2主角层（2a主角设计+2b金手指设计+2c爽感矛盾设计）
2. 产出`设计/主角设计.md`，更新项目总控.html
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
3. 更新项目总控.html：`phase=phase4`

### Phase 4: Plot（叙事流剧情白描）

```
触发条件：state.phase = phase4
前置检查：设计/全书设定/ + 设计/角色库/角色库.md 存在
```

**执行流程**：
1. 调pop-qidian-plot v4.0.0，消费骨架.md+主角设计.md+全书设定+角色库，产出`设计/第一卷剧情/剧情白描.md`（含四层结构+困难三层面：每幕出场角色清单）+ `章锚点表.md`
2. 更新项目总控.html：`phase=phase5`，`current_chapter=ch002`

> **注**：起点架构中plot在character之后（与番茄pipeline的plot→character顺序不同），因为character需要骨架.md的众生攀登方式分层作为输入，而plot需要角色库作为输入。world→character→plot是血肉层的依赖链。

### Phase 5: Write（正文渲染 ch002+）

```
触发条件：state.phase = phase5
前置检查：设计/第一卷剧情/剧情白描.md + 设计/角色库/角色库.md + current_chapter 存在
```

**执行流程**：
1. **必须用子agent调write**——主agent只做路由，不直接执行write
2. 流派选择（v1.3.0简化）：
   - **永远调pop-qidian-write**（唯一write skill）
   - 用户声明流派后，将流派名称传给子agent，子agent在write的Step 4自动加载`references/流派专属/{流派名}/`技法包
   - 支持的流派：D&D数据面板流（dndlike）/ 海贼王世界冒险流（onepiece）/ 无流派（默认通用）
   - 子agent指令需包含：`用户声明流派={流派名}，请在Step 4加载references/流派专属/{流派名}/技法文件`
3. 子agent指令模板：`你扮演 pop-qidian-write，读取 skills/pop-qidian-write/SKILL.md 了解完整SOP。项目目录：{projectDir}。当前章节：{current_chapter}。按SOP执行：加载输入→选章型→写正文→字数自检→落盘。注意：必须加载设计/角色库/角色库.md和设计/主角设计.md（爽感矛盾公式），战斗/升级场景必须使用DNA面板格式。`
4. 子agent产出`正文/chXXX.txt`
5. 更新项目总控.html：`phase=phase6`
6. **write完成后必须进入Phase 6 review**——不得连续写两章不review（v1.4.0红线）

### Phase 6: Review（审核+沉淀+小说快照）

```
触发条件：state.phase = phase6
前置检查：正文/chXXX.txt 存在
```

**执行流程**：
1. 调pop-qidian-review v3.1.0，产出`审核/review-chXXX.md`（四维审核+骨架维度检查）
2. review Step 4沉淀产出：`current-state.md`更新 + `审核/小说快照.md`更新（全书累计视图——涌现设定/角色状态总表/剧情线进度/读者已知信息池/待回收伏笔总表）
3. 通过 → 更新项目总控.html：`phase=phase5`，`chapter=chNNN+1`
4. 打回 → 更新项目总控.html：`phase=phase5`（重写本章）

---

## 项目总控.html

项目总控.html是**唯一状态文件**——agent读它判断phase+路由，人读它看进度。没有project-state.md。

- **模板文件**：`skills/pop-qidian-pipeline/templates/项目总控.html`
- **初始化**：step1.md负责创建（读模板→写入项目根目录→SearchReplace更新project_name和timestamp）
- **更新**：step2.md负责每次phase完成后用SearchReplace更新html中的`<!--STATE:xxx -->`标记字段
- **字段说明**：所有可变字段用`<!--STATE:field -->值<!--/STATE:field -->`注释标记包裹，agent用SearchReplace精确替换
- **phase circle**：用CSS class控制状态（pending→done/current），agent用SearchReplace改class属性

**不要手动写HTML标签**——只通过SearchReplace更新已有标记字段的值。

---

## 红线

1. **项目总控.html是唯一状态文件**——没有project-state.md。agent读html判断phase+路由，人读html看进度。用SearchReplace更新`<!--STATE:xxx -->`标记字段
2. **每phase完成后必须SearchReplace更新项目总控.html**——至少更新phase+timestamp+next_step+phase circle。不更新html=phase没完成
3. **Phase 0必须先深问再并发**——不完成Stage 1用户意图深问，不进入Stage 2
4. **pipeline只做路由不干活**——不写正文、不创意、不审核、不提取DNA
5. **Phase 5必须用子agent调write**——主agent只做路由，不直接执行write。主agent执行write会导致skill读取不全+正文质量退化+字数越来越短
6. **初始化必须创建全部8个目录（含审核/）+自检通过**——任何目录缺失=初始化失败
7. **write完成后必须进入review**——Phase 5产出后必须路由到Phase 6，不得连续写两章不review。未review的正文不得作为下一章的前置输入
8. **三层骨架依赖链不可跳过**——骨架没就绪不进主角层，主角没就绪不进血肉层，血肉没就绪不写作
9. **Phase 3.5 Character必须执行**——world完成后必须经过character建角色库，plot和write才能消费角色库
10. **agent每次对话第一件事是读项目总控.html**——从`<!--STATE:phase -->`标记提取当前phase值，按速查表路由
11. **Phase 6 review必须更新小说快照**——review完成后必须更新`审核/小说快照.md`（全书累计视图），不更新=沉淀未完成

---

## 速查表

### 启动时判断

| 项目总控.html 存在？ | phase 值 | 执行 |
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
| Phase 5 | pop-qidian-write (**子agent**) | v3.3.0 | 设计/第一卷剧情/ + 设计/角色库/ + 设计/主角设计.md + 用户声明流派 | 正文/chXXX.txt |
| Phase 6 | pop-qidian-review | v3.1.0 | 正文/chXXX.txt | 审核/review-chXXX.md + current-state.md + 小说快照.md |

---

## 版本

v1.1.0 | 2026-07-21 | 全链路联调完成。版本快照表对齐所有已升级skill。Phase路由微调+Skill调度表标注版本号。 → CHANGELOG.md

v1.4.0 | 2026-07-22 | review新增小说快照（全书累计视图）。write→review链路改硬约束（不得连续写两章不review）。Phase 6产出新增小说快照.md。
v1.3.0 | 2026-07-22 | 合并dndlike/onepiece到兜底write为流派技法包。Phase 5路由简化为永远调pop-qidian-write。删除两个独立流派skill。
v1.2.0 | 2026-07-22 | 删除project-state.md，项目总控.html成为唯一状态文件。agent直接用SearchReplace更新html标记字段。初始化强制创建全部8目录+自检。write DNA改为100%项目空间读取。
v1.0.0 | 2026-07-21 | 新建skill。Phase 0→6路由+三层骨架依赖链。基于番茄pipeline v3.2.0适配起点架构。 → CHANGELOG.md
