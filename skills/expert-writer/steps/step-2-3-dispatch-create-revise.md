# Step 2.3 - 正文写作调度

正文写作默认只调 `pop-writer-v3-create`。

## 正式/试写门

正文请求必须先判定 create 模式：

- `formal`：已读取 `pop-writer-v3-create/SKILL.md`、`steps/step-1-create.md`、`templates/创作-模板.md`，且 create 输入包齐全。
- `draft`：create skill 已读取，但章级导演包、案例消化、爽文审计、状态快照等关键输入有缺口。
- `trial`：未读取 create skill，或用户只要快速试写。

只有 `formal` 可以落入 `正文/` 并称为正式正文。`draft/trial` 必须在标题或回报中标明“草案/试写”，不得冒充正式 create。

## Create 输入包

- 当前 plot 章级施工卡：必须包含 POV、scene、剧情骨架、主爽点、主角主动动作、可数收益/明确损失、爽点外显、系统/战斗节点、章末钩子、禁改项。
- 当前章节运行日志：必须是本章正文的直接依据。
- 幕级外部燃料台/案例消化摘要：本幕对应的可迁移结构、爽点证据、内容肌理。
- 爽文审计结果或施工卡字段：本章必须兑现的主角主动、可数收益、误判/认知差、章末追读。
- 当前状态快照：人物位置、资源、伤势、关系、威胁、未兑现承诺。
- 角色锚点切片：只包含本章登场角色的反应模式、说话方式、关系状态和本章功能；不得让 create 读取整份角色储备池。
- 设定账本：只提供本章会碰到的设定文件，但关键规则必须完整。
- 文风DNA：按 plot 施工卡 `scene` 字段切片读取；深度修订不在此步做。
- 上章末尾：用于衔接开场。

关键对白方向、场景锚点是可选增强，缺失不得导致 create 降级。缺 plot 章级施工卡时，create 只能产出“降级草案”。如果用户要正式正文，先回 plot 补章级施工卡，不要让 create 临时重构剧情。

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

- 用户明确说“修/润/改/审/重写”。
- create 产出后用户不满意并指出方向。
- 正文存在明显硬伤，且用户允许修订。

不要默认 create 后立刻 revise。写作专家是调度器，不是自动双层流水线。
