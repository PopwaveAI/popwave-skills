# Step 2.3 - 正文写作调度

正文写作默认只调 `pop-novel-create`。

## 正式/试写门

正文请求必须先判定 create 模式：

- `formal`：已读取 `pop-novel-create/SKILL.md`、`steps/step-1-create.md`、`templates/创作-模板.md`，且 create 输入包齐全，章卡边界和微beat施工表通过。
- `draft`：create skill 已读取，但章级导演包、章卡边界、微beat施工表、案例消化、爽文审计、状态快照等关键输入有缺口。
- `trial`：未读取 create skill，或用户只要快速试写。

只有 `formal` 可以落入 `正文/` 并称为正式正文。`draft/trial` 必须在标题或回报中标明“草案/试写”，不得冒充正式 create。

## Create 输入包

- 商业网文目标函数：当前项目的目标读者、主爽文引擎、当章读者奖励、严肃文学偏移禁区；没有这项只能 draft，不能指望文风DNA补救剧情目标。
- 当前 plot 章级施工卡：必须包含章卡边界、POV、scene、宏观剧情骨架、微beat施工表、主爽点、主角主动动作、可数收益/明确损失、爽点外显、系统/战斗节点、章末钩子、禁改项。
- 当前章节运行日志：必须是本章正文的直接依据。
- 幕级外部燃料台/案例消化摘要：本幕对应的可迁移结构、爽点证据、内容肌理。
- 爽文审计结果或施工卡字段：本章必须兑现的主角主动、可数收益、误判/认知差、章末追读。
- 当前状态快照：人物位置、资源、伤势、关系、威胁、未兑现承诺。
- 角色锚点切片：只包含本章登场角色的反应模式、说话方式、关系状态和本章功能；不得让 create 读取整份角色储备池。
- 设定账本：只提供本章会碰到的设定文件，但关键规则必须完整。
- 读者表达偏好：直白度、旁白/心理许可、环境描写长度、爽点外显强度和严肃文学偏移禁区。
- 文风DNA：写正文前必须用 exec（Get-Content -Raw）读取全文，禁止用 Read 工具读取。调度 create/revise 时文风DNA必须全文注入，禁止摘要/压缩传递。详见 create step-1 文风DNA全文读取协议。
- review 下一章修正规则：若存在最近一次 review 报告，读取“下一章修正规则/处理队列”并传给 create。
- 上章末尾：用于衔接开场。

关键对白方向、场景锚点是可选增强，缺失不得导致 create 降级。缺 plot 章级施工卡、章卡边界或微beat施工表时，create 只能产出“降级草案”。如果用户要正式正文，先回 plot 补章级施工卡，不要让 create 临时重构剧情。

## 章卡边界硬门

- create 只能写当前章施工卡允许的内容。
- 不得把下一章的坐标、战斗、揭示、结算或情绪兑现提前吞并。
- 如果正文自然滑到下一章，必须在本章主动钩子处停下，并在创作记录里写 `chapter_boundary_check.swallowed_next_chapter: false`。
- 如果已经吞并下一章，不能标记 formal，必须拆分或回报失败。

## Create 执行凭证

调 create 时必须要求正文创作记录写入：

```yaml
execution:
  mode:
  loaded_skills:
    - pop-novel
    - pop-novel-create
  loaded_steps:
    - pop-novel-create/SKILL.md
    - pop-novel-create/steps/step-1-create.md
    - pop-novel-create/templates/创作-模板.md
  required_inputs:
    present:
    missing:
```

若 `mode` 不是 `formal`，正文不得写入正式 `正文/`；如用户坚持写入，文件名或创作记录必须保留 `mode: draft|trial`。

## Revise 触发

只有这些情况才调 `pop-novel-revise`：

- 用户明确说“修/润/改/重写”，且目标是产出修订稿。
- create 产出后用户不满意并指出方向。
- 正文存在明显硬伤，且用户允许修订。

revise 不能只做语言润色。凡是涉及小说内容的修改，都要检查是否削弱了主角主动性、收益兑现、围观反馈、压迫解除、打脸强度和追读钩子；如果削弱，必须保留或补回。

## Review 触发

只有这些情况才调 `pop-novel-review`：

- 用户明确说“审稿/检查/看看问题/像编辑一样读”。
- 用户关心 AI 味、爽不爽、bug、OOC、剧情是否好看。
- 用户要项目体检或判断问题来自 create/plot/world 哪一环。

review 只输出编辑诊断和处理建议，不直接改正文。若用户看完审稿意见后要求修改，再调 revise 或 create。

不要默认 create 后立刻 revise。写作专家是调度器，不是自动双层流水线。

## 文风DNA全文传递红线

调 create 或 revise 写正文时，文风DNA必须全文注入到执行 agent 的上下文，禁止任何形式的摘要/压缩/要点化传递。

**为什么**：实测发现主 agent 读取文风DNA全文后，通过 sessions_spawn 传给子 agent 时压缩成 6 条抽象 bullet points（784-1488 chars），丢弃全部 ≥500 字原文摘录。子 agent 知道"嗅觉优先于视觉"这个规则，但看不到任何一段示范这个规则的原著笔触。文风DNA纯抽象描述对子 agent 毫无意义。

**要求**：
- 调度 create/revise 前，主 agent 必须先用 exec（Get-Content -Raw）读取文风DNA全文。
- 调度子 agent 时，文风DNA全文必须作为 task 内容的一部分注入，不得压缩成要点。
- 如果上下文窗口确实装不下文风DNA全文，优先压缩其他材料（设定账本、运行日志、外部燃料台），文风DNA全文最后压缩。
- 禁止用"文风DNA要点"、"文风DNA关键特征"、"文风DNA继承特征"等摘要形式替代全文。
- **笔触 vs 内容**：传给子 agent 的 task 里，文风相关指令只描述笔触（句式节奏/感官顺序/叙事距离/段落呼吸/对话引导），禁止描述内容（战术思维/战斗复盘/击杀余韵/剧情模板）。禁止把文风DNA原文摘录里的剧情设计提取为创作要求。
