# CHANGELOG

## v6.0.1 | 2026-08-31

### review 三族合并，downstream 改指 pop-review

> **根因**：pop-qidian-review + pop-fanqie-review + test-review 合并为 pop-review，旧 3 skill 废弃删除。

- skill.json `pipeline.downstream`：`pop-qidian-review`→`pop-review`
- skill.json version 6.0.0→6.0.1

## v6.0.0 | 2026-08-24

### steps 四件全合入 SKILL.md 单文件精炼

> **根因**：实测 step 文件在当前 harness 从未被加载/Read（子agent注入链断在骨架层），SKILL.md 里的 step 引用形同虚设。参考 write/pipeline 改造模式，把 step 内容合入主文档。

**改动**：
- **steps/ 目录删除**：step-0-interactive / step-1-material / step-2-act / step-3-chapters 四件全部合入 SKILL.md 对应 Step 0-3
- **执行模式明确**：交互决策环节（Step 0 五轮决策、Step 2 阶段A候选确认）主agent直执；Step 1 Part B 素材收集外部搜索可派子agent（research purpose 天然适配只读通道，子agent搜索回报、主agent落盘）
- **内容精炼**：Step 0 五轮决策压缩为一张表（轮次/必答/底牌/动作/选项规则）；Step 2 阶段B四步链路保留全部业务逻辑（活跃层/燃料改造四式/白描必含项/3项自检/反拆分章/五问自检）；红线从9条收敛为4条（业务约束全部保留，就近内联到各Step）
- **模板保留**：卷纲.md四层结构、起承转合四段式模板、章锚点表4硬+3软全部内联；templates/ 与 references/ 保持外部文件不变
- skill.json version 5.2.0→6.0.0

---

## v5.2.0 | 2026-08-13

### skill.json 面向用户介绍 + 可调用专家标签 + 版本同步

**改动**：
- **skill.json**：description 改为面向用户介绍、tags 改为可调用专家标签
- **SKILL.md**：版本号同步至 v5.2.0
- **CHANGELOG.md**：新增本条版本记录

---

## v5.1.0 | 2026-08-13

### 新增全书卷级目录：主线广度先行

> **根因**：主线.md只有抽象的阶段推进链（阶段X→阶段Y），没有每卷的卷级落点。后卷只有方向没有目的地，写后卷时卷纲从零起、可能偏轨或透支后续爽点。story需"广度先行圈定，深度后置深化"。

**改动**：
- **step-1-material.md 新增P0-f全书卷级目录**：主线.md在阶段推进链基础上追加每卷的卷级目录（卷定位/主压力/主收益/卷末爽点/不抢的后续收益），附录在主线.md
- **广度先行深度递归**：卷级目录只给每卷一句话战略（广度），首卷深做到幕/章，后卷写到时递归深化；卷级目录禁止写成章级细节
- **不抢后续收益**：每卷标注"不抢的后续收益"列，防前置卷透支后续高潮爽点
- **SKILL.md更新**：主线.md输出描述+新增红线9广度先行·深度递归+版本
- skill.json version 5.0.0→5.1.0

## v5.0.0 | 2026-08-13

### 消费PRD方向句，自己展开主线

> **根因**：seed重构为极轻六要素立项引擎（v13.0.0），只产出立项/01-立项PRD.md，不再产出力量体系.md+动力引擎.md+主角设计.md+主线任务链.md。plot作为"剧情展开器"，输入从seed骨架文件改为PRD「起因/经过/结果」方向句+world全书设定+character角色库，自己展开主线。

**改动**：
- **输入改为PRD方向句**：消费立项/01-立项PRD.md「起因/经过/结果」方向句（故事怎么起/怎么发展/怎么收），替代原主角设计.md+主线任务链.md
- **新增主线展开**：plot自己从PRD「经过」方向句展开设计/主线.md（阶段推进链+敌人阶梯+因果链+跨卷伏笔），替代原主线任务链.md——step-1-material.md Part 0新增
- **主角信息从character消费**：设计/角色库/角色库.md（主角深度卡：行动偏好/爽感矛盾公式/核心欲望）+设计/金手指.md（金手指限制/赋能范围），替代主角设计.md
- **step文件同步**：step-0-interactive.md（前置条件+底牌消费改PRD方向句+角色库）、step-1-material.md（Part 0主线展开+Part A消费源改主线.md）、step-2-act.md（2A-a加载上下文改角色库+金手指+主线）
- **references同步**：开局设计原则.md+情感设计原则.md 的"主角设计.md"引用改为"设计/角色库/角色库.md（主角深度卡）"
- **红线更新**：新增第2条"主线从PRD经过方向句展开"红线，困难三层面"主角设计"改"金手指限制"
- **SKILL.md更新**：定位/输入/输出表/前置依赖/Step 1描述/速查表/版本号同步更新
- skill.json version 4.5.0→5.0.0
- 版本三处一致（SKILL.md + skill.json + CHANGELOG.md）

---

> 历史版本条目已归档：`_archive/changelog-history/pop-qidian-plot/CHANGELOG.md`（全量保留，本文件仅保留最近3个版本）
