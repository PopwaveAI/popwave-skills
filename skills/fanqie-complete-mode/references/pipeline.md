# 番茄完本计划 · 文件协议与 goal 契约

## 目录

```text
状态.md
立项/
  00-立项卡.md
  01-黄金开篇.md
人物/
剧情/
  00-卷爽点表.md
章纲/
  ch{NNN}-章纲.md
正文/
  ch{NNN}.txt
剧情日志/
  ch{NNN}.md
  全书日志.md
目标/
  spec.md
验收/
  verify.mjs
完本包/
```

目录名借雪花流的文件协议；内容、模板、字段全部由番茄四包定义，不读雪花内容模块。

## 状态总账

```text
mode: fanqie_complete
stage: trial | full
phase: 1-8
current_volume: N
current_chapter: N
word_count: N
goal_word_count: 150000 | 300000
last_confirmed_chapter: N
hook_type: A | B | C | D | E
payoff_form: 碾压 | 信息兑付 | 认可 | 关系兑付 | 整活兑付
paid_off_chapters: N
```

## 两条 goal

### 试读 goal

- 目标 3 万字，约 12-15 章。
- 验收：正文 ≥30000 字；章文件数=章日志数；phase ≥7；每章 ≥1800 字；`stop=false`。
- 完成出试读报告：字数、章数、黄金三章、钩子类型、问题、建议。

### 完本 goal

- 目标 15/30 万字。
- 验收：全书字数 ≥目标；章文件数=章日志数；phase 7/8；无空章。
- `stop`：距 `last_confirmed_chapter` 的成章数 ≥10 → 停等。
- 从试读进度继续；不重写已确认章。

## 阶段与门禁

| 阶段 | 技能 | 必读 | 产出 | 门禁 |
| --- | --- | --- | --- | --- |
| 赛道诊断 | fanqie-plan | genre-fit | 2-3 个赛道建议 | 30 万字可行性五问 |
| 规划 | fanqie-plan | golden-three | 立项卡、黄金开篇、spec、verifier | 前 300 字爆点、前 1/3 爽点 |
| 卷纲 | fanqie-plan | emotion-and-payoff | 卷爽点表 | 不得连续 3 章无爽点 |
| 章纲 | fanqie-plan | hook-and-reversal | 章纲 | 钩子五型、相邻不同型 |
| 正文 | fanqie-write | prose-rules | 正文 | 字数、章末钩子、承接四问 |
| 批末 | fanqie-review | quality-gate | 章日志、批次报告 | 四块报告齐全 |
| 完本 | fanqie-review | quality-gate | 完本包 | 字数、章数、日志、phase |

## goal.create

- 只在用户明确同意开始下一阶段时调用。
- 只创建 `planning`；不确认、不执行、不继续。
- 绑定当前 run 的 user/project/conversation；一个对话只能有一个活动目标。
- 创建失败（GOAL_ACTIVE / PROJECT_BUSY / 余额不足）原样告诉用户，不重试。
- 没有该工具时，给用户可发送的 `/goal` 指令。

## 恢复

- 每章落盘；`状态.md` 记录当前章与已确认章。
- 中断后从最后一章继续；不重复写已确认章。
- 连续 3 轮无推进，goal 置 `blocked`；等用户处理，不自行重启。
- 用户终止后不再自动续跑。
