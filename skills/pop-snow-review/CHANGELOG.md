# CHANGELOG

## v1.4.1 | 2026-09-04

### 章节日志接住 write 下放的交接 + 字数门禁由 review 自跑（配合 write v1.5.1）

每章账本收敛为一份（章节日志），不再与创作记录双写。三件事落地：

- **字数门禁迁入 review**：`scripts/word-count.ps1` 从 write 迁到本 skill，review 第 2 步 exec 自跑（纯汉字 2000-2500），stdout 原文进章节日志头部"字数"栏；write 彻底不承担字数检测、不自报字数。
- **章节日志模板对齐四模块**：`templates/chapter-card.tpl.md` 从旧白描卡结构（事件白描/关键数据/本章DNA）重写为 时间·地点·人物／本章剧情／这一章定了哪些事／这一章动了哪些线 四模块，去掉了 v1.3 白描卡残留与早前试点加的 `## write 接入` 节（用户判定过度设计）——write 交接信息（冲突标注/新增事实待核）由 review 在生成日志时自然并入"定了哪些事"。
- SKILL.md 第 2 步同步"review 自己跑字数门禁"，并明确 write 对话交接（冲突标注/新增事实待核）核验后并入"这一章定了哪些事"。

同步三件套：SKILL.md / skill.json（1.4.1）/ CHANGELOG；`templates/chapter-card.tpl.md` 重写；新增 `scripts/word-count.ps1`（迁自 write）。

## v1.4.0 | 2026-09-03

### 重构：review 收敛为"三件事"（章节验收+归档），砍掉庞大审核引擎

老板拍板："全部删掉重来，review 就两三个活"。SKILL.md 从四步审核引擎（正向符合性/正文质量/AI味15条/好看度4问/节奏物理量/六章型七节拍/番茄五卡口/范式判定 等）整体重写为极简三件事：

- **第1步 确认满意**：判断本章正文是否定稿；未定稿打回 write、不入库。
- **第2步 生成本章日志**：按定稿正文写 `章节日志/ch{NNN}.md`（时间地点人物／本章剧情／定了哪些事／动了哪些线）。
- **第3步 更新全书日志**：按本章日志 replace 为"只记活跃"，回收项落退出档案。

- 定位从"质量审核引擎"转向"**账本维护闸门**"：质量归 write，review 只负责把正文的剧情进度/人物状态记准、把全书日志更新到下一章可依赖的准。
- 保留防偏机制 v3 三条心法（只记活跃／世界规则不入全书日志／当前态不拆分）与役（章日志=事件源·只增不改，全书日志=当前态·replace，退出档案=归档·追加）。
- 批量回溯降为可选附注（存量逐章跑同一流程），不再单列 Reconstruct 大节。
- 同步三件套：SKILL.md 全量重写 / skill.json（version 1.4.0、displayName 章节验收归档、description）/ CHANGELOG。

## v1.3.0 | 2026-09-03

### 三文件沉淀层 · 防偏机制 v3 落地（单章日志/全书日志·只记活跃/退出档案）

经渲染《拆解昨日书》卷一 + 深渊主宰 ch001-005 滚动压测收敛，把"防偏机制 v3"并入 review 沉淀层：

- **双文件 → 三文件**：白描卡（=单章日志·事件源·只增不改）／状态快照（=全书日志·当前态·只记活跃·replace）／退出档案（=归档层·追加）。description/做什么/Step4/速查表全同步。
- **状态快照改"只记活跃"**：未回收钩子台账只列仍未回收的，回收即移除入退出档案（不再标"已回收"残留）；角色表只留活跃角色，退场落退出档案——快照"进得来出得去"，防随章节线性膨胀。
- **新增"世界规则/静态设定不入快照"红线**：力量体系/货币/地理/势力等静态设定在大纲·设定库·卷纲已存在，快照不重复载入，避免重复+双源打架。
- **新增模板** `templates/exit-archive.tpl.md`（已回收钩子/已退场角色/已完结线）；`templates/state-snapshot.tpl.md` 升级为只记活跃版。
- 根因：v1 把约束当"预设断言"，ch007"她自己换号叫念卿"实证预设会拦错 → 确立"约束是快照、随正文 replace、不预设未来"，已写入禁止漂移注释。
- 同步 skill.json（version 1.3.0 / description）。

