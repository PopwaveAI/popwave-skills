---
name: pop-fanqie-pipeline
description: "当用户说'初始化项目/管线总控/番茄pipeline/导入/续写'时启用。Phase 0→5全链路调度，项目空间标准化，project-state状态可视化。"
---

# pop-fanqie-pipeline

> 番茄管线总控。Phase 0→5全链路调度，pipeline只做路由不干活。v3.13.0：step2 路由循环合入 SKILL.md（每次对话零跳转自包含），删除step2.md。完整版本历史见 [CHANGELOG.md](CHANGELOG.md)。

## 做什么

输入：项目名或当前项目目录。mode=fresh（从零开始）/import（导入已有设定）/resume（续写已有正文）
输出：标准化目录结构（素材/设计[全书设定/角色库/第一卷剧情]/正文/审核）+ project-state.md（agent读，含mode字段）+ project-state.html（人看）

pipeline不写正文、不创意、不审核——只负责把agent指向正确的phase和skill。所有下游skill由pipeline按phase调度。

## 怎么操作（SOP骨架）

> execution.mode: 串联式 | 强保障：本SKILL.md由host层强制注入 | 弱保障：steps/scripts需agent主动读取，设计时假设可能没读到

- **Step 0** 导入/续写模式 → `steps/step0-import.md`（检测已有资产→缺口分析→落地Phase→状态重建→正文反推。用户说"导入/续写/已有"或目录已有文件时触发）
- **Step 1** 初始化项目目录+project-state.md+project-state.html → `steps/step1.md`（创建四文件夹+state=init。**如果检测到已有文件→重定向到Step 0**）
- **Step 2** 路由循环（每次对话）→ **直接执行本文件下方「路由循环」节**

### 路由循环（每次对话开始时）

1. 读 `project-state.md`，提取 phase（决定路由）、current_chapter（Write阶段当前章）、底牌就绪（Phase 0是否完成）
2. 对照下方「Phase调度表」路由到对应Phase执行
3. Phase完成后按「state更新方法」更新 state.md 并运行脚本生成 html，再回到第1步判断下一步

### Phase调度表

| Phase | 调用Skill | 前置检查 | 产出 | 完成后更新 |
|:--|:--|:--|:--|:--|
| init | （执行Step 1初始化） | — | 四文件夹+state文件 | phase→phase0，进Phase 0 |
| 0 Stage1 | 主agent用户意图深问（四层递进：赛道方向必答→标签/元素→参考书群→现有设定，后三层可跳过） | phase=phase0 | 素材/用户意图.md | 进Stage2 |
| 0 Stage2 | 子agent并发：下载参考书（用户给书名+无本地文件）/笔触DNA提取（已下载）/decon-lite拆书（力量体系参考书+已下载）/赛道定位调研（必有） | Stage1完成 | 素材/downloads/{书名}.txt+文风锚定.md+decon-lite-{书名}.md+赛道调研.md | phase→phase1 |
| 1 | pop-fanqie-seed | 用户意图已落盘（或明确跳过）+赛道调研已落盘（如有） | 设计/创意.md+正文/ch001.txt | phase→phase2、current_chapter=ch001、创意摘要填seed产出 |
| 2 | pop-fanqie-world | 设计/创意.md+正文/ch001.txt 存在 | 设计/全书设定/（力量体系.md+地图.md+势力.md+危机.md+各卷切片.md+全书配角.md） | phase→phase3 |
| 3 | pop-fanqie-plot | 设计/全书设定/ 存在 | 设计/第一卷剧情/剧情白描.md | phase→phase3.5 |
| 3.5 | pop-fanqie-character | 剧情白描.md存在（含分幕出场角色清单） | 设计/角色库/角色库.md（消费分幕出场清单+势力.md敌人梯度+创意主角轮廓） | phase→phase4、current_chapter=ch002 |
| 4 | pop-fanqie-write（**必须子agent**） | 剧情白描.md+角色库.md 存在 | 正文/chXXX.txt（写current_chapter指定章） | phase→phase5 |
| 5 | pop-fanqie-review | 正文/chXXX.txt 存在 | 审核/剧情白描流水账.md（append白描卡）+审核/状态快照.md（replace），结论对话内输出 | 通过→phase4+ch{NNN+1}；打回→phase4重写本章 |

> Phase 0并发规则：下载先返回→再同时派发DNA+decon-lite，赛道调研第一优先级独立启动。
> Phase 4子agent指令模板：你扮演 pop-fanqie-write，读取 skills/pop-fanqie-write/SKILL.md 了解完整SOP。项目目录：{projectDir}。当前章节：{current_chapter}。按SOP执行：加载输入→选章型→写正文→字数自检→落盘。注意：必须加载设计/角色库/角色库.md，战斗/升级场景必须使用DNA面板格式。

### state更新方法（每次Phase完成后）

**1. 更新 project-state.md**（SearchReplace）：①`phase:` 行 ②`current_chapter:` 行 ③`更新：` 行→当前时间 ④阶段完成情况→勾选完成的phase ⑤底牌就绪区块→更新状态 ⑥创意摘要→填写seed产出 ⑦最近产出表→追加新行

