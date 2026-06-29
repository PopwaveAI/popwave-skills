# Step 2：路由执行与轻写作调度

## 1. 路由到子 skill

非正文写作请求直接路由：

1. 完整读取目标 `SKILL.md`。
2. 按目标 skill 的说明执行。
3. 完成后进入 `step-3-reflect.md`。

## 2. 写正文：轻调度

当路由决定为 `create` 时，执行以下流程。

### 2.1 定位当前章

从用户请求或项目总控确定章号：

- 用户说“写第 7 章” → ch007。
- 用户说“继续/下一章” → 从项目总控或正文目录推断下一章。

### 2.2 定位单元材料

找到当前章所在单元：

- `卷纲/幕NNN-{名称}.md`
- `卷纲/运行/幕NNN-{名称}-运行日志.md`
- `卷纲/运行/幕NNN-{名称}-设定账本.md`
- `活记忆/活记忆.yaml`
- `正文/ch{上一章}.md`
- `写作资产/文风库/{书名}.md`

缺少任一关键材料：

| 缺少 | 处理 |
|:-----|:-----|
| 运行日志 | 路由 `pop-writer-v3-plot` |
| 设定账本 | 路由 `pop-writer-v3-plot` 或 `pop-writer-v3-arc` |
| 单元卡 | 路由 `pop-writer-v3-plot` |
| 文风 DNA | 路由 seed 的文风 DNA 步骤或提示用户补充 |

### 2.3 读取 create

```powershell
Get-Content -Encoding UTF8 -Raw 'skills/pop-writer-v3-create/SKILL.md'
```

### 2.4 装配 create 输入

完整读取：

- 当前章运行日志段落。
- 单元卡当前章导演指令表对应行。
- 设定账本全文。
- 被单元卡指针引用的硬设定文件。
- 上章末尾。
- 活记忆。
- 文风 DNA。

装配为 create 输入包，不再生成旧 `director_intent`。

### 2.5 调度 create

调用 `pop-writer-v3-create` 完成正文。

create 输出：

- 正文。
- `create_record`。

### 2.6 用户不满意时

如果用户要求修改，路由 `pop-writer-v3-revise`。不要在本 skill 内部修正文。

## 3. 落盘和状态更新

写正文成功后，读取 `steps/step-2-5-memory-commit.md` 执行落盘和活记忆更新。

## 4. 单元结束检查

如果当前章是单元最后一章：

1. 提示触发 `pop-writer-v3-arc`。
2. 如果 Pop 流程要求自动触发，则完整读取 arc `SKILL.md` 并执行。

## 5. 回滚

用户要求回滚时，先确认影响范围：

- 将删除哪些正文。
- 将移除哪些活记忆 events。
- 是否需要重跑 arc。

确认后再执行，不自动破坏文件。