## v1.2.0 | 2026-08-31

### 意识层 + wiki 站取源

- 新增「心智前置·意识层」节（Know-Gap/Pack/Worth/Deepen + 取材预算硬上限），贯穿本 skill 与全流程。
- wiki 取源统一走网站 https://wiki.popwave.cn（替代本地 D:\popwave-wiki\docs 镜像 / sync.ps1）。

## v1.1.2 | 2026-08-31

### 去 AI 味 + 文档瘦身

- 身份词"章节审核引擎"→"章节审核"，description 精简
- 引语与版本节版本历史解耦，仅留当前版本 + 指向 CHANGELOG
- 正文"改编引擎"→"改编机制"
- 同步 skill.json（version/displayName/description）

## v1.1.1 | 2026-08-31

### 更名：pop-review → pop-snow-review

- 雪花流家族徽记：统一管线 8 件 skill 加 snow 中间名，与旧族 pop-fanqie-*/pop-qidian-* 区分（老板 2026-08-31 拍板）；test 系列 5 件（adapt/lite/plot/research/write）同批删除退役（备份 temp/_backup-test-20260831/）
- name/version/全仓引用同步；功能零变化

## v1.1.0 | 2026-08-31

### 统一管线对齐

- 对照物表加入「统一管线」行：本章章纲（pop-outline 产出）作为 Step 1 正向符合性基准，旧三范式保留标注「旧管线」
- 字数脚本路径 `pop-qidian-write/scripts/word-count.ps1` → `pop-write/scripts/word-count.ps1`（2d + 速查表两处）
- skill.json version 1.0.0→1.1.0

## v1.0.0 | 2026-08-31

### 三族合并首版：pop-qidian-review + pop-fanqie-review + test-review → pop-review

> **根因**：三族 review 骨架同构（四步审核+双文件沉淀+子agent审计/主agent落盘+reconstruct采样策略逐字一致），AI味检测体系（15项patterns+疲劳词3级+结构性4项）三件完全重复维护；差异全部收为范式门禁分支。对齐 pop-world/pop-character 合并范式（老板 2026-08-31 拍板的第二轮合并路线图第一棒）。

**公共内核（单点维护）**：Step 0 范式判定 / 四步审核骨架（正向符合性 1a-1e→正文质量 2a-2d→反向充足性 4 维度→沉淀双文件）/ AI味检测全套 / 对话质量6项 / 好看度4问 / 字数脚本实测 / 双文件职责（存"发生"只增不改 + 存"状态"replace）/ 执行模式（Step1-3 子agent审计+Step4 主agent落盘）/ reconstruct 批量回溯（采样策略统一+>8章拆批）/ PASS-REJECT 明确判定。

**范式分支**：
- 番茄追加五项卡口：1e' 番茄底线检查（含合规底线）/ 1f 6章型7节拍对齐 / 1g 战斗可写性 / 1h 主角主动性（连续2章C级=REJECT）/ 1i 多视角覆盖；双文件路径=审核/剧情白描流水账.md(append)+审核/状态快照.md(replace)
- test 前置双门禁：第0审配方符合性（<90%打回）+ 第0.5审X符合性（改编专属）；白描卡追加本章DNA执行包节
- 起点追加：按需更新库文件（设定库/角色库/卷纲/写作燃料）

**模板**：templates/chapter-card.tpl.md（起点/test 通用，新增 test 可选 DNA执行包节）+ templates/state-snapshot.tpl.md（三族通用；番茄流水账格式保持 SKILL.md 内联）。

**废弃**：pop-qidian-review(v4.1.0)、pop-fanqie-review(v5.0.0)、test-review(v7.0.0) 3 件 skill 删除；旧版历史见 `_archive/changelog-history/`。
