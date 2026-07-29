---
name: pop-qidian-pipeline
description: 起点管线总控。当用户说"管线""pipeline""继续写""下一步""导入""续写"时启用。读项目总控.html→按Phase 0-6路由调度各子skill（seed/world/character/plot/write/review）。
---

# pipeline

> 起点管线总控。Phase 0→6路由调度。v3.9.0：文件全景图对齐——修复骨架.md残留引用+Phase路由表产出列补全+HTML模板文件夹树更新+产出目录初始化。v3.8.0：Phase 3产出更新为10个最小闭环文件（world v4.4.0）。完整版本历史见CHANGELOG.md。

---

## 做什么

pipeline只做路由不干活——读项目总控.html判断phase→路由到对应子skill→完成后更新html。不写正文、不创意、不审核、不提取DNA。

输入：项目名或当前项目目录（mode=fresh/import/resume）
输出：标准化目录结构 + `项目总控.html`（唯一状态文件）

---

## 怎么操作（SOP骨架）

1. **Step 0**（导入/续写）→ `steps/step0-import.md`：资产清点→文件归位（不做内容转换）→调度skill reconstruct补跑→落地Phase决策。当用户说"导入/续写/已有"或目录已有文件时触发
2. **Step 1**（初始化）→ `steps/step1.md`：创建8个子目录+生成项目总控.html+自检
3. **Step 2**（路由循环）→ `steps/step2.md`：读html→按Phase路由表调度子skill→SearchReplace更新html

### Phase路由表

| Phase | 调用Skill | 前置检查 | 产出 |
|:--|:--|:--|:--|
| 0-Stage1 | 深问四层（赛道/标签/参考书/现有设定） | state=init/phase0 | 素材/用户意图.md |
| 0-Stage2 | ①拆书任务（download→dna-style→decon-lite） ②seed Step 0交互（S0→S1世界→S2力量→S3主角）。主agent依次执行拆书任务，同时推进seed交互 | Stage1完成 | 素材/（赛道调研.md+文风锚定.md v1+decon-lite-{书名}.md+downloads/{书名}.txt） + 设计/立项决策表.md（S0-S3部分） |
| 1 | pop-qidian-seed v9.0.0（S4-S5续交互→骨架+创意+首章） | S1-S3完成+拆书就绪 | 立项决策表.md（完整）+力量体系.md+动力引擎.md+创意候选PK.md+创意.md+正文/ch001.txt |
| 2 | pop-qidian-seed v9.0.0（主角层） | 骨架自洽通过 | 设计/主角设计.md |
| 3 | pop-qidian-world v4.4.0（交互→主agent加载skill执行生成世界设定） | 骨架+主角+ch001就绪 | 设计/世界决策表.md+设计/全书设定/（10个最小闭环文件） |
| 3→3.5 | pop-dna-style v1.4.0 Stage 2（主agent加载skill执行DNA综合重构） | 全书设定文件就绪 | 素材/文风锚定.md v2（笔触层+世界画风层+用户需求层） |
| 3.5 | pop-qidian-character v1.2.0（交互→主agent加载skill执行生成角色库） | 全书设定就绪 | 设计/角色库/角色库决策表.md+角色库.md |
| 4 | pop-qidian-plot v4.3.0（交互→主agent加载skill执行生成卷纲+章锚点） | 设定+角色库就绪 | 设计/第一卷剧情/卷纲决策表.md+卷纲.md+章锚点表.md+产出/正文/事实快照-幕NNN.md |
| 5 | pop-qidian-write v3.5.0 | 剧情+角色库+主角就绪 | 正文/chXXX.txt |
| 6 | pop-qidian-review v3.4.0 | 正文产出 | 审核/review-chXXX.md+小说快照.md+review-沉淀.md+current-state.md（项目根） |

> Phase 0-1并行设计、产出真实性门禁、下载失败中断、主agent执行指南、Phase 5/6执行细节、Phase 1-4交互模式等规则见 `steps/step2.md`

---

## 红线

1. **读取协议**：每次对话第一件事读项目总控.html获取当前phase→按路由表调度。禁止跳过读html直接干活。
2. **pipeline只做路由不干活**——所有产出由下游skill生成。pipeline不直接写正文/创意/审核/提取DNA。
3. **三层骨架依赖链不可跳过**——骨架没就绪不进主角层，主角没就绪不进血肉层，血肉没就绪不写作。
4. **混合执行模式**——交互型step（底牌摸底/决策交互）由主agent直接执行；执行型step（骨架展开/世界设定/角色库/卷纲/正文/审核）由主agent收集上下文后派发子agent执行。主agent职责：读取skill SKILL.md+step文件→提炼红线+操作要点+项目上下文→组装instruction→派发子agent→检查产出→更新项目总控→衔接下一step。子agent职责：按instruction读取skill文件+输入文件→执行SOP→落盘产出。不依赖harness层skillNames传参。

---

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `SKILL.md` | 每次对话必读 | 管线骨架+Phase路由表+红线 |
| `steps/step0-import.md` | 用户说"导入/续写/已有"或检测到已有文件时 | 资产清点→文件归位→调度skill reconstruct→落地Phase |
| `steps/step1.md` | 初始化时（state=init且无已有文件） | 目录创建+项目总控.html生成+自检 |
| `steps/step2.md` | 每次路由时 | 读html状态→按phase路由→主agent执行指南→更新html |
| `templates/项目总控.html` | 初始化时读模板 | 状态文件模板 |
| `项目总控.html`（项目空间） | 每次对话第一件事 | 唯一状态源（phase+next_step+就绪状态+产出表） |
