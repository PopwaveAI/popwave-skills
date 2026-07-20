# pop-fanqie-pipeline · 番茄管线总控

> 项目初始化 + 状态追踪 + 阶段路由。不重复下游skill的SOP，只做"地图"。
> 每次对话开始，agent读project-state.md就知道"我在哪、该进哪个phase"。

---

## 做什么

输入：项目名（用户给）或当前项目目录
输出：标准化目录结构 + `project-state.md`（持续更新的管线地图）

**定位**：pipeline不写正文、不创意、不审核——它只负责"把agent指向正确的phase和skill"。所有下游skill（seed/plot/write/review/dna-style/download/pop-research）由pipeline按phase调度，不自行启动。

---

## SOP骨架

| 步骤 | 做什么 | 产出 | 详细方法 |
|------|--------|------|---------|
| Step 1 | 初始化项目目录 + project-state.md | 目录就绪 + state=init | steps/step1.md |
| Step 2 | 读project-state.md → 按phase路由到对应phase执行 | 进入对应phase | steps/step2.md |

---

## Phase 路由规则

### Phase 0: 参考书就绪（闸门）

```
触发条件：state.phase in [init, phase0]
参考书状态：未就绪
```

**执行流程**：
1. 问用户："有没有想参考笔触的书？比如觉得哪本书的节奏/爽感/写法对胃口？"
2. 根据回答路由：
   - 用户给书名 → tool-download-webnovel下载 → pop-dna-style提取DNA（档位A笔触必做+档位B剧情brief可选）
   - 用户没想好 → pop-research（种子级）调研同赛道热门 → 产出推荐书单 → 用户选1-2本 → download + dna-style
   - 用户明确拒绝 → 在state标注"无参考书风险"，write将因缺失DNA进trial模式
3. DNA部署完成后，更新project-state.md：`phase=phase1`，参考书条目填"就绪"

**红线**：不完成参考书摸底，不进入Phase 1。用户明确拒绝是唯一跳过允许。

### Phase 1: Seed（创意+首章）

```
触发条件：state.phase = phase1
前置检查：参考书已就绪 OR 用户已明确拒绝
```

**执行流程**：
1. 调pop-fanqie-seed，按v13.1.0 SOP执行（市场调研→纯自由发散→市场校准→用户选→结构化打磨→黄金首章）
2. Seed产出的`创意.md`和`ch001.md`落盘后，更新project-state.md：`phase=phase2`

### Phase 2: Plot（世界构筑+剧情白描）

```
触发条件：state.phase = phase2
前置检查：0-立项/创意.md + 2-正文/ch001.md 存在
```

**执行流程**：
1. 调pop-fanqie-plot，按v9.1.0 SOP执行（加载创意文档→世界构筑→第一卷详规→四图叠加推演剧情白描→落盘）
2. Plot产出的`剧情白描.md`+`章锚点表.md`落盘后，更新project-state.md：`phase=phase3`，`current_chapter=ch002`

### Phase 3: Write（正文渲染 ch002+）

```
触发条件：state.phase = phase3
前置检查：1-骨架/剧情白描.md + 1-骨架/章锚点表.md + current-state.md 存在
```

**执行流程**：
1. 调pop-fanqie-write，按v8.0.0 SOP执行（加载剧情白描+笔触DNA三态协议→选章型→写正文→篇幅检查→落盘）
2. Write产出`chNNN.md`后，更新project-state.md：`phase=phase4`，`current_chapter=chNNN`

### Phase 4: Review（审核+沉淀）

```
触发条件：state.phase = phase4
前置检查：2-正文/chNNN.md 存在
```

**执行流程**：
1. 调pop-fanqie-review，按v4.1.0 SOP执行（符合性检查→笔触检查→好看度→剧情沉淀→落盘审核-chNNN.md）
2. Review产出`审核-chNNN.md`后：
   - 通过 → 更新project-state.md：`phase=phase3`，`current_chapter=chNNN+1`（回到write写下一章）
   - 打回 → 更新project-state.md：`phase=phase3`（回到write重写本章）

---

## project-state.md 模板

```markdown
# 项目：{项目名}

> 管线：番茄skill群 | 创建：{timestamp}

## 当前阶段
phase: {init | phase0 | phase1 | phase2 | phase3 | phase4}
current_chapter: {ch000 | ch001 | ch002 | ...}

## 阶段完成情况
- [ ] Phase 0: 参考书就绪
- [ ] Phase 1: Seed → 创意.md + ch001.md
- [ ] Phase 2: Plot → 世界构筑 + 剧情白描 + 章锚点表
- [ ] Phase 3: Write → 逐章渲染 (当前: chNNN)
- [ ] Phase 4: Review → 审核-chNNN.md

## 参考书
- 书名：{书名 or 未就绪}
- 本地文件：downloads/{书名}.txt {✅ or ❌}
- 笔触DNA：涌现/文风锚定.md {✅ 档位A / ✅ 档位A+B / ❌}
- 用户拒绝：{是/否}

## 创意摘要
- 书名(暂)：{seed产出}
- 一句话：{seed产出}

## 最近产出
| 阶段 | 产出文件 | 落盘时间 |
|------|---------|---------|
| seed | 0-立项/创意.md | ... |
| seed | 2-正文/ch001.md | ... |
| plot | 1-骨架/剧情白描.md | ... |
| write | 2-正文/ch002.md | ... |
| review | 审核-ch002.md | ... |
```

---

## 红线

1. **project-state.md是唯一状态源**——所有phase切换、进度追踪以它为准，禁止agent凭空判断"现在该干嘛"
2. **Phase 0是必选闸门**——参考书未就绪且用户未明确拒绝时，不得进入Phase 1
3. **pipeline只做路由不干活**——不写正文、不创意、不审核、不提取DNA，只把agent指向正确的skill
4. **每phase完成后必须更新project-state.md**——更新phase + current_chapter + 最近产出表
5. **agent每次对话第一件事是读project-state.md**——读到phase=phase0就知道"先去问参考书"，读到phase=phase3就知道"当前该写chNNN"

---

## 速查表

### 启动时判断

| project-state.md 存在？ | phase 值 | 执行 |
|------------------------|---------|------|
| 不存在 | — | Step 1 初始化 → 进 Phase 0 |
| 存在 | init / phase0 | Phase 0 参考书摸底 |
| 存在 | phase1 | Phase 1 Seed |
| 存在 | phase2 | Phase 2 Plot |
| 存在 | phase3 | Phase 3 Write (current_chapter) |
| 存在 | phase4 | Phase 4 Review |

### Skill调度表

| Phase | 调用Skill | 前置检查 |
|-------|----------|---------|
| Phase 0 | tool-download-webnovel → pop-dna-style | 用户给了书名 |
| Phase 0 | pop-research（种子级）→ download → dna-style | 用户没想好 |
| Phase 1 | pop-fanqie-seed | 参考书已就绪 |
| Phase 2 | pop-fanqie-plot | 创意.md + ch001.md 存在 |
| Phase 3 | pop-fanqie-write | 剧情白描.md + 章锚点表.md 存在 |
| Phase 4 | pop-fanqie-review | chNNN.md 存在 |

---

## 版本

v1.0.0 | 2026-07-20 | 新建skill。项目初始化+project-state.md状态追踪+5个phase路由+Phase 0参考书闸门。解决管线三大缺口：无状态文件、skill间盲调度、参考书可选 → CHANGELOG.md
