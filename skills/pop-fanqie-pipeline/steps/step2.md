# Step 2: 状态路由

> 每次对话开始，读project-state.md → 按phase值分流到对应Phase执行 → 完成后更新project-state.md + project-state.html。

---

## 读state

打开`project-state.md`，提取：

| 字段 | 用途 |
|------|------|
| phase | 当前在哪个阶段，决定路由 |
| current_chapter | Write阶段当前该写哪一章 |
| 底牌就绪 | Phase 0是否已完成 |

---

## 路由分流

### Phase: init

执行Step 1初始化（创建四文件夹目录+落盘project-state.md+生成html）→ 更新state到phase0 → 进Phase 0

### Phase: phase0（用户意图深问+并发前置准备）

**Stage 1: 用户意图深问**

四层递进问用户：赛道方向（必答）→ 标签/元素（可跳过）→ 参考书群（可跳过）→ 现有设定（可跳过）

落盘 `素材/用户意图.md`

**Stage 2: 子agent并发推进**

| 任务 | 触发条件 | 产出路径 |
|:--|:--|:--|
| 下载参考书 | 用户给了书名+无本地文件 | 素材/downloads/{书名}.txt |
| 笔触DNA提取 | 参考书已下载 | 素材/文风锚定.md |
| decon-lite拆书 | 力量体系参考书+已下载 | 素材/decon-lite-{书名}.md |
| 赛道定位调研 | 必有 | 素材/赛道调研.md |

全部返回后 → 更新state.md + state.html → `phase=phase1`

### Phase: phase1（Seed创意+首章）

```
前置检查：
  ✅ 用户意图已落盘 或 用户已明确跳过
  ✅ 赛道调研已落盘（如有）

执行：
  → 调pop-fanqie-seed
  → 产出：设计/创意.md + 正文/ch001.txt
  → 更新state.md + state.html：
     phase = phase2
     current_chapter = ch001
     创意摘要.书名 = seed产出
     创意摘要.一句话 = seed产出
```

### Phase: phase2（World世界构筑）

```
前置检查：
  ✅ 设计/创意.md 存在
  ✅ 正文/ch001.txt 存在

执行：
  → 调pop-fanqie-world
  → 产出：设计/骨架.md
  → 更新state.md + state.html：
     phase = phase3
```

### Phase: phase3（Plot剧情白描）

```
前置检查：
  ✅ 设计/骨架.md 存在

执行：
  → 调pop-fanqie-plot
  → 产出：设计/剧情白描.md
  → 更新state.md + state.html：
     phase = phase3.5
```

### Phase: phase3.5（Character角色库建设）

```
前置检查：
  ✅ 设计/剧情白描.md 存在（含分幕设计的出场角色清单）

执行：
  → 调pop-fanqie-character
  → 消费分幕设计出场角色清单+骨架敌人梯度+创意主角轮廓
  → 产出：设计/角色库.md
  → 更新state.md + state.html：
     phase = phase4
     current_chapter = ch002
```

### Phase: phase4（Write正文渲染）

```
前置检查：
  ✅ 设计/剧情白描.md 存在
  ✅ 设计/角色库.md 存在

执行：
  → 必须用子agent调pop-fanqie-write（主agent只做路由）
  → 子agent指令：你扮演 pop-fanqie-write，读取 skills/pop-fanqie-write/SKILL.md 了解完整SOP。项目目录：{projectDir}。当前章节：{current_chapter}。按SOP执行：加载输入→选章型→写正文→字数自检→落盘。注意：必须加载角色库.md，战斗/升级场景必须使用DNA面板格式。
  → 写current_chapter指定的章节 → 正文/chXXX.txt
  → 更新state.md + state.html：
     phase = phase5
```

### Phase: phase5（Review审核沉淀）

```
前置检查：
  ✅ 正文/chXXX.txt 存在

执行：
  → 调pop-fanqie-review
  → 产出：审核/review-chXXX.md

结果A·通过
  → 更新state.md + state.html：
     phase = phase4
     current_chapter = ch{NNN+1}

结果B·废章打回
  → 更新state.md + state.html：
     phase = phase4（current_chapter不变，重写本章）
```

---

## 更新project-state.md + project-state.html的方法

**1. 更新project-state.md**（用SearchReplace工具）：

1. `phase:` 行 → 更新为新phase值
2. `current_chapter:` 行 → 更新为当前章节号
3. `更新：` 行 → 更新为当前时间
4. 阶段完成情况 → 勾选完成的phase
5. 底牌就绪区块 → 更新状态
6. 创意摘要 → 填写seed产出
7. 最近产出表 → 追加新行

**2. 生成project-state.html**（每次更新state.md后必须同步）：

运行脚本：
```bash
python skills/pop-fanqie-pipeline/scripts/generate-state-html.py {projectDir}/project-state.md
```

脚本自动解析state.md字段→替换模板占位符→同目录生成state.html。**禁止手动写HTML**。

**Phase→下一步操作映射**（脚本内置）：
| Phase | 下一步操作 |
|:--|:--|
| init | Phase 0: 用户意图深问 |
| phase0 | Phase 1: Seed创意+首章 |
| phase1 | Phase 2: World世界构筑 |
| phase2 | Phase 3: Plot剧情白描 |
| phase3 | Phase 3.5: Character角色库建设 |
| phase3.5 | Phase 4: Write正文渲染 (ch002) |
| phase4 | Phase 5: Review审核 (chXXX) |
| phase5 | Phase 4: Write下一章 / 重写本章 |

---

## 下一步

> 路由完成 → 进入对应phase执行 → 执行完成后回到本Step 2继续路由
