# Step 2.3 - 正文写作调度

正文写作默认只调 `pop-writer-v3-create`。

## 正式/试写门

正文请求必须先判定 create 模式：

- `formal`：已读取 `pop-writer-v3-create/SKILL.md`、`steps/step-1-create.md`、`templates/创作-模板.md`，且 create 输入包齐全，章卡边界和微beat施工表通过。
- `draft`：create skill 已读取，但章级导演包、章卡边界、微beat施工表、案例消化、爽文审计、状态快照等关键输入有缺口。
- `trial`：未读取 create skill，或用户只要快速试写。

只有 `formal` 可以落入 `正文/` 并称为正式正文。`draft/trial` 必须在标题或回报中标明“草案/试写”，不得冒充正式 create。

## Create 输入包

- 当前 plot 章级施工卡：必须包含章卡边界、POV、scene、宏观剧情骨架、微beat施工表、主爽点、主角主动动作、可数收益/明确损失、爽点外显、系统/战斗节点、章末钩子、禁改项。
- 当前章节运行日志：必须是本章正文的直接依据。
- 幕级外部燃料台/案例消化摘要：本幕对应的可迁移结构、爽点证据、内容肌理。
- 爽文审计结果或施工卡字段：本章必须兑现的主角主动、可数收益、误判/认知差、章末追读。
- 当前状态快照：人物位置、资源、伤势、关系、威胁、未兑现承诺。
- 角色锚点切片：只包含本章登场角色的反应模式、说话方式、关系状态和本章功能；不得让 create 读取整份角色储备池。
- 设定账本：只提供本章会碰到的设定文件，但关键规则必须完整。
- 读者表达偏好：直白度、旁白/心理许可、环境描写长度、爽点外显强度和严肃文学偏移禁区。
- 文风DNA：按 plot 施工卡 `scene` 字段切片读取；深度修订不在此步做。
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
    - expert-writer
    - pop-writer-v3-create
  loaded_steps:
    - pop-writer-v3-create/SKILL.md
    - pop-writer-v3-create/steps/step-1-create.md
    - pop-writer-v3-create/templates/创作-模板.md
  required_inputs:
    present:
    missing:
```

若 `mode` 不是 `formal`，正文不得写入正式 `正文/`；如用户坚持写入，文件名或创作记录必须保留 `mode: draft|trial`。

## Revise 触发

只有这些情况才调 `pop-writer-v3-revise`：

- 用户明确说“修/润/改/重写”，且目标是产出修订稿。
- create 产出后用户不满意并指出方向。
- 正文存在明显硬伤，且用户允许修订。

## Review 触发

只有这些情况才调 `pop-writer-v3-review`：

- 用户明确说“审稿/检查/看看问题/像编辑一样读”。
- 用户关心 AI 味、爽不爽、bug、OOC、剧情是否好看。
- 用户要项目体检或判断问题来自 create/plot/world 哪一环。

review 只输出编辑诊断和处理建议，不直接改正文。若用户看完审稿意见后要求修改，再调 revise 或 create。

不要默认 create 后立刻 revise。写作专家是调度器，不是自动双层流水线。
