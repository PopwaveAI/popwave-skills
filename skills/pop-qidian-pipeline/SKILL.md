---
name: pop-qidian-pipeline
description: 起点管线总控。当用户说"管线""pipeline""继续写""下一步"时启用。读项目总控.html→按Phase 0-6路由调度各子skill（seed/world/character/plot/write/review）。
---

# pipeline

> 起点管线总控。Phase 0→6路由调度。v3.0.0：seed v9.0.0引擎三要素重构（S1/S2/S3全部加入定位+好坏标准+达成方法）。完整版本历史见seed CHANGELOG.md。

---

## 做什么

输入：项目名（用户给）或当前项目目录
输出：标准化目录结构（素材/设计/正文/审核）+ `项目总控.html`（唯一状态文件）

**定位**：pipeline只做路由不干活——不写正文、不创意、不审核、不提取DNA。按phase调度下游skill（seed/world/character/plot/write/review/research/dna-style），下游skill不自行启动。每次对话第一件事：读项目总控.html判断phase→路由→执行→SearchReplace更新html。

---

## 怎么操作（SOP骨架）

> execution.mode: 每次对话先读项目总控.html→按phase路由→执行→SearchReplace更新html。
> 强弱加载：SKILL.md=完整骨架（必读），steps/step文件=详细操作（强加载全文），项目总控.html=状态源（每次必读），Phase路由表=弱加载参考。

### Step 1：初始化 → `steps/step1.md`
创建项目目录（8个子目录含审核/）+读模板生成项目总控.html+自检11项。

### Step 2：路由循环 → `steps/step2.md`
读html提取phase→按Phase路由表调度对应skill→完成后SearchReplace更新html。

### Phase路由表

| Phase | 调用Skill | 前置检查 | 产出 |
|:--|:--|:--|:--|
| 0-Stage1 | 深问四层（赛道/标签/参考书/现有设定） | state=init/phase0 | 素材/用户意图.md |
| 0-Stage2 | **并行**：①拆书子agent（download/dna-style/research×2） ②seed Step 0交互（S0前置收集→S1世界构筑→S2力量体系设计→S3主角设计） | Stage1完成 | 素材/（调研+文风锚定+decon-lite） + 设计/立项决策表.md（S0-S3部分） |
| 1 | pop-qidian-seed v9.0.0（Step 0续交互S4-S5→骨架层+创意+首章） | Step 0 S1-S3完成+拆书就绪 | 设计/立项决策表.md（完整）+骨架.md+创意.md+正文/ch001.txt |
| 2 | pop-qidian-seed v9.0.0（主角层） | 骨架自洽通过 | 设计/主角设计.md |
| 3 | pop-qidian-world v3.0.0（Step 0交互→世界圣经） | 骨架+主角+ch001就绪 | 设计/世界决策表.md+全书设定/（多文件） |
| 3.5 | pop-qidian-character v1.2.0（Step 0交互→角色库） | 全书设定就绪 | 设计/角色库/角色库决策表.md+角色库.md |
| 4 | pop-qidian-plot v4.3.0（Step 0交互→卷纲+章锚点） | 设定+角色库就绪 | 设计/第一卷剧情/卷纲决策表.md+卷纲.md+章锚点表.md |
| 5 | pop-qidian-write v3.4.0（**子agent**） | 剧情+角色库+主角就绪 | 正文/chXXX.txt |
| 6 | pop-qidian-review v3.2.0 | 正文产出 | 审核/review-chXXX.md+current-state.md+小说快照.md |

> **Phase 0-1并行设计**（v1.8.0新增，v2.3.0更新）：Stage1深问完成后，拆书子agent和seed Step 0交互**同时启动**。拆书结果（decon-lite/decon-plot）可实时喂给Step 0的S2-S5选项。S0前置收集+S1世界构筑仅需用户意图.md，不依赖拆书结果，因此可立即开始。S2力量体系设计（含三境界广义分级）消费拆书结果（decon-lite表1/表9），需等拆书返回或用已有信息先生成选项。
> Phase 0并发规则：下载先返回→再同时派发dna-style+decon-lite；赛道调研独立第一优先级启动。
> Phase 5→6→5循环：write完成必进review，review通过回Phase 5写下一章，打回重写本章。
> Phase 3.5 Character必须执行，world→character→plot是血肉层依赖链。

### Phase 1-4执行模式：先交互→再生成

> Phase 1-4在进入自动生成前，必须先完成Step 0交互式决策。核心轮用户确认后才进入下游skill自动生成。可选轮用户可跳过。

| Phase | Step 0交互轮次 | 核心必答/可选 | 决策表产出 | 完成后执行 |
|:--|:--|:--|:--|:--|
| 1 seed | S0-S5（6轮） | S1-S4核心必答+S5可选 | 设计/立项决策表.md | 再执行骨架生成 |
| 3 world | W1-W2（2轮） | W1核心必答+W2可选 | 设计/世界决策表.md | 再执行世界圣经生成 |
| 3.5 character | C1-C2（2轮） | C1核心必答+C2可选 | 设计/角色库/角色库决策表.md | 再执行角色库生成 |
| 4 plot | R1-R5（5轮） | 前3轮核心必答+后2轮可选 | 设计/第一卷剧情/卷纲决策表.md | 再执行Step 1-3自动生成 |

### Phase 5详细执行流程

```
触发条件：state.phase = phase5
前置检查：设计/第一卷剧情/卷纲.md + 设计/第一卷剧情/章锚点表.md + 设计/角色库/角色库.md + current_chapter 存在
```

