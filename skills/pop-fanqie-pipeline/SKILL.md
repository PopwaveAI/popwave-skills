---
name: pop-fanqie-pipeline
description: "当用户说'初始化项目/管线总控/番茄pipeline'时启用。Phase 0→5全链路调度，项目空间标准化，project-state状态可视化。"
---

# pop-fanqie-pipeline

> 番茄管线总控。Phase 0→5全链路调度，pipeline只做路由不干活。v3.3.0

## 做什么

输入：项目名或当前项目目录
输出：标准化目录结构（素材/设计[全书设定/角色库/第一卷剧情]/正文/审核）+ project-state.md（agent读）+ project-state.html（人看）

pipeline不写正文、不创意、不审核——只负责把agent指向正确的phase和skill。所有下游skill由pipeline按phase调度。

## 怎么操作（SOP骨架）

> execution.mode: 串联式 | 强保障：本SKILL.md由host层强制注入 | 弱保障：steps/scripts需agent主动读取，设计时假设可能没读到

- **Step 1** 初始化项目目录+project-state.md+project-state.html → `steps/step1.md`（创建四文件夹+state=init）
- **Step 2** 读project-state.md→按phase路由→完成后更新state.md+运行脚本生成state.html → `steps/step2.md`

### Phase路由

| Phase | 做什么 | 调用Skill | 产出 |
|:--|:--|:--|:--|
| 0 | 用户意图深问(Stage1)+子agent并发(Stage2:下载/DNA/decon-lite/赛道调研) | tool-download-webnovel/pop-dna-style/pop-research | 素材/各文件 |
| 1 | Seed创意+首章 | pop-fanqie-seed | 设计/创意.md+正文/ch001.txt |
| 2 | World世界构筑 | pop-fanqie-world | 设计/全书设定/（多文件） |
| 3 | Plot叙事白描 | pop-fanqie-plot | 设计/第一卷剧情/剧情白描.md |
| 3.5 | Character角色库 | pop-fanqie-character | 设计/角色库/角色库.md |
| 4 | Write正文渲染(**子agent**) | pop-fanqie-write | 正文/chXXX.txt |
| 5 | Review审核+沉淀 | pop-fanqie-review | 审核/review-chXXX.md |

Phase 0并发规则：下载先返回→再同时派发DNA+decon-lite，赛道调研第一优先级独立启动。Phase 5通过→phase4+ch+1，打回→phase4重写。

## 红线

1. **读取协议**——读取skill文件用`Get-Content -Encoding UTF8 -Raw`，Read工具有行数限制会截断丢内容
2. **project-state.md是唯一状态源**——所有phase切换以它为准，每次更新state.md必须同步运行脚本生成state.html
3. **Phase 0必须先深问再并发**——不完成Stage 1用户意图深问，不进入Stage 2
4. **pipeline只做路由不干活**——不写正文/不创意/不审核/不提取DNA
5. **Phase 4必须用子agent调write**——主agent只做路由，主agent执行write会导致skill读取不全+正文质量退化
6. **Phase 3.5 Character必须执行**——plot完成后必须经过character建角色库，跳过=角色设计丢失
7. **agent每次对话第一件事是读project-state.md**

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `SKILL.md` | 每次run强制注入 | SOP骨架+Phase路由表+红线 |
| `steps/step1.md` | 初始化时读取 | 项目目录初始化（四文件夹+downloads）+state.md/html生成 |
| `steps/step2.md` | 路由时读取 | Phase路由规则+state更新+脚本调用 |
| `scripts/generate-state-html.py` | 每次更新state.md后运行 | 读取state.md→生成project-state.html |
| `templates/project-state.html.tpl` | 脚本自动使用 | HTML可视化模板 |

## 版本

v3.3.0 | 2026-07-22 | 按Popwave Skill设计规范重写SKILL.md结构（≤100行），红线合并为7条含读取协议 → CHANGELOG.md