**2. 生成 project-state.html**（每次更新state.md后必须同步）：

```bash
python skills/pop-fanqie-pipeline/scripts/generate-state-html.py {projectDir}/project-state.md
```

脚本自动解析state.md字段→替换模板占位符→同目录生成state.html（下一步文案由脚本内置映射自动生成）。**禁止手动写HTML**。

## 📦 可调度 Skill 清单（素材表）

> 本 pipeline 整个专家入口与调度器，可调度的子 skill 总清单如下（与 `skill.json` 的 `skills` 数组一致）。这些 skill 按 Phase 调度表调度，**部分 skill 会被其他专家复用**（如 `pop-dna-style` / `pop-research` / `tool-download-webnovel`）。

| Skill | 定位 | 何时调用 |
|:--|:--|:--|
| `pop-fanqie-seed` | 种子创意+首章 | Phase 1 |
| `pop-fanqie-world` | 世界构筑（全书设定） | Phase 2 |
| `pop-fanqie-plot` | 剧情白描 | Phase 3 |
| `pop-fanqie-character` | 角色库 | Phase 3.5 |
| `pop-fanqie-write` | 正文渲染 | Phase 4 |
| `pop-fanqie-review` | 审核+沉淀 | Phase 5 |
| `pop-dna-style` | 文风综合重构 | Phase 0 |
| `pop-research` | 赛道调研/decon-lite/采风 | Phase 0 |
| `tool-download-webnovel` | 下载对标书 | Phase 0 |

## 🚪 首次对话引导（onboarding）

> 用户第一次触发番茄网文专家（无任何写作项目、非续写场景）时，**先输出 `references/onboarding-guide.md` 的引导语内容**给用户建立认知，再进入 Step 0 意图深问。
>
> 展示方式：在回复中**直接粘贴 `references/onboarding-guide.md` 全文**（声明本次为功能介绍+引导、未执行 skill 任务），用 1-2 句口头补充"报书号+想法就开始"。若用户已明确要开做，可跳过引导直接干活。

## 红线

1. **读取协议**——读取skill文件用`Get-Content -Encoding UTF8 -Raw`，Read工具有行数限制会截断丢内容
2. **project-state.md是唯一状态源**——所有phase切换以它为准，每次更新state.md必须同步运行脚本生成state.html
3. **Phase 0必须先深问再并发**——不完成Stage 1用户意图深问，不进入Stage 2
4. **pipeline只做路由不干活**——不写正文/不创意/不审核/不提取DNA
5. **Phase 4必须用子agent调write**——主agent只做路由，主agent执行write会导致skill读取不全+正文质量退化
6. **Phase 3.5 Character必须执行**——plot完成后必须经过character建角色库，跳过=角色设计丢失
7. **agent每次对话第一件事是读project-state.md**
8. **导入/续写模式不可跳过资产扫描**——用户说"导入/续写/已有"时必须走Step 0（资产扫描→缺口分析→落地Phase决策→用户确认），禁止直接凭空设置phase

## 速查表

| 文件 | 读取时机 | 核心内容 |
|:--|:--|:--|
| `SKILL.md` | 每次run强制注入 | SOP骨架+路由循环+Phase调度表+state更新方法+红线 |
| `steps/step0-import.md` | 用户说"导入/续写/已有"或检测到已有文件时 | 资产扫描→缺口分析→落地Phase→状态重建→正文反推 |
| `steps/step1.md` | 初始化时读取（无已有文件） | 项目目录初始化（四文件夹+downloads）+state.md/html生成 |
| `scripts/generate-state-html.py` | 每次更新state.md后运行 | 读取state.md→生成project-state.html |
| `templates/project-state.html.tpl` | 脚本自动使用 | HTML可视化模板 |
| `references/onboarding-guide.md` | 用户第一次触发（首次对话引导）时 | C端口吻引导语——「🚪 首次对话引导」区块强触发输出全文 |
| `references/import-structures.md` | 导入/续写模式 step0-import 0b-2 环节 | 16个标准文件的内容分节结构+转换方式（导入转换视角，结构正源在各子skill step） |

## 🗺️ 知识地图（reference 读取索引）

> pipeline 有 2 个 reference，均为场景触发式（首次对话引导/导入结构转换），无需分级。**看就记住，别读全文**。

| 参考 | 级别 | 什么时候必须读（触发条件） |
|:--|:--|:--|
| `references/onboarding-guide.md` | 🔴强触发 | **用户第一次触发番茄专家时必读**——SKILL.md「首次对话引导」区块声明输出全文 |
| `references/import-structures.md` | 🟡场景触发 | 导入/续写模式 step0-import 0b-2 环节（16个标准文件结构转换） |

## 版本

v3.13.0 | 2026-08-18
- **step2 路由循环合入 SKILL.md**：路由分流/state更新/脚本调用全部上提，每次对话零跳转自包含；Phase调度表合并前置检查+完成后更新两列；下一步文案映射表删除（脚本内置单源）；知识地图补import-structures条目
- 删除 steps/step2.md
v3.12.1 | 2026-08-18 | step0-import 结构表下沉 → [CHANGELOG.md](CHANGELOG.md)
