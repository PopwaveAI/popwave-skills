# CHANGELOG

## v4.3.0 | 2026-08-27

### 状态源统一为 状态.md，html 降级为展示；日常路由上移专家提示词

**背景**：六专家收敛——状态文件统一为「小而机器可读的状态片段」，人看展示面板（html）降级为可选按需导出。起点此前把 STATE 与整张 Phase 路线图同文件内嵌 `项目总控.html`，每次对话全量 Read 吃上下文；且 Phase 推进/章节授权的状态读写源不统一。

**改动**：
- **状态源拆分**：从 `项目总控.html` 拆出薄机器 `状态.md`（mode/phase/current_chapter/next_step/书目/就绪态/最近产出），`templates/状态.md` 为新模板；`项目总控.html` 降级为仅供老板查看的展示面板，由 状态.md 套值按需导出，**agent 不再读 html**
- **路由上移专家提示词**：Phase 路线图不再作机器路由源，日常路由由专家提示词阶段地图承载（读 状态.md 状态片段→按阶段地图选 skill→灵活调度）
- **更新协议改名**：`references/html-update-protocol.md` → `references/状态更新协议.md`，字段表从 STATE 标记改为 状态.md 字段；phase 推进改为由对应 skill（seed/world/character/plot/write/review）完成后更新 状态.md，pipeline 只在初始化/导入时碰它
- **write/review 挂钩**：write 章节授权读源、review 输入/授权/重建均从 `项目总控.html STATE 区` → `状态.md`
- 新增红线4「状态源」
- **skill.json**：4.0.0→4.3.0，description 同步

---

## v4.0.0 | 2026-08-24

### 一次性安装器化：路由外置到项目总控.html，删除常驻调度职责

**背景**：70 run 实测 pipeline 每次注入 ~7KB 但 90% 是静态路由表；两两成宝 57 章里 pipeline 的"每次路由"职责从未真正运转（用户直接说写正文，agent 直接干活）。路由表对每个项目是常量，不该占每次注入的注意力预算。

**改动**：
- **SKILL.md 重写**（12681→约3800字符）：职责收敛为一次性安装（新建目录+总控.html）+一次性导入（资产清点/归位映射表/缺口分析/落地Phase/补跑调度）+html格式协议指针；step0-import/step1 全量合入（精炼压缩）后**删除 steps/ 目录**
- **路由外置**：Phase 调度表（执行skill+前置门禁+产出）写入 `templates/项目总控.html` 新增「03.5 Phase 路线图」节——总控从状态显示器升级为状态+路由表合一；html 是项目内文件，Read 时才加载，不占注入预算
- **触发词收缩**：删"管线/pipeline/继续写/下一步"（日常路由职责已下放），保留"初始化/新建/导入/续写/迁移"
- **日常路由协议**：用户说"继续写/下一步"时主agent直接读总控.html（STATE+路线图）路由，不经 pipeline
- **write/review 挂钩**：write 派发指令硬清单加第0项（章节授权：读总控STATE确认phase/chapter，不一致不开工）；review 输入清单加总控.html；write 主agent职责加"验收通过后更新总控"
- **skill.json**：3.16.0→4.0.0，description/activation 同步

**注意力账**：写正文/审核轮的 pipeline 注入成本 12.7KB→0KB（路由信息随总控.html按需Read）；pipeline 自身触发面从"每次写作对话"缩到"建项目/导入"两个一次性场景。

---

## v3.16.0 | 2026-08-24

### Phase 5 改派发子agent执行 write；红线4翻案

**背景**：两两成宝实测事故链——主 agent 直写正文（重任务）→会话膨胀 7.8MB→compaction 崩溃→expert 配置丢失回退 unrestricted→skill 零注入。子 agent 链路实测已通（SKILL.md 全文注入+主动 Read），write v4.2.0 SOP 全内联后天然适配。

**改动**：
- **Phase 5 调度**：主agent直读执行→**派发子agent执行**；主agent职责收窄为：核对输入路径→按 write SKILL.md「派发指令硬清单」组装指令→派发→验收门禁
- **验收门禁**：查文件系统不信口头——正文≥1800字+白描卡新建+快照 mtime 更新，缺任一幂等重派（先查半成品防覆盖）
- **红线4翻案**：「主agent直接执行所有step、禁止派发子agent」→「分环执行模式」：Phase 1-4 设计层主agent直接执行；Phase 5 重任务必须派发子agent。原约束的前提（子agent拿不到skill）已被实测推翻
- **skill.json**：3.15.0→3.16.0

**配套**：write 同步升 v4.2.0（新增「执行模式」节：角色分工+派发指令硬清单+验收门禁）。

---

## v3.15.0 | 2026-08-18

### step2 路由循环合入 SKILL.md，删除 step2.md

**改动**：
- **SKILL.md**：新增「路由循环」节（读总控STATE→对照Phase调度表路由→按协议更新html），Phase调度表与执行协议合入，每次对话零跳转自包含
- **references/html-update-protocol.md**（新增）：HTML 更新协议单源化——STATE字段/Phase ID对照表/badge表从 step0/step1/step2 三处归一
- **steps/step2.md**：删除，step0/step1 指针改为指向 SKILL.md「路由循环」节
- skill.json version 3.14.1→3.15.0，版本三处一致

---

## v3.14.1 | 2026-08-18

### step2 调度卡化：砍子skill红线/SOP复述段

**改动**：
- **step2.md**：412行复述段改为"更新协议+门禁+Phase调度卡"结构，调度卡只含四要素（目标skill+step、输入、产出、完成后动作）
- 红线与SOP细节一律读子skill SKILL.md，此处不复述（防双源漂移）
- 路由表去版本号（版本正源=CHANGELOG）
- skill.json version 3.14.0→3.14.1，版本三处一致

---

## v3.14.0 | 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v3.14.0
- **CHANGELOG.md**：新增本条版本记录

---

## v3.13.2 | 2026-08-13

### 势力边界收敛版本同步

**背景**：world v5.2.0势力边界收敛（势力人物.md删全书配角，只做势力组织+代表人物一句话锚定），character同步为全部"人"的唯一产出方。

**改动**：
- **SKILL.md Phase 表版本同步**：world v5.1.0→v5.2.0、character v2.1.0→v2.2.0
- 势力=棋盘（world·组织），角色=棋子（character·个体），消灭两层皮

## v3.13.1 | 2026-08-13

### 广度先行三补丁：world/character/plot 版本同步

**背景**：老板定调"广度先行圈定，深度后置深化"——三个skill都先处理全书格局（广度），再深做第一卷（深度），不排除后卷追加世界观/剧情。pipeline 同步 Phase 路由表版本号。

**改动**：
- **SKILL.md Phase 表版本同步**：world v5.0.0→v5.1.0（W1拆两层：W1a全书世界格局+W1b首卷舞台）、character v2.0.0→v2.1.0（新增全书角色版图前置）、plot v5.0.0→v5.1.0（新增全书卷级目录）
- 三个skill均新增"广度先行·深度递归"红线：先圈定全书格局，再深做首卷；后卷递归拓展（追加非重写）

---

> 历史版本条目已归档：`_archive/changelog-history/pop-qidian-pipeline/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