1. **必须用子agent调write**——主agent只做路由，不直接执行write
2. **永远调pop-qidian-write**（唯一write skill）。用户声明流派后，将流派名称传给子agent，子agent在write的Step 4自动加载`references/流派专属/{流派名}/`技法包
3. 子agent指令模板：`你扮演 pop-qidian-write，读取 skills/pop-qidian-write/SKILL.md 了解完整SOP。项目目录：{projectDir}。当前章节：{current_chapter}。按SOP执行：加载输入→选章型→写正文→字数自检→落盘。注意：必须加载设计/角色库/角色库.md和设计/主角设计.md（爽感矛盾公式），战斗/升级场景必须使用DNA面板格式。`
4. 子agent产出`正文/chXXX.txt`
5. 更新项目总控.html：`phase=phase6`
6. **write完成后必须进入Phase 6 review**——不得连续写两章不review

### Phase 6详细执行流程

```
触发条件：state.phase = phase6
前置检查：正文/chXXX.txt 存在
```

1. 调pop-qidian-review v3.2.0，产出`审核/review-chXXX.md`（四维审核+骨架维度检查）
2. review Step 4沉淀产出：`current-state.md`更新 + `审核/小说快照.md`更新（全书累计视图——涌现设定/角色状态总表/剧情线进度/读者已知信息池/待回收伏笔总表）
3. 通过 → 更新项目总控.html：`phase=phase5`，`chapter=chNNN+1`
4. 打回 → 更新项目总控.html：`phase=phase5`（重写本章）

### 项目空间结构树

```
项目根/
├── 素材/                    Phase 0 产出（调研+DNA+拆书+原书）
│   ├── 用户意图.md
│   ├── 赛道调研.md
│   ├── 文风锚定.md           pop-dna-style 提取的笔触DNA
│   └── decon-lite-{书名}.md  research 拆书9表
├── 设计/                    Phase 1-4 产出
│   ├── 立项决策表.md         Phase 1 Step 0 交互决策产出
│   ├── 骨架.md              Phase 1 seed（力量体系+动力引擎）
│   ├── 创意.md              Phase 1 seed（故事纲领）
│   ├── 主角设计.md           Phase 2 seed（主角+金手指+爽感矛盾）
│   ├── 世界决策表.md         Phase 3 Step 0 交互决策产出
│   ├── 全书设定/            Phase 3 world
│   ├── 角色库/              Phase 3.5 character
│   │   ├── 角色库决策表.md   Phase 3.5 Step 0 交互决策产出
│   │   └── 角色库.md
│   └── 第一卷剧情/          Phase 4 plot
│       ├── 卷纲决策表.md     Phase 4 Step 0 交互决策产出
│       ├── 卷纲.md
│       └── 章锚点表.md
├── 正文/                    Phase 5 write
│   ├── ch001.md
│   └── ch002.md ...
└── 审核/                    Phase 6 review
    ├── review-chXXX.md
    └── 小说快照.md            全书累计视图（每章review后更新）
```

---

## 红线

1. **读取协议**：每次对话第一件事读项目总控.html获取当前phase→按速查表路由。SKILL.md=完整骨架（必读），steps/step文件=详细操作（强加载全文），项目总控.html=状态源（每次必读）。禁止跳过读html直接干活。
2. **项目总控.html是唯一状态文件**——每phase完成后必须SearchReplace更新（phase+timestamp+next_step+phase circle）。不更新=phase没完成。
3. **Phase 0必须先深问再并发**——不完成Stage 1用户意图深问，不进入Stage 2子agent并发。
4. **pipeline只做路由不干活**——不写正文、不创意、不审核、不提取DNA。所有产出由下游skill生成。
5. **Phase 5必须用子agent调write**——主agent只做路由，不直接执行write。
6. **write完成后必须进入review**——不得连续写两章不review。未review的正文不得作为下一章前置输入。
7. **三层骨架依赖链不可跳过**——骨架没就绪不进主角层，主角没就绪不进血肉层，血肉没就绪不写作。
8. **Phase 1-4的Step 0交互决策不可跳过**——核心轮必须用户确认后才进入自动生成。
9. **Phase 3.5 Character必须执行**——world完成后必须经过character建角色库，plot和write才能消费角色库。
10. **Phase 6 review必须更新小说快照**——review完成后必须更新`审核/小说快照.md`（全书累计视图），不更新=沉淀未完成。
11. **初始化必须创建全部8个目录（含审核/）+自检通过**——任何目录缺失=初始化失败。

---

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `SKILL.md` | 每次对话必读 | 管线骨架+Phase路由表+红线 |
| `steps/step1.md` | 初始化时（state=init） | 目录创建+项目总控.html生成+自检11项 |
| `steps/step2.md` | 每次路由时 | 读html状态→按phase路由→SearchReplace更新html |
| `templates/项目总控.html` | 初始化时读模板 | 状态文件模板（phase circle+就绪卡片+产出表） |
| `项目总控.html`（项目空间） | 每次对话第一件事 | 唯一状态源（phase+next_step+就绪状态+产出表） |

---

## 版本

> 完整版本历史见 `d:\popwave-skills\skills\pop-qidian-seed\CHANGELOG.md`

v3.0.0 | 2026-07-23
- **seed v9.0.0引擎三要素重构**：S1/S2/S3全部加入定位+好坏标准+达成方法。S1增量吸引力≥3+4组合模式。S2适配度6维判断。S3主角引擎（三定位+金手指5方法论+追读钩子5类型+危机关系4模式）
- Phase路由表更新：seed版本v8.16.0→v9.0.0
- 清理历史版本耦合：SKILL.md不再堆叠全部changelog，只保留最近版本，完整历史见CHANGELOG.md
